# Doctrine Rework Investigation and Handoff

Date: 2026-09-04

Branch/commit inspected: `development-branch` / `4a999ae3f3`

Game reference: local Hearts of Iron IV 1.19.2 installation with all DLC enabled

Scope: `Cold War Iron Curtain/common/doctrines/`, `Cold War Iron Curtain/common/technologies/doctrine rework/`, relevant technology folders/categories, Git history, and current runtime doctrine errors.

Related document: `LogDocs/Tank_Designer_Rework_Audit.md`

## Executive diagnosis

Doctrines do not exist in the current game because both implementations were deliberately disabled pending completion.

Both systems are therefore inactive:

1. The files in `common/doctrines/` override the current vanilla doctrine definitions with empty files. This removes the grand doctrines, tracks, and subdoctrines used by the current DLC doctrine interface.
2. The custom old-style doctrine trees contain approximately 19,850 lines under `common/technologies/doctrine rework/`. They were deliberately moved to a directory that Hearts of Iron IV does not recursively load.

The repository preserves substantial custom doctrine content in the old technology format, but this does **not** establish that restoring the old system is the desired final architecture. The current history supports only two firm conclusions: the legacy rework was intentionally parked, and the imported DLC-era implementation was also intentionally removed. Architecture must be selected before either one is re-enabled.

## Current file state

### New doctrine system

All gameplay-content files under these locations are empty:

- `common/doctrines/grand_doctrines/`
- `common/doctrines/tracks/`
- `common/doctrines/subdoctrines/air/`
- `common/doctrines/subdoctrines/land/`
- `common/doctrines/subdoctrines/sea/`
- `common/doctrines/subdoctrines/special_forces/`

The only active gameplay definition in the directory is `common/doctrines/folders/doctrine_folders.txt`. It defines the land, naval, and air folders but omits the vanilla special-forces folder.

These files share the same relative paths as vanilla files. Their zero-byte contents consequently replace the vanilla definitions rather than allowing vanilla to act as a fallback.

### Technology-tree doctrine rework

The parked replacement files are:

| File | Approximate size |
| --- | ---: |
| `common/technologies/doctrine rework/land_doctrine.txt` | 15,048 lines |
| `common/technologies/doctrine rework/air_doctrine.txt` | 2,826 lines |
| `common/technologies/doctrine rework/naval_doctrine.txt` | 1,976 lines |
| `common/technologies/doctrine rework/special_forces_doctrine.txt` | 0 lines |

The populated files use the legacy doctrine technology model, including `doctrine = yes`, XP research types and unlock costs, and folder assignments such as:

```text
folder = {
    name = old_land_doctrine_folder
    position = { x = 0 y = 0 }
}
```

The corresponding folders remain defined in `common/technology_tags/00_technology.txt`:

- `old_land_doctrine_folder`
- `old_naval_doctrine_folder`
- `old_air_doctrine_folder`
- `special_forces_doctrine_folder` (currently assigned to the hidden ledger)

The definitions are inactive because of their placement inside `common/technologies/doctrine rework/`. This placement is an intentional parking mechanism, not an accidental loader mistake.

## Git history and likely intent

Commit `77ed29d189` (`a lot of fixes`, 2025-11-26) imported the DLC-era doctrine framework: grand doctrines, tracks, subdoctrines, folders, and documentation. The imported IDs and structure are vanilla-style (`new_mobile_warfare`, `armored_spearhead`, mastery tracks, and similar content). At least one imported file, `air_grand_doctrines.txt`, is still byte-identical to the current local vanilla 1.19.2 file; other files differ primarily because vanilla continued to receive updates. No subsequent commit develops CWIC-specific gameplay definitions in this framework.

Commit `0e87e343b2` (`removed new doctrine stuffs`, 2025-11-29) deleted 6,321 lines from the imported subdoctrine and track files while retaining empty overrides. Commit `d6f60c40cb` (`More error fixes and update raid documentation`, also 2025-11-29) then deleted the remaining 1,149 lines of imported land, air, and naval grand doctrines. This was a deliberate rollback of the new system three days after its import.

Commit `209b2a17cc` (`@Yuri1918 make the ui for doctrines and offier corps gui`, 2025-12-06) added the new doctrine UI/GFX files after the gameplay definitions had been removed. Those files remain in the repository and are close to their current vanilla equivalents. Their presence shows that UI compatibility work was retained, but it does not by itself demonstrate a completed CWIC doctrine design.

Meanwhile, the old technology-tree doctrines continued active development. Commit `b3d3a53c48` (`I love doctrines`, 2025-12-07) modified all three old trees. Commit `cce535ae9c` (`work i havent pushed`, 2025-12-23) substantially rewrote the land tree, followed by fixes through February 2026. Approximately 160 custom doctrine images also remain, including NATO, Warsaw Pact, Maoist, insurgent, Iranian, Himalayan, and other Cold War doctrine assets tied to technology IDs such as `cw_nato_1940s_*`.

Commit `18a4f76c19` (`bunch of fixes`, 2026-07-03) moved `common/technologies/land_doctrine.txt` to `common/technologies/doctrine rework/land_doctrine.txt` and added the air, naval, and empty special-forces files in that subdirectory.

That move intentionally disabled the legacy implementation. It was followed 72 minutes later in direct ancestry by commit `790a693684`, explicitly titled `doctrines removed until completion`, which removed the remaining old-doctrine AI strategy file. The July sequence is decisive evidence that the nested directory is a parking location.

The history therefore contains two different unfinished tracks:

- a short-lived import and UI integration of the new DLC doctrine framework, with no surviving CWIC-specific grand-doctrine/subdoctrine implementation;
- a large, genuinely custom Cold War doctrine rework built in the legacy technology format, developed for years and explicitly parked in July 2026 until completion.

