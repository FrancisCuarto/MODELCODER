# Informe de Exportación a Godot 4 — station_corridor
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-16T19:48:19.297317Z` | **Generador:** `StationCorridorGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\station_corridor.glb`
- **Tamaño:** `104.17 KB` (106672 bytes)
- **Dimensiones:** `3.320m (W) × 4.000m (D) × 3.160m (H)`
- **Polígonos:** `192 tris` (Objetivo: `550`, Ratio: `0.35`)
- **Vértices:** `128 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.0, -0.0, 0.08]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `station_corridor` | `MESH` | 192 | 128 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `station_corridor` |
| `socket_light` | `EMPTY` | 0 | 0 | `station_corridor` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `station_corridor` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_fluorescent_lit_w50` | `PBR` | 0.18 | 0.00 | 3.0x |
| `mat_psx_industrial_hazard_rubber_tire_w50` | `PBR` | 0.90 | 0.00 | None |
| `mat_psx_industrial_hazard_floor_metal_w50` | `PBR` | 0.78 | 0.32 | None |
| `mat_psx_industrial_hazard_floor_hazard_w50` | `PBR` | 0.72 | 0.10 | None |
| `mat_psx_industrial_hazard_wall_bulkhead_w50` | `PBR` | 0.74 | 0.28 | None |
| `mat_psx_industrial_hazard_wall_support_beam_w50` | `PBR` | 0.52 | 0.75 | None |
| `mat_psx_industrial_hazard_ceiling_girder_w50` | `PBR` | 0.65 | 0.60 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -2.55, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 3.18]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 2.686]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** Sí
- **Resultado:** ✅ IMPORTACIÓN CORRECTA
- **Binario Utilizado:** `C:\Users\lopez\Downloads\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64_console.exe`
- **Mallas Reconocidas por Godot:** 1
- **Superficies Totales:** 7
- **StaticBody3D Generados:** 0
- **CollisionShape3D Generados:** 0
- **Materiales Mapeados:** 7
