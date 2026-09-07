# National Focus Icon Session Handoff

Companion to `HANDOFF.md` (VIN/FRE rework), which is a separate, unrelated document - do not merge them.

## Checkpoint

- Repository: `/home/zom/Projects/ColdWarIronCurtain`
- Branch: `development-branch`
- Base commit before this work: `b63efa1f6a` (`More VIE event pictures`)
- Status: **committed** as `Consolidate and rename the generic focus icon library` (797 files).
  Deliberately left out of it and still uncommitted: `tools/` (untracked) and the `.gitignore`
  change.
- Two things in that commit came from the first session and are **not** icon work:
  - `SIA_50s.txt` carries 474 lines of pure trailing-whitespace churn (398 blank-line trims plus
    ~76 lines whose only change is a stripped trailing space). No content change at all.
  - `VIN_50s.txt` carries 5 deliberate focus-coordinate edits (`x = 0` -> `x = -1`, `y = 4` -> `y = 3`).
  Every other focus file in the commit changes `icon =` lines only.

## What this session was for

The Indochina focus trees used placeholder and borrowed icons (`GFX_unknown`, KMT art on Vietnamese
focuses, USA art in the Laos tree, heavy intra-tree repetition). The user imported 22 new generic
icons to draw from. Work expanded from there into three engine-level rendering bugs that were
breaking icons mod-wide, unrelated to Indochina.

## Curation state - read this first

The automated remap in this session was too aggressive in one specific way: it treated *any* repeated
icon inside a tree as a defect and reassigned the second and later uses, **including focuses that
already had correct, purpose-drawn bespoke art**. In `VIE_50s_CuongDe.txt` it overwrote real icons
such as `GFX_VIE_Intercept_CuongDe_Return_Bangkok` and `GFX_VIE_CuongDe_Press_Conferences`.

The user reviewed the diff by hand and reverted what was wrong. The resulting working tree is the
source of truth:

- **Staged changes are user-verified.** Treat them as correct.
- **Reverted files are deliberate.** The original icons in them are human-checked and correct.
- The user chose to keep the `GFX_unknown` replacements ("better something than nothing").

15 focus files are currently modified:

```
50s_LAO.txt          CAM_50s.txt        FRE_50s_Indochina.txt   MAL_1950s.txt
MEO_50s.txt          MLA_50s.txt        SIA_50s.txt             Shared_LAO.txt
Shared_MLA_MQJ.txt   TIB_1950s.txt      VIE_50s_CuongDe.txt     VIE_50s_Diplo.txt
VIE_French_Hinh.txt  VIN_50s.txt        VIN_FORPOL.txt
```

**Rule for any future remap:** never replace an icon whose sprite name matches `GFX_<TAG>_*` and
resolves to bespoke art. Only remap placeholders (`GFX_unknown`, `GFX_goal_unknown`) and vanilla
`GFX_goal_generic_*` / `GFX_focus_generic_*` fillers.

## Three rendering bugs found and fixed

These were the real cause of "icons look broken even though the files are fine", and none of them
were specific to Indochina.

### 1. 16-bit PNGs (322 files) - the big one

HOI4's PNG loader only handles 8 bits per channel. Given a 16-bit (64-bit RGBA) file it walks the
buffer at half the true stride, rendering a magenta, horizontally smeared image. The art itself is
fine and looks correct in every viewer outside the game.

- 22 were the newly imported generic icons
- 4 were pre-existing in `Generic_National_Focus/` (`Diplomacy_52`, `Military_46`, `Production_22`,
  `Research_23`)
- **~296 were pre-existing under `gfx/interface/goals/USA_1980s/`** - the whole 1980s USA
  foreign-policy art set had been rendering this way

Fixed by `tools/png_depth_fix.py`. 322 converted, 0 failed, re-scan finds none left.

### 2. Uncompressed DDS in the generic focus library (74 files)

`Generic_National_Focus/` held 74 dds, 67 of them uncompressed 32-bit ARGB8888 and one 16-bit
A1R5G5B5 - formats Clausewitz renders unreliably. All converted to png and the dds deleted, with
**1124 references repointed** across 7 registries (`texturefile` and `animationmaskfile` both, so
shine masks follow the art).

