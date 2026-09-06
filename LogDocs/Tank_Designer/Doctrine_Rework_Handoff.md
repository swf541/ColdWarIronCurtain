# Tank Designer and Doctrine Rework Handoff

## Start here

- Repository: `/home/zom/Projects/ColdWarIronCurtain`
- Branch: `tank-designer-and-doctrine-rework-test`
- Base: `development-branch` at `4a999ae3f3`
- Current HEAD: `38e6ec8e02`
- Date of handoff: 2026-09-04 (balance sources appended same day)
- Goal: bugfix, sanitize, complete, and polish the Tank Designer and Doctrine reworks without merging into `development-branch`.
- Status: script work complete and verified at runtime on both bookmarks. The interactive designer UI pass is **partly done and was stopped mid-way**; see `## Designer UI pass` for exactly where it got to and what is left.

Read these investigations before making broad design changes:

- `LogDocs/Doctrine_Rework/Doctrine_Rework_Investigation.md`
- `LogDocs/Tank_Designer_Rework_Audit.md`
- `LogDocs/Tank_Designer_Balance_Sources.md`

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
4. **The land doctrine tab has never been looked at in-game.** It should return with the revert described below, but nobody has confirmed the 78-cell layout actually reads well.
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

## Tank ammunition and the doctrine tabs

Two further changes landed after the UI pass.

### Tank guns produced no attack

Every conventional-gun tank design left `special_type_slot_1` and `special_type_slot_2` empty. In NSB a tank gun's soft, hard and piercing attack come from its ammunition modules, so all 27 gun variants and every AI recipe fielded tanks with **zero attack**. The designer screenshot taken during the UI pass shows `Soft attack: 0.0`, `Hard attack: 0.0`, `Piercing: 0.0` — the symptom was on screen and was not recognised at the time.

- The 27 gun variants in `cwic_create_starting_tank_variants` now carry `ap_0p` and `tank_he_0p`. The three SPAA variants correctly do not: AA guns supply their own attack.
- The AI recipes now request `tank_ammo_kinetic` and `tank_ammo_he`, and their `enable` blocks gate on `has_tech = nsb_ammo` and `has_tech = nsb_he_ammo0` so the AI cannot pick a design it cannot build.
- The validator enforces both. It decides which guns need ammunition by looking for `soft_attack`/`hard_attack`/`ap_attack` in the module's `multiply_stats`, so AA and flame modules are exempt automatically rather than by name.

### Doctrines: why none of them appeared, and what is staged now

**Symptom.** No land, naval or air doctrine is reachable anywhere. The only thing visible is a special-forces doctrine box that does nothing when clicked. Verified in-game: the research ledger has no doctrine tab at all, and the Officer Corps window does not open.

**The commit that did it** is `b3d3a53c48` "I love doctrines" (Canthonk, 2025-12-07). It renamed the three doctrine technology folders:

- `land_doctrine_folder` -> `old_land_doctrine_folder`
- `naval_doctrine_folder` -> `old_naval_doctrine_folder`
- `air_doctrine_folder` -> `old_air_doctrine_folder`

and added `special_forces_doctrine_folder`. It updated `countrydoctrinetreeview.gui` to match but nothing else, so every other consumer of those names went stale. The one folder it did **not** rename, `special_forces_doctrine_folder`, is the one box still visible — a clean natural experiment. That box does nothing because no technology anywhere is assigned to that folder.

**The deeper problem is that the legacy path is dead on this engine version.** Vanilla 1.19 declares `land_doctrine_folder`, `naval_doctrine_folder`, `air_doctrine_folder` and `special_forces_doctrine_folder` with `doctrine = yes`, and assigns **zero technologies to any of them**. Paradox moved doctrines to the grand-doctrine system under `common/doctrines/`, which this mod deliberately keeps switched off through zero-byte overrides. So a `doctrine = yes` folder routes to a UI the mod has gutted, and nothing can render no matter how the names line up. Renaming the Officer Corps `X_doctrine_button` containers to match the folders was tried and did not help.

**What is staged instead: treat them as ordinary technology folders.** `xp_research_type` and `xp_unlock_cost` do not depend on the doctrine flag — vanilla's MTG naval technologies use XP unlocks inside ordinary tech-tree folders — so the doctrine feel survives the move.

A technology folder needs **four** pieces to render, and a folder missing any one of them draws nothing **and logs no error**:

1. `doctrine = no` in `common/technology_tags/00_technology.txt`
2. a `<folder>` `containerWindowType` in `interface/countrytechtreeview.gui`
3. a `<folder>_tab` button inside that file's `folder_tabs`
4. `techtree_<folder>_item` **and** `techtree_<folder>_small_item` node templates

