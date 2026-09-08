# CWIC deferred designer scope - handoff

Date: 2026-09-06. Verified against branch `tank-designer-and-doctrine-rework-test`, HEAD
`e526c478f4`, working tree clean. Every number below was produced by a script run or a grep
this session, not copied from an earlier document. Where an older CWIC document disagrees,
this one is the corrected version and says so.

**Purpose.** The tank designer branch reached its stopping point with a block of scope
explicitly cut: mechanized/APC/IFV, artillery, AA, amphibious, night vision, and the design
diagram's page-2 specials. The owner has decided to finish that work across multiple
sessions. This document is the entry point for those sessions: what exists today, what the
2023 sources actually specify, which target numbers are already recoverable, and what must
be decided before code is written.

Read order for a new session: this file, then `Balance_Sources.md` (how the workbook and
diagram decode), then `Balance_Target_Manifest.md` (the frozen tank/mech target rows). Read
`HANDOFF_Tier3.md` and `Tank_Designer_Completion_Plan.md` only for the completed tank work -
their Tier 1/2/3 items are shipped and their scope lists are what this document expands.

---

## 0. Ground truth you should not re-derive

**Sync state.** Local is level with `origin/tank-designer-and-doctrine-rework-test`
(0 ahead / 0 behind), no tracked modifications, nothing staged. All PC-side work is present.

Untracked and therefore device-local, not shared through git:

- `LogDocs/Doctrine_Rework/Doctrine_Rework_Plan.md`, `Doctrine_Cell_Manifest.md`,
  `Land_Doctrine_Tree_Structure.md`, `Doctrine_Icon_Art_Requests.md`
  (only `Doctrine_Rework_Investigation.md` in that folder is tracked)
- `CWIC Backup/documentation/Tank_Designer_Development_Branch_Comparison_2026-09-05.md`
- `CWIC Backup/tools/loc_audit_1.py`, `CWIC Backup/tools/hyprland_uimouse.py`,
  `CWIC Backup/tools/indochina_event_pictures/`, `LogDocs/Indochina/`

If the same filenames exist on the other device they will diverge silently. Commit or delete
them deliberately before the next multi-device session.

**The validator does not live where the docs say it does.** Every prior document writes
`tools/validate_military_reworks.py`. The real path is:

```
python3 "CWIC Backup/tools/validate_military_reworks.py"
```

`tools/` contains only `loc_audit.py` and `hyprland_uimouse.py`. Current output at this HEAD:

```
Doctrine rework is parked under 'common/technologies/doctrine rework/' and is not loaded
by the game; skipping doctrine contracts.
Military rework validation passed: 1287 technologies, 246 tank modules, 125 historical tank
designs, 30 bookmark variants and 460 named OOB requests across 68 NSB OOBs, 76
country-history bootstrap sites, and 15 designer slots checked.
```

1287, not the 1933 quoted by several earlier reports - commits `66c37cf447` and `ee384cee61`
parked the doctrine technology files again. Expected, not a regression.

**Doctrine is parked.** `common/technologies/doctrine rework/` holds land, air, naval and
special forces doctrine where HOI4 does not load them. The validator accepts either
arrangement and rejects only a half-parked mix. Nothing in this document touches doctrine.

---

## 1. Gate: finish the tank branch's QA before opening new scope

The branch comparison report's position, which stands. None of this is new development; it is
acceptance testing of work already committed. Do it first, because every item below adds
sub-units, technologies or equipment on top of it.

1. Re-open both armor technology tabs on final HEAD. `aac8ddfcd2` / `760bb7de6a` moved
   coordinates after the last visual check.
2. Fresh 1949 and 1980 starts, NSB **and** non-NSB. Role activation was changed specifically
   for the non-NSB case (`73c23beb19` set all 15 tank sub-units to `active = yes`).
3. Heavy Siege Cannon still mountable; three representative designs show sane live stats,
   including non-zero conventional-gun soft/hard/piercing.
4. The four export-reward branches (USA-generic, SOV-generic, GRE, FIN): one stockpile branch
   fires, license is usable, no duplicate producer variant.
5. Save, exit to menu, reload. Pre-branch saves are unsupported; use fresh campaigns only.

