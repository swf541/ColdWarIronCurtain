# Ratified decisions

Accepted choices. **Check here before proposing a redesign - most of it is settled,
and several entries record a wrong answer that was already tried.** The owner has
authorized practical design judgment within this scope; no repeat approval is needed.

## Three-hull restructure, ratified 2026-09-10

**Owner direction, and it is the largest architectural change this project has taken.
It supersedes every earlier statement about how many designer families exist.** Read
this section before anything below it: several entries in "Architecture" describe the
five-family world and are marked superseded where they conflict.

**Every armoured ground vehicle is a role on one of three hulls: light, medium, heavy.**
The five shipped designer families (light tank, medium tank, heavy tank,
`mechanized_equipment`/`apc_chassis_0..7`, `mechanized_heavy_equipment`/`ifv_chassis_0..7`)
collapse to three. APC and IFV stop being standalone families and become light-hull
roles; Heavy APC and Heavy IFV become medium-hull roles. This directly supersedes
"APC and IFV are standalone designer families" below, and it keeps that entry's
Heavy-APC/Heavy-IFV-are-medium-generation conclusion while changing its mechanism from
hull tiers to a role root.

### The role table

Light hull `light_tank_chassis`, tiers 0-9, 1939/1942/1944/1950/1960/1970/1980/1990/2000/2010:

| Vehicle | Role root | `type` set | State |
| --- | --- | --- | --- |
| Light Tank | base archetype | `{ armor light_armor }` | exists |
| APC | `light_tank_apc_chassis` | `{ armor light_armor mechanized }` | new |
| IFV | `light_tank_ifv_chassis` | `{ armor light_armor mechanized ifv }` | new |
| Light Tank Destroyer | `light_tank_destroyer_chassis` | `{ armor light_armor anti_tank }` | exists |
| Light SP Artillery (LL/LM/LH) | `light_tank_artillery_chassis` | `{ armor light_armor artillery }` | exists |
| Light SPAA | `light_tank_aa_chassis` | `{ armor light_armor anti_air }` | exists |
| ATGM Carrier | `light_tank_atgm_chassis` | `{ armor light_armor atgm }` | new |

Medium hull `medium_tank_chassis`, tiers 0-9, same year ladder:

| Vehicle | Role root | `type` set | State |
| --- | --- | --- | --- |
| MBT / Medium Tank | base archetype | `{ armor }` | exists |
| Heavy APC | `medium_tank_apc_chassis` | `{ armor mechanized }` | new |
| Heavy IFV | `medium_tank_ifv_chassis` | `{ armor mechanized ifv }` | new |
| Medium Tank Destroyer | `medium_tank_destroyer_chassis` | `{ armor anti_tank }` | exists |
| Medium SP Artillery (ML/MM/MH) | `medium_tank_artillery_chassis` | `{ armor artillery }` | exists |
| Medium SPAA | `medium_tank_aa_chassis` | `{ armor anti_air }` | exists |
| ATGM Tank | `medium_tank_atgm_chassis` | `{ armor atgm }` | new |

Heavy hull `heavy_tank_chassis`, tiers 0-4, 1939/1942/1944/1950/1955:

| Vehicle | Role root | `type` set | State |
| --- | --- | --- | --- |
| Heavy Tank | base archetype | `{ armor }` | exists |
| Heavy Tank Destroyer | `heavy_tank_destroyer_chassis` | `{ armor anti_tank }` | exists |
| Heavy SP Artillery (HL/HM/HH) | `heavy_tank_artillery_chassis` | `{ armor artillery }` | exists |

Six new role roots, one retirement. `heavy_tank_aa_chassis` retires: the ratified
Anti-Air taxonomy is Light SPAAG and Medium SPAAG only, with no heavy entry. The three
flame roots are not in the taxonomy either - see open decision 2.

**LL/LM/LH is a gun choice, not a role.** The owner enumerates nine light-hull vehicles
including LL, LM and LH Self-Propelled Artillery, but the battalion taxonomy has exactly
three artillery types - Light, Medium and Heavy SP Artillery - which map one-to-one onto
the three hulls. So the three gun weights share one artillery role per hull, selected by
which artillery gun module is mounted. Nine artillery role roots would also be
unusable: a sub-unit's `need` names one family, so a "Light SP Artillery" battalion can
consume only one of them.

### This restructure repairs the defect that blocked amphibious, and it is why the design works

`duplicate_archetypes` derives a role's tier ids by substituting the parent archetype's
name inside each member id. That only produces a clean id when the member id **contains**
the archetype id. Measured, and already recorded below under the reverted carrier
attempt:

| Family | Archetype | Members | Derived role tier |
| --- | --- | --- | --- |
| tanks | `light_tank_chassis` | `light_tank_chassis_0..9` | `light_tank_apc_chassis_3` - clean |
| carriers | `mechanized_equipment` | `apc_chassis_0..7` | `apc_amphibious_chassisapc_chassis_0` - concatenated |

Moving carriers onto the tank hulls puts every future carrier role on the left-hand row.
The concatenation defect class disappears permanently rather than being worked around.

**Consequence: Findings 14 and 15 are resolved, not deferred.** Finding 15 established
that a land sub-unit's `need` and `transport` resolve an equipment *family* - an
`is_archetype = yes` root or a `duplicate_archetypes` role root - and never a plain
numbered member, which is why explicitly declared `apc_amphibious_chassis_N` hulls could
never supply marines selectively. A role root **is** a family. `mechanized_infantry` can
name `light_tank_apc_chassis`, `armored_infantry` can name `light_tank_ifv_chassis`, and
an amphibious role root is nameable the same way. The three priced amphibious options in
Finding 15 are obsolete: option 1's "full sixth family" cost collapses to one
`duplicate_archetypes` block. Do not re-price that batch off the old finding.

### Battalion taxonomy

Line battalions, which make up the division's line:

| Class | Members |
| --- | --- |
| Infantry Carrier | APC, Heavy APC, IFV, Heavy IFV |
| Armor | Light Tank, MBT, Heavy Tank |

Support companies:

| Class | Members |
| --- | --- |
| Recon | Light Tank Recon, IFV Recon, APC Recon, Motorised Recon, MBT Recon |
| Artillery | Light SP Artillery, Medium SP Artillery, Heavy SP Artillery |
| Anti-Air | Light SPAAG, Medium SPAAG |
| Fire Support | Tank Destroyer, ATGM Carrier, ATGM Tank |

Every one of these consumes a role root or a base hull from the table above. The current
sub-units consume legacy archetypes instead (`spaag_equipment`, `sp_artillery_equipment`,
`medium_tank_destroyer_equipment`, `atgm_carrier_equipment`, `mechanized_equipment`,
`mechanized_heavy_equipment`), and all of them except the three `need_for_tank_roles.txt`
armour battalions are `active = no`. Rewiring `need`/`transport` onto role roots is the
step that makes the designer output actually reach the battlefield.

### The 20 positions are fully specialized - there are no free slots

Supersedes the shipped "slots 5-16 share one twelve-category free list" map below, and
corrects the 21-position count downward - see the engine cap immediately after the table.
The layout is five mandatory positions plus fifteen dedicated special slots. Measured
against the module inventory, the fit is exact rather than approximate:

| Slot | Label | Categories | Modules | State |
| --- | --- | --- | ---: | --- |
| mandatory | Gun, Turret, Suspension, Armour, Engine | unchanged | - | exists |
| 1 | AP Ammunition | `tank_ammo_kinetic` | 13 | exists |
| 2 | HE / HEAT Ammunition | `tank_ammo_he`, `tank_ammo_chemical` | 22 | exists |
| 3 | Aiming | `tank_fcs_aiming` | 11 | exists |
| 4 | Optics | `tank_fcs_optics` | 22 | exists |
| 5 | Computing | `tank_fcs_computer`, `tank_fcs_radar` | 21 | exists |
| 6 | Loading System | `tank_loader_manual_assist`, `tank_loader_autoloader`, `tank_loader_artillery` | 14 | exists |
| 7 | ATGM | `tank_ammo_missile` | 9 | exists |
| 8 | External Armour / Fuel Tanks | `tank_protection_passive`, `tank_external_fuel` | 7 + 1 | new category |
| 9 | Explosive Reactive Armour | `tank_protection_reactive` | 5 | exists |
| 10 | Secondary Armament | `tank_secondary_turret` | 5 | exists |
| 11 | Active Protection | `tank_protection_active` | 6 | exists |
| 12 | Smoke | `tank_smoke` | 6 | exists |
| 13 | Fire Fighting Systems | `tank_survivability` | 5 | exists |
| 14 | Auxiliary Power Unit | `tank_power_auxiliary` | 11 | new category |
| 15 | Engineering Equipment | `tank_mine_clearing`, `tank_engineering_blade` | 6 | new categories |

**The engine renders at most 20 custom module slot windows, and this is now the binding
constraint on the whole designer.** Established 2026-09-10 by owner live test, and it
overturns "21 positions is now verified" recorded on 2026-09-09. That earlier
verification was of the *declaration*, not of the render: all 21
`tank_special_slot_*` names resolved and the log was clean, which is exactly why the
missing 21st cell read as `-debug` overlay noise at the time - see the "one cosmetic note"
paragraph in `STATUS.md` Finding 6, which described a dark seventh cell in the bottom row.
That cell was the defect.

The test that settles it: `pos_custom_module_slot_window_20` never renders; removing index
19 and renaming 20 into its place still yields only the first twenty. The cap is on the
**count of positions**, not on any particular index. So the ceiling is
`pos_custom_module_slot_window_0..19` - twenty positions, laid out 7 / 7 / 6 - and five
mandatory slots leave exactly fifteen special slots.

