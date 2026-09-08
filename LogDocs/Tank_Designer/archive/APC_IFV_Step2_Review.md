# APC / IFV Step 2 verification gate

Date: 2026-09-07. Branch `tank-designer-and-doctrine-rework-test`.
Implementation baseline: `faddc3dd5e` (`Add IFV designer family`).
This is the gate output promised by `IFV_APC_HANDOFF.md`; the batch is verified
static-only and is still uncommitted in the working tree.

## Gate result

`CWIC Backup/tools/validate_military_reworks.py` passes:

```
1303 technologies, 269 tank modules, 125 historical tank designs,
40 generic bookmark variants, 586 national presets and
560 named OOB requests across 68 NSB OOBs, 76 country-history bootstrap sites,
8 APC designer hulls, 8 IFV designer hulls, and 15 designer slots checked
```

Against the `faddc3dd5e` baseline (30 generic variants, 14 national presets,
460 named OOB requests) this batch adds 10 generic carrier designs, 572 national
carrier designs and 100 named carrier OOB requests. Bootstrap site count is
unchanged: the carrier grants land inside the existing 76 sites.

## Two failures the first gate run reported, and their resolution

### 1. Global design-name uniqueness was the wrong invariant

The validator keyed every recipe by name alone and failed on any repeat, which
produced 382 `duplicate tank recipe name` failures. The invariant does not hold
for carriers: a design name is only unique per country, and the presets give 86
tags the same exported vehicles. Verified over the preset file: 216 distinct
`(name, chassis)` pairs, **zero** with conflicting loadouts, so every repeat is a
byte-identical re-creation for another tag.

Ten names legitimately span two chassis tiers, because an incomplete national
ladder shifts a vehicle up or down relative to the common ladder:

| name | lower tier (tags) | higher tier (tags) |
| --- | --- | --- |
| BTR-40 | apc_chassis_0 (22) | apc_chassis_1 (FIN) |
| M9 Halftrack | apc_chassis_0 (FRA) | apc_chassis_1 (CAN) |
| M59 | apc_chassis_1 (BEL) | ifv_chassis_1 (TUR) |
| BTR-152 | apc_chassis_1 (3) | ifv_chassis_0 (25) |
| BTR-60 | apc_chassis_2 (3) | apc_chassis_3 (YUG) |
| BTR-60PB | apc_chassis_2 (ADR) | apc_chassis_3 (17) |
| BTR-50P | ifv_chassis_1 (17) | ifv_chassis_2 (RAJ) |
| BTR-50PK | ifv_chassis_1 (6) | ifv_chassis_2 (14) |
| MT-LB | ifv_chassis_2 (9) | ifv_chassis_3 (FIN) |
| BMP-1 | ifv_chassis_3 (20) | ifv_chassis_4 (FIN) |

`_variant_recipes()` is now keyed by `(name, chassis)` and fails only on a real
conflict - the same name on the same chassis with a different loadout. The
name-only view the frozen-envelope map needs is `_variant_recipes_by_name()`,
which marks a name ambiguous rather than silently keeping the last recipe; the
envelope map fails on an ambiguous sample. No envelope target is ambiguous.

### 2. Three medium-tank OOB requests contradicted the new attribution rule

The batch's decision 1 resolves a design's producer as producer, then creator,
then owner, then the OOB tag. Under that rule three pre-existing requests break:
they ask for a generic design name while naming SOV as creator, and SOV creates
national names at every medium tier, never the generic one.

Owner decision: name the Soviet design. Applied:

- `KPA_1949_nsb.txt:594` - `medium_tank_chassis_0` now `version_name = "T-34-85"`.
  Historically correct; the 1949 KPA armoured division ran Soviet-supplied T-34-85s.
- `BUL_1949_nsb.txt:183,193` - `medium_tank_chassis_1` now `version_name = "T-44"`,
  SOV's tier-1 national design. Noted at decision time: Bulgaria did not field
  T-44s in reality; the request's chassis tier, not the name, is the ahistorical part.

These three requests were latent breakage, not a regression from this batch. The
old first-token attribution resolved them to BUL/KPA, which do create the generic
designs, so the gate never looked at SOV.

## Independent spot checks

- 100 carrier requests across the NSB OOBs, every one carrying an explicit
  `version_name`. Tier distribution: apc 45/2/6/12/4, ifv 6/3/7/14/1.
- No NSB OOB still references `heavy_mechanized_equipment*`,
  `mechanized_heavy_equipment*` or `mechanized_equipment_3+`.
- No added line in the whole diff contains a non-ASCII byte, and no touched mod
  file carries a BOM.

## Owner QA outcome, 2026-09-08

Passed and committed. Both bookmarks load, presets load, stockpiles and factory
lines exist, `error.log` is acceptable. AI production is deferred to a single
final pass once the remaining designer content is in, at the owner's direction.

Three findings came out of the run - legacy armour focus awards never migrated to
NSB designer equipment, `tank_gasoline_engine` outperforming the `Petrol_*`
ladder, and carrier designs inheriting the generic archetype picture. All three are next-session scope and
written up in `IFV_APC_HANDOFF.md`. Finding 2 is the one that touches this batch:
every carrier preset uses `tank_gasoline_engine`, so an engine rebalance means
re-pointing all of them.

## What this gate did not establish

Static verification only; the owner QA above supersedes it for start-up loading,
presets, stockpiles and factory lines. Still unverified: newest-only production
visibility, save/reload, non-NSB regression, and the open question of whether the
AI ever assigns factories to `land_apc`/`land_ifv` without a `role_ratio` - that
last one is explicitly deferred to the final designer AI pass.
