# Tank Designer Rework and Content Audit

Date: 2026-09-03

Branch/commit inspected: `development-branch` / `4a999ae3f3`

Game reference: local Hearts of Iron IV 1.19.2 installation

Scope: tank designer UI, chassis and role definitions, NSB and legacy research paths, marine mechanized content, affected support companies, AI designs, bookmark OOB integration, graphics references, and supplied runtime logs.

## Executive diagnosis

The reports are correct. The tank designer is not merely short on polish; several integration layers were never completed.

The module and technology content itself is substantial: the rework defines 287 tank modules, 239 of which are connected to NSB technology unlocks, and 169 NSB armor/module technologies with complete English names and descriptions. The unfinished part is the wiring between those systems and the rest of the game. The main release blockers are:

1. The chassis declare 15 module slots, but the active tank designer view only provides nine slot positions. Six declared special slots therefore have no outer UI position.
2. No AI or historical module-equipped tank designs exist. The mod replaces vanilla `common/ai_equipment`, provides only four naval AI files, and has no tank design file. NSB OOBs refer to raw chassis or nonexistent role variants. All three supplied logs reproduce missing tank-variant errors.
3. The marine mechanized equipment line exists, but its five enabling technologies are present only in the non-NSB armor folder. With NSB active, those technologies are hidden. A visible amphibious-warfare technology also depends on the hidden first tech, blocking the later amphibious-warfare branch.
4. The complete seven-tech armored-engineer chain depends on legacy MBT technologies that are hidden with NSB. This affects both armored and mechanized engineer support companies.
5. `light_tank_artillery_chassis` incorrectly duplicates `medium_tank_chassis`, so light SP artillery inherits the medium chassis family.

The architecture is currently a mixed legacy/NSB stack. That can work, but every shared consumer must use a DLC-neutral prerequisite or have explicit DLC-specific wiring. The rework updates many equipment needs to chassis types while leaving technology prerequisites, AI designs, historical variants, designer layout, amphibious content, technology categories, and graphics mappings partly on the old model.

## Priority summary

| Priority | Work item | Why it is here |
| --- | --- | --- |
| P0 | Add all 15 tank designer slot positions and redesign the panel around them | Six declared slots are inaccessible through the inherited UI. This blocks the central feature. |
| P0 | Add generic AI tank designs and valid historical/bookmark variants; repair all NSB OOB references | The AI has no tank-design recipes, raw OOB chassis are not proper armed designs, and role variants fail at runtime. |
| P0 | Make marine mechanized research and the armored-engineer chain DLC-safe | Both are player-facing progression blockers with NSB enabled. |
| P0 | Change `light_tank_artillery_chassis` back to `archetype = light_tank_chassis` | Small fix with broad correctness impact on every light SPG tier and design. |
| P1 | Decide and finish or remove amphibious, rocket, modern, super-heavy, and heavy-artillery designer roles | These roles have orphan definitions/references or no consuming unit. |
| P1 | Correct NSB technology categories and AI research timing | Almost every NSB tank tech is classified as APC research, so armor bonuses do not apply correctly and AI dates are copied from 1944. |
| P1 | Reconcile equipment graphics/entities with the final role list | Current logs contain extensive missing or obsolete tank equipment/entity references. |
| P2 | Remove or finish the dead first-generation module set, add five missing module icons, and remove dangling tech paths | These are strong maintenance and presentation problems but follow the functional blockers. |
| P2 | Add automated DLC-on/off and design/OOB validation | The present defects are cross-reference failures that static checks can catch cheaply. |

## Findings

### 1. Six module slots are declared but have no designer positions — P0

The light, medium, and heavy chassis each declare:

- five required slots: turret, main armament, suspension, armor, and engine;
- ten optional slots: `special_type_slot_1` through `special_type_slot_10`.

Examples are in `common/units/equipment/tank_chassis.txt`:

