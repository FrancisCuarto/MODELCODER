"""
Blender Viewport Addon / Interactive Panel for Below Nominal Master Asset Generator.
Exposes deep granular customization options, marked variants, and authentic PS1
weathered texture controls for all 17 retro-industrial asset families.
"""

bl_info = {
    "name": "Below Nominal - Master Asset Generator",
    "author": "Antigravity",
    "version": (1, 5, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar (N) > Below Nominal",
    "description": "Deep procedural asset generator for Below Nominal (44 PSX aesthetic families & textured wear)",
    "category": "3D View",
}

import sys
import os
import random

addon_dir = os.path.dirname(os.path.abspath(__file__))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy.types import Operator, Panel, PropertyGroup

from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    CrashCartConfig,
    OfficeDeskConfig,
    OfficeChairConfig,
    SignPlacardConfig,
    TrashBinConfig,
    LightFixtureConfig,
    FireExtinguisherConfig,
    VentGrateConfig,
    CableBundleConfig,
    ElectricalPanelConfig,
    TerminalConfig,
    OxypodConfig,
    DoorConfig,
    ServerRackConfig,
    CrateConfig,
    LockerConfig,
    PipeConfig,
    StationCorridorConfig,
    StationRoomConfig,
    CrewBedConfig,
    BunkBedConfig,
    NightstandConfig,
    RadiatorHeaterConfig,
    OfficeDoorConfig,
    AutopsyTableConfig,
    MedicalScreenConfig,
    MorgueGurneyConfig,
    ChemicalCabinetConfig,
    RestraintChairConfig,
    MessTableConfig,
    RationAutomatConfig,
    CanteenCounterConfig,
    FileCabinetConfig,
    LockerBenchConfig,
    WorkBenchConfig,
    HeavyShelvingConfig,
    ToolChestCartConfig,
    SafetyShowerConfig,
    HydroponicTrayBedConfig,
    SecurityDeskConfig,
    WeaponsRackConfig,
    BridgeConsoleDeskConfig,
    SpaceToiletConfig,
    ScrubSinkConfig
)
from procedural_assets.export.glb_exporter import GLBExporter

