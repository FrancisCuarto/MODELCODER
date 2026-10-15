from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List, Set, Any
import hashlib
import bpy
from .texture_atlas import PS1TextureAtlas, Rect

class MaterialCategory:
    """Surface material physics categories for authentic PS1 / retrofuturistic PBR."""
    PAINTED_METAL = "painted_metal"      # Dielectric enamel over metal (low metallic, mid-high roughness)
    STEEL = "steel"                      # Bare/galvanized/brushed steel (high metallic, satin roughness)
    PLASTIC = "plastic"                  # Molded retro computing polymer/bakelite (zero metallic, mid roughness)
    GLASS = "glass"                      # Transparent or wired safety glass (low metallic, very low roughness)
    SCREEN = "screen"                    # CRT display with active phosphor emission (zero metallic, low roughness)
    CERAMIC = "ceramic"                  # Vitreous sanitary glazed china/porcelain (zero metallic, low roughness)
    RUBBER = "rubber"                    # Vulcanized synthetic rubber/elastomer (zero metallic, high roughness)

class MaterialRole:
    """Semantic functional component roles for coherent, non-accidental material assignment."""
    FRAME = "frame"                      # Heavy structural chassis, legs, columns, ribs
    CASING = "casing"                    # Outer primary body enclosure / sheet metal
    CASING_ALT = "casing_alt"            # Secondary panels, drawers, sub-assemblies
    CASING_ACCENT = "casing_accent"      # Bold emergency / hazard accent trims
    PANEL = "panel"                      # Internal bulkhead panels, instrument decks
    HARDWARE = "hardware"                # Fasteners, bolts, hinges, latch handles, switches
    PLASTIC = "plastic"                  # Molded bezels, CRT housing, terminal shrouds
    SCREEN = "screen"                    # Active glowing CRT / instrument monitor
    SCREEN_OFF = "screen_off"            # Powered-down glass CRT screen
    INDICATOR = "indicator"              # Active status LED / pilot indicator
    GLASS = "glass"                      # Window panes, cabinet lights, specimen jars
    CERAMIC = "ceramic"                  # Hospital sinks, autopsy drain gutters, sanitary tiles
    HAZARD = "hazard"                    # Diagonal safety stripes, warning borders
    RUBBER = "rubber"                    # Gaskets, tires, vacuum hoses, umbilical conduits
    STAIN = "stain"                      # Rust crust, chemical leaks, biological grime

@dataclass
class MaterialDef:
    name: str
    rgba: Tuple[float, float, float, float]  # sRGB fallback / base vertex color
    roughness: float = 0.70
    metallic: float = 0.10
    emission_color: Optional[Tuple[float, float, float, float]] = None
    emission_strength: float = 0.0
    atlas_rect_name: str = "metal_dark_grime"
    transmission: float = 0.0
    alpha: float = 1.0
    category: str = MaterialCategory.PAINTED_METAL

# -------------------------------------------------------------------------
# PALETTE DEFINITIONS (Retrofuturistic Industrial Sector Palettes)
# -------------------------------------------------------------------------

