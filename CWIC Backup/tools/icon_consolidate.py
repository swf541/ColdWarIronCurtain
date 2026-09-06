#!/usr/bin/env python3
"""Fold the four scattered generic icon libraries into gfx/interface/goals/generic/.

Before:
    goals/Generic_National_Focus/<Category>/  290 files, numbered names
    goals/GENERIC_ICONS/                       48 files, content names
    goals/Generic_Icons/                       22 files, the newly imported pack
    goals/new_generic/                          3 dds

After:
    goals/generic/<category>/                  one tree, lowercase throughout

Sprite names are NOT touched here - only the art paths and which registry
declares them. Renaming the numbered sprites by content is a separate pass
(tools/icon_rename.py).

Usage:
    python3 tools/icon_consolidate.py --dry-run
    python3 tools/icon_consolidate.py
"""

import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx_lib as G

MOD = "Cold War Iron Curtain"
GOALS = os.path.join(MOD, "gfx", "interface", "goals")
INTERFACE = os.path.join(MOD, "interface")
DEST = "generic"

CATEGORIES = ["agriculture", "construction", "diplomacy", "economics", "military",
              "other", "politics", "production", "research", "trading", "usa", "ussr"]

# Files that do not already live in a Generic_National_Focus/<Category>/ folder
# need an explicit home. Where a numbered sprite already aliases the art, the
# category is taken from that sprite instead - see alias_categories().
MANUAL = {
    "GENERIC_ICONS/Biden_Presidency.png": "usa",
    "GENERIC_ICONS/DDR.png": "politics",
    "GENERIC_ICONS/Generic_Asia_Police.png": "military",
    "GENERIC_ICONS/Generic_Brezhnev_1.png": "ussr",
    "GENERIC_ICONS/Generic_Communism.png": "politics",
    "GENERIC_ICONS/Generic_Diplomacy_3.dds": "diplomacy",
    "GENERIC_ICONS/Generic_Government.png": "politics",
    "GENERIC_ICONS/Generic_Indonesia.png": "diplomacy",
    "GENERIC_ICONS/Generic_Indonesia1.png": "diplomacy",
    "GENERIC_ICONS/Generic_Indonesia2.png": "diplomacy",
    "GENERIC_ICONS/Generic_Light_Tank.png": "military",
    "GENERIC_ICONS/Generic_Nationalism.png": "politics",
    "GENERIC_ICONS/Generic_Religion.png": "other",
    "GENERIC_ICONS/Generic_Tank.png": "military",

    "Generic_Icons/icon_generic_a_fistful_of_dollars.png": "economics",
    "Generic_Icons/icon_generic_akm.png": "military",
    "Generic_Icons/icon_generic_black_gold.png": "production",
    "Generic_Icons/icon_generic_cia.png": "usa",
    "Generic_Icons/icon_generic_communism.png": "politics",
    "Generic_Icons/icon_generic_globe_handshake.png": "diplomacy",
    "Generic_Icons/icon_generic_handgun.png": "military",
    "Generic_Icons/icon_generic_heli_swarm.png": "military",
    "Generic_Icons/icon_generic_infrastructure.png": "construction",
    "Generic_Icons/icon_generic_intel.png": "other",
    "Generic_Icons/icon_generic_lenin.png": "ussr",
    "Generic_Icons/icon_generic_mas36.png": "military",
    "Generic_Icons/icon_generic_medical.png": "research",
    "Generic_Icons/icon_generic_mig15.png": "military",
    "Generic_Icons/icon_generic_mig17.png": "military",
    "Generic_Icons/icon_generic_molotov.png": "politics",
    "Generic_Icons/icon_generic_politics.png": "politics",
    "Generic_Icons/icon_generic_scales.png": "politics",
    "Generic_Icons/icon_generic_skull.png": "other",
    "Generic_Icons/icon_generic_soviet_truck.png": "ussr",
    "Generic_Icons/icon_generic_united_nations.png": "diplomacy",
    "Generic_Icons/icon_generic_white_house.png": "usa",

    "new_generic/icon_114.dds": "usa",
    "new_generic/usa_fp_generic_congress_approve.dds": "usa",
    "new_generic/usa_fp_generic_weapon_increase.dds": "usa",
}

# Not an asset - a Photoshop source file that ships in the mod for no reason.
PARKED = {"GENERIC_ICONS/Template for dummies.psd": os.path.join(
    "CWIC Backup", "documentation", "Icon Sources", "Template for dummies.psd")}

