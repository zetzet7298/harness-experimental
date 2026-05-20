# Validation — S30 Missing Visual Source Absence Audit

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s30.md`

## Commands Run

```bash
python3 /var/www/vltk-h5-survivors/harness-experimental/.codex/skills/vhcnd-item-research/scripts/vltk_extract_tables.py \
  --client-dir /var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/bin/Client \
  --source-root /var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3 \
  --out /tmp/vltk-missing-38-sprs \
  --all-matches \
  --paths <38 missing virtual SPR paths>

# exact basename search under /var/www/vhcnd only
find /var/www/vhcnd -iname <missing basename> -type f -print

npm run check:runtime-isolation
```

## Results

- PAK all-matches extractor: PASS as absence evidence — manifest had 39 lines including header, and `nonMISS=0` for the 38 missing paths.
- Exact filesystem search under `/var/www/vhcnd`: PASS as absence evidence — 0 hits for every missing basename.
- Audit artifact committed at `data/vltk-normalized/equipment-visual-missing-sources.audit.json` with `missingCount=38`, `copiedLocalSources=284`, and all extractor rows marked `MISS`.
- Runtime isolation: PASS — no runtime symlink/direct `/var/www/vhcnd` usage.

## Remaining Gap

The 38 missing source SPRs cannot be recovered from the current VHCND source/PAK evidence. The next story must choose a source-backed fallback or mark affected catalog rows unresolved; do not synthesize or borrow from `/var/www/vltkunity`.
