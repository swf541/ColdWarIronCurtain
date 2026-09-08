# Tank Designer research-cost proposal

Status: RATIFIED AND APPLIED (2026-09-05). The R1-R7 schedule below is now the live pricing in `NSB_armor.txt` and `NSB_armor_modules.txt`; 91 of the 169 technologies were repriced and the applied distribution matches this document exactly (NSB_armor: 1x1, 56x2, 10x3; NSB_armor_modules: 42x1.5, 21x2, 39x2.5; total 345.5). XP policy is separately decided and unchanged: `xp_cost` stays flat at 1.

Prepared 2026-09-05 from controlling manual section D and the corrected Tier 3 handoff. The archived Opus proposal was used only as historical context and does not set any price.

## Scope and parser verification

Sources parsed as actual top-level entries:

- Cold War Iron Curtain/common/technologies/NSB_armor.txt: 67 top-level technology blocks.
- Cold War Iron Curtain/common/technologies/NSB_armor_modules.txt: 102 top-level technology blocks.

Verified membership: 67 + 102 = 169 technologies. Existing top-level prices sum to 337 = 133 + 204 = 337 (NSB_armor.txt + NSB_armor_modules.txt). All 169 parsed blocks have research_cost and start_year.

Parser saw 172 path arrows and 172 nested research_cost_coeff entries. The nested coefficients are connector modifiers, not top-level research prices, and are excluded from every total below. One connector targets out-of-scope mechanized_infantry; it is recorded as an external edge and does not enter the 169-tech tree.

Family membership is explicit below. The per-ID table is the authoritative row-by-row schedule for this proposal.

## Deterministic candidate schedule

The schedule applies start_year from each technology block. GUI @year anchors are not used. Prices are base-cost sums, not calendar research time.

| Code | Candidate rule | Rationale |
| --- | --- | --- |
| R1 | nsb_iw_armored_vehicles = 1 | Keep the single root at the existing root price; do not synthesize a module-tree root. |
| R2 | Modules-file technology with start_year < 1960 = 1.5 | Early module baseline follows the manual module tier. |
| R3 | Modules-file technology with 1960 <= start_year < 1980 = 2 | 1960s and 1970s module tier. |
| R4 | Modules-file technology with start_year >= 1980 = 2.5 | 1980+ module tier. |
| R5 | Light/MBT/heavy chassis technology with start_year < 1970 = 2 | Early chassis tier. |
| R6 | Light/MBT/heavy chassis technology with start_year >= 1970 = 3 | 1970+ chassis tier. |
| R7 | Any other NSB_armor.txt technology = 2 | Other chassis-file ladders retain the deterministic 2-point price. |

### Proposed exceptions

| Exact ID | New price | Reason |
| --- | ---: | --- |
| nsb_iw_armored_vehicles | 1 | Explicit root rule R1; it is the only exception to the family defaults. |

There are no other proposed exception IDs. Every row below uses R1-R7 exactly.

### Per-ID schedule

