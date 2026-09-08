# Balance

Source interpretation, frozen targets, and the deferred-batch specs.

## The two primary sources

- `data/2023 - CWIC Tank Rework Balance.xlsx` - module balance master, 16 tabs.
- `data/Tank_Designer_Slimemix (1).drawio` - design tree, 12 pages, draw.io 20.7.4,
  last modified 2023-09-23.

Both were handed over by Lead Dev and predate this branch by roughly three years.

**Workbook SHA-256:** `dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`

The workbook is frozen and byte-identical; `--tank-balance-report` checks the hash. The
living document is the CSV mirror,
`data/2023 - CWIC Tank Rework Balance(Total Balance Sheet Minimal).csv`, which carries
the reviewed overrides plus the `Script-Owned [NEEDS REVIEW]` and `Coverage [STATUS]`
sections.

## Headline finding: the workbook is already implemented

The `Total Balance Sheet` tab is the exact source of the numbers currently in
`00_tank_modules.txt` and `tank_chassis.txt`. A field-by-field comparison of all 224
shared modules across `add_stats` and `multiply_stats` produced **zero real
differences**; the only flags were naming artifacts of the comparison (`recon` vs
`reconnaissance`) and `hardness`, kept in an unmapped column.

**Do not treat the workbook as a to-do list of numbers to enter.** It is the reference
explaining where the shipped numbers came from, and the place to change them if balance
moves. Two consequences:

1. The `[DONE]` tags inside the workbook are stale. Guns and ammunition carry no
   `[DONE]` marker yet their values are in the game and match. Judge completeness from
   the mod, not from the tags.
2. The per-category `(DONE) ...` tabs are earlier drafts. `(DONE) FCS & Gun Loading`
   gives `Gun Rammer` supply 0.01 / cost 1.5; `Total Balance Sheet` and the mod both say
   0.02 / 1. **When two tabs disagree, `Total Balance Sheet` wins.**

## Workbook tab guide

| Tab | What it is | Use it for |
| --- | --- | --- |
| `Total Balance Sheet` | **Master.** Left block: target stat envelopes for 41 vehicle generations. Right block: every module with full stat and resource columns. | Authoritative for both module values and design targets |
| `Total Balance Sheet Minimal` | Same module list, stats stripped, adds the **`Unlocked by Tech`** column | Mapping a module to its unlocking technology |
| `Svedenie` | Consolidated numeric export, non-zero stat columns only | Fast reading of the same data |
| `Total Balance Sheet Object 842` | The 41-row vehicle envelope block plus role penalty rows (APC -0.4 hardness/armor, IFV -0.2, Artillery -0.4) | Role modifier deltas |
| `(DONE) AFV Hulls`, `(DONE) FCS & Gun Loading`, `(DONE) Armor & Protection` | Earlier per-category drafts, each ending in a `Max Bonus` row | The `Max Bonus` rows only |
| `Gun Modules` | Rough gun draft, mixed decimal conventions, incomplete rows | Nothing. Superseded |
| `Piercing` | Real-world mm RHA per ammunition generation against each gun class, the scaling grids behind the in-game piercing ladders, DU variants, a T-54 200mm anchor | Justifying or re-deriving piercing numbers |
| `Work Sheet` | Scratch. Artillery/AA/AT/SAM targets, cost proportion budgets, per-category cost bands, a real-tank RHA table | Cost budgeting and the artillery/AA targets, which are **not** in the master sheet |
| `Years` | The 18 canonical tech years | Every ladder anchors to this list |
| `Hulls`, `Roles`, `Armored Battalions`, `Night & Thermal Vision Effects` | Scaffolding; `Roles` is filled in, the other three near-empty | `Roles` only |
| `Implementation Status` | Added 2026-09-05 by surgical zip edit | Page/scope status |

Canonical years: 1939, 1942, 1944, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985,
1990, 1995, 2000, 2005, 2010, 2015, 2020.

Cost proportion budgets from `Work Sheet` - modern: hull 0.1, gun 0.075, armor 0.2,
suspension 0.1, engine 0.15, FCS 0.25, ammo 0.05, APS 0.075. 1960s: hull 0.35, gun 0.1,
suspension 0.1, engine 0.2, FCS 0.05, ammo 0.05. Real-tank RHA anchors: T-34 75,
T-62 222.5, T-64A 366.5, T-80U 795, M60 200, M1 467.5, M1A1 HA 607.5.

