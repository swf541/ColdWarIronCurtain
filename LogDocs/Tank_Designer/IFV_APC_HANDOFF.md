# IFV / APC implementation handoff

Date: 2026-09-06 (updated). This is the entry point for a new, blank-context session.
Branch: `tank-designer-and-doctrine-rework-test`.
Gameplay HEAD at the previous handoff: `80304e2030`.

## Status: APC family complete and validated in game. Next agent builds the IFV.

Date: 2026-09-07. Branch `tank-designer-and-doctrine-rework-test`. Gameplay HEAD at the
start of this work: `80304e2030`. **Everything is staged, nothing is committed.**

The APC designer family is done and confirmed working in a live NSB campaign: eight
designer hulls on the `mechanized_equipment` archetype covering the eight frozen Light
Mech rows, with modules, NSB-only technologies, unit supply, AI recipes, 1980 research
integration, English localisation, the designer GUI window and a validator contract.

Owner QA confirmed, in game:

- The Tank Designer opens for `apc_chassis_0` with the correct unarmed profile.
- **One design, not two.** The hull lists under both the infantry/land and armor
  production filters, and the design syncs across them - it is a single equipment shown
  twice, exactly as the two-value `type` predicts. This was the open question from the
  previous round and it is now closed.
- **Battalions draw it.** Mechanized battalions correctly consume designer APCs, and
  the equipment is labelled as an APC in the unit view. The shared-archetype decision -
  the core architectural bet of this batch - is validated end to end.
- `error.log` is clean for this work. No errors reference the new technologies, hulls,
  modules, sprites, designer GUI or localisation.

**The next agent's job is the IFV family.** Read "IFV batch: exact instructions for the
next agent" below; it is a step-by-step mirror of what is already proven here.

## Designer routing: three rounds of QA, resolved

### Round 1 - the designer did not open

The owner ran a 1949 NSB campaign as USA. Result:

- The `nsb_apc_hulls*` technologies render correctly in the NSB armour tree, are
  researchable, and their tooltips list the hull and module unlocks.
- `apc_chassis_0` ("Early Postwar APC Hull") appears in the production equipment
  list with sensible stats (defense 14.5, breakthrough 6.0, hardness 30%, armor 15,
  max speed 13.2 km/h, reliability 94%, fuel 2.10, cost 7.70).
- **But clicking it opened the legacy "Create Variant" upgrade popup** - the one with
  Armor / Engine `+`/`-` steppers - not the module designer. The owner checked every
  other APC/IFV entry point too; no module designer appeared anywhere.

So the assumption recorded in the previous version of this document - that an
archetype with `module_slots` and `type = mechanized` routes to the equipment
designer - was **wrong as written**, but the cause was not the equipment type.

### Attempt 1 (missing designer window) - tried, did not fix it

`interface/equipmentdesigner/_documentation.info` says the designer layout window is
resolved by searching, in order:

```
equipment_designer_<EQUIPMENT_TYPE>_<COUNTRY_TAG>
equipment_designer_<EQUIPMENT_ARCHETYPE>_<COUNTRY_TAG>
equipment_designer_<EQUIPMENT_TYPE>
equipment_designer_<EQUIPMENT_ARCHETYPE>
```

Every designable chassis in this mod has an `equipment_designer_<archetype>` window
under `interface/equipmentdesigner/tanks/`; `mechanized_equipment` had none. A new
`tank_chassis_apc.gui` was added to supply it.

**The owner re-tested and the upgrade popup still appeared.** So the missing window was
not the cause. The file is kept regardless: it is required for the designer to have a
layout once the designer does open, and every other family already ships one. Do not
read the presence of this file as evidence that the routing problem is solved.

### Attempt 2 (equipment domain) - this is what fixed it

The remaining discriminator is the equipment domain. Evidence:

- The binary exposes three module designers, `tank_designer_view`,
  `plane_designer_view` and `countryequipmentdesignerview` (ships), and three legacy
  upgrade views defined in `equipmentupgradedesignerwindow.gui`:
  `land_equipment_designer_view`, `air_equipment_designer_view` and
  `naval_equipment_designer_view`.
- The window the owner saw is the **land** upgrade view. The APC hulls were
  `type = mechanized`, i.e. generic land equipment, so that is the view they were
  classified into.
- `interface_category` is not the lever: vanilla `armored_car.txt` and legacy
  `tank_light.txt` use `interface_category_armor` and still get the upgrade window,
  because they have no module slots.
- Module slots are also not sufficient on their own - that is exactly what this batch
  demonstrated.

So `mechanized_equipment` and all eight `apc_chassis_*` hulls now declare
`type = { armor mechanized }`. `armor` is what should route them to
`tank_designer_view`; `mechanized` is retained so the archetype keeps its land and
transport classification for the AI and for every `transport = mechanized_equipment`
consumer. Multi-value `type` is an established pattern - `x_tank_chassis.txt` already
ships `type = { armor anti_air }` and `type = { armor artillery }` duplicates.

The type is restated on each hull as well as the archetype, so the routing holds
whether the engine reads the domain from the individual equipment or from its
archetype. The validator pins both.

