# Remaining root move evidence — mig-7pk

- Feature: `migrate-vhcnd-to-vhcnd`
- Bead: `mig-7pk`
- Timestamp: `2026-05-19T13:02:19.016062+00:00`
- Operation: same-filesystem `mv` of remaining source root.

## Move command

```sh
mv /var/www/vhcnd/other-game/downloads_pak_extract /var/www/vhcnd/other-game/downloads_pak_extract
```

Result: command exited `0`.

## Acceptance evidence

```sh
du -sh /var/www/vhcnd/other-game/downloads_pak_extract
# 1.3G	/var/www/vhcnd/other-game/downloads_pak_extract

[ ! -e /var/www/vhcnd/other-game/downloads_pak_extract ]
# source_absent_ok
```

## Guardrail

Did not touch `/var/www/vhcnd/other-game/download-source/data_cdn_pak_extract`; per task contract, that path does not exist and the equivalent report target is `/var/www/vhcnd/datasets/data_cdn/pak_extract/data_cdn_pak_extract`.