**Mine Clearing and Engineering Blade were merged to pay for it.** They are the cheapest
pair to merge and the merge is thematically right rather than expedient: both are hull-front
attachments, a vehicle mounts one of them, and slot exclusivity is exactly that statement.
Neither category is deleted - both survive with their own `count < 2` limit, all six modules
stay reachable, and no module changes category. The alternatives were worse: dropping the
ATGM slot would strand nine missile modules, and dropping Secondary Armament would strand
five modules with fourteen live preset references.

**Do not add a 21st position.** The validator now fails on
`pos_custom_module_slot_window_20`, and any future slot family has to displace an existing
one or share a slot the way slots 2, 5, 6, 8 and 15 do.

**Slot ids were chosen to make the migration free, and the ordering is deliberate.** The
owner's picture reads in a visual order; slot *ids* do not have to match it, and
`DECISIONS.md` already establishes that the GUI label number is allowed to differ from the
slot id. Measured: of 6,041 special-slot assignments across the three scripted-effect
files only **567 are non-empty**, and every one of them already sits in a slot whose
meaning this map preserves - slot 1 `ap_*` (257), slot 2 `tank_he_*` / `tank_aa_ammo_*`
(260), slot 3 `Aim_*` (14), slot 4 `Optics_*` (14), slot 5 `Computer_*` (6), slot 6
`Loader_3a_Carousel` (2), slot 10 `cwic_coaxial_mg` (14). Slots 7-9 and 11-16 are `empty`
or absent everywhere. So full specialization costs **zero** preset, OOB, focus or
AI-recipe edits. Any reordering to match the picture visually would break 567 live
assignments for presentation only. Do not renumber these slots.

**Secondary Armament takes the slot the owner's list gave to Underwater Driving.** One
swap against the owner's enumeration, and the reason is asymmetric evidence:
`tank_secondary_turret` has five live modules and fourteen live preset references, while
Underwater Driving has **zero** modules, no technology and no balance row, and is blocked
on the same missing engine mechanism as amphibious and OPVT. Authoring an empty dedicated
slot while evicting a live five-module family would be the wrong way round. Underwater
Driving takes a position when its modules are authored in the amphibious batch - either as
a 22nd position or by sharing slot 16. This closes open decision 1 below.

**`tank_mobility_auxiliary` dissolves exactly, with no remainder.** Its 18 modules split
four ways and nothing is orphaned: `APU_0..6` plus `GT_APU_0..3` (11) to
`tank_power_auxiliary`, `Fuel_Tanks_0` (1) to `tank_external_fuel`, `Mine_Plow_0/1` and
`Mine_Roller_0/1` (4) to `tank_mine_clearing`, `Dozer_0` and `Trench_Plow_0` (2) to
`tank_engineering_blade`. The category is then deleted, not left empty. That the arithmetic
lands on 18 with no leftovers is the strongest evidence available that the owner's
sixteen-slot list was drawn against this module set.

`tank_survivability` already holds `FFS_0..2` alongside `Log_0` and `Blowout_Panels_0`, so
the Fire Fighting Systems slot needs no new module; the picture's "Blow-Out Pannels" box is
that slot showing a different mounted module.

**Mutual exclusion is expressed by slot sharing, not by a module key.** The owner requires
External Additional Fuel Tanks to be mutually exclusive with External Additional Armour.
`DECISIONS.md` already establishes that this engine has no module-to-module compatibility
key for land equipment. One slot admitting both categories delivers exactly that
exclusion, because a slot holds one module. Do not look for a `conflicts_with` key.

**The `count < 2` limits are kept, and the limited-category list goes 18 -> 21.** With
every category owning a dedicated slot the limits are strictly redundant - a slot holds
one module, and the four two-category slots cannot stack either. They are retained
anyway, because deleting 90 blocks across five archetypes would also mean rewriting the
validator's limit contract and its multi-category rejection fixture for no behavioural
gain. The one required change is that `tank_mobility_auxiliary`'s limit is replaced by
four limits for the categories that replace it. A multi-category limit block stays
prohibited.

**The slot-budget debt is discharged.** "Owner decisions, 2026-09-09 (gated-item batch)"
item 5 accepted the per-category fallback and recorded the debt that twelve free slots let
a design mount all three protection categories and all three utility categories where the
frozen envelopes assumed two of each. Full specialization removes that: protection is now
three separate one-per-vehicle slots by design rather than by accident, and the
still-unverified multi-category shared budget is no longer needed for anything. Do not
reopen the shared-budget test.

### The two engine gates

**Gate A: novel `type` tokens - CLOSED 2026-09-10, equipment `type` is an open enum.**
The role table needs two tokens outside vanilla's vocabulary: `ifv`, to tell an IFV role
from an APC role on the same hull, and `atgm`, to tell an ATGM carrier from a tank
destroyer. Without them `allow_equipment_type` cannot separate `tank_ifv_armament` from
`tank_apc_armament`, because both roles would read `mechanized`. The owner closed this by
live test: `light_armor` - a token this mod invented, absent from vanilla's 43 equipment
`type` tokens - was built onto a light tank chassis with zero errors and no issues, and
custom equipment types are documented as supported. **Custom `type` tokens are legal. Do
not reopen this as an engine risk.** The vanilla token vocabulary, measured for reference,
is 43 tokens across `common/units/equipment/*.txt`, of which the land-relevant ones are
`armor`, `infantry`, `motorized`, `mechanized`, `artillery`, `anti_air`, `anti_tank`,
`amphibious`, `flame`, `rocket`, `support`, `railway_gun`.

**Gate B: enum coverage for derived tiers - resolved by planning, not by test.**
`script_enum_equipment_bonus_type` (`common/script_enums.txt:152-1046`, 872 entries)
enumerates role roots at `:773-784`, base hull tiers at `:785-809` **and** derived role
tiers at `:810-909`. A new role root therefore needs its root plus every derived tier
listed, or the game logs one `equipment_database.cpp:656` line per missing id. Six new
roots across the 10/10/5 tier ladders is 6 roots + 50 derived ids, all authored in phase 3.
Note the existing derived entries at `:962-1045` contain malformed `chassist` / `chassisbt`
forms - artefacts to check when the block is extended, not a pattern to copy.

## Role tokens are a closed set - ratified 2026-09-10

**The tank designer's role vocabulary is hardcoded in the binary.** A custom equipment
`type` token is legal and works for module eligibility, but it can never be a named,
selectable designer role. This is the constraint the carrier half of the restructure has
to live inside, and it was settled by in-game probe rather than by reading: pointing one
module at `amphibious` and another at `rocket` made both appear as roles, while
`mechanized`, `ifv` and `atgm` never did - and `mechanized` is a vanilla category, which
rules out "declare it as a category" as the answer.

The full vanilla vocabulary, measured across the whole install: `anti_tank` (9
`allow_equipment_type` uses), `artillery` (6), `anti_air` (3), `flame` (2), `amphibious`
(1), plus `rocket`, which has a `tank_designer_rocket` localisation key and no vanilla role
root - now confirmed usable by the same probe.

**Ratified mapping.** The label a player sees is our localisation, so the internal token
name does not have to match the vehicle:

| Vehicle role | Token | Dropdown label |
| --- | --- | --- |
| Tank Destroyer, ATGM Carrier, ATGM Tank | `anti_tank` | Tank Destroyer |
| SP Artillery | `artillery` | Artillery |
| SPAA | `anti_air` | Anti-Air |
| APC, Heavy APC | `amphibious` | Armored Personnel Carrier |
| IFV, Heavy IFV | `rocket` | Infantry Fighting Vehicle |

**ATGM is a loadout, not a role.** Folding ATGM into the tank destroyer role is better than
spending a token on it: `tank_atgm_launcher_cannon` already gates on `anti_tank` and sits in
`tank_small_main_armament`, which both the light and medium hulls admit, so an ATGM Carrier
is a tank-destroyer-role design that mounts the launcher instead of a gun. The ratified Fire
Support taxonomy still ships in full; the distinction is the weapon, not the chassis role.

**`rocket` does work as a role - the apparent failure was a benign log line.** Established
2026-09-11 by owner QA: both carrier roles assign, save, produce and appear correctly in the
production and equipment tabs. `equipmentdesignerview.cpp:3657` fires only because
`allow_equipment_type` has already moved the design into the role before the player selects
it, so the dropdown click is a no-op. See `STATUS.md` Finding 24.

**The one-role carrier consolidation was tried and reverted 2026-09-11.** It is recorded
in `STATUS.md` Finding 23 as a dead end. The theory was that a second carrier role poisons
the hull's role list, since moving IFV onto `flame` broke the previously working APC role.
Consolidating both carriers onto `amphibious` alone reported both still broken, which
disproved that theory; the truth is that neither was ever broken. The tree is reverted to
the last state with a confirmed-working APC: APC on `amphibious`, IFV on `rocket` and still
failing its role change. One working role beats two broken ones.

**`flame` remains unused and should stay that way** - it is the one token observed to break
a role that was previously working.

**`rocket` renders but cannot be switched to - the usable set is five, not six.** Corrected
2026-09-10 after the remap shipped on `rocket` and the owner hit
`equipmentdesignerview.cpp:3657: Failed to change role to "Infantry Fighting Vehicle"` on
save, while the `amphibious` APC role worked completely. The discriminator is structural:
`amphibious`, `anti_air`, `anti_tank`, `artillery` and `flame` each have a vanilla
`duplicate_archetypes` role root in `x_tank_chassis.txt`; `rocket` has a
`tank_designer_rocket` localisation key and a category entry but **no role root anywhere in
the base game**. That is enough to render it in the dropdown and not enough to make it a
real role.