`interface_category` was deliberately **not** changed. `mechanized_equipment` stays
`interface_category_land`, so legacy mechanized keeps its production-tab grouping. If
the upgrade popup still appears, moving the archetype to `interface_category_armor` is
the next and last lever, and it does move all legacy mechanized into the armor tab.

Known cost of this change: equipment `type` is what the AI uses by default to map
archetypes to strategies such as `unit_ratio`, so legacy mechanized now also counts as
armor for those strategies. The documented override is `ai_type`, but its documented
values are all air/naval and it was not used here rather than guess at a land value.
Watch AI armor-versus-mechanized production ratios in a long run.

Nothing else changed: the shared-archetype decision, sub-unit supply, technologies,
modules, hull stats, AI recipes and localisation are all as the owner's run validated
them.

### Round 3 - confirmed working

The owner re-ran the campaign and the **Tank Designer window now opens** for
`apc_chassis_0`. Observed and matching the intended design:

- Title bar reads "Tank Designer"; the design is named "Early Postwar APC MkO"; the
  hull label reads "Early Postwar APC Hull".
- Base/Combat/Misc stat panels read max speed 13.2 km/h, reliability 94.0%, hardness
  30.0%, armor 15.0, breakthrough 6.0, defense 14.5, soft attack 0.0, hard attack 0.0,
  piercing 0.0, fuel usage 2.10, production cost 7.70. These match the hull table plus
  the default recipe, and confirm the **unarmed** APC profile the frozen Light Mech
  rows call for (zero soft/hard attack and zero piercing).
- Hardness 30% is hull `0.5` plus the default `Half_track` suspension's `-0.2`, so
  module stacking on an APC hull behaves as designed.
- The Armor / Engine upgrade steppers now render **inside** the designer, which is the
  correct tank-chassis behavior, rather than as a standalone Create Variant popup.
- The XP cost (300) and Save controls are present.

So the equipment domain was the discriminator, and the routing question that blocked
this whole family is closed.

### Duplicate production listing - resolved, working as intended

The APC hull lists under both the infantry/land and the armor production filters. This
is the expected consequence of `type = { armor mechanized }`: the production filter row
matches on equipment type, so a two-type equipment matches two filters. Vanilla does the
same - `light_tank_aa_chassis` is `type = { armor anti_air }` and shows under both the
armor and anti-air filters.

**Owner QA confirmed it is one design, not a clone**: a design saved from one filter
appears with the same identity and stats under the other, and they stay in sync. There
is a single `apc_chassis_N` equipment definition under a single archetype, so this is
the expected behavior and no fix is needed. Do not "fix" it by dropping `mechanized`
from the type - that would strip the archetype's land and transport classification.

### Remaining cosmetic and polish gaps

Confirmed in game, none of them blocking:

- **Blueprint art is the light tank hull.** `tank_chassis_apc.gui` reuses
  `GFX_TC_light_tank_chassis` and the `GFX_TM_light_tank_chassis_*_slot` blueprints. An
  APC blueprint plus per-slot blueprint sprites are an art task.
- **The 3D preview panel is empty** ("Select Model" with no entries). Designer models
  come from a `tank_designer_model` list with no APC entry. Unit and map appearance are
  unaffected: those use the sub-unit entity lookup
  (`<TAG>_<sub_unit>_<level>_entity`), which this batch did not touch and which
  `zz_CWIC_armor_entity_aliases.asset` still owns.
- **The role dropdown read "Unknown".** Role labels come from
  `tank_designer_<archetype>` / `tank_designer_<extra type>` keys in
  `localisation/english/designer_l_english.yml` (see `tank_designer_light_tank_chassis`
  and `tank_designer_anti_air` for the two shapes). Both
  `tank_designer_mechanized_equipment` and `tank_designer_mechanized` have now been
  added as "Armored Personnel Carrier", with their `_role_disallowed` companions.
  **Which of the two keys the engine actually reads is unverified** - check the label in
  the next run and delete the unused pair.
- The APC hulls are still in no `search_filters` group. The mod ships no
  `tank_filters.txt`, so adding one would override vanilla's; a separate file in
  `common/units/equipment/` holding only a `search_filters` block is the low-risk route
  if this is ever wanted.

### Fixed in this round

- **Technology tree years were wrong.** The APC column shipped on raw folder rows
  (`y = 6, 9, 12, ...`) copied from the mechanized line in `armor.txt`, which uses a
  different scale from the `@year` macros every other NSB armour column uses. The tree
  drew "1947 APC" on the 1955 row. All eight hull technologies now sit on the `@year`
  row matching their `start_year`, and a new `@1947 = 3` macro was added for the tier-0
  row. The validator now pins `start_year` to the tree row for every APC technology.
- **Eight `equipment_database.cpp:656` log lines** - `apc_chassis_0..7` were missing
  from `script_enum_equipment_bonus_type`. Added to `common/script_enums.txt`, next to
  the `mechanized_equipment_*` block, and pinned by the validator.

### Pre-existing bug found while reading error.log - not touched

`common/national_focus/PHI_1950s.txt:587` does
`add_equipment_to_stockpile = { type = apc_equipment_1 ... producer = CAP }`.
`apc_equipment_1` is not an equipment id anywhere in the repo, so the focus silently
awards nothing and the log records
`invalid database object for effect/trigger: ... apc_equipment_1`. This predates the APC
work and is **not** fixed by it: `apc_equipment_1` now exists only as the
`derived_variant_name` of `apc_chassis_1`, which is a variant-name localisation key, not
an equipment type. The focus most likely wants `mechanized_equipment_3`, or a designer
APC once national presets exist. Out of scope here; flagged for whoever owns PHI.