One standing accept-or-defer decision: the `*_brigade` 3D entities still fall back to default
models (~1,190 `equipment_graphic_database` lines). Cosmetic, ours, needs an explicit call.

---

## 2. Mechanized / APC / IFV - the balance work is already done

This is the headline finding and it changes the shape of the project.

### 2.1 The 18 mechanized envelope rows are already shipped, exactly

`Balance_Target_Manifest.md` freezes 18 mechanized target rows as out of scope for the tank
pass. Those rows map one-to-one onto legacy equipment that already ships, and the numbers
match to the digit. Verified this session by script: **216 stat cells compared across all 18
rows, 1 mismatch, 0 missing.**

| Manifest target | Legacy equipment | Result |
| --- | --- | --- |
| WWII Mech 1-2 (1942, 1944) | `mechanized_equipment_1`, `_2` | match |
| Light Mech I-VIII (1947-2005) | `mechanized_equipment_3` .. `_10` | match |
| Heavy Mech I-VIII (1947-2005) | `mechanized_heavy_equipment_1` .. `_8` | match, 1 year off |

Fields compared per row: `year`, `reliability`, `hardness`, `hard_attack`, `soft_attack`,
`breakthrough`, `defense`, `armor_value`, `ap_attack`, `maximum_speed`, `fuel_consumption`,
`build_cost_ic`, with archetype inheritance resolved (`mechanized_equipment_1` carries only
`year` and inherits the rest from the `mechanized_equipment` archetype).

The single mismatch: **`mechanized_heavy_equipment_3` declares `year = 1955`, while the
Heavy Mech III target row says 1960.** Stats are correct; only the year differs. Decide
whether the equipment moves to 1960 or the workbook row is wrong - it is the sole open
numeric question in the whole mechanized block.

The comparison script is in the session scratchpad and is about 60 lines; rebuild it from the
field list above rather than hunting for it.

### 2.2 Light Mech is the APC line and Heavy Mech is the IFV line

Not stated in any prior document, and it resolves what the two ladders are *for*:

- Light Mech I-VIII carry hard attack 0, soft attack 0, piercing 0 throughout - a troop
  carrier, i.e. APC.
- Heavy Mech IV-VIII match the workbook `Work Sheet` tab's **IFV** column exactly:

| Year | Work Sheet IFV (soft / hard / pierce) | Heavy Mech row | Match |
| ---: | --- | --- | --- |
| 1965 | 12 / 8 / 24 | Heavy Mech IV | yes |
| 1975 | 12 / 8 / 26 | Heavy Mech V | yes |
| 1985 | 12 / 8 / 30 | Heavy Mech VI | yes |
| 1995 | 14 / 9 / 32 | Heavy Mech VII | yes |
| 2005 | 14 / 9 / 34 | Heavy Mech VIII | yes |

So `mechanized.txt` is the APC ladder and `mechanized_heavy.txt` is the IFV ladder, already
balanced against the 2023 sources. `mechanized_marine.txt` (`mechanized_marine_equipment_1..5`)
is the amphibious variant of the same idea - see section 4.

### 2.3 What is therefore actually missing

Only the designer conversion. Confirmed absent today: `grep -iE '\b(apc|ifv)\b'` over
`common/units/equipment/tank_chassis.txt` and `common/units/equipment/modules/00_tank_modules.txt`
returns **zero hits**. There is no APC/IFV chassis, no role duplicate, no AI recipe, no GUI.

The 2023 sources already specify the design:

- `Roles` tab: light hull hosts APC, IFV, Light Tank, Light TD, LL/LM/LH SP artillery, Light
  SPAA, ATGM Carrier. Medium hull hosts Heavy APC, Heavy IFV, MBT, Medium TD, ML/MM/MH SP
  artillery, Medium SPAA, ATGM Tank. Heavy hull hosts Heavy Tank, Heavy TD, HL/HM/HH SP
  artillery.
- `Total Balance Sheet Object 842` tab: role penalty rows - APC -0.4 hardness and armor,
  IFV -0.2, Artillery -0.4. These are the deltas a designer role would apply.
- Diagram page 10 chains Early/Mid/Late WW2 Mechanized into APC and Heavy APC/IFV, then
  Light Mechanised II-VII and Heavy Mechanised II-VII.
