# APC/IFV bookmark mapping

Approved phase-1 selections, 2026-09-07. Authority: [IFV_APC_HANDOFF.md](IFV_APC_HANDOFF.md), with the user's authorization to reconcile producer and naming conflicts before implementation. Exact source provenance, alternate conflicting source entries, concrete recipes, future inventory and resolved OOB requests are retained in [APC_IFV_Preset_Manifest.json](APC_IFV_Preset_Manifest.json).

There are 572 selected producer/chassis pairs across 86 tags, ten bookmark chassis (APC and IFV tiers 0 through 4), and 100 migrated OOB requests. The 354 national pairs for tiers 5 through 7 are retained as future inventory, not authored presets: no NSB OOB references those hulls in this batch. WWII mechanized equipment tiers 1 and 2 remain legacy-only.

## Decisions and limitations

- Mozambique's localisation uses the undefined source tag `MBZ`, while `common/country_tags/00_countries.txt:119` defines `MZB` as Mozambique. The six new presets use producer `MZB`; legacy `MBZ` localisation keys, paths and raw provenance remain unchanged. The manifest records this source-tag alias explicitly. No OOB request uses `MBZ`.
- Restrict authored bookmark national presets to OOB chassis union apc0..4 and ifv0..4; future tiers preserved separately.
- Country-specific national localisation overrides consolidated keys.
- ALB and MBZ repeated IFV3 choose first BMP-1; BMP-1P duplication retained in provenance, no legacy loc correction.
- ASCII NFKD transliteration and surrounding-whitespace trimming for new names.
- Undefined heavy_mechanized_equipment_1/3 corrected to mechanized_heavy_equipment_1/3, hence ifv0/2.
- Producer resolution uses explicit producer > creator > owner > filename tag, independent of token order; all original scope fields preserved.
- Producer precedence is independent of token order. The main review used the installed vanilla FRA/YUG owner/creator example to resolve the previous validator disagreement; both variant identity and bootstrap use the same producer resolution.
- Country-specific sources win because they carry the country's detailed ladder. ALB and MBZ duplicate IFV tier-3 entries choose the first BMP-1, consistent with the tier-3 ladder elsewhere; their duplicate BMP-1P source entries remain in provenance. TUR's country-specific ladder wins over consolidated localisation. Existing localisation is preserved.
- Historical names do not imply exact historical configurations. Every APC preset uses the unarmed baseline firing ports, open troop bay, half-track suspension, welded armor and gasoline engine. Every IFV uses its tier's autocannon, fighting compartment, bogie suspension, welded armor, gasoline engine, AP and HE ammunition. All fifteen slots are explicit, and engine/armor upgrades are zero. These conservative functional recipes are authored approximations; balance calibration and live-game behavior remain untested.
- National creation is split into ten per-hull helpers. The caller interleaves national and generic creation for each ascending hull, with each family contiguous. Calling all national tiers before all generic fallbacks would create an older generic design after a newer national design for tags with gaps, violating newest-only obsolescence. Shared per-chassis flags also prevent generic duplicate creation.
- Each national design requires NSB, its producer tag, its hull technology and an unset per-chassis creation flag. The historical initialization effect deliberately permits modules without separate technology checks, matching the established bookmark pattern.

## Selected national mapping