## Drawio page guide

| # | Page | Nodes/edges | Status |
| --- | --- | --- | --- |
| 0 | Armour & Tank Protection Systems | 230 / 37 | Implemented |
| 1 | Engine, Transmission & Suspension | 60 / 18 | Implemented |
| 2 | Base & Other Tech Modules | 42 / 2 | **Almost entirely unbuilt** |
| 3 | `[DONE]` Tank Guns & Ammunition | 519 / 101 | Implemented |
| 4 | `[DONE]` Fire Control & Gun Loading Systems | 287 / 53 | Implemented except night vision |
| 5 | `[DONE]` AFV Hulls | 176 / 36 | Implemented |
| 6 | Artillery | 256 / 93 | **Unbuilt** |
| 7 | Trucks & Amphibious | 29 / 10 | **Unbuilt stub - do not mine it, it will waste a session** |
| 8 | Tank Desiner Composition | 67 / 0 | Designer slot sketch |
| 9 | Light Chassis Based Vehicles | 1014 / 0 | Research reference, no build work |
| 10 | Whole Tech Tree | 1439 / 251 | The other pages assembled into one canvas |

Every tree page uses the same convention: a year column down the left drawn from the
`Years` tab, technology boxes on their year row, a numeric badge indexing each box, and
a long prose description parked in a right-hand column keyed to that badge. Those
descriptions are written localisation - several paragraphs per node of real engineering
history - worth mining if node descriptions are ever rewritten.

Page 9 is a per-nation historical table (Soviet, British, German, USA) listing real
vehicles per generation with production date, suspension type, gun and engine, plus a
role-availability matrix. ATGM first appears at the Early Cold War Light Tank / First
Gen MBT row.

**Max fontSize in the file is 20, so do not try to find headings by font size - cluster
by `x`.** On the Whole Tech Tree page the year axis is at `x = 6400`: `y=80` is 1940,
200 is 1943, 320 is 1945, then every 120px is five years (440 is 1950, up to 2120 for
2020).

## Re-reading the sources

Neither file is text. `openpyxl` is not installed and must not be used to write.

```python
# xlsx: worksheets are xl/worksheets/sheetN.xml, strings index xl/sharedStrings.xml
import zipfile, xml.etree.ElementTree as ET
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z = zipfile.ZipFile("2023 - CWIC Tank Rework Balance.xlsx")
ss = [''.join(t.text or '' for t in si.iter(NS+'t'))
      for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
```

Sheet order does not match tab order; resolve through `xl/workbook.xml` and
`xl/_rels/workbook.xml.rels`.

```python
# drawio: each <diagram> body is raw-deflate, base64, then URL-encoded
import base64, zlib, urllib.parse, xml.etree.ElementTree as ET
for d in ET.parse("Tank_Designer_Slimemix (1).drawio").getroot().findall('diagram'):
    xml = urllib.parse.unquote(zlib.decompress(base64.b64decode(d.text.strip()), -15).decode())
```

Node text is `value=` on `<mxCell>` (HTML fragments - strip tags and unescape);
position is the child `<mxGeometry x= y=>`. Edge endpoints are `mxCell` `source`/`target`
ids, and many edges on the busier pages point at unlabelled decorative boxes, so an edge
list alone under-reports the tree - read positions alongside it.

## Frozen vehicle envelope manifest

**Authoritative copy: `data/Balance_Target_Manifest.md`.** That file is parsed by
`--tank-balance-report`; its table format is a machine contract, so edit it with care
and do not reformat it. It is not duplicated here on purpose - one copy, one truth.

It freezes the 40 reviewed rows from `Total Balance Sheet`: 39 design targets plus the
separately marked M1 Abrams reference, with workbook row numbers preserved as
provenance. Reliability and hardness are normalized from percentages to fractions;
decimal commas to points. An em dash means the workbook cell is empty and is **never**
treated as zero.