Caveat worth carrying forward: `goals/VIE/` holds 127 uncompressed-32 dds that apparently render
fine, so format alone does not fully explain the failures. If more icons look wrong, check bit depth
and file magic before assuming the format is the cause.

### 3. Duplicate sprite registries

`CWIC_goals.gfx` was a strict subset of `IC_goals.gfx` - 7995 sprites, every body byte-identical,
zero unique. `CWIC_goals_shine.gfx` was near-identical with 8 unique entries, all of which pointed at
textures that do not exist and had no base sprite anywhere. Both files were deleted.

Duplicate sprite names across `interface/`: **16,905 -> 1,038**. Verified no regression: 56,655 ->
56,652 sprite names, the 3 lost (`GFX_Cotton_shine`, `GFX_GFX_Paper_shine`, `GFX_Paper_Two_shine`)
are referenced by no focus and were already non-functional.

## Tooling added

| Tool | Purpose |
|---|---|
| `tools/icon_audit.py` | Parses focus blocks, resolves every `icon =` against all sprites declared under `interface/**/*.gfx`, writes round-trippable CSVs to `CWIC Backup/documentation/Icon Audit/`. `--check` lints for MISSING/ILLEGAL, `--summary` prints counts. Hand columns `Verdict`/`Replacement`/`Notes` survive re-runs. |
| `tools/art_to_png.py` | Replaces `dds_to_png.py`. Converts any dds/tga/bmp under `goals/generic/` to png, verifies the round-trip (dims + per-channel means must match exactly), repoints every `.gfx` reference, deletes the original only after everything resolves. |
| `tools/gfx_lib.py` | Shared SpriteType block parser. Its `read_text`/`write_text` refuse to write a BOM or CRLF into a registry - Clausewitz rejects a `.gfx` with a BOM. |
| `tools/icon_consolidate.py` | Moved the four generic art directories into `goals/generic/<category>/` and repointed every reference. Kept for the record; the merge it performs is done. |
| `tools/icon_rename.py` | Drives the number-to-content rename from `Icon Rename Map.csv`: sprite names, `_shine` twins, art filenames and every `icon =` reference in one pass. `--check` asserts no numbered name survives anywhere. |
| `tools/png_depth_fix.py` | Finds PNGs deeper than 8 bits by reading the IHDR header directly (decoding all 17k images is far too slow - this takes 0.09s) and rewrites them as 8-bit PNG32, verifying dims and channel drift under one 8-bit step. |

All three follow the CLI shape of the existing `tools/loc_audit.py`.

## Current audit state

`python3 tools/icon_audit.py --summary`:

```
South Vietnam      677 focuses    0 placeholder   17 foreign  192 duplicate
North Vietnam      278 focuses    0 placeholder   63 foreign    2 duplicate
French Indochina    31 focuses    1 placeholder    0 foreign    0 duplicate
Laos               167 focuses    0 placeholder   14 foreign    0 duplicate
Cambodia           200 focuses    0 placeholder    5 foreign    0 duplicate
Meo Highlands       46 focuses    0 placeholder    6 foreign    0 duplicate
Malaya             476 focuses    0 placeholder   28 foreign    0 duplicate
Thailand           251 focuses   25 placeholder    2 foreign    4 duplicate
TOTAL             2126 focuses   26 placeholder  135 foreign  198 duplicate  0 missing  0 illegal
```

`--check` passes: every focus icon in the audited trees resolves to a declared sprite.

Reading these numbers correctly:

- **0 missing / 0 illegal** is the hard guarantee. No audited focus points at an undeclared sprite.
- **198 duplicates** are mostly the user's deliberate reverts in `VIE_50s_CuongDe.txt` plus mirrored
  Bao Dai / Cuong De route pairs that *should* match. Duplication is a smell, not a bug.
- **135 foreign** are borrows judged acceptable: USA-desk art on Cold War focuses, SOV/PRC art on
  communist-doctrine focuses, FRA art on French focuses. The clearly-wrong ones (Greek education art
  on Cambodian focuses, Indian RAJ art on Vietnamese focuses, German art on anti-communist focuses)
  were replaced.
- **26 placeholders**: 23 in `SIA_50s.txt` (Thailand), deliberately out of scope, plus the 3 that
  the second session exposed by teaching the auditor that `generic_focus_*_placeholder` resolves to
  `goal_unknown.dds`. Those 3 are a real gap, not a counting change.

