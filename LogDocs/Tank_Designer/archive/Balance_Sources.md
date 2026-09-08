# Tank Designer Balance Sources

Date: 2026-09-04

Two design artifacts were handed over by Lead Dev and now sit untracked in the repository
root:

- `2023 - CWIC Tank Rework Balance.xlsx` - the module balance master sheet, 15 tabs.
- `Tank_Designer_Slimemix (1).drawio` - the design tree, 11 pages, authored in draw.io
  20.7.4 and last modified 2023-09-23.

Both predate this branch by roughly three years. This document records what they contain,
how they relate to what the mod already ships, and which parts of them are still unbuilt.

## Headline finding: the workbook is already implemented

The workbook's `Total Balance Sheet` tab is the exact source of the numbers currently in
`common/units/equipment/modules/00_tank_modules.txt` and `common/units/equipment/tank_chassis.txt`.

A field-by-field comparison of every module the two have in common - 224 modules across
`add_stats` and `multiply_stats` - produced **zero real differences**. The only entries
flagged were naming artifacts of the comparison itself (`recon` vs `reconnaissance`) and
`hardness`, which the sheet keeps in a column the comparison did not map. Spot checks of
guns, ammunition, armor, autoloaders and hulls all matched to the digit:

| Module | Sheet | Mod |
| --- | --- | --- |
| `Light_Hull_0` | rel 1, hardness 0.7, brk 20, def 6, armor 5, speed 6, cost 2.5, steel 1 | identical |
| `tank_light_cannon0` | rel -0.05, ha/sa -0.55, pierce -0.8, speed -0.2, cost 1.5 | identical |
| `tank_smooth_mbt_cannon1` | rel -0.3, ha/sa +0.025, pierce +0.125, speed -0.6, cost 4.6 | identical |
| `ap_0p` | hard 20, pierce 150, cost 0.25 | identical |
| `hesh_p` | hard 35, soft 12.5, pierce 120 | identical |

**Do not treat the workbook as a to-do list of numbers to enter.** It is the reference that
explains where the shipped numbers came from, and the place to change them if balance moves.

Two consequences follow:

1. The `[DONE]` tags inside the workbook are stale. Guns and ammunition carry no `[DONE]`
   marker on any of their category rows, yet their values are in the game and match. Judge
   completeness from the mod, not from the tags.
2. The per-category `(DONE) ...` tabs are earlier drafts, not the master. `(DONE) FCS & Gun
   Loading` gives `Gun Rammer` a supply cost of 0.01 and a production cost of 1.5; the
   `Total Balance Sheet` and the mod both say 0.02 and 1. **When two tabs disagree,
   `Total Balance Sheet` wins.**

### Counts

- Workbook module rows: 250, of which 25 are hulls (modelled in the mod as chassis, not
  modules) and 224 are true modules.
- Mod tank modules: 243. The 19 not in the workbook are the turret and superstructure
  family (`pintle_turret`, `light_turret`, `conventional_turret`, `oscillating_turret`,
  `open_gun` and its medium/heavy variants, `external_gun`, `fixed_superstructure` and its
  medium/heavy variants, `light_lp_turret`, `lp_turret`), the three
  `tank_anti_air_cannon*` entries, `flamethrower`, and `tank_gasoline_engine`. These were
  never balanced in the workbook.

## Workbook tab guide

