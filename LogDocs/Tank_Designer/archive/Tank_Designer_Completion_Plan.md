# Finish the CWIC Tank Designer

Status: **draft by Claude Opus 5, 2026-09-05, for GPT 6 Astra to finalize and polish.**
Verified against branch `tank-designer-and-doctrine-rework-test`, HEAD `034c4d0b70` and its
working tree. Every claim below was checked against the tree or a live runtime log this
session; where a prior CWIC document disagrees, this document is the corrected version and
says so explicitly.

Intended destination once approved: `Tank_Designer_Completion_Plan.md` at repository root,
beside the existing `Doctrine_Rework_Plan.md`.

---

## Context

The Tank Designer rework replaced CWIC's legacy armor equipment ladder with a No Step Back
style module designer: 3 chassis archetypes, 12 role duplicates, 25 derived hulls, 242
modules, 169 technologies, 125 AI design recipes and 30 bookmark variant bootstraps. The
integration landed in a compressed 2026 sequence on top of scaffolding dating back to 2023.

Two prior documents assess it. `LogDocs/Tank_Designer_Rework_Audit.md` (2026-09-03) found
five P0 integration failures; `LogDocs/Tank_Designer_Doctrine_Rework_Handoff.md` records
what was then fixed and stops mid-way through an interactive UI pass. Since those were
written, most of the P0/P1 backlog has actually been closed - but nobody has re-audited, so
the open items are buried in stale findings, and at least one genuine content-breaking
defect has never been reported at all.

This plan establishes the true remaining scope and sequences it against a hard deadline and
against a parallel doctrine effort that is mid-flight on the same branch.

**Intended outcome.** Every declared tank designer role is buildable, no module or chassis
reference dangles, the armament layer is balanced rather than stubbed, and the designer's
remaining UI and validation debt is either closed or explicitly deferred with a reason.

---

## Scope decisions (made by the repository owner, 2026-09-05)

1. **Branch-flagged work only.** Out of scope, permanently, for this pass: artillery and AA
   *designer* ladders replacing the legacy equipment techs; the mechanized APC/IFV designer
   ladder; the night/thermal vision line; and the 2023 diagram's "page 2" specials (RWS,
   dozer/mine plows, blow-out panels, unmanned turret, underwater driving, external fuel
   tanks, modular construction, NBC). These are real designed scope - see
   `LogDocs/Tank_Designer_Balance_Sources.md` - but they are a multi-week project.
2. **Tiered delivery.** Tier 1 is a genuinely completable one-day push. Tiers 2 and 3 are
   explicitly deferred with rationale. The owner cuts the line wherever they like.
3. **Armament depth: balance what exists PLUS a secondary armament layer.** This is a
   deliberate override of the drafting agent's recommendation to defer secondary armament
   entirely. It is honoured here, placed in Tier 2, with its cost stated honestly in
   *Edge cases* below.
4. **Sequencing: work alongside the doctrine effort, avoiding shared files.** Tier 1 adds
   **zero** lines to `tools/validate_military_reworks.py` and touches **zero** lines of
   `interface/countrytechtreeview.gui`.

---

## Ground truth: the state of the world

Do not re-derive these. They were checked this session.

**The validator passes today.** `python3 tools/validate_military_reworks.py` exits 0:

> Military rework validation passed: 1933 technologies, 242 tank modules, 125 historical
> tank designs, 30 bookmark variants and 460 named OOB requests across 68 NSB OOBs, 76
> country-history bootstrap sites, and 15 designer slots checked.

**Healthy layers - do not spend time here.**

- All 242 modules are granted by a technology. Zero orphans, zero dangling grants.
  (103 from `NSB_armor.txt`, 139 from `NSB_armor_modules.txt`, exactly disjoint.)
- All 242 modules and all 40 chassis ids have an English name *and* `_desc`. Zero missing.
- All 169 NSB technologies have name and `_desc`. Zero missing.
- Module icons are complete: 429 `GFX_SMI_*` sprites declared, and all 344 `texturefile`
  paths in `interface/cwic_tank_rework_icons.gfx` resolve on disk. (Case-sensitivity is a
  recurring CWIC failure mode; this file is clean.)
