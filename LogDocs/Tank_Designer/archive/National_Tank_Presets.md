# National tank presets - first implementation batch

Date: 2026-09-06. Builds on Claude's slot namespace and entity alias updates.
The owner confirmed the prior QA issues are fixed; the stale open-issue list
in ContextUpdate-9-6-26-1819 is not a new defect list.

## Implemented

Fourteen NSB starting medium-tank presets replace their producer's generic
equivalent. Names follow existing country equipment localisation; existing
OOB chassis assignments remain unchanged.

| Medium chassis tier | USA | SOV |
| --- | --- | --- |
| 0 | M4 Sherman | T-34-85 |
| 1 | M26 Pershing | T-44 |
| 2 | M46 Patton | T-54 |
| 3 | M47 Patton | T-55 |
| 4 | M48 Patton | T-62 |
| 5 | M60 Patton | T-64A |
| 6 | M1 Abrams | T-72 |

These are legacy tier mappings, not assertions that chassis technology years
equal historical vehicle introduction dates. Historical remapping would also
require research and OOB allocation changes, outside this batch.

Exact recipes live in National_Tank_Preset_Manifest.json and are checked against
common/scripted_effects/CWIC_national_tank_presets.txt. Loadouts are authored
approximations using existing modules: Soviet diesel/smoothbore progression,
late carousel loaders and composite armor; US gasoline/diesel/turbine engines
and rifled guns. All have kinetic and HE ammunition and coaxial MGs. Late US
gun naming follows the available module ladder, not exact historical gun
classification. Further historical refinement remains possible.

The national helper runs before generic setup. Both use producer-local,
per-chassis flags: repeat calls add newly unlocked designs without recreating
old ones. USA/SOV medium tiers 0-6 are excluded from generic setup. The 1980
research helper refreshes NSB designs after granting technologies. Unused
special slots are explicitly empty, with zero engine/armor upgrades.

OOB requests resolve names by producer, creator or owner, not merely the country
loading the OOB. Foreign requests in Canada, Italy, Mongolia and China retain
their US/Soviet owners. Quantities, chassis IDs and non-NSB OOBs are unchanged.
The 125 generic AI historical recipes remain unchanged: this is bookmark
setup, not national AI redesign or automatic future-research preset creation.

## Calibration status

The diagnostic estimator no longer sums upgrade predecessors into installed
module values. Regression anchors are Radar II fuel consumption 1.2 and
gun-launched ATGM III hard attack 95, matching prior module-level QA. This
changes tooling, not module balance.

Full-design calibration remains pending. Static estimates do not certify engine
modifier ordering, caps, role bonuses, inherited chassis defaults, technology
or MIO effects. Passing the envelope report does not certify these new recipes
against frozen workbook targets. Workbook, balance CSV, renamed slots and
entity aliases are untouched.

## Verification and next handoff

Run the military validator with --tank-self-test, --tank-balance-report,
--tank-module-balance-report and --tank-envelope-report. Contracts cover the
14-entry manifest, national names, explicit slots, creation guards, generic
exclusions and producer-aware OOB references.

Fresh-game acceptance is still needed for this batch: inspect USA/SOV 1949 and
1980 designs, production and stockpiles; inspect foreign-owned examples; repeat
the bootstrap and confirm one design per name/type; save/reload; smoke test
non-NSB. Record finished design stats with upgrades/MIO/technology context
before claiming full calibration. Old saves are not migrated.

Next major implementation is APC/IFV designer conversion on existing hulls,
retaining non-NSB equipment and the accepted Heavy Mech III 1955 exception.