| Tab | What it is | Use it for |
| --- | --- | --- |
| `Total Balance Sheet` | **Master.** Left block: target stat envelopes for 41 finished vehicle generations. Right block: every module with full stat and resource columns. | The authoritative reference for both module values and design targets. |
| `Total Balance Sheet Minimal` | Same module list, stats stripped, but adds the **`Unlocked by Tech`** column. | Mapping a module to the technology that should unlock it. |
| `Svedenie` (Cyrillic tab name) | Consolidated numeric export, non-zero stat columns only. | Fast reading of the same data. |
| `Total Balance Sheet Object 842` | The 41-row vehicle envelope block alone, plus role penalty rows (APC -0.4 hardness/armor, IFV -0.2, Artillery -0.4). | Role modifier deltas. |
| `(DONE) AFV Hulls`, `(DONE) FCS & Gun Loading`, `(DONE) Armor & Protection` | Earlier per-category drafts. Each ends with a `Max Bonus` row totalling the best achievable stack. | The `Max Bonus` rows only; the values above them are superseded. |
| `Gun Modules` | Rough gun draft. Mixed decimal conventions (`1,5`), stray percent strings (`82,5%`), incomplete rows. | Nothing. Superseded. |
| `Piercing` | Penetration research: real-world mm RHA per ammunition generation against each gun class, and the scaling grids used to derive the in-game piercing ladders. Includes DU variants and a T-54 (200mm) anchor. | Justifying or re-deriving piercing numbers. |
| `Work Sheet` | Scratch. Air-attack ladders for SPAAG and SAM, soft/hard/piercing targets for SP artillery light/medium/heavy and AT, cost proportion budgets (modern: hull 0.1, gun 0.075, armor 0.2, suspension 0.1, engine 0.15, FCS 0.25, ammo 0.05, APS 0.075; 1960s: hull 0.35, gun 0.1, suspension 0.1, engine 0.2, FCS 0.05, ammo 0.05), per-category cost min/1950/max/iteration bands, and a real-tank RHA table (T-34 75, T-62 222.5, T-64A 366.5, T-80U 795, M60 200, M1 467.5, M1A1 HA 607.5). | Cost budgeting and the artillery/AA target stats, which are **not** in the master sheet. |
| `Years` | The 18 canonical tech years: 1939, 1942, 1944, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020. | Every ladder anchors to this list. |
| `Hulls`, `Roles`, `Armored Battalions`, `Night & Thermal Vision Effects` | Scaffolding. `Roles` is filled in and useful; `Armored Battalions` and the vision tab are near-empty. | `Roles` only. |

### The vehicle envelope table

The master sheet's left block states what a *finished design* of each generation should
total. This is the acceptance target for AI recipes and bootstrap variants, and nothing in
the repository currently checks against it.

Families and their spans: Light Tank I-VI (1942-1995), WWII Tank 1-2 and MBT I-VIII
(1942-2005), Heavy Tank I-V (1942-1960), WWII Mech 1-2 and Light Mech I-VIII (1942-2005),
Heavy Mech I-VIII (1947-2005). Sample rows:

| Design | Year | Hard | Soft | Brk | Def | Armor | Pierce | Speed | Fuel | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Light Tank I | 1942 | 9 | 8 | 35 | 9 | 20 | 24 | 11 | 1.8 | 10 |
| WWII Tank 1 | 1942 | 12 | 16 | 40 | 8 | 25 | 30 | 9 | 3.6 | 15 |
| Heavy Tank I | 1942 | 15 | 20 | 45 | 6 | 30 | 36 | 7 | 4.6 | 20 |
| MBT III | 1960 | 26 | 29 | 84 | 16 | 55 | 50 | 12 | 3.6 | 30 |
| MBT VIII | 2005 | 50 | 54 | 162 | 30 | 100 | 85 | 17 | 3.6 | 50 |
| Heavy Mech VIII | 2005 | 9 | 14 | 18 | 45 | 80 | 34 | 19 | 2.6 | 28 |

Reliability is 70% for the two 1942/1944 heavies and 95.5% everywhere else. Hardness is
fixed per family: heavy tank 90, MBT 80, light tank 70, heavy mech 60, light mech 50.
An `M1 Abrams` row sits among the MBTs as a real-world sanity check, not a design target.

`Roles` fixes which roles each hull class may take:

- Light hull: APC, IFV, Light Tank, Light Tank Destroyer, LL/LM/LH SP Artillery, Light
  SPAA, ATGM Carrier.
- Medium hull: Heavy APC, Heavy IFV, MBT, Medium Tank Destroyer, ML/MM/MH SP Artillery,
  Medium SPAA, ATGM Tank.