- The 125 AI recipes cover the full contract - light 0-9, medium 0-9, heavy 0-4 x {plain,
  aa, artillery, destroyer, flame} = 125, with 125 `history = yes`.
- All five removed roles (rocket, amphibious-designer, modern-designer,
  super-heavy-designer, medium-heavy-artillery) are cleanly gone from script.

**Prior audit findings that are now FIXED** - the audit text is stale, do not act on it:

- NSB tech categories. The audit says 168 of 169 techs are mistagged
  `infantry_vehicles_apc`. They are now `vehicles` + `armor` + the correct
  `armor_light`/`armor_medium`/`armor_heavy` tag.
- BRA's invalid `light_tank_chassis` technology category - gone from `BRA_50s.txt`.
- Armored engineers. `common/technologies/support.txt` now OR-gates all seven sites:
  `allow = { OR = { has_tech = main_battle_tanks  has_tech = nsb_main_battle_tanks0 } }`.
- Marine mechanized - safe by construction, the chain hangs off `amphibious1`, which is
  dual-foldered into both `armour_folder` and `nsb_armor_folder`.
- `date > 1944.1.1` AI spam - down from 87 occurrences to 9.
- The five modules the audit says lack a `GFX_SMI_` sprite all have one.
- `light_tank_artillery_chassis` no longer duplicates `medium_tank_chassis`.

**Log hygiene.** The root `error.log` / `error_1.log` / `error_2.log` / `game.log` are
stale (2026-09-02, pre-branch-work) and are protected user files - do not read them as
current evidence and do not touch them. The live log is
`~/.local/share/Paradox Interactive/Hearts of Iron IV/logs/error.log`.

The ~255 `Entity referenced in equipment graphic database does not exist` and
`Unknown equipment type: modern_tank_chassis / super_heavy_tank_chassis` lines in the live
log come from the **base game's** graphics database referencing equipment types this mod
deliberately removed. Nothing in `Cold War Iron Curtain/` references them (grep confirms
zero hits). These are engine-side and ignorable - consistent with the project's earlier
`error(4).log` triage. Do not chase them.

---

## Tier 1 - Day-1 must-ship

All script-only. No shared-file collisions with the doctrine working tree. Execute in
order; a single validator run and a single runtime run gate the whole tier.

### T1.1 - Revive the flame tank role (P0, previously unreported)

**This is the highest-value fix in the plan and appears in no prior document.**

The flame role is wired everywhere except the two places that make it exist:

- `common/technologies/NSB_armor.txt` `nsb_iw_armored_vehicles` grants 12 chassis at
  L24-38 - light/medium/heavy x {base, destroyer, artillery, aa} - and **no flame chassis**.
  A grep for `flame_chassis` across all of `common/technologies/` returns **zero hits**,
  while `light_tank_aa_chassis_0` and its siblings are granted normally.
- All three flame subunits carry `active = no` in
  `common/units/equipment/../../units/need_for_tank_roles.txt` (`light_flame_tank` L223,
  `medium_flame_tank` L310, `heavy_flame_tank` L399). **Every other tank subunit in that
  file is `active = yes`** - the three armor, three tank-destroyer, three SP artillery and
  three SP anti-air brigades.

Meanwhile the role is fully built out: 3 chassis duplicates in `x_tank_chassis.txt`
(L35, L70, L106) with `type = { armor flame }`; the `flamethrower` module with the file's
only `can_convert_from`; `enable_subunits` already listing all three; `script_enums.txt`
entries; 18 designer GUI files; and 25 AI recipes covering exactly light 0-9, medium 0-9,
heavy 0-4 - a perfect match for the chassis contract.

Net effect today: 3 unbuildable battalion types, 25 dead AI recipes, one unusable module.

**Edit A.** `common/technologies/NSB_armor.txt` - add 25 flame chassis ids across 23
technologies. The grant pattern is mechanical and already consistent:
`nsb_iw_armored_vehicles` grants tier 0 for all three families (9 role chassis + 3 base),
then each of 22 ladder techs - `nsb_light_tanks0..8` (9), `nsb_main_battle_tanks0..8` (9),
`nsb_heavy_tanks0..3` (4) - grants exactly 3 role chassis at its tier. Add
`<family>_tank_flame_chassis_<N>` alongside each existing
`<family>_tank_destroyer_chassis_<N>`.

