#!/usr/bin/env python3
"""Rename the generic icon library from numbers to content, driven by a CSV.

GFX_Generic_National_Focus_Agriculture_5 says nothing about what the icon
shows. This renames every sprite, its _shine twin, the art file and every
`icon =` reference in one pass, so the five things can never drift apart.

The mapping lives in CWIC Backup/documentation/Icon Audit/Icon Rename Map.csv
and is hand-authored from the contact sheets. Rows with an empty Old Sprite are
art files whose sprite is declared in another registry: the file still moves,
the sprite name is left alone.

Usage:
    python3 tools/icon_rename.py --dry-run
    python3 tools/icon_rename.py
    python3 tools/icon_rename.py --check    # nothing numbered left anywhere
"""

import argparse
import csv
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx_lib as G

MOD = "Cold War Iron Curtain"
INTERFACE = os.path.join(MOD, "interface")
FOCUS = os.path.join(MOD, "common", "national_focus")
MAP = os.path.join("CWIC Backup", "documentation", "Icon Audit", "Icon Rename Map.csv")
NUMBERED = re.compile(r"GFX_Generic_National_Focus_[A-Za-z]+_\d+|GFX_icon_generic_[a-z0-9_]+")
ICON_LINE = re.compile(r"(icon\s*=\s*)(GFX_[A-Za-z0-9_]+)")


def load_map(path):
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    sprites, files = {}, {}
    for r in rows:
        if r["Old Sprite"]:
            if r["Old Sprite"] in sprites:
                sys.exit(f"duplicate Old Sprite {r['Old Sprite']}")
            if not r["New Sprite"]:
                sys.exit(f"empty New Sprite for {r['Old Sprite']}")
            sprites[r["Old Sprite"]] = r["New Sprite"]
        if r["Old File"]:
            files[r["Old File"]] = r["New File"]
    if len(set(sprites.values())) != len(sprites):
        sys.exit("collision among New Sprite values")
    if len(set(files.values())) != len(files):
        sys.exit("collision among New File values")
    return sprites, files


def sprite_pattern(sprites):
    """Match a sprite name and its _shine twin, longest alternative first.

    The negative lookahead stops Politics_1 from matching inside Politics_19,
    and putting the _shine form first stops it from being truncated.
    """
    alts = []
    for old in sprites:
        alts.append(old + "_shine")
        alts.append(old)
    alts.sort(key=len, reverse=True)
    return re.compile("(?:" + "|".join(re.escape(a) for a in alts) + r")(?![A-Za-z0-9_])")


def rewrite_registries(sprites, files, dry):
    pat = sprite_pattern(sprites)

    def sub(m):
        tok = m.group(0)
        if tok.endswith("_shine") and tok[:-6] in sprites:
            return sprites[tok[:-6]] + "_shine"
        return sprites[tok]

    n_sprite = n_path = touched = 0
    for dirpath, _d, fs in os.walk(INTERFACE):
        for fn in fs:
            if not fn.lower().endswith(".gfx"):
                continue
            p = os.path.join(dirpath, fn)
            text = G.read_text(p)
            new, a = pat.subn(sub, text)
            b = 0
            for old, dst in files.items():
                if old in new:
                    b += new.count(old)
                    new = new.replace(old, dst)
            if a or b:
                touched += 1
                n_sprite += a
                n_path += b
                if not dry:
                    G.write_text(p, new)
    return n_sprite, n_path, touched


def rewrite_focuses(sprites, dry):
    """Rewrite `icon =` values only, preserving each file's BOM as found."""
    n_ref = touched = 0
    stray = []
    for dirpath, _d, fs in os.walk(FOCUS):
        for fn in fs:
            if not fn.lower().endswith(".txt"):
                continue
            p = os.path.join(dirpath, fn)
            raw = open(p, "rb").read()
            bom = raw.startswith(b"\xef\xbb\xbf")
            text = raw.decode("utf-8-sig" if bom else "utf-8", errors="surrogateescape")

            hits = [0]

            def sub(m):
                if m.group(2) in sprites:
                    hits[0] += 1
                    return m.group(1) + sprites[m.group(2)]
                return m.group(0)

            new = ICON_LINE.sub(sub, text)
            for tok in set(NUMBERED.findall(ICON_LINE.sub("", new))):
                if tok in sprites:
                    stray.append((os.path.relpath(p, FOCUS), tok))
            if hits[0]:
                touched += 1
                n_ref += hits[0]
                if not dry:
                    data = new.encode("utf-8", errors="surrogateescape")
                    if bom:
                        data = b"\xef\xbb\xbf" + data
                    with open(p, "wb") as fh:
                        fh.write(data)
                    after = open(p, "rb").read()
                    if after.startswith(b"\xef\xbb\xbf") != bom:
                        sys.exit(f"{p}: BOM state changed")
    return n_ref, touched, stray


def check():
    bad = []
    for root in (INTERFACE, FOCUS):
        for dirpath, _d, fs in os.walk(root):
            for fn in fs:
                if not fn.lower().endswith((".gfx", ".txt", ".gui")):
                    continue
                p = os.path.join(dirpath, fn)
                text = open(p, encoding="utf-8", errors="surrogateescape").read()
                for tok in sorted(set(NUMBERED.findall(text))):
                    bad.append((p, tok))
    if bad:
        print(f"{len(bad)} numbered generic names still present:")
        for p, tok in bad[:30]:
            print(f"  {p}: {tok}")
        return 1
    print("no numbered generic icon names remain")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    os.chdir(args.root)
    if args.check:
        sys.exit(check())

    sprites, files = load_map(MAP)
    print(f"{len(sprites)} sprites, {len(files)} art files")

    for old, new in files.items():
        src, dst = os.path.join(MOD, old), os.path.join(MOD, new)
        if src == dst or args.dry_run:
            continue
        subprocess.run(["git", "mv", src, dst], check=True)

    a, b, t = rewrite_registries(sprites, files, args.dry_run)
    print(f"registries: {a} sprite names, {b} texture paths, across {t} files")
    n, ft, stray = rewrite_focuses(sprites, args.dry_run)
    print(f"focus trees: {n} icon references across {ft} files")
    if stray:
        print(f"WARNING: {len(stray)} generic names outside an icon = line:")
        for p, tok in stray[:10]:
            print(f"  {p}: {tok}")


if __name__ == "__main__":
    main()
