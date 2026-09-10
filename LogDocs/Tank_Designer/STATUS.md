# Status

Branch `tank-designer-and-doctrine-rework-test`. Last updated 2026-09-09.

## Where the project stands

Tier 1 and Tier 2 of the original completion plan are shipped and stable. The APC and
IFV designer families are built, validated and accepted in live QA. Bookmark presets
and the NSB OOB migration are committed.

**The designer itself is not finished, and that is the headline.** The module set and
the designer GUI stop at 15 of the 21 designed positions, and ten of the sketch's
special-module families have no script at all. Finding 6 records the gap; `DECISIONS.md`
carries the ratified 21-position architecture. What remains is that expansion,
historical coverage, three QA findings, and the deferred content batches.

### Committed checkpoints

| Commit | Change |
| --- | --- |
| `a997a48e0e` | Tools moved under `CWIC Backup/tools/`; root `tools/` paths are stale |
| `368fa4815c` | All ten tank special slots renamed `tank_special_slot_1..10`, avoiding plane localisation collisions |
| `b2cd5694b9` | `zz_CWIC_armor_entity_aliases.asset` (3,019 aliases) replaces the old level-0-only file |
| `88c94a5b1c` | Fourteen USA/SOV national medium presets, producer-aware OOB names, duplicate guards, module estimator correction |
| `80304e2030` | Newest bookmark design only in the default production tab |
| `660f8984ae` | APC designer family |
| `faddc3dd5e` | IFV designer family |
| `eb708e3691` | APC/IFV bookmark presets and NSB carrier OOB migration (Step 2) |

### Step 2 acceptance, 2026-09-08

Owner QA passed and committed. Both bookmarks load, presets load, stockpiles and
factory lines exist, `error.log` is acceptable. AI production is deferred to a single
final pass once the remaining designer content is in, at the owner's direction.

The batch added 10 generic carrier designs, 572 national carrier designs and 100 named
carrier OOB requests over the `faddc3dd5e` baseline. Bootstrap site count unchanged at
76: the carrier grants land inside the existing sites.

Two failures the first gate run reported, both resolved:

1. **Global design-name uniqueness was the wrong invariant.** It produced 382 false
   `duplicate tank recipe name` failures. A design name is only unique *per country*,
   and ten names legitimately span two chassis tiers because an incomplete national
   ladder shifts a vehicle relative to the common ladder. `_variant_recipes()` is now
   keyed by `(name, chassis)`; `_variant_recipes_by_name()` marks a name ambiguous
   rather than silently keeping the last recipe.
