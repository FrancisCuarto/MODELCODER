"""
Selective re-baking script for generator models affected by UV texture atlas defect.
Regenerates access_card_reader first, followed by the remaining 22 affected models,
and validates GLB export + Godot engine import.
"""
import os
import sys
import bpy

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.generators import GENERATOR_REGISTRY
from procedural_assets.export.glb_exporter import GLBExporter
from procedural_assets.export.godot_validator import validate_glb_with_godot, is_godot_available

PUBLIC_MODELS_DIR = os.path.join(current_dir, "web", "public", "models")
os.makedirs(PUBLIC_MODELS_DIR, exist_ok=True)

# Prioritize access_card_reader first, followed by other affected models
AFFECTED_FAMILIES = [
    "access_card_reader",  # Priority 1
    "alarm_siren",
    "antenna_dish",
    "biometric_scanner",
    "camera_monitor",
    "comms_antenna",
    "conveyor_segment",
    "crew_shower",
    "emergency_beacon",
    "food_storage_unit",
    "forklift_cart",
    "hydroponic_tank",
    "nav_console",
    "nutrient_pump",
    "office_door",
    "personal_effects_box",
    "security_camera",
    "speaker_intercom",
    "star_chart_display",
    "station_corridor",
    "station_room",
    "wall_clock",
    "water_recycler",
]

print(f"=== Regenerating & Re-baking {len(AFFECTED_FAMILIES)} Affected Models ===")
print(f"Godot validation available: {is_godot_available()}")

results = []

for family_name in AFFECTED_FAMILIES:
    if family_name not in GENERATOR_REGISTRY:
        print(f"WARNING: '{family_name}' not in GENERATOR_REGISTRY, skipping.")
        continue
    
    config_cls, generator_cls = GENERATOR_REGISTRY[family_name]
    dest_path = os.path.join(PUBLIC_MODELS_DIR, f"{family_name}.glb")
    
    print(f"\n[Baking] {family_name} -> {dest_path}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    cfg = config_cls(name=family_name)
    gen = generator_cls()
    obj = gen.generate(cfg)
    rep = gen.validate(obj, cfg)
    
    glb_out, _ = GLBExporter.export(
        obj=obj,
        config=cfg,
        report=rep,
        filepath=dest_path,
        generator_name=generator_cls.__name__
    )
    
    file_size = os.path.getsize(dest_path) if os.path.exists(dest_path) else 0
    print(f"  Exported GLB: {file_size:,} bytes")
    
    # Run Godot headless verification if available
    godot_res = None
    if is_godot_available() and file_size > 0:
        godot_res = validate_glb_with_godot(dest_path, timeout=10)
        imported = godot_res.get("imported_ok", False)
        print(f"  Godot 4 validation: {'PASS' if imported else 'FAIL'}")
    
    results.append({
        "family": family_name,
        "generator": generator_cls.__name__,
        "size_bytes": file_size,
        "godot_ok": godot_res.get("imported_ok", False) if godot_res else None
    })

print("\n" + "="*70)
print(f"Successfully re-baked {len(results)} affected models.")
print("="*70)
for r in results:
    g_status = "Godot: PASS" if r["godot_ok"] else ("Godot: N/A" if r["godot_ok"] is None else "Godot: FAIL")
    print(f"  {r['family']:<25} | {r['size_bytes']:>8} bytes | {g_status}")
