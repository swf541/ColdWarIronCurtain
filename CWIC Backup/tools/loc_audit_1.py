#!/usr/bin/env python3
"""CWIC localisation auditor for the Southeast Asia content.

Parses the event files listed in THEATRES, resolves every title / description /
option key against localisation/english/*.yml, and writes one CSV per theatre.

The CSVs are round-trippable: generated columns are refreshed on every run while
the hand-written columns (Grade, Priority, Action, Completion, Context, Notes)
are carried over from the existing file, keyed on (Event File, Event ID).

Usage:
    python3 tools/loc_audit.py            # regenerate every theatre CSV
    python3 tools/loc_audit.py --check    # lint the SEA loc files, exit 1 on failure
    python3 tools/loc_audit.py --summary  # print counts, write nothing

See Cold War Iron Curtain/LOC_STYLE_GUIDE.md for the rules this enforces.
"""

import argparse
import csv
import os
import re
import sys
from collections import OrderedDict

MOD = "Cold War Iron Curtain"
EVENT_DIR = os.path.join(MOD, "events")
LOC_DIR = os.path.join(MOD, "localisation", "english")

EVENT_KINDS = (
    "country_event",
    "news_event",
    "state_event",
    "unit_leader_event",
    "operative_leader_event",
)

# An event definition always carries at least one of these. A bare
# `country_event = { id = X days = 2 }` effect invocation carries none of them,
# which is how the two are told apart - definitions are not at a fixed indent.
DEFINITION_MARKERS = ("option", "title", "desc", "hidden", "is_triggered_only",
                      "trigger", "fire_only_once", "mean_time_to_happen")

SEA_KEYWORDS = re.compile(
    r"vietnam|viet minh|vietminh|indochina|indochine|saigon|hanoi|haiphong|tonkin|annam|"
    r"cochinchina|dien bien|geneva|malaya|malaysia|kuala lumpur|singapore|"
    r"laos|laotian|vientiane|cambodia|cambodian|phnom penh|thailand|siam|bangkok|"
    r"\bVIE\b|\bVIN\b|\bFRE\b|\bMLA\b|\bMAL\b|\bLOS\b|\bCAM\b|\bMEO\b|\bNLF\b",
    re.I,
)

THEATRES = OrderedDict([
    ("VIE Audit - VIE Events.csv", ["VIE_Events.txt"]),
    ("SEA Audit - North Vietnam.csv", [
        "VIN_Events.txt", "VIN_FORPOL_events.txt", "VIN_MIL_events.txt",
        "VIN_Campaign_Events.txt", "VIN_Post_DBP_South_Events.txt", "SWF_VIN_events.txt",
        "SWF_VIN_second_congress_events_final.txt",
        "North_Vietnam_Flavor.txt", "North Vietnam.txt",
    ]),
    ("SEA Audit - French Indochina.csv", [
        "FRE_Events.txt", "FRE_Operation_Events.txt", "Indochina_War.txt",
        "Indochina_War_Rework.txt", "Indochina_Flavor_Events.txt",
        "IC_Laos_Raid.txt", "FRE_Dien_Bien_Response_Events.txt",
        "FRE_Pollux_Events.txt", "FRE_Atlante_Events.txt",
        "SWF_Indochina_War_events.txt",
    ]),
    ("SEA Audit - Geneva and Settlement.csv", [
        "Geneva_Conference_Invitations.txt", "Geneva_Conference_Session.txt",
        "VIE_Border_Settlement.txt", "VIE_VIN_Reunification_50s_events.txt",
        "American_Indochina.txt",
    ]),
    ("SEA Audit - Indochina Minors.csv", [
        "MEO.txt", "MEO_50s_events.txt", "Cambodia.txt", "Cambodia_1950s.txt",
        "Cambodia_Civil_War.txt", "Cambodian_Elections.txt", "Phu Dai Army.txt",
        "SIA.txt", "Vietnam.txt",
    ]),
    ("SEA Audit - Malaya.csv", [
        "Malayan_Emergency.txt", "MLA.txt", "Malaysia.txt", "KLFA_Events.txt",
        "Com_Malaysia.txt", "SGP.txt",
    ]),
    # Filtered to SEA-touching events only - see sea_only below.
    ("SEA Audit - Great Powers in SEA.csv", [
        "USA.txt", "America_1950s_Expansion.txt", "USA_70s_Events.txt",
        "France.txt", "KMT_China_Events.txt", "prc.txt", "PRC_Dispute.txt",
        "SOV_Andropov_Events.txt",
    ]),
])