| ID | Source | Line | Old | New | start_year | Family | Rationale |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| nsb_iw_armored_vehicles | NSB_armor.txt | 20 | 1 | 1 | 1918 | root | R1 |
| nsb_light_tanks0 | NSB_armor.txt | 127 | 2 | 2 | 1942 | light chassis | R5 |
| nsb_light_tanks1 | NSB_armor.txt | 157 | 2 | 2 | 1944 | light chassis | R5 |
| nsb_light_tanks2 | NSB_armor.txt | 196 | 2 | 2 | 1950 | light chassis | R5 |
| nsb_light_tanks3 | NSB_armor.txt | 235 | 2 | 2 | 1960 | light chassis | R5 |
| nsb_light_tanks4 | NSB_armor.txt | 274 | 2 | 3 | 1970 | light chassis | R6 |
| nsb_light_tanks5 | NSB_armor.txt | 313 | 2 | 3 | 1980 | light chassis | R6 |
| nsb_light_tanks6 | NSB_armor.txt | 352 | 2 | 3 | 1990 | light chassis | R6 |
| nsb_light_tanks7 | NSB_armor.txt | 391 | 2 | 3 | 2000 | light chassis | R6 |
| nsb_light_tanks8 | NSB_armor.txt | 430 | 2 | 3 | 2010 | light chassis | R6 |
| nsb_main_battle_tanks0 | NSB_armor.txt | 465 | 2 | 2 | 1942 | MBT chassis | R5 |
| nsb_main_battle_tanks1 | NSB_armor.txt | 526 | 2 | 2 | 1944 | MBT chassis | R5 |
| nsb_main_battle_tanks2 | NSB_armor.txt | 565 | 2 | 2 | 1950 | MBT chassis | R5 |
| nsb_main_battle_tanks3 | NSB_armor.txt | 604 | 2 | 2 | 1960 | MBT chassis | R5 |
| nsb_main_battle_tanks4 | NSB_armor.txt | 645 | 2 | 3 | 1970 | MBT chassis | R6 |
| nsb_main_battle_tanks5 | NSB_armor.txt | 684 | 2 | 3 | 1980 | MBT chassis | R6 |
| nsb_main_battle_tanks6 | NSB_armor.txt | 723 | 2 | 3 | 1990 | MBT chassis | R6 |
| nsb_main_battle_tanks7 | NSB_armor.txt | 762 | 2 | 3 | 2010 | MBT chassis | R6 |
| nsb_main_battle_tanks8 | NSB_armor.txt | 801 | 2 | 3 | 2020 | MBT chassis | R6 |
| nsb_heavy_tanks0 | NSB_armor.txt | 836 | 2 | 2 | 1942 | heavy chassis | R5 |
| nsb_heavy_tanks1 | NSB_armor.txt | 908 | 2 | 2 | 1944 | heavy chassis | R5 |
| nsb_heavy_tanks2 | NSB_armor.txt | 947 | 2 | 2 | 1950 | heavy chassis | R5 |
| nsb_heavy_tanks3 | NSB_armor.txt | 990 | 2 | 2 | 1955 | heavy chassis | R5 |
| nsb_engines | NSB_armor.txt | 1025 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_engines0 | NSB_armor.txt | 1089 | 2 | 2 | 1950 | other chassis-file | R7 |
| nsb_engines1 | NSB_armor.txt | 1114 | 2 | 2 | 1960 | other chassis-file | R7 |
| nsb_engines2 | NSB_armor.txt | 1143 | 2 | 2 | 1980 | other chassis-file | R7 |
| nsb_engines3 | NSB_armor.txt | 1170 | 2 | 2 | 2000 | other chassis-file | R7 |
| nsb_gt_engines0 | NSB_armor.txt | 1194 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_gt_engines1 | NSB_armor.txt | 1220 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_gt_engines2 | NSB_armor.txt | 1244 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_gt_engines3 | NSB_armor.txt | 1268 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_hybrid_engines | NSB_armor.txt | 1292 | 2 | 2 | 2020 | other chassis-file | R7 |
| nsb_suspension0 | NSB_armor.txt | 1314 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_suspension1 | NSB_armor.txt | 1343 | 2 | 2 | 1944 | other chassis-file | R7 |
| nsb_suspension2 | NSB_armor.txt | 1363 | 2 | 2 | 1960 | other chassis-file | R7 |
| nsb_suspension3 | NSB_armor.txt | 1386 | 2 | 2 | 1985 | other chassis-file | R7 |
| nsb_armor | NSB_armor.txt | 1405 | 2 | 2 | 1940 | other chassis-file | R7 |
| nsb_armor0 | NSB_armor.txt | 1433 | 2 | 2 | 1944 | other chassis-file | R7 |
| nsb_armor1 | NSB_armor.txt | 1457 | 2 | 2 | 1955 | other chassis-file | R7 |
| nsb_armor2 | NSB_armor.txt | 1481 | 2 | 2 | 1965 | other chassis-file | R7 |
| nsb_armor3 | NSB_armor.txt | 1509 | 2 | 2 | 1975 | other chassis-file | R7 |
| nsb_armor4 | NSB_armor.txt | 1539 | 2 | 2 | 1985 | other chassis-file | R7 |
| nsb_armor5 | NSB_armor.txt | 1563 | 2 | 2 | 1995 | other chassis-file | R7 |
| nsb_armor6 | NSB_armor.txt | 1591 | 2 | 2 | 2010 | other chassis-file | R7 |
| nsb_du_armor0 | NSB_armor.txt | 1611 | 2 | 2 | 1985 | other chassis-file | R7 |
| nsb_du_armor1 | NSB_armor.txt | 1636 | 2 | 2 | 1995 | other chassis-file | R7 |
| nsb_du_armor2 | NSB_armor.txt | 1659 | 2 | 2 | 2010 | other chassis-file | R7 |
| nsb_era0 | NSB_armor.txt | 1678 | 2 | 2 | 1975 | other chassis-file | R7 |
| nsb_era1 | NSB_armor.txt | 1703 | 2 | 2 | 1985 | other chassis-file | R7 |
| nsb_era2 | NSB_armor.txt | 1727 | 2 | 2 | 2005 | other chassis-file | R7 |
| nsb_era3 | NSB_armor.txt | 1750 | 2 | 2 | 2015 | other chassis-file | R7 |
| nsb_al_armor0 | NSB_armor.txt | 1769 | 2 | 2 | 1955 | other chassis-file | R7 |
| nsb_al_armor1 | NSB_armor.txt | 1794 | 2 | 2 | 1965 | other chassis-file | R7 |
| nsb_addon_armor0 | NSB_armor.txt | 1813 | 2 | 2 | 1995 | other chassis-file | R7 |
| nsb_addon_armor1 | NSB_armor.txt | 1838 | 2 | 2 | 2005 | other chassis-file | R7 |
| nsb_defenses0 | NSB_armor.txt | 1857 | 2 | 2 | 1944 | other chassis-file | R7 |
| nsb_defenses1 | NSB_armor.txt | 1885 | 2 | 2 | 1975 | other chassis-file | R7 |
| nsb_defenses2 | NSB_armor.txt | 1913 | 2 | 2 | 1985 | other chassis-file | R7 |
| nsb_defenses3 | NSB_armor.txt | 1936 | 2 | 2 | 1995 | other chassis-file | R7 |
| nsb_defenses4 | NSB_armor.txt | 1959 | 2 | 2 | 2015 | other chassis-file | R7 |
| nsb_aps0 | NSB_armor.txt | 1978 | 2 | 2 | 1980 | other chassis-file | R7 |
| nsb_aps1 | NSB_armor.txt | 2008 | 2 | 2 | 1990 | other chassis-file | R7 |
| nsb_aps2 | NSB_armor.txt | 2031 | 2 | 2 | 2005 | other chassis-file | R7 |
| nsb_aps3 | NSB_armor.txt | 2054 | 2 | 2 | 2015 | other chassis-file | R7 |
| nsb_softkill0 | NSB_armor.txt | 2073 | 2 | 2 | 1990 | other chassis-file | R7 |
| nsb_softkill1 | NSB_armor.txt | 2099 | 2 | 2 | 2010 | other chassis-file | R7 |
| nsb_light_guns | NSB_armor_modules.txt | 20 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_light_guns1 | NSB_armor_modules.txt | 59 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_light_guns2 | NSB_armor_modules.txt | 96 | 2 | 1.5 | 1944 | modules-file | R2 |
| nsb_light_guns3 | NSB_armor_modules.txt | 135 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_light_guns4 | NSB_armor_modules.txt | 170 | 2 | 2 | 1960 | modules-file | R3 |
| nsb_light_guns5 | NSB_armor_modules.txt | 209 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_light_guns6 | NSB_armor_modules.txt | 244 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_light_guns7 | NSB_armor_modules.txt | 279 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_light_guns8 | NSB_armor_modules.txt | 314 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_light_guns9 | NSB_armor_modules.txt | 349 | 2 | 2.5 | 2015 | modules-file | R4 |
| nsb_low_pressure_guns | NSB_armor_modules.txt | 380 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_low_pressure_guns1 | NSB_armor_modules.txt | 408 | 2 | 2 | 1960 | modules-file | R3 |
| nsb_low_pressure_guns2 | NSB_armor_modules.txt | 442 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_low_pressure_guns3 | NSB_armor_modules.txt | 476 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_medium_guns | NSB_armor_modules.txt | 506 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_medium_guns1 | NSB_armor_modules.txt | 547 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_medium_guns2 | NSB_armor_modules.txt | 582 | 2 | 1.5 | 1944 | modules-file | R2 |
| nsb_medium_guns3 | NSB_armor_modules.txt | 617 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_medium_guns4 | NSB_armor_modules.txt | 652 | 2 | 2 | 1960 | modules-file | R3 |
| nsb_medium_guns5 | NSB_armor_modules.txt | 692 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_medium_guns6 | NSB_armor_modules.txt | 728 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_medium_guns7 | NSB_armor_modules.txt | 768 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_medium_guns8 | NSB_armor_modules.txt | 808 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_medium_guns9 | NSB_armor_modules.txt | 848 | 2 | 2.5 | 2015 | modules-file | R4 |
| nsb_heavy_guns1 | NSB_armor_modules.txt | 880 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heavy_guns2 | NSB_armor_modules.txt | 917 | 2 | 1.5 | 1944 | modules-file | R2 |
| nsb_heavy_guns3 | NSB_armor_modules.txt | 952 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_heavy_guns4 | NSB_armor_modules.txt | 987 | 2 | 1.5 | 1955 | modules-file | R2 |
| nsb_heavy_guns5 | NSB_armor_modules.txt | 1022 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_heavy_guns6 | NSB_armor_modules.txt | 1059 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_heavy_guns7 | NSB_armor_modules.txt | 1094 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_superheavy_guns1 | NSB_armor_modules.txt | 1125 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_gun_launcher0 | NSB_armor_modules.txt | 1157 | 2 | 2 | 1965 | modules-file | R3 |
| nsb_ammo | NSB_armor_modules.txt | 1189 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_ap_ammo0 | NSB_armor_modules.txt | 1229 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_ap_ammo1 | NSB_armor_modules.txt | 1265 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_ap_ammo2 | NSB_armor_modules.txt | 1299 | 2 | 2 | 1960 | modules-file | R3 |
| nsb_ap_ammo3 | NSB_armor_modules.txt | 1333 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_ap_ammo4 | NSB_armor_modules.txt | 1375 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_ap_ammo5 | NSB_armor_modules.txt | 1409 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_ap_ammo6 | NSB_armor_modules.txt | 1443 | 2 | 2.5 | 2000 | modules-file | R4 |
| nsb_ap_ammo7 | NSB_armor_modules.txt | 1477 | 2 | 2.5 | 2015 | modules-file | R4 |
| nsb_ap_du_ammo0 | NSB_armor_modules.txt | 1507 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_ap_du_ammo1 | NSB_armor_modules.txt | 1543 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_ap_du_ammo2 | NSB_armor_modules.txt | 1577 | 2 | 2.5 | 2000 | modules-file | R4 |
| nsb_ap_du_ammo3 | NSB_armor_modules.txt | 1611 | 2 | 2.5 | 2015 | modules-file | R4 |
| nsb_he_ammo0 | NSB_armor_modules.txt | 1641 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_hesh_ammo0 | NSB_armor_modules.txt | 1685 | 2 | 1.5 | 1955 | modules-file | R2 |
| nsb_he_ammo1 | NSB_armor_modules.txt | 1714 | 2 | 1.5 | 1955 | modules-file | R2 |
| nsb_he_ammo2 | NSB_armor_modules.txt | 1747 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_he_ammo3 | NSB_armor_modules.txt | 1781 | 2 | 2.5 | 1985 | modules-file | R4 |
| nsb_he_ammo4 | NSB_armor_modules.txt | 1815 | 2 | 2.5 | 2015 | modules-file | R4 |
| nsb_heat_ammo0 | NSB_armor_modules.txt | 1845 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heat_ammo1 | NSB_armor_modules.txt | 1881 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_heat_ammo2 | NSB_armor_modules.txt | 1915 | 2 | 2 | 1960 | modules-file | R3 |
| nsb_heat_ammo3 | NSB_armor_modules.txt | 1949 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_heat_ammo4 | NSB_armor_modules.txt | 1985 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_heat_ammo5 | NSB_armor_modules.txt | 2029 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_heat_ammo6 | NSB_armor_modules.txt | 2065 | 2 | 2.5 | 2000 | modules-file | R4 |
| nsb_heat_mp_ammo0 | NSB_armor_modules.txt | 2096 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heat_mp_ammo1 | NSB_armor_modules.txt | 2132 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heat_mp_ammo2 | NSB_armor_modules.txt | 2166 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heat_du_ammo0 | NSB_armor_modules.txt | 2196 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heat_du_ammo1 | NSB_armor_modules.txt | 2232 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_heat_du_ammo2 | NSB_armor_modules.txt | 2266 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_tank_design | NSB_armor_modules.txt | 2296 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_autoloader0 | NSB_armor_modules.txt | 2329 | 2 | 1.5 | 1940 | modules-file | R2 |
| nsb_autoloader1 | NSB_armor_modules.txt | 2357 | 2 | 1.5 | 1944 | modules-file | R2 |
| nsb_autoloader2 | NSB_armor_modules.txt | 2383 | 2 | 1.5 | 1950 | modules-file | R2 |
| nsb_autoloader3 | NSB_armor_modules.txt | 2413 | 2 | 2 | 1960 | modules-file | R3 |
| nsb_autoloader4 | NSB_armor_modules.txt | 2439 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_autoloader5 | NSB_armor_modules.txt | 2469 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_autoloader6 | NSB_armor_modules.txt | 2495 | 2 | 2.5 | 2010 | modules-file | R4 |
| nsb_drum_autoloader0 | NSB_armor_modules.txt | 2517 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_conveyer_autoloader0 | NSB_armor_modules.txt | 2539 | 2 | 2 | 1965 | modules-file | R3 |
| nsb_conveyer_autoloader1 | NSB_armor_modules.txt | 2568 | 2 | 2.5 | 1985 | modules-file | R4 |
| nsb_conveyer_autoloader2 | NSB_armor_modules.txt | 2595 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_aiming_devices0 | NSB_armor_modules.txt | 2618 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_aiming_devices1 | NSB_armor_modules.txt | 2646 | 2 | 1.5 | 1944 | modules-file | R2 |
| nsb_aiming_devices2 | NSB_armor_modules.txt | 2669 | 2 | 1.5 | 1955 | modules-file | R2 |
| nsb_aiming_devices3 | NSB_armor_modules.txt | 2698 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_aiming_devices4 | NSB_armor_modules.txt | 2725 | 2 | 2.5 | 1985 | modules-file | R4 |
| nsb_aiming_devices5 | NSB_armor_modules.txt | 2753 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_optics0 | NSB_armor_modules.txt | 2780 | 2 | 1.5 | 1942 | modules-file | R2 |
| nsb_optics1 | NSB_armor_modules.txt | 2805 | 2 | 1.5 | 1944 | modules-file | R2 |
| nsb_optics2 | NSB_armor_modules.txt | 2835 | 2 | 1.5 | 1955 | modules-file | R2 |
| nsb_optics3 | NSB_armor_modules.txt | 2861 | 2 | 2 | 1965 | modules-file | R3 |
| nsb_optics4 | NSB_armor_modules.txt | 2891 | 2 | 2 | 1970 | modules-file | R3 |
| nsb_optics5 | NSB_armor_modules.txt | 2918 | 2 | 2.5 | 1980 | modules-file | R4 |
| nsb_optics6 | NSB_armor_modules.txt | 2945 | 2 | 2.5 | 1990 | modules-file | R4 |
| nsb_optics7 | NSB_armor_modules.txt | 2972 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_ballistic_calculator0 | NSB_armor_modules.txt | 3000 | 2 | 1.5 | 1955 | modules-file | R2 |
| nsb_ballistic_calculator1 | NSB_armor_modules.txt | 3028 | 2 | 2 | 1965 | modules-file | R3 |
| nsb_ballistic_calculator2 | NSB_armor_modules.txt | 3056 | 2 | 2 | 1975 | modules-file | R3 |
| nsb_ballistic_calculator3 | NSB_armor_modules.txt | 3083 | 2 | 2.5 | 1985 | modules-file | R4 |
| nsb_ballistic_calculator4 | NSB_armor_modules.txt | 3111 | 2 | 2.5 | 1995 | modules-file | R4 |
| nsb_ballistic_calculator5 | NSB_armor_modules.txt | 3139 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_ballistic_calculator6 | NSB_armor_modules.txt | 3168 | 2 | 2.5 | 2015 | modules-file | R4 |
| nsb_pano_sight0 | NSB_armor_modules.txt | 3196 | 2 | 2 | 1965 | modules-file | R3 |
| nsb_pano_sight1 | NSB_armor_modules.txt | 3224 | 2 | 2.5 | 1985 | modules-file | R4 |
| nsb_pano_sight2 | NSB_armor_modules.txt | 3250 | 2 | 2.5 | 2005 | modules-file | R4 |
| nsb_awareness_system | NSB_armor_modules.txt | 3272 | 2 | 2.5 | 2020 | modules-file | R4 |

