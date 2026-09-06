# CWIC Tank Designer - Tier 3 handoff

> RATIFICATION PASS, 2026-09-05. Sections 5.3 and 6 are now decided and applied; see
> "Ratified decisions" immediately below before reading the historical text. Two reported defects
> were retracted after measurement: the AA/flamethrower/niche sprites resolve against the base game
> and are not broken, and `nsb_armor_modules_folder` is not missing a year label. Section 3's
> `active = no` conclusion is reversed.
>
> Finalization correction, 2026-09-05: follow the ratified decisions above before acting on this
> historical handoff. The Luna implementation manual it used to cite has been retired; its rules are
> now recorded here. Do not add `nsb_armor_modules_tree` or move the vanilla intel side panel.
> Screenshot the designer before choosing header coordinates; never accept seventh-slot overlap.
> Sections 5–8 below retain historical proposals where marked, not implementation authority: the 22
> missing IDs are now reconciled; use the authoritative master module schema, not the
> superseded Gun Modules draft; preserve existing gameplay/XP/activation values. The current target
> scope is 21 tanks among 40 reviewed rows, not 41 envelopes. Research changes remain proposal-only.
> The manual supplies the replacement schema, workbook-preservation, validation and acceptance rules.

## Ratified decisions (2026-09-05)

| # | Decision | Outcome |
| --- | --- | --- |
| 5.3.1 | Reliability expressed two ways | **Kept split.** Guns use a negative multiplier, turrets a positive flat add. Units genuinely differ; converting would touch 13 blocks for cosmetic consistency. No script change. |
| 5.3.2 | `cwic_hull_mg` flat `defense = 0.5` | **Reduced to 0.25.** Script, CSV, both workbook tables updated. |
| 5.3.3 | Secondaries lacked reliability cost | **All four now carry one:** coax -0.005, hull MG -0.005, HMG -0.01, autocannon -0.025 unchanged. |
| 5.3.4 | Turret cost ordering | **LP premium kept; 1.5 tie broken.** `oscillating_turret` 1.5 -> 1.75, dismantling 0.75 -> 0.875 to preserve the file-wide 0.5 ratio. |
| 5.3.5 | 12 of 15 sub-units `active = yes` | **Normalised to `active = yes`, not `no`.** The manual's recommendation was wrong: legacy `armor.txt` enables only `light_armor`, `medium_armor`, `heavy_armor`, `super_heavy_armor`. The 9 role brigades and 3 flame tanks are enabled only by `nsb_iw_armored_vehicles`, so in a non-NSB profile `active = yes` is the sole thing making them buildable. Setting them to `no` would have deleted them from non-NSB play. The validator contract was inverted to match. |
| 5.3.6 | `tank_gasoline_engine` home + missing `xp_cost` | **Base engine, not a duplicate.** It is `Petrol_0`'s declared `parent` and the `engine_type_slot` default at `tank_chassis.txt:391, 795, 1200`; folding it in would orphan those defaults. Gains `xp_cost = 1` and `dismantle_cost_ic = 0.5`. |
| 6 | Research cost curve | **Ratified and applied.** R1-R7; 91 of 169 technologies repriced; 337 -> 345.5 (+2.52%); USA/SOV 1970 -1.67%, 2020 +8.33%. |
| 6 | XP economy | **Flat at 1, deliberate.** No repricing. Question closed. |

Retracted after measurement, do not re-open:

- **The AA/flamethrower sprites are not broken.** `tank_module_aa_gun{,_2,_3}.dds`,
  `tank_module_flamethrower.dds`, `EMI_tank_flamethrower.dds` and `Niche_icon_strip.dds` all exist in
  the base game under `gfx/interface/equipmentdesigner/tanks/{modules,icons}/`, which the mod does not
  shadow. HOI4 resolves sprite paths mod-first then vanilla. The live `_local/logs/error.log` shows zero texture
  misses for them. Checking only the mod directory produced the false positive.
- **`nsb_armor_modules_folder` is not missing a year column.** Labels sit at x=20/1450/3100 against
  trees at x=428/1950/3600 - one per tree. `_mid_left` merely sorts after `_mid` by position. The
  `nsb_armor` folder's fourth label at x=4000 is the anomaly, sitting beyond its last tree at x=2400.