SEA_ONLY = {"SEA Audit - Great Powers in SEA.csv"}

# Loc files the --check lint covers. Union'd with whatever the audited events
# actually resolve into, so new files are picked up automatically.
SEA_LOC_FILES = [
    "VIE_events_l_english.yml", "VIE_focus_l_english.yml", "VIE_misc_l_english.yml",
    "VIE_parties_l_english.yml", "VIE_Border_Settlement_l_english.yml",
    "VIE_VIN_Reunification_50s_l_english.yml",
    "VIN_events_l_english.yml", "VIN_focus_l_english.yml", "VIN_misc_l_english.yml",
    "VIN_FORPOL_l_english.yml", "VIN_MIL_l_english.yml", "VIN_newstuff_l_english.yml",
    "VIN_parties_l_english.yml", "VIN_custom_effect_tooltips_l_english.yml",
    "VIN_Post_DBP_South_l_english.yml",
    "French_Indochina_l_english.yml", "FRE_CEFEO_l_english.yml",
    "FRE_Dien_Bien_Response_l_english.yml",
    "FRE_events_l_english.yml", "FRE_focus_l_english.yml", "FRE_misc_l_english.yml",
    "IC_Laos_Raid_l_english.yml", "CWIC_Geneva_Conference_l_english.yml",
    "CWIC_Indochina_Outcomes_l_english.yml", "CWIC_Struggle_l_english.yml",
    "MEO_events_l_english .yml", "MEO_focus_50s_l_english.yml",
    "MEO_characters_l_english.yml",
    "MLA_l_english.yml", "MAL_l_english.yml", "extracted_MLA_l_english.yml",
    "extracted_Malaysia_l_english.yml", "extracted_Indochina_l_english.yml",
    "focus_CAM_50s_l_english.yml", "focus_SIA_50s_l_english.yml",
    "focus_VIN_50s_l_english.yml", "focus_VIN_60s_l_english.yml",
    "SWF_Indochina_War_l_english.yml", "SWF_VIN_l_english.yml",
    "SWF_VIN_second_congress_l_english.yml",
]

GENERATED_COLUMNS = [
    "Event ID", "Event File", "Loc File", "Type", "Fires For", "Options",
    "Has Title", "Has Description", "Picture", "Desc Chars", "Paragraphs",
    "News Format", "Flags",
]
HAND_COLUMNS = ["Grade", "Priority", "Action", "Completion", "Context", "Notes"]
COLUMNS = GENERATED_COLUMNS + HAND_COLUMNS

# Keys may contain an apostrophe - MLA_60s.txt really does define focuses like
# MLA_Become_the_World's_Largest_Tin_Producer, and the game resolves them.
LOC_LINE = re.compile(r"^([ \t]*)([A-Za-z0-9_.'\-]+):\s*(\d*)\s*\"(.*)\"[ \t]*(#.*)?$")
PLACEHOLDER = re.compile(r"^\s*(will be added|to be added|tbd|placeholder|desc|text|todo)\s*\.?\s*$", re.I)
# Lowercase only: "Mau Mau", "Quoc-Gia Gia" and friends are proper nouns, not typos.
DOUBLED_WORD = re.compile(r"\b([a-z]+)\s+\1\b")
SMART_PUNCT = "‘’“”–—…•"
NEWS_DATELINE = re.compile(r"\[\??[A-Za-z0-9_.]*Get(Date|Month|Year)")
EVENT_ID_TOKEN = re.compile(r"\b([A-Za-z0-9_]+\.\d+)\b")
_KINDS = "|".join(EVENT_KINDS)
FIRE_BLOCK = re.compile(r"\b(?:" + _KINDS + r")\s*=\s*\{")
FIRE_SHORTHAND = re.compile(r"\b(?:" + _KINDS + r")\s*=\s*([A-Za-z0-9_.]+)")
FIRE_CALLBACK = re.compile(r"\bon_(?:win|lose|cancel)\s*=\s*([A-Za-z0-9_.]+)")
RANDOM_EVENTS = re.compile(r"\brandom_events\s*=\s*\{([^{}]*)\}")
RANDOM_ENTRY = re.compile(r"=\s*([A-Za-z0-9_.]+)")
# Any `<key> = <namespaced id>`, whatever the key is called - except the keys
# that take a loc key, where naming an event id is a typo rather than a fire.
ID_ASSIGNMENT = re.compile(
    r"\b(?!(?:desc|title|name|text|picture)\b)[A-Za-z_][A-Za-z0-9_]*"
    r"\s*=\s*([A-Za-z_][A-Za-z0-9_]*\.\d+)(?![.\w])")


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