## Exact family totals and full-tree arithmetic

| Family | Count | Membership | Old total | Candidate total | Delta |
| --- | ---: | --- | ---: | ---: | ---: |
| root | 1 | nsb_iw_armored_vehicles | 1 | 1 | 0 |
| light chassis | 9 | nsb_light_tanks0, nsb_light_tanks1, nsb_light_tanks2, nsb_light_tanks3, nsb_light_tanks4, nsb_light_tanks5, nsb_light_tanks6, nsb_light_tanks7, nsb_light_tanks8 | 18 | 23 | 5 |
| MBT chassis | 9 | nsb_main_battle_tanks0, nsb_main_battle_tanks1, nsb_main_battle_tanks2, nsb_main_battle_tanks3, nsb_main_battle_tanks4, nsb_main_battle_tanks5, nsb_main_battle_tanks6, nsb_main_battle_tanks7, nsb_main_battle_tanks8 | 18 | 23 | 5 |
| heavy chassis | 4 | nsb_heavy_tanks0, nsb_heavy_tanks1, nsb_heavy_tanks2, nsb_heavy_tanks3 | 8 | 8 | 0 |
| other chassis-file | 44 | nsb_engines, nsb_engines0, nsb_engines1, nsb_engines2, nsb_engines3, nsb_gt_engines0, nsb_gt_engines1, nsb_gt_engines2, nsb_gt_engines3, nsb_hybrid_engines, nsb_suspension0, nsb_suspension1, nsb_suspension2, nsb_suspension3, nsb_armor, nsb_armor0, nsb_armor1, nsb_armor2, nsb_armor3, nsb_armor4, nsb_armor5, nsb_armor6, nsb_du_armor0, nsb_du_armor1, nsb_du_armor2, nsb_era0, nsb_era1, nsb_era2, nsb_era3, nsb_al_armor0, nsb_al_armor1, nsb_addon_armor0, nsb_addon_armor1, nsb_defenses0, nsb_defenses1, nsb_defenses2, nsb_defenses3, nsb_defenses4, nsb_aps0, nsb_aps1, nsb_aps2, nsb_aps3, nsb_softkill0, nsb_softkill1 | 88 | 88 | 0 |
| modules-file | 102 | nsb_light_guns, nsb_light_guns1, nsb_light_guns2, nsb_light_guns3, nsb_light_guns4, nsb_light_guns5, nsb_light_guns6, nsb_light_guns7, nsb_light_guns8, nsb_light_guns9, nsb_low_pressure_guns, nsb_low_pressure_guns1, nsb_low_pressure_guns2, nsb_low_pressure_guns3, nsb_medium_guns, nsb_medium_guns1, nsb_medium_guns2, nsb_medium_guns3, nsb_medium_guns4, nsb_medium_guns5, nsb_medium_guns6, nsb_medium_guns7, nsb_medium_guns8, nsb_medium_guns9, nsb_heavy_guns1, nsb_heavy_guns2, nsb_heavy_guns3, nsb_heavy_guns4, nsb_heavy_guns5, nsb_heavy_guns6, nsb_heavy_guns7, nsb_superheavy_guns1, nsb_gun_launcher0, nsb_ammo, nsb_ap_ammo0, nsb_ap_ammo1, nsb_ap_ammo2, nsb_ap_ammo3, nsb_ap_ammo4, nsb_ap_ammo5, nsb_ap_ammo6, nsb_ap_ammo7, nsb_ap_du_ammo0, nsb_ap_du_ammo1, nsb_ap_du_ammo2, nsb_ap_du_ammo3, nsb_he_ammo0, nsb_hesh_ammo0, nsb_he_ammo1, nsb_he_ammo2, nsb_he_ammo3, nsb_he_ammo4, nsb_heat_ammo0, nsb_heat_ammo1, nsb_heat_ammo2, nsb_heat_ammo3, nsb_heat_ammo4, nsb_heat_ammo5, nsb_heat_ammo6, nsb_heat_mp_ammo0, nsb_heat_mp_ammo1, nsb_heat_mp_ammo2, nsb_heat_du_ammo0, nsb_heat_du_ammo1, nsb_heat_du_ammo2, nsb_tank_design, nsb_autoloader0, nsb_autoloader1, nsb_autoloader2, nsb_autoloader3, nsb_autoloader4, nsb_autoloader5, nsb_autoloader6, nsb_drum_autoloader0, nsb_conveyer_autoloader0, nsb_conveyer_autoloader1, nsb_conveyer_autoloader2, nsb_aiming_devices0, nsb_aiming_devices1, nsb_aiming_devices2, nsb_aiming_devices3, nsb_aiming_devices4, nsb_aiming_devices5, nsb_optics0, nsb_optics1, nsb_optics2, nsb_optics3, nsb_optics4, nsb_optics5, nsb_optics6, nsb_optics7, nsb_ballistic_calculator0, nsb_ballistic_calculator1, nsb_ballistic_calculator2, nsb_ballistic_calculator3, nsb_ballistic_calculator4, nsb_ballistic_calculator5, nsb_ballistic_calculator6, nsb_pano_sight0, nsb_pano_sight1, nsb_pano_sight2, nsb_awareness_system | 204 | 202.5 | -1.5 |

