# Informe de Exportación a Godot 4 — office_door
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T22:33:45.989819Z` | **Generador:** `ProceduralAssetGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\office_door.glb`
- **Tamaño:** `96.16 KB` (98464 bytes)
- **Dimensiones:** `1.200m (W) × 0.220m (D) × 2.400m (H)`
- **Polígonos:** `120 tris` (Objetivo: `420`, Ratio: `0.29`)
- **Vértices:** `80 verts` en `4` objeto(s)

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
| `office_door` | `MESH` | 120 | 80 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `office_door` |
| `socket_light` | `EMPTY` | 0 | 0 | `office_door` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `office_door` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_mounting_w50` | `PBR` | 0.42 | 0.88 | None |
| `mat_psx_industrial_hazard_glass_observation_w50` | `PBR` | 0.14 | 0.08 | None |
| `mat_psx_industrial_hazard_door_frame_heavy_w50` | `PBR` | 0.70 | 0.45 | None |
| `mat_psx_industrial_hazard_locker_gray_w50` | `PBR` | 0.68 | 0.25 | None |
| `mat_psx_industrial_hazard_wall_support_beam_w50` | `PBR` | 0.52 | 0.75 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -0.66, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 2.42]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 2.04]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** No
- **Resultado:** ❌ ERROR
