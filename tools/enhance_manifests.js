const fs = require('fs');
const path = require('path');

const SPANISH_NAMES_AND_DESCS = {
  access_card_lvl1: {
    name: "Tarjeta de Acceso Nivel 1",
    description: "Tarjeta de identificación y pase de seguridad con chip de contacto y banda magnética. Podés personalizar sus medidas de ancho, alto y grosor para descargar en formato GLB."
  },
  autopsy_table: {
    name: "Mesa Quirúrgica y Autopsia",
    description: "Mesa médica mortuoria de acero inoxidable con canal perimetral de drenaje. Podés modificar el largo, ancho y lámpara superior para descargar en formato GLB."
  },
  bridge_console_desk: {
    name: "Consola de Mando y Navegación",
    description: "Escritorio de control con pantallas anguladas y paneles de navegación. Podés ajustar el nivel de desgaste, paleta y accesorios para descargar en formato GLB."
  },
  bunk_bed: {
    name: "Cama Litera Modular",
    description: "Litera metálica de dos niveles con escalera de acceso frontal. Podés ajustar sus medidas, nivel de desgaste y paleta de color para descargar en formato GLB."
  },
  cable_bundle: {
    name: "Mazo de Cables y Conductos",
    description: "Conjunto de cables y canalizaciones industriales adosables a paredes o techos. Podés personalizar el grosor, longitud y paleta de aislamiento para descargar en formato GLB."
  },
  canteen_counter: {
    name: "Mostrador de Comedor y Cafetería",
    description: "Mostrador de servicio con bandeja y división para zonas de descanso o cafeterías. Podés ajustar dimensiones y paleta para descargar en formato GLB."
  },
  chemical_cabinet: {
    name: "Gabinete de Químicos y Reactivos",
    description: "Armario metálico reforzado para almacenamiento de sustancias y reactivos de laboratorio. Podés ajustar sus dimensiones y puertas para descargar en formato GLB."
  },
  crash_cart: {
    name: "Carro de Paro / Emergencia Médica",
    description: "Carro hospitalario rodante de reanimación con cajones modulares y monitor superior. Podés configurar la cantidad de gavetas y paleta de color para descargar en formato GLB."
  },
  crate: {
    name: "Contenedor de Carga Modular",
    description: "Caja de almacenamiento y carga presurizada con esquinas reforzadas. Podés personalizar las medidas de ancho, largo y alto, nivel de desgaste y paleta para descargar en formato GLB."
  },
  crew_bed: {
    name: "Cama Individual de Tripulación",
    description: "Cama individual compacta con cajonera inferior para camarotes y dormitorios. Podés regular las medidas, nivel de uso y paleta para descargar en formato GLB."
  },
  door: {
    name: "Puerta Corrediza Industrial",
    description: "Puerta corrediza automatizada para mamparas y accesos entre sectores. Podés ajustar el ancho, alto, franjas de peligro y luces de estado para descargar en formato GLB."
  },
  electrical_panel: {
    name: "Panel Eléctrico y Distribución",
    description: "Caja de disyuntores e interruptores de alta tensión para muros técnicos. Podés modificar el tamaño de la caja, paleta y luces indicadoras para descargar en formato GLB."
  },
  file_cabinet: {
    name: "Archivador Metálico de Oficina",
    description: "Mueble vertical de gavetas para documentos y carpetas. Podés personalizar el número de cajones y nivel de desgaste para descargar en formato GLB."
  },
  fire_extinguisher: {
    name: "Extintor de Emergencia y Soporte",
    description: "Cilindro de extinción de incendios presurizado con manómetro y soporte de pared. Podés ajustar la escala y paleta de seguridad para descargar en formato GLB."
  },
  heavy_shelving: {
    name: "Estantería Pesada Industrial",
    description: "Estructura metálica de repisas abiertas para almacenamiento de carga pesada. Podés regular el número de estantes y altura total para descargar en formato GLB."
  },
  hydroponic_tray_bed: {
    name: "Bandeja de Cultivo Hidropónico",
    description: "Módulo de cultivo botánico con canal de sustrato y lámparas de crecimiento. Podés ajustar la longitud y sistemas de soporte para descargar en formato GLB."
  },
  light_fixture: {
    name: "Lámpara de Techo / Luminaria",
    description: "Dispositivo de iluminación para techos y pasillos transitables. Podés configurar la longitud, rejilla y escala de emisión para descargar en formato GLB."
  },
  locker: {
    name: "Casillero Personal / Taquilla",
    description: "Módulo de casilleros de acero con rendijas de ventilación y cerradura. Podés configurar el número de compartimentos y paleta para descargar en formato GLB."
  },
  locker_bench: {
    name: "Banco de Vestuario y Pasillo",
    description: "Banco alargado de madera o metal para vestuarios y zonas de cambio de ropa. Podés ajustar el largo y estructura de soporte para descargar en formato GLB."
  },
  medical_screen: {
    name: "Biombo Médico Plegable",
    description: "Mampara divisoria articulada de privacidad para consultorios y enfermerías. Podés ajustar la cantidad de paneles y altura para descargar en formato GLB."
  },
  mess_table: {
    name: "Mesa de Comedor con Bancos",
    description: "Mesa comunitaria con bancos integrados para áreas sociales y comedores. Podés modificar el largo y capacidad de asientos para descargar en formato GLB."
  },
  morgue_gurney: {
    name: "Camilla de Traslado / Morgue",
    description: "Camilla rodante de acero inoxidable para transporte de pacientes o cuerpos. Podés ajustar altura y freno de ruedas para descargar en formato GLB."
  },
  nightstand: {
    name: "Mesa de Noche Compacta",
    description: "Mueble auxiliar de cabecera con gaveta superior y repisa inferior. Podés ajustar las proporciones y paleta de materiales para descargar en formato GLB."
  },
  office_chair: {
    name: "Silla Ergonómica de Oficina",
    description: "Silla giratoria de escritorio con respaldo alto y apoyabrazos. Podés regular la altura, inclinación y estilo de tapicería para descargar en formato GLB."
  },
  office_desk: {
    name: "Escritorio Administrativo",
    description: "Escritorio de trabajo con cajonera lateral y pasacables. Podés personalizar el ancho de la mesa y distribución de gavetas para descargar en formato GLB."
  },
  office_door: {
    name: "Puerta Batiente de Oficina",
    description: "Puerta interior con manija o picaporte para salas y despachos. Podés ajustar las medidas de la hoja y el marco para descargar en formato GLB."
  },
  oxypod: {
    name: "Cápsula de Oxígeno / Soporte Vital",
    description: "Cámara cilíndrica de regeneración atmosférica y soporte vital con ventanilla circular. Podés personalizar el radio y válvulas para descargar en formato GLB."
  },
  pipes: {
    name: "Sistema de Tuberías Industriales",
    description: "Conjunto de cañerías modulares con bridas, codos y válvulas de paso. Podés ajustar el diámetro y recorrido de la tubería para descargar en formato GLB."
  },
  radiator_heater: {
    name: "Radiador / Calefactor de Pared",
    description: "Unidad de calefacción térmica con aletas de disipación y termostato. Podés configurar la cantidad de celdas radiantes para descargar en formato GLB."
  },
  ration_automat: {
    name: "Máquina Expendedora de Raciones",
    description: "Autómata de suministros y alimentos con teclado numérico y vitrina de dispensado. Podés personalizar la altura y paleta para descargar en formato GLB."
  },
  restraint_chair: {
    name: "Silla de Contención y Sujeción",
    description: "Asiento reforzado con correas y soportes de seguridad para áreas médicas o de confinamiento. Podés ajustar el respaldo y anclajes para descargar en formato GLB."
  },
  safety_shower: {
    name: "Ducha de Seguridad y Lavaojos",
    description: "Estación de descontaminación de emergencia con tirador de ducha y cubeta lavaojos. Podés modificar la altura del surtidor para descargar en formato GLB."
  },
  scrub_sink: {
    name: "Lavamanos Quirúrgico",
    description: "Pila profunda de acero inoxidable con pedal o sensor de accionamiento para esterilización médica. Podés ajustar el ancho y grifería para descargar en formato GLB."
  },
  security_desk: {
    name: "Puesto de Guardia / Seguridad",
    description: "Mostrador elevado con ventanilla blindada y panel de control para control de acceso. Podés personalizar el frente y mampara para descargar en formato GLB."
  },
  server_rack: {
    name: "Armario de Servidores / Rack",
    description: "Gabinete vertical para unidades de cómputo con bahías ventiladas y luces LED. Podés configurar la cantidad de módulos para descargar en formato GLB."
  },
  sign_placard: {
    name: "Cartel de Señalización de Pared",
    description: "Placa de aviso y señalética modular para pasillos y compuertas. Podés elegir las dimensiones y colores de advertencia para descargar en formato GLB."
  },
  space_toilet: {
    name: "Inodoro Sanitario Compacto",
    description: "Unidad sanitaria compacta de succión al vacío con asideros y pedales de fijación. Podés personalizar la altura y accesorios para descargar en formato GLB."
  },
  station_corridor: {
    name: "Sección de Pasillo Modular",
    description: "Módulo de túnel o corredor transitable con mamparas y nervaduras de refuerzo. Podés ajustar el largo, ancho y altura para descargar en formato GLB."
  },
  station_room: {
    name: "Sala Modular Prefabricada",
    description: "Habitación cúbica prefabricada para recintos habitacionales o laboratorios. Podés regular las dimensiones de suelo a techo para descargar en formato GLB."
  },
  terminal: {
    name: "Terminal Informático de Pie",
    description: "Consola vertical con monitor CRT inclinado y teclado robusto. Podés modificar la inclinación de pantalla y altura de consola para descargar en formato GLB."
  },
  tool_chest_cart: {
    name: "Carro Portaherramientas de Taller",
    description: "Caja de herramientas rodante de varios cajones con superficie de trabajo superior. Podés ajustar el número de bandejas para descargar en formato GLB."
  },
  trash_bin: {
    name: "Contenedor de Residuos",
    description: "Bote o depósito cilíndrico de basura con pedal de apertura. Podés configurar el volumen y acabado del contenedor para descargar en formato GLB."
  },
  vent_grate: {
    name: "Rejilla de Ventilación",
    description: "Enrejado metálico de lamas para conductos de aire y filtrado. Podés personalizar el ancho, alto y ángulo de las ranuras para descargar en formato GLB."
  },
  weapons_rack: {
    name: "Armero / Soporte de Armas",
    description: "Mueble vertical con ranuras de seguridad para almacenamiento y custodia de equipo. Podés regular la capacidad y pestillos para descargar en formato GLB."
  },
  work_bench: {
    name: "Banco de Trabajo de Taller",
    description: "Mesa robusta de mantenimiento con panel perforado trasero y tornillo de banco. Podés ajustar la superficie y herramientas para descargar en formato GLB."
  }
};