def scan_entries(body):
    """Yield (key, scalar, subbody) for every `key = value` at depth 1 of body.

    body includes its outer braces. Exactly one of scalar/subbody is not None.
    """
    inner = body[body.index("{") + 1:body.rindex("}")]
    i = 0
    n = len(inner)
    while i < n:
        m = re.compile(r"([A-Za-z0-9_.\-]+)\s*(=|<|>)\s*").match(inner, i)
        if not m:
            i += 1
            continue
        key = m.group(1)
        j = m.end()
        if j >= n:
            break
        if inner[j] == "{":
            close = match_brace(inner, j)
            if close == -1:
                break
            yield key, None, inner[j:close + 1]
            i = close + 1
        elif inner[j] == '"':
            close = inner.find('"', j + 1)
            yield key, inner[j + 1:close], None
            i = close + 1
        else:
            vm = re.compile(r"[^\s{}]+").match(inner, j)
            if not vm:
                i = j + 1
                continue
            yield key, vm.group(0), None
            i = vm.end()


def iter_event_definitions(text):
    """Yield (kind, body) for every real event definition in an event file."""
    clean = strip_comments(text)
    pattern = re.compile(r"\b(" + "|".join(EVENT_KINDS) + r")\s*=\s*\{")
    for m in pattern.finditer(clean):
        open_idx = clean.index("{", m.end() - 1)
        close = match_brace(clean, open_idx)
        if close == -1:
            continue
        body = clean[open_idx:close + 1]
        keys = {k for k, _, _ in scan_entries(body)}
        if "id" not in keys:
            continue
        if not keys.intersection(DEFINITION_MARKERS):
            continue  # an effect invocation, not a definition
        yield m.group(1), body


def text_keys(scalar, subbody):
    """Loc keys behind a title/desc/name entry, scalar or `{ text = K trigger = {} }`."""
    if scalar is not None:
        return [scalar]
    if subbody is None:
        return []
    return [v for k, v, _ in scan_entries(subbody) if k == "text" and v]


def parse_event(kind, body):
    ev = {
        "kind": kind, "id": None, "title": [], "desc": [], "picture": "",
        "options": [], "hidden": False, "major": False, "tags": set(),
        "triggered_only": False,
    }
    for key, scalar, sub in scan_entries(body):
        if key == "id" and scalar:
            ev["id"] = scalar
        elif key == "title":
            ev["title"] += text_keys(scalar, sub)
        elif key == "desc":
            ev["desc"] += text_keys(scalar, sub)
        elif key == "picture" and scalar:
            ev["picture"] = scalar
        elif key == "hidden" and scalar == "yes":
            ev["hidden"] = True
        elif key == "major" and scalar == "yes":
            ev["major"] = True
        elif key == "is_triggered_only" and scalar == "yes":
            ev["triggered_only"] = True
        elif key == "option" and sub:
            names = []
            for k2, s2, sb2 in scan_entries(sub):
                if k2 == "name":
                    names += text_keys(s2, sb2)
            ev["options"].append(names)
    for m in re.finditer(r"\b(?:original_tag|tag|has_country_flag_tag)\s*=\s*([A-Z]{3})\b", body):
        ev["tags"].add(m.group(1))
    # HOI4 falls back to <id>.t / <id>.d when the block omits them.
    if not ev["title"] and ev["id"]:
        ev["title"] = [ev["id"] + ".t"]
    if not ev["desc"] and ev["id"]:
        ev["desc"] = [ev["id"] + ".d"]
    return ev


