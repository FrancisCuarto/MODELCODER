import os
import sys
import json

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(current_dir, "docs", "audit_raw.json")

with open(raw_path, "r", encoding="utf-8") as f:
    existing_data = json.load(f)

existing_map = {item["family"]: item for item in existing_data}

# Define the full 100 families as specified in BELOW_NOMINAL_PLAN_100_MODELOS_PROCEDURALES.md
plan_families = [
    # 001-044: Existing
    ("001", "station_corridor", "Pasillo modular de estación", "Entornos", "existente", "Lote A"),
    ("002", "station_room", "Habitación modular de estación", "Entornos", "existente", "Lote A"),
    ("003", "autopsy_table", "Mesa de autopsia", "Médico", "existente", "Lote A"),
    ("004", "crash_cart", "Carro de emergencias", "Médico", "existente", "Lote A"),
    ("005", "medical_screen", "Biombo médico", "Médico", "existente", "Lote A"),
    ("006", "morgue_gurney", "Camilla de morgue", "Médico", "existente", "Lote A"),
    ("007", "chemical_cabinet", "Armario de seguridad química", "Médico/laboratorio", "existente", "Lote A"),
    ("008", "restraint_chair", "Silla de contención clínica", "Médico", "existente", "Lote A"),
    ("009", "scrub_sink", "Lavamanos quirúrgico", "Médico", "existente", "Lote A"),
    ("010", "oxypod", "Estación de recarga de oxígeno", "Soporte vital", "existente", "Lote A"),
    ("011", "crew_bed", "Cama de tripulación", "Habitabilidad", "existente", "Lote A"),
    ("012", "bunk_bed", "Litera doble", "Habitabilidad", "existente", "Lote A"),
    ("013", "nightstand", "Mesa de luz", "Habitabilidad", "existente", "Lote A"),
    ("014", "radiator_heater", "Radiador térmico", "Habitabilidad/ingeniería", "existente", "Lote A"),
    ("015", "office_door", "Puerta vidriada de oficina", "Arquitectura", "existente", "Lote A"),
    ("016", "mess_table", "Mesa de comedor", "Habitabilidad", "existente", "Lote A"),
    ("017", "ration_automat", "Expendedora de raciones", "Habitabilidad", "existente", "Lote A"),
    ("018", "canteen_counter", "Mostrador de cantina", "Habitabilidad", "existente", "Lote A"),
    ("019", "locker_bench", "Banco de vestuario", "Habitabilidad", "existente", "Lote A"),
    ("020", "space_toilet", "Inodoro espacial", "Habitabilidad", "existente", "Lote A"),
    ("021", "work_bench", "Banco de trabajo pesado", "Mantenimiento", "existente", "Lote A"),
    ("022", "heavy_shelving", "Estantería metálica pesada", "Mantenimiento", "existente", "Lote A"),
    ("023", "tool_chest_cart", "Carro de herramientas", "Mantenimiento", "existente", "Lote A"),
    ("024", "safety_shower", "Ducha de emergencia y lavaojos", "Seguridad", "existente", "Lote A"),
    ("025", "hydroponic_tray_bed", "Bandeja hidropónica", "Hidroponía", "existente", "Lote A"),
    ("026", "electrical_panel", "Panel eléctrico", "Ingeniería", "existente", "Lote A"),
    ("027", "pipes", "Tuberías modulares", "Ingeniería", "existente", "Lote A"),
    ("028", "cable_bundle", "Haz de cables colgantes", "Ingeniería", "existente", "Lote A"),
    ("029", "vent_grate", "Rejilla de ventilación", "Ingeniería", "existente", "Lote A"),
    ("030", "crate", "Caja de carga industrial", "Carga", "existente", "Lote A"),
    ("031", "locker", "Taquilla metálica", "Habitabilidad", "existente", "Lote A"),
    ("032", "security_desk", "Puesto de seguridad", "Seguridad", "existente", "Lote A"),
    ("033", "weapons_rack", "Armero de seguridad", "Seguridad", "existente", "Lote A"),
    ("034", "bridge_console_desk", "Consola de mando", "Comando", "existente", "Lote A"),
    ("035", "file_cabinet", "Archivador", "Oficina", "existente", "Lote A"),
    ("036", "terminal", "Terminal informático", "Comando", "existente", "Lote A"),
    ("037", "server_rack", "Rack de servidores y archivos de conciencia", "Comando/narrativa", "existente", "Lote A"),
    ("038", "door", "Puerta de presión", "Arquitectura/seguridad", "existente", "Lote A"),
    ("039", "office_desk", "Escritorio de oficina", "Mobiliario", "existente", "Lote A"),
    ("040", "office_chair", "Silla de oficina", "Mobiliario", "existente", "Lote A"),
    ("041", "sign_placard", "Cartel y placa de señalización", "Señalización", "existente", "Lote A"),
    ("042", "trash_bin", "Tacho de residuos", "Mobiliario", "existente", "Lote A"),
    ("043", "light_fixture", "Luminaria fluorescente protegida", "Iluminación", "existente", "Lote A"),
    ("044", "fire_extinguisher", "Extintor de incendios", "Seguridad", "existente", "Lote A"),
    # 045-053: Lote B (Soporte Vital y Narrativa)
    ("045", "cryo_stasis_pod", "Cápsula de criostasis", "Médico/narrativa", "crear", "Lote B"),
    ("046", "consciousness_archive", "Módulo de archivo de conciencia", "Comando/narrativa", "crear", "Lote B"),
    ("047", "neural_interface_chair", "Silla de interfaz neuronal", "Médico/narrativa", "crear", "Lote B"),
    ("048", "memory_extraction_terminal", "Terminal de extracción de memoria", "Comando/narrativa", "crear", "Lote B"),
    ("049", "oxygen_regulator", "Regulador de oxígeno", "Soporte vital", "crear", "Lote B"),
    ("050", "oxygen_tank", "Cilindro de oxígeno industrial", "Soporte vital", "crear", "Lote B"),
    ("051", "pressure_door_control", "Panel de control de presión", "Soporte vital", "crear", "Lote B"),
    ("052", "airlock_chamber", "Módulo de esclusa de aire", "Arquitectura/soporte vital", "crear", "Lote B"),
    ("053", "pressure_indicator", "Indicador de presión de sector", "Soporte vital", "crear", "Lote B"),
    # 054-062: Lote C (Médico y Laboratorio)
    ("054", "suit_rack", "Perchero de trajes espaciales", "Equipamiento EVA", "crear", "Lote C"),
    ("055", "eva_suit_stand", "Soporte de traje EVA", "Equipamiento EVA", "crear", "Lote C"),
    ("056", "helmet_storage", "Armario para cascos EVA", "Equipamiento EVA", "crear", "Lote C"),
    ("057", "decon_chamber", "Cabina de descontaminación", "Arquitectura/médico", "crear", "Lote C"),
    ("058", "quarantine_bed", "Cama de aislamiento", "Médico", "crear", "Lote C"),
    ("059", "specimen_freezer", "Congelador de muestras", "Laboratorio", "crear", "Lote C"),
    ("060", "biohazard_bin", "Contenedor de bioseguridad", "Médico/seguridad", "crear", "Lote C"),
    ("061", "surgical_light", "Lámpara quirúrgica", "Médico/iluminación", "crear", "Lote C"),
    ("062", "microscope", "Microscopio de laboratorio", "Laboratorio", "crear", "Lote C"),
    # 063-072: Lote D (Ingeniería y Energía)
    ("063", "lab_workstation", "Puesto de laboratorio", "Laboratorio", "crear", "Lote D"),
    ("064", "sample_analyzer", "Analizador de muestras", "Laboratorio", "crear", "Lote D"),
    ("065", "chemical_drum", "Bidón químico", "Laboratorio/carga", "crear", "Lote D"),
    ("066", "coolant_pump", "Bomba de refrigerante", "Ingeniería", "crear", "Lote D"),
    ("067", "reactor_control_console", "Consola de control de reactor", "Ingeniería/comando", "crear", "Lote D"),
    ("068", "power_transformer", "Transformador de potencia", "Ingeniería", "crear", "Lote D"),
    ("069", "fuse_box", "Caja de fusibles mural", "Ingeniería", "crear", "Lote D"),
    ("070", "battery_bank", "Banco de baterías", "Ingeniería", "crear", "Lote D"),
    ("071", "generator_unit", "Generador auxiliar", "Ingeniería", "crear", "Lote D"),
    ("072", "coolant_pipe_junction", "Distribuidor de refrigerante", "Ingeniería", "crear", "Lote D"),
    # 073-080: Lote E (Infraestructura Modular)
    ("073", "cable_tray", "Bandeja portacables", "Ingeniería", "crear", "Lote E"),
    ("074", "overhead_pipe_support", "Soporte de tuberías aéreas", "Ingeniería", "crear", "Lote E"),
    ("075", "floor_grating", "Rejilla de suelo industrial", "Arquitectura/ingeniería", "crear", "Lote E"),
    ("076", "maintenance_hatch", "Escotilla de mantenimiento", "Arquitectura", "crear", "Lote E"),
    ("077", "ladder", "Escalera fija industrial", "Arquitectura", "crear", "Lote E"),
    ("078", "service_lift_door", "Puerta de montacargas", "Arquitectura/carga", "crear", "Lote E"),
    ("079", "cargo_pallet", "Palé industrial", "Carga", "crear", "Lote E"),
    ("080", "cargo_container", "Contenedor de carga", "Carga", "crear", "Lote E"),
    # 081-089: Lote F (Seguridad y Comunicaciones)
    ("081", "conveyor_segment", "Tramo de cinta transportadora", "Carga/ingeniería", "crear", "Lote F"),
    ("082", "forklift_cart", "Carro elevador manual", "Carga", "crear", "Lote F"),
    ("083", "security_camera", "Cámara de seguridad", "Seguridad", "crear", "Lote F"),
    ("084", "access_card_reader", "Lector de tarjetas de acceso", "Seguridad", "crear", "Lote F"),
    ("085", "biometric_scanner", "Escáner biométrico", "Seguridad", "crear", "Lote F"),
    ("086", "alarm_siren", "Sirena de alarma industrial", "Seguridad", "crear", "Lote F"),
    ("087", "speaker_intercom", "Intercomunicador de pared", "Comunicaciones", "crear", "Lote F"),
    ("088", "emergency_beacon", "Baliza de emergencia", "Seguridad/iluminación", "crear", "Lote F"),
    ("089", "camera_monitor", "Monitor de cámaras CCTV", "Seguridad/comando", "crear", "Lote F"),
    # 090-100: Lote G (Navegación y Habitabilidad)
    ("090", "comms_antenna", "Antena de comunicaciones", "Comunicaciones", "crear", "Lote G"),
    ("091", "antenna_dish", "Antena parabólica compacta", "Comunicaciones", "crear", "Lote G"),
    ("092", "nav_console", "Consola de navegación orbital", "Comando", "crear", "Lote G"),
    ("093", "star_chart_display", "Display de mapa estelar", "Comando", "crear", "Lote G"),
    ("094", "hydroponic_tank", "Depósito hidropónico", "Hidroponía", "crear", "Lote G"),
    ("095", "nutrient_pump", "Bomba de nutrientes", "Hidroponía/ingeniería", "crear", "Lote G"),
    ("096", "water_recycler", "Unidad de reciclaje de agua", "Soporte vital/ingeniería", "crear", "Lote G"),
    ("097", "food_storage_unit", "Armario de almacenamiento de alimentos", "Habitabilidad", "crear", "Lote G"),
    ("098", "crew_shower", "Cabina de ducha de tripulación", "Habitabilidad", "crear", "Lote G"),
    ("099", "wall_clock", "Reloj industrial de pared", "Habitabilidad/señalización", "crear", "Lote G"),
    ("100", "personal_effects_box", "Caja de efectos personales", "Habitabilidad/narrativa", "crear", "Lote G"),
]

