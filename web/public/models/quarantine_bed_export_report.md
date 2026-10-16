# Informe de Exportación a Godot 4 — quarantine_bed
**Estado:** ✅ EXITOSA | **Fecha:** `2026-10-16T04:59:12.580315Z` | **Generador:** `QuarantineBedGenerator`

## 1. Archivo y Dimensiones
- **Archivo GLB:** `D:\MODELCODER\web\public\models\quarantine_bed.glb`
- **Tamaño:** `125.6 KB` (128612 bytes)
- **Dimensiones:** `1.120m (W) × 2.127m (D) × 1.819m (H)`
- **Polígonos:** `500 tris` (Objetivo: `750`, Ratio: `0.67`)
- **Vértices:** `328 verts` en `4` objeto(s)

## 2. Normalización de Pipeline
- **Unidades:** Meters (1 Blender unit = 1.0 Godot unit)
- **Transformaciones Congeladas:** Escala (1,1,1), Rotación (0,0,0), Traslación (0,0,0) aplicadas.
- **Pivote / Origen:** Regla `floor_center` aplicada con desplazamiento `[-0.025, -0.0112, -0.008]`.
- **Normales y Sombreado:** Flat (poly.use_smooth = False, PS1 low-poly crisp) con recálculo hacia afuera.
- **Mapeado UV / Texturas:** TEXCOORD_0 (Component-mapped to PS1 Weathered Texture Atlas)
- **Colores por Vértice:** COLOR_0 (Col / PS1 Gouraud tinting and wear)

## 3. Jerarquía de Objetos
| Nombre de Nodo | Tipo | Triángulos | Vértices | Padre |
| :--- | :--- | :--- | :--- | :--- |
| `quarantine_bed` | `MESH` | 484 | 328 | `None (Root)` |
| `socket_item_spawn` | `EMPTY` | 0 | 0 | `quarantine_bed` |
| `socket_light` | `EMPTY` | 0 | 0 | `quarantine_bed` |
| `socket_player_interact` | `EMPTY` | 0 | 0 | `quarantine_bed` |

## 4. Materiales Compactados (glTF PBR)
| Slot / Nombre | Categoría | Rugosidad | Metálico | Emisión |
| :--- | :--- | :--- | :--- | :--- |
| `mat_psx_medbay_clean_casing_w35` | `PBR` | 0.55 | 0.05 | None |

## 5. Colisión para Godot 4
- **Habilitada:** No
- **Nodo de Colisión:** `None`
- **Tipo de Forma:** `box`
- **Sufijo Godot:** `-convcolonly` (Crea StaticBody3D automáticamente)

## 6. Sockets / Puntos de Anclaje
| Nombre del Socket | Posición Local [X, Y, Z] | Propósito |
| :--- | :--- | :--- |
| `socket_player_interact` | `[0.0, -1.614, 0.0]` | Standard player character interaction stand point |
| `socket_item_spawn` | `[0.0, 0.0, 1.839]` | Prop or pickup spawn snap position (keycards, ammo, medical items) |
| `socket_light` | `[0.0, 0.0, 1.547]` | OmniLight3D / SpotLight3D mount anchor point |

## 7. Validación Real en Motor Godot 4
- **Ejecutado en Godot:** Sí
- **Resultado:** ✅ IMPORTACIÓN CORRECTA
- **Binario Utilizado:** `C:\Users\lopez\Downloads\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64_console.exe`
- **Mallas Reconocidas por Godot:** 1
- **Superficies Totales:** 1
- **StaticBody3D Generados:** 0
- **CollisionShape3D Generados:** 0
- **Materiales Mapeados:** 1
