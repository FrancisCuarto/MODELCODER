# Informe de Exportación a Godot 4 — trash_bin
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:46.517791Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\trash_bin.glb`
- **Tamaño:** `94.15 KB` (96408 bytes)
- **Dimensiones:** `0.424m (W) × 0.936m (D) × 0.470m (H)`
- **Polígonos:** `120 tris` (Objetivo: `320`, Ratio: `0.38`)
- **Vértices:** `72 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, -0.468, 0.21]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `trash_bin` | `MESH` | 96 | 72 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `trash_bin` |
| `socket_light` | `EMPTY` | 0 | 0 | `trash_bin` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `trash_bin` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w70` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_casing_inner_w70` | `PBR` | 0.75 | 0.15 | None |
| `mat_psx_industrial_hazard_mounting_w70` | `PBR` | 0.42 | 0.88 | None |
| `mat_psx_industrial_hazard_switch_base_w70` | `PBR` | 0.82 | 0.00 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -1.018, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 0.49]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 0.399]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
