#!/usr/bin/env python3
"""Full-set VHCND named-path FNV-1a hash probe.

Mirrors /var/www/vhcnd/sources/Client/Classes/engine/KStrBase.cpp:881-887:
    hash starts at 0
    for each byte after byte-wise ASCII uppercase:
        hash *= 16777619
        hash ^= byte
        hash &= 0xffffffff

The probe compares named SPR/PNG path variants under post-move roots with the
8-hex basename stems present in the VHCND data_cdn pak extract.
"""

from __future__ import annotations

import csv
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ITEM_SPR_ROOT = Path("/var/www/vhcnd/item_spr")
ITEM_SPR_IMG_ROOT = Path("/var/www/vhcnd/item_spr_img")
HASH_STORE_ROOT = Path("/var/www/vhcnd/datasets/data_cdn/pak_extract/data_cdn_pak_extract")
OUT_DIR = Path("history/migrate-vhcnd-to-vhcnd/spike-scripts")
CSV_PATH = OUT_DIR / "fnv1a-probe.csv"
SUMMARY_PATH = OUT_DIR / "fnv1a-probe-summary.json"
EVIDENCE_PATH = OUT_DIR / "fnv1a-probe-evidence.md"
HEX8_RE = re.compile(r"^[0-9a-fA-F]{8}$")
FNV_MULTIPLIER = 16777619


def engine_upper_byte(byte: int) -> int:
    """Mirror C toupper for ASCII path bytes without locale side effects."""
    if 0x61 <= byte <= 0x7A:
        return byte - 0x20
    return byte


def engine_hash(path_variant: str) -> int:
    """Mirror KStrBase.cpp _ccHash over the path variant."""
    value = 0
    for byte in path_variant.encode("utf-8", "surrogateescape"):
        value = (value * FNV_MULTIPLIER) & 0xFFFFFFFF
        value ^= engine_upper_byte(byte)
        value &= 0xFFFFFFFF
    return value


def add_variant(seen: OrderedDict[str, None], variant: str) -> None:
    if variant:
        seen.setdefault(variant.replace("//", "/"), None)


def root_preserving_variants(rel_path: str) -> list[str]:
    """Return deterministic de-duped path spellings for hash probing."""
    rel = rel_path.replace("\\", "/").strip("/")
    seen: OrderedDict[str, None] = OrderedDict()

    bases: list[str] = []
    for candidate in (rel, rel.lower(), rel.upper()):
        if candidate not in bases:
            bases.append(candidate)

    # Preserve or introduce common client roots. If the path already starts with
    # spr/, keep both spr/ and Spr/ spellings while preserving the remainder.
    if rel.lower().startswith("spr/"):
        tail = rel[4:]
        for prefix in ("spr/", "Spr/", "SPR/"):
            for tail_variant in (tail, tail.lower(), tail.upper()):
                candidate = prefix + tail_variant
                if candidate not in bases:
                    bases.append(candidate)
    else:
        for prefix in ("spr/", "Spr/", "SPR/"):
            for body in (rel, rel.lower(), rel.upper()):
                candidate = prefix + body
                if candidate not in bases:
                    bases.append(candidate)

    for base in bases:
        add_variant(seen, base)
        add_variant(seen, "/" + base)
        add_variant(seen, base.replace("/", "\\"))
        add_variant(seen, ("/" + base).replace("/", "\\"))

    return list(seen.keys())


def gather_named_paths() -> list[dict[str, str]]:
    roots = [
        ("spr", ITEM_SPR_ROOT, ".spr"),
        ("png", ITEM_SPR_IMG_ROOT, ".png"),
    ]
    missing = [str(root) for _, root, _ in roots if not root.is_dir()]
    if missing:
        raise SystemExit(f"BLOCKED: missing named path roots: {', '.join(missing)}")

    named: list[dict[str, str]] = []
    for kind, root, suffix in roots:
        for path in sorted(root.rglob(f"*{suffix}"), key=lambda p: p.as_posix().lower()):
            if path.is_file():
                named.append(
                    {
                        "kind": kind,
                        "root": str(root),
                        "named_path": path.relative_to(root).as_posix(),
                        "absolute_path": str(path),
                    }
                )
    return named


