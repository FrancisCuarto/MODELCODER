# Informe de Exportación a Godot 4 — fire_extinguisher
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-15T19:13:34.723535Z` | **Generador:** `FireExtinguisherGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `d:\MODELCODER\web\public\models\fire_extinguisher.glb`
- **Tamaño:** `105.69 KB` (108228 bytes)
- **Dimensiones:** `0.206m (W) × 0.700m (D) × 0.238m (H)`
- **Polígonos:** `196 tris` (Objetivo: `340`, Ratio: `0.58`)
- **Vértices:** `120 verts` en `5` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[0.0128, -0.125, -0.0]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `fire_extinguisher` | `MESH` | 172 | 120 | `None (Root)` |
| `fire_extinguisher-convcolonly` | `MESH` | 12 | 8 | `fire_extinguisher` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `fire_extinguisher` |
| `socket_light` | `EMPTY` | 0 | 0 | `fire_extinguisher` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `fire_extinguisher` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_industrial_hazard_casing_w65` | `PBR` | 0.68 | 0.18 | None |
| `mat_psx_industrial_hazard_casing_red_w65` | `PBR` | 0.65 | 0.12 | None |
| `mat_psx_industrial_hazard_mounting_w65` | `PBR` | 0.42 | 0.88 | None |
| `mat_psx_industrial_hazard_switch_metal_w65` | `PBR` | 0.30 | 0.92 | None |
| `mat_psx_industrial_hazard_switch_base_w65` | `PBR` | 0.82 | 0.00 | None |
| `mat_psx_industrial_hazard_cable_black_w65` | `PBR` | 0.88 | 0.00 | None |
| `mat_psx_industrial_hazard_door_emergency_red_w65` | `PBR` | 0.55 | 0.15 | None |
| `mat_psx_industrial_hazard_gauge_w65` | `PBR` | 0.40 | 0.15 | None |

## 5. Colisión para Godot 4
- **Habilitada:** Sí
- **Nodo de Colisión:** `fire_extinguisher-convcolonly`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -0.9, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 0.258]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 0.202]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** Sí
- **Resultado:** ✅ IMPORTACIÓN CORRECTA
- **Binario Utilizado:** `C:\Users\lopez\Downloads\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64_console.exe`
- **Mallas Reconocidas por Godot:** 2
- **Superficies Totales:** 9
- **StaticBody3D Generados:** 1
- **CollisionShape3D Generados:** 1
- **Materiales Mapeados:** 9
