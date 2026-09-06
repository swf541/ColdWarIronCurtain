# Deferred designer progress

## 2026-09-06: owner QA fixes and specialized slots

The owner supplied QA results and Section 8 choices in `TankQANotes.txt` after
the source-freeze session below. Current decisions, implemented changes and
remaining work are recorded in `Deferred_Design_Decisions.md`. Those accepted
choices supersede the earlier "owner decisions pending" statements below.

This batch fixes 14 research dates, Finland's DLC-specific focus condition,
USA/SOV 1980 tank research, export tooltip internals, export-only production
clutter, and the identical conventional/light turret choice. The ten special
slots are now specialized while retaining the existing 15-position designer.
National presets, APC/IFV conversion and the subsequent content batches remain
open. No new runtime acceptance is claimed.

Validation passed: military validator and tank negative fixtures, balance and
module reports, diagnostic envelope report, targeted recipe/slot compatibility,
14 technology date/row contracts, 1980 research coverage, four export branch
contracts, SEA localisation audit (22 files), and `git diff --check`.
The artillery/AA manifest also matches its frozen workbook. The user-staged
move of its checker into `CWIC Backup/tools/` leaves its root calculation one
directory too shallow; that check used an in-memory root correction and did not
edit the relocated file. The staged tool move/deletions and unrelated files
remain separate from this batch.

## 2026-09-06: artillery/AA source freeze (Session B)

Completed the handoff's script-only target freeze in
`Artillery_AA_Target_Manifest.md`, with a reproducible standard-library extractor
and checker at `tools/artillery_aa_targets.py`. The workbook remains byte-identical.
The manifest freezes 31 vehicle rows (111 combat-stat cells) and six module cost
bands, preserving worksheet cell references and original years alongside the
canonical-grid mapping. Year mapping is an explicit implementation decision;
it does not rewrite source data or create extra tiers.

Validation passed: military validator, tank self-tests, tank balance report,
module balance report, envelope report, `tools/loc_audit.py --check`, manifest
check, and `git diff --check`. The localisation command reports 22 SEA files;
it is not a global localisation audit. Workbook-hash and manifest-drift rejection
paths were also checked. Envelope estimates remain diagnostic, with 10 of 21
tank generations unsampled; passing the report does not establish live balance.

Session A is still open. No live game was launched or visual acceptance claimed
in this session. Both armor tabs, fresh 1949/1980 NSB and non-NSB starts, live
design stats, export rewards, and save/reload still need the handoff's runtime
checks. The cosmetic 3D fallback decision remains open. Source preparation was
performed independently of that gate; no game content has been changed.

Recommended continuation: complete Session A, calibrate envelope evaluation,
then build the APC/IFV conversion while retaining non-NSB legacy support. For
artillery/AA, DLC-gated delivery is the compatibility-preserving option; the
new manifest does not itself authorize retirement of legacy equipment. These
are recommendations, not completed owner decisions. Heavy Mech III's 1955/1960
discrepancy, amphibious scope, invented vision stats and special-slot choices
remain open as listed in the handoff.

The existing staged files under `CWIC Backup/` and unrelated untracked files
were left untouched. The old handoff's clean-worktree statement is historical,
not the state observed at the start of this session.
