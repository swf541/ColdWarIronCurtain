# VIE Events - Event Picture Report

Generated from `events/VIE_Events.txt` cross-referenced against `interface/*.gfx` and the files on disk.
364 events total. Sorted by how badly each case needs art.

Last verified 2026-08-28, after the second art import (see *Delivered* at the bottom).

---

## 1. Broken now - sprite referenced but never defined (4)

These events have a `picture = GFX_X` line pointing at a sprite name that no `.gfx` file defines.
The game logs an error and falls back to a default frame. Fixing these needs both an image *and* a
`spriteType` entry.

| Event | Missing sprite |
|---|---|
| `VNA.4` | `GFX_VNA.4` |
| `VNA.5` | `GFX_VNA.5` |
| `VNA.7` | `GFX_VNA.7` |
| `VNG.0` | `GFX_VNG.0` |

`VNA.3`, `VNA.6`, and `USA_VIE_CuongDe_Installation.1` came off this list in the 2026-08-28 import.
`VNA.4`/`.5`/`.7` are the same Bao Dai / Vietnamese National Army sub-chain as the two that were
just done - one archival source set covers all of them. `VNG.0` is a `NO_DATELINE` news event
(185x460) and is also flagged `UNFIRED` in the audit, so confirm it still wants art before drawing.

## 2. Broken now - sprite defined but the texture file is absent (2)

The `.gfx` entry exists and points at a path with nothing at it. Dropping the image in at the named
path is the whole fix - no script change needed.

| Event | Sprite | Expected file |
|---|---|---|
| `VIE_Historical.4` | `GFX_VIE_Historical.4` | `gfx/event_pictures/VIE/VIE_Historical_4.png` |
| `VIE_PQC_Mil.2` | `GFX_VIE_PQC_Mil.2` | `gfx/event_pictures/VIE/VIE_PQC_Mil.2.png` |

`VIE_Historical.6` used to sit in this list. It was never missing art - `GFX_VIE_Historical.6` was
defined twice, once at the top of `eventpictures.gfx` pointing at an underscore path that does not
exist and once further down pointing at `VIE_Historical.6.png`, which does. The stale duplicate has
been removed. `GFX_VIE_Historical.5` still points at a nonexistent `VIE_Historical_5.png`, but no
event references it, so it is dead weight rather than a visible bug.

## 3. Art was planned then disabled - commented-out `picture` line (32)

Someone wrote the `picture =` line and commented it out, which almost always means the art was
specced but never delivered. Note that 11 of these comment a bare id rather than a `GFX_` name, so
the sprite would need naming as well as drawing.

| Event | Commented value |
|---|---|
| `Initial_CuongDe.10` | `GFX_Initial_CuongDe.10` |
| `VIE_Vinh.0` | `GFX_Vinh.0` |
| `BaoDai_Personality_Cult.1` | `GFX_BaoDai_Personality_Cult.1` |
| `FireWater_Kings.1` | `GFX_FireWater_Kings.1` |
| `Montagnard_Administrative.1` | `Montagnard_Administrative.1` |
| `Du_So_21.1` | `Du_So_21.1` |
| `Du_So_21.2` | `Du_So_21.2` |
| `Autonomous_FUL_Republic.1` | `GFX_Autonomous_FUL_Republic.1` |
| `Autonomous_FUL_Republic.2` | `GFX_Autonomous_FUL_Republic.2` |
| `FUL_DanVuong_Model.1` | `FUL_DanVuong_Model.1` |
| `FUL_DanVuong_Model.2` | `FUL_DanVuong_Model.2` |
| `CuongDe_Annexation.1` | `CuongDe_Annexation.1` |
| `CuongDe_Annexation.2` | `CuongDe_Annexation.2` |
| `FUL_Econ_Committee.1` | `FUL_Econ_Committee.1` |
| `Colonel_Massau.1` | `Colonel_Massau.1` |
| `French_Econ_Aid.1` | `French_Econ_Aid.1` |
| `French_Econ_Aid.2` | `French_Econ_Aid.2` |
| `French_Econ_Aid.3` | `French_Econ_Aid.3` |
| `Central_Highland_Railway.2` | `Central_Highland_Railway.2` |
| `Central_Highland_Railway.3` | `Central_Highland_Railway.3` |
| `Central_Highland_Railway.4` | `Central_Highland_Railway.4` |
| `Central_Highland_Railway.5` | `Central_Highland_Railway.5` |
| `FUL_Armed_Forces.1` | `FUL_Armed_Forces.1` |
| `FUL_Armed_Forces.3` | `FUL_Armed_Forces.3` |
| `FUL_Armed_Forces.4` | `FUL_Armed_Forces.4` |
| `Militarize_Viet_Border.1` | `Militarize_Viet_Border.1` |
| `DaLat_Question.1` | `DaLat_Question.1` |
| `DaLat_Question.3` | `DaLat_Question.3` |
| `DaLat_Question.5` | `DaLat_Question.5` |
| `DaLat_Question.6` | `DaLat_Question.6` |
| `DaLat_Question.7` | `DaLat_Question.7` |
| `Autonomous_FUL_Republic.0` | `GFX_Autonomous_FUL_Republic.0` |