Total: **3** ids into `nsb_iw_armored_vehicles`, **1** id into each of the **22** ladder
techs = 25 ids, matching the 25 AI flame recipes exactly (light 0-9, medium 0-9,
heavy 0-4 - confirmed by grep against `generic_tank.txt`).

**Edit B.** `common/units/need_for_tank_roles.txt` - flip `active = no` to `active = yes`
on the three flame subunits.

**The one judgement call in Tier 1.** `active = no` may be a deliberate parking of the
role rather than an oversight. Two readings:

- *Left half-wired* (the weight of evidence): 25 AI recipes, 3 chassis duplicates, 18 GUI
  files, a bespoke `can_convert_from`, and script_enums entries all exist. Nobody builds
  that much for a role they intend to disable.
- *Deliberately parked*: the project has precedent - `mechanized_marine` carries
  `active = no` and the validator **asserts** it stays that way.

Confirm with the owner before flipping Edit B. Edit A is correct either way: even a parked
role should not have a chassis contract that no technology can satisfy.

**Risk: low.** Flame tanks are `group = support` with `priority = 0`, `ai_priority = 0` -
support companies, exactly as in vanilla NSB. Support companies never appear in bookmark
variants or OOB battalion lists, and a repo-wide grep confirms **zero** references to
`flame_chassis` / `flame_equipment` anywhere under `history/`. So this needs no bookmark
variant, no change to `cwic_create_starting_tank_variants`, and no OOB edits. The 30-entry
variant map stays at 30 and the validator's counts are unaffected.

**Known residual.** No AI division template fields a flame battalion (`grep flame_tank
common/ai_templates/` is empty), so the AI still will not build them without a template
change. That is a follow-up, not a blocker - the player gets the role back immediately.

**Verify.** `grep -c flame_chassis "Cold War Iron Curtain/common/technologies/NSB_armor.txt"`
returns 25. In-game, the Flame role appears in the designer's role dropdown and a flame
support company can be added to a template. **Do T1.5 first** - adding a role is exactly
the growth that overflows the dropdown.

### T1.2 - Fix two module parents that name nonexistent modules (P0)

Live log, confirmed today:

```
Declared parent "tank_diesel_engine" of module "Diesel_0" is not a valid module.
Declared parent "tank_gas_turbine_engine" of module "GT_0" is not a valid module.
```

`00_tank_modules.txt` L3371 (`Diesel_0`) and L3657 (`GT_0`).

**Correction to the drafting agent, which matters.** The agent proposed also retiring
`tank_gasoline_engine` as a redundant stub duplicating `Petrol_0..3`. **That is wrong.**
`Petrol_0` declares `parent = tank_gasoline_engine`, so `tank_gasoline_engine` is the
deliberate 1939 root of the gasoline line, not a stray. The real defect is *asymmetry*: the
design clearly intended three engine-family root modules and only the gasoline one was ever
created, leaving the diesel and gas-turbine lines pointing at ghosts.

Two coherent fixes; take the first:

- **Delete the two `parent` lines.** `Diesel_0` and `GT_0` become their own roots. One-line
  change each, zero stat impact, clears both errors.
- Create `tank_diesel_engine` and `tank_gas_turbine_engine` root modules mirroring
  `tank_gasoline_engine`. Restores the intended symmetry but adds two modules that need
  tech grants, loc, icons and balance - Tier 2 work at best.

Do **not** repoint them at `tank_gasoline_engine`; that would put diesel and turbine
engines downstream of a petrol engine.

**Verify.** Relaunch; `grep "not a valid module"` on the live error.log returns nothing.

### T1.3 - Make the super-heavy gun equippable (P0)

`tank_super_heavy_cannon` (`00_tank_modules.txt` L4961) has
`category = tank_super_heavy_main_armament`. No `main_armament_slot` on any of the three
archetypes lists that category, so the module can never be equipped - yet tech
`nsb_superheavy_guns1` grants it and a `leads_to_tech` path points at it.