class BelowNominalPanelSettings(PropertyGroup):
    asset_family: EnumProperty(
        name="Familia de Asset",
        description="Familia de objeto 3D a generar con estética PS1 retrofuturista",
        items=[
            ("station_corridor", "Módulo de Pasillo / Corredor (Tile)", "Corredor modular con costillas, suelo diamantado, cables e iluminación"),
            ("station_room", "Habitación / Sala de Estación", "Cámara completa: Medbay, Control, Bahía de Carga o Esclusa con vanos para puertas"),
            ("crew_bed", "Cama de Tripulación / Camilla", "Cama modular de descanso o camilla de enfermería con inclinación"),
            ("bunk_bed", "Litera de Tripulación Doble", "Litera apilada de dos niveles con escalera, barandilla y taquillas"),
            ("nightstand", "Mesa de Luz / Taquilla de Noche", "Mueble de cabecera con cajones deslizables, bandeja y lámpara de lectura"),
            ("radiator_heater", "Radiador / Calefactor Industrial", "Calefacción de mamparo con aletas térmicas, convector o torre"),
            ("office_door", "Puerta de Oficina Vidriada", "Puerta de laboratorio con vidrio armado con malla de alambre y barra antipánico"),
            ("crash_cart", "Carrito de Mantenimiento / Choque", "Carrito industrial con cajones deslizables, monitor CRT y ruedas"),
            ("office_desk", "Mesa / Escritorio de Laboratorio", "Mesa metálica modular con cajoneras, pasacables y estantes"),
            ("office_chair", "Silla de Oficina / Mando", "Silla giratoria ergonómica con cojín vinílico y variantes rotas"),
            ("sign_placard", "Cartel / Señalética de Estación", "Placard de advertencia o evacuación con opciones de daño"),
            ("trash_bin", "Tacho de Basura / Biohazard", "Contenedor de residuos con pedal, tapa batiente y basura visible"),
            ("light_fixture", "Luminaria Industrial / Mamparo", "Tubo fluorescente, mamparo con jaula o baliza de emergencia"),
            ("fire_extinguisher", "Extintor de Incendios", "Extintor presurizado con manómetro, manguera y gabinete mural"),
            ("vent_grate", "Rejilla de Ventilación / Ducto", "Lamas HVAC, aspas de ventilador interno y rejilla de escape"),
            ("cable_bundle", "Mazo de Cables / Bandeja", "Cables umbilicales con catenaria, bandejas y cables cortados"),
            ("electrical_panel", "Panel Eléctrico Industrial", "Panel de control con botones, interruptores, display y cables"),
            ("terminal", "Terminal de Computadora", "Terminal diegético con pantalla CRT y teclado"),
            ("oxypod", "Estación Oxypod (Oxígeno)", "Estación de recarga de oxígeno con indicador cian brillante"),
            ("door", "Puerta de Esclusa / Mamparo", "Puerta corredera industrial blindada con opción de atasco"),
            ("server_rack", "Rack de Servidores / Memoria", "Armario de servidores con módulos de conciencias"),
            ("crate", "Caja de Carga / Químicos", "Caja de suministros o contenedor químico"),
            ("locker", "Taquillas de Tripulación", "Batería de lockers metálicos para vestuarios"),
            ("pipes", "Tubería con Válvula", "Tramo de tubería industrial con válvula manual y manómetro"),
            # 20 Nuevas Familias de Mobiliario y Survival Horror
            ("autopsy_table", "Mesa de Autopsia / Disección", "Mesa de examen post-mortem en acero inoxidable con lámpara quirúrgica y desagüe"),
            ("medical_screen", "Biombo Médico Plegable", "Biombo acordeón sobre ruedas para aislamiento o privacidad"),
            ("morgue_gurney", "Camilla de Morgue / Tijera", "Carro de transporte con elevador tijera y silueta de bolsa mortuoria"),
            ("chemical_cabinet", "Gabinete de Químicos / Muestras", "Armario vidriado con malla de alambre, candado y frascos"),
            ("restraint_chair", "Silla de Contención / Interrogatorio", "Silla de detención reforzada con grilletes y soporte de suero"),
            ("mess_table", "Mesa de Comedor / Cantina", "Mesa comunal con taburetes giratorios anclados y bandejas de comida"),
            ("ration_automat", "Autómata Dispensador de Raciones", "Expendedora brutalista con teclado, display y compuerta trabada"),
            ("canteen_counter", "Mostrador de Servicio / Cantina", "Pasa-platos de acero con persiana metálica, rieles y lámparas térmicas"),
            ("file_cabinet", "Archivador Metálico de Oficina", "Archivador vertical u horizontal con cajones abiertos y documentos"),
            ("locker_bench", "Banco de Vestuario / Botas", "Banco de chapa perforada con estante inferior para calzado magnético"),
            ("work_bench", "Banco de Trabajo / Taller", "Mesa de mantenimiento con tornillo de banco, herramientas y luminaria"),
            ("heavy_shelving", "Estantería de Carga Pesada", "Estantes de perfil angular con cajas de carga, bidones y refuerzos en X"),
            ("tool_chest_cart", "Carro Porta-Herramientas", "Carro rodante de mecánico con cajoneras, tirador y repuestos"),
            ("safety_shower", "Ducha de Seguridad / Lavaojos", "Estación de descontaminación de emergencia con cadena y bacha lavaojos"),
            ("hydroponic_tray_bed", "Bandeja Hidropónica / Soporte Vital", "Cultivo botánico con tuberías de nutrientes, lámpara UV y vegetación"),
            ("security_desk", "Puesto de Guardia / Seguridad", "Mostrador de control con vidrio antibalas, interfono y monitor CCTV"),
            ("weapons_rack", "Armero Vertical / Armería", "Soporte de armas largas con barra de cierre con candado y munición"),
            ("bridge_console_desk", "Consola de Mando / Puente", "Puesto de pilotaje en herradura con múltiples pantallas CRT y asiento"),
            ("space_toilet", "Retrete de Vacío Zero-G", "Inodoro estanco en acero con abrazaderas de muslos y manguera de succión"),
            ("scrub_sink", "Lavabo Quirúrgico / Sanitización", "Pila quirúrgica con grifo cuello de cisne, dispensador y espejo"),
        ],
        default="station_corridor"
    )

    # --- CONTROLES GLOBALES Y TEXTURAS PS1 ---
    palette_name: EnumProperty(
        name="Paleta de Sector",
        description="Paleta temática y sectorial de la estación Below Nominal",
        items=[
            ("industrial_hazard", "Sector Industrial / Reactor", "Metal oscuro, franjas de peligro amarillo/negro y luces ámbar"),
            ("medbay_clean", "Enfermería / Laboratorio Clínico", "Esmalte blanco antiséptico, acero inoxidable, azulejos cerámicos y telemetría azul"),
            ("command_bridge", "Puente de Mando / Operaciones", "Gris carbón táctico, aluminio satinado, latón y fósforo ámbar"),
            ("habitation_worn", "Hábitat / Módulos de Tripulación", "Plástico beige retrocomputación, oliva apagado y luz cálida de lectura"),
            ("derelict_decay", "Sector Abandonado / Decadencia", "Óxido severo, pintura desconchada, pantallas muertas y luces de emergencia rojas tenue")
        ],
        default="industrial_hazard"
    )
    emission_scale: FloatProperty(
        name="Intensidad Emisión",
        description="Multiplicador de intensidad emisiva para pantallas CRT, indicadores LED y fluidos brillantes",
        default=1.0,
        min=0.0,
        max=5.0
    )
    seed: IntProperty(
        name="Semilla (Seed)",
        description="Semilla numérica aleatoria. El mismo número siempre genera el mismo modelo y manchas de desgaste.",
        default=1337
    )
    asset_name: StringProperty(
        name="Nombre del Asset",
        description="Nombre del objeto 3D y de los archivos exportados",
        default="asset_psx"
    )
    wear_level: FloatProperty(
        name="Desgaste y Óxido PS1",
        description="0.0 = De fábrica / Limpio, 1.0 = Ruina industrial con óxido pesado y pintura descascarada",
        default=0.65,
        min=0.0,
        max=1.0
    )
    target_tri_budget: IntProperty(
        name="Presupuesto Triángulos",
        description="Límite objetivo de polígonos PSX (Recomendado: 300 - 650)",
        default=550,
        min=150,
        max=1400
    )
    scale_factor: FloatProperty(
        name="Escala Global",
        default=1.0,
        min=0.4,
        max=3.0
    )

    # --- VARIANTES DE STATION CORRIDOR ---
    corridor_type: EnumProperty(
        name="Tipo de Corredor",
        items=[
            ("straight", "Pasillo Recto", "Módulo recto con paredes continuas"),
            ("corner_90", "Codo 90° (Curva)", "Curva en ángulo recto de pasillo"),
            ("t_junction", "Intersección en T (3 vías)", "Cruce de 3 direcciones con portal lateral"),
            ("cross_junction", "Cruce en Cruz (+ 4 vías)", "Intersección de 4 direcciones con 4 pilares"),
            ("doorway_arch", "Marco de Puerta / Mamparo", "Corredor con vano central para puerta corredera"),
            ("dead_end", "Fin de Pasillo / Cul-de-Sac", "Extremo ciego con escotilla de mantenimiento")
        ],
        default="straight"
    )
    corridor_width: FloatProperty(name="Ancho Pasillo (m)", default=3.0, min=2.0, max=6.0)
    corridor_length: FloatProperty(name="Largo Pasillo (m)", default=4.0, min=2.5, max=8.0)
    corridor_height: FloatProperty(name="Alto Techo (m)", default=3.0, min=2.4, max=4.5)
    corridor_floor_style: EnumProperty(
        name="Estilo de Suelo",
        items=[
            ("tread_plate", "Chapa Antideslizante", "Chapa metálica con franjas de advertencia"),
            ("grated_trench", "Trinchera con Rejilla", "Trinchera central de drenaje con rejilla metálica"),
            ("smooth_tile", "Piso de Placas Lisas", "Placas compuestas modulares de estación")
        ],
        default="tread_plate"
    )
    corridor_wall_style: EnumProperty(
        name="Estilo de Paredes",
        items=[
            ("structural_ribs", "Costillas / Columnas", "Pilares verticales de refuerzo estructural"),
            ("recessed_panels", "Paneles con Nichos", "Vanos embutidos para equipos y extintores"),
            ("smooth_bulkhead", "Mamparo Blindado Liso", "Chapas lisas con remaches de unión")
        ],
        default="structural_ribs"
    )
    corridor_ceiling_style: EnumProperty(
        name="Estilo de Techo",
        items=[
            ("exposed_beams", "Vigas en I Expuestas", "Girders metálicos transversales con bandejas"),
            ("vaulted_conduit", "Achaflanado con Ductos", "Techo biselado industrial"),
            ("flat_recessed", "Liso con Troffers", "Techo cerrado con bandejas de luz embutidas")
        ],
        default="exposed_beams"
    )
    corridor_lighting: BoolProperty(name="Luminarias Integradas", default=True)
    corridor_light_state: EnumProperty(
        name="Estado Iluminación",
        items=[
            ("working", "Operativo (Blanco)", "Tubo fluorescente encendido normal"),
            ("flickering", "Titilante / Fallando", "Iluminación inestable de survival horror"),
            ("emergency_red", "Alarma Roja", "Luz roja de emergencia de descompresión"),
            ("unlit", "Apagado / Muerto", "Tubo quemado a oscuras")
        ],
        default="working"
    )
    corridor_cable_runs: BoolProperty(name="Bandejas de Cables Superiores", default=True)
    corridor_wall_alcove: BoolProperty(name="Nicho Mural para Props", default=True)
    corridor_hazard_stripes: BoolProperty(name="Franjas de Peligro en Bordes", default=True)
    corridor_damage: EnumProperty(
        name="Daño / Survival Horror",
        items=[
            ("pristine", "Intacto / Operativo", "Sin daños estructurales visibles"),
            ("collapsed_ceiling_wires", "Techo Caído y Cables", "Placa de techo descolgada con cables colgando"),
            ("blood_oil_stain", "Mancha de Sangre / Aceite", "Charco oscuro con óxido y desgaste en el suelo"),
            ("breached_vent", "Ducto de Rejilla Reventado", "Rejilla de pared rota y arrancada hacia el ducto")
        ],
        default="pristine"
    )

    # --- VARIANTES DE STATION ROOM ---
    room_archetype: EnumProperty(
        name="Arquetipo de Sala",
        items=[
            ("medbay_lab", "Medbay / Lab Criogénico", "Enfermería y laboratorio con trinchera de drenaje"),
            ("control_hub", "Centro de Control / Puente", "Puesto de mando con plataforma elevada y mirador"),
            ("cargo_bay", "Bahía de Carga / Depósito", "Almacén industrial de techo alto con grúa puente"),
            ("airlock_chamber", "Cámara de Esclusa / Airlock", "Cámara de descompresión con vanos blindados"),
            ("crew_quarters", "Camarotes de Tripulación", "Módulo habitacional con nichos de descanso")
        ],
        default="medbay_lab"
    )
    room_width: FloatProperty(name="Ancho Sala (m)", default=6.0, min=4.0, max=14.0)
    room_depth: FloatProperty(name="Profundidad Sala (m)", default=8.0, min=4.0, max=16.0)
    room_height: FloatProperty(name="Alto Sala (m)", default=3.4, min=2.8, max=6.0)
    room_door_north: BoolProperty(name="Vano de Puerta Norte (+Y)", default=True)
    room_door_south: BoolProperty(name="Vano de Puerta Sur (-Y)", default=True)
    room_door_east: BoolProperty(name="Vano de Puerta Este (+X)", default=False)
    room_door_west: BoolProperty(name="Vano de Puerta Oeste (-X)", default=False)
    room_pillar_layout: EnumProperty(
        name="Distribución Columnas",
        items=[
            ("perimeter_buttresses", "Contrafuertes Perimetrales", "Columnas adosadas a las esquinas y paredes"),
            ("center_single", "Columna Central Gruesa", "Pilar brutalista central de soporte"),
            ("dual_columns", "Doble Columna en Eje", "Dos columnas simétricas a lo largo de la sala"),
            ("none", "Espacio Diáfano (Sin Columnas)", "Sala abierta sin columnas intermedias")
        ],
        default="perimeter_buttresses"
    )
    room_elevation: EnumProperty(
        name="Desnivel del Suelo",
        items=[
            ("flat", "Piso Plano", "Nivel continuo en toda la sala"),
            ("raised_platform", "Plataforma Elevada con Escalón", "Estrado superior para puesto de mando"),
            ("sunken_pit", "Foso Central Hundido", "Área central deprimida con bordillos")
        ],
        default="flat"
    )
    room_observation_window: BoolProperty(name="Mirador de Vidrio Blindado", default=False)
    room_overhead_gantry: BoolProperty(name="Grúa Puente Industrial", default=False)
    room_floor_drain: BoolProperty(name="Trinchera de Drenaje", default=False)
    room_lighting_color: EnumProperty(
        name="Tono de Iluminación",
        items=[
            ("clean_white", "Blanco Fluorescente", "Luz blanca de laboratorio estándar"),
            ("emergency_red", "Rojo de Emergencia", "Luces de alarma de descompresión"),
            ("medbay_cyan", "Cian Criogénico", "Atmósfera fría de soporte vital"),
            ("dim_amber", "Ámbar Tenue / Alerta", "Iluminación de guardia nocturna")
        ],
        default="clean_white"
    )

    # --- VARIANTES DE CRASH CART ---
    cart_width: FloatProperty(name="Ancho Carrito (m)", default=0.65, min=0.35, max=1.3)
    cart_height: FloatProperty(name="Alto Carrito (m)", default=0.85, min=0.45, max=1.6)
    cart_depth: FloatProperty(name="Profundidad Carrito (m)", default=0.48, min=0.25, max=1.0)
    cart_drawers: IntProperty(name="Cantidad de Cajones", default=4, min=1, max=6)
    cart_drawer_mode: EnumProperty(
        name="Apertura Cajones",
        items=[
            ("staggered", "Escalonado (Estilo PS1)", "Cajones abiertos a diferentes profundidades visibles"),
            ("all_closed", "Todos Cerrados", "Cajones completamente guardados en el mueble"),
            ("top_open", "Solo Cajón Superior", "Cajón superior abierto para acceso rápido"),
            ("all_open", "Todos Abiertos (Saqueado)", "Todos los cajones extraídos tras una evacuación")
        ],
        default="staggered"
    )
    cart_slide_max: FloatProperty(name="Extensión Máxima (m)", default=0.22, min=0.05, max=0.45)
    cart_handle_style: EnumProperty(
        name="Tipo de Manijas",
        items=[
            ("metal_bar", "Barra Tubular Metálica", "Tirador cilíndrico de acero"),
            ("recessed_lip", "Bisel Embutido", "Ranura metálica integrada")
        ],
        default="metal_bar"
    )
    has_top_monitor: BoolProperty(name="Monitor CRT / Desfibrilador Superior", default=True)
    cart_monitor_phosphor: EnumProperty(
        name="Fósforo Monitor",
        items=[("green", "Verde Fósforo", "CRT verde"), ("amber", "Ámbar Fósforo", "CRT ámbar")],
        default="green"
    )
    has_push_handle: BoolProperty(name="Barra de Empuje Lateral", default=True)
    push_handle_side: EnumProperty(
        name="Lado de Empuje",
        items=[("left", "Izquierdo", ""), ("right", "Derecho", "")],
        default="left"
    )
    has_oxygen_rack: BoolProperty(name="Soporte de Tubos de Oxígeno", default=True)
    oxygen_tank_count: IntProperty(name="Tubos de Oxígeno", default=1, min=1, max=2)
    body_color_preset: EnumProperty(
        name="Pintura del Carrito",
        items=[
            ("red_emergency", "Rojo Emergencia Desgastado", "Pintura roja con desconchones y óxido"),
            ("dirty_beige", "Beige Plástico Sucio", "Carcasa retro envejecida"),
            ("hazard_yellow", "Amarillo Advertencia / Peligro", "Franjas industriales de seguridad")
        ],
        default="red_emergency"
    )

    # --- VARIANTES DE OFFICE DESK ---
    desk_width: FloatProperty(name="Ancho Mesa (m)", default=1.40, min=0.8, max=2.5)
    desk_height: FloatProperty(name="Alto Mesa (m)", default=0.76, min=0.6, max=1.1)
    desk_depth: FloatProperty(name="Profundidad (m)", default=0.75, min=0.5, max=1.2)
    desk_leg_style: EnumProperty(
        name="Estilo de Patas",
        items=[
            ("tubular_four_legs", "4 Patas Tubulares", "Patas de acero con regatones"),
            ("panel_sides", "Paneles Laterales Ciegos", "Laterales macizos de chapa"),
            ("cantilever_t_frame", "Chasis en T Invertida", "Base cantiléver industrial")
        ],
        default="tubular_four_legs"
    )
    desk_pedestals: EnumProperty(
        name="Cajoneras (Pedestales)",
        items=[
            ("right_only", "Solo Derecha", "Cajonera en lado derecho"),
            ("left_only", "Solo Izquierda", "Cajonera en lado izquierdo"),
            ("dual_pedestals", "Doble Cajonera", "Cajoneras a ambos lados"),
            ("none", "Sin Cajones (Mesa Simple)", "Mesa de trabajo libre")
        ],
        default="right_only"
    )
    desk_drawers: IntProperty(name="Cajones por Pedestal", default=3, min=1, max=4)
    desk_drawer_style: EnumProperty(
        name="Apertura de Cajones",
        items=[
            ("top_open", "Cajón Superior Abierto", "Primer cajón entreabierto"),
            ("all_closed", "Todos Cerrados", "Cajones guardados"),
            ("all_ajar", "Todos Entreabiertos", "Desorden / evacuable")
        ],
        default="top_open"
    )
    desk_cable_grommet: BoolProperty(name="Pasacables en Tapa", default=True)
    desk_partition: BoolProperty(name="Biombo / Mampara Posterior", default=False)
    desk_under_shelf: BoolProperty(name="Estante Inferior para CPU", default=True)
    desk_surface_material: EnumProperty(
        name="Acabado de Tapa",
        items=[
            ("metal_dark", "Chapa Oscura Oxidada", "Acero con marcas de grasa"),
            ("beige_formica", "Fórmica Beige Retro", "Plástico amarillento desgastado"),
            ("hazard", "Franjas de Peligro", "Franjas amarillas y negras")
        ],
        default="metal_dark"
    )

    # --- VARIANTES DE OFFICE CHAIR ---
    chair_seat_width: FloatProperty(name="Ancho Asiento (m)", default=0.52, min=0.4, max=0.7)
    chair_seat_depth: FloatProperty(name="Profundidad Asiento (m)", default=0.50, min=0.4, max=0.65)
    chair_seat_height: FloatProperty(name="Altura Asiento (m)", default=0.48, min=0.35, max=0.65)
    chair_backrest_style: EnumProperty(
        name="Tipo de Respaldo",
        items=[
            ("mid_back", "Medio Acolchado", "Respaldo estándar de oficina"),
            ("high_back_headrest", "Alto con Cabezal", "Butaca de comando ejecutivo"),
            ("low_back", "Bajo Operativo", "Silla compacta de operario")
        ],
        default="mid_back"
    )
    chair_backrest_tilt: FloatProperty(name="Inclinación Respaldo", default=8.0, min=0.0, max=25.0)
    chair_base_style: EnumProperty(
        name="Tipo de Base",
        items=[
            ("five_star_casters", "5 Ruedas Giratorias", "Base estrella móvil"),
            ("four_leg_tubular", "4 Patas Tubulares Fijas", "Estructura fija para vibración"),
            ("pedestal_bolted", "Pedestal Embridado al Piso", "Atornillado al suelo naval")
        ],
        default="five_star_casters"
    )
    chair_spokes: IntProperty(name="Rayos de Base", default=5, min=3, max=6)
    chair_armrests: EnumProperty(
        name="Apoyabrazos",
        items=[
            ("both", "Ambos Intactos", "Dos apoyabrazos acolchados"),
            ("one_broken", "Uno Roto (Survival Horror)", "Apoyabrazos derecho partido"),
            ("none", "Sin Apoyabrazos", "Silla de trabajo rápido")
        ],
        default="both"
    )
    chair_upholstery: EnumProperty(
        name="Tapizado Vinílico",
        items=[
            ("dark_charcoal", "Cuerina Gris Oscura", "Vinilo gastado con arrugas"),
            ("emergency_red", "Cuero Rojo Emergencia", "Tapizado rojo desgastado"),
            ("industrial_blue", "Azul Técnico", "Tapizado azul estación")
        ],
        default="dark_charcoal"
    )

    # --- VARIANTES DE SIGN PLACARD ---
    sign_width: FloatProperty(name="Ancho Cartel (m)", default=0.80, min=0.3, max=2.0)
    sign_height: FloatProperty(name="Alto Cartel (m)", default=0.35, min=0.15, max=1.0)
    sign_mount: EnumProperty(
        name="Montaje Cartel",
        items=[
            ("wall_flush", "Mural Atornillado", "Fijado plano a la pared"),
            ("ceiling_hanging", "Colgante del Techo", "Suspendido por cadenas"),
            ("flag_perpendicular", "Bandera Perpendicular", "Proyectado hacia el pasillo")
        ],
        default="wall_flush"
    )
    sign_type: EnumProperty(
        name="Tipo de Señal",
        items=[
            ("hazard_biohazard", "Peligro Biológico / Químico", "Amarillo con símbolo de biohazard"),
            ("emergency_exit", "Salida de Emergencia / Evacuación", "Verde brillante iluminado"),
            ("sector_id", "Identificación de Sector / Laboratorio", "Azul con código de sub-nivel"),
            ("high_voltage", "Alta Tensión / Eléctrico", "Rojo peligro de electrocución")
        ],
        default="hazard_biohazard"
    )
    sign_damage: EnumProperty(
        name="Estado / Daño",
        items=[
            ("bent_corner", "Esquina Doblada / Arrancada", "Chapa doblada hacia afuera"),
            ("pristine", "Intacto", "Sin deformaciones estructurales"),
            ("hanging_crooked", "Cadena Cortada / Torcido", "Colgando inclinado de un eslabón")
        ],
        default="bent_corner"
    )
    sign_chain_len: FloatProperty(name="Largo de Cadenas (m)", default=0.45, min=0.1, max=1.2)

    # --- VARIANTES DE TRASH BIN ---
    trash_height: FloatProperty(name="Alto Tacho (m)", default=0.65, min=0.3, max=1.2)
    trash_radius: FloatProperty(name="Radio / Ancho (m)", default=0.20, min=0.1, max=0.4)
    trash_is_rectangular: BoolProperty(name="Forma Rectangular", default=False)
    trash_bin_type: EnumProperty(
        name="Tipo de Tacho",
        items=[
            ("pedal_can", "Tacho a Pedal con Tapa", "Tacho metálico con pedal inferior"),
            ("drum_hazard", "Tambor de Desechos Peligrosos", "Barril con aros de refuerzo"),
            ("office_basket", "Papelera de Oficina Simple", "Cesto abierto sin tapa")
        ],
        default="pedal_can"
    )
    trash_lid_state: EnumProperty(
        name="Estado de Tapa",
        items=[
            ("ajar", "Entreabierta (25°)", "Tapa semiabierta"),
            ("closed", "Cerrada", "Completamente tapado"),
            ("open_wide", "Completamente Abierta", "Pedal presionado a tope"),
            ("missing", "Sin Tapa", "Tapa ausente o arrancada")
        ],
        default="ajar"
    )
    trash_foot_pedal: BoolProperty(name="Pedal de Pie", default=True)
    trash_overflowing: BoolProperty(name="Basura Desbordando", default=True)

    # --- VARIANTES DE LIGHT FIXTURE ---
    light_type: EnumProperty(
        name="Tipo de Luminaria",
        items=[
            ("fluorescent_troffer", "Tubo Fluorescente Doble", "Armadura de chapa con tubos"),
            ("bulkhead_cage", "Mamparo Oval con Jaula", "Lámpara estanca con rejilla protectora"),
            ("emergency_beacon", "Baliza de Alarma Rotativa", "Domo rojo giratorio de emergencia")
        ],
        default="fluorescent_troffer"
    )
    light_length: FloatProperty(name="Largo Luminaria (m)", default=1.20, min=0.4, max=2.5)
    light_width: FloatProperty(name="Ancho Luminaria (m)", default=0.28, min=0.15, max=0.6)
    light_depth: FloatProperty(name="Profundidad (m)", default=0.10, min=0.06, max=0.3)
    light_tubes: IntProperty(name="Cantidad de Tubos", default=2, min=1, max=3)
    light_state: EnumProperty(
        name="Estado Eléctrico",
        items=[
            ("both_working", "Tubos Encendidos", "Iluminación operativa"),
            ("flickering_one_dead", "Uno Muerto / Parpadeo", "Un tubo quemado negro, uno titilando"),
            ("completely_dead", "Totalmente Apagado", "Sin corriente, tubos oscuros"),
            ("emergency_red", "Luz Roja de Emergencia", "Luz roja de alarma de esclusa")
        ],
        default="flickering_one_dead"
    )
    light_wire_guard: BoolProperty(name="Rejilla de Alambre Protectora", default=True)
    light_dangling_wire: BoolProperty(name="Cable Eléctrico Colgando", default=True)

    # --- VARIANTES DE FIRE EXTINGUISHER ---
    ext_tank_radius: FloatProperty(name="Radio Tanque (m)", default=0.08, min=0.05, max=0.15)
    ext_tank_height: FloatProperty(name="Alto Tanque (m)", default=0.45, min=0.3, max=0.7)
    ext_mount_style: EnumProperty(
        name="Tipo de Montaje",
        items=[
            ("wall_bracket", "Soporte Mural Abierto", "Abrazadera metálica directo a pared"),
            ("emergency_cabinet", "Gabinete de Emergencia Rojo", "Caja metálica de vidrio para romper")
        ],
        default="wall_bracket"
    )
    ext_glass_state: EnumProperty(
        name="Vidrio del Gabinete",
        items=[
            ("intact", "Vidrio Intacto", "Cristal protector sellado"),
            ("broken_shattered", "Vidrio Roto / Golpeado", "Cristal roto en emergencia"),
            ("door_open", "Puerta Abierta", "Gabinete abierto de par en par")
        ],
        default="intact"
    )
    ext_pressure_gauge: BoolProperty(name="Manómetro con Aguja", default=True)
    ext_hose_nozzle: BoolProperty(name="Manguera de Goma con Cono", default=True)
    ext_wall_sign: BoolProperty(name="Cartel Indicador Mural Superior", default=True)

    # --- VARIANTES DE VENT GRATE ---
    vent_width: FloatProperty(name="Ancho Rejilla (m)", default=0.60, min=0.3, max=1.5)
    vent_height: FloatProperty(name="Alto Rejilla (m)", default=0.60, min=0.3, max=1.5)
    vent_grate_type: EnumProperty(
        name="Diseño de Rejilla",
        items=[
            ("wall_louver", "Lamas Horizontales Inclinadas", "Rejilla de persiana estándar"),
            ("heavy_floor_grate", "Reja de Piso Transitable", "Parrilla gruesa para suelo"),
            ("perforated_mesh", "Malla Perforada", "Malla metálica de protección")
        ],
        default="wall_louver"
    )
    vent_grate_state: EnumProperty(
        name="Estado de Montaje",
        items=[
            ("bolted_intact", "Atornillada Firme", "4 bulones en las esquinas"),
            ("hanging_by_one_screw", "Colgando de un Tornillo", "Rejilla caída (ruta de escape)"),
            ("removed_open_duct", "Arrancada (Ducto Abierto)", "Acceso libre al conducto")
        ],
        default="bolted_intact"
    )
    vent_hanging_angle: FloatProperty(name="Ángulo de Caída", default=28.0, min=5.0, max=60.0)
    vent_has_fan: BoolProperty(name="Aspas de Ventilador Interior", default=True)
    vent_fan_blades: IntProperty(name="Cantidad de Aspas", default=4, min=3, max=6)

    # --- VARIANTES DE CABLE BUNDLE ---
    cable_bundle_length: FloatProperty(name="Largo del Mazo (m)", default=2.0, min=0.8, max=5.0)
    cable_bundle_type: EnumProperty(
        name="Disposición de Cables",
        items=[
            ("hanging_umbilical", "Catenaria Colgante Libre", "Mazo de cables con comba por gravedad"),
            ("ladder_rack_tray", "Bandeja Pasacables Tipo Escalera", "Bandeja metálica con peldaños"),
            ("vertical_riser", "Tronal Vertical Mural", "Bajada vertical con abrazaderas")
        ],
        default="hanging_umbilical"
    )
    cable_bundle_count: IntProperty(name="Cantidad de Cables", default=4, min=2, max=6)
    cable_bundle_sag: FloatProperty(name="Comba / Caída (m)", default=0.28, min=0.02, max=0.8)
    cable_severed_wire: BoolProperty(name="Cable Cortado / Peligro", default=False)
    cable_support_ties: BoolProperty(name="Abrazaderas / Zunchos de Sujeción", default=True)
    cable_junction_box: BoolProperty(name="Cajas de Derivación Terminales", default=True)

    # --- VARIANTES DE ELECTRICAL PANEL ---
    panel_width: FloatProperty(name="Ancho Panel (m)", default=0.70, min=0.35, max=1.6)
    panel_height: FloatProperty(name="Alto Panel (m)", default=0.90, min=0.40, max=2.0)
    panel_depth: FloatProperty(name="Profundidad Panel (m)", default=0.22, min=0.10, max=0.6)
    button_rows: IntProperty(name="Filas de Botones", default=2, min=1, max=4)
    button_cols: IntProperty(name="Columnas de Botones", default=3, min=1, max=5)
    switch_count: IntProperty(name="Interruptores Palanca", default=2, min=0, max=6)
    indicator_count: IntProperty(name="Luces Indicadoras LED", default=3, min=0, max=8)
    cable_count: IntProperty(name="Cables Colgantes", default=2, min=0, max=6)
    has_crt: BoolProperty(name="Pantalla CRT", default=True)
    has_knife_switch: BoolProperty(name="Interruptor de Cuchilla Alta Tensión", default=False)
    door_ajar: BoolProperty(name="Puerta de Mantenimiento Abierta", default=False)
    door_open_angle: FloatProperty(name="Ángulo Apertura Puerta", default=35.0, min=5.0, max=90.0)
    has_digital_readout: BoolProperty(name="Display Digital LED", default=True)
    panel_phosphor: EnumProperty(
        name="Color Fósforo CRT",
        items=[("green", "Verde Fósforo", "CRT verde"), ("amber", "Ámbar Fósforo", "CRT ámbar")],
        default="green"
    )

    # --- VARIANTES DE TERMINAL ---
    terminal_width: FloatProperty(name="Ancho Terminal (m)", default=0.55, min=0.35, max=1.2)
    terminal_height: FloatProperty(name="Alto Terminal (m)", default=0.65, min=0.40, max=1.5)
    terminal_depth: FloatProperty(name="Profundidad (m)", default=0.35, min=0.20, max=0.8)
    terminal_type: EnumProperty(
        name="Montaje Terminal",
        items=[
            ("wall", "Mural (Pared)", "Montado en la pared con biseles"),
            ("desktop", "Escritorio / Mesa", "Consola para mesa con patas de goma"),
            ("pedestal", "Pedestal / Columna", "Montado sobre poste o columna de pie")
        ],
        default="wall"
    )
    terminal_state: EnumProperty(
        name="Estado del Terminal",
        items=[
            ("active", "Activo / Normal", "Pantalla encendida y LEDs verdes"),
            ("alarm", "Alarma / Emergencia", "Pantalla roja y LEDs de alarma"),
            ("damaged", "Dañado / Con Fallas", "Pantalla rota/parpadeante y cables sueltos"),
            ("powered_off", "Apagado", "Pantalla negra sin corriente")
        ],
        default="active"
    )
    keyboard_style: EnumProperty(
        name="Estilo Teclado",
        items=[
            ("integrated", "Integrado", "Teclado completo en ángulo"),
            ("tray_projecting", "Bandeja Saliente", "Bandeja de teclado extendida"),
            ("keypad_numeric", "Teclado Numérico", "Solo teclado numérico compacto"),
            ("none", "Sin Teclado", "Panel frontal liso")
        ],
        default="integrated"
    )
    terminal_cables: IntProperty(name="Cables Colgantes", default=2, min=0, max=4)

    # --- VARIANTES DE OXYPOD ---
    oxypod_type: EnumProperty(
        name="Tipo de Oxypod",
        items=[
            ("wall_station", "Estación de Pared", "Estación fija de recarga de oxígeno"),
            ("portable_canister", "Tanque Portátil", "Cilindro con manija de transporte"),
            ("dual_tank_rig", "Batería Doble Tanque", "Doble cilindro de alta capacidad")
        ],
        default="wall_station"
    )
    oxygen_level: FloatProperty(
        name="Nivel de Oxígeno",
        description="Nivel del fluido brillante (Cian si > 40%, amarillo si medio, rojo si vacío)",
        default=0.85,
        min=0.0,
        max=1.0
    )
    has_mask_dock: BoolProperty(name="Puerto de Mascarilla", default=True)
    has_coiled_hose: BoolProperty(name="Manguera Colgante", default=True)

    # --- VARIANTES DE PUERTA ---
    door_width: FloatProperty(name="Ancho Marco (m)", default=2.0, min=1.0, max=3.5)
    door_height: FloatProperty(name="Alto Marco (m)", default=2.4, min=1.8, max=3.5)
    door_type: EnumProperty(
        name="Tipo de Puerta",
        items=[
            ("standard_sliding", "Estándar Automática", "Puerta corredera de estación"),
            ("heavy_airlock", "Airlock / Esclusa", "Mamparo pesado con franjas de advertencia"),
            ("emergency_bulkhead", "Mamparo de Emergencia", "Puerta roja con señalización de cierre"),
            ("manual_hatch", "Escotilla Manual", "Puerta con volante circular")
        ],
        default="standard_sliding"
    )
    door_open_ratio: FloatProperty(
        name="Apertura / Atasco",
        description="0.0 = Cerrada, 0.15 = Atascada/Entreabierta (Survival Horror), 1.0 = Abierta",
        default=0.0,
        min=0.0,
        max=1.0
    )
    has_reinforced_window: BoolProperty(name="Mirilla de Vidrio Blindado", default=True)
    has_hydraulic_pistons: BoolProperty(name="Pistones Hidráulicos", default=True)

    # --- VARIANTES DE SERVER RACK ---
    rack_type: EnumProperty(
        name="Tipo de Servidor",
        items=[
            ("consciousness_bank", "Banco de Conciencias", "Bahías de memoria con cartuchos brillantes"),
            ("telemetry_server", "Servidor de Telemetría", "Servidores de datos generales"),
            ("cryo_cooling_rack", "Rack con Criogenia", "Con serpentines de refrigeración líquida")
        ],
        default="consciousness_bank"
    )
    cartridge_occupancy: FloatProperty(
        name="Densidad de Cartuchos",
        description="Porcentaje de bahías ocupadas por cartuchos de conciencia",
        default=0.80,
        min=0.0,
        max=1.0
    )
    has_service_terminal: BoolProperty(name="Terminal 1U Retráctil", default=True)

    # --- VARIANTES DE CRATE / CONTENEDOR ---
    crate_type: EnumProperty(
        name="Tipo de Contenedor",
        items=[
            ("cargo_chest", "Caja de Carga", "Cofre apilable con esquineros reforzados"),
            ("chemical_drum", "Tambor Químico", "Barril cilíndrico de materiales peligrosos"),
            ("battery_cell", "Batería Industrial", "Célula de energía con bornes de alta tensión"),
            ("medical_crate", "Botiquín Médico", "Caja de emergencias médicas con cruz roja")
        ],
        default="cargo_chest"
    )
    crate_lid: EnumProperty(
        name="Estado de Tapa",
        items=[("closed", "Sellada / Cerrada", ""), ("ajar_open", "Entreabierta (Saqueada)", "")],
        default="closed"
    )

    # --- VARIANTES DE LOCKER ---
    locker_cols: IntProperty(name="Columnas de Taquillas", default=2, min=1, max=4)
    locker_door_state: EnumProperty(
        name="Estado Puertas",
        items=[("all_closed", "Todas Cerradas", ""), ("one_open", "Una Abierta (Interior Visible)", "")],
        default="all_closed"
    )
    has_integrated_bench: BoolProperty(name="Banco de Vestuario Integrado", default=True)

    # --- VARIANTES DE PIPES ---
    pipe_type: EnumProperty(
        name="Diseño de Tubería",
        items=[
            ("valve_assembly", "Con Válvula y Manómetro", "Tramo con válvula central"),
            ("straight", "Tramo Recto", "Tubería recta con bridas de acople"),
            ("elbow_90", "Codo de 90 Grados", "Giro en ángulo recto para esquinas"),
            ("t_junction", "Unión en T (Bifurcación)", "Bifurcación perpendicular")
        ],
        default="valve_assembly"
    )
    pipe_valve: EnumProperty(
        name="Tipo de Válvula",
        items=[
            ("handwheel_red", "Volante Circular Rojo", "Válvula de rueda manual"),
            ("lever_quarter_turn", "Palanca Cuarto de Vuelta", "Palanca rápida de paso"),
            ("none", "Sin Válvula", "Solo tubería")
        ],
        default="handwheel_red"
    )
    has_insulation_layer: BoolProperty(name="Aislamiento Térmico", default=False)

    # --- VARIANTES DE CREW BED ---
    bed_type: EnumProperty(
        name="Tipo de Cama",
        items=[
            ("crew_cot", "Catre de Tripulación", "Cama industrial estándar con patas tubulares"),
            ("medical_gurney", "Camilla de Enfermería", "Camilla clínica con ruedas y cabecero reclinable"),
            ("enclosed_pod", "Cápsula de Descanso", "Cama en nicho cerrado con mamparos protectores")
        ],
        default="crew_cot"
    )
    bed_width: FloatProperty(name="Ancho Cama", default=1.00, min=0.6, max=2.0)
    bed_length: FloatProperty(name="Largo Cama", default=2.05, min=1.5, max=2.5)
    bed_height: FloatProperty(name="Alto Cama", default=0.65, min=0.3, max=1.2)
    bed_mattress_state: EnumProperty(
        name="Estado del Colchón",
        items=[
            ("made_clean", "Tendido / Impecable", "Cama tendida de tripulación"),
            ("rumpled_disheveled", "Revuelto / Arrugado", "Sábanas revueltas tras huida repentina"),
            ("bare_foam_stained", "Espuma Manchada", "Sin sábanas con manchas de fluidos")
        ],
        default="made_clean"
    )
    bed_has_pillow: BoolProperty(name="Almohada", default=True)
    bed_has_under_drawers: BoolProperty(name="Cajoneras Inferiores", default=True)
    bed_has_guardrails: BoolProperty(name="Barandillas de Contención", default=False)
    bed_headrest_incline: FloatProperty(name="Inclinación Cabecero", default=0.0, min=0.0, max=35.0)
    bed_blanket_color: EnumProperty(
        name="Color Manta",
        items=[
            ("station_gray", "Gris Estación", "Lana gris estándar"),
            ("medical_blue", "Azul Sanitario", "Tejido esterilizado de enfermería"),
            ("emergency_orange", "Naranja Emergencia", "Lona térmica de rescate"),
            ("brown_wool", "Marrón Térmico", "Manta gruesa de abrigo")
        ],
        default="station_gray"
    )

    # --- VARIANTES DE BUNK BED ---
    bunk_frame: EnumProperty(
        name="Estructura Litera",
        items=[
            ("tubular_metal", "Metal Tubular Soldado", "Estructura ligera de acero con remaches"),
            ("reinforced_bulkhead", "Mamparo Integrado", "Montada fija a la pared de la nave"),
            ("capsule_stacked", "Cápsulas Apiladas", "Literas modulares estilo colmena espacial")
        ],
        default="tubular_metal"
    )
    bunk_width: FloatProperty(name="Ancho Litera", default=1.05, min=0.7, max=1.8)
    bunk_length: FloatProperty(name="Largo Litera", default=2.05, min=1.5, max=2.5)
    bunk_height: FloatProperty(name="Alto Total", default=2.05, min=1.5, max=2.6)
    bunk_ladder_pos: EnumProperty(
        name="Posición Escalera",
        items=[
            ("front_right", "Frontal Derecha", "Escalera frontal a la derecha"),
            ("front_left", "Frontal Izquierda", "Escalera frontal a la izquierda"),
            ("side_head", "Lateral Cabecero", "Peldaños en el extremo del cabecero")
        ],
        default="front_right"
    )
    bunk_upper_guardrail: BoolProperty(name="Barandilla Superior", default=True)
    bunk_lower_state: EnumProperty(
        name="Cama Inferior",
        items=[
            ("made", "Tendida", "Cama tendida"),
            ("disheveled", "Revuelta", "Desordenada"),
            ("bare_foam_stained", "Espuma Manchada", "Manchas de óxido o fluidos")
        ],
        default="made"
    )
    bunk_upper_state: EnumProperty(
        name="Cama Superior",
        items=[
            ("made", "Tendida", "Cama tendida"),
            ("disheveled", "Revuelta", "Desordenada"),
            ("bare_foam_stained", "Espuma Manchada", "Manchas de óxido"),
            ("empty_storage", "Depósito Cajas", "Usada para almacenar suministros")
        ],
        default="made"
    )
    bunk_has_reading_lights: BoolProperty(name="Luces LED de Lectura", default=True)
    bunk_has_lockers: BoolProperty(name="Baúles / Taquillas Inferiores", default=True)
    bunk_has_curtains: BoolProperty(name="Cortinas de Privacidad", default=False)
    bunk_blanket_color: EnumProperty(
        name="Color Manta",
        items=[
            ("station_gray", "Gris Estación", "Gris utilitario"),
            ("medical_blue", "Azul Sanitario", "Azul clínico"),
            ("emergency_orange", "Naranja Emergencia", "Alta visibilidad"),
            ("brown_wool", "Marrón Lana", "Marrón pesado")
        ],
        default="station_gray"
    )

    # --- VARIANTES DE NIGHTSTAND ---
    nightstand_type: EnumProperty(
        name="Tipo de Mesa de Luz",
        items=[
            ("crew_locker_cubby", "Mueble Cubículo Tripulante", "Mesa baja compacta con estante abierto y cajón"),
            ("sliding_drawers", "Cajonera Metálica", "Mueble con múltiples cajones deslizables"),
            ("medical_tray_cart", "Carrito Clínico Auxiliar", "Mesa auxiliar con ruedas para instrumental"),
            ("wall_mounted", "Repisa Mural Flotante", "Fijada directamente al mamparo")
        ],
        default="crew_locker_cubby"
    )
    nightstand_width: FloatProperty(name="Ancho Mesa", default=0.48, min=0.3, max=0.9)
    nightstand_depth: FloatProperty(name="Profundidad Mesa", default=0.44, min=0.3, max=0.8)
    nightstand_height: FloatProperty(name="Altura Mesa", default=0.68, min=0.4, max=1.2)
    nightstand_drawers: IntProperty(name="Cantidad Cajones", default=2, min=1, max=3)
    nightstand_drawer_open: FloatProperty(name="Apertura Cajón", default=0.0, min=0.0, max=0.5)
    nightstand_raised_rim: BoolProperty(name="Reborde Antideslizante", default=True)
    nightstand_has_lamp: BoolProperty(name="Lámpara de Lectura", default=True)
    nightstand_lamp_state: EnumProperty(
        name="Estado Luz Lámpara",
        items=[("on", "Encendida", ""), ("off", "Apagada", ""), ("flickering", "Parpadeante", "")],
        default="on"
    )
    nightstand_swivel_tray: BoolProperty(name="Bandeja Articulada / Giratoria", default=False)

    # --- VARIANTES DE RADIATOR HEATER ---
    heater_type: EnumProperty(
        name="Tipo de Calefactor",
        items=[
            ("wall_radiator_fins", "Radiador Mural de Aletas", "Cuerpo clásico de fundición con aletas térmicas"),
            ("convector_blower", "Gabinete Termoconvector", "Turbina de aire caliente con rejillas frontales"),
            ("space_tower_heater", "Torre Térmica Vertical", "Torre cilíndrica con bobinas incandescentes")
        ],
        default="wall_radiator_fins"
    )
    heater_width: FloatProperty(name="Ancho Calefactor", default=0.85, min=0.4, max=2.0)
    heater_height: FloatProperty(name="Alto Calefactor", default=0.70, min=0.3, max=1.8)
    heater_depth: FloatProperty(name="Prof. Calefactor", default=0.22, min=0.1, max=0.6)
    heater_fin_count: IntProperty(name="Cantidad de Aletas", default=8, min=4, max=14)
    heater_is_operational: BoolProperty(name="En Funcionamiento (Resplandor)", default=True)
    heater_thermostat: BoolProperty(name="Dial Termostato", default=True)
    heater_steam_pipe: BoolProperty(name="Tubería con Volante de Paso", default=True)
    heater_damage: EnumProperty(
        name="Estado de Daño",
        items=[
            ("intact", "Operativo / Íntegro", "Funcionando normalmente"),
            ("battered_bent_fins", "Golpeado / Aletas Dobladas", "Aletas térmicas deformadas por impacto"),
            ("leaking_burst", "Fuga / Fisura de Vapor", "Tubería reventada con manchas de óxido hirviente")
        ],
        default="intact"
    )

    # --- VARIANTES DE OFFICE DOOR ---
    office_door_style: EnumProperty(
        name="Estilo de Puerta",
        items=[
            ("single_swing", "Batiente Simple (1 Hoja)", "Puerta de despacho o laboratorio de un panel"),
            ("double_swing", "Batiente Doble (2 Hojas)", "Acceso ancho para salas de reunión o clínica"),
            ("sliding_pocket", "Corredera Empotrada", "Puerta corredera acristalada dentro del marco")
        ],
        default="single_swing"
    )
    office_glass_type: EnumProperty(
        name="Tipo de Cristal",
        items=[
            ("wired_safety_glass", "Vidrio Armado con Malla", "Cristal de seguridad con rejilla de alambre embebida"),
            ("clear_tinted", "Cristal Ahumado Tintado", "Vidrio con filtro verdoso de radiación"),
            ("frosted_privacy", "Vidrio Esmerilado Opaco", "Cristal traslúcido para privacidad de oficinas")
        ],
        default="wired_safety_glass"
    )
    office_door_width: FloatProperty(name="Ancho Marco", default=1.20, min=0.8, max=3.0)
    office_door_height: FloatProperty(name="Alto Marco", default=2.40, min=1.8, max=3.2)
    office_door_depth: FloatProperty(name="Espesor Marco", default=0.22, min=0.1, max=0.5)
    office_open_angle: FloatProperty(name="Ángulo Apertura (Grados)", default=0.0, min=0.0, max=90.0)
    office_glass_damage: EnumProperty(
        name="Daño en el Cristal",
        items=[
            ("intact", "Vidrio Íntegro", "Sin fracturas"),
            ("cracked_spiderweb", "Fisurado en Telaraña", "Fisuras radiales por impacto o bala"),
            ("shattered_missing", "Destrozado / Hueco Roto", "Panel partido con fragmentos faltantes")
        ],
        default="intact"
    )
    office_handle_type: EnumProperty(
        name="Tipo de Manija",
        items=[
            ("horizontal_push_bar", "Barra Antipánico Horizontal", "Barra de empuje de emergencia"),
            ("industrial_lever", "Manivela Metálica de Palanca", "Picaporte industrial acodado"),
            ("recessed_pull", "Tirador Embutido", "Cazoleta empotrada para correderas")
        ],
        default="horizontal_push_bar"
    )
    office_kickplate: BoolProperty(name="Placa de Choque Inferior (Kickplate)", default=True)
    office_transom: BoolProperty(name="Ventana Superior (Tragaluz/Transom)", default=False)

    # --- 20 NUEVAS FAMILIAS DE MOBILIARIO Y SUPERVIVENCIA ---
    # 1. Autopsy Table
    autopsy_type: EnumProperty(
        name="Tipo de Mesa",
        items=[
            ("standard_autopsy", "Mesa de Autopsia Estándar", "Mesa tubular de acero inoxidable con desagüe"),
            ("dissection_station", "Estación de Disección", "Mesa con canales perimetrales profundos"),
            ("quarantine_slab", "Losa de Cuarentena", "Monolito pesado de contención biológica")
        ],
        default="standard_autopsy"
    )
    autopsy_straps: EnumProperty(
        name="Correas de Sujeción",
        items=[
            ("none", "Sin Correas", "Losa despejada"),
            ("buckled", "Correas Abrochadas", "Correas de cuero abrochadas sobre la losa"),
            ("torn", "Correas Desgarradas", "Correas cortadas o rotas violentamente")
        ],
        default="none"
    )
    autopsy_drain: BoolProperty(name="Canaleta y Sumidero de Drenaje", default=True)
    autopsy_lamp: BoolProperty(name="Foco Quirúrgico Articulado", default=True)
    autopsy_tray: BoolProperty(name="Bandeja de Instrumental y Sierra", default=False)
    autopsy_jars: IntProperty(name="Frascos de Especímenes", default=0, min=0, max=3)

    # 2. Medical Screen
    screen_type: EnumProperty(
        name="Tipo de Biombo",
        items=[
            ("three_panel", "Biombo de 3 Paneles", "Biombo plegable triple"),
            ("four_panel", "Biombo de 4 Paneles", "Biombo largo cuádruple"),
            ("single_partition", "Panel Divisor Simple", "Partición única sobre ruedas")
        ],
        default="three_panel"
    )
    screen_panels: IntProperty(name="Cantidad de Paneles", default=3, min=1, max=4)
    screen_fold_angle: FloatProperty(name="Ángulo de Pliegue (Grados)", default=30.0, min=0.0, max=60.0)
    screen_damage: EnumProperty(
        name="Estado de Cortina",
        items=[
            ("intact", "Vinilo Íntegro", "Cortina plástica limpia"),
            ("torn_hanging", "Vinilo Rasgado", "Cortina desgarrada colgando"),
            ("blood_splatter", "Salpicaduras de Sangre", "Manchas hemáticas visibles")
        ],
        default="intact"
    )

    # 3. Morgue Gurney
    gurney_type: EnumProperty(
        name="Estado de Camilla",
        items=[
            ("tray_open", "Bandeja Abierta Despejada", "Bandeja metálica limpia"),
            ("body_bag_closed", "Bolsa Mortuoria Cerrada", "Bolsa de vinilo negro con cremallera"),
            ("body_bag_ajar", "Bolsa Entreabierta", "Cremallera descorrida mostrando silueta")
        ],
        default="tray_open"
    )
    gurney_scissor: BoolProperty(name="Elevador Tijera en X", default=True)
    gurney_handles: BoolProperty(name="Barras de Empuje", default=True)

    # 4. Chemical Cabinet
    chem_cabinet_type: EnumProperty(
        name="Tipo de Armario",
        items=[
            ("tall_two_door", "Armario Alto de 2 Puertas", "Gabinete vertical de laboratorio"),
            ("low_counter_top", "Mostrador Bajo de Reactivos", "Módulo de sobremesa"),
            ("wall_hanging", "Módulo Mural de Pared", "Armario suspendido")
        ],
        default="tall_two_door"
    )
    chem_glass_type: EnumProperty(
        name="Cristal de Puertas",
        items=[
            ("wired_mesh", "Vidrio con Malla de Alambre", "Seguridad industrial reforzada"),
            ("frosted_hazard", "Vidrio Esmerilado Opaco", "Privacidad para muestras peligrosas"),
            ("missing_broken", "Vidrio Roto y Astillado", "Cristal quebrado con fragmentos en suelo")
        ],
        default="wired_mesh"
    )
    chem_door_state: EnumProperty(
        name="Apertura de Puertas",
        items=[
            ("both_closed", "Ambas Cerradas", "Puertas cerradas"),
            ("left_open", "Puerta Izquierda Abierta", "Puerta batiente abierta a 75 grados"),
            ("right_ajar", "Puerta Derecha Entreabierta", "Puerta ligeramente descuadrada")
        ],
        default="both_closed"
    )
    chem_padlock: BoolProperty(name="Aldaba con Candado", default=True)
    chem_clutter: FloatProperty(name="Densidad de Frascos", default=0.70, min=0.0, max=1.0)

    # 5. Restraint Chair
    restraint_chair_type: EnumProperty(
        name="Tipo de Asiento",
        items=[
            ("bolted_steel_chair", "Silla de Acero Apernada", "Silla metálica fijada al piso"),
            ("interrogation_throne", "Trono de Interrogatorio", "Silla pesada de seguridad"),
            ("detox_seat", "Asiento de Desintoxicación", "Módulo de enfermería psiquiátrica")
        ],
        default="bolted_steel_chair"
    )
    restraint_straps: EnumProperty(
        name="Correas de Brazos",
        items=[
            ("buckled", "Abrochadas", "Correas de cuero tensadas"),
            ("loose", "Sueltas", "Correas colgando"),
            ("torn", "Desgarradas", "Correas violentamente rotas")
        ],
        default="buckled"
    )
    restraint_shackles: BoolProperty(name="Grilletes de Tobillo", default=True)
    restraint_iv_pole: BoolProperty(name="Soporte de Suero IV", default=True)

    # 6. Mess Table
    mess_table_type: EnumProperty(
        name="Estilo de Mesa",
        items=[
            ("bolted_stools_4", "4 Taburetes Anclados", "Mesa comunal de 4 plazas"),
            ("bolted_stools_6", "6 Taburetes Anclados", "Mesa larga de 6 plazas"),
            ("free_standing_bench", "Bancos Corridos", "Mesa con bancos laterales")
        ],
        default="bolted_stools_4"
    )
    mess_stools: IntProperty(name="Cantidad de Taburetes", default=4, min=2, max=6)
    mess_stool_state: EnumProperty(
        name="Disposición de Taburetes",
        items=[
            ("all_tucked", "Todos Recogidos", "Taburetes alineados bajo la mesa"),
            ("random_pulled", "Desorden Habitual", "Algunos taburetes girados hacia afuera"),
            ("scattered", "Caos de Evacuación", "Taburetes desplazados al máximo")
        ],
        default="random_pulled"
    )
    mess_trays: BoolProperty(name="Bandejas de Raciones Abandonadas", default=True)

    # 7. Ration Automat
    automat_type: EnumProperty(
        name="Tipo de Dispensador",
        items=[
            ("nutrient_paste", "Tubos de Pasta Nutritiva", "Dispensador estándar de raciones"),
            ("synthetic_cigarettes", "Filtros y Estimulantes", "Expendedora de suministros médicos"),
            ("hot_caffeine", "Infusor de Cafeína Líquida", "Dispensador de bebidas calientes")
        ],
        default="nutrient_paste"
    )
    automat_dispenser_state: EnumProperty(
        name="Estado de Compuerta",
        items=[
            ("normal", "Operativo / Cerrado", "Compuerta de recogida cerrada"),
            ("jammed_door", "Compuerta Atascada", "Trampilla entreabierta con paquete trabado"),
            ("smashed_glass", "Display Siniestrado", "Frontal quebrado y saqueado")
        ],
        default="normal"
    )
    automat_display_color: EnumProperty(
        name="Fósforo de Pantalla",
        items=[
            ("amber", "Ámbar Industrial", "Fósforo naranja retro"),
            ("green", "Verde CRT", "Monocromo clásico"),
            ("dim_red", "Rojo Emergencia", "Alerta de racionamiento crítico")
        ],
        default="amber"
    )

    # 8. Canteen Counter
    counter_type: EnumProperty(
        name="Configuración Mostrador",
        items=[
            ("straight_pass", "Pasa-platos Lineal", "Módulo recto de cocina"),
            ("corner_l_counter", "Mostrador en L", "Esquina de cantina"),
            ("island_buffet", "Isla Central", "Buffet de autoservicio")
        ],
        default="straight_pass"
    )
    counter_shutter: EnumProperty(
        name="Persiana Metálica",
        items=[
            ("open", "Abierta al 100%", "Acceso completo a cocina"),
            ("half_closed", "A Medio Bajar", "Persiana trabada a mitad de recorrido"),
            ("fully_shuttered", "Cerrada / Bloqueada", "Persiana blindada cerrada")
        ],
        default="open"
    )
    counter_sneeze_guard: BoolProperty(name="Mampara Sanitaria de Cristal", default=True)
    counter_tray_rails: BoolProperty(name="Rieles para Bandejas", default=True)

    # 9. File Cabinet
    file_cabinet_type: EnumProperty(
        name="Tipo de Archivador",
        items=[
            ("vertical_tower", "Torre Vertical", "Columna de 4 cajones"),
            ("lateral_wide", "Mueble Lateral Ancho", "Archivador apaisado"),
            ("fireproof_safe", "Archivador Blindado", "Caja fuerte para documentos clasificados")
        ],
        default="vertical_tower"
    )
    file_open_drawer: IntProperty(name="Cajón Abierto (-1 = ninguno)", default=1, min=-1, max=4)
    file_scattered: BoolProperty(name="Documentos Desparramados", default=True)

    # 10. Locker Bench
    locker_bench_type: EnumProperty(
        name="Estilo de Banco",
        items=[
            ("perforated_metal", "Chapa Perforada", "Acero antideslizante"),
            ("composite_slats", "Listones Sintéticos", "Brazos de composite"),
            ("boot_rack_integrated", "Con Soporte de Botas", "Estante inferior de alambre")
        ],
        default="perforated_metal"
    )
    locker_bench_gear: BoolProperty(name="Equipo / Botas Abandonadas", default=True)

    # 11. Work Bench
    work_bench_style: EnumProperty(
        name="Estilo de Banco",
        items=[
            ("heavy_maintenance", "Taller Pesado", "Tapa gruesa de acero"),
            ("electronics_soldering", "Mesa de Electrónica", "Mesa de soldadura y placas"),
            ("dirty_mechanic", "Mecánica Sucia", "Mesa con restos de aceite y motores")
        ],
        default="heavy_maintenance"
    )
    work_pegboard: BoolProperty(name="Panel Perforado de Herramientas", default=True)
    work_vise: BoolProperty(name="Tornillo de Banco / Prensa", default=True)
    work_luminaire: BoolProperty(name="Lámpara Fluorescente Superior", default=True)
    work_clutter: FloatProperty(name="Densidad de Herramientas", default=0.75, min=0.0, max=1.0)

    # 12. Heavy Shelving
    shelf_type: EnumProperty(
        name="Tipo de Carga",
        items=[
            ("cargo_storage", "Cajas de Suministros", "Contenedores de carga y embalajes"),
            ("chemical_drums_rack", "Bidones de Químicos", "Tambores cilíndricos sellados"),
            ("empty_looted", "Estantería Saqueada", "Estructura vacía y perfiles torcidos")
        ],
        default="cargo_storage"
    )
    shelf_levels: IntProperty(name="Niveles de Estante", default=4, min=3, max=5)
    shelf_x_bracing: BoolProperty(name="Riostras Traseras en X", default=True)
    shelf_bent_index: IntProperty(name="Estante Deformado (-1 = ninguno)", default=-1, min=-1, max=4)

    # 13. Tool Chest Cart
    tool_cart_style: EnumProperty(
        name="Estilo de Carro",
        items=[
            ("mobile_mechanic_cart", "Carro Taller Rodante", "Módulo de 5 cajoneras con tirador"),
            ("roll_cab_combo", "Cofre Combinado Doble", "Cofre superior e inferior"),
            ("low_service_trolley", "Carretilla Baja de Servicio", "Bandejas abiertas de servicio")
        ],
        default="mobile_mechanic_cart"
    )
    tool_open_style: EnumProperty(
        name="Apertura de Cajoneras",
        items=[
            ("all_closed", "Todos Cerrados", "Cajones guardados"),
            ("top_drawer_open", "Cajón Superior Abierto", "Primer cajón extendido con herramientas"),
            ("staggered", "Apertura Escalonada", "Varios cajones abiertos a distintas distancias")
        ],
        default="top_drawer_open"
    )
    tool_top_parts: BoolProperty(name="Piezas Sueltas en Bandeja Superior", default=True)

    # 14. Safety Shower
    shower_station_type: EnumProperty(
        name="Estación de Seguridad",
        items=[
            ("combination_shower_eyewash", "Ducha y Cuenco Lavaojos", "Estación completa de descontaminación"),
            ("eyewash_pedestal", "Pedestal Solo Lavaojos", "Lavaojos de laboratorio"),
            ("ceiling_drench", "Ducha Cenital de Mamparo", "Rociador empotrado en techo")
        ],
        default="combination_shower_eyewash"
    )
    shower_eyewash: BoolProperty(name="Cuenco Lavaojos", default=True)
    shower_pull_chain: BoolProperty(name="Cadena de Activación Rápida", default=True)
    shower_drain_grate: BoolProperty(name="Rejilla de Desagüe en Piso", default=True)

    # 15. Hydroponic Tray Bed
    hydro_bed_type: EnumProperty(
        name="Tipo de Bandeja",
        items=[
            ("single_tier", "Bandeja Simple de Piso", "Módulo botánico bajo"),
            ("stacked_dual_tier", "Bandeja Doble en Altura", "Dos niveles de cultivo superpuestos"),
            ("quarantine_specimen_tank", "Tanque de Especímenes", "Cámara de contención biológica")
        ],
        default="single_tier"
    )
    hydro_plant_state: EnumProperty(
        name="Estado de Flora",
        items=[
            ("healthy_green", "Cultivo Saludable", "Plantas verdes bajo luz ultravioleta"),
            ("withered_dead", "Vegetación Marchita", "Tallos secos y quebradizos"),
            ("mutated_spores", "Esporas Mutadas / Alienígenas", "Pústulas bioluminiscentes y zarcillos")
        ],
        default="healthy_green"
    )
    hydro_uv_light: EnumProperty(
        name="Iluminación UV",
        items=[
            ("on_violet", "UV Encendido (Violeta)", "Lámparas emitiendo luz ultravioleta"),
            ("flickering", "Parpadeo Inestable", "Balastro defectuoso con destellos"),
            ("off", "Apagado", "Sin luz artificial")
        ],
        default="on_violet"
    )

    # 16. Security Desk
    sec_desk_type: EnumProperty(
        name="Tipo de Puesto",
        items=[
            ("checkpoint_barrier", "Barrera de Checkpoint", "Control de acceso con cristal blindado"),
            ("intake_counter", "Mostrador de Admisión", "Recepción de personal"),
            ("airlock_terminal", "Puesto de Esclusa", "Puesto blindado de descompresión")
        ],
        default="checkpoint_barrier"
    )
    sec_bulletproof_glass: BoolProperty(name="Cristal Blindado Antibalas", default=True)
    sec_cctv_monitor: BoolProperty(name="Monitor de Circuito Cerrado (CCTV)", default=True)
    sec_intercom: BoolProperty(name="Rejilla de Intercomunicador", default=True)

    # 17. Weapons Rack
    weapons_rack_type: EnumProperty(
        name="Tipo de Armero",
        items=[
            ("long_guns_vertical", "Armas Largas Verticales", "Escopetas y rifles de asalto"),
            ("sidearm_cabinet", "Gabinete de Pistolas", "Cajas de armas cortas"),
            ("stun_batons", "Varas Antidisturbios", "Armamento disuasivo no letal")
        ],
        default="long_guns_vertical"
    )
    weapons_slots: IntProperty(name="Cantidad de Espacios", default=5, min=3, max=6)
    weapons_locked: BoolProperty(name="Barra de Cierre con Candado", default=True)
    weapons_occupancy: FloatProperty(name="Ocupación de Armas", default=0.60, min=0.0, max=1.0)

    # 18. Bridge Console Desk
    bridge_console_type: EnumProperty(
        name="Geometría de Consola",
        items=[
            ("horseshoe_arc", "Herradura Envolvente", "Consola curva semicircular"),
            ("straight_dual_tier", "Recta de Dos Niveles", "Bancada frontal de instrumentos"),
            ("corner_l_station", "Puesto en L", "Esquina de oficiales")
        ],
        default="horseshoe_arc"
    )
    bridge_screens: IntProperty(name="Monitores CRT", default=4, min=2, max=6)
    bridge_swivel_chair: BoolProperty(name="Asiento de Piloto Giratorio", default=True)
    bridge_throttles: BoolProperty(name="Cuadrante de Palancas de Empuje", default=True)

    # 19. Space Toilet
    toilet_type: EnumProperty(
        name="Tipo de Inodoro",
        items=[
            ("zero_g_cubicle", "Cubículo Zero-G", "Sanitario cerrado de acero"),
            ("open_bulkhead_latrine", "Letrina Abierta de Mamparo", "Inodoro básico de emergencia"),
            ("medical_specimen_toilet", "Sanitario de Muestras Médicas", "Retrete con analizador bioquímico")
        ],
        default="zero_g_cubicle"
    )
    toilet_clamps: BoolProperty(name="Abrazaderas de Muslos y Pies", default=True)
    toilet_suction_hose: BoolProperty(name="Manguera de Succión de Vacío", default=True)

    # 20. Scrub Sink
    scrub_sink_type: EnumProperty(
        name="Tipo de Lavabo",
        items=[
            ("single_bay", "Bacha Simple Profunda", "Lavabo quirúrgico individual"),
            ("dual_bay", "Bacha Doble de Cirugía", "Dos senos para cirujanos simultáneos"),
            ("pedestal_fountain", "Fuente de Lavado Vertical", "Módulo autónomo de pie")
        ],
        default="single_bay"
    )
    scrub_dispenser: BoolProperty(name="Dispensador de Jabón Antiséptico", default=True)
    scrub_mirror: BoolProperty(name="Espejo Antivaho", default=True)

    # Godot 4 Collision Mesh Option
    generate_collision_shape: BoolProperty(
        name="Generar Colisión Godot 4",
        description="Incluir automáticamente una forma de colisión optimizada para StaticBody3D en Godot 4",
        default=True
    )
    export_collision_type: EnumProperty(
        name="Tipo de Colisión",
        description="Geometría generada para colisión física",
        items=[
            ("box", "Caja Ajustada (Bounding Box)", "Caja mínima envolvente (12 triángulos, ultra-rápida)"),
            ("convex_hull", "Casco Convexo (Convex Hull)", "Envolvente convexa ajustada a la forma exacta de la malla")
        ],
        default="box"
    )
    export_collision_suffix: EnumProperty(
        name="Sufijo Godot",
        description="Convención de importación automática de Godot 4",
        items=[
            ("-convcolonly", "-convcolonly (ConvexPolygonShape3D)", "Crea StaticBody3D con colisión convexa y descarta la malla visual"),
            ("-colonly", "-colonly (ConcavePolygonShape3D)", "Crea StaticBody3D con colisión trimesh y descarta la malla visual"),
            ("-col", "-col (Malla Visual + Colisión)", "Conserva la malla visual y genera StaticBody3D")
        ],
        default="-convcolonly"
    )
    export_pivot_rule: EnumProperty(
        name="Regla de Pivote",
        description="Normalización del origen / pivote del asset para colocación diegética",
        items=[
            ("floor_center", "Suelo / Contacto (Z = 0)", "Pivote en la base del asset, centrado en X/Y (muebles y props de suelo)"),
            ("wall_back", "Pared / Espaldar (Y = 0)", "Pivote en la superficie de montaje mural (paneles, rejillas, extintores)"),
            ("center", "Centro Geométrico (0, 0, 0)", "Pivote en el centro de masa del objeto"),
            ("keep", "Sin Modificar (Tal cual)", "Mantiene el origen original de modelado")
        ],
        default="floor_center"
    )
    export_validate_godot: BoolProperty(
        name="Validar en Godot 4",
        description="Ejecutar motor Godot en modo headless para certificar la importación y materiales",
        default=True
    )

    last_tri_count: IntProperty(name="Triángulos", default=0)
    last_status: StringProperty(name="Estado", default="Listo para generar")

