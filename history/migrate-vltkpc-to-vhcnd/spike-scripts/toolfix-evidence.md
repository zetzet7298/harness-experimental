# mig-x5e toolfix evidence

Patched `/var/www/vhcnd/tools/scan_required_spr.py` defaults to remove stale `servernew_up` and use canonical `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item...` paths.

## Validation

```text
$ python3 -c "import ast; ast.parse(open('/var/www/vhcnd/tools/scan_required_spr.py').read())"
(exit 0)

$ grep -n 'servernew_up' /var/www/vhcnd/tools/scan_required_spr.py
(no matches; command returned non-zero as expected)

$ grep -n '/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004' /var/www/vhcnd/tools/scan_required_spr.py
140:        default="/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004",

$ grep -n '/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item' /var/www/vhcnd/tools/scan_required_spr.py
140:        default="/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004",
161:        default="/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item",

$ grep -n '/var/www/vhcnd/item_spr' /var/www/vhcnd/tools/scan_required_spr.py
145:        default="/var/www/vhcnd/item_spr",
```