So IFV takes `flame`. The token is free precisely because flame tanks were deleted earlier
the same day, and the name is internal - the dropdown reads "Infantry Fighting Vehicle"
because `tank_designer_flame` says so. `tank_designer_rocket` was restored to "Rocket
Artillery" since nothing uses it.

**The usable designer role vocabulary is therefore exactly five:** `anti_air`, `anti_tank`,
`artillery`, `amphibious`, `flame`. All five are now spent - AA, Tank Destroyer, Artillery,
APC, IFV - which is the real reason ATGM had to become a loadout, and it means **no further
designer role can ever be added.** Any future vehicle class must be a loadout on an existing
role or a separate archetype family.

**Consequence for the flame-removal contract:** the validator no longer bans the `flame`
type token, because the IFV roles legitimately carry it. What it bans is any chassis or role
whose *name* contains `flame`, which is the thing that was actually retired.

Role roots therefore settle at **12**, not 14.

**Do not reopen this by trying to register a new token.** There is no mechanism. The
validator rejects any `allow_equipment_type` or `forbid_equipment_type` value, and any
non-`armor` token on the three hulls or their role roots, outside
`{anti_air, anti_tank, artillery, amphibious, rocket, flame}` plus the three size tokens -
`rocket` stays in the legal set because it is a real equipment type, but nothing uses it.
The two standalone carrier families additionally keep `mechanized`, which is a vanilla
equipment type and not a designer role.

**Consequence worth tracking:** APC now carries the `amphibious` token. Vanilla marine
sub-units consume the `amphibious_tank_chassis` *archetype*, not the token, so nothing is
wired up by accident - but `light_tank_apc_chassis` is a nameable `duplicate_archetypes`
family, which is exactly what Finding 15 said a marine sub-unit needs. The amphibious
supply problem is now solvable whenever that batch is picked up.

### Flame tanks are removed - ratified 2026-09-10

**Owner ruling: flame is axed completely.** Nothing in the mod uses flame tanks, and
everything flame-related is legacy or vanilla-inherited. This is a clean cutover, and it
closes the last open decision on the restructure.

The removal was safe to take in full because the consumers do not exist: **`history/`,
`common/ai_templates/` and every OOB contain zero references to any flame sub-unit or
flame chassis.** No division template, no starting order of battle and no AI template
fields a flame battalion, which is the same evidence known inconsistency 1 recorded from
the other side when it noted that no AI division template fields a flame battalion.

What goes: the three `duplicate_archetypes` role roots, the three `active = yes`
sub-units in `need_for_tank_roles.txt`, the `flamethrower` module and its
`tank_flamethrower` category, that category's place in all three `main_armament_slot`
lists, every flame grant in `NSB_armor.txt`, the flame AI recipes, all flame entries in
`script_enum_equipment_bonus_type`, 24 blueprint GUI files, the flame designer-module and
MIO department sprites, the English localisation, and the dead flame entity aliases.

**Four surfaces are deliberately left alone**, and each for a reason rather than by
omission:

- `interface/texticons.gfx`. It is a full vanilla override, and a comment at `:2920`
  records that dropping entries there previously produced 1002 error-log lines. Orphan
  sprites are harmless; editing that file is not.
- `localisation/french/` and `localisation/japanese/`. Another team owns translations.
  Dead keys there are acceptable.
- `sound/sound.asset` and `combat_tactics.txt`. The sound entries are animation effects
  with no equipment binding, and the tactics block is already commented out.
- `common/military_industrial_organization/`. Six policies test
  `has_mio_equipment_type = flame`; with no equipment carrying that type they simply stop
  matching. That content has another owner, and silently deleting policy conditions to
  tidy a type token would be the wrong trade.

**Consequence for the role dropdown.** `REFERENCE.md` explains that the dropdown lists one
entry per distinct `allow_equipment_type` value in the loaded module set. Removing
`flamethrower` - the only module carrying `allow_equipment_type = flame` - drops the mod
from four such values to three, so every chassis designer now shows four entries instead
of five. That is the intended outcome, not a regression to investigate.

The `tank_secondary_turret` question is closed - see the slot table above. No open
decisions remain on the restructure.

### What this restructure costs - see `STATUS.md` Finding 16 for the measured blast radius

The headline is that the carrier retirement is a **mass content migration**, not the
contract-only change the 15-to-21 slot expansion was. 857 `apc_chassis_*` / `ifv_chassis_*`
references live across 70 files, 572 of them in `CWIC_national_tank_presets.txt` alone, and
full slot specialization invalidates the "already-explicit assignments stay legal"
guarantee that made the last expansion cheap.

## Architecture

**SUPERSEDED 2026-09-10 by the three-hull restructure above. Kept for provenance.**
~~**APC and IFV are standalone designer families**, not roles on the light and medium
tank hulls. Superseded 2026-09-07 on evidence: the drawio `[REFERENCE] Whole Tech Tree`
mechanized column specifies a dedicated ladder separate from every tank hull column.
Light Mech is the APC line (`mechanized_equipment` / `apc_chassis_*`); Heavy Mech is
the IFV line (`mechanized_heavy_equipment` / `ifv_chassis_*`).~~ The owner reversed this
on 2026-09-10: carriers are light-hull and medium-hull roles.

**Heavy APC and Heavy IFV are a medium hull generation**, not more tiers on the
light-hull families. Both the xlsx `Roles` tab and the drawio AFV Hulls page place them
there (Heavy APC 1985 off Second Gen MBT, Heavy IFV 2005 off Second+ Gen MBT). Still
true, and the restructure implements it as `medium_tank_apc_chassis` /
`medium_tank_ifv_chassis` rather than as hull tiers.

**Tier count and years come from the frozen manifest, not the diagram.** 8+8 at
1947/1950/1960/1965/1975/1985/1995/2005, from the 18 mechanized envelope rows. The
diagram's seven-tier decade cadence is a sketch. Do not "correct" the years to it.

**`mechanized_heavy_equipment_3` stays at 1955.** The workbook's 1960 is a deliberate
year exception and is not permission to alter the stats or the workbook. `nsb_ifv_hulls2`
carries `start_year = 1955` and the `@1955` tree row so tree, tooltip and hull agree.

**CORRECTED 2026-09-10 to 20 positions by the engine cap on custom module slot windows.
Everything below about the expansion still holds except the count and the trailing slot.**

**The designer expands from 15 to 21 positions.** Ratified 2026-09-09, superseding
"the 15-position designer is final". The target is drawio page 8
`[REFERENCE] Tank Designer Composition`, which lays out nine named slots - Gun, Turret,
AP Ammo, HE Ammo, Aiming, Optics, Suspension, Armour, Engine - plus `Slot 1..12`, i.e.
21 positions. `archive/Balance_Sources.md:148-151` had ruled that page "a sketch, not a
specification, and the shipped 15-slot layout in interface/tank_designer_view.gui is the
thing that exists"; the owner reversed that on 2026-09-09. The sketch is now the
contract and the shipped 15-slot layout is the **unfinished** state - see `STATUS.md`
Finding 6.

- Slot set: the five mandatory slots plus `tank_special_slot_1..16`. Names stay
  `tank_special_slot_N`; `special_type_slot_N` is still prohibited in tank content
  (the plane-airframe collision fixed by `368fa4815c`).
- Specialized: slot 1 anti-tank ammunition, slot 2 HE ammunition, slot 3 aiming,
  slot 4 optics. This splits today's "either ammunition in either slot" pair, and it
  costs no preset edits because the shipped presets already follow it: of 586 national
  blocks, slot 1 holds only `ap_*` (213 assignments, 373 `empty`) and slot 2 only
  `tank_he_*` (213 assignments, 373 `empty`).
- Free: slots 5-16 accept every remaining special category and every category authored
  later. Their GUI labels are `Slot 1`..`Slot 12` per the sketch, so the label number is
  deliberately offset from the slot id. Do not "fix" that by renumbering the slots.
- The same 21-position layout applies to all five archetypes. `mechanized.txt:37-164`
  and `mechanized_heavy.txt:28-42` already mirror the tank special-slot names and
  category map and diverge only in mandatory armament/turret categories, so this is one
  change applied five times, not two designs.

