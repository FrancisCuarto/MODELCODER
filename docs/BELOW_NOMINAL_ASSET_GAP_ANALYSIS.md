# Below Nominal — Análisis de Brechas de Assets Procedurales (Asset Gap Analysis)

> **Documento de Auditoría y Especificación Previa al Desarrollo.**
> Cumple con la Sección 15 del documento maestro `BELOW_NOMINAL_PLAN_100_MODELOS_PROCEDURALES.md`.
> **Estado del Proyecto:** 44 familias base operativas + 1 modelo comunitario integrado (`access_card_lvl1`). Objetivo: 100 familias estructuradas en 7 lotes de producción.

---

## 1. Resumen Ejecutivo de la Auditoría

Se realizó una inspección exhaustiva de los generadores procedurales presentes en `procedural_assets/generators/`, auditando `manifest.json`, `config.py`, `generator.py` y el registro central `GENERATOR_REGISTRY`.

### Métricas Globales del Inventario Real:
- **Familias registradas y activas:** 45 (44 oficiales del núcleo Below Nominal + 1 comunitaria de control de accesos).
- **Cobertura de Manifiestos:** 100% validados contra `schemas/generator-v1.json`.
- **Suite de Pruebas Automatizadas:** 68 tests ejecutados en Blender 5.0 Headless con **100% de éxito (OK)**.
- **Exportación glTF 2.0 / GLB:** Todas las familias existentes compilan y exportan con normalización de pivotes, baking de transforms y colisiones Godot 4 (`-convcolonly`).

---

## 2. Auditoría a Fondo de los 5 Modelos de Referencia

La especificación exige evaluar 5 modelos canónicos para establecer el estándar de calidad de parámetros, presets y geometrías.

| Modelo de Referencia | Categoría | Parámetros Actuales | Presets | Sockets | Colisión | Veredicto & Oportunidad de Mejora |
|---|---|---|---|---|---|---|
| **`door`** | Arquitectura / Seguridad | 10 (`width`, `height`, `thickness`, `panel_count`, `has_window`, `is_jammed`, etc.) | 4 (`standard_bulkhead`, `airlock_door`, `cargo_gate`, `derelict_jammed`) | Sí (`socket_door_frame`, `socket_access_panel`) | `-convcolonly` (compuesta) | **Excelente.** Es el modelo dorado de arquitectura. Sirve de plantilla para puertas de esclusa (`airlock_chamber`) y montacargas (`service_lift_door`). |
| **`terminal`** | Comando | 11 (`terminal_type`, `crt_screen`, `phosphor_color`, `screen_tilt`, `keypad_type`, etc.) | 4 (`operator_console`, `system_monitor`, `emergency_terminal`, `derelict_terminal`) | Sí (`socket_keyboard`, `socket_screen_light`) | `-convcolonly` | **Excelente.** Gran jerarquía de controles de pantalla CRT y color de fósforo. Base directa para `memory_extraction_terminal` y `camera_monitor`. |
| **`oxypod`** | Soporte Vital | 10 (`canister_count`, `mount_type`, `has_gauge`, `wear_level`, etc.) | 3 (`nominal_station`, `low_reserve`, `critical_failure`) | Sí (`socket_canister_mount`, `socket_hud_marker`) | `-convcolonly` | **Muy sólido.** Es la identidad narrativa del oxígeno en el juego. Falta expandir controles para conectar directamente al nuevo `oxygen_tank` (050). |
| **`crew_bed`** | Habitabilidad | 8 (`length`, `width`, `height`, `headboard_height`, `drawer_count`, `messy_sheet`, etc.) | 3 (`standard_crew`, `double_shift_worn`, `abandoned_derelict`) | No requerido | `-convcolonly` | **Cumple estándar.** Modela fielmente camarotes de tripulación y sirve de referencia para `quarantine_bed` (058). |
| **`electrical_panel`**| Ingeniería | 13 (`fuse_count`, `has_knife_switch`, `door_state`, `cable_slack`, etc.) | 4 (`operational`, `breaker_tripped`, `critical_overload`, `scavenged`) | Sí (`socket_cable_in`, `socket_power_out`) | `-convcolonly` | **Modelo insignia de ingeniería.** Maneja cables procedurales catenarios y switches de cuchilla. Base directa para `power_transformer` (068) y `fuse_box` (069). |

