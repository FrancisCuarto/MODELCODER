import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

def generate_export_report(
    glb_filepath: str,
    config_dict: Dict[str, Any],
    validation_dict: Dict[str, Any],
    hierarchy_nodes: List[Dict[str, Any]],
    materials_list: List[Dict[str, Any]],
    collision_info: Optional[Dict[str, Any]] = None,
    sockets_list: Optional[List[Dict[str, Any]]] = None,
    godot_validation: Optional[Dict[str, Any]] = None,
    generator_name: str = "ProceduralAssetGenerator",
    pivot_info: Optional[Dict[str, Any]] = None,
    warnings: Optional[List[str]] = None
) -> Tuple[str, str]:
    """
    Generate both JSON and Markdown export reports for the produced asset.
    Returns: (json_report_path, markdown_report_path)
    """
    base, _ = os.path.splitext(glb_filepath)
    json_path = f"{base}_export_report.json"
    md_path = f"{base}_export_report.md"

    filesize = os.path.getsize(glb_filepath) if os.path.exists(glb_filepath) else 0
    all_warnings = list(warnings or [])
    if validation_dict.get("warnings"):
        all_warnings.extend(validation_dict["warnings"])

    report_data: Dict[str, Any] = {
        "export_metadata": {
            "generator": generator_name,
            "asset_name": config_dict.get("name", "asset"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "format": "glTF 2.0 Binary (.glb)",
            "output_file": os.path.abspath(glb_filepath),
            "file_size_bytes": filesize,
            "file_size_kb": round(filesize / 1024.0, 2),
        },
        "normalization": {
            "units": "Meters (1 Blender unit = 1.0 Godot unit)",
            "scale_applied": True,
            "rotation_applied": True,
            "location_applied": True,
            "pivot_rule": pivot_info.get("rule", "floor_center") if pivot_info else "floor_center",
            "pivot_offset_applied": pivot_info.get("offset", [0.0, 0.0, 0.0]) if pivot_info else [0.0, 0.0, 0.0],
            "normals_shading": "Flat (poly.use_smooth = False, PS1 low-poly crisp)",
            "normals_recalculated": True,
            "uv_mapping": "TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)",
            "vertex_colors": "COLOR_0 (Col / PS1 Gouraud tinting and wear)",
        },
        "dimensions_meters": validation_dict.get("dimensions", {"x": 0, "y": 0, "z": 0}),
        "geometry_metrics": {
            "total_triangles": validation_dict.get("triangle_count", 0),
            "total_vertices": validation_dict.get("vertex_count", 0),
            "target_tri_budget": validation_dict.get("target_tri_budget", 450),
            "budget_compliance_ratio": validation_dict.get("budget_compliance_ratio", 1.0),
            "object_count": len(hierarchy_nodes),
            "hierarchy": hierarchy_nodes
        },
        "materials": {
            "count": len(materials_list),
            "compacted": True,
            "list": materials_list
        },
        "collision": collision_info or {
            "enabled": False,
            "message": "No collision mesh requested"
        },
        "sockets": sockets_list or [],
        "godot_4_validation": godot_validation or {
            "tested_in_godot": False,
            "message": "Live Godot test not executed"
        },
        "warnings": all_warnings
    }

    # Write JSON report
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    # Write Markdown summary report
    md_content = _build_markdown_report(report_data)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return json_path, md_path

def _build_markdown_report(data: Dict[str, Any]) -> str:
    meta = data["export_metadata"]
    norm = data["normalization"]
    dims = data["dimensions_meters"]
    geo = data["geometry_metrics"]
    mats = data["materials"]
    col = data["collision"]
    godot = data["godot_4_validation"]
    warns = data["warnings"]

    dims_str = f"{dims.get('x', 0):.3f}m (W) × {dims.get('y', 0):.3f}m (D) × {dims.get('z', 0):.3f}m (H)" if isinstance(dims, dict) else str(dims)

    status_badge = "✅ EXITOSA" if (not warns and godot.get("success", True)) else "⚠️ REVISAR ADVERTENCIAS"

    lines = [
        f"# Informe de Exportación a Godot 4 — {meta['asset_name']}",
        f"**Estado:** {status_badge} | **Fecha:** `{meta['timestamp']}` | **Generador:** `{meta['generator']}`",
        "",
        "## 1. Archivo y Dimensiones",
        f"- **Archivo GLB:** `{meta['output_file']}`",
        f"- **Tamaño:** `{meta['file_size_kb']} KB` ({meta['file_size_bytes']} bytes)",
        f"- **Dimensiones:** `{dims_str}`",
        f"- **Polígonos:** `{geo['total_triangles']} tris` (Objetivo: `{geo['target_tri_budget']}`, Ratio: `{geo['budget_compliance_ratio']}`)",
        f"- **Vértices:** `{geo['total_vertices']} verts` en `{geo['object_count']}` objeto(s)",
        "",
        "## 2. Normalización de Pipeline",
        f"- **Unidades:** {norm['units']}",
        f"- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.",
        f"- **Pivote / Origen:** Regla `{norm['pivot_rule']}` aplicada con desplazamiento `{norm['pivot_offset_applied']}`.",
        f"- **Normales y Sombreado:** {norm['normals_shading']} con recálculo hacia afuera.",
        f"- **Mapeado UV / Texturas:** {norm.get('uv_mapping', 'TEXCOORD_0 (Atlas PS1)')}",
        f"- **Colores por Vértice:** {norm.get('vertex_colors', 'COLOR_0 (Col)')}",
        "",
        "## 3. Jerarquía de Objetos",
        "| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for node in geo["hierarchy"]:
        p_name = node.get("parent") or "None (Root)"
        lines.append(f"| `{node['name']}` | `{node['type']}` | {node.get('triangles', 0)} | {node.get('vertices', 0)} | `{p_name}` |")

    lines.extend([
        "",
        "## 4. Materiales Compactados (glTF PBR)",
        "| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for m in mats["list"]:
        em = m.get("emission", "None")
        lines.append(f"| `{m['name']}` | `{m.get('category', 'PBR')}` | {m.get('roughness', 0.5):.2f} | {m.get('metallic', 0.0):.2f} | {em} |")

    lines.extend([
        "",
        "## 5. Colisión para Godot 4",
        f"- **Habilitada:** {'Sí' if col.get('enabled') else 'No'}",
        f"- **Nodo de Colisión:** `{col.get('node_name', 'N/A')}`",
        f"- **Tipo de Forma:** `{col.get('shape_type', 'N/A')}`",
        f"- **Sufijo Godot:** `{col.get('godot_suffix', 'N/A')}` (Crea StaticBody3D automáticamente)",
        "",
        "## 6. Sockets / Puntos de Anclaje",
    ])

    sockets = data.get("sockets", [])
    if sockets:
        lines.append("| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |")
        lines.append("| :--- | :--- | :--- |")
        for s in sockets:
            pos = [round(p, 3) for p in s.get("position", [0, 0, 0])]
            lines.append(f"| `{s['name']}` | `{pos}` | {s.get('description', '')} |")
    else:
        lines.append("*No se definieron sockets específicos.*")

    lines.extend([
        "",
        "## 7. Validación Real en Motor Godot 4",
        f"- **Ejecutado en Godot:** {'Sí' if godot.get('tested_in_godot') else 'No'}",
        f"- **Resultado:** {'✅ IMPORTACIÓN CORRECTA' if godot.get('success') else '❌ ERROR'}",
    ])

    if godot.get("tested_in_godot"):
        lines.extend([
            f"- **Binario Utilizado:** `{godot.get('godot_binary', 'Godot 4')}`",
            f"- **Mallas Reconocidas por Godot:** {godot.get('mesh_count', 0)}",
            f"- **Superficies Totales:** {godot.get('total_surfaces', 0)}",
            f"- **StaticBody3D Generados:** {godot.get('static_body_count', 0)}",
            f"- **CollisionShape3D Generados:** {godot.get('collision_shape_count', 0)}",
            f"- **Materiales Mapeados:** {len(godot.get('materials', []))}",
        ])
        if godot.get("errors"):
            lines.append(f"- **Errores de Godot:** `{godot['errors']}`")

    if warns:
        lines.extend([
            "",
            "## ⚠️ Advertencias Detectadas",
        ])
        for w in warns:
            lines.append(f"- {w}")

    return "\n".join(lines) + "\n"