### Exact changes

| File | Change |
| --- | --- |
| `common/units/equipment/mechanized.txt` | `mechanized_equipment` archetype moves to `type = { armor mechanized }` and gains the 15-position APC designer layout (5 mandatory + `tank_special_slot_1..10` with the same categories as the tank hulls), eleven `module_count_limit` blocks and `default_modules`. Appends `apc_chassis_0..7`. |
| `common/units/equipment/modules/00_tank_modules.txt` | Seven new modules in two APC-only categories: `tank_apc_superstructure` (`apc_open_troop_bay`, `apc_troop_compartment`, `apc_frontal_engine_layout`) and `tank_apc_armament` (`apc_firing_ports`, `apc_pintle_mg`, `apc_cupola_hmg`, `apc_remote_weapon_station`). |
| `common/technologies/NSB_armor.txt` | New `nsb_apc_hulls0..7` column at `nsb_armor_folder` `x = -6`, chained by `path`, entered from `nsb_iw_armored_vehicles`, with `allow = { has_tech = mechanized_infantry }` on tier 0. Unlocks the hulls and the seven modules. |
| `common/scripted_effects/CWIC_tank_bookmark_research.txt` | 1980 major-producer NSB grant adds `nsb_apc_hulls0..4` (every APC tech with `start_year <= 1980`). |
| `common/ai_equipment/generic_tank.txt` | New `cwic_generic_apc` group, `roles = { land_apc }`, one historical recipe per hull gated on its own technology. |
| `interface/cwic_tank_rework_icons.gfx` | `GFX_SMI_*` for the seven modules (reusing existing APC art) and `GFX_nsb_apc_hulls0..7[_medium]` (reusing `apc_3..10.dds`). |
| `localisation/english/tank_modules_l_english.yml` | Hull, derived-variant and module names/descriptions. ASCII only. |
| `localisation/english/nsb_armor_l_english.yml` | The eight technology names/descriptions. ASCII only. |
| `interface/equipmentdesigner/tanks/tank_chassis_apc.gui` | **New.** `equipment_designer_mechanized_equipment` window, fifteen slot containers, reusing light-tank sprites. Needed for the designer layout; on its own it did not fix the routing. |
| `common/script_enums.txt` | `apc_chassis_0..7` added to `script_enum_equipment_bonus_type`. |
| `localisation/english/designer_l_english.yml` | `tank_designer_mechanized_equipment` and `tank_designer_mechanized` role labels. |
| `CWIC Backup/tools/validate_military_reworks.py` | New APC contract plus negative fixtures (see below). |

### Hull table

Hulls are authored approximations. Hull plus the baseline recipe
(`apc_open_troop_bay`, `apc_firing_ports`, `Half_track`, `Armor_0_W`,
`tank_gasoline_engine`) is *intended* to land near the legacy row; `armor_value` is
the only stat pinned equal to the frozen row and enforced by the validator.

| Hull | Year | Replaces | Tech | speed / def / bt / armor / IC |
| --- | --- | --- | --- | --- |
| `apc_chassis_0` | 1947 | `mechanized_equipment_3` | `nsb_apc_hulls0` | 11 / 11 / 3 / 15 / 5.6 |
| `apc_chassis_1` | 1950 | `mechanized_equipment_4` | `nsb_apc_hulls1` | 11.5 / 14 / 4 / 18 / 6.6 |
| `apc_chassis_2` | 1960 | `mechanized_equipment_5` | `nsb_apc_hulls2` | 12.5 / 14 / 4 / 22 / 7.6 |
| `apc_chassis_3` | 1965 | `mechanized_equipment_6` | `nsb_apc_hulls3` | 13.5 / 16 / 5 / 24 / 8.6 |
| `apc_chassis_4` | 1975 | `mechanized_equipment_7` | `nsb_apc_hulls4` | 15 / 16 / 5 / 28 / 10.6 |
| `apc_chassis_5` | 1985 | `mechanized_equipment_8` | `nsb_apc_hulls5` | 16 / 16 / 5 / 32 / 11.6 |
| `apc_chassis_6` | 1995 | `mechanized_equipment_9` | `nsb_apc_hulls6` | 17 / 19 / 6 / 36 / 12.6 |
| `apc_chassis_7` | 2005 | `mechanized_equipment_10` | `nsb_apc_hulls7` | 18.5 / 19 / 6 / 40 / 14.6 |

`hardness = 0.5` and `reliability = 1` on every hull; half-track suspension takes
hardness to 0.3 and reliability to 0.9, tracked suspensions keep 0.5 / 1.0.

### Full 18-envelope mapping (only the first block is implemented)