# --------------------------------------------------------------------------- #
# Localisation
# --------------------------------------------------------------------------- #

def collect_defined_ids():
    """Every event id defined anywhere in events/, with how many times."""
    defined = {}
    for name in sorted(os.listdir(EVENT_DIR)):
        if not name.endswith(".txt"):
            continue
        text = read_loc_file(os.path.join(EVENT_DIR, name))
        for kind, body in iter_event_definitions(text):
            ev_id = parse_event(kind, body)["id"]
            if ev_id:
                defined[ev_id] = defined.get(ev_id, 0) + 1
    return defined


def explicit_fires(text):
    """Yield ids fired by an unambiguous firing construct.

    `news_event = X` shorthand, `country_event = { id = X days = 2 }` block form
    (told apart from a definition by DEFINITION_MARKERS), `random_events` lists
    and the `start_border_war` on_win/on_lose/on_cancel callbacks. Used for the
    handful of events with a bare numeric id, where the generic scan below
    cannot tell an event id from a state or province number.
    """
    for m in FIRE_BLOCK.finditer(text):
        open_idx = text.index("{", m.end() - 1)
        close = match_brace(text, open_idx)
        if close == -1:
            continue
        body = text[open_idx:close + 1]
        entries = list(scan_entries(body))
        if {k for k, _, _ in entries}.intersection(DEFINITION_MARKERS):
            continue  # a definition, not a fire
        for key, scalar, _ in entries:
            if key == "id" and scalar:
                yield scalar
    for pattern in (FIRE_SHORTHAND, FIRE_CALLBACK):
        for m in pattern.finditer(text):
            yield m.group(1)
    for m in RANDOM_EVENTS.finditer(text):
        for entry in RANDOM_ENTRY.finditer(m.group(1)):
            yield entry.group(1)


def build_reference_index(defined):
    """event id -> number of places in live mod script that fire it.

    HOI4 has too many firing forms to enumerate - the block and shorthand forms,
    `random_events` weights, and callbacks like the `start_border_war`
    on_win/on_lose/on_cancel trio, which is where the first cut of this went
    wrong. So instead of matching firing syntax, match the ids themselves: any
    `<key> = <id>` naming a defined event is a fire, minus the event's own
    definition line. An event's title/desc/option keys are `<id>.t` and friends,
    so they do not collide. Comments are stripped, so a commented-out fire does
    not count as wiring.
    """
    counts = {}
    numeric = {i for i in defined if "." not in i}
    skip = {"localisation", "gfx", "interface", "music", "sound", "tutorial", "map"}
    for root, dirs, files in os.walk(MOD):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in files:
            if not name.endswith(".txt"):
                continue
            try:
                text = strip_comments(read_loc_file(os.path.join(root, name)))
            except OSError:
                continue
            for m in ID_ASSIGNMENT.finditer(text):
                token = m.group(1)
                if token in defined:
                    counts[token] = counts.get(token, 0) + 1
            if numeric:
                for token in explicit_fires(text):
                    if token in numeric:
                        counts[token] = counts.get(token, 0) + 1
    for event_id, definitions in defined.items():
        if "." in event_id:
            counts[event_id] = counts.get(event_id, 0) - definitions
    return counts


def read_loc_file(path):
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        return fh.read()


def load_loc(loc_dir):
    """key -> (value, filename). First definition wins, matching the game."""
    loc = {}
    for name in sorted(os.listdir(loc_dir)):
        if not name.endswith(".yml"):
            continue
        for line in read_loc_file(os.path.join(loc_dir, name)).splitlines():
            m = LOC_LINE.match(line)
            if m:
                loc.setdefault(m.group(2), (m.group(4), name))
    return loc


def resolve(keys, loc):
    """(present, joined_value, files, variants) for a list of loc keys.

    Conditional events resolve to several variants (.d.a, .d.b, ...). The joined
    value is what the lint scans; the variants are what length is measured on,
    so a four-way conditional is not scored as one 3600-character paragraph.
    """
    found = [loc[k] for k in keys if k in loc]
    if not found:
        return False, "", [], []
    return (True,
            "\n".join(v for v, _ in found),
            sorted({f for _, f in found}),
            [v for v, _ in found])


