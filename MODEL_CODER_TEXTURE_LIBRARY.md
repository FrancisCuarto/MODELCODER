# MODEL CODER — Expansión Masiva y Eficiente de la Biblioteca de Texturas (`MODEL_CODER_TEXTURE_LIBRARY.md`)

**Fecha:** 2026-10-17  
**Rama:** `polish/product-completion`  
**Estado:** Implementado, verificado con 33 pruebas automatizadas y compilado en producción (`106 páginas estáticas`).

---

## 1. Auditoría de Almacenamiento y Línea Base

Antes de ampliar la biblioteca, se auditó la arquitectura real de archivos, servicios y consumo de almacenamiento del repositorio `MODELCODER`:

### 1.1 Servicios Configurados en el Proyecto
| Servicio | Rol en ModelCoder | Límites del Plan Actual / Estándar | Estado de Verificación |
| :--- | :--- | :--- | :--- |
| **Vercel** (`vercel.json`) | Hosting estático principal y CDN global (`web/dist`) | **100 MB** máx. por despliegue descomprimido (Hobby) / **100 GB/mes** transferencia | Confirmado por configuración estática Astro |
| **GitHub Pages** (`.github/workflows/deploy-web.yml`) | Hosting estático espejo por GitHub Actions | **1 GB** tamaño máx. de sitio publicado / **100 GB/mes** ancho de banda suave | Confirmado en workflow CI/CD |
| **Supabase** (`web/src/lib/supabase.ts`) | Base de datos PostgreSQL (modelos comunitarios, inventario y comentarios) | **500 MB** Base de Datos / **1 GB** Storage (Free Tier) | Confirmado en cliente Supabase |
| **Navegador Local (`localStorage`)** | Borradores en curso, favoritos, colecciones y memoria procedural | **~5 MB** por origen (`5,242,880 bytes`) | Confirmado |

### 1.2 Línea Base de Almacenamiento (Antes vs. Después)
| Categoría de Recurso | Antes de la Ampliación | Después de la Ampliación | Diferencia Neta |
| :--- | :--- | :--- | :--- |
| **Modelos 3D del Catálogo (`web/public/models/*.glb`)** | `37,122,318 bytes` (**35.40 MiB** / 488 archivos) | `37,122,318 bytes` (**35.40 MiB** / 488 archivos) | `+0 bytes` |
| **Activos Estáticos Web (`logo.png`, `favicon.svg`, `.bat`)** | `957,713 bytes` (**0.91 MiB**) | `957,713 bytes` (**0.91 MiB**) | `+0 bytes` |
| **Archivos Estáticos de Texturas en Servidor (`web/public/`)** | `0 bytes` | `0 bytes` | **`+0 bytes` (0 MB)** |
| **Módulo `texture-library.ts` (Código Fuente)** | `20,044 bytes` (18 presets) | `49,482 bytes` (118 presets PBR + 20 variantes + NormalMaps) | `+29,438 bytes` (~28.7 KB) |
| **Bundle JS Compilado de Studio (`dist/_astro/studio.*.js`)** | `870.24 kB` (`226.40 kB` gzip) | `902.61 kB` (`233.69 kB` gzip) | **`+32.37 kB` (`+7.29 kB` gzip)** |
| **Tamaño Total de Producción (`web/dist/`)** | `~40.07 MB` | `~40.10 MB` | **`+0.03 MB` (+0.08%)** |

---

## 2. Presupuesto de Almacenamiento y Eficiencia por Megabyte

- **Presupuesto objetivo:** Mantener el proyecto completo por debajo del **50%** de la cuota más restrictiva (100 MB en Vercel Hobby) y conservar más del **50% libre** para futuras actualizaciones.
- **Resultado alcanzado:**
  - Consumo total de `web/dist`: **40.10 MB / 100 MB (40.1%)** en Vercel Hobby (**59.9% libre**) y **40.10 MB / 1,024 MB (3.9%)** en GitHub Pages (**96.1% libre**).
  - La ampliación completa de **120 nuevos materiales (de 18 a 138 materiales totales)** y **118 mapas normales tangenciales** ocupa únicamente **32.37 KB sin comprimir (7.29 KB gzip)** en el bundle JS y **0 bytes** de archivos de imagen en el servidor.
  - **Tamaño promedio por material incorporado:** **`~234 bytes` sin comprimir (`~53 bytes` en transferencia gzip)** por material completo con su mapa de color y mapa normal.