- Heavy hull: Heavy Tank, Heavy Tank Destroyer, HL/HM/HH SP Artillery.

## Design tree page guide

`/tmp` scratch aside, the pages decode with the script in the last section. Page titles
carry their own `[DONE]` markers, which disagree with the workbook's - see the note above.

| # | Page | Nodes/edges | Status |
| --- | --- | --- | --- |
| 0 | Armour & Tank Protection Systems | 230 / 37 | Implemented |
| 1 | Engine, Transmission & Suspension | 60 / 18 | Implemented |
| 2 | Base & Other Tech Modules | 42 / 2 | **Almost entirely unbuilt** |
| 3 | `[DONE]` Tank Guns & Ammunition | 519 / 101 | Implemented |
| 4 | `[DONE]` Fire Control & Gun Loading Systems | 287 / 53 | Implemented except night vision |
| 5 | `[DONE]` AFV Hulls | 176 / 36 | Implemented |
| 6 | Artillery | 256 / 93 | **Unbuilt** |
| 7 | Trucks & Amphibious | 29 / 10 | **Unbuilt stub** |
| 8 | Tank Desiner Composition | 67 / 0 | Designer slot sketch, see below |
| 9 | Light Chassis Based Vehicles | 1014 / 0 | Research reference, no build work |
| 10 | Whole Tech Tree | 1439 / 251 | The other pages assembled into one canvas |

Every tree page uses the same layout convention: a year column down the left drawn from
the `Years` tab, technology boxes placed on their year row, a numeric badge beside each box
that indexes it, and a long prose description parked in a right-hand column keyed to that
badge. Those descriptions are written localisation - several paragraphs per node explaining
the real engineering history - and are worth mining if node descriptions are ever rewritten.

Page 9 is a different animal: a per-nation historical table (Soviet, British, German, USA)
listing real vehicles per generation with production date, suspension type, gun and engine
- for instance `T-50 1941 / Torsion bar / 45mm 20-K / Diesel`. Its right-hand block is a
role-availability matrix: which of SPA, SPAT, SPAA, APC, IFV and ATGM each chassis
generation may host. ATGM first appears at the Early Cold War Light Tank / First Gen MBT
row, matching `Roles`.

### Designer composition sketch (page 8)

The page shows the designer laid out as fixed slots plus numbered generic slots:

- Fixed: Gun, Turret, Aiming, Optics, Suspension, Armour, Engine, and two ammunition slots
  (AP Ammo, HE Ammo).
- Generic: `Slot 1` through `Slot 12`.
- A parking list of candidate special modules: Belt Autoloader, Blow-Out Panels, Active
  Protection, ERA, Anti-Mine Plow, External Additional Fuel Tanks, ATGM, Unmanned Turret,
  Auxiliary Power Unit, Underwater Driving, Integrated Trench Plow, Modular Construction,
  External Additional Armour, Smoke Grenades Launcher.

This is a sketch, not a specification, and the shipped 15-slot layout in
`interface/tank_designer_view.gui` is the thing that exists. The sketch is still useful as
the record of which special modules were meant to be reachable - of that list, only the
autoloaders, APS, ERA, APU and smoke launchers exist as modules today.

## What the sources specify that the mod does not have

Ordered roughly by size. None of this is a regression on this branch; it is scope that was
designed in 2023 and never built.

1. **Artillery and AA designer ladders (page 6).** The page designs six-step ladders -
   `Medium Artillery I-VI` with `Artillery Modernisation I-VI` interleaved, `Light
   Artillery I-VI`, `Heavy Artillery I-VI`, `Artillery Ammunition I-VI`, `AA Autocannon
   I-VI` with `AA Modernisation I-VI`, and `AA Ammunition I-VI` - each anchored to real
   guns per year (ML-20 152mm 1937, D-20 152mm 1947, M-46 130mm 1951, S-60 57mm 1950,
   61-K 37mm 1941, and so on). The mod still runs the legacy five-step equipment ladders
   in `common/technologies/artillery.txt` (`artillery_1..5`, `light_artillery_1..5`,
   `heavy_artillery_1..5`, `art_ammo_1..5`, `art_upgrade_1..5`, `autocannon_1..5`,
   `spaag_1..5`, `aa_upgrade_1..5`, `cannon_ammo_1..5`), which unlock whole equipment
   models rather than designer modules. Target stats for these live in `Work Sheet`, not
   in the master sheet.