def _build_config_internal(settings):
    fam = settings.asset_family
    s = settings.scale_factor
    name = settings.asset_name if settings.asset_name != "asset_psx" else f"{fam}_{settings.seed}"

    if fam == "station_corridor":
        return StationCorridorConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            corridor_type=settings.corridor_type,
            width=settings.corridor_width * s,
            length=settings.corridor_length * s,
            height=settings.corridor_height * s,
            floor_style=settings.corridor_floor_style,
            wall_style=settings.corridor_wall_style,
            ceiling_style=settings.corridor_ceiling_style,
            has_integrated_lighting=settings.corridor_lighting,
            lighting_state=settings.corridor_light_state,
            has_cable_runs=settings.corridor_cable_runs,
            has_wall_alcove=settings.corridor_wall_alcove,
            has_hazard_stripes=settings.corridor_hazard_stripes,
            damage_state=settings.corridor_damage
        )
    elif fam == "station_room":
        return StationRoomConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            room_archetype=settings.room_archetype,
            width=settings.room_width * s,
            depth=settings.room_depth * s,
            height=settings.room_height * s,
            door_north=settings.room_door_north,
            door_south=settings.room_door_south,
            door_east=settings.room_door_east,
            door_west=settings.room_door_west,
            pillar_layout=settings.room_pillar_layout,
            floor_elevation=settings.room_elevation,
            has_observation_window=settings.room_observation_window,
            has_overhead_gantry=settings.room_overhead_gantry,
            has_floor_drain=settings.room_floor_drain,
            lighting_color=settings.room_lighting_color
        )
    elif fam == "crash_cart":
        return CrashCartConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            width=settings.cart_width * s,
            height=settings.cart_height * s,
            depth=settings.cart_depth * s,
            drawer_count=settings.cart_drawers,
            drawer_open_mode=settings.cart_drawer_mode,
            drawer_slide_max=settings.cart_slide_max * s,
            drawer_handle_style=settings.cart_handle_style,
            has_top_monitor=settings.has_top_monitor,
            monitor_phosphor_color=settings.cart_monitor_phosphor,
            has_push_handle=settings.has_push_handle,
            push_handle_side=settings.push_handle_side,
            has_oxygen_rack=settings.has_oxygen_rack,
            oxygen_tank_count=settings.oxygen_tank_count,
            body_color_preset=settings.body_color_preset
        )
    elif fam == "office_desk":
        return OfficeDeskConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            width=settings.desk_width * s,
            height=settings.desk_height * s,
            depth=settings.desk_depth * s,
            leg_style=settings.desk_leg_style,
            pedestal_layout=settings.desk_pedestals,
            drawer_count_per_pedestal=settings.desk_drawers,
            drawer_open_style=settings.desk_drawer_style,
            has_cable_grommet=settings.desk_cable_grommet,
            has_partition_screen=settings.desk_partition,
            has_under_shelf=settings.desk_under_shelf,
            surface_material=settings.desk_surface_material
        )
    elif fam == "office_chair":
        return OfficeChairConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            seat_width=settings.chair_seat_width * s,
            seat_depth=settings.chair_seat_depth * s,
            seat_height=settings.chair_seat_height * s,
            backrest_style=settings.chair_backrest_style,
            backrest_tilt=settings.chair_backrest_tilt,
            base_style=settings.chair_base_style,
            spoke_count=settings.chair_spokes,
            armrest_style=settings.chair_armrests,
            upholstery_color=settings.chair_upholstery
        )
    elif fam == "sign_placard":
        return SignPlacardConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            width=settings.sign_width * s,
            height=settings.sign_height * s,
            mount_type=settings.sign_mount,
            sign_type=settings.sign_type,
            damage_style=settings.sign_damage,
            hanging_chain_length=settings.sign_chain_len * s
        )
    elif fam == "trash_bin":
        return TrashBinConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            height=settings.trash_height * s,
            radius=settings.trash_radius * s,
            is_rectangular=settings.trash_is_rectangular,
            bin_type=settings.trash_bin_type,
            lid_state=settings.trash_lid_state,
            has_foot_pedal=settings.trash_foot_pedal,
            has_overflowing_trash=settings.trash_overflowing
        )
    elif fam == "light_fixture":
        return LightFixtureConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            fixture_type=settings.light_type,
            length=settings.light_length * s,
            width=settings.light_width * s,
            depth=settings.light_depth * s,
            tube_count=settings.light_tubes,
            lighting_state=settings.light_state,
            has_wire_guard=settings.light_wire_guard,
            has_dangling_wire=settings.light_dangling_wire
        )
    elif fam == "fire_extinguisher":
        return FireExtinguisherConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            tank_radius=settings.ext_tank_radius * s,
            tank_height=settings.ext_tank_height * s,
            mount_style=settings.ext_mount_style,
            cabinet_glass_state=settings.ext_glass_state,
            has_pressure_gauge=settings.ext_pressure_gauge,
            has_hose_nozzle=settings.ext_hose_nozzle,
            has_wall_sign=settings.ext_wall_sign
        )
    elif fam == "vent_grate":
        return VentGrateConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            width=settings.vent_width * s,
            height=settings.vent_height * s,
            grate_type=settings.vent_grate_type,
            grate_state=settings.vent_grate_state,
            hanging_angle=settings.vent_hanging_angle,
            has_fan_blades=settings.vent_has_fan,
            fan_blade_count=settings.vent_fan_blades
        )
    elif fam == "cable_bundle":
        return CableBundleConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            length=settings.cable_bundle_length * s,
            bundle_type=settings.cable_bundle_type,
            cable_count=settings.cable_bundle_count,
            max_sag=settings.cable_bundle_sag * s,
            has_severed_wire=settings.cable_severed_wire,
            has_support_ties=settings.cable_support_ties,
            has_junction_box=settings.cable_junction_box
        )
    elif fam == "electrical_panel":
        return ElectricalPanelConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            width=settings.panel_width * s,
            height=settings.panel_height * s,
            depth=settings.panel_depth * s,
            button_rows=settings.button_rows,
            button_cols=settings.button_cols,
            switch_count=settings.switch_count,
            indicator_count=settings.indicator_count,
            cable_count=settings.cable_count,
            has_crt=settings.has_crt,
            crt_phosphor_color=settings.panel_phosphor,
            has_knife_switch=settings.has_knife_switch,
            door_ajar=settings.door_ajar,
            door_open_angle=settings.door_open_angle,
            has_digital_readout=settings.has_digital_readout
        )
    elif fam == "terminal":
        return TerminalConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            terminal_type=settings.terminal_type,
            state=settings.terminal_state,
            keyboard_style=settings.keyboard_style,
            width=settings.terminal_width * s,
            height=settings.terminal_height * s,
            depth=settings.terminal_depth * s,
            phosphor_color=settings.panel_phosphor,
            cable_count=settings.terminal_cables
        )
    elif fam == "oxypod":
        return OxypodConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            station_type=settings.oxypod_type,
            oxygen_level=settings.oxygen_level,
            has_mask_dock=settings.has_mask_dock,
            has_coiled_hose=settings.has_coiled_hose,
            tank_height=0.95 * s,
            tank_radius=0.18 * s
        )
    elif fam == "door":
        return DoorConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            door_type=settings.door_type,
            open_ratio=settings.door_open_ratio,
            has_reinforced_window=settings.has_reinforced_window,
            has_hydraulic_pistons=settings.has_hydraulic_pistons,
            width=settings.door_width * s,
            height=settings.door_height * s,
            frame_depth=0.35 * s
        )
    elif fam == "server_rack":
        return ServerRackConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            rack_type=settings.rack_type,
            cartridge_occupancy=settings.cartridge_occupancy,
            has_service_terminal=settings.has_service_terminal,
            width=0.80 * s,
            height=2.00 * s,
            depth=0.85 * s
        )
    elif fam == "crate":
        return CrateConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            crate_type=settings.crate_type,
            lid_state=settings.crate_lid,
            width=0.80 * s,
            height=0.65 * s,
            depth=0.60 * s
        )
    elif fam == "locker":
        return LockerConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            columns=settings.locker_cols,
            door_state=settings.locker_door_state,
            has_integrated_bench=settings.has_integrated_bench,
            height=1.90 * s,
            depth=0.50 * s
        )
    elif fam == "pipes":
        return PipeConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            pipe_type=settings.pipe_type,
            valve_type=settings.pipe_valve,
            has_insulation_layer=settings.has_insulation_layer,
            length=1.80 * s,
            radius=0.09 * s
        )
    elif fam == "crew_bed":
        return CrewBedConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            bed_type=settings.bed_type,
            width=settings.bed_width * s,
            length=settings.bed_length * s,
            height=settings.bed_height * s,
            mattress_state=settings.bed_mattress_state,
            has_pillow=settings.bed_has_pillow,
            has_under_drawers=settings.bed_has_under_drawers,
            has_guardrails=settings.bed_has_guardrails,
            headrest_incline=settings.bed_headrest_incline,
            blanket_color=settings.bed_blanket_color
        )
    elif fam == "bunk_bed":
        return BunkBedConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            frame_style=settings.bunk_frame,
            width=settings.bunk_width * s,
            length=settings.bunk_length * s,
            height=settings.bunk_height * s,
            ladder_position=settings.bunk_ladder_pos,
            upper_guardrail=settings.bunk_upper_guardrail,
            lower_bunk_state=settings.bunk_lower_state,
            upper_bunk_state=settings.bunk_upper_state,
            has_reading_lights=settings.bunk_has_reading_lights,
            has_storage_lockers=settings.bunk_has_lockers,
            has_curtains=settings.bunk_has_curtains,
            blanket_color=settings.bunk_blanket_color
        )
    elif fam == "nightstand":
        return NightstandConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            stand_type=settings.nightstand_type,
            width=settings.nightstand_width * s,
            depth=settings.nightstand_depth * s,
            height=settings.nightstand_height * s,
            drawer_count=settings.nightstand_drawers,
            drawer_open_ratio=settings.nightstand_drawer_open,
            has_raised_rim=settings.nightstand_raised_rim,
            has_bedside_lamp=settings.nightstand_has_lamp,
            lamp_state=settings.nightstand_lamp_state,
            has_swivel_tray=settings.nightstand_swivel_tray
        )
    elif fam == "radiator_heater":
        return RadiatorHeaterConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            heater_type=settings.heater_type,
            width=settings.heater_width * s,
            height=settings.heater_height * s,
            depth=settings.heater_depth * s,
            fin_count=settings.heater_fin_count,
            is_operational=settings.heater_is_operational,
            has_thermostat_dial=settings.heater_thermostat,
            has_steam_pipe=settings.heater_steam_pipe,
            damage_state=settings.heater_damage
        )
    elif fam == "office_door":
        return OfficeDoorConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            door_style=settings.office_door_style,
            glass_type=settings.office_glass_type,
            width=settings.office_door_width * s,
            height=settings.office_door_height * s,
            frame_depth=settings.office_door_depth * s,
            open_angle_deg=settings.office_open_angle,
            glass_damage=settings.office_glass_damage,
            handle_type=settings.office_handle_type,
            has_kickplate=settings.office_kickplate,
            has_transom=settings.office_transom
        )
    elif fam == "autopsy_table":
        return AutopsyTableConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            table_type=settings.autopsy_type,
            drainage_channel=settings.autopsy_drain,
            overhead_lamp=settings.autopsy_lamp,
            restraint_straps=settings.autopsy_straps,
            has_instrument_tray=settings.autopsy_tray,
            specimen_jar_count=settings.autopsy_jars
        )
    elif fam == "medical_screen":
        return MedicalScreenConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            screen_type=settings.screen_type,
            panel_count=settings.screen_panels,
            fold_angle_deg=settings.screen_fold_angle,
            curtain_damage=settings.screen_damage
        )
    elif fam == "morgue_gurney":
        return MorgueGurneyConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            gurney_type=settings.gurney_type,
            has_scissor_lift=settings.gurney_scissor,
            has_push_handles=settings.gurney_handles
        )
    elif fam == "chemical_cabinet":
        return ChemicalCabinetConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            cabinet_type=settings.chem_cabinet_type,
            glass_type=settings.chem_glass_type,
            door_state=settings.chem_door_state,
            has_padlock=settings.chem_padlock,
            shelf_item_density=settings.chem_clutter
        )
    elif fam == "restraint_chair":
        return RestraintChairConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            chair_type=settings.restraint_chair_type,
            arm_straps=settings.restraint_straps,
            leg_shackles=settings.restraint_shackles,
            iv_pole=settings.restraint_iv_pole
        )
    elif fam == "mess_table":
        return MessTableConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            table_type=settings.mess_table_type,
            stool_count=settings.mess_stools,
            stool_swing_state=settings.mess_stool_state,
            has_mess_trays=settings.mess_trays
        )
    elif fam == "ration_automat":
        return RationAutomatConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            machine_type=settings.automat_type,
            dispenser_state=settings.automat_dispenser_state,
            display_color=settings.automat_display_color
        )
    elif fam == "canteen_counter":
        return CanteenCounterConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            counter_type=settings.counter_type,
            roll_up_shutter=settings.counter_shutter,
            has_tray_rails=settings.counter_tray_rails
        )
    elif fam == "file_cabinet":
        drawer_mode = "all_closed" if settings.file_open_drawer < 0 else "single_open"
        return FileCabinetConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            cabinet_style=settings.file_cabinet_type,
            drawer_count=4 if settings.file_cabinet_type == "vertical_tower" else 2,
            drawer_open_mode=drawer_mode
        )
    elif fam == "locker_bench":
        return LockerBenchConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            bench_type=settings.locker_bench_type,
            has_forgotten_gear=settings.locker_bench_gear
        )
    elif fam == "work_bench":
        return WorkBenchConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            bench_type=settings.work_bench_style,
            has_pegboard=settings.work_pegboard,
            has_vise=settings.work_vise,
            has_overhead_light=settings.work_luminaire
        )
    elif fam == "heavy_shelving":
        return HeavyShelvingConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            shelf_type=settings.shelf_type,
            levels=settings.shelf_levels,
            has_x_bracing=settings.shelf_x_bracing,
            bent_shelf_index=settings.shelf_bent_index
        )
    elif fam == "tool_chest_cart":
        return ToolChestCartConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            cart_style=settings.tool_cart_style,
            drawer_open_style=settings.tool_open_style,
            has_top_mat_parts=settings.tool_top_parts
        )
    elif fam == "safety_shower":
        return SafetyShowerConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            shower_type=settings.shower_station_type,
            has_pull_chain=settings.shower_pull_chain,
            has_eyewash_bowl=settings.shower_eyewash,
            has_floor_drain_grate=settings.shower_drain_grate
        )
    elif fam == "hydroponic_tray_bed":
        return HydroponicTrayBedConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            bed_type=settings.hydro_bed_type,
            plant_state=settings.hydro_plant_state,
            uv_light_state=settings.hydro_uv_light
        )
    elif fam == "security_desk":
        return SecurityDeskConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            desk_style=settings.sec_desk_type,
            bulletproof_glass=settings.sec_bulletproof_glass,
            has_cctv_monitor=settings.sec_cctv_monitor,
            has_intercom_grille=settings.sec_intercom
        )
    elif fam == "weapons_rack":
        return WeaponsRackConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            rack_type=settings.weapons_rack_type,
            slot_count=settings.weapons_slots,
            is_locked=settings.weapons_locked,
            occupancy_ratio=settings.weapons_occupancy
        )
    elif fam == "bridge_console_desk":
        return BridgeConsoleDeskConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            console_shape=settings.bridge_console_type,
            crt_count=settings.bridge_screens,
            chair_included=settings.bridge_swivel_chair
        )
    elif fam == "space_toilet":
        return SpaceToiletConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            toilet_type=settings.toilet_type,
            has_thigh_restraints=settings.toilet_clamps
        )
    elif fam == "scrub_sink":
        return ScrubSinkConfig(
            seed=settings.seed,
            name=name,
            target_tri_budget=settings.target_tri_budget,
            wear_level=settings.wear_level,
            sink_type=settings.scrub_sink_type,
            has_soap_dispenser=settings.scrub_dispenser,
            has_splash_mirror=settings.scrub_mirror
        )
    elif fam in GENERATOR_REGISTRY:
        cfg_cls, _ = GENERATOR_REGISTRY[fam]
        kwargs = {
            "seed": settings.seed,
            "name": name,
            "wear_level": settings.wear_level,
        }
        dummy = cfg_cls(name=name)
        if hasattr(dummy, "target_tri_budget") and settings.target_tri_budget > 0:
            kwargs["target_tri_budget"] = settings.target_tri_budget
        return cfg_cls(**kwargs)
    return CrashCartConfig(seed=settings.seed, name=name)

