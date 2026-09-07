#!/usr/bin/env python3
"""Static integration checks for the doctrine and NSB tank reworks.

Pass ``--doctrine-self-test`` to exercise the bounded parser and its negative
fixtures without changing the working tree.
"""

from __future__ import annotations

import re
import sys
import csv
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree


if "--help" in sys.argv:
    print(
        "Usage: python3 tools/validate_military_reworks.py "
        "[--doctrine-self-test] [--tank-self-test] [--tank-balance-report] "
        "[--tank-module-balance-report] [--tank-envelope-report]\n"
        "Default validation reads the tracked mod files and exits 0 on success or 1 "
        "on contract failures.\n"
        "--doctrine-self-test and --tank-self-test add in-memory negative fixtures.\n"
        "--tank-balance-report additionally reads the untracked workbook at the repository "
        "root and prints the reviewed scope; the tracked manifest is "
        "LogDocs/Tank_Designer/Balance_Target_Manifest.md."
    )
    sys.exit(0)


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "Cold War Iron Curtain"
TECH_DIR = MOD / "common/technologies"
MODULE_FILE = MOD / "common/units/equipment/modules/00_tank_modules.txt"
CHASSIS_FILE = MOD / "common/units/equipment/tank_chassis.txt"
MECHANIZED_FILE = MOD / "common/units/equipment/mechanized.txt"
# The APC designer family reuses the mechanized_equipment archetype so every
# existing mechanized consumer resolves designer personnel carriers unchanged.
# tier -> (legacy Light Mech row it replaces, hull technology, introduction year)
APC_HULL_ROWS = {
    0: ("mechanized_equipment_3", "nsb_apc_hulls0", 1947),
    1: ("mechanized_equipment_4", "nsb_apc_hulls1", 1950),
    2: ("mechanized_equipment_5", "nsb_apc_hulls2", 1960),
    3: ("mechanized_equipment_6", "nsb_apc_hulls3", 1965),
    4: ("mechanized_equipment_7", "nsb_apc_hulls4", 1975),
    5: ("mechanized_equipment_8", "nsb_apc_hulls5", 1985),
    6: ("mechanized_equipment_9", "nsb_apc_hulls6", 1995),
    7: ("mechanized_equipment_10", "nsb_apc_hulls7", 2005),
}
# The 2023 balance workbook is frozen and predates the APC designer family, so
# its module sheets can never carry these rows. They are authored values kept in
# script only, and the module balance report reports them as an explicit
# exemption instead of silently widening workbook coverage.
APC_SUPERSTRUCTURE_MODULES = (
    "apc_open_troop_bay",
    "apc_troop_compartment",
    "apc_frontal_engine_layout",
)
APC_ARMAMENT_MODULES = (
    "apc_firing_ports",
    "apc_pintle_mg",
    "apc_cupola_hmg",
    "apc_remote_weapon_station",
)
TANK_SPECIAL_SLOT_CATEGORIES = {
    1: {"tank_ammo_kinetic", "tank_ammo_chemical", "tank_ammo_missile", "tank_ammo_he"},
    2: {"tank_ammo_kinetic", "tank_ammo_chemical", "tank_ammo_missile", "tank_ammo_he"},
    3: {"tank_fcs_aiming"},
    4: {"tank_fcs_optics"},
    5: {"tank_fcs_computer", "tank_fcs_radar"},
    6: {"tank_loader_manual_assist", "tank_loader_autoloader", "tank_loader_artillery"},
    7: {"tank_protection_passive", "tank_protection_reactive"},
    8: {"tank_protection_passive", "tank_protection_reactive", "tank_protection_active"},
    9: {"tank_survivability", "tank_mobility_auxiliary", "tank_smoke"},
    10: {"tank_secondary_turret", "tank_survivability", "tank_mobility_auxiliary", "tank_smoke"},
}
AI_FILE = MOD / "common/ai_equipment/generic_tank.txt"
ENUM_FILE = MOD / "common/script_enums.txt"
VARIANT_EFFECT_FILE = MOD / "common/scripted_effects/CWIC_tank_designer_effects.txt"
FOCUS_EFFECT_FILE = MOD / "common/scripted_effects/CWIC_tank_focus_effects.txt"
NATIONAL_EFFECT_FILE = MOD / "common/scripted_effects/CWIC_national_tank_presets.txt"
NATIONAL_MANIFEST_FILE = ROOT / "LogDocs/Tank_Designer/National_Tank_Preset_Manifest.json"
NATIONAL_PRESETS = json.loads(NATIONAL_MANIFEST_FILE.read_text(encoding="utf-8"))["presets"]
FOCUS_FILES = (
    MOD / "common/national_focus/60s_Generic.txt",
    MOD / "common/national_focus/GRE_military_shared_1950s.txt",
    MOD / "common/national_focus/50s_FIN.txt",
)
TANK_ROLE_FILE = MOD / "common/units/need_for_tank_roles.txt"
TANK_ICON_FILE = MOD / "interface/cwic_tank_rework_icons.gfx"
TANK_LOC_FILE = MOD / "localisation/english/tank_modules_l_english.yml"
BALANCE_MANIFEST_FILE = ROOT / "LogDocs/Tank_Designer/Balance_Target_Manifest.md"
BALANCE_WORKBOOK_FILE = ROOT / "LogDocs/Tank_Designer/2023 - CWIC Tank Rework Balance.xlsx"
BALANCE_CSV_FILE = ROOT / "LogDocs/Tank_Designer/2023 - CWIC Tank Rework Balance(Total Balance Sheet Minimal).csv"
BALANCE_METRICS = (
    ("reliability", "C", True),
    ("hardness", "D", True),
    ("hard_attack", "E", False),
    ("soft_attack", "F", False),
    ("breakthrough", "G", False),
    ("defense", "H", False),
    ("armor", "I", False),
    ("piercing", "J", False),
    ("speed", "K", False),
    ("supply", "L", False),
    ("fuel_usage", "M", False),
    ("production_cost", "N", False),
)
# The two module tables deliberately retain their original stat columns.  The
# operation column added by Tier 3 is a compact audit trail for fields such as
# reliability, whose old percentage column cannot distinguish add_stats from
# multiply_stats by itself.
MODULE_BALANCE_COLUMNS = {
    "reliability": ("I", 8, None, None),
    "hardness": ("J", 9, None, None),
    "hard_attack": ("K", 10, "L", 11),
    "soft_attack": ("M", 12, "N", 13),
    "breakthrough": ("O", 14, "P", 15),
    "defense": ("Q", 16, "R", 17),
    "armor_value": ("S", 18, "T", 19),
    "ap_attack": ("U", 20, "V", 21),
    "maximum_speed": ("W", 22, "X", 23),
    "reconnaissance": ("Y", 24, "Z", 25),
    "entrenchment": ("AA", 26, None, None),
    "supply_consumption": ("AB", 27, "AC", 28),
    "fuel_consumption": ("AD", 29, "AE", 30),
    "air_attack": ("AF", 31, "AG", 32),
    "build_cost_ic": ("AH", 33, "AI", 34),
}
MODULE_FIELD_ALIASES = {
    "recon": "reconnaissance",
    "armor": "armor_value",
}
MODULE_RESOURCE_COLUMNS = {
    "electricity": ("AK", 36),
    "steel": ("AL", 37),
    "aluminium": ("AM", 38),
    "tungsten": ("AN", 39),
    "nuclear_materials": ("AO", 40),
}
MODULE_OPERATION_COLUMN = ("AP", 41)
MODULE_DISMANTLE_COLUMN = ("AJ", 35)
MODULE_SCRIPT_FIELDS = set(MODULE_BALANCE_COLUMNS) | set(MODULE_RESOURCE_COLUMNS) | {
    "dismantle_cost_ic",
}
MODULE_EXPLICIT_EXCLUSIONS = {
    "parent": "inheritance is retained in script and reported separately",
    "category": "designer eligibility metadata, not a numeric balance column",
    "allow_equipment_type": "designer eligibility metadata",
    "forbid_equipment_type": "designer eligibility metadata",
    "forbid_equipment_type_exact_match": "designer eligibility metadata",
    "allowed_module_categories": "designer eligibility metadata",
    "can_convert_from": "conversion metadata; convert_cost_ic is not a balance stat",
    "xp_cost": "designer XP policy is frozen by the manual",
    "abbreviation": "display metadata, checked by the existing contract",
    "sfx": "display metadata, outside the balance workbook",
    "icon": "display metadata, outside the balance workbook",
}
# These two cells are prose notes inherited from the source workbook's radar
# draft.  They occupy a percentage column, but are not numeric balance data;
# keep them as explicit annotations rather than silently treating arbitrary
# text as valid.
MODULE_SOURCE_ANNOTATIONS = {
    "Нужно ли добавить топливо в запас?",
    "????? ?? ???????? ??????? ? ??????",
}
SCRIPT_OWNED_MODULES = {
    "conventional_turret",
    "cwic_coaxial_mg",
    "cwic_hull_mg",
    "cwic_secondary_autocannon",
    "cwic_secondary_hmg",
    "external_gun",
    "fixed_superstructure",
    "flamethrower",
    "heavy_fixed_superstructure",
    "heavy_open_gun",
    "light_lp_turret",
    "light_turret",
    "lp_turret",
    "medium_fixed_superstructure",
    "medium_open_gun",
    "open_gun",
    "oscillating_turret",
    "pintle_turret",
    "tank_anti_air_cannon",
    "tank_anti_air_cannon_2",
    "tank_anti_air_cannon_3",
    "tank_gasoline_engine",
}
OOB_DIR = MOD / "history/units"
HISTORY_DIR = MOD / "history/countries"

SUPPORTED_ROLES = ("aa", "artillery", "destroyer", "flame")
FAMILY_TIERS = {"light": 10, "medium": 10, "heavy": 5}
OOB_TANK_PATTERN = re.compile(
    r"\b(?:light|medium|heavy)_tank"
    r"(?:_(?:aa|artillery|destroyer|flame))?_chassis_[0-9]+\b"
)
STARTING_VARIANT_EFFECT = "cwic_create_starting_tank_variants = yes"
# Manufacturer bloc tags sell tanks but never load an OOB of their own.
MANUFACTURER_BLOC_TAGS = {"CAP", "CUM"}
# `producer` on a stockpile/production request and `creator` on a forced
# variant both name the tag whose designer built the tank.
FOREIGN_CREATOR_PATTERN = re.compile(r'\b(?:producer|creator)\s*=\s*"?([A-Z]{3})"?')
REQUIRED_VARIANT_SLOTS = {
    "main_armament_slot",
    "turret_type_slot",
    "suspension_type_slot",
    "armor_type_slot",
    "engine_type_slot",
}
SECONDARY_MODULES = {
    "cwic_coaxial_mg": "nsb_iw_armored_vehicles",
    "cwic_hull_mg": "nsb_iw_armored_vehicles",
    "cwic_secondary_hmg": "nsb_iw_armored_vehicles",
    "cwic_secondary_autocannon": "nsb_aiming_devices2",
}
SECONDARY_ICON_PATHS = {
    "cwic_coaxial_mg": "gfx/interface/equipmentdesigner/tanks/Modules/Other Modules/LMG.png",
    "cwic_hull_mg": "gfx/interface/equipmentdesigner/tanks/Modules/Other Modules/LMG.png",
    "cwic_secondary_hmg": "gfx/interface/equipmentdesigner/tanks/Modules/Other Modules/HMG.png",
    "cwic_secondary_autocannon": "gfx/interface/equipmentdesigner/tanks/Modules/SPAAG/AFV Autocannons/Light autocannon 1960.png",
}
FLAME_TECH_GRANTS = {
    "nsb_iw_armored_vehicles": {
        "light_tank_flame_chassis_0",
        "medium_tank_flame_chassis_0",
        "heavy_tank_flame_chassis_0",
    },
    **{
        f"nsb_light_tanks{tier}": {f"light_tank_flame_chassis_{tier + 1}"}
        for tier in range(9)
    },
    **{
        f"nsb_main_battle_tanks{tier}": {f"medium_tank_flame_chassis_{tier + 1}"}
        for tier in range(9)
    },
    **{
        f"nsb_heavy_tanks{tier}": {f"heavy_tank_flame_chassis_{tier + 1}"}
        for tier in range(4)
    },
}
EXPORT_VARIANTS = {
    "CWIC Export Main Battle Tank 1950": "medium_tank_chassis_3",
    "CWIC Export Main Battle Tank 1944": "medium_tank_chassis_2",
    "CWIC Export Light Tank 1942": "light_tank_chassis_1",
    "CWIC Export Light Tank 1944": "light_tank_chassis_2",
    "CWIC Export Heavy Tank 1944": "heavy_tank_chassis_2",
}
BOOKMARK_VARIANT_NAMES = {
    "heavy_tank_artillery_chassis_1": "Standard Heavy SPG 1942",
    "heavy_tank_artillery_chassis_3": "Standard Heavy SPG 1950",
    "heavy_tank_chassis_1": "Standard Heavy Tank 1942",
    "heavy_tank_chassis_2": "Standard Heavy Tank 1944",
    "heavy_tank_chassis_3": "Standard Heavy Tank 1950",
    "heavy_tank_chassis_4": "Standard Heavy Tank 1955",
    "light_tank_aa_chassis_1": "Standard Light SPAA 1942",
    "light_tank_aa_chassis_2": "Standard Light SPAA 1944",
    "light_tank_aa_chassis_3": "Standard Light SPAA 1950",
    "light_tank_artillery_chassis_1": "Standard Light SPG 1942",
    "light_tank_artillery_chassis_2": "Standard Light SPG 1944",
    "light_tank_artillery_chassis_3": "Standard Light SPG 1950",
    "light_tank_chassis_1": "Standard Light Tank 1942",
    "light_tank_chassis_2": "Standard Light Tank 1944",
    "light_tank_chassis_3": "Standard Light Tank 1950",
    "light_tank_chassis_4": "Standard Light Tank 1960",
    "light_tank_chassis_5": "Standard Light Tank 1970",
    "medium_tank_artillery_chassis_1": "Standard Main Battle SPG 1942",
    "medium_tank_artillery_chassis_2": "Standard Main Battle SPG 1944",
    "medium_tank_artillery_chassis_3": "Standard Main Battle SPG 1950",
    "medium_tank_chassis_0": "Standard Main Battle Tank 1939",
    "medium_tank_chassis_1": "Standard Main Battle Tank 1942",
    "medium_tank_chassis_2": "Standard Main Battle Tank 1944",
    "medium_tank_chassis_3": "Standard Main Battle Tank 1950",
    "medium_tank_chassis_4": "Standard Main Battle Tank 1960",
    "medium_tank_chassis_5": "Standard Main Battle Tank 1970",
    "medium_tank_chassis_6": "Standard Main Battle Tank 1980",
    "medium_tank_destroyer_chassis_1": "Standard Main Battle Tank Destroyer 1942",
    "medium_tank_destroyer_chassis_2": "Standard Main Battle Tank Destroyer 1944",
    "medium_tank_destroyer_chassis_3": "Standard Main Battle Tank Destroyer 1950",
}
BOOKMARK_VARIANT_TECHS = {
    "heavy_tank_artillery_chassis_1": "nsb_heavy_tanks0",
    "heavy_tank_artillery_chassis_3": "nsb_heavy_tanks2",
    "heavy_tank_chassis_1": "nsb_heavy_tanks0",
    "heavy_tank_chassis_2": "nsb_heavy_tanks1",
    "heavy_tank_chassis_3": "nsb_heavy_tanks2",
    "heavy_tank_chassis_4": "nsb_heavy_tanks3",
    "light_tank_aa_chassis_1": "nsb_light_tanks0",
    "light_tank_aa_chassis_2": "nsb_light_tanks1",
    "light_tank_aa_chassis_3": "nsb_light_tanks2",
    "light_tank_artillery_chassis_1": "nsb_light_tanks0",
    "light_tank_artillery_chassis_2": "nsb_light_tanks1",
    "light_tank_artillery_chassis_3": "nsb_light_tanks2",
    "light_tank_chassis_1": "nsb_light_tanks0",
    "light_tank_chassis_2": "nsb_light_tanks1",
    "light_tank_chassis_3": "nsb_light_tanks2",
    "light_tank_chassis_4": "nsb_light_tanks3",
    "light_tank_chassis_5": "nsb_light_tanks4",
    "medium_tank_artillery_chassis_1": "nsb_main_battle_tanks0",
    "medium_tank_artillery_chassis_2": "nsb_main_battle_tanks1",
    "medium_tank_artillery_chassis_3": "nsb_main_battle_tanks2",
    "medium_tank_chassis_0": "nsb_iw_armored_vehicles",
    "medium_tank_chassis_1": "nsb_main_battle_tanks0",
    "medium_tank_chassis_2": "nsb_main_battle_tanks1",
    "medium_tank_chassis_3": "nsb_main_battle_tanks2",
    "medium_tank_chassis_4": "nsb_main_battle_tanks3",
    "medium_tank_chassis_5": "nsb_main_battle_tanks4",
    "medium_tank_chassis_6": "nsb_main_battle_tanks5",
    "medium_tank_destroyer_chassis_1": "nsb_main_battle_tanks0",
    "medium_tank_destroyer_chassis_2": "nsb_main_battle_tanks1",
    "medium_tank_destroyer_chassis_3": "nsb_main_battle_tanks2",
}
UNSUPPORTED_IDS = {
    "light_tank_rocket_chassis",
    "medium_tank_rocket_chassis",
    "heavy_tank_rocket_chassis",
    "medium_tank_heavy_artillery_chassis",
    "amphibious_tank_chassis",
    "modern_tank_chassis",
    "super_heavy_tank_chassis",
    "amphibious_mechanized_infantry",
    "category_amphibious_tanks",
}


def bookmark_variant_name(equipment_type: str, producer: str) -> str:
    for preset in NATIONAL_PRESETS:
        if (preset["type"], preset["producer"]) == (equipment_type, producer):
            return preset["name"]
    return BOOKMARK_VARIANT_NAMES[equipment_type]


def oob_variant_producer(block: str, default_tag: str) -> str:
    match = re.search(r'\b(?:owner|producer|creator)\s*=\s*"?([A-Z]{3})"?', code_only(block))
    return match[1] if match else default_tag

errors: list[str] = []

LAND_MANIFEST_FILE = ROOT / "LogDocs/Doctrine_Rework/Doctrine_Cell_Manifest.md"
REVIEWED_LAND_MANIFEST_SHA256 = "d0adb7a947404256e43fe7a28a08b9d31a94a114a2252c76fafb11b61ccf201e"
DOCTRINE_CONTENT_SHA256 = {
    "land_doctrine.txt": "30f7b88844a779da077ddbea0cb2f5bf3ab6f47c5d21db9167b59dbe40941fea",
    "air_doctrine.txt": "60805d1cddae8deb5e2827501dfcb1186708f2b1045702c72dff4a6bab78f89c",
    "naval_doctrine.txt": "81b983873396a3dd108c85184163beaf2efdb02f2ff144904d7d4c1ed420d085",
}
EXPECTED_DOCTRINE_COUNTS = {"land_doctrine.txt": 528, "air_doctrine.txt": 73, "naval_doctrine.txt": 45}
LAND_ROOTS = (
    "cw_nato_1940s_integrated_arms_reorganization",
    "cw_france_1940s_doctrine_header",
    "cw_israel_1940s_doctrine_header",
    "cw_warsaw_1940s_doctrine_header",
    "cw_prc_1940s_doctrine_header",
    "cw_yugo_1940s_doctrine_header",
    "cw_himalayan_1960s_doctrine_header",
    "cw_non_aligned_1940s_doctrine_header",
    "cw_iran_1980s_doctrine_header",
    "cw_ins_1940s_doctrine_header",
    "cw_islamist_alt_ins_1990s_doctrine_header",
)
LAND_ROW_Y = {1940: 172, 1950: 790, 1960: 1420, 1970: 2050, 1980: 2680, 1990: 3310}
LEDGER_FOLDERS = {
    "old_land_doctrine_folder": "army",
    "old_naval_doctrine_folder": "navy",
    "old_air_doctrine_folder": "air",
}


class ScriptParseError(ValueError):
    """A bounded Clausewitz block could not be parsed safely."""


def strip_script_comments(value: str) -> str:
    """Remove comments while preserving quoted strings and line structure."""
    result: list[str] = []
    quoted = False
    escaped = False
    comment = False
    for character in value:
        if comment:
            if character == "\n":
                comment = False
                result.append(character)
            continue
        if quoted:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
            result.append(character)
        elif character == "#":
            comment = True
        else:
            result.append(character)
    return "".join(result)


