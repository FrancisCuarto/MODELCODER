# Informe de Exportación a Godot 4 — electrical_panel
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:45.598555Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\electrical_panel.glb`
- **Tamaño:** `136.71 KB` (139988 bytes)
- **Dimensiones:** `0.716m (W) × 1.351m (D) × 0.274m (H)`
- **Polígonos:** `490 tris` (Objetivo: `450`, Ratio: `1.09`)
- **Vértices:** `322 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, 0.1855, 0.0097]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `electrical_panel` | `MESH` | 482 | 322 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `electrical_panel` |
| `socket_light` | `EMPTY` | 0 | 0 | `electrical_panel` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `electrical_panel` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w50` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_casing_inner_w50` | `PBR` | 0.75 | 0.15 | None |
| `mat_psx_industrial_hazard_mounting_w50` | `PBR` | 0.42 | 0.88 | None |
| `mat_psx_industrial_hazard_crt_frame_w50` | `PBR` | 0.52 | 0.02 | None |
| `mat_psx_industrial_hazard_crt_screen_w50` | `PBR` | 0.22 | 0.00 | 2.2x |
| `mat_psx_industrial_hazard_btn_yellow_w50` | `PBR` | 0.45 | 0.05 | None |
| `mat_psx_industrial_hazard_btn_blue_w50` | `PBR` | 0.45 | 0.05 | None |
| `mat_psx_industrial_hazard_switch_metal_w50` | `PBR` | 0.30 | 0.92 | None |
| `mat_psx_industrial_hazard_switch_base_w50` | `PBR` | 0.82 | 0.00 | None |
| `mat_psx_industrial_hazard_screw_w50` | `PBR` | 0.35 | 0.88 | None |
| `mat_psx_industrial_hazard_led_green_w50` | `PBR` | 0.20 | 0.00 | 2.8x |
| `mat_psx_industrial_hazard_led_red_w50` | `PBR` | 0.20 | 0.00 | 2.8x |
| `mat_psx_industrial_hazard_cable_black_w50` | `PBR` | 0.88 | 0.00 | None |
| `mat_psx_industrial_hazard_cable_hazard_w50` | `PBR` | 0.85 | 0.00 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -1.225, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 0.294]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 0.233]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