| Frozen rows | Legacy equipment | Archetype it must supply | Designer family | State |
| --- | --- | --- | --- | --- |
| Light Mech I-VIII / APC | `mechanized_equipment_3..10` | `mechanized_equipment` | `apc_chassis_0..7`, light-hull generation | **done** |
| Heavy Mech I-VIII / IFV | `mechanized_heavy_equipment_1..8` | `mechanized_heavy_equipment` | `ifv_chassis_0..7`, light-hull generation, armed | not started |
| WWII Mech 1-2 | `mechanized_equipment_1..2` | `mechanized_equipment` | intentionally legacy-only; pre-designer era | not planned |
| Marine mech | `mechanized_marine_equipment` | `mechanized_marine_equipment` | amphibious mobility module on eligible designs | not started |
| Heavy APC / heavy IFV (medium hull) | no legacy row | tbd | medium-hull generation of the two families above | not started |

The IFV batch is the direct mirror of this one: `mechanized_heavy_equipment` gains the
same 15-position layout, a `tank_apc_armament`-plus-autocannon/ATGM armament set, and
`ifv_chassis_0..7` pinned to the `mechanized_heavy_equipment_1..8` rows. It is the
armed line, so its AI recipes **do** need the ammunition contract that APC recipes are
explicitly exempted from.

### Validation actually performed

```bash
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-self-test
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-balance-report --tank-module-balance-report --tank-envelope-report
python3 "CWIC Backup/tools/loc_audit_1.py" --check
git diff --check
```

All pass. The validator now reports 1295 technologies, 253 tank modules, 125 historical
tank designs, 30 generic bookmark variants, 14 national presets, 460 named OOB requests
across 68 NSB OOBs, 76 country-history bootstrap sites, **8 APC designer hulls** and 15
designer slots. Workbook SHA-256 re-verified unchanged
(`dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`).

New validator contract (`validate_apc_designer_family`), all of it enforced on every run:

- Archetype exposes ten specialized slots with the shared category layout, both
  mandatory weapon positions restricted to APC-only categories and still `required`.
- `default_modules` fills all five mandatory slots with APC-legal modules; one
  secondary-turret count limit is retained.
- **`mechanized_equipment_1..10` contain no `module_slots`** - the non-NSB invariant.
- Per hull: archetype, `module_slots = inherit`, `derived_variant_name`, year, DLC gate,
  parent chain, `armor_value` equal to the frozen row, unlocked by an NSB technology,
  and that technology absent from `armor.txt` (no legacy-folder leak).
- Modules exist, carry the right category, and do not multiply gun stats.
- Archetype and every hull declare exactly the `armor` plus `mechanized` domain.
- Every hull technology's `start_year` matches its `@year` tree row.
- Every hull id is present in `script_enum_equipment_bonus_type`.
- One AI recipe per hull, using the APC categories, gated on its own technology.
- Localisation keys present for every hull, derived variant, module and technology.
- `validate_designer_window_coverage`: every `module_slots = inherit` equipment and
  every `duplicate_archetypes` role resolves an `equipment_designer_*` window.

Six negative fixtures run under `--tank-self-test` (they write a mutation to
`mechanized.txt`, assert rejection, and restore the file byte-identically): legacy row
inherits slots; a tank gun category is allowed on an APC; a hull leaves the mechanized
archetype; a hull loses its DLC gate; the archetype leaves the armor domain; and the APC designer window is removed.

The module balance report now excludes the seven APC modules from frozen-workbook
coverage and names them as an explicit exemption. The 2023 workbook predates this family
and cannot carry those rows; the alternative was silently widening its coverage.

### Limitations - do not overstate this batch

- **Runtime QA now covers the designer, the design identity and unit supply.** Owner
  runs confirmed the technologies, the hull and its stats in production, the Tank
  Designer opening with the correct unarmed profile, one shared design across both
  production filters, mechanized battalions drawing designer APCs with the correct APC
  label, and a clean `error.log`. **Still not tested:** save/reload of a saved design,
  long-run AI production behavior with mechanized now also in the `armor` domain, the
  1980 bookmark path, and non-NSB regression.
- Legacy mechanized equipment is now also `armor` domain for AI strategy purposes. This
  is a deliberate, documented cost of the routing fix and has not been observed over a
  long AI run.
- Legacy mechanized equipment is now also `armor` domain for AI strategy purposes. This
  is a deliberate, documented cost of the routing fix, not a tested-neutral change.
- The designer's 3D preview may be blank for APC hulls. Unit models come from the
  sub-unit entity lookup (`<TAG>_<sub_unit>_<level>_entity`), which is unchanged, so
  in-game and map appearance are unaffected. `zz_CWIC_armor_entity_aliases.asset` was
  not touched.
- The APC hulls are still in no `search_filters` group. A mod-side file adding one was
  deliberately skipped while the routing is unresolved.
- The owner's screenshots show `2800 errors` in the corner. That counter was not
  attributed to these changes and no error.log was captured or read for them.
- Hull stats are authored approximations, not calibrated balance. The estimator
  calibration gap from the previous handoff is still open, so no static estimate here
  proves live balance.
- **No bookmark preset designs and no OOB migration.** `CWIC_tank_designer_effects.txt`
  is untouched: the validator requires the bookmark variant set to equal the set of
  chassis types referenced by NSB OOBs, so adding APC presets requires migrating OOB
  mechanized requests in the same change. Bookmark integration in this batch is the 1980
  research grant only; at 1980 USA/SOV unlock `apc_chassis_0..4` and the generic AI
  recipes design a carrier at runtime.
