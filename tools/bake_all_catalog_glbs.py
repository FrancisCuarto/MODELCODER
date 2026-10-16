"""
Bakes default GLBs for all registered generator families directly into web/public/models/
"""
import os
import sys
import bpy

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.generators import GENERATOR_REGISTRY
from procedural_assets.export.glb_exporter import GLBExporter

PUBLIC_MODELS_DIR = os.path.join(current_dir, "web", "public", "models")
os.makedirs(PUBLIC_MODELS_DIR, exist_ok=True)

print(f"=== Baking GLB Models for {len(GENERATOR_REGISTRY)} Families ===")

count = 0
for family_name, (config_cls, generator_cls) in sorted(GENERATOR_REGISTRY.items()):
    dest_path = os.path.join(PUBLIC_MODELS_DIR, f"{family_name}.glb")
    # If already exists and is valid, skip unless forced
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        count += 1
        continue
    
    print(f"Baking GLB for: {family_name}...")
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
    if os.path.exists(dest_path):
        count += 1
        print(f"  -> Generated {dest_path} ({os.path.getsize(dest_path)} bytes)")

print(f"=== Done: {count}/{len(GENERATOR_REGISTRY)} models present in {PUBLIC_MODELS_DIR} ===")