Modules: `Optics_0` (Direct Vision Optics) and `AA_Optics_0` (Anti-Air Optics 1) were added by hand
as the forgotten tier-0 entries of the optics and SPAAG-optics ladders, modelled on their modernized
siblings. Their balance rows already existed as placeholders carrying only `build_cost_ic = 0` and a
dismantling cost, so the script values were mirrored into the CSV and both workbook module tables.

Tech tree: a manual aesthetic repositioning pass introduced four same-cell collisions, resolved by
unifying each family into one column - `nsb_main_battle_tanks0`-`2` x=10 -> x=12 to join siblings
3-8, `nsb_suspension3` to (18,12), and `nsb_autoloader0`-`2` x=-4 -> x=-2 to join siblings 3-6, which
leaves x=-4 to the low-pressure gun ladder. `amphibious1`-`amphibious5` moved from x=14 to x=-3 in `nsb_armor_folder` only, placing
them left of `mechanized_infantry` at x=0. At x=14 they were in the heavy tank column and two of them
occupied the *same cell* as a heavy tank (`amphibious1`/`nsb_heavy_tanks0` at y=0,
`amphibious2`/`nsb_heavy_tanks2` at y=4). Both folders now resolve to zero coordinate collisions with
year anchors expanded. The legacy `armour_folder` was already collision-free and was left untouched.

3D entities: `gfx/entities/zz_CWIC_armor_level0_entities.asset` adds 62 clone aliases so every
`<TAG>_<light|medium|heavy>_armor_0_entity` the equipment graphic database derives now resolves to
that country's existing base armor entity. Only 29 of 67 tag/class combinations defined a `_0` entity,
which is why opening the production tab on armor and hovering designer modules spammed
`equipment_model_util` at roughly one line per hover. The filename is `zz_`-prefixed deliberately: it
must load after every other `.asset`, because all 278 existing clones in the mod resolve backward and
none forward. This closes the reported symptom; the separate `*_brigade` entity gap is unaffected.

Localisation: `nsb_optics7` no longer duplicates `nsb_optics5`; nine over-long names shortened. The
`nsb_ap_du_ammo` family uses "DU Long-Rod APFSDS" - dropping "Elongated Projectile" outright would
have collided with `nsb_ap_ammo7` "Modern Depleted Uranium APFSDS Ammunition". No display name now
exceeds 55 characters and no two technologies share one.

Designer UI: `tag_icon_bg` 465 -> 461 and `niche_button` 474 -> 470, aligning the role group to the
`design_company_icon` rail at x=461. The premise that overlaying `equipment_preview` is a defect did
not survive measurement - `design_company_icon`/`design_team_button` at (461,382) sit inside the same
preview rectangle, so floating icons over the blueprint is the panel's existing layout language.
The zero-slack boundary stands: module column seven spans x 452..528 inside a 515-wide container, so
any slot frame wider than 76px re-clips.

---

Written 2026-09-05 at the end of the verification/repair passes. Everything below was checked against
the repo, not copied from an earlier report. Where a number appears, it came from a script run in that
session.

Companion documents:

- `Manual_Test_Checklist.md` - the live test checklist, sections 0-8, with pass-1 and pass-2 results.
- `Tank_Designer_Completion_Plan.md` - the original tiered plan. Tier definitions there still stand.
- `Balance_Target_Manifest.md` - frozen 40-row review manifest + coverage table + workbook SHA.
- `2023 - CWIC Tank Rework Balance.xlsx` - now has an `Implementation Status` worksheet (16th sheet).
- `Tank_Designer_Slimemix (1).drawio` - pages prefixed `[DONE]` / `[TODO]` / `[REFERENCE]` / `[STATUS]`.
- `Research_Cost_Proposal.md` - the ratified and applied R1-R7 pricing schedule.
- `Rework_Audit.md`, `Balance_Sources.md`, `Doctrine_Rework_Handoff.md` - earlier audits, moved into
  this folder from `LogDocs/` root during the 2026-09-05 consolidation.

