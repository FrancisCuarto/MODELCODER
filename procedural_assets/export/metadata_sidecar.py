import json
import os
from datetime import datetime
from typing import Dict, Any
from ..core.base_generator import ValidationReport
from ..core.base_config import BaseAssetConfig

def save_metadata_sidecar(
    glb_filepath: str,
    config: BaseAssetConfig,
    report: ValidationReport,
    generator_name: str = "ProceduralAssetGenerator"
) -> str:
    """Save sidecar JSON file containing generation parameters and mesh telemetry."""
    base, _ = os.path.splitext(glb_filepath)
    json_path = f"{base}.json"

    metadata: Dict[str, Any] = {
        "generator": generator_name,
        "model_name": config.name,
        "seed": config.seed,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "mesh_metrics": {
            "triangle_count": report.triangle_count,
            "vertex_count": report.vertex_count,
            "target_tri_budget": report.target_tri_budget,
            "budget_compliance_ratio": round(report.triangle_count / max(1, report.target_tri_budget), 2),
            "dimensions_meters": {
                "width": round(report.dimensions[0], 4),
                "height": round(report.dimensions[1], 4),
                "depth": round(report.dimensions[2], 4)
            },
            "has_vertex_colors": report.has_vertex_colors,
            "materials_assigned": report.material_names
        },
        "config_parameters": config.to_dict(),
        "sockets": (config.extra_params.get("sockets") if getattr(config, "extra_params", None) else None) or [
            {
                "name": "socket_player_interact",
                "position": [0.0, -round(report.dimensions[1] * 0.5 + 0.55, 3), 0.0],
                "rotation_deg": [0.0, 0.0, 0.0],
                "description": "Standard player character interaction stand point"
            },
            {
                "name": "socket_item_spawn",
                "position": [0.0, 0.0, round(report.dimensions[2] + 0.02, 3)],
                "rotation_deg": [0.0, 0.0, 0.0],
                "description": "Prop or pickup spawn snap position (keycards, ammo, medical items)"
            },
            {
                "name": "socket_light",
                "position": [0.0, 0.0, round(report.dimensions[2] * 0.85, 3)],
                "rotation_deg": [0.0, 0.0, 0.0],
                "description": "OmniLight3D / SpotLight3D mount anchor point"
            }
        ],
        "godot_4_compatibility": {
            "format": "glTF 2.0 Binary (.glb)",
            "unit": "meters (1.0 Blender unit = 1.0 Godot unit)",
            "forward_axis": "-Z",
            "up_axis": "+Y",
            "collision_mesh_convention": "Child node with -col or -colonly creates Godot StaticBody3D collision shape",
            "vertex_colors": "Exported in COLOR_0 accessor (usable with StandardMaterial3D or PSX shader)",
            "pbr_materials": "Exported as glTF PBR metallic/roughness + emissive"
        }
    }

    os.makedirs(os.path.dirname(os.path.abspath(json_path)), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return json_path