def _build_industrial_hazard_palette() -> Dict[str, MaterialDef]:
    """Default heavy engineering, reactor, and maintenance sector palette."""
    return {
        # Core Architecture & Casings
        "casing": MaterialDef("mat_casing", (0.16, 0.18, 0.20, 1.0), roughness=0.68, metallic=0.18, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "casing_red": MaterialDef("mat_casing_red", (0.58, 0.10, 0.08, 1.0), roughness=0.65, metallic=0.12, atlas_rect_name="red_paint_worn", category=MaterialCategory.PAINTED_METAL),
        "casing_inner": MaterialDef("mat_casing_inner", (0.24, 0.26, 0.28, 1.0), roughness=0.75, metallic=0.15, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "casing_alt": MaterialDef("mat_casing_alt", (0.20, 0.22, 0.25, 1.0), roughness=0.62, metallic=0.22, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "mounting": MaterialDef("mat_mounting", (0.55, 0.58, 0.62, 1.0), roughness=0.42, metallic=0.88, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "steel_brushed": MaterialDef("mat_steel_brushed", (0.65, 0.68, 0.72, 1.0), roughness=0.38, metallic=0.92, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "steel_dark": MaterialDef("mat_steel_dark", (0.25, 0.27, 0.30, 1.0), roughness=0.48, metallic=0.85, atlas_rect_name="metal_dark_grime", category=MaterialCategory.STEEL),

        # Molded Plastics & Housings
        "crt_frame": MaterialDef("mat_crt_frame", (0.12, 0.13, 0.14, 1.0), roughness=0.52, metallic=0.02, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PLASTIC),
        "plastic_beige": MaterialDef("mat_plastic_beige", (0.72, 0.70, 0.62, 1.0), roughness=0.55, metallic=0.02, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PLASTIC),

        # Displays, CRTs & Glowing Screens
        "crt_screen_green": MaterialDef("mat_crt_screen", (0.05, 0.15, 0.08, 1.0), roughness=0.22, metallic=0.0, emission_color=(0.15, 0.95, 0.35, 1.0), emission_strength=2.2, atlas_rect_name="crt_screen_green", category=MaterialCategory.SCREEN),
        "crt_screen_amber": MaterialDef("mat_crt_screen_amber", (0.18, 0.10, 0.03, 1.0), roughness=0.22, metallic=0.0, emission_color=(0.95, 0.60, 0.08, 1.0), emission_strength=2.2, atlas_rect_name="crt_screen_amber", category=MaterialCategory.SCREEN),
        "crt_screen_off": MaterialDef("mat_crt_screen_off", (0.06, 0.07, 0.08, 1.0), roughness=0.18, metallic=0.05, atlas_rect_name="crt_screen_off", category=MaterialCategory.SCREEN),
        "crt_screen": MaterialDef("mat_crt_screen_gen", (0.05, 0.15, 0.08, 1.0), roughness=0.22, metallic=0.0, emission_color=(0.15, 0.95, 0.35, 1.0), emission_strength=2.2, atlas_rect_name="crt_screen_green", category=MaterialCategory.SCREEN),

        # Buttons, Controls & Fasteners
        "button_red": MaterialDef("mat_btn_red", (0.65, 0.12, 0.10, 1.0), roughness=0.45, metallic=0.05, atlas_rect_name="button_red", category=MaterialCategory.PLASTIC),
        "button_yellow": MaterialDef("mat_btn_yellow", (0.85, 0.55, 0.05, 1.0), roughness=0.45, metallic=0.05, atlas_rect_name="button_yellow", category=MaterialCategory.PLASTIC),
        "button_blue": MaterialDef("mat_btn_blue", (0.12, 0.32, 0.52, 1.0), roughness=0.45, metallic=0.05, atlas_rect_name="button_blue", category=MaterialCategory.PLASTIC),
        "button_gray": MaterialDef("mat_btn_gray", (0.35, 0.37, 0.40, 1.0), roughness=0.50, metallic=0.15, atlas_rect_name="button_white", category=MaterialCategory.PLASTIC),
        "switch_metal": MaterialDef("mat_switch_metal", (0.65, 0.68, 0.72, 1.0), roughness=0.30, metallic=0.92, atlas_rect_name="switch_metal", category=MaterialCategory.STEEL),
        "switch_base": MaterialDef("mat_switch_base", (0.08, 0.08, 0.09, 1.0), roughness=0.82, metallic=0.0, atlas_rect_name="rubber_black", category=MaterialCategory.RUBBER),
        "screw": MaterialDef("mat_screw", (0.32, 0.34, 0.37, 1.0), roughness=0.35, metallic=0.88, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),

        # Pilot LEDs & Illumination
        "led_green": MaterialDef("mat_led_green", (0.08, 0.30, 0.10, 1.0), roughness=0.20, metallic=0.0, emission_color=(0.10, 0.95, 0.20, 1.0), emission_strength=2.8, atlas_rect_name="led_green", category=MaterialCategory.SCREEN),
        "led_red": MaterialDef("mat_led_red", (0.35, 0.08, 0.08, 1.0), roughness=0.20, metallic=0.0, emission_color=(0.95, 0.10, 0.08, 1.0), emission_strength=2.8, atlas_rect_name="led_red", category=MaterialCategory.SCREEN),
        "led_yellow": MaterialDef("mat_led_yellow", (0.35, 0.28, 0.05, 1.0), roughness=0.20, metallic=0.0, emission_color=(0.95, 0.80, 0.05, 1.0), emission_strength=2.8, atlas_rect_name="led_yellow", category=MaterialCategory.SCREEN),
        "fluorescent_tube_lit": MaterialDef("mat_fluorescent_lit", (0.85, 0.95, 0.98, 1.0), roughness=0.18, metallic=0.0, emission_color=(0.90, 0.98, 1.00, 1.0), emission_strength=3.0, atlas_rect_name="fluorescent_lit", category=MaterialCategory.SCREEN),

        # Cables & Elastomers
        "cable_black": MaterialDef("mat_cable_black", (0.09, 0.09, 0.10, 1.0), roughness=0.88, metallic=0.0, atlas_rect_name="rubber_black", category=MaterialCategory.RUBBER),
        "cable_hazard": MaterialDef("mat_cable_hazard", (0.80, 0.52, 0.08, 1.0), roughness=0.85, metallic=0.0, atlas_rect_name="hazard_stripes", category=MaterialCategory.RUBBER),
        "cable_red": MaterialDef("mat_cable_red", (0.55, 0.10, 0.08, 1.0), roughness=0.85, metallic=0.0, atlas_rect_name="red_paint_worn", category=MaterialCategory.RUBBER),
        "rubber_tire": MaterialDef("mat_rubber_tire", (0.12, 0.12, 0.13, 1.0), roughness=0.90, metallic=0.0, atlas_rect_name="rubber_black", category=MaterialCategory.RUBBER),

        # Glass & Optical Elements
        "glass_tube": MaterialDef("mat_glass_tube", (0.15, 0.28, 0.35, 1.0), roughness=0.12, metallic=0.08, transmission=0.75, atlas_rect_name="glass_reinforced", category=MaterialCategory.GLASS),
        "glass_observation": MaterialDef("mat_glass_observation", (0.10, 0.18, 0.22, 1.0), roughness=0.14, metallic=0.08, transmission=0.80, atlas_rect_name="glass_reinforced", category=MaterialCategory.GLASS),
        "glass_reinforced": MaterialDef("mat_glass_reinforced", (0.18, 0.28, 0.32, 1.0), roughness=0.15, metallic=0.12, transmission=0.70, atlas_rect_name="glass_reinforced", category=MaterialCategory.GLASS),
        "glass_clear": MaterialDef("mat_glass_clear", (0.12, 0.22, 0.28, 1.0), roughness=0.10, metallic=0.05, transmission=0.85, atlas_rect_name="glass_reinforced", category=MaterialCategory.GLASS),

        # Ceramic & Sanitary Surfaces
        "ceramic_white": MaterialDef("mat_ceramic_white", (0.88, 0.90, 0.90, 1.0), roughness=0.18, metallic=0.0, atlas_rect_name="ceramic_tile_white", category=MaterialCategory.CERAMIC),
        "ceramic_tile": MaterialDef("mat_ceramic_tile", (0.86, 0.88, 0.88, 1.0), roughness=0.20, metallic=0.0, atlas_rect_name="ceramic_tile_white", category=MaterialCategory.CERAMIC),

        # Fluids & Biological Glow
        "oxygen_cyan": MaterialDef("mat_oxygen_cyan", (0.05, 0.65, 0.75, 1.0), roughness=0.12, metallic=0.0, emission_color=(0.10, 0.85, 0.95, 1.0), emission_strength=2.4, atlas_rect_name="oxygen_cyan_glow", category=MaterialCategory.SCREEN),

        # Hazard, Signage & Architecture
        "hazard_yellow": MaterialDef("mat_hazard_yellow", (0.85, 0.62, 0.08, 1.0), roughness=0.65, metallic=0.08, atlas_rect_name="hazard_stripes", category=MaterialCategory.PAINTED_METAL),
        "hazard_black": MaterialDef("mat_hazard_black", (0.08, 0.08, 0.09, 1.0), roughness=0.80, metallic=0.05, atlas_rect_name="rubber_black", category=MaterialCategory.RUBBER),
        "door_emergency_red": MaterialDef("mat_door_emergency_red", (0.58, 0.10, 0.08, 1.0), roughness=0.55, metallic=0.15, atlas_rect_name="door_seal_red", category=MaterialCategory.PAINTED_METAL),
        "door_frame_heavy": MaterialDef("mat_door_frame_heavy", (0.15, 0.16, 0.18, 1.0), roughness=0.70, metallic=0.45, atlas_rect_name="metal_dark_grime", category=MaterialCategory.STEEL),
        "door_frame": MaterialDef("mat_door_frame", (0.15, 0.16, 0.18, 1.0), roughness=0.70, metallic=0.45, atlas_rect_name="metal_dark_grime", category=MaterialCategory.STEEL),
        "server_blade_metal": MaterialDef("mat_server_blade_metal", (0.20, 0.22, 0.25, 1.0), roughness=0.58, metallic=0.35, atlas_rect_name="metal_dark_grime", category=MaterialCategory.STEEL),
        "memory_cartridge": MaterialDef("mat_memory_cartridge", (0.75, 0.45, 0.10, 1.0), roughness=0.40, metallic=0.30, emission_color=(0.85, 0.50, 0.10, 1.0), emission_strength=1.6, atlas_rect_name="cartridge_amber", category=MaterialCategory.SCREEN),
        "chemical_barrel_yellow": MaterialDef("mat_chem_yellow", (0.78, 0.55, 0.08, 1.0), roughness=0.62, metallic=0.10, atlas_rect_name="hazard_stripes", category=MaterialCategory.PAINTED_METAL),
        "chemical_barrel_blue": MaterialDef("mat_chem_blue", (0.10, 0.30, 0.50, 1.0), roughness=0.62, metallic=0.10, atlas_rect_name="button_blue", category=MaterialCategory.PAINTED_METAL),
        "locker_gray": MaterialDef("mat_locker_gray", (0.26, 0.28, 0.30, 1.0), roughness=0.68, metallic=0.25, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "pipe_industrial": MaterialDef("mat_pipe_industrial", (0.35, 0.38, 0.42, 1.0), roughness=0.48, metallic=0.75, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "valve_red": MaterialDef("mat_valve_red", (0.72, 0.14, 0.10, 1.0), roughness=0.45, metallic=0.25, atlas_rect_name="red_paint_worn", category=MaterialCategory.PAINTED_METAL),
        "rust_patch": MaterialDef("mat_rust_patch", (0.45, 0.18, 0.08, 1.0), roughness=0.92, metallic=0.10, atlas_rect_name="rust_heavy", category=MaterialCategory.PAINTED_METAL),
        "gauge": MaterialDef("mat_gauge", (0.88, 0.86, 0.80, 1.0), roughness=0.40, metallic=0.15, atlas_rect_name="gauge_meter", category=MaterialCategory.PLASTIC),
        "vent": MaterialDef("mat_vent", (0.25, 0.25, 0.25, 1.0), roughness=0.68, metallic=0.35, atlas_rect_name="vent_grill", category=MaterialCategory.STEEL),
        "chair_vinyl": MaterialDef("mat_chair_vinyl", (0.16, 0.18, 0.20, 1.0), roughness=0.62, metallic=0.04, atlas_rect_name="chair_vinyl_dark", category=MaterialCategory.PLASTIC),
        "sign_exit": MaterialDef("mat_sign_exit", (0.08, 0.65, 0.25, 1.0), roughness=0.30, metallic=0.08, emission_color=(0.10, 0.85, 0.30, 1.0), emission_strength=1.8, atlas_rect_name="sign_exit_green", category=MaterialCategory.SCREEN),
        "sign_sector": MaterialDef("mat_sign_sector", (0.10, 0.28, 0.55, 1.0), roughness=0.48, metallic=0.15, atlas_rect_name="sign_sector_blue", category=MaterialCategory.PAINTED_METAL),
        "sign_caution": MaterialDef("mat_sign_caution", (0.85, 0.65, 0.05, 1.0), roughness=0.52, metallic=0.08, atlas_rect_name="caution_label", category=MaterialCategory.PAINTED_METAL),
        "floor_metal": MaterialDef("mat_floor_metal", (0.22, 0.24, 0.26, 1.0), roughness=0.78, metallic=0.32, atlas_rect_name="metal_dark_grime", category=MaterialCategory.STEEL),
        "floor_hazard": MaterialDef("mat_floor_hazard", (0.85, 0.62, 0.08, 1.0), roughness=0.72, metallic=0.10, atlas_rect_name="hazard_stripes", category=MaterialCategory.PAINTED_METAL),
        "floor_grate": MaterialDef("mat_floor_grate", (0.18, 0.19, 0.20, 1.0), roughness=0.60, metallic=0.65, atlas_rect_name="vent_grill", category=MaterialCategory.STEEL),
        "wall_bulkhead": MaterialDef("mat_wall_bulkhead", (0.28, 0.30, 0.32, 1.0), roughness=0.74, metallic=0.28, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "wall_support_beam": MaterialDef("mat_wall_support_beam", (0.38, 0.40, 0.44, 1.0), roughness=0.52, metallic=0.75, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "ceiling_girder": MaterialDef("mat_ceiling_girder", (0.18, 0.19, 0.21, 1.0), roughness=0.65, metallic=0.60, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
    }

def _build_medbay_clean_palette() -> Dict[str, MaterialDef]:
    """Clinical medbay, quarantine isolation, autopsy, and laboratory sector palette."""
    base = _build_industrial_hazard_palette()
    base.update({
        "casing": MaterialDef("mat_casing", (0.84, 0.85, 0.86, 1.0), roughness=0.55, metallic=0.05, atlas_rect_name="painted_metal_white", category=MaterialCategory.PAINTED_METAL),
        "casing_alt": MaterialDef("mat_casing_alt", (0.55, 0.72, 0.75, 1.0), roughness=0.58, metallic=0.08, atlas_rect_name="painted_metal_white", category=MaterialCategory.PAINTED_METAL),
        "casing_inner": MaterialDef("mat_casing_inner", (0.75, 0.78, 0.80, 1.0), roughness=0.62, metallic=0.12, atlas_rect_name="painted_metal_white", category=MaterialCategory.PAINTED_METAL),
        "mounting": MaterialDef("mat_mounting", (0.72, 0.75, 0.78, 1.0), roughness=0.32, metallic=0.92, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "steel_brushed": MaterialDef("mat_steel_brushed", (0.75, 0.78, 0.82, 1.0), roughness=0.28, metallic=0.95, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "ceramic_white": MaterialDef("mat_ceramic_white", (0.92, 0.94, 0.95, 1.0), roughness=0.14, metallic=0.0, atlas_rect_name="ceramic_tile_white", category=MaterialCategory.CERAMIC),
        "ceramic_tile": MaterialDef("mat_ceramic_tile", (0.90, 0.92, 0.93, 1.0), roughness=0.16, metallic=0.0, atlas_rect_name="ceramic_tile_white", category=MaterialCategory.CERAMIC),
        "crt_screen": MaterialDef("mat_crt_screen_med", (0.06, 0.22, 0.35, 1.0), roughness=0.20, metallic=0.0, emission_color=(0.15, 0.75, 0.95, 1.0), emission_strength=2.4, atlas_rect_name="oxygen_cyan_glow", category=MaterialCategory.SCREEN),
        "crt_frame": MaterialDef("mat_crt_frame", (0.70, 0.72, 0.75, 1.0), roughness=0.48, metallic=0.02, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PLASTIC),
        "glass_tube": MaterialDef("mat_glass_tube", (0.20, 0.38, 0.42, 1.0), roughness=0.10, metallic=0.05, transmission=0.82, atlas_rect_name="glass_reinforced", category=MaterialCategory.GLASS),
        "wall_bulkhead": MaterialDef("mat_wall_bulkhead", (0.78, 0.80, 0.82, 1.0), roughness=0.60, metallic=0.10, atlas_rect_name="painted_metal_white", category=MaterialCategory.PAINTED_METAL),
    })
    return base

def _build_command_bridge_palette() -> Dict[str, MaterialDef]:
    """Command bridge, tactical navigation, and main operations center palette."""
    base = _build_industrial_hazard_palette()
    base.update({
        "casing": MaterialDef("mat_casing", (0.10, 0.12, 0.18, 1.0), roughness=0.60, metallic=0.10, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "casing_alt": MaterialDef("mat_casing_alt", (0.16, 0.18, 0.24, 1.0), roughness=0.52, metallic=0.25, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "casing_inner": MaterialDef("mat_casing_inner", (0.12, 0.14, 0.19, 1.0), roughness=0.65, metallic=0.18, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
        "mounting": MaterialDef("mat_mounting", (0.68, 0.70, 0.74, 1.0), roughness=0.35, metallic=0.85, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "crt_screen": MaterialDef("mat_crt_screen_bridge", (0.28, 0.16, 0.04, 1.0), roughness=0.20, metallic=0.0, emission_color=(0.95, 0.62, 0.08, 1.0), emission_strength=2.6, atlas_rect_name="crt_screen_amber", category=MaterialCategory.SCREEN),
        "switch_metal": MaterialDef("mat_switch_metal", (0.82, 0.72, 0.45, 1.0), roughness=0.28, metallic=0.90, atlas_rect_name="switch_metal", category=MaterialCategory.STEEL), # Brushed brass toggle
        "chair_vinyl": MaterialDef("mat_chair_vinyl", (0.08, 0.10, 0.14, 1.0), roughness=0.58, metallic=0.02, atlas_rect_name="chair_vinyl_dark", category=MaterialCategory.PLASTIC),
        "wall_bulkhead": MaterialDef("mat_wall_bulkhead", (0.14, 0.16, 0.22, 1.0), roughness=0.62, metallic=0.20, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
    })
    return base

def _build_habitation_worn_palette() -> Dict[str, MaterialDef]:
    """Crew living quarters, canteen, bunk pods, and mess hall palette."""
    base = _build_industrial_hazard_palette()
    base.update({
        "casing": MaterialDef("mat_casing", (0.42, 0.40, 0.35, 1.0), roughness=0.72, metallic=0.08, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PLASTIC),
        "casing_alt": MaterialDef("mat_casing_alt", (0.48, 0.38, 0.28, 1.0), roughness=0.68, metallic=0.12, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PAINTED_METAL),
        "casing_inner": MaterialDef("mat_casing_inner", (0.35, 0.33, 0.30, 1.0), roughness=0.75, metallic=0.10, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PAINTED_METAL),
        "mounting": MaterialDef("mat_mounting", (0.38, 0.36, 0.35, 1.0), roughness=0.48, metallic=0.75, atlas_rect_name="metal_light_brushed", category=MaterialCategory.STEEL),
        "crt_frame": MaterialDef("mat_crt_frame", (0.72, 0.70, 0.62, 1.0), roughness=0.55, metallic=0.02, atlas_rect_name="beige_plastic_worn", category=MaterialCategory.PLASTIC),
        "crt_screen": MaterialDef("mat_crt_screen_hab", (0.12, 0.22, 0.10, 1.0), roughness=0.22, metallic=0.0, emission_color=(0.20, 0.88, 0.30, 1.0), emission_strength=1.8, atlas_rect_name="crt_screen_green", category=MaterialCategory.SCREEN),
        "chair_vinyl": MaterialDef("mat_chair_vinyl", (0.38, 0.24, 0.16, 1.0), roughness=0.65, metallic=0.03, atlas_rect_name="chair_vinyl_dark", category=MaterialCategory.PLASTIC),
        "wall_bulkhead": MaterialDef("mat_wall_bulkhead", (0.45, 0.44, 0.40, 1.0), roughness=0.75, metallic=0.15, atlas_rect_name="metal_dark_grime", category=MaterialCategory.PAINTED_METAL),
    })
    return base

def _build_derelict_decay_palette() -> Dict[str, MaterialDef]:
    """Infested, breached, ruined, and blood-soaked survival horror sector palette."""
    base = _build_industrial_hazard_palette()
    base.update({
        "casing": MaterialDef("mat_casing", (0.38, 0.22, 0.14, 1.0), roughness=0.88, metallic=0.35, atlas_rect_name="rust_heavy", category=MaterialCategory.STEEL),
        "casing_alt": MaterialDef("mat_casing_alt", (0.24, 0.14, 0.10, 1.0), roughness=0.92, metallic=0.20, atlas_rect_name="rust_heavy", category=MaterialCategory.STEEL),
        "casing_inner": MaterialDef("mat_casing_inner", (0.18, 0.12, 0.08, 1.0), roughness=0.95, metallic=0.15, atlas_rect_name="rust_heavy", category=MaterialCategory.STEEL),
        "mounting": MaterialDef("mat_mounting", (0.32, 0.22, 0.16, 1.0), roughness=0.75, metallic=0.60, atlas_rect_name="rust_heavy", category=MaterialCategory.STEEL),
        "crt_screen": MaterialDef("mat_crt_screen_dead", (0.04, 0.04, 0.05, 1.0), roughness=0.25, metallic=0.05, emission_strength=0.0, atlas_rect_name="crt_screen_off", category=MaterialCategory.SCREEN),
        "fluorescent_tube_lit": MaterialDef("mat_fluorescent_dim", (0.45, 0.15, 0.12, 1.0), roughness=0.30, metallic=0.0, emission_color=(0.85, 0.15, 0.10, 1.0), emission_strength=0.9, atlas_rect_name="fluorescent_lit", category=MaterialCategory.SCREEN),
        "wall_bulkhead": MaterialDef("mat_wall_bulkhead", (0.25, 0.18, 0.14, 1.0), roughness=0.88, metallic=0.25, atlas_rect_name="rust_heavy", category=MaterialCategory.STEEL),
        "ceramic_white": MaterialDef("mat_ceramic_white", (0.55, 0.48, 0.42, 1.0), roughness=0.35, metallic=0.0, atlas_rect_name="ceramic_tile_white", category=MaterialCategory.CERAMIC),
    })
    return base

DEFAULT_PALETTES: Dict[str, Dict[str, MaterialDef]] = {
    "industrial_hazard": _build_industrial_hazard_palette(),
    "medbay_clean": _build_medbay_clean_palette(),
    "command_bridge": _build_command_bridge_palette(),
    "habitation_worn": _build_habitation_worn_palette(),
    "derelict_decay": _build_derelict_decay_palette(),
}

PALETTE_ROLE_MAP: Dict[str, Dict[str, str]] = {
    "industrial_hazard": {
        MaterialRole.FRAME: "mounting",
        MaterialRole.CASING: "casing",
        MaterialRole.CASING_ALT: "casing_inner",
        MaterialRole.CASING_ACCENT: "hazard_yellow",
        MaterialRole.PANEL: "wall_bulkhead",
        MaterialRole.HARDWARE: "screw",
        MaterialRole.PLASTIC: "crt_frame",
        MaterialRole.SCREEN: "crt_screen",
        MaterialRole.SCREEN_OFF: "crt_screen_off",
        MaterialRole.INDICATOR: "led_green",
        MaterialRole.GLASS: "glass_tube",
        MaterialRole.CERAMIC: "ceramic_white",
        MaterialRole.HAZARD: "hazard_yellow",
        MaterialRole.RUBBER: "cable_black",
        MaterialRole.STAIN: "rust_patch",
    },
    "medbay_clean": {
        MaterialRole.FRAME: "mounting",
        MaterialRole.CASING: "casing",
        MaterialRole.CASING_ALT: "casing_alt",
        MaterialRole.CASING_ACCENT: "casing_red",
        MaterialRole.PANEL: "wall_bulkhead",
        MaterialRole.HARDWARE: "screw",
        MaterialRole.PLASTIC: "crt_frame",
        MaterialRole.SCREEN: "crt_screen",
        MaterialRole.SCREEN_OFF: "crt_screen_off",
        MaterialRole.INDICATOR: "led_green",
        MaterialRole.GLASS: "glass_tube",
        MaterialRole.CERAMIC: "ceramic_white",
        MaterialRole.HAZARD: "hazard_yellow",
        MaterialRole.RUBBER: "cable_black",
        MaterialRole.STAIN: "rust_patch",
    },
    "command_bridge": {
        MaterialRole.FRAME: "mounting",
        MaterialRole.CASING: "casing",
        MaterialRole.CASING_ALT: "casing_alt",
        MaterialRole.CASING_ACCENT: "switch_metal",
        MaterialRole.PANEL: "wall_bulkhead",
        MaterialRole.HARDWARE: "screw",
        MaterialRole.PLASTIC: "crt_frame",
        MaterialRole.SCREEN: "crt_screen",
        MaterialRole.SCREEN_OFF: "crt_screen_off",
        MaterialRole.INDICATOR: "led_yellow",
        MaterialRole.GLASS: "glass_observation",
        MaterialRole.CERAMIC: "ceramic_white",
        MaterialRole.HAZARD: "hazard_yellow",
        MaterialRole.RUBBER: "cable_black",
        MaterialRole.STAIN: "rust_patch",
    },
    "habitation_worn": {
        MaterialRole.FRAME: "mounting",
        MaterialRole.CASING: "casing",
        MaterialRole.CASING_ALT: "casing_alt",
        MaterialRole.CASING_ACCENT: "hazard_yellow",
        MaterialRole.PANEL: "wall_bulkhead",
        MaterialRole.HARDWARE: "screw",
        MaterialRole.PLASTIC: "crt_frame",
        MaterialRole.SCREEN: "crt_screen",
        MaterialRole.SCREEN_OFF: "crt_screen_off",
        MaterialRole.INDICATOR: "led_green",
        MaterialRole.GLASS: "glass_observation",
        MaterialRole.CERAMIC: "ceramic_white",
        MaterialRole.HAZARD: "hazard_yellow",
        MaterialRole.RUBBER: "cable_black",
        MaterialRole.STAIN: "rust_patch",
    },
    "derelict_decay": {
        MaterialRole.FRAME: "mounting",
        MaterialRole.CASING: "casing",
        MaterialRole.CASING_ALT: "casing_alt",
        MaterialRole.CASING_ACCENT: "rust_patch",
        MaterialRole.PANEL: "wall_bulkhead",
        MaterialRole.HARDWARE: "screw",
        MaterialRole.PLASTIC: "crt_frame",
        MaterialRole.SCREEN: "crt_screen",
        MaterialRole.SCREEN_OFF: "crt_screen_off",
        MaterialRole.INDICATOR: "led_red",
        MaterialRole.GLASS: "glass_reinforced",
        MaterialRole.CERAMIC: "ceramic_white",
        MaterialRole.HAZARD: "hazard_yellow",
        MaterialRole.RUBBER: "cable_black",
        MaterialRole.STAIN: "rust_patch",
    },
}

class MaterialManager:
    """
    Manages creation, caching, semantic assignment, and deduplication of
    textured PS1 materials with point sampling and physical roughness/metallic calibration.
    """

    def __init__(
        self,
        palette_name: str = "industrial_hazard",
        wear_level: float = 0.5,
        seed: int = 42,
        emission_multiplier: float = 1.0
    ):
        self.palette_name = palette_name if palette_name in DEFAULT_PALETTES else "industrial_hazard"
        self.palette = DEFAULT_PALETTES[self.palette_name]
        self.wear_level = wear_level
        self.seed = seed
        self.emission_multiplier = max(0.0, emission_multiplier)
        self.atlas_image = PS1TextureAtlas.get_or_create_blender_image(wear_level=wear_level, seed=seed)
        self.material_cache: Dict[str, bpy.types.Material] = {}
        self.material_indices: Dict[str, int] = {k: i for i, k in enumerate(self.palette.keys())}
        self.used_keys: Set[str] = set()

    def get_rect(self, key: str) -> Rect:
        """Get UV atlas rect for a given material key or semantic role."""
        actual_key = self.resolve_key(key)
        mat_def = self.palette.get(actual_key)
        rect_name = mat_def.atlas_rect_name if mat_def else actual_key
        return PS1TextureAtlas.get_rect(rect_name)

    def resolve_key(self, key_or_role: str) -> str:
        """Normalize and resolve keys with mat_ prefixes or semantic functional roles."""
        role_map = PALETTE_ROLE_MAP.get(self.palette_name, PALETTE_ROLE_MAP["industrial_hazard"])
        if key_or_role in role_map:
            return role_map[key_or_role]
        if key_or_role in self.palette:
            return key_or_role
        if key_or_role.startswith("mat_"):
            clean = key_or_role[4:]
            if clean in self.palette:
                return clean
            if clean in role_map:
                return role_map[clean]
        return key_or_role

    def get_or_create_material(self, key: str) -> bpy.types.Material:
        """Retrieve existing material or create a new stable-ID PS1 Textured Material in Blender."""
        actual_key = self.resolve_key(key)
        self.used_keys.add(actual_key)

        mat_def = self.palette.get(actual_key)
        if not mat_def:
            mat_def = MaterialDef(
                name=f"mat_{actual_key}",
                rgba=(0.5, 0.5, 0.5, 1.0),
                atlas_rect_name="metal_dark_grime",
                roughness=0.7,
                metallic=0.1
            )

        # Stable and descriptive material name: mat_psx_{palette}_{key}_w{wear}
        clean_name = mat_def.name.replace("mat_", "")
        mat_name = f"mat_psx_{self.palette_name}_{clean_name}_w{int(self.wear_level * 100)}"

        # Reuse existing material if present in Blender session (Prevents Material.001 duplicates)
        if mat_name in bpy.data.materials:
            mat = bpy.data.materials[mat_name]
            mat["atlas_rect"] = list(self.get_rect(actual_key))
            mat["atlas_rect_name"] = mat_def.atlas_rect_name
            mat["material_key"] = actual_key
            self.material_cache[actual_key] = mat
            return mat

        mat = bpy.data.materials.new(name=mat_name)
        mat["atlas_rect"] = list(self.get_rect(actual_key))
        mat["atlas_rect_name"] = mat_def.atlas_rect_name
        mat["material_key"] = actual_key
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Create PS1 Principled BSDF setup with Point/Closest texture sampling
        output_node = nodes.new(type="ShaderNodeOutputMaterial")
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        tex_node = nodes.new(type="ShaderNodeTexImage")

        # Crucial PS1 Setting: Closest / Point sampling (Crisp pixel art, no bilinear blur)
        tex_node.interpolation = "Closest"
        tex_node.image = self.atlas_image

        # Vertex color attribute node (PS1 Gouraud / baked vertex grime & blood)
        vcol_node = nodes.new(type="ShaderNodeAttribute")
        vcol_node.attribute_name = "Col"

        # Multiply texture color with vertex color
        mix_node = nodes.new(type="ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = 'MULTIPLY'
        mix_node.inputs[0].default_value = 1.0  # Full multiplier factor
        links.new(tex_node.outputs["Color"], mix_node.inputs[6])
        links.new(vcol_node.outputs["Color"], mix_node.inputs[7])
        links.new(mix_node.outputs[2], bsdf.inputs["Base Color"])

        # PBR settings: Coherent metallic & roughness per category
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = mat_def.roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = mat_def.metallic

        # Transmission / Glass properties
        if mat_def.transmission > 0:
            if "Transmission Weight" in bsdf.inputs:
                bsdf.inputs["Transmission Weight"].default_value = mat_def.transmission
            elif "Transmission" in bsdf.inputs:
                bsdf.inputs["Transmission"].default_value = mat_def.transmission
            if hasattr(mat, "blend_method"):
                mat.blend_method = 'HASHED'

        # Alpha transparency
        if mat_def.alpha < 1.0:
            if "Alpha" in bsdf.inputs:
                bsdf.inputs["Alpha"].default_value = mat_def.alpha
            if hasattr(mat, "blend_method"):
                mat.blend_method = 'HASHED'

        # Connect emission with configurable multiplier
        if mat_def.emission_color and mat_def.emission_strength > 0:
            eff_strength = mat_def.emission_strength * self.emission_multiplier
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = mat_def.emission_color
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = mat_def.emission_color

            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = eff_strength

        # Connect BSDF to surface output
        links.new(bsdf.outputs["BSDF"], output_node.inputs["Surface"])

        self.material_cache[actual_key] = mat
        return mat

    def assign_to_mesh(self, obj: bpy.types.Object):
        """Append all cached palette materials to the object's material slots and record slot indices."""
        from .mesh_builder import MeshBuilder
        MeshBuilder.set_active_material_manager(self)

        for key in self.palette.keys():
            mat = self.get_or_create_material(key)
            if mat.name not in obj.data.materials:
                obj.data.materials.append(mat)
            self.material_indices[key] = obj.data.materials.find(mat.name)

    apply_to_object = assign_to_mesh

    def get_key_by_index(self, index: int) -> Optional[str]:
        """Find material key by slot index."""
        for k, idx in self.material_indices.items():
            if idx == index:
                return k
        keys = list(self.palette.keys())
        if 0 <= index < len(keys):
            return keys[index]
        return None

    def get_rect_by_index(self, index: int) -> Rect:
        """Find UV atlas rect by material slot index."""
        key = self.get_key_by_index(index)
        if key:
            return self.get_rect(key)
        return PS1TextureAtlas.get_rect("metal_dark_grime")

    def get_index(self, key_or_role: str) -> int:
        """Get the material index for face assignment by key, alias, or semantic role."""
        actual_key = self.resolve_key(key_or_role)
        self.used_keys.add(actual_key)
        if actual_key in self.material_indices:
            return self.material_indices[actual_key]
        if actual_key in self.palette:
            return list(self.palette.keys()).index(actual_key)
        return 0

    get_material_index = get_index

    def get_role_index(self, role: str) -> int:
        """Assign material by semantic functional role (e.g. MaterialRole.FRAME)."""
        return self.get_index(role)

    def get_role_material(self, role: str) -> bpy.types.Material:
        """Get Blender Material object by semantic functional role."""
        return self.get_or_create_material(role)

    def get_rgba(self, key_or_role: str) -> Tuple[float, float, float, float]:
        """Get RGBA tuple for vertex coloring."""
        actual_key = self.resolve_key(key_or_role)
        mat_def = self.palette.get(actual_key)
        if mat_def:
            return mat_def.rgba
        return (0.5, 0.5, 0.5, 1.0)

    def get_component_rgba(
        self,
        key_or_role: str,
        component_id: int = 0,
        variation_amount: float = 0.07
    ) -> Tuple[float, float, float, float]:
        """
        Calculates a slightly varied RGBA color for adjoining panels, drawers, or sub-assemblies.
        Uses deterministic pseudo-random modulation based on self.seed and component_id.
        Preserves alpha and keeps colors clamped to [0.0, 1.0].
        """
        base_rgba = self.get_rgba(key_or_role)
        if component_id == 0 or variation_amount <= 0:
            return base_rgba

        h_val = int(hashlib.md5(f"{self.seed}_{component_id}".encode()).hexdigest()[:6], 16)
        norm = (h_val % 1000) / 1000.0  # 0.0 .. 1.0
        delta = (norm * 2.0 - 1.0) * variation_amount
        warmth = (((h_val >> 4) % 1000) / 1000.0) * 0.02

        r = min(1.0, max(0.0, base_rgba[0] * (1.0 + delta + warmth)))
        g = min(1.0, max(0.0, base_rgba[1] * (1.0 + delta)))
        b = min(1.0, max(0.0, base_rgba[2] * (1.0 + delta - warmth)))
        return (r, g, b, base_rgba[3])

    @staticmethod
    def compact_materials(obj: bpy.types.Object):
        """
        Removes unused material slots from obj and remaps polygon material indices,
        leaving only materials actually referenced by geometry.
        Eliminates duplicate or empty primitive slots in glTF and Godot 4 exports.
        """
        if not obj or not obj.data or not isinstance(obj.data, bpy.types.Mesh):
            return

        mesh = obj.data
        if not mesh.polygons or not mesh.materials:
            return

        used_indices = set(p.material_index for p in mesh.polygons)
        if not used_indices:
            return

        old_to_new = {}
        new_materials = []
        for old_idx in sorted(used_indices):
            if 0 <= old_idx < len(mesh.materials) and mesh.materials[old_idx] is not None:
                old_to_new[old_idx] = len(new_materials)
                new_materials.append(mesh.materials[old_idx])

        poly_new_indices = [old_to_new.get(p.material_index, 0) for p in mesh.polygons]

        mesh.materials.clear()
        for mat in new_materials:
            mesh.materials.append(mat)

        for p, new_idx in zip(mesh.polygons, poly_new_indices):
            p.material_index = new_idx

        mesh.update()