Repository evidence does not record the team's final architectural decision. The phrase `doctrine rework` currently names the parked legacy files, but that does not prevent their concepts, effects, localization, art, and country distinctions from serving as source material for a new-system rewrite. Restoring those files unchanged should not be assumed to be the final goal.

## Runtime evidence and secondary inconsistencies

The current logs contain no references to `common/technologies/doctrine rework/`, consistent with those files never being parsed.

The logs do contain this doctrine-related error:

```text
Invalid trigger 'can_unlock_second_track_of_sf_doctrine' in
common/doctrines/tracks/special_forces_tracks.txt line 23
```

This happens because the mod does not provide an empty override for vanilla's `special_forces_tracks.txt`, so the vanilla track still loads. At the same time, the mod overrides vanilla's `common/scripted_triggers/00_scripted_triggers.txt` without retaining `can_unlock_second_track_of_sf_doctrine`. The surviving vanilla track therefore calls a trigger that no longer exists.

Another current error is:

```text
common/national_focus/50s_PAR.txt:913: add_tech_bonus:
Unknown technology category air_doctrine
```

The technology category file defines `cat_air_doctrine`, not `air_doctrine`. This focus reward must be reconciled with the final category scheme.

The special-forces replacement is also unfinished:

- `common/technologies/doctrine rework/special_forces_doctrine.txt` is empty;
- `special_forces_doctrine_folder` uses `ledger = hidden`;
- the new-system special-forces grand doctrine and subdoctrine overrides are empty;
- the vanilla special-forces track is still partially loading and producing an error.

## Architecture decision required before implementation

Do not begin by moving the parked technology files back into `common/technologies/`. That would reactivate the deliberately retired system before confirming whether it remains the target.

The preferred direction for an all-DLC modernization should be evaluated as:

1. Use the current DLC grand-doctrine, track, subdoctrine, mastery, milestone, and reward framework as the runtime architecture.
2. Treat the parked old land, air, and naval trees as design source material rather than files to reactivate wholesale.
3. Map their Cold War schools, era progression, effects, country-specific distinctions, localization, and 160 existing art assets into the new framework.
4. Update the November 2025 imported definitions against the current game version before customization; they are an old vanilla snapshot, not a safe implementation base as-is.
5. Reconcile all history grants, focuses, events, AI, scripted checks, categories, XP costs, and UI expectations with the selected framework.
6. Decide special-forces scope explicitly because neither parked implementation contains completed custom special-forces doctrine content.

If maintainers instead explicitly choose the legacy architecture, moving the files to the top level is the smallest way to begin testing it—but that should be a conscious architecture choice, not described as repairing an accidental regression.

## Test-branch audit checklist

After selecting and minimally enabling the chosen architecture on the test branch, audit the following before polishing:

- parser errors, duplicate technology IDs, invalid modifiers, and obsolete effects;
- every `path`, `leads_to_tech`, and mutual-exclusion relationship;
- root technology availability and whether a country can begin each tree;
- folder/track layout, overlap, clipping, and branch readability;
- XP costs, mastery gain, milestones, rewards, and doctrine switching behavior under the selected framework;
- land, air, and naval technology categories and all focus research bonuses;
- country-history grants and references to removed vanilla doctrine IDs;
- scripted triggers, scripted effects, decisions, events, AI strategies, and focuses that check doctrine ownership;
- AI research weights and whether AI countries acquire coherent doctrine branches;
- doctrine localization, icons, tooltips, and missing GFX;
- save/load behavior and multiplayer synchronization;
- DLC-on and DLC-off behavior, even if all-DLC is the primary supported configuration;
- special-forces doctrine scope and whether it belongs in this rework at all.

Acceptance criteria for the first functional milestone:

1. Land, naval, and air doctrine tabs are visible and populated with all DLC enabled.
2. A player can unlock at least one complete branch in each tree using the intended XP/mastery flow.
3. The AI can select and advance through valid branches.
4. No doctrine parser, unknown-technology, unknown-category, or invalid-trigger errors remain in `error.log`.
5. Exactly one doctrine architecture is active; no legacy/new-system duplication or unintended vanilla fallback remains.

## Coordination with the tank-designer rework

Doctrine and tank-designer work should share a dedicated test branch because both are unfinished systems that affect military research, AI behavior, starting content, technology categories, UI integration, and all-DLC compatibility.

The tank-designer audit remains the authoritative backlog for chassis, modules, variants, OOBs, and designer UI. This document is the doctrine-side handoff. Changes should be kept in logically separated commits so doctrine loader restoration, doctrine content fixes, tank-designer fixes, and shared AI/category work can be reviewed or reverted independently.

Suggested first-session order:

1. Create the test branch from the currently agreed base commit.
2. Record the architecture decision: finish the DLC-era framework or deliberately retain the legacy technology model.
3. Build the smallest proof of concept in the selected system—preferably one land grand doctrine, one track, and one custom subdoctrine if choosing the DLC-era framework.
4. Capture a fresh all-DLC startup log and doctrine UI screenshots.
5. Fix doctrine parse/reference failures until the proof of concept is testable.
6. Begin tank-designer P0 work from `LogDocs/Tank_Designer_Rework_Audit.md`.
7. Revisit shared technology categories and AI behavior after both systems load reliably.

## Files expected to be involved later

- `common/doctrines/**`
- `common/technologies/doctrine rework/**`
- `common/technology_tags/00_technology.txt`
- `common/scripted_triggers/00_scripted_triggers.txt`
- `common/national_focus/50s_PAR.txt`
- doctrine localization and interface/GFX files discovered during the full audit
- country history, focuses, events, decisions, and AI scripts that reference doctrine technologies or categories

No gameplay files were changed as part of this investigation document.