An earlier attempt supplied only 1-3 for land doctrine and was reverted when it did not work; the missing node template was the reason. All four are now present for all three folders. The folder containers were copied from `countrydoctrinetreeview.gui`, which already held complete layouts (land 78 branch anchors, naval 3, air 3), and the node templates were cloned from `mtgnavalfolder` because that is vanilla's closest analogue: XP-researched technologies in an ordinary folder. Tabs sit at x=410, 650 and 970, the free slots in the strip.

`countryofficercorpview.gui` is back to its committed state; with `doctrine = no` those doctrine buttons are no longer the route in.

**If this still does not work**, the remaining options are, in order of cost: check whether `special_forces_doctrine_folder` should be deleted from `technology_folders` (it has no technologies and only contributes the dead box); or port the 646 doctrine technologies to the grand-doctrine system under `common/doctrines/`, which is the only path vanilla 1.19 actually uses.

### Doctrine icons

Confirmed working: the doctrine folders now appear in the technologies section alongside industry and military, and researching one does not consume a research slot. That last part is correct rather than a bug — these nodes carry `xp_research_type` and `xp_unlock_cost`, so they are XP unlocks, not slot research. Say so if slot consumption is actually wanted.

Icon state before this pass: air 73/73 and naval 45/45 fully illustrated; land 53/528, all of them NATO.

- 27 land nodes already had art sitting in `gfx/interface/doctrines/Technology/` that was never declared in `interface/CWIC_Doctrines.gfx`. Now declared.
- The remaining 448 now declare the base game's 64x64 `doctrine_placeholder.dds`, which matches the art's own 64x64, so the tree reads consistently instead of falling back.

`LogDocs/Doctrine_Rework/Doctrine_Icon_Art_Requests.md` lists all 448 by bloc and decade. To promote one: drop `<technology>.png` into `gfx/interface/doctrines/Technology/` and repoint that entry's `texturefile`. **Do not point an entry at art that does not exist yet** — a missing texture logs an error on every load, which is how the two blank doctrine icons fixed earlier in this branch were found.

The bloc and decade banner art is fine: 78 of 79 PNGs in `gfx/interface/doctrines/` are declared, the odd one out being an unused `Doctrine_Overlay`.

### Land doctrine tree structure is only half-wired

Full analysis in `LogDocs/Doctrine_Rework/Land_Doctrine_Tree_Structure.md`.

The grid in `countrytechtreeview.gui` is the design, not just layout: columns are
blocs, rows are decades, and a column that starts partway down does so because that
doctrine arrives later in Cold War history. Each cell has one root header and one
capstone terminal.

Decade chaining is already implemented, through `allow = { has_tech = ... }` rather
than `path`. **The file writes `allow  = {` with two spaces**, which is why an earlier
pass in this branch reported "no gating at all" — a `grep 'allow = '` misses all 60 of
them. That claim was wrong.

Seven of those gates are cross-bloc and encode real lineage: `sadf` continues `nato`,
`dprk` continues `warsaw`, `cuba` branches off `foco`, and `maoist`, `foco`,
`hybrid_ins` and `islamist_ins` all descend from the `ins` column's 1950s capstone.
So there are 11 independent roots, not 17.

Four gaps, in the order worth fixing:

1. **Gates sit on capstones, never on headers.** This is the reported bug. Gating the
   capstone leaves the header and the rest of that cell freely purchasable, so a
   country with no 1940s progress still buys most of a 1960s cell. Gate the header
   instead — it is the cell's only root, so that locks the whole cell. 61 headers need
   it.
2. **Nothing enforces one bloc.** No exclusivity between the 11 independent roots,
   which is why one country researches NATO and Warsaw side by side. Continuation
   columns inherit exclusivity through their parent's lineage gate.
3. **Eight 1940s-to-1950s gates were never written.** Every column starting in the
   1940s is missing its first transition; the pattern is otherwise complete.
4. **No date gating anywhere.** Not one date condition in the file.

`himalayan` and `iran` start mid-war with no lineage parent, so they are reachable
from turn one. That is a design decision — genuinely independent and date-gated, or
missing a parent — not a mechanical fix.

An earlier commit on this branch, `7b50137918`, removed a cross-decade `path` from
`cw_nato_1950s_tactical_nuclear_fire_planning` as a "duplicate". It was not a
duplicate; it was the one place the vertical intent was expressed as a `path` rather
than an `allow`.

### Caution about verification

A folder that fails to render logs nothing. Several earlier "clean `error.log`" results in this document were taken as evidence that a doctrine change worked; they were not. Only looking at the ledger settles it.

## The Lead Dev balance sources