## 4. Borrowing another event's art (28)

The 2026-08-28 import cleared five borrowers that the table below never enumerated individually:
`Diem.1` (was `GFX_BaoDai.13`), `Diem.6` (`GFX_BaoDai.9`), `Diem.61` (`GFX_BaoDai.11`),
`Can_Lao.1` (`GFX_BaoDai.100`), and `VIE_PMs.9` (`GFX_VIE_PMs.5`) - the placeholder set tracked
in `LogDocs/VIE_DIEM_ART_REQUESTS.md`. The eight in the table below are untouched.

These render fine but reuse a picture that belongs to a different event. Some are deliberate and
fine (a chain sharing one frame); some are clearly stand-ins.

**Deliberate-looking, low priority:** the `Brevert_Lines` chain all share `GFX_Brevert_Lines.3`,
and `Elysee_Accord.1/.2` point at `GFX_Elysee_Accords.*` - a plural-vs-singular naming mismatch,
not a missing asset.

**Placeholders worth replacing:**

| Event | Currently uses | Note |
|---|---|---|
| `CCC_Pol.1` | `GFX_BaoDai.1` | unrelated Bao-Dai portrait |
| `HoangLienRevolt.1` | `GFX_BaoDai.10` | unrelated Bao-Dai portrait |
| `HoangLienRevolt.2` | `GFX_BaoDai.10` | unrelated Bao-Dai portrait |
| `Initial_CuongDe.7` | `GFX_Etat_du_Vietnam.1` | Cochinchina annexation using the Etat founding frame |
| `CuongDe.11` | `GFX_Initial_CuongDe.3` | French-side telegram using an Initial_CuongDe frame |
| `VIE_Saigon_Captured.1` | `GFX_KMT_Generic_Soldiers` | generic KMT soldiers art |
| `VNA.1` | `GFX_VNA.0` |  |
| `USA_VIE_CuongDe_Installation.2` | `GFX_Cuong_De` | generic Cuong-De portrait |

The whole 8-event `USA_VIN_Reunification.1-8` chain shares `GFX_USA_VIE.3`, and the 9-event
`CCC_Unification.2-10` chain is offset by one against its own sprite numbering
(`.2` uses `.1`, `.3` uses `.1`, `.4` uses `.2` ...). Both read as unfinished rather than intentional.

## 5. No `picture` line at all (82)

These fall back to the default event frame. Grouped by chain so art can be commissioned per chain
rather than per event.

