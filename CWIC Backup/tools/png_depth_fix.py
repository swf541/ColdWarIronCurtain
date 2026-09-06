#!/usr/bin/env python3
"""Rewrite 16-bit-per-channel PNGs as 8-bit so HOI4 can render them.

The Clausewitz PNG loader only handles 8 bits per channel. Handed a 16-bit file
it walks the buffer at half the real stride, which renders as a magenta,
horizontally smeared image - the source art itself is fine.

Candidates are found by reading the PNG IHDR header directly (decoding all
17k images just to learn their bit depth is far too slow). Each hit is then
converted in place to PNG32 and checked against the source: dimensions must
match exactly and every channel mean must land within one 8-bit step.

Usage:
    python3 tools/png_depth_fix.py --dry-run
    python3 tools/png_depth_fix.py            # convert in place
"""

import argparse
import os
import struct
import subprocess
import sys

MOD = "Cold War Iron Curtain"
GFX_DIR = os.path.join(MOD, "gfx")
TOLERANCE = 1.0 / 255.0
PNG_SIG = b"\x89PNG\r\n\x1a\n"
FMT = "%z %w %h %[fx:mean.r] %[fx:mean.g] %[fx:mean.b] %[fx:mean.a]"


def png_header(path):
    """(width, height, bit_depth, colour_type) straight out of IHDR, or None."""
    with open(path, "rb") as fh:
        head = fh.read(26)
    if len(head) < 26 or head[:8] != PNG_SIG or head[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h, head[24], head[25]


def probe(path):
    """Decoded stats. Only called for the handful of files we actually touch."""
    out = subprocess.run(["identify", "-quiet", "-format", FMT, path],
                         capture_output=True, text=True, check=True).stdout.split()
    return int(out[0]), int(out[1]), int(out[2]), [float(v) for v in out[3:]]


def find_deep():
    hits = []
    for root, _dirs, files in os.walk(GFX_DIR):
        for fn in files:
            if not fn.lower().endswith(".png"):
                continue
            path = os.path.join(root, fn)
            hdr = png_header(path)
            if hdr is None:
                print("warning: not a readable PNG: %s" % path, file=sys.stderr)
                continue
            if hdr[2] > 8:
                hits.append((path, hdr))
    return sorted(hits)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="report only, change nothing")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()

    os.chdir(args.root)
    if not os.path.isdir(GFX_DIR):
        sys.exit("error: run from the repo root - %s not found" % GFX_DIR)

    hits = find_deep()
    print("%d PNGs are deeper than 8 bits per channel" % len(hits))
    if args.dry_run:
        for path, (w, h, depth, ctype) in hits:
            print("  %-100s %dx%d depth=%d colour=%d"
                  % (path[len(GFX_DIR) + 1:], w, h, depth, ctype))
        return

    failed = 0
    for path, _hdr in hits:
        _d, w, h, means = probe(path)
        subprocess.run(["magick", path, "-depth", "8", "PNG32:" + path], check=True)
        depth, nw, nh, nmeans = probe(path)
        drift = max(abs(a - b) for a, b in zip(means, nmeans))
        if depth > 8 or (nw, nh) != (w, h) or drift > TOLERANCE:
            print("  FAILED %s  depth=%d %dx%d drift=%.6f" % (path, depth, nw, nh, drift))
            failed += 1
    print("converted %d files, %d failed" % (len(hits) - failed, failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
