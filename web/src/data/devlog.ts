export interface DevlogEntry {
  version: string;
  date: string;
  badge: 'FEATURE' | 'MAJOR' | 'MILESTONE' | 'IMPROVEMENT' | 'FIX';
  badgeColor?: string;
  title: string;
  summary: string;
  highlights: string[];
  tags: string[];
  author?: string;
}

export const DEVLOG_ENTRIES: DevlogEntry[] = [
  {
    version: 'v3.0.0',
    date: '24 de Octubre, 2026',
    badge: 'MAJOR',
    badgeColor: '#e53e3e',
    title: 'Motor de Modelado Avanzado (CSG, Primitivas, Arrays, Imán a Caras), Paquete Godot 4 y Tema Dark Profesional',
    summary: 'Actualización mayor de ModelCoder que transforma a Studio 3D en un entorno de modelado procedural completo y profesional. Introduce operaciones booleanas CSG (diferencia, unión, intersección) con horneado, 4 nuevas primitivas paramétricas, modificadores de array lineal y radial, sistema de alineación y encastre magnético a caras, exportación corregida a Godot 4 con empaquetador ZIP y mapas de normales PBR, conmutador de tema visual Dark Profesional y sincronización de capacidades con el motor de IA.',
    highlights: [
      'Operaciones Booleanas CSG en Tiempo Real: Capacidad de realizar cortes, sustracciones (Difference), uniones e intersecciones entre piezas paramétricas en vivo mediante Three-BVH-CSG, con horneado permanente a geometrías optimizadas (bake).',
      '4 Nuevas Primitivas Paramétricas: Incorporación de chamfer_box (caja con bisel/chaflán), pipe (tubo hueco cilíndrico de grosor ajustable), prism (prismas regulares de 3 a 8 lados) y pyramid (pirámides regulares y truncadas).',
      'Modificadores de Array No Destructivos: Duplicación en serie lineal (ejes X, Y, Z con espaciado) y radial (distribución circular con radio y ángulo) con opción de despliegue a componentes independientes.',
      'Sistema de Alineación de Precisión & Face Magnet: Asentamiento exacto al suelo (Y=0.00), centrado en ejes, snap multi-paso de posición/ángulo y herramienta de Imán a Caras con alineación por vector normal para ensamblaje mecánico sin holguras.',
      'Exportador Godot 4 & GLB Perfeccionado: Reparación completa de los mapas de normales y rugosidad en la exportación GLB, deduplicación de materiales para evitar saturar el FileSystem de Godot y nuevo botón de descarga "Paquete Godot 4 (.zip)" con escena .tscn (rutas relativas sin UIDs corruptos), modelo .glb y script .gd listos.',
      'Conmutador de Estilo Visual (Dark Profesional vs Retro PS1): Selector de tema visual accesible desde la barra superior y menú para alternar entre el clásico modo Cyber-Industrial PS1 y un tema oscuro moderno, limpio y de alto contraste para largas sesiones de modelado.',
      'IA Generativa Sincronizada: El modelo de IA y el sintetizador procedural ahora conocen y aplican activamente todas las nuevas primitivas, cortes booleanos y modificadores de array para generar modelos con un nivel de detalle y complejidad muy superior dentro del presupuesto low-poly.',
      'Soporte Nativo de Escritorio (Tauri v2): Guardado de proyectos en carpetas personalizadas del sistema, enlaces externos seguros al navegador y sincronización de sesiones de cuenta.'
    ],
    tags: ['CSG Booleans', 'Godot 4', 'Primitivas Avanzadas', 'Array Modifier', 'Face Magnet', 'Dark Theme', 'IA Generativa', 'Tauri Desktop'],
    author: 'Franciscuarto'
  },
  {
    version: 'v2.5.0',
    date: '18 de Octubre, 2026',
    badge: 'FEATURE',
    badgeColor: 'var(--ps1-gold)',
    title: 'Refactor de IA Generativa (5 Leyes 3D), Exportador de Colisiones para Godot 4 y Limpieza de Cabecera',
    summary: 'Reestructuración integral del generador por IA en Studio para eliminar piezas flotantes y desordenadas mediante 5 Leyes de Construcción 3D y temperatura 0.2. Se incorpora soporte completo para exportar colisionadores compatibles con Godot 4 y generación automática de escenas .tscn. La barra de navegación se rediseña para mantener únicamente lo esencial visible.',
    highlights: [
      'IA Generativa Refinada: Se inyectan las 5 Leyes de Construcción 3D (Anclaje al suelo Y=0, Cero piezas flotantes, Rotaciones ortogonales en grados, Jerarquía mecánica y Simetría bilateral).',
      'Reducción de temperatura a 0.2 y modelos de respaldo ultrarrápidos (gemini-2.0-flash y gemini-1.5-flash) para eliminar tiempos de espera.',
      'Auto-Grounding Matemático: El motor calcula el Bounding Box 3D de cualquier especificación generada y la asienta automáticamente en el suelo (Y=0).',
      'Integración Godot 4: Opción de exportación GLB con sufijos de colisión (-convcol y -col) y generación de archivo de escena lista .tscn con StaticBody3D y CollisionShape3D.',
      'Rediseño de Consola Insignia: sci_bridge_console_curved reconstruida de 9 a 30 piezas hiperdetalladas con cero holguras mecánicas.',
      'Nueva Cabecera Limpia: Menú desplegable [⋯ MÁS ▼] que agrupa Devlog, Documentación, Inventario, Cómo funciona y enlaces de proyecto.',
      'Inauguración de la sección oficial de Devlog y Registro de Vuelo.'
    ],
    tags: ['IA Generativa', 'Godot 4', 'Modelado 3D', 'Colisiones', 'UI/UX'],
    author: 'Franciscuarto'
  },
  {
    version: 'v2.4.0',
    date: '17-18 de Octubre, 2026',
    badge: 'MILESTONE',
    badgeColor: 'var(--ps1-cyan)',
    title: '100 Modelos Modulares Procedurales en 5 Lotes Temáticos',
    summary: 'Construcción e integración de 100 modelos procedurales 100% editables en el navegador mediante ModelSpec y Three.js, listos para exportar a GLB con geometrías limpias y materiales PBR.',
    highlights: [
      'Lote 1 (Arquitectura y Habitáculos): Compuertas estancas, esclusas de descompresión, pasillos modulares, literas de tripulación y ventanas de observación.',
      'Lote 2 (Consolas, Red Eléctrica y Servidores): Racks de servidores de telecomunicaciones, transformadores de alto voltaje, consolas curvas y terminales de mando.',
      'Lote 3 (Laboratorio, Medicina y Criogenia): Cápsulas de estasis criogénica, analizadores genéticos, camillas quirúrgicas y mesas de autopsia.',
      'Lote 4 (Carga, Contención e Infraestructura): Palets industriales, contenedores de materiales peligrosos, estanterías pesadas y grúas de bahía.',
      'Lote 5 (Seguridad, Sensores y Señalética): Cámaras de seguridad con paneo, balizas estroboscópicas, paneles de alarma de fuego y señalética de peligro.',
      'Desglose en componentes individuales editables directamente dentro de Studio 3D.'
    ],
    tags: ['Catálogo', 'Modelos 3D', 'Modular', 'Three.js'],
    author: 'Franciscuarto'
  },
  {
    version: 'v2.3.0',
    date: '17 de Octubre, 2026',
    badge: 'FEATURE',
    badgeColor: '#38a169',
    title: 'Autenticación Supabase, Borradores en la Nube e Inventario de Piloto',
    summary: 'Se introduce persistencia en la nube mediante Supabase Auth y Base de Datos, permitiendo a los usuarios registrarse con GitHub OAuth o correo electrónico y sincronizar sus proyectos.',
    highlights: [
      'Inicio de sesión seguro con GitHub OAuth y Magic Link / Password mediante Supabase.',
      'Sincronización de borradores entre diferentes navegadores y dispositivos.',
      'Sistema de Favoritos para marcar modelos clave del catálogo.',
      'Colecciones de modelos para organizar kits temáticos listos para desarrollo de juegos.',
      'Widget de perfil de piloto en la cabecera con acceso directo al inventario.'
    ],
    tags: ['Autenticación', 'Supabase', 'Cloud Storage', 'Inventario'],
    author: 'Franciscuarto'
  },
  {
    version: 'v2.2.0',
    date: '16-17 de Octubre, 2026',
    badge: 'FEATURE',
    badgeColor: '#805ad5',
    title: 'Sistema de Animaciones Declarativas, Curvas de Aceleración y CodeSandbox',
    summary: 'Potente motor de animación para dotar de movimiento a los modelos 3D procedurales y exportar pistas cinemáticas dentro del estándar GLB.',
    highlights: [
      'AnimationEngine: Pistas declarativas para rotación, traslación y escala de piezas individuales.',
      'Curvas de interpolación mecánica y perfiles easing (linear, ease-in-out, bounce, step).',
      'Exportador GLB con pistas de animación embebidas compatibles con Godot AnimationPlayer y Unity Animator.',
      'CodeSandbox para programar componentes y jerarquías dinámicamente con JavaScript.',
      'Grabador de video en bucle WebM para compartir clips en redes sociales y fichas técnicas.'
    ],
    tags: ['Animaciones', 'GLB', 'CodeSandbox', 'Gamedev'],
    author: 'Franciscuarto'
  },
  {
    version: 'v2.1.0',
    date: '16 de Octubre, 2026',
    badge: 'IMPROVEMENT',
    badgeColor: 'var(--ps1-steel-light)',
    title: 'Biblioteca Expandida de Materiales PBR Retro (118 Texturas Procedurales)',
    summary: 'Generación algorítmica de 118 texturas procedimentales mediante Canvas 2D en tiempo de ejecución, eliminando dependencias de imágenes externas y tiempos de carga.',
    highlights: [
      '8 familias PBR completas: Metales, Construcción, Maderas, Piedras y Minerales, Plásticos y Gomas, Pantallas y Circuitos, Vidrios y Telas.',
      'Mapas normales sintéticos para dar relieve visual auténtico con muy pocos polígonos.',
      'Control de aspereza (roughness), metalicidad (metalness) y rotación UV por pieza.',
      'Mapeo UV anti-estiramiento adaptativo para prismas rectangulares, cilindros y cuñas.'
    ],
    tags: ['Texturas PBR', 'Canvas 2D', 'Retro PS1', 'Shading'],
    author: 'Franciscuarto'
  },
  {
    version: 'v2.0.0',
    date: '15-16 de Octubre, 2026',
    badge: 'MAJOR',
    badgeColor: '#e53e3e',
    title: 'Rediseño Total de Studio 3D v2.0 (Outliner, Gizmos y 8 Primitivas)',
    summary: 'Transformación del editor en un entorno de modelado procedural completo tipo suite de modelado PS1 en tiempo real.',
    highlights: [
      'Outliner jerárquico con emparentamiento entre piezas (parentId), duplicación, renombramiento y control de visibilidad.',
      '8 primitivas geométricas básicas: caja, cilindro, esfera, cuña, cono, toroide, cápsula y plano.',
      'Gizmos de transformación visuales (Mover, Rotar, Escalar) con imantado de cuadrícula (snap).',
      'Exportación con un solo clic a formato GLB, código Three.js, scripts C# para Unity y GDScript para Godot 4.'
    ],
    tags: ['Studio 3D', 'Editor', 'Outliner', 'Transform Gizmos'],
    author: 'Franciscuarto'
  },
  {
    version: 'v1.0.0',
    date: 'Octubre, 2026',
    badge: 'MILESTONE',
    badgeColor: 'var(--ps1-steel)',
    title: 'Lanzamiento Inicial de ModelCoder',
    summary: 'Nace ModelCoder como una biblioteca abierta de modelos 3D procedurales low-poly para desarrolladores de videojuegos independientes.',
    highlights: [
      'Catálogo inicial de generadores paramétricos y modelos utilitarios.',
      'Visor interactivo WebGL con estética CRT retro.',
      'Descarga directa de archivos GLB universales optimizados.'
    ],
    tags: ['Lanzamiento', 'Open Source', 'Low Poly', 'Game Assets'],
    author: 'Franciscuarto'
  }
];
