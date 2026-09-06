# Reworked MLA — parked content

Archive of Malaya (MLA) content removed during the insurgency-economy rework.
Kept here for safekeeping in case we want to reimplement it later.

**This folder is intentionally outside `Cold War Iron Curtain/` so the game never
loads it.** Do not move it into the mod folder as-is: the focus snapshots below
duplicate focus IDs that still exist in the live tree and would cause
duplicate-focus errors.

Files are snapshots taken from `HEAD` at the time of the rework commit, mirroring
their original relative paths under the mod folder:

- `common/decisions/MLA.txt` — fully removed (MLA decisions)
- `common/decisions/categories/MLA_decision_categories.txt` — fully removed
- `common/scripted_localisation/MLA_scripted_localisation.txt` — fully removed
- `interface/MLA_GUI.gfx`, `interface/MLA_GUI.gui` — fully removed (MLA GUI)
- `common/scripted_guis/MLA_gui.txt` — pre-rework full version (had content stripped)
- `common/national_focus/MLA_Initial_Emergency.txt` — pre-rework full version (focuses stripped)
- `common/national_focus/MLA_50s.txt` — pre-rework full version (focuses stripped)

For the three "pre-rework full version" files, only some content was removed in the
live tree; the whole pre-rework file is preserved here so nothing is lost. Diff
against the live version to see exactly what was cut.