**Fix: recategorize to `tank_heavy_main_armament`** (one line). Do **not** add
`tank_super_heavy_main_armament` to the heavy hull's slot list - that leaves a
one-module category and a second name for the same concept, and `super_heavy_tank_chassis`
is in the validator's `UNSUPPORTED_IDS`, i.e. the mod has deliberately dropped super-heavy
hulls entirely.

The stats support the move: `+8 IC`, `-1.2 max speed`, `-0.4 reliability`, `+0.35 ap` reads
as a heavy-hull siege gun, not a Maus gun. It also carries
`allow_equipment_type = anti_tank`, so it will surface on heavy tank destroyers - coherent,
and self-limiting via the reliability and speed penalties. No AI recipe will pick it up
unasked, because AI recipes name modules explicitly.

Update the loc *text* if it reads "super-heavy" misleadingly; keep the loc *key* id.

### T1.4 - Purge dangling module count limits (P1, safe)

`common/units/equipment/tank_chassis.txt`, blocks at L299-419, L741-857, L1179-1296.

- 9 `module_count_limit = { module = X }` entries x 3 archetypes = **27 dead entries**
  naming vanilla NSB modules this mod's replacement file deleted: `sloped_armor`,
  `amphibious_drive`, `wet_ammo_storage`, `squeezebore_adaptor`, `armor_skirts`,
  `dozer_blade`, `easy_maintenance`, `auto_loader`, `stabilizer`.
- 3 `category` limits with zero modules and no slot exposure: `tank_radio_module`,
  `tank_secondary_turret`, `tank_mobility_fuel`.

Delete all of them **except `tank_secondary_turret`**, which Tier 2 will fill - leaving its
limit in place avoids deleting and re-adding the same six lines.

**Risk: none.** A count limit naming a nonexistent module is inert at parse and cannot
appear in any saved design, because no such module can ever be equipped. Existing saves are
unaffected.

**Verify.** Grep the nine ids in `tank_chassis.txt` - empty. Load an existing save; designs
intact.

### T1.5 - Role localisation, and unblock the role dropdown (P1)

Two coupled edits; both are prerequisites for seeing T1.1 work.

**Loc.** The 15 engine role keys (`land_light_tank`, `land_medium_tank_anti_air`, ...
`land_heavy_tank_flame`) are absent from the mod's English localisation, so they fall
through to vanilla strings. Most visibly, the medium roles render "Medium Tank" while the
mod's own `BOOKMARK_VARIANT_NAMES` say "Main Battle Tank". Add all 15 to the file that
already owns designer strings (do not create a new file).

CWIC loc constraints apply: **ASCII only** - no diacritics, em dashes or smart quotes; the
files are read as ANSI and non-ASCII renders as `?`. English only; never touch `french/` or
`japanese/`.

**Dropdown.** `dropdown_tank_roles`'s `expanded_window` in
`interface/tank_designer_view.gui` (container at L984) has a hardcoded height of 608 with
an in-file comment that it "must be large enough to hold the largest possible list". It
silently truncates when the list grows. T1.1 grows the list. Recompute from the post-T1.1
role count with margin.

**Verify.** Screenshot the expanded role dropdown at 1.0x and 2.4x UI scale; confirm every
role including Flame is reachable and reads with CWIC naming.

### Tier 1 gate

1. `python3 tools/validate_military_reworks.py` - must still pass with **unchanged** counts.
   **Do not edit the validator in Tier 1.**
2. One detached runtime run, then diff the live error.log against a pre-change baseline
   captured before any edit:

```bash
cd "/home/zom/.local/share/Steam/steamapps/common/Hearts of Iron IV"
setsid nohup ./run_hoi4 -mod=mod/Cold_War_Iron_Curtain.mod -debug -ai_testing >/dev/null 2>&1 &
```

   Launch detached - the harness kills a tracked background game process under memory
   pressure during load. `-ai_testing` starts the **default bookmark only** and does not
   accept a start-date argument.
3. **Finally confirm the ammunition fix visually.** It has never been seen in-game. Open the
   designer on a starting variant and check soft attack / hard attack / piercing read
   non-zero; before the fix all three read `0.0`.