2. **Three medium-tank OOB requests contradicted the producer-resolution rule.** They
   named a generic design with SOV as creator, and SOV creates national names at every
   medium tier. Resolved by naming the Soviet design: `KPA_1949_nsb.txt:594` to
   `T-34-85` (historically correct), `BUL_1949_nsb.txt:183,193` to `T-44` (Bulgaria did
   not field T-44s; the request's chassis tier, not the name, is the ahistorical part).
   These were latent breakage, not a regression.

## Open findings

### Finding 1: legacy armour focus awards were never migrated to NSB designer equipment - resolved 2026-09-08

Reported case: `BUL_Soviet_T55s` shows no completion award though it should grant 200
`mbt_equipment_3` from CUM.

Confirmed cause, and it is our own NSB designer change rather than a focus scripting
bug: every legacy armour equipment entry is reparented onto a designer archetype.
`tank_medium.txt` puts all 10 `mbt_equipment_*` on `archetype = medium_tank_chassis`,
and `tank_heavy.txt` (5), `tank_light.txt` (6) and `mechanized.txt` (18) do the same.
So `add_equipment_to_stockpile = { type = mbt_equipment_3 producer = CUM }` names
equipment that now belongs to a designer family with no design behind it for that
producer. Nothing is granted; the reward renders empty.

To be explicit, because an earlier draft got this wrong: **two `completion_reward`
blocks in one focus is not the cause here.** That pattern is a real and separate
issue - see `GOTCHAS.md` - but it is not what `BUL_Soviet_T55s` demonstrates.

Scope owed: **301 `add_equipment_to_stockpile` grants across the focus trees name a
legacy armour type, and all 301 specify a producer.** They span 22 distinct types, led
by `mbt_equipment_3` (57), `mbt_equipment_2` (44), `lt_equipment_2` (31),
`mbt_equipment_0` (30), `ht_equipment_3` (25) and `mbt_equipment_1` (24), plus 28
mechanized/heavy-mechanized grants. Heaviest files: `60s_Generic.txt` (41),
`60s_ITA.txt` (26), `60s_SOM.txt` (26), `60s_VIE.txt` (26).

Each grant needs a decision, not a mechanical rename: which designer chassis and which
named design the awarding producer hands over, on both the NSB and non-NSB profiles.
The carrier presets are the model - same producer-resolution rule, same named national
designs. This wants a validator contract pinning every focus armour grant to a design
some bootstrap creates, exactly like the OOB `force_equipment_variants` check.

Resolution: every active, in-scope legacy armour grant now keeps its original
non-NSB branch and gains an NSB branch that creates an obsolete producer-owned
export design before granting the matching chassis variant. The mapping uses the
largest designer chassis whose ratified introduction year is no later than the
legacy equipment year. This pass added 314 migrations; 9 existing export branches
were retained. The validator now checks all 323 in-scope grants, their chassis and
variant pairs, producer helper calls, and the 8 intentional equipment-type exceptions
(16 grants).

The 11 explicitly reference-only focus paths remain outside this contract:
`FOR HOTFIX/`, `Need Finished/`, `OUTDATED_PRC_60s.txt`, `Old/`, `Toberemoved/`,
and `Trees for 0.35/`. Static validation passed; no live QA or balance acceptance
is claimed for this migration.

Deferred follow-up: the migrated NSB focus effects currently use generic
`CWIC Export ...` `variant_name` values rather than historical preset variants.
This is immersion-breaking and does not track the legacy equipment identity.
Another session must research and map each focus effect/equipment grant to its
historical variant counterpart. This is intentionally deferred because the
research cost is high; no mapping is implemented in this pass.

### Finding 2: base gasoline engine outranked the CWIC petrol ladder - resolved

The script-owned `tank_gasoline_engine` was the `Petrol_0` parent and the default
engine slot, but its `maximum_speed` multiplier was 0.15, above every CWIC petrol
tier (`Petrol_0` 0.05, `Petrol_1` 0.07, `Petrol_2` 0.09, `Petrol_3` 0.11). It is
enabled by the base NSB armour tech (`NSB_armor.txt:63`); `Petrol_0` remains gated
at `NSB_armor.txt:1074`.

The ladder is corrected in place: `tank_gasoline_engine.maximum_speed` is 0.03,
below `Petrol_0` at 0.05. The module remains the pre-WW2 parent/base definition;
`Petrol_0` is the starting template. The English localisation now calls the former
"Gasoline Engine" **"Pre-WW2 Gasoline Engine"**.

Every tank-bootstrap country-history site grants `nsb_engines`, so `Petrol_0` is
available through the same starting-tech contract. The two scripted effects now route
all 576 national and 40 generic starting variants to `Petrol_0`; the four USA
manifest entries are synchronized. The three archetype default slots elsewhere remain
`tank_gasoline_engine` under the existing parent/default decision and were not changed
by this scoped preset migration.

The full static report passes with the inventory line unchanged. Relative to the
previous engine-only report, the 11 sampled tank envelope estimates changed as
follows (`speed`, `fuel_usage`):

| Recipe | Speed | Fuel |
| --- | ---: | ---: |
| Heavy Tank I | -3.13 -> -2.59 | -2.45 -> -2.02 |
| Heavy Tank II | -2.69 -> -2.14 | -2.45 -> -2.02 |
| Heavy Tank IV | -3.25 -> -2.69 | -2.45 -> -2.02 |
| Heavy Tank V | -3.81 -> -3.24 | -2.45 -> -2.02 |
| WWII Tank 1 | -4.07 -> -3.51 | -1.45 -> -1.02 |
| WWII Tank 2 | -4.63 -> -4.06 | -1.45 -> -1.02 |
| MBT II | -5.19 -> -4.61 | -1.45 -> -1.02 |
| MBT III | -5.75 -> -5.16 | -1.45 -> -1.02 |
| Light Tank I | -5.02 -> -4.43 | 0.35 -> 0.78 |
| Light Tank II | -5.58 -> -4.98 | 0.35 -> 0.78 |
| Light Tank IV | -7.70 -> -7.08 | 0.35 -> 0.78 |

These are diagnostic estimates only; no live balance acceptance is claimed.

### Finding 3: presets show the generic carrier icon - resolved 2026-09-08

`BTR-40` rendered with the generic APC picture. `apc_chassis_*` and `ifv_chassis_*`
declared no `picture` of their own, so every carrier design inherited
`archetype_motorized_equipment` from the `mechanized_equipment` archetype
(`mechanized.txt:11`) and `archetype_mechanized_heavy_equipment` from
`mechanized_heavy.txt:12`.

Stats are the good news: the owner confirms legacy and new NSB APC/IFV stats match
closely, so the module baselines are landing where they were aimed.

Per-design art was measured and rejected, not skipped. The designer icon compositor
is an explicit tank-family graphics contract, not a generic consequence of having
modules: vanilla `super_heavy_artillery_equipment_1` has `module_slots = inherit`
and still keeps its static archetype picture, and vanilla enumerates profile art as
`GFX_<tag-or-generic>_<size>_<profile>` in `interface/tank_profiles.gfx` with no
mechanized family. Vanilla NSB gives mechanized no generated icons either.

Resolution: one static picture per hull tier. Each of the sixteen hulls declares
`picture = cwic_apc_chassis_N` / `cwic_ifv_chassis_N`, and sixteen matching
`GFX_..._medium` sprites in `interface/cwic_tank_rework_icons.gfx` point at the
already-shipped neutral `gfx/interface/technologies/apc_N.dds` and `ifv_N.dds`
textures - the same art the corresponding hull technology icon uses, so the tech
tree and the production tab agree. Zero new, copied or renamed assets. The
validator pins the picture value, sprite registration and texture existence per
hull, with four negative fixtures.

This is a per-hull-tier icon, not per-vehicle: every APC tier-2 design still shares
one picture. That limit is now a recorded consequence of the engine's graphics
contract rather than an open question. Static verification only; the rendered icon
has not been confirmed in game.

### Finding 4: major-country Petrol_1 bootstrap is deferred

`nsb_engines0` enables `Petrol_1`, starts in 1950, costs 2 research, and is not
granted by any country history. USA, SOV, FRA, ENG and WGR grant `nsb_engines` in
their NSB starting-tech blocks but do not grant `nsb_engines0`. Current historical
medium-tank national presets exist only for USA and SOV; FRA/ENG/WGR/JAP appear in
carrier paths, not this medium-tank ladder.

Recommendation: keep `Petrol_0` as the universal starting preset engine. Do not add
major-country `nsb_engines0` grants or `Petrol_1` routing until a country/tier
historical mapping and balance contract exists. This is an open design item, not
implemented in this pass.

### Finding 5: stockpile grants silently awarded nothing - resolved 2026-09-08

Found by triaging the four owner playtest logs, then re-confirmed against current
source. Three shapes, all of which parse as valid script and award nothing:

1. **`creator` on `add_equipment_to_stockpile`.** The effect accepts `type`,
   `amount`, `variant_name` and `producer` only. The engine logs
   `effect.cpp:358 Unexpected token: creator` and drops the grant. 246 grants
   carried it: 121 in `SOV_1980_nsb.txt`, 121 in `SOV_1980.txt`, 4 in
   `SWI_1980.txt`. The Soviet block is the entire 1980 armour and aircraft
   stockpile for both profiles, so both bookmarks started with none of it.
   `creator` stays legal and untouched on `force_equipment_variants` and
   `add_equipment_production`, which is why the token looked right.
2. **Transposed equipment ids.** `heavy_mechanized_equipment_1`/`_3` are not
   defined anywhere; the real ids are `mechanized_heavy_equipment_1`/`_3`. Seven
   grants across CUB, DDR, POL, CZE, ISR, TUR and HUN `_1980.txt`. The `_nsb`
   counterparts were already migrated to designer chassis in `eb708e3691`; only
   the non-NSB mirrors were left, and `DECISIONS.md` had recorded them as out of
   the *designer migration*, which is not the same as leaving a dead id in place.
3. **Misspelt and mistyped ids.** `infnatry_eqipment_1` in DOC, TOG and UGA
   `_1980.txt`. Each logs `invalid database object for effect/trigger`.

Also corrected in the same file, both engine-confirmed dead `add_tech_bonus`
categories: `BRA_50s.txt:3601` used `mechanized_equipment` where the declared
category is `cat_mechanized_equipment`, and `BRA_50s.txt:3564` used
`infantry_equipment` where four sibling mod focuses use `infantry_weapons`. Both
bonuses previously applied to nothing.

`validate_stockpile_grants()` now pins all **6220 stockpile grants mod-wide**, not
just the 2349 under `history/` - two thirds live in `common/national_focus/` and
`common/decisions/`, and a blind spot there is exactly where this defect class
would return. It requires no `creator` key, and every `type` must resolve to a
declared equipment id or to a tier its parent family actually declares behind a
`duplicate_archetypes` root, so `light_tank_aa_chassis_1` passes while
`light_tank_aa_chassis_99` does not. Six negative fixtures cover the rejected key,
a transposed id, a technology id used as equipment, the valid derived tier, a
deregistered carrier sprite and a carrier sprite pointing at a missing texture.

The wider scan surfaced nine pre-existing content bugs that are not
tank-designer-owned and that each need their content owner to say what was meant.
They are carried as a named, commented exception set rather than guessed at or
deleted:

| Id | Sites | What it actually is |
| --- | --- | --- |
| `mp_uav_1` | `ISR_1980{,_nsb}.txt:486` | technology in `helicopter.txt` |
| `apc_equipment_1` | `PHI_1950s.txt:586` | `derived_variant_name` only; see known inconsistency 12 |
| `manpads_3` | `USA_80s_CIA.txt:1850,1872` | undeclared |
| `cv_nav_bomber_equipment_6` | `JAP_1950s.txt:437` | undeclared |
| `armor_light`, `armor_medium`, `artillery_light`, `artillery_medium`, `support_artillery` | `PRC_50s_New.txt:2489-2509` | technology categories used as equipment |

Five further invalid `add_tech_bonus` categories appear in the logs outside
`BRA_50s.txt` and were left alone: `air_techs`, `electronic_mechanical_engineering`,
`excavation_tech`, `screen_hull_light`, and `radio` at `BRA_50s.txt:1041`. `radio`
is in a file this pass edited but its correct target is a content judgement - the
declared `radio_tech` category carries exactly one technology - so it was recorded
rather than guessed.

Static verification only.

### Finding 6: the designer module set and GUI are unfinished - 15 shipped against 21 designed

Recorded 2026-09-09 at the owner's direction, because nothing in this folder said it
out loud: the shipped designer is two thirds of the designed one, and the difference
was previously filed as a rejected sketch rather than as owed work.

**Shipped.** Five mandatory slots plus `tank_special_slot_1..10`, every special slot
specialized to a fixed category list, on all five archetypes: `tank_chassis.txt:16-152`
(light), `:271-411` (medium), `:522-660` (heavy), `mechanized.txt:37-164` (APC),
`mechanized_heavy.txt:28-42` (IFV). The GUI declares
`pos_custom_module_slot_window_0..14` at `interface/tank_designer_view.gui:129-215`, and
the validator pins exactly that set at `validate_military_reworks.py:3826-3829` while
printing the literal `15 designer slots` at `:4646-4647`.

**Designed.** 21 positions: drawio page 8 `[REFERENCE] Tank Designer Composition` lays
out Gun, Turret, AP Ammo, HE Ammo, Aiming, Optics, Suspension, Armour, Engine plus
`Slot 1..12`, with a candidate special-module row beneath it. The owner's screenshot is
that page over a designer capture, not a render of current code.

**The gap is two things, and only one of them is the slot count.**

1. Six missing positions and a semantic change: the sketch dedicates AP and HE
   ammunition, aiming and optics, and leaves the other twelve free. The architecture,
   GUI layout, exclusivity model, migration cost and its two unverified engine
   assumptions are ratified in `DECISIONS.md`.
2. Ten of the sketch's eighteen named specials have no module, no technology and no
   balance row: Blow-Out Panels, Anti-Mine Plow and rollers, External Additional Fuel
   Tanks, Unmanned Turret / RWS, Underwater Driving, Integrated Trench Plow, Modular
   Construction, amphibious drive, dozer plough, night vision I-III. Eight families
   from that row do exist (belt autoloaders, APS, ERA, add-on armour, APU, ATGM, smoke,
   thermal sights) - 145 special modules across 18 categories. Drawio page 11 already
   said "None exist in script"; the workbook's `Night & Thermal Vision Effects` tab is
   empty, so all ten families need invented numbers recorded as authored.

**Blast radius, measured.** The expansion is small in content and concentrated in the
validator, because unused optional slots may be omitted from a creation block
(vanilla `GER - Germany.txt:1097-1108`):

| Surface | Count | Needs rewriting? |
| --- | --- | --- |
| Archetype slot blocks | 5 | Yes - six new slots, four re-specialized, exclusivity groups |
| GUI positions | 15 -> 21 | Yes - six positions, one promoted row macro |
| Validator sites | 11 functions/constants | Yes - see the edit list in `DECISIONS.md` |
| National preset blocks | 586 (8,790 special assignments) | No - already-explicit 15 stay legal |
| Generic bookmark blocks | 40 (160 special assignments) | No |
| Focus export blocks | 16 (80 special assignments) | No |
| AI recipes in `generic_tank.txt` | 116 | No, unless a recipe wants a new special |
| Slot localisation keys | 15 -> 21 | Yes - twelve free-slot labels |

**The two gating engine assumptions are now answered.** Positions above 8 work: the
owner's 2026-09-09 designer capture renders the 7 / 7 / 7 layout with the middle row
over the blueprint exactly as ratified, and the top row reads turret, gun, suspension,
armour, engine, AP ammunition, HE ammunition - confirming both the 21-position layout
and the slot 1 / slot 2 ammunition split in game. The multi-category
`module_count_limit` shared budget was **not** authored: `DECISIONS.md` forbids it
before a positive engine test, and a log diff can only disprove such a block, never
confirm its enforcement. The ratified per-category `count < 2` fallback shipped
instead, so the envelope recalibration below is now owed rather than hypothetical.

**Implemented 2026-09-09.** Phases 1 and 2 are done and statically verified; the
self-test line moved from `15 designer slots checked` to `21 designer slots checked`
with every other count byte-identical.

- All five archetypes declare `tank_special_slot_1..16`. Slot 1 is AP ammunition
  (`tank_ammo_kinetic`, `tank_ammo_chemical`, `tank_ammo_missile`), slot 2 is
  `tank_ammo_he`, slots 3 and 4 are unchanged, and slots 5-16 share one 12-category
  free list. `tank_chassis.txt`, `mechanized.txt`, `mechanized_heavy.txt`.
- Each archetype now carries all 18 single-category `count < 2` limits. APC and IFV
  were missing seven (four ammunition, three loader). Those three loader limits are
  load-bearing: without them a twelve-free-slot carrier could mount three loading
  systems.
- `interface/tank_designer_view.gui` declares positions 0-20 at 7 / 7 / 7 with no
  geometry change - `equipment_modules` stays 515x350 and `equipment_preview` 508x248.
- Twelve free-slot labels added; slots 5-16 read `Slot 1`..`Slot 12`, slot 1 is
  "AP Ammunition" and slot 2 "HE Ammunition". The six retired specialized labels are
  gone.
- **A sixth surface the blast-radius table above missed:** the 106 per-hull blueprint
  files under `interface/equipmentdesigner/tanks/` enumerate the slot names by hand.
  All 106 declared only `tank_special_slot_1..10`, so the engine logged
  `containerwindow.cpp: Could not find "tank_special_slot_11" in window module_slots`
  plus a `Requested GUI element not found` assertion the moment a designer opened.
  All 106 now declare 1-16. This was found only by loading the game; nothing static
  pointed at it, which is why the validator now pins the file count and the exact
  ordered slot list per blueprint.
- Validator migrated off cardinality onto `variant_slot_errors()`
  (mandatory-complete plus specials-a-subset, per the vanilla precedent that optional
  slots may be omitted) and `tank_count_limit_errors()`. Eleven negative fixtures were
  added, including one asserting that a multi-category limit block is still rejected
  so the unverified form cannot be introduced by accident.

No preset, OOB, focus or AI-recipe content was edited, as predicted: the 8,790 + 160 +
80 already-explicit special assignments stay legal.

**Remaining plan.** Phases 1 and 2 are closed; these two are not.

3. *Module authoring*, in the order "Next scope" item 6 sets: amphibious (only with
   marine sub-unit supply), night/thermal vision, then the base/other specials. Each
   family needs a category decision, a per-hull eligibility decision, invented numbers
   recorded as authored, an unlock in `NSB_armor_modules.txt` and a `GFX_SMI_*` icon.
   The owner supplied the two source mockups on 2026-09-09 - see `DECISIONS.md` for the
   ladders they fix.
4. *Envelope recalibration.* Twelve free slots let a design mount more specials than
   the frozen envelopes assumed, and the shipped fallback does not cap the total. This
   is known inconsistency 2 in its full form now.

**The render is confirmed, 2026-09-09.** The owner re-checked in game after the
106-file blueprint fix and reports the 21 slots load correctly, on a T-54 /
`medium_tank_chassis_1` Late WW2 Medium Tank Hull. The live `error.log` corroborates
it: zero `Could not find "tank_special_slot_*"`, zero `Requested GUI element not
found`, zero `containerwindow.cpp` lines of any kind, with the designer open. The
pre-fix boot logged 85 slot-lookup failures plus the assertion, so this is a real
before/after and not an absence of evidence. Every one of the 21 positions resolves.

One cosmetic note, not a defect: in the captures the bottom row shows six `+`
affordances and a dark seventh cell. The engine resolves that element - it reports no
missing GUI element - and a `-debug` resolution overlay (`1600x900`, `x720`) is drawn
across exactly that area. Re-check without `-debug` if it ever matters visually.

**Owner direction, 2026-09-09: specialized slot restrictions must still be adjusted.**
21 slots on all five hulls is confirmed final, but slots are to be *locked per hull*
according to which specialized modules that hull may access - amphibious drive belongs
to APC and IFV and must not appear on the medium, MBT or heavy hulls. The shipped
state gives all five archetypes an identical free list, which is correct only while
every free-list category exists on every hull. The per-hull lock model must land in
the same pass as the first hull-restricted module, or that module silently becomes
mountable everywhere. See `DECISIONS.md`.

### Finding 7: the carrier bookmark validator was dead code and had never run - resolved 2026-09-09

Found while migrating the slot-cardinality sites. `validate_carrier_bookmarks()` in
`validate_military_reworks.py` was defined and **never called from anywhere**, and it
contained a reference to an undefined `SPECIAL_SLOT_CATEGORIES` on its per-slot
legality path - a guaranteed `NameError` that proves the function had never executed
once. So the entire Step 2 carrier contract the `eb708e3691` acceptance notes describe
as checked - 572-preset source coverage, the `MBZ -> MZB` alias, producer tag
existence, per-slot module legality, the per-guard creation contract, dispatcher
interleave order and the manufacturer-bloc technology ordering - was never enforced.

Wiring it in produced 36 failures, and every one was a validator defect rather than a
content defect. The function had been written against a design that was never shipped:

1. Its mandatory-slot category sets named `tank_suspension_type`, `tank_armor_type` and
   `tank_engine_type`, none of which exist anywhere in the mod. The real categories are
   per-type - `Armor_0_W` is `tank_armor_welded`, `Bogie_0` is `tank_suspension_bogie`.
   Now derived from each family archetype's own `allowed_module_categories` so the check
   cannot drift from the archetype again.
2. It passed raw effect files to the bounded block parser, which needs one balanced
   root, so all ten per-hull helpers and the dispatcher read as absent. The helpers and
   the shipped `cwic_create_starting_tank_variants` dispatcher were there all along.
3. Quoted values (`name`, `variant_name`, `version_name`) were fed to a parser that
   deliberately only reads unquoted atoms, and five 1949 production requests wrap their
   payload in `equipment = { ... }`, which the OOB inventory never looked inside.
4. Its recipe expected `tank_gasoline_engine`; the accepted shipped effects use
   `Petrol_0` per Finding 2's engine reroute.

All seven repaired check shapes were re-proven with in-memory mutation probes through
the function's existing `*_override` parameters, so nothing was loosened to make it
pass. Static verification only; this changes no mod content.

### Finding 8: a validator self-test run corrupts a live `-debug` game

Recorded 2026-09-09 because it cost most of an investigation cycle and will do so
again. `run_apc_negative_fixtures()` and `run_ifv_negative_fixtures()` write their
mutated fixtures to the **real** `mechanized.txt` and `mechanized_heavy.txt` paths and
then restore them. A `-debug` game hot-reloads changed equipment files, and the reload
re-registers every `module_count_limit` on top of the existing registry.

Symptom: 2380 `A limit for category X already exists` errors, 1480 of them in
`CWIC_ship_hull_*.txt` files that no one had touched, appearing 90 seconds after load
finished in ten identical bursts - one per re-parse. It reads exactly like a global
engine limit being blown by the slot expansion, and it is not. A clean boot with the
expansion in place and no concurrent validator run reports zero.

**Never run the validator while a `-debug` game is loading or running.** The A/B that
settles any suspected engine regression must hold file writes still on both arms.
### Finding 9: the per-hull slot lock does not need a slot mechanism - the engine already has one

Recorded 2026-09-09 while planning the owner's per-hull lock direction, and it changes
the shape of that work. Restricting a module to certain hulls **cannot** be done through
the free-slot category lists, because a category is shared by all five archetypes - the
free list is per archetype, but a category is global, so putting amphibious drive in
`tank_mobility_auxiliary` makes it legal on any hull whose free slots accept that
category.

The engine's own primitive is module-side and already in use. Vanilla's
`amphibious_drive` at
`<steam>/Hearts of Iron IV/common/units/equipment/modules/00_tank_modules.txt:1372-1397`:

```
category = tank_special_module
allow_equipment_type = amphibious
forbid_equipment_type_exact_match = armor
forbid_equipment_type = { anti_air artillery anti_tank flame }
```

`allow_equipment_type` / `forbid_equipment_type` / `forbid_equipment_type_exact_match`
key off the archetype's own `type = { ... }` set, and the mod's module file already uses
those keys **49 times**. The designer role roots supply exactly the discriminators
needed: `x_tank_chassis.txt:8-15` declares `light_tank_aa_chassis` as
`type = { armor anti_air }`, `:18-25` gives `light_tank_artillery_chassis`
`type = { armor artillery }`, and the APC and IFV archetypes carry `mechanized`
alongside `armor`.

So the lock model is: author the hull-restricted module into an existing category, then
bound it with `allow_equipment_type` / `forbid_equipment_type`. No new slot, no GUI
change, no fifth copy of a category list, and no per-archetype divergence in the free
list. The one open question is what type token distinguishes an APC/IFV from a gun tank
for amphibious purposes - `mechanized` is the obvious candidate and must be confirmed
against the archetype `type` sets before authoring.

### Finding 10: `APU_6` is an orphan module with no unlock

`APU_6` is declared at
`common/units/equipment/modules/00_tank_modules.txt:4024-4038` with
`category = tank_mobility_auxiliary` and the strongest stats in its family
(`breakthrough = 4`, `defense = 4`, `build_cost_ic = 4`, `reliability` +0.06,
`fuel_consumption` -0.3). No `enable_equipment_modules` block anywhere in
`NSB_armor.txt` lists it: the ladder grants `APU_0` at 1940, `APU_1` 1950, `APU_2` 1960,
`APU_3` and `APU_4` together at 1980, and `APU_5` at 2000, then stops. So the top APU
tier is unreachable in play. Either it wants a 2020 grant beside `Diesel_5`'s
`nsb_engines3` tier, or it is a leftover and should be deleted. Not tank-designer
urgent, but it is a real dead end and the validator does not currently notice orphaned
modules.

### Finding 11: one missing `=` crashed every tank designer - resolved 2026-09-09

Owner-reported: the tank, APC and IFV designers all crashed on open. Cause found in the
log, not guessed:

```
Error: "Malformed token: positionType, near line: 143" in file: "interface/tank_designer_view.gui"
```

`interface/tank_designer_view.gui:140` read
`position = { x=@fixed_btn_mod_col_0 y@fixed_btn_mod_row_0 }` - the `=` after `y` was
missing. Introduced when the position block was rewritten for the 21-slot expansion.

The failure chain is worth writing down because every step is silent:

1. The malformed token aborts the parse of everything after it, so **125 children of
   `tank_designer_view` were dropped** - `module_selector_window`, `close_button`,
   `equipments`, `info` and the rest all logged
   `Could not find "X" in window tank_designer_view`.
2. Opening the designer then laid out against those missing containers and divided by a
   zero dimension: **`Caught signal 8 (SIGFPE)`**, per
   `crashes/hoi4_20260909_183945/exception.txt`. The crash is an integer division by
   zero, not a null dereference, which is why it presents as a hard crash rather than a
   missing panel.

**Why nothing caught it, and what now does.** Brace balance was 0 and every byte check
passed - a missing `=` changes neither. The validator's GUI check matches
`pos_custom_module_slot_window_(\d+)"` by regex, which matches the broken line perfectly,
so `21 designer slots checked` passed against a file the engine could not parse. The
validator now scans every `position` / `size` / `margin` block in
`tank_designer_view.gui` and all 106 blueprint files and fails on any token lacking an
`=`, with the failing file and line number. Mutation-probed: reintroducing the typo
produces
`tank_designer_view.gui:131 has a malformed assignment 'y@fixed_btn_mod_row_0'`.

**Verified by reproduction, not by inspection.** These errors fire at load time with
`no_game_date`, so a plain boot reproduces them without opening the designer. After the
fix a fresh boot reports **zero** `tank_designer_view.gui` errors and **zero**
`Could not find ... in window` lines, and the total `Could not find` count is back to 54
- byte-identical to the HEAD baseline, and all of it unrelated mesh/animation asset
noise. The 9 remaining `Malformed token` lines mod-wide are all in files untouched this
session (`USA_1980s_*` events, `HAI_1949.txt`, `PQC_1950s.txt`, `INO_Military_50s.txt`,
`KMT_dynamic_modifiers.txt`) and are pre-existing content bugs.

The designer opening successfully still needs an owner check; what is proven here is
that the parse error which caused the crash is gone.

**Lesson for this folder: brace balance is not a syntax check.** Any pass that rewrites
script or GUI assignment blocks must verify token shape, not just braces and bytes. A
boot is the cheap confirmation - load-time parse errors need no gameplay at all.

### Finding 12: the armour tech folders clip their right edge - open

Owner-reported 2026-09-09, after the designer fix. Both the gun/loading tab and the
armour/protection tab of the module tree lose their rightmost column to the window edge.

**This is not caused by the new columns, and widening the gridbox did not fix it.** Two
pieces of evidence. First, the owner's second capture clips in a region containing no
new content at all - the APS/softkill and add-on-armour area - so the clip predates this
session's columns and they merely made it visible. Second, `nsb_tank_design_tree` was
already widened from 2200 to 2500 (`countrytechtreeview.gui:4535-4541`), and at 70
pixels per x unit the last used column x=20 sits ~1000 pixels inside that rectangle, so
**the gridbox width is demonstrably not the limiting value.**

What that leaves, none of it yet measured: the folder's own scroll extent
(`:4496-4505`, `size = 100%%`, `clipping = yes`, `margin` right 25, horizontal
scrollbar), the `armortech_bg` background sprite's dimensions, or a tech item's rendered
width exceeding its 70-pixel slot so the last column's label overflows.

**The one interactive measurement that would settle it:** with the tree scrolled fully
right, does the horizontal scrollbar sit at its end while content is still cut off? If
yes the scroll extent is short and the folder/background is the culprit; if the scrollbar
has travel left the input handling is at fault. Deliberately not fixed by guesswork -
Finding 11 is what unverified GUI geometry costs.

### Finding 13: light / medium / heavy hulls are indistinguishable to `allow_equipment_type`

Recorded 2026-09-09, and it blocks the owner's ratified "paradrop for light hulls only"
decision. Finding 9 established that per-hull module locking uses
`allow_equipment_type` / `forbid_equipment_type`, which key off the archetype's own
`type = { ... }` set. Measured, those sets are:

| Archetype | `type` |
| --- | --- |
| `light_tank_chassis` | `armor` |
| `medium_tank_chassis` | `armor` |
| `heavy_tank_chassis` | `armor` |
| `mechanized_equipment` (APC) | `armor mechanized` |
| `mechanized_heavy_equipment` (IFV) | `armor mechanized` |
| the twelve role roots | `armor` plus `anti_air` / `artillery` / `anti_tank` / `flame` |

So the mechanism can separate carriers from gun tanks, and roles from base hulls, but it
**cannot separate light from medium from heavy** - all three are the same bare `armor`.
Amphibious-to-carriers works; paradrop-to-light-hulls does not.

Options, all needing an owner decision because each has a blast radius beyond the
designer: add a discriminating token to the light archetype and its hulls (e.g.
`type = { armor light_armor }`), which changes how the AI and any
`type`-matching script classify every light design; or accept paradrop on all gun-tank
hulls; or drop the box. Do not author a paradrop module before this is answered - it
would silently be mountable on every hull, which is the exact failure mode the lock model
exists to prevent.

### Finding 14: the documented module-based amphibious design is engine-impossible

Established 2026-09-09 from vanilla evidence, and it overrides `REFERENCE.md:129-131`,
which specifies an "amphibious mobility module on eligible mechanized designs". That
cannot work, and Finding 9's module-side approach - correct for ordinary stat modules -
is the wrong tool for this family.

**Sub-units consume equipment ids, never module-bearing variants.** Vanilla
`amphibious_mech.txt:44-59` has `transport = amphibious_mechanized_equipment` and
`need = { amphibious_mechanized_equipment = 50 infantry_equipment = 100 }`; vanilla
`amphibious_armor.txt:98-100` consumes `light_tank_amphibious_chassis`. Every value is
an equipment archetype id. A search of the whole vanilla `common/units/` tree found **no
land sub-unit key that references a tank module at all** - the only
`need_equipment_modules` sites are naval (`battlecruiser.txt:8-12`,
`battleship.txt:8-12`), and `can_be_parachuted` is a sub-unit key, not an equipment key.

**Vanilla amphibious capability follows the chassis role, not the fitted module.** The
chain is `light_tank_amphibious_chassis` with `type = { armor amphibious }`
(`x_tank_chassis.txt:38-40`) consumed by the sub-unit, which carries its own amphibious
terrain modifier (`amphibious_armor.txt:66-68`). `amphibious_drive` is only a module
eligibility-and-stats definition gated by `allow_equipment_type = amphibious`; it grants
no capability by itself.

**Consequence: amphibious must be a restored designer ROLE**, not a module - which is
exactly the "rebuilding it is new work, not a restore" that `DECISIONS.md` already warned
about, now with the engine reason attached. The alternative is pointing
`mechanized_marine`'s `need`/`transport` at `mechanized_equipment`, the APC designer
archetype - but that would make **every** APC a valid marine transport regardless of any
amphibious module, a balance consequence the owner must accept or reject explicitly.

Cost of the role route, all of it now measured: a new role chassis family typed
`{ armor mechanized amphibious }`, per-hull blueprint GUI files for it, and **six**
validator contracts to change consciously - the unsupported-id set (`:421-430`), the
generic unsupported scan (`:3957-3960`), the forbidden module id `amphibious_drive`
(`:2499-2502`), the rejected `tank_chassis_*_tank_amphibious*.gui` filenames
(`:2707-2708`), the 106-blueprint count and slot contract (`:4023-4044`), and the
`mechanized_marine` `active = no` assertion (`:4061-4062`). Note the validator currently
rejects precisely the blueprint filenames a restored role would need.

Nothing was implemented. This is a decision the owner must take before the amphibious
batch can start: **module (impossible), role rebuild (expensive but correct), or APC-wide
marine transport (cheap but unselective)**. OPVT and Underwater Driving Capability
inherit the same blocker.

### AA ammunition - IMPLEMENTED 2026-09-09

The owner's reversal of the self-supplying-AA-gun rule is shipped. Self-test delta:
`286 tank modules` -> **`289 tank modules`**, everything else unchanged.

Three modules `tank_aa_ammo_1..3`, one per existing AA cannon tier rather than a
six-tier ladder that would outrun the three guns able to use it. They sit in the
**existing** `tank_ammo_he` category - so no new category, no archetype edits, no new
count limit - and therefore mount in the dedicated HE slot `tank_special_slot_2`, which
is consistent with the slot contract. Each carries
`allow_equipment_type = anti_air`, so an AA shell cannot be fitted to a gun tank, and
each declares **no** `soft_attack`, `hard_attack` or `ap_attack`, so SPAA does not become
an anti-tank platform. Air attack is roughly 22% of the paired cannon: 4 / 7 / 10 against
18 / 32 / 46. All values authored. Unlocked from the existing
`nsb_aiming_devices0/2/4`, which already own the AA cannon tiers, so no new technology
and no `cwic_major_tank_research_1980` change was needed.

The three `Standard Light SPAA` starting variants (1942/1944/1950) now mount
`tank_aa_ammo_1`; every other field is byte-identical. The cannons' pinned air-attack
values 18/32/46 were not touched.

**The validator rule was inverted rather than deleted.** `needs_ammunition` now returns
true for AA armament, with a new `ammunition_requirement_error` distinguishing the AA
case, and the comment cites the 2026-09-09 decision instead of the retired rationale.
**Flame remains exempt** - verified in the final source. A negative fixture proves an AA
design without AA ammunition is now rejected.

Consequence to carry forward: known inconsistency 10's claim that "the three SPAA
variants deliberately carry no ammunition" is now **false and superseded**.



## Module content plan, 2026-09-09

Written at the owner's request, from a four-lane evidence pass. **Nothing in this
section is implemented.**

### First, a correction: the special modules are not missing

The premise "AFAIK, all special modules are missing" is not what the source says.
`00_tank_modules.txt` holds **270 module definitions, 145 of them in the 18 special
categories** - verified by per-module category parse, not by counting `category` lines:

| Category | Modules | Category | Modules |
| --- | ---: | --- | ---: |
| `tank_ammo_kinetic` | 13 | `tank_loader_artillery` | 3 |
| `tank_ammo_chemical` | 14 | `tank_protection_passive` | 7 |
| `tank_ammo_missile` | 9 | `tank_protection_reactive` | 5 |
| `tank_ammo_he` | 5 | `tank_protection_active` | 6 |
| `tank_fcs_aiming` | 11 | `tank_survivability` | 3 |
| `tank_fcs_optics` | 16 | `tank_mobility_auxiliary` | 11 |
| `tank_fcs_computer` | 14 | `tank_smoke` | 6 |
| `tank_fcs_radar` | 7 | `tank_secondary_turret` | 4 |
| `tank_loader_manual_assist` | 2 | `tank_loader_autoloader` | 9 |

What is missing is narrower and it is worth stating precisely, because it decides how
much work this is: **one whole family (Special Capabilities, 11 boxes), the night-vision
ladder (6 technologies), and four previously recorded orphans** (Blow-Out Panels,
External Additional Fuel Tanks, Unmanned Turret / RWS, Modular Construction). Thermal
vision is *not* missing and suspension is *not* missing - see below. That is roughly
15-20 new modules against 145 existing, not a from-scratch build.

### On the proposed order: technologies first, then map to the designer

Agreed with one correction. Authoring the technologies and modules first is right,
because a module cannot be reached without an unlock and the tree geometry is the
scarce resource. But "then map it to the designer" is mostly already done: the 21-slot
contract exists, the free-slot list exists, and per Finding 9 the per-hull lock is a
module-side attribute rather than a designer change. The real sequencing constraint is
the opposite of what it looks like - **every new module must land in the free-slot
category list and the count limits in the same edit as its technology**, or it silently
stacks. There is no separate "map to designer" phase to defer to.

### Lane 1: night vision - IMPLEMENTED 2026-09-09

Shipped in this pass. Six technologies `nsb_night_vision0..5` in a new x=18 column of
`nsb_armor_modules_folder` at @1944 / @1960 / @1975 / @1990 / @2000 / @2020 - every
anchor already existed, none was added - chained
`nsb_optics0 -> nsb_night_vision0 -> .. -> nsb_night_vision5`, with `nsb_optics7` as the
second required input to Fusion so the thermal branch converges into it as the mockup
shows. Six modules `Night_Vision_0..5`, abbreviations `nvis0..5`, all in the existing
`tank_fcs_optics` category - so **no archetype, free-list or count-limit edit was
needed**, which is why that category was chosen. Localisation for all twelve keys from
the owner's descriptions 37-41 and 45, ASCII-only.

All stats are **authored/invented** - the workbook sheet is empty. They are monotonic
across the six tiers and bounded by `Optics_7`: the top tier matches `Optics_7` on fuel,
build IC, reliability, breakthrough, defence, dismantle and XP while staying below it on
hard/soft attack (0.15 against 0.25), so night vision reads as capability rather than a
raw attack upgrade.

**The tree was clipped and is now widened.** `nsb_tank_design_tree` hosts the FCS graph
and its gridbox width was the limiting value, at 2200 with 70px per x unit
(`countrytechtreeview.gui:4535-4541`). One number changed, 2200 -> 2500, which buys the
280px needed to reach x=20 plus 20px headroom. No tree origin, folder size, scrollbar or
year label moved. **This is a measured change, not a verified render** - the owner should
confirm the night-vision column is visible and scrollable in the module tree.

**One contract catch, worth recording because only the validator found it.** The six new
technologies broke `cwic_major_tank_research_1980`, which must grant every tank
technology with `start_year <= 1980`: the validator failed with
`1980 tank research coverage differs: ['nsb_night_vision0', 'nsb_night_vision1',
'nsb_night_vision2']`. Fixed by adding those three to
`CWIC_tank_bookmark_research.txt`. **Any future technology added to an NSB armour file
must be added there too if its `start_year` is 1980 or earlier.**

Self-test after: `1309 technologies, 275 tank modules ... 21 designer slots checked` -
plus six technologies and six modules, every other count unchanged.

### Lane 1 background: why night vision was absent and thermal was not

Before this pass no **night**-vision technology or module existed anywhere;
`night_vision` survived only as an orphan tag at
`common/technology_tags/00_technology.txt:42`, referenced by no technology, module,
localisation key or icon. Thermal vision was a different story - see below.

The existing FCS ladder in `NSB_armor_modules.txt` occupies columns x10 (aiming,
`nsb_aiming_devices0..5`), x12 (optics, `nsb_optics0..7`), x14 (ballistic computer,
`nsb_ballistic_calculator0..6`) and x16 (panoramic sight, `nsb_pano_sight0..2`), with
`nsb_awareness_system` converging at x8/@2020. **x18 is free**, which is exactly where
the owner's mockup puts the night-vision column - immediately right of the panoramic
sights. No existing technology has to move.

**The thermal half is already built, and that halves this lane.** `Optics_4..7` are
localised **"Thermal Sight I", "Thermal Sight II", "Thermal Sight III"** and
**"Advanced Thermal Sight"** (`tank_modules_l_english.yml:951-957`), category
`tank_fcs_optics`, unlocked by `nsb_optics4..7` at 1970 / 1980 / 1990 / 2005
(`NSB_armor_modules.txt:2895, 2922, 2949, 2976`). So the mockup's three-step thermal
branch is already four steps in script - it just lives in the optics column rather than
a column of its own, and its stat operations are ordinary optics operations rather than
anything thermal-specific.

That leaves a genuine decision, not an authoring task: either accept the existing
`Optics_4..7` as the thermal branch and only add night vision beside it, or split
thermal out into the new column to match the mockup - which means retargeting four
shipped modules and their four unlock technologies, and the shipped presets that
reference them. **The cheap and boring option is to keep `Optics_4..7` where they are**
and treat the mockup's thermal boxes as already satisfied, with a note that the mockup's
years (1975/1990/2000) disagree with the shipped 1970/1980/1990/2005.

Owner ladder and row status, with `@year` anchors resolved:

| Technology | Year | Status |
| --- | --- | --- |
| Zero Gen Night Vision | 1944 | new; row exists (`nsb_aiming_devices1`, `nsb_optics1`) |
| First Gen Night Vision | 1960 | new; **new row** |
| Second Gen Night Vision | 1975 | new; row exists (`nsb_ballistic_calculator2`) |
| Third Gen Night Vision | 1990 | new; row exists (`nsb_optics6`) |
| Third+ Gen Night Vision | 2000 | new; **new row** |
| First Gen Thermal Vision | 1975 | satisfied by `Optics_4` (shipped 1970) |
| Second Gen Thermal Vision | 1990 | satisfied by `Optics_5`/`Optics_6` (1980/1990) |
| Third Gen Thermal Vision | 2000 | satisfied by `Optics_7` (2005) |
| Fusion Night Vision | 2020 | new; row exists (`nsb_awareness_system`) |

So six new technologies, not nine, and two new tree rows. The owner supplied
description text for all nine boxes, numbered 37-45, which removes the localisation
blocker; entries 42-45 describe the thermal and fusion steps and can be attached to the
existing `Optics_4..7` if the cheap option is taken.

**Category decision for night vision.** If night vision goes in `tank_fcs_optics` it
competes with the day sights and the thermal tiers for the one dedicated optics slot,
which is probably right historically and costs nothing. If it gets its own category it
becomes a free-slot module that stacks with a sight, and that category must be added to
the free list and the count limits in the same edit.

**All numbers are invented.** The frozen workbook's `Night & Thermal Vision Effects`
sheet has dimension ref `A1` and **zero value cells** - confirmed by reading the sheet
XML out of the xlsx, without writing to it. The "recorded as authored" rule applies to
every stat in this lane.

### Lane 2: suspension - already implemented, do not rebuild it

This answers the owner's "needs further review if it should be implemented/already is"
directly: **it is implemented.** Fifteen suspension modules exist across all six
categories, with a full unlock chain:

| Mockup box | Status | Existing id |
| --- | --- | --- |
| Torsion Bar Suspension 1939 | exists | `Torsion_0`, granted by `nsb_iw_armored_vehicles` |
| Torsion Bar With Shock Absorbers 1944 | exists, year/name differ | `Torsion_1`, granted by `nsb_suspension0` (1940), localised "Modernized Torsion Bar Suspension" |
| Tracked Hydro-Pneumatic 1960 | exists, year agrees | `Hydro_pneumatic_1`, `nsb_suspension2` @1960 |
| Tracked Active Hydro-Pneumatic 1985 | exists, year agrees | `Hydro_pneumatic_2`, `nsb_suspension3` @1985 |
| Experimental 4-Track Suspension | **absent** | no module, technology or localisation key |

So the only genuinely new suspension item is Experimental 4-Track, whose mockup
annotation "Opened by 1955 H Tank" implies a prerequisite on a heavy hull rather than a
free-standing tech. Everything else is a naming and year reconciliation question, not
implementation. The mockup's "Modernised External Spring Suspension" annotation is
ambiguous: `Independent_external_1` exists and is localised "Modernized External
Independent Suspension", so decide whether that annotation labels `Torsion_1` or points
at the external-independent family before renaming anything.

There is **no transmission module family at all** - no `transmission` match anywhere in
the module file - so the mockup's "Transmission" heading currently describes nothing in
script. Decide whether it is a real surface or just a heading.

The engine column is likewise implemented (`Petrol_0..3`, `Diesel_0..6`, `GT_0..3`,
`APU_0..6`, `GT_APU_0..3`) but carries a systematic year disagreement worth one
decision rather than eleven: **the icon assets encode one year and the unlocking
technology another**, consistently for the gas turbines (icons 1960/1970/1980/2000 vs
techs 1965/1975/1985/2005) and the GT APUs (icons 1960/1970/1980/2000 vs techs
1965/1975/1985/2005). The mockup agrees with the icons. Pick one authority and record
it; do not fix these one at a time.

The mockup annotation "Early Auxiliary Power Unit - needed for SPAA with radar" is
**aspirational, not implemented**: no `allow`, prerequisite or trigger anywhere ties any
`APU_*` or `GT_APU_*` to `Radar_*` or to an AA chassis. If that coupling is wanted it is
new work, and Finding 9's `allow_equipment_type` is the mechanism for the AA half of it.

### Lane 3: Special Capabilities - absent, and two boxes have no engine mechanism

Every box is absent from the mod: no module, no technology, no icon, for Amphibious
Drive, OPVT, Underwater Driving Capability, Dozer Plow, Log, Anti-Mine Plow (1955 and
1970), Paradrop Capability, Anti-Mine Roller (KMT-5), Integrated Trench-Digging Plow,
or Anti-Mine Roller With Electro-Magnetic Coils (KMT-7 EMT).

Most of them are ordinary stat modules and have a home category already:

| Box | Available existing category |
| --- | --- |
| Log, Blow-Out Panels | `tank_survivability` (Blow-Out Panels also fits `tank_protection_passive`) |
| Dozer Plow, both Anti-Mine Plows, both Anti-Mine Rollers, Integrated Trench-Digging Plow, External Additional Fuel Tanks | `tank_mobility_auxiliary` |
| Unmanned Turret / RWS | `tank_secondary_turret` |
| Modular Construction | none clearly semantic |

**Two boxes are not stat modules and need a decision before they are designed.**

- *Amphibious Drive and Underwater Driving / OPVT.* Vanilla's mechanism is
  `allow_equipment_type = amphibious`, but this mod **deleted** the designer amphibious
  role (`DECISIONS.md`), so there is no `amphibious` type to allow. The legacy
  `amphibious1..5` technologies (`armor.txt:1765-1918`) only
  `enable_equipments = mechanized_marine_equipment_1..5`; they grant no module and no
  capability key. And `mechanized_marine` is still `active = no`
  (`CWIC-Special-Units.txt:62-70`) with the validator asserting it stays that way.
  Making an amphibious module actually supply marine sub-units therefore means
  rebuilding the role, flipping that sub-unit, and consciously changing that validator
  assertion - which is exactly the pre-condition `DECISIONS.md` already set for this
  family. This is the largest item in the whole plan and it is not a module.
- *Paradrop Capability.* There is **no engine field for it in the module system.** A
  search of the vanilla module directory finds no `can_be_parachuted`, `parachut*`,
  `special_forces` or `marines` key on any module - the only capability-bearing vanilla
  module is `amphibious_drive`, and it works through equipment types, not a paradrop
  flag. So a paradrop *module* cannot grant paradrop capability. It has to be a sub-unit
  or technology property, or the box has to be dropped. Do not author it as a module and
  discover this afterwards.

Authoring conventions for the rest, from three cited families: costs go inside
`add_stats` with a module-level `dismantle_cost_ic`, and `xp_cost = 1` universally -
`Addon_0_Comb` 1.5/0.1/1, `ERA_0` 1/0.05/1, `Smoke_0` 0.5/0.05/1. Each module also needs
a `GFX_SMI_<id>` sprite in `interface/cwic_tank_rework_icons.gfx` whose texture exists
on disk, or the engine logs a miss every load.

### Lane 4: armoured artillery and SPAA - the limbo is real and now measured

The owner's read is correct, and it is duplication of identity, not just of listing.

*The designer path.* Six role roots in `x_tank_chassis.txt` - light/medium/heavy
artillery and anti-air, e.g. `light_tank_aa_chassis` `type = { armor anti_air }` at
`:8-15` and `light_tank_artillery_chassis` `type = { armor artillery }` at `:18-25`.
`NSB_armor.txt` grants light and medium tiers 0-9 and heavy tiers 0-4 for both roles.

*The legacy path, still fully live.* `artillery.txt` is **85 technologies in 17
five-tier families**, confirming known inconsistency 8's count. It sits in an
**unconditional** `artillery_folder` - no `has_dlc`, no `allow`, no trigger anywhere in
the file - and it enables its own sub-units and its own equipment archetypes:
`sp_artillery_1` enables `sp_artillery` + `sp_artillery_equipment_1` (`:1271-1277`),
`light_sp_artillery_1` (`:1619-1625`), `heavy_sp_artillery_1` (`:1978-1984`), and
`spaag_1` enables `spaag` + `spaag_equipment_1` (`:252-259`). The consumers are real
sub-units in `CWIC-Artillery.txt` and `CWIC-Anti-Air.txt`, and the legacy archetypes
carry five tiers each at 1940/1955/1970/1985/2000 (`sp_art.txt:54-160`,
`sp_aa.txt:50-155`).

*What the tree grants the designer today: nothing.* The only
`enable_equipment_modules` in all of `artillery.txt` are `ship_AA_gun_1..5`. Eighty-five
technologies, zero tank designer modules.

**The gating decision already exists** - `DECISIONS.md` ratified that artillery and AA
gate legacy and designer paths by DLC, preserving technology-based sub-unit activation,
reusing the `OR = { has_tech = legacy has_tech = nsb_* }` shape. That shape is live in
`support.txt` at seven sites (`:82-86, 130-134, 184-188, 238-242, 290-294, 378-382,
430-434`). So the remaining work is implementation plus the mockup's restructure, not a
new decision about approach.

**Where the mockup and the existing module set disagree - resolve before authoring.**
The mockup wants each artillery/AA technology to unlock *gun modules only*, on six-tier
ladders. The modules it would unlock are only partly there:

| Mockup column | Existing designer modules | Gap |
| --- | --- | --- |
| Light/Medium/Heavy Artillery I-VI | `tank_low_p_cannon0..3`, category `tank_low_pressure_main_armament`, already `allow_equipment_type = artillery` | 4 tiers exist against 18 mockup boxes; there is no separate light/medium/heavy artillery gun family |
| AA Autocannon I-VI | `tank_anti_air_cannon`, `_2`, `_3` | 3 tiers against 6 |
| Artillery Ammunition I-VI | none - no artillery ammunition category exists | 6 new, and needs a category decision |
| AA Ammunition I-VI | none | **conflicts with a ratified decision** |
| Artillery / AA Modernisation I-VI | no module family; these are modifier technologies | decide whether they grant modules at all |

The AA ammunition column is the one to settle first, because it contradicts something
already ratified: AA guns deliberately supply their own attack, the three SPAA bookmark
variants deliberately carry no ammunition (known inconsistency 10), and the validator
pins that exemption. An AA ammunition ladder either overturns that or has to be modelled
as technology bonuses rather than modules.

Also note the frozen `Artillery_AA_Target_Manifest.md` already fixes 31 vehicle target
rows over SPAAG, SAM, SP Light/Medium/Heavy and AT, with six module budget rows, and
explicitly defines no towed-artillery or ammunition loadout. Any restructure has to land
inside that frozen contract or renegotiate it explicitly.

The validator would have to renegotiate its role-chassis grant formula
(`validate_tank_rework` expected grants), the `SUPPORTED_ROLES` constant, the exact AA
air-attack values 18/32/46, the `needs_ammunition` AA exemption, and the generated-enum
checks for artillery chassis.

### Amphibious: the documented specification and the five blockers

Researched 2026-09-09 under the owner's ruling that the design documents are the
authority.

**What the documents actually specify.** `REFERENCE.md:129-131` maps
`mechanized_marine_equipment` onto the same archetype with an **amphibious mobility
module**, marked NOT STARTED - so the documented design is a module on eligible
mechanized designs, not a restored tank role. `BALANCE.md:312-330` (drawio page 2) puts
`Amphibious Drive` at 1940 in the Special Capabilities column and records that it
**retires the legacy line**. Two things the documents do *not* provide: the xlsx `Roles`
tab contains no amphibious or marine row at all, and `Balance_Target_Manifest.md` rows
24-41 cover only WWII/Light/Heavy Mech - `BALANCE.md:259-261` states outright that no
source target defines amphibious equipment. Drawio page 7 "Trucks & Amphibious" is a
bare grid. **So every amphibious stat is authored, with no frozen envelope to match.**

**Current state.** The legacy half exists and works: `armor.txt:1765-1932` defines
`amphibious1..5` at 1944/1950/1965/1985/2005, each only
`enable_equipments = mechanized_marine_equipment_N`, and `mechanized_marine.txt:8-165`
defines the archetype plus five tiers. The consuming sub-unit is parked -
`CWIC-Special-Units.txt:62-108` has `special_forces = yes`, `marines = yes`,
`active = no`, `type = { mechanized }`, needing 50 `mechanized_marine_equipment` and 150
`infantry_equipment`. The designer half is gone: no `amphibious` type, no role chassis,
no module. Only cosmetics survive - MIO sprites at
`industrial_organization_department_icons.gfx:180,212,244`, a texticon at
`texticons.gfx:4597`, and vanilla-inherited loc keys at
`tank_modules_l_english.yml:241-242,280-284,303-307,336-340`.

**The hull-lock token is settled by measurement.** All three gun-tank archetypes are
bare `type = armor` (`tank_chassis.txt:2-15, 415-428, 825-838`); APC and IFV are
`type = { armor mechanized }` (`mechanized.txt:7-20`, `mechanized_heavy.txt:7-16`) and
every one of their sixteen hulls repeats it. The twelve designer role roots in
`x_tank_chassis.txt` add `anti_air` / `artillery` / `anti_tank` / `flame`. So
**`mechanized` is the discriminator** that locks amphibious to the carriers, and
`forbid_equipment_type_exact_match = armor` is the shape that excludes bare gun tanks -
exactly what vanilla's `amphibious_drive` does. Vanilla's own role root for comparison:
`x_tank_chassis.txt:39-45` is `light_tank_amphibious_chassis` with
`type = { armor amphibious }`.

**Five blockers, all of which must be crossed consciously.** The validator does not
merely lack support for this - it actively forbids it, in four places:

| # | Blocker | Site |
| --- | --- | --- |
| 1 | `amphibious_drive` is on the forbidden-module-id list | `validate_military_reworks.py:2499-2502` |
| 2 | `amphibious_tank_chassis`, `amphibious_mechanized_infantry`, `category_amphibious_tanks` are forbidden orphan ids | `:425-430` |
| 3 | any `tank_chassis_*_tank_amphibious*.gui` blueprint is rejected | `:2703-2705` |
| 4 | `mechanized_marine` must stay `active = no` | `:4039-4040`, exact assertion |
| 5 | `mechanized_marine_equipment_1..5` sit in `UNMIGRATED_LEGACY_ARMOUR` and are one of the eight ratified focus-grant exceptions | `:350-355`, `DECISIONS.md` |

Recommended shape, consistent with both the documents and Finding 9: author an
amphibious **mobility module** in `tank_mobility_auxiliary`, bounded by
`allow_equipment_type = mechanized` plus
`forbid_equipment_type_exact_match = armor`, rather than restoring a vanilla-style
amphibious role. That keeps the 21-slot contract and the free lists untouched. The hard
part is unchanged and is not a module problem: making an amphibious carrier design
actually supply the `mechanized_marine` sub-unit means flipping blocker 4 and rewriting
that assertion, and `DECISIONS.md` forbids retiring `amphibious1..5` until that supply
demonstrably works.

### Artillery and SPAA: restructure plan inputs

Researched 2026-09-09. Four things are now measured that the plan needs.

**1. The gate shape is `allow`, so gated legacy technologies stay visible.** All seven
`support.txt` sites (`:82-87, 130-135, 184-189, 238-243, 290-295, 378-383, 430-435`) put
`OR = { has_tech = legacy has_tech = nsb_* }` inside a per-technology `allow` block, not
`allow_branch` and not the folder block. A failing gate therefore leaves the technology
in the tree but unresearchable. That is the desired behaviour here and it is why folder
removal was rejected for mechanized.

**2. Gating is the right call, and the margin is now five times larger than the
precedent.** Legacy artillery/AA technologies are granted at **5653 `set_technology`
sites across 460 country-history files**. The mechanized precedent that made
`DECISIONS.md` choose DLC-gating over folder removal was 1144 sites. Removing these
families from the folder is not on the table.

**3. The AA ammunition reversal has three concrete consequences.** The validator's
`needs_ammunition` exemption at `:3619-3624` explicitly encodes "AA and flame supply
their own attack, no shell", and it is invoked on starting variants at `:3890-3893`. The
three affected designs are `Standard Light SPAA` 1942/1944/1950 at
`CWIC_tank_designer_effects.txt:159-173, 181-195, 203-217`, each mounting
`tank_anti_air_cannon` with no ammunition slot filled. And the only ammunition
categories that exist are `tank_ammo_kinetic` and `tank_ammo_he`, so an AA shell either
joins one of those - free - or gets a new category, which costs an edit to all five
archetypes' free lists **and** the count limits in the same edit. Prefer joining an
existing category unless the design genuinely needs AA-only exclusivity.

**4. The mockup's premise collides with the module-provenance contract.** The validator
only scans `NSB_armor.txt` and `NSB_armor_modules.txt` for module unlocks
(`:1795-1806`, `:3648-3655`). The mockup wants artillery technologies to unlock designer
gun modules, which would put unlocks in `artillery.txt` - outside that contract. Either
the new gun-module unlocks live in the NSB files while the artillery tree only gates
them, or the provenance contract is widened deliberately. **Decide this before authoring
a single technology.**

Existing module coverage against the mockup's six-tier ladders, all unlocks cited:

| Family | Have | Want | Unlocks |
| --- | ---: | ---: | --- |
| Low-pressure artillery guns `tank_low_p_cannon0..3` | 4 | 18 (light+medium+heavy) | `nsb_low_pressure_guns0..3` at `NSB_armor_modules.txt:385, 411, 445, 479` |
| AA cannon `tank_anti_air_cannon`/`_2`/`_3` | 3 | 6 | base at `NSB_armor.txt:59-69`, then `nsb_aiming_devices2/4` |
| AA aiming `Aim_AA_0..4` | 5 | - | base plus `nsb_aiming_devices2..5` |
| AA optics `AA_Optics_0..5` | 6 | - | base plus `nsb_optics4..7` |
| Artillery optics `Arty_Optics_0..1` | 2 | 6 | base plus `nsb_ballistic_calculator5` |
| Artillery computer `Computer_arty_0..3` | 4 | 6 | `nsb_ballistic_calculator3..6` |
| Artillery loader `Loader_5a/5b/5c` | 3 | 6 | `nsb_conveyer_autoloader0..2` |
| Artillery ammunition | 0 | 6 | none - new |
| AA ammunition | 0 | 6 | none - new, and see consequence 3 |

**Tree geometry: there is room, but the existing lattice already collides.** The 85
technologies occupy only **55 unique cells** in a lattice of x = -7,-4,-3,0,3,4,7 by
y = 0..28 even. At x=0 seven families overlap the same cells - `(0,0)` holds
`autocannon`, `artillery` and `direct_fire_gun`; `(0,2)` holds `spaag`, `sp_rocket` and
`tank_destroyer` - and `x=-3` doubles `cannon_ammo` with `at_ammo` while `x=3` doubles
`aa_upgrade` with `at_upgrade`. Roughly 50 cells are free. Per `README.md`'s guardrail,
do not resolve a collision by moving a technology to an arbitrary free cell; keep each
family in one column and move the minimum. Note the `artillery_folder` GUI declares only
one explicit gridbox (`countrytechtreeview.gui:5222-5229`, anti-air grid at
`:5252-5257`), so a widened tree may need the same clipping fix Lane 1 needed.

**Frozen-manifest boundary.** `Artillery_AA_Target_Manifest.md` freezes 31 vehicle rows
(SPAAG 5, SAM 6, SP Light/Medium/Heavy 5 each, AT 5) and six module budget rows, and
**explicitly leaves towed artillery, rocket artillery, amphibious, night vision and any
complete designer loadout undefined**. Omitted stats are unspecified, not zero. A
restructure lands inside that boundary or renegotiates it in writing.

**Migration checklist** - the DLC gate must cover all 17 five-tier families
(`artillery`, `light_artillery`, `heavy_artillery`, `art_ammo`, `art_upgrade`,
`sp_artillery`, `light_sp_artillery`, `heavy_sp_artillery`, `sp_rocket`, `autocannon`,
`spaag`, `aa_upgrade`, `cannon_ammo`, `direct_fire_gun`, `at_ammo`, `at_upgrade`,
`tank_destroyer`), their sub-units including the `_support` variants, and their eleven
five-tier equipment ladders.

### Order and status

1. ~~Four blocking decisions~~ - **answered by the owner 2026-09-09**, recorded in
   `DECISIONS.md` under "Owner decisions".
2. ~~Night vision~~ - **implemented 2026-09-09**, see Lane 1. Owner still owes a visual
   confirmation that the new x=18 column is visible after the tree widening.
3. ~~Special Capabilities minus amphibious and paradrop~~ - **implemented 2026-09-09**,
   see "Special Capabilities and 4-Track" below.
4. ~~Experimental 4-Track and the icon-year authority migration~~ - **implemented
   2026-09-09**, same section.
5. **Amphibious**, own batch - a module plus a sub-unit activation plus four validator
   assertions that must consciously change.
6. **Artillery/AA restructure**, last and largest, against the frozen manifest, and
   gated on the module-provenance decision in that plan.

Items 3-4 were run as two concurrent agents split by **file ownership** rather than by
lane - one owning the module/archetype/icon files, the other the technology/effect files
- with the module-id-to-unlock map fixed in the batch contract so the halves met. Both
lanes editing `00_tank_modules.txt` is what makes a lane-shaped split impossible.

### Special Capabilities and 4-Track - IMPLEMENTED 2026-09-09

Self-test delta: `1309 technologies, 275 tank modules` -> **`1317 technologies, 286 tank
modules`**; every other count unchanged, still `21 designer slots checked`.

**Ten Special Capabilities modules, all into existing categories** - deliberately, since
an existing category needs no free-slot or count-limit edit. `tank_mobility_auxiliary`
11 -> 18 (`Dozer_0`, `Fuel_Tanks_0`, `Mine_Plow_0`, `Mine_Roller_0`, `Mine_Plow_1`,
`Trench_Plow_0`, `Mine_Roller_1`), `tank_survivability` 3 -> 5 (`Log_0`,
`Blowout_Panels_0`), `tank_secondary_turret` 4 -> 5 (`RWS_0`). Seven technologies
`nsb_special_capabilities0..6` at 1945/1950/1955/1965/1970/1980/1990 in a new x=20
column, chained off `nsb_tank_design`. A `@1945` anchor had to be added, resolving to 3
between `@1944 = 2` and `@1950 = 4`; no duplicate row value resulted.

All stats are **authored/invented** except `Log_0`, whose +2% reliability is the one
documented value in the drawio. Each module was priced against a named neighbour in its
own family. No new abbreviation collision was introduced.

**`Four_Track_0` needed a new category, and it is a mandatory-slot category rather than
a free-slot one.** `tank_suspension_multi_track` is now listed on `suspension_type_slot`
in all five archetypes (3 in `tank_chassis.txt`, 1 each in `mechanized.txt` and
`mechanized_heavy.txt`) and correctly has **no** `module_count_limit` - a mandatory slot
holds exactly one module, so the count-limit rule that governs free-slot categories does
not apply. Verified: the limit blocks stayed at 54 / 18 / 18. Its unlock
`nsb_suspension_multi_track` is gated on `nsb_heavy_tanks3`, the heavy ladder's 1955
technology, implementing the mockup's "Opened by 1955 H Tank" annotation as a
prerequisite rather than a free-standing tech.

**Icon-year authority applied to the gas turbines.** `nsb_gt_engines0..3` moved from
1965/1975/1985/2005 to **1960/1970/1980/2000**, with their tree rows moved to match and
no coordinate collision. This is the ratified rule that the icon asset year wins.

**The validator had to move with it, exactly as the guardrail predicts.** It hardcoded
those four years at `validate_military_reworks.py:2660-2665` and failed with
`nsb_gt_engines0..3 has the wrong start year or tree row`. Updated to the icon years
with the rationale in a comment. `README.md`'s warning that any balance change needs a
matching validator edit held true.

**Second hit of the 1980-coverage rule.** As in Lane 1, new technologies dated <= 1980
had to be added to `cwic_major_tank_research_1980`: `nsb_special_capabilities0..5`,
`nsb_suspension_multi_track`, and the gas-turbine technologies the migration newly
brought to 1980 or earlier. `nsb_special_capabilities6` (1990) is correctly excluded.
This rule has now bitten twice in one session - treat it as part of the definition of
adding an NSB armour technology.

**Deferred with reasons, not forgotten.** `OPVT` and `Underwater Driving Capability`
were pulled out of this batch: they are amphibious-adjacent and share the amphibious
missing-mechanism problem, so they belong to that batch rather than being approximated
with unrelated stats. `Modular Construction` remains deferred for want of a semantically
available category. Neither is implemented, and no stat was invented for them.

Static verification only. No live check of the new column, the new suspension option, or
any of the eleven modules in the designer.


## Owner QA notes, 2026-09-06 playtest

Both NSB and non-NSB loaded clean at 1949 and 1980. Verbatim notes are in
`TankQANotes.txt`; screenshots in `Screenshots_9-6-26/`.

**Items 2, 3, 4, 6 and 7 were human-verified in game and closed by the owner on
2026-09-08**, confirming the static dispositions below. Still open:

1. On non-NSB, FIN's focus "Acquire Soviet T-55's" needs a check that SOV has
   researched T-55 technology, or it grants nothing.
2. Tank research is not date-gated in either profile. A 1980 start still shows USA with
   1955+ tech locked.
3. NSB only: Light Turret Module has the same stats as Conventional Turret. (A revised
   conventional turret was authored - see `DECISIONS.md` - so confirm whether this
   observation predates that change.)
4. NSB only: Early MBT Heavy Gun, HEAT-MP Ammunition (1985) and HEAT-DU Ammunition
   (1985) are researchable in 1980 with no ahead-of-time penalty. May apply to other
   tank tech at other dates.
5. NSB only: ATGM modules have very high piercing. Gun-Launched ATGM III is 600
   piercing / 95 hard attack / 5.5 soft attack. This matches both script and workbook -
   see `DECISIONS.md` - so the question is whether the source itself is right.
6. NSB only: Vehicle Radar System stats look odd - supply use renders as `-0`,
   air attack +25%, reliability -5%, fuel usage 1.20. These match the workbook; the
   `-0` is a display rounding artifact, not a zero in the module definition.
7. NSB only: `CWIC_tank_focus_effects.txt` effects are verbose and fill the Armor
   Production tab with preset tanks for USA/SOV. Does not match non-NSB.
8. NSB only: preset tanks are not made for NSB - no T-54/T-55 for SOV, just a generic
   hull. (Superseded for carriers by the Step 2 commit; still true for other families.)

## Static QA disposition, 2026-09-08

Static review of owner QA items 2, 3, 4, 6 and 7 found no remaining source discrepancy:

- **QA 2:** `cwic_major_tank_research_1980` is called from the dated 1980 USA and
  SOV history blocks. Its NSB branch grants every tank technology with
  `start_year <= 1980`, and its legacy branch grants the corresponding legacy
  ladder. The validator checks both exact grant sets and the one-call-per-country
  history contract.
- **QA 3:** `light_turret` remains the inexpensive 1 IC / 0.15 reliability option.
  `conventional_turret` is the reviewed 1.5 IC / 0.15 reliability option with
  +0.05 breakthrough. The validator pins this deliberate difference.
- **QA 4:** `nsb_heavy_guns5`, `nsb_heat_mp_ammo0` and `nsb_heat_du_ammo0` each
  carry `start_year = 1985` and sit on the `@1985` row. The validator pins these
  dates; no missing `start_year` source defect was found.
- **QA 6:** `Radar_1` carries fuel 1.2, supply-use -0.075, air attack +0.25 and
  reliability -0.05, matching the living CSV and frozen workbook. The displayed
  `-0` supply value remains a tooltip-precision question, not a zero in script.
- **QA 7:** all 16 focus export helpers use `hidden_effect`, `obsolete = yes` and
  `allow_without_tech = yes`; all 586 national and 40 generic startup designs
  use `mark_older_equipment_obsolete = yes`. The shipped newest-only mechanism
  is present, with no design-name changes.

These were static verification. The owner then confirmed all five in game on
2026-09-08, along with newest-only production visibility and save/reload of an NSB
design, so those three items leave the unverified list below.

## Not yet verified, any batch

Non-NSB regression, long-run AI production behaviour with mechanized now also in the
`armor` domain, the 1980 bookmark path end to end, the sixteen new carrier hull
icons rendering in the production tab, and whether the AI ever assigns factories to
`land_apc` or `land_ifv` without a `role_ratio`.

Newest-only production visibility and save/reload of a saved NSB design were
confirmed by the owner on 2026-09-08 and are no longer open.

On that last point: `common/ai_equipment/generic_tank.txt` defines eight `history = yes`
recipes for each of `land_apc` and `land_ifv`, and no `role_ratio` strategy in this
repository names either role. The installed game's `_documentation.md` does not specify
default demand when an explicit ratio is absent. Static recipe availability does not
demonstrate factory assignment, but absence of a ratio does not prove failure either.
No AI strategy change is justified by this evidence alone. Deferred to the final
designer AI pass.

Also outstanding from Tier 3: a runtime render check of the legacy armour folder for
non-NSB players, and a designer UI pass at 1920x1080 and 2560x1440 at 1.0x and 2.4x.

## Playtest log corpus - read the dates before citing it

`error-1949NSB.log`, `error-1949NoNSB.log`, `error-1980NSB.log` and
`error-1980NoNSB.log` at the /LogDocs/Tank_Designer/archive directory are the owner's 2026-09-06 captures.
They are untracked and **predate `eb708e3691` by two days**, so their variant and
OOB evidence describes the pre-migration tree. That is provable rather than assumed:
they report `heavy_mechanized_equipment_3` at `CZE_1980_nsb.txt:289`, and that id
has not existed in any `_nsb` file since `eb708e3691`. New, unverified error logs arrive in
the /LogDocs/Tank_Designer/data directory. As seen by error_9-8-26-2119.log.

Findings 3 and 5 were taken from these logs and then **re-confirmed against current
source** before being acted on. Everything else in them - notably the 1980
`Trying to fill variant where none exist` counts - is stale and must not be used to
size work. A fresh four-profile capture is needed before the coverage sweep is
scoped from runtime demand.

What the stale corpus does establish, because it is a same-build comparison: the
designer bootstrap strictly improves 1980 armour coverage. `medium_tank_chassis`
empty-variant failures were 3 on NSB versus 53 on non-NSB, and `light_tank_chassis`
0 versus 12. The `mechanized_equipment` (79) and `mechanized_heavy_equipment` (93)
failures were **identical in both profiles**, so they are legacy 1980 content gaps
in those countries' histories, not a designer regression.

## Next scope

1. **Fresh playtest capture** at 1949 and 1980 on both profiles, replacing the
   stale 2026-09-06 corpus. This gates item 3. Confirm the Soviet 1980 stockpile now
   actually arrives, and that the sixteen carrier hull icons render distinctly.
2. **Module content authoring** - see "Module content plan, 2026-09-09" above for the
   evidence, the per-lane ledger and the recommended order. The 21-position contract
   and the render are shipped and confirmed; per-hull locking turns out to be a module
   attribute rather than designer work (Finding 9), so the blocking items are the four
   content decisions listed at the end of that plan, then night vision, then the
   Special Capabilities modules. Amphibious and the artillery/AA restructure are their
   own later batches.
3. **Historical coverage sweep.** Explicitly required, not optional polish: named
   designs for **all** armour vehicle families (light, medium, heavy, APC, IFV and
   other armoured roles) across all countries, or at minimum every country with a
   corresponding non-NSB vehicle already implemented. Sized 2026-09-08: the English
   `TAG_<equipment>` inventory holds **2,189 distinct `(tag, family, tier)`
   combinations across 86 tags**, of which 586 have a national preset today, leaving
   **1,603 uncovered** - `lt` 399, `mbt` 616, `ht` 94, `mechanized` 341,
   `mechanized_heavy` 153. Light and heavy have **no** national coverage at all, and
   medium has only USA and SOV. At the current 20,549-line generated file for 586
   presets this is a generator batch, not hand authoring, and it needs a demand
   filter first: creating 2,189 startup designs for 86 tags is a production-tab and
   load-time cost nobody has agreed to. Drive selection from the fresh capture's
   actual variant demand plus the localisation inventory, not from the inventory
   alone. The manifest's `future_inventory` already holds 354 selected tier 5-7
   carrier pairs with provenance.
4. **Finding 4** - decide whether any country/tier receives `nsb_engines0` and
   `Petrol_1`; requires a historical mapping and balance contract before implementation.
5. **`mp_uav_1`** - the two ISR grants need a content owner's decision; the validator
   carries them as a named exception until then.
6. **Deferred content batches**, in this order and each with an explicit slot-budget
   statement: amphibious (only together with marine sub-unit supply), artillery/AA
   against the frozen manifest, night/thermal vision, page-2 specials. This is
   Finding 6 phase 3 for everything except artillery/AA, and it needs item 2's free
   slots to exist first - ten of these families have no module at all today.
7. **Envelope calibration** slots in before any batch that needs static estimates as
   acceptance evidence, and before item 2's free slots widen what a design can mount.

Estimator status: module parents no longer stack predecessor stats. Radar II fuel 1.2
and GL ATGM III hard attack 95 are tested regression anchors. Full-design ordering,
caps, role bonuses, inherited chassis defaults, technology/MIO effects and agreed
tolerances remain uncalibrated. The envelope report samples 11 of 21 tank generations.