Candidate distribution: light chassis 4 x 2 + 5 x 3 = 23; MBT chassis 4 x 2 + 5 x 3 = 23; heavy chassis 4 x 2 = 8; other chassis-file 44 x 2 = 88; modules-file 42 x 1.5 + 21 x 2 + 39 x 2.5 = 202.5; root = 1.

Arithmetic check: old total = 1 + 18 + 18 + 8 + 88 + 204 = 337. Candidate total = 1 + 23 + 23 + 8 + 88 + 202.5 = 345.5. Whole-tree delta = 8.5 (2.52%).

## 1949 setup and path model

The 1949 NSB path uses the No Step Back branches. The 1949 bookmark is Cold War Iron Curtain/common/bookmarks/the_gathering_storm.txt (date = 1949.5.23.1; USA is default and SOV is an available country). The non-NSB legacy branches are excluded from this NSB proposal.

History evidence:

- USA NSB OOB bootstrap in history/countries/USA - United States.txt:51-61 sets six IDs: nsb_heavy_tanks0, nsb_iw_armored_vehicles, nsb_light_tanks0, nsb_light_tanks1, nsb_main_battle_tanks0, nsb_main_battle_tanks1.
- SOV NSB OOB bootstrap in history/countries/SOV - Soviet union.txt:19-31 sets eight IDs: nsb_heavy_tanks0, nsb_heavy_tanks1, nsb_heavy_tanks2, nsb_iw_armored_vehicles, nsb_light_tanks0, nsb_light_tanks1, nsb_main_battle_tanks0, nsb_main_battle_tanks1.
- USA later static NSB starting block at history/countries/USA - United States.txt:1697-1742 and SOV corresponding block at history/countries/SOV - Soviet union.txt:357-402 both set the same 40 IDs listed below.
- Each OOB bootstrap set is a subset of that 40-ID block. Therefore the effective 1949 starting set is identical for USA and SOV; the OOB difference does not change the remaining path.

