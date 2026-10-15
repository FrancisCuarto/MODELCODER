"""
Destination and Export Directory Management for Below Nominal procedural assets.
Handles target folder resolution, persistent game project configurations (.export_config.json),
environment variable overrides, and optional asset categorization subfolders.
"""

import os
import json
from typing import Optional, Dict

FAMILY_CATEGORIES: Dict[str, str] = {
    # Medical & Research Lab
    "autopsy_table": "medical",
    "medical_screen": "medical",
    "morgue_gurney": "medical",
    "chemical_cabinet": "medical",
    "restraint_chair": "medical",
    "scrub_sink": "medical",
    "crash_cart": "medical",
    "oxypod": "medical",

    # Living Quarters, Office & Furniture
    "crew_bed": "furniture",
    "bunk_bed": "furniture",
    "nightstand": "furniture",
    "radiator_heater": "furniture",
    "office_desk": "furniture",
    "office_chair": "furniture",
    "mess_table": "furniture",
    "locker_bench": "furniture",
    "work_bench": "furniture",
    "heavy_shelving": "furniture",
    "file_cabinet": "furniture",
    "bridge_console_desk": "furniture",
    "security_desk": "furniture",

    # Fixtures, Sanitation & Appliances
    "ration_automat": "fixtures",
    "canteen_counter": "fixtures",
    "space_toilet": "fixtures",
    "safety_shower": "fixtures",
    "tool_chest_cart": "fixtures",
    "hydroponic_tray_bed": "fixtures",
    "light_fixture": "fixtures",
    "trash_bin": "fixtures",
    "fire_extinguisher": "fixtures",
    "vent_grate": "fixtures",

    # Architectural Modules & Doors
    "station_corridor": "architecture",
    "station_room": "architecture",
    "office_door": "architecture",
    "door": "architecture",

    # Industrial Infrastructure & Props
    "electrical_panel": "infrastructure",
    "terminal": "infrastructure",
    "server_rack": "infrastructure",
    "pipes": "infrastructure",
    "cable_bundle": "infrastructure",
    "crate": "infrastructure",
    "locker": "infrastructure",
    "sign_placard": "infrastructure",
    "weapons_rack": "infrastructure",
}

def get_config_filepath() -> str:
    """Return absolute path to .export_config.json in project root."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, ".export_config.json")

def load_export_config() -> Dict[str, str]:
    """Load settings from .export_config.json if it exists."""
    cfg_file = get_config_filepath()
    if os.path.isfile(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
    return {}

def save_export_config(config: Dict[str, str]) -> None:
    """Persist settings to .export_config.json."""
    cfg_file = get_config_filepath()
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def get_saved_game_dir() -> Optional[str]:
    """Retrieve saved game asset directory if configured."""
    cfg = load_export_config()
    return cfg.get("game_assets_dir")

def set_saved_game_dir(path: str) -> str:
    """Save persistent game asset directory to .export_config.json."""
    abs_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
    os.makedirs(abs_path, exist_ok=True)
    cfg = load_export_config()
    cfg["game_assets_dir"] = abs_path
    save_export_config(cfg)
    return abs_path

def clear_saved_game_dir() -> None:
    """Clear configured game asset directory."""
    cfg = load_export_config()
    if "game_assets_dir" in cfg:
        del cfg["game_assets_dir"]
        save_export_config(cfg)

def resolve_output_dir(
    cli_arg: Optional[str] = None,
    family: Optional[str] = None,
    organize_by_category: bool = False
) -> str:
    """
    Resolve final export output directory with priority:
    1. Explicit CLI argument (--output-dir / -o).
    2. Environment variable (BELOW_NOMINAL_ASSETS_DIR, BN_GAME_DIR, GODOT_ASSETS_DIR).
    3. Saved game directory in .export_config.json.
    4. Fallback default: 'output'.

    If organize_by_category is True and family is known, subfolder is appended.
    """
    selected_dir: str = ""

    # 1. Explicit CLI argument
    if cli_arg and cli_arg.strip():
        selected_dir = cli_arg.strip()

    # 2. Environment variables
    if not selected_dir:
        for env_var in ("BELOW_NOMINAL_ASSETS_DIR", "BN_GAME_DIR", "GODOT_ASSETS_DIR"):
            val = os.environ.get(env_var)
            if val and val.strip():
                selected_dir = val.strip()
                break

    # 3. Persistent config
    if not selected_dir:
        saved = get_saved_game_dir()
        if saved and saved.strip():
            selected_dir = saved.strip()

    # 4. Fallback default
    if not selected_dir:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        selected_dir = os.path.join(base_dir, "output")

    # Clean path resolution
    norm_path = os.path.abspath(os.path.expanduser(os.path.expandvars(selected_dir)))

    # Optional category subfolder
    if organize_by_category and family and family in FAMILY_CATEGORIES:
        category = FAMILY_CATEGORIES[family]
        norm_path = os.path.join(norm_path, category)

    os.makedirs(norm_path, exist_ok=True)
    return norm_path
