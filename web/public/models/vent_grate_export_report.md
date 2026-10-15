# Informe de Exportación a Godot 4 — vent_grate
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:46.657985Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\vent_grate.glb`
- **Tamaño:** `101.68 KB` (104120 bytes)
- **Dimensiones:** `0.600m (W) × 0.600m (D) × 0.312m (H)`
- **Polígonos:** `188 tris` (Objetivo: `280`, Ratio: `0.67`)
- **Vértices:** `124 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, -0.0, 0.25]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `vent_grate` | `MESH` | 184 | 124 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `vent_grate` |
| `socket_light` | `EMPTY` | 0 | 0 | `vent_grate` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `vent_grate` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w70` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_mounting_w70` | `PBR` | 0.42 | 0.88 | None |
| `mat_psx_industrial_hazard_switch_base_w70` | `PBR` | 0.82 | 0.00 | None |
| `mat_psx_industrial_hazard_screw_w70` | `PBR` | 0.35 | 0.88 | None |
| `mat_psx_industrial_hazard_vent_w70` | `PBR` | 0.68 | 0.35 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -0.85, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 0.332]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 0.265]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