| Producer | Chassis | Historical name | Legacy localisation key | Source |
| --- | --- | --- | --- | --- |
| ADR | apc_chassis_0 | Sd.Kfz. 251/1 W/ IR | ADR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:89 |
| ADR | apc_chassis_1 | OT-810 | ADR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:91 |
| ADR | apc_chassis_2 | BTR-60PB | ADR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:93 |
| ADR | apc_chassis_3 | OT-64A | ADR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:95 |
| ADR | apc_chassis_4 | OT-64B | ADR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:97 |
| ADR | ifv_chassis_0 | BTR-152 | ADR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:106 |
| ADR | ifv_chassis_1 | BTR-50P | ADR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:108 |
| ADR | ifv_chassis_2 | BTR-50PK | ADR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:110 |
| ADR | ifv_chassis_3 | BMP-1 | ADR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:112 |
| ADR | ifv_chassis_4 | BMP-1P | ADR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/ADR_equipment_l_english .yml:114 |
| AFG | apc_chassis_0 | BTR-40 | AFG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:80 |
| AFG | apc_chassis_1 | BTR-40B | AFG_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:82 |
| AFG | apc_chassis_2 | BTR-60P | AFG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:84 |
| AFG | apc_chassis_3 | BTR-60PB | AFG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:86 |
| AFG | apc_chassis_4 | BTR-70 | AFG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:88 |
| AFG | ifv_chassis_0 | BTR-152 | AFG_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:95 |
| AFG | ifv_chassis_1 | BTR-50P | AFG_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:97 |
| AFG | ifv_chassis_2 | BTR-50PK | AFG_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:99 |
| AFG | ifv_chassis_3 | BMP-1 | AFG_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:101 |
| AFG | ifv_chassis_4 | BMP-1P | AFG_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/AFG_equipment_l_english.yml:103 |
| ALB | apc_chassis_0 | BTR-40 | ALB_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:51 |
| ALB | apc_chassis_1 | BTR-40B | ALB_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:53 |
| ALB | apc_chassis_2 | Type 531 | ALB_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:55 |
| ALB | apc_chassis_3 | Type 63 | ALB_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:57 |
| ALB | apc_chassis_4 | Type 85 | ALB_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:59 |
| ALB | ifv_chassis_0 | BTR-152 | ALB_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:62 |
| ALB | ifv_chassis_1 | BTR-50PK | ALB_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:64 |
| ALB | ifv_chassis_2 | MT-LB | ALB_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:66 |
| ALB | ifv_chassis_3 | BMP-1 | ALB_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/ALB_equipment_l_english.yml:68 |
| ALG | apc_chassis_0 | BTR-40 | ALG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:56 |
| ALG | apc_chassis_1 | BTR-40B | ALG_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:58 |
| ALG | apc_chassis_2 | BTR-60P | ALG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:60 |
| ALG | apc_chassis_3 | Panhard M3 VTT | ALG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:62 |
| ALG | apc_chassis_4 | OT-64B | ALG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:64 |
| ALG | ifv_chassis_0 | BTR-152 | ALG_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:73 |
| ALG | ifv_chassis_1 | BTR-50P | ALG_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:75 |
| ALG | ifv_chassis_2 | BTR-50PK | ALG_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:77 |
| ALG | ifv_chassis_3 | BMP-1 | ALG_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:79 |
| ALG | ifv_chassis_4 | BMP-1P | ALG_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/ALG_equipment_l_english.yml:81 |
| ANG | apc_chassis_0 | BTR-40 | ANG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:33 |
| ANG | apc_chassis_1 | BTR-40B | ANG_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:35 |
| ANG | apc_chassis_2 | BTR-60P | ANG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:37 |
| ANG | apc_chassis_3 | BTR-60PB | ANG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:39 |
| ANG | apc_chassis_4 | Engesa EE-11 Urutu | ANG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:41 |
| ANG | ifv_chassis_0 | BTR-152 | ANG_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:46 |
| ANG | ifv_chassis_3 | BMP-1 | ANG_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:49 |
| ANG | ifv_chassis_4 | BMP-1P | ANG_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/ANG_equipment_l_english.yml:51 |
| ARG | apc_chassis_0 | M3A1 Half-Track | ARG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ARG_equipment_l_english.yml:65 |
| ARG | apc_chassis_2 | AMX-VCI | ARG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ARG_equipment_l_english.yml:70 |
| ARG | apc_chassis_3 | M113A1 | ARG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ARG_equipment_l_english.yml:72 |
| ARG | apc_chassis_4 | MOWAG Grenadier | ARG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ARG_equipment_l_english.yml:74 |
| AST | apc_chassis_0 | Loyd Carrier | AST_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1155 |
| AST | apc_chassis_1 | FV603 Saracen | AST_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1157 |
| AST | apc_chassis_2 | M113 | AST_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1159 |
| AST | apc_chassis_3 | M113A1 | AST_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1161 |
| AST | apc_chassis_4 | M113A1 LRV | AST_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1163 |
| AUS | apc_chassis_1 | Saurer 4K 4F | AUS_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/AUS_equipment_l_english.yml:63 |
| AUS | apc_chassis_2 | Saurer 4K 3FA | AUS_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/AUS_equipment_l_english.yml:65 |
| AUS | apc_chassis_3 | Saurer 4K 4FA | AUS_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/AUS_equipment_l_english.yml:67 |
| AUS | apc_chassis_4 | Steyr 4K 7FA | AUS_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/AUS_equipment_l_english.yml:69 |
| BAN | apc_chassis_4 | BTR-70 | BAN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/BAN_equipment_l_english.yml:45 |
| BEL | apc_chassis_0 | Loyd Carrier | BEL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:800 |
| BEL | apc_chassis_1 | M59 | BEL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:802 |
| BEL | apc_chassis_2 | AMX-VTP | BEL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:805 |
| BEL | apc_chassis_3 | M113-B | BEL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:807 |
| BEL | apc_chassis_4 | AIFV-B-.50 | BEL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:809 |
| BEL | ifv_chassis_1 | M75 | BEL_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:822 |
| BEL | ifv_chassis_4 | FMC AIFV-B-C25 | BEL_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:825 |
| BRA | apc_chassis_0 | M3A1 Half-Track | BRA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/BRA_equipment_l_english.yml:65 |
| BRA | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | BRA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/BRA_equipment_l_english.yml:68 |
| BRA | apc_chassis_2 | M113 | BRA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/BRA_equipment_l_english.yml:70 |
| BRA | apc_chassis_3 | M113A1 | BRA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/BRA_equipment_l_english.yml:72 |
| BRA | apc_chassis_4 | Engesa EE-11 Urutu | BRA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/BRA_equipment_l_english.yml:74 |
| BRM | apc_chassis_0 | Humber Pig | BRM_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/BRM_equipment_l_english.yml:63 |
| BRM | apc_chassis_3 | Type 63 | BRM_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/BRM_equipment_l_english.yml:69 |
| BRM | apc_chassis_4 | Type 85 | BRM_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/BRM_equipment_l_english.yml:71 |
| BRM | ifv_chassis_4 | Type 86A | BRM_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/BRM_equipment_l_english.yml:80 |
| BUL | apc_chassis_0 | BTR-40 | BUL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:86 |
| BUL | apc_chassis_1 | BTR-40B | BUL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:89 |
| BUL | apc_chassis_2 | BTR-60P | BUL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:92 |
| BUL | apc_chassis_3 | BTR-60PB | BUL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:95 |
| BUL | apc_chassis_4 | BTR-60PBZ | BUL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:98 |
| BUL | ifv_chassis_0 | BTR-152 | BUL_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:113 |
| BUL | ifv_chassis_1 | BTR-50PK | BUL_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:115 |
| BUL | ifv_chassis_2 | MT-LB | BUL_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:118 |
| BUL | ifv_chassis_3 | BMP-1 | BUL_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:120 |
| BUL | ifv_chassis_4 | MT-LB-M1 | BUL_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/BUL_equipment_l_english.yml:122 |
| CAN | apc_chassis_0 | Kangaroo | CAN_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/CAN_Equipment_l_english.yml:22 |
| CAN | apc_chassis_1 | M9 Halftrack | CAN_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/CAN_Equipment_l_english.yml:24 |
| CAN | apc_chassis_2 | M113 | CAN_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/CAN_Equipment_l_english.yml:26 |
| CAN | apc_chassis_3 | M113A1 | CAN_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/CAN_Equipment_l_english.yml:29 |
| CAN | apc_chassis_4 | LAV I Grizzly | CAN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/CAN_Equipment_l_english.yml:32 |
| CAP | apc_chassis_0 | M3A1 Half-Track | CAP_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:105 |
| CAP | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | CAP_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:108 |
| CAP | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | CAP_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:111 |
| CAP | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | CAP_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:114 |
| CAP | apc_chassis_4 | Carrier, Personnel, Full Tracked, Armored, M113A2 | CAP_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:117 |
| CAP | ifv_chassis_0 | M44 | CAP_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:130 |
| CAP | ifv_chassis_1 | Carrier, Personnal, Full Tracked, Armored, M75 | CAP_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:133 |
| CAP | ifv_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 ACAV | CAP_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:136 |
| CAP | ifv_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 ACAV | CAP_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:139 |
| CAP | ifv_chassis_4 | M2 Bradley | CAP_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:142 |
| CHI | apc_chassis_0 | Carrier, Personnel, Half-track, M5 | CHI_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:267 |
| CHI | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | CHI_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:271 |
| CHI | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | CHI_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:273 |
| CHI | apc_chassis_4 | Carrier, Personnel, Full Tracked, Armored, M113A2 | CHI_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:276 |
| CHL | apc_chassis_0 | M3A1 Half-Track | CHL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/CHL_equipment_l_english.yml:62 |
| CHL | apc_chassis_2 | M113 | CHL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/CHL_equipment_l_english.yml:67 |
| CHL | apc_chassis_3 | M113A1 | CHL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/CHL_equipment_l_english.yml:69 |
| COL | apc_chassis_0 | M3A1 Half-Track | COL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/COL_equipment_l_english.yml:42 |
| COL | apc_chassis_1 | REO M35 'Meteoro' | COL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/COL_equipment_l_english.yml:45 |
| COL | apc_chassis_2 | M113 | COL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/COL_equipment_l_english.yml:47 |
| COL | apc_chassis_3 | M113A1 | COL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/COL_equipment_l_english.yml:49 |
| COL | apc_chassis_4 | Engesa EE-11 Urutu | COL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/COL_equipment_l_english.yml:51 |
| CUB | apc_chassis_0 | M3A1 Half-Track | CUB_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:63 |
| CUB | apc_chassis_1 | BTR-40B | CUB_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:66 |
| CUB | apc_chassis_2 | BTR-60P | CUB_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:68 |
| CUB | apc_chassis_3 | BTR-60PB | CUB_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:70 |
| CUB | apc_chassis_4 | BTR-70 | CUB_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:72 |
| CUB | ifv_chassis_0 | BTR-152 | CUB_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:77 |
| CUB | ifv_chassis_3 | BMP-1 | CUB_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:79 |
| CUB | ifv_chassis_4 | BMP-1M | CUB_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/CUB_equipment_l_english.yml:81 |
| CUM | apc_chassis_0 | BTR-40 | CUM_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1178 |
| CUM | apc_chassis_1 | BTR-40B | CUM_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1180 |
| CUM | apc_chassis_2 | BTR-60P | CUM_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1182 |
| CUM | apc_chassis_3 | BTR-60PB | CUM_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1184 |
| CUM | apc_chassis_4 | BTR-70 | CUM_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1186 |
| CUM | ifv_chassis_0 | BTR-152 | CUM_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1195 |
| CUM | ifv_chassis_1 | BTR-50P | CUM_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1197 |
| CUM | ifv_chassis_2 | BTR-50PK | CUM_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1199 |
| CUM | ifv_chassis_3 | BMP-1 | CUM_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1201 |
| CUM | ifv_chassis_4 | BMP-1P | CUM_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/armtrader_l_english.yml:1203 |
| CYP | apc_chassis_3 | FMC M113A1 | CYP_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/CYP_equipment_l_english.yml:74 |
| CYP | apc_chassis_4 | Engesa EE-11 Urutu | CYP_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/CYP_equipment_l_english.yml:76 |
| CYP | ifv_chassis_0 | BTR-152 | CYP_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/CYP_equipment_l_english.yml:85 |
| CYP | ifv_chassis_1 | BTR-152V1 | CYP_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/CYP_equipment_l_english.yml:87 |
| CYP | ifv_chassis_2 | AMX-VCI 12.7 | CYP_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/CYP_equipment_l_english.yml:89 |
| CYP | ifv_chassis_3 | AMX-VCI M.56 | CYP_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/CYP_equipment_l_english.yml:91 |
| CZE | apc_chassis_0 | Sd.Kfz. 251/1 W/ IR | CZE_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:84 |
| CZE | apc_chassis_1 | OT-810 | CZE_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:86 |
| CZE | apc_chassis_2 | OT-66 | CZE_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:88 |
| CZE | apc_chassis_3 | OT-64A | CZE_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:90 |
| CZE | apc_chassis_4 | OT-64B | CZE_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:92 |
| CZE | ifv_chassis_0 | Sd.Kfz. 251/16 | CZE_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:101 |
| CZE | ifv_chassis_1 | OT-62A | CZE_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:103 |
| CZE | ifv_chassis_2 | OT-62B | CZE_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:105 |
| CZE | ifv_chassis_3 | BVP-1 | CZE_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:107 |
| CZE | ifv_chassis_4 | BVP-1P | CZE_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/CZE_equipment_country_l_english.yml:109 |
| DDR | apc_chassis_0 | BTR-40 | DDR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1217 |
| DDR | apc_chassis_1 | BTR-40B | DDR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1219 |
| DDR | apc_chassis_2 | SPW-60P | DDR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1221 |
| DDR | apc_chassis_3 | SPW-60PB | DDR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1223 |
| DDR | apc_chassis_4 | SPW-70 | DDR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1225 |
| DDR | ifv_chassis_0 | SPW-152 | DDR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1234 |
| DDR | ifv_chassis_1 | SPW-50PK | DDR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1236 |
| DDR | ifv_chassis_2 | MZTM MT-LB | DDR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1238 |
| DDR | ifv_chassis_3 | SPz BMP-1 | DDR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1240 |
| DDR | ifv_chassis_4 | SPz BMP-1 SP-2 | DDR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/DDR_l_english.yml:1242 |
| DEN | apc_chassis_0 | M6 Mosegris | DEN_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4905 |
| DEN | apc_chassis_1 | FMC M59 | DEN_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4907 |
| DEN | apc_chassis_2 | FMC M113 | DEN_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4909 |
| DEN | apc_chassis_3 | M113A2 | DEN_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4911 |
| DEN | apc_chassis_4 | M113G1DK | DEN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4913 |
| EGY | apc_chassis_0 | BTR-40 | EGY_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:70 |
| EGY | apc_chassis_1 | BTR-40B | EGY_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:72 |
| EGY | apc_chassis_2 | BTR-60P | EGY_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:74 |
| EGY | apc_chassis_3 | BTR-60PB | EGY_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:76 |
| EGY | apc_chassis_4 | OT-64B | EGY_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:78 |
| EGY | ifv_chassis_0 | BTR-152 | EGY_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:87 |
| EGY | ifv_chassis_1 | BTR-50P | EGY_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:89 |
| EGY | ifv_chassis_2 | BTR-50PK | EGY_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:91 |
| EGY | ifv_chassis_3 | BMP-1 | EGY_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:93 |
| EGY | ifv_chassis_4 | BMP-1P | EGY_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/EGY_equipment_l_english.yml:95 |
| ENG | apc_chassis_0 | Humber Pig | ENG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1575 |
| ENG | apc_chassis_1 | FV603 Saracen | ENG_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1577 |
| ENG | apc_chassis_2 | FV432 | ENG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1579 |
| ENG | apc_chassis_3 | FV432 Mk.2 | ENG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1581 |
| ENG | apc_chassis_4 | FV103 Spartan | ENG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1583 |
| ENG | ifv_chassis_0 | Churchill Kangaroo | ENG_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1592 |
| ENG | ifv_chassis_4 | FV432 Rarden | ENG_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1594 |
| FIN | apc_chassis_0 | Sd.Kfz. 251/1 W/ IR | FIN_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:59 |
| FIN | apc_chassis_1 | BTR-40 | FIN_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:61 |
| FIN | apc_chassis_2 | BTR-60PA | FIN_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:63 |
| FIN | apc_chassis_3 | BTR-60PB | FIN_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:65 |
| FIN | apc_chassis_4 | BTR-60PZ | FIN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:67 |
| FIN | ifv_chassis_0 | Sd.Kfz. 251/16 | FIN_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:76 |
| FIN | ifv_chassis_1 | BTR-50P | FIN_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:78 |
| FIN | ifv_chassis_2 | BTR-50PK | FIN_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:80 |
| FIN | ifv_chassis_3 | MT-LB | FIN_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:82 |
| FIN | ifv_chassis_4 | BMP-1 | FIN_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/FIN_equipment_country_l_english.yml:84 |
| FRA | apc_chassis_0 | M9 Halftrack | FRA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2002 |
| FRA | apc_chassis_1 | Hotchkiss TT6 | FRA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2004 |
| FRA | apc_chassis_2 | AMX-VTP | FRA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2006 |
| FRA | apc_chassis_3 | AMX-VTT | FRA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2008 |
| FRA | apc_chassis_4 | VAB VTT | FRA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2010 |
| FRA | ifv_chassis_2 | AMX-VCI 12.7 | FRA_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2019 |
| FRA | ifv_chassis_3 | AMX-VCI M.56 | FRA_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2021 |
| FRA | ifv_chassis_4 | AMX-10P | FRA_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2023 |
| GRE | apc_chassis_0 | Loyd Carrier | GRE_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/GRE_equipment_l_english.yml:32 |
| GRE | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | GRE_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/GRE_equipment_l_english.yml:34 |
| GRE | apc_chassis_2 | M113 | GRE_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/GRE_equipment_l_english.yml:37 |
| GRE | apc_chassis_3 | M113A2 | GRE_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/GRE_equipment_l_english.yml:39 |
| GRE | apc_chassis_4 | ELVO Leonidas 1 | GRE_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/GRE_equipment_l_english.yml:41 |
| HOL | apc_chassis_0 | Loyd Carrier | HOL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2266 |
| HOL | apc_chassis_1 | Hotchkiss TT6 | HOL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2268 |
| HOL | apc_chassis_2 | FMC M113 | HOL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2270 |
| HOL | apc_chassis_3 | YP-408 PWI | HOL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2272 |
| HOL | apc_chassis_4 | YPR-765 pri .50 | HOL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2274 |
| HOL | ifv_chassis_2 | AMX-PRI | HOL_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2249 |
| HOL | ifv_chassis_3 | DAF YP-408 C&V | HOL_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2251 |
| HOL | ifv_chassis_4 | FMC YPR-765 PRI 25KBA | HOL_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2253 |
| HUN | apc_chassis_0 | BTR-40 | HUN_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:70 |
| HUN | apc_chassis_1 | BTR-40B | HUN_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:72 |
| HUN | apc_chassis_2 | PSzH | HUN_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:74 |
| HUN | apc_chassis_3 | D-944 PSzH-IV | HUN_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:76 |
| HUN | apc_chassis_4 | BTR-70 | HUN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:78 |
| HUN | ifv_chassis_0 | BTR-152 | HUN_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:87 |
| HUN | ifv_chassis_1 | BTR-50P | HUN_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:89 |
| HUN | ifv_chassis_2 | BTR-50PK | HUN_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:91 |
| HUN | ifv_chassis_3 | BMP-1 | HUN_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:93 |
| HUN | ifv_chassis_4 | BMP-1P | HUN_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/HUN_equipment_country_l_english.yml:95 |
| IND | ifv_chassis_1 | Sonderkraftfahrzeug 251 Half-Track | IND_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/research_country_l_english.yml:1209 |
| INO | apc_chassis_0 | BTR-40 | INO_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:88 |
| INO | apc_chassis_1 | FV603 Saracen | INO_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:90 |
| INO | apc_chassis_2 | AMX-VCI | INO_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:92 |
| INO | apc_chassis_3 | M113-B | INO_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:94 |
| INO | apc_chassis_4 | Cadilac Gage Commando V-150 APC | INO_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:96 |
| INO | ifv_chassis_0 | BTR-152 | INO_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:105 |
| INO | ifv_chassis_1 | BTR-50P | INO_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:107 |
| INO | ifv_chassis_2 | BTR-50PK | INO_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:109 |
| INS | apc_chassis_0 | Loyd Carrier | INS_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:189 |
| IRE | apc_chassis_0 | Scania M41 APC | IRE_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/IRE_equipment_l_english.yml:66 |
| IRE | apc_chassis_2 | FMC M113 | IRE_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/IRE_equipment_l_english.yml:69 |
| IRE | apc_chassis_3 | Panhard M3 VTT | IRE_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/IRE_equipment_l_english.yml:72 |
| IRE | apc_chassis_4 | Timoney Mk IV APC | IRE_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/IRE_equipment_l_english.yml:75 |
| IRQ | apc_chassis_0 | BTR-40 | IRQ_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:66 |
| IRQ | apc_chassis_1 | BTR-40B | IRQ_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:68 |
| IRQ | apc_chassis_2 | BTR-60P | IRQ_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:70 |
| IRQ | apc_chassis_3 | Panhard M3 VTT | IRQ_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:72 |
| IRQ | apc_chassis_4 | Engesa EE-11 Urutu | IRQ_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:74 |
| IRQ | ifv_chassis_0 | BTR-152 | IRQ_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:83 |
| IRQ | ifv_chassis_1 | BTR-50P | IRQ_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:85 |
| IRQ | ifv_chassis_2 | BTR-50PK | IRQ_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:87 |
| IRQ | ifv_chassis_3 | BMP-1 | IRQ_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:89 |
| IRQ | ifv_chassis_4 | AMX-10P | IRQ_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/IRQ_equipment_l_english.yml:91 |
| ISR | apc_chassis_0 | Zachlam M9 | ISR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1296 |
| ISR | apc_chassis_1 | Zachlam M9A1 | ISR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1298 |
| ISR | apc_chassis_2 | Nimda Shoet | ISR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1300 |
| ISR | apc_chassis_3 | M113 Nagmash | ISR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1302 |
| ISR | apc_chassis_4 | M113 Vayzata | ISR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1304 |
| ISR | ifv_chassis_0 | BTR-152 | ISR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1313 |
| ISR | ifv_chassis_1 | BTR-50PK | ISR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1315 |
| ISR | ifv_chassis_2 | Uparmored Zachlam M3 | ISR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1317 |
| ISR | ifv_chassis_3 | Uparmored Zachlam M9 w/20mm HS.404 | ISR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1319 |
| ISR | ifv_chassis_4 | M113 Nagman | ISR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1321 |
| ITA | apc_chassis_0 | M5 Half-Track | ITA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:49 |
| ITA | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | ITA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:52 |
| ITA | apc_chassis_2 | M113 | ITA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:55 |
| ITA | apc_chassis_3 | M113A2 | ITA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:57 |
| ITA | apc_chassis_4 | Fiat Type 6614 | ITA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:59 |
| ITA | ifv_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 ACAV | ITA_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:69 |
| ITA | ifv_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 ACAV | ITA_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:72 |
| ITA | ifv_chassis_4 | OTO-Melara VCC-1 Camilino | ITA_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/ITA_equipment_l_english.yml:75 |
| JAP | apc_chassis_0 | M5 Half-Track | JAP_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:464 |
| JAP | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | JAP_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:467 |
| JAP | apc_chassis_2 | Komatsu Type 60 Roku-Maru-Shiki | JAP_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:470 |
| JAP | apc_chassis_3 | Komatsu Type 60 Kai Roku-Maru-Shiki | JAP_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:473 |
| JAP | apc_chassis_4 | Mitsubishi Type 73 Nana-San-Shiki | JAP_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:476 |
| JOR | apc_chassis_1 | FV603 Saracen | JOR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/JOR_equipment_l_english.yml:82 |
| JOR | apc_chassis_2 | M113 | JOR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/JOR_equipment_l_english.yml:84 |
| JOR | apc_chassis_3 | M113A1 | JOR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/JOR_equipment_l_english.yml:87 |
| JOR | apc_chassis_4 | FV103 Spartan | JOR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/JOR_equipment_l_english.yml:90 |
| KOR | apc_chassis_0 | Carrier, Personnel, Half-track, M3A1 | KOR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:84 |
| KOR | apc_chassis_1 | Carrier, Personnel, Half-track, M9 | KOR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:87 |
| KOR | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, KM113 | KOR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:89 |
| KOR | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, KM113A1 | KOR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:92 |
| KOR | apc_chassis_4 | Carrier, Personnel, Wheeled, 4X4, Armored, KM900 | KOR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:95 |
| KOR | ifv_chassis_0 | Carrier, Personnel, Wheeled, 6X6, Armored, M8 | KOR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:104 |
| KOR | ifv_chassis_1 | Carrier, Personnal, Full Tracked, Armored, M75 | KOR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:106 |
| KOR | ifv_chassis_2 | Carrier, Personnel, Full Tracked, Armored, KM113 ACAV | KOR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:109 |
| KOR | ifv_chassis_3 | Carrier, Personnel, Full Tracked, Armored, KM113A1 ACAV | KOR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:112 |
| KOR | ifv_chassis_4 | Carrier, Personnel, Full Tracked, Armored, KM113A2 ACAV | KOR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/KOR_equipment_l_english.yml:115 |
| KPA | apc_chassis_0 | Type 55 | KPA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3938 |
| KPA | apc_chassis_1 | BTR-152 | KPA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3940 |
| KPA | apc_chassis_2 | BTR-152V | KPA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3942 |
| KPA | apc_chassis_3 | BTR-60PB | KPA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3944 |
| KPA | apc_chassis_4 | M1992 | KPA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3946 |
| KPA | ifv_chassis_0 | BTR-40A | KPA_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3951 |
| KPA | ifv_chassis_1 | BTR-50PK | KPA_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3953 |
| KPA | ifv_chassis_2 | MT-LB | KPA_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3955 |
| KPA | ifv_chassis_3 | Korshun | KPA_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3957 |
| KPA | ifv_chassis_4 | VTT-323 M1973 Sinhung | KPA_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3959 |
| KUW | apc_chassis_1 | FV603 Saracen | KUW_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/KUW_equip_l_english.yml:63 |
| KUW | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | KUW_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/KUW_equip_l_english.yml:65 |
| KUW | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | KUW_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/KUW_equip_l_english.yml:67 |
| KUW | apc_chassis_4 | Cadilac Gage Commando V-150 APC | KUW_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/KUW_equip_l_english.yml:69 |
| LBA | apc_chassis_0 | Loyd Carrier | LBA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:57 |
| LBA | apc_chassis_1 | BTR-40B | LBA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:59 |
| LBA | apc_chassis_2 | BTR-60P | LBA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:61 |
| LBA | apc_chassis_3 | M113A1 | LBA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:63 |
| LBA | apc_chassis_4 | Fiat Type 6614 | LBA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:65 |
| LBA | ifv_chassis_0 | BTR-152 | LBA_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:68 |
| LBA | ifv_chassis_1 | BTR-50P | LBA_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:70 |
| LBA | ifv_chassis_2 | BTR-50PK | LBA_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:72 |
| LBA | ifv_chassis_3 | BMP-1 | LBA_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/LBA_equipment_l_english.yml:74 |
| LEB | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | LEB_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/LEB_equipment_l_english.yml:55 |
| LEB | apc_chassis_2 | AMX-VCI | LEB_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/LEB_equipment_l_english.yml:57 |
| LEB | apc_chassis_3 | M113A1 | LEB_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/LEB_equipment_l_english.yml:59 |
| LEB | apc_chassis_4 | Carrier, Personnel, Full Tracked, Armored, M113A2 | LEB_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/LEB_equipment_l_english.yml:62 |
| LUX | apc_chassis_0 | Loyd Carrier | LUX_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/LUX_equipment_l_english.yml:48 |
| MAL | apc_chassis_0 | General Motors Canada C15TA, Truck, 4.5t, Armoured | MAL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/MAL_l_english.yml:419 |
| MAL | apc_chassis_1 | FV603 Saracen | MAL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/MAL_l_english.yml:421 |
| MAL | apc_chassis_2 | Bedford RL 'Pig' APC | MAL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/MAL_l_english.yml:423 |
| MAL | apc_chassis_3 | Panhard M3 VTT | MAL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/MAL_l_english.yml:425 |
| MAL | apc_chassis_4 | Thyssen-Henschel Condor | MAL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/MAL_l_english.yml:427 |
| MAO | apc_chassis_3 | YW531 | MAO_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/research_country_l_english.yml:1059 |
| MAO | ifv_chassis_3 | WZ-501 | MAO_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/research_country_l_english.yml:1063 |
| MZB | apc_chassis_0 | BTR-40 | MBZ_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/MBZ_equipment_l_english.yml:25 |
| MZB | apc_chassis_1 | BTR-40B | MBZ_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/MBZ_equipment_l_english.yml:27 |
| MZB | apc_chassis_2 | BTR-60P | MBZ_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/MBZ_equipment_l_english.yml:29 |
| MZB | apc_chassis_3 | BTR-60PB | MBZ_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/MBZ_equipment_l_english.yml:31 |
| MZB | ifv_chassis_0 | BTR-152 | MBZ_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/MBZ_equipment_l_english.yml:34 |
| MZB | ifv_chassis_3 | BMP-1 | MBZ_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/MBZ_equipment_l_english.yml:37 |
| MEX | apc_chassis_0 | M3A1 Half-Track | MEX_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/MEX_equipment_l_english.yml:41 |
| MEX | apc_chassis_2 | AMX-VCI | MEX_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/MEX_equipment_l_english.yml:46 |
| MEX | apc_chassis_3 | Sedena-Henschel HWK-11 Mk1 | MEX_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/MEX_equipment_l_english.yml:48 |
| MEX | apc_chassis_4 | Sedena DN-3 Caballo | MEX_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/MEX_equipment_l_english.yml:50 |
| MLA | apc_chassis_0 | General Motors Canada C15TA, Truck, 4.5t, Armoured | MLA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/MLA_l_english.yml:1254 |
| MLA | apc_chassis_1 | BTR-40B | MLA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/MLA_l_english.yml:1256 |
| MLA | apc_chassis_2 | BTR-60P | MLA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/MLA_l_english.yml:1258 |
| MON | apc_chassis_0 | BTR-40 | MON_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:92 |
| MON | apc_chassis_1 | BTR-40B | MON_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:94 |
| MON | apc_chassis_2 | BTR-60P | MON_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:96 |
| MON | apc_chassis_3 | BTR-60PB | MON_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:98 |
| MON | apc_chassis_4 | BTR-70 | MON_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:100 |
| MON | ifv_chassis_0 | BTR-152 | MON_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:109 |
| MON | ifv_chassis_1 | BTR-50P | MON_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:111 |
| MON | ifv_chassis_2 | BTR-50PK | MON_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:113 |
| MON | ifv_chassis_3 | BMP-1 | MON_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:115 |
| MON | ifv_chassis_4 | BMP-1P | MON_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/MON_equipment_l_english.yml:117 |
| MOR | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | MOR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/MOR_equip_l_english.yml:69 |
| MOR | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | MOR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/MOR_equip_l_english.yml:71 |
| MOR | apc_chassis_4 | AIFV-B-.50 | MOR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/MOR_equip_l_english.yml:73 |
| NLF | apc_chassis_0 | BTR-40 | NLF_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:80 |
| NLF | apc_chassis_1 | BTR-40B | NLF_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:82 |
| NLF | apc_chassis_2 | BTR-60P | NLF_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:84 |
| NLF | apc_chassis_3 | BTR-60PB | NLF_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:86 |
| NLF | apc_chassis_4 | BTR-70 | NLF_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:88 |
| NLF | ifv_chassis_0 | BTR-152 | NLF_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:97 |
| NLF | ifv_chassis_1 | BTR-50P | NLF_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:99 |
| NLF | ifv_chassis_2 | MT-LB | NLF_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:101 |
| NLF | ifv_chassis_3 | M113A1 ACAV | NLF_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:103 |
| NLF | ifv_chassis_4 | BMP-1P | NLF_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/NLF_equipment_l_english.yml:106 |
| NOR | apc_chassis_0 | Loyd Carrier | NOR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4697 |
| NOR | apc_chassis_1 | FMC M59 | NOR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4699 |
| NOR | apc_chassis_2 | FMC M113 | NOR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4701 |
| NOR | apc_chassis_3 | M113F1 | NOR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4703 |
| NOR | apc_chassis_4 | M113F2 | NOR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4705 |
| NZL | apc_chassis_0 | Loyd Carrier | NZL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/NZL_equipment_l_english.yml:56 |
| NZL | apc_chassis_1 | FV603 Saracen | NZL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/NZL_equipment_l_english.yml:58 |
| NZL | apc_chassis_2 | M113 | NZL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/NZL_equipment_l_english.yml:60 |
| NZL | apc_chassis_3 | M113A1 | NZL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/NZL_equipment_l_english.yml:62 |
| NZL | apc_chassis_4 | M113A1 LRV | NZL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/NZL_equipment_l_english.yml:64 |
| PAK | apc_chassis_2 | M113 | PAK_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/PAK_equipment_l_english.yml:63 |
| PAK | apc_chassis_3 | M113A1 | PAK_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/PAK_equipment_l_english.yml:65 |
| PAK | apc_chassis_4 | BTR-70 | PAK_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/PAK_equipment_l_english.yml:67 |
| PDG | apc_chassis_0 | BTR-40 | PDG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:62 |
| PDG | apc_chassis_1 | BTR-40B | PDG_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:64 |
| PDG | apc_chassis_2 | BTR-60 | PDG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:66 |
| PDG | apc_chassis_3 | BTR-60PB | PDG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:68 |
| PDG | apc_chassis_4 | ELVO Leonidas 1 | PDG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:70 |
| PDG | ifv_chassis_0 | BTR-152 | PDG_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:79 |
| PDG | ifv_chassis_1 | BTR-50P | PDG_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:81 |
| PDG | ifv_chassis_2 | BTR-50PK | PDG_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:83 |
| PDG | ifv_chassis_3 | BMP-1 | PDG_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:85 |
| PDG | ifv_chassis_4 | BMP-1P | PDG_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/PDG_equipment_l_english.yml:87 |
| PER | apc_chassis_0 | General Motors Canada C15TA, Truck, 4.5t, Armoured | PER_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/PER_equipment_l_english.yml:72 |
| PER | apc_chassis_2 | M113 | PER_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/PER_equipment_l_english.yml:76 |
| PER | apc_chassis_3 | M113A1 | PER_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/PER_equipment_l_english.yml:78 |
| PER | apc_chassis_4 | Engesa EE-11 Urutu | PER_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/PER_equipment_l_english.yml:80 |
| PHI | apc_chassis_0 | M3A1 Half-Track | PHI_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/PHI_equipment_l_english.yml:49 |
| PHI | apc_chassis_1 | REO M35A1 Guntruck | PHI_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/PHI_equipment_l_english.yml:52 |
| PHI | apc_chassis_2 | M113 | PHI_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/PHI_equipment_l_english.yml:55 |
| PHI | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | PHI_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/PHI_equipment_l_english.yml:58 |
| PHI | apc_chassis_4 | Cadilac Gage Commando V-150 APC | PHI_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/PHI_equipment_l_english.yml:61 |
| PHI | ifv_chassis_4 | Carrier, Personnel, Full Tracked, Armored, M113A2 IFV | PHI_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/PHI_equipment_l_english.yml:71 |
| POL | apc_chassis_0 | BTR-40 | POL_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:91 |
| POL | apc_chassis_1 | BTR-152 | POL_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:94 |
| POL | apc_chassis_2 | BTR-152K | POL_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:97 |
| POL | apc_chassis_3 | SKOT-1 | POL_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:100 |
| POL | apc_chassis_4 | SKOT-2 | POL_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:103 |
| POL | ifv_chassis_0 | Sd.Kfz. 251/16 | POL_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:117 |
| POL | ifv_chassis_1 | TOPAS | POL_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:120 |
| POL | ifv_chassis_2 | MT-LB | POL_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:123 |
| POL | ifv_chassis_3 | BWP-1 | POL_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:126 |
| POL | ifv_chassis_4 | BWP-1P | POL_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/POL_equipment_l_english_1.yml:129 |
| POR | apc_chassis_0 | Kangaroo | POR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1031 |
| POR | apc_chassis_1 | Panhard ETT | POR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1033 |
| POR | apc_chassis_2 | FMC M113 | POR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1035 |
| POR | apc_chassis_3 | YP-408 | POR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1037 |
| POR | apc_chassis_4 | Cadillac Cage Commando V-100 | POR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:1039 |
| PRC | apc_chassis_0 | Type 55 | PRC_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4045 |
| PRC | apc_chassis_1 | Type 56 | PRC_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4047 |
| PRC | apc_chassis_2 | Type 531 | PRC_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4049 |
| PRC | apc_chassis_3 | Type 63 | PRC_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4051 |
| PRC | apc_chassis_4 | Type 85 | PRC_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4053 |
| PRC | ifv_chassis_3 | Type 86 | PRC_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4062 |
| PRC | ifv_chassis_4 | Type 85 YW-307 | PRC_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4064 |
| PRU | apc_chassis_0 | M3A1 Half-Track | PRU_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/PRU_equipment_l_english.yml:57 |
| PRU | apc_chassis_2 | BTR-60P | PRU_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/PRU_equipment_l_english.yml:62 |
| PRU | apc_chassis_3 | M113A1 | PRU_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/PRU_equipment_l_english.yml:64 |
| PRU | apc_chassis_4 | Fiat Type 6614 | PRU_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/PRU_equipment_l_english.yml:66 |
| PRU | ifv_chassis_4 | Fiat Type 6616 | PRU_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/PRU_equipment_l_english.yml:69 |
| RAJ | apc_chassis_0 | Loyd Carrier | RAJ_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:96 |
| RAJ | apc_chassis_1 | BTR-152 | RAJ_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:99 |
| RAJ | apc_chassis_2 | BTR-60 | RAJ_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:102 |
| RAJ | apc_chassis_3 | BTR-60PB | RAJ_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:105 |
| RAJ | apc_chassis_4 | OT-64B | RAJ_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:108 |
| RAJ | ifv_chassis_2 | BTR-50P | RAJ_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:122 |
| RAJ | ifv_chassis_3 | BMP-1 | RAJ_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:124 |
| RAJ | ifv_chassis_4 | BMP-1P | RAJ_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/RAJ_equipment_l_english.yml:127 |
| ROM | apc_chassis_0 | BTR-40 | ROM_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:88 |
| ROM | apc_chassis_1 | BTR-40B | ROM_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:90 |
| ROM | apc_chassis_2 | BTR-60 | ROM_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:92 |
| ROM | apc_chassis_3 | TAB-71 | ROM_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:94 |
| ROM | apc_chassis_4 | TAB-77 | ROM_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:96 |
| ROM | ifv_chassis_0 | BTR-152 | ROM_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:107 |
| ROM | ifv_chassis_1 | BTR-50PK | ROM_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:109 |
| ROM | ifv_chassis_2 | MT-LB | ROM_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:111 |
| ROM | ifv_chassis_3 | BMP-1 | ROM_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:113 |
| ROM | ifv_chassis_4 | MLI-84 | ROM_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/ROM_equipment_country_l_english.yml:115 |
| SAF | apc_chassis_0 | Loyd Carrier | SAF_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/SAF_equipment_l_english.yml:66 |
| SAF | apc_chassis_1 | FV603 Saracen | SAF_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/SAF_equipment_l_english.yml:68 |
| SAF | apc_chassis_3 | Armscor South Africa Hippo Mk1-R | SAF_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SAF_equipment_l_english.yml:71 |
| SAF | apc_chassis_4 | CSIR Buffel | SAF_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/SAF_equipment_l_english.yml:73 |
| SAF | ifv_chassis_4 | Denel Ratel 20 | SAF_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/SAF_equipment_l_english.yml:82 |
| SAU | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | SAU_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/SAU_equip_l_english.yml:61 |
| SAU | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | SAU_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SAU_equip_l_english.yml:63 |
| SAU | apc_chassis_4 | Cadilac Gage Commando V-150 APC | SAU_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/SAU_equip_l_english.yml:65 |
| SAU | ifv_chassis_4 | AMX-10P | SAU_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/SAU_equip_l_english.yml:72 |
| SGP | apc_chassis_0 | General Motors Canada C15TA, Truck, 4.5t, Armoured | SGP_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/SGP_equipment_l_english.yml:48 |
| SGP | apc_chassis_1 | FV603 Saracen | SGP_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/SGP_equipment_l_english.yml:50 |
| SGP | apc_chassis_2 | M113 | SGP_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/SGP_equipment_l_english.yml:51 |
| SGP | apc_chassis_3 | M113A1 | SGP_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SGP_equipment_l_english.yml:53 |
| SGP | apc_chassis_4 | Cadilac Gage Commando V-150 APC | SGP_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/SGP_equipment_l_english.yml:55 |
| SGP | ifv_chassis_4 | AMX-10P | SGP_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/SGP_equipment_l_english.yml:64 |
| SIA | apc_chassis_0 | M3A1 Half-Track | SIA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/SIA_equipment_l_english.yml:77 |
| SIA | apc_chassis_2 | M113 | SIA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/SIA_equipment_l_english.yml:82 |
| SIA | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | SIA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SIA_equipment_l_english.yml:85 |
| SIA | apc_chassis_4 | Type 85 | SIA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/SIA_equipment_l_english.yml:88 |
| SOV | apc_chassis_0 | BTR-40 | SOV_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3391 |
| SOV | apc_chassis_1 | BTR-40B | SOV_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3393 |
| SOV | apc_chassis_2 | BTR-60P | SOV_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3395 |
| SOV | apc_chassis_3 | BTR-60PB | SOV_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3397 |
| SOV | apc_chassis_4 | BTR-70 | SOV_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3399 |
| SOV | ifv_chassis_0 | BTR-152 | SOV_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3408 |
| SOV | ifv_chassis_1 | BTR-50P | SOV_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3410 |
| SOV | ifv_chassis_2 | BTR-50PK | SOV_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3412 |
| SOV | ifv_chassis_3 | BMP-1 | SOV_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3414 |
| SOV | ifv_chassis_4 | BMP-1P | SOV_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3416 |
| SPR | apc_chassis_2 | FMW M113 | SPR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2479 |
| SPR | apc_chassis_3 | FMW M113A2 | SPR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2482 |
| SPR | apc_chassis_4 | Pegaso 3560 BMR | SPR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2486 |
| SPR | ifv_chassis_3 | M113 ACAV | SPR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2495 |
| SWE | apc_chassis_0 | Terrangbil modell 1942 Scania Karosseri Pansar Fordonsluftvarn | SWE_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:49 |
| SWE | apc_chassis_1 | Terrangbil modell 1942 Volvo Karosseri Pansar Fordonsluftvarn | SWE_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:51 |
| SWE | apc_chassis_2 | Terrangbil modell 1942 Scania Karosseri Pansar Fordonsluftvarn Mid-life update | SWE_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:53 |
| SWE | apc_chassis_3 | Terrangbil modell 1942 Volvo Karosseri Pansar Fordonsluftvarn Mid-life update | SWE_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:55 |
| SWE | ifv_chassis_2 | Pansarbandvagn 301 | SWE_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:72 |
| SWE | ifv_chassis_3 | Pansarbandvagn 302A | SWE_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:74 |
| SWE | ifv_chassis_4 | Pansarbandvagn 302B | SWE_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/SWE_equipment_l_english.yml:76 |
| SWI | apc_chassis_1 | Hotchkiss TT6 | SWI_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/SWI_equipment_l_english.yml:54 |
| SWI | apc_chassis_2 | AMX-VTP | SWI_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/SWI_equipment_l_english.yml:56 |
| SWI | apc_chassis_3 | Schutzenpanzer 63 | SWI_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SWI_equipment_l_english.yml:58 |
| SWI | apc_chassis_4 | Schutzenpanzer 63/73 | SWI_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/SWI_equipment_l_english.yml:60 |
| SWI | ifv_chassis_2 | Saurer Tartaruga | SWI_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/SWI_equipment_l_english.yml:73 |
| SYR | apc_chassis_0 | BTR-40 | SYR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:83 |
| SYR | apc_chassis_1 | BTR-40B | SYR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:85 |
| SYR | apc_chassis_2 | BTR-60P | SYR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:87 |
| SYR | apc_chassis_3 | BTR-60PB | SYR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:89 |
| SYR | apc_chassis_4 | BTR-70 | SYR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:91 |
| SYR | ifv_chassis_0 | BTR-152 | SYR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:65 |
| SYR | ifv_chassis_1 | BTR-50P | SYR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:67 |
| SYR | ifv_chassis_2 | BTR-50PK | SYR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:69 |
| SYR | ifv_chassis_3 | BMP-1 | SYR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:71 |
| SYR | ifv_chassis_4 | BMP-1P | SYR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/SYR_equipment_l_english.yml:73 |
| TUR | apc_chassis_0 | M5 Half-Track | TUR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/TUR_equipment_l_english.yml:65 |
| TUR | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | TUR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/TUR_equipment_l_english.yml:68 |
| TUR | apc_chassis_2 | FMC M113 | TUR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/TUR_equipment_l_english.yml:71 |
| TUR | apc_chassis_3 | FMC M113A1 | TUR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/TUR_equipment_l_english.yml:73 |
| TUR | apc_chassis_4 | FMC M113A2 | TUR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/TUR_equipment_l_english.yml:75 |
| TUR | ifv_chassis_1 | M59 | TUR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:745 |
| UAE | apc_chassis_0 | General Motors Canada C15TA, Truck, 4.5t, Armoured | UAE_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:64 |
| UAE | apc_chassis_1 | FV603 Saracen | UAE_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:66 |
| UAE | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | UAE_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:69 |
| UAE | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | UAE_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:71 |
| UAE | apc_chassis_4 | Engesa EE-11 Urutu | UAE_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:73 |
| UAE | ifv_chassis_2 | AMX-VCI 12.7 | UAE_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:80 |
| UAE | ifv_chassis_3 | AMX-VCI M.56 | UAE_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:82 |
| UAE | ifv_chassis_4 | AMX-10P | UAE_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/UAE_equip_l_english.yml:84 |
| UKR | apc_chassis_0 | BTR-40 | UKR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:95 |
| UKR | apc_chassis_1 | BTR-40B | UKR_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:97 |
| UKR | apc_chassis_2 | BTR-60P | UKR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:99 |
| UKR | apc_chassis_3 | BTR-60PB | UKR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:101 |
| UKR | apc_chassis_4 | BTR-70 | UKR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:103 |
| UKR | ifv_chassis_0 | BTR-152 | UKR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:112 |
| UKR | ifv_chassis_1 | BTR-50P | UKR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:114 |
| UKR | ifv_chassis_2 | MT-LB | UKR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:116 |
| UKR | ifv_chassis_3 | BMP-1 | UKR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:118 |
| UKR | ifv_chassis_4 | BMP-1P | UKR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/UKR_equipment_l_english.yml:120 |
| USA | apc_chassis_0 | M3A1 Half-Track | USA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3035 |
| USA | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | USA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3038 |
| USA | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | USA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3041 |
| USA | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | USA_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3044 |
| USA | apc_chassis_4 | Carrier, Personnel, Full Tracked, Armored, M113A2 | USA_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3047 |
| USA | ifv_chassis_0 | M44 | USA_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3060 |
| USA | ifv_chassis_1 | Carrier, Personnal, Full Tracked, Armored, M75 | USA_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3063 |
| USA | ifv_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 ACAV | USA_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3066 |
| USA | ifv_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 ACAV | USA_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3069 |
| USA | ifv_chassis_4 | M2 Bradley | USA_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3072 |
| VEN | apc_chassis_0 | M3A1 Half-Track | VEN_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/VEN_equipment_l_english.yml:51 |
| VEN | apc_chassis_1 | Carrier, Personnel, Full Tracked, Armored, M59 | VEN_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/VEN_equipment_l_english.yml:54 |
| VEN | apc_chassis_2 | AMX-VCI | VEN_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/VEN_equipment_l_english.yml:57 |
| VEN | apc_chassis_4 | Engesa EE-11 Urutu | VEN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/VEN_equipment_l_english.yml:61 |
| VIE | apc_chassis_0 | M3A1 Half-Track | VIE_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4374 |
| VIE | apc_chassis_1 | REO M35A1 Guntruck | VIE_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4377 |
| VIE | apc_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 | VIE_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4380 |
| VIE | apc_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 | VIE_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4383 |
| VIE | apc_chassis_4 | Carrier, Personnel, Full Tracked, Armored, M113A2 | VIE_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4386 |
| VIE | ifv_chassis_0 | M44 | VIE_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4399 |
| VIE | ifv_chassis_1 | Carrier, Personnal, Full Tracked, Armored, M75 | VIE_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4402 |
| VIE | ifv_chassis_2 | Carrier, Personnel, Full Tracked, Armored, M113 ACAV | VIE_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4405 |
| VIE | ifv_chassis_3 | Carrier, Personnel, Full Tracked, Armored, M113A1 ACAV | VIE_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4408 |
| VIE | ifv_chassis_4 | M2 Bradley | VIE_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:4411 |
| VIN | apc_chassis_0 | BTR-40 | VIN_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:182 |
| VIN | apc_chassis_1 | BTR-40B | VIN_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:184 |
| VIN | apc_chassis_2 | BTR-60P | VIN_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:186 |
| VIN | apc_chassis_3 | BTR-60PB | VIN_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:188 |
| VIN | apc_chassis_4 | BTR-70 | VIN_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:190 |
| VIN | ifv_chassis_0 | BTR-152 | VIN_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:199 |
| VIN | ifv_chassis_1 | BTR-50P | VIN_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:201 |
| VIN | ifv_chassis_2 | MT-LB | VIN_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:203 |
| VIN | ifv_chassis_3 | M113A1 ACAV | VIN_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:205 |
| VIN | ifv_chassis_4 | BMP-1P | VIN_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/VIN_misc_l_english.yml:208 |
| WGR | apc_chassis_0 | M3A1 Halftrack | WGR_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2720 |
| WGR | apc_chassis_2 | Mannschaftstransportwagen M113AG | WGR_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2724 |
| WGR | apc_chassis_3 | Mannschaftstransportwagen M113A1G | WGR_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2726 |
| WGR | apc_chassis_4 | Daimler-Benz Transportpanzer Fuchs 1 | WGR_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2728 |
| WGR | ifv_chassis_0 | Hotchkiss SP1A | WGR_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2737 |
| WGR | ifv_chassis_1 | Hispano-Suiza Schutzenpanzer Lang HS.30 | WGR_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2739 |
| WGR | ifv_chassis_2 | Hispano-Suiza Schutzenpanzer Lang HS.30-3 | WGR_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2741 |
| WGR | ifv_chassis_3 | Rheinmetall Marder 1 | WGR_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2743 |
| WGR | ifv_chassis_4 | Rheinmetall Marder 1A1 | WGR_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:2745 |
| WPA | apc_chassis_0 | Loyd Carrier | WPA_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:216 |
| WPA | apc_chassis_1 | Hotchkiss TT6 | WPA_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:218 |
| WPA | apc_chassis_2 | FMC M113 | WPA_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:220 |
| WPA | ifv_chassis_2 | AMX-PRI | WPA_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/INO_equipment_l_english.yml:223 |
| YUG | apc_chassis_0 | BTR-40 | YUG_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3734 |
| YUG | apc_chassis_1 | BTR-40B | YUG_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3736 |
| YUG | apc_chassis_2 | OT M-60 | YUG_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3738 |
| YUG | apc_chassis_3 | BTR-60 | YUG_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3740 |
| YUG | apc_chassis_4 | BTR-70 | YUG_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3743 |
| YUG | ifv_chassis_0 | BTR-152 | YUG_mechanized_heavy_equipment_1 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3752 |
| YUG | ifv_chassis_1 | BTR-50PK | YUG_mechanized_heavy_equipment_2 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3754 |
| YUG | ifv_chassis_2 | MT-LB | YUG_mechanized_heavy_equipment_3 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3756 |
| YUG | ifv_chassis_3 | BVP-1 | YUG_mechanized_heavy_equipment_4 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3758 |
| YUG | ifv_chassis_4 | BVP-1P | YUG_mechanized_heavy_equipment_5 | Cold War Iron Curtain/localisation/english/equipment_country_l_english.yml:3760 |
| ZIM | apc_chassis_0 | Loyd Carrier | ZIM_mechanized_equipment_3 | Cold War Iron Curtain/localisation/english/ZIM_equipment_l_english.yml:37 |
| ZIM | apc_chassis_1 | FV603 Saracen | ZIM_mechanized_equipment_4 | Cold War Iron Curtain/localisation/english/ZIM_equipment_l_english.yml:39 |
| ZIM | apc_chassis_2 | IWM Ltd. Leopard Security Vehicle | ZIM_mechanized_equipment_5 | Cold War Iron Curtain/localisation/english/ZIM_equipment_l_english.yml:41 |
| ZIM | apc_chassis_3 | ZC Ltd. Bullet Troop-Carrying Vehicle | ZIM_mechanized_equipment_6 | Cold War Iron Curtain/localisation/english/ZIM_equipment_l_english.yml:44 |
| ZIM | apc_chassis_4 | ZC Ltd. Crocodile Troop-Carrying Vehicle | ZIM_mechanized_equipment_7 | Cold War Iron Curtain/localisation/english/ZIM_equipment_l_english.yml:46 |

