"""
Universal CLI script to generate procedural assets for Below Nominal using Blender.
Run via Blender:
    blender -b --python generate.py -- [arguments]
"""

import sys
import os
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import bpy
from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    ElectricalPanelConfig,
    TerminalConfig,
    OxypodConfig,
    DoorConfig,
    ServerRackConfig,
    CrateConfig,
    LockerConfig,
    PipeConfig,
    CrashCartConfig,
    OfficeDeskConfig,
    OfficeChairConfig,
    SignPlacardConfig,
    TrashBinConfig,
    LightFixtureConfig,
    FireExtinguisherConfig,
    VentGrateConfig,
    CableBundleConfig,
    StationCorridorConfig,
    StationRoomConfig,
    CrewBedConfig,
    BunkBedConfig,
    NightstandConfig,
    RadiatorHeaterConfig,
    OfficeDoorConfig
)
from procedural_assets.export import (
    GLBExporter,
    resolve_output_dir,
    get_saved_game_dir,
    set_saved_game_dir,
    clear_saved_game_dir,
    FAMILY_CATEGORIES
)
from procedural_assets.core import (
    find_manifest_for_family,
    discover_all_manifests,
    GeneratorManifest
)

def parse_args():
    raw_args = sys.argv
    if "--" in raw_args:
        cli_args = raw_args[raw_args.index("--") + 1:]
    else:
        cli_args = []

    parser = argparse.ArgumentParser(description="Below Nominal - Procedural PSX Asset Generator")
    parser.add_argument(
        "--family",
        type=str,
        default="crash_cart",
        choices=list(GENERATOR_REGISTRY.keys()),
        help="Asset family to generate (all 44 Below Nominal families supported)"
    )
    parser.add_argument("--seed", type=int, default=1337, help="Random generation seed")
    parser.add_argument("--name", type=str, default=None, help="Asset base name")
    parser.add_argument("--budget", type=int, default=550, help="Target triangle budget")
    parser.add_argument("--wear-level", type=float, default=0.65, help="PS1 texture wear & rust (0.0 clean, 1.0 ruined)")
    parser.add_argument("--palette", type=str, default="industrial_hazard", choices=["industrial_hazard", "medbay_clean", "command_bridge", "habitation_worn", "derelict_decay"], help="Sector color palette")
    parser.add_argument("--preset", type=str, default=None, help="Apply a curated parameter preset defined in the generator's manifest.json")
    parser.add_argument("--collision", action="store_true", default=False, help="Generate Godot 4 collision mesh")
    parser.add_argument("--collision-type", choices=["box", "convex_hull"], default="box", help="Collision shape type")
    parser.add_argument("--collision-suffix", choices=["-convcolonly", "-colonly", "-col"], default="-convcolonly", help="Godot import suffix")
    parser.add_argument("--pivot-rule", choices=["floor_center", "center", "wall_back", "keep"], default="floor_center", help="Pivot normalization rule")
    parser.add_argument("--no-godot-test", action="store_true", default=False, help="Skip live headless Godot verification")
    parser.add_argument(
        "-o", "--out", "--output-dir",
        dest="output_dir",
        type=str,
        default=None,
        help="Target output directory (e.g. 'D:/MiJuego/assets/models' or relative 'output')"
    )
    parser.add_argument(
        "--set-game-dir", "--set-default-output",
        dest="set_game_dir",
        type=str,
        default=None,
        help="Persistently configure a default game asset folder in .export_config.json"
    )
    parser.add_argument(
        "--get-game-dir", "--show-config",
        dest="get_game_dir",
        action="store_true",
        help="Display the currently saved game project export directory"
    )
    parser.add_argument(
        "--clear-game-dir",
        dest="clear_game_dir",
        action="store_true",
        help="Reset and clear the saved game project export directory"
    )
    parser.add_argument(
        "--category-subfolder", "--by-category",
        dest="category_subfolder",
        action="store_true",
        help="Automatically group models into subfolders by category (furniture, medical, architecture, fixtures, infrastructure)"
    )
    parser.add_argument("--save-blend", action="store_true", help="Also save .blend file for visual inspection")

    # Generic dimension overrides
    parser.add_argument("--width", type=float, default=None, help="Custom width in meters")
    parser.add_argument("--height", type=float, default=None, help="Custom height in meters")
    parser.add_argument("--depth", type=float, default=None, help="Custom depth in meters")

    # Station Corridor variants
    parser.add_argument("--corridor-type", choices=["straight", "corner_90", "t_junction", "cross_junction", "doorway_arch", "dead_end"], default="straight")
    parser.add_argument("--corridor-floor", choices=["tread_plate", "grated_trench", "smooth_tile"], default="tread_plate")
    parser.add_argument("--corridor-wall", choices=["structural_ribs", "recessed_panels", "smooth_bulkhead"], default="structural_ribs")
    parser.add_argument("--corridor-ceiling", choices=["exposed_beams", "vaulted_conduit", "flat_recessed"], default="exposed_beams")
    parser.add_argument("--corridor-lighting", choices=["working", "flickering", "emergency_red", "unlit"], default="working")
    parser.add_argument("--corridor-damage", choices=["pristine", "blood_oil_stain", "collapsed_ceiling_wires", "breached_vent"], default="pristine")
    parser.add_argument("--no-corridor-lighting", action="store_true", help="Omit ceiling luminaire")
    parser.add_argument("--no-corridor-cables", action="store_true", help="Omit conduit raceways")
    parser.add_argument("--no-corridor-alcove", action="store_true", help="Omit wall niche")
    parser.add_argument("--no-corridor-hazard", action="store_true", help="Omit floor hazard stripes")

    # Station Room variants
    parser.add_argument("--room-archetype", choices=["medbay_lab", "control_hub", "cargo_bay", "airlock_chamber", "crew_quarters"], default="medbay_lab")
    parser.add_argument("--no-door-north", action="store_true", help="Solid north (+Y) wall")
    parser.add_argument("--no-door-south", action="store_true", help="Solid south (-Y) wall")
    parser.add_argument("--door-east", action="store_true", help="Add doorway on east (+X) wall")
    parser.add_argument("--door-west", action="store_true", help="Add doorway on west (-X) wall")
    parser.add_argument("--room-pillars", choices=["none", "center_single", "dual_columns", "perimeter_buttresses"], default="perimeter_buttresses")
    parser.add_argument("--room-elevation", choices=["flat", "raised_platform", "sunken_pit"], default="flat")
    parser.add_argument("--room-window", action="store_true", help="Reinforced observation viewport window")
    parser.add_argument("--room-gantry", action="store_true", help="Overhead industrial crane beam")
    parser.add_argument("--room-drain", action="store_true", help="Center drainage grate trench")
    parser.add_argument("--room-lighting", choices=["clean_white", "emergency_red", "medbay_cyan", "dim_amber"], default="clean_white")

    # Crash Cart variants
    parser.add_argument("--cart-drawers", type=int, default=4, help="Number of drawers (1-6)")
    parser.add_argument("--cart-drawer-mode", choices=["staggered", "all_closed", "top_open", "all_open"], default="staggered")
    parser.add_argument("--cart-slide-max", type=float, default=0.22, help="Max drawer pullout in meters")
    parser.add_argument("--cart-handle", choices=["metal_bar", "recessed_lip"], default="metal_bar")
    parser.add_argument("--no-cart-monitor", action="store_true", help="Omit top CRT/defibrillator")
    parser.add_argument("--no-cart-handle", action="store_true", help="Omit push handle")
    parser.add_argument("--no-cart-o2", action="store_true", help="Omit oxygen tank rack")
    parser.add_argument("--cart-o2-tanks", type=int, default=2, help="Oxygen cylinders (1-3)")
    parser.add_argument("--cart-color", choices=["medical_red", "station_grey", "hazard_orange", "clean_teal"], default="medical_red")

    # Office Desk variants
    parser.add_argument("--desk-legs", choices=["tubular_4leg", "panel_sides", "t_cantilever"], default="tubular_4leg")
    parser.add_argument("--desk-pedestals", choices=["none", "left", "right", "dual_pedestals"], default="right")
    parser.add_argument("--desk-drawers", type=int, default=3, help="Drawers per pedestal (1-4)")
    parser.add_argument("--desk-drawer-style", choices=["all_closed", "top_open", "staggered"], default="top_open")
    parser.add_argument("--desk-partition", action="store_true", help="Add privacy partition screen")
    parser.add_argument("--desk-shelf", action="store_true", help="Add under-desk CPU/storage shelf")
    parser.add_argument("--no-desk-grommet", action="store_true", help="Omit cable grommet")
    parser.add_argument("--desk-surface", choices=["dark_grey_laminate", "beige_composite", "hazard_orange"], default="dark_grey_laminate")

    # Office Chair variants
    parser.add_argument("--chair-base", choices=["five_star_casters", "tubular_four_legs", "floor_bolted_swivel"], default="five_star_casters")
    parser.add_argument("--chair-arms", choices=["dual_armrests", "one_broken", "none"], default="dual_armrests")
    parser.add_argument("--chair-backrest", choices=["standard_mid", "high_back_headrest", "low_task"], default="standard_mid")
    parser.add_argument("--chair-tilt", type=float, default=6.0, help="Backrest recline angle in degrees")
    parser.add_argument("--chair-spokes", type=int, default=5, help="Number of base spokes/legs (4-6)")
    parser.add_argument("--chair-upholstery", choices=["dark_vinyl", "worn_blue", "hazard_brown"], default="dark_vinyl")

    # Sign Placard variants
    parser.add_argument("--sign-type", choices=["hazard_biohazard", "station_exit", "sector_identification", "high_voltage"], default="hazard_biohazard")
    parser.add_argument("--sign-mount", choices=["wall_flush", "ceiling_hanging", "perpendicular_flag"], default="wall_flush")
    parser.add_argument("--sign-damage", choices=["pristine", "bent_corner", "hanging_crooked"], default="pristine")
    parser.add_argument("--sign-chain-len", type=float, default=0.45, help="Hanging chain drop length in meters")

    # Trash Bin variants
    parser.add_argument("--bin-type", choices=["pedal_can", "hazard_drum", "mesh_office_basket"], default="pedal_can")
    parser.add_argument("--bin-rectangular", action="store_true", help="Rectangular instead of cylindrical bin")
    parser.add_argument("--bin-lid", choices=["closed", "ajar", "open_wide", "missing"], default="ajar")
    parser.add_argument("--no-bin-pedal", action="store_true", help="Omit foot step pedal")
    parser.add_argument("--bin-overflow", action="store_true", help="Show overflowing low-poly trash")

    # Light Fixture variants
    parser.add_argument("--light-type", choices=["fluorescent_troffer", "bulkhead_cage", "emergency_beacon"], default="fluorescent_troffer")
    parser.add_argument("--light-state", choices=["working", "flickering_one_dead", "dead_unlit", "emergency_red"], default="working")
    parser.add_argument("--light-tubes", type=int, default=2, help="Number of fluorescent tubes (1-3)")
    parser.add_argument("--light-wire-guard", action="store_true", help="Protective wire mesh cage")
    parser.add_argument("--light-dangling-wire", action="store_true", help="Dangling disconnected power lead")

    # Fire Extinguisher variants
    parser.add_argument("--ext-mount", choices=["wall_bracket", "emergency_cabinet"], default="wall_bracket")
    parser.add_argument("--ext-glass", choices=["intact_glass", "broken_shattered", "door_open"], default="intact_glass")
    parser.add_argument("--no-ext-gauge", action="store_true", help="Omit pressure gauge dial")
    parser.add_argument("--no-ext-hose", action="store_true", help="Omit discharge hose and horn")
    parser.add_argument("--no-ext-sign", action="store_true", help="Omit photoluminescent wall sign")

    # Vent Grate variants
    parser.add_argument("--vent-type", choices=["wall_louver", "floor_heavy_grate", "perforated_metal"], default="wall_louver")
    parser.add_argument("--vent-state", choices=["bolted_secure", "hanging_by_one_screw", "removed_duct_exposed"], default="bolted_secure")
    parser.add_argument("--vent-fan", action="store_true", help="Add internal spinning circulation fan")
    parser.add_argument("--vent-angle", type=float, default=32.0, help="Hanging tilt angle if loose")

    # Cable Bundle variants
    parser.add_argument("--cable-type", choices=["hanging_umbilical", "ladder_rack_tray", "vertical_riser"], default="hanging_umbilical")
    parser.add_argument("--cable-count", type=int, default=4, help="Number of cables in bundle (2-6)")
    parser.add_argument("--cable-sag", type=float, default=0.28, help="Catenary sag depth in meters")
    parser.add_argument("--cable-severed", action="store_true", help="Include cut / sparking exposed wire")
    parser.add_argument("--no-cable-ties", action="store_true", help="Omit clamp bands / zip ties")
    parser.add_argument("--no-cable-junction", action="store_true", help="Omit terminal junction breakout boxes")

    # Terminal variants
    parser.add_argument("--terminal-type", choices=["wall", "desktop", "pedestal"], default="wall")
    parser.add_argument("--terminal-state", choices=["active", "alarm", "damaged", "powered_off"], default="active")
    parser.add_argument("--keyboard-style", choices=["integrated", "tray_projecting", "keypad_numeric", "none"], default="integrated")
    parser.add_argument("--phosphor", choices=["green", "amber"], default="green", help="CRT phosphor color")

    # Oxypod variants
    parser.add_argument("--oxypod-type", choices=["wall_station", "portable_canister", "dual_tank_rig"], default="wall_station")
    parser.add_argument("--oxygen-level", type=float, default=0.85, help="Oxygen fluid level 0.0 to 1.0")
    parser.add_argument("--no-mask", action="store_true", help="Omit mask dock and hose")

    # Door variants
    parser.add_argument("--door-type", choices=["standard_sliding", "heavy_airlock", "emergency_bulkhead", "manual_hatch"], default="standard_sliding")
    parser.add_argument("--door-open", type=float, default=0.0, help="Door open ratio (0.0 closed, 0.15 jammed, 1.0 open)")
    parser.add_argument("--door-access", choices=["card_reader", "manual_wheel", "none"], default="card_reader")

    # Server Rack variants
    parser.add_argument("--rack-type", choices=["consciousness_bank", "telemetry_server", "cryo_cooling_rack"], default="consciousness_bank")
    parser.add_argument("--rack-occupancy", type=float, default=0.80, help="Consciousness cartridge population 0.0 to 1.0")
    parser.add_argument("--rack-cooling", choices=["cooling_pipes", "louver_vents"], default="cooling_pipes")

    # Crate variants
    parser.add_argument("--crate-type", choices=["cargo_chest", "chemical_drum", "battery_cell", "medical_crate"], default="cargo_chest")
    parser.add_argument("--crate-lid", choices=["closed", "ajar_open"], default="closed")

    # Locker variants
    parser.add_argument("--locker-cols", type=int, default=2, help="Number of locker columns (1 to 4)")
    parser.add_argument("--locker-door", choices=["all_closed", "one_open"], default="all_closed")
    parser.add_argument("--no-bench", action="store_true", help="Omit front locker bench")

    # Pipe variants
    parser.add_argument("--pipe-type", choices=["valve_assembly", "straight", "elbow_90", "t_junction"], default="valve_assembly")
    parser.add_argument("--pipe-valve", choices=["handwheel_red", "lever_quarter_turn", "none"], default="handwheel_red")
    parser.add_argument("--pipe-insulation", action="store_true", help="Add thermal lagging insulation layer")

    # Electrical Panel variants
    parser.add_argument("--no-crt", action="store_true", help="Disable CRT on electrical panel")
    parser.add_argument("--knife-switch", action="store_true", help="Add heavy knife breaker switch")
    parser.add_argument("--door-ajar", action="store_true", help="Front maintenance door open")

    # Crew Bed variants
    parser.add_argument("--bed-type", choices=["crew_cot", "medical_gurney", "enclosed_pod"], default="crew_cot")
    parser.add_argument("--mattress-state", choices=["made_clean", "rumpled_disheveled", "bare_foam_stained"], default="made_clean")
    parser.add_argument("--no-pillow", action="store_true", help="Omit pillow")
    parser.add_argument("--no-under-drawers", action="store_true", help="Omit under-bed storage drawers")
    parser.add_argument("--bed-guardrails", action="store_true", help="Add safety/restraint side rails")
    parser.add_argument("--headrest-incline", type=float, default=0.0, help="Headrest incline angle (0 to 35 deg)")
    parser.add_argument("--blanket-color", choices=["station_gray", "medical_blue", "emergency_orange", "brown_wool"], default="station_gray")

    # Bunk Bed variants
    parser.add_argument("--bunk-frame", choices=["tubular_metal", "reinforced_bulkhead", "capsule_stacked"], default="tubular_metal")
    parser.add_argument("--ladder-pos", choices=["front_right", "front_left", "side_head"], default="front_right")
    parser.add_argument("--no-guardrail", action="store_true", help="Omit upper bunk guardrail")
    parser.add_argument("--lower-bunk-state", choices=["made", "disheveled", "bare_foam_stained"], default="made")
    parser.add_argument("--upper-bunk-state", choices=["made", "disheveled", "bare_foam_stained", "empty_storage"], default="made")
    parser.add_argument("--no-reading-lights", action="store_true", help="Omit personal bunk reading LEDs")
    parser.add_argument("--no-bunk-lockers", action="store_true", help="Omit under-bunk footlockers")
    parser.add_argument("--bunk-curtains", action="store_true", help="Add privacy curtains")
    parser.add_argument("--bunk-blanket-color", choices=["station_gray", "medical_blue", "emergency_orange", "brown_wool"], default="station_gray")

    # Nightstand variants
    parser.add_argument("--stand-type", choices=["crew_locker_cubby", "sliding_drawers", "medical_tray_cart", "wall_mounted"], default="crew_locker_cubby")
    parser.add_argument("--drawers", type=int, default=2, help="Number of drawers (1-3)")
    parser.add_argument("--drawer-open", type=float, default=0.0, help="Drawer open extension ratio (0.0 to 0.5)")
    parser.add_argument("--no-raised-rim", action="store_true", help="Omit anti-slide rim on tabletop")
    parser.add_argument("--no-lamp", action="store_true", help="Omit bedside gooseneck lamp")
    parser.add_argument("--lamp-state", choices=["on", "off", "flickering"], default="on")
    parser.add_argument("--swivel-tray", action="store_true", help="Add medical over-bed cantilever tray")

    # Radiator Heater variants
    parser.add_argument("--heater-type", choices=["wall_radiator_fins", "convector_blower", "space_tower_heater"], default="wall_radiator_fins")
    parser.add_argument("--fin-count", type=int, default=8, help="Number of radiator fins (4-14)")
    parser.add_argument("--not-operational", action="store_true", help="Disable heating element glow")
    parser.add_argument("--no-thermostat", action="store_true", help="Omit thermostat control dial")
    parser.add_argument("--no-steam-pipe", action="store_true", help="Omit pipe connection with handwheel")
    parser.add_argument("--heater-damage", choices=["intact", "battered_bent_fins", "leaking_burst"], default="intact")

    # Office Door variants
    parser.add_argument("--office-door-style", choices=["single_swing", "double_swing", "sliding_pocket"], default="single_swing")
    parser.add_argument("--glass-type", choices=["wired_safety_glass", "clear_tinted", "frosted_privacy"], default="wired_safety_glass")
    parser.add_argument("--open-angle", type=float, default=0.0, help="Door open angle in degrees (or sliding open distance)")
    parser.add_argument("--glass-damage", choices=["intact", "cracked_spiderweb", "shattered_missing"], default="intact")
    parser.add_argument("--office-door-handle", choices=["horizontal_push_bar", "industrial_lever", "recessed_pull"], default="horizontal_push_bar")
    parser.add_argument("--no-kickplate", action="store_true", help="Omit bottom steel kickplate")
    parser.add_argument("--has-transom", action="store_true", help="Add upper observation transom window")

    # Dynamically inject CLI arguments from any generator containing a manifest.json
    all_manifests = discover_all_manifests()
    for fam_name, manifest in all_manifests.items():
        manifest.add_to_argparse(parser)

    return parser.parse_args(cli_args)