---

## 1. Where the project actually stands

**Tier 1: complete.** Including the plan's open question 1 - `active = no` on the three flame
sub-units is correct, not a bug. `nsb_iw_armored_vehicles` enables all 15 sub-units through
`enable_subunits` (NSB_armor.txt:78), so they are tech-gated rather than dead.

**Tier 2: complete.** Validator gap closed, secondary armament layer shipped, hull upgrade sliders
retained, four export-variant focus branches fixed, 24 orphan designer GUI files purged, NSB tech
hygiene done.

**Balance fidelity: verified.** 25 hulls and all 246 live modules match the CSV, minimal workbook,
and master workbook. The new module report checks 5,106 populated stat/resource cells across the
three mirrors and records operation/provenance metadata for all 22 formerly missing script-owned IDs.
The manual's 23 count is an arithmetic inconsistency with no additional module ID. Every balance row
is defined in script and reachable through a technology.

**Tier 3: static reconciliation delivered; runtime evidence remains open.** Detailed in section 4.

The baseline validator modes and the new module/envelope reports pass:

```
python3 tools/validate_military_reworks.py --tank-self-test
python3 tools/validate_military_reworks.py --tank-balance-report
python3 tools/validate_military_reworks.py --tank-module-balance-report
python3 tools/validate_military_reworks.py --tank-envelope-report
```

---

## 2. What the last two passes changed - do not redo this

| Area | Change |
| --- | --- |
| Focus rewards | All four export branches now create the variant and issue `create_production_license` on the **same** tag (FIN/SOV, GRE/CAP, `60s_Generic` USA-branch/CAP, `60s_Generic` SOV-branch/CUM). The fourth branch was missed in the first review. |
| Focus rewards | Legacy stockpile grant is now `else_if` nested in the NSB `if` in all four - one generation granted, never both. |
| SPAAG | `tank_anti_air_cannon` air attack reverted to 18/32/46 (an unsourced nerf to 12/14/20 had been applied and misdescribed as a raise). Validator's hardcoded expectation updated to match. |
| Validator | `BALANCE_WORKBOOK_FILE` repointed to `LogDocs/Tank_Designer/...xlsx`; `--tank-balance-report` had been failing with "workbook is missing" while the report claimed it passed. |
| texticons | `interface/texticons.gfx` is a **full override** of vanilla and was silently dropping 294 entries. All restored. This alone was 1,002 log lines. |
| texticons | `GFX_unit_super_heavy_armor_icon_small` repointed to the real vanilla file. |
| Localisation | 9 tank-role sub-units (`*_tank_destroyer_brigade`, `*_sp_artillery_brigade`, `*_sp_anti_air_brigade`) given names + descriptions. All 15 sub-units in `need_for_tank_roles.txt` now have loc. |
| Localisation | "Ballisitc" -> "Ballistic" (7 places); 10 non-ASCII characters stripped from `nsb_armor_l_english.yml`, including a Cyrillic `С` opening "Сonveyor belt type autoloader". |
| Tech tree | 31 mechanical tech relocations reverted; the 11 genuine collisions resolved keeping each family in one straight column. `aiming_devices` -> x=10, `ballistic_calculator` -> x=14, `optics` stays 12, `superheavy_guns1` -> 16, `main_battle_tanks2` -> 12, `nsb_iw_armored_vehicles` -> 8. |
| Tech tree GUI | Tech name label `120x50` -> `168x72` in the six CWIC-authored `techtree_*_item` blocks. Names over budget: 29 -> 7. |
| Docs | CSV gained `Script-Owned [NEEDS REVIEW]` + `Coverage [STATUS]`; workbook gained an `Implementation Status` sheet; drawio pages got status prefixes and a `[STATUS]` page. |

---

## 3. error_4.log - confirmed the pass-2 fixes landed

Do a full triage next session, but the delta is already measured:

| Signal | error_3.log | error_4.log |
| --- | ---: | ---: |
| Total lines | 9,296 | 7,639 |
| `Couldnt find texticon: flame_texticon` | 1,002 | **0** |
| `unit_super_heavy_armor_icon_small` | 3 | **0** |
| `equipment_model_util` | 740 | 94 |
| `equipment_graphic_database` | 1,190 | 1,190 |

`equipment_graphic_database` at 1,189-1,190 is now the single largest block, 16% of the log. It plus
`equipment_model_util` is the missing-3D-entity family: the engine derives
`<TAG>_<subunit>_<level>_entity` for the new `*_brigade` sub-units and finds nothing. 13 distinct
names. Cosmetic (default model fallback), needs art or a graphic-database remap onto existing armor
entities. The historical `_local/logs/error_4.log` confirms that all remaining 94 `equipment_model_util` lines
are the same `USA_light_armor_0_entity` missing-entity family; `equipment_graphic_database` remains
at 1,190. This is historical confirmation, not a fresh Tier 3 runtime run, so fresh provenance is
still required.

Everything else in the log is pre-existing non-tank content: China/Malaya/Japan/WWN effects and
triggers, leader-portrait and culture-icon texture misses, and 214 cosmetic "Missing icon shine"
focus lines.

---

## 4. Tier 3 work items

### T3.1 - `countrytechtreeview.gui` armour folder repair (static done, runtime pending)

The label enlargement is done. Still missing, verified by grep:

- **Withdrawn: do not add `nsb_armor_modules_tree`.** The four-piece rule was unsupported. The
  modules folder already has `nsb_light_guns_tree`, `nsb_ammo_tree` and `nsb_tank_design_tree`.
  Verify actual rendering; script reachability does not establish visual completeness.
- no `nsb_armor_modules_small_year_right` (the `nsb_armor` folder has `..._left`, `_mid_left`,
  `_mid`, `_right`; the modules folder stops at `_mid`). Add/reposition labels only if rendered
  inspection establishes a need; names and missing symmetry alone do not prove a defect.
- the armour tab uses `GFX_armour_folder_tab`; the modules tab currently uses `GFX_artillery_folder_tab`.
  No tank-module tab art exists in the mod. Runtime inspection and an art decision are pending; no
  replacement asset was guessed.
- `techtree_armour_folder_small_item` **does** now exist - the plan's claim that it was missing is
  out of date.

Verify by loading a profile without the No Step Back DLC. Estimate: half a day.

### T3.2 - Designer UI structural pass (not started)

The resolution sweep is ticked in the checklist, but these structural defects were never examined:

- `tag_icon_bg` (465,212) and `niche_button` (474,219) are **siblings** of `equipment_modules`, not
  children, so they do not track it, and both now overlay `equipment_preview` (3,50, 508x248).
- `equipment_modules` is 515 wide against a 7th column ending at exactly 515 - zero slack, so any
  slot frame wider than 76px re-clips.
- **Not a defect:** `designer_intel_container` at x=1088 and root `clipping = no` match vanilla
  according to Opus's inspection. Preserve them. Sibling ownership of role controls is also not
  itself a defect. Leave the 515-wide modules container unless current rendering shows clipping.

Mandatory gate: screenshot the populated designer and opened niche selector before editing. The
proposed header strip may contain runtime-injected name/chassis controls. Move the entire role-control
group and popup into measured free space, or reflow the smallest local group. Never accept overlap
with column seven or the blueprint. If runtime verification is unavailable, leave this item pending.

Recorded lesson from the handoff, worth repeating: on this panel *"it still responds to clicks"* does
**not** rule out an overlay, because most decorative icons here are `alwaystransparent`. Estimate:
half a day to a day.

### T3.3 - Workbook envelope validation (static implemented, runtime calibration pending)

Report shipped designs against the frozen manifest's 21 tank targets. Its other reviewed rows are
18 out-of-scope mechanized targets and one Abrams reference (40 total). These are point targets,
not specified tolerance bands. Explicitly map recipes and report unsampled targets. Static composition
remains an estimate until calibrated against runtime observations; unsupported semantics stay unknown.
`--tank-envelope-report` now parses 35 shipped recipes, maps 11 exact target generations, keeps SPAA
and SPG recipes separate, expands module parents, counts repeated slots, and reports static deltas.
Ten target generations are explicitly unsampled because no exact-year shipped recipe exists. The
static composition remains an estimate until calibrated against runtime observations; unsupported
semantics stay unknown. Follow manual section F for the runtime acceptance contract.

