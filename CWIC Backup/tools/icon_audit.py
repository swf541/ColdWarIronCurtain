#!/usr/bin/env python3
"""CWIC national focus icon auditor for the Southeast Asia content.

Parses the focus tree files listed in THEATRES, resolves every `icon = GFX_...`
against the sprite definitions in `interface/**/*.gfx`, and writes one CSV per
theatre.

The CSVs are round-trippable: generated columns are refreshed on every run while
the hand-written columns (Verdict, Replacement, Notes) are carried over from the
existing file, keyed on (Focus File, Focus ID).

Usage:
    python3 tools/icon_audit.py            # regenerate every theatre CSV
    python3 tools/icon_audit.py --check    # lint, exit 1 on MISSING / ILLEGAL
    python3 tools/icon_audit.py --summary  # print counts, write nothing
"""

import argparse
import csv
import os
import re
import sys
from collections import Counter, OrderedDict

MOD = "Cold War Iron Curtain"
FOCUS_DIR = os.path.join(MOD, "common", "national_focus")
INTERFACE_DIR = os.path.join(MOD, "interface")
OUT_DIR = os.path.join("CWIC Backup", "documentation", "Icon Audit")

THEATRES = OrderedDict([
    ("Icon Audit - South Vietnam.csv", [
        "VIE_50s_Initial.txt", "VIE_50s_Bao_Dai.txt", "VIE_50s_CuongDe.txt",
        "VIE_50s_Diplo.txt", "VIE_50s_Economy.txt", "VIE_50s_Economy_CD.txt",
        "VIE_50s_Military.txt", "VIE_50s_Military_CD.txt",
        "VIE_50s_Northern_Question.txt", "VIE_50s_Northern_Question_CD.txt",
        "VIE_French_Hinh.txt", "60s_VIE.txt",
    ]),
    ("Icon Audit - North Vietnam.csv", ["VIN_50s.txt", "VIN_FORPOL.txt"]),
    ("Icon Audit - French Indochina.csv", ["FRE_50s_Indochina.txt"]),
    ("Icon Audit - Laos.csv", ["50s_LAO.txt", "Shared_LAO.txt"]),
    ("Icon Audit - Cambodia.csv", ["CAM_50s.txt"]),
    ("Icon Audit - Meo Highlands.csv", ["MEO_50s.txt"]),
    ("Icon Audit - Malaya.csv", [
        "MLA_Initial_Emergency.txt", "MLA_50s.txt", "MLA_60s.txt", "MLA_70s.txt",
        "MAL_1950s.txt", "Shared_MLA_MQJ.txt",
    ]),
    ("Icon Audit - Thailand.csv", ["SIA_50s.txt"]),
])

# Which tag each focus file belongs to - a sprite carrying any other tag prefix
# is a borrow from an unrelated nation.
FILE_TAG = {
    "VIE_50s_Initial.txt": "VIE", "VIE_50s_Bao_Dai.txt": "VIE",
    "VIE_50s_CuongDe.txt": "VIE", "VIE_50s_Diplo.txt": "VIE",
    "VIE_50s_Economy.txt": "VIE", "VIE_50s_Economy_CD.txt": "VIE",
    "VIE_50s_Military.txt": "VIE", "VIE_50s_Military_CD.txt": "VIE",
    "VIE_50s_Northern_Question.txt": "VIE",
    "VIE_50s_Northern_Question_CD.txt": "VIE",
    "VIE_French_Hinh.txt": "VIE", "60s_VIE.txt": "VIE",
    "VIN_50s.txt": "VIN", "VIN_FORPOL.txt": "VIN",
    "FRE_50s_Indochina.txt": "FRE",
    "50s_LAO.txt": "LAO", "Shared_LAO.txt": "LAO",
    "CAM_50s.txt": "CAM", "MEO_50s.txt": "MEO",
    "MLA_Initial_Emergency.txt": "MLA", "MLA_50s.txt": "MLA",
    "MLA_60s.txt": "MLA", "MLA_70s.txt": "MLA",
    "MAL_1950s.txt": "MAL", "Shared_MLA_MQJ.txt": "MLA",
    "SIA_50s.txt": "SIA",
}

PLACEHOLDERS = {"GFX_unknown", "GFX_goal_unknown", "GFX_focus_unknown",
                "GFX_generic_focus_military_placeholder",
                "GFX_generic_focus_politics_placeholder"}

# The generic icon library, renamed from numbers to content: every sprite
# under gfx/interface/goals/generic/ carries this prefix.
GENERIC_PREFIX = "GFX_generic_focus_"

# Base-game sprites live outside this repo, so "not defined here" is not a bug
# for anything in the vanilla GFX_goal_* / GFX_focus_* namespace.
VANILLA = re.compile(r"^GFX_(goal|focus)_")




