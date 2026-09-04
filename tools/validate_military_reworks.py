#!/usr/bin/env python3
"""Static integration checks for the doctrine and NSB tank reworks."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "Cold War Iron Curtain"
TECH_DIR = MOD / "common/technologies"
MODULE_FILE = MOD / "common/units/equipment/modules/00_tank_modules.txt"
CHASSIS_FILE = MOD / "common/units/equipment/tank_chassis.txt"
AI_FILE = MOD / "common/ai_equipment/generic_tank.txt"
ENUM_FILE = MOD / "common/script_enums.txt"
VARIANT_EFFECT_FILE = MOD / "common/scripted_effects/CWIC_tank_designer_effects.txt"
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

errors: list[str] = []


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
    MOD / "interface/tank_designer_view.gui",
]
for candidate in key_files:
    brace_balance(candidate)

# Doctrine loader contract.
for candidate in doctrine_files:
    if not candidate.is_file() or candidate.stat().st_size == 0:
        fail(f"doctrine technology file is absent or empty: {candidate.name}")
parked = TECH_DIR / "doctrine rework"
if parked.exists() and any(parked.iterdir()):
    fail("common/technologies/doctrine rework must be empty or absent")

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
if re.search(r"\bdefence\s*=", code_only(text(TECH_DIR / "land_doctrine.txt"))):
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
            elif name_match.group(1) != BOOKMARK_VARIANT_NAMES[tank_type]:
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
                elif name_match.group(1) != BOOKMARK_VARIANT_NAMES[tank_type]:
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
            r"^\s*([A-Za-z0-9_]+_slot)\s*=\s*([A-Za-z0-9_]+)",
            block,
            re.MULTILINE,
        )
    )
    slot_names = {slot for slot, _ in slots}
    if slot_names != REQUIRED_VARIANT_SLOTS:
        fail(
            f"starting variant {variant_type} has wrong required slots: "
            f"{sorted(slot_names)}"
        )
    for _, module in slots:
        if module not in module_ids:
            fail(f"starting variant {variant_type} uses undefined module {module}")
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
if len(re.findall(r"^\s*history\s*=\s*yes\b", ai_text, re.MULTILINE)) != len(expected_types):
    fail("generic tank AI file must contain one historical recipe per supported tank type")

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

if errors:
    print("Military rework validation failed:")
    for message in errors:
        print(f"- {message}")
    sys.exit(1)

print(
    "Military rework validation passed: "
    f"{len(technology_set)} technologies, {len(module_ids)} tank modules, "
    f"{len(expected_types)} historical tank designs, {len(oob_refs)} bookmark variants "
    f"and {versioned_oob_requests} named OOB requests across "
    f"{len(oob_files_with_tanks)} NSB OOBs, {history_bootstrap_sites} country-history "
    "bootstrap sites, and 15 designer slots checked."
)