- light chassis: required slots begin at line 18; special slots begin at line 71 and end at line 314;
- medium chassis: required slots begin at line 503; special slots begin at line 557 and end at line 800;
- heavy chassis: required slots begin at line 984; special slots begin at line 1039 and end at line 1282.

All 252 files under `interface/equipmentdesigner/tanks/` contain placeholders for all ten special slots. For example, `tank_chassis_medium_tank.gui` includes slot 4 at line 94, slot 5 at line 101, and slot 10 at line 136. Those containers do not choose screen coordinates; they are module-content placeholders.

The outer layout is controlled by `interface/tank_designer_view.gui`. The mod does not provide this file, so it inherits the 1.19.2 vanilla view. That view defines only `pos_custom_module_slot_window_0` through `_8` (local game file lines 136–180): nine total positions, matching vanilla's five required plus four optional slots.

Result: the data model asks for 15 positions and the UI supplies nine. The 2026-06-14 integration commit added slots 5–10 to all 252 equipment-specific GUI files but did not add the corresponding outer layout positions. The reported “couple of extra slots missing” is therefore six missing positions, not two.

Required work:

1. Add a mod `interface/tank_designer_view.gui` based on the current 1.19.2 file.
2. Define positions 0–14 and deliberately lay out all five required plus ten optional slots.
3. Rework the lower controls/tooltips if needed rather than overlapping the extra row with upgrades, cost, or role controls.
4. Verify generic and country-specific light/medium/heavy views at supported resolutions and UI scales.
5. Test keyboard/mouse hitboxes and module tooltips, not only visible icons.

### 2. AI and historical tank designs are absent; bookmark equipment is invalid or bare — P0

`descriptor.mod:20` uses `replace_path="common/ai_equipment"`. The mod's replacement directory contains only:

- `generic_naval_capitals.txt`
- `generic_naval_carriers.txt`
- `generic_naval_screens.txt`
- `generic_naval_submarines.txt`

There is no generic or country tank AI-design file. By comparison, the current base game supplies `generic_tank.txt` plus ENG, FRA, GER, HUN, ITA, JAP, SOV, and USA tank files. The base `_documentation.md` describes these scripts as the instructions the AI uses to create and upgrade variants for equipment roles. Vanilla files cannot act as a fallback because the directory is replaced.

There are also no scripted historical tank module layouts elsewhere in the mod. A repository-wide scan finds `main_armament_slot =` only in the chassis and module definition files, never in country history, unit history, or AI equipment. The chassis defaults explicitly use `main_armament_slot = empty` (`tank_chassis.txt:464`, `:945`, and `:1427`).

The NSB unit histories then reference chassis directly:

- 148 tank-chassis stockpile/production references occur across 59 of the 68 `*_nsb.txt` OOB files;
- 40 of those references are specialized AA, artillery, or destroyer chassis across eight OOB files;
- `history/units/USA_1949_nsb.txt:1572-1626` starts production on raw light, medium, destroyer, artillery, and AA chassis;
- the same file's stockpiles at lines 1719–1795 use raw chassis identifiers rather than created variant names.

The supplied runtime evidence confirms the impact. Each of `error.log`, `error_1.log`, and `error_2.log` contains the same 54 tank “does not have any equipment variant” errors. In `error.log:7303-7346`, USA repeatedly lacks the referenced light artillery and AA variants. Lines 7347–7361 show SOV and USA also lacking medium destroyer, medium artillery, and heavy artillery variants. Five unique missing types are observed in that run.

This means two different failures coexist:

- specialized role chassis referenced by OOBs may not exist as variants at all;
- main tank chassis can resolve to their version-zero/default chassis, but no historical module design was created, and the default main armament is empty.

Required work:

1. Create a generic tank AI-design suite using the rework's actual module IDs and 15-slot layout. Cover normal light/medium/heavy tanks and every retained role.
2. Add country-specific preferences only after the generic suite works for every AI country.
3. Create historical starting variants before OOB stockpiles and production lines consume them. At minimum cover every chassis referenced in the 1949 and 1980 NSB OOBs.
4. Point stockpile and production entries to valid created variants where the scripting API requires a variant, not merely a chassis type/version.
5. Give every retained role a valid gun/turret/armor/engine/suspension combination and test design upgrades after new chassis/module research.
6. Treat a clean absence of `equipmentpool.cpp:1410` and `equipmentvariant.cpp:1108` tank errors as an acceptance gate.

### 3. Marine mechanized equipment is hidden with NSB and blocks amphibious progression — P0

The content exists:

- `common/units/equipment/mechanized_marine.txt:8-172` defines the archetype and five equipment tiers for 1944, 1950, 1965, 1985, and 2005.
- `common/units/CWIC-Special-Units.txt:62-108` defines `mechanized_marine`, marks it as special forces and marines, and makes it consume `mechanized_marine_equipment`.
- `common/technologies/armor.txt:1765-1932` defines `amphibious1` through `amphibious5`, each enabling the corresponding equipment tier.

The acquisition path is broken with NSB:

- all five `amphibious*` technologies have only `folder = { name = armour_folder ... }`;
- `common/technology_tags/00_technology.txt:357-367` makes `armour_folder` available only without NSB and `nsb_armor_folder` available only with NSB;
- the shared APC technologies immediately above this line demonstrate the intended dual-folder pattern (`armor.txt:967-974`, `:1003-1009`), but the marine line never received the NSB folder entries;
- `common/technologies/infantry.txt:2740-2752` makes the visible `amphibious_warfare_3` tech depend on hidden `amphibious1`. This also blocks `amphibious_warfare_3` and everything after it, not just equipment production.

There is inconsistent gating as well: the subunit is `active = yes`, while `amphibious_warfare_3` also tries to enable it. The user may see the battalion but still have no normally researchable equipment for it.

Why the bug can appear inconsistent between countries/bookmarks: 135 country-history files directly grant one or more `amphibious1-5` technologies, which can bypass the hidden research node for those starts. That masks rather than fixes the generic acquisition path.

`common/units/equipment/amphibious_mechanized.txt` is a zero-byte leftover while the implemented custom line lives in `mechanized_marine.txt`. Because the mod replaces `common/units`, there is no vanilla equipment fallback.

Required work:

1. Add `nsb_armor_folder` entries to `amphibious1-5`, matching the dual-folder APC pattern, or move the canonical line into the always-visible infantry amphibious branch.
2. Keep one authoritative unlock for the battalion (`active = no` plus a tech unlock, or deliberately active from start), not both.
3. Keep `amphibious_warfare_3` reachable under both DLC states.
4. Test a generic country without direct history grants as well as a major that starts with `amphibious1`.
5. Confirm research enables equipment production, the battalion can receive it, and AI research/production can use it.

### 4. Armored and mechanized engineer support companies use the hidden legacy MBT tree — P0

`common/technologies/support.txt` has a seven-stage armored-engineer line:

- `tech_armor_engineers` enables both `engineer_armored` and `engineer_mechanized` (`support.txt:61-82`) and requires legacy `main_battle_tanks`;
- stages 2–7 require `main_battle_tanks_2` through `_7` at lines 124, 173, 222, 269, 352, and 399.

Those MBT technologies are defined in `common/technologies/armor.txt` and appear only in `armour_folder`, which is hidden with NSB. The NSB equivalents are `nsb_main_battle_tanks0` through `_8` in `NSB_armor.txt:500-837`, but the support chain never references them.

A full cross-check of dependencies outside `armor.txt` found exactly eight dependencies on technologies available only in the legacy armor folder:

- the seven armored-engineer dependencies above;
- `amphibious_warfare_3 -> amphibious1`.

The equipment side was only partly migrated. Commit `f5775b61d4` changed `engineer_armored` from `mbt_equipment` to `medium_tank_chassis` and armored recon from `lt_equipment` to `light_tank_chassis`; it did not migrate the support-tech prerequisites.