# Tag prefixes seen on borrowed art, matched either directly after GFX_ or
# after the vanilla goal_/focus_ namespace (GFX_focus_RAJ_indian_gurkhas).
TAG_TOKENS = (
    "usa_50", "usa_80", "usa", "SOV", "PRC", "KMT", "KPA", "JAP", "jap", "INO",
    "RAJ", "Gre", "SWK", "CHI", "chi", "ITA", "ger", "SOV_50", "FRA", "SPR",
    "VIE", "VIN", "FRE", "LAO", "CAM", "MEO", "MLA", "MAL", "SIA", "NLF",
    "TAM", "TAI",
)
TAG_PREFIX = re.compile(
    r"^GFX_(?:goal_|focus_)?(" + "|".join(TAG_TOKENS) + r")_")

# Sprite names are bare tokens. The mod does declare hyphenated names
# (GFX_PRC_50s_Prepare_to_Counter-offense_...) and the game resolves them, so a
# hyphen is only a problem when nothing declares that exact name - which the
# MISSING check already catches.
LEGAL_NAME = re.compile(r"^GFX_[A-Za-z0-9_'\-]+$")

FOCUS_BLOCK = re.compile(r"^\s*(shared_focus|focus)\s*=\s*\{", re.M)
ID_LINE = re.compile(r"^\s*id\s*=\s*([A-Za-z0-9_.'\-]+)", re.M)
ICON_LINE = re.compile(r"^\s*icon\s*=\s*([A-Za-z0-9_.'\-]+)", re.M)
SPRITE_NAME = re.compile(r'^\s*name\s*=\s*"(GFX_[^"]*)"', re.M)

GENERATED_COLUMNS = [
    "Focus ID", "Focus File", "Tag", "Line", "Icon", "Icon Source",
    "Sprite Defined", "Dup Count In Tree", "Flags",
]
HAND_COLUMNS = ["Verdict", "Replacement", "Notes"]
COLUMNS = GENERATED_COLUMNS + HAND_COLUMNS


# --------------------------------------------------------------------------- #
# Paradox script scanning
# --------------------------------------------------------------------------- #

def strip_comments(text):
    """Blank out # comments without changing offsets, respecting quoted strings."""
    out = []
    in_str = False
    in_comment = False
    for ch in text:
        if in_comment:
            out.append("\n" if ch == "\n" else " ")
            if ch == "\n":
                in_comment = False
            continue
        if ch == '"':
            in_str = not in_str
        elif ch == "#" and not in_str:
            in_comment = True
            out.append(" ")
            continue
        out.append(ch)
    return "".join(out)


def match_brace(text, open_idx):
    """Index of the } closing the { at open_idx, or -1."""
    depth = 0
    in_str = False
    for i in range(open_idx, len(text)):
        ch = text[i]
        if ch == '"':
            in_str = not in_str
        elif not in_str:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
    return -1


def read_script(path):
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        return fh.read()


def iter_focuses(text):
    """Yield (focus_id, icon, line_number) for every focus block in text."""
    pos = 0
    while True:
        m = FOCUS_BLOCK.search(text, pos)
        if not m:
            return
        open_idx = text.index("{", m.start())
        close_idx = match_brace(text, open_idx)
        if close_idx < 0:
            return
        body = text[open_idx:close_idx + 1]
        fid = ID_LINE.search(body)
        icon = ICON_LINE.search(body)
        yield (fid.group(1) if fid else "",
               icon.group(1) if icon else "",
               text.count("\n", 0, m.start()) + 1)
        pos = close_idx + 1


def load_sprites():
    """Every GFX_ name declared anywhere under interface/."""
    names = set()
    for root, _dirs, files in os.walk(INTERFACE_DIR):
        for fn in files:
            if not fn.lower().endswith(".gfx"):
                continue
            text = strip_comments(read_script(os.path.join(root, fn)))
            names.update(SPRITE_NAME.findall(text))
    return names


# --------------------------------------------------------------------------- #
# Classification
# --------------------------------------------------------------------------- #

def icon_source(icon, sprites):
    if icon in PLACEHOLDERS:
        return "placeholder"
    if icon in sprites:
        if icon.startswith(GENERIC_PREFIX):
            return "generic library"
    if VANILLA.match(icon):
        return "vanilla"
    if icon in sprites:
        return "bespoke"
    return "unresolved"


def foreign_tag(icon, tag):
    """The tag this sprite belongs to, when it is not the tree's own."""
    m = TAG_PREFIX.match(icon)
    if not m:
        return ""
    prefix = m.group(1)
    own = {tag}
    if tag == "MAL":
        own.add("MLA")
    elif tag == "MLA":
        own.add("MAL")
    return "" if prefix.upper().replace("USA_50", "USA") in {t.upper() for t in own} else prefix