- No national historical APC presets. The coverage baseline already exists as
  `TAG_mechanized_equipment_3..10` localisation across roughly 40 country equipment
  files; that is the inventory the sweep should be driven from.
- APC hulls are in no `search_filters` group (the mod ships no `tank_filters.txt`), so
  they are ungrouped in the designer chassis list.
- `visual_level` 2-9 is shared with the legacy mechanized rows; no new entity aliases
  were added and `zz_CWIC_armor_entity_aliases.asset` is untouched.

## IFV batch: exact instructions for the next agent

The IFV family is a direct mirror of the APC family. Every architectural question it
raises has already been answered and validated in game by the APC batch. Follow the
APC implementation as the reference; the diff for it is staged and readable.

### Ground truth for the IFV

| | |
| --- | --- |
| Frozen rows | Heavy Mech I-VIII = `mechanized_heavy_equipment_1..8` |
| Archetype that must supply units | `mechanized_heavy_equipment` |
| File | `common/units/equipment/mechanized_heavy.txt` |
| Current archetype state | `type = mechanized`, `interface_category_land`, no module slots |
| Consumers | `common/units/CWIC-Infantry.txt` (`mechanized_heavy_equipment = 50`), `common/units/CWIC-Special-Units.txt` |
| Legacy technologies | `mechanized_heavy_infantry`..`8` in `common/technologies/armor.txt`, NSB folder column `x = 3` |
| Equipment years | 1947, 1950, **1955**, 1965, 1975, 1985, 1995, 2005 |
| Legacy tech start years | 1947, 1950, **1960**, 1965, 1975, 1985, 1995, 2005 |

Note the tier-2 mismatch. The accepted design choice is that
`mechanized_heavy_equipment_3` stays at **1955**; the workbook's 1960 is a deliberate
year exception and neither the stats nor the workbook may be changed. Give the new
`nsb_ifv_hulls2` technology `start_year = 1955` and the `@1955` tree row so the tree,
the tooltip and the hull all agree, and write that down.

Unlike the APC line, **Heavy Mech is armed**: it has real soft/hard attack and
piercing. Do not copy the APC's zero-attack profile.

### The seven things that make this work

1. **Put the designer hulls on the existing `mechanized_heavy_equipment` archetype.**
   Sub-unit `need` resolves an archetype name and multiple entries are AND, not OR, so a
   separate archetype would produce equipment no battalion can consume. Sharing the
   archetype means zero sub-unit edits. This is proven: mechanized battalions draw
   designer APCs correctly.
2. **`type = { armor mechanized }` on the archetype and restated on every hull.** This
   is what routes the equipment to `tank_designer_view` instead of the legacy
   `land_equipment_designer_view` Create Variant popup. Nothing else does it - not
   module slots, not `interface_category`, not a designer GUI window. Leave
   `interface_category = interface_category_land` alone.
3. **Leave the legacy rows without `module_slots`.** `mechanized_heavy_equipment_1..8`
   must never gain slots or `module_slots = inherit`; that invariant is what keeps
   non-NSB games untouched, and the validator enforces the APC equivalent.
4. **Add a designer GUI window.** New
   `interface/equipmentdesigner/tanks/tank_chassis_ifv.gui` defining
   `equipment_designer_mechanized_heavy_equipment` with a `module_slots` container for
   all fifteen positions. Copy `tank_chassis_apc.gui`. Without it the designer has no
   layout. Reuse existing sprites; there is already
   `gfx/interface/equipmentdesigner/tanks/Modules/Other Modules/IFV fighting compartment.png`
   and a full `ATGM/IFV ATGM 1955..2015` set that this batch deliberately left for you.
5. **NSB-only technologies.** New `nsb_ifv_hulls0..7` column in
   `common/technologies/NSB_armor.txt`, entered by a `path` from
   `nsb_iw_armored_vehicles`, `allow = { has_tech = mechanized_heavy_infantry }` on tier
   0, and each folder position on the `@year` macro matching its `start_year`. Use a
   free column; the APC took `x = -6`, mechanized is `x = 0`, heavy mech `x = 3`,
   amphibious `x = -3`. Unlock the new modules from these technologies, not from
   `armor.txt` - the validator only scans `NSB_armor.txt` and `NSB_armor_modules.txt`
   for module unlocks and will report anything else as an unreachable module.
6. **Add every hull id to `common/script_enums.txt`** under
   `script_enum_equipment_bonus_type`, or the game logs one
   `equipment_database.cpp:656` line per hull.
7. **Add the role label** to `localisation/english/designer_l_english.yml` as
   `tank_designer_mechanized_heavy_equipment`, following the APC entries.

### Also required, same as the APC batch

- Modules in `common/units/equipment/modules/00_tank_modules.txt` in IFV-only categories
  so a personnel carrier cannot mount a tank gun and an IFV cannot mount a tank turret.
  Register `GFX_SMI_<module>` icons in `interface/cwic_tank_rework_icons.gfx`.
- One generic historical AI recipe per hull in `common/ai_equipment/generic_tank.txt`,
  gated on its own technology, in a new group with its own `roles = { }` value.
- Every APC technology with `start_year <= 1980` was added to the 1980 major-producer
  grant in `common/scripted_effects/CWIC_tank_bookmark_research.txt`; the validator
  fails if that coverage is incomplete, so do the same for the IFV.
