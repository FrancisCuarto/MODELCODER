# Informe de Exportación a Godot 4 — pipes
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:46.132076Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\pipes.glb`
- **Tamaño:** `101.07 KB` (103496 bytes)
- **Dimensiones:** `1.800m (W) × 0.483m (D) × 0.333m (H)`
- **Polígonos:** `184 tris` (Objetivo: `400`, Ratio: `0.46`)
- **Vértices:** `118 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, -0.1023, 0.1665]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `pipes` | `MESH` | 158 | 118 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `pipes` |
| `socket_light` | `EMPTY` | 0 | 0 | `pipes` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `pipes` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w50` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_casing_inner_w50` | `PBR` | 0.75 | 0.15 | None |
| `mat_psx_industrial_hazard_switch_metal_w50` | `PBR` | 0.30 | 0.92 | None |
| `mat_psx_industrial_hazard_screw_w50` | `PBR` | 0.35 | 0.88 | None |
| `mat_psx_industrial_hazard_pipe_industrial_w50` | `PBR` | 0.48 | 0.75 | None |
| `mat_psx_industrial_hazard_valve_red_w50` | `PBR` | 0.45 | 0.25 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -0.792, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 0.353]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 0.283]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