# The two functional escapes HOI4 reads out of loc values: the colour code and
# the inline sprite reference (`£texticon_foo`). Everything else above U+007F is
# text, and renders as `?` because the game reads these files as ANSI.
ALLOWED_NON_ASCII = "§£"


def non_ascii(value):
    return [c for c in value if ord(c) > 127 and c not in ALLOWED_NON_ASCII]


def unescaped_quotes(value):
    return len(re.findall(r'(?<!\\)"', value))


# --------------------------------------------------------------------------- #
# Row building
# --------------------------------------------------------------------------- #

def news_format(ev, title_val, desc_val, paragraphs):
    if ev["kind"] != "news_event":
        return "N/A"
    issues = []
    if "GetNewspaperHeader" not in title_val:
        issues.append("NO_HEADER")
    if not NEWS_DATELINE.search(desc_val):
        issues.append("NO_DATELINE")
    if len(desc_val) < 500:
        issues.append("TOO_SHORT")
    if paragraphs < 3:
        issues.append("FEW_PARAS")
    return ";".join(issues) if issues else "OK"


def build_row(ev, event_file, loc, refs=None):
    has_title, title_val, title_files, _ = resolve(ev["title"], loc)
    has_desc, desc_val, desc_files, desc_variants = resolve(ev["desc"], loc)

    option_keys = [k for names in ev["options"] for k in names]
    missing_opts = [k for k in option_keys if k not in loc]
    option_vals = "\n".join(loc[k][0] for k in option_keys if k in loc)

    body_text = "\n".join(x for x in (title_val, desc_val, option_vals) if x)
    # Score the longest variant, not the concatenation of all of them.
    longest = max(desc_variants, key=len) if desc_variants else ""
    paragraphs = longest.count("\\n\\n") + 1 if longest else 0

    flags = []
    if ev["hidden"]:
        flags.append("HIDDEN")
    if not ev["hidden"]:
        if not has_title:
            flags.append("NO_TITLE_LOC")
        if not has_desc:
            flags.append("NO_DESC_LOC")
        if missing_opts:
            flags.append("NO_OPTION_LOC")
    if non_ascii(body_text):
        flags.append("NON_ASCII")
    if any(c in body_text for c in SMART_PUNCT):
        flags.append("SMART_PUNCT")
    if unescaped_quotes(body_text):
        flags.append("UNESCAPED_QUOTE")
    if any(PLACEHOLDER.match(v) for v in (title_val, desc_val) if v):
        flags.append("PLACEHOLDER")
    if DOUBLED_WORD.search(longest):
        flags.append("DOUBLED_WORD")
    if title_val and title_val[0].islower():
        flags.append("LOWERCASE_START")
    if any(v.endswith(" ") for v in (title_val, desc_val) if v):
        flags.append("TRAILING_SPACE")
    if has_desc and 0 < len(longest) < 200:
        flags.append("THIN_DESC")
    if len(longest) > 400 and paragraphs == 1:
        flags.append("NO_PARA_BREAKS")
    if ev["major"] and ev["kind"] == "country_event":
        flags.append("MAJOR_BROADCAST")
    # Only `is_triggered_only` events need a fire site. Everything else carries a
    # trigger/mean_time_to_happen and is fired by the engine, so it is never dead.
    if ev["triggered_only"] and ev.get("fire_sites") == 0:
        flags.append("UNFIRED")

    kind_label = {
        "country_event": "Country", "news_event": "News", "state_event": "State",
        "unit_leader_event": "Leader", "operative_leader_event": "Operative",
    }[ev["kind"]]
    if ev["hidden"]:
        kind_label = "Hidden"

    return {
        "Event ID": ev["id"],
        "Event File": event_file,
        "Loc File": ", ".join(sorted(set(title_files + desc_files))) or "[NONE]",
        "Type": kind_label,
        "Fires For": ", ".join(sorted(ev["tags"])),
        "Options": str(len(ev["options"])),
        "Has Title": "TRUE" if has_title else "FALSE",
        "Has Description": "TRUE" if has_desc else "FALSE",
        "Picture": ev["picture"] or "[NONE]",
        "Desc Chars": str(len(longest)),
        "Paragraphs": str(paragraphs),
        "News Format": news_format(ev, title_val, longest, paragraphs),
        "Flags": ";".join(flags),
        "_sea": bool(SEA_KEYWORDS.search(body_text) or SEA_KEYWORDS.search(ev["id"] or "")),
    }


