# Reference

Mechanics, tables and file map. For *why* a choice was made see `DECISIONS.md`.

## Designer routing - the one thing that makes carriers work

`type = { armor mechanized }` on the archetype, restated on every hull, is what routes
equipment to `tank_designer_view` instead of the legacy `land_equipment_designer_view`
"Create Variant" popup. **Nothing else does it** - not module slots, not
`interface_category`, not a designer GUI window. Three rounds of QA established this:

- The binary exposes three module designers (`tank_designer_view`,
  `plane_designer_view`, `countryequipmentdesignerview`) and three legacy upgrade views
  in `equipmentupgradedesignerwindow.gui` (`land_`, `air_`, `naval_equipment_designer_view`).
- The popup owners saw was the **land** upgrade view. The APC hulls were
  `type = mechanized`, i.e. generic land equipment, so that is what they classified into.
- `interface_category` is not the lever: vanilla `armored_car.txt` and legacy
  `tank_light.txt` use `interface_category_armor` and still get the upgrade window,
  because they have no module slots.
- Module slots alone are not sufficient either - that is what the first attempt proved.
- Adding the missing `equipment_designer_<archetype>` window did **not** fix routing.
  The file is still required so the designer has a layout once it does open, but do not
  read its presence as evidence the routing problem is solved.

`mechanized` is retained in the type so the archetype keeps its land and transport
classification for the AI and for every `transport = mechanized_equipment` consumer.
Multi-value `type` is an established pattern - `x_tank_chassis.txt` already ships
`type = { armor anti_air }` and `type = { armor artillery }`.

`interface_category` was deliberately **not** changed; `mechanized_equipment` stays
`interface_category_land` so legacy mechanized keeps its production-tab grouping. If the
upgrade popup ever reappears, moving the archetype to `interface_category_armor` is the
next and last lever, and it moves all legacy mechanized into the armor tab.

**Known cost:** equipment `type` is what the AI uses by default to map archetypes to
strategies such as `unit_ratio`, so legacy mechanized now also counts as armor. The
documented override is `ai_type`, but its documented values are all air/naval, so it was
not used rather than guess at a land value. Watch AI armor-versus-mechanized production
ratios in a long run.

**Duplicate production listing is correct.** A carrier lists under both the
infantry/land and armor production filters because the filter row matches on equipment
type and a two-type equipment matches two filters. Owner QA confirmed it is one design,
not a clone: a design saved from one filter appears with the same identity and stats
under the other and stays in sync. Vanilla does the same - `light_tank_aa_chassis` is
`type = { armor anti_air }`. **Do not "fix" it by dropping `mechanized` from the type**;
that strips the archetype's land and transport classification.

## Why the role dropdown reads "Unknown"

Confirmed 2026-09-07 by reading the module set and vanilla GUI:

- The role dropdown is **global, not per-archetype**. It lists the base role plus one
  entry per distinct `allow_equipment_type` value in the loaded module set. CWIC has
  exactly four (`anti_tank` x35, `artillery` x4, `anti_air` x3, `flame` x1), so every
  chassis designer in the mod shows exactly five entries. No APC or IFV module carries
  `allow_equipment_type`, so four of the five are forbidden (`GFX_role_forbidden`).
- An entry's **name** comes from the `duplicate_archetypes` entry it would switch to, in
  `x_tank_chassis.txt`. `mechanized_equipment` and `mechanized_heavy_equipment` have
  none, so the engine has nothing to name and falls back to the generic `unknown` loc
  key (`terrain_l_english.yml:2`). That is why even Artillery and Anti-Air, which render
  fine in a light-tank designer, read "Unknown" here.

Consequence: the `tank_designer_mechanized_equipment`, `tank_designer_mechanized` and
`tank_designer_mechanized_heavy_equipment` loc keys **cannot** fix the label - the
lookup never reaches localisation. Both key shapes are structurally plausible (vanilla
uses `tank_designer_<archetype>` for chassis-swap roles and `tank_designer_<extra type>`
for role types like `anti_air`), so leave both in place until one is observed resolving.

To give these families working roles you need **both** halves: a `duplicate_archetypes`
entry targeting the archetype, and at least one module with `allow_equipment_type`. One
without the other yields either an unnamed entry or a permanently forbidden one.

## APC hull table

Hulls are authored approximations. Hull plus the baseline recipe (`apc_open_troop_bay`,
`apc_firing_ports`, `Half_track`, `Armor_0_W`, `tank_gasoline_engine`) is *intended* to
land near the legacy row; `armor_value` is the only stat pinned equal to the frozen row
and enforced by the validator.

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