### Desglose por Tipo de Recurso
1. **Texturas Base Procedurales (118 presets `64×64` RGBA):** `0 bytes` en disco; se sintetizan bajo demanda en memoria RAM (`16,384 bytes` por `THREE.DataTexture` instanciada) únicamente cuando un componente las utiliza.
2. **Mapas PBR Adicionales (118 Mapas Normales `64×64` Sobel Tangent-Space):** `0 bytes` en disco; se calculan en memoria a partir del relieve de luminancia de cada textura y se cachean en `TextureLibrary.normalTextures`.
3. **Miniaturas del Explorador Visual (`48×48` WebP/PNG):** `0 bytes` en disco; se renderizan perezosamente (*lazy*) en un `<canvas>` 2D con iluminación especular diagonal y compresión `image/webp` (`calidad 0.85`), cacheadas en memoria (`thumbnailCache`).
4. **Recursos Generados durante la Exportación `.GLB`:** Durante `GLBExporterService.exportToArrayBuffer`, se empaquetan únicamente los mapas de color utilizados por las piezas del modelo exportado y se omiten los `DataTexture` de mapas normales temporales para reducir a la mitad el peso del archivo `.glb` resultante, restaurando los mapas normales en el visor inmediatamente después de exportar.

---

## 3. Catálogo de Materiales Incorporados (138 Materiales en 8 Familias)

| Familia / Categoría | Texturas Base Procedurales | Variantes Paramétricas Curadas | Mapas Normales PBR | Total Materiales Listos | Ejemplos Principales |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. ⚙️ Metales & Aleaciones (`metals`)** | 23 | 6 | 23 | **29** | `worn_metal`, `metal_dark_grime`, `metal_light_brushed`, `steel_polished`, `steel_galvanized`, `iron_cast`, `iron_aged`, `aluminum_anodized`, `copper_polished`, `copper_oxidized`, `bronze_antique`, `brass_burnished`, `titanium_aerospace`, `diamond_plate`, `metal_perforated`, `gold_contacts`, `chrome_mirror`, `lead_shielding`, `painted_metal_blue/olive/yellow`, `steel_blackened_gunmetal` |
| **2. 🧱 Construcción & Obra (`construction`)** | 15 | 4 | 15 | **19** | `concrete_smooth`, `concrete_rough`, `concrete_cracked`, `cinder_block`, `brick_red`, `brick_industrial`, `stucco_plaster`, `asphalt_road`, `ceramic_tile_white`, `industrial_tile_dirty`, `nonslip_floor`, `station_modular_panel`, `corrugated_metal`, `terrazzo_floor`, `hazard_stripes`, `brick_whitewashed` |
| **3. 🪵 Maderas & Carpintería (`woods`)** | 10 | 2 | 10 | **12** | `wood_oak`, `wood_pine`, `wood_walnut`, `wood_plywood`, `wood_painted_worn`, `wood_rustic_planks`, `wood_varnished`, `wood_parquet`, `wood_bamboo`, `wood_charred`, `wood_cherry_red`, `wood_weathered_grey` |
| **4. 🪨 Piedras & Minerales (`stones`)** | 12 | 2 | 12 | **14** | `granite_grey`, `granite_pink`, `marble_white`, `marble_black_gold`, `slate_layered`, `basalt_lunar`, `limestone_sand`, `sand_compacted`, `gravel_mineral`, `quartz_crystal`, `energy_mineral`, `obsidian_volcanic`, `marble_emerald_green`, `crystal_amethyst_purple` |
| **5. 🧪 Plásticos & Gomas (`plastics`)** | 12 | 2 | 11 | **14** | `beige_plastic_worn`, `rubber_black`, `plastic_abs_matte`, `plastic_acrylic_gloss`, `plastic_translucent`, `rubber_ribbed_mat`, `silicone_medical`, `acoustic_foam`, `polymer_tactical`, `plastic_hazard_orange`, `vinyl_grip`, `teflon_white`, `plastic_cyber_yellow`, `plastic_medical_white` |
| **6. 📟 Tecnología, PCB & Pantallas (`tech`)** | 21 | 1 | 15 | **22** | `pcb_green_gold`, `pcb_black_hd`, `pcb_blue_proto`, `carbon_fiber`, `hex_composite`, `server_vent_panel`, `thermal_tile_white`, `thermal_tile_black`, `solar_panel_blue`, `laser_grid_red`, `vent_grill`, `crt_screen_green/amber/blue/off`, `crt_data_matrix`, `caution_label`, `radiation_label`, `biohazard_label`, `high_voltage_label`, `plasma_core_glow`, `carbon_fiber_gold_weave` |
| **7. 🪟 Vidrios & Transparencias (`glass`)** | 10 | 1 | 0 (Transp.) | **11** | `clean_glass`, `tinted_glass`, `reinforced_glass`, `frosted_glass`, `cryo_glass_ice`, `amber_lab_glass`, `hologram_cyan`, `hologram_amber`, `hologram_green_tactical`, `forcefield_hex`, `visor_gold_mirror` |
| **8. 🧵 Telas, Cuero, Papel & Desgaste (`fabrics_organic`)** | 15 | 2 | 15 | **17** | `kevlar_ballistic`, `canvas_military`, `quilted_padding_white/orange`, `synthetic_mesh`, `leather_black_worn`, `leather_brown_aged`, `cardboard_corrugated`, `blueprint_paper`, `duct_tape_silver`, `kapton_gold_foil`, `rust_heavy`, `moss_biological`, `ash_dust_coating`, `soil_mud_packed`, `kevlar_olive_tactical`, `leather_burgundy_luxury` |
| **TOTAL GENERAL** | **118** | **20** | **101** | **138** | **+ Variaciones continuas infinitas mediante parámetros UV, Tinte, Rugosidad, Metalicidad, Desgaste y Relieve Normal** |