def collect_rows(event_files, loc, sea_only, refs=None):
    rows = []
    seen = set()
    for name in event_files:
        path = os.path.join(EVENT_DIR, name)
        if not os.path.exists(path):
            print("  ! missing event file: %s" % name, file=sys.stderr)
            continue
        text = read_loc_file(path)
        for kind, body in iter_event_definitions(text):
            ev = parse_event(kind, body)
            if not ev["id"]:
                continue
            key = (name, ev["id"])
            if key in seen:
                continue
            seen.add(key)
            if refs is not None:
                ev["fire_sites"] = refs.get(ev["id"], 0)
            row = build_row(ev, name, loc, refs)
            if sea_only and not row.pop("_sea"):
                continue
            row.pop("_sea", None)
            rows.append(row)
    rows.sort(key=lambda r: (r["Event File"],) + sort_key(r["Event ID"]))
    return rows


def sort_key(event_id):
    """Namespace then numeric index, tolerating ids that are not `ns.number`."""
    ns, _, idx = event_id.rpartition(".")
    return (ns or event_id, 0 if idx.isdigit() else 1, int(idx) if idx.isdigit() else 0, idx)


# --------------------------------------------------------------------------- #
# CSV round-tripping
# --------------------------------------------------------------------------- #

def load_existing(path):
    """(event file, event id) -> hand-written column values from a prior run."""
    if not os.path.exists(path):
        return {}
    kept = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            eid = (row.get("Event ID") or "").strip()
            if not re.match(r"^[A-Za-z0-9_]+\.\d+$", eid):
                continue  # header echo / footer junk from the hand-made sheet
            efile = (row.get("Event File") or "").strip()
            hand = {c: (row.get(c) or "").strip() for c in HAND_COLUMNS}
            kept[(efile, eid)] = hand
            kept.setdefault((None, eid), hand)  # pre-Event File CSVs
    return kept


def write_csv(path, rows, kept, do_triage=False):
    for row in rows:
        hand = kept.get((row["Event File"], row["Event ID"])) or kept.get((None, row["Event ID"])) or {}
        for col in HAND_COLUMNS:
            row[col] = hand.get(col, "")
        if not row["Completion"]:
            row["Completion"] = "FALSE"
        if do_triage:
            grade, priority, action = triage(row)
            row["Grade"] = row["Grade"] or grade
            row["Priority"] = row["Priority"] or priority
            row["Action"] = row["Action"] or action
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)



# --------------------------------------------------------------------------- #
# First-pass triage
# --------------------------------------------------------------------------- #

def triage(row):
    """(Grade, Priority, Action) suggested from the generated flags alone.

    A starting point for review, not a verdict - it only ever fills cells that
    are still empty, so anything a human has graded stays put.

    F missing text / D stub / C broken English / B polish / A ship as-is,
    and N/A for events no longer reachable in game.
    """
    flags = set(filter(None, row["Flags"].split(";")))
    news_bad = row["News Format"] not in ("OK", "N/A")

    if "UNFIRED" in flags:
        return "N/A", "P3", "Wire or cut"
    if "HIDDEN" in flags:
        return "A", "", "Keep"
    if flags & {"NO_TITLE_LOC", "NO_DESC_LOC", "NO_OPTION_LOC"}:
        return "F", "P1", "Write"
    if "UNESCAPED_QUOTE" in flags:
        return "B", "P1", "Polish"
    if "DOUBLED_WORD" in flags:
        return "C", "P2", "Rewrite"
    if "THIN_DESC" in flags:
        return "D", "P2", "Rewrite"
    if news_bad:
        return "C", "P2", "Rewrite"
    if flags & {"NON_ASCII", "SMART_PUNCT", "TRAILING_SPACE", "LOWERCASE_START", "PLACEHOLDER"}:
        return "B", "P2", "Polish"
    if "NO_PARA_BREAKS" in flags:
        return "B", "P3", "Polish"
    return "A", "P3", "Keep"