Observed in game for `apc_chassis_0`: max speed 13.2 km/h, reliability 94.0%, hardness
30.0%, armor 15.0, breakthrough 6.0, defense 14.5, soft/hard attack and piercing 0.0,
fuel usage 2.10, production cost 7.70. Hardness 30% is hull 0.5 plus half-track -0.2,
confirming module stacking on an APC hull behaves as designed.

## IFV ground truth

| | |
| --- | --- |
| Frozen rows | Heavy Mech I-VIII = `mechanized_heavy_equipment_1..8` |
| Archetype | `mechanized_heavy_equipment` |
| File | `common/units/equipment/mechanized_heavy.txt` |
| Consumers | `common/units/CWIC-Infantry.txt` (`mechanized_heavy_equipment = 50`), `common/units/CWIC-Special-Units.txt` |
| Legacy technologies | `mechanized_heavy_infantry`..`8` in `common/technologies/armor.txt`, NSB folder column `x = 3` |
| Equipment years | 1947, 1950, **1955**, 1965, 1975, 1985, 1995, 2005 |
| Legacy tech start years | 1947, 1950, **1960**, 1965, 1975, 1985, 1995, 2005 |

**Heavy Mech is armed** - real soft/hard attack and piercing. Do not copy the APC's
zero-attack profile. Do not equate the legacy name "Heavy Mech" with heavy tank hulls.

Source role penalties: APC -0.4 armor/hardness, IFV -0.2. Exact implementation and
stacking must be checked against game semantics.

NSB technology columns: APC `x = -6`, mechanized `x = 0`, heavy mech `x = 3`,
amphibious `x = -3`, IFV `x = -9`. Unlock new modules from `NSB_armor.txt` or
`NSB_armor_modules.txt` only - the validator scans nothing else and will report a
module unlocked elsewhere as unreachable.

## The 18-envelope mapping

| Frozen rows | Legacy equipment | Archetype | Designer family | State |
| --- | --- | --- | --- | --- |
| Light Mech I-VIII / APC | `mechanized_equipment_3..10` | `mechanized_equipment` | `apc_chassis_0..7` | **done** |
| Heavy Mech I-VIII / IFV | `mechanized_heavy_equipment_1..8` | `mechanized_heavy_equipment` | `ifv_chassis_0..7`, armed | **done** |
| WWII Mech 1-2 | `mechanized_equipment_1..2` | `mechanized_equipment` | legacy-only, pre-designer era | not planned |
| Marine mech | `mechanized_marine_equipment` | `mechanized_marine_equipment` | amphibious mobility module | not started |
| Heavy APC / heavy IFV | no legacy row | tbd | medium-hull generation | not started |

## Three conflicting carrier designs in the sources

| # | Source | Design |
| --- | --- | --- |
| 1 | xlsx `Roles` tab | APC/IFV as roles hosted on the light and medium tank hulls |
| 2 | drawio `[DONE] AFV Hulls` | Three carrier leaf nodes only: `IFV` (1960, off Post-WW2 Light Tank), `Heavy APC` (1985, off Second Gen MBT), `Heavy IFV` (2005, off Second+ Gen MBT) |
| 3 | drawio `[REFERENCE] Whole Tech Tree`, `x = -840..-920` | A dedicated mechanized ladder in its own column, separate from every tank hull column |

**Design 3 is implemented and was ratified 2026-09-07:**

```
Early WW2 Mechanized (1940) -> Mid-WW2 Mechanized (1943) -> Late WW2 Mechanized (1945)
        |
        +-- Light Mech./Wheeled Mech. -> APC           -> Light Mechanised II..VII
        +-- Heavy Mech./Tracked Mech. -> Heavy APC/IFV -> Heavy Mechanised II..VII
```

The wheeled/tracked flavour split is explicit in the node labels and is the design
reason APC AI recipes allow `tank_non_tracked_suspension_type` while the IFV line leans
tracked. The one part of the Roles tab that still holds is that Heavy APC and Heavy IFV
belong to the medium hull generation.

## National medium tank presets

| Medium chassis tier | USA | SOV |
| --- | --- | --- |
| 0 | M4 Sherman | T-34-85 |
| 1 | M26 Pershing | T-44 |
| 2 | M46 Patton | T-54 |
| 3 | M47 Patton | T-55 |
| 4 | M48 Patton | T-62 |
| 5 | M60 Patton | T-64A |
| 6 | M1 Abrams | T-72 |

