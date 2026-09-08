# Status

Branch `tank-designer-and-doctrine-rework-test`. Last updated 2026-09-08.

## Where the project stands

Tier 1 and Tier 2 of the original completion plan are shipped and stable. The APC and
IFV designer families are built, validated and accepted in live QA. Bookmark presets
and the NSB OOB migration are committed. What remains is historical coverage, three
QA findings, and the deferred content batches.

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

### Finding 1: legacy armour focus awards were never migrated to NSB designer equipment

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

### Finding 2: `tank_gasoline_engine` outperforms the entire CWIC petrol ladder

| Module | Localised name | Speed multiplier |
| --- | --- | --- |
| `tank_gasoline_engine` | Gasoline Engine | **0.15** |
| `Petrol_0` | WW2 Gasoline Engine | 0.05 |
| `Petrol_1` | Post-WW2 Gasoline Engine | 0.07 |
| `Petrol_2` | Early Cold War Gasoline Engine | 0.09 |
| `Petrol_3` | Mid-Cold War Gasoline Engine | 0.11 |

`tank_gasoline_engine` is the vanilla module, inherited unchanged, and CWIC's only
module on `category = tank_engine_gasoline` outside the `Petrol_*` ladder. It is
enabled by the base NSB armour tech (`NSB_armor.txt:63`) while `Petrol_0` is gated
much later (`NSB_armor.txt:1074`). The earliest, cheapest gasoline engine is strictly
the best one, beating even Mid-Cold War petrol.

**Blast radius:** all 40 generic and 576 of 586 national presets use
`engine_type_slot = tank_gasoline_engine`. Rebalancing the ladder or retiring
`tank_gasoline_engine` in favour of `Petrol_0` means re-pointing every carrier preset
recipe and re-checking the frozen envelopes. Do this **before** authoring further
preset tiers, not after.

Note that `tank_gasoline_engine` is not a stub and must not simply be deleted:
`Petrol_0` declares it as `parent`, and it is the `engine_type_slot` default at
`tank_chassis.txt:391, 795, 1200`.

### Finding 3: presets show the generic carrier icon, not per-design art

`BTR-40` renders with the generic APC picture. `apc_chassis_*` and `ifv_chassis_*`
declare no `picture` of their own in `common/units/equipment/mechanized.txt`, so every
carrier design inherits `archetype_motorized_equipment` from the `mechanized_equipment`
archetype (`mechanized.txt:11`). Legacy per-country carrier equipment had its own art;
a designer design has one name but no art hook per name.

Stats are the good news: the owner confirms legacy and new NSB APC/IFV stats match
closely, so the module baselines are landing where they were aimed.

Unresolved: whether carrier designs get per-chassis pictures (cheap, one icon per hull
tier, still not per-vehicle), or whether the tank icon-generation path can be reused
for the mechanized archetype at all.

## Owner QA notes, 2026-09-06 playtest

Both NSB and non-NSB loaded clean at 1949 and 1980. Verbatim notes are in
`TankQANotes.txt`; screenshots in `Screenshots_9-6-26/`. Still open:

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

## Not yet verified, any batch

Newest-only production visibility, save/reload of a saved design, non-NSB regression,
long-run AI production behaviour with mechanized now also in the `armor` domain, the
1980 bookmark path end to end, and whether the AI ever assigns factories to `land_apc`
or `land_ifv` without a `role_ratio`.

On that last point: `common/ai_equipment/generic_tank.txt` defines eight `history = yes`
recipes for each of `land_apc` and `land_ifv`, and no `role_ratio` strategy in this
repository names either role. The installed game's `_documentation.md` does not specify
default demand when an explicit ratio is absent. Static recipe availability does not
demonstrate factory assignment, but absence of a ratio does not prove failure either.
No AI strategy change is justified by this evidence alone. Deferred to the final
designer AI pass.

Also outstanding from Tier 3: a runtime render check of the legacy armour folder for
non-NSB players, and a designer UI pass at 1920x1080 and 2560x1440 at 1.0x and 2.4x.

## Next scope

1. **Finding 2 first.** It has the widest blast radius and gates further preset
   authoring. Decide the engine ladder, then re-point presets and re-check envelopes.
2. **Finding 1.** The 301 focus grants, with a validator contract. Plan the mapping
   rule and its exception list before editing; the applications themselves are
   mechanical once the rule exists.
3. **QA items 2 and 4** - research date gating and ahead-of-time penalties. Bounded.
4. **QA items 3, 6, 7** - turret stat check, radar tooltip verification, focus-effect
   verbosity. Bounded cleanups.
5. **Finding 3** - carrier art decision.
6. **Historical coverage sweep.** Explicitly required, not optional polish: named
   designs for **all** armour vehicle families (light, medium, heavy, APC, IFV and other
   armoured roles) across all countries, or at minimum every country with a
   corresponding non-NSB vehicle already implemented. The 14 national medium presets do
   not complete this. Drive it from the existing `TAG_<equipment>` localisation
   inventory rather than inventing mappings. The manifest's `future_inventory` already
   holds 354 selected APC/IFV tier 5-7 pairs with provenance.
7. **Deferred content batches**, in this order and each with an explicit slot-budget
   statement: amphibious (only together with marine sub-unit supply), artillery/AA
   against the frozen manifest, night/thermal vision, page-2 specials.
8. **Envelope calibration** slots in before any batch that needs static estimates as
   acceptance evidence.

Estimator status: module parents no longer stack predecessor stats. Radar II fuel 1.2
and GL ATGM III hard attack 95 are tested regression anchors. Full-design ordering,
caps, role bonuses, inherited chassis defaults, technology/MIO effects and agreed
tolerances remain uncalibrated. The envelope report samples 11 of 21 tank generations.