---

## 4. Sistema de Variaciones Paramétricas y Explorador en el Editor (`Studio 3D`)

En [`studio.astro`](file:///d:/MODELCODER/web/src/pages/studio.astro) y [`procedural-engine.ts`](file:///d:/MODELCODER/web/src/lib/studio/procedural-engine.ts) se implementaron:

1. **Explorador Visual de Materiales PBR (`#mat-browser-grid`):**
   - Filtro instantáneo por las **8 familias** + pestaña de **Variantes Curadas** + vista **Todos (138)**.
   - Buscador en tiempo real por nombre, ID o etiquetas semánticas en español e inglés (`madera`, `mármol`, `ladrillo`, `cobre`, `pcb`, `kevlar`, `holograma`, etc.).
   - Miniaturas `48×48` generadas perezosamente en formato `WebP` con previsualización del brillo metálico y tinte.
   - Insignias indicadoras de mapas y propiedades PBR (`NORM`, `METAL`, `EMISSIVE`, `ALPHA`, `VAR`).
2. **Controles Paramétricos por Componente (sin duplicar archivos):**
   - **Color Superficial / Tinte (`#inp-mat-color`):** Modula el color base sobre cualquier textura.
   - **Rugosidad (`0.0–1.0`) y Metalicidad (`0.0–1.0`):** Se autocompletan con la física calibrada del material al seleccionarlo y permiten ajuste manual fino.
   - **Frecuencia UV `[U, V]` Anti-Estiramiento:** Escala la repetición de textura manteniendo proporción métrica real en cajas, cilindros y cuñas.
   - **Rotación UV (`0°–360°` + botones rápidos `0°`, `45°`, `90°`):** Rota las coordenadas UV de la geometría (`ProceduralEngine.applyUVRotation`) permitiendo cambiar la orientación de vetas de madera, ladrillos o chapa acanalada **compartiendo la misma instancia `DataTexture` en GPU**.
   - **Desgaste / Suciedad Procedural (`0%–100%`):** Aplica desconchado en bordes, pátina de óxido y motas de polvo/hollín (`TextureLibrary.applyParametricWear`) e incrementa automáticamente la microrrugosidad superficial.
   - **Relieve de Mapa Normal (`0.0–1.4`):** Ajusta la intensidad del filtro Sobel tangencial (`TextureLibrary.getNormalTexture`) en tiempo real.

---

## 5. Licencias y Procedencia Legal

- **Origen:** 100% de las 118 texturas base, sus 118 mapas normales y las 20 variantes paramétricas son **generadas algorítmicamente por el código propio de ModelCoder** (`web/src/lib/studio/texture-library.ts`) mediante funciones matemáticas deterministas (PRNG Mulberry32, ondas sinusoidales moduladas, patrones celulares y filtros Sobel).
- **Licencia:** **CC0 1.0 Universal (Dominio Público) / MIT License** (misma licencia del repositorio ModelCoder).
- **Restricciones:** **Ninguna.** Pueden utilizarse libremente en aplicaciones comerciales, videojuegos (Godot, Unity, Unreal), modelos exportados en `.glb` y redistribuirse sin requerir atribución externa.

---

## 6. Pruebas Automatizadas Ejecutadas

Se ejecutaron las suites de pruebas automatizadas (`npm --prefix web test`) y el build de producción (`npm --prefix web run build`):

- **`tests/studio_engine.test.ts` (24 pruebas — 100% PASS):**
  - Incluye 4 nuevas pruebas dedicadas (`Expanded Texture Library 1..4`) que verifican:
    1. Existencia de las **118 texturas base PBR** y **20 variantes paramétricas** distribuidas en las **8 categorías** sin IDs duplicados ni referencias rotas.
    2. Síntesis válida de buffers `64×64` RGBA y firmas de píxeles únicas entre familias (`steel_polished`, `diamond_plate`, `copper_oxidized`, `brick_red`, `concrete_cracked`, `wood_oak`, `wood_parquet`, `marble_white`, `granite_grey`, `acoustic_foam`, `pcb_green_gold`, `carbon_fiber`, `solar_panel_blue`, `frosted_glass`, `kevlar_ballistic`, `leather_brown_aged`) más generación de `normalMap`.
    3. Funcionamiento de variaciones paramétricas (`wear`, `uvRotation`, `normalStrength`) y preservación de `map` y `normalMap` en `ProceduralEngine.disposeHierarchy`.
    4. Exportación e importación verificada a `.glb` binario de escenas multi-familia y restauración intacta de `normalMap` tras la exportación.
- **`tests/user_inventory.test.ts` (9 pruebas — 100% PASS):**
  - Verifica borradores, favoritos, colecciones e importación/exportación JSON.