Starting histories can again mask the first break. For example, SOV starts with `tech_armor_engineers` already granted and uses mutually exclusive blocks for legacy versus NSB tank starting techs (`history/countries/SOV - Soviet union.txt:327-365`). A campaign researching later tiers will still encounter the inaccessible legacy dependency.

Required work:

1. Do not put both legacy and NSB tank techs in the same `dependencies` block; dependencies are cumulative, so that would require both.
2. Prefer a DLC-neutral armor milestone used by shared support content. Grant/complete it from the appropriate legacy or NSB chassis tech.
3. A smaller alternative is to keep the visible engineer/support prerequisite chain and use a tested `allow` trigger with `OR = { has_tech = legacy; has_tech = NSB }` for the armor requirement.
4. Map tiers by intended year rather than blindly matching suffixes: the two MBT lines do not use identical year/suffix sequences.
5. Test every engineer tier in a progressing game, not only its pre-granted bookmark state.

### 5. Light SP artillery is built from the medium chassis family — P0 quick fix

`common/units/equipment/x_tank_chassis.txt:18-24` currently contains:

```text
light_tank_artillery_chassis = {
    archetype = medium_tank_chassis
```

The vanilla relationship and the rework's own original 2026-06-14 definition both use `light_tank_chassis`. Commit `27b63dd93b` changed this single line from light to medium while adding the separate `medium_tank_heavy_artillery_chassis` role.

Impact: every generated light artillery tier inherits the medium chassis family/module constraints and then presents itself as light artillery. This can distort available guns, base cost/stats, research-tier relationship, and variant matching.

Required work: restore `archetype = light_tank_chassis`, regenerate/test all light SPG tiers, and verify existing save compatibility.

### 6. Several designer roles are orphaned or only partially present — P1

#### Amphibious tanks

The mod overrides the files that normally define amphibious designer content but does not recreate it:

- no `amphibious_drive` module definition exists;
- no light, medium, or heavy `*_tank_amphibious_chassis` duplicate archetype exists in `x_tank_chassis.txt`;
- no `amphibious_tank_chassis` equipment or technology exists;
- `tank_amphibious.txt` is empty.

References remain:

- 44 tank designer GUI files whose names contain `amphibious_tank`;
- `common/equipment_groups/mio_equipment_groups.txt:131-135` includes nonexistent `amphibious_tank_chassis`;
- `common/factions/goals/faction_goals_medium_term.txt:1268-1289` checks vanilla amphibious unit/technology IDs;
- each supplied error log reports invalid `amphibious_mechanized_infantry` and `amphibious_tank_chassis` database objects.

This needs a product decision. Either implement the complete amphibious designer role using the rework's technology timeline, or remove/update all stale UI, MIO, faction-goal, localization, and graphics references. Leaving half of each approach is the current failure mode.

#### Rocket tank roles

`x_tank_chassis.txt` defines light, medium, and heavy rocket chassis, and the NSB chassis techs enable every generated tier. No subunit `need` consumes any of those archetypes. The only meaningful references are their definitions, technology unlocks, and script enums. They are research-visible designer outputs without a battlefield consumer.

Decide whether these should supply a new armored rocket-artillery subunit, alias an existing rocket SP artillery need, or be removed.

#### Medium heavy-artillery chassis

`medium_tank_heavy_artillery_chassis` is defined at `x_tank_chassis.txt:63-71` and enumerated, but no technology enables it and no unit consumes it. It is currently a dead role.

#### Modern and super-heavy designer chassis

The mod has empty `tank_modern.txt` and retains a legacy `sht_equipment` line rather than designer super-heavy chassis. That may be an intentional Cold War design choice, but inherited and copied systems still expect modern and super-heavy chassis:

- MIO groups list `modern_tank_chassis` and `super_heavy_tank_chassis` (`mio_equipment_groups.txt:138-148`);
- the current error log has 56 “Unknown equipment type” messages covering eight modern/super-heavy chassis and role IDs, seven repetitions of each;
- 40 modern and 40 super-heavy tank designer GUI files remain.

Choose one model and make every consumer agree with it. If MBTs intentionally remain `medium_tank_chassis` and super-heavy tanks remain legacy equipment, remove/remap designer-era expectations rather than restoring unused archetypes only to quiet logs.

### 7. NSB technology categories and AI research timing are copy-pasted — P1

The two NSB files define 169 technologies. Their category distribution is:

- the initial `nsb_iw_armored_vehicles`: `vehicles, armor`;
- all other 168 technologies: `vehicles, infantry_vehicles, infantry_vehicles_apc`.

That includes light tanks, MBTs, heavy tanks, engines, suspension, armor, guns, ammunition, fire-control systems, loaders, defenses, and smoke. None of those 168 technologies is tagged `armor`, `armor_light`, `armor_medium`, or `armor_heavy`.

Consequences:

- existing armor-category research bonuses do not affect the NSB replacement line as intended;
- APC/infantry-vehicle bonuses can affect unrelated tank hull and module research;
- light, medium, and heavy specialization bonuses cannot distinguish the branches;
- `common/national_focus/BRA_50s.txt:3542-3546` uses the nonexistent technology category `light_tank_chassis`, producing a repeated runtime error in all three logs;
- the repository contains another 42 focus reward references to valid legacy armor categories (`armor`, light/medium/heavy variants) that need their NSB behavior checked.

AI research scripting shows the same copy pattern. `NSB_armor.txt` contains 23 and `NSB_armor_modules.txt` contains 64 occurrences of `date > 1944.1.1`, including technologies dated decades later. Other nodes simply use `ai_will_do = { factor = 100 }`. This is not a tuned 1940–2020 research plan.

Required work:

1. Define a category policy for chassis branches and module families.
2. Apply `armor` plus the correct light/medium/heavy tag to chassis techs; apply appropriate armor/module categories to component technologies.
3. Remove `infantry_vehicles_apc` from tank-only technologies unless the overlap is deliberate and documented.
4. Audit all focus `add_tech_bonus` rewards against both technology systems. Replace BRA's invalid category.
5. Set AI dates/weights by the actual node year and desired country behavior, then observer-test research order together with AI design creation.

### 8. Graphics integration is noisy and incomplete — P1 after role IDs stabilize

The current `error.log` contains:

- 732 equipment-graphics “Entity referenced ... does not exist” lines associated with tank/armor/chassis names, covering 64 equipment IDs in the static count;
- 56 unknown modern/super-heavy tank chassis/type lines described above;
- a missing `gfx/texticons/unit_super_heavy_armor_icon_small.dds` texture;
- four directly counted missing tank/armor GFX references, in addition to the entity warnings.

Some entity warnings are inherited vanilla/DLC asset-pack mappings and may be harmless visual fallbacks, so they should be triaged after the final equipment role list is decided. They are still evidence that the rework was not validated against the active equipment graphic database.

Five unlocked modules have English localization but no exact `GFX_SMI_<module>` sprite in either the mod or current base game:

- `flamethrower`
- `medium_open_gun`
- `heavy_open_gun`
- `medium_fixed_superstructure`
- `heavy_fixed_superstructure`

Verify whether the UI has a deliberate fallback. If not, add the small module sprites or explicitly alias them to the intended base icon.

### 9. Module and technology cleanup debt — P2

The active module/tech relationship is healthier than the integration around it:

- 287 tank modules are defined;
- 239 are referenced by `enable_equipment_modules` in the two NSB armor files;
- all 239 live modules have English names and descriptions;
- no NSB armor-tech module unlock points to an undefined tank module;
- all 169 NSB technologies have English names and descriptions.