def build_row(focus_id, icon, line, focus_file, tag, sprites, dup_counts):
    flags = []
    source = icon_source(icon, sprites)
    defined = icon in sprites

    if not icon:
        flags.append("NO ICON")
    elif icon in PLACEHOLDERS:
        flags.append("PLACEHOLDER")
    if icon and not LEGAL_NAME.match(icon):
        flags.append("ILLEGAL")
    elif icon and source == "unresolved":
        flags.append("MISSING")
    borrowed = foreign_tag(icon, tag) if icon else ""
    if borrowed:
        flags.append("FOREIGN:%s" % borrowed)
    dups = dup_counts.get(icon, 0)
    if icon and icon not in PLACEHOLDERS and dups > 1:
        flags.append("DUPLICATE")

    return {
        "Focus ID": focus_id,
        "Focus File": focus_file,
        "Tag": tag,
        "Line": line,
        "Icon": icon,
        "Icon Source": source,
        "Sprite Defined": "yes" if defined else ("vanilla" if source == "vanilla" else "no"),
        "Dup Count In Tree": dups if dups > 1 else "",
        "Flags": "; ".join(flags),
    }


def collect_rows(focus_files, sprites):
    rows = []
    for fn in focus_files:
        path = os.path.join(FOCUS_DIR, fn)
        if not os.path.exists(path):
            print("warning: %s not found" % path, file=sys.stderr)
            continue
        text = strip_comments(read_script(path))
        focuses = list(iter_focuses(text))
        dup_counts = Counter(icon for _fid, icon, _ln in focuses if icon)
        tag = FILE_TAG.get(fn, "")
        for fid, icon, line in focuses:
            rows.append(build_row(fid, icon, line, fn, tag, sprites, dup_counts))
    return rows


# --------------------------------------------------------------------------- #
# CSV round-trip
# --------------------------------------------------------------------------- #

def load_existing(path):
    """(focus file, focus id) -> hand-written column values from a prior run."""
    if not os.path.exists(path):
        return {}
    kept = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            fid = (row.get("Focus ID") or "").strip()
            if not fid:
                continue
            ffile = (row.get("Focus File") or "").strip()
            kept[(ffile, fid)] = {c: (row.get(c) or "").strip() for c in HAND_COLUMNS}
    return kept


def write_csv(path, rows, kept):
    for row in rows:
        hand = kept.get((row["Focus File"], row["Focus ID"])) or {}
        for col in HAND_COLUMNS:
            row[col] = hand.get(col, "")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------------------- #
# Lint
# --------------------------------------------------------------------------- #

def check(sprites):
    failures = 0
    for _csv_name, focus_files in THEATRES.items():
        for row in collect_rows(focus_files, sprites):
            hard = [f for f in row["Flags"].split("; ")
                    if f in ("MISSING", "ILLEGAL", "NO ICON")]
            if hard:
                failures += 1
                print("%s: %s  icon = %s  [%s]"
                      % (row["Focus File"], row["Focus ID"] or "<no id>",
                         row["Icon"] or "<none>", ", ".join(hard)))
    if failures:
        print("\n%d focus icons fail to resolve" % failures)
        return 1
    print("all focus icons resolve")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="lint the audited trees, exit 1 on MISSING / ILLEGAL")
    ap.add_argument("--summary", action="store_true", help="print counts, write no CSVs")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()

    os.chdir(args.root)
    if not os.path.isdir(FOCUS_DIR):
        sys.exit("error: run from the repo root - %s not found" % FOCUS_DIR)

    sprites = load_sprites()

    if args.check:
        sys.exit(check(sprites))

    grand = Counter()
    for csv_name, focus_files in THEATRES.items():
        rows = collect_rows(focus_files, sprites)
        counts = Counter()
        for row in rows:
            for flag in row["Flags"].split("; "):
                if flag:
                    counts[flag.split(":")[0]] += 1
        counts["focuses"] = len(rows)
        grand.update(counts)
        line = ("%-38s %4d focuses  %3d placeholder  %3d foreign  %3d duplicate  "
                "%3d missing  %3d illegal"
                % (csv_name, len(rows), counts["PLACEHOLDER"], counts["FOREIGN"],
                   counts["DUPLICATE"], counts["MISSING"], counts["ILLEGAL"]))
        if args.summary:
            print(line)
            continue
        path = os.path.join(OUT_DIR, csv_name)
        write_csv(path, rows, load_existing(path))
        print(line)
    print("%-38s %4d focuses  %3d placeholder  %3d foreign  %3d duplicate  "
          "%3d missing  %3d illegal"
          % ("TOTAL", grand["focuses"], grand["PLACEHOLDER"], grand["FOREIGN"],
             grand["DUPLICATE"], grand["MISSING"], grand["ILLEGAL"]))


if __name__ == "__main__":
    main()