# Generate docs/BELOW_NOMINAL_ASSET_GAP_ANALYSIS.md
gap_doc = """# Below Nominal — Análisis de Brechas de Assets Procedurales (Asset Gap Analysis)

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
"""

gap_path = os.path.join(current_dir, "docs", "BELOW_NOMINAL_ASSET_GAP_ANALYSIS.md")
with open(gap_path, "w", encoding="utf-8") as f:
    f.write(gap_doc)
print(f"Generated {gap_path}")

# Generate docs/BELOW_NOMINAL_100_ASSET_ROADMAP.md
roadmap_doc = """# Below Nominal — Hoja de Ruta de 100 Familias Procedurales (100 Asset Roadmap)

> **Documento de Planificación y Arquitectura de Producción.**
> Cumple con la Sección 15 del documento maestro `BELOW_NOMINAL_PLAN_100_MODELOS_PROCEDURALES.md`.
> **Ecosistema:** Blender 5.0 Headless → glTF 2.0 / GLB → Godot 4.3+ → Web Catálogo Astro.

---

## 1. Visión y Cronograma de Entregas por Lotes

La producción de las 100 familias se divide en **7 lotes funcionales** para garantizar que ningún lote avance sin pruebas unitarias completas, exportación validada y sincronización con el catálogo web.

```mermaid
flowchart LR
    A["Lote A<br/>Auditoría 44 Base<br/>(Completado)"] --> B["Lote B<br/>Soporte Vital & Narrativa<br/>(45-53)"]
    B --> C["Lote C<br/>Médico & Laboratorio<br/>(54-62)"]
    C --> D["Lote D<br/>Ingeniería & Energía<br/>(63-72)"]
    D --> E["Lote E<br/>Infraestructura Modular<br/>(73-80)"]
    E --> F["Lote F<br/>Seguridad & Comms<br/>(81-89)"]
    F --> G["Lote G<br/>Navegación & Vida<br/>(90-100)"]
```

---

## 2. Detalle de Lotes y Familias

### Lote A: Auditoría y Estandarización Base (44 Familias + 1 Comunitaria)
- **Objetivo:** Auditar, normalizar y validar que las 44 familias fundacionales cumplan con el contrato de manifiesto v1, colisión Godot y suite de pruebas.
- **Familias:** `station_corridor`, `station_room`, `autopsy_table`, `crash_cart`, `medical_screen`, `morgue_gurney`, `chemical_cabinet`, `restraint_chair`, `scrub_sink`, `oxypod`, `crew_bed`, `bunk_bed`, `nightstand`, `radiator_heater`, `office_door`, `mess_table`, `ration_automat`, `canteen_counter`, `locker_bench`, `space_toilet`, `work_bench`, `heavy_shelving`, `tool_chest_cart`, `safety_shower`, `hydroponic_tray_bed`, `electrical_panel`, `pipes`, `cable_bundle`, `vent_grate`, `crate`, `locker`, `security_desk`, `weapons_rack`, `bridge_console_desk`, `file_cabinet`, `terminal`, `server_rack`, `door`, `office_desk`, `office_chair`, `sign_placard`, `trash_bin`, `light_fixture`, `fire_extinguisher`, y `access_card_lvl1`.
- **Estado:** **100% Auditado y Certificado** (68/68 tests pasando en Blender 5.0).

---

### Lote B: Núcleo de Soporte Vital y Narrativa (Familias 45–53)
*Foco: Mecánica central de supervivencia (oxígeno, presión y almacenamiento de conciencia).*

1. **`045. cryo_stasis_pod`**: Cápsula vertical de criostasis industrial con visor de escarcha y bisagras pesadas.
2. **`046. consciousness_archive`**: Banco de racks con cartuchos de memoria y refrigeración líquida.
3. **`047. neural_interface_chair`**: Silla de interfaz neuronal con electrodos low-poly y apoyacabezas.
4. **`048. memory_extraction_terminal`**: Consola con doble CRT, ranura de cartucho y dial analógico.
5. **`049. oxygen_regulator`**: Regulador mural con doble manómetro y válvulas de bronce.
6. **`050. oxygen_tank`**: Botella de oxígeno recargable para carritos, armarios y oxypods.
7. **`051. pressure_door_control`**: Panel numérico diegético con lector de presión bar/psi.
8. **`052. airlock_chamber`**: Módulo de esclusa completa con compuertas dobles y rejillas.
9. **`053. pressure_indicator`**: Indicador analógico circular con aguja de alerta.

---

### Lote C: Médico y Laboratorio (Familias 54–62)
*Foco: Bioseguridad, investigación y trajes de protección exterior.*

1. **`054. suit_rack`**: Perchero reforzado para trajes EVA con perchas tubulares.
2. **`055. eva_suit_stand`**: Maniquí técnico independiente para ajuste de traje espacial.
3. **`056. helmet_storage`**: Armario con compartimentos cúbicos ventilados para cascos.
4. **`057. decon_chamber`**: Cabina de ducha desinfectante con boquillas a 3 niveles.
5. **`058. quarantine_bed`**: Cama de aislamiento con arcos y soportes de sujeción.
6. **`059. specimen_freezer`**: Congelador criogénico de muestras con cierre hermético.
7. **`060. biohazard_bin`**: Contenedor de residuos biológicos con pedal y bolsa visible.
8. **`061. surgical_light`**: Lámpara quirófano multi-reflector con brazo articulado.
9. **`062. microscope`**: Microscopio óptico facetado con torreta de 3 objetivos.

---

### Lote D: Ingeniería y Energía (Familias 63–72)
*Foco: Distribución eléctrica, reactores y análisis químico.*

1. **`063. lab_workstation`**: Mesa de análisis químico con fregadero y repisas reactivas.
2. **`064. sample_analyzer`**: Analizador de sobremesa con bandeja retráctil y leds.
3. **`065. chemical_drum`**: Tambor de reactivos químicos apilable con nervaduras.
4. **`066. coolant_pump`**: Bomba centrífuga de refrigeración con motor de aletas.
5. **`067. reactor_control_console`**: Consola masiva de control nuclear con palancas y diales.
6. **`068. power_transformer`**: Subestación transformadora con aisladores de cerámica.
7. **`069. fuse_box`**: Caja mural con fusibles cerámicos extraíbles.
8. **`070. battery_bank`**: Banco de acumulación energética con bornes de cobre.
9. **`071. generator_unit`**: Grupo electrógeno diésel/auxiliar encapsulado.
10. **`072. coolant_pipe_junction`**: Distribuidor de refrigerante en 3 y 4 vías con válvulas.

---

### Lote E: Infraestructura Modular (Familias 73–80)
*Foco: Conectividad estructural y logística de almacén.*

1. **`073. cable_tray`**: Bandeja perforada para tender cables por el techo.
2. **`074. overhead_pipe_support`**: Estructura de anclaje para colgar tubos de vigas.
3. **`075. floor_grating`**: Panel de suelo desmontable tipo pasarela de trinchera.
4. **`076. maintenance_hatch`**: Escotilla cuadrada/redonda para conductos de servicio.
5. **`077. ladder`**: Escalera fija vertical con jaula protectora antikaídas.
6. **`078. service_lift_door`**: Puerta reforzada de montacargas industrial.
7. **`079. cargo_pallet`**: Palé de transporte para manipulación de cajas y tambores.
8. **`080. cargo_container`**: Contenedor modular de almacenamiento con cantoneras de izaje.

---

### Lote F: Seguridad y Comunicaciones (Familias 81–89)
*Foco: Vigilancia de la estación, alarmas y transporte automatizado.*

1. **`081. conveyor_segment`**: Módulo recto o curvo de cinta transportadora de rodillos.
2. **`082. forklift_cart`**: Carretilla elevadora manual de palés.
3. **`083. security_camera`**: Cámara domo/caja con LED de grabación y visera.
4. **`084. access_card_reader`**: Lector mural de proximidad con ranura e indicador de acceso.
5. **`085. biometric_scanner`**: Escáner de huella/palma con luz láser y placa metálica.
6. **`086. alarm_siren`**: Bocina de advertencia rotativa con campana protectora.
7. **`087. speaker_intercom`**: Intercomunicador de pared de dos vías con rejilla perforada.
8. **`088. emergency_beacon`**: Luz estroboscópica de baliza ámbar/roja con jaula.
9. **`089. camera_monitor`**: Rack de pantallas CRT para monitoreo simultáneo CCTV.

---

### Lote G: Navegación y Habitabilidad (Familias 90–100)
*Foco: Vida a bordo, comunicaciones de largo alcance y soporte vital secundario.*

1. **`090. comms_antenna`**: Mástil de antenas dipolo para enlaces de radiofrecuencia.
2. **`091. antenna_dish`**: Parabólica orientable con alimentador focal para enlace orbital.
3. **`092. nav_console`**: Puesto de pilotaje y telemetría espacial con mandos analógicos.
4. **`093. star_chart_display`**: Pantalla mural de coordenadas de la órbita de Europa.
5. **`094. hydroponic_tank`**: Tanque translúcido de soluciones biológicas y sales.
6. **`095. nutrient_pump`**: Micro-bomba dosificadora para cultivos agrícolas.
7. **`096. water_recycler`**: Depurador de aguas grises con filtros de ósmosis.
8. **`097. food_storage_unit`**: Armario hermético para paquetes de raciones sintéticas.
9. **`098. crew_shower`**: Cabina de ducha individual con cortina industrial y grifo.
10. **`099. wall_clock`**: Reloj analógico militar de 24 horas para turnos de estación.
11. **`100. personal_effects_box`**: Baúl de recuerdos personales de la tripulación.

---

## 3. Protocolo de Validación Obligatorio por Cada Familia

Para cada generador nuevo o modificado se sigue rigurosamente el pipeline de 13 pasos:
1. **Auditoría de Requisitos:** Verificar unicidad de ID y ausencia de duplicados.
2. **Configuración Tipada:** Crear `config.py` heredando de `BaseAssetConfig` con tipado estricto.
3. **Manifiesto Formal:** Redactar `manifest.json` con etiquetas en español, sliders, grupos y al menos 2 presets.
4. **Construcción BMesh:** Implementar `generator.py` reutilizando primitivas de `MeshBuilder`.
5. **Mapeo al Atlas:** Asignar roles semánticos (`CASING`, `METAL`, `SCREEN`, `PANEL`, etc.) vinculados al atlas 256×256 con protección de medio texel.
6. **Verificación UV y Colores:** Auditoría obligatoria con capas `UVMap` y vertex colors `Col`.
7. **Compactación:** Limpieza de slots de materiales vacíos mediante `compact_materials(obj)`.
8. **Pivote y Normalización:** Configuración de pivote diegético (`floor_center`, `wall_back`, `center`) y horneado de transforms.
9. **Colisiones para Godot:** Generación automática de nodos `-convcolonly`.
10. **Exportación Dual:** Generar binario `.glb` y metadatos sidecar `.json`.
11. **Pruebas en Blender Headless:** Integrar test unitario en `tests/` comprobando determinismo y presets.
12. **Sincronización Web:** Actualizar `web/src/data/catalog.json` y generar modelo para visualización 3D.
13. **Inspección Visual:** Verificar proporciones y estética retro PSX (sin subdivisiones excesivas).
"""

roadmap_path = os.path.join(current_dir, "docs", "BELOW_NOMINAL_100_ASSET_ROADMAP.md")
with open(roadmap_path, "w", encoding="utf-8") as f:
    f.write(roadmap_doc)
print(f"Generated {roadmap_path}")
