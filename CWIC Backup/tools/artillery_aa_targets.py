#!/usr/bin/env python3
"""Render or verify the frozen artillery/AA source manifest (standard library only)."""

import argparse
import hashlib
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "LogDocs/Tank_Designer"
WORKBOOK = DIRECTORY / "2023 - CWIC Tank Rework Balance.xlsx"
MANIFEST = DIRECTORY / "Artillery_AA_Target_Manifest.md"
SHA = "dc2c9800b69b0f2f00568cdfe0f4bcac55c8bdd61476409b4a88b6d8e566b532"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def worksheet(archive, name):
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {item.attrib["Id"]: item.attrib["Target"] for item in relationships}
    sheets = ET.fromstring(archive.read("xl/workbook.xml"))
    sheet = next(s for s in sheets.iter(NS + "sheet") if s.attrib["name"] == name)
    target = targets[sheet.attrib[REL + "id"]]
    path = target.lstrip("/") if target.startswith("/") else "xl/" + target
    strings = ["".join(t.text or "" for t in s.iter(NS + "t"))
               for s in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
    cells = {}
    for cell in ET.fromstring(archive.read(path)).iter(NS + "c"):
        value = cell.find(NS + "v")
        if cell.find(NS + "f") is not None:
            continue  # Scratch formulas are not accepted as frozen source values.
        if value is not None:
            cells[cell.attrib["r"]] = (strings[int(value.text)]
                if cell.get("t") == "s" else value.text)
        elif cell.get("t") == "inlineStr":
            cells[cell.attrib["r"]] = "".join(t.text or "" for t in cell.iter(NS + "t"))
    return path, cells


def render():
    if hashlib.sha256(WORKBOOK.read_bytes()).hexdigest() != SHA:
        raise ValueError("workbook SHA-256 changed; source review required")
    with ZipFile(WORKBOOK) as archive:
        path, cells = worksheet(archive, "Work Sheet")
        _, year_cells = worksheet(archive, "Years")
    years = sorted({int(v) for v in year_cells.values() if v.isdigit() and 1900 <= int(v) <= 2100})
    if len(years) != 18:
        raise ValueError(f"expected 18 canonical years, found {years}")

    def mapped_year(source):
        # Bands use their lower bound; off-grid dates use the nearest grid year.
        # Earlier wins an equal-distance tie. No interpolation of source stats.
        anchor = int(source.split("-")[0])
        return min(years, key=lambda year: (abs(year - anchor), year))

    lines = [
        "# Artillery and AA target manifest", "",
        "Frozen 2026-09-06 from the 2023 workbook's `Work Sheet` scratch tab.",
        "This is the source contract for deferred implementation, not a claim that game",
        "equipment or designer recipes already match these targets. No gameplay changes",
        "are made by this freeze. Live branch QA remains required before new content.", "",
        f"Workbook SHA-256: `{SHA}`", "",
        f"Worksheet: `Work Sheet` (`{path}`). Every table preserves cell-range provenance.",
        "Values are literal workbook numbers. Missing values are `missing`, never zero.", "",
        "## Year policy", "",
        "Canonical years from `Years`: " + ", ".join(map(str, years)) + ".", "",
        "The implementation grid is shared, but each family retains its own cadence.",
        "Use a band's lower year as its anchor, then choose the nearest canonical year",
        "(earlier wins ties). Thus SPAAG 1935-1940 maps to 1939, SP 1945 maps to 1944,",
        "and AT 1940 maps to 1939. All other single years remain unchanged; later SPAAG",
        "bands map to 1950, 1965, 1980 and 1995. This mapping is an implementation",
        "decision made in this freeze, not a date specified by the source. Source years",
        "remain visible so later historical research can revise the mapping explicitly.", "",
        "Do not interpolate extra tiers or invent a sixth SP/AT tier to fit the diagram.",
        "The diagram's six-step towed artillery/AA technology layout is not a six-row",
        "equipment balance table. These targets alone do not specify that whole tree.", "",
        "## Vehicle targets", "",
        "SP fields map to `soft_attack`, `hard_attack`, `ap_attack`, `breakthrough`,",
        "and `defense`; AA maps to `air_attack`. SP Heavy's low piercing is intentional.",
        "Unlisted stats (including cost, armor and reliability) are unspecified, not zero.", "",
    ]
    families = [
        ("SPAAG", "B", ["C"], ["Air attack"], range(4, 9)),
        ("SAM", "B", ["C"], ["Air attack"], range(13, 19)),
        ("SP Light", "F", list("GHIJK"), ["Soft", "Hard", "Piercing", "Breakthrough", "Defense"], range(4, 9)),
        ("SP Medium", "N", list("OPQRS"), ["Soft", "Hard", "Piercing", "Breakthrough", "Defense"], range(4, 9)),
        ("SP Heavy", "V", ["W", "X", "Y", "Z", "AA"], ["Soft", "Hard", "Piercing", "Breakthrough", "Defense"], range(4, 9)),
        ("AT", "AD", ["AE", "AF", "AG", "AH", "AI"], ["Soft", "Hard", "Piercing", "Breakthrough", "Defense"], range(4, 9)),
    ]
    for name, year_col, columns, headings, rows in families:
        lines += [f"### {name}", "",
                  "| Source cells | Source year/band | Grid year | " + " | ".join(headings) + " |",
                  "| " + " | ".join(["---"] * (3 + len(columns))) + " |"]
        for row in rows:
            source = cells[f"{year_col}{row}"]
            values = [f"`{year_col}{row}:{columns[-1]}{row}`", source, str(mapped_year(source))]
            values += [cells[f"{col}{row}"] for col in columns]
            lines.append("| " + " | ".join(values) + " |")
        lines.append("")
    lines += ["## Reserved module cost bands", "",
              "These are budget references, not implemented module stats or interpolated costs.",
              "Iteration counts do not establish technology dates or unlock requirements.", "",
              "| Source cells | Category | Minimum | 1950 | Maximum | Iterations |",
              "| --- | --- | --- | --- | --- | --- |"]
    for row in [58, 61, 64, 65, 69, 70]:
        values = [f"`AP{row}:AT{row}`"] + [cells[f"{col}{row}"] for col in ["AP", "AQ", "AR", "AS", "AT"]]
        lines.append("| " + " | ".join("missing" if v == "---" else v for v in values) + " |")
    lines += ["", "## Implementation boundaries", "",
              "31 vehicle target rows, 111 combat-stat cells and six module budget rows are frozen.",
              "IFV rows F13:I17 are excluded: the existing mechanized manifest owns them.",
              "No source targets here define towed artillery, rocket artillery, amphibious",
              "equipment, night vision, or a complete designer loadout. Those need separate contracts.", "",
              "Before implementing: finish fresh 1949/1980 NSB and non-NSB runtime QA; settle",
              "legacy versus DLC-gated technology delivery; retain sub-unit activation; and",
              "calibrate designer stat evaluation against live designs. None is waived here.", "",
              "Reproduce with `python3 tools/artillery_aa_targets.py`; verify with",
              "`python3 tools/artillery_aa_targets.py --check`. The command never edits files.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the manifest differs from its source contract")
    args = parser.parse_args()
    try:
        expected = render()
        if args.check:
            if MANIFEST.read_text(encoding="utf-8") != expected:
                raise ValueError("artillery/AA manifest differs from the frozen source contract")
            print("Artillery/AA target validation passed: 31 targets, 111 combat-stat cells, 6 budget rows.")
        else:
            sys.stdout.write(expected)
    except (OSError, ValueError, KeyError, StopIteration) as error:
        parser.exit(1, f"Artillery/AA target validation failed: {error}\n")


if __name__ == "__main__":
    main()