- English localisation for hulls, derived variant names, modules and technologies.
  ASCII only. Do not touch `localisation/french/` or `localisation/japanese/`.

### The ammunition contract - read this before writing AI recipes

The validator requires every AI recipe to include attack-producing AP and HE ammunition
modules, and the APC family is explicitly exempted because its armament modules use
`add_stats` only. The rule is driven by `needs_ammunition()`, which tests whether a
module **multiplies** `soft_attack`/`hard_attack`/`ap_attack`. So:

- If IFV armament modules multiply attack stats (the conventional gun pattern), the IFV
  recipes **must** carry ammunition modules and must not be exempted.
- If they add flat stats like the APC modules do, extend the exemption instead.

Decide deliberately and record which you chose. Also note
`tank_module_balance_report()` excludes the seven APC modules from the frozen workbook by
name; new IFV modules need the same treatment, since the 2023 workbook predates both
families and **must stay byte-identical**
(SHA-256 `dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`).

### Validator work

`CWIC Backup/tools/validate_military_reworks.py` is the maintained validator and is the
one `CWIC Backup/` file you may edit. Mirror `validate_apc_designer_family()` as
`validate_ifv_designer_family()` and register it next to the existing call. It should
pin, per hull: archetype, `module_slots = inherit`, `derived_variant_name`, year, DLC
gate, parent chain, the `armor` plus `mechanized` domain, the frozen-row stat match,
technology unlock, absence from the legacy armour folder, `start_year` versus tree row,
and script-enum presence. Also mirror `run_apc_negative_fixtures()`; those fixtures
write a mutation to the source file, assert rejection and restore it byte-identically,
so keep the `try/finally` and the `encoding="utf-8", newline=""` write.

`validate_designer_window_coverage()` already fails when any `module_slots = inherit`
equipment has no `equipment_designer_*` window, so it will catch a missing
`tank_chassis_ifv.gui` for free.

### Commands to run

```bash
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-self-test
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-balance-report --tank-module-balance-report --tank-envelope-report
python3 "CWIC Backup/tools/loc_audit_1.py" --check
git diff --check
```

Run the first one as a baseline before editing. The current expected pass line is:
1295 technologies, 253 tank modules, 125 historical tank designs, 30 generic bookmark
variants, 14 national presets, 460 named OOB requests across 68 NSB OOBs, 76
country-history bootstrap sites, 8 APC designer hulls, 15 designer slots.

The owner's error log is at
`~/.local/share/Paradox Interactive/Hearts of Iron IV/logs/error.log`. It is currently
clean for APC content; grep it for your new ids after a run.

### Deliberately left out of scope - do not start these without asking

- **Bookmark preset designs and the NSB OOB migration.**
  `CWIC_tank_designer_effects.txt` is untouched by the APC batch. The validator requires
  the bookmark variant set to equal the set of chassis types referenced by NSB OOBs, so
  presets and OOB migration have to land in one change. Do APC and IFV together,
  preserving newest-only production visibility and producer-aware named requests.
- **National historical presets.** The coverage baseline already exists as
  `TAG_mechanized_equipment_3..10` localisation across roughly 40 country equipment
  files; drive the sweep from that inventory rather than inventing mappings.
- Heavy APC / heavy IFV on medium hulls, amphibious conversion, artillery/AA, and
  night/thermal vision. Amphibious in particular must not remove the NSB legacy
  amphibious unlocks until replacement vehicles actually supply the marine sub-units.
- Art: APC/IFV blueprints, per-slot blueprint sprites and designer 3D models.

### Working rules that bit this batch

- Do not stage or modify unrelated files. `.gitignore` and `interface/popupwindow.gui`
  carry other people's uncommitted work; leave them alone.
- Localisation `.yml` files need a UTF-8 BOM; script and GUI files must not gain one.
  Verify bytes, not text, across the whole changeset.
- Do not claim live testing you did not perform, and do not treat a passing validator or
  a static estimate as balance acceptance. The full-design estimator calibration gap is
  still open.

## Owner direction and stopping point

Historical note, superseded by the status section above: the documentation-only
session that first wrote this file stopped before any APC/IFV implementation. The
owner confirmed the previous QA issues were already fixed. Do not reopen the stale
issue list at the end of `ContextUpdate-9-6-26-1819` as though it describes current
defects.

The owner has now updated bookmark creation to keep only the newest designs
visible in the production tab. Preserve that behavior during all future work.

Historical national medium tanks are implemented for USA/SOV only. A large
historical coverage sweep remains necessary for **all armor vehicle families**:
light, medium, heavy, APC, IFV and other armored roles, across all countries,
or at minimum countries with corresponding non-NSB vehicles already implemented.
This is an explicit remaining requirement, not optional cosmetic polish and not
something the current 14 national presets have completed.

## Read order and authority

1. This handoff: current status and next implementation course.
2. `National_Tank_Presets.md` and `National_Tank_Preset_Manifest.json`: exact
   first-batch mappings, loadouts and limitations. Production-tab behavior is
   superseded by the newer commit described below.
3. `Deferred_Design_Decisions.md`: accepted Section 8 choices. Its statements
   that national presets are entirely missing are historical and superseded.
