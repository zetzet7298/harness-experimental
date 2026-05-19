# Recovery Evidence — swarming state repair after D7 scope-gap

## Context

Previous orchestration accidentally reset/reopened `mig-n53` and deleted `mig-piy`
while trying to resolve D7. This file records authoritative current filesystem
state and the graph repair required before continuing the swarm.

## Current filesystem state

The seven desired vhcnd roots now exist and the corresponding vltkunity sources
are gone:

```text
EXISTS /var/www/vhcnd/item_spr
EXISTS /var/www/vhcnd/item_spr_img
EXISTS /var/www/vhcnd/other-game/item_spr_like_img
EXISTS /var/www/vhcnd/other-game/download-source/data_cdn_spr_img
EXISTS /var/www/vhcnd/item_data
EXISTS /var/www/vhcnd/other-game/downloads_spr_img_struct
EXISTS /var/www/vhcnd/other-game/item_spr_like
MISSING /var/www/vltkunity/item_spr
MISSING /var/www/vltkunity/item_spr_img
MISSING /var/www/vltkunity/other-game/item_spr_like_img
MISSING /var/www/vltkunity/other-game/download-source/data_cdn_spr_img
MISSING /var/www/vltkunity/item_data
MISSING /var/www/vltkunity/other-game/downloads_spr_img_struct
MISSING /var/www/vltkunity/other-game/item_spr_like
```

## Decision for safe continuation

Do not perform destructive cleanup/deletion without explicit user approval.
Because the missing three roots are already moved, continue with a non-destructive
patch: rewrite residual `/var/www/vltkunity/...` references in vhcnd manifests
and tool defaults to equivalent `/var/www/vhcnd/...` paths, then run acceptance.

## Bead graph repair

- Close `mig-n53` based on current filesystem evidence above.
- Replace deleted `mig-piy` with:
  - `mig-428`: non-destructive residual reference patch (renamed from cleanup/delete).
  - `mig-yv0`: validation/manifest parse/tool default patch as needed.
- Add dependency `mig-6dg depends on mig-yv0` so acceptance waits for patch.