4. Treat this branch as **save-incompatible with pre-branch saves** - earlier commits
   removed tank roles and their generated enums, and loading an old save into the Production
   tab produced a SIGSEGV. Test with fresh campaigns only.

---

## Tier 2 - after the doctrine diff is committed

### T2.1 - Close the validator gap that hid T1.1

Nothing asserts that every chassis type targeted by an AI recipe is actually granted by some
technology's `enable_equipments`. That is precisely the hole the flame defect fell through,
and it is the single most valuable check to add.

Implement with the bounded Clausewitz parser helpers the doctrine work added at L158-296
(`strip_script_comments`, `balanced_end`, `top_level_ranges`, `strict_top_level_blocks`,
`key_blocks`, `top_level_values`) - and in the same commit **delete** the near-duplicate
`top_level_blocks` / `keyed_blocks` at L1025-1073. The file currently carries two parallel
parser families, which is a live maintenance hazard.

Add alongside: assert every `active = yes/no` on tank subunits matches an explicit expected
map, so a parked role is a deliberate, reviewed statement rather than a silent one.

**Must land strictly after the doctrine commit** - the doctrine effort has +881 uncommitted
lines in this file and any tank edit conflicts hard.

### T2.2 - Balance the armament stubs

The 13 turret and superstructure modules are byte-identical stubs. Every one is exactly:

```
add_stats = { build_cost_ic = 1  reliability = 0.15 }
multiply_stats = { }
dismantle_cost_ic = 2
```

No `xp_cost` (against 228 modules that have one), no `build_cost_resources`. They were never
entered in the 2023 balance workbook - see `LogDocs/Tank_Designer_Balance_Sources.md`, which
establishes that workbook as the authoritative source of every other shipped module number
and confirms all 224 shared modules match it exactly.

Also in scope: the 3 ad-hoc `tank_anti_air_cannon*` modules, which likewise have no workbook
provenance.

**Fix the duplicate abbreviations - this is worse than the turret stubs.** HOI4 uses
`abbreviation` for variant auto-naming, and the module file has **14 colliding
abbreviations covering 60 modules**:

| Abbreviation | Modules | Note |
| --- | --- | --- |
| `tanklightc` | 10 | the entire light gun ladder, all ten tiers |
| `tankrifled` | 6 | entire rifled MBT gun ladder |
| `tanksmooth` | 6 | entire smoothbore MBT gun ladder |
| `computerar`, `ext`, `independen`, `tankheavyc`, `tanklowpca`, `tankmedium` | 4 each | |
| `fix`, `hydropneum`, `panoramics`, `tankmbthea` | 3 each | |
| `artyoptics` | 2 | |

The gun collisions are 10-character truncations of the module id, so every tier of a gun
family yields an identical name fragment - a 1939 light gun and a 2015 light gun both
abbreviate to `tanklightc`. Auto-named variants across the whole armor line are therefore
indistinguishable in the production list. Give each module a short unique abbreviation
encoding tier (e.g. `ltcan0`..`ltcan9`).

**Art is already staged.** `gfx/tank_modules/_Missing from Sheet/Other Modules/Turrets/`
holds 13 PNGs whose names map almost 1:1 onto the existing turret set - `Pintle mount`,
`Light turret`, `Low-profile light turret`, `Low-profile turret`, `Oscillating turret`,
`Open gun placement`, `External gun placement`, `Fixed superstructure` - plus a
`Cast turret` / `Welded turret` pair that is *not* currently modelled and suggests the
intended differentiation axis.

### T2.3 - Secondary armament layer (owner-directed scope)

Fill the declared-but-empty `tank_secondary_turret` category with coaxial/hull machine guns
and secondary autocannons. Art exists: `HMG`, `LMG`, `AGL`,
`Light remotely-controled turret` in `_Missing from Sheet/Other Modules/`, and 7
`_Missing from Sheet/SPAAG/AFV Autocannons/` icons spanning 1960-2020.

**Slot strategy - take option A.**