def balanced_end(value: str, opening: int, label: str) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(value)):
        character = value[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                raise ScriptParseError(f"negative brace depth in {label}")
            if depth == 0:
                return index
    raise ScriptParseError(f"unbalanced block in {label}")


def top_level_ranges(block: str, label: str) -> list[tuple[str, int, int, str]]:
    """Return direct child blocks, including inline blocks, from a balanced block."""
    value = strip_script_comments(block)
    opening = value.find("{")
    if opening < 0:
        raise ScriptParseError(f"missing opening brace in {label}")
    ending = balanced_end(value, opening, label)
    result: list[tuple[str, int, int, str]] = []
    index = opening + 1
    depth = 0
    quoted = False
    escaped = False
    while index < ending:
        character = value[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            index += 1
            continue
        if character == '"':
            quoted = True
            index += 1
            continue
        if depth == 0:
            match = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*\{", value[index:ending])
            if match:
                name = match.group(1)
                start = index + match.start(1)
                child_opening = value.find("{", index + match.start(), index + match.end())
                child_ending = balanced_end(value, child_opening, f"{label}.{name}")
                result.append((name, start, child_ending, value[start : child_ending + 1]))
                index = child_ending + 1
                continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                raise ScriptParseError(f"negative child brace depth in {label}")
        index += 1
    if depth:
        raise ScriptParseError(f"unbalanced child block in {label}")
    return result


def top_level_named_blocks(block: str, key: str, label: str = "block") -> list[str]:
    return [child for name, _, _, child in top_level_ranges(block, label) if name == key]


def strict_top_level_blocks(value: str, root_name: str, label: str) -> list[tuple[str, str]]:
    code = strip_script_comments(value)
    matches = list(re.finditer(rf"(?m)^\s*{re.escape(root_name)}\s*=\s*\{{", code))
    if len(matches) != 1:
        raise ScriptParseError(f"expected one {root_name} block in {label}, found {len(matches)}")
    match = matches[0]
    opening = code.find("{", match.start(), match.end())
    ending = balanced_end(code, opening, label)
    root = code[match.start() : ending + 1]
    result = [(name, child) for name, _, _, child in top_level_ranges(root, label)]
    names = [name for name, _ in result]
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        raise ScriptParseError(f"duplicate top-level IDs in {label}: {duplicates}")
    return result


def key_blocks(value: str, key: str, label: str) -> list[str]:
    code = strip_script_comments(value)
    result = []
    for match in re.finditer(rf"(?m)^\s*{re.escape(key)}\s*=\s*\{{", code):
        opening = code.find("{", match.start(), match.end())
        ending = balanced_end(code, opening, f"{label}.{key}")
        result.append(code[match.start() : ending + 1])
    return result


def top_level_values(block: str, key: str) -> list[str]:
    value = strip_script_comments(block)
    opening = value.find("{")
    if opening < 0:
        raise ScriptParseError(f"missing opening brace while reading {key}")
    ending = balanced_end(value, opening, key)
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(key)}\s*=\s*([A-Za-z0-9_.-]+)")
    result: list[str] = []
    index = opening + 1
    depth = 0
    quoted = False
    escaped = False
    while index < ending:
        character = value[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            index += 1
            continue
        if character == '"':
            quoted = True
            index += 1
            continue
        if depth == 0:
            match = pattern.match(value, index, ending)
            if match:
                result.append(match.group(1))
                index = match.end()
                continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
        index += 1
    return result


def doctrine_content_digest(blocks: list[tuple[str, str]]) -> str:
    canonical: list[str] = []
    for name, block in blocks:
        code = strip_script_comments(block)
        for child_name, start, ending, _ in reversed(top_level_ranges(code, name)):
            if child_name == "allow":
                code = code[:start] + code[ending + 1 :]
        canonical.append(name + "=" + re.sub(r"\s+", " ", code).strip())
    return sha256("\n".join(sorted(canonical)).encode("utf-8")).hexdigest()


def read_land_manifest() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    value = text(LAND_MANIFEST_FILE)
    for line in value.splitlines():
        if not line.startswith("| ") or line.startswith("| GUI") or line.startswith("| ---"):
            continue
        fields = [field.strip() for field in line.strip("|").split("|")]
        if len(fields) != 6:
            fail(f"malformed land cell manifest row: {line}")
            continue
        x, decade, header, nodes, terminal, parent = fields
        try:
            row = {
                "x": int(x),
                "decade": int(decade),
                "header": header.strip("`"),
                "nodes": int(nodes),
                "terminal": terminal.strip("`"),
                "parent": None if parent.startswith("**") else parent.strip("`"),
            }
        except ValueError:
            fail(f"malformed land cell manifest row: {line}")
            continue
        rows.append(row)
    canonical = "\n".join(
        "|".join(
            (
                str(row["x"]),
                str(row["decade"]),
                str(row["header"]),
                str(row["nodes"]),
                str(row["terminal"]),
                "ROOT" if row["parent"] is None else str(row["parent"]),
            )
        )
        for row in rows
    ) + "\n"
    if sha256(canonical.encode("utf-8")).hexdigest() != REVIEWED_LAND_MANIFEST_SHA256:
        fail("reviewed land cell manifest does not match its implementation contract")
    return rows


def named_gui_blocks(value: str, kind: str, wanted: str | None, label: str) -> list[str]:
    code = strip_script_comments(value)
    result: list[str] = []
    for match in re.finditer(rf"(?m)^\s*{re.escape(kind)}\s*=\s*\{{", code):
        opening = code.find("{", match.start(), match.end())
        ending = balanced_end(code, opening, f"{label}.{kind}")
        block = code[match.start() : ending + 1]
        name = re.search(r'\bname\s*=\s*"([^"]+)"', block)
        if name and (wanted is None or name.group(1) == wanted):
            result.append(block)
    return result


def parse_allow_signature(allow: str, technology: str) -> tuple[list[str], list[tuple[str, str]]]:
    children = top_level_ranges(allow, f"{technology}.allow")
    if any(name in {"OR", "AND"} for name, _, _, _ in children):
        fail(f"{technology} allow prerequisite is hidden under OR/AND")
    direct_positive = top_level_values(allow, "has_tech")
    direct_researching = top_level_values(allow, "is_researching_technology")
    if direct_researching:
        fail(f"{technology} allow has a direct research-state clause")
    clauses: list[tuple[str, str]] = []
    for name, _, _, child in children:
        if name != "NOT":
            if name not in {"allow"}:
                fail(f"{technology} allow contains unsupported block {name}")
            continue
        child_has = top_level_values(child, "has_tech")
        child_researching = top_level_values(child, "is_researching_technology")
        dates = re.findall(r"\bdate\s*<\s*([0-9]+\.[0-9]+\.[0-9]+)", child)
        if child_has and not child_researching and not dates and len(child_has) == 1:
            clauses.append(("has", child_has[0]))
        elif child_researching and not child_has and not dates and len(child_researching) == 1:
            clauses.append(("researching", child_researching[0]))
        elif dates and not child_has and not child_researching and len(dates) == 1:
            clauses.append(("date", dates[0]))
        else:
            fail(f"{technology} allow contains malformed NOT clause")
    if re.search(r"\bdate\s*[<>]=?", allow) and not re.search(
        r"\bdate\s*<\s*[0-9]+\.[0-9]+\.[0-9]+", allow
    ):
        fail(f"{technology} allow has an unsupported date boundary")
    return direct_positive, clauses


def fixture_allow_signature(allow: str) -> tuple[list[str], list[tuple[str, str]]]:
    """Parse an allow fixture without adding failures to the real validation run."""
    children = top_level_ranges(allow, "fixture.allow")
    if any(name in {"OR", "AND"} for name, _, _, _ in children):
        raise ScriptParseError("allow contains OR/AND")
    positive = top_level_values(allow, "has_tech")
    clauses: list[tuple[str, str]] = []
    for name, _, _, child in children:
        if name != "NOT":
            raise ScriptParseError(f"unsupported allow block {name}")
        child_has = top_level_values(child, "has_tech")
        child_researching = top_level_values(child, "is_researching_technology")
        dates = re.findall(r"\bdate\s*<\s*([0-9]+\.[0-9]+\.[0-9]+)", child)
        if child_has and not child_researching and not dates and len(child_has) == 1:
            clauses.append(("has", child_has[0]))
        elif child_researching and not child_has and not dates and len(child_researching) == 1:
            clauses.append(("researching", child_researching[0]))
        elif dates and not child_has and not child_researching and len(dates) == 1:
            clauses.append(("date", dates[0]))
        else:
            raise ScriptParseError("malformed NOT clause")
    if re.search(r"\bdate\s*[<>]=?", allow) and not re.search(
        r"\bdate\s*<\s*[0-9]+\.[0-9]+\.[0-9]+", allow
    ):
        raise ScriptParseError("unsupported date boundary")
    return positive, clauses


def fixture_graph_check(
    edges: dict[str, list[str]], anchors: list[str], all_nodes: set[str]
) -> None:
    owners: dict[str, str] = {}
    state: dict[str, int] = {}

    def visit_graph(node: str) -> None:
        if state.get(node, 0) == 1:
            raise ScriptParseError(f"cycle at {node}")
        if state.get(node, 0) == 2:
            return
        state[node] = 1
        for target in edges.get(node, []):
            if target not in all_nodes:
                raise ScriptParseError(f"undefined target {target}")
            visit_graph(target)
        state[node] = 2

    for node in all_nodes:
        visit_graph(node)

    def visit_cell(cell: str, node: str, active: set[str]) -> None:
        if node in active:
            raise ScriptParseError(f"cycle at {node}")
        if node in owners:
            if owners[node] != cell:
                raise ScriptParseError(f"duplicate ownership of {node}")
            return
        owners[node] = cell
        active.add(node)
        for target in edges.get(node, []):
            visit_cell(cell, target, active)
        active.remove(node)

    for anchor in anchors:
        if anchor not in all_nodes:
            raise ScriptParseError(f"orphan anchor {anchor}")
        visit_cell(anchor, anchor, set())
    if set(owners) != all_nodes:
        raise ScriptParseError(f"orphan nodes: {sorted(all_nodes - set(owners))}")
    for source, targets in edges.items():
        for target in targets:
            if owners.get(source) != owners.get(target):
                raise ScriptParseError(f"cross-cell edge {source} -> {target}")


def run_doctrine_negative_fixtures() -> None:
    def require_rejection(label: str, function) -> None:
        try:
            function()
        except (AssertionError, ScriptParseError):
            return
        fail(f"doctrine negative fixture was accepted: {label}")

    def assert_one_allow_fixture() -> None:
        assert len(top_level_named_blocks("tech = { allow = { has_tech = root } allow = { has_tech = root } }", "allow")) == 1

    def assert_allow_signature(value: str, positive: list[str], clauses: list[tuple[str, str]]) -> None:
        assert fixture_allow_signature(value) == (positive, clauses)

    def assert_without_test_flag(value: str) -> None:
        assert "X_TESt" not in strip_script_comments(value)

    accepted = strict_top_level_blocks(
        "technologies = { root = { path = { leads_to_tech = child } } child = { allow  = { has_tech = root NOT = { date < 1950.1.1 } } } }",
        "technologies",
        "two-space fixture",
    )
    accepted_map = dict(accepted)
    assert top_level_values(top_level_named_blocks(accepted_map["root"], "path")[0], "leads_to_tech") == ["child"]
    assert fixture_allow_signature(top_level_named_blocks(accepted_map["child"], "allow")[0]) == (
        ["root"],
        [("date", "1950.1.1")],
    )
    inline = strict_top_level_blocks(
        "technologies = { root = { path = { leads_to_tech = child } } child = { allow = { has_tech = root } } }",
        "technologies",
        "inline fixture",
    )
    assert fixture_allow_signature(top_level_named_blocks(dict(inline)["child"], "allow")[0]) == (["root"], [])
    commented = strict_top_level_blocks(
        "technologies = { root = { # path = { leads_to_tech = ghost }\n } }",
        "technologies",
        "comment fixture",
    )
    assert not top_level_named_blocks(dict(commented)["root"], "path")

    require_rejection(
        "unbalanced block",
        lambda: strict_top_level_blocks("technologies = { root = {", "technologies", "unbalanced fixture"),
    )
    require_rejection(
        "missing prerequisite",
        lambda: assert_allow_signature("allow = { NOT = { date < 1950.1.1 } }", ["root"], [("date", "1950.1.1")]),
    )
    require_rejection(
        "wrong prerequisite",
        lambda: assert_allow_signature("allow = { has_tech = wrong }", ["root"], []),
    )
    require_rejection(
        "negated prerequisite",
        lambda: assert_allow_signature("allow = { NOT = { has_tech = root } }", ["root"], []),
    )
    require_rejection(
        "OR bypass",
        lambda: fixture_allow_signature("allow = { OR = { has_tech = root has_tech = sibling } }"),
    )
    require_rejection(
        "wrong date boundary",
        lambda: fixture_allow_signature("allow = { NOT = { date > 1950.1.1 } }"),
    )
    require_rejection(
        "duplicate allow",
        lambda: assert_one_allow_fixture(),
    )
    require_rejection(
        "missing reciprocal exclusion",
        lambda: assert_allow_signature(
            "allow = { NOT = { has_tech = rival } }",
            ["root"],
            [("has", "rival"), ("researching", "rival")],
        ),
    )
    require_rejection(
        "restored test flag",
        lambda: assert_without_test_flag("allow = { has_country_flag = X_TESt }"),
    )
    require_rejection(
        "cross-cell edge",
        lambda: fixture_graph_check({"a": ["b"], "b": []}, ["a", "b"], {"a", "b"}),
    )
    require_rejection(
        "cycle",
        lambda: fixture_graph_check({"a": ["b"], "b": ["a"]}, ["a"], {"a", "b"}),
    )
    require_rejection(
        "orphan",
        lambda: fixture_graph_check({"a": [], "b": []}, ["a"], {"a", "b"}),
    )
    require_rejection(
        "duplicate ownership",
        lambda: fixture_graph_check({"a": ["c"], "b": ["c"], "c": []}, ["a", "b"], {"a", "b", "c"}),
    )
    # Prefix changes do not change cell ownership; the anchor traversal is the contract.
    fixture_graph_check({"alt_header": ["cw_islamist_ins_1990s_global_operational_continuum"], "cw_islamist_ins_1990s_global_operational_continuum": []}, ["alt_header"], {"alt_header", "cw_islamist_ins_1990s_global_operational_continuum"})


def validate_doctrine_rework() -> None:
    parked = [path for path in doctrine_files if not path.is_file()]
    if len(parked) == len(doctrine_files):
        print(
            "Doctrine rework is parked under "
            "'common/technologies/doctrine rework/' and is not loaded by the game; "
            "skipping doctrine contracts."
        )
        return
    if parked:
        fail(
            "doctrine rework is half parked; these files are missing from the active "
            f"technologies directory: {sorted(path.name for path in parked)}"
        )
        return
    by_file: dict[str, dict[str, str]] = {}
    for path in doctrine_files:
        filename = path.name
        try:
            blocks = strict_top_level_blocks(text(path), "technologies", filename)
        except ScriptParseError as problem:
            fail(str(problem))
            continue
        by_file[filename] = dict(blocks)
        expected_count = EXPECTED_DOCTRINE_COUNTS[filename]
        if len(blocks) != expected_count:
            fail(f"{filename} must contain {expected_count} technologies, found {len(blocks)}")
        expected_type = {"land_doctrine.txt": "army", "air_doctrine.txt": "air", "naval_doctrine.txt": "navy"}[filename]
        for name, block in blocks:
            for field in ("xp_research_type", "xp_unlock_cost", "doctrine"):
                values = top_level_values(block, field)
                if len(values) != 1:
                    fail(f"{name} in {filename} must define exactly one {field}")
            if top_level_values(block, "xp_research_type") != [expected_type]:
                fail(f"{name} in {filename} has the wrong XP research type")
            if top_level_values(block, "xp_unlock_cost") != ["100"]:
                fail(f"{name} in {filename} must cost exactly 100 XP")
            if top_level_values(block, "doctrine") != ["yes"]:
                fail(f"{name} in {filename} must retain doctrine = yes")
            for path_block in top_level_named_blocks(block, "path", name):
                targets = top_level_values(path_block, "leads_to_tech")
                if not targets:
                    # Land capstones retain a documented, commented-out future path.
                    continue
                if len(targets) != 1:
                    fail(f"{name} has a malformed path block")
                elif targets[0] not in technology_set:
                    fail(f"undefined technology path {name} -> {targets[0]} in {filename}")
            for target in re.findall(
                r"\b(?:has_tech|is_researching_technology)\s*=\s*([A-Za-z0-9_]+)",
                strip_script_comments(block),
            ):
                if target not in technology_set:
                    fail(f"undefined doctrine prerequisite target {target} in {name}")
        expected_digest = DOCTRINE_CONTENT_SHA256.get(filename)
        if expected_digest and doctrine_content_digest(blocks) != expected_digest:
            fail(f"{filename} has an unexpected effect/path/content change outside allow blocks")

    land = by_file.get("land_doctrine.txt", {})
    air = by_file.get("air_doctrine.txt", {})
    naval = by_file.get("naval_doctrine.txt", {})
    manifest = read_land_manifest()
    if len(manifest) != 78:
        fail(f"land cell manifest must contain 78 rows, found {len(manifest)}")
    manifest_by_header = {row["header"]: row for row in manifest}
    if len(manifest_by_header) != len(manifest):
        fail("land cell manifest contains duplicate headers")
    if tuple(row["header"] for row in manifest if row["parent"] is None) != tuple(
        row["header"] for row in manifest if row["header"] in LAND_ROOTS
    ):
        fail("land cell manifest root set or order changed")
    if set(row["header"] for row in manifest if row["parent"] is None) != set(LAND_ROOTS):
        fail("land cell manifest has the wrong independent root set")

    if land:
        for name, block in land.items():
            allows = top_level_named_blocks(block, "allow", name)
            if top_level_named_blocks(block, "dependencies", name):
                fail(f"land technology {name} adds a cumulative dependencies block")
            if name not in manifest_by_header:
                if allows:
                    fail(f"non-header land technology {name} retains an allow block")
                continue
            if len(allows) != 1:
                fail(f"land header {name} must contain exactly one allow block")
                continue
            positive, clauses = parse_allow_signature(allows[0], name)
            row = manifest_by_header[name]
            expected_positive = [] if row["parent"] is None else [row["parent"]]
            if positive != expected_positive:
                fail(f"{name} has the wrong direct lineage prerequisite: {positive}")
            expected_clauses: set[tuple[str, str]] = set()
            if row["decade"] > 1940:
                expected_clauses.add(("date", f"{row['decade']}.1.1"))
            if name in LAND_ROOTS:
                for rival in LAND_ROOTS:
                    if rival != name:
                        expected_clauses.add(("has", rival))
                        expected_clauses.add(("researching", rival))
            if len(clauses) != len(set(clauses)) or set(clauses) != expected_clauses:
                fail(f"{name} has the wrong lineage/date/root exclusion clauses")
        header_names = set(manifest_by_header)
        actual_allow_names = {name for name, block in land.items() if top_level_named_blocks(block, "allow", name)}
        if actual_allow_names != header_names:
            fail("land allow blocks are not exactly the 78 reviewed header blocks")
        if re.search(r"\b(?:X_TESt|has_country_flag)\b", strip_script_comments(text(doctrine_files[0]))):
            fail("land doctrine retains the obsolete X_TESt/country-flag gate")

        outgoing: dict[str, list[str]] = {name: [] for name in land}
        incoming: dict[str, list[str]] = {name: [] for name in land}
        for name, block in land.items():
            for path_block in top_level_named_blocks(block, "path", name):
                targets = top_level_values(path_block, "leads_to_tech")
                if len(targets) != 1:
                    continue
                target = targets[0]
                outgoing[name].append(target)
                if target in incoming:
                    incoming[target].append(name)
            if len(outgoing[name]) != len(set(outgoing[name])):
                fail(f"land technology {name} contains a duplicate active path")

        graph_state: dict[str, int] = {}
        def visit_graph(node: str) -> None:
            state = graph_state.get(node, 0)
            if state == 1:
                fail(f"land doctrine path graph contains a cycle at {node}")
                return
            if state == 2:
                return
            graph_state[node] = 1
            for target in outgoing.get(node, []):
                if target in land:
                    visit_graph(target)
            graph_state[node] = 2
        for name in land:
            visit_graph(name)

        owners: dict[str, str] = {}
        def visit_cell(cell: str, node: str, active: set[str]) -> None:
            if node in active:
                fail(f"land cell {cell} contains a cycle at {node}")
                return
            previous = owners.get(node)
            if previous is not None:
                if previous != cell:
                    fail(f"land technology {node} is owned by both {previous} and {cell}")
                return
            owners[node] = cell
            active.add(node)
            for target in outgoing.get(node, []):
                if target in land:
                    visit_cell(cell, target, active)
            active.remove(node)

        for row in manifest:
            header = row["header"]
            if header in land:
                visit_cell(header, header, set())
        if set(owners) != set(land):
            fail(
                "land GUI anchors do not uniquely cover all technologies: "
                f"missing={sorted(set(land) - set(owners))}, extra={sorted(set(owners) - set(land))}"
            )
        for source, targets in outgoing.items():
            for target in targets:
                if target in owners and source in owners and owners[source] != owners[target]:
                    fail(f"cross-cell land path {source} -> {target}")
        for row in manifest:
            cell = row["header"]
            nodes = {name for name, owner in owners.items() if owner == cell}
            cell_roots = [name for name in nodes if not any(source in nodes for source in incoming[name])]
            cell_terminals = [name for name in nodes if not any(target in nodes for target in outgoing[name])]
            if len(nodes) != row["nodes"]:
                fail(f"land cell {cell} owns {len(nodes)} nodes, expected {row['nodes']}")
            if len(cell_roots) != 1 or cell_roots[0] != cell:
                fail(f"land cell {cell} must have exactly one root at its header")
            if len(cell_terminals) != 1 or cell_terminals[0] != row["terminal"]:
                fail(f"land cell {cell} has the wrong terminal: {cell_terminals}")

        gui_code = strip_script_comments(text(MOD / "interface/countrytechtreeview.gui"))
        land_folders = named_gui_blocks(gui_code, "containerWindowType", "old_land_doctrine_folder", "countrytechtreeview")
        if len(land_folders) != 1:
            fail(f"expected one active old_land_doctrine_folder GUI container, found {len(land_folders)}")
        else:
            anchors: dict[str, tuple[int, int]] = {}
            for grid in top_level_named_blocks(land_folders[0], "gridboxtype", "old_land_doctrine_folder"):
                name_match = re.search(r'(?m)^\s*name\s*=\s*"([^"]+)"', grid)
                if not name_match:
                    fail("land GUI grid anchor has no name")
                    continue
                grid_name = name_match.group(1)
                if not grid_name.endswith("_tree"):
                    fail(f"unexpected non-cell grid in old_land_doctrine_folder: {grid_name}")
                    continue
                technology = grid_name[:-5]
                position = re.search(
                    r"\bposition\s*=\s*\{\s*x\s*=\s*(-?[0-9]+)\s*y\s*=\s*(-?[0-9]+)",
                    grid,
                )
                if not position:
                    fail(f"land GUI anchor {technology} has no position")
                    continue
                if technology in anchors:
                    fail(f"duplicate land GUI anchor: {technology}")
                anchors[technology] = (int(position.group(1)), int(position.group(2)))
            expected_anchors = {
                row["header"]: (row["x"], LAND_ROW_Y.get(row["decade"], -1)) for row in manifest
            }
            if anchors != expected_anchors:
                fail("land GUI anchors or coordinates differ from the reviewed manifest")

    expected_air = {
        "air_doctrine_versatile": {("has", "air_doctrine_integral"), ("researching", "air_doctrine_integral"), ("has", "air_doctrine_systemic"), ("researching", "air_doctrine_systemic")},
        "air_doctrine_systemic": {("has", "air_doctrine_integral"), ("researching", "air_doctrine_integral"), ("has", "air_doctrine_versatile"), ("researching", "air_doctrine_versatile")},
        "air_doctrine_integral": {("has", "air_doctrine_systemic"), ("researching", "air_doctrine_systemic"), ("has", "air_doctrine_versatile"), ("researching", "air_doctrine_versatile")},
        "air_doctrine_systemic_5a1": {("has", "air_doctrine_systemic_5a2"), ("researching", "air_doctrine_systemic_5a2")},
        "air_doctrine_systemic_5a2": {("has", "air_doctrine_systemic_5a1"), ("researching", "air_doctrine_systemic_5a1")},
        "air_doctrine_systemic_5b1": {("has", "air_doctrine_systemic_5b2"), ("researching", "air_doctrine_systemic_5b2")},
        "air_doctrine_systemic_5b2": {("has", "air_doctrine_systemic_5b1"), ("researching", "air_doctrine_systemic_5b1")},
        "air_doctrine_integral_2a1": {("has", "air_doctrine_integral_2a2"), ("researching", "air_doctrine_integral_2a2")},
        "air_doctrine_integral_2a2": {("has", "air_doctrine_integral_2a1"), ("researching", "air_doctrine_integral_2a1")},
        "air_doctrine_integral_2b1": {("has", "air_doctrine_integral_2b2"), ("researching", "air_doctrine_integral_2b2")},
        "air_doctrine_integral_2b2": {("has", "air_doctrine_integral_2b1"), ("researching", "air_doctrine_integral_2b1")},
        "air_doctrine_integral_6a": {("has", "air_doctrine_integral_6b"), ("researching", "air_doctrine_integral_6b")},
        "air_doctrine_integral_6b": {("has", "air_doctrine_integral_6a"), ("researching", "air_doctrine_integral_6a")},
    }
    if air:
        actual_air = {}
        for name, block in air.items():
            allows = top_level_named_blocks(block, "allow", name)
            if allows:
                if len(allows) != 1:
                    fail(f"{name} has duplicate air allow blocks")
                else:
                    positive, clauses = parse_allow_signature(allows[0], name)
                    if positive or len(clauses) != len(set(clauses)):
                        fail(f"{name} has a malformed air exclusion block")
                    actual_air[name] = set(clauses)
        if set(actual_air) != set(expected_air):
            fail(f"air exclusion block set changed: {sorted(set(actual_air) ^ set(expected_air))}")
        for name, expected in expected_air.items():
            if actual_air.get(name) != expected:
                fail(f"air exclusion semantics changed for {name}")

    expected_naval = {
        "fleet_in_being": {("has", "trade_interdiction"), ("researching", "trade_interdiction"), ("has", "base_strike"), ("researching", "base_strike")},
        "trade_interdiction": {("has", "fleet_in_being"), ("researching", "fleet_in_being"), ("has", "base_strike"), ("researching", "base_strike")},
        "base_strike": {("has", "fleet_in_being"), ("researching", "fleet_in_being"), ("has", "trade_interdiction"), ("researching", "trade_interdiction")},
    }
    if naval:
        actual_naval = {}
        for name, block in naval.items():
            allows = top_level_named_blocks(block, "allow", name)
            if allows:
                if len(allows) != 1:
                    fail(f"{name} has duplicate naval allow blocks")
                else:
                    positive, clauses = parse_allow_signature(allows[0], name)
                    if positive or len(clauses) != len(set(clauses)):
                        fail(f"{name} has a malformed naval exclusion block")
                    actual_naval[name] = set(clauses)
        if actual_naval != expected_naval:
            fail("naval root exclusion semantics changed")

    tags_code = strip_script_comments(text(MOD / "common/technology_tags/00_technology.txt"))
    gui_code = strip_script_comments(text(MOD / "interface/countrytechtreeview.gui"))
    for folder, ledger in LEDGER_FOLDERS.items():
        tag_blocks = key_blocks(tags_code, folder, "technology_tags")
        if len(tag_blocks) != 1:
            fail(f"expected one technology tag definition for {folder}")
        elif top_level_values(tag_blocks[0], "ledger") != [ledger] or top_level_values(tag_blocks[0], "doctrine") != ["no"]:
            fail(f"{folder} must remain an ordinary {ledger} ledger folder")
        if len(named_gui_blocks(gui_code, "containerWindowType", folder, "countrytechtreeview")) != 1:
            fail(f"missing active GUI container for {folder}")
        tabs = named_gui_blocks(gui_code, "containerWindowType", "folder_tabs", "countrytechtreeview")
        if len(tabs) != 1:
            fail("expected one active folder_tabs container")
        else:
            button_names = []
            for button in top_level_named_blocks(tabs[0], "buttonType", "folder_tabs"):
                name_match = re.search(r'(?m)^\s*name\s*=\s*"([^"]+)"', button)
                if name_match:
                    button_names.append(name_match.group(1))
            if button_names.count(folder + "_tab") != 1:
                fail(f"missing or duplicate tab registration for {folder}")
        for suffix in ("_item", "_small_item"):
            template = "techtree_" + folder + suffix
            if len(named_gui_blocks(gui_code, "containerWindowType", template, "countrytechtreeview")) != 1:
                fail(f"missing or duplicate node template for {template}")

    gfx_code = strip_script_comments(text(MOD / "interface/CWIC_Doctrines.gfx"))
    doctrine_sprites = named_gui_blocks(gfx_code, "spriteType", None, "CWIC_Doctrines")
    doctrine_sprites += named_gui_blocks(gfx_code, "SpriteType", None, "CWIC_Doctrines")
    for sprite in doctrine_sprites:
        texture = re.search(r'\btexturefile\s*=\s*"([^"]+)"', sprite)
        vanilla_placeholder = "gfx/interface/doctrines/icons/doctrine_placeholder.dds"
        if texture and texture.group(1).startswith("gfx/") and texture.group(1) != vanilla_placeholder and not (MOD / texture.group(1)).is_file():
            name_match = re.search(r'\bname\s*=\s*"([^"]+)"', sprite)
            fail(f"missing doctrine icon texture for {name_match.group(1) if name_match else 'unnamed sprite'}")

    if manifest:
        expected_parent_count = sum(row["parent"] is not None for row in manifest)
        expected_date_count = sum(row["decade"] > 1940 for row in manifest)
        if expected_parent_count != 67 or expected_date_count != 70:
            fail("reviewed land manifest counts changed: expected 67 lineage and 70 date gates")
        # Static route model: the graph must expose a route to each terminal,
        # while header conjunctions enforce the reviewed date and lineage.
        for row in manifest:
            header = row["header"]
            terminal = row["terminal"]
            reachable = {header}
            frontier = [header]
            while frontier:
                node = frontier.pop()
                for target in outgoing.get(node, []):
                    if target not in reachable:
                        reachable.add(target)
                        frontier.append(target)
            if terminal not in reachable:
                fail(f"static route model cannot reach terminal {terminal} from {header}")

        def model_eligible(row: dict[str, object], year: int, owned: set[str], researching: set[str]) -> bool:
            if year < row["decade"]:
                return False
            parent = row["parent"]
            if parent is not None and parent not in owned:
                return False
            if row["header"] in LAND_ROOTS:
                rival_roots = set(LAND_ROOTS) - {row["header"]}
                if rival_roots & (owned | researching):
                    return False
            return True

        for year, expected_roots in (
            (1949, {row["header"] for row in manifest if row["decade"] == 1940}),
            (1980, {row["header"] for row in manifest if row["header"] in LAND_ROOTS and row["decade"] <= 1980}),
        ):
            eligible = {row["header"] for row in manifest if model_eligible(row, year, set(), set())}
            if eligible != expected_roots:
                fail(f"static date model has the wrong eligible headers at {year}")
        for row in manifest:
            if row["decade"] <= 1940:
                continue
            parent_owned = set() if row["parent"] is None else {row["parent"]}
            if model_eligible(row, row["decade"] - 1, parent_owned, set()):
                fail(f"static date model accepts {row['header']} before {row['decade']}.1.1")
            if not model_eligible(row, row["decade"], parent_owned, set()):
                fail(f"static date model rejects {row['header']} on {row['decade']}.1.1")
            if row["parent"] is not None and model_eligible(row, row["decade"], set(), set()):
                fail(f"static lineage model unlocks {row['header']} without its predecessor")
        for root in LAND_ROOTS:
            root_row = manifest_by_header.get(root)
            if root_row is None:
                continue
            for rival in set(LAND_ROOTS) - {root}:
                if model_eligible(root_row, root_row["decade"], {rival}, set()) or model_eligible(root_row, root_row["decade"], set(), {rival}):
                    fail(f"static root exclusion model permits {root} after {rival}")
        children_by_parent: dict[str, list[dict[str, object]]] = {}
        for row in manifest:
            if row["parent"] is not None:
                children_by_parent.setdefault(row["parent"], []).append(row)
        for parent, children in children_by_parent.items():
            if len(children) < 2:
                continue
            year = max(child["decade"] for child in children)
            if not all(model_eligible(child, year, {parent}, set()) for child in children):
                fail(f"static sibling model cannot unlock all children of {parent}")

        # Follow each independent root through its manifest descendants. This
        # permits multiple native branch routes inside a cell without inventing
        # an all-branches prerequisite for the terminal.
        for root in LAND_ROOTS:
            owned_terminals: set[str] = set()
            completed: set[str] = set()
            changed = True
            while changed:
                changed = False
                for row in manifest:
                    if row["header"] in completed:
                        continue
                    if row["parent"] is None:
                        available = row["header"] == root
                    else:
                        available = row["parent"] in owned_terminals
                    if available and model_eligible(row, max(1949, row["decade"]), owned_terminals, set()):
                        completed.add(row["header"])
                        owned_terminals.add(row["terminal"])
                        changed = True
            expected_family = {root}
            changed = True
            while changed:
                changed = False
                for row in manifest:
                    if row["parent"] in {manifest_by_header[name]["terminal"] for name in expected_family} and row["header"] not in expected_family:
                        expected_family.add(row["header"])
                        changed = True
            if completed != expected_family:
                fail(f"static family route model cannot complete descendants of {root}")


def fail(message: str) -> None:
    errors.append(message)


def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
        return ""


def code_only(value: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in value.splitlines())


def brace_balance(path: Path) -> None:
    value = code_only(text(path))
    depth = 0
    for number, line in enumerate(value.splitlines(), 1):
        depth += line.count("{") - line.count("}")
        if depth < 0:
            fail(f"negative brace depth: {path.relative_to(ROOT)}:{number}")
            return
    if depth:
        fail(f"unbalanced braces ({depth:+d}): {path.relative_to(ROOT)}")


def top_level_blocks(value: str, root_name: str) -> list[tuple[str, str]]:
    lines = value.splitlines(keepends=True)
    depth = 0
    inside = False
    start: int | None = None
    name: str | None = None
    result: list[tuple[str, str]] = []
    for index, line in enumerate(lines):
        code = line.split("#", 1)[0]
        if not inside and re.match(rf"^{re.escape(root_name)}\s*=\s*\{{", code):
            inside = True
            depth += code.count("{") - code.count("}")
            continue
        if not inside:
            continue
        if depth == 1:
            match = re.match(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{", code)
            if match:
                start = index
                name = match.group(1)
        depth += code.count("{") - code.count("}")
        if start is not None and depth == 1:
            result.append((name or "", "".join(lines[start : index + 1])))
            start = None
            name = None
    return result


def keyed_blocks(value: str, key: str) -> list[str]:
    """Return every balanced `key = { ... }` block from comment-free script."""
    value = code_only(value)
    result: list[str] = []
    pattern = re.compile(rf"\b{re.escape(key)}\s*=\s*\{{")
    for match in pattern.finditer(value):
        depth = 0
        for index in range(match.end() - 1, len(value)):
            if value[index] == "{":
                depth += 1
            elif value[index] == "}":
                depth -= 1
                if depth == 0:
                    result.append(value[match.start() : index + 1])
                    break
        else:
            fail(f"unbalanced {key} block")
    return result


def direct_values(block: str, key: str) -> list[str]:
    """Read simple direct values from a balanced block."""
    return top_level_values(block, key)


def listed_values(block: str) -> list[str]:
    """Read bare values from a list block such as enable_equipments."""
    value = strip_script_comments(block)
    opening = value.find("{")
    if opening < 0:
        raise ScriptParseError("missing opening brace while reading list block")
    ending = balanced_end(value, opening, "list block")
    return re.findall(r"(?m)^\s*([A-Za-z0-9_]+)\s*$", value[opening + 1 : ending])


def flame_grant_errors(technologies: dict[str, str]) -> list[str]:
    errors_found: list[str] = []
    for technology, expected in FLAME_TECH_GRANTS.items():
        actual = {
            equipment
            for block in top_level_named_blocks(technologies.get(technology, ""), "enable_equipments", technology)
            for equipment in listed_values(block)
        }
        missing = expected - actual
        if missing:
            errors_found.append(f"{technology} is missing flame chassis grants: {sorted(missing)}")
    return errors_found


def module_parent_errors(definitions: dict[str, str]) -> list[str]:
    errors_found: list[str] = []
    parents: dict[str, str] = {}
    for name, block in definitions.items():
        values = direct_values(block, "parent")
        if len(values) > 1:
            errors_found.append(f"tank module {name} has multiple parents")
        if not values:
            continue
        parent = values[0]
        if parent not in definitions:
            errors_found.append(f"tank module {name} has undefined parent {parent}")
        else:
            parents[name] = parent
    for name in definitions:
        trail: set[str] = set()
        node = name
        while node in parents:
            if node in trail:
                errors_found.append(f"tank module parent graph contains a cycle at {node}")
                break
            trail.add(node)
            node = parents[node]
    return errors_found


def abbreviation_errors(definitions: dict[str, str]) -> list[str]:
    errors_found: list[str] = []
    abbreviations: dict[str, str] = {}
    for name, block in definitions.items():
        values = re.findall(r"(?m)^\s*abbreviation\s*=\s*\"([^\"]+)\"", block)
        if len(values) != 1:
            errors_found.append(f"tank module {name} must have one abbreviation")
            continue
        previous = abbreviations.get(values[0])
        if previous and previous != name:
            errors_found.append(f"tank module abbreviation collision: {previous} and {name} use {values[0]}")
        abbreviations[values[0]] = name
    return errors_found


def secondary_unlock_errors(unlocked: set[str]) -> list[str]:
    return [
        f"secondary turret module is not unlocked: {module}"
        for module in SECONDARY_MODULES
        if module not in unlocked
    ]


def tank_self_loop_ids(technologies: dict[str, str]) -> set[str]:
    return {
        owner
        for owner, block in technologies.items()
        for path in top_level_named_blocks(block, "path", owner)
        if owner in direct_values(path, "leads_to_tech")
    }


def export_variant_map(value: str) -> dict[str, str]:
    variants: dict[str, str] = {}
    for block in keyed_blocks(value, "create_equipment_variant"):
        name_match = re.search(r"(?m)^\s*name\s*=\s*\"([^\"]+)\"", block)
        type_match = re.search(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", block)
        if name_match and type_match:
            variants[name_match.group(1)] = type_match.group(1)
    return variants


def missing_ammunition_categories(installed_categories: set[str]) -> set[str]:
    return ammo_categories - installed_categories


def named_focus_blocks(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for kind in ("focus", "shared_focus"):
        for block in keyed_blocks(value, kind):
            match = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", block)
            if match:
                result[match.group(1)] = block
    return result


def balance_manifest_rows() -> list[tuple[int, str, str, int, str]]:
    rows: list[tuple[int, str, str, int, str]] = []
    for line in text(BALANCE_MANIFEST_FILE).splitlines():
        if not line.startswith("|") or not re.match(r"\|\s*\d+\s*\|", line):
            continue
        fields = [field.strip() for field in line.strip("|").split("|")]
        if len(fields) < 5:
            fail(f"malformed tank balance manifest row: {line}")
            continue
        try:
            rows.append((int(fields[0]), fields[1], fields[2], int(fields[3]), fields[4]))
        except ValueError:
            fail(f"malformed tank balance manifest row: {line}")
    return rows


def balance_manifest_values() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in text(BALANCE_MANIFEST_FILE).splitlines():
        if not line.startswith("|") or not re.match(r"\|\s*\d+\s*\|", line):
            continue
        fields = [field.strip() for field in line.strip("|").split("|")]
        if len(fields) < 17:
            fail(f"tank balance manifest row lacks normalized target values: {line}")
            continue
        try:
            row: dict[str, object] = {
                "row": int(fields[0]),
                "name": fields[1],
                "kind": fields[2],
                "year": int(fields[3]),
                "role": fields[4],
            }
            for index, (metric, _, _) in enumerate(BALANCE_METRICS, start=5):
                raw = fields[index].replace(",", ".").strip()
                if raw in {"", "—", "-"}:
                    row[metric] = None
                    continue
                row[metric] = float(raw.rstrip("%"))
            rows.append(row)
        except (ValueError, IndexError) as error:
            fail(f"malformed normalized tank balance values: {line}")
    return rows


def read_balance_workbook(path: Path) -> list[dict[str, object]]:
    """Read the review rows with the standard library only."""
    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    relationships_namespace = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    with ZipFile(path) as archive:
        strings_root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
        shared_strings = [
            "".join(node.text or "" for node in item.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
            for item in strings_root.findall("main:si", namespace)
        ]
        workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        relationships = ElementTree.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationship_targets = {
            node.attrib["Id"]: node.attrib["Target"] for node in relationships
        }
        sheet_target = None
        for sheet in workbook.findall("main:sheets/main:sheet", namespace):
            if sheet.attrib.get("name") == "Total Balance Sheet":
                sheet_target = relationship_targets[
                    sheet.attrib[f"{{{relationships_namespace}}}id"]
                ]
                break
        if sheet_target is None:
            raise ValueError("Total Balance Sheet worksheet is missing")
        archive_path = "xl/" + sheet_target.lstrip("/")
        if archive_path.startswith("xl/xl/"):
            archive_path = archive_path[3:]
        worksheet = ElementTree.fromstring(archive.read(archive_path))
        rows: list[dict[str, object]] = []
        for row in worksheet.findall(".//main:sheetData/main:row", namespace):
            row_number = int(row.attrib["r"])
            cells: dict[str, str] = {}
            for cell in row.findall("main:c", namespace):
                reference = cell.attrib.get("r", "")
                value = cell.find("main:v", namespace)
                cell_value = "" if value is None else value.text or ""
                if cell.attrib.get("t") == "s" and cell_value:
                    cell_value = shared_strings[int(cell_value)]
                cells[reference.rstrip("0123456789")] = cell_value
            if row_number < 2 or not cells.get("A") or not cells.get("B"):
                continue
            try:
                year = int(float(cells["B"].replace(",", ".")))
            except ValueError as error:
                raise ValueError(f"invalid balance year in workbook row {row_number}") from error
            row: dict[str, object] = {
                "row": row_number,
                "name": cells["A"],
                "year": year,
            }
            for metric, column, percentage in BALANCE_METRICS:
                raw = cells.get(column, "").strip()
                if not raw:
                    row[metric] = None
                    continue
                try:
                    value = float(raw.replace(",", ".").rstrip("%"))
                except ValueError as error:
                    raise ValueError(
                        f"invalid balance value in workbook row {row_number}, column {column}"
                    ) from error
                row[metric] = value / 100 if percentage else value
            rows.append(row)
        return rows


def _xlsx_sheet_target(archive: ZipFile, sheet_name: str) -> str:
    """Resolve a worksheet through workbook relationships without openpyxl."""
    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    relationships_namespace = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
    relationships = ElementTree.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {node.attrib["Id"]: node.attrib["Target"] for node in relationships}
    for sheet in workbook.findall("main:sheets/main:sheet", namespace):
        if sheet.attrib.get("name") == sheet_name:
            target = targets[sheet.attrib[f"{{{relationships_namespace}}}id"]]
            path = "xl/" + target.lstrip("/")
            return path[3:] if path.startswith("xl/xl/") else path
    raise ValueError(f"worksheet is missing: {sheet_name}")


def _xlsx_shared_strings(archive: ZipFile) -> list[str]:
    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(node.text or "" for node in item.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
        for item in root.findall("main:si", namespace)
    ]


def _xlsx_cell_value(cell: ElementTree.Element, shared_strings: list[str]) -> str:
    namespace = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    inline = cell.find(namespace + "is")
    if inline is not None:
        return "".join(node.text or "" for node in inline.iter(namespace + "t"))
    value = cell.find(namespace + "v")
    if value is None or value.text is None:
        return ""
    raw = value.text
    if cell.attrib.get("t") == "s" and raw:
        return shared_strings[int(raw)]
    return raw


def read_module_workbook(path: Path, sheet_name: str, id_column: str) -> dict[str, dict[str, object]]:
    """Read module rows while retaining cell presence for absent-versus-zero checks."""
    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(path) as archive:
        shared_strings = _xlsx_shared_strings(archive)
        worksheet = ElementTree.fromstring(archive.read(_xlsx_sheet_target(archive, sheet_name)))
        rows: dict[str, dict[str, object]] = {}
        for row in worksheet.findall(".//main:sheetData/main:row", namespace):
            row_number = int(row.attrib["r"])
            cells: dict[str, str] = {}
            present: set[str] = set()
            for cell in row.findall("main:c", namespace):
                reference = cell.attrib.get("r", "")
                column = reference.rstrip("0123456789")
                value = _xlsx_cell_value(cell, shared_strings)
                cells[column] = value
                if value.strip():
                    present.add(column)
            module = cells.get(id_column, "").strip()
            if not module or module == "Module Loc Name":
                continue
            if module not in module_ids:
                if row_number > 33 and not module.startswith(("Light_Hull_", "MBT_Hull_", "Heavy_Hull_")):
                    fail(f"unknown tank module ID in {sheet_name} row {row_number}: {module}")
                continue
            if module in rows:
                fail(f"duplicate {sheet_name} module row for {module}")
                continue
            rows[module] = {"row": row_number, "cells": cells, "present": present}
        return rows


def _decimal(value: str, *, percentage: bool = False, context: str = "value") -> float:
    raw = value.strip().replace(",", ".")
    if not raw:
        raise ValueError(f"empty numeric {context}")
    has_percent = raw.endswith("%")
    if has_percent:
        raw = raw[:-1].strip()
    try:
        result = float(raw)
    except ValueError as error:
        raise ValueError(f"malformed numeric {context}: {value!r}") from error
    if has_percent or percentage:
        return result / 100
    return result


def _numeric_block(block: str, label: str) -> dict[str, float]:
    """Read direct numeric assignments from one already-bounded child block."""
    value = strip_script_comments(block)
    opening = value.find("{")
    ending = balanced_end(value, opening, label)
    body = value[opening + 1 : ending]
    result: dict[str, float] = {}
    for match in re.finditer(
        r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)\s*$",
        body,
    ):
        key, raw = match.groups()
        key = MODULE_FIELD_ALIASES.get(key, key)
        if key in result:
            fail(f"duplicate numeric field {key} in {label}")
        result[key] = float(raw)
    return result


def module_balance_record(module: str) -> dict[str, object]:
    """Extract direct module operations; parent effects remain explicit metadata."""
    definition = module_definitions.get(module, "")
    record: dict[str, object] = {"add": {}, "multiply": {}, "resources": {}}
    for operation in ("add_stats", "multiply_stats"):
        children = top_level_named_blocks(definition, operation, module)
        if len(children) > 1:
            fail(f"tank module {module} has multiple {operation} blocks")
        if children:
            record["add" if operation == "add_stats" else "multiply"] = _numeric_block(
                children[0], f"{module}.{operation}"
            )
    resources = top_level_named_blocks(definition, "build_cost_resources", module)
    if len(resources) > 1:
        fail(f"tank module {module} has multiple build_cost_resources blocks")
    if resources:
        record["resources"] = _numeric_block(resources[0], f"{module}.build_cost_resources")
    for field in ("hardness", "reliability", "breakthrough", "defense", "armor_value", "maximum_speed", "build_cost_ic", "fuel_consumption", "supply_consumption"):
        values = direct_values(definition, field)
        if values:
            record.setdefault("add", {})[MODULE_FIELD_ALIASES.get(field, field)] = float(values[0])
    dismantle = direct_values(definition, "dismantle_cost_ic")
    record["dismantle"] = float(dismantle[0]) if dismantle else None
    record["parent"] = (direct_values(definition, "parent") or ["none"])[0]
    record["category"] = (direct_values(definition, "category") or [""])[0]
    record["xp_present"] = bool(direct_values(definition, "xp_cost"))
    conversions = top_level_named_blocks(definition, "can_convert_from", module)
    conversion = []
    for child in conversions:
        category = (direct_values(child, "module_category") or [""])[0]
        cost = (direct_values(child, "convert_cost_ic") or [""])[0]
        conversion.append(f"module_category={category},convert_cost_ic={cost}")
    record["conversion"] = conversion
    numeric_fields = set(record["add"]) | set(record["multiply"])
    for field in sorted(numeric_fields):
        if field not in MODULE_BALANCE_COLUMNS:
            fail(f"unmapped numeric module stat {module}.{field}")
    for resource in record["resources"]:
        if resource not in MODULE_RESOURCE_COLUMNS:
            fail(f"unmapped module resource {module}.{resource}")
    return record


def module_unlock_provenance() -> dict[str, list[tuple[str, str | None]]]:
    result: dict[str, list[tuple[str, str | None]]] = {module: [] for module in module_ids}
    for technology, block, path in technology_blocks:
        if path not in {TECH_DIR / "NSB_armor.txt", TECH_DIR / "NSB_armor_modules.txt"}:
            continue
        year_values = direct_values(block, "start_year")
        year = year_values[0] if year_values else None
        for unlock in top_level_named_blocks(block, "enable_equipment_modules", technology):
            for module in listed_values(unlock):
                if module in result:
                    result[module].append((technology, year))
    return result


def _module_metadata(module: str, record: dict[str, object], unlocks: dict[str, list[tuple[str, str | None]]]) -> str:
    operations = []
    for operation in ("add", "multiply"):
        values = record[operation]
        if values:
            operations.append(
                f"{operation}=" + ",".join(f"{field}:{values[field]:g}" for field in sorted(values))
            )
    resources = record["resources"]
    if resources:
        operations.append("resources=" + ",".join(f"{key}:{resources[key]:g}" for key in sorted(resources)))
    provenance = unlocks.get(module, [])
    unlock_text = "|".join(
        f"{technology}@{year if year is not None else 'default/inherited'}"
        for technology, year in provenance
    ) or "default/inherited"
    conversion = "|".join(record["conversion"]) or "none"
    operation_text = "; ".join(operations) if operations else "none"
    return (
        f"parent={record['parent']}; unlock={unlock_text}; "
        f"xp_cost={'present' if record['xp_present'] else 'absent'}; "
        f"dismantle_cost_ic={record['dismantle'] if record['dismantle'] is not None else 'absent'}; "
        f"conversion={conversion}; operations={operation_text}; "
        "exclusions=category,eligibility,abbreviation,display"
    )


def _module_csv_rows(path: Path) -> dict[str, list[str]]:
    if not path.is_file():
        fail(f"tank module balance CSV is missing: {path.relative_to(ROOT)}")
        return {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    headers = [index for index, row in enumerate(rows) if len(row) > 7 and row[7] == "Module Loc Name"]
    if len(headers) < 2 or headers[0] != 0:
        fail("tank module balance CSV must contain two module-table headers with Module Loc Name at column 7")
    if not rows or len(rows[0]) <= 7 or rows[0][7] != "Module Loc Name":
        fail("tank module balance CSV header moved Module Loc Name from column 7")
    result: dict[str, list[str]] = {}
    hull_prefixes = ("Light_Hull_", "MBT_Hull_", "Heavy_Hull_")
    for line_number, row in enumerate(rows, 1):
        if len(row) <= 7:
            continue
        module = row[7].strip()
        if not module or module == "Module Loc Name":
            continue
        if row[0].strip().startswith("Coverage") or row[3].strip().endswith(" rows"):
            continue
        if module.startswith(hull_prefixes) or row[0].strip() == "Hulls":
            continue
        if module not in module_ids:
            fail(f"unknown tank module ID in balance CSV row {line_number}: {module}")
            continue
        if module in result:
            fail(f"duplicate tank module ID in balance CSV: {module}")
            continue
        if len(row) < 41:
            fail(f"tank module balance CSV row {line_number} is shorter than the stat/resource schema")
        result[module] = row
    return result


def _module_cell_value(cells: dict[str, str], column: str) -> str:
    return cells.get(column, "").strip()


def _is_module_annotation(value: str) -> bool:
    return value.strip() in MODULE_SOURCE_ANNOTATIONS


def _normalize_master_module_rows(rows: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    """Project the master table's S:BG layout onto the minimal table's A:AO layout."""
    def column_letter(number: int) -> str:
        result = ""
        while number:
            number, remainder = divmod(number - 1, 26)
            result = chr(ord("A") + remainder) + result
        return result

    master_columns = [column_letter(number) for number in range(_csv_column_index("S") + 1, _csv_column_index("BH") + 2)]
    minimal_columns = [column_letter(number) for number in range(1, len(master_columns) + 1)]
    result: dict[str, dict[str, object]] = {}
    for module, row in rows.items():
        cells = row["cells"]
        present = row["present"]
        result[module] = {
            **row,
            "cells": {minimal: cells.get(master, "") for master, minimal in zip(master_columns, minimal_columns)},
            "present": {minimal for master, minimal in zip(master_columns, minimal_columns) if master in present},
        }
    return result


def _compare_module_row(module: str, row: dict[str, object] | list[str], record: dict[str, object], source: str) -> tuple[int, int]:
    if isinstance(row, dict):
        cells = row["cells"]
        present = row["present"]
        get = lambda column: _module_cell_value(cells, column)
        is_present = lambda column: column in present
    else:
        cells = row
        get = lambda column: cells[ord(column) - ord("A")] if len(column) == 1 and ord(column) <= ord("Z") else cells[_csv_column_index(column)] if _csv_column_index(column) < len(cells) else ""
        is_present = lambda column: bool(get(column).strip())

    checked = 0
    populated = set()
    for metric, (flat_column, _, multiply_column, _) in MODULE_BALANCE_COLUMNS.items():
        add_value = record["add"].get(metric)
        multiply_value = record["multiply"].get(metric)
        expected_by_column = {
            flat_column: (add_value if multiply_column is not None or add_value is not None else multiply_value)
        }
        if multiply_column:
            expected_by_column[multiply_column] = multiply_value
        for column, expected in expected_by_column.items():
            if expected is not None:
                checked += 1
                if not is_present(column):
                    fail(f"{source} module {module} is missing {column} for {metric}")
                else:
                    try:
                        actual = _decimal(get(column), context=f"{source} {module}.{metric}")
                    except ValueError as error:
                        fail(str(error))
                        actual = None
                    if actual is not None and abs(actual - expected) > 1e-9:
                        fail(f"{source} module {module}.{metric}: {actual:g} != {expected:g}")
                populated.add(column)
        for column in expected_by_column:
            if column and is_present(column):
                if _is_module_annotation(get(column)):
                    continue
                if column not in populated:
                    fail(f"{source} module {module} has unmapped populated stat column {column}")
    if record["dismantle"] is not None:
        checked += 1
        if not is_present(MODULE_DISMANTLE_COLUMN[0]):
            fail(f"{source} module {module} is missing dismantle_cost_ic")
        else:
            try:
                actual = _decimal(get(MODULE_DISMANTLE_COLUMN[0]), context=f"{source} {module}.dismantle_cost_ic")
            except ValueError as error:
                fail(str(error))
                actual = None
            if actual is not None and abs(actual - record["dismantle"]) > 1e-9:
                fail(f"{source} module {module}.dismantle_cost_ic: {actual:g} != {record['dismantle']:g}")
    for resource, (column, _) in MODULE_RESOURCE_COLUMNS.items():
        expected = record["resources"].get(resource)
        if expected is not None:
            checked += 1
            if not is_present(column):
                fail(f"{source} module {module} is missing resource {resource}")
            else:
                try:
                    actual = _decimal(get(column), context=f"{source} {module}.{resource}")
                except ValueError as error:
                    fail(str(error))
                    actual = None
                if actual is not None and abs(actual - expected) > 1e-9:
                    fail(f"{source} module {module}.{resource}: {actual:g} != {expected:g}")
        elif is_present(column):
            fail(f"{source} module {module} has unmapped populated resource column {column}")
    metadata_column = MODULE_OPERATION_COLUMN[0]
    if module in SCRIPT_OWNED_MODULES:
        if not is_present(metadata_column):
            fail(f"{source} module {module} is missing operation/provenance metadata")
        else:
            metadata = get(metadata_column)
            for token in ("parent=", "unlock=", "xp_cost=", "dismantle_cost_ic=", "conversion=", "operations=", "exclusions="):
                if token not in metadata:
                    fail(f"{source} module {module} metadata lacks {token}")
    return checked, len(populated)


def _csv_column_index(column: str) -> int:
    result = 0
    for character in column:
        result = result * 26 + ord(character) - ord("A") + 1
    return result - 1


def tank_module_balance_report() -> str:
    if not BALANCE_WORKBOOK_FILE.is_file():
        fail("tank balance workbook is missing for --tank-module-balance-report")
        return ""
    csv_rows = _module_csv_rows(BALANCE_CSV_FILE)
    minimal = read_module_workbook(BALANCE_WORKBOOK_FILE, "Total Balance Sheet Minimal", "H")
    master = _normalize_master_module_rows(
        read_module_workbook(BALANCE_WORKBOOK_FILE, "Total Balance Sheet", "Z")
    )
    exempt = set(APC_SUPERSTRUCTURE_MODULES) | set(APC_ARMAMENT_MODULES)
    sourced_modules = module_ids - exempt
    if exempt - module_ids:
        fail(f"workbook-exempt modules that no longer exist: {sorted(exempt - module_ids)}")
    if len(csv_rows) != len(sourced_modules):
        fail(f"tank balance CSV has {len(csv_rows)} module rows; expected {len(sourced_modules)}")
    for source, rows in (("CSV", csv_rows), ("Minimal", minimal), ("Master", master)):
        missing = sourced_modules - set(rows)
        extra = set(rows) - sourced_modules
        if missing:
            fail(f"{source} tank balance is missing module IDs: {sorted(missing)}")
        if extra:
            fail(f"{source} tank balance has unknown module IDs: {sorted(extra)}")
    unlocks = module_unlock_provenance()
    checked = 0
    populated = 0
    for module in sorted(sourced_modules):
        record = module_balance_record(module)
        for source, rows in (("CSV", csv_rows), ("Minimal", minimal), ("Master", master)):
            if module not in rows:
                continue
            source_record = record
            # The workbook is immutable. The reviewed QA turret change lives in
            # the CSV and script; still verify the old source cells explicitly.
            # See Deferred_Design_Decisions.md, conventional turret balance.
            if module == "conventional_turret" and source != "CSV":
                source_record = record | {
                    "add": {"build_cost_ic": 1.0, "reliability": 0.15},
                    "multiply": {},
                    "dismantle": 0.5,
                }
            row_checked, row_populated = _compare_module_row(module, rows[module], source_record, source)
            checked += row_checked
            populated += row_populated
            if source in {"Minimal", "Master"}:
                cells = rows[module]["cells"]
                other = csv_rows.get(module)
                if other:
                    for metric, (column, csv_index, multiply_column, multiply_index) in MODULE_BALANCE_COLUMNS.items():
                        if module == "conventional_turret" and metric in {"build_cost_ic", "breakthrough"}:
                            continue  # Explicit source-to-live deviation, checked above and by turret_contract.
                        for workbook_column, csv_column in ((column, csv_index), (multiply_column, multiply_index)):
                            if workbook_column is None:
                                continue
                            workbook_value = _module_cell_value(cells, workbook_column)
                            csv_value = other[csv_column].strip() if csv_column < len(other) else ""
                            if not workbook_value or not csv_value:
                                continue
                            if _is_module_annotation(workbook_value) or _is_module_annotation(csv_value):
                                continue
                            try:
                                workbook_number = _decimal(workbook_value, context=f"{source} {module}.{metric}")
                                csv_number = _decimal(csv_value, context=f"CSV {module}.{metric}")
                            except ValueError as error:
                                fail(str(error))
                                continue
                            if abs(workbook_number - csv_number) > 1e-9:
                                fail(f"{source}/CSV mismatch for {module}.{metric}")
    missing_script_owned = SCRIPT_OWNED_MODULES - module_ids
    if missing_script_owned:
        fail(f"script-owned module list contains undefined IDs: {sorted(missing_script_owned)}")
    metadata_count = sum(
        1 for module in SCRIPT_OWNED_MODULES if module in minimal and MODULE_OPERATION_COLUMN[0] in minimal[module]["present"]
    )
    if metadata_count != len(SCRIPT_OWNED_MODULES):
        fail(f"operation/provenance metadata covers {metadata_count}/{len(SCRIPT_OWNED_MODULES)} script-owned modules")
    return (
        f"Tank module balance report: {len(sourced_modules)} IDs reconciled across CSV, "
        f"Total Balance Sheet Minimal, and Total Balance Sheet; {checked} populated "
        f"stat/resource cells checked; operation/provenance metadata {metadata_count}/{len(SCRIPT_OWNED_MODULES)}; "
        f"22 script-owned IDs reconciled; 1 reviewed turret source-to-live override; "
        f"explicit exclusions cover eligibility, display, conversion, and XP fields "
        f"(the manual's 23 count has no additional module ID); "
        f"{len(exempt)} APC designer modules are authored in script only and are "
        f"exempt from the frozen workbook: {sorted(exempt)}."
    )


ENVELOPE_METRICS = (
    "reliability",
    "hardness",
    "hard_attack",
    "soft_attack",
    "breakthrough",
    "defense",
    "armor_value",
    "ap_attack",
    "maximum_speed",
    "fuel_consumption",
    "build_cost_ic",
)
ENVELOPE_RECIPE_MAP = {
    "Heavy Tank I": "Standard Heavy Tank 1942",
    "Heavy Tank II": "Standard Heavy Tank 1944",
    "Heavy Tank IV": "Standard Heavy Tank 1950",
    "Heavy Tank V": "Standard Heavy Tank 1955",
    "WWII Tank 1": "Standard Main Battle Tank 1942",
    "WWII Tank 2": "Standard Main Battle Tank 1944",
    "MBT II": "Standard Main Battle Tank 1950",
    "MBT III": "Standard Main Battle Tank 1960",
    "Light Tank I": "Standard Light Tank 1942",
    "Light Tank II": "Standard Light Tank 1944",
    "Light Tank IV": "Standard Light Tank 1960",
}


def _variant_recipes() -> dict[str, dict[str, object]]:
    recipes: dict[str, dict[str, object]] = {}
    for path in (VARIANT_EFFECT_FILE, FOCUS_EFFECT_FILE, NATIONAL_EFFECT_FILE):
        for block in keyed_blocks(text(path), "create_equipment_variant"):
            name_match = re.search(r'(?m)^\s*name\s*=\s*"([^"]+)"', block)
            type_match = re.search(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", block)
            if not name_match or not type_match:
                fail(f"tank recipe lacks name or chassis type in {path.name}")
                continue
            modules = top_level_named_blocks(block, "modules", name_match.group(1))
            if len(modules) != 1:
                fail(f"tank recipe {name_match.group(1)} must have one modules block")
                continue
            slots: list[tuple[str, str]] = []
            module_body = modules[0]
            opening = module_body.find("{")
            ending = balanced_end(module_body, opening, f"{name_match.group(1)}.modules")
            for match in re.finditer(
                r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\s*$",
                module_body[opening + 1 : ending],
            ):
                if match.group(2) != "empty":
                    slots.append((match.group(1), match.group(2)))
            name = name_match.group(1)
            if name in recipes:
                fail(f"duplicate tank recipe name: {name}")
            recipes[name] = {"name": name, "type": type_match.group(1), "slots": slots, "source": path.name}
    return recipes


def _effective_module_operations(module: str, trail: tuple[str, ...] = ()) -> tuple[dict[str, float], dict[str, float], set[str]]:
    if module not in module_definitions:
        return {}, {}, {f"unknown module {module}"}
    if module in trail:
        return {}, {}, {f"module parent cycle at {module}"}
    record = module_balance_record(module)
    # A module parent identifies the preceding upgrade, not another installed
    # module. Summing it made Radar II consume 2.2 fuel instead of the observed
    # 1.2 and GL ATGM III supply 255 hard attack instead of the observed 95.
    # Parent validity/cycles remain checked separately by module_parent_errors.
    return dict(record["add"]), dict(record["multiply"]), set()


def _direct_chassis_numbers(block: str) -> dict[str, float]:
    aliases = {"armor_value": "armor_value"}
    numbers: dict[str, float] = {}
    for field in ENVELOPE_METRICS:
        values = direct_values(block, field)
        if not values:
            continue
        try:
            numbers[aliases.get(field, field)] = float(values[0])
        except ValueError as error:
            raise ValueError(f"malformed chassis numeric field {field}: {values[0]}") from error
    return numbers


def _static_recipe_estimate(recipe: dict[str, object]) -> tuple[dict[str, float], set[str], list[str]]:
    chassis_blocks = dict(top_level_blocks(text(CHASSIS_FILE), "equipments"))
    chassis_type = recipe["type"]
    unknown: set[str] = set()
    reasons = ["engine modifier order, caps, and role bonuses are not modeled"]
    if chassis_type not in chassis_blocks:
        return {}, {f"unknown chassis {chassis_type}"}, reasons
    try:
        base = _direct_chassis_numbers(chassis_blocks[chassis_type])
    except ValueError as error:
        fail(str(error))
        return {}, {"malformed chassis value"}, reasons
    adds: dict[str, float] = {}
    multipliers: dict[str, float] = {}
    slots = recipe["slots"]
    slot_names = {slot for slot, _ in slots}
    missing_slots = REQUIRED_VARIANT_SLOTS - slot_names
    if missing_slots:
        unknown.add("missing required slots: " + ",".join(sorted(missing_slots)))
    for slot, module in slots:
        if module not in module_ids:
            unknown.add(f"unknown module {module} in {slot}")
            continue
        module_adds, module_multipliers, module_unknown = _effective_module_operations(module)
        unknown.update(module_unknown)
        for field, value in module_adds.items():
            adds[field] = adds.get(field, 0.0) + value
        for field, value in module_multipliers.items():
            multipliers[field] = multipliers.get(field, 0.0) + value
    values: dict[str, float] = {}
    for metric in ENVELOPE_METRICS:
        value = base.get(metric, 0.0) + adds.get(metric, 0.0)
        values[metric] = value * (1.0 + multipliers.get(metric, 0.0))
    return values, unknown, reasons


def _format_estimate(value: float, metric: str) -> str:
    if metric in {"reliability", "hardness"}:
        return f"{value * 100:.1f}%"
    return f"{value:.2f}".rstrip("0").rstrip(".")


def tank_envelope_report() -> str:
    recipes = _variant_recipes()
    if not recipes:
        fail("tank envelope report found no selected tank recipes")
        return ""
    manifest = [row for row in balance_manifest_values() if row.get("kind") == "tank" and row.get("role") == "target"]
    if len(manifest) != 21:
        fail(f"tank envelope report has {len(manifest)} tank targets; expected 21")
    selected: dict[str, dict[str, object]] = {}
    for target, recipe_name in ENVELOPE_RECIPE_MAP.items():
        if target not in {row["name"] for row in manifest}:
            fail(f"tank envelope map names unknown target: {target}")
        if recipe_name not in recipes:
            fail(f"tank envelope map recipe is missing: {recipe_name}")
        else:
            selected[target] = recipes[recipe_name]
    if not selected:
        fail("tank envelope report selected sample set is empty")
        return ""
    lines = [
        f"Tank envelope report: {len(manifest)} tank targets; {len(selected)} explicitly mapped recipes; "
        f"{len(recipes)} shipped recipes parsed.",
        "Static estimates are diagnostic only: module upgrade parents are not stacked, repeated slots are counted, "
        "and unknown engine order/caps/role bonuses remain annotated rather than treated as zero.",
    ]
    role_counts = Counter()
    for recipe in recipes.values():
        name = recipe["name"]
        role_counts["SPAA" if "SPAA" in name else "SPG" if "SPG" in name else "tank"] += 1
    lines.append(
        "Recipe role separation: "
        + ", ".join(f"{role}={role_counts[role]}" for role in ("tank", "SPAA", "SPG"))
        + "."
    )
    manifest_by_name = {row["name"]: row for row in manifest}
    for target in ENVELOPE_RECIPE_MAP:
        target_row = manifest_by_name[target]
        recipe = selected[target]
        values, unknown, reasons = _static_recipe_estimate(recipe)
        deltas = []
        target_metric_map = {
            "reliability": "reliability",
            "hardness": "hardness",
            "hard_attack": "hard_attack",
            "soft_attack": "soft_attack",
            "breakthrough": "breakthrough",
            "defense": "defense",
            "armor": "armor_value",
            "piercing": "ap_attack",
            "speed": "maximum_speed",
            "fuel_usage": "fuel_consumption",
            "production_cost": "build_cost_ic",
        }
        for metric, source_metric in target_metric_map.items():
            expected = target_row.get(metric)
            if expected is None:
                continue
            deltas.append(f"{metric}={_format_estimate(values[source_metric] - expected, metric)}")
        status = "UNKNOWN: " + "; ".join(sorted(unknown)) if unknown else "estimate"
        lines.append(f"- {target} <- {recipe['name']}: {status}; deltas " + ", ".join(deltas))
    unsampled = [row["name"] for row in manifest if row["name"] not in selected]
    lines.append(
        "Unsampled exact target generations: "
        + (", ".join(unsampled) if unsampled else "none")
        + ". No nearest-year recipe was silently substituted."
    )
    return "\n".join(lines)


def tank_balance_report() -> str:
    manifest = balance_manifest_rows()
    if not BALANCE_WORKBOOK_FILE.is_file():
        fail("tank balance workbook is missing for --tank-balance-report")
        return ""
    workbook_rows = read_balance_workbook(BALANCE_WORKBOOK_FILE)
    if len(manifest) != 40:
        fail(f"tank balance manifest has {len(manifest)} rows; expected 40")
    if len(workbook_rows) < 40:
        fail(f"tank balance workbook has {len(workbook_rows)} review rows; expected at least 40")
        return ""
    workbook_review = workbook_rows[:40]
    manifest_review = [(row, name, year) for row, name, _, year, _ in manifest]
    workbook_identity = [(row["row"], row["name"], row["year"]) for row in workbook_review]
    if manifest_review != workbook_identity:
        fail("tank balance manifest no longer matches workbook rows 2-41")
    manifest_values = balance_manifest_values()
    if len(manifest_values) != 40:
        fail(f"tank balance manifest has {len(manifest_values)} normalized value rows; expected 40")
    for manifest_row, workbook_row in zip(manifest_values, workbook_review):
        for metric, _, _ in BALANCE_METRICS:
            if manifest_row.get(metric) != workbook_row.get(metric):
                fail(
                    f"tank balance value mismatch at workbook row {workbook_row['row']}, "
                    f"field {metric}: {manifest_row.get(metric)!r} != {workbook_row.get(metric)!r}"
                )
    target_rows = [row for row in manifest if row[4] == "target"]
    reference_rows = [row for row in manifest if row[4] == "reference"]
    if len(target_rows) != 39 or len(reference_rows) != 1:
        fail("tank balance manifest must contain 39 targets and one reference row")
    if Counter(row[2] for row in target_rows) != Counter({"tank": 21, "mech": 18}):
        fail("tank balance manifest must contain 21 tank and 18 mechanized targets")
    years = Counter(row["year"] for row in workbook_review)
    return (
        f"Tank balance report: {len(workbook_review)} workbook rows parsed "
        f"(39 targets, 1 Abrams reference), {sum(years.values())} year entries; "
        f"scope manifest: {BALANCE_MANIFEST_FILE.relative_to(ROOT)}"
    )


def validate_tank_rework() -> None:
    armor_techs = dict(top_level_blocks(text(TECH_DIR / "NSB_armor.txt"), "technologies"))
    module_techs = dict(top_level_blocks(text(TECH_DIR / "NSB_armor_modules.txt"), "technologies"))
    all_tank_techs = {**armor_techs, **module_techs}

    for message in flame_grant_errors(all_tank_techs):
        fail(message)
    expected_chassis_techs: dict[str, set[str]] = {}
    for family, tier_count in FAMILY_TIERS.items():
        for tier in range(tier_count):
            technology = (
                "nsb_iw_armored_vehicles"
                if tier == 0
                else f"nsb_{'main_battle_tanks' if family == 'medium' else family + '_tanks'}{tier - 1}"
            )
            expected_chassis_techs.setdefault(technology, set()).add(
                f"{family}_tank_chassis_{tier}"
            )
            expected_chassis_techs[technology].update(
                f"{family}_tank_{role}_chassis_{tier}" for role in SUPPORTED_ROLES
            )
    for technology, expected in expected_chassis_techs.items():
        actual = {
            equipment
            for enable in top_level_named_blocks(all_tank_techs.get(technology, ""), "enable_equipments", technology)
            for equipment in listed_values(enable)
        }
        missing = expected - actual
        if missing:
            fail(f"{technology} is missing supported chassis grants: {sorted(missing)}")
    roles = text(TANK_ROLE_FILE)
    inactive_roles = sorted(
        {
            name
            for name in re.findall(r"(?m)^\t(\w+)\s*=\s*\{", roles)
            for block in keyed_blocks(roles, name)
            if re.search(r"\bactive\s*=\s*no\b", block)
        }
    )
    if inactive_roles:
        fail(
            "every tank role must stay active so non-NSB profiles keep them buildable; "
            f"inactive: {inactive_roles}"
        )
    if not set(re.findall(r"\b(?:light|medium|heavy)_flame_tank\b", roles)) >= {
        "light_flame_tank", "medium_flame_tank", "heavy_flame_tank"
    }:
        fail("base NSB armor technology no longer retains all flame subunit unlocks")

    definitions = {name: block for name, block in module_blocks if name != "limit"}
    for message in module_parent_errors(definitions):
        fail(message)

    chassis_text = text(CHASSIS_FILE)
    for invalid in (
        "sloped_armor", "amphibious_drive", "wet_ammo_storage", "squeezebore_adaptor",
        "armor_skirts", "dozer_blade", "easy_maintenance", "auto_loader", "stabilizer",
        "tank_radio_module", "tank_mobility_fuel",
    ):
        if re.search(rf"module_count_limit\s*=\s*\{{[^}}]*\b(?:module|category)\s*=\s*{re.escape(invalid)}\b", chassis_text, re.DOTALL):
            fail(f"tank chassis retains removed count limit {invalid}")

    for message in abbreviation_errors(definitions):
        fail(message)

    for module, technology in SECONDARY_MODULES.items():
        if module not in definitions:
            fail(f"secondary turret module is missing: {module}")
        if module not in unlocked_modules:
            fail(f"secondary turret module is not unlocked: {module}")
        if technology not in all_tank_techs:
            fail(f"secondary turret unlock technology is missing: {technology}")
        if module not in english_loc_keys or f"{module}_desc" not in english_loc_keys:
            fail(f"secondary turret localization is incomplete: {module}")
        icon_match = re.search(
            rf'name\s*=\s*"GFX_SMI_{re.escape(module)}"[\s\S]*?textureFile\s*=\s*"([^"]+)"',
            text(TANK_ICON_FILE),
        )
        if not icon_match:
            fail(f"secondary turret icon declaration is missing: {module}")
        elif icon_match.group(1) != SECONDARY_ICON_PATHS[module] or not (MOD / icon_match.group(1)).is_file():
            fail(f"secondary turret icon path is invalid: {module}")
        category = module_category(module)
        if category != "tank_secondary_turret":
            fail(f"secondary module {module} has category {category}, expected tank_secondary_turret")
    for message in secondary_unlock_errors(unlocked_modules):
        fail(message)

    chassis_blocks = dict(top_level_blocks(chassis_text, "equipments"))
    for archetype in ("light_tank_chassis", "medium_tank_chassis", "heavy_tank_chassis"):
        block = chassis_blocks.get(archetype, "")
        slots = [
            slot
            for index in range(1, 11)
            for slot in keyed_blocks(block, f"tank_special_slot_{index}")
        ]
        if len(slots) != 10:
            fail(f"{archetype} must retain ten specialized special slots")
        for message in tank_slot_layout_errors(block):
            fail(f"{archetype}: {message}")
        limits = re.findall(r"module_count_limit\s*=\s*\{([^{}]*)\}", block, re.DOTALL)
        if sum("category = tank_secondary_turret" in limit for limit in limits) != 1:
            fail(f"{archetype} must retain one secondary turret count limit")

    anti_air_expected = {
        "tank_anti_air_cannon": "18",
        "tank_anti_air_cannon_2": "32",
        "tank_anti_air_cannon_3": "46",
    }
    for module, expected in anti_air_expected.items():
        if not re.search(rf"{re.escape(module)}\s*=\s*\{{[\s\S]*?air_attack\s*=\s*{expected}\b", text(MODULE_FILE)):
            fail(f"{module} does not use the expected air attack value {expected}")
    turret_contract = {
        "pintle_turret": (0.5, 0.05, -0.1, 0.0),
        "light_lp_turret": (1.25, 0.10, 0.0, 0.05),
        "light_turret": (1.0, 0.15, 0.0, 0.0),
        "lp_turret": (1.5, 0.10, 0.0, 0.10),
        "conventional_turret": (1.5, 0.15, 0.05, 0.0),
        "oscillating_turret": (1.75, 0.05, 0.10, 0.0),
        "open_gun": (0.5, 0.10, -0.20, -0.10),
        "medium_open_gun": (0.75, 0.10, -0.20, -0.10),
        "heavy_open_gun": (1.0, 0.10, -0.20, -0.10),
        "external_gun": (1.25, 0.05, -0.05, 0.10),
        "fixed_superstructure": (0.75, 0.20, -0.15, 0.05),
        "medium_fixed_superstructure": (1.0, 0.20, -0.15, 0.05),
        "heavy_fixed_superstructure": (1.25, 0.20, -0.15, 0.05),
    }
    def stat_value(block: str, key: str) -> float:
        match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(-?\d+(?:\.\d+)?)\b", block)
        return 0.0 if match is None else float(match.group(1))
    for module, expected in turret_contract.items():
        block = definitions.get(module, "")
        add_stats = next(iter(keyed_blocks(block, "add_stats")), "")
        multiply_stats = next(iter(keyed_blocks(block, "multiply_stats")), "")
        actual = (
            stat_value(add_stats, "build_cost_ic"),
            stat_value(add_stats, "reliability"),
            stat_value(multiply_stats, "breakthrough"),
            stat_value(multiply_stats, "defense"),
        )
        if actual != expected:
            fail(f"{module} turret stats differ from the reviewed contract: {actual} != {expected}")
    superheavy = definitions.get("tank_super_heavy_cannon", "")
    if module_category("tank_super_heavy_cannon") != "tank_heavy_main_armament":
        fail("tank_super_heavy_cannon must use the heavy main armament category")

    for owner in sorted(tank_self_loop_ids(all_tank_techs)):
        fail(f"tank technology {owner} retains an active self-loop")
    tank_edges = {
        owner: [target for path in top_level_named_blocks(block, "path", owner)
                for target in direct_values(path, "leads_to_tech")]
        for owner, block in all_tank_techs.items()
    }
    visit_state: dict[str, int] = {}
    def visit(node: str) -> None:
        if visit_state.get(node, 0) == 1:
            fail(f"tank technology path graph contains a cycle at {node}")
            return
        if visit_state.get(node, 0) == 2:
            return
        visit_state[node] = 1
        for target in tank_edges.get(node, []):
            if target in all_tank_techs:
                visit(target)
            elif target not in technology_set:
                fail(f"tank technology {node} points to undefined technology {target}")
        visit_state[node] = 2
    for owner in all_tank_techs:
        visit(owner)

    variable_values: dict[str, str] = {}
    for path in (TECH_DIR / "NSB_armor.txt", TECH_DIR / "NSB_armor_modules.txt"):
        variable_values.update(dict(re.findall(r"(?m)^\s*(@[0-9]+)\s*=\s*([^\s#]+)", text(path))))
    gridbox_roots = {
        "nsb_armor_folder": ("nsb_iw_armored_vehicles", "nsb_engines", "nsb_armor"),
        "nsb_armor_modules_folder": ("nsb_light_guns", "nsb_ammo", "nsb_tank_design"),
    }
    tree_owner: dict[str, str] = {}
    for folder_name, roots in gridbox_roots.items():
        for root in roots:
            if root not in all_tank_techs:
                fail(f"{folder_name} gridbox root {root} is not a tank technology")
                continue
            seen = {root}
            stack = [root]
            while stack:
                node = stack.pop()
                for target in tank_edges.get(node, []):
                    if target in all_tank_techs and target not in seen:
                        seen.add(target)
                        stack.append(target)
            for member in seen:
                tree_owner.setdefault(member, root)
    positions: dict[str, dict[tuple[str, str, str], str]] = {
        "nsb_armor_folder": {},
        "nsb_armor_modules_folder": {},
    }
    for owner, block in all_tank_techs.items():
        folders = top_level_named_blocks(block, "folder", owner)
        if len(folders) != 1:
            fail(f"tank technology {owner} must have one folder placement")
            continue
        folder = folders[0]
        folder_name = direct_values(folder, "name")
        position = re.search(r"position\s*=\s*\{\s*x\s*=\s*([^\s}]+)\s*y\s*=\s*([^\s}]+)", folder)
        if not folder_name or not position or folder_name[0] not in positions:
            continue
        cell = tuple(variable_values.get(value, value) for value in position.groups())
        coordinate = (tree_owner.get(owner, owner), *cell)
        previous = positions[folder_name[0]].get(coordinate)
        if previous:
            fail(
                f"duplicate tank technology coordinate {cell} in {folder_name[0]} "
                f"gridbox {coordinate[0]}_tree: {previous} and {owner}"
            )
        positions[folder_name[0]][coordinate] = owner
    expected_years = {
        # QA 2026-09-06: raw GUI rows had hidden 1940/1942 research dates.
        "nsb_gt_engines0": ("1965", "@1965"),
        "nsb_gt_engines1": ("1975", "@1975"),
        "nsb_gt_engines2": ("1985", "@1985"),
        "nsb_gt_engines3": ("2005", "@2005"),
        "nsb_heavy_guns5": ("1985", "@1985"),
        "nsb_heavy_guns6": ("1995", "@1995"),
        "nsb_heavy_guns7": ("2010", "@2010"),
        "nsb_superheavy_guns1": ("1955", "@1955"),
        "nsb_heat_mp_ammo0": ("1985", "@1985"),
        "nsb_heat_mp_ammo1": ("1995", "@1995"),
        "nsb_heat_mp_ammo2": ("2005", "@2005"),
        "nsb_heat_du_ammo0": ("1985", "@1985"),
        "nsb_heat_du_ammo1": ("1995", "@1995"),
        "nsb_heat_du_ammo2": ("2005", "@2005"),
        "nsb_al_armor0": ("1955", "@1955"),
        "nsb_al_armor1": ("1965", "@1965"),
        "nsb_addon_armor0": ("1995", "@1995"),
        "nsb_addon_armor1": ("2005", "@2005"),
    }
    for owner, (year, y_position) in expected_years.items():
        block = all_tank_techs.get(owner, "")
        if direct_values(block, "start_year") != [year] or y_position not in block:
            fail(f"{owner} has the wrong start year or tree row")
    validate_tank_qa_contracts(all_tank_techs)

    role_ui = text(MOD / "interface/tank_designer_view.gui")
    if not re.search(r"name\s*=\s*\"dropdown_tank_roles\"[\s\S]*?size\s*=\s*\{\s*width\s*=\s*285\s+height\s*=\s*40", role_ui):
        fail("tank role selector dimensions changed")
    role_dropdowns = named_gui_blocks(role_ui, "dropDownBoxType", "dropdown_tank_roles", "tank_designer_view")
    role_windows = top_level_named_blocks(role_dropdowns[0], "expandedWindow", "dropdown_tank_roles") if role_dropdowns else []
    role_window = role_windows[0] if role_windows else ""
    if not role_window or "height=308" not in role_window or "verticalScrollbar = \"right_vertical_slider\"" not in role_window:
        fail("tank role selector lacks the bounded scrollable viewport")
    role_entry = next(iter(named_gui_blocks(role_ui, "containerWindowType", "tank_designer_role_entry", "tank_designer_view")), "")
    if "height = 50" not in role_entry:
        fail("tank role entries must remain 50 pixels high")
    research_ui = text(MOD / "interface/countrytechtreeview.gui")
    if 'name = "techtree_armour_folder_small_item"' not in research_ui:
        fail("legacy armor tree is missing its small-node template")
    modules_tab = re.search(r'name\s*=\s*"nsb_armor_modules_folder_tab"[\s\S]*?quadTextureSprite\s*=\s*"([^"]+)"', research_ui)
    if not modules_tab or modules_tab.group(1) != "GFX_artillery_folder_tab":
        fail("NSB armor modules tab does not use the artillery folder sprite")
    if len(list((MOD / "interface/equipmentdesigner/tanks").glob("tank_chassis_*_tank_amphibious*.gui"))) != 0:
        fail("orphan amphibious tank designer GUI files remain")

    variant_text = text(FOCUS_EFFECT_FILE)
    variants = export_variant_map(variant_text)
    for block in keyed_blocks(variant_text, "create_equipment_variant"):
        name_match = re.search(r"(?m)^\s*name\s*=\s*\"([^\"]+)\"", block)
        if name_match and ("allow_without_tech = yes" not in block or "parent_version = 0" not in block):
            fail(f"export variant {name_match.group(1)} lacks the stable no-tech contract")
        if name_match and "obsolete = yes" not in block:
            fail(f"export variant {name_match.group(1)} must be archived in its producer's production list")
    if variants != EXPORT_VARIANTS:
        fail(f"export variant map differs from contract: {variants}")
    for helper in EXPORT_VARIANTS:
        flag = re.sub(r"[^A-Za-z0-9]+", "_", helper).lower().strip("_") + "_created"
        if "set_country_flag = " + flag not in variant_text:
            fail(f"export variant {helper} lacks its producer flag guard")
    focus_contracts = {
        "BRA_american_tanks": ("nsb_main_battle_tanks2", "medium_tank_chassis_3", "CWIC Export Main Battle Tank 1950"),
        "BRA_soviet_tanks": ("nsb_main_battle_tanks2", "medium_tank_chassis_3", "CWIC Export Main Battle Tank 1950"),
        "GRE_heavy_weapons_tanks_arty": ("nsb_main_battle_tanks1", "medium_tank_chassis_2", "CWIC Export Main Battle Tank 1944"),
        "FIN_Acquire_Soviet_T55s": ("nsb_main_battle_tanks2", "medium_tank_chassis_3", "CWIC Export Main Battle Tank 1950"),
    }
    focus_stockpiles = {
        "BRA_american_tanks": (
            ("medium_tank_chassis_3", "CWIC Export Main Battle Tank 1950"),
            ("light_tank_chassis_1", "CWIC Export Light Tank 1942"),
            ("heavy_tank_chassis_2", "CWIC Export Heavy Tank 1944"),
        ),
        "BRA_soviet_tanks": (
            ("medium_tank_chassis_3", "CWIC Export Main Battle Tank 1950"),
            ("light_tank_chassis_1", "CWIC Export Light Tank 1942"),
            ("heavy_tank_chassis_2", "CWIC Export Heavy Tank 1944"),
        ),
        "GRE_heavy_weapons_tanks_arty": (
            ("light_tank_chassis_2", "CWIC Export Light Tank 1944"),
            ("medium_tank_chassis_2", "CWIC Export Main Battle Tank 1944"),
        ),
        "FIN_Acquire_Soviet_T55s": (
            ("medium_tank_chassis_3", "CWIC Export Main Battle Tank 1950"),
        ),
    }
    for path in FOCUS_FILES:
        focus_blocks = named_focus_blocks(text(path))
        for focus, (technology, chassis, variant) in focus_contracts.items():
            if focus not in focus_blocks:
                continue
            block = focus_blocks[focus]
            reward = next((reward for reward in keyed_blocks(block, "completion_reward") if "add_equipment_to_stockpile" in reward), "")
            nsb_branches = top_level_named_blocks(reward, "if", focus)
            legacy_branches = top_level_named_blocks(reward, "else_if", focus)
            if len(nsb_branches) != 1 or len(legacy_branches) != 1:
                fail(f"{focus} must have sibling designer and legacy reward branches")
            else:
                nsb_limit = top_level_named_blocks(nsb_branches[0], "limit", focus)[0]
                legacy_limit = top_level_named_blocks(legacy_branches[0], "limit", focus)[0]
                if 'has_dlc = "No Step Back"' not in nsb_limit or 'NOT = { has_dlc = "No Step Back" }' not in legacy_limit:
                    fail(f"{focus} rewards lack mutually exclusive DLC conditions")
            if technology not in block or chassis not in block or variant not in block:
                fail(f"{focus} lacks its NSB technology, chassis, or export variant branch")
            stockpile_blocks = keyed_blocks(block, "add_equipment_to_stockpile")
            for equipment_type, variant_name in focus_stockpiles[focus]:
                selected = any(
                    re.search(rf"\btype\s*=\s*{re.escape(equipment_type)}\b", stockpile)
                    and re.search(rf'\bvariant_name\s*=\s*"{re.escape(variant_name)}"', stockpile)
                    for stockpile in stockpile_blocks
                )
                if not selected:
                    fail(f"{focus} NSB stockpile does not select {variant_name}")
            legacy_tech = {
                "BRA_american_tanks": "main_battle_tanks_3",
                "BRA_soviet_tanks": "main_battle_tanks_3",
                "GRE_heavy_weapons_tanks_arty": "main_battle_tanks_2",
                "FIN_Acquire_Soviet_T55s": "main_battle_tanks_3",
            }[focus]
            if legacy_tech not in block:
                fail(f"{focus} no longer retains its legacy branch")


def validate_tank_qa_contracts(tank_techs: dict[str, str]) -> None:
    validate_national_tank_presets()
    path = MOD / "common/scripted_effects/CWIC_tank_bookmark_research.txt"
    brace_balance(path)
    effect = text(path)
    grants = keyed_blocks(effect, "set_technology")
    expected_nsb = {
        name for name, block in tank_techs.items()
        if name != "nsb_superheavy_guns1"
        and direct_values(block, "start_year")
        and int(direct_values(block, "start_year")[0]) <= 1980
    }
    legacy = dict(top_level_blocks(text(TECH_DIR / "armor.txt"), "technologies"))
    expected_legacy = {
        name for name, block in legacy.items()
        if re.fullmatch(r"iw_armored_vehicles|main_battle_tanks(?:_\d+)?|light_tanks_\d+|heavy_tanks_\d+", name)
        and direct_values(block, "start_year")
        and int(direct_values(block, "start_year")[0]) <= 1980
    }
    if len(grants) != 2 or 'limit = { has_dlc = "No Step Back" }' not in effect:
        fail("1980 major tank research must have two DLC-separated grant blocks")
    else:
        for grant, expected in zip(grants, (expected_nsb, expected_legacy)):
            actual = set(re.findall(r"(?m)^\s*(\w+)\s*=\s*1\s*$", grant))
            if actual != expected:
                fail(f"1980 tank research coverage differs: {sorted(actual ^ expected)}")
    for filename in ("USA - United States.txt", "SOV - Soviet union.txt"):
        history = text(HISTORY_DIR / filename)
        calls = "cwic_major_tank_research_1980 = yes"
        if history.count(calls) != 1 or not any(calls in block for block in keyed_blocks(history, "1980.1.1")):
            fail(f"{filename} must apply its tank research once in 1980 history")

    focus = named_focus_blocks(text(MOD / "common/national_focus/50s_FIN.txt"))["FIN_Acquire_Soviet_T55s"]
    available = keyed_blocks(focus, "available")[0]
    for pattern in (
        r'AND\s*=\s*\{\s*NOT\s*=\s*\{\s*has_dlc\s*=\s*"No Step Back"\s*\}\s*SOV\s*=\s*\{\s*has_tech\s*=\s*main_battle_tanks_3',
        r'AND\s*=\s*\{\s*has_dlc\s*=\s*"No Step Back"\s*SOV\s*=\s*\{\s*has_tech\s*=\s*nsb_main_battle_tanks2',
    ):
        if not re.search(pattern, available):
            fail("Finnish tank focus availability must pair producer research with the DLC profile")
    limits = keyed_blocks(focus, "limit")
    if len(limits) != 2 or 'has_dlc = "No Step Back"' not in limits[0] or 'NOT = { has_dlc = "No Step Back" }' not in limits[1]:
        fail("Finnish tank focus rewards must select mutually exclusive DLC branches")
    for helper in top_level_blocks("effects = {\n" + text(FOCUS_EFFECT_FILE) + "\n}", "effects"):
        if not top_level_named_blocks(helper[1], "hidden_effect", helper[0]):
            fail(f"export setup helper {helper[0]} must hide internal variant creation")
    for name, recipe in _variant_recipes().items():
        for slot, module in recipe["slots"]:
            match = re.fullmatch(r"tank_special_slot_(\d+)", slot)
            if match and module_category(module) not in TANK_SPECIAL_SLOT_CATEGORIES.get(int(match[1]), set()):
                fail(f"{name} places {module} in incompatible {slot}")
    for recipe in keyed_blocks(text(AI_FILE), "target_variant"):
        for slot, value in re.findall(r"(?m)^\s*(tank_special_slot_\d+)\s*=\s*(\w+)\s*$", recipe):
            if value == "empty":
                continue
            index = int(slot.rsplit("_", 1)[1])
            category = value if value in module_categories else module_category(value)
            if category not in TANK_SPECIAL_SLOT_CATEGORIES.get(index, set()):
                fail(f"AI recipe places {value} in incompatible {slot}")


def validate_national_tank_presets(national_override: str | None = None, generic_override: str | None = None) -> None:
    """Keep the named producer designs, bootstrap guards and manifest in sync."""
    brace_balance(NATIONAL_EFFECT_FILE)
    national = text(NATIONAL_EFFECT_FILE) if national_override is None else national_override
    generic = text(VARIANT_EFFECT_FILE) if generic_override is None else generic_override
    expected_pairs = {(tag, f"medium_tank_chassis_{tier}") for tag in ("USA", "SOV") for tier in range(7)}
    pairs = {(p["producer"], p["type"]) for p in NATIONAL_PRESETS}
    if len(NATIONAL_PRESETS) != 14 or pairs != expected_pairs:
        fail("national presets must cover exactly USA/SOV medium tiers 0-6")
    guards = keyed_blocks(national, "if")
    if len(guards) != len(NATIONAL_PRESETS):
        fail("national preset guard count differs from manifest")
    legacy_loc = text(MOD / "localisation/english/equipment_country_l_english.yml")
    for preset in NATIONAL_PRESETS:
        name, kind, tag = preset["name"], preset["type"], preset["producer"]
        matches = [g for g in guards if f'name = "{name}"' in g]
        if len(matches) != 1:
            fail(f"national preset {name} must occur exactly once")
            continue
        guard = matches[0]
        flag = f"cwic_starting_{kind}_created"
        for required in (f"tag = {tag}", f"has_tech = {preset['technology']}",
                         'has_dlc = "No Step Back"', f"NOT = {{ has_country_flag = {flag} }}",
                         f"set_country_flag = {flag}", f"type = {kind}",
                         "allow_without_tech = yes", "parent_version = 0",
                         "tank_engine_upgrade = 0", "tank_armor_upgrade = 0"):
            if required not in guard:
                fail(f"national preset {name} missing contract: {required}")
        blocks = keyed_blocks(guard, "modules")
        actual = re.findall(r"(?m)^\s*(\w+)\s*=\s*(\w+)\s*$", blocks[0]) if len(blocks) == 1 else []
        expected = {f"tank_special_slot_{i}": "empty" for i in range(1, 11)}
        expected.update(preset["modules"])
        if dict(actual) != expected or len(actual) != 15:
            fail(f"national preset {name} must match its manifest and explicitly fill/clear all 15 slots")
        if not re.search(rf'(?m)^\s*{re.escape(preset["legacy_name_key"])}:\d*\s*"{re.escape(name)}"', legacy_loc):
            fail(f"national preset {name} differs from existing country equipment name")
    for guard in keyed_blocks(generic, "if"):
        types = re.findall(r"\btype\s*=\s*(\w+)", guard)
        if len(types) != 1:
            continue
        kind = types[0]
        flag = f"cwic_starting_{kind}_created"
        if f"NOT = {{ has_country_flag = {flag} }}" not in guard or f"set_country_flag = {flag}" not in guard:
            fail(f"generic preset {kind} is not idempotent")
        if ("USA", kind) in pairs and "NOT = { OR = { tag = USA tag = SOV } }" not in guard:
            fail(f"generic preset {kind} must exclude national preset producers")
    if generic.find("cwic_create_national_tank_variants = yes") < 0 or generic.find("cwic_create_national_tank_variants = yes") > generic.find("create_equipment_variant ="):
        fail("national presets must bootstrap before generic presets")


def tank_slot_layout_errors(block: str) -> list[str]:
    errors = []
    for index, expected in TANK_SPECIAL_SLOT_CATEGORIES.items():
        slots = keyed_blocks(block, f"tank_special_slot_{index}")
        if len(slots) != 1:
            errors.append(f"slot {index} must occur exactly once")
            continue
        categories = keyed_blocks(slots[0], "allowed_module_categories")
        actual = set(re.findall(r"\btank_[a-z_]+\b", " ".join(categories)))
        if actual != expected:
            errors.append(f"slot {index} category mismatch: {sorted(actual ^ expected)}")
    return errors


def run_tank_negative_fixtures() -> None:
    """Exercise the tank contract's failure shapes without touching files."""
    for module, metric, expected in (("Radar_1", "fuel_consumption", 1.2), ("gl_atgm_2p", "hard_attack", 95)):
        adds, _, unknown = _effective_module_operations(module)
        if unknown or adds.get(metric) != expected:
            raise AssertionError(f"upgrade parent stats stacked for {module}")
    if bookmark_variant_name("medium_tank_chassis_3", "SOV") != "T-55":
        raise AssertionError("Soviet named preset lookup failed")
    if bookmark_variant_name("medium_tank_chassis_3", "FIN") != BOOKMARK_VARIANT_NAMES["medium_tank_chassis_3"]:
        raise AssertionError("national preset leaked into another producer")
    national = text(NATIONAL_EFFECT_FILE)
    generic = text(VARIANT_EFFECT_FILE)
    for label, mutated_national, mutated_generic in (
        ("wrong producer", national.replace("tag = USA", "tag = FIN", 1), generic),
        ("stale slot", national.replace("tank_special_slot_1 =", "special_type_slot_1 =", 1), generic),
        ("missing guard", national.replace("NOT = { has_country_flag", "NOT = { wrong_flag", 1), generic),
        ("duplicate generic", national, generic.replace("NOT = { OR = { tag = USA tag = SOV } }", "", 1)),
    ):
        previous_errors = len(errors)
        validate_national_tank_presets(mutated_national, mutated_generic)
        rejected_mutation = len(errors) > previous_errors
        del errors[previous_errors:]
        if not rejected_mutation:
            raise AssertionError(f"national preset mutation accepted: {label}")
    slots = "\n".join(
        f"tank_special_slot_{i} = {{ allowed_module_categories = {{ {' '.join(sorted(categories))} }} }}"
        for i, categories in TANK_SPECIAL_SLOT_CATEGORIES.items()
    )
    if tank_slot_layout_errors(slots):
        raise AssertionError("valid specialized slot layout rejected")
    if not tank_slot_layout_errors(slots.replace("tank_fcs_aiming", "tank_fcs_radar")):
        raise AssertionError("radar accepted in aiming slot")
    if not tank_slot_layout_errors(slots.replace("tank_protection_active", "")):
        raise AssertionError("unreachable active protection was accepted")
    parser_fixture = 'root = { child = { label = "quoted { brace }" } # ignored { }\n }'
    parsed = top_level_named_blocks(parser_fixture, "child", "fixture")
    if len(parsed) != 1 or 'label = "quoted { brace }"' not in parsed[0]:
        raise AssertionError("bounded parser failed quoted-brace/comment fixture")

    def rejected(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(f"tank negative fixture was accepted: {label}")

    armor_techs = dict(top_level_blocks(text(TECH_DIR / "NSB_armor.txt"), "technologies"))
    module_techs = dict(top_level_blocks(text(TECH_DIR / "NSB_armor_modules.txt"), "technologies"))
    all_tank_techs = {**armor_techs, **module_techs}

    missing_flame = dict(all_tank_techs)
    missing_flame["nsb_iw_armored_vehicles"] = re.sub(
        r"(?m)^\s*light_tank_flame_chassis_0\s*$", "",
        missing_flame["nsb_iw_armored_vehicles"],
    )
    rejected(bool(flame_grant_errors(missing_flame)), "missing flame grant")

    invalid_parent = {name: block for name, block in module_definitions.items() if name != "limit"}
    invalid_parent["fixture_invalid_parent"] = "fixture_invalid_parent = { parent = missing_parent }"
    rejected(bool(module_parent_errors(invalid_parent)), "invalid module parent")

    missing_secondary = unlocked_modules - {"cwic_secondary_autocannon"}
    rejected(bool(secondary_unlock_errors(missing_secondary)), "missing secondary unlock")

    abbreviation_fixture = {name: block for name, block in module_definitions.items() if name != "limit"}
    abbreviation_fixture["fixture_duplicate_abbreviation"] = (
        'fixture_duplicate_abbreviation = { abbreviation = "diesel0" }'
    )
    rejected(bool(abbreviation_errors(abbreviation_fixture)), "abbreviation collision")

    self_loop_fixture = dict(all_tank_techs)
    self_loop_fixture["fixture_self_loop"] = (
        "fixture_self_loop = { path = { leads_to_tech = fixture_self_loop } }"
    )
    rejected("fixture_self_loop" in tank_self_loop_ids(self_loop_fixture), "tank technology self-loop")

    variant_fixture = export_variant_map(text(FOCUS_EFFECT_FILE))
    variant_fixture["Undefined Export"] = "medium_tank_chassis_3"
    rejected(variant_fixture != EXPORT_VARIANTS, "undefined export variant")

    rejected(bool(missing_ammunition_categories({"tank_ammo_kinetic"})), "missing ammunition category")

    module_rows = _module_csv_rows(BALANCE_CSV_FILE)

    def fixture_must_fail(callback, label: str) -> None:
        before = len(errors)
        callback()
        if len(errors) == before:
            raise AssertionError(f"tank negative fixture was accepted: {label}")
        del errors[before:]

    def duplicate_module_fixture() -> None:
        if "flamethrower" in module_rows:
            fail("duplicate tank module ID in fixture CSV")

    fixture_must_fail(duplicate_module_fixture, "duplicate module ID")

    changed_numeric = list(module_rows["tank_anti_air_cannon"])
    changed_numeric[_csv_column_index("K")] = "2.25"
    fixture_must_fail(
        lambda: _compare_module_row(
            "tank_anti_air_cannon", changed_numeric,
            module_balance_record("tank_anti_air_cannon"), "fixture changed numeric"
        ),
        "changed numeric value",
    )

    confused_operation = list(module_rows["tank_gasoline_engine"])
    confused_operation[_csv_column_index("W")] = ""
    confused_operation[_csv_column_index("X")] = "0.5"
    fixture_must_fail(
        lambda: _compare_module_row(
            "tank_gasoline_engine", confused_operation,
            module_balance_record("tank_gasoline_engine"), "fixture operation"
        ),
        "operation confusion",
    )

    missing_value = list(module_rows["flamethrower"])
    missing_value[_csv_column_index("AJ")] = ""
    fixture_must_fail(
        lambda: _compare_module_row(
            "flamethrower", missing_value,
            module_balance_record("flamethrower"), "fixture missing value"
        ),
        "missing value",
    )

    malformed_numeric = list(module_rows["tank_anti_air_cannon"])
    malformed_numeric[_csv_column_index("AH")] = "not-a-number"
    fixture_must_fail(
        lambda: _compare_module_row(
            "tank_anti_air_cannon", malformed_numeric,
            module_balance_record("tank_anti_air_cannon"), "fixture malformed numeric"
        ),
        "malformed numeric value",
    )


def expected_tank_types() -> set[str]:
    result = set()
    for family, count in FAMILY_TIERS.items():
        for tier in range(count):
            result.add(f"{family}_tank_chassis_{tier}")
            result.update(
                f"{family}_tank_{role}_chassis_{tier}" for role in SUPPORTED_ROLES
            )
    return result


doctrine_files = [
    TECH_DIR / "land_doctrine.txt",
    TECH_DIR / "air_doctrine.txt",
    TECH_DIR / "naval_doctrine.txt",
]
key_files = doctrine_files + [
    TECH_DIR / "NSB_armor.txt",
    TECH_DIR / "NSB_armor_modules.txt",
    TECH_DIR / "armor.txt",
    TECH_DIR / "support.txt",
    MODULE_FILE,
    CHASSIS_FILE,
    MOD / "common/units/equipment/x_tank_chassis.txt",
    MOD / "common/units/CWIC-Special-Units.txt",
    AI_FILE,
    ENUM_FILE,
    VARIANT_EFFECT_FILE,
    FOCUS_EFFECT_FILE,
    TANK_ROLE_FILE,
    TANK_ICON_FILE,
    TANK_LOC_FILE,
    MOD / "interface/tank_designer_view.gui",
    MOD / "interface/countrytechtreeview.gui",
    *FOCUS_FILES,
]
for candidate in key_files:
    if candidate in doctrine_files and not candidate.is_file():
        continue
    brace_balance(candidate)

# Doctrine loader contract. The rework is either active in
# common/technologies/ or parked in common/technologies/doctrine rework/,
# which HOI4 does not load. Both are valid; a mix of the two is not.
parked_dir = TECH_DIR / "doctrine rework"
active_doctrine = [path for path in doctrine_files if path.is_file() and path.stat().st_size]
parked_doctrine = sorted(parked_dir.glob("*.txt")) if parked_dir.is_dir() else []
if active_doctrine and parked_doctrine:
    fail(
        "doctrine technologies exist both in common/technologies and in "
        "common/technologies/doctrine rework; the game would load only the active copy"
    )
elif active_doctrine and len(active_doctrine) != len(doctrine_files):
    missing = sorted(path.name for path in doctrine_files if path not in active_doctrine)
    fail(f"doctrine rework is active but incomplete; missing: {missing}")
elif not active_doctrine and not parked_doctrine:
    fail("doctrine technologies are neither active nor parked")

doctrine_root = MOD / "common/doctrines"
intentional_empty = {
    "grand_doctrines/air_grand_doctrines.txt",
    "grand_doctrines/land_grand_doctrines.txt",
    "grand_doctrines/sea_grand_doctrines.txt",
    "grand_doctrines/special_forces_grand_doctrines.txt",
    "tracks/air_doctrine_track.txt",
    "tracks/land_doctrine_tracks.txt",
    "tracks/sea_doctrine_tracks.txt",
    "tracks/special_forces_tracks.txt",
    "subdoctrines/air/air_fighter_aircraft_subdoctrines.txt",
    "subdoctrines/air/air_heavy_aircraft_subdoctrines.txt",
    "subdoctrines/air/air_medium_aircraft_subdoctrines.txt",
    "subdoctrines/air/air_strike_aircraft_subdoctrines.txt",
    "subdoctrines/land/armor_subdoctrines.txt",
    "subdoctrines/land/combat_support_subdoctrines.txt",
    "subdoctrines/land/infantry_subdoctrines.txt",
    "subdoctrines/land/operations_subdoctrines.txt",
    "subdoctrines/sea/navy_capital_subdoctrines.txt",
    "subdoctrines/sea/navy_carrier_doctrines.txt",
    "subdoctrines/sea/navy_screen_doctrines.txt",
    "subdoctrines/sea/navy_submarine_doctrines.txt",
    "subdoctrines/special_forces/special_forces_subdoctrines.txt",
}
actual_empty = {
    str(path.relative_to(doctrine_root))
    for path in doctrine_root.rglob("*.txt")
    if path.stat().st_size == 0
}
if actual_empty != intentional_empty:
    fail(
        "zero-byte doctrine override set changed: "
        f"missing={sorted(intentional_empty - actual_empty)}, "
        f"unexpected={sorted(actual_empty - intentional_empty)}"
    )

# Technology IDs, links, folders, and duplicate definitions.
technology_blocks: list[tuple[str, str, Path]] = []
for path in sorted(TECH_DIR.glob("*.txt")):
    technology_blocks.extend(
        (name, block, path) for name, block in top_level_blocks(text(path), "technologies")
    )
technology_ids = [name for name, _, _ in technology_blocks]
for name, count in Counter(technology_ids).items():
    if count > 1:
        fail(f"duplicate technology id: {name} ({count} definitions)")
technology_set = set(technology_ids)
for name, block, path in technology_blocks:
    for target in re.findall(r"\bleads_to_tech\s*=\s*([A-Za-z0-9_]+)", code_only(block)):
        checked_path_files = set(doctrine_files) | {
            TECH_DIR / "NSB_armor.txt",
            TECH_DIR / "NSB_armor_modules.txt",
        }
        if path in checked_path_files and target not in technology_set:
            fail(f"undefined technology path {name} -> {target} in {path.name}")

# A cross-decade path plus an allow prerequisite assigns the target to two grid
# boxes. The engine reports this as "multiple potential grid boxes" at startup.
land_blocks = {
    name: block
    for name, block, path in technology_blocks
    if path == TECH_DIR / "land_doctrine.txt"
}
for source, block in land_blocks.items():
    source_decade = re.search(r"_(\d{4})s_", source)
    if not source_decade:
        continue
    for target in re.findall(r"\bleads_to_tech\s*=\s*([A-Za-z0-9_]+)", code_only(block)):
        target_decade = re.search(r"_(\d{4})s_", target)
        target_block = code_only(land_blocks.get(target, ""))
        if (
            target_decade
            and source_decade.group(1) != target_decade.group(1)
            and re.search(rf"\bhas_tech\s*=\s*{re.escape(source)}\b", target_block)
        ):
            fail(
                "cross-decade doctrine path duplicates its allow prerequisite: "
                f"{source} -> {target}"
            )

doctrine_blocks = [
    (name, block, path)
    for name, block, path in technology_blocks
    if path in set(doctrine_files)
]
english_loc_keys = set()
for path in (MOD / "localisation/english").glob("*.yml"):
    english_loc_keys.update(
        re.findall(r"^\s*([A-Za-z0-9_.-]+):\d*\s", text(path), re.MULTILINE)
    )
for name, _, path in doctrine_blocks:
    if name not in english_loc_keys:
        fail(f"missing English doctrine name for {name} ({path.name})")
    if f"{name}_desc" not in english_loc_keys:
        fail(f"missing English doctrine description for {name} ({path.name})")

land_effect_patterns = (
    r"\bcategory_all_armor\s*=\s*\{",
    r"\bcategory_all_infantry\s*=\s*\{",
    r"\bartillery\s*=\s*\{",
    r"\brecon\s*=\s*\{",
    r"\bplanning_speed\s*=",
    r"\bsupply_consumption_factor\s*=",
)
for name, block, path in doctrine_blocks:
    if path == TECH_DIR / "land_doctrine.txt" and not any(
        re.search(pattern, code_only(block)) for pattern in land_effect_patterns
    ):
        fail(f"land doctrine has no gameplay effect: {name}")
if active_doctrine and re.search(
    r"\bdefence\s*=", code_only(text(TECH_DIR / "land_doctrine.txt"))
):
    fail("land doctrine uses rejected equipment stat spelling 'defence'; use 'defense'")

tag_text = code_only(text(MOD / "common/technology_tags/00_technology.txt"))
folder_ids = set(re.findall(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{", tag_text, re.MULTILINE))
for name, block, path in technology_blocks:
    for folder in re.findall(r"\bfolder\s*=\s*\{[\s\S]*?\bname\s*=\s*([A-Za-z0-9_]+)", code_only(block)):
        if folder not in folder_ids:
            fail(f"undefined technology folder {folder} used by {name} in {path.name}")

# Tank module definition/unlock/category contract.
module_blocks = top_level_blocks(text(MODULE_FILE), "equipment_modules")
module_ids = {name for name, _ in module_blocks if name != "limit"}
module_definitions = dict(module_blocks)
ammo_categories = {"tank_ammo_kinetic", "tank_ammo_he"}


def module_category(module: str) -> str:
    match = re.search(r"\bcategory\s*=\s*(\w+)", module_definitions.get(module, ""))
    return match.group(1) if match else ""


def needs_ammunition(module: str) -> bool:
    # Conventional guns multiply attack supplied by ammunition. AA guns and
    # flamethrowers supply their own attack and do not need shell modules.
    return any(
        re.search(r"\b(?:soft_attack|hard_attack|ap_attack)\s*=", block)
        for block in keyed_blocks(module_definitions.get(module, ""), "multiply_stats")
    )

module_categories = {
    match.group(1)
    for _, block in module_blocks
    if (match := re.search(r"^\s*category\s*=\s*([A-Za-z0-9_]+)", block, re.MULTILINE))
}
unlocked_modules = set()
for _, block, path in technology_blocks:
    if path not in {TECH_DIR / "NSB_armor.txt", TECH_DIR / "NSB_armor_modules.txt"}:
        continue
    for match in re.finditer(r"enable_equipment_modules\s*=\s*\{([^}]*)\}", code_only(block), re.DOTALL):
        for module in re.findall(r"\b[A-Za-z][A-Za-z0-9_]*\b", match.group(1)):
            unlocked_modules.add(module)
            if module not in module_ids:
                fail(f"undefined equipment module unlocked in {path.name}: {module}")
dead_modules = module_ids - unlocked_modules
if dead_modules:
    fail(f"unreachable tank modules remain: {sorted(dead_modules)}")

allowed_categories = set()
for match in re.finditer(
    r"allowed_module_categories\s*=\s*\{([^}]*)\}",
    code_only(text(CHASSIS_FILE)),
    re.DOTALL,
):
    allowed_categories.update(re.findall(r"\b[A-Za-z][A-Za-z0-9_]*\b", match.group(1)))
missing_categories = allowed_categories - module_categories
if missing_categories:
    fail(f"chassis allow module categories with no live module: {sorted(missing_categories)}")

for required in {
    "flamethrower",
    "tank_anti_air_cannon",
    "tank_anti_air_cannon_2",
    "tank_anti_air_cannon_3",
}:
    if required not in module_ids:
        fail(f"required retained-role module is missing: {required}")

# Supported types, OOB references, AI historical designs, and removed roles.
expected_types = expected_tank_types()
chassis_text = text(CHASSIS_FILE)
base_types = set(
    re.findall(r"^\s*((?:light|medium|heavy)_tank_chassis_[0-9]+)\s*=\s*\{", chassis_text, re.MULTILINE)
)
expected_base = {name for name in expected_types if re.match(r"^(light|medium|heavy)_tank_chassis_", name)}
if base_types != expected_base:
    fail(f"base tank chassis set differs from contract: {sorted(base_types ^ expected_base)}")

oob_refs: set[str] = set()
oob_required_techs: dict[str, set[str]] = {}
foreign_producer_techs: dict[tuple[str, str], set[str]] = {}
oob_files_with_tanks: list[Path] = []
versioned_oob_requests = 0
for path in sorted(OOB_DIR.glob("*_nsb.txt")):
    value = code_only(text(path))
    refs = set(OOB_TANK_PATTERN.findall(value))
    if not refs:
        continue
    oob_files_with_tanks.append(path)
    oob_refs.update(refs)
    brace_balance(path)
    if STARTING_VARIANT_EFFECT in value:
        fail(
            f"{path.name} bootstraps variants inside the OOB; the bootstrap must run "
            "in country history before set_oob"
        )
    oob_required_techs[path.stem] = {
        BOOKMARK_VARIANT_TECHS[ref] for ref in refs if ref in BOOKMARK_VARIANT_TECHS
    }
    # A tank bought from or designed by another tag is created by that tag, so
    # its chassis technology belongs to that tag's bookmark bootstrap rather
    # than this OOB's.
    era = path.stem.split("_")[1]

    def record_creator(block: str, refs: list[str]) -> None:
        creator = FOREIGN_CREATOR_PATTERN.search(code_only(block))
        if not creator:
            return
        for ref in refs:
            if ref in BOOKMARK_VARIANT_TECHS:
                foreign_producer_techs.setdefault((creator.group(1), era), set()).add(
                    BOOKMARK_VARIANT_TECHS[ref]
                )

    for effect in ("add_equipment_to_stockpile", "add_equipment_production"):
        for block in keyed_blocks(value, effect):
            record_creator(block, OOB_TANK_PATTERN.findall(block))
    for block in keyed_blocks(value, "force_equipment_variants"):
        for tank_type in set(OOB_TANK_PATTERN.findall(block)):
            for variant_request in keyed_blocks(block, tank_type):
                record_creator(variant_request, [tank_type])

    for effect, field in (
        ("add_equipment_production", "version_name"),
        ("add_equipment_to_stockpile", "variant_name"),
    ):
        for block in keyed_blocks(value, effect):
            type_match = re.search(
                r"\btype\s*=\s*([A-Za-z0-9_]+)", code_only(block)
            )
            if not type_match or type_match.group(1) not in BOOKMARK_VARIANT_NAMES:
                continue
            tank_type = type_match.group(1)
            name_match = re.search(
                rf'\b{field}\s*=\s*"([^"]+)"', code_only(block)
            )
            if not name_match:
                fail(
                    f"{path.name} {effect} request for {tank_type} does not select "
                    f"an explicit variant with {field}"
                )
            elif name_match.group(1) != bookmark_variant_name(tank_type, oob_variant_producer(block, path.stem[:3])):
                fail(
                    f"{path.name} {effect} request asks for {tank_type} variant "
                    f"{name_match.group(1)!r}, which no bootstrap creates"
                )
            versioned_oob_requests += 1

    for block in keyed_blocks(value, "force_equipment_variants"):
        for tank_type in BOOKMARK_VARIANT_NAMES:
            for variant_request in keyed_blocks(block, tank_type):
                name_match = re.search(
                    r'\bversion_name\s*=\s*"([^"]+)"',
                    code_only(variant_request),
                )
                if not name_match:
                    fail(
                        f"{path.name} forced variant request for {tank_type} does not "
                        "select an explicit version_name"
                    )
                elif name_match.group(1) != bookmark_variant_name(tank_type, oob_variant_producer(variant_request, path.stem[:3])):
                    fail(
                        f"{path.name} forced variant request asks for {tank_type} "
                        f"variant {name_match.group(1)!r}, which no bootstrap creates"
                    )
                versioned_oob_requests += 1
invalid_oob = oob_refs - expected_types
if invalid_oob:
    fail(f"NSB OOBs reference invalid tank types: {sorted(invalid_oob)}")

# The bootstrap must run in country history immediately before the matching
# set_oob, because an OOB-local instant_effect resolves after that OOB's
# version-sensitive requests.
history_bootstrap_sites = 0
set_oob_pattern = re.compile(r'^([ \t]*)set_oob = "([A-Za-z0-9_]+_nsb)"[ \t]*$', re.MULTILINE)
bootstrapped_oobs: set[str] = set()
bootstrapped_files: set[Path] = set()
for path in sorted(HISTORY_DIR.glob("*.txt")):
    value = text(path)
    tag_match = re.match(r"([A-Z]{3}) - ", path.name)
    tag = tag_match.group(1) if tag_match else ""
    if tag in MANUFACTURER_BLOC_TAGS and STARTING_VARIANT_EFFECT not in value:
        fail(
            f"{path.name} sells tanks to 1980 OOBs but never creates its variants"
        )
    for match in set_oob_pattern.finditer(value):
        indent, oob = match.group(1), match.group(2)
        if oob not in oob_required_techs:
            continue
        bootstrapped_oobs.add(oob)
        bootstrapped_files.add(path)
        history_bootstrap_sites += 1
        required = oob_required_techs[oob] | foreign_producer_techs.get(
            (tag, oob.split("_")[1]), set()
        )
        expected = "\n".join(
            [
                f"{indent}# Starting tank variants must exist before the OOB is loaded.",
                f"{indent}set_technology = {{",
                *(f"{indent}\t{tech} = 1" for tech in sorted(required)),
                f"{indent}\tpopup = no",
                f"{indent}}}",
                f"{indent}{STARTING_VARIANT_EFFECT}",
                "",
            ]
        )
        if not value[: match.start()].endswith(expected):
            fail(
                f"{path.name} does not bootstrap the required chassis technologies and "
                f"starting variants immediately before set_oob = \"{oob}\""
            )
missing_bootstrap = set(oob_required_techs) - bootstrapped_oobs
if missing_bootstrap:
    fail(f"NSB OOBs are never loaded from country history: {sorted(missing_bootstrap)}")
unbootstrapped_producers = {
    producer
    for producer, _ in foreign_producer_techs
    if producer not in MANUFACTURER_BLOC_TAGS
    and not any(path.name.startswith(f"{producer} - ") for path in bootstrapped_files)
}
if unbootstrapped_producers:
    fail(
        "OOBs buy tanks from tags that never create variants: "
        f"{sorted(unbootstrapped_producers)}"
    )

variant_effect_text = text(VARIANT_EFFECT_FILE)
variant_blocks = keyed_blocks(variant_effect_text, "create_equipment_variant")
variant_guard_techs: dict[str, list[str]] = {}
for guarded_block in keyed_blocks(variant_effect_text, "if"):
    guarded_variants = keyed_blocks(guarded_block, "create_equipment_variant")
    if len(guarded_variants) != 1:
        fail("each starting tank variant guard must contain exactly one variant")
        continue
    guarded_type = re.search(
        r"^\s*type\s*=\s*([A-Za-z0-9_]+)",
        guarded_variants[0],
        re.MULTILINE,
    )
    if guarded_type:
        variant_guard_techs[guarded_type.group(1)] = re.findall(
            r"\bhas_tech\s*=\s*([A-Za-z0-9_]+)", guarded_block
        )
variant_types: list[str] = []
for block in variant_blocks:
    type_match = re.search(r"^\s*type\s*=\s*([A-Za-z0-9_]+)", block, re.MULTILINE)
    if not type_match:
        fail("starting tank create_equipment_variant block has no type")
        continue
    variant_type = type_match.group(1)
    variant_types.append(variant_type)
    name_match = re.search(r'^\s*name\s*=\s*"([^"]+)"', block, re.MULTILINE)
    if not name_match or name_match.group(1) != BOOKMARK_VARIANT_NAMES.get(variant_type):
        fail(
            f"starting variant {variant_type} does not use its stable bookmark name"
        )
    if not re.search(r"^\s*allow_without_tech\s*=\s*yes\b", block, re.MULTILINE):
        fail(
            f"starting variant {variant_type} can be skipped before OOB tech state settles"
        )
    slots = set(
        re.findall(
            r"^\s*([A-Za-z0-9_]+_slot(?:_[0-9]+)?)\s*=\s*([A-Za-z0-9_]+)",
            block,
            re.MULTILINE,
        )
    )
    slot_names = {slot for slot, _ in slots}
    if not REQUIRED_VARIANT_SLOTS <= slot_names:
        fail(
            f"starting variant {variant_type} has wrong required slots: "
            f"{sorted(slot_names)}"
        )
    for _, module in slots:
        if module not in module_ids:
            fail(f"starting variant {variant_type} uses undefined module {module}")
    if needs_ammunition(dict(slots).get("main_armament_slot", "")):
        installed_categories = {module_category(module) for _, module in slots}
        if missing_ammunition_categories(installed_categories):
            fail(f"starting variant {variant_type} lacks attack-producing AP/HE ammunition")
    variant_techs = variant_guard_techs.get(variant_type, [])
    if variant_techs != [BOOKMARK_VARIANT_TECHS.get(variant_type)]:
        fail(f"starting variant {variant_type} has the wrong chassis technology guard")
    for tech in variant_techs:
        if tech not in technology_set:
            fail(f"starting variant {variant_type} is gated by undefined tech {tech}")
if len(variant_types) != len(set(variant_types)):
    duplicates = sorted(
        name for name, count in Counter(variant_types).items() if count > 1
    )
    fail(f"duplicate starting tank variant types: {duplicates}")
if set(variant_types) != oob_refs:
    fail(
        "starting tank variant set differs from NSB OOB references: "
        f"missing={sorted(oob_refs - set(variant_types))}, "
        f"unused={sorted(set(variant_types) - oob_refs)}"
    )
if set(variant_types) != set(BOOKMARK_VARIANT_NAMES):
    fail(
        "starting tank variant name map differs from created variants: "
        f"missing={sorted(set(variant_types) - set(BOOKMARK_VARIANT_NAMES))}, "
        f"unused={sorted(set(BOOKMARK_VARIANT_NAMES) - set(variant_types))}"
    )
if set(BOOKMARK_VARIANT_TECHS) != set(BOOKMARK_VARIANT_NAMES):
    fail("starting tank variant technology map differs from its name map")

ai_text = code_only(text(AI_FILE))
ai_types = set(re.findall(r"^\s*type\s*=\s*([A-Za-z0-9_]+)", ai_text, re.MULTILINE))
missing_ai = expected_types - ai_types
if missing_ai:
    fail(f"tank types without a generic historical AI design: {sorted(missing_ai)}")
if len(re.findall(r"^\s*history\s*=\s*yes\b", ai_text, re.MULTILINE)) != len(expected_types) + len(APC_HULL_ROWS):
    fail("generic tank AI file must contain one historical recipe per supported tank and APC type")
for recipe in keyed_blocks(ai_text, "target_variant"):
    type_match = re.search(r"\btype\s*=\s*(\w+)", recipe)
    if not type_match:
        continue
    equipment_type = type_match.group(1)
    if re.search(r"_(?:aa|flame)_chassis_", equipment_type):
        continue
    # APC hulls mount troop-compartment armament, never a gun that multiplies
    # ammunition stats, so shell modules do not apply to them.
    if equipment_type.startswith("apc_chassis_"):
        continue
    for category in ammo_categories:
        if not re.search(rf"\btank_special_slot_\d+\s*=\s*{category}\b", recipe):
            fail(f"AI recipe {equipment_type} lacks attack-producing {category}")
for enable in keyed_blocks(ai_text, "enable"):
    # Every cannon recipe must wait for the two ammunition research unlocks.
    # AA/flame recipes share the same chassis gates, so check the count below.
    if "nsb_ammo" in enable and "nsb_he_ammo0" not in enable:
        fail("AI ammunition prerequisite omits HE research")
if len(re.findall(r"\bhas_tech\s*=\s*nsb_he_ammo0\b", ai_text)) != 75:
    fail("all 75 conventional-gun AI recipes must require ammunition research")

active_roots = [MOD / "common", MOD / "interface"]
for path_root in active_roots:
    for path in path_root.rglob("*"):
        if not path.is_file() or path.suffix not in {".txt", ".gui", ".gfx", ".info"}:
            continue
        value = code_only(text(path))
        for identifier in UNSUPPORTED_IDS:
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(identifier)}(?![A-Za-z0-9_])", value):
                fail(f"unsupported id {identifier} remains in {path.relative_to(MOD)}")

enum_text = code_only(text(ENUM_FILE))
stale_generated_enums = (
    r"light_tank_artillery_chassisbt_equipment_[0-9]+",
    r"light_tank_rocket_chassist_equipment_[0-9]+",
    r"medium_tank_heavy_artillery_chassisbt_equipment_[0-9]+",
    r"medium_tank_rocket_chassisbt_equipment_[0-9]+",
    r"heavy_tank_rocket_chassist_equipment_[0-9]+",
)
for tier in range(len(APC_HULL_ROWS)):
    # equipment_database.cpp:656 logs every equipment id missing from this
    # documentation enum. QA 2026-09-07 saw eight such lines for the APC hulls.
    if not re.search(rf"(?m)^\s*apc_chassis_{tier}\s*$", enum_text):
        fail(f"apc_chassis_{tier} is missing from script_enum_equipment_bonus_type")

for pattern in stale_generated_enums:
    if re.search(rf"^\s*{pattern}\s*$", enum_text, re.MULTILINE):
        fail(f"stale generated tank enum remains: {pattern}")
for tier in range(1, 7):
    expected_enum = f"light_tank_artillery_chassist_equipment_{tier}"
    if not re.search(rf"^\s*{expected_enum}\s*$", enum_text, re.MULTILINE):
        fail(f"generated tank enum is missing: {expected_enum}")

# UI and corrected shared progression checks.
ui_text = text(MOD / "interface/tank_designer_view.gui")
positions = set(
    int(value)
    for value in re.findall(r'pos_custom_module_slot_window_(\d+)"', ui_text)
)
if positions != set(range(15)):
    fail(f"tank designer slot positions must be exactly 0-14, found {sorted(positions)}")

support_text = code_only(text(TECH_DIR / "support.txt"))
for tier in range(1, 8):
    name = "tech_armor_engineers" if tier == 1 else f"tech_armor_engineers{tier}"
    block = next((value for tech, value, _ in technology_blocks if tech == name), "")
    if "allow =" not in block or "nsb_main_battle_tanks" not in block:
        fail(f"{name} does not allow an NSB MBT prerequisite")
    if re.search(r"dependencies\s*=\s*\{[^}]*\bmain_battle_tanks", block, re.DOTALL):
        fail(f"{name} still has a cumulative legacy-only MBT dependency")

armor_text = code_only(text(TECH_DIR / "armor.txt"))
for tier in range(1, 6):
    name = f"amphibious{tier}"
    block = next((value for tech, value, _ in technology_blocks if tech == name), "")
    if "name = armour_folder" not in block or "name = nsb_armor_folder" not in block:
        fail(f"{name} is not exposed in both armor folder configurations")
if not re.search(r"mechanized_marine\s*=\s*\{[\s\S]*?\bactive\s*=\s*no", code_only(text(MOD / "common/units/CWIC-Special-Units.txt"))):
    fail("mechanized_marine must be technology-gated (active = no)")

validate_doctrine_rework()
if "--doctrine-self-test" in sys.argv:
    run_doctrine_negative_fixtures()
validate_tank_rework()
if "--tank-self-test" in sys.argv:
    run_tank_negative_fixtures()


def designer_window_names() -> set[str]:
    names: set[str] = set()
    for path in sorted((MOD / "interface/equipmentdesigner/tanks").glob("*.gui")):
        names.update(re.findall(r'name\s*=\s*"(equipment_designer_[A-Za-z0-9_]+)"', code_only(text(path))))
    return names


def validate_designer_window_coverage(window_override: set[str] | None = None) -> None:
    """Every designable hull must resolve an equipment designer window.

    QA 2026-09-06: apc_chassis_* shipped with module slots but no designer window,
    and the production view silently fell back to the legacy Create Variant upgrade
    popup instead of the module designer. Per
    interface/equipmentdesigner/_documentation.info the window is resolved as
    equipment_designer_<EQUIPMENT>[_TAG] then equipment_designer_<ARCHETYPE>[_TAG],
    so a missing window is a silent, non-erroring downgrade. This check makes that
    class of failure loud for every future designer family.
    """
    windows = designer_window_names() if window_override is None else window_override
    designable: dict[str, str] = {}
    for source in (CHASSIS_FILE, MECHANIZED_FILE):
        for name, block in top_level_blocks(text(source), "equipments"):
            if direct_values(block, "module_slots") != ["inherit"]:
                continue
            parents = direct_values(block, "archetype")
            designable[name] = parents[0] if parents else name
    duplicates = {
        name: direct_values(block, "archetype")[0]
        for name, block in top_level_blocks(
            text(MOD / "common/units/equipment/x_tank_chassis.txt"), "duplicate_archetypes"
        )
        if direct_values(block, "archetype")
    }
    if not designable:
        fail("no designable hulls were found for designer window coverage")
    for equipment, archetype in sorted(designable.items()):
        wanted = {f"equipment_designer_{equipment}", f"equipment_designer_{archetype}"}
        wanted.update(
            f"equipment_designer_{duplicate}"
            for duplicate, parent in duplicates.items()
            if parent == archetype
        )
        if not (wanted & windows):
            fail(
                f"{equipment} has designer module slots but no designer window; "
                f"the production view would fall back to the legacy upgrade popup"
            )
    for duplicate, archetype in sorted(duplicates.items()):
        if f"equipment_designer_{duplicate}" not in windows:
            fail(f"duplicate role archetype {duplicate} has no designer window")


def validate_apc_designer_family() -> None:
    """Contract for the APC designer family carried on mechanized_equipment.

    The hulls deliberately share the legacy archetype so that mechanized,
    marine-support and support-company sub-units resolve designer personnel
    carriers with no `need` change. That only stays safe while the legacy rows
    keep no module slots of their own, so non-NSB games are unaffected.
    """
    brace_balance(MECHANIZED_FILE)
    blocks = dict(top_level_blocks(text(MECHANIZED_FILE), "equipments"))

    archetype = blocks.get("mechanized_equipment", "")
    if not archetype:
        fail("mechanized_equipment archetype is missing")
        return
    special = [
        slot
        for index in range(1, 11)
        for slot in keyed_blocks(archetype, f"tank_special_slot_{index}")
    ]
    if len(special) != 10:
        fail("APC archetype must expose the ten shared specialized special slots")
    for message in tank_slot_layout_errors(archetype):
        fail(f"mechanized_equipment: {message}")
    for slot, expected in (
        ("turret_type_slot", {"tank_apc_superstructure"}),
        ("main_armament_slot", {"tank_apc_armament"}),
    ):
        found = keyed_blocks(archetype, slot)
        categories = set(
            re.findall(r"\btank_[a-z_]+\b", " ".join(keyed_blocks(found[0], "allowed_module_categories")))
        ) if len(found) == 1 else set()
        if categories != expected:
            fail(f"APC {slot} must be restricted to {sorted(expected)}, found {sorted(categories)}")
        if len(found) == 1 and "required = yes" not in found[0]:
            fail(f"APC {slot} must stay mandatory")
    defaults = keyed_blocks(archetype, "default_modules")
    default_map = dict(re.findall(r"(?m)^\s*(\w+)\s*=\s*(\w+)\s*$", defaults[0])) if len(defaults) == 1 else {}
    if set(default_map) != {
        "main_armament_slot", "turret_type_slot", "suspension_type_slot",
        "armor_type_slot", "engine_type_slot",
    }:
        fail("APC archetype must give every mandatory slot a default module")
    if default_map.get("turret_type_slot") not in APC_SUPERSTRUCTURE_MODULES:
        fail("APC default turret module is not an APC superstructure")
    if default_map.get("main_armament_slot") not in APC_ARMAMENT_MODULES:
        fail("APC default armament is not APC armament")
    limits = re.findall(r"module_count_limit\s*=\s*\{([^{}]*)\}", archetype, re.DOTALL)
    if sum("category = tank_secondary_turret" in limit for limit in limits) != 1:
        fail("APC archetype must retain one secondary turret count limit")
    # QA 2026-09-06: the designer is chosen from the equipment domain. Without
    # `armor` the production view opens the legacy land upgrade popup instead of
    # tank_designer_view; without `mechanized` the archetype loses its land and
    # transport classification for the AI and for `transport = mechanized_equipment`.
    archetype_domain = set(re.findall(r"\w+", " ".join(direct_values(archetype, "type")) or ""))
    if not archetype_domain:
        archetype_domain = set(re.findall(r"(?m)^\s*type\s*=\s*\{([^}]*)\}", archetype))
        archetype_domain = set(re.findall(r"\w+", " ".join(archetype_domain)))
    if archetype_domain != {"armor", "mechanized"}:
        fail(f"APC archetype domain must be armor plus mechanized, found {sorted(archetype_domain)}")

    # Legacy rows must stay plain equipment so non-NSB games are untouched.
    for tier in range(1, 11):
        legacy = blocks.get(f"mechanized_equipment_{tier}", "")
        if not legacy:
            fail(f"legacy mechanized_equipment_{tier} is missing")
        elif "module_slots" in code_only(legacy):
            fail(f"legacy mechanized_equipment_{tier} must not inherit designer slots")

    tech_text = code_only(text(TECH_DIR / "NSB_armor.txt"))
    legacy_folder_text = code_only(text(TECH_DIR / "armor.txt"))
    for tier, (legacy_row, technology, year) in APC_HULL_ROWS.items():
        hull = blocks.get(f"apc_chassis_{tier}", "")
        if not hull:
            fail(f"apc_chassis_{tier} is missing")
            continue
        if direct_values(hull, "archetype") != ["mechanized_equipment"]:
            fail(f"apc_chassis_{tier} must share the mechanized_equipment archetype")
        hull_domain = set(re.findall(r"\w+", " ".join(re.findall(r"(?m)^\s*type\s*=\s*\{([^}]*)\}", hull))))
        if hull_domain != {"armor", "mechanized"}:
            fail(f"apc_chassis_{tier} must restate the armor/mechanized domain, found {sorted(hull_domain)}")
        if direct_values(hull, "module_slots") != ["inherit"]:
            fail(f"apc_chassis_{tier} must inherit the APC designer slots")
        if direct_values(hull, "derived_variant_name") != [f"apc_equipment_{tier}"]:
            fail(f"apc_chassis_{tier} has the wrong derived variant name")
        if direct_values(hull, "year") != [str(year)]:
            fail(f"apc_chassis_{tier} year differs from the {legacy_row} row it replaces")
        produced = keyed_blocks(hull, "can_be_produced")
        if len(produced) != 1 or 'has_dlc = "No Step Back"' not in produced[0]:
            fail(f"apc_chassis_{tier} must be gated behind No Step Back")
        expected_parent = [] if tier == 0 else [f"apc_chassis_{tier - 1}"]
        if direct_values(hull, "parent") != expected_parent:
            fail(f"apc_chassis_{tier} has a broken hull upgrade chain")
        legacy = blocks.get(legacy_row, "")
        for stat in ("armor_value",):
            hull_value = direct_values(hull, stat)
            legacy_value = direct_values(legacy, stat)
            if hull_value != legacy_value:
                fail(
                    f"apc_chassis_{tier} {stat} {hull_value} drifts from frozen "
                    f"{legacy_row} {legacy_value}"
                )
        if not re.search(rf"\benable_equipments\s*=\s*\{{[^}}]*\bapc_chassis_{tier}\b", tech_text, re.DOTALL):
            fail(f"apc_chassis_{tier} is not unlocked by an NSB technology")
        if technology not in technology_set:
            fail(f"APC hull technology {technology} is undefined")
        if re.search(rf"\b{technology}\b", legacy_folder_text):
            fail(f"{technology} leaks into the legacy armour folder")
        # QA 2026-09-07: the APC column first shipped on raw folder rows copied from
        # the mechanized line, which sit on a different scale than the @year macros
        # used by every other NSB armour column. The tree then drew "1947 APC" on the
        # 1955 row. Pin each hull technology to the year row its start_year claims.
        tech_block = dict(top_level_blocks(text(TECH_DIR / "NSB_armor.txt"), "technologies")).get(technology, "")
        if direct_values(tech_block, "start_year") != [str(year)]:
            fail(f"{technology} start_year differs from the {legacy_row} row it replaces")
        row = re.search(r"nsb_armor_folder\s*}?\s*position\s*=\s*\{[^}]*y\s*=\s*(@?[0-9]+)", tech_block)
        if not row:
            row = re.search(r"position\s*=\s*\{[^}]*y\s*=\s*(@?[0-9]+)", tech_block)
        if not row or row.group(1) != f"@{year}":
            fail(
                f"{technology} sits on tree row {row.group(1) if row else 'none'}, "
                f"expected the @{year} year row"
            )

    for module, category in (
        [(name, "tank_apc_superstructure") for name in APC_SUPERSTRUCTURE_MODULES]
        + [(name, "tank_apc_armament") for name in APC_ARMAMENT_MODULES]
    ):
        if module not in module_ids:
            fail(f"APC module {module} is missing")
            continue
        if module_category(module) != category:
            fail(f"APC module {module} has category {module_category(module)}, expected {category}")
        if needs_ammunition(module):
            fail(f"APC module {module} multiplies gun stats and would need ammunition")

    apc_recipes = [
        recipe for recipe in keyed_blocks(ai_text, "target_variant")
        if re.search(r"\btype\s*=\s*apc_chassis_\d+", recipe)
    ]
    if len(apc_recipes) != len(APC_HULL_ROWS):
        fail("every APC hull needs one generic historical AI recipe")
    for recipe in apc_recipes:
        tier = int(re.search(r"\btype\s*=\s*apc_chassis_(\d+)", recipe).group(1))
        if "turret_type_slot = tank_apc_superstructure" not in recipe:
            fail(f"APC AI recipe {tier} does not use the APC superstructure category")
        if "main_armament_slot = tank_apc_armament" not in recipe:
            fail(f"APC AI recipe {tier} does not use the APC armament category")
    for tier, (_, technology, _) in APC_HULL_ROWS.items():
        if not re.search(rf"enable = \{{ has_tech = {technology} \}}", ai_text):
            fail(f"APC AI recipe for tier {tier} is not gated on {technology}")

    hull_loc = text(MOD / "localisation/english/tank_modules_l_english.yml")
    tech_loc = text(MOD / "localisation/english/nsb_armor_l_english.yml")
    for tier, (_, technology, _) in APC_HULL_ROWS.items():
        for key, source in (
            (f"apc_chassis_{tier}", hull_loc),
            (f"apc_chassis_{tier}_short", hull_loc),
            (f"apc_chassis_{tier}_desc", hull_loc),
            (f"apc_equipment_{tier}", hull_loc),
            (technology, tech_loc),
        ):
            if not re.search(rf"(?m)^\s*{key}:\d*\s+\"", source):
                fail(f"APC localisation key is missing: {key}")
    for module in APC_SUPERSTRUCTURE_MODULES + APC_ARMAMENT_MODULES:
        for key in (module, f"{module}_desc"):
            if not re.search(rf"(?m)^\s*{key}:\d*\s+\"", hull_loc):
                fail(f"APC localisation key is missing: {key}")


def run_apc_negative_fixtures() -> None:
    """The APC contract must reject the shapes that would break legacy support."""
    source = text(MECHANIZED_FILE)
    for label, mutation in (
        ("legacy row inherits slots", lambda v: v.replace(
            "\tmechanized_equipment_3 = {\n\t\tyear = 1947",
            "\tmechanized_equipment_3 = {\n\t\tmodule_slots = inherit\n\t\tyear = 1947", 1)),
        ("tank gun allowed on an APC", lambda v: v.replace(
            "\t\t\t\t\ttank_apc_armament\n", "\t\t\t\t\ttank_small_main_armament\n", 1)),
        ("hull leaves the mechanized archetype", lambda v: v.replace(
            "\tapc_chassis_0 = {\n\t\tabbreviation", "\tapc_chassis_0 = {\n\t\tarchetype = light_tank_chassis\n\t\tabbreviation", 1)),
        ("hull loses its DLC gate", lambda v: v.replace('has_dlc = "No Step Back"', "always = yes", 1)),
        ("archetype leaves the armor domain", lambda v: v.replace(
            "\t\ttype = { armor mechanized }\n", "\t\ttype = mechanized\n", 1)),
    ):
        mutated = mutation(source)
        if mutated == source:
            raise AssertionError(f"APC fixture did not mutate the source: {label}")
        MECHANIZED_FILE.write_text(mutated, encoding="utf-8", newline="")
        previous = len(errors)
        try:
            validate_apc_designer_family()
            rejected = len(errors) > previous
        finally:
            del errors[previous:]
            MECHANIZED_FILE.write_text(source, encoding="utf-8", newline="")
        if not rejected:
            raise AssertionError(f"APC contract accepted a broken mutation: {label}")
    windows = designer_window_names()
    if "equipment_designer_mechanized_equipment" not in windows:
        raise AssertionError("the APC designer window is missing from the fixture baseline")
    previous = len(errors)
    validate_designer_window_coverage(windows - {"equipment_designer_mechanized_equipment"})
    rejected = len(errors) > previous
    del errors[previous:]
    if not rejected:
        raise AssertionError("designer window coverage accepted a missing APC window")


validate_apc_designer_family()
validate_designer_window_coverage()
if "--tank-self-test" in sys.argv:
    run_apc_negative_fixtures()

balance_report = tank_balance_report() if "--tank-balance-report" in sys.argv else ""
module_balance_report = (
    tank_module_balance_report() if "--tank-module-balance-report" in sys.argv else ""
)
envelope_report = tank_envelope_report() if "--tank-envelope-report" in sys.argv else ""

if errors:
    print("Military rework validation failed:")
    for message in errors:
        print(f"- {message}")
    sys.exit(1)

print(
    "Military rework validation passed: "
    f"{len(technology_set)} technologies, {len(module_ids)} tank modules, "
    f"{len(expected_types)} historical tank designs, {len(oob_refs)} generic bookmark variants, "
    f"{len(NATIONAL_PRESETS)} national presets "
    f"and {versioned_oob_requests} named OOB requests across "
    f"{len(oob_files_with_tanks)} NSB OOBs, {history_bootstrap_sites} country-history "
    f"bootstrap sites, {len(APC_HULL_ROWS)} APC designer hulls, and 15 designer slots checked."
)
if balance_report:
    print(balance_report)
if module_balance_report:
    print(module_balance_report)
if envelope_report:
    print(envelope_report)