4. `Balance_Sources.md` and `Balance_Target_Manifest.md`: source interpretation
   and frozen tank/mechanized envelopes.
5. `HANDOFF_Deferred_Scope.md`: detailed APC/IFV, artillery/AA, amphibious and
   specials reference. Its clean-tree, old tool paths, counts and undecided
   Section 8 language are historical; use current files and accepted choices.
6. `Deferred_Scope_Progress.md`, `Artillery_AA_Target_Manifest.md`, and
   `HANDOFF_Tier3.md` as needed for prior implementation and later scope.

Some source notes are untracked/device-local, including HANDOFF_Deferred_Scope,
TankQANotes, ContextUpdate and screenshots. Do not assume they accompany a clone
on another device. This document carries forward the essential accepted choices.

## Recent changes that must survive

| Commit | Change |
| --- | --- |
| `a997a48e0e` | Tools moved under `CWIC Backup/tools/`; old root `tools/` paths are stale. |
| `368fa4815c` | All ten tank special slots renamed to `tank_special_slot_1` through `_10`, avoiding plane localisation collisions. |
| `b2cd5694b9` | New `zz_CWIC_armor_entity_aliases.asset` replaces the old level-0-only file. |
| `88c94a5b1c` | Fourteen USA/SOV national medium presets, producer-aware OOB names, duplicate guards, module estimator correction and tests. |
| `80304e2030` | Newest bookmark design only in the default production tab. |

The entity alias file contains 3,019 aliases. Keep its `zz_` load order, flame
clones and deliberate exclusions (GER light/heavy, ITA heavy, JAP light).
Do not resurrect `zz_CWIC_armor_level0_entities.asset`.

### Production-tab update

`80304e2030` adds `mark_older_equipment_obsolete = yes` to all 44 creation
blocks in `CWIC_tank_designer_effects.txt` and `CWIC_national_tank_presets.txt`.
Creation order is important: families are contiguous and tiers ascend, so the
newest eligible design is created last. The national helper runs first; generic
medium creation excludes USA/SOV. Preserve ascending order and verify that new
APC/IFV roles do not incorrectly obsolete a different role in the same family.

Older designs must remain resolvable for starting units, stockpiles and named
requests; obsolescence is not deletion. Export presets were already created
with `obsolete = yes` in `CWIC_tank_focus_effects.txt` and were not the cause of
bookmark spam. Existing saves are not migrated. The owner reports this update
as fixed; this handoff session checked the code and static validator, not live UI.

### National presets already implemented

| Medium chassis tier | USA | SOV |
| --- | --- | --- |
| 0 | M4 Sherman | T-34-85 |
| 1 | M26 Pershing | T-44 |
| 2 | M46 Patton | T-54 |
| 3 | M47 Patton | T-55 |
| 4 | M48 Patton | T-62 |
| 5 | M60 Patton | T-64A |
| 6 | M1 Abrams | T-72 |

Names follow existing country equipment localisation. Existing chassis-tier
assignments were retained; their technology years are not necessarily vehicle
introduction dates. Recipes are authored approximations, not certified exact
historical configurations or frozen-envelope matches.

`cwic_create_starting_tank_variants` calls the national helper before generic
creation. Producer-local per-chassis flags prevent repeat creation. The 1980
major-producer research helper refreshes newly unlocked NSB designs. All 15
national slots are explicit, with unused special slots empty and engine/armor
upgrades zero. Generic AI's 125 historical recipes remain unchanged.

OOB names resolve by actual owner/producer/creator, including imports in Canada,
Italy, Mongolia and China. Never rename all requests according to the country
whose OOB file is being loaded. Quantities and chassis IDs were preserved.

## Accepted design choices - do not ask again

- Build APC/IFV designer roles on existing light/medium hull families. Preserve
  non-NSB legacy equipment support.
- Keep `mechanized_heavy_equipment_3` at **1955**. The workbook's 1960 is a
  deliberate year exception, not permission to alter the stats or workbook.
- Gate legacy and designer artillery/AA paths by DLC, preserving technology
  activation of sub-units. Artillery/AA source targets are already frozen.
- Amphibious capability belongs in a mobility module on eligible mechanized
  designs. Do not remove NSB legacy amphibious unlocks until replacement
  vehicles actually supply the marine sub-units correctly.
- Invent night/thermal vision balance values and document them as authored
  decisions. They are not supplied numeric targets.
- Keep the 15-position designer: five mandatory slots plus ten specialized
  special slots. No further layout expansion is approved or needed by default.
- Workbook is frozen; CSV is the living balance mirror with reviewed overrides.
  Owner permits practical design judgment within this scope.

Special slots, all named `tank_special_slot_N`: 1-2 ammunition; 3 aiming;
4 optics; 5 computer/radar; 6 loading system; 7 passive/reactive protection;
8 passive/reactive/active protection; 9 survivability/mobility/smoke;
10 secondary weapon/survivability/mobility/smoke. Do not introduce the obsolete
`special_type_slot_N` names in tank content.

## APC / IFV ground truth

The legacy mechanized balance is already implemented; the missing work is
designer conversion and its integration, not inventing 18 new target envelopes.

