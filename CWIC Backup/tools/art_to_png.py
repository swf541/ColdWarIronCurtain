#!/usr/bin/env python3
"""Normalise the generic icon library to 8-bit png and repoint the registries.

HOI4 renders uncompressed 32-bit ARGB and 16-bit A1R5G5B5 dds unreliably, and
dispatches image loading on the file extension, so a stray .tga or .dds in an
otherwise-png library is a latent rendering bug. Each file is converted with
ImageMagick, checked against the source (dimensions and per-channel means must
match exactly), and only then is every texturefile / animationmaskfile
reference repointed and the original removed.

Usage:
    python3 tools/art_to_png.py --dry-run   # report what would change
    python3 tools/art_to_png.py             # convert, repoint, delete
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx_lib as G

MOD = "Cold War Iron Curtain"
ART_DIR = os.path.join(MOD, "gfx", "interface", "goals", "generic")
INTERFACE_DIR = os.path.join(MOD, "interface")
CONVERTIBLE = (".dds", ".tga", ".bmp")


def probe(path):
    """(width, height, mean r/g/b/a) as ImageMagick reads the file."""
    fmt = "%w %h %[fx:mean.r] %[fx:mean.g] %[fx:mean.b] %[fx:mean.a]"
    out = subprocess.run(["identify", "-quiet", "-format", fmt, path],
                         capture_output=True, text=True, check=True).stdout.split()
    return (int(out[0]), int(out[1])) + tuple(round(float(v), 6) for v in out[2:])


def convert(src, dry):
    png = os.path.splitext(src)[0] + ".png"
    before = probe(src)
    if dry:
        return png, before
    subprocess.run(["magick", src, "PNG32:" + png], check=True)
    after = probe(png)
    if before != after:
        os.remove(png)
        sys.exit(f"error: {src} did not round-trip\n  src {before}\n  png {after}")
    return png, before


def find_sources():
    out = []
    for dirpath, _dirs, files in os.walk(ART_DIR):
        for fn in files:
            if fn.lower().endswith(CONVERTIBLE):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="report only, change nothing")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()
    os.chdir(args.root)
    if not os.path.isdir(ART_DIR):
        sys.exit(f"error: run from the repo root - {ART_DIR} not found")

    sources = find_sources()
    print(f"converting {len(sources)} files")

    table = {}
    for src in sources:
        png, dims = convert(src, args.dry_run)
        rel_old = os.path.relpath(src, MOD).replace(os.sep, "/")
        rel_new = os.path.relpath(png, MOD).replace(os.sep, "/")
        table[rel_old] = rel_new
        print(f"  {os.path.basename(src):<52s} {dims[0]}x{dims[1]}")

    if not table:
        return

    total, touched = 0, 0
    for dirpath, _dirs, files in os.walk(INTERFACE_DIR):
        for fn in files:
            if not fn.lower().endswith(".gfx"):
                continue
            path = os.path.join(dirpath, fn)
            text = G.read_text(path)
            new, n = text, 0
            for old_rel, new_rel in table.items():
                if old_rel in new:
                    n += new.count(old_rel)
                    new = new.replace(old_rel, new_rel)
            if n:
                total += n
                touched += 1
                if not args.dry_run:
                    G.write_text(path, new)
                print(f"{fn:<48s} {n:4d} references")
    print(f"{total} references repointed across {touched} registries")

    if not args.dry_run:
        for src in sources:
            subprocess.run(["git", "rm", "-q", "--ignore-unmatch", "--cached", src],
                           capture_output=True)
            os.remove(src)
        print(f"removed {len(sources)} originals")


if __name__ == "__main__":
    main()