However, 48 defined tank modules are never unlocked by either NSB armor file. They form an older/prototype set, including machine guns/IFV guns, hybrid engine, suspension variants, welded/cast/composite/NERA armor, add-on/ERA armor, smoke launchers, blowout panels, and external fuel. The same area contains 35 `#PLACEHOLDER` resource blocks.

This leaves allowed chassis categories with no live module:

- `tank_armor_nera`
- `tank_engine_hybrid`
- `tank_light_vehicle_main_armament`
- `tank_mobility_fuel`
- `tank_radio_module`
- `tank_secondary_turret`
- `tank_special_module`

The first four have dead module definitions; the last three have no local module definition at all. These empty choices may not appear in the picker, but they show that the chassis slot contract and the live module catalog were never reconciled.

There are also three dangling `leads_to_tech` paths in `NSB_armor.txt`:

- `nsb_light_tanks8 -> nsb_light_tanks9` at line 437;
- `nsb_main_battle_tanks8 -> nsb_main_battle_tanks9` at line 812;
- `nsb_heavy_tanks3 -> nsb_heavy_tanks4` at line 1005.

The target tech blocks are commented-out placeholders. Remove the paths if those are terminal nodes, or implement real successors.

Four tank-adjacent scaffold files are zero bytes: `00_CWIC_modules.txt`, `amphibious_mechanized.txt`, `tank_amphibious.txt`, and `tank_modern.txt`. Delete them if they are intentionally obsolete or populate them under a documented architecture; empty overrides make fallback assumptions difficult to reason about.

Finally, `common/script_enums.txt:979-1102` retains more than a hundred malformed legacy IDs from a `chassist`/`chassisbt` naming era solely to silence old-save warnings. That is a reasonable temporary compatibility measure, but it should be documented with a removal version and covered by an explicit save-migration policy.

## How the rework reached this state

The designer was not created entirely in the recent rush. Git history shows technology/module scaffolding and partial work dating back to September 2023, with additional work in 2024 and 2025. The broad integration happened in a short 2026 sequence:

- 2026-06-13: NSB armor techs/icons and tank designer;
- 2026-06-14: categories, roles, ten-slot GUI placeholders across 252 files;
- 2026-06-15 to 2026-06-25: role and turret fixes;
- 2026-07-03: vanilla-style units for tank roles;
- 2026-07-04 to 2026-07-05: multiple module/OOB fixes, including a fix commit, same-day revert, and “attempt 2 tank part only tested”;
- 2026-07-09: compatibility enums and error cleanup.

This explains the current shape: the module catalog is relatively deep, while cross-system integration was applied in separate passes and tested narrowly. The clearest examples are equipment needs migrated without their tech prerequisites, GUI slot containers added without the outer positions, OOB chassis references added without historical variants, and role IDs added without unit consumers.

## Recommended implementation sequence

### Phase 1: unblock progression and correct data

1. Fix the light SPG archetype.
2. Add the NSB-visible marine equipment tech path and remove the hidden prerequisite from the visible amphibious branch.
3. Replace the seven legacy-only engineer prerequisites with a DLC-neutral or tested OR-gated solution.
4. Remove the three dangling path arrows.
5. Add a small static check that rejects visible techs depending on techs exclusive to a hidden DLC folder.

### Phase 2: make the designer and bookmarks function end-to-end

1. Implement the 15-position tank designer view.
2. Build and validate a generic AI design suite.
3. Create starting historical variants for all chassis used by the 1949 and 1980 NSB OOBs.
4. Update stockpile/production references and rerun until all tank missing-variant errors are gone.
5. Observer-test AI research, design creation, upgrading, production, and template supply.

### Phase 3: settle the content contract

1. Decide which of amphibious, rocket, modern, super-heavy, and medium-heavy-artillery roles are supported.
2. For every retained role, require all six pieces: equipment archetype, enabling tech, usable modules, consuming subunit, AI design, and historical/OOB integration.
3. Remove every stale reference for roles that are intentionally unsupported.
4. Correct technology categories and focus research bonuses.