Effective 1949 starting IDs, exempt from remaining-path charges because they are explicitly set_technology at setup:

nsb_iw_armored_vehicles, nsb_light_tanks0, nsb_light_tanks1, nsb_main_battle_tanks0, nsb_main_battle_tanks1, nsb_main_battle_tanks2, nsb_heavy_tanks0, nsb_heavy_tanks1, nsb_heavy_tanks2, nsb_engines, nsb_suspension0, nsb_armor, nsb_light_guns, nsb_medium_guns, nsb_ammo, nsb_tank_design, nsb_autoloader0, nsb_light_guns1, nsb_medium_guns1, nsb_heavy_guns1, nsb_ap_ammo0, nsb_he_ammo0, nsb_heat_ammo0, nsb_aiming_devices0, nsb_optics0, nsb_light_guns2, nsb_medium_guns2, nsb_heavy_guns2, nsb_armor0, nsb_defenses0, nsb_autoloader1, nsb_aiming_devices1, nsb_optics1, nsb_light_guns3, nsb_medium_guns3, nsb_heavy_guns3, nsb_low_pressure_guns, nsb_ap_ammo1, nsb_heat_ammo1, nsb_autoloader2

Starting-set arithmetic: 40 IDs; current-price sum = 79; candidate-price sum = 66. Some explicitly granted IDs have start_year after the June 1949 bookmark date; they remain starting IDs because setup grants them. start_year is used for horizon eligibility of non-starting IDs.