# --------------------------------------------------------------------------- #
# Lint
# --------------------------------------------------------------------------- #

def resolved_loc_files(loc):
    """Loc files the audited events actually land in, beyond the SEA_LOC_FILES list.

    SEA events reach into shared files (events_l_english, MAL_l_english, ROC_l_english_),
    so the lint follows them rather than trusting a hand-maintained list.
    """
    files = set()
    for event_files in THEATRES.values():
        for name in event_files:
            path = os.path.join(EVENT_DIR, name)
            if not os.path.exists(path):
                continue
            for kind, body in iter_event_definitions(read_loc_file(path)):
                ev = parse_event(kind, body)
                keys = ev["title"] + ev["desc"] + [k for n in ev["options"] for k in n]
                files.update(loc[k][1] for k in keys if k in loc)
    return sorted(files)


def check(extra_files=()):
    names = []
    for name in list(SEA_LOC_FILES) + list(extra_files):
        if name not in names and os.path.exists(os.path.join(LOC_DIR, name)):
            names.append(name)

    problems = []
    for name in names:
        path = os.path.join(LOC_DIR, name)
        for lineno, line in enumerate(read_loc_file(path).splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("l_english"):
                continue
            m = LOC_LINE.match(line)
            if not m:
                problems.append((name, lineno, "MALFORMED", stripped[:90]))
                continue
            value = m.group(4)
            if unescaped_quotes(value):
                problems.append((name, lineno, "UNESCAPED_QUOTE", stripped[:90]))
            bad = non_ascii(value) + non_ascii(m.group(2))
            if bad:
                problems.append((name, lineno, "NON_ASCII " + "".join(sorted(set(bad))), stripped[:90]))

    if problems:
        by_kind = {}
        for name, lineno, kind, snippet in problems:
            by_kind.setdefault(kind.split()[0], []).append((name, lineno, kind, snippet))
        for kind in sorted(by_kind):
            hits = by_kind[kind]
            print("%s: %d" % (kind, len(hits)))
            for name, lineno, full, snippet in hits[:20]:
                print("  %s:%d  %s" % (name, lineno, snippet))
            if len(hits) > 20:
                print("  ... and %d more" % (len(hits) - 20))
        print("\n%d problem(s) across %d file(s)." % (len(problems), len(names)))
        return 1
    print("OK - %d SEA loc file(s) clean." % len(names))
    return 0


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="lint SEA loc files, exit 1 on failure")
    ap.add_argument("--all", action="store_true",
                    help="with --check, also lint the shared loc files SEA events reach into "
                         "(reports long-standing violations outside this project's scope)")
    ap.add_argument("--summary", action="store_true", help="print counts, write no CSVs")
    ap.add_argument("--triage", action="store_true",
                    help="fill empty Grade/Priority/Action cells from the flags; never overwrites")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()

    os.chdir(args.root)
    if not os.path.isdir(EVENT_DIR):
        sys.exit("error: run from the repo root - %s not found" % EVENT_DIR)

    loc = load_loc(LOC_DIR)
    refs = None

    if args.check:
        sys.exit(check(resolved_loc_files(loc) if args.all else ()))
    refs = build_reference_index(collect_defined_ids())
    grand = 0
    for csv_name, event_files in THEATRES.items():
        rows = collect_rows(event_files, loc, csv_name in SEA_ONLY, refs)
        grand += len(rows)
        flagged = sum(1 for r in rows if r["Flags"])
        if args.summary:
            print("%-42s %4d events  %4d flagged" % (csv_name, len(rows), flagged))
            continue
        kept = load_existing(csv_name)
        write_csv(csv_name, rows, kept, args.triage)
        carried = sum(1 for r in rows if any(r.get(c) for c in HAND_COLUMNS if c != "Completion"))
        print("%-42s %4d events  %4d flagged  %4d hand-annotated carried over"
              % (csv_name, len(rows), flagged, carried))
    print("%-42s %4d events" % ("TOTAL", grand))


if __name__ == "__main__":
    main()