---

## 3. Matriz Completa de Clasificación de las 100 Familias

Estado asignado según el plan de producción:
- **`existente`**: Familia implementada y testeada en Lote A (44 modelos).
- **`ampliar`**: Familia existente que requiere enriquecimiento de parámetros o presets adicionales.
- **`crear`**: Familia nueva de las 56 propuestas para los Lotes B al G.
- **`integrado_comunitario`**: Familia aportada por la comunidad (`access_card_lvl1`).

| # | ID de Familia | Nombre Humano | Categoría | Estado | Lote | Presupuesto Tris | Pivot Recomendado |
|---|---|---|---|---|---|---|---|
| 001 | `station_corridor` | Pasillo modular de estación | Entornos | existente | Lote A | 700–1.800 | `floor_center` |
| 002 | `station_room` | Habitación modular de estación | Entornos | existente | Lote A | 800–2.000 | `floor_center` |
| 003 | `autopsy_table` | Mesa de autopsia | Médico | existente | Lote A | 400–850 | `floor_center` |
| 004 | `crash_cart` | Carro de emergencias | Médico | existente | Lote A | 350–700 | `floor_center` |
| 005 | `medical_screen` | Biombo médico | Médico | existente | Lote A | 200–500 | `floor_center` |
| 006 | `morgue_gurney` | Camilla de morgue | Médico | existente | Lote A | 350–750 | `floor_center` |
| 007 | `chemical_cabinet` | Armario de seguridad química | Médico/lab | existente | Lote A | 300–650 | `floor_center` |
| 008 | `restraint_chair` | Silla de contención clínica | Médico | existente | Lote A | 350–700 | `floor_center` |
| 009 | `scrub_sink` | Lavamanos quirúrgico | Médico | existente | Lote A | 250–550 | `wall_back` |
| 010 | `oxypod` | Estación de recarga de oxígeno | Soporte vital | existente | Lote A | 450–900 | `wall_back` |
| 011 | `crew_bed` | Cama de tripulación | Habitabilidad | existente | Lote A | 300–650 | `floor_center` |
| 012 | `bunk_bed` | Litera doble | Habitabilidad | existente | Lote A | 500–1.100 | `floor_center` |
| 013 | `nightstand` | Mesa de luz | Habitabilidad | existente | Lote A | 150–350 | `floor_center` |
| 014 | `radiator_heater` | Radiador térmico | Habitabilidad | existente | Lote A | 250–550 | `wall_back` |
| 015 | `office_door` | Puerta vidriada de oficina | Arquitectura | existente | Lote A | 350–750 | `floor_center` |
| 016 | `mess_table` | Mesa de comedor | Habitabilidad | existente | Lote A | 250–600 | `floor_center` |
| 017 | `ration_automat` | Expendedora de raciones | Habitabilidad | existente | Lote A | 400–850 | `floor_center` |
| 018 | `canteen_counter` | Mostrador de cantina | Habitabilidad | existente | Lote A | 350–750 | `floor_center` |
| 019 | `locker_bench` | Banco de vestuario | Habitabilidad | existente | Lote A | 180–400 | `floor_center` |
| 020 | `space_toilet` | Inodoro espacial | Habitabilidad | existente | Lote A | 300–650 | `floor_center` |
| 021 | `work_bench` | Banco de trabajo pesado | Mantenimiento | existente | Lote A | 400–900 | `floor_center` |
| 022 | `heavy_shelving` | Estantería metálica pesada | Mantenimiento | existente | Lote A | 300–700 | `floor_center` |
| 023 | `tool_chest_cart` | Carro de herramientas | Mantenimiento | existente | Lote A | 350–750 | `floor_center` |
| 024 | `safety_shower` | Ducha de emergencia y lavaojos | Seguridad | existente | Lote A | 350–700 | `floor_center` |
| 025 | `hydroponic_tray_bed` | Bandeja hidropónica | Hidroponía | existente | Lote A | 450–950 | `floor_center` |
| 026 | `electrical_panel` | Panel eléctrico | Ingeniería | existente | Lote A | 500–1.100 | `wall_back` |
| 027 | `pipes` | Tuberías modulares | Ingeniería | existente | Lote A | 200–600 | `center` |
| 028 | `cable_bundle` | Haz de cables colgantes | Ingeniería | existente | Lote A | 300–750 | `center` |
| 029 | `vent_grate` | Rejilla de ventilación | Ingeniería | existente | Lote A | 150–400 | `wall_back` |
| 030 | `crate` | Caja de carga industrial | Carga | existente | Lote A | 120–300 | `floor_center` |
| 031 | `locker` | Taquilla metálica | Habitabilidad | existente | Lote A | 250–550 | `floor_center` |
| 032 | `security_desk` | Puesto de seguridad | Seguridad | existente | Lote A | 450–950 | `floor_center` |
| 033 | `weapons_rack` | Armero de seguridad | Seguridad | existente | Lote A | 350–800 | `wall_back` |
| 034 | `bridge_console_desk` | Consola de mando | Comando | existente | Lote A | 550–1.200 | `floor_center` |
| 035 | `file_cabinet` | Archivador | Oficina | existente | Lote A | 180–400 | `floor_center` |
| 036 | `terminal` | Terminal informático | Comando | existente | Lote A | 300–700 | `floor_center` |
| 037 | `server_rack` | Rack de servidores | Comando/narrativa | existente | Lote A | 500–1.100 | `floor_center` |
| 038 | `door` | Puerta de presión | Arquitectura | existente | Lote A | 450–950 | `floor_center` |
| 039 | `office_desk` | Escritorio de oficina | Mobiliario | existente | Lote A | 250–550 | `floor_center` |
| 040 | `office_chair` | Silla de oficina | Mobiliario | existente | Lote A | 200–450 | `floor_center` |
| 041 | `sign_placard` | Placa de señalización | Señalización | existente | Lote A | 80–220 | `wall_back` |
| 042 | `trash_bin` | Tacho de residuos | Mobiliario | existente | Lote A | 150–350 | `floor_center` |
| 043 | `light_fixture` | Luminaria fluorescente | Iluminación | existente | Lote A | 180–400 | `wall_back` |
| 044 | `fire_extinguisher` | Extintor de incendios | Seguridad | existente | Lote A | 220–500 | `wall_back` |
| COM | `access_card_lvl1` | Tarjeta de Acceso Nivel 1 | Props / Fixtures | integrado_comunitario | Lote A | 80–180 | `center` |
| 045 | `cryo_stasis_pod` | Cápsula de criostasis | Médico/narrativa | crear | Lote B | 600–1.300 | `floor_center` |
| 046 | `consciousness_archive` | Módulo archivo de conciencia | Comando/narrativa | crear | Lote B | 550–1.200 | `floor_center` |
| 047 | `neural_interface_chair` | Silla de interfaz neuronal | Médico/narrativa | crear | Lote B | 450–950 | `floor_center` |
| 048 | `memory_extraction_terminal` | Terminal extracción memoria | Comando/narrativa | crear | Lote B | 400–850 | `floor_center` |
| 049 | `oxygen_regulator` | Regulador de oxígeno | Soporte vital | crear | Lote B | 250–550 | `wall_back` |
| 050 | `oxygen_tank` | Cilindro de oxígeno industrial | Soporte vital | crear | Lote B | 180–420 | `floor_center` |
| 051 | `pressure_door_control` | Control de compuerta presión | Soporte vital | crear | Lote B | 200–450 | `wall_back` |
| 052 | `airlock_chamber` | Módulo de esclusa de aire | Arquitectura/soporte | crear | Lote B | 800–2.000 | `floor_center` |
| 053 | `pressure_indicator` | Indicador de presión sector | Soporte vital | crear | Lote B | 120–280 | `wall_back` |
| 054 | `suit_rack` | Perchero de trajes espaciales | Equipamiento EVA | crear | Lote C | 400–850 | `floor_center` |
| 055 | `eva_suit_stand` | Soporte de traje EVA | Equipamiento EVA | crear | Lote C | 350–750 | `floor_center` |
| 056 | `helmet_storage` | Armario para cascos EVA | Equipamiento EVA | crear | Lote C | 300–650 | `floor_center` |
| 057 | `decon_chamber` | Cabina de descontaminación | Arquitectura/médico | crear | Lote C | 700–1.600 | `floor_center` |
| 058 | `quarantine_bed` | Cama de aislamiento | Médico | crear | Lote C | 400–850 | `floor_center` |
| 059 | `specimen_freezer` | Congelador de muestras | Laboratorio | crear | Lote C | 350–750 | `floor_center` |
| 060 | `biohazard_bin` | Contenedor de bioseguridad | Médico/seguridad | crear | Lote C | 150–350 | `floor_center` |
| 061 | `surgical_light` | Lámpara quirúrgica | Médico/iluminación | crear | Lote C | 250–550 | `wall_back` |
| 062 | `microscope` | Microscopio de laboratorio | Laboratorio | crear | Lote C | 180–400 | `floor_center` |
| 063 | `lab_workstation` | Puesto de laboratorio | Laboratorio | crear | Lote D | 500–1.100 | `floor_center` |
| 064 | `sample_analyzer` | Analizador de muestras | Laboratorio | crear | Lote D | 250–550 | `floor_center` |
| 065 | `chemical_drum` | Bidón químico | Laboratorio/carga | crear | Lote D | 150–350 | `floor_center` |
| 066 | `coolant_pump` | Bomba de refrigerante | Ingeniería | crear | Lote D | 350–750 | `floor_center` |
| 067 | `reactor_control_console` | Consola control de reactor | Ingeniería/comando | crear | Lote D | 600–1.300 | `floor_center` |
| 068 | `power_transformer` | Transformador de potencia | Ingeniería | crear | Lote D | 450–950 | `floor_center` |
| 069 | `fuse_box` | Caja de fusibles mural | Ingeniería | crear | Lote D | 200–450 | `wall_back` |
| 070 | `battery_bank` | Banco de baterías | Ingeniería | crear | Lote D | 400–900 | `floor_center` |
| 071 | `generator_unit` | Generador auxiliar | Ingeniería | crear | Lote D | 500–1.200 | `floor_center` |
| 072 | `coolant_pipe_junction` | Distribuidor de refrigerante | Ingeniería | crear | Lote D | 250–600 | `center` |
| 073 | `cable_tray` | Bandeja portacables | Ingeniería | crear | Lote E | 200–500 | `wall_back` |
| 074 | `overhead_pipe_support` | Soporte de tuberías aéreas | Ingeniería | crear | Lote E | 180–420 | `wall_back` |
| 075 | `floor_grating` | Rejilla de suelo industrial | Arquitectura | crear | Lote E | 150–380 | `floor_center` |
| 076 | `maintenance_hatch` | Escotilla de mantenimiento | Arquitectura | crear | Lote E | 200–450 | `floor_center` |
| 077 | `ladder` | Escalera fija industrial | Arquitectura | crear | Lote E | 200–480 | `wall_back` |
| 078 | `service_lift_door` | Puerta de montacargas | Arquitectura/carga | crear | Lote E | 450–950 | `floor_center` |
| 079 | `cargo_pallet` | Palé industrial | Carga | crear | Lote E | 120–280 | `floor_center` |
| 080 | `cargo_container` | Contenedor de carga | Carga | crear | Lote E | 400–900 | `floor_center` |
| 081 | `conveyor_segment` | Tramo de cinta transportadora | Carga/ingeniería | crear | Lote F | 350–750 | `floor_center` |
| 082 | `forklift_cart` | Carro elevador manual | Carga | crear | Lote F | 300–650 | `floor_center` |
| 083 | `security_camera` | Cámara de seguridad | Seguridad | crear | Lote F | 180–400 | `wall_back` |
| 084 | `access_card_reader` | Lector tarjetas de acceso | Seguridad | crear | Lote F | 120–280 | `wall_back` |
| 085 | `biometric_scanner` | Escáner biométrico | Seguridad | crear | Lote F | 150–350 | `wall_back` |
| 086 | `alarm_siren` | Sirena de alarma industrial | Seguridad | crear | Lote F | 150–350 | `wall_back` |
| 087 | `speaker_intercom` | Intercomunicador de pared | Comunicaciones | crear | Lote F | 120–280 | `wall_back` |
| 088 | `emergency_beacon` | Baliza de emergencia | Seguridad/luz | crear | Lote F | 120–260 | `wall_back` |
| 089 | `camera_monitor` | Monitor de cámaras CCTV | Seguridad/comando | crear | Lote F | 250–600 | `floor_center` |
| 090 | `comms_antenna` | Antena de comunicaciones | Comunicaciones | crear | Lote G | 200–500 | `wall_back` |
| 091 | `antenna_dish` | Antena parabólica compacta | Comunicaciones | crear | Lote G | 250–550 | `floor_center` |
| 092 | `nav_console` | Consola de navegación orbital | Comando | crear | Lote G | 550–1.200 | `floor_center` |
| 093 | `star_chart_display` | Display de mapa estelar | Comando | crear | Lote G | 350–750 | `wall_back` |
| 094 | `hydroponic_tank` | Depósito hidropónico | Hidroponía | crear | Lote G | 250–600 | `floor_center` |
| 095 | `nutrient_pump` | Bomba de nutrientes | Hidroponía | crear | Lote G | 200–450 | `floor_center` |
| 096 | `water_recycler` | Unidad de reciclaje de agua | Soporte vital | crear | Lote G | 450–950 | `floor_center` |
| 097 | `food_storage_unit` | Armario de alimentos | Habitabilidad | crear | Lote G | 300–650 | `floor_center` |
| 098 | `crew_shower` | Cabina de ducha de tripulación | Habitabilidad | crear | Lote G | 400–850 | `floor_center` |
| 099 | `wall_clock` | Reloj industrial de pared | Habitabilidad | crear | Lote G | 100–220 | `wall_back` |
| 100 | `personal_effects_box` | Caja de efectos personales | Habitabilidad | crear | Lote G | 120–280 | `floor_center` |