def create_config_for_family(args):
    family = args.family
    name = args.name or f"bn_{family}_{args.seed}"

    # 1. Dynamic Manifest Resolution (Contract v1)
    manifest = find_manifest_for_family(family)
    if manifest and family in GENERATOR_REGISTRY:
        cfg_cls, _ = GENERATOR_REGISTRY[family]
        init_kwargs = manifest.get_default_values()

        # Apply preset if specified
        if getattr(args, "preset", None):
            matched_preset = False
            for pr in manifest.presets:
                if pr.id == args.preset:
                    init_kwargs.update(pr.values)
                    print(f"[PRESET] Applied manifest preset '{pr.id}' ({pr.name})")
                    matched_preset = True
                    break
            if not matched_preset:
                valid_ids = [p.id for p in manifest.presets]
                print(f"[WARN] Preset '{args.preset}' not found in manifest for '{family}'. Available presets: {valid_ids}")

        # Override with explicit CLI flags from manifest
        manifest_kwargs = manifest.build_config_kwargs(args)
        init_kwargs.update(manifest_kwargs)

        # Common overrides
        init_kwargs["seed"] = args.seed
        init_kwargs["name"] = name
        init_kwargs["wear_level"] = args.wear_level
        if args.budget != 550:
            init_kwargs["target_tri_budget"] = args.budget
        if args.palette and hasattr(cfg_cls, "palette_name"):
            init_kwargs["palette_name"] = args.palette

        # Dimensional overrides
        dummy = cfg_cls(name=name)
        if args.width:
            for w_field in ("width", "table_width", "panel_width"):
                if hasattr(dummy, w_field):
                    init_kwargs[w_field] = args.width
                    break
        if args.height:
            for h_field in ("height", "table_height", "panel_height"):
                if hasattr(dummy, h_field):
                    init_kwargs[h_field] = args.height
                    break
        if args.depth:
            for d_field in ("depth", "table_length", "length"):
                if hasattr(dummy, d_field):
                    init_kwargs[d_field] = args.depth
                    break

        valid_fields = cfg_cls.__dataclass_fields__.keys() if hasattr(cfg_cls, "__dataclass_fields__") else init_kwargs.keys()
        filtered = {k: v for k, v in init_kwargs.items() if k in valid_fields}
        return cfg_cls(**filtered)

    # 2. Legacy fallback for families without a manifest.json
    if family == "station_corridor":
        return StationCorridorConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            corridor_type=args.corridor_type,
            width=args.width or 3.0,
            length=args.height or 4.0,  # CLI height or default length
            height=args.depth or 3.0,   # CLI depth or default height
            floor_style=args.corridor_floor,
            wall_style=args.corridor_wall,
            ceiling_style=args.corridor_ceiling,
            has_integrated_lighting=not args.no_corridor_lighting,
            lighting_state=args.corridor_lighting,
            has_cable_runs=not args.no_corridor_cables,
            has_wall_alcove=not args.no_corridor_alcove,
            has_hazard_stripes=not args.no_corridor_hazard,
            damage_state=args.corridor_damage
        )
    elif family == "station_room":
        return StationRoomConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            room_archetype=args.room_archetype,
            width=args.width or 6.0,
            depth=args.height or 8.0,
            height=args.depth or 3.4,
            door_north=not args.no_door_north,
            door_south=not args.no_door_south,
            door_east=args.door_east,
            door_west=args.door_west,
            pillar_layout=args.room_pillars,
            floor_elevation=args.room_elevation,
            has_observation_window=args.room_window,
            has_overhead_gantry=args.room_gantry,
            has_floor_drain=args.room_drain,
            lighting_color=args.room_lighting
        )
    elif family == "crash_cart":
        return CrashCartConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            width=args.width or 0.65,
            height=args.height or 0.85,
            depth=args.depth or 0.48,
            drawer_count=args.cart_drawers,
            drawer_open_mode=args.cart_drawer_mode,
            drawer_slide_max=args.cart_slide_max,
            drawer_handle_style=args.cart_handle,
            has_top_monitor=not args.no_cart_monitor,
            monitor_phosphor_color=args.phosphor,
            has_push_handle=not args.no_cart_handle,
            has_oxygen_rack=not args.no_cart_o2,
            oxygen_tank_count=args.cart_o2_tanks,
            body_color_preset=args.cart_color
        )
    elif family == "office_desk":
        return OfficeDeskConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            width=args.width or 1.40,
            height=args.height or 0.75,
            depth=args.depth or 0.70,
            leg_style=args.desk_legs,
            pedestal_layout=args.desk_pedestals,
            drawer_count_per_pedestal=args.desk_drawers,
            drawer_open_style=args.desk_drawer_style,
            has_cable_grommet=not args.no_desk_grommet,
            has_partition_screen=args.desk_partition,
            has_under_shelf=args.desk_shelf,
            surface_material=args.desk_surface
        )
    elif family == "office_chair":
        return OfficeChairConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            seat_width=args.width or 0.52,
            seat_height=args.height or 0.48,
            seat_depth=args.depth or 0.48,
            base_style=args.chair_base,
            armrest_style=args.chair_arms,
            backrest_style=args.chair_backrest,
            backrest_tilt=args.chair_tilt,
            spoke_count=args.chair_spokes,
            upholstery_color=args.chair_upholstery
        )
    elif family == "sign_placard":
        return SignPlacardConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            width=args.width or 0.70,
            height=args.height or 0.28,
            sign_type=args.sign_type,
            mount_type=args.sign_mount,
            damage_style=args.sign_damage,
            hanging_chain_length=args.sign_chain_len
        )
    elif family == "trash_bin":
        return TrashBinConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            height=args.height or 0.55,
            radius=(args.width / 2.0) if args.width else 0.20,
            is_rectangular=args.bin_rectangular,
            bin_type=args.bin_type,
            lid_state=args.bin_lid,
            has_foot_pedal=not args.no_bin_pedal,
            has_overflowing_trash=args.bin_overflow
        )
    elif family == "light_fixture":
        return LightFixtureConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            length=args.height or 1.25,
            width=args.width or 0.32,
            depth=args.depth or 0.12,
            fixture_type=args.light_type,
            lighting_state=args.light_state,
            tube_count=args.light_tubes,
            has_wire_guard=args.light_wire_guard,
            has_dangling_wire=args.light_dangling_wire
        )
    elif family == "fire_extinguisher":
        return FireExtinguisherConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            tank_height=args.height or 0.52,
            tank_radius=(args.width / 2.0) if args.width else 0.09,
            mount_style=args.ext_mount,
            cabinet_glass_state=args.ext_glass,
            has_pressure_gauge=not args.no_ext_gauge,
            has_hose_nozzle=not args.no_ext_hose,
            has_wall_sign=not args.no_ext_sign
        )
    elif family == "vent_grate":
        return VentGrateConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            width=args.width or 0.60,
            height=args.height or 0.60,
            grate_type=args.vent_type,
            grate_state=args.vent_state,
            hanging_angle=args.vent_angle,
            has_fan_blades=args.vent_fan
        )
    elif family == "cable_bundle":
        return CableBundleConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            length=args.height or 2.00,
            bundle_type=args.cable_type,
            cable_count=args.cable_count,
            max_sag=args.cable_sag,
            has_severed_wire=args.cable_severed,
            has_support_ties=not args.no_cable_ties,
            has_junction_box=not args.no_cable_junction
        )
    elif family == "electrical_panel":
        return ElectricalPanelConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            width=args.width or 0.70,
            height=args.height or 0.90,
            depth=args.depth or 0.22,
            has_crt=not args.no_crt,
            crt_phosphor_color=args.phosphor,
            has_knife_switch=args.knife_switch,
            door_ajar=args.door_ajar
        )
    elif family == "terminal":
        return TerminalConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            terminal_type=args.terminal_type,
            state=args.terminal_state,
            keyboard_style=args.keyboard_style,
            width=args.width or 0.55,
            height=args.height or 0.65,
            depth=args.depth or 0.35,
            phosphor_color=args.phosphor
        )
    elif family == "oxypod":
        return OxypodConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            station_type=args.oxypod_type,
            oxygen_level=args.oxygen_level,
            has_mask_dock=not args.no_mask,
            tank_height=args.height or 0.95,
            tank_radius=(args.width / 2.0) if args.width else 0.18
        )
    elif family == "door":
        return DoorConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            door_type=args.door_type,
            open_ratio=args.door_open,
            access_interface=args.door_access,
            width=args.width or 2.00,
            height=args.height or 2.40,
            frame_depth=args.depth or 0.35
        )
    elif family == "server_rack":
        return ServerRackConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            rack_type=args.rack_type,
            cartridge_occupancy=args.rack_occupancy,
            cooling_system=args.rack_cooling,
            width=args.width or 0.80,
            height=args.height or 2.00,
            depth=args.depth or 0.85
        )
    elif family == "crate":
        return CrateConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            crate_type=args.crate_type,
            lid_state=args.crate_lid,
            width=args.width or 0.80,
            height=args.height or 0.65,
            depth=args.depth or 0.60
        )
    elif family == "locker":
        return LockerConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            columns=args.locker_cols,
            door_state=args.locker_door,
            has_integrated_bench=not args.no_bench,
            height=args.height or 1.90,
            depth=args.depth or 0.50
        )
    elif family == "pipes":
        return PipeConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            pipe_type=args.pipe_type,
            valve_type=args.pipe_valve,
            has_insulation_layer=args.pipe_insulation,
            length=args.height or 1.80,
            radius=args.width or 0.09
        )
    elif family == "crew_bed":
        return CrewBedConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            bed_type=args.bed_type,
            width=args.width or 1.00,
            length=args.height or 2.05,
            height=args.depth or 0.65,
            mattress_state=args.mattress_state,
            has_pillow=not args.no_pillow,
            has_under_drawers=not args.no_under_drawers,
            has_guardrails=args.bed_guardrails,
            headrest_incline=args.headrest_incline,
            blanket_color=args.blanket_color
        )
    elif family == "bunk_bed":
        return BunkBedConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            frame_style=args.bunk_frame,
            width=args.width or 1.05,
            length=args.height or 2.05,
            height=args.depth or 2.05,
            ladder_position=args.ladder_pos,
            upper_guardrail=not args.no_guardrail,
            lower_bunk_state=args.lower_bunk_state,
            upper_bunk_state=args.upper_bunk_state,
            has_reading_lights=not args.no_reading_lights,
            has_storage_lockers=not args.no_bunk_lockers,
            has_curtains=args.bunk_curtains,
            blanket_color=args.bunk_blanket_color
        )
    elif family == "nightstand":
        return NightstandConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            stand_type=args.stand_type,
            width=args.width or 0.48,
            depth=args.depth or 0.44,
            height=args.height or 0.68,
            drawer_count=args.drawers,
            drawer_open_ratio=args.drawer_open,
            has_raised_rim=not args.no_raised_rim,
            has_bedside_lamp=not args.no_lamp,
            lamp_state=args.lamp_state,
            has_swivel_tray=args.swivel_tray
        )
    elif family == "radiator_heater":
        return RadiatorHeaterConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            heater_type=args.heater_type,
            width=args.width or 0.85,
            height=args.height or 0.70,
            depth=args.depth or 0.22,
            fin_count=args.fin_count,
            is_operational=not args.not_operational,
            has_thermostat_dial=not args.no_thermostat,
            has_steam_pipe=not args.no_steam_pipe,
            damage_state=args.heater_damage
        )
    elif family == "office_door":
        return OfficeDoorConfig(
            seed=args.seed,
            name=name,
            target_tri_budget=args.budget,
            wear_level=args.wear_level,
            door_style=args.office_door_style,
            glass_type=args.glass_type,
            width=args.width or 1.20,
            height=args.height or 2.40,
            frame_depth=args.depth or 0.22,
            open_angle_deg=args.open_angle,
            glass_damage=args.glass_damage,
            handle_type=args.office_door_handle,
            has_kickplate=not args.no_kickplate,
            has_transom=args.has_transom
        )
    elif family in GENERATOR_REGISTRY:
        cfg_cls, _ = GENERATOR_REGISTRY[family]
        kwargs = {
            "seed": args.seed,
            "name": name,
            "wear_level": args.wear_level,
        }
        if args.budget != 550:
            kwargs["target_tri_budget"] = args.budget

        dummy = cfg_cls(name=name)
        if args.width:
            for w_field in ("width", "table_width", "panel_width"):
                if hasattr(dummy, w_field):
                    kwargs[w_field] = args.width
                    break
        if args.height:
            for h_field in ("height", "table_height", "panel_height"):
                if hasattr(dummy, h_field):
                    kwargs[h_field] = args.height
                    break
        if args.depth:
            for d_field in ("depth", "table_length", "length"):
                if hasattr(dummy, d_field):
                    kwargs[d_field] = args.depth
                    break
        return cfg_cls(**kwargs)
    else:
        raise ValueError(f"Unknown family: {family}")