Shape of it, so you know whether you need to open it: 21 tank target rows (Light Tank
I-VI, WWII Tank 1-2, MBT I-VIII, Heavy Tank I-V) and 18 mechanized rows (WWII Mech 1-2,
Light Mech I-VIII, Heavy Mech I-VIII), each carrying year, reliability, hardness, hard
and soft attack, breakthrough, defense, armor, piercing, speed, supply, fuel usage and
production cost. Hardness is fixed per family: heavy tank 0.9, MBT 0.8, light tank 0.7,
heavy mech 0.6, light mech 0.5. Reliability is 0.7 for the two 1942/1944 heavies and
0.955 everywhere else. The Supply column is empty for every row. The Abrams row is a
real-world sanity check, not a design target, and is excluded from target counts.

The 18 mechanized rows are the acceptance target for the APC/IFV families - see
`REFERENCE.md` for the mapping from those rows to hulls.

### Coverage status

| Section | Rows | Status |
| --- | ---: | --- |
| Hulls | 25 | Verified - 200/200 stat cells match script |
| All module sections | 224 | Verified - 1224/1224 stat cells match script |
| Script-owned modules | 22 | No balance row; values read back from script, needs a decision |
| Mechanized | 18 | Out of scope for the tank designer pass |

The 22 script-owned modules are every turret and superstructure,
`open_gun`/`medium_open_gun`/`heavy_open_gun`, `external_gun`, `flamethrower`,
`tank_gasoline_engine`, the three `tank_anti_air_cannon` tiers, and the four `cwic_*`
secondary turrets. Packet B changed turret and AA numbers with nothing in the sheet to
check them against; the AA change was reverted for that reason. Decide whether these get
workbook rows or are formally declared script-owned.

The seven APC and sixteen IFV modules are explicit exemptions from frozen-workbook
coverage - the 2023 workbook predates both families.

## Artillery and AA targets

Frozen 2026-09-06 from `Work Sheet` (`xl/worksheets/sheet14.xml`). **This is a source
contract for deferred implementation, not a claim that anything matches these targets.**
Values are literal workbook numbers; missing values are `missing`, never zero. SP fields
map to `soft_attack`, `hard_attack`, `ap_attack`, `breakthrough`, `defense`; AA maps to
`air_attack`. SP Heavy's low piercing is intentional. Unlisted stats, including cost,
armor and reliability, are unspecified rather than zero.

**Year policy.** Use a band's lower year as its anchor, then choose the nearest
canonical year, earlier wins ties. SPAAG 1935-1940 maps to 1939, SP 1945 maps to 1944,
AT 1940 maps to 1939; later SPAAG bands map to 1950, 1965, 1980, 1995. This mapping is
an implementation decision made at freeze time, not a date specified by the source.
**Do not interpolate extra tiers or invent a sixth SP/AT tier to fit the diagram.** The
diagram's six-step towed layout is not a six-row equipment balance table.

### SPAAG (air attack)

| Cells | Source band | Grid year | Air attack |
| --- | --- | --- | --- |
| `B4:C4` | 1935-1940 | 1939 | 12 |
| `B5:C5` | 1950-1955 | 1950 | 14 |
| `B6:C6` | 1965-1970 | 1965 | 16 |
| `B7:C7` | 1980-1985 | 1980 | 20 |
| `B8:C8` | 1995-2000 | 1995 | 24 |

### SAM (air attack)

| Cells | Year | Air attack |
| --- | --- | --- |
| `B13:C13` | 1955 | 35 |
| `B14:C14` | 1965 | 45 |
| `B15:C15` | 1975 | 60 |
| `B16:C16` | 1985 | 75 |
| `B17:C17` | 1995 | 90 |
| `B18:C18` | 2005 | 105 |

### SP Light

| Cells | Source | Grid year | Soft | Hard | Pierce | Brk | Def |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `F4:K4` | 1945 | 1944 | 24 | 6 | 12 | 7 | 10 |
| `F5:K5` | 1960 | 1960 | 27 | 8 | 14 | 8 | 12 |
| `F6:K6` | 1975 | 1975 | 33 | 10 | 16 | 10 | 14 |
| `F7:K7` | 1990 | 1990 | 39 | 12 | 18 | 11 | 16 |
| `F8:K8` | 2005 | 2005 | 45 | 14 | 20 | 13 | 18 |

### SP Medium

