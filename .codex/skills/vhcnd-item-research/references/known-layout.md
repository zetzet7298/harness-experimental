# Known VLTK/JX Source Layout

Use these as starting points, then verify in the current checkout.

## Extracted JXWin Source

Common root from the recovered VM archive:

```text
/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3
```

Important subpaths:

- `SwordOnline/Sources/JXAll.dsw` - Visual C++ 6 workspace.
- `SwordOnline/Sources/Core/Src` - item, skill, player, NPC, magic logic.
- `SwordOnline/Sources/Engine/Src/XPackFile.cpp` - PAK/XPack reader.
- `SwordOnline/Sources/Engine/Src/KPakList.cpp` - package order and `FileNameToId` hash.
- `SwordOnline/Sources/Engine/Src/ucl` + `SwordOnline/Sources/Engine/Include/ucl` - bundled UCL decompressor.
- `bin/Client/package.ini` - client package load order.
- `bin/Client/data/*.pak` - runtime packages.
- `bin/Client/Settings/item/*.txt` - loose item tables; can be stale or Chinese.
- `bin/Server/Settings/item/*.txt` - server-side loose item tables.

## Runtime Package Notes

`Client/package.ini` order matters. A virtual file such as `\settings\item\helm.txt` may appear in multiple PAKs. The first package-order hit is the runtime candidate, but compare all hits when investigating Vietnamese overrides.

Observed examples:

- `\settings\item\helm.txt` appears in `update01.pak`, `volamtest1.pak`, `vltkcache.pak`.
- `\settings\Skills.txt` appears in `slistcache.pak`, multiple update packs, `vltkcache.pak`, and `volamtest1.pak`.
- `package.ini` may omit some existing `.pak` files, so mention whether the result is package-order or extra-package evidence.

## Encoding Notes

- Loose tables may be GBK Chinese.
- PAK tables may be TCVN3 Vietnamese or GBK Chinese.
- UI files and rank strings may be TCVN3 Vietnamese.
- Search Unicode Vietnamese only after extracting and converting to UTF-8.
- Do not claim Vietnamese localization if the string was manually translated from GBK.
