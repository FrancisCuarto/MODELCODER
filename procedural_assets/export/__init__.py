try:
    from .glb_exporter import GLBExporter
    from .metadata_sidecar import save_metadata_sidecar
    from .export_report import generate_export_report
    from .godot_validator import validate_glb_with_godot, is_godot_available
except (ImportError, ModuleNotFoundError):
    GLBExporter = None  # type: ignore
    save_metadata_sidecar = None  # type: ignore
    generate_export_report = None  # type: ignore
    validate_glb_with_godot = None  # type: ignore
    is_godot_available = None  # type: ignore

from .destination import (
    resolve_output_dir,
    get_saved_game_dir,
    set_saved_game_dir,
    clear_saved_game_dir,
    FAMILY_CATEGORIES
)



__all__ = [
    "GLBExporter",
    "save_metadata_sidecar",
    "generate_export_report",
    "validate_glb_with_godot",
    "is_godot_available",
    "resolve_output_dir",
    "get_saved_game_dir",
    "set_saved_game_dir",
    "clear_saved_game_dir",
    "FAMILY_CATEGORIES",
]