- **A. Add `tank_secondary_turret` to the `special_type_slot_*` category lists.** All ten
  special slots on all three archetypes carry a byte-identical 17-category list; this makes
  it 18, across 30 blocks. No new slot, no designer GUI change, no change to the validator's
  `pos_custom_module_slot_window_0..14` assertion. The `module_count_limit` for
  `tank_secondary_turret` (`count < 2`) **already exists** in all three archetypes - strong
  evidence this is what the original design intended.
- **B. Add a dedicated 16th slot.** Rejected: the UI defines exactly 15 positions, the
  validator asserts exactly 0-14, and `equipment_modules` has **0px** of slack.

**State the cost honestly.** Option A puts secondary armament in direct competition with
ammunition, FCS and protection packages for the same ten special slots. Every one of the 125
AI recipes currently fills slots 1 and 2 with ammunition and leaves 3-10 empty, so nothing
breaks - but a designer who adds a coaxial MG is trading away a protection or FCS module,
and the 41 vehicle stat envelopes in the workbook were computed without secondary armament.
Re-check a representative design of each family against its envelope before calling this
done.

### T2.4 - Hull upgrades

All 25 derived hulls carry only `upgrades = { tank_engine_upgrade tank_armor_upgrade }`.
`tank_gun_upgrade` and `tank_reliability_upgrade` are defined in
`common/units/equipment/upgrades/land_upgrades.txt` (L2, L30) and used by nothing. Cheap to
add, but it is a real balance lever - decide the numbers together with T2.2.

### T2.5 - NSB technology hygiene

- Three `start_year` / grid-position mismatches in `NSB_armor.txt`: `nsb_light_tanks8`
  (L418), `nsb_main_battle_tanks8` (L780, `start_year = 2020` against `y = @2010`),
  `nsb_heavy_tanks3` (L965, `start_year = 1955` against `y = @1944`). These look like
  leftover duplicated blocks.
- One duplicate grid position `(14, 10)` - two technologies draw on top of each other.
- One off-grid `x = 15` on `nsb_armor` (L1387); every other x is even.
- Three `leads_to_tech` paths whose targets are commented-out placeholders:
  `nsb_light_tanks9` (L452), `nsb_main_battle_tanks9` (L814), `nsb_heavy_tanks4` (L999).
  Remove the paths or implement successors. Note the heavy line stopping at tier 4 (1955)
  is **correct** - the workbook's Heavy Hull line is `Heavy_Hull_0..4` and ends in 1955.
- Flat `research_cost = 2` across all 169 techs with no era scaling.
- **XP economy is a design decision, not a bug.** `xp_research_type` and `xp_unlock_cost`
  have zero matches in both NSB armor files, so modules are free once researched, even
  though 228 modules carry a `xp_cost`. Raise separately with the owner.

### T2.6 - National focus gates that silently no-op under NSB

Three focus sites still hard-gate on legacy-only technologies that are invisible when NSB is
active. They grant licenses and stockpiles, so they fail silently rather than erroring:

- `common/national_focus/60s_Generic.txt` L7033-7037, L7044-7047, L8099-8101, L8109-8111 -
  USA `AND = { main_battle_tanks_3, light_tanks_1, heavy_tanks_2 }`
- `common/national_focus/GRE_military_shared_1950s.txt` L109-113 - USA
  `main_battle_tanks_2` + `light_tanks_3`
- `common/national_focus/50s_FIN.txt` L2252-2254 - SOV `main_battle_tanks_3`

Map each to its NSB equivalent using the same `OR = { has_tech = legacy  has_tech = nsb_* }`
shape already used in `support.txt`. Verify by completing the focus in-game and confirming
the reward actually fires.

### T2.7 - Orphan designer GUI files

24 `*_amphibious.gui` files remain in `interface/equipmentdesigner/tanks/` (128 files total)
for a role with no chassis duplicate, no AI design and no script reference. Delete them -
this matches the precedent of commit `ff036b399b`, which removed 124 unused role files.
Separately, `heavy_tank_aa` has only the generic GUI file while comparable combinations have
5-8 national variants; add them or accept the generic deliberately.

---

## Tier 3 - deferred, with reasons