Legacy tier mappings, not assertions that chassis technology years equal historical
introduction dates. Loadouts are authored approximations: Soviet diesel/smoothbore
progression with late carousel loaders and composite armor; US gasoline/diesel/turbine
engines and rifled guns. All carry kinetic and HE ammunition and coaxial MGs. Late US
gun naming follows the available module ladder, not exact historical classification.

Exact recipes are in `data/National_Tank_Preset_Manifest.json`, checked against
`common/scripted_effects/CWIC_national_tank_presets.txt`.

Carrier presets: 572 selected producer/chassis pairs across 86 tags, ten bookmark
chassis (APC and IFV tiers 0-4), 100 migrated OOB requests. Full table and provenance
in `data/APC_IFV_Bookmark_Mapping.md` and `data/APC_IFV_Preset_Manifest.json`.

Ten names legitimately span two chassis tiers because an incomplete national ladder
shifts a vehicle relative to the common ladder: BTR-40, M9 Halftrack, M59, BTR-152,
BTR-60, BTR-60PB, BTR-50P, BTR-50PK, MT-LB, BMP-1.

## Production-tab obsolescence

`80304e2030` adds `mark_older_equipment_obsolete = yes` to all 44 creation blocks in
`CWIC_tank_designer_effects.txt` and `CWIC_national_tank_presets.txt`. Creation order
matters: families are contiguous and tiers ascend, so the newest eligible design is
created last. The national helper runs first; generic medium creation excludes USA/SOV.

Preserve ascending order, and verify that new APC/IFV roles do not incorrectly obsolete
a different role in the same family. Older designs must remain resolvable for starting
units, stockpiles and named requests - obsolescence is not deletion. Export presets are
created with `obsolete = yes` in `CWIC_tank_focus_effects.txt` and were not the cause of
bookmark spam.

## The ammunition contract

The validator requires every AI recipe to include attack-producing AP and HE ammunition
modules. The rule is driven by `needs_ammunition()`, which tests whether a module
**multiplies** `soft_attack`/`hard_attack`/`ap_attack`:

- If armament modules multiply attack stats (the conventional gun pattern), recipes
  **must** carry ammunition modules.
- If they add flat stats, extend the exemption instead.

The APC family is exempted because its armament modules use `add_stats` only. IFV
weapon modules multiply, so all eight IFV recipes mount kinetic/AP and HE ammunition and
are gated on the hull, ammunition and HE-ammunition techs.

`tank_module_balance_report()` excludes the seven APC and sixteen IFV modules from
frozen-workbook coverage by name, since the 2023 workbook predates both families and
must stay byte-identical.

## Validator contract, per designer family

`validate_apc_designer_family()` and `validate_ifv_designer_family()` pin:

- Archetype exposes ten specialized slots with the shared category layout, both
  mandatory weapon positions restricted to family-only categories and still `required`.
- `default_modules` fills all five mandatory slots with family-legal modules; one
  secondary-turret count limit retained.
- **The legacy rows contain no `module_slots`** - the non-NSB invariant.
- Per hull: archetype, `module_slots = inherit`, `derived_variant_name`, year, DLC gate,
  parent chain, `armor_value` equal to the frozen row, unlocked by an NSB technology,
  and that technology absent from `armor.txt` (no legacy-folder leak).
- Modules exist, carry the right category, and do not multiply gun stats (APC).
- Archetype and every hull declare exactly the `armor` plus `mechanized` domain.
- Every hull technology's `start_year` matches its `@year` tree row.
- Every hull id present in `script_enum_equipment_bonus_type`.
- One AI recipe per hull, using the family categories, gated on its own technology.
- Localisation keys for every hull, derived variant, module and technology.
- `validate_designer_window_coverage()`: every `module_slots = inherit` equipment and
  every `duplicate_archetypes` role resolves an `equipment_designer_*` window.

Six APC and eleven IFV negative fixtures run under `--tank-self-test`. They write a
mutation to the source, assert rejection, and restore the file byte-identically - keep
the `try/finally` and the `encoding="utf-8", newline=""` write.

## Seven things a new designer family needs

1. Put the hulls on the **existing** archetype. Sub-unit `need` resolves an archetype
   name and multiple entries are AND, not OR, so a separate archetype produces equipment
   no battalion can consume. Sharing means zero sub-unit edits.