Path calculation contract:

1. Seed the graph with the effective 40-ID setup set.
2. For horizon H, repeatedly add an in-scope technology when its start_year <= H and at least one incoming path arrow comes from an already reached technology.
3. Charge each reached, non-starting ID once. Shared prerequisites and a node reached through multiple alternatives are deduplicated by ID.
4. Treat multiple incoming path arrows as alternative prerequisites (OR) for reachability, as required by the manual. The exact alternatives found are listed below.
5. Do not invent a connection from nsb_iw_armored_vehicles to the modules folder. The six in-scope graph roots are all explicitly granted in the 1949 setup.

Multiple incoming prerequisite alternatives:
- nsb_main_battle_tanks4: nsb_main_battle_tanks3 OR nsb_heavy_tanks2
- nsb_hybrid_engines: nsb_engines3 OR nsb_gt_engines3
- nsb_gun_launcher0: nsb_light_guns4 OR nsb_medium_guns4
- nsb_heavy_guns6: nsb_medium_guns7 OR nsb_heavy_guns5
- nsb_heavy_guns7: nsb_medium_guns8 OR nsb_heavy_guns6
- nsb_ap_ammo5: nsb_ap_ammo3 OR nsb_ap_ammo4
- nsb_awareness_system: nsb_aiming_devices5 OR nsb_optics7 OR nsb_ballistic_calculator6