- Diagram page 9 (`Light Chassis Based Vehicles`, 1014 nodes) is the per-nation historical
  reference and carries the role-availability matrix per chassis generation. ATGM first
  appears at the Early Cold War Light Tank / First Gen MBT row.

### 2.4 The decision this forces

Because the numbers are already correct in the legacy ladders, an APC/IFV designer is not a
balance project - it is a re-plumbing project whose success criterion is *reproducing these
same 18 envelopes through modules*. Two coherent paths:

- **Keep the legacy ladders.** Cost: nothing. The mechanized line stays a tech ladder while
  armor is a designer. Accepts the same structural inconsistency the artillery line has.
- **Build the designer roles.** Cost: chassis duplicates on the light and medium hulls, role
  penalty modules, AI recipes, bookmark variants, OOB and country-history bootstrap, designer
  GUI files, loc, and a validator contract - the same surface the tank pass took, minus the
  balance research. The 18 envelopes become the acceptance test.

Decide this before anything else in section 2 is started. It is the single largest scope
question remaining in the project.

---

## 3. Artillery and AA - the largest structural gap, and the weakest sources

### 3.1 What runs today

`common/technologies/artillery.txt` holds **85 technologies in 17 five-step families**, all
unconditional, all unlocking whole equipment models rather than designer modules:

```
artillery          light_artillery     heavy_artillery     art_ammo      art_upgrade
sp_artillery       light_sp_artillery  heavy_sp_artillery  sp_rocket
autocannon         spaag               aa_upgrade          cannon_ammo
direct_fire_gun    tank_destroyer      at_ammo             at_upgrade
```

Their equipment ladders, all five-tier plus archetype:

| File | Equipment |
| --- | --- |
| `artillery.txt` | `artillery_equipment_1..5`, `rocket_artillery_equipment_1..2` |
| `light_artillery.txt` / `heavy_artillery.txt` | `light_/heavy_artillery_equipment_1..5` |
| `sp_art.txt` / `light_sp_art.txt` / `heavy_sp_art.txt` | `*_sp_artillery_equipment_1..5` |
| `anti_air.txt` | `auto_cannon_equipment_1..5` |
| `anti_tank.txt` | `direct_fire_gun_equipment_1..5` |
| `rocket_artillery.txt` | `motorized_rocket_equipment_1..5` |
| `atgm_carrier.txt` | `atgm_carrier_equipment_0..4` |
| `sam_carrier.txt` | `sam_carrier_equipment_1..6` |

**Activation pattern, important.** Every sub-unit in `CWIC-Artillery.txt`, `CWIC-Anti-Air.txt`
and `CWIC-Anti-Tank.txt` carries `active = no` and is switched on by its tier-1 technology's
`enable_subunits`. That is the same contract the tank roles use through
`nsb_iw_armored_vehicles`. Any replacement ladder must keep some technology enabling these
sub-units or it deletes artillery, AA and anti-tank from play - this is exactly the failure
mode the Tier 3 pass caught with the flame roles.

**Three parallel lines, not two.** `sam_carrier` and `atgm_carrier` are enabled from
`common/technologies/rocket.txt`, not `artillery.txt`. Any AA rework touches the guided
missile line as well.

**The overlap with the designer already exists.** The designer ships SPG, SPAA and tank
destroyer *chassis roles* with 125 AI recipes, while `sp_artillery_*`, `spaag_*` and
`tank_destroyer_*` run the legacy stat ladder in parallel every game. This is the largest
structural inconsistency in the military system and it is deliberate current behaviour.

### 3.2 What the 2023 sources specify

Diagram page 6 (`Artillery`, 256 nodes / 93 edges) designs six-step ladders, each anchored to
real guns per year: `Medium Artillery I-VI` interleaved with `Artillery Modernisation I-VI`,
`Light Artillery I-VI`, `Heavy Artillery I-VI`, `Artillery Ammunition I-VI`,
`AA Autocannon I-VI` with `AA Modernisation I-VI`, and `AA Ammunition I-VI`. Named anchors
include ML-20 152mm (1937), D-20 152mm (1947), M-46 130mm (1951), S-60 57mm (1950), 61-K 37mm
(1941).

