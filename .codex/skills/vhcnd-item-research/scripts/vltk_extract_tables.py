#!/usr/bin/env python3
"""Extract and convert VLTK/JX XPack PAK tables and loose legacy text.

Designed for SwordOnline/JX source trees where Client/data/*.pak uses the
XPackFile.cpp format and text tables are GBK or TCVN3 legacy Vietnamese.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_VIRTUAL_PATHS = [
    r"\settings\item\helm.txt",
    r"\settings\item\armor.txt",
    r"\settings\item\meleeweapon.txt",
    r"\settings\item\rangeweapon.txt",
    r"\settings\item\horse.txt",
    r"\settings\item\boot.txt",
    r"\settings\item\belt.txt",
    r"\settings\item\cuff.txt",
    r"\settings\item\amulet.txt",
    r"\settings\item\ring.txt",
    r"\settings\item\pendant.txt",
    r"\settings\item\magicattrib.txt",
    r"\settings\item\GoldItem.txt",
    r"\settings\MagicDesc.ini",
    r"\settings\Skills.txt",
    r"\settings\300Skills.txt",
    r"\settings\RankSetting.txt",
    r"\script\skill\gaibang.lua",
    r"\script\skill\shaolin.lua",
    r"\script\skill\tianwang.lua",
    r"\script\skill\wudu.lua",
    r"\script\skill\tangmen.lua",
]

TEXT_SUFFIXES = {".txt", ".ini", ".lua", ".cfg"}
UCL_C = r'''
#include <stdio.h>
#include <stdlib.h>
#include "ucl/ucl.h"
int main(int argc, char **argv) {
  if (argc != 4) { fprintf(stderr, "usage: %s in out out_size\n", argv[0]); return 2; }
  FILE *fi = fopen(argv[1], "rb"); if (!fi) { perror("open in"); return 1; }
  fseek(fi, 0, SEEK_END); long in_size = ftell(fi); fseek(fi, 0, SEEK_SET);
  unsigned char *in = (unsigned char*)malloc(in_size); if (!in) return 1;
  if (fread(in, 1, in_size, fi) != (size_t)in_size) return 1; fclose(fi);
  unsigned long out_size = strtoul(argv[3], NULL, 0);
  unsigned char *out = (unsigned char*)malloc(out_size); if (!out) return 1;
  ucl_uint dest_len = out_size;
  int r = ucl_nrv2b_decompress_8(in, (ucl_uint)in_size, out, &dest_len, NULL);
  if (r != UCL_E_OK || dest_len != out_size) {
    fprintf(stderr, "decompress failed r=%d dest=%lu expected=%lu\n", r, (unsigned long)dest_len, out_size);
    return 3;
  }
  FILE *fo = fopen(argv[2], "wb"); if (!fo) { perror("open out"); return 1; }
  fwrite(out, 1, out_size, fo); fclose(fo);
  return 0;
}
'''

@dataclass
class PakRecord:
    pak: Path
    index: int
    offset: int
    size: int
    packed_size: int
    method: int


def file_name_to_id(path: str) -> int:
    value = 0
    for index, byte in enumerate(path.encode("ascii"), start=1):
        if 65 <= byte <= 90:
            byte += 32
        value = (((value + index * byte) % 0x8000000B) * 0xFFFFFFEF) & 0xFFFFFFFF
    return (value ^ 0x12345678) & 0xFFFFFFFF


def package_order(client_dir: Path) -> list[Path]:
    data_dir = client_dir / "data"
    order: list[str] = []
    package_ini = client_dir / "package.ini"
    if package_ini.exists():
        for raw in package_ini.read_text(errors="ignore").splitlines():
            line = raw.strip()
            if "=" in line and line.split("=", 1)[0].isdigit():
                order.append(line.split("=", 1)[1].strip())
    for pak in sorted(data_dir.glob("*.pak")):
        if pak.name not in order:
            order.append(pak.name)
    return [data_dir / name for name in order if (data_dir / name).exists()]


def find_record(pak: Path, file_id: int) -> PakRecord | None:
    with pak.open("rb") as handle:
        header = handle.read(32)
        if len(header) < 32 or header[:4] != b"PACK":
            return None
        _sig, count, index_offset, _data_offset, _crc = struct.unpack("<4sIIII", header[:20])
        lo, hi = 0, count - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            handle.seek(index_offset + mid * 16)
            record = handle.read(16)
            if len(record) != 16:
                return None
            rec_id, offset, size, compress_flag = struct.unpack("<IIII", record)
            if file_id < rec_id:
                hi = mid - 1
            elif file_id > rec_id:
                lo = mid + 1
            else:
                return PakRecord(pak, mid, offset, size, compress_flag & 0x00FFFFFF, compress_flag & 0xFF000000)
    return None


def find_ucl_source(source_root: Path) -> tuple[Path, Path] | None:
    candidates = [
        source_root / "SwordOnline/Sources/Engine",
        source_root / "SwordOnline/Sources/Engine/Src",
        source_root / "Sources/Engine",
        source_root,
    ]
    for base in candidates:
        n2b = base / "Src/ucl/n2b_d.c"
        include = base / "Include"
        if n2b.exists() and (include / "ucl/ucl.h").exists():
            return n2b, include
        n2b = base / "ucl/n2b_d.c"
        include = base.parent / "Include"
        if n2b.exists() and (include / "ucl/ucl.h").exists():
            return n2b, include
    return None


def build_ucl_helper(source_root: Path, out_dir: Path) -> Path | None:
    found = find_ucl_source(source_root)
    if not found or not shutil.which("gcc"):
        return None
    n2b, include = found
    tools = out_dir / ".tools"
    tools.mkdir(parents=True, exist_ok=True)
    c_path = tools / "deucl.c"
    exe = tools / "deucl"
    digest = hashlib.sha1((str(n2b) + str(include)).encode()).hexdigest()[:12]
    stamp = tools / f"deucl.{digest}.stamp"
    if exe.exists() and stamp.exists():
        return exe
    c_path.write_text(UCL_C)
    cmd = ["gcc", "-O2", f"-I{include}", f"-I{n2b.parent}", str(c_path), str(n2b), "-o", str(exe)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return None
    stamp.write_text("ok\n")
    return exe


def decode_record(record: PakRecord, helper: Path | None, out_file: Path) -> bool:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with record.pak.open("rb") as handle:
        handle.seek(record.offset)
        packed = handle.read(record.packed_size)
    if record.method == 0:
        if len(packed) != record.size:
            return False
        out_file.write_bytes(packed)
        return True
    if record.method in (0x01000000, 0x20000000) and helper:
        with tempfile.TemporaryDirectory() as temp:
            inp = Path(temp) / "in.bin"
            inp.write_bytes(packed)
            result = subprocess.run([str(helper), str(inp), str(out_file), str(record.size)], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"failed UCL decode {record.pak.name}: {result.stderr.strip()}", file=sys.stderr)
                return False
        return True
    print(f"skip unsupported compression method {record.method:#x} in {record.pak.name}", file=sys.stderr)
    return False


def iconv_convert(data: bytes, encoding: str) -> str | None:
    if encoding == "utf-8":
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if encoding == "gbk":
        try:
            return data.decode("gbk")
        except UnicodeDecodeError:
            return None
    if encoding == "latin1":
        return data.decode("latin1")
    if shutil.which("iconv"):
        result = subprocess.run(["iconv", "-f", encoding, "-t", "UTF-8"], input=data, capture_output=True)
        if result.returncode == 0:
            return result.stdout.decode("utf-8", errors="ignore")
    return None


def score_text(text: str) -> int:
    vietnamese = "ăâđêôơưĂÂĐÊÔƠƯáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    vi = sum(1 for ch in text if ch in vietnamese)
    ascii_letters = sum(1 for ch in text if ch.isascii() and ch.isalpha())
    replacement = text.count("�")
    return vi * 8 + cjk * 4 + ascii_letters // 20 - replacement * 20


def convert_best(data: bytes) -> tuple[str, str]:
    variants: list[tuple[int, str, str]] = []
    for enc in ("utf-8", "TCVN", "gbk", "latin1"):
        text = iconv_convert(data, enc)
        if text is not None:
            variants.append((score_text(text), enc, text))
    if not variants:
        return "binary", ""
    variants.sort(reverse=True, key=lambda item: item[0])
    return variants[0][1], variants[0][2]


def safe_name(virtual_path: str, pak_name: str | None = None) -> str:
    name = virtual_path.strip("\\/").replace("\\", "__").replace("/", "__")
    if pak_name:
        name += "__" + Path(pak_name).stem
    return name


def extract_paths(args: argparse.Namespace, out_dir: Path) -> list[Path]:
    client_dir = Path(args.client_dir).resolve()
    helper = build_ucl_helper(Path(args.source_root).resolve(), out_dir) if args.source_root else None
    raw_dir = out_dir / "pak_raw"
    text_dir = out_dir / "pak_utf8"
    extracted_text: list[Path] = []
    paks = package_order(client_dir)
    manifest = ["virtual_path\tfile_id\tpak\tmethod\tsize\tencoding\toutput"]
    for virtual_path in args.paths or DEFAULT_VIRTUAL_PATHS:
        file_id = file_name_to_id(virtual_path)
        hits = []
        for pak in paks:
            record = find_record(pak, file_id)
            if record:
                hits.append(record)
                if not args.all_matches:
                    break
        if not hits:
            manifest.append(f"{virtual_path}\t{file_id:#x}\tMISS\t\t\t\t")
            continue
        for record in hits:
            raw_out = raw_dir / (safe_name(virtual_path, record.pak.name) + ".bin")
            if not decode_record(record, helper, raw_out):
                manifest.append(f"{virtual_path}\t{file_id:#x}\t{record.pak.name}\t{record.method:#x}\t{record.size}\tDECODE_FAIL\t")
                continue
            enc, text = convert_best(raw_out.read_bytes())
            text_out = text_dir / (safe_name(virtual_path, record.pak.name) + ".txt")
            text_out.parent.mkdir(parents=True, exist_ok=True)
            text_out.write_text(text, encoding="utf-8")
            extracted_text.append(text_out)
            manifest.append(f"{virtual_path}\t{file_id:#x}\t{record.pak.name}\t{record.method:#x}\t{record.size}\t{enc}\t{text_out}")
    (out_dir / "manifest.tsv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return extracted_text


def convert_loose(client_dir: Path, out_dir: Path) -> list[Path]:
    roots = [client_dir / "Settings", client_dir / "Ui", client_dir / "script"]
    outputs: list[Path] = []
    manifest = ["source\tencoding\toutput"]
    for root in roots:
        if not root.exists():
            continue
        for source in root.rglob("*"):
            if not source.is_file() or source.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                data = source.read_bytes()
            except OSError:
                continue
            enc, text = convert_best(data)
            rel = source.relative_to(client_dir)
            dest = out_dir / "loose_utf8" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
            outputs.append(dest)
            manifest.append(f"{source}\t{enc}\t{dest}")
    (out_dir / "loose_manifest.tsv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return outputs


def search_outputs(paths: Iterable[Path], query: str) -> int:
    query_lower = query.lower()
    hits = 0
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            if query_lower in line.lower():
                print(f"{path}:{line_no}: {line[:1000]}")
                hits += 1
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract/convert VLTK JX item tables from PAK and loose files.")
    parser.add_argument("--client-dir", required=True, help="Path to swrod3/bin/Client")
    parser.add_argument("--source-root", help="Path to swrod3 or source root containing SwordOnline/Sources/Engine")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--paths", nargs="*", help="Virtual PAK paths to extract; defaults to common item/skill paths")
    parser.add_argument("--all-matches", action="store_true", help="Extract every matching package instead of first package-order hit")
    parser.add_argument("--include-loose", action="store_true", help="Also convert loose Client/Settings, Client/Ui, Client/script text files")
    parser.add_argument("--query", help="Search decoded outputs for a Unicode query")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = extract_paths(args, out_dir)
    if args.include_loose:
        outputs.extend(convert_loose(Path(args.client_dir).resolve(), out_dir))
    if args.query:
        hits = search_outputs(outputs, args.query)
        print(f"hits={hits}")
    print(f"manifest={out_dir / 'manifest.tsv'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