const PARAM_TRANSLATIONS = {
  seed: { label: "Semilla Aleatoria", group: "Rendimiento" },
  target_tri_budget: { label: "Presupuesto de Triángulos", group: "Rendimiento" },
  name: { label: "Nombre de Instancia", group: "General" },
  wear_level: { label: "Nivel de Desgaste", group: "Materiales" },
  palette_name: { label: "Paleta de Color", group: "Materiales" },
  palette: { label: "Paleta de Color", group: "Materiales" },
  style_palette: { label: "Paleta de Color", group: "Materiales" },
  body_color_preset: { label: "Paleta de Color", group: "Materiales" },
  add_collision_mesh: { label: "Generar Colisión", group: "Opciones de Exportación" },
  collision_type: { label: "Tipo de Colisión", group: "Opciones de Exportación" },
  collision_suffix: { label: "Sufijo de Colisión", group: "Opciones de Exportación" },
  pivot_rule: { label: "Regla de Pivote", group: "Opciones de Exportación" },
  export_subcomponents: { label: "Exportar Subcomponentes", group: "Opciones de Exportación" },
  emission_scale: { label: "Intensidad de Emisión", group: "Materiales" },
  width: { label: "Ancho (m)", group: "Dimensiones" },
  height: { label: "Alto (m)", group: "Dimensiones" },
  length: { label: "Largo (m)", group: "Dimensiones" },
  depth: { label: "Profundidad (m)", group: "Dimensiones" },
  thickness: { label: "Grosor (m)", group: "Dimensiones" },
  radius: { label: "Radio (m)", group: "Dimensiones" }
};

const genDir = path.join(__dirname, '..', 'procedural_assets', 'generators');
const dirs = fs.readdirSync(genDir).filter(f => f !== '__pycache__' && fs.statSync(path.join(genDir, f)).isDirectory());

let updatedCount = 0;
dirs.forEach(family => {
  const mPath = path.join(genDir, family, 'manifest.json');
  if (!fs.existsSync(mPath)) return;
  const manifest = JSON.parse(fs.readFileSync(mPath, 'utf8'));

  if (SPANISH_NAMES_AND_DESCS[family]) {
    manifest.name = SPANISH_NAMES_AND_DESCS[family].name;
    manifest.description = SPANISH_NAMES_AND_DESCS[family].description;
  }

  // Update common parameter labels and groups
  if (Array.isArray(manifest.parameters)) {
    manifest.parameters.forEach(p => {
      const trans = PARAM_TRANSLATIONS[p.key];
      if (trans) {
        p.label = trans.label;
        p.group = trans.group;
      }
    });
  }

  fs.writeFileSync(mPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  updatedCount++;
});

console.log(`Updated ${updatedCount} generator manifests with unified Spanish names and descriptions.`);