### 3.3 The target numbers exist - in `Work Sheet`, and they are scratch quality

Unlike the tank modules, artillery and AA targets were never promoted into `Total Balance
Sheet`. They live in the `Work Sheet` tab (sheet14), which is unlabelled, mixed-language
(cell AN5 reads `pomenyat` in Cyrillic, i.e. "change") and never frozen. Extracted verbatim
this session:

**SPAAG - air attack only**

| Year band | Air attack |
| --- | ---: |
| 1935-1940 | 12 |
| 1950-1955 | 14 |
| 1965-1970 | 16 |
| 1980-1985 | 20 |
| 1995-2000 | 24 |

**SAM - air attack only**

| Year | 1955 | 1965 | 1975 | 1985 | 1995 | 2005 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Air attack | 35 | 45 | 60 | 75 | 90 | 105 |

**SP artillery - soft / hard / piercing / breakthrough / defense**

| Year | SP Light | SP Medium | SP Heavy |
| ---: | --- | --- | --- |
| 1945 | 24 / 6 / 12 / 7 / 10 | 32 / 6 / 12 / 8 / 7.5 | 40 / 9 / 6 / 9 / 5 |
| 1960 | 27 / 8 / 14 / 8 / 12 | 36 / 8 / 14 / 10 / 9 | 45 / 12 / 7 / 11 / 6 |
| 1975 | 33 / 10 / 16 / 10 / 14 | 44 / 10 / 16 / 11 / 10.5 | 55 / 15 / 8 / 13 / 7 |
| 1990 | 39 / 12 / 18 / 11 / 16 | 52 / 12 / 18 / 13 / 12 | 65 / 18 / 9 / 14 / 8 |
| 2005 | 45 / 14 / 20 / 13 / 18 | 60 / 14 / 20 / 14 / 13.5 | 75 / 21 / 10 / 16 / 9 |

Note the SP Heavy piercing column (6-10) is deliberately far below SP Light (12-20) - big
low-velocity howitzers. It is not a transcription error.

**Anti-tank - soft / hard / piercing / breakthrough / defense**

| Year | 1940 | 1955 | 1970 | 1985 | 2000 |
| --- | --- | --- | --- | --- | --- |
| AT | 12 / 15 / 30 / 13 / 10 | 14 / 20 / 35 / 15 / 12 | 17 / 25 / 40 / 18 / 14 | 30 / 30 / 45 / 20 / 16 | 46 / 35 / 50 / 23 / 18 |

**Module cost bands the workbook already reserved for artillery and AA** (`Category | cost min
| 1950 | cost max | iterations`):

```
Aiming AA      0.5   3     6.6   5
Optics AA      0.5   ---   9     6
Optics Arty    0.5   ---   8     2
Computer Arty  5.25  ---   7.5   4
Radar          4     ---   8.5   7
Mech ammo arty 2.5   3.5   4.5   3
```

Somebody planned artillery and AA fire-control modules and never built them.

### 3.4 Required first step

Before any artillery or AA ladder is implemented, these tables must go through the same
freeze the tank targets did: normalized, provenance-stamped, and written into a manifest
beside `Balance_Target_Manifest.md`. Building against an unfrozen scratch tab is how the
turret stubs happened. Note the year grids do not agree with each other (SPAAG uses bands,
SAM uses single years, SP uses 1945/1960/1975/1990/2005, AT uses 1940/1955/1970/1985/2000)
and none of them match the workbook `Years` tab's 18 canonical years. Reconciling the year
grid is part of the freeze, not an implementation detail.

To re-extract: the tab is `xl/worksheets/sheet14.xml`; use the standard-library recipe in
`Balance_Sources.md` (openpyxl is not installed and was deliberately not added).

---

## 4. Amphibious - three different things, do not conflate them

1. **Legacy amphibious technologies, live.** `amphibious1..5` in
   `common/technologies/armor.txt` grant `mechanized_marine_equipment_1..5`. `73c23beb19`
   moved them from x=14 to x=-3 in `nsb_armor_folder` only, because two of them shared a cell
   with `nsb_heavy_tanks0` and `nsb_heavy_tanks2`. They are dual-foldered into both
   `armour_folder` and `nsb_armor_folder`, which is why the marine mechanized chain is safe
   with and without NSB.