2. **Base and other tech modules (page 2).** Front engine placement, external gun mount,
   fixed superstructure, blow-out panels (noted incompatible with carousel autoloaders),
   unmanned and semi-unmanned fighting compartment (requires a carousel or belt loader),
   dozer plow into anti-mine plow and integrated trench-digging plow, anti-mine rollers
   (KMT-5, KMT-7 EMT), external fuel containers, remote weapon stations `RWS I/II/III`
   (1965 / 1985 / 2005), heavy machine guns as `Infantry weapons I`, amphibious drive, and
   a `Log` module (+2% reliability). Of these the mod has only the turret and
   superstructure modules, which were never balanced in the workbook.
3. **Night and thermal vision.** Page 4 designs `Zero Gen Night Vision` (1944) through
   `First`, `Second`, `Third Gen Night Vision` and `Thermal Vision`. The workbook reserves
   a `Night & Thermal Vision Effects` tab for the numbers and it was left empty. Nothing
   in the mod matches - `grep -ri night_vision common/technologies` returns nothing.
4. **Trucks and amphibious (page 7).** A bare grid of `Truck I` and `Amphibious I`
   repeating down the year column with no differentiated nodes. Designed but not designed
   *out*; the mod's `amphibious1..5` in `common/technologies/armor.txt` is the legacy line.
5. **The mechanized ladder.** Page 10 chains `Early/Mid/Late WW2 Mechanized` into `APC`
   and `Heavy APC/IFV`, then `Light Mechanised II-VII` and `Heavy Mechanised II-VII`. The
   master sheet gives all sixteen of those generations full stat envelopes. The mod still
   uses `mechanized_infantry1..10` and `mechanized_heavy_infantry1..8` from legacy
   `armor.txt`, which are equipment techs, not designer content.
6. **Nothing validates against the vehicle envelope table.** `tools/validate_military_reworks.py`
   checks module contracts and ammunition presence. It does not check that a bootstrap
   variant or AI recipe of a given generation lands near its target hard/soft/breakthrough/
   armor/piercing row. That check is now possible because the targets are written down.

## Re-reading the files

Neither file is text. `openpyxl` is not installed and was not added; the workbook was read
with the standard library, and the diagram is deflate-compressed base64 inside XML.

```python
# xlsx: worksheets are xl/worksheets/sheetN.xml, strings are indices into xl/sharedStrings.xml
import zipfile, xml.etree.ElementTree as ET
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z = zipfile.ZipFile("2023 - CWIC Tank Rework Balance.xlsx")
ss = [''.join(t.text or '' for t in si.iter(NS+'t'))
      for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
```

Sheet order does not match tab order; resolve it through `xl/workbook.xml` and
`xl/_rels/workbook.xml.rels`.

```python
# drawio: each <diagram> body is raw-deflate, base64, then URL-encoded
import base64, zlib, urllib.parse, xml.etree.ElementTree as ET
for d in ET.parse("Tank_Designer_Slimemix (1).drawio").getroot().findall('diagram'):
    xml = urllib.parse.unquote(zlib.decompress(base64.b64decode(d.text.strip()), -15).decode())
```

Node labels are HTML fragments inside `value=`; strip tags and unescape before reading.
Edge endpoints are `mxCell` `source`/`target` ids, and a fair number of edges on the busier
pages point at unlabelled decorative boxes, so an edge list alone under-reports the tree -
read positions alongside it.

## Do not stage these two files

`2023 - CWIC Tank Rework Balance.xlsx` and `Tank_Designer_Slimemix (1).drawio` are
untracked working files in the repository root, alongside the unrelated user files the
handoff already lists. Leave them untracked unless the user asks otherwise.