### Phase 4: presentation, cleanup, and balance

1. Resolve equipment graphic database mappings and module sprites.
2. Delete or finish the 48 dead modules and their placeholder resource costs.
3. Tune module stats, research pacing, AI priorities, and production costs only after all slots and roles are reachable.
4. Set an old-save compatibility window and eventual cleanup plan for malformed enums.

## Acceptance test matrix

| Area | NSB off | NSB on |
| --- | --- | --- |
| Research folders | Legacy armor line visible; NSB folders hidden | NSB chassis/module folders visible; legacy armor folder hidden |
| Marine mechanized | `amphibious1-5` researchable; equipment producible | Same five tiers researchable through a visible path; amphibious-warfare branch remains reachable |
| Engineer supports | All seven tiers reachable through legacy progression | All seven tiers reachable through NSB progression without researching hidden legacy MBTs |
| Designer UI | Not applicable to legacy equipment | All 15 declared slots visible and usable at supported UI scales |
| Starting OOBs | Legacy equipment and production resolve | Every chassis stockpile/line resolves to a valid design; no empty-gun historical tank defaults |
| AI | Produces legacy equipment | Creates, upgrades, and produces valid tank designs for researched chassis and needed roles |
| Roles | Legacy units receive their equipment | Every retained designer role has a consuming unit and valid design; removed roles have no stale references |
| Logs | No new tank errors | No missing tank variants, invalid amphibious IDs, invalid tank tech categories, or unknown retained chassis types |

Minimum scenarios:

1. A generic minor with no direct armor/amphibious history grants, starting in 1949.
2. USA and SOV in 1949, because the supplied log already reproduces variant failures there.
3. USA, SOV, and a generic minor in 1980 to exercise late module/research progression.
4. At least one hands-off AI run long enough to unlock a new chassis generation and replace production.
5. Designer checks at 1920×1080 and 2560×1440, plus the project's supported UI scale extremes.

## Validation notes and limits

This is a source, history, base-game comparison, and supplied-log audit. It did not launch a new interactive game session. Findings marked as runtime failures are backed by the three current logs; UI behavior and the five potential icon fallbacks should still be confirmed in-game after implementation.

The audit deliberately distinguishes “missing” from “intentionally redesigned.” Modern and super-heavy designer chassis may be intentionally excluded, for example. The defect is that other live systems still reference them. The required outcome is consistency, whether the team restores those roles or removes/remaps their consumers.

## Primary evidence index

- Mod replacement policy: `Cold War Iron Curtain/descriptor.mod:20-25`
- Chassis slots/defaults: `common/units/equipment/tank_chassis.txt:18-469`, `:503-950`, `:984-1432`
- Role archetypes and light-SPG error: `common/units/equipment/x_tank_chassis.txt:5-148`
- Tank modules/dead prototype content: `common/units/equipment/modules/00_tank_modules.txt`
- NSB chassis/module research: `common/technologies/NSB_armor.txt`, `NSB_armor_modules.txt`
- Legacy/shared armor and marine equipment research: `common/technologies/armor.txt:45-1932`
- DLC folder visibility: `common/technology_tags/00_technology.txt:350-374`
- Engineer prerequisites: `common/technologies/support.txt:61-415`
- Marine battalion and amphibious branch: `common/units/CWIC-Special-Units.txt:62-108`, `common/technologies/infantry.txt:2740-2860`
- NSB role battalions: `common/units/need_for_tank_roles.txt`
- AI equipment replacement contents: `common/ai_equipment/`
- Representative NSB OOB: `history/units/USA_1949_nsb.txt:1550-1800`
- Orphan MIO/faction references: `common/equipment_groups/mio_equipment_groups.txt:115-148`, `common/factions/goals/faction_goals_medium_term.txt:1265-1290`
- Runtime evidence: repository-root `error.log`, `error_1.log`, and `error_2.log`

## Implementation outcome (2026-09-04)