- **T3.1 - `countrytechtreeview.gui` armour folder repair.** `techtree_armour_folder_item`
  exists (L16483) but there is **no** `techtree_armour_folder_small_item`. By this
  project's own documented four-piece rule, a technology folder missing a node template
  draws nothing *and logs nothing*, so the legacy armour folder may silently fail to render
  for non-NSB players. Also missing: `nsb_armor_modules_small_year_right` and an
  `nsb_armor_modules_tree` gridbox (the `nsb_armor` folder has both), and both NSB tabs
  reuse `GFX_armour_folder_tab` so they are visually identical.
  **Deferred because** this file has 7109 uncommitted lines of doctrine changes. The diff is
  textually disjoint from the armour sections - verified - but editing a file in that state
  invites a painful manual merge. Must land strictly after the doctrine commit. Verify by
  loading a profile without the No Step Back DLC.
- **T3.2 - Remaining designer UI pass.** Never done: 1920x1080 and 2560x1440, at 1.0x and
  2.4x UI scale. Structural items to fix while there: `tag_icon_bg` (465,212) and
  `niche_button` (474,219) are **siblings** of `equipment_modules`, not children, so they do
  not track it and both now overlay `equipment_preview` (3,50, 508x248);
  `equipment_modules` is 515 wide against a 7th column ending at exactly 515, i.e. zero
  slack, so any slot frame wider than 76px re-clips; `designer_intel_container` sits at
  x=1088 inside a 1091-wide root and overflows 317px, relying on root `clipping = no`.
  Note the lesson recorded in the handoff: on this panel *"it still responds to clicks"*
  does not rule out an overlay, because most decorative icons here are `alwaystransparent`.
- **T3.3 - Workbook envelope validation.** Assert shipped designs against the 41 vehicle
  generation stat envelopes recorded in `LogDocs/Tank_Designer_Balance_Sources.md`
  (hard/soft/breakthrough/defence/armor/piercing/speed/fuel/cost per generation). Highest
  long-term value, largest effort, and it should follow T2.2/T2.3 so it validates final
  numbers rather than stubs.

---

## Edge cases and design inconsistencies

Things likely to bite, collected in one place.

1. **`active = no` on the flame subunits may be intentional.** Precedent exists
   (`mechanized_marine`), and the validator asserts that one. Confirm before flipping.
2. **Granting flame chassis does not make the AI build them.** No AI division template
   fields a flame battalion. Player-facing fix lands immediately; AI adoption needs
   `common/ai_templates/` work.
3. **`tank_gasoline_engine` is not a stub.** `Petrol_0` declares it as parent. Deleting it
   would orphan the whole gasoline line. The asymmetry is that diesel and gas-turbine roots
   were never created.
4. **Secondary armament competes for the special slots.** Option A costs a protection or FCS
   choice per secondary weapon, and the workbook envelopes were computed without it.
5. **Two parser families in the validator.** The doctrine work added a bounded parser; the
   tank half still uses older near-duplicates. Do not add a third - reuse and delete.
6. **Turret modules have no `xp_cost`.** Every other module family does. Either the turrets
   are deliberately free or this was missed; decide explicitly in T2.2.
7. **14 abbreviation collisions across 60 modules**, including all ten light gun tiers
   sharing `tanklightc`. Variant auto-naming cannot distinguish a 1939 gun from a 2015 one.
   Cosmetic, but it touches every armor design a player or the AI ever produces.
8. **`main_armament_slot = empty` in `default_modules`** despite `required = yes` on all
   three archetypes. This is why a fresh design opens with no gun. Probably intentional, but
   it is the first thing a player sees.
9. **Legacy orphan archetypes.** `lt_equipment`, `mbt_equipment`, `ht_equipment` are declared
   as archetypes but nothing targets them - their numbered children were repointed at the
   designer chassis. Harmless, confusing.
10. **The artillery tree is entirely NSB-unaware.** 85 techs in an unconditional
    `artillery_folder` granting zero designer modules, running in parallel with the designer
    every game. SPAAG/TD/SPG role chassis exist in the designer while their stat ladder is
    still legacy. This is the largest structural inconsistency in the system and is
    **deliberately out of scope** - record it, do not start it.
11. **`derived_variant_name` targets do not exist in script.** `light_tank_equipment_0` etc.
    are generated at runtime. Correct NSB behaviour, but it means no script can reference
    them - a recurring source of confusion when writing OOBs.
