# Artillery and AA target manifest

Frozen 2026-09-06 from the 2023 workbook's `Work Sheet` scratch tab.
This is the source contract for deferred implementation, not a claim that game
equipment or designer recipes already match these targets. No gameplay changes
are made by this freeze. Live branch QA remains required before new content.

Workbook SHA-256: `dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532`

Worksheet: `Work Sheet` (`xl/worksheets/sheet14.xml`). Every table preserves cell-range provenance.
Values are literal workbook numbers. Missing values are `missing`, never zero.

## Year policy

Canonical years from `Years`: 1939, 1942, 1944, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020.

The implementation grid is shared, but each family retains its own cadence.
Use a band's lower year as its anchor, then choose the nearest canonical year
(earlier wins ties). Thus SPAAG 1935-1940 maps to 1939, SP 1945 maps to 1944,
and AT 1940 maps to 1939. All other single years remain unchanged; later SPAAG
bands map to 1950, 1965, 1980 and 1995. This mapping is an implementation
decision made in this freeze, not a date specified by the source. Source years
remain visible so later historical research can revise the mapping explicitly.

Do not interpolate extra tiers or invent a sixth SP/AT tier to fit the diagram.
The diagram's six-step towed artillery/AA technology layout is not a six-row
equipment balance table. These targets alone do not specify that whole tree.

## Vehicle targets

SP fields map to `soft_attack`, `hard_attack`, `ap_attack`, `breakthrough`,
and `defense`; AA maps to `air_attack`. SP Heavy's low piercing is intentional.
Unlisted stats (including cost, armor and reliability) are unspecified, not zero.

### SPAAG

| Source cells | Source year/band | Grid year | Air attack |
| --- | --- | --- | --- |
| `B4:C4` | 1935-1940 | 1939 | 12 |
| `B5:C5` | 1950-1955 | 1950 | 14 |
| `B6:C6` | 1965-1970 | 1965 | 16 |
| `B7:C7` | 1980-1985 | 1980 | 20 |
| `B8:C8` | 1995-2000 | 1995 | 24 |

### SAM

| Source cells | Source year/band | Grid year | Air attack |
| --- | --- | --- | --- |
| `B13:C13` | 1955 | 1955 | 35 |
| `B14:C14` | 1965 | 1965 | 45 |
| `B15:C15` | 1975 | 1975 | 60 |
| `B16:C16` | 1985 | 1985 | 75 |
| `B17:C17` | 1995 | 1995 | 90 |
| `B18:C18` | 2005 | 2005 | 105 |

### SP Light

| Source cells | Source year/band | Grid year | Soft | Hard | Piercing | Breakthrough | Defense |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `F4:K4` | 1945 | 1944 | 24 | 6 | 12 | 7 | 10 |
| `F5:K5` | 1960 | 1960 | 27 | 8 | 14 | 8 | 12 |
| `F6:K6` | 1975 | 1975 | 33 | 10 | 16 | 10 | 14 |
| `F7:K7` | 1990 | 1990 | 39 | 12 | 18 | 11 | 16 |
| `F8:K8` | 2005 | 2005 | 45 | 14 | 20 | 13 | 18 |

### SP Medium

| Source cells | Source year/band | Grid year | Soft | Hard | Piercing | Breakthrough | Defense |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N4:S4` | 1945 | 1944 | 32 | 6 | 12 | 8 | 7.5 |
| `N5:S5` | 1960 | 1960 | 36 | 8 | 14 | 10 | 9 |
| `N6:S6` | 1975 | 1975 | 44 | 10 | 16 | 11 | 10.5 |
| `N7:S7` | 1990 | 1990 | 52 | 12 | 18 | 13 | 12 |
| `N8:S8` | 2005 | 2005 | 60 | 14 | 20 | 14 | 13.5 |

### SP Heavy

| Source cells | Source year/band | Grid year | Soft | Hard | Piercing | Breakthrough | Defense |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `V4:AA4` | 1945 | 1944 | 40 | 9 | 6 | 9 | 5 |
| `V5:AA5` | 1960 | 1960 | 45 | 12 | 7 | 11 | 6 |
| `V6:AA6` | 1975 | 1975 | 55 | 15 | 8 | 13 | 7 |
| `V7:AA7` | 1990 | 1990 | 65 | 18 | 9 | 14 | 8 |
| `V8:AA8` | 2005 | 2005 | 75 | 21 | 10 | 16 | 9 |

### AT

| Source cells | Source year/band | Grid year | Soft | Hard | Piercing | Breakthrough | Defense |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AD4:AI4` | 1940 | 1939 | 12 | 15 | 30 | 13 | 10 |
| `AD5:AI5` | 1955 | 1955 | 14 | 20 | 35 | 15 | 12 |
| `AD6:AI6` | 1970 | 1970 | 17 | 25 | 40 | 18 | 14 |
| `AD7:AI7` | 1985 | 1985 | 30 | 30 | 45 | 20 | 16 |
| `AD8:AI8` | 2000 | 2000 | 46 | 35 | 50 | 23 | 18 |

## Reserved module cost bands

These are budget references, not implemented module stats or interpolated costs.
Iteration counts do not establish technology dates or unlock requirements.

| Source cells | Category | Minimum | 1950 | Maximum | Iterations |
| --- | --- | --- | --- | --- | --- |
| `AP58:AT58` | Mech ammo arty | 2.5 | 3.5 | 4.5 | 3 |
| `AP61:AT61` | Aiming AA | 0.5 | 3 | 6.6 | 5 |
| `AP64:AT64` | Optics AA | 0.5 | missing | 9 | 6 |
| `AP65:AT65` | Optics Arty | 0.5 | missing | 8 | 2 |
| `AP69:AT69` | Computer Arty | 5.25 | missing | 7.5 | 4 |
| `AP70:AT70` | Radar | 4 | missing | 8.5 | 7 |

## Implementation boundaries

31 vehicle target rows, 111 combat-stat cells and six module budget rows are frozen.
IFV rows F13:I17 are excluded: the existing mechanized manifest owns them.
No source targets here define towed artillery, rocket artillery, amphibious
equipment, night vision, or a complete designer loadout. Those need separate contracts.

Before implementing: finish fresh 1949/1980 NSB and non-NSB runtime QA; settle
legacy versus DLC-gated technology delivery; retain sub-unit activation; and
calibrate designer stat evaluation against live designs. None is waived here.

Reproduce with `python3 tools/artillery_aa_targets.py`; verify with
`python3 tools/artillery_aa_targets.py --check`. The command never edits files.