def gather_hash_store() -> dict[str, str]:
    if not HASH_STORE_ROOT.is_dir():
        raise SystemExit(f"BLOCKED: missing hash store root: {HASH_STORE_ROOT}")

    store: dict[str, str] = {}
    for path in sorted(HASH_STORE_ROOT.rglob("*.spr"), key=lambda p: p.as_posix().lower()):
        stem = path.stem.lower()
        if HEX8_RE.match(stem) and stem not in store:
            store[stem] = str(path)
    if not store:
        raise SystemExit(f"BLOCKED: hash store is empty under {HASH_STORE_ROOT}")
    return store


def write_outputs(named: list[dict[str, str]], store: dict[str, str]) -> dict[str, object]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_variants = 0
    matched_variants = 0
    matched_named: OrderedDict[str, dict[str, str]] = OrderedDict()
    sample_matches: list[dict[str, str]] = []

    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "kind",
                "named_path",
                "variant",
                "hash",
                "match_found",
                "matched_path",
            ],
        )
        writer.writeheader()
        for item in named:
            variants = root_preserving_variants(item["named_path"])
            for variant in variants:
                total_variants += 1
                hash_hex = f"{engine_hash(variant):08x}"
                matched_path = store.get(hash_hex, "")
                match_found = bool(matched_path)
                if match_found:
                    matched_variants += 1
                    matched_named.setdefault(
                        item["named_path"],
                        {
                            "kind": item["kind"],
                            "named_path": item["named_path"],
                            "variant": variant,
                            "hash": hash_hex,
                            "matched_path": matched_path,
                        },
                    )
                    if len(sample_matches) < 20:
                        sample_matches.append(
                            {
                                "kind": item["kind"],
                                "named_path": item["named_path"],
                                "variant": variant,
                                "hash": hash_hex,
                                "matched_path": matched_path,
                            }
                        )
                writer.writerow(
                    {
                        "kind": item["kind"],
                        "named_path": item["named_path"],
                        "variant": variant,
                        "hash": hash_hex,
                        "match_found": "true" if match_found else "false",
                        "matched_path": matched_path,
                    }
                )

    matched_named_paths = len(matched_named)
    if matched_named_paths == 0:
        verdict = "engine_hash_lookup=unmatched"
    else:
        verdict = "engine_hash_lookup=matched"

    summary: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": {
            "item_spr": str(ITEM_SPR_ROOT),
            "item_spr_img": str(ITEM_SPR_IMG_ROOT),
            "hash_store": str(HASH_STORE_ROOT),
        },
        "total_named": len(named),
        "total_variants": total_variants,
        "hash_store_count": len(store),
        "matched_variants": matched_variants,
        "matched_named_paths": matched_named_paths,
        "verdict": verdict,
        "sample_matches": sample_matches,
        "outputs": {
            "csv": str(CSV_PATH),
            "summary_json": str(SUMMARY_PATH),
            "evidence_md": str(EVIDENCE_PATH),
        },
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    evidence_lines = [
        "\n## FNV-1a full-set probe — " + summary["generated_at"],
        "",
        f"- Named roots: `{ITEM_SPR_ROOT}` and `{ITEM_SPR_IMG_ROOT}`.",
        f"- Hash store root: `{HASH_STORE_ROOT}`.",
        f"- Total named paths: {len(named)}.",
        f"- Total variants: {total_variants}.",
        f"- Hash store count: {len(store)}.",
        f"- Matched variants: {matched_variants}.",
        f"- Matched named paths: {matched_named_paths}.",
        f"- Verdict: `{verdict}`.",
        f"- CSV: `{CSV_PATH}`.",
        f"- Summary JSON: `{SUMMARY_PATH}`.",
    ]
    if sample_matches:
        evidence_lines.append("- Sample matches:")
        for match in sample_matches[:5]:
            evidence_lines.append(
                f"  - `{match['named_path']}` via `{match['variant']}` -> `{match['hash']}` -> `{match['matched_path']}`"
            )
    else:
        evidence_lines.append("- Sample matches: none.")
    EVIDENCE_PATH.open("a", encoding="utf-8").write("\n".join(evidence_lines) + "\n")
    return summary


def main() -> int:
    named = gather_named_paths()
    store = gather_hash_store()
    summary = write_outputs(named, store)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