## Broken-reference fixes

- `MLA_50s.txt` pointed at `GFX_Co-rule_with_Shamishyaalt`, which no sprite declares -> now
  `GFX_MLA_Collaborating_Shamsiah_Fakeh`.
- `SIA_50s.txt` pointed at undeclared `GFX_Red_Star_above_China` -> now `GFX_icon_generic_communism`.
- `Generic_National_Focus_Economics_22.png` never existed on disk, yet two sprites pointed at it:
  `GFX_Generic_National_Focus_Economics_22` (used by `TIB_Bhutanese_Trade_Pact`) and
  **`GFX_usa_fp_generic_financial_aid`, used by 6 focuses** across `USA_FP_50s.txt`, the 1980/1984/1988
  USA term FP trees, and `COG_70s_Communism.txt`. The TIB focus now uses `Trading_3`, the USA sprite
  now uses `Economics_15`, and the dead declaration was removed.

## New assets

- 22 imported icons moved from `generic icons/` into the mod, lowercased (case mismatches are a
  recurring source of missing-texture errors on Linux). The second session sorted them into
  `goals/generic/<category>/` and renamed them into the one library prefix, so
  `icon_generic_mas36.png` is now `generic/military/generic_focus_military_crossed_mas36.png`.
- `interface/CWIC_Generic_Icons.gfx` and `_shine.gfx` are the single home for the whole library -
  348 sprites each. Deliberately **not** added to `IC_goals.gfx`: that registry is already the union
  of everything, and a second home for these names would recreate the duplication just cleaned up.

## What the second session did

### 1. Consolidation - done

Four scattered art directories folded into one lowercase tree:

```
goals/Generic_National_Focus/  290           goals/generic/agriculture/   26
goals/GENERIC_ICONS/            48    ->     goals/generic/construction/  13
goals/Generic_Icons/            22           ... 12 categories, 362 files
goals/new_generic/               3
```

- `interface/GenericIcons/Generic_goals.gfx` + `_shine.gfx` deleted: 46 sprites each, bodies
  identical to `IC_goals.gfx`, zero unique. Same pattern as the `CWIC_goals.gfx` pair.
- 280 `GFX_Generic_National_Focus_*_shine` duplicates stripped from `IC_goals_shine_autogen.gfx`.
- `CWIC_Generic_National_Focus.gfx` + `_shine` merged into `CWIC_Generic_Icons.gfx` + `_shine`,
  348 sprites each, grouped by category with a header per group. The old pair is gone.
- Duplicate sprite declarations across `interface/`: **2598 -> 2226**, generic-focus **280 -> 0**,
  with distinct sprite names unchanged at 57090 (nothing lost).
- Library is now **100% 8-bit png**: the last 5 dds and 1 tga converted with a round-trip check.
- `Template for dummies.psd` moved out of the mod into `CWIC Backup/documentation/Icon Sources/`.

### 2. Content renaming - done

`GFX_Generic_National_Focus_Agriculture_5` -> `GFX_generic_focus_<category>_<content>`, hard rename
with no aliases. `GFX_icon_generic_*` collapsed into the same prefix, so the library has exactly one.

- 348 sprites + 348 shines renamed, 362 art files renamed to match, **1252 `icon =` references**
  rewritten across 29 focus files, 2830 texture paths repointed.
- Names come from labelled contact sheets read one category at a time:
  `Politics_1` -> `politics_petition`, `Military_2` -> `military_massed_infantry`,
  `USSR_1` -> `ussr_moscow_handshake`.
- The mapping is kept in `CWIC Backup/documentation/Icon Audit/Icon Rename Map.csv` (365 rows), so
  the rename is reviewable and reversible.

**Found while renaming:** `GFX_Generic_National_Focus_Military_11` and `Politics_19` resolved to
`goal_unknown.dds` - live placeholders sitting inside the generic library, used by 7 focuses in
BHU, Brunei, SIA, TIB and FRE. They are now named `GFX_generic_focus_military_placeholder` and
`..._politics_placeholder` and are counted as placeholders by `icon_audit.py`, which is why the
placeholder total moved 23 -> 26. **They still need real art.** A third, `USSR_9`, borrows PRC art
and is referenced by nothing.