2. `type = { armor mechanized }` on the archetype and restated on every hull.
3. Leave the legacy rows without `module_slots`, ever.
4. A designer GUI window under `interface/equipmentdesigner/tanks/`.
5. NSB-only technologies in a free column, entered by `path` from
   `nsb_iw_armored_vehicles`, each on the `@year` macro matching its `start_year`.
6. Every hull id in `common/script_enums.txt` under
   `script_enum_equipment_bonus_type`, or the game logs one `equipment_database.cpp:656`
   line per hull.
7. A role label in `localisation/english/designer_l_english.yml`.

Plus: modules in family-only categories with `GFX_SMI_<module>` icons registered; one
generic historical AI recipe per hull in a new group with its own `roles = { }`; every
technology with `start_year <= 1980` added to the 1980 major-producer grant in
`CWIC_tank_bookmark_research.txt`; ASCII English localisation for hulls, derived variant
names, modules and technologies.

## Cosmetic and art debt

- **Blueprint art is the light tank hull.** `tank_chassis_apc.gui` reuses
  `GFX_TC_light_tank_chassis` and the `GFX_TM_light_tank_chassis_*_slot` blueprints.
- **The 3D preview panel is empty.** Designer models come from a `tank_designer_model`
  list with no APC/IFV entry. Unit and map appearance are unaffected - those use the
  sub-unit entity lookup `<TAG>_<sub_unit>_<level>_entity`, owned by
  `zz_CWIC_armor_entity_aliases.asset`, which was not touched.
- **Carrier designs inherit the generic archetype picture.** See `STATUS.md` Finding 3.
- **No `search_filters` group.** The mod ships no `tank_filters.txt`, so adding one
  would override vanilla's; a separate file in `common/units/equipment/` holding only a
  `search_filters` block is the low-risk route if this is ever wanted.
- `visual_level` 2-9 is shared with the legacy mechanized rows; no new entity aliases
  were added.

`zz_CWIC_armor_entity_aliases.asset` holds 3,019 aliases spanning base armor, tank
destroyer, SP artillery, SP AA and flame sub-units across levels 0-9 (light, medium) and
0-4 (heavy), for the 75 tag/class combinations that define a base armor entity. Flame
aliases clone the shared `<class>_flame_tank_entity`. GER light, GER heavy, ITA heavy
and JAP light are deliberately excluded - the mod's `units_tanks.asset` replaces
vanilla's and those four have no base entity to clone. **The `zz_` prefix is load-order
critical**: all existing clones resolve backward, none forward, so it must load last.
Do not resurrect `zz_CWIC_armor_level0_entities.asset`.

## File map

Under `Cold War Iron Curtain/`:

| Path | Role |
| --- | --- |
| `common/units/equipment/mechanized.txt`, `mechanized_heavy.txt`, `mechanized_marine.txt` | Legacy equipment, archetypes, carrier hulls |
| `common/units/equipment/tank_chassis.txt` | Tank designer hulls |
| `common/units/equipment/modules/00_tank_modules.txt` | All designer modules |
| `common/units/CWIC-Infantry.txt`, `CWIC-Special-Units.txt` | Sub-unit supply consumers |
| `common/technologies/NSB_armor.txt`, `NSB_armor_modules.txt` | NSB unlocks and DLC routing |
| `common/technologies/armor.txt`, `artillery.txt` | Legacy ladders |
| `common/ai_equipment/generic_tank.txt` | AI recipes |
| `common/scripted_effects/CWIC_tank_designer_effects.txt` | Generic bookmark variant creation |
| `common/scripted_effects/CWIC_national_tank_presets.txt` | National presets |
| `common/scripted_effects/CWIC_tank_bookmark_research.txt` | 1980 major-producer grants |
| `common/scripted_effects/CWIC_tank_focus_effects.txt` | Focus rewards and exports |
| `common/script_enums.txt` | `script_enum_equipment_bonus_type` |
| `history/countries/`, `history/units/*_nsb.txt` | Bootstrap sites and OOBs |
| `interface/equipmentdesigner/tanks/` | Designer GUI windows |
| `interface/cwic_tank_rework_icons.gfx` | Module and technology icons |
| `localisation/english/tank_modules_l_english.yml`, `nsb_armor_l_english.yml`, `designer_l_english.yml` | Names and descriptions |
| `gfx/entities/zz_CWIC_armor_entity_aliases.asset` | 3D entity aliases |
| `CWIC Backup/tools/validate_military_reworks.py` | The static gate - the one backup file you may edit |