2. **The designer amphibious role, deleted.** No chassis duplicate, no AI design, no script
   reference; `ff036b399b` and the later 24-file purge removed its GUI. Rebuilding it is new
   work, not a restore.
3. **`mechanized_marine` sub-unit is `active = no` and the validator asserts it stays that
   way.** This is the project's precedent for a deliberately parked role. Any amphibious work
   must change that assertion consciously.

Diagram page 7 (`Trucks & Amphibious`, 29 nodes / 10 edges) is a bare grid of `Truck I` and
`Amphibious I` repeating down the year column with no differentiated nodes - designed, but
never designed out. There is no target block for it anywhere in the workbook. If amphibious
becomes a designer module rather than a chassis line, the natural home is a special-slot
module (`amphibious_drive` appears on diagram page 2), which is far cheaper than a role.

---

## 5. Night and thermal vision

Diagram page 4 designs `Zero Gen Night Vision` (1944), `First`, `Second`, `Third Gen Night
Vision` and `Thermal Vision`. The workbook reserved a `Night & Thermal Vision Effects` tab
(sheet6) for the numbers and **left it empty**.

In the mod today: one orphan `night_vision` string in
`common/technology_tags/00_technology.txt` line 42. Nothing else - no technology, no module,
no equipment.

So this line has a design, no numbers, and no implementation. It is the cheapest of the
remaining items to build (it fits the existing FCS/optics module family and the special
slots already exist) and the one with the least source guidance. Expect to invent the stats
and to record that they were invented.

---

## 6. Diagram page 2 - the specials

`Base & Other Tech Modules` (42 nodes / 2 edges), described in `Balance_Sources.md` as
"almost entirely unbuilt". The full list, with the dependencies the page itself records:

- Remote weapon stations `RWS I/II/III` (1965 / 1985 / 2005)
- Blow-out panels - the page notes these are **incompatible with carousel autoloaders**
- Unmanned and semi-unmanned fighting compartment - **requires a carousel or belt loader**
- Dozer plough -> anti-mine plough -> integrated trench-digging plough
- Anti-mine rollers (KMT-5, KMT-7 EMT)
- External fuel containers
- Underwater driving
- Modular construction, NBC protection
- Front engine placement, external gun mount, fixed superstructure
- Amphibious drive (see section 4)
- Heavy machine guns as `Infantry weapons I`
- A `Log` module, +2% reliability

Of these the mod has only the turret and superstructure modules, and those were never in the
workbook - they are the "script-owned" set documented in `Balance_Target_Manifest.md`.

Two structural facts that constrain this work:

- **Slot pressure.** All ten special slots on all three archetypes carry an identical
  category list, currently 18 entries after secondary armament was added. Every new special
  competes with ammunition, FCS and protection for the same ten slots, and the 41 vehicle
  envelopes were computed without any of them.
- **No new slot is available.** The designer GUI defines exactly 15 positions, the validator
  asserts `pos_custom_module_slot_window_0..14`, and `equipment_modules` is 515 wide against
  a seventh column ending at exactly 515 - zero slack. Any slot frame wider than 76px
  re-clips.

Do these as small batches keyed to an existing module family, not as one page-2 sweep.

---

## 7. Envelope calibration - the shared prerequisite

`--tank-envelope-report` parses 35 shipped recipes and maps only **11 of the 21** tank target
generations; 10 are explicitly unsampled, and the sampled static estimates differ
substantially from target in attack, breakthrough, speed and piercing. The tool does not model
engine ordering, caps, role bonuses, or several game semantics, and no tolerance bands were
ever agreed - so it is a calibration backlog, not a failing gate.

It matters here because it is the same machinery any mechanized, artillery or AA envelope
check would reuse. If section 2.4 chooses the designer path, calibrate this tool first;
otherwise the APC/IFV work will be verified by a tool that cannot yet reproduce known-good
tank designs.

---

## 8. Decisions the owner must make before implementation

1. **Mechanized: keep the legacy ladders, or build APC/IFV designer roles?** (section 2.4)
   Everything else in section 2 depends on this.
