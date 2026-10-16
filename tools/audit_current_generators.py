import os
import sys
import json

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.core.manifest import discover_all_manifests

manifests = discover_all_manifests()
print(f"Total discovered manifests: {len(manifests)}")

audit_data = []

for family, m in sorted(manifests.items()):
    entry = {
        "family": family,
        "id": m.id,
        "name": m.name,
        "category": m.category,
        "param_count": len(m.parameters),
        "param_keys": [p.key for p in m.parameters],
        "preset_count": len(m.presets),
        "preset_ids": [p.id for p in m.presets],
        "supports_collision": m.export_capabilities.get("supports_collision", False),
        "collision_suffix": m.export_capabilities.get("default_collision_suffix", ""),
        "supports_sockets": m.export_capabilities.get("supports_sockets", False),
    }
    audit_data.append(entry)

out_path = os.path.join(current_dir, "docs", "audit_raw.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2, ensure_ascii=False)

print(f"Wrote audit data to {out_path}")