## Resolved OOB mapping

Owner, creator and producer fields are preserved in the machine-readable manifest. Quantities and non-NSB files are outside the migration edits.

| OOB source | Legacy type | Chassis | Resolved producer | Variant name | Name source |
| --- | --- | --- | --- | --- | --- |
| Cold War Iron Curtain/history/units/ALG_1980_nsb.txt:248 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/ANG_1980_nsb.txt:184 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/BAN_1980_nsb.txt:367 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/BOL_1980_nsb.txt:162 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/BRA_1980_nsb.txt:425 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/BUL_1980_nsb.txt:350 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/CAN_1980_nsb.txt:227 | mechanized_equipment_6 | apc_chassis_3 | CAN | M113A1 | national |
| Cold War Iron Curtain/history/units/CAN_1980_nsb.txt:236 | mechanized_equipment_7 | apc_chassis_4 | CAN | LAV I Grizzly | national |
| Cold War Iron Curtain/history/units/CAN_1980_nsb.txt:245 | mechanized_equipment_7 | apc_chassis_4 | CAN | LAV I Grizzly | national |
| Cold War Iron Curtain/history/units/CAN_1980_nsb.txt:254 | mechanized_equipment_7 | apc_chassis_4 | CAN | LAV I Grizzly | national |
| Cold War Iron Curtain/history/units/CAN_1980_nsb.txt:384 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/CHL_1980_nsb.txt:133 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/COL_1980_nsb.txt:250 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/CUB_1980_nsb.txt:387 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/CUB_1980_nsb.txt:392 | heavy_mechanized_equipment_3 | ifv_chassis_2 | CUM | BTR-50PK | national |
| Cold War Iron Curtain/history/units/CUB_1980_nsb.txt:417 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/CZE_1980_nsb.txt:284 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/CZE_1980_nsb.txt:289 | heavy_mechanized_equipment_3 | ifv_chassis_2 | CUM | BTR-50PK | national |
| Cold War Iron Curtain/history/units/CZE_1980_nsb.txt:309 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/DDR_1980_nsb.txt:295 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/DDR_1980_nsb.txt:300 | heavy_mechanized_equipment_3 | ifv_chassis_2 | CUM | BTR-50PK | national |
| Cold War Iron Curtain/history/units/DDR_1980_nsb.txt:320 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/DEN_1980_nsb.txt:212 | mechanized_equipment_3 | apc_chassis_0 | DEN | M6 Mosegris | national |
| Cold War Iron Curtain/history/units/DRY_1980_nsb.txt:160 | mechanized_equipment_5 | apc_chassis_2 | CUM | BTR-60P | national |
| Cold War Iron Curtain/history/units/DRY_1980_nsb.txt:161 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/DRY_1980_nsb.txt:217 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/DRY_1980_nsb.txt:222 | mechanized_heavy_equipment_1 | ifv_chassis_0 | CUM | BTR-152 | national |
| Cold War Iron Curtain/history/units/DRY_1980_nsb.txt:227 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/EGY_1980_nsb.txt:456 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/ENG_1980_nsb.txt:598 | mechanized_equipment_3 | apc_chassis_0 | ENG | Humber Pig | national |
| Cold War Iron Curtain/history/units/ETH_1980_nsb.txt:249 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/GRE_1980_nsb.txt:347 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/HOL_1949_nsb.txt:423 | mechanized_equipment_3 | apc_chassis_0 | HOL | Loyd Carrier | national |
| Cold War Iron Curtain/history/units/HOL_1980_nsb.txt:435 | mechanized_equipment_3 | apc_chassis_0 | HOL | Loyd Carrier | national |
| Cold War Iron Curtain/history/units/HUN_1980_nsb.txt:227 | heavy_mechanized_equipment_1 | ifv_chassis_0 | CUM | BTR-152 | national |
| Cold War Iron Curtain/history/units/HUN_1980_nsb.txt:242 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:213 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:222 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:231 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:240 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:249 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:258 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:267 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:290 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:299 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:308 | mechanized_heavy_equipment_2 | ifv_chassis_1 | CUM | BTR-50P | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:309 | mechanized_equipment_6 | apc_chassis_3 | CZE | OT-64A | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:318 | mechanized_heavy_equipment_2 | ifv_chassis_1 | CUM | BTR-50P | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:319 | mechanized_equipment_6 | apc_chassis_3 | CZE | OT-64A | national |
| Cold War Iron Curtain/history/units/IRQ_1980_nsb.txt:368 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CUM | BMP-1 | national |
| Cold War Iron Curtain/history/units/ISR_1980_nsb.txt:434 | mechanized_equipment_3 | apc_chassis_0 | ISR | Zachlam M9 | national |
| Cold War Iron Curtain/history/units/ISR_1980_nsb.txt:439 | heavy_mechanized_equipment_3 | ifv_chassis_2 | ISR | Uparmored Zachlam M3 | national |
| Cold War Iron Curtain/history/units/ISR_1980_nsb.txt:459 | mechanized_equipment_3 | apc_chassis_0 | ISR | Zachlam M9 | national |
| Cold War Iron Curtain/history/units/JOR_1980_nsb.txt:270 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/MOR_1980_nsb.txt:305 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/NGA_1980_nsb.txt:204 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/NOR_1980_nsb.txt:259 | mechanized_equipment_4 | apc_chassis_1 | NOR | FMC M59 | national |
| Cold War Iron Curtain/history/units/NOR_1980_nsb.txt:264 | mechanized_equipment_5 | apc_chassis_2 | NOR | FMC M113 | national |
| Cold War Iron Curtain/history/units/NOR_1980_nsb.txt:269 | mechanized_equipment_6 | apc_chassis_3 | NOR | M113F1 | national |
| Cold War Iron Curtain/history/units/PAK_1980_nsb.txt:660 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:170 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:179 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:188 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:197 | mechanized_heavy_equipment_3 | ifv_chassis_2 | CUM | BTR-50PK | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:206 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:215 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/PER_1980_nsb.txt:224 | mechanized_equipment_6 | apc_chassis_3 | CAP | Carrier, Personnel, Full Tracked, Armored, M113A1 | national |
| Cold War Iron Curtain/history/units/PHI_1980_nsb.txt:186 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/POL_1949_nsb.txt:370 | mechanized_equipment_3 | apc_chassis_0 | POL | BTR-40 | national |
| Cold War Iron Curtain/history/units/POL_1980_nsb.txt:454 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/POL_1980_nsb.txt:459 | heavy_mechanized_equipment_3 | ifv_chassis_2 | CUM | BTR-50PK | national |
| Cold War Iron Curtain/history/units/POL_1980_nsb.txt:479 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/PRU_1980_nsb.txt:179 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/RAJ_1980_nsb.txt:755 | mechanized_equipment_5 | apc_chassis_2 | CUM | BTR-60P | national |
| Cold War Iron Curtain/history/units/RAJ_1980_nsb.txt:1106 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/SAF_1980_nsb.txt:350 | mechanized_equipment_3 | apc_chassis_0 | SAF | Loyd Carrier | national |
| Cold War Iron Curtain/history/units/SAU_1980_nsb.txt:284 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/SOV_1949_nsb.txt:1964 | mechanized_equipment_3 | apc_chassis_0 | SOV | BTR-40 | national |
| Cold War Iron Curtain/history/units/SOV_1949_nsb.txt:1973 | mechanized_heavy_equipment_1 | ifv_chassis_0 | SOV | BTR-152 | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1274 | mechanized_equipment_3 | apc_chassis_0 | SOV | BTR-40 | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1275 | mechanized_equipment_4 | apc_chassis_1 | SOV | BTR-40B | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1276 | mechanized_equipment_5 | apc_chassis_2 | SOV | BTR-60P | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1277 | mechanized_equipment_6 | apc_chassis_3 | SOV | BTR-60PB | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1278 | mechanized_equipment_7 | apc_chassis_4 | SOV | BTR-70 | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1279 | mechanized_heavy_equipment_1 | ifv_chassis_0 | SOV | BTR-152 | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1280 | mechanized_heavy_equipment_2 | ifv_chassis_1 | SOV | BTR-50P | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1281 | mechanized_heavy_equipment_3 | ifv_chassis_2 | SOV | BTR-50PK | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1282 | mechanized_heavy_equipment_4 | ifv_chassis_3 | CZE | BVP-1 | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1283 | mechanized_heavy_equipment_4 | ifv_chassis_3 | SOV | BMP-1 | national |
| Cold War Iron Curtain/history/units/SOV_1980_nsb.txt:1284 | mechanized_heavy_equipment_5 | ifv_chassis_4 | SOV | BMP-1P | national |
| Cold War Iron Curtain/history/units/TUR_1980_nsb.txt:716 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/TUR_1980_nsb.txt:721 | heavy_mechanized_equipment_1 | ifv_chassis_0 | CAP | M44 | national |
| Cold War Iron Curtain/history/units/UNT_1980_nsb.txt:112 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/USA_1949_nsb.txt:1508 | mechanized_equipment_3 | apc_chassis_0 | USA | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/USA_1949_nsb.txt:1754 | mechanized_equipment_3 | apc_chassis_0 | USA | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/VEN_1980_nsb.txt:232 | mechanized_equipment_3 | apc_chassis_0 | CAP | M3A1 Half-Track | national |
| Cold War Iron Curtain/history/units/YEM_1980_nsb.txt:209 | mechanized_equipment_5 | apc_chassis_2 | CAP | Carrier, Personnel, Full Tracked, Armored, M113 | national |
| Cold War Iron Curtain/history/units/YEM_1980_nsb.txt:214 | mechanized_equipment_5 | apc_chassis_2 | CUM | BTR-60P | national |
| Cold War Iron Curtain/history/units/YEM_1980_nsb.txt:219 | mechanized_equipment_3 | apc_chassis_0 | CUM | BTR-40 | national |
| Cold War Iron Curtain/history/units/YEM_1980_nsb.txt:224 | mechanized_heavy_equipment_1 | ifv_chassis_0 | CUM | BTR-152 | national |

## Deferred national inventory

The manifest's `future_inventory` preserves all 354 selected later-tier pairs and their source provenance for the next coverage batch. They are intentionally absent from bookmark creation until the bookmark/OOB chassis contract can expand coherently.