## Open work - next session

### 1. Give the two placeholders real art

See above. Seven focuses are rendering `goal_unknown`.

### 2. Consolidation and assortment of focus definition files

Not started. `common/national_focus/` holds 490 entries including `FOR HOTFIX/`, `Old/`,
`Toberemoved/`, `NEP To Fix/`, `Need Fix/`, `Need Finished/`, `Trees for 0.35/` - **HOI4 loads these
subdirectories**, which is why `OUTDATED_PRC_50s_Rework.txt` still throws errors. `JAP_national_focus.md`
also sits among the `.txt` trees and holds the last dead reference to a numbered generic name.

### 3. The other duplicate registries

The generic library is clean but 2226 excess declarations remain elsewhere:
`CWIC_ideas.gfx` vs `ideas_vanilla.gfx` (709), `IC_goals_shine.gfx` vs `goals_shine.gfx` (184),
`decisions.gfx` vs `decisions_vanilla.gfx` (82), and 251 self-duplicates inside `ADR_techs.gfx`.

### 4. Known-broken, deliberately left alone

- **`GFX_Paper` / `GFX_Paper_Two` / `GFX_GFX_Paper`**: used as icons by 19 focuses across
  `USA 1980s/` (11 files), `EGY_50s`, `50s_ZIM`, `50s_IRQ`, `YEM_50s`, `AUS_50s`, `YUG_1950s`. No base
  sprite is declared for any of them and no matching art exists on disk. Rendering blank.
- **179 distinct focus icons mod-wide resolve to nothing.** The bulk is `TIB_KMT_50s.txt` and
  `stalintreereworknew.txt`, where the values are missing the `GFX_` prefix entirely
  (`icon = TIB_KMT_50s_Census`). Mechanical to fix.
- **14 files named `.png` that are not PNG**: 13 JPEGs and one DDS
  (`ideas/usa/companies/USA_Colt.png`), under `ideas/vin/`, `ideas/huk/`,
  `ideas/dynamic_modifiers/USA/`. HOI4 dispatches on extension, so these fail to load.
- **100 PNGs at 4-bit indexed colour**, all GUI under `Scripted_GUI_Special/` (GDR, INO party boxes,
  MAL, checkboxes). Not reported as broken; flagged only.
- **`GFX_Soviet_Loans`** was reported as broken but I could not reproduce any defect: single
  declaration, DXT5 98x82, file size exactly what the header requires, decodes to correct art. An
  early theory that non-multiple-of-4 dimensions break block-compressed DDS was **wrong** - 7274
  files in the mod share that property and work, since DDS stores padded blocks by design. Re-check
  in game after the 16-bit fix.
- **3412 dds remain under `goals/`** overall. Only the 74 in `Generic_National_Focus/` were converted.

## Verification

```bash
python3 tools/icon_audit.py --check       # every audited focus icon resolves - 0 MISSING / 0 ILLEGAL
python3 tools/icon_audit.py --summary     # counts must match "Current audit state" above
python3 tools/icon_rename.py --check      # no numbered generic name survives anywhere
python3 tools/png_depth_fix.py --dry-run  # expect: 0 PNGs deeper than 8 bits
git diff -U0 -- "Cold War Iron Curtain/common/national_focus" \
  | grep -E "^[+-]" | grep -v "^[+-][+-]" | grep -vc "icon *="   # expect 0: icon lines only
```

Also confirm no BOM or CRLF was introduced into any `.gfx` or focus file, and that every
`texturefile` and `animationmaskfile` resolves case-sensitively - all 2830 `generic/` paths do.

In game (the only check that catches a bad texture the parser accepts): open the VIE, LAO, CAM and
MLA trees plus a USA 1980s FP tree, then grep a fresh `error.log` for `nationalfocus.cpp:637`,
`nationalfocus.cpp:642`, `texturehandler.cpp:160` and `spritetype.cpp:330` naming anything under
`generic/`. The baseline is `error_1.log` from 2026-09-02, which has **zero** such entries and shows
no regression from any of this work - the 208 missing-icon errors it does carry are JAP, 60s_ITA,
PRC_50s_Interim and friends, none of them Indochina and none of them generic.
