# CWIC tank designer implementation report

The Luna implementation packets are complete in the current worktree.

## Implemented packets

- Packet A: flame support chassis grants, inactive flame roles, repaired module parent graph, corrected chassis count limits, corrected NSB armor rows, removed the three tank technology self loops, and preserved the one base research cost with 168 follow-on costs.
- Packet B: corrected turret stats, left anti-air cannon air attack at its original 18/32/46 values, added four secondary turret modules, exposed the secondary turret slot on all 30 designer chassis variants, retained engine and armor upgrade sliders, and repaired module abbreviations and icon/localisation contracts.
- Packet C: added legacy/NSB focus branches for American, Soviet, Greek, and Finnish tank rewards, including producer-scoped licenses, stockpiles, and stable export variants.
- Packet D: bounded the tank role selector, repaired the armor modules tab sprite, removed 24 orphan amphibious designer GUI files, and added the role labels required by the designer.

## Static evidence

The validator currently reports these repository counts:

| Contract | Count |
| --- | ---: |
| Technologies | 1,933 |
| Tank modules | 246 |
| Historical tank designs | 125 |
| Bookmark variants | 30 |
| Named OOB requests | 460 |
| NSB OOBs | 68 |
| Country-history bootstrap sites | 76 |
| Tank designer chassis slots | 15 |

The balance scope is frozen in [Balance_Target_Manifest.md](Balance_Target_Manifest.md): 40 workbook rows, consisting of 39 targets and one M1 Abrams reference, with 21 tank targets and 18 mechanized targets.

Validation commands completed successfully:

```text
python3 -m py_compile tools/validate_military_reworks.py
python3 tools/validate_military_reworks.py --tank-self-test
python3 tools/validate_military_reworks.py --tank-balance-report
```

The tank self-test includes parser, module-parent, secondary-module, abbreviation, technology-loop, export-variant, and ammunition-category negative fixtures. The balance report verifies that the manifest still matches workbook rows 2 through 41.

## Deviations and limits

- The instruction to change `tank_super_heavy_cannon` to `tank_heavy_main_armament` was implemented as the module category change. The existing module ID, localisation key, graphics key, and national overrides remain stable so saved equipment references are not broken.
- Duplicate technology coordinates found during validation were moved to unused cells in their owning trees. This preserves every technology while satisfying the unique-coordinate contract.
- Runtime UI acceptance still requires launching the game client and checking 1920x1080 at 1.0, 2560x1440 at 1.0 and 1.4, and 3840x2160 at 2.4. The static GUI contract verifies the bounded role viewport and the preserved 50-pixel role entries; lower-resolution 2.4 behavior remains a client-side check.
- Fresh 1949 and 1980 NSB and non-NSB starts, historical focus execution, and save/load behavior also require a game-client smoke test. No old-save compatibility claim is made here.
- The balance report validates the normalized workbook target manifest and its worksheet-row provenance. It does not claim that shipped AI or bookmark designs meet those envelopes because fresh runtime design samples and independent stat calculations were not captured in this pass.
