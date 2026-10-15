# Informe de Exportación a Godot 4 — crate
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:45.426159Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\crate.glb`
- **Tamaño:** `99.21 KB` (101588 bytes)
- **Dimensiones:** `0.880m (W) × 0.654m (D) × 0.639m (H)`
- **Polígonos:** `168 tris` (Objetivo: `340`, Ratio: `0.49`)
- **Vértices:** `112 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, -0.325, 0.312]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `crate` | `MESH` | 168 | 112 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `crate` |
| `socket_light` | `EMPTY` | 0 | 0 | `crate` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `crate` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w50` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_casing_inner_w50` | `PBR` | 0.75 | 0.15 | None |
| `mat_psx_industrial_hazard_mounting_w50` | `PBR` | 0.42 | 0.88 | None |
| `mat_psx_industrial_hazard_switch_metal_w50` | `PBR` | 0.30 | 0.92 | None |
| `mat_psx_industrial_hazard_screw_w50` | `PBR` | 0.35 | 0.88 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -0.877, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 0.66]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 0.544]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
