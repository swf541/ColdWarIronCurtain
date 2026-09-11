# Tank Designer

Working documentation for the CWIC tank/mechanized designer rework on branch
`tank-designer-and-doctrine-rework-test`.

Consolidated 2026-09-08 from 18 overlapping documents. Superseded originals are in
`archive/`; bulk data is in `data/`. **Do not read `archive/` unless you are chasing
the provenance of a specific decision** - everything still true was carried forward
into the five documents below.

## Read order

| # | Document | Read it for |
| --- | --- | --- |
| 1 | `STATUS.md` | What is committed, what is open, what to do next. Start here. |
| 2 | `DECISIONS.md` | Ratified choices. Check before proposing a redesign - most questions are already answered. |
| 3 | `REFERENCE.md` | Hull tables, envelope mapping, designer routing mechanics, file map, validator contract. |
| 4 | `BALANCE.md` | Frozen stat targets, source decode recipes, artillery/AA targets, research costs. |
| 5 | `TankQANotes.txt` | The owner's raw QA notes, verbatim. |

`GOTCHAS.md` in the repository root applies to all work here.

## Data files - query, never read

These are too large to read into context. Query them with `python3` or `grep` and
report only the rows you need.

| File | Size | Notes |
| --- | --- | --- |
| `data/APC_IFV_Preset_Manifest.json` | 1.0 MB | 572 preset pairs, full provenance |
| `data/Tank_Designer_Slimemix (1).drawio` | 1.0 MB | 12 deflate+base64 pages; decode recipe in `BALANCE.md` |
| `data/2023 - CWIC Tank Rework Balance.xlsx` | 188 KB | **Frozen. Must stay byte-identical.** |
| `data/2023 - CWIC Tank Rework Balance(Total Balance Sheet Minimal).csv` | 60 KB | The living balance mirror |
| `data/APC_IFV_Bookmark_Mapping.md` | 103 KB | 572-row mapping table + 100 resolved OOB requests |
| `data/National_Tank_Preset_Manifest.json` | 10 KB | The 14 USA/SOV medium presets |
| `data/Balance_Target_Manifest.md` | 12 KB | The frozen 40-row envelope manifest |
| `data/Artillery_AA_Target_Manifest.md` | 5 KB | Frozen artillery/AA/AT/SAM targets |

`Balance_Target_Manifest.md`, `Artillery_AA_Target_Manifest.md` and the two JSON
manifests are **parsed by the tools**, not just read by humans. Their formats are
machine contracts - edit carefully and do not reformat. `BALANCE.md` describes them and
deliberately does not duplicate their tables.

Workbook SHA-256, re-verify after any pass that could touch it:
`dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`

## Validation

Run the first command as a baseline **before** editing, and again after. Report the
delta, not a narrative.

```bash
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-self-test
python3 "CWIC Backup/tools/validate_military_reworks.py" --tank-balance-report --tank-module-balance-report --tank-envelope-report
python3 "CWIC Backup/tools/loc_audit_1.py" --check
git diff --check
```

Current expected pass line, re-measured 2026-09-10:

```
1317 technologies, 288 tank modules, 135 historical tank designs,
40 generic bookmark variants, 586 national presets and
560 named OOB requests across 68 NSB OOBs, 76 country-history bootstrap sites,
6220 stockpile grants, 8 APC designer hulls, 8 IFV designer hulls,
and 20 designer slots checked
```

**Twenty is an engine cap, not a design choice.** `pos_custom_module_slot_window_20`
never renders. See `STATUS.md` Finding 17.

**`equipmentdesignerview.cpp:3657: Failed to change role` is ignorable when the design is
already in the named role.** Carrier modules carry `allow_equipment_type`, which assigns the
role as soon as they are fitted, so selecting that role in the dropdown is a no-op the engine
logs as a failure. It cost three debugging rounds. See `STATUS.md` Finding 24.

The historical-design count is family x tier x role, so it moves whenever a role does:
125 -> 100 when flame was removed (three roles across 10 / 10 / 5) and 100 -> 155 when
phase 3 added six light/medium roles and retired heavy AA (+60 -5). No design content is
lost when it falls.