| Chain | Events | Count |
|---|---|---|
| `VIE_Vinh` | `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15` | 14 |
| `VIE_Huu` | `1`, `2`, `5`, `6`, `8`, `9`, `10`, `12`, `13`, `14` | 10 |
| `USA_VIE` | `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `13` | 9 |
| `CD_Nhiep` | `2`, `3`, `5`, `6`, `7`, `8`, `10` | 7 |
| `NV_CuongDe_Unification` | `1`, `3`, `6`, `7`, `9` | 5 |
| `VIE_KOR` | `2`, `3`, `4`, `5` | 4 |
| `VIE_JAP` | `1`, `2`, `4`, `5` | 4 |
| `Crown_Domains` | `1`, `4`, `5`, `6` | 4 |
| `VIE_PQC_Mil` | `1`, `3`, `4`, `5` | 4 |
| `NV_CuongDe` | `1`, `2`, `3` | 3 |
| `VIE_PQC` | `1`, `2`, `3` | 3 |
| `CuongDe_Successor` | `0`, `100`, `200` | 3 |
| `Initial_CuongDe` | `2`, `3` | 2 |
| `VIE_USA_Support` | `1`, `2` | 2 |
| `VIE_Econ_SelfDem` | `1`, `2` | 2 |
| `VIE_Tam` | `3` | 1 |
| `VIE_Chinese_Cooperation` | `2` | 1 |
| `VIE_Malaysia` | `1` | 1 |
| `Brevert_Lines` | `1` | 1 |
| `VIE_Sect_Militias` | `1` | 1 |
| `VIE_China_Civil_War` | `1` | 1 |

The three biggest gaps are the `VIE_Vinh` premiership chain (14), the `VIE_Huu` premiership chain (10),
and the `USA_VIE` American-engagement chain (9). Those are the highest-traffic uncovered chains.

---

## Summary

- Events with no working picture: **120** of 364
  - 4 reference an undefined sprite (error in log)
  - 2 reference a missing file (error in log)
  - 32 have the line commented out
  - 82 have no line at all
- Events reusing another event's art: **28**

---

## Delivered - 2026-08-28 import (9, commit `d27729a`)

First batch through the `eventpic` generator (`CWIC Backup/tools/EventPicGenerator`), manifest
`batches/indochina_2026-08.yml`, sources from `~/Pictures/Event Pictures/`. Nine PNGs plus nine
`spriteType` entries appended to the VIE block of `interface/eventpictures.gfx`; each event's
`picture =` line was repointed off its placeholder.

| Event | New sprite | File | Was |
|---|---|---|---|
| `VNA.3` | `GFX_VNA.3` | `VIE/VNA.3.png` | undefined sprite (section 1) |
| `VNA.6` | `GFX_VNA.6` | `VIE/VNA.6.png` | undefined sprite (section 1) |
| `USA_VIE_CuongDe_Installation.1` | `GFX_USA_VIE_CuongDe_Installation.1` | `VIE/USA_VIE_CuongDe_Installation.1.png` | undefined sprite (section 1) |
| `Diem.1` | `GFX_Diem.1` | `VIE/Diem.1.png` | borrowed `GFX_BaoDai.13` |
| `Diem.6` | `GFX_Diem.6` | `VIE/Diem.6.png` | borrowed `GFX_BaoDai.9` |
| `Diem.61` | `GFX_Diem.61` | `VIE/Diem.61.png` | borrowed `GFX_BaoDai.11` |
| `Can_Lao.1` | `GFX_Can_Lao.1` | `VIE/Can_Lao.1.png` | borrowed `GFX_BaoDai.100` |
| `VIE_PMs.9` | `GFX_VIE_PMs.9` | `VIE/VIE_PMs.9.png` | borrowed `GFX_VIE_PMs.5` |
| `FRE_Dien_Bien.1` | `GFX_FRE_Dien_Bien.1` | `FRE/FRE_Dien_Bien.1.png` | vanilla `GFX_report_event_generic_soldiers` (not a VIE event) |

`Can_Lao.1` is the only news picture in the batch (185x460); the rest are 210x176 country frames.

---

## Delivered - 2026-08-05 import (13)

Thirteen images landed in `gfx/event_pictures/VIE/` with matching `spriteType` entries appended to
the VIE block of `interface/eventpictures.gfx`. All thirteen came off section 1, taking it from 21
(really 20 - the old header miscounted its own table) down to 7.

| Event | Sprite | File |
|---|---|---|
| `NUN_Unification.3` | `GFX_NUN_Unification.3` | `NUN_Unification.3.png` |
| `French_Hinh.0` | `GFX_French_Hinh.0` | `French_Hinh.0.png` |
| `French_Hinh.1` | `GFX_French_Hinh.1` | `French_Hinh.1.png` |
| `French_Hinh.2` | `GFX_French_Hinh.2` | `French_Hinh.2.png` |
| `French_Hinh.3` | `GFX_French_Hinh.3` | `French_Hinh.3.png` |
| `French_Hinh.100` | `GFX_French_Hinh.100` | `French_Hinh.100.png` |
| `NgoDinh_Brothers.4` | `GFX_NgoDinh_Brothers.4` | `NgoDinh_Brothers.4.png` |
| `VIE_Toan.1` | `GFX_VIE_Toan.1` | `VIE_Toan.1.png` |
| `VIE_Toan.2` | `GFX_VIE_Toan.2` | `VIE_Toan.2.png` |
| `VIE_Toan.3` | `GFX_VIE_Toan.3` | `VIE_Toan.3.png` |
| `VIE_Toan.4` | `GFX_VIE_Toan.4` | `VIE_Toan.4.png` |
| `VIE_Historical.7` | `GFX_VIE_Historical.7` | `VIE_Historical.7.png` |
| `VIE_Historical.8` | `GFX_VIE_Historical.8` | `VIE_Historical.8.png` |

### Notes for the next batch

- **Sizes.** Country events want **210x176**; news events (the `.0` / `.100` ids) want **185x460**.
  Everything in this batch matched except `NUN_Unification.3.png` at **290x182**, which will overflow
  the country-event frame and wants a re-crop.
- **Colour model.** Five of the thirteen arrived as 8-bit grayscale PNGs. Every other picture in the
  folder is RGB/RGBA, so they were converted to RGBA on import - pixel-identical, just a safer
  encoding for the texture loader. Exporting as RGBA up front skips that step.
- **Naming.** Sprite name is `GFX_<event id>` and the file is `<event id>.png`, dots kept as-is.
  The older underscore variants (`VIE_Historical_1.png`) are legacy - do not start new ones that way.