The only out-of-scope connector is nsb_iw_armored_vehicles -> mechanized_infantry; it is not included in any armor/module path.

## Deduplicated remaining paths

The membership blocks below enumerate every charged ID. The same membership applies to USA and SOV because the effective 1949 starting set is identical; the country-specific totals are still shown separately in the comparison table.

### Membership P1970

Reachable including setup: 85. Charged remaining IDs: 45.
Nine IDs have start_year <= 1970 but no reachable incoming path from the actual setup; they are excluded rather than charged: nsb_heavy_guns5, nsb_heavy_guns6, nsb_heavy_guns7, nsb_heat_mp_ammo0, nsb_heat_mp_ammo1, nsb_heat_mp_ammo2, nsb_heat_du_ammo0, nsb_heat_du_ammo1, nsb_heat_du_ammo2.

| Family | Count | IDs | Current total | Candidate total |
| --- | ---: | --- | ---: | ---: |
| root | 0 |  | 0 | 0 |
| light chassis | 3 | nsb_light_tanks2, nsb_light_tanks3, nsb_light_tanks4 | 6 | 7 |
| MBT chassis | 2 | nsb_main_battle_tanks3, nsb_main_battle_tanks4 | 4 | 5 |
| heavy chassis | 1 | nsb_heavy_tanks3 | 2 | 2 |
| other chassis-file | 12 | nsb_engines0, nsb_engines1, nsb_gt_engines0, nsb_gt_engines1, nsb_gt_engines2, nsb_gt_engines3, nsb_suspension1, nsb_suspension2, nsb_armor1, nsb_armor2, nsb_al_armor0, nsb_al_armor1 | 24 | 24 |
| modules-file | 27 | nsb_light_guns4, nsb_light_guns5, nsb_low_pressure_guns1, nsb_low_pressure_guns2, nsb_medium_guns4, nsb_medium_guns5, nsb_heavy_guns4, nsb_superheavy_guns1, nsb_gun_launcher0, nsb_ap_ammo2, nsb_ap_ammo3, nsb_hesh_ammo0, nsb_he_ammo1, nsb_he_ammo2, nsb_heat_ammo2, nsb_heat_ammo3, nsb_autoloader3, nsb_autoloader4, nsb_conveyer_autoloader0, nsb_aiming_devices2, nsb_aiming_devices3, nsb_optics2, nsb_optics3, nsb_optics4, nsb_ballistic_calculator0, nsb_ballistic_calculator1, nsb_pano_sight0 | 54 | 50.5 |

P1970 arithmetic: current = 90; candidate = 88.5.

### Membership P2020

Reachable including setup: 169. Charged remaining IDs: 129.

