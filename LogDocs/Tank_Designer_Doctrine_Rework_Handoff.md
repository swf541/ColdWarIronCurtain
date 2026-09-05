# Tank Designer and Doctrine Rework Handoff

## Start here

- Repository: `/home/zom/Projects/ColdWarIronCurtain`
- Branch: `tank-designer-and-doctrine-rework-test`
- Base: `development-branch` at `4a999ae3f3`
- Current HEAD: `38e6ec8e02`
- Date of handoff: 2026-09-04
- Goal: bugfix, sanitize, complete, and polish the Tank Designer and Doctrine reworks without merging into `development-branch`.
- Status: script work complete and verified at runtime on both bookmarks. The interactive designer UI pass is **partly done and was stopped mid-way**; see `## Designer UI pass` for exactly where it got to and what is left.

Read these investigations before making broad design changes:

- `LogDocs/Doctrine_Rework/Doctrine_Rework_Investigation.md`
- `LogDocs/Tank_Designer_Rework_Audit.md`

Do not restart the completed audit work. Continue from the commits below; the remaining work is the unfinished half of the designer UI pass.

## Committed checkpoints

1. `f71dd22ba0 Document doctrine and tank designer audits`
2. `7b50137918 Restore and complete legacy doctrine rework`
3. `ff036b399b Finish tank designer integration and role cleanup`
4. `6e13668058 Complete NSB bookmark tank variants`
5. `2f4d7c6dc4 Add military rework regression validation and outcomes`
6. `38e6ec8e02 Fix designer module clipping and two blank doctrine icons`

Commits 1-5 were pushed to `origin/tank-designer-and-doctrine-rework-test`. Commit `38e6ec8e02` is committed locally but **not pushed** — the user handles pushing from here on. Do not push without asking.

Commit messages on this branch carry no `Co-Authored-By` or `Claude-Session` trailer, and must not gain one.

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

- Designer UI at UI-scale extremes and at a second resolution — partly done, see `## Designer UI pass`.
- Save/load and multiplayer synchronization.
- Doctrine tab population, a full player branch unlock through the XP/mastery flow, and AI branch advancement.

## Designer UI pass

Stopped part-way on 2026-09-04. Everything below was observed in a live 1949 USA campaign at 3840x2160 with UI scaling 1.0x.

### Done and confirmed in-game

- The designer opens and works. Route: Production tab -> the armor `+` (second add-line button) -> a chassis row such as `Late WW2 Light Tank Hull` -> the yellow warning button on that row.
- **All 15 module slots are present, correctly positioned, and clickable.** Seven across the top row, seven across the bottom row, and one on the right-hand side of the blueprint area. Each opens its module category picker and shows a correct `Module Slot` tooltip.
- The seventh top-row slot rendered as a plain grey plate rather than a `+`. **This was a real defect and is now fixed** — see the correction below.
- The USA production list is populated with the bootstrap variants (`Standard Light Tank 1944`, `Standard Main Battle Tank 1942`, `Standard Heavy SPG 1942`, and so on), which is direct visual confirmation of the variant work.
- Opening the Production tab in a fresh game does **not** crash. See the crash note below.

### Fixed as a result of the pass

- `equipment_modules` was 512 wide while the seventh module column starts at x=439 with a 76-wide slot frame, so slots 6, 13 and 14 were clipped by 3px. `containerWindowType` clips by default (vanilla has 866 explicit `clipping = no` against 87 `clipping = yes`), and vanilla never uses the seventh column. Widened to 515; the next sibling starts at x=538. Verified in-game afterwards: the bottom row's seventh slot draws complete.
- `GFX_mobile_warfare_medium` and `GFX_convoy_escorts_medium` pointed at textures present in neither the mod nor the base game, so both doctrine icons rendered blank and logged a missing-texture error every run. Repointed at the placeholder the base game already uses for these two entries.

### Correction to an earlier reading of that grey plate

The pass originally recorded the seventh top-row slot's grey plate as the harmless resting sprite of an empty special slot, on the grounds that it still hovered and clicked correctly. That was wrong, and the note said not to fix it. The real cause: `tag_icon_bg` (the role selector's `GFX_role_icon_bg`, 52x52 in this mod) sat at panel `(465,143)`, and the seventh top-row slot occupies panel `x 452..528, y 147..194`. The icon covered the middle 52px of that slot over its full height. It is `alwaystransparent = yes`, which is exactly why clicks passed through and the slot appeared to work — the evidence that looked exculpatory was the tell.

The role selector and its `niche_button` were moved down to `y=212/219`. They now sit over the upper right of the blueprint preview instead, clear of both the top row and the fifteenth slot at container `(439,150)`.

Lesson for the next session: on this panel, "it still responds to clicks" does not rule out an overlay, because most decorative icons here are `alwaystransparent`.

### Not finished

1. **UI-scale extremes.** UI scaling was raised to its maximum, 2.4x at 3840x2160, but HOI4 requires a restart to apply it, and the restart was not done. `settings.txt` has been restored to the user's original 3840x2160 / 1.4x, so the next session must set it again.
2. **A second resolution.** The audit asks for 1920x1080 and 2560x1440. Neither was exercised. The resolution dropdown was being stepped down to 1920x1080 when work stopped.
3. **The blueprint area now carries two overlays.** The fifteenth module slot sits at container `(439,150)` and the role selector now sits at panel `(465,212)`; both are drawn over `equipment_preview` (container x 3..511, y 50..298). Neither overlaps the other or the module rows, and at 1.0x the blueprint tank is drawn far enough left that both are clear of it. **This still needs a judgement call at other scales and for wider chassis art** — if either covers the tank, move it or shrink the preview.
4. **The land doctrine tree has never been looked at in-game.** It was switched to a classic tech tree this session (see below) and the layout is entirely unverified.
5. **The ammunition fix has not been seen in-game.** Confirm a starting tank now shows non-zero soft/hard attack and piercing in the designer; before the fix the designer read `0.0` for all three.