**Never run the validator while a `-debug` game is live.** Check `pgrep hoi4` first. The
APC and IFV negative fixtures write to the real `mechanized.txt` and
`mechanized_heavy.txt`; a `-debug` game hot-reloads them and logs 2380 spurious
`A limit for category X already exists` lines. See `STATUS.md` Finding 8.

`git diff --check` reporting trailing whitespace in `GRE - Greece.txt` is expected;
that file is CRLF in the index.

The localisation audit covers 22 SEA files, not all tank localisation.

**A passing validator is not balance acceptance.** The full-design estimator
calibration gap is open: it does not model engine ordering, caps, role bonuses,
inherited chassis defaults, or technology/MIO effects, and no tolerance bands were
ever agreed. Say which of the two you are claiming.

## Runtime

Launch detached - a tracked background game process gets killed under memory
pressure during load.

```bash
cd "<steam>/steamapps/common/Hearts of Iron IV"
setsid nohup ./run_hoi4 -mod=mod/Cold_War_Iron_Curtain.mod -debug -ai_testing >/dev/null 2>&1 &
```

`-ai_testing` starts the default bookmark only and does not accept a start-date
argument. To test 1980, temporarily date the gathering-storm bookmark to
`1980.1.1.12` and revert the edit afterwards.

Live log: `~/.local/share/Paradox Interactive/Hearts of Iron IV/logs/error.log`.
Diff it against a baseline captured before the change. Use fresh campaigns; old
saves are not migrated.

Do not claim live testing you did not perform.

## Guardrails

**Protected - do not stage, edit or delete:** `CWIC Backup/` except the maintained
validator `validate_military_reworks.py`; root `HANDOFF.md`; root `error.log`,
`error_1.log`, `error_2.log`, `game.log` (stale, dated 2026-09-02, not current
evidence); doctrine documents; screenshots; lock files; `.gitignore` and
`interface/popupwindow.gui`, which carry other people's uncommitted work.

**Never rewrite the workbook with `openpyxl`.** `Total Balance Sheet` holds 217
formulas; openpyxl writes formulas without their cached `<v>` values and the
validator reads exactly those. The `Implementation Status` sheet was added by a
surgical zip edit. Re-stamp the SHA in `BALANCE.md` after any workbook change.

**Localisation is ASCII-only and needs the BOM.** `.yml` files must keep the UTF-8
BOM; script and GUI files must never gain one. Verify bytes, not text, across the
whole changeset. Only section-sign colour codes and pound-sign texticon prefixes are
legal non-ASCII. English only - never touch `french/` or `japanese/`.

**The validator hardcodes magic numbers.** Any balance change needs a matching
validator edit. Grep for the module name before assuming a value is free to change.

**Tech tree coordinates must be compared with year anchors resolved.** `y = @1955`
and `y = 6` are the same cell; a raw string comparison misses collisions. Do not fix
a collision by moving a technology to an arbitrary free cell - keep each family in
one column and move the minimum.

**`interface/texticons.gfx` is a full override.** Anything vanilla adds there in a
patch is lost unless mirrored. The same trap applies to any wholesale override.

**Commit trailers:** no commit on this branch carries a `Co-Authored-By` or
`Claude-Session` trailer. Match the surrounding history.

**Ignorable engine noise, already triaged - do not chase:** roughly 255
`Entity referenced in equipment graphic database does not exist` and
`Unknown equipment type: modern_tank_chassis / super_heavy_tank_chassis` lines come
from the base game's graphics database referencing equipment this mod deliberately
removed. Zero hits under `Cold War Iron Curtain/`.

## Stale paths

Tools moved under `CWIC Backup/tools/` in `a997a48e0e`; the root `tools/` directory
no longer exists in git. `CWIC Backup/tools/loc_audit.py` and `loc_audit_1.py` are
byte-identical duplicates; one should be deleted rather than both maintained.

Several documents here are untracked and device-local, so they do not accompany a
clone on another device: `TankQANotes.txt`, `Screenshots_9-6-26/`, and the archived
`HANDOFF_Deferred_Scope.md` and `ContextUpdate-9-6-26-1819`.