SOURCE_DIRS = ["Generic_National_Focus", "GENERIC_ICONS", "Generic_Icons", "new_generic"]


def alias_categories():
    """{GENERIC_ICONS/<file>: category} for art a numbered sprite already aliases.

    GFX_Generic_National_Focus_Agriculture_2 pointing at Generic_Agriculture.png
    is the mod telling us that file belongs under agriculture.
    """
    out = {}
    reg = os.path.join(INTERFACE, "CWIC_Generic_National_Focus.gfx")
    text = G.read_text(reg)
    for name, start, end in G.iter_blocks(text):
        if not name:
            continue
        m = re.search(r'texturefile\s*=\s*"([^"]+)"', text[start:end], re.I)
        cat = re.match(r"GFX_Generic_National_Focus_([A-Za-z]+)_\d+$", name)
        if not m or not cat:
            continue
        rel = m.group(1).split("goals/", 1)[-1]
        if rel.split("/")[0] in SOURCE_DIRS and not rel.startswith("Generic_National_Focus/"):
            out[rel] = cat.group(1).lower()
    return out


def build_moves():
    """{old path relative to goals/: new path relative to goals/}."""
    moves = {}
    aliases = alias_categories()
    for src in SOURCE_DIRS:
        base = os.path.join(GOALS, src)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for fn in files:
                rel = os.path.relpath(os.path.join(dirpath, fn), GOALS).replace(os.sep, "/")
                if rel in PARKED:
                    continue
                parts = rel.split("/")
                if src == "Generic_National_Focus" and len(parts) == 3:
                    cat = parts[1].lower()
                else:
                    cat = aliases.get(rel) or MANUAL.get(rel)
                if cat is None:
                    raise SystemExit(f"no category for {rel} - add it to MANUAL")
                if cat not in CATEGORIES:
                    raise SystemExit(f"unknown category {cat!r} for {rel}")
                moves[rel] = f"{DEST}/{cat}/{fn}"
    dests = {}
    for old, new in moves.items():
        if new in dests:
            raise SystemExit(f"collision: {old} and {dests[new]} both -> {new}")
        dests[new] = old
    return moves


def repoint(moves, dry_run):
    """Rewrite every reference to a moved file across interface/**/*.gfx."""
    table = {f"gfx/interface/goals/{o}": f"gfx/interface/goals/{n}" for o, n in moves.items()}
    pattern = re.compile("|".join(re.escape(k) for k in sorted(table, key=len, reverse=True)))
    touched, total = 0, 0
    for dirpath, _dirs, files in os.walk(INTERFACE):
        for fn in files:
            if not fn.lower().endswith(".gfx"):
                continue
            path = os.path.join(dirpath, fn)
            text = G.read_text(path)
            new, n = pattern.subn(lambda m: table[m.group(0)], text)
            if n:
                touched += 1
                total += n
                if not dry_run:
                    G.write_text(path, new)
    return touched, total


def run(cmd, dry_run):
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def tracked(path):
    return subprocess.run(["git", "ls-files", "--error-unmatch", path],
                          capture_output=True).returncode == 0


def move_file(old_abs, new_abs, dry_run):
    if not dry_run:
        os.makedirs(os.path.dirname(new_abs), exist_ok=True)
    if tracked(old_abs):
        run(["git", "mv", old_abs, new_abs], dry_run)
    elif not dry_run:
        os.replace(old_abs, new_abs)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="report, change nothing")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()
    os.chdir(args.root)

    moves = build_moves()
    print(f"{len(moves)} files to move into goals/{DEST}/")
    by_cat = {}
    for new in moves.values():
        by_cat[new.split("/")[1]] = by_cat.get(new.split("/")[1], 0) + 1
    for cat in CATEGORIES:
        print(f"  {cat:14s} {by_cat.get(cat, 0)}")

    for old, new in sorted(moves.items()):
        move_file(os.path.join(GOALS, old), os.path.join(GOALS, new), args.dry_run)
    for old, new in PARKED.items():
        move_file(os.path.join(GOALS, old), new, args.dry_run)
        print(f"parked {old} -> {new}")

    touched, total = repoint(moves, args.dry_run)
    print(f"repointed {total} paths across {touched} registries")

    if not args.dry_run:
        for src in SOURCE_DIRS:
            base = os.path.join(GOALS, src)
            for dirpath, _dirs, _f in os.walk(base, topdown=False):
                try:
                    os.rmdir(dirpath)
                except OSError:
                    pass
            if os.path.exists(base):
                print(f"WARNING: {base} is not empty")


if __name__ == "__main__":
    main()
