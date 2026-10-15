"""
Sync utility for ModelCoder Community Platform.
Extracts manifests, metadata, source code, and pre-rendered GLB assets from the engine
and packages them into web/src/data/catalog.json and web/public/models/ for Astro SSG.
"""

import os
import sys
import json
import shutil
import glob
from typing import Dict, Any, List, Optional

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.core import discover_all_manifests, GeneratorManifest
from procedural_assets.export.destination import FAMILY_CATEGORIES

WEB_DIR = os.path.join(current_dir, "web")
PUBLIC_MODELS_DIR = os.path.join(WEB_DIR, "public", "models")
DATA_DIR = os.path.join(WEB_DIR, "src", "data")
OUTPUT_DIR = os.path.join(current_dir, "output")
EXPORTS_DIR = os.path.join(current_dir, "exports")

def find_glb_for_family(family_name: str) -> Optional[str]:
    """Search output/, exports/, and web/public/models/ for pre-rendered GLB files matching family."""
    search_dirs = [PUBLIC_MODELS_DIR, OUTPUT_DIR, EXPORTS_DIR]
    patterns = [
        f"below_nominal_{family_name}.glb",
        f"bn_{family_name}_*.glb",
        f"bn_{family_name}.glb",
        f"test_{family_name}.glb",
        f"*{family_name}*.glb"
    ]
    
    for sdir in search_dirs:
        if not os.path.isdir(sdir):
            continue
        for pat in patterns:
            matches = glob.glob(os.path.join(sdir, pat))
            if matches:
                # Return the largest valid file or first match
                return matches[0]
    return None

def sync_catalog():
    print("=== ModelCoder Catalog Synchronization ===")
    os.makedirs(PUBLIC_MODELS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    manifests = discover_all_manifests()
    print(f"Found {len(manifests)} generator manifests.")

    catalog_entries: List[Dict[str, Any]] = []
    models_copied = 0

    generators_dir = os.path.join(current_dir, "procedural_assets", "generators")

    for family_name, manifest in sorted(manifests.items()):
        family_dir = os.path.join(generators_dir, family_name)
        
        # Read source code
        gen_py_path = os.path.join(family_dir, "generator.py")
        cfg_py_path = os.path.join(family_dir, "config.py")
        
        source_code = ""
        if os.path.isfile(gen_py_path):
            with open(gen_py_path, "r", encoding="utf-8") as f:
                source_code = f.read()

        config_code = ""
        if os.path.isfile(cfg_py_path):
            with open(cfg_py_path, "r", encoding="utf-8") as f:
                config_code = f.read()

        # Find GLB
        glb_src = find_glb_for_family(family_name)
        has_model = False
        model_url = None
        file_size_bytes = 0

        if glb_src and os.path.isfile(glb_src):
            dest_glb = os.path.join(PUBLIC_MODELS_DIR, f"{family_name}.glb")
            if os.path.abspath(glb_src) != os.path.abspath(dest_glb):
                shutil.copy2(glb_src, dest_glb)
            has_model = True
            model_url = f"/models/{family_name}.glb"
            file_size_bytes = os.path.getsize(dest_glb)
            models_copied += 1

        category = manifest.category or FAMILY_CATEGORIES.get(family_name, "props")

        entry = {
            "id": manifest.id,
            "family": family_name,
            "name": manifest.name,
            "version": manifest.version,
            "description": manifest.description,
            "category": category,
            "tags": manifest.tags,
            "author": manifest.author.to_dict() if manifest.author else {"name": "Community"},
            "license": manifest.license,
            "compatibility": manifest.compatibility,
            "parameters": [p.to_dict() for p in manifest.parameters],
            "presets": [pr.to_dict() for pr in manifest.presets],
            "export_capabilities": manifest.export_capabilities,
            "has_model": has_model,
            "model_url": model_url,
            "file_size_bytes": file_size_bytes,
            "source_code": source_code,
            "config_code": config_code
        }
        catalog_entries.append(entry)

    catalog_path = os.path.join(DATA_DIR, "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_entries, f, indent=2, ensure_ascii=False)

    print(f"Catalog saved to {catalog_path} with {len(catalog_entries)} generators.")
    print(f"3D Models copied to {PUBLIC_MODELS_DIR}: {models_copied}/{len(catalog_entries)}")

    # Category summary
    categories: Dict[str, int] = {}
    for e in catalog_entries:
        cat = e["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\nGenerators by category:")
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count}")

if __name__ == "__main__":
    sync_catalog()