2. **`mechanized_heavy_equipment_3`: year 1955 or 1960?** (section 2.1)
3. **Artillery/AA: replace the legacy ladders, or NSB-gate them?** The `support.txt` pattern
   `OR = { has_tech = legacy has_tech = nsb_* }` already exists in the repo for exactly this.
   Replacement means 85 technologies and 11 equipment ladders retire; gating means both run
   and the player sees whichever their DLC profile supports.
4. **Do the `Work Sheet` artillery/AA/AT/SAM targets get frozen into a manifest first?**
   (section 3.4) Recommended yes, and it includes reconciling four disagreeing year grids.
5. **Amphibious: designer role, special-slot module, or leave the legacy line alone?**
   (section 4)
6. **Night vision: invent the numbers, or leave the line unbuilt?** (section 5)
7. **Page-2 specials: which ones, given every one costs a special slot?** (section 6)

---

## 9. Suggested session sequencing

Each session should end with the validator green and a committed working tree.

1. **Session A - close the branch.** Section 1's five QA items plus the 3D entity decision.
   No new content. Also resolve the untracked-docs question in section 0.
2. **Session B - freeze the artillery/AA targets.** Produce
   `Artillery_AA_Target_Manifest.md` beside the existing manifest: normalized tables,
   worksheet-row provenance, workbook SHA, a reconciled year grid. Script only, no game
   changes. Answers decision 4 by doing it.
3. **Session C - mechanized decision and, if designer: the chassis/role skeleton.** Start
   from the 18 verified envelopes as the acceptance test. Fix decision 2 either way, since it
   is one line.
4. **Session D - artillery/AA ladder implementation** against Session B's manifest, keeping
   the `active = no` + `enable_subunits` activation contract intact.
5. **Session E - specials and night vision**, in small batches, each with an explicit
   slot-budget statement.

Envelope calibration (section 7) slots in before whichever of C or D goes first, if either
takes the designer path.

---

## 10. Working rules carried forward

**Validation, after every meaningful change:**

```bash
python3 "CWIC Backup/tools/validate_military_reworks.py"
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-self-test
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-balance-report
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-module-balance-report
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-envelope-report
python3 tools/loc_audit.py --check
git diff --check
```

`git diff --check` reporting trailing whitespace in `GRE - Greece.txt` is expected; that file
is CRLF in the index.

**Runtime**, once per tier of work. Launch detached - a tracked background game process gets
killed under memory pressure during load:

```bash
cd "<steam>/steamapps/common/Hearts of Iron IV"
setsid nohup ./run_hoi4 -mod=mod/Cold_War_Iron_Curtain.mod -debug -ai_testing >/dev/null 2>&1 &
```

`-ai_testing` starts the default bookmark only and does not accept a start-date argument. The
live log is `~/.local/share/Paradox Interactive/Hearts of Iron IV/logs/error.log`; diff it
against a baseline captured before the change.

**Localisation:** ASCII only - the files are read as ANSI and non-ASCII renders as `?`.
English only; never touch `french/` or `japanese/`.

**Protected - do not stage, edit or delete:** `CWIC Backup/` (excluding the validator, which
is tracked and maintained), root `HANDOFF.md`, root `error.log` / `error_1.log` /
`error_2.log` / `game.log`. The root logs are stale (2026-09-02) and are not current evidence.

**Sources are frozen.** `LogDocs/Tank_Designer/2023 - CWIC Tank Rework Balance.xlsx` must stay
byte-identical - `--tank-balance-report` checks its SHA-256
(`dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`). The living document is
the CSV mirror in the same folder. The drawio pages carry `[DONE]` / `[TODO]` / `[REFERENCE]`
/ `[STATUS]` prefixes; keep them accurate as scope closes.

**Commit trailers:** no commit on this branch carries a `Co-Authored-By` or `Claude-Session`
trailer. Match the surrounding history unless the owner says otherwise.

**Ignorable engine noise, already triaged - do not chase:** ~255
`Entity referenced in equipment graphic database does not exist` and
`Unknown equipment type: modern_tank_chassis / super_heavy_tank_chassis` lines come from the
base game's graphics database referencing equipment this mod deliberately removed. Zero hits
under `Cold War Iron Curtain/`.