| Frozen rows | Legacy equipment |
| --- | --- |
| WWII Mech 1-2 | `mechanized_equipment_1..2` |
| Light Mech I-VIII / APC | `mechanized_equipment_3..10` |
| Heavy Mech I-VIII / IFV | `mechanized_heavy_equipment_1..8` |

The prior audit compared 216 cells across 18 rows with only the accepted year
exception. Resolve archetype inheritance when checking legacy values. Light
Mech has zero soft/hard attack and piercing; Heavy Mech is the armed IFV line.
Do not equate the legacy name "Heavy Mech" automatically with heavy tank hulls.

Source role matrix: light hull supports APC and IFV; medium hull supports heavy
APC and heavy IFV. Source role penalties give APC -0.4 armor/hardness and IFV
-0.2; exact implementation and stacking must be checked against game semantics.
Use the Roles tab, Total Balance Sheet Object 842, diagram page 10 progression,
and page 9 per-nation light-chassis vehicles/availability as design references.

Relevant paths under `Cold War Iron Curtain/`:

- `common/units/equipment/mechanized.txt`, `mechanized_heavy.txt`,
  `mechanized_marine.txt`: legacy equipment and inheritance.
- `common/units/CWIC-Infantry.txt`: mechanized/marine supply consumers.
- `common/units/equipment/tank_chassis.txt` and
  `common/units/equipment/modules/00_tank_modules.txt`: designer hulls/modules.
- `common/technologies/NSB_armor.txt`, `NSB_armor_modules.txt`, and the legacy
  armor/support technologies: unlocks, DLC routing and sub-unit activation.
- `common/ai_equipment/generic_tank.txt`: AI recipe patterns.
- `common/scripted_effects/CWIC_tank_designer_effects.txt`,
  `CWIC_national_tank_presets.txt`, `CWIC_tank_bookmark_research.txt` and
  `CWIC_tank_focus_effects.txt`: setup and exports.
- `history/countries/`, `history/units/*_nsb.txt`, designer GUIs under
  `interface/`, and `localisation/english/`: integration surfaces.

## Recommended next implementation course

1. Read current git status/history and the sources above. Preserve unrelated
   work. Run the validator baseline before edits.
2. Address the remaining estimator calibration gap before treating static
   mechanized estimates as acceptance evidence. Module parents no longer stack
   predecessor stats: Radar II fuel 1.2 and GL ATGM III hard attack 95 are tested.
   Full-design engine ordering, caps, role bonuses, inherited chassis defaults,
   technology/MIO effects and agreed tolerances are still not calibrated.
3. Create an explicit APC/IFV mapping from all 18 envelopes to hull generations,
   roles, technologies and supply consumers. Define how unarmed APC and armed
   IFV designs satisfy mandatory weapon/turret slots without accidental tank
   stats. Avoid designing only equipment names with no usable sub-unit supply.
4. Implement a coherent role/hull slice with modules, technology/DLC gates,
   sub-units, AI recipes, GUI routing, English localisation, bookmark setup and
   validator fixtures together. Keep non-NSB functional throughout.
5. Expand the historical coverage manifest by country and vehicle family.
   Inventory existing non-NSB names, variants, research and OOBs first; use them
   as the minimum coverage baseline. Record missing/ambiguous mappings instead
   of assuming current generic or USA/SOV medium coverage is sufficient.
6. Migrate named references and producer bootstrap together for each completed
   family, including foreign-owned vehicles, stockpiles, production, forced
   variants and relevant exports. Preserve counts and newest-only production
   visibility. Add regression checks for creation order/obsolescence as coverage
   expands; the current validator passing alone does not certify that behavior.
7. Validate fresh 1949/1980 NSB and non-NSB starts, usable mechanized divisions,
   design stats, AI choices, imports/exports, production list and save/reload.
   Commit bounded green batches. Artillery/AA and vision remain later batches;
   amphibious conversion requires marine supply acceptance in the same slice.

## Validation and working rules

Baseline rerun at `80304e2030` during this handoff: validator plus tank self-tests
passed with 1,287 technologies, 246 modules, 125 historical AI designs, 30 generic
bookmark variants, 14 national presets, 460 named requests across 68 NSB OOBs,
76 country-history bootstrap sites and 15 slots. Doctrine is intentionally parked.
The prior implementation's envelope report parsed 49 recipes but sampled only
11 of 21 tank targets. Static success is not full-design balance acceptance.

```bash
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-self-test
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-balance-report --tank-module-balance-report --tank-envelope-report
python3 "CWIC Backup/tools/loc_audit_1.py" --check
git diff --check
```

The localisation audit covers 22 SEA files, not all tank localisation. English
localisation must remain ASCII; leave French/Japanese to translation owners.
Use fresh campaigns; old saves are not migrated. Existing root QA logs are not
evidence for new changes. Do not claim live testing unless actually performed.

Keep `2023 - CWIC Tank Rework Balance.xlsx` byte-identical, SHA-256
`dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`.
Do not edit/stage/delete unrelated `CWIC Backup/` files (maintained validator
excepted), root handoffs/logs, doctrine documents, screenshots or lock files.
The relocated artillery/AA checker has a previously noted root-path issue;
do not mistake that tooling issue for target drift or silently edit backup tools.

The APC session left the unrelated untracked user documents, screenshots, logs and
the tool-managed `.gitignore` edit untouched and unstaged.
