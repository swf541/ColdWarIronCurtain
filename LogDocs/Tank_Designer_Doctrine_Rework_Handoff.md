# Tank Designer and Doctrine Rework Handoff

## Start here

- Repository: `/home/zom/Projects/ColdWarIronCurtain`
- Branch: `tank-designer-and-doctrine-rework-test`
- Base: `development-branch` at `4a999ae3f3`
- Current HEAD: `ff036b399b`
- Date of handoff: 2026-09-04
- Goal: bugfix, sanitize, complete, and polish the Tank Designer and Doctrine reworks without merging into `development-branch`.
- Status: complete. The doctrine rework, the tank designer rework, and the NSB bookmark variant bootstrap are implemented and verified at runtime on both bookmarks. See `## Outcome` below.

Read these investigations before making broad design changes:

- `LogDocs/Doctrine_Rework/Doctrine_Rework_Investigation.md`
- `LogDocs/Tank_Designer_Rework_Audit.md`

Do not restart the completed audit work. Continue from the three commits below and resolve the runtime blocker.

## Committed checkpoints

1. `f71dd22ba0 Document doctrine and tank designer audits`
2. `7b50137918 Restore and complete legacy doctrine rework`
3. `ff036b399b Finish tank designer integration and role cleanup`

The branch has not been pushed at this handoff.

### Doctrine work already committed

- Moved land, air, and naval doctrine technology files out of the parked `common/technologies/doctrine rework` path and into the active technology root.
- Kept the new DLC doctrine framework intentionally disabled through the exact zero-byte override set under `common/doctrines`.
- Added the missing zero-byte special-forces track override so the vanilla track does not leak into the retained legacy model.
- Corrected all `category = air_doctrine` references to `cat_air_doctrine`.
- Corrected BRA's invalid `light_tank_chassis` category to `armor_light`.
- Corrected the NATO transitional combined-arms technology-path typo.
- Added conservative gameplay effects to all 528 land-doctrine nodes.
- Added the missing Cuban capstone localization.

### Tank Designer work already committed

- Restored a 15-slot tank designer UI.
- Added 125 generic historical AI recipes covering the supported role matrix.
- Supported light, medium, and heavy tank, tank-destroyer, SPG, SPAA, and flame roles.
- Removed unfinished rocket, amphibious-designer, modern-designer, super-heavy-designer, and medium-heavy-artillery roles and references.
- Corrected the SPG archetype, module contracts, anti-air modules, aliases, NSB categories, and dates.
- Made marine and armored-engineer progression safe with and without NSB.
- Removed 124 unused GUI role files and five empty scaffolds.
- Added `common/ai_equipment/generic_tank.txt` and `interface/tank_designer_view.gui`.

## Outcome

The blocker was ordering, and it was resolved as recommended: an OOB-local `instant_effect` runs after that OOB's own version-sensitive requests, so the bootstrap moved into country history immediately before `set_oob`.

Two rules were discovered during runtime testing and were not in the original plan:

1. `producer` on a stockpile or production request and `creator` on a forced variant both name the tag whose designer must already hold the variant. Those chassis technologies belong in *that* tag's bootstrap, not the loading country's. This is what made FRA, ENG, and the `CAP`/`CUM` manufacturer bloc tags fail.
2. Bootstrap technology sets are scoped per bookmark, so a 1949 site never preloads a chassis its country only sells in 1980.

`CAP` and `CUM` never load an OOB, so they call the creator directly from their own history.

`RAJ_1980_nsb` requested a `light_tank_chassis_3` variant named `AMX-13/75`; that name exists only as a legacy `lt_equipment_3` variant in FRA's history and no bootstrap creates it, so those six requests now use the generic `Standard Light Tank 1950`.

Four owned NSB OOBs also failed to parse and silently dropped content. `IRQ_1980_nsb` and `PER_1980_nsb` were missing the `=` in `marine { ... }`; `CUB_1980_nsb` and `NOR_1980_nsb` had an uncommented section label inside `units = { ... }`.

