# Informe de Exportación a Godot 4 — bunk_bed
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:45.180135Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\bunk_bed.glb`
- **Tamaño:** `126.66 KB` (129700 bytes)
- **Dimensiones:** `1.087m (W) × 2.050m (D) × 2.050m (H)`
- **Polígonos:** `444 tris` (Objetivo: `480`, Ratio: `0.93`)
- **Vértices:** `296 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[0.0188, -0.0, -0.0]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `bunk_bed` | `MESH` | 444 | 296 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `bunk_bed` |
| `socket_light` | `EMPTY` | 0 | 0 | `bunk_bed` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `bunk_bed` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w50` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_btn_gray_w50` | `PBR` | 0.50 | 0.15 | None |
| `mat_psx_industrial_hazard_fluorescent_lit_w50` | `PBR` | 0.18 | 0.00 | 3.0x |
| `mat_psx_industrial_hazard_locker_gray_w50` | `PBR` | 0.68 | 0.25 | None |
| `mat_psx_industrial_hazard_wall_bulkhead_w50` | `PBR` | 0.74 | 0.28 | None |
| `mat_psx_industrial_hazard_wall_support_beam_w50` | `PBR` | 0.52 | 0.75 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -1.575, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 2.07]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 1.743]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