---

## 4. Hallazgos y Riesgos de Duplicación Auditados

1. **`access_card_lvl1` vs `access_card_reader` (084):**
   - *Evaluación:* No hay duplicación. `access_card_lvl1` es el prop consumible/físico de la tarjeta en mano o sobre mesas. `access_card_reader` es la estación mural con lector magnético empotrado junto a las puertas.
2. **`cable_bundle` (028) vs `cable_tray` (073):**
   - *Evaluación:* Se diferencian claramente. `cable_bundle` es orgánico, flácido y colgante (usa cálculo catenario); `cable_tray` es una pasarela rígida de chapa perforada para canalizaciones de techo.
3. **`pipes` (027) vs `coolant_pipe_junction` (072) vs `overhead_pipe_support` (074):**
   - *Evaluación:* `pipes` son tramos lineales y codos estándar. `coolant_pipe_junction` actúa como manifold repartidor central de fluidos. `overhead_pipe_support` es la estructura de fijación aérea a vigas de techo.
4. **`oxypod` (010) vs `oxygen_tank` (050) vs `oxygen_regulator` (049):**
   - *Evaluación:* Forman el ecosistema modular de soporte vital. `oxypod` es la estación de recarga de pared; `oxygen_tank` es la botella removible intercambiable; `oxygen_regulator` es la válvula reguladora con doble dial.

---

## 5. Prioridades Inmediatas de Ejecución

1. **Lote A (Estandarización 44 existentes):**
   - Actualizar manifests para asegurar que todos los parámetros tengan etiquetas en español y descripciones breves.
   - Preservar compatibilidad total con `tests/` y `web/src/data/catalog.json`.
2. **Lote B (Inicio de Producción Nueva - Familias 45–53):**
   - Priorizar `cryo_stasis_pod`, `consciousness_archive`, `neural_interface_chair`, `memory_extraction_terminal`, `oxygen_regulator`, `oxygen_tank`, `pressure_door_control`, `airlock_chamber`, `pressure_indicator`.