### Verified runtime results

Full 35-DLC `-debug -ai_testing` runs of both bookmarks report zero tank variant lookup failures and zero doctrine, enum, or variant-creator errors. Remaining `does not have any equipment variant` entries belong to unrelated systems: legacy infantry and artillery equipment, MTG naval hulls, jet and transport aircraft, and the legacy `lt_`/`mbt_`/`ht_` equipment sold by the weapon-purchasing decisions.

`-ai_testing` starts the default bookmark and does not accept a start-date argument. `-starting_date` is not a command-line flag; the string in the binary is a playthrough-stats key. The 1980 runs were produced by temporarily dating the gathering-storm bookmark to `1980.1.1.12`, and that edit was reverted.

Under memory pressure the harness kills a tracked background game process during load. Launching detached (`setsid nohup ... &`) and watching the log separately avoids this.

### Still needing a manual pass

- Designer UI at multiple resolutions and UI scales.
- Save/load and multiplayer synchronization.
- Doctrine tab population, a full player branch unlock through the XP/mastery flow, and AI branch advancement.

## Runtime environment and commands

Installed game:

```text
/home/zom/.local/share/Steam/steamapps/common/Hearts of Iron IV
```

Full runtime command, from the game directory:

```bash
./run_hoi4 -mod=mod/Cold_War_Iron_Curtain.mod -debug -ai_testing
```

Runtime logs:

```text
/home/zom/.local/share/Paradox Interactive/Hearts of Iron IV/logs/
```

Search `error.log` for regressions with:

```bash
rg -n -i 'does not have any equipment variant.*(light|medium|heavy)_tank|selecting latest version.*(light|medium|heavy)_tank|multiple potential grid boxes|unexpected token: defence|unknown category.*air_doctrine|equipment_database\.cpp:656|CWIC_tank_designer_effects' error.log
```

Always terminate the running game before editing or relaunching.

## Validation sequence

Run after each meaningful change:

```bash
python3 tools/validate_military_reworks.py
python3 tools/loc_audit.py --check
git diff --check
```

`git diff --check` reports the added lines in `GRE - Greece.txt` as trailing whitespace. That file is CRLF in the index, and the inserted block matches it; the report is expected.

## Do not touch these unrelated user files

These were already untracked before this task and must not be staged, edited, or deleted:

- `CWIC Backup/documentation/Indochina_AFK_Playtest.md`
- `CWIC Backup/tools/indochina_event_pictures/`
- root `HANDOFF.md` (the existing Indochina handoff)
- root `error.log`
- root `error_1.log`
- root `error_2.log`
- root `game.log`

## Useful inspection points

- Shared variant creator: `Cold War Iron Curtain/common/scripted_effects/CWIC_tank_designer_effects.txt`
- Representative bootstrap site: `Cold War Iron Curtain/history/countries/USA - United States.txt`
- Cross-country foreign variant requests: `Cold War Iron Curtain/history/units/SOV_1949_nsb.txt`
- Foreign `creator` requests that drove the second fix: `Cold War Iron Curtain/history/units/RAJ_1980_nsb.txt`, `PER_1980_nsb.txt`, `GRE_1980_nsb.txt`
- Manufacturer bloc tags with no OOB: `Cold War Iron Curtain/history/countries/CAP - WP Western Manufacturers.txt`, `CUM - WP Communist Manufacturers.txt`
- Technology/type unlock mapping: `Cold War Iron Curtain/common/technologies/NSB_armor.txt`
- Regression validator and authoritative 30-type maps: `tools/validate_military_reworks.py`

The bootstrap is generated, not hand-maintained. If OOB tank references change, recompute the per-country technology sets from the OOB `producer`/`creator` attributions rather than editing individual history files; the validator enforces that the two stay in sync.