**The 21 positions render 7 / 7 / 7 with the middle row over the blueprint.** Ratified
2026-09-09. `equipment_modules` stays 515x350 and `equipment_preview` keeps its 508x248
blueprint, so no art is rescaled or cropped: positions 0-6 on `@fixed_btn_mod_row_0 = 1`,
7-13 on the existing `@fixed_btn_mod_row_middle = 180` promoted to a full row, and 14-20
on `@fixed_btn_mod_row_1 = 300`. Frames stay 76x47
(`interface/equipmentdesignerview.gui:1743-1751`) and the seven existing column macros at
pitch 73 end at exactly 515. Two alternatives were rejected: the sketch's literal 6x3 +
3 geometry, and a 3x7 grid above the blueprint. Both force the preview down to <=162px,
which buys an art pass and no capacity. Overlaying frames on the blueprint is already
this panel's layout language - slot 14 sits at (439,180) today, and
`tag_icon_bg`/`niche_button` overlay the same rectangle (see "Retracted after
measurement").

**Gate: 21 positions is beyond anything vanilla ships and must be confirmed in game
before any content depends on it.** The vanilla tank designer declares
`pos_custom_module_slot_window_0..8` for 5 mandatory + 4 `special_type_slot_N` slots, and
the highest index anywhere in the vanilla interface files is 8. No engine-side cap is
documented and none was found; the mod's own 15 positions prove the count is not fixed at
9. That makes 21 plausible, not verified.

**Free slots keep today's tradeoffs through shared-budget exclusivity groups, pending an
engine test.** Slot specialization is currently the only thing making computing compete
with radar, allowing one loading system, and making active protection compete with an
armour layer. Twelve free slots delete all of that unless one `module_count_limit` block
can hold several `category` entries as a shared budget. **That form is unverified:**
vanilla ships no multi-category limit block anywhere under
`common/units/equipment/`, and all 18 blocks on the mod's own archetypes are
single-category `count < 2`. Test it in the same pass as the 21-position render. If the
engine rejects a shared budget, the fallback is per-category `count < 2` only, and the
consequence - up to 12 specials mounted where the frozen envelopes assumed 10
specialized picks - is an explicit balance-recalibration item, not a silent change.

**Shipped 2026-09-09 with the per-category fallback, not the shared budgets.** The
multi-category test was not runnable to a positive answer: a log diff can prove the
engine *rejects* a multi-category `module_count_limit`, but engine silence cannot prove
a shared budget is enforced rather than parsed and ignored, and that distinction needs
a human in the designer. So the ratified fallback shipped - one single-category
`count < 2` per special category, on all five archetypes, 18 each. APC and IFV were
missing seven of those limits before this pass (four ammunition, three loader); the
three loader limits are load-bearing, because twelve free slots would otherwise let a
carrier mount three loading systems. The validator now rejects a multi-category limit
block outright, so the unverified form cannot be reintroduced by accident. Authoring
the shared budgets remains open and still requires a live enforcement test.

**Positions above 8 are confirmed in game.** Ratified gate cleared 2026-09-09 by the
owner's designer capture: the 7 / 7 / 7 layout renders with the middle row over the
blueprint, and the top row reads turret, gun, suspension, armour, engine, AP
ammunition, HE ammunition - so both the 21-position layout and the slot 1 / slot 2
ammunition split are live. The gate is fully closed: after the blueprint fix below the
owner re-checked in game and confirms all 21 slots load, and the live `error.log`
carries zero `Could not find "tank_special_slot_*"`, zero `Requested GUI element not
found` and zero `containerwindow.cpp` lines with the designer open, against 85
slot-lookup failures on the pre-fix boot. **21 positions is now verified, not
plausible** - do not reopen it as an engine risk.

**The 106 per-hull blueprint files are a sixth surface, and they are hand-enumerated.**
Discovered 2026-09-09. Every file under `interface/equipmentdesigner/tanks/` lists the
slot names itself inside its `module_slots` window. A slot the archetype declares but a
blueprint omits produces `containerwindow.cpp: Could not find "tank_special_slot_N" in
window module_slots` and a `Requested GUI element not found` assertion, but **only once
that specific hull's designer is opened** - so no static check and no ordinary load test
sees it. All 106 now declare `tank_special_slot_1..16`; the validator pins the file
count and the exact ordered slot list per file. The 147 unshadowed vanilla blueprint
files were left alone: they all belong to chassis families this mod removed
(`amphibious_tank`, `modern_tank`, `super_heavy_tank`, `land_cruiser`, and the deleted
`*_amphibious` roles). Any future slot change must touch all 106 again.

**Slots are to be locked per hull, not uniformly free.** Owner direction 2026-09-09,
refining the free-slot rule above rather than replacing it. 21 positions on all five
hulls is final; what is not final is that all five share one free-list. Specialized
modules that only some hulls may carry - amphibious drive on APC and IFV, not on
medium, MBT or heavy - need per-hull slot eligibility. The shipped identical free list
is correct only while every free-list category applies to every hull, so the lock model
must land in the same pass as the first hull-restricted module. Authoring such a module
against the current uniform list would silently make it mountable everywhere.

**The two owner mockups are the source for the unbuilt families.** Supplied 2026-09-09
and now the authority for their ladders, superseding "invent the whole tree":

- *Night and thermal vision* sits on the optics/aiming page as a four-step ladder off
  the base optic sights: First Gen Night Vision (off Telescopic/Periscopic Sight,
  alongside Sterioscopic Sight With Optical Rangefinder), Second Gen Night Vision,
  Third Gen Night Vision, then Thermal Vision. The stat values are still invented and
  still fall under the "recorded as authored" rule - the mockup fixes the shape and the
  prerequisites, not the numbers.
- *Special Capabilities* is its own dated column: Amphibious Drive 1940; OPVT,
  Underwater Driving Capability and Dozer Plow 1945; Log (+2% reliability) 1950;
  Anti-Mine Plow 1955 off Dozer Plow; Paradrop Capability 1960; Anti-Mine Roller 1965
  (KMT-5); Integrated Trench-Digging Plow and a second Anti-Mine Plow 1970; Anti-Mine
  Roller With Electro-Magnetic Coils 1980 (KMT-7 EMT). Amphibious Drive and Paradrop
  Capability are hull-restricted by nature and are the reason the per-hull lock model
  above is a prerequisite rather than a follow-up.

**The per-hull lock is a module attribute, not a slot attribute.** Established
2026-09-09 on engine evidence, and it supersedes any reading of the direction above
that implies per-archetype free-slot lists. A category is global while a free-slot list
is per archetype, so a category cannot restrict a module to some hulls: putting
amphibious drive in `tank_mobility_auxiliary` makes it legal on every hull whose free
slots take that category. The engine primitive is
`allow_equipment_type` / `forbid_equipment_type` / `forbid_equipment_type_exact_match`,
which key off the archetype's own `type = { ... }` set. Vanilla's `amphibious_drive`
uses exactly that shape, and the mod's own module file already uses these keys 49
times. The designer role roots supply the discriminators: `x_tank_chassis.txt:8-15`
makes `light_tank_aa_chassis` `type = { armor anti_air }` and `:18-25` makes
`light_tank_artillery_chassis` `type = { armor artillery }`, while the carrier
archetypes carry `mechanized` beside `armor`. Consequence: hull-restricted modules
need no GUI change, no new slot and no divergence between the five free lists. Do not
implement per-hull locking by forking the category lists.

**Thermal vision is already shipped; only night vision is missing.** Established
2026-09-09. `Optics_4..7` are localised "Thermal Sight I/II/III" and "Advanced Thermal
Sight" (`tank_modules_l_english.yml:951-957`) in category `tank_fcs_optics`, unlocked by
`nsb_optics4..7` at 1970/1980/1990/2005. The owner's mockup shows a three-step thermal
branch in a separate column; the shipped four steps in the optics column satisfy it. The
default is to leave them where they are and treat the mockup's thermal boxes as done -
splitting them into their own column would retarget four shipped modules, four
technologies and every preset that names them, for presentation only. Night vision is
the genuinely absent half: six technologies, column x18 free immediately right of the
panoramic sights at x16, two new tree rows (1960 and 2000).

**Paradrop capability cannot be a designer module.** Established 2026-09-09 by
searching the vanilla module directory: no module anywhere carries
`can_be_parachuted`, `parachut*`, `special_forces` or `marines`. The only
capability-bearing vanilla module is `amphibious_drive`, and it works through equipment
types. So the mockup's Paradrop Capability box has no module mechanism - it must be a
sub-unit or technology property, or be dropped. Do not author it as a module.

## Owner decisions, 2026-09-09 (module content)

All four blocking decisions from the module content plan are answered. These are
ratified; do not reopen them.

1. **`Optics_4..7` are accepted as the thermal branch in place.** No new thermal
   column, no retargeting of the four shipped modules or their `nsb_optics4..7`
   unlocks. The mockup's thermal boxes are satisfied; its 1975/1990/2000 years yield to
   the shipped 1970/1980/1990/2005. Descriptions 42-45 attach to the existing modules.
2. **Amphibious follows the design documents, not an improvised role.** The proper
   amphibious role is whatever the design documentation specifies; that specification is
   the authority over any reconstruction from current script.
3. **Paradrop is restricted to light hulls and light vehicles only.** It is therefore
   hull-restricted in the Finding 9 sense. Since no module can carry a paradrop
   capability key, the capability itself must come from a sub-unit or technology, and
   the light-hull restriction is expressed with
   `allow_equipment_type` / `forbid_equipment_type` on whatever module or role carries
   it.
4. **AA ammunition overturns the legacy self-supplying-AA-gun rule.** The ratified
   position that AA guns supply their own attack and that SPAA variants carry no
   ammunition is **superseded**. An AA ammunition ladder is authorized. Consequences to
   settle in that batch: known inconsistency 10's "three SPAA variants deliberately
   carry no ammunition" no longer holds, and the validator's `needs_ammunition` AA
   exemption must be inverted rather than worked around.

**Engine and suspension year authority: the icon assets win.** Ratified 2026-09-09.
Where an icon year and its unlocking technology's `start_year` disagree, the icon year
is correct and the technology moves. This is one systematic decision, not eleven: gas
turbines `GT_0..3` icons 1960/1970/1980/2000 against techs
`nsb_gt_engines0..3` 1965/1975/1985/2005, and `GT_APU_0..3` icons 1960/1970/1980/2000
against the same four technologies. Also covers the combustion 1939-versus-1940 case.

**Experimental 4-Track Suspension is authorized** as described in the mockup, including
its "Opened by 1955 H Tank" prerequisite - a heavy-hull-gated unlock rather than a
free-standing technology.

**The module technology folder is visually clipped at x=16 and must be widened before
any column is added there.** Established 2026-09-09: across all 102 technologies in
`nsb_armor_modules_folder` the distinct x columns are
-8, -6, -4, -2, -1, 0, 2, 4, 6, 8, 10, 12, 14, 16, so x=16 (`nsb_pano_sight0..2`) is the
rightmost that has ever rendered, and the owner reports the tree is cut off there. The
night-vision column at x=18 therefore depends on a GUI change in
`interface/countrytechtreeview.gui` first. Per `GOTCHAS.md` the layout must be measured
rather than inferred from element names before any value is changed.

## Owner decisions, 2026-09-09 (gated-item batch)

These six decisions close the gated-item batch. They are ratified and must not be
reopened as unresolved implementation questions.

1. **Amphibious carriers are deferred.** Defer the whole batch; the three priced
   options remain open: a real sixth designer family, rejected carrier-member renaming,
   or APC-wide marine transport.
2. **Paradrop and hull-size discrimination use `light_armor`.** The light family is
   now `{ armor light_armor }`; any new light-family role root must carry the token.
   No paradrop consumer is authored yet.
3. **Artillery/AA is deferred entirely.** This includes widening the module-unlock
   provenance boundary.
4. **The tech-tree clip is fixed by moving two gridbox origins.** Move
   `nsb_tank_design_tree` from `x = 3600` to `x = 1650` and `nsb_armor_tree` from
   `x = 2400` to `x = 950`; technology coordinates do not move. The 3187 ceiling is
   empirical, not an engine constant.
5. **Slot-budget debt is accepted.** Keep the per-category fallback and its recorded
   debt; do not replace it with the unverified shared budget. Any future re-cut edits
   the frozen 40-row manifest.
6. **Major-country `Petrol_1` bootstrap is implemented.** Grant `nsb_engines0` to
   USA, SOV, FRA, ENG and WGR. Keep generic fallback recipes on `Petrol_0`; reroute
   only the tag-exclusive USA `M47 Patton` preset to `Petrol_1`.

**Standing rule: a new NSB armour technology dated 1980 or earlier is incomplete until
it is added to `cwic_major_tank_research_1980`.** That effect must grant every tank
technology with `start_year <= 1980`, and the validator fails with "1980 tank research
coverage differs" otherwise. It caught this twice on 2026-09-09 - once for
`nsb_night_vision0..2` and once for `nsb_special_capabilities0..5`,
`nsb_suspension_multi_track` and the migrated gas turbines. The effect lives in
`common/scripted_effects/CWIC_tank_bookmark_research.txt`. Treat updating it as part of
the definition of adding the technology, not as a follow-up.

**A new category's cost depends on whether its slot is mandatory or free.** Established
2026-09-09 by `tank_suspension_multi_track`. A **free-slot** category must be added to
the free list of all five archetypes AND given a `module_count_limit { count < 2 }`, or
it silently stacks. A **mandatory-slot** category - suspension, armour, engine, turret,
main armament - is added only to that slot's `allowed_module_categories` on all five
archetypes and must NOT get a count limit, because a mandatory slot holds exactly one
module. Do not reflexively add a limit for every new category.

**Brace balance and byte checks are not a syntax check, and a passing validator is not
a passing parse.** Established 2026-09-09 the hard way: a single missing `=` in
`tank_designer_view.gui` (`y@fixed_btn_mod_row_0`) aborted the parse of 125 children of
`tank_designer_view` and crashed every tank, APC and IFV designer with SIGFPE, while
brace balance was 0, all bytes were clean, and the validator reported
`21 designer slots checked` - because its slot regex matched the broken line. Any pass
that rewrites script or GUI assignment blocks MUST verify token shape. The validator now
enforces this for `position`/`size`/`margin` blocks in the designer GUI and all 106
blueprint files. Load-time parse errors appear with `no_game_date`, so a plain boot
confirms them with no gameplay required - do that after any GUI edit.

## Amphibious as a designer role, ratified 2026-09-09

**Owner ruling, superseding every earlier amphibious statement** including
`REFERENCE.md:129-131`'s "amphibious mobility module" and the "eligible mechanized
designs" wording: the replacement for the legacy mechanized amphibious vehicle is an
APC/IFV design that gains the **amphibious designer role**, in the same way a tank's main
armament determines whether it is a gun tank, SP artillery, SPAA, tank destroyer or flame
tank. Where earlier notes conflict, this wins.

**The mechanism is real and already in use here - with the causality the other way
round.** A module does not create a role; the role exists as an archetype and the module
is *restricted to* it, which produces the same player experience. Measured:
`tank_anti_air_cannon` carries `allow_equipment_type = anti_air` plus
`forbid_equipment_type_exact_match = armor`, and `tank_low_p_cannon0` carries
`allow_equipment_type = artillery`. The roles themselves are cheap `duplicate_archetypes`
entries - `x_tank_chassis.txt:8-15` is six lines declaring `light_tank_aa_chassis` as
`archetype = light_tank_chassis`, `type = { armor anti_air }` - and the engine derives
every tier from the parent family, which is why `light_tank_aa_chassis_1` is legal though
never declared.

So the amphibious implementation is two small pieces plus rewiring:

1. Carrier amphibious role roots in `x_tank_chassis.txt`, e.g. `apc_amphibious_chassis`
   with `archetype = mechanized_equipment` and `type = { armor mechanized amphibious }`,
   and the IFV equivalent.
2. An amphibious drive module gated `allow_equipment_type = amphibious`, so it is
   mountable only on those roles and nowhere else.
3. `mechanized_marine`'s `need` / `transport` point at those **role chassis**, not at
   `mechanized_equipment`. This is what makes the capability selective and it removes the
   objection recorded in Finding 14: an ordinary APC is not a marine transport, only an
   amphibious-role APC is.

Finding 14 stands as the reason a module alone cannot do it - sub-units consume equipment
ids and no land sub-unit can test for a fitted module - but its "expensive role rebuild"
framing is downgraded: `duplicate_archetypes` makes the role itself nearly free. The real
cost remains the six validator contracts and the `mechanized_marine` `active = no`
assertion, all of which must change consciously.

**Module-to-module compatibility does not exist in this engine, and the design must not
assume it.** The complete tank-module vocabulary for restricting a module is three keys,
confirmed by scanning the whole vanilla module directory: `allow_equipment_type` (23
uses), `forbid_equipment_type` (4) and `forbid_equipment_type_exact_match` (6). There is
**no** key expressing "this module requires that module" or "this module conflicts with
that module" for land equipment; `need_equipment_modules` exists only on ship hulls
(`battlecruiser.txt:8-12`). Consequences for any future module-limitation design:

Restriction by **hull or role** is expressible, via the archetype `type` set.
Restriction between **individual modules** is not. The only levers are which category a
module sits in, the per-category `count < 2` limits, and the still-unverified
multi-category shared budget.
Restriction by **hull size** is now expressible for light versus medium/heavy:
`light_tank_chassis` is `{ armor light_armor }`, while the medium and heavy archetypes
remain `{ armor }`. Any new light-family role root must include `light_armor`.

**Attempted 2026-09-09, reverted: `duplicate_archetypes` cannot give the carrier
families clean role tier ids.** The role-as-designer-role design above is right; this is
a naming constraint on the mechanism, discovered by boot testing and not visible
statically.

`duplicate_archetypes` derives a role's tier ids by substituting the parent archetype's
name inside each member's id:

| Family | Archetype | Members | Derived role tier |
| --- | --- | --- | --- |
| tanks | `light_tank_chassis` | `light_tank_chassis_0..9` | `light_tank_aa_chassis_3` - clean |
| carriers | `mechanized_equipment` | `apc_chassis_0..7` | `apc_amphibious_chassisapc_chassis_0` - concatenated |

The tank case works because the member id **contains** the archetype id. The carrier
members were deliberately renamed to `apc_chassis_N` / `ifv_chassis_N`, which do not
contain `mechanized_equipment`, so the engine falls back to concatenating the role id and
the member id. A live boot produced 24 error lines, eight of them
`apc_amphibious_chassisapc_chassis_N is an equipment type ... not in script enum`, plus
13 `Failed to change role to "Unknown"` before the `for_each variant_name
find_and_replace` was removed. Renaming the role does not help - the mismatch is between
the archetype id and the member ids, not in the role id.

The whole attempt was reverted rather than shipped: the validator passed at
`1318 technologies, 290 tank modules` with malformed equipment ids in play, which is
Finding 11's lesson repeating in a new place. Post-revert boot is clean - zero
`amphibious_chassis`, zero `Failed to change role`, zero `script_enum` complaints.

**The explicit-declaration route is withdrawn, 2026-09-09.** It read: declare the
amphibious carrier role chassis explicitly, sixteen equipment blocks in the style of the
existing `apc_chassis_0..7` and `ifv_chassis_0..7` members, each carrying
`type = { armor mechanized amphibious }`, instead of deriving them. It does fix the
id-concatenation defect above, and it is **still wrong**, because it cannot supply the
marine sub-unit - see `STATUS.md` Finding 15. A land sub-unit's `need` and `transport`
resolve an equipment *family*: every such value in the whole vanilla `common/units/`
tree is an `is_archetype = yes` archetype or a `duplicate_archetypes` role root, and no
vanilla sub-unit anywhere names a plain numbered member. Hulls declared as members of
`mechanized_equipment` are therefore unnameable in `need`; the only nameable id is
`mechanized_equipment` itself, which makes **every** APC a marine transport - the
unselective option Finding 14 rejects.

What survives from that route is only the module half: the `amphibious` token in an
archetype's `type` set still gates modules through `allow_equipment_type`.

**The three surviving options, priced.** No route is ratified; the owner picks one.

1. *A real sixth designer family* - amphibious carrier hulls under their own
   `is_archetype = yes` root, which is vanilla's own shape
   (`amphibious_mechanized_equipment`, `amphibious_tank_chassis`). The only route that
   is both selective and proven, and the honest cost is a full family - archetype block
   with the 21-slot layout, hull tiers, pictures, blueprint GUI, unlocks, presets, and
   the six validator contracts in Finding 14. This is **not** the "nearly free"
   `duplicate_archetypes` role assumed above.
2. *Rename the carrier members* to contain `mechanized_equipment` so derivation works -
   **rejected**, unchanged: those ids appear across 586 national presets, the generic
   bookmark variants and the OOB migration.
3. *Accept APC-wide marine transport* - cheap, unselective, needs an explicit ruling.

Also established while attempting this, and it is why the module half is not enough on
its own: a single sub-unit cannot accept either the legacy equipment or a designer role
chassis. `transport` is one scalar id and `need` entries are conjunctive, so listing both
`mechanized_marine_equipment` and an amphibious role chassis makes the sub-unit require
**both** at once. Supplying marines from a designer carrier therefore needs a **second**
sub-unit consuming the role chassis, leaving legacy `mechanized_marine` intact for
non-NSB players - which touches division and AI templates and is its own decision.
`CWIC-Special-Units.txt` was left byte-for-byte unchanged.

Both columns are now partly built. Night vision shipped 2026-09-09 as
`nsb_night_vision0..5` with six `tank_fcs_optics` modules; the thermal half was already
shipped as `Optics_4..7`. The Special Capabilities column shipped the same day as
`nsb_special_capabilities0..6` with ten modules, plus `nsb_suspension_multi_track` and
`Four_Track_0`. Still unbuilt from that column: Amphibious Drive, Paradrop Capability,
OPVT, Underwater Driving Capability and Modular Construction - the first four for want
of an engine mechanism, the last for want of a category. All authored stats in both
columns are invented and recorded as authored; `Log_0`'s +2% reliability is the sole
documented value.

**Free slots are not enumerated in presets.** Vanilla proves optional slots may be
omitted: `history/countries/GER - Germany.txt:1097-1108` creates `light_tank_chassis_0`
with the five mandatory slots and one special, nothing else. So the shipped 586 national,
40 generic and 16 export creation blocks stay valid as written - their 8,790 + 160 + 80
special-slot assignment lines need no rewrite - and the validator moves from "exactly 15
assignments" to "five mandatory present, specials a subset of the declared set". Adding
six slots is therefore a contract change in one archetype family plus the validator, not
a mass content migration.

**Legacy mechanized ladders retire by DLC-gating production, not by removing
technologies from `nsb_armor_folder`.** Dropping the folder placement from
`mechanized_infantry*` and `mechanized_heavy_infantry*` would take four things with it:
their `enable_subunits` for `mechanized_infantry` and `armored_infantry`; the
cross-links feeding `light_tanks_3/4/5/6` and `amphibious1`; the `allow` gates on
`nsb_apc_hulls0` and `nsb_ifv_hulls0`; and 1144 `set_technology` sites in
`history/countries/` plus focus references in `USA_70s_Military.txt` and
`60s_Generic.txt`. DLC-gating keeps the technologies researchable and their sub-unit
activation intact while `can_be_produced` removes the legacy models from the NSB
production tab. `mechanized_equipment_1..2` must stay ungated - they are the
pre-designer WWII rows with no designer replacement.
*Blocker:* gating leaves an NSB bookmark start with no buildable carrier until a design
exists, so this depends on the presets and OOB migration landing first.

**Amphibious capability belongs in a mobility module on eligible mechanized designs.**
Do not remove the NSB legacy amphibious unlocks until replacement vehicles actually
supply the marine sub-units correctly. Three separate things must not be conflated:
the live legacy `amphibious1..5` technologies granting
`mechanized_marine_equipment_1..5`; the designer amphibious role, which was **deleted**
(rebuilding it is new work, not a restore); and the `mechanized_marine` sub-unit, which
is `active = no` with the validator asserting it stays that way. Any amphibious work
must change that assertion consciously.

**Night and thermal vision values are invented and must be recorded as authored.** The
design exists on drawio page 4; the workbook reserved a `Night & Thermal Vision Effects`
tab and left it empty. The mod has one orphan `night_vision` string in
`common/technology_tags/00_technology.txt:42` and nothing else.

**Artillery and AA gate legacy and designer paths by DLC**, preserving technology-based
sub-unit activation. The `support.txt` pattern `OR = { has_tech = legacy has_tech = nsb_* }`
already exists in the repo for exactly this. Source targets are frozen in `BALANCE.md`.

**Workbook is frozen; the CSV is the living balance mirror** with explicit reviewed
overrides.

## Producer resolution

A design's producer resolves as **producer, then creator, then owner, then the OOB
tag**, independent of token order. Both naming and bootstrap attribution use this rule;
neither source field is removed.

The old validator selected the first owner/producer/creator token, which disagreed with
attributing technology to creator/producer - for example DRY's forced request has
`owner = DRY creator = "CUM"`. Installed vanilla evidence settles it: `YUG_1939_nsb`
requests France's `FT mod. 31` with owner YUG and creator FRA, and France creates that
design.

Consequences already established by runtime testing:

- A tank bought from or designed by another tag is looked up on *that* tag. The chassis
  technology belongs in that country's bootstrap, not the loading country's. This is
  what made FRA, ENG and the `CAP`/`CUM` manufacturer bloc tags fail.
- Tech sets are scoped per bookmark. A 1949 bootstrap must not preload the 1970s
  chassis its country only sells in 1980.
- `CAP` and `CUM` sell tanks but never load an OOB, so they call the creator directly
  from their own history.
- Never rename all requests according to the country whose OOB file is being loaded.

The bootstrap ordering rule this depends on: an OOB-local `instant_effect` runs *after*
that OOB's own production, stockpile and forced-variant requests resolve, so a variant
created there is always too late. The bootstrap runs in country history immediately
before `set_oob`:

```
country scope
  -> set_technology for exactly the chassis technologies this bookmark needs
  -> cwic_create_starting_tank_variants = yes
  -> set_oob = <bookmark NSB OOB>
```

## Legacy focus armour grants

**Ratified 2026-09-08.** On an NSB profile, a legacy armour focus grant maps to
the largest designer chassis whose introduction year is no later than the legacy
equipment year. The producer creates one obsolete, no-tech export variant for
that chassis, and the focus grants that producer-owned variant. The non-NSB
branch remains the original legacy equipment grant unchanged. Producer
resolution follows the established producer, creator, owner, OOB-tag order.

The export inventory required by the current grants is:

- Main Battle Tank: 1942, 1944, 1950, 1960, 1970 and 1980.
- Light Tank: 1942 and 1944.
- Heavy Tank: 1942 and 1944.
- APC: 1947, 1950, 1960 and 1965.
- IFV: 1950 and 1965.

All export variants use the established obsolete baseline loadouts. The eight
equipment-type exceptions remain legacy grants: `mechanized_equipment`,
`mechanized_equipment_1`, `mechanized_equipment_2`, and
`mechanized_marine_equipment_1..5`. The first three are pre-designer WWII rows
without replacements; the marine rows remain legacy until a designer vehicle
supplies the marine sub-unit. The 11 explicitly reference-only focus paths are
excluded from this migration and from its validator contract: `FOR HOTFIX/`,
`Need Finished/`, `OUTDATED_PRC_60s.txt`, `Old/`, `Toberemoved/`, and
`Trees for 0.35/`.

**Deferred follow-up.** The current focus effects use generic `CWIC Export ...`
`variant_name` values instead of historical preset variants. This is
immersion-breaking and does not track the legacy equipment identity. A future
session must research and map each focus effect/equipment grant to its
historical variant counterpart. The research cost is intentionally deferred;
no historical mapping is part of this migration.

## Stockpile grants

**Ratified 2026-09-08.** `add_equipment_to_stockpile` takes `type`, `amount`,
`variant_name` and `producer`. It does **not** take `creator`, even though
`creator` is correct on `force_equipment_variants` and `add_equipment_production`
and is what the producer-resolution rule above talks about. The engine rejects the
token and drops the whole grant with no in-game symptom. Do not "restore" `creator`
here for consistency with the resolution rule - the rule is about which tag owns a
design, not about this effect's parameter names.

Every stockpile `type` must resolve to a declared equipment id, or to a tier its
parent family actually declares behind a `duplicate_archetypes` root. The engine
derives those tiers at runtime, so `light_tank_aa_chassis_1` is legal despite never
being declared, while `light_tank_aa_chassis_99` is not - the allowance is bounded
rather than "any number after a known root".

`validate_stockpile_grants()` pins both halves across **all 6220 grants in the mod**,
not only the 2349 under `history/`. Two thirds live in `common/national_focus/` and
`common/decisions/`; scanning only `history/` would leave the blind spot where this
defect class returns. Six negative fixtures.

Nine ids are carried as a named, commented exception set because each names
something that is not equipment and each needs its content owner to say what was
meant. None is tank-designer owned: `mp_uav_1` (ISR), `apc_equipment_1` (PHI),
`manpads_3` (USA), `cv_nav_bomber_equipment_6` (JAP), and `armor_light`,
`armor_medium`, `artillery_light`, `artillery_medium`, `support_artillery` (PRC,
all technology categories used as equipment types). Recorded, not guessed at and
not deleted. Shrinking this set is a content task with an owner, not a validator
task.

## Carrier art

**Ratified 2026-09-08.** Carrier designs get **one static picture per hull tier**,
not per-design art. Per-design art was measured and is not available: the designer
icon compositor is an explicit tank-family graphics contract keyed on enumerated
profile sprites in `interface/tank_profiles.gfx`, not a generic consequence of an
equipment having module slots. Vanilla `super_heavy_artillery_equipment_1` inherits
`module_slots` and still keeps a static archetype picture, and vanilla NSB gives
mechanized no generated icons at all. Do not reopen this as "wire the carriers into
the tank icon generator".

Each hull declares `picture = cwic_apc_chassis_N` / `cwic_ifv_chassis_N`, resolved
by the engine through `GFX_<picture>_medium`. Only the `_medium` sprite form is
registered, matching vanilla. The sixteen sprites point at the already-shipped
neutral `gfx/interface/technologies/apc_{N+3}.dds` and `ifv_{N+1}.dds` textures, so
a hull's production icon is the same art as its technology icon. Neutral mod art was
chosen over the equally complete USA and Soviet tech icon sets so no country's
artwork is baked into a shared chassis definition. No new, copied or renamed assets.

Consequence, accepted: every design on one hull tier shares one icon. `BTR-60P` and
`BTR-60PB` are both `apc_chassis_2` art.

## Naming and localisation

- Country-specific localisation is the naming authority over the consolidated file
  where they disagree. This is a project naming policy, not a claim about engine
  localisation precedence. TUR's country-specific ladder wins.
- ALB and MZB duplicate IFV3 keys select the first `BMP-1`, consistent with the
  surrounding tier progression. The duplicate `BMP-1P` source entries stay in
  provenance; legacy localisation is not edited.
- New names trim surrounding whitespace and transliterate diacritics to ASCII (NFKD).
  Literal variant names need no new localisation keys. No translation files change.
- Mozambique's source localisation uses the undefined tag `MBZ`; the registered tag is
  `MZB` (`common/country_tags/00_countries.txt:119`). The six corresponding preset
  guards use MZB, with MBZ source keys retained in provenance. No OOB request uses MBZ.
- Seven NSB requests used undefined `heavy_mechanized_equipment_1/3`. These are treated
  as spelling errors for `mechanized_heavy_equipment_1/3` and migrate to IFV tiers 0/2.
  A documented inference; mirrored non-NSB typos are deliberately outside the migration.

## Preset authoring

- All APC loadouts use the existing unarmed baseline modules. IFVs use their tier's
  autocannon plus the baseline fighting compartment, suspension, armor, gasoline engine,
  AP and HE ammunition. All fifteen slots are explicit, with zero engine/armor upgrades.
  `allow_without_tech` follows existing bookmark setup.
- These are **functional authored baseline designs carrying historical names**, not
  exact historical configurations and not calibrated frozen-envelope matches.
- Scope is the two bookmarks' chassis union (APC and IFV tiers 0-4), not future tier
  authoring. The 354 selected tier 5-7 pairs are preserved as `future_inventory` in the
  manifest, deliberately absent from bookmark creation until the bookmark/OOB chassis
  contract can expand coherently.
- National creation is split into ten per-hull helpers, and the caller **interleaves**
  national and generic creation for each ascending hull with each family contiguous.
  Calling all national tiers before all generic fallbacks would create an older generic
  design after a newer national one for tags with gaps, violating newest-only
  obsolescence. Shared per-chassis flags also prevent generic duplicate creation.
- Each national design requires NSB, its producer tag, its hull technology and an unset
  per-chassis creation flag. The historical initialization effect deliberately permits
  modules without separate technology checks, matching the established bookmark pattern.
- Touched country-history scripts that had a BOM have it removed; localisation BOMs are
  untouched.

## Special slot map

All named `tank_special_slot_N`. Do not introduce the obsolete `special_type_slot_N`
names in tank content - that collision with plane airframes is what made Computer/Radar
and Loading System both render as "Optics".

**Retired 15-position map.** Superseded in script on 2026-09-09; kept because the
shipped presets were authored against it and its tradeoffs are what the count limits
now have to reproduce. The 21-position map below is what exists today.

| Slot | Allowed categories | Tradeoff |
| --- | --- | --- |
| 1, 2 | Kinetic, chemical, missile or HE ammunition | Two ammunition choices |
| 3 | Aiming devices | Dedicated aiming/stabilization |
| 4 | Optics | Dedicated sight capacity |
| 5 | Ballistic/artillery computer or radar | Computing and radar compete |
| 6 | Manual loader assist, autoloader or artillery loader | One loading system |
| 7 | Passive or reactive protection | Additional armor choice |
| 8 | Passive, reactive or active protection | APS competes with another layer |
| 9 | Survivability, auxiliary mobility or smoke | Utility capacity |
| 10 | Secondary weapon, survivability, auxiliary mobility or smoke | Secondary weapon competes with utility |

All 18 existing special-module categories remain reachable on all three hull
archetypes. Existing category count limits remain in force. Player designs from before
the slot specialization may use now-ineligible placements - use fresh campaigns.

**Shipped 21-position map, ratified and implemented 2026-09-09.** Five mandatory slots
plus `tank_special_slot_1..16`, on all five archetypes.

| Slot | GUI label | Allowed categories |
| --- | --- | --- |
| mandatory x5 | Gun, Turret, Suspension, Armour, Engine | unchanged |
| 1 | AP Ammunition | `tank_ammo_kinetic`, `tank_ammo_chemical`, `tank_ammo_missile` |
| 2 | HE Ammunition | `tank_ammo_he` |
| 3 | Aiming | `tank_fcs_aiming` |
| 4 | Optics | `tank_fcs_optics` |
| 5-16 | Slot 1 - Slot 12 | the twelve categories with no dedicated slot: `tank_fcs_computer`, `tank_fcs_radar`, `tank_loader_manual_assist`, `tank_loader_autoloader`, `tank_loader_artillery`, `tank_protection_passive`, `tank_protection_reactive`, `tank_protection_active`, `tank_survivability`, `tank_mobility_auxiliary`, `tank_smoke`, `tank_secondary_turret` |

Free slots deliberately exclude the four dedicated categories, so one AP round, one HE
round, one aiming device and one sight remain structurally enforced without a limit.
A category authored later must be added to this list **and** to the count limits in the
same edit, or it silently stacks - and, once the per-hull lock model exists, to the
eligibility map as well.

Exclusivity was to move from slot restriction to shared budgets, preserving the current
tradeoffs. Every budget below is what the retired specialized layout enforced, so this
would be a re-expression, not a rebalance:

| Group | Budget |
| --- | --- |
| `tank_fcs_computer` + `tank_fcs_radar` | 1 |
| `tank_loader_manual_assist` + `tank_loader_autoloader` + `tank_loader_artillery` | 1 |
| `tank_protection_passive` + `tank_protection_reactive` + `tank_protection_active` | 2 |
| `tank_survivability` + `tank_mobility_auxiliary` + `tank_smoke` | 2 |
| `tank_secondary_turret` | 1 (already `count < 2`) |

**Not shipped, and still contingent on the multi-category `module_count_limit` test.**
The per-category `count < 2` fallback shipped instead. The consequence is exact and
recorded: the four one-per-group tradeoffs above survive, because each of those groups'
members reduces to one pick anyway, but the two budget-2 groups do not - a design may
now mount all three protection categories and all three utility categories rather than
two of each. That is the balance debt the expansion created.

**The sketch's special-module list is 8 shipped families and 10 unbuilt ones.** Shipped
today, all in `common/units/equipment/modules/00_tank_modules.txt`: Belt Autoloader
(`Loader_4a/4b/4c_Belt`), Active Protection (`APS_0_H..3_H`, `APS_0_S..1_S`), ERA
(`ERA_0`, `ERA_1`, `ERA_L`, `ERA_2`, `ERA_3`), External Additional Armour (`Addon_0_Comb`,
`Addon_1..4_NERA`, `Addon_0/1_CE`), Auxiliary Power Unit (`APU_0..6`, `GT_APU_0..3`),
ATGM (`tank_atgm_launcher_cannon`, `gl_atgm_0p..3p`, `h_atgm_0..4`), smoke launchers
(`Smoke_0`, `Smoke_ESS`, `Smoke_1..4`) and thermal sights (`Optics_4..7`, category
`tank_fcs_optics`). 145 special modules exist across the 18 special categories.

Unbuilt - no module, no technology, no balance row: Blow-Out Panels, Anti-Mine Plow
(and rollers), External Additional Fuel Tanks, Unmanned Turret / RWS, Underwater
Driving, Integrated Trench Plow, Modular Construction, amphibious drive, dozer plough,
and night vision I-III. Drawio page 11 `[STATUS]` states it verbatim: "`[TODO] Base &
Other Tech Modules - RWS I-III, blow-out panels, unmanned turret, anti-mine ploughs and
rollers, dozer plough, external fuel. None exist in script.`" The workbook carries rows
only for the Belt/ERA/APS/APU/ATGM families, and its `Night & Thermal Vision Effects`
tab has zero non-empty rows, so every unbuilt family's numbers are invented and fall
under the existing "recorded as authored" rule. "Bulldozer" is the owner's word for the
sketch's `Dozer Plow`; there is no separate module. `night_vision` exists only as an
orphan tag at `common/technology_tags/00_technology.txt:42`.

Each unbuilt family needs a category decision as well as numbers: some fit existing
categories (external armour -> `tank_protection_passive`), others have none (external
fuel, mine/trench ploughs, unmanned turret, amphibious drive). A new category is cheap
in a free slot but must be added to an exclusivity group and to a count limit in the
same edit, or it silently stacks.

## Module balance, ratified 2026-09-05

| # | Question | Outcome |
| --- | --- | --- |
| 5.3.1 | Reliability expressed two ways | **Kept split.** Guns use a negative multiplier, turrets a positive flat add. Units genuinely differ; converting would touch 13 blocks for cosmetic consistency. |
| 5.3.2 | `cwic_hull_mg` flat `defense = 0.5` | **Reduced to 0.25.** Script, CSV and both workbook tables updated. |
| 5.3.3 | Secondaries lacked reliability cost | **All four now carry one:** coax -0.005, hull MG -0.005, HMG -0.01, autocannon -0.025 unchanged. |
| 5.3.4 | Turret cost ordering | **LP premium kept, 1.5 tie broken.** `oscillating_turret` 1.5 to 1.75, dismantling 0.75 to 0.875, preserving the file-wide 0.5 ratio. |
| 5.3.5 | 12 of 15 sub-units `active = yes` | **Normalised to `active = yes`, not `no`.** The manual's recommendation was wrong: legacy `armor.txt` enables only `light_armor`, `medium_armor`, `heavy_armor`, `super_heavy_armor`. The 9 role brigades and 3 flame tanks are enabled only by `nsb_iw_armored_vehicles`, so in a non-NSB profile `active = yes` is the sole thing making them buildable. Setting them to `no` would have deleted them from non-NSB play. The validator contract was inverted to match. |
| 5.3.6 | `tank_gasoline_engine` home, missing `xp_cost` | **Base engine, not a duplicate.** It is `Petrol_0`'s declared parent and the `engine_type_slot` default at `tank_chassis.txt:391, 795, 1200`. Gains `xp_cost = 1` and `dismantle_cost_ic = 0.5`. |
| 5.3.7 | Base gasoline engine speed ordering and preset baseline | **Rebalanced and rerouted.** `tank_gasoline_engine` remains the script-owned pre-WW2 base module and `Petrol_0` remains its child/starting template. Its `maximum_speed` multiplier is 0.03, below `Petrol_0` at 0.05. The living CSV and frozen-workbook validator override are updated. The 576 national and 40 generic preset references in the two scripted effects now use `Petrol_0`; the four USA manifest entries are synchronized. `tank_gasoline_engine` localisation is "Pre-WW2 Gasoline Engine". |
| 5.3.8 | Major-country `Petrol_1` bootstrap | **Implemented 2026-09-09.** `nsb_engines0` is granted to USA, SOV, FRA, ENG and WGR. Generic fallback recipes remain on `Petrol_0`; only USA's tag-exclusive 1950 `M47 Patton` reroutes to `Petrol_1`. |
| 6 | Research cost curve | **Ratified and applied.** R1-R7; 91 of 169 technologies repriced; 337 to 345.5 (+2.52%); USA/SOV 1970 -1.67%, 2020 +8.33%. |
| 6 | XP economy | **Flat at 1, deliberate.** No repricing. Closed. |

**Conventional turret balance.** Authored in response to QA: conventional turret gets
+5% breakthrough for an extra 0.5 IC. Light turret remains the inexpensive option.
Reliability unchanged. This is a limited cost-versus-breakthrough choice, not a
turret/weapon-size eligibility redesign.

| Field | Frozen workbook | Revised conventional | Light turret |
| --- | --- | --- | --- |
| Build cost IC | 1 | 1.5 | 1 |
| Additive reliability | 0.15 | 0.15 | 0.15 |
| Breakthrough multiplier | absent | +0.05 | absent |
| Dismantle cost IC | 0.5 | 0.75 | 0.5 |

The CSV carries the revised row. The validator checks that row against the script, the
workbook against the old values, and the revised turret against its numeric contract.
These are the only cross-source exceptions.

## Static QA dispositions, 2026-09-08

The bounded owner-QA review is resolved at source level without a balance redesign:

- USA and SOV 1980 dated history already call
  `cwic_major_tank_research_1980`. Its two DLC branches and exact technology set
  are validator contracts; no second country-history research convention is added.
- The reported 1985 ahead-of-time cases already use matching `start_year` and
  `@1985` rows. The source contains no missing-date defect, so no technology dates
  are changed.
- The Light/Conventional Turret difference is intentional: the former is the
  1 IC option and the latter buys +0.05 breakthrough for 1.5 IC.
- `Radar_1`'s script values match both balance sources. A displayed `-0` supply
  value is a runtime tooltip-precision issue, not a balance correction.
- Focus exports are internal obsolete designs: every helper is hidden and marked
  obsolete, while startup national and generic designs use the existing
  newest-only obsolescence marker. No focus effect names or creation order change.

These are static dispositions only. Live tooltip, production-tab, bookmark and
balance acceptance remain unverified.

## QA findings that are not transcription errors

- **Gun-Launched ATGM III (`gl_atgm_2p`)** has additive hard attack 95, soft attack 5.5
  and piercing 600 in **both script and workbook**. Heavy ATGM values are likewise
  covered by the module balance report. Matching the source does not establish that the
  finished vehicle is balanced; missile/gun interactions need live calibration before
  imposing a new scale.
- **Radar II (`Radar_1`)** has additive fuel use 1.2, supply-use multiplier -0.075,
  air-attack multiplier +0.25 and reliability multiplier -0.05. These match the
  workbook. The screenshot's supply use rounded to `-0.0` is display precision, not a
  zero in the module definition. Verify application and tooltip precision live before
  changing balance to address a display symptom.

## Retracted after measurement - do not reopen

- **The AA and flamethrower sprites are not broken.** `tank_module_aa_gun{,_2,_3}.dds`,
  `tank_module_flamethrower.dds`, `EMI_tank_flamethrower.dds` and `Niche_icon_strip.dds`
  all exist in the base game under
  `gfx/interface/equipmentdesigner/tanks/{modules,icons}/`, which the mod does not
  shadow. HOI4 resolves sprite paths mod-first then vanilla, and the live error.log
  shows zero texture misses. Checking only the mod directory produced the false positive.
- **`nsb_armor_modules_folder` is not missing a year column.** Labels sit at
  x=20/1450/3100 against trees at x=428/1950/3600 - one per tree. The `nsb_armor`
  folder's fourth label at x=4000 is the anomaly.
- **The designer role group does not wrongly overlay `equipment_preview`.**
  `design_company_icon` and `design_team_button` at (461,382) sit inside the same
  preview rectangle, so floating icons over the blueprint is the panel's existing layout
  language. `tag_icon_bg` 465 to 461 and `niche_button` 474 to 470 aligned the group to
  the x=461 rail; the defect premise did not survive measurement.
- **Duplicate production listing of a carrier is working as intended.** See
  `REFERENCE.md`.
- **Two `completion_reward` blocks did not cause the empty `BUL_Soviet_T55s` award.**
  See `STATUS.md` Finding 1.

## Known inconsistencies - recorded, not scheduled

1. Granting flame chassis does not make the AI build them; no AI division template
   fields a flame battalion. Needs `common/ai_templates/` work.
2. Secondary armament competes for the special slots, and the workbook envelopes were
   computed without it.
3. Two parser families live in the validator - the doctrine work added a bounded parser
   while the tank half uses older near-duplicates. Do not add a third; reuse and delete.
   Partially paid down 2026-09-08: the lenient brace scanner is now the single
   `located_keyed_blocks`, with `keyed_blocks` and `stockpile_grants` as thin views
   over it. The bounded/lenient split itself remains.
4. Turret modules have no `xp_cost` while every other module family does.
5. 14 abbreviation collisions across 60 modules, including all ten light gun tiers
   sharing `tanklightc`. Variant auto-naming cannot distinguish a 1939 gun from a 2015
   one. Cosmetic, but it touches every armor design ever produced.
6. `main_armament_slot = empty` in `default_modules` despite `required = yes` on all
   three archetypes, which is why a fresh design opens with no gun. Probably
   intentional, but it is the first thing a player sees.
7. Legacy orphan archetypes `lt_equipment`, `mbt_equipment`, `ht_equipment` are declared
   but nothing targets them. Harmless, confusing.
8. The artillery tree is entirely NSB-unaware: 85 techs in an unconditional
   `artillery_folder` granting zero designer modules, running in parallel with the
   designer every game. The largest structural inconsistency in the system, and
   deliberately out of scope - record it, do not start it.
9. `derived_variant_name` targets do not exist in script; `light_tank_equipment_0` and
   friends are generated at runtime. Correct NSB behaviour, but it means no script can
   reference them.
10. Bookmark variants use concrete module ids (`ap_0p`, `tank_he_0p`) while AI recipes
    use categories (`tank_ammo_kinetic`, `tank_ammo_he`). Both correct; the asymmetry
    misleads. The claim that "the three SPAA variants deliberately carry no ammunition
    because AA guns supply their own attack" is **superseded as of 2026-09-09**: the
    owner reversed that rule, `tank_aa_ammo_1..3` exist in `tank_ammo_he` restricted to
    `allow_equipment_type = anti_air`, all three SPAA variants now mount tier 1, and the
    validator requires it. Flamethrowers remain self-supplying and exempt.
11. `sp_tag_tank_speed_factor` is an invalid modifier in
    `common/dynamic_modifiers/wuw_dynamic_modifiers.txt` - one live log error,
    tank-adjacent, trivial, unowned.
12. `common/national_focus/PHI_1950s.txt:587` grants `apc_equipment_1`, which is not an
    equipment id anywhere in the repo, so the focus silently awards nothing.
    `apc_equipment_1` exists only as the `derived_variant_name` of `apc_chassis_1`,
    which is a localisation key rather than an equipment type. Predates the APC work.
    Most likely wants `mechanized_equipment_3`, or a designer APC. Flagged for whoever
    owns PHI.
    Now also carried in `STOCKPILE_TYPE_EXCEPTIONS`, alongside eight sibling grants
    the mod-wide stockpile contract found in ISR, USA, JAP and PRC content.