def build_config(settings):
    cfg = _build_config_internal(settings)
    if hasattr(cfg, "add_collision_mesh"):
        cfg.add_collision_mesh = settings.generate_collision_shape
    if hasattr(cfg, "collision_type"):
        cfg.collision_type = settings.export_collision_type
    if hasattr(cfg, "collision_suffix"):
        cfg.collision_suffix = settings.export_collision_suffix
    if hasattr(cfg, "pivot_rule"):
        cfg.pivot_rule = settings.export_pivot_rule
    if hasattr(cfg, "palette_name"):
        cfg.palette_name = settings.palette_name
    if hasattr(cfg, "emission_scale"):
        cfg.emission_scale = settings.emission_scale
    return cfg

class BELOWNOMINAL_OT_generate_asset(Operator):
    """Generar o regenerar el asset seleccionado en la vista 3D"""
    bl_idname = "belownominal.generate_asset"
    bl_label = "¡Generar Modelo 3D!"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.below_nominal_settings
        config = build_config(settings)

        _, generator_cls = GENERATOR_REGISTRY[settings.asset_family]
        gen = generator_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        settings.last_tri_count = report.triangle_count
        settings.last_status = f"Generado: {report.triangle_count} tris ({report.vertex_count} verts)"

        context.view_layer.objects.active = obj
        obj.select_set(True)

        self.report({'INFO'}, f"Generado '{obj.name}' con éxito ({report.triangle_count} tris)")
        return {'FINISHED'}