def main():
    args = parse_args()

    # Handle persistent configuration operations
    raw_args = sys.argv
    cli_tokens = raw_args[raw_args.index("--") + 1:] if "--" in raw_args else []

    if args.set_game_dir:
        saved_dir = set_saved_game_dir(args.set_game_dir)
        print(f"[CONFIG] Persistent game asset directory set to: {saved_dir}")
        print("All future model exports will automatically be saved to this folder unless overridden with -o / --output-dir.")
        if "--family" not in cli_tokens:
            sys.exit(0)

    if args.clear_game_dir:
        clear_saved_game_dir()
        print("[CONFIG] Cleared persistent game asset directory. Exports will default to local 'output/' folder.")
        sys.exit(0)

    if args.get_game_dir:
        saved = get_saved_game_dir()
        if saved:
            print(f"[CONFIG] Active persistent game asset directory: {saved}")
        else:
            print("[CONFIG] No persistent game asset directory configured. Current default is local 'output/' folder.")
        sys.exit(0)

    target_output_dir = resolve_output_dir(
        cli_arg=args.output_dir,
        family=args.family,
        organize_by_category=args.category_subfolder
    )

    print(f"=== Below Nominal Procedural Generator ===")
    print(f"Family: {args.family} | Seed: {args.seed}")
    print(f"Target Directory: {target_output_dir}")

    bpy.ops.wm.read_factory_settings(use_empty=True)

    config = create_config_for_family(args)
    if hasattr(config, "palette_name") and args.palette:
        config.palette_name = args.palette
    if hasattr(config, "add_collision_mesh"):
        config.add_collision_mesh = args.collision
    if hasattr(config, "collision_type") and args.collision_type:
        config.collision_type = args.collision_type
    if hasattr(config, "collision_suffix") and args.collision_suffix:
        config.collision_suffix = args.collision_suffix
    if hasattr(config, "pivot_rule") and args.pivot_rule:
        config.pivot_rule = args.pivot_rule

    _, generator_cls = GENERATOR_REGISTRY[args.family]
    generator = generator_cls()
    generator.config = config

    try:
        obj = generator.generate(config)
    except TypeError:
        obj = generator.generate()

    report = generator.validate(obj, config)

    print("\n--- Validation Report ---")
    print(f"Valid Geometry: {report.is_valid}")
    print(f"Triangles: {report.triangle_count} / Budget: {report.target_tri_budget} (Ratio: {report.triangle_count / max(1, report.target_tri_budget):.2f})")
    print(f"Vertices: {report.vertex_count}")
    print(f"Dimensions: {report.dimensions[0]:.3f}m x {report.dimensions[1]:.3f}m x {report.dimensions[2]:.3f}m")
    print(f"Materials ({len(report.material_names)}): {', '.join(report.material_names)}")
    print(f"Vertex Colors: {report.has_vertex_colors}")
    if report.warnings:
        print(f"Warnings: {report.warnings}")
    if report.errors:
        print(f"Errors: {report.errors}")
        sys.exit(1)

    glb_path = os.path.join(target_output_dir, f"{config.name}.glb")
    res = GLBExporter.export(
        obj=obj,
        config=config,
        report=report,
        filepath=glb_path,
        generator_name=generator_cls.__name__,
        validate_with_godot=not args.no_godot_test
    )

    print(f"\n[SUCCESS] Exported GLB: {res.glb_path}")
    print(f"[SUCCESS] Exported JSON: {res.json_path}")
    if hasattr(res, "report_json_path") and res.report_json_path:
        print(f"[SUCCESS] Exported Report JSON: {res.report_json_path}")
    if hasattr(res, "report_md_path") and res.report_md_path:
        print(f"[SUCCESS] Exported Report MD: {res.report_md_path}")

    if args.save_blend:
        blend_path = os.path.join(target_output_dir, f"{config.name}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"[SUCCESS] Saved Blender scene: {blend_path}")

    print("=== Generation Complete ===")

if __name__ == "__main__":
    main()
