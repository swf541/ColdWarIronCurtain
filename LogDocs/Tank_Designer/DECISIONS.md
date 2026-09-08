# Ratified decisions

Accepted choices. **Check here before proposing a redesign - most of it is settled,
and several entries record a wrong answer that was already tried.** The owner has
authorized practical design judgment within this scope; no repeat approval is needed.

## Architecture

**APC and IFV are standalone designer families**, not roles on the light and medium
tank hulls. Superseded 2026-09-07 on evidence: the drawio `[REFERENCE] Whole Tech Tree`
mechanized column specifies a dedicated ladder separate from every tank hull column.
Light Mech is the APC line (`mechanized_equipment` / `apc_chassis_*`); Heavy Mech is
the IFV line (`mechanized_heavy_equipment` / `ifv_chassis_*`). See "Three conflicting
carrier designs" below.

**Heavy APC and Heavy IFV are a medium hull generation**, not more tiers on the
light-hull families. Both the xlsx `Roles` tab and the drawio AFV Hulls page place them
there (Heavy APC 1985 off Second Gen MBT, Heavy IFV 2005 off Second+ Gen MBT). Not
started.

**Tier count and years come from the frozen manifest, not the diagram.** 8+8 at
1947/1950/1960/1965/1975/1985/1995/2005, from the 18 mechanized envelope rows. The
diagram's seven-tier decade cadence is a sketch. Do not "correct" the years to it.

**`mechanized_heavy_equipment_3` stays at 1955.** The workbook's 1960 is a deliberate
year exception and is not permission to alter the stats or the workbook. `nsb_ifv_hulls2`
carries `start_year = 1955` and the `@1955` tree row so tree, tooltip and hull agree.

**The 15-position designer is final.** Five mandatory slots plus ten specialized
special slots. No further layout expansion is approved or needed. The GUI defines
exactly 15 positions, the validator asserts `pos_custom_module_slot_window_0..14`, and
`equipment_modules` is 515 wide against a seventh column ending at exactly 515 - zero
slack. Any slot frame wider than 76px re-clips.

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

## Module balance, ratified 2026-09-05

| # | Question | Outcome |
| --- | --- | --- |
| 5.3.1 | Reliability expressed two ways | **Kept split.** Guns use a negative multiplier, turrets a positive flat add. Units genuinely differ; converting would touch 13 blocks for cosmetic consistency. |
| 5.3.2 | `cwic_hull_mg` flat `defense = 0.5` | **Reduced to 0.25.** Script, CSV and both workbook tables updated. |
| 5.3.3 | Secondaries lacked reliability cost | **All four now carry one:** coax -0.005, hull MG -0.005, HMG -0.01, autocannon -0.025 unchanged. |
| 5.3.4 | Turret cost ordering | **LP premium kept, 1.5 tie broken.** `oscillating_turret` 1.5 to 1.75, dismantling 0.75 to 0.875, preserving the file-wide 0.5 ratio. |
| 5.3.5 | 12 of 15 sub-units `active = yes` | **Normalised to `active = yes`, not `no`.** The manual's recommendation was wrong: legacy `armor.txt` enables only `light_armor`, `medium_armor`, `heavy_armor`, `super_heavy_armor`. The 9 role brigades and 3 flame tanks are enabled only by `nsb_iw_armored_vehicles`, so in a non-NSB profile `active = yes` is the sole thing making them buildable. Setting them to `no` would have deleted them from non-NSB play. The validator contract was inverted to match. |
| 5.3.6 | `tank_gasoline_engine` home, missing `xp_cost` | **Base engine, not a duplicate.** It is `Petrol_0`'s declared parent and the `engine_type_slot` default at `tank_chassis.txt:391, 795, 1200`. Gains `xp_cost = 1` and `dismantle_cost_ic = 0.5`. |
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
    misleads. The three SPAA variants deliberately carry no ammunition, because AA guns
    supply their own attack.
11. `sp_tag_tank_speed_factor` is an invalid modifier in
    `common/dynamic_modifiers/wuw_dynamic_modifiers.txt` - one live log error,
    tank-adjacent, trivial, unowned.
12. `common/national_focus/PHI_1950s.txt:587` grants `apc_equipment_1`, which is not an
    equipment id anywhere in the repo, so the focus silently awards nothing.
    `apc_equipment_1` exists only as the `derived_variant_name` of `apc_chassis_1`,
    which is a localisation key rather than an equipment type. Predates the APC work.
    Most likely wants `mechanized_equipment_3`, or a designer APC. Flagged for whoever
    owns PHI.