---

## 5. The 22 script-owned modules - balance row plan

These exist in `common/units/equipment/modules/00_tank_modules.txt`. Their 22 authoritative rows now
exist in both workbook module tables and the CSV mirror; no balance change was made. This is why the
SPAAG nerf was reverted rather than judged.

### 5.1 The established conventions to copy

Two different schemas already exist in the workbook. **Use the matching one per family - do not
invent a third.**

**Schema A - `Gun Modules` worksheet** (armament). Columns: `Type | Year | Name | Abbreviation |
Loc Name | Reliability | Hard attack | Soft attack | Piercing | Production cost | Max speed`.
Combat stats are **multipliers**, production cost is a **flat add**, reliability is a negative
multiplier that scales with gun weight. Worked example, the light gun ladder:

```
tank_light_cannon0  1939  rel -0.05  hard 0.45  soft 0.45  pierce 0.35  cost 1.5
tank_light_cannon9  2015  rel -0.10  hard 1.05  soft 1.05  pierce 0.95  cost 10.5
```

Per-tier step: attack +0.05/+0.10, piercing +0.05/+0.15, cost +1. Reliability penalty by class:
light -0.05, medium -0.10/-0.15, heavy -0.20, super heavy -0.30, MBT heavy -0.25,
low-pressure -0.025.

**Schema B - `Total Balance Sheet Minimal`** (everything else, and what the CSV mirrors). Flat adds
plus separate `, %` multiplier columns per stat.

**The workbook already anticipates this work.** `Gun Modules` rows 43-44 are `Ammo | Primary` and
`Ammo | Secondary` - both **empty**. The `Secondary` row is the intended home for the four `cwic_*`
secondary-turret modules. Somebody planned this and never filled it in.

### 5.2 Current script values - the starting point

Read straight from script this session. `mult` = `multiply_stats`, everything else `add_stats`.

**Turrets and superstructures (13)** - all `tank_*_turret_type`:

| Module | cost | reliability (add) | mult |
| --- | ---: | ---: | --- |
| `pintle_turret` | 0.5 | +0.05 | breakthrough -0.1 |
| `light_turret` | 1.0 | +0.15 | - |
| `light_lp_turret` | 1.25 | +0.10 | defense +0.05 |
| `conventional_turret` | 1.0 | +0.15 | - |
| `lp_turret` | 1.5 | +0.10 | defense +0.10 |
| `oscillating_turret` | 1.5 | +0.05 | breakthrough +0.1 |
| `open_gun` | 0.5 | +0.10 | breakthrough -0.2, defense -0.1 |
| `medium_open_gun` | 0.75 | +0.10 | breakthrough -0.2, defense -0.1 |
| `heavy_open_gun` | 1.0 | +0.10 | breakthrough -0.2, defense -0.1 |
| `external_gun` | 1.25 | +0.05 | breakthrough -0.05, defense +0.1 |
| `fixed_superstructure` | 0.75 | +0.20 | breakthrough -0.15, defense +0.05 |
| `medium_fixed_superstructure` | 1.0 | +0.20 | breakthrough -0.15, defense +0.05 |
| `heavy_fixed_superstructure` | 1.25 | +0.20 | breakthrough -0.15, defense +0.05 |

**Anti-air cannons (3)** - armament, so Schema A, except `air_attack` which has no multiplier
equivalent and stays a flat add:

| Module | soft | hard | ap | air | cost | reliability |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `tank_anti_air_cannon` | 6 | 2 | 10 | 18 | 2 | -0.1 |
| `tank_anti_air_cannon_2` | 8 | 5 | 18 | 32 | 3 | -0.1 |
| `tank_anti_air_cannon_3` | 10 | 5 | 24 | 46 | 4 | -0.1 |

**Secondary turrets (4)** - the `Gun Modules > Ammo > Secondary` placeholder:

| Module | soft | hard | ap | defense | cost | reliability |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cwic_coaxial_mg` | 0.5 | - | - | - | 0.25 | - |
| `cwic_hull_mg` | 0.5 | - | - | 0.5 | 0.35 | - |
| `cwic_secondary_hmg` | 1 | 0.25 | - | - | 0.75 | - |
| `cwic_secondary_autocannon` | 2 | 1 | 2 | - | 1.5 | -0.025 |

**Two singletons:**

- `flamethrower` - soft 5, cost 0.5, reliability -0.05. Belongs in `Gun Modules` as its own type.
- `tank_gasoline_engine` - cost 1, fuel 2, speed +0.5, speed mult +0.15. Belongs with the engine
  families in `Total Balance Sheet Minimal`, which already has `Petrol_0..3` (1939/1950/1960/1970).
  Decide whether this is the pre-`Petrol_0` base engine or a duplicate that should be folded in.
  **It is also the only one of 246 modules missing `xp_cost`.**

### 5.3 Inconsistencies to resolve while writing the rows

1. **Reliability is expressed two different ways.** Guns use a negative *multiplier* (Schema A);
   turrets use a positive *flat add* (+0.05..+0.20). A turret making a tank more reliable is
   defensible for a fixed superstructure (simpler = more reliable), but the sign and the units
   should be a deliberate choice, not an accident.
2. **`cwic_hull_mg` gives `defense = 0.5` as a flat add** against chassis defense values of 4-6.
   That is a 10% swing from a machine gun. Check it against the hull rows before blessing it.
3. **The three coax/hull/HMG secondaries carry no reliability cost** while the autocannon carries
   -0.025. Either all four should, or none.
4. **Turret cost ordering has a gap**: `light_lp_turret` (1.25) costs more than `light_turret` (1.0)
   and `conventional_turret` (1.0), while `lp_turret` and `oscillating_turret` tie at 1.5.
5. **12 of 15 sub-units are `active = yes`** while the three flame ones are `active = no`. Both
   routes work because the root tech enables all 15, but the inconsistency will confuse the next
   reader.

### 5.4 Suggested order of work

1. Add a `Turrets & Superstructures` block to `Total Balance Sheet Minimal` using Schema B, seeded
   with 5.2's values, then reconcile 5.3 items 1 and 4.
2. Add the three AA cannons to `Gun Modules` as their own `Type`, Schema A.
3. Fill `Gun Modules > Ammo > Secondary` with the four `cwic_*` modules, resolving 5.3 items 2-3.
4. Place `flamethrower` in `Gun Modules`; decide `tank_gasoline_engine`'s home and give it `xp_cost`.
5. Re-run the CSV<->script comparator (section 7) - it should stay at zero mismatches, because you
   are documenting existing values, not changing them. **Any change to a value must be a conscious
   edit to both sides.**

---

## 6. Research cost weighting

Currently `research_cost = 2` on 168 of 169 armor techs; the root `nsb_iw_armored_vehicles` is 1.
No era or importance weighting exists. Open question 5 in the completion plan.

The mod already has a weighting convention elsewhere - these are real counts from
`common/technologies/`:

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

The established pattern, clearest in the MTG naval pair: **hull/chassis lines cost more than module
lines**, modules sit at 1.5-2, and cost rises with tier. The armor tree is the outlier in being flat.

A proposal that follows precedent rather than inventing a scale - to be argued, not applied blind:

- Chassis ladders (`nsb_light_tanks*`, `nsb_main_battle_tanks*`, `nsb_heavy_tanks*`): `2` early
  tiers rising to `3` post-1970, matching `armor.txt`'s legacy 2/3/4 spread.
- Module ladders in `NSB_armor_modules.txt`: `1.5` baseline, `2` from the 1960s, `2.5-3` for the
  late-tier exotics (DU ammo, NERA, hardkill APS, digital FCS), mirroring `MTG_navalmodule.txt`.
- Roots and enabling techs: `1`.
- Keep the total research investment for a full 1949-start armor path within ~10% of today's, so
  this reads as reshaping the curve rather than a global nerf. Compute before and after.

Whoever does this must also decide whether an XP economy should exist at all - 245 of 246 modules
carry `xp_cost`, almost all `= 1`, which is close to no economy.

---

## 7. Guardrails - things that have already bitten

- **`tools/validate_military_reworks.py` hardcodes magic numbers.** The SPAAG revert failed the
  self-test because 12/14/20 was baked in as a "corrected" contract. Any balance change needs a
  matching validator edit. Grep for the module name before assuming a value is free to change.
- **Never rewrite the workbook with openpyxl.** `Total Balance Sheet` holds 217 formulas; openpyxl
  writes formulas without their cached `<v>` values and the validator reads exactly those. The
  `Implementation Status` sheet was added by a surgical zip edit - copy every entry through, and
  append one entry each to `xl/workbook.xml`, `xl/_rels/workbook.xml.rels` and
  `[Content_Types].xml`. Verified afterwards: 15 original sheets byte-identical, formula counts
  unchanged, 0 cell diffs in the validator's range. **Re-stamp the SHA-256 in
  `Balance_Target_Manifest.md` after any workbook change** (currently `e4afa06e...`).
- **Localisation is ASCII-only and needs the BOM.** `.yml` files must keep the UTF-8 BOM; script
  files must never gain one. Only `§` colour codes and `£` texticon prefixes are legal non-ASCII.
- **`interface/texticons.gfx` is a full override.** Anything vanilla adds there in a patch is lost
  unless mirrored. Same trap applies to any other file the mod overrides wholesale.
- **Tech tree coordinates must be compared with year anchors resolved.** `y = @1955` and `y = 6` are
  the same cell; a raw string comparison misses those collisions and that is how 8 real overlaps got
  through the first time.
- **Do not "fix" coordinate collisions by moving techs to arbitrary free cells.** That is what
  produced the visual mess in `_local/screenshots/TankPictures/`. Keep each family in one column, move the minimum.
- `has_focus_tree` takes a tree `id`, not a filename. `fire_only_once` is global, not per country.
  `major = yes` on a `country_event` broadcasts to every country.

### Commands to run first

```bash
cd /home/zom/Projects/ColdWarIronCurtain
python3 tools/validate_military_reworks.py --tank-self-test
python3 tools/validate_military_reworks.py --tank-balance-report
git status --short
```

The CSV<->script comparator used throughout these passes is not committed as a tool; it walks the
CSV's `Module Loc Name` column (index 7), maps flat columns to `add_stats` and `, %` columns to
`multiply_stats`, and compares against the module and chassis files. It reported 1,424 cells with
zero mismatches. Rebuilding it takes about 20 lines and is worth doing before touching balance.

---

## 8. Definition of done

Tier 1 and Tier 2 are shipped and stable. "Finished" for Tier 3 means:

- [x] T3.1 resolved by measurement: no gridbox added, no year label added; both reported gaps were retracted with evidence. Runtime render check still outstanding.
- [o] T3.2 role group aligned to the x=461 company-icon rail; the overlay premise was retracted. Runtime re-check at 1920x1080 and 2560x1440, 1.0x/2.4x is still outstanding.
- [x] T3.3 static target reporting implemented with explicit 21-tank coverage; runtime calibration is tracked separately.
- [x] Actual missing module set reconciled: 22 IDs are present in the script and now have authoritative rows and comparator coverage; the manual's 23 count has no additional ID.
- [x] Research cost curve ratified and applied (section 6); XP policy closed as deliberately flat.
- [o] 3D entity gap remains documented art debt pending an explicit acceptance or asset mapping.
- [x] Over-long names shortened and the optics duplicate resolved; gasoline engine settled as the base engine with `xp_cost = 1`.

Permanently out of scope for this project, already marked `[TODO]` on the drawio pages so they are
not silently re-scoped: artillery and AA *designer* ladders, the mechanized APC/IFV ladder, the
night/thermal vision line, and the diagram's page-2 specials (RWS, dozer and mine ploughs, blow-out
panels, unmanned turret, underwater driving, external fuel, modular construction, NBC).