### How to run the interactive pass

The pointer and screenshot rig used here is worth reusing.

- `tools/hyprland_uimouse.py` is a small `/dev/uinput` relative mouse with `hyprctl cursorpos` feedback (`goto X Y`, `click X Y`). `/dev/uinput` is writable by ACL. The compositor swallows small deltas and scales the rest to about 0.30x, so requested moves are pre-multiplied by 3.4 with a minimum step of 4; without that the pointer never converges.
- **HOI4 confines the pointer to a 2560x1440 region while rendering at 3840x2160.** Screen coordinates seen in a `grim` screenshot must be divided by 1.5 to get pointer coordinates. Get this wrong and clicks land on whatever is behind the game.
- `grim -o DP-1` captures the 4K output; crop with `magick` and read the PNG back.
- `wtype` reaches the game (Escape works), but **the debug console could not be opened** — grave, asciitilde, section, degree, F11 and F12 were all tried. Everything had to be done with the mouse. If a future session finds the console key, `tag USA` removes most of the menu navigation.
- HOI4 rewrites `size=` in `settings.txt` at startup to match the monitor, so the resolution must be changed from the in-game menu (hamburger, top right) -> `Game Options` -> `Video`, not from the file.
- A country intro popup blocks Escape until dismissed with its `Oh, say can you see...!` button.
- The game's own tooltip mentions `Tab + Click to switch to this country` in debug builds. Untested, but it may be a cheaper way to reach a country with tank technology than restarting.

### Crash note, resolved

Loading the pre-branch save `ENG_1951_08_07_01.hoi4` and opening the Production tab produced an immediate SIGSEGV (`crashes/hoi4_20260904_181831`, stripped stack). A fresh 1949 campaign opens Production fine, so this is old-save incompatibility, not a live defect — expected, because earlier commits on this branch removed tank roles and their generated enums. **Treat this branch as save-incompatible with pre-branch saves** and do not test it with them.

## Tank ammunition and the land doctrine tree

Two further changes landed after the UI pass.

### Tank guns produced no attack

Every conventional-gun tank design left `special_type_slot_1` and `special_type_slot_2` empty. In NSB a tank gun's soft, hard and piercing attack come from its ammunition modules, so all 27 gun variants and every AI recipe fielded tanks with **zero attack**. The designer screenshot taken during the UI pass shows `Soft attack: 0.0`, `Hard attack: 0.0`, `Piercing: 0.0` — the symptom was on screen and was not recognised at the time.

- The 27 gun variants in `cwic_create_starting_tank_variants` now carry `ap_0p` and `tank_he_0p`. The three SPAA variants correctly do not: AA guns supply their own attack.
- The AI recipes now request `tank_ammo_kinetic` and `tank_ammo_he`, and their `enable` blocks gate on `has_tech = nsb_ammo` and `has_tech = nsb_he_ammo0` so the AI cannot pick a design it cannot build.
- The validator enforces both. It decides which guns need ammunition by looking for `soft_attack`/`hard_attack`/`ap_attack` in the module's `multiply_stats`, so AA and flame modules are exempt automatically rather than by name.

### Land doctrine moved to a classic tech tree

`old_land_doctrine_folder` changed from `doctrine = yes` to `doctrine = no`, and `countrytechtreeview.gui` gained a folder container of about 3,175 lines.

The layout is a bloc x decade grid: bloc columns at `x = 80 + 480n`, decade rows at `y = 172, 790, 1420, 2050, 2680, 3310`, one `<tech>_tree` anchor plus a title and description textbox per cell, 78 cells in total.

Verified statically:

- All 78 anchors resolve to real technologies, and all 528 land doctrine technologies are reachable from an anchor through `leads_to_tech`.
- All 156 title/description localisation keys exist in English.
- All sprites referenced by the block are defined.

**How this file works, because it is easy to misread.** A `<tech>_tree` `containerWindowType` is a *branch anchor* placed at an absolute pixel position; the technologies below it are auto-placed from their own `folder = { position = { x y } }`, which are small grid units *relative to that anchor*. That is why 476 technologies share only 7 distinct coordinates — `(0,0)`, `(-2,2)`, `(2,2)`, `(-2,4)`, `(2,4)`, `(0,6)`, `(-3,6)` — and it is correct, not a collision. Vanilla does the same: `infantry_folder` has 9 anchors for 67 technologies. Do not "fix" the shared coordinates and do not add an anchor per technology.

`old_naval_doctrine_folder` and `old_air_doctrine_folder` remain `doctrine = yes` with no GUI container, so land doctrine is now the odd one out. That is deliberate: the doctrine grid view has no room for 17 blocs across six decades.

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
- Pointer rig for interactive UI testing: `tools/hyprland_uimouse.py` (QA only, not mod content; drop it if unwanted)

The bootstrap is generated, not hand-maintained. If OOB tank references change, recompute the per-country technology sets from the OOB `producer`/`creator` attributions rather than editing individual history files; the validator enforces that the two stay in sync.