| Cells | Source | Grid year | Soft | Hard | Pierce | Brk | Def |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N4:S4` | 1945 | 1944 | 32 | 6 | 12 | 8 | 7.5 |
| `N5:S5` | 1960 | 1960 | 36 | 8 | 14 | 10 | 9 |
| `N6:S6` | 1975 | 1975 | 44 | 10 | 16 | 11 | 10.5 |
| `N7:S7` | 1990 | 1990 | 52 | 12 | 18 | 13 | 12 |
| `N8:S8` | 2005 | 2005 | 60 | 14 | 20 | 14 | 13.5 |

### SP Heavy

| Cells | Source | Grid year | Soft | Hard | Pierce | Brk | Def |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `V4:AA4` | 1945 | 1944 | 40 | 9 | 6 | 9 | 5 |
| `V5:AA5` | 1960 | 1960 | 45 | 12 | 7 | 11 | 6 |
| `V6:AA6` | 1975 | 1975 | 55 | 15 | 8 | 13 | 7 |
| `V7:AA7` | 1990 | 1990 | 65 | 18 | 9 | 14 | 8 |
| `V8:AA8` | 2005 | 2005 | 75 | 21 | 10 | 16 | 9 |

### AT

| Cells | Source | Grid year | Soft | Hard | Pierce | Brk | Def |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AD4:AI4` | 1940 | 1939 | 12 | 15 | 30 | 13 | 10 |
| `AD5:AI5` | 1955 | 1955 | 14 | 20 | 35 | 15 | 12 |
| `AD6:AI6` | 1970 | 1970 | 17 | 25 | 40 | 18 | 14 |
| `AD7:AI7` | 1985 | 1985 | 30 | 30 | 45 | 20 | 16 |
| `AD8:AI8` | 2000 | 2000 | 46 | 35 | 50 | 23 | 18 |

### Reserved module cost bands

Budget references, not implemented module stats. Iteration counts do not establish
technology dates or unlock requirements.

| Cells | Category | Min | 1950 | Max | Iterations |
| --- | --- | --- | --- | --- | --- |
| `AP58:AT58` | Mech ammo arty | 2.5 | 3.5 | 4.5 | 3 |
| `AP61:AT61` | Aiming AA | 0.5 | 3 | 6.6 | 5 |
| `AP64:AT64` | Optics AA | 0.5 | missing | 9 | 6 |
| `AP65:AT65` | Optics Arty | 0.5 | missing | 8 | 2 |
| `AP69:AT69` | Computer Arty | 5.25 | missing | 7.5 | 4 |
| `AP70:AT70` | Radar | 4 | missing | 8.5 | 7 |

31 vehicle target rows, 111 combat-stat cells and six module budget rows are frozen.
IFV rows `F13:I17` are excluded - the mechanized manifest owns them. No source target
here defines towed artillery, rocket artillery, amphibious equipment, night vision, or
a complete designer loadout; those need separate contracts.

Reproduce with `python3 "CWIC Backup/tools/artillery_aa_targets.py"`; verify with
`--check`. The command never edits files. Note the relocated tool's root calculation is
one directory too shallow after the `CWIC Backup/tools/` move - a known tooling issue,
not target drift. Do not silently edit backup tools.

What the legacy artillery tree runs today, for contrast: `artillery_1..5`,
`light_artillery_1..5`, `heavy_artillery_1..5`, `art_ammo_1..5`, `art_upgrade_1..5`,
`autocannon_1..5`, `spaag_1..5`, `aa_upgrade_1..5`, `cannon_ammo_1..5` in
`common/technologies/artillery.txt` - equipment ladders, not designer modules.

## Research cost weighting

Ratified and applied as schedule R1-R7: 91 of 169 technologies repriced, total 337 to
345.5 (+2.52%), USA/SOV 1970 path -1.67%, 2020 path +8.33%. The full per-ID schedule
lives in `archive/Research_Cost_Proposal.md` if it ever needs re-deriving.

The convention it followed, from real counts across `common/technologies/`:

| File | research_cost distribution |
| --- | --- |
| `NSB_armor.txt` | `2` x66, `1` x1 |
| `NSB_armor_modules.txt` | `2` x102 |
| `armor.txt` (legacy) | `2` x31, `3` x13, `4` x3, `1` x1 |
| `MTG_naval.txt` | `4` x19, `1` x15, `3` x14, `2` x10, `1.5` x9 |
| `MTG_navalmodule.txt` | `1.5` x33, `2` x16, `3.5` x10, `1` x8, `3` x6, `4` x3 |
| `light_air.txt` | `3` x32, `2` x24, `4` x22, `6` x5, `3.5` x3 |
| `industry.txt` | `2.5` x143, `1.5` x16, `3` x11 |
| Mod-wide | `3` x884, `2` x416, `1.5` x191, `2.5` x143, `1` x139, `4` x90 |

The pattern, clearest in the MTG naval pair: **hull/chassis lines cost more than module
lines**, modules sit at 1.5-2, and cost rises with tier. Roots and enabling techs are 1.
Keep total investment for a full 1949-start armor path within ~10% of the current curve.

The XP economy is deliberately flat at 1 and that question is closed.

## Designed but unbuilt

Ordered roughly by size. None of this is a regression; it is 2023 scope never built.

1. **Artillery and AA designer ladders** (drawio page 6). Six-step ladders -
   `Medium Artillery I-VI` with `Artillery Modernisation I-VI` interleaved, `Light
   Artillery I-VI`, `Heavy Artillery I-VI`, `Artillery Ammunition I-VI`, `AA Autocannon
   I-VI` with `AA Modernisation I-VI`, `AA Ammunition I-VI` - each anchored to real guns
   per year (ML-20 152mm 1937, D-20 152mm 1947, M-46 130mm 1951, S-60 57mm 1950, 61-K
   37mm 1941).
2. **Base and other tech modules** (page 2), mirrored on `[TODO] Base & Other Tech
   Modules`. Years read off the `x = 6400` axis of the Whole Tech Tree page:

   | Year | Nodes |
   | --- | --- |
   | 1940 | Amphibious Drive |
   | 1945 | OPVT, Underwater Driving Capability, Dozer Plow |
   | 1950 | Log (+2% reliability) |
   | 1955 | Anti-Mine Plow |
   | 1960 | Paradrop Capability (annotated "Light tanks only - Weight - Fuel consumption - Armour %") |
   | 1965 | Anti-Mine Roller (KMT-5) |
   | 1970 | Integrated Trench-Digging Plow, Anti-Mine Plow (second tier) |
   | 1980 | Anti-Mine Roller With Electro-Magnetic Coils (KMT-7 EMT) |

   Plus RWS I/II/III (1965/1985/2005), blow-out panels (**incompatible with carousel
   autoloaders**), unmanned and semi-unmanned fighting compartment (**requires a
   carousel or belt loader**), unmanned/semi-unmanned turret and superstructure,
   external fuel containers, modular construction, NBC protection, front engine
   placement, external gun mount, fixed superstructure, heavy machine guns as
   `Infantry weapons I`, and 50s/60s/80s/90s MBT hull notes.

   `Amphibious Drive` at 1940 is the node that would retire the legacy
   `amphibious1..5` / `mechanized_marine_equipment_1..5` compatibility line.

   **Slot pressure constrains all of this.** All ten special slots on all three
   archetypes carry an identical 18-entry category list. Every new special competes with
   ammunition, FCS and protection for the same ten slots, and the 41 vehicle envelopes
   were computed without any of them. Do these as small batches keyed to an existing
   module family, each with an explicit slot-budget statement - not as one page-2 sweep.
3. **Night and thermal vision** (page 4). `Zero Gen Night Vision` (1944) through
   `First`, `Second`, `Third Gen` and `Thermal Vision`. Cheapest remaining item to build
   - it fits the existing FCS/optics module family and the slots exist - and the one
   with the least source guidance. Expect to invent the stats and record that.
4. **Trucks and amphibious** (page 7). A bare undifferentiated grid with no design
   content.
5. **The designer composition sketch** (page 8) lists candidate specials that were meant
   to be reachable: belt autoloader, blow-out panels, active protection, ERA, anti-mine
   plow, external fuel tanks, ATGM, unmanned turret, APU, underwater driving, integrated
   trench plow, modular construction, external additional armour, smoke grenade
   launchers. Of these only the autoloaders, APS, ERA, APU and smoke launchers exist
   today. It is a sketch, not a specification; the shipped 15-slot layout is what exists.
