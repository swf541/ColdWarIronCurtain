#!/usr/bin/env python3
"""Shared sprite-registry helpers for the CWIC icon tools.

Every function here works on `bytes` decoded as UTF-8, never on a re-encoded
string round trip: the .gfx registries carry no BOM and LF-only line endings,
and both must survive untouched (a BOM makes Clausewitz reject the file).
"""

import os
import re

SPRITE_OPEN = re.compile(r'\bspriteType\s*=\s*\{', re.I)
NAME_IN_BODY = re.compile(r'name\s*=\s*"([^"]+)"', re.I)
NAME_LINE = re.compile(r'^[ \t]*name\s*=\s*"([^"]+)"', re.I | re.M)


def read_text(path):
    """Read a registry, asserting it carries no BOM."""
    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise SystemExit(f"{path}: unexpected BOM")
    return raw.decode("utf-8", errors="strict")


def write_text(path, text):
    """Write LF-only UTF-8 with no BOM, then verify the bytes landed that way."""
    data = text.encode("utf-8")
    if data.startswith(b"\xef\xbb\xbf"):
        raise SystemExit(f"{path}: refusing to write a BOM")
    with open(path, "wb") as fh:
        fh.write(data)
    check = open(path, "rb").read()
    if check[:3] == b"\xef\xbb\xbf" or b"\r\n" in check:
        raise SystemExit(f"{path}: BOM or CRLF appeared after write")


def match_brace(text, open_idx):
    """Index of the } closing the { at open_idx, or -1."""
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def iter_blocks(text):
    """Yield (name, start, end) for every SpriteType block.

    `start` is the index of the `spriteType` keyword and `end` is one past its
    closing brace, so text[start:end] is the whole block.
    """
    pos = 0
    while True:
        m = SPRITE_OPEN.search(text, pos)
        if not m:
            return
        close = match_brace(text, m.end() - 1)
        if close < 0:
            return
        body = text[m.end():close]
        nm = NAME_IN_BODY.search(body)
        yield (nm.group(1) if nm else None), m.start(), close + 1
        pos = close + 1


def declarations(interface_dir):
    """{sprite name: [registry paths]} across every .gfx under interface_dir."""
    out = {}
    for dirpath, _dirs, files in os.walk(interface_dir):
        for fn in files:
            if not fn.lower().endswith(".gfx"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, interface_dir)
            text = open(path, encoding="utf-8-sig", errors="replace").read()
            for m in NAME_LINE.finditer(text):
                out.setdefault(m.group(1), []).append(rel)
    return out


def drop_blocks(text, predicate):
    """Remove every SpriteType block whose name satisfies predicate.

    Also swallows the blank line a removed block leaves behind so the file does
    not accumulate whitespace churn.
    """
    spans = [(s, e) for name, s, e in iter_blocks(text) if name and predicate(name)]
    for start, end in reversed(spans):
        line_start = text.rfind("\n", 0, start) + 1
        if text[line_start:start].strip():
            line_start = start
        after = end
        while after < len(text) and text[after] in " \t":
            after += 1
        if after < len(text) and text[after] == "\n":
            after += 1
        while after < len(text) and text[after] == "\n":
            after += 1
            break
        text = text[:line_start] + text[after:]
    return text, len(spans)