12. **Bookmark variants use concrete module ids** (`ap_0p`, `tank_he_0p`) while AI recipes
    use *categories* (`tank_ammo_kinetic`, `tank_ammo_he`). Both are correct; the asymmetry
    misleads. The three SPAA variants deliberately carry no ammunition at all, because AA
    guns supply their own attack.
13. **`sp_tag_tank_speed_factor`** is an invalid modifier in
    `common/dynamic_modifiers/wuw_dynamic_modifiers.txt` - one live log error, tank-adjacent,
    trivial, unowned.

---

## Merge order against the uncommitted doctrine diff

The doctrine effort has ~5,957 uncommitted insertions on this branch across
`tools/validate_military_reworks.py` (+881), `interface/countrytechtreeview.gui` (7109
lines changed), `common/technology_tags/00_technology.txt`,
`common/technologies/land_doctrine.txt`, `naval_doctrine.txt` and
`interface/CWIC_Doctrines.gfx`. Its own plan states: *"Do not resume its unrelated tank UI
backlog as part of this task."*

1. **Land all of Tier 1 now.** It touches only `NSB_armor.txt`, `00_tank_modules.txt`,
   `tank_chassis.txt`, `need_for_tank_roles.txt`, one English loc file, and
   `interface/tank_designer_view.gui`. Zero overlap with the doctrine working tree.
2. **While the doctrine tree is dirty, run nothing that rewrites**
   `tools/validate_military_reworks.py` or `interface/countrytechtreeview.gui`.
3. Commit doctrine.
4. Then T2.1 (validator) and T3.1 (tech tree GUI), in that order.

Commits on this branch carry **no** `Co-Authored-By` or `Claude-Session` trailer and must
not gain one.

---

## Verification

**Static, after every meaningful change:**

```bash
python3 tools/validate_military_reworks.py
python3 tools/loc_audit.py --check
git diff --check
```

`git diff --check` reporting trailing whitespace in `GRE - Greece.txt` is expected - that
file is CRLF in the index and the inserted block matches it.

**Runtime, once per tier:**

```bash
cd "/home/zom/.local/share/Steam/steamapps/common/Hearts of Iron IV"
setsid nohup ./run_hoi4 -mod=mod/Cold_War_Iron_Curtain.mod -debug -ai_testing >/dev/null 2>&1 &
```

Then diff `~/.local/share/Paradox Interactive/Hearts of Iron IV/logs/error.log` against a
baseline captured before the tier began. Targeted regression grep:

```bash
rg -n -i 'not a valid module|does not have any equipment variant.*(light|medium|heavy)_tank|multiple potential grid boxes|CWIC_tank_designer_effects' error.log
```

**Manual acceptance for Tier 1:**

1. Fresh 1949 campaign, Production tab opens without crashing.
2. Designer role dropdown lists every role including Flame, fully expanded, at 1.0x and
   2.4x UI scale, with CWIC naming ("Main Battle Tank", not "Medium Tank").
3. A flame support company can be added to a division template.
4. A starting variant shows non-zero soft attack, hard attack and piercing.
5. Heavy tank destroyer designer offers the ex-super-heavy gun.
6. Live error.log contains no `is not a valid module` lines.

**Protected files - do not stage, edit or delete:** `CWIC Backup/`, root `HANDOFF.md`, root
`error.log` / `error_1.log` / `error_2.log` / `game.log`,
`2023 - CWIC Tank Rework Balance.xlsx`, `Tank_Designer_Slimemix (1).drawio`.

---

## Open questions for the finalizer

1. Is `active = no` on the three flame subunits deliberate? (T1.1 Edit B)
2. T1.2 - delete the two orphan `parent` lines, or create the two missing engine root
   modules for symmetry?
3. T2.2 - should turret modules carry `xp_cost` like every other module family?
4. T2.3 - confirm Option A (secondary armament shares the special slots) is acceptable
   given it trades against protection and FCS choices.
5. T2.5 - is a flat `research_cost = 2` across all 169 techs intended, and should an XP
   economy exist at all?
6. Does the deadline apply to Tier 1 only, or is Tier 2 also expected tomorrow?