class BELOWNOMINAL_OT_random_seed(Operator):
    """Generar nueva semilla aleatoria y regenerar el modelo actual"""
    bl_idname = "belownominal.random_seed"
    bl_label = "🎲 Variación Aleatoria (Nueva Semilla)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.below_nominal_settings
        settings.seed = random.randint(1, 999999)
        return bpy.ops.belownominal.generate_asset('INVOKE_DEFAULT')

class BELOWNOMINAL_OT_export_glb(Operator):
    """Exportar el modelo actual como GLB y JSON listo para Godot 4"""
    bl_idname = "belownominal.export_glb"
    bl_label = "💾 Exportar a Godot 4 (GLB + JSON)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        settings = context.scene.below_nominal_settings
        config = build_config(settings)
        obj_name = config.name

        if obj_name not in bpy.data.objects:
            self.report({'ERROR'}, f"No se encontró el objeto '{obj_name}'. Primero hacé clic en 'Generar Modelo 3D'.")
            return {'CANCELLED'}

        obj = bpy.data.objects[obj_name]
        _, generator_cls = GENERATOR_REGISTRY[settings.asset_family]
        gen = generator_cls()
        report = gen.validate(obj, config)

        output_dir = os.path.join(addon_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        glb_path = os.path.join(output_dir, f"{config.name}.glb")

        res = GLBExporter.export(
            obj=obj,
            config=config,
            report=report,
            filepath=glb_path,
            generator_name=generator_cls.__name__,
            validate_with_godot=settings.export_validate_godot
        )

        report_name = os.path.basename(res.report_md_path) if hasattr(res, "report_md_path") and res.report_md_path else "export_report.md"
        settings.last_status = f"Exportado: {os.path.basename(res.glb_path)} | Reporte: {report_name}"
        self.report({'INFO'}, f"Exportado con éxito: {res.glb_path}")
        return {'FINISHED'}

class VIEW3D_PT_below_nominal_panel(Panel):
    """Pestaña en la barra lateral (N) de la vista 3D con variantes profundas"""
    bl_label = "Below Nominal - Generador PSX"
    bl_idname = "VIEW3D_PT_below_nominal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Below Nominal"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.below_nominal_settings

        # 1. Selector de Familia de Asset
        box_fam = layout.box()
        box_fam.label(text="Familia de Asset", icon='SOLO_ON')
        box_fam.prop(settings, "asset_family", text="")

        # 2. Acciones Principales
        col = layout.column(align=True)
        col.scale_y = 1.4
        col.operator("belownominal.generate_asset", icon='MESH_CUBE')
        col.operator("belownominal.random_seed", icon='FILE_REFRESH')

        # 3. Estado del Modelo Actual
        box_st = layout.box()
        box_st.label(text=f"Polígonos: {settings.last_tri_count} tris", icon='INFO')
        box_st.label(text=f"Estado: {settings.last_status}")

        # 4. Parámetros Globales y Texturas PS1
        box_gen = layout.box()
        box_gen.label(text="Textura y Parámetros Globales PS1", icon='MATERIAL')
        box_gen.prop(settings, "palette_name")
        box_gen.prop(settings, "emission_scale", slider=True)
        box_gen.prop(settings, "wear_level", slider=True)
        box_gen.prop(settings, "seed")
        box_gen.prop(settings, "asset_name")
        box_gen.prop(settings, "target_tri_budget")
        box_gen.prop(settings, "scale_factor")

        # 5. Opciones Específicas Dinámicas por Familia
        fam = settings.asset_family
        box_spec = layout.box()
        box_spec.label(text=f"Modificadores: {fam.replace('_', ' ').capitalize()}", icon='PROPERTIES')

        if fam == "station_corridor":
            box_spec.prop(settings, "corridor_type")
            row = box_spec.row(align=True)
            row.prop(settings, "corridor_width", text="Ancho")
            row.prop(settings, "corridor_length", text="Largo")
            row.prop(settings, "corridor_height", text="Alto")
            box_spec.prop(settings, "corridor_floor_style")
            box_spec.prop(settings, "corridor_wall_style")
            box_spec.prop(settings, "corridor_ceiling_style")
            box_spec.prop(settings, "corridor_damage")
            box_spec.prop(settings, "corridor_lighting")
            if settings.corridor_lighting:
                box_spec.prop(settings, "corridor_light_state")
            box_spec.prop(settings, "corridor_cable_runs")
            box_spec.prop(settings, "corridor_wall_alcove")
            box_spec.prop(settings, "corridor_hazard_stripes")

        elif fam == "station_room":
            box_spec.prop(settings, "room_archetype")
            row = box_spec.row(align=True)
            row.prop(settings, "room_width", text="Ancho")
            row.prop(settings, "room_depth", text="Prof.")
            row.prop(settings, "room_height", text="Alto")
            box_doors = box_spec.box()
            box_doors.label(text="Vanos de Puerta Conectores", icon='SNAP_ON')
            r_d1 = box_doors.row(align=True)
            r_d1.prop(settings, "room_door_north", text="Norte (+Y)")
            r_d1.prop(settings, "room_door_south", text="Sur (-Y)")
            r_d2 = box_doors.row(align=True)
            r_d2.prop(settings, "room_door_east", text="Este (+X)")
            r_d2.prop(settings, "room_door_west", text="Oeste (-X)")
            box_spec.prop(settings, "room_pillar_layout")
            box_spec.prop(settings, "room_elevation")
            box_spec.prop(settings, "room_lighting_color")
            box_spec.prop(settings, "room_observation_window")
            box_spec.prop(settings, "room_overhead_gantry")
            box_spec.prop(settings, "room_floor_drain")

        elif fam == "crash_cart":
            row = box_spec.row(align=True)
            row.prop(settings, "cart_width", text="Ancho")
            row.prop(settings, "cart_height", text="Alto")
            row.prop(settings, "cart_depth", text="Prof.")
            box_spec.prop(settings, "cart_drawers")
            box_spec.prop(settings, "cart_drawer_mode")
            box_spec.prop(settings, "cart_slide_max")
            box_spec.prop(settings, "cart_handle_style")
            box_spec.prop(settings, "body_color_preset")
            box_spec.prop(settings, "has_top_monitor")
            if settings.has_top_monitor:
                box_spec.prop(settings, "cart_monitor_phosphor")
            box_spec.prop(settings, "has_push_handle")
            if settings.has_push_handle:
                box_spec.prop(settings, "push_handle_side")
            box_spec.prop(settings, "has_oxygen_rack")
            if settings.has_oxygen_rack:
                box_spec.prop(settings, "oxygen_tank_count")

        elif fam == "office_desk":
            row = box_spec.row(align=True)
            row.prop(settings, "desk_width", text="Ancho")
            row.prop(settings, "desk_height", text="Alto")
            row.prop(settings, "desk_depth", text="Prof.")
            box_spec.prop(settings, "desk_leg_style")
            box_spec.prop(settings, "desk_pedestals")
            box_spec.prop(settings, "desk_drawers")
            box_spec.prop(settings, "desk_drawer_style")
            box_spec.prop(settings, "desk_surface_material")
            box_spec.prop(settings, "desk_cable_grommet")
            box_spec.prop(settings, "desk_partition")
            box_spec.prop(settings, "desk_under_shelf")

        elif fam == "office_chair":
            row = box_spec.row(align=True)
            row.prop(settings, "chair_seat_width", text="Ancho")
            row.prop(settings, "chair_seat_depth", text="Prof.")
            row.prop(settings, "chair_seat_height", text="Alto")
            box_spec.prop(settings, "chair_backrest_style")
            box_spec.prop(settings, "chair_backrest_tilt", slider=True)
            box_spec.prop(settings, "chair_base_style")
            box_spec.prop(settings, "chair_spokes")
            box_spec.prop(settings, "chair_armrests")
            box_spec.prop(settings, "chair_upholstery")

        elif fam == "sign_placard":
            row = box_spec.row(align=True)
            row.prop(settings, "sign_width", text="Ancho")
            row.prop(settings, "sign_height", text="Alto")
            box_spec.prop(settings, "sign_mount")
            box_spec.prop(settings, "sign_type")
            box_spec.prop(settings, "sign_damage")
            if settings.sign_mount == "ceiling_hanging":
                box_spec.prop(settings, "sign_chain_len")

        elif fam == "trash_bin":
            box_spec.prop(settings, "trash_bin_type")
            row = box_spec.row(align=True)
            row.prop(settings, "trash_height", text="Alto")
            row.prop(settings, "trash_radius", text="Radio/Ancho")
            box_spec.prop(settings, "trash_is_rectangular")
            box_spec.prop(settings, "trash_lid_state")
            box_spec.prop(settings, "trash_foot_pedal")
            box_spec.prop(settings, "trash_overflowing")

        elif fam == "light_fixture":
            box_spec.prop(settings, "light_type")
            row = box_spec.row(align=True)
            row.prop(settings, "light_length", text="Largo")
            row.prop(settings, "light_width", text="Ancho")
            row.prop(settings, "light_depth", text="Prof.")
            box_spec.prop(settings, "light_tubes")
            box_spec.prop(settings, "light_state")
            box_spec.prop(settings, "light_wire_guard")
            box_spec.prop(settings, "light_dangling_wire")

        elif fam == "fire_extinguisher":
            row = box_spec.row(align=True)
            row.prop(settings, "ext_tank_height", text="Alto")
            row.prop(settings, "ext_tank_radius", text="Radio")
            box_spec.prop(settings, "ext_mount_style")
            if settings.ext_mount_style == "emergency_cabinet":
                box_spec.prop(settings, "ext_glass_state")
            box_spec.prop(settings, "ext_pressure_gauge")
            box_spec.prop(settings, "ext_hose_nozzle")
            box_spec.prop(settings, "ext_wall_sign")

        elif fam == "vent_grate":
            row = box_spec.row(align=True)
            row.prop(settings, "vent_width", text="Ancho")
            row.prop(settings, "vent_height", text="Alto")
            box_spec.prop(settings, "vent_grate_type")
            box_spec.prop(settings, "vent_grate_state")
            if settings.vent_grate_state == "hanging_by_one_screw":
                box_spec.prop(settings, "vent_hanging_angle", slider=True)
            box_spec.prop(settings, "vent_has_fan")
            if settings.vent_has_fan:
                box_spec.prop(settings, "vent_fan_blades")

        elif fam == "cable_bundle":
            box_spec.prop(settings, "cable_bundle_type")
            box_spec.prop(settings, "cable_bundle_length")
            box_spec.prop(settings, "cable_bundle_count")
            box_spec.prop(settings, "cable_bundle_sag")
            box_spec.prop(settings, "cable_severed_wire")
            box_spec.prop(settings, "cable_support_ties")
            box_spec.prop(settings, "cable_junction_box")

        elif fam == "electrical_panel":
            row = box_spec.row(align=True)
            row.prop(settings, "panel_width", text="Ancho")
            row.prop(settings, "panel_height", text="Alto")
            row.prop(settings, "panel_depth", text="Prof.")
            row_ctrl = box_spec.row(align=True)
            row_ctrl.prop(settings, "button_rows", text="Filas Botones")
            row_ctrl.prop(settings, "button_cols", text="Cols Botones")
            box_spec.prop(settings, "switch_count")
            box_spec.prop(settings, "indicator_count")
            box_spec.prop(settings, "cable_count")
            box_spec.prop(settings, "has_crt")
            if settings.has_crt:
                box_spec.prop(settings, "panel_phosphor")
            box_spec.prop(settings, "has_knife_switch")
            box_spec.prop(settings, "has_digital_readout")
            box_spec.prop(settings, "door_ajar")
            if settings.door_ajar:
                box_spec.prop(settings, "door_open_angle", slider=True)

        elif fam == "terminal":
            row = box_spec.row(align=True)
            row.prop(settings, "terminal_width", text="Ancho")
            row.prop(settings, "terminal_height", text="Alto")
            row.prop(settings, "terminal_depth", text="Prof.")
            box_spec.prop(settings, "terminal_type")
            box_spec.prop(settings, "terminal_state")
            box_spec.prop(settings, "keyboard_style")
            box_spec.prop(settings, "panel_phosphor")
            box_spec.prop(settings, "terminal_cables")

        elif fam == "door":
            row = box_spec.row(align=True)
            row.prop(settings, "door_width", text="Ancho")
            row.prop(settings, "door_height", text="Alto")
            box_spec.prop(settings, "door_type")
            box_spec.prop(settings, "door_open_ratio", slider=True)
            box_spec.prop(settings, "has_reinforced_window")
            box_spec.prop(settings, "has_hydraulic_pistons")

        elif fam == "oxypod":
            box_spec.prop(settings, "oxypod_type")
            box_spec.prop(settings, "oxygen_level", slider=True)
            box_spec.prop(settings, "has_mask_dock")
            box_spec.prop(settings, "has_coiled_hose")

        elif fam == "server_rack":
            box_spec.prop(settings, "rack_type")
            box_spec.prop(settings, "cartridge_occupancy", slider=True)
            box_spec.prop(settings, "has_service_terminal")

        elif fam == "crate":
            box_spec.prop(settings, "crate_type")
            box_spec.prop(settings, "crate_lid")

        elif fam == "locker":
            box_spec.prop(settings, "locker_cols")
            box_spec.prop(settings, "locker_door_state")
            box_spec.prop(settings, "has_integrated_bench")

        elif fam == "pipes":
            box_spec.prop(settings, "pipe_type")
            box_spec.prop(settings, "pipe_valve")
            box_spec.prop(settings, "has_insulation_layer")

        elif fam == "crew_bed":
            box_spec.prop(settings, "bed_type")
            row = box_spec.row(align=True)
            row.prop(settings, "bed_width", text="Ancho")
            row.prop(settings, "bed_length", text="Largo")
            row.prop(settings, "bed_height", text="Alto")
            box_spec.prop(settings, "bed_mattress_state")
            box_spec.prop(settings, "bed_blanket_color")
            box_spec.prop(settings, "bed_has_pillow")
            box_spec.prop(settings, "bed_has_under_drawers")
            box_spec.prop(settings, "bed_has_guardrails")
            box_spec.prop(settings, "bed_headrest_incline", slider=True)

        elif fam == "bunk_bed":
            box_spec.prop(settings, "bunk_frame")
            row = box_spec.row(align=True)
            row.prop(settings, "bunk_width", text="Ancho")
            row.prop(settings, "bunk_length", text="Largo")
            row.prop(settings, "bunk_height", text="Alto")
            box_spec.prop(settings, "bunk_ladder_pos")
            box_spec.prop(settings, "bunk_lower_state")
            box_spec.prop(settings, "bunk_upper_state")
            box_spec.prop(settings, "bunk_blanket_color")
            box_spec.prop(settings, "bunk_upper_guardrail")
            box_spec.prop(settings, "bunk_has_reading_lights")
            box_spec.prop(settings, "bunk_has_lockers")
            box_spec.prop(settings, "bunk_has_curtains")

        elif fam == "nightstand":
            box_spec.prop(settings, "nightstand_type")
            row = box_spec.row(align=True)
            row.prop(settings, "nightstand_width", text="Ancho")
            row.prop(settings, "nightstand_depth", text="Prof.")
            row.prop(settings, "nightstand_height", text="Alto")
            box_spec.prop(settings, "nightstand_drawers")
            box_spec.prop(settings, "nightstand_drawer_open", slider=True)
            box_spec.prop(settings, "nightstand_raised_rim")
            box_spec.prop(settings, "nightstand_has_lamp")
            if settings.nightstand_has_lamp:
                box_spec.prop(settings, "nightstand_lamp_state")
            box_spec.prop(settings, "nightstand_swivel_tray")

        elif fam == "radiator_heater":
            box_spec.prop(settings, "heater_type")
            row = box_spec.row(align=True)
            row.prop(settings, "heater_width", text="Ancho")
            row.prop(settings, "heater_height", text="Alto")
            row.prop(settings, "heater_depth", text="Prof.")
            box_spec.prop(settings, "heater_fin_count")
            box_spec.prop(settings, "heater_damage")
            box_spec.prop(settings, "heater_is_operational")
            box_spec.prop(settings, "heater_thermostat")
            box_spec.prop(settings, "heater_steam_pipe")

        elif fam == "office_door":
            box_spec.prop(settings, "office_door_style")
            box_spec.prop(settings, "office_glass_type")
            row = box_spec.row(align=True)
            row.prop(settings, "office_door_width", text="Ancho")
            row.prop(settings, "office_door_height", text="Alto")
            row.prop(settings, "office_door_depth", text="Espesor")
            box_spec.prop(settings, "office_open_angle", slider=True)
            box_spec.prop(settings, "office_glass_damage")
            box_spec.prop(settings, "office_handle_type")
            box_spec.prop(settings, "office_kickplate")
            box_spec.prop(settings, "office_transom")

        elif fam == "autopsy_table":
            box_spec.prop(settings, "autopsy_type")
            box_spec.prop(settings, "autopsy_straps")
            box_spec.prop(settings, "autopsy_drain")
            box_spec.prop(settings, "autopsy_lamp")
            box_spec.prop(settings, "autopsy_tray")
            box_spec.prop(settings, "autopsy_jars")

        elif fam == "medical_screen":
            box_spec.prop(settings, "screen_type")
            box_spec.prop(settings, "screen_panels")
            box_spec.prop(settings, "screen_fold_angle", slider=True)
            box_spec.prop(settings, "screen_damage")

        elif fam == "morgue_gurney":
            box_spec.prop(settings, "gurney_type")
            box_spec.prop(settings, "gurney_scissor")
            box_spec.prop(settings, "gurney_handles")

        elif fam == "chemical_cabinet":
            box_spec.prop(settings, "chem_cabinet_type")
            box_spec.prop(settings, "chem_glass_type")
            box_spec.prop(settings, "chem_door_state")
            box_spec.prop(settings, "chem_padlock")
            box_spec.prop(settings, "chem_clutter", slider=True)

        elif fam == "restraint_chair":
            box_spec.prop(settings, "restraint_chair_type")
            box_spec.prop(settings, "restraint_straps")
            box_spec.prop(settings, "restraint_shackles")
            box_spec.prop(settings, "restraint_iv_pole")

        elif fam == "mess_table":
            box_spec.prop(settings, "mess_table_type")
            box_spec.prop(settings, "mess_stools")
            box_spec.prop(settings, "mess_stool_state")
            box_spec.prop(settings, "mess_trays")

        elif fam == "ration_automat":
            box_spec.prop(settings, "automat_type")
            box_spec.prop(settings, "automat_dispenser_state")
            box_spec.prop(settings, "automat_display_color")

        elif fam == "canteen_counter":
            box_spec.prop(settings, "counter_type")
            box_spec.prop(settings, "counter_shutter")
            box_spec.prop(settings, "counter_sneeze_guard")
            box_spec.prop(settings, "counter_tray_rails")

        elif fam == "file_cabinet":
            box_spec.prop(settings, "file_cabinet_type")
            box_spec.prop(settings, "file_open_drawer")
            box_spec.prop(settings, "file_scattered")

        elif fam == "locker_bench":
            box_spec.prop(settings, "locker_bench_type")
            box_spec.prop(settings, "locker_bench_gear")

        elif fam == "work_bench":
            box_spec.prop(settings, "work_bench_style")
            box_spec.prop(settings, "work_pegboard")
            box_spec.prop(settings, "work_vise")
            box_spec.prop(settings, "work_luminaire")
            box_spec.prop(settings, "work_clutter", slider=True)

        elif fam == "heavy_shelving":
            box_spec.prop(settings, "shelf_type")
            box_spec.prop(settings, "shelf_levels")
            box_spec.prop(settings, "shelf_x_bracing")
            box_spec.prop(settings, "shelf_bent_index")

        elif fam == "tool_chest_cart":
            box_spec.prop(settings, "tool_cart_style")
            box_spec.prop(settings, "tool_open_style")
            box_spec.prop(settings, "tool_top_parts")

        elif fam == "safety_shower":
            box_spec.prop(settings, "shower_station_type")
            box_spec.prop(settings, "shower_eyewash")
            box_spec.prop(settings, "shower_pull_chain")
            box_spec.prop(settings, "shower_drain_grate")

        elif fam == "hydroponic_tray_bed":
            box_spec.prop(settings, "hydro_bed_type")
            box_spec.prop(settings, "hydro_plant_state")
            box_spec.prop(settings, "hydro_uv_light")

        elif fam == "security_desk":
            box_spec.prop(settings, "sec_desk_type")
            box_spec.prop(settings, "sec_bulletproof_glass")
            box_spec.prop(settings, "sec_cctv_monitor")
            box_spec.prop(settings, "sec_intercom")

        elif fam == "weapons_rack":
            box_spec.prop(settings, "weapons_rack_type")
            box_spec.prop(settings, "weapons_slots")
            box_spec.prop(settings, "weapons_locked")
            box_spec.prop(settings, "weapons_occupancy", slider=True)

        elif fam == "bridge_console_desk":
            box_spec.prop(settings, "bridge_console_type")
            box_spec.prop(settings, "bridge_screens")
            box_spec.prop(settings, "bridge_swivel_chair")
            box_spec.prop(settings, "bridge_throttles")

        elif fam == "space_toilet":
            box_spec.prop(settings, "toilet_type")
            box_spec.prop(settings, "toilet_clamps")
            box_spec.prop(settings, "toilet_suction_hose")

        elif fam == "scrub_sink":
            box_spec.prop(settings, "scrub_sink_type")
            box_spec.prop(settings, "scrub_dispenser")
            box_spec.prop(settings, "scrub_mirror")

        elif fam in GENERATOR_REGISTRY:
            box_spec.label(text="Mobiliario y Survival Horror (Below Nominal)", icon='CHECKMARK')
            box_spec.label(text="Variantes procedurales y geometría PS1 listas para generar.")
            row = box_spec.row(align=True)
            row.label(text=f"Familia: {fam}", icon='OBJECT_DATAMODE')

        # 6. Exportación a Godot 4
        layout.separator()
        box_exp = layout.box()
        box_exp.label(text="Pipeline de Exportación a Godot 4", icon='EXPORT')
        box_exp.prop(settings, "generate_collision_shape")
        if settings.generate_collision_shape:
            row_col = box_exp.row(align=True)
            row_col.prop(settings, "export_collision_type", text="Forma")
            row_col.prop(settings, "export_collision_suffix", text="Sufijo")
        box_exp.prop(settings, "export_pivot_rule")
        box_exp.prop(settings, "export_validate_godot")
        col_exp = box_exp.column(align=True)
        col_exp.scale_y = 1.3
        col_exp.operator("belownominal.export_glb", text="Exportar Asset (GLB + Informes)")

classes = (
    BelowNominalPanelSettings,
    BELOWNOMINAL_OT_generate_asset,
    BELOWNOMINAL_OT_random_seed,
    BELOWNOMINAL_OT_export_glb,
    VIEW3D_PT_below_nominal_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.below_nominal_settings = bpy.props.PointerProperty(type=BelowNominalPanelSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.below_nominal_settings

if __name__ == "__main__":
    register()
