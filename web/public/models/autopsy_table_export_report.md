# Informe de Exportación a Godot 4 — autopsy_table
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:45.055409Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\autopsy_table.glb`
- **Tamaño:** `123.05 KB` (126008 bytes)
- **Dimensiones:** `0.900m (W) × 2.100m (D) × 1.719m (H)`
- **Polígonos:** `444 tris` (Objetivo: `420`, Ratio: `1.06`)
- **Vértices:** `272 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, -0.0, -0.0]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `autopsy_table` | `MESH` | 372 | 272 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `autopsy_table` |
| `socket_light` | `EMPTY` | 0 | 0 | `autopsy_table` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `autopsy_table` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w50` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_steel_brushed_w50` | `PBR` | 0.38 | 0.92 | None |
| `mat_psx_industrial_hazard_cable_black_w50` | `PBR` | 0.88 | 0.00 | None |
| `mat_psx_industrial_hazard_cable_hazard_w50` | `PBR` | 0.85 | 0.00 | None |
| `mat_psx_industrial_hazard_gauge_w50` | `PBR` | 0.40 | 0.15 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -1.6, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 1.739]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 1.461]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
