"""
Bootstrap utility to generate declarative manifest.json templates for all
generator families in Below Nominal.
Introspects family configuration dataclasses, infers types and defaults,
and outputs JSON Schema (generator-v1.json) compliant manifests.
"""

import os
import sys
import json
import dataclasses
from typing import Dict, Any, List

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.generators import GENERATOR_REGISTRY
from procedural_assets.export.destination import FAMILY_CATEGORIES

SCHEMA_URL = "https://raw.githubusercontent.com/usuario/modelcoder-community/main/schemas/generator-v1.json"

def infer_param_def(field: dataclasses.Field) -> Dict[str, Any]:
    key = field.name
    val = field.default if field.default is not dataclasses.MISSING else None
    
    # Human-readable label
    label = key.replace("_", " ").title()

    # Determine type
    ptype = "string"
    step = None
    min_val = None
    max_val = None
    options = None

    if isinstance(val, bool):
        ptype = "boolean"
    elif isinstance(val, int):
        ptype = "int"
        step = 1
        min_val = 0
        if key in ("seed", "random_seed"):
            ptype = "seed"
            min_val = 0
            max_val = 2147483647
    elif isinstance(val, float):
        ptype = "float"
        min_val = 0.0
        step = 0.05
        if "wear" in key or "damage" in key or "dirt" in key:
            min_val = 0.0
            max_val = 1.0
            step = 0.05
    elif isinstance(val, (list, tuple)) and len(val) == 4 and all(isinstance(x, (int, float)) for x in val):
        ptype = "color_rgba"
    elif isinstance(val, str):
        ptype = "string"
        if key == "palette_name":
            ptype = "enum"
            options = [
                {"value": "industrial_hazard", "label": "Industrial Hazard"},
                {"value": "medbay_clean", "label": "Medbay Clean"},
                {"value": "command_bridge", "label": "Command Bridge"},
                {"value": "habitation_worn", "label": "Habitation Worn"},
                {"value": "derelict_decay", "label": "Derelict Decay"}
            ]

    # Assign group
    group = "General"
    if key in ("width", "height", "depth", "length", "radius", "thickness"):
        group = "Dimensiones"
    elif key in ("palette_name", "wear_level", "color", "base_color"):
        group = "Materiales"
    elif key in ("seed", "random_seed", "target_tri_budget"):
        group = "Rendimiento"

    param = {
        "key": key,
        "label": label,
        "type": ptype,
        "default": val,
        "group": group
    }
    if min_val is not None:
        param["min"] = min_val
    if max_val is not None:
        param["max"] = max_val
    if step is not None:
        param["step"] = step
    if options is not None:
        param["options"] = options

    return param

def bootstrap_family(family_name: str, config_cls: Any, force: bool = False) -> bool:
    generators_dir = os.path.join(current_dir, "procedural_assets", "generators")
    family_dir = os.path.join(generators_dir, family_name)
    manifest_path = os.path.join(family_dir, "manifest.json")

    if os.path.exists(manifest_path) and not force:
        print(f"[SKIP] Manifest already exists for '{family_name}'")
        return False

    category = FAMILY_CATEGORIES.get(family_name, "props")
    fields = dataclasses.fields(config_cls)

    params: List[Dict[str, Any]] = []
    default_values: Dict[str, Any] = {}

    for f in fields:
        p_def = infer_param_def(f)
        params.append(p_def)
        if f.default is not dataclasses.MISSING:
            default_values[f.name] = f.default

    manifest = {
        "$schema": SCHEMA_URL,
        "id": f"below_nominal.{category}.{family_name}",
        "version": "1.0.0",
        "name": family_name.replace("_", " ").title(),
        "description": f"Generador procedural paramétrico de {family_name.replace('_', ' ')} para Below Nominal.",
        "author": {
            "name": "Below Nominal Team",
            "github": "below-nominal",
            "url": "https://belownominal.com"
        },
        "license": "CC-BY-4.0",
        "category": category,
        "tags": [category, family_name, "psx", "low-poly", "retro-sci-fi"],
        "compatibility": {
            "engine_version": ">=1.5.0",
            "blender_version": ">=4.2"
        },
        "parameters": params,
        "presets": [
            {
                "id": "default",
                "name": "Estándar / Por Defecto",
                "description": "Configuración base del generador",
                "values": default_values
            }
        ],
        "export_capabilities": {
            "supports_collision": True,
            "default_collision_suffix": "-convcolonly",
            "supports_sockets": family_name in ("station_corridor", "station_room", "pipes")
        }
    }

    os.makedirs(family_dir, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"[CREATED] Manifest written for '{family_name}' at {manifest_path}")
    return True

def main():
    force = "--force" in sys.argv
    print(f"Bootstrapping manifests for {len(GENERATOR_REGISTRY)} registered families (force={force})...")
    created = 0
    skipped = 0
    for family_name, (cfg_cls, gen_cls) in sorted(GENERATOR_REGISTRY.items()):
        if bootstrap_family(family_name, cfg_cls, force=force):
            created += 1
        else:
            skipped += 1

    print(f"\nDone! Created: {created}, Skipped: {skipped}, Total: {len(GENERATOR_REGISTRY)}")

if __name__ == "__main__":
    main()