Implemented on branch `tank-designer-and-doctrine-rework-test`. This section records what was actually built and verified; the sections above remain the original audit.

### Supported role contract

The designer supports light, medium, and heavy chassis in five roles: base tank, tank destroyer, self-propelled artillery, self-propelled anti-air, and flame. The rocket, amphibious-designer, modern-designer, super-heavy-designer, and medium-heavy-artillery roles were removed rather than finished, together with their GUI files, aliases, and generated enums. Every retained role has an archetype, enabling technology, usable modules, a consuming subunit, an AI recipe, and OOB integration. The designer view provides all 15 declared slot positions.

### Bookmark variant bootstrap

Each NSB bookmark OOB names an explicit variant on every version-sensitive request. Those variants come from one shared creator, `cwic_create_starting_tank_variants`, which builds 30 conservative five-module designs, each guarded by its own chassis technology.

The ordering rule that this depends on: an OOB-local `instant_effect` runs *after* that OOB's own production, stockpile, and forced-variant requests are resolved, so a variant created there is always too late. The bootstrap therefore runs in country history immediately before `set_oob`:

```text
country scope
  -> set_technology for exactly the chassis technologies this bookmark needs
  -> cwic_create_starting_tank_variants = yes
  -> set_oob = <bookmark NSB OOB>
```

Two further rules were established by runtime testing:

- A tank bought from or designed by another tag is looked up on *that* tag. `producer` on a stockpile or production request and `creator` on a forced variant both name the country whose designer must already hold the variant, so the chassis technology belongs in that country's bootstrap, not the loading country's. This is what made FRA, ENG, and the `CAP`/`CUM` manufacturer bloc tags fail.
- Those tech sets are scoped per bookmark. A 1949 bootstrap must not preload the 1970s chassis its country only sells in 1980.
- `CAP` and `CUM` sell tanks but never load an OOB, so they call the creator directly from their own history.

`RAJ_1980_nsb` asked for a `light_tank_chassis_3` variant named `AMX-13/75`. That name only exists as a legacy `lt_equipment_3` variant in FRA's history and no designer bootstrap creates it, so those six requests were retargeted to the generic `Standard Light Tank 1950`.

### Pre-existing OOB defects repaired while testing

Four owned NSB OOBs failed to parse and silently dropped content:

- `IRQ_1980_nsb.txt` and `PER_1980_nsb.txt`: `marine { ... }` was missing its `=`, breaking the Marine Brigade template.
- `CUB_1980_nsb.txt` and `NOR_1980_nsb.txt`: an uncommented section label inside `units = { ... }`.

### Verified runtime results

Full 35-DLC `-debug -ai_testing` runs of both bookmarks:

| Bookmark | Tank variant lookup failures | Doctrine/enum/creator errors |
| --- | --- | --- |
| 1949 | 0 | 0 |
| 1980 | 0 | 0 |

Remaining `does not have any equipment variant` entries in both logs belong to unrelated systems: legacy infantry and artillery equipment, MTG naval hulls, jet and transport aircraft, and the legacy `lt_`/`mbt_`/`ht_` equipment sold by the weapon-purchasing decisions. None involve a designer chassis type.

`-ai_testing` starts the default bookmark and does not accept a start-date argument, so the 1980 runs were produced by temporarily dating the gathering-storm bookmark to `1980.1.1.12`. That edit was reverted; the bookmark files are unchanged on this branch.

### Regression validation

`tools/validate_military_reworks.py` is the static gate. It checks doctrine loading and content, technology paths, localization and effects, tank modules, unlocks and categories, the supported role set, AI recipes, enum cleanup, OOB types and named requests, that every requested variant name is one a bootstrap actually creates, that no OOB bootstraps its own variants, that every country-history bootstrap precedes its `set_oob` with exactly the required technologies, and the 15 designer slots.

### Not covered automatically

The designer UI at multiple resolutions and UI scales, save/load, and multiplayer synchronization were not exercised. They still need a manual pass.