| Family | Count | IDs | Current total | Candidate total |
| --- | ---: | --- | ---: | ---: |
| root | 0 |  | 0 | 0 |
| light chassis | 7 | nsb_light_tanks2, nsb_light_tanks3, nsb_light_tanks4, nsb_light_tanks5, nsb_light_tanks6, nsb_light_tanks7, nsb_light_tanks8 | 14 | 19 |
| MBT chassis | 6 | nsb_main_battle_tanks3, nsb_main_battle_tanks4, nsb_main_battle_tanks5, nsb_main_battle_tanks6, nsb_main_battle_tanks7, nsb_main_battle_tanks8 | 12 | 17 |
| heavy chassis | 1 | nsb_heavy_tanks3 | 2 | 2 |
| other chassis-file | 39 | nsb_engines0, nsb_engines1, nsb_engines2, nsb_engines3, nsb_gt_engines0, nsb_gt_engines1, nsb_gt_engines2, nsb_gt_engines3, nsb_hybrid_engines, nsb_suspension1, nsb_suspension2, nsb_suspension3, nsb_armor1, nsb_armor2, nsb_armor3, nsb_armor4, nsb_armor5, nsb_armor6, nsb_du_armor0, nsb_du_armor1, nsb_du_armor2, nsb_era0, nsb_era1, nsb_era2, nsb_era3, nsb_al_armor0, nsb_al_armor1, nsb_addon_armor0, nsb_addon_armor1, nsb_defenses1, nsb_defenses2, nsb_defenses3, nsb_defenses4, nsb_aps0, nsb_aps1, nsb_aps2, nsb_aps3, nsb_softkill0, nsb_softkill1 | 78 | 78 |
| modules-file | 76 | nsb_light_guns4, nsb_light_guns5, nsb_light_guns6, nsb_light_guns7, nsb_light_guns8, nsb_light_guns9, nsb_low_pressure_guns1, nsb_low_pressure_guns2, nsb_low_pressure_guns3, nsb_medium_guns4, nsb_medium_guns5, nsb_medium_guns6, nsb_medium_guns7, nsb_medium_guns8, nsb_medium_guns9, nsb_heavy_guns4, nsb_heavy_guns5, nsb_heavy_guns6, nsb_heavy_guns7, nsb_superheavy_guns1, nsb_gun_launcher0, nsb_ap_ammo2, nsb_ap_ammo3, nsb_ap_ammo4, nsb_ap_ammo5, nsb_ap_ammo6, nsb_ap_ammo7, nsb_ap_du_ammo0, nsb_ap_du_ammo1, nsb_ap_du_ammo2, nsb_ap_du_ammo3, nsb_hesh_ammo0, nsb_he_ammo1, nsb_he_ammo2, nsb_he_ammo3, nsb_he_ammo4, nsb_heat_ammo2, nsb_heat_ammo3, nsb_heat_ammo4, nsb_heat_ammo5, nsb_heat_ammo6, nsb_heat_mp_ammo0, nsb_heat_mp_ammo1, nsb_heat_mp_ammo2, nsb_heat_du_ammo0, nsb_heat_du_ammo1, nsb_heat_du_ammo2, nsb_autoloader3, nsb_autoloader4, nsb_autoloader5, nsb_autoloader6, nsb_drum_autoloader0, nsb_conveyer_autoloader0, nsb_conveyer_autoloader1, nsb_conveyer_autoloader2, nsb_aiming_devices2, nsb_aiming_devices3, nsb_aiming_devices4, nsb_aiming_devices5, nsb_optics2, nsb_optics3, nsb_optics4, nsb_optics5, nsb_optics6, nsb_optics7, nsb_ballistic_calculator0, nsb_ballistic_calculator1, nsb_ballistic_calculator2, nsb_ballistic_calculator3, nsb_ballistic_calculator4, nsb_ballistic_calculator5, nsb_ballistic_calculator6, nsb_pano_sight0, nsb_pano_sight1, nsb_pano_sight2, nsb_awareness_system | 152 | 163.5 |

P2020 arithmetic: current = 258; candidate = 279.5.

## USA/SOV path evaluation against +/-10%

The comparison is candidate remaining-path sum versus the existing remaining-path sum at the same 1949 setup and horizon. The +/-10% band is applied to each country/horizon path, not only to the 169-tech whole-tree aggregate.

| Country | Horizon | Charged IDs | Current | Candidate | Delta | +/-10% interval around current | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| USA | 1970 | 45 | 90 | 88.5 | -1.67% | 81 to 99 | PASS |
| USA | 2020 | 129 | 258 | 279.5 | +8.33% | 232.2 to 283.8 | PASS |
| SOV | 1970 | 45 | 90 | 88.5 | -1.67% | 81 to 99 | PASS |
| SOV | 2020 | 129 | 258 | 279.5 | +8.33% | 232.2 to 283.8 | PASS |

USA and SOV both pass: P1970 changes by -1.67%; P2020 changes by +8.33%. The full-tree change is +2.52% as a separate aggregate check. No revised schedule is required because every country/horizon path remains within +/-10%.

## Semantics and limits

These are exact arithmetic results for the declared parser and path contract. They are not calendar research-time simulations and do not model research slots, bonuses, ahead-of-time penalties, focuses, events, or player queue choices.

No unresolved 1949 setup condition prevents the static totals: both relevant country files explicitly grant the same effective 40-ID NSB set under has_dlc = No Step Back. The unresolved semantic boundary is dynamic progression: the repository does not specify which of the reachable technologies USA or SOV actually researched between 1949 and a horizon, so the report uses graph reachability plus start_year eligibility rather than claiming an historical queue. If No Step Back is absent, the legacy armor tree is active and these NSB path totals are not applicable.

The alternative-prerequisite treatment is an explicit reporting convention based on the path arrows. If a future runtime check establishes different all-parent behavior, recompute the path membership; no script price should be applied from this proposal without ratification.

Research pricing remains unratified. XP policy remains a separate decision. This document does not authorize or imply edits to research_cost, research_cost_coeff, or any XP field.