Two 2023 design artifacts arrived on 2026-09-04 and sit untracked in the repository root:
`2023 - CWIC Tank Rework Balance.xlsx` (module balance master, 15 tabs) and
`Tank_Designer_Slimemix (1).drawio` (design tree, 11 pages). Full analysis in
`LogDocs/Tank_Designer_Balance_Sources.md`.

**They are reference, not backlog.** The workbook's `Total Balance Sheet` tab is the exact
source of the numbers already in `00_tank_modules.txt` and `tank_chassis.txt`: a
field-by-field comparison of all 224 modules the two share found zero real differences,
guns and ammunition included. Nothing on this branch needs its numbers re-entered.

Three things in them that change how the remaining work should be judged:

1. **The `[DONE]` tags in both files are stale and contradict each other.** The workbook
   leaves every gun and ammunition category untagged although those values shipped; the
   diagram marks its guns page `[DONE]` and its armour page not, although both shipped.
   Judge completeness from the mod.
2. **The workbook states target stat envelopes for 41 finished vehicle generations**
   (Light Tank I-VI, WWII Tank 1-2, MBT I-VIII, Heavy Tank I-V, Light/Heavy Mech I-VIII),
   giving hard, soft, breakthrough, defence, armor, piercing, speed, fuel and cost per
   generation. Nothing in the repository checks bootstrap variants or the 125 AI recipes
   against those targets. `tools/validate_military_reworks.py` is the natural home for
   that check, and it is now writable because the targets exist on paper.
3. **The scope the sources define but the mod never built** is larger than anything left on
   this branch: the artillery and AA designer ladders (page 6, still legacy five-step
   equipment techs in `common/technologies/artillery.txt`), the page 2 special modules
   (blow-out panels, unmanned compartment, dozer and mine plows, RWS, external fuel, log,
   amphibious drive), the night and thermal vision line, the mechanized APC/IFV ladder, and
   trucks/amphibious. Treat all of that as post-branch scope; **this branch is a bugfix and
   completion pass, not the place to start it.**

When two workbook tabs disagree, `Total Balance Sheet` wins - the `(DONE) ...` tabs are
earlier drafts and the `Gun Modules` tab is a rough draft with mixed decimal conventions.

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
- root `2023 - CWIC Tank Rework Balance.xlsx`
- root `Tank_Designer_Slimemix (1).drawio`

## Useful inspection points

- Shared variant creator: `Cold War Iron Curtain/common/scripted_effects/CWIC_tank_designer_effects.txt`
- Representative bootstrap site: `Cold War Iron Curtain/history/countries/USA - United States.txt`
- Cross-country foreign variant requests: `Cold War Iron Curtain/history/units/SOV_1949_nsb.txt`
- Foreign `creator` requests that drove the second fix: `Cold War Iron Curtain/history/units/RAJ_1980_nsb.txt`, `PER_1980_nsb.txt`, `GRE_1980_nsb.txt`
- Manufacturer bloc tags with no OOB: `Cold War Iron Curtain/history/countries/CAP - WP Western Manufacturers.txt`, `CUM - WP Communist Manufacturers.txt`
- Technology/type unlock mapping: `Cold War Iron Curtain/common/technologies/NSB_armor.txt`
- Regression validator and authoritative 30-type maps: `tools/validate_military_reworks.py`
- Balance provenance for every module and chassis number: `LogDocs/Tank_Designer_Balance_Sources.md`
- Pointer rig for interactive UI testing: `tools/hyprland_uimouse.py` (QA only, not mod content; drop it if unwanted)

The bootstrap is generated, not hand-maintained. If OOB tank references change, recompute the per-country technology sets from the OOB `producer`/`creator` attributions rather than editing individual history files; the validator enforces that the two stay in sync.

### Doctrine completion correction (2026-09-05)

The doctrine progression pass is implemented in the retained legacy technology trees.
The reviewed manifest covers 78 land cells and 528 nodes: 67 header lineage gates, 70
inclusive decade gates, and 11 independent roots. The apparent 13-node regional
Islamist cell and singleton alternative are prefix-grouping artifacts; the alternative
header owns seven existing `cw_islamist_ins_1990s_*` nodes.

The prior 60 terminal gates were replaced by header gates using each graph cell's
actual terminal, including Foco's terminal for Cuba. The alternative Islamist terminal
no longer requires regional Islamist ownership or `X_TESt`. Air retains its three root
exclusions and five reciprocal internal pairs; naval now has symmetric exclusions on
its three roots. `tools/validate_military_reworks.py --doctrine-self-test` covers the
balanced parser and negative graph/allow mutations. Static validation passes; fresh
game, UI, AI, save/load, and multiplayer acceptance remain to be exercised.
