import type { ModularModelEntry } from './modular-catalog.ts';

export const MODULAR_MODELS_LOTE_5: ModularModelEntry[] = [
  // -------------------------------------------------------------------------
  // 01. TORRETA CENTINELA AUTOMATIZADA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_automated_sentry_turret',
    family: 'sci_automated_sentry_turret',
    name: 'Torreta Centinela Automatizada',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Sistema defensivo autónomo con base de trípode pesada, cabeza giratoria con doble cañón de pulso, telémetro óptico y sensor de rastreo.',
    tags: ['torreta', 'centinela', 'defensa', 'seguridad', 'laser', 'arma', 'canon'],
    dimensions: { width: 0.95, height: 1.45, depth: 0.95 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_automated_sentry_turret.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_automated_sentry_turret',
      name: 'Torreta Centinela Automatizada',
      category: 'fixtures',
      description: 'Sistema defensivo autónomo con base de trípode pesada, cabeza giratoria con doble cañón de pulso, telémetro óptico y sensor de rastreo.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.45, depth: 0.95 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_tripode_pesada',
          shape: 'cylinder',
          size: [0.45, 0.45, 0.12, 6],
          position: [0, 0.06, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'mastil_eje_elevacion',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.45, 12],
          position: [0, 0.34, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'cuerpo_torreta_blindada',
          shape: 'box',
          size: [0.42, 0.35, 0.55],
          position: [0, 0.72, 0],
          color: '#334155',
          texturePreset: 'carbon_fiber',
          roughness: 0.4,
          metalness: 0.6
        },
        {
          name: 'canon_pulso_izq',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.65, 8],
          position: [-0.15, 0.72, 0.45],
          rotation: [Math.PI / 2, 0, 0],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.9
        },
        {
          name: 'canon_pulso_der',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.65, 8],
          position: [0.15, 0.72, 0.45],
          rotation: [Math.PI / 2, 0, 0],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.9
        },
        {
          name: 'bocacha_compensador_izq',
          shape: 'cylinder',
          size: [0.045, 0.045, 0.08, 8],
          position: [-0.15, 0.72, 0.78],
          rotation: [Math.PI / 2, 0, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'bocacha_compensador_der',
          shape: 'cylinder',
          size: [0.045, 0.045, 0.08, 8],
          position: [0.15, 0.72, 0.78],
          rotation: [Math.PI / 2, 0, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'modulo_telemetro_sensor',
          shape: 'box',
          size: [0.22, 0.12, 0.16],
          position: [0, 0.95, -0.05],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'lente_optico_infrarrojo',
          shape: 'sphere',
          size: [0.05, 8, 8],
          position: [0, 0.95, 0.05],
          color: '#ef4444',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 02. MOLINETE DE SEGURIDAD CON ESCÁNER BIOMÉTRICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_biometric_security_turnstile',
    family: 'sci_biometric_security_turnstile',
    name: 'Molinete de Seguridad Biométrico',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Control de acceso peatonal con aspas batientes de cristal templado, lector de palma dactilar y semáforo LED de paso.',
    tags: ['molinete', 'torniquete', 'acceso', 'biometrico', 'seguridad', 'control', 'puerta'],
    dimensions: { width: 0.95, height: 1.15, depth: 1.20 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_biometric_security_turnstile.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_biometric_security_turnstile',
      name: 'Molinete de Seguridad Biométrico',
      category: 'fixtures',
      description: 'Control de acceso peatonal con aspas batientes de cristal templado, lector de palma dactilar y semáforo LED de paso.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.15, depth: 1.20 },
      palette: 'clean_lab',
      components: [
        {
          name: 'columna_cuerpo_acero_izq',
          shape: 'box',
          size: [0.22, 1.05, 1.15],
          position: [-0.35, 0.525, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'columna_cuerpo_acero_der',
          shape: 'box',
          size: [0.22, 1.05, 1.15],
          position: [0.35, 0.525, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'aspa_cristal_batiente_izq',
          shape: 'box',
          size: [0.24, 0.65, 0.02],
          position: [-0.14, 0.70, 0],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.5,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'aspa_cristal_batiente_der',
          shape: 'box',
          size: [0.24, 0.65, 0.02],
          position: [0.14, 0.70, 0],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.5,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'lector_biometrico_palma_izq',
          shape: 'box',
          size: [0.12, 0.03, 0.16],
          position: [-0.35, 1.06, 0.25],
          color: '#10b981',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'lector_biometrico_palma_der',
          shape: 'box',
          size: [0.12, 0.03, 0.16],
          position: [0.35, 1.06, 0.25],
          color: '#10b981',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'indicador_paso_semaforo_izq',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.02, 10],
          position: [-0.35, 0.85, 0.58],
          color: '#22c55e',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'indicador_paso_semaforo_der',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.02, 10],
          position: [0.35, 0.85, 0.58],
          color: '#22c55e',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 03. MESA TÁCTICA HOLOGRÁFICA DE MANDO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_tactical_holo_table_briefing',
    family: 'sci_tactical_holo_table_briefing',
    name: 'Mesa Táctica Holográfica de Mando',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Mesa de operaciones para reuniones estratégicas con proyector volumétrico 3D de terreno, controles táctiles y bisel de aluminio oscuro.',
    tags: ['mesa', 'tactica', 'holograma', 'mando', 'estrategia', 'mapa', 'briefing'],
    dimensions: { width: 1.50, height: 1.35, depth: 1.50 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_tactical_holo_table_briefing.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_tactical_holo_table_briefing',
      name: 'Mesa Táctica Holográfica de Mando',
      category: 'fixtures',
      description: 'Mesa de operaciones para reuniones estratégicas con proyector volumétrico 3D de terreno, controles táctiles y bisel de aluminio oscuro.',
      units: 'meters',
      dimensions: { width: 1.50, height: 1.35, depth: 1.50 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'pedestal_central_lastrado',
          shape: 'cylinder',
          size: [0.45, 0.45, 0.65, 12],
          position: [0, 0.325, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'anillo_soporte_base',
          shape: 'ring',
          size: [0.65, 0.08, 12],
          position: [0, 0.04, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'tablero_hexagonal_marco',
          shape: 'cylinder',
          size: [0.75, 0.75, 0.12, 6],
          position: [0, 0.71, 0],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'anillo_proyector_laser_focal',
          shape: 'cylinder',
          size: [0.48, 0.48, 0.04, 16],
          position: [0, 0.78, 0],
          color: '#0284c7',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'holograma_terreno_tactico',
          shape: 'cone',
          size: [0.38, 0.38, 0.35, 8],
          position: [0, 1.05, 0],
          color: '#00e5ff',
          opacity: 0.45,
          roughness: 0.05,
          metalness: 0.0
        },
        {
          name: 'consola_perimetral_mandos_1',
          shape: 'box',
          size: [0.28, 0.04, 0.12],
          position: [0, 0.78, 0.58],
          color: '#1e293b',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'consola_perimetral_mandos_2',
          shape: 'box',
          size: [0.28, 0.04, 0.12],
          position: [0, 0.78, -0.58],
          color: '#1e293b',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 04. POSTE SENSOR DE MOVIMIENTO PERIMETRAL
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_perimeter_motion_sensor_post',
    family: 'sci_perimeter_motion_sensor_post',
    name: 'Poste Sensor de Movimiento Perimetral',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Poste detector perimetral con radomo microondas giratorio, sensores infrarrojos pasivos de intrusión y antena de enlace UHF.',
    tags: ['sensor', 'movimiento', 'perimetro', 'seguridad', 'radar', 'antena', 'intrusos'],
    dimensions: { width: 0.55, height: 1.85, depth: 0.55 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_perimeter_motion_sensor_post.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_perimeter_motion_sensor_post',
      name: 'Poste Sensor de Movimiento Perimetral',
      category: 'fixtures',
      description: 'Poste detector perimetral con radomo microondas giratorio, sensores infrarrojos pasivos de intrusión y antena de enlace UHF.',
      units: 'meters',
      dimensions: { width: 0.55, height: 1.85, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_placa_anclaje_suelo',
          shape: 'box',
          size: [0.45, 0.06, 0.45],
          position: [0, 0.03, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'columna_tubular_acero',
          shape: 'cylinder',
          size: [0.06, 0.06, 1.35, 10],
          position: [0, 0.72, 0],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'modulo_radomo_microondas',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.22, 12],
          position: [0, 1.48, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'antena_enlace_uhf',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.35, 6],
          position: [0, 1.76, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'lente_pir_frontal',
          shape: 'sphere',
          size: [0.05, 8, 8],
          position: [0, 1.48, 0.18],
          color: '#ef4444',
          roughness: 0.15,
          metalness: 0.0
        },
        {
          name: 'caja_empalmes_cables',
          shape: 'box',
          size: [0.18, 0.22, 0.12],
          position: [0, 0.65, -0.08],
          color: '#334155',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 05. BARRICADA TÁCTICA DESPLEGABLE DE ASALTO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_heavy_blast_door_barricade',
    family: 'sci_heavy_blast_door_barricade',
    name: 'Barricada Táctica Desplegable',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Parapeto balístico pesado para contención de pasillos con aspilleras blindadas, estabilizadores hidráulicos y franjas de peligro.',
    tags: ['barricada', 'tactica', 'balistica', 'parapeto', 'asalto', 'seguridad', 'escudo'],
    dimensions: { width: 1.60, height: 1.25, depth: 0.80 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_heavy_blast_door_barricade.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_heavy_blast_door_barricade',
      name: 'Barricada Táctica Desplegable',
      category: 'fixtures',
      description: 'Parapeto balístico pesado para contención de pasillos con aspilleras blindadas, estabilizadores hidráulicos y franjas de peligro.',
      units: 'meters',
      dimensions: { width: 1.60, height: 1.25, depth: 0.80 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'pantalla_blindada_frontal',
          shape: 'box',
          size: [1.50, 1.05, 0.10],
          position: [0, 0.60, 0],
          color: '#334155',
          texturePreset: 'carbon_fiber',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'pie_estabilizador_izq',
          shape: 'box',
          size: [0.12, 0.08, 0.75],
          position: [-0.60, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'pie_estabilizador_der',
          shape: 'box',
          size: [0.12, 0.08, 0.75],
          position: [0.60, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'aspillera_visor_blindado',
          shape: 'box',
          size: [0.55, 0.08, 0.12],
          position: [0, 0.90, 0],
          color: '#38bdf8',
          texturePreset: 'reinforced_glass',
          opacity: 0.6,
          roughness: 0.15,
          metalness: 0.1
        },
        {
          name: 'franja_seguridad_baja',
          shape: 'box',
          size: [1.52, 0.12, 0.02],
          position: [0, 0.15, 0.06],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'refuerzo_puntal_trasero_izq',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.70, 8],
          position: [-0.55, 0.45, -0.25],
          rotation: [-0.6, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'refuerzo_puntal_trasero_der',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.70, 8],
          position: [0.55, 0.45, -0.25],
          rotation: [-0.6, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 06. ESTACIÓN MURAL DE LANZAMIENTO DE DRONES CENTINELA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_surveillance_drone_dock',
    family: 'sci_surveillance_drone_dock',
    name: 'Estación de Lanzamiento de Drones Centinela',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Hangar mural para dron autónomo de patrulla con cuna de carga inductiva magnética, compuerta basculante y panel de telemetría.',
    tags: ['dron', 'hangar', 'patrulla', 'centinela', 'lanzamiento', 'recarga', 'seguridad'],
    dimensions: { width: 0.85, height: 0.90, depth: 0.65 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_surveillance_drone_dock.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_surveillance_drone_dock',
      name: 'Estación de Lanzamiento de Drones Centinela',
      category: 'fixtures',
      description: 'Hangar mural para dron autónomo de patrulla con cuna de carga inductiva magnética, compuerta basculante y panel de telemetría.',
      units: 'meters',
      dimensions: { width: 0.85, height: 0.90, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'soporte_placa_mural',
          shape: 'box',
          size: [0.80, 0.85, 0.08],
          position: [0, 0.55, -0.25],
          color: '#1e293b',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'cuna_plataforma_atraque',
          shape: 'box',
          size: [0.70, 0.10, 0.55],
          position: [0, 0.25, 0.05],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.85
        },
        {
          name: 'chasis_dron_acoplado',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.10, 8],
          position: [0, 0.42, 0.05],
          color: '#0f172a',
          texturePreset: 'carbon_fiber',
          roughness: 0.4,
          metalness: 0.6
        },
        {
          name: 'brazo_rotor_so',
          shape: 'box',
          size: [0.03, 0.02, 0.24],
          position: [-0.15, 0.45, -0.10],
          rotation: [0, 0.78, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'brazo_rotor_ne',
          shape: 'box',
          size: [0.03, 0.02, 0.24],
          position: [0.15, 0.45, 0.20],
          rotation: [0, 0.78, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'sensor_ojo_dron',
          shape: 'sphere',
          size: [0.04, 8, 8],
          position: [0, 0.38, 0.22],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'panel_telemetria_vuelo',
          shape: 'box',
          size: [0.24, 0.18, 0.03],
          position: [0, 0.80, -0.20],
          color: '#06b6d4',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 07. COLUMNA BALIZA DE ALARMA SONORA Y ÓPTICA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_emergency_alarm_beacon_pillar',
    family: 'sci_emergency_alarm_beacon_pillar',
    name: 'Columna Baliza de Alarma Sonora y Óptica',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Poste de emergencia para alerta de evacuación con sirena omnidireccional de bocina, luces de xenón rojas y pulsador tipo seta.',
    tags: ['alarma', 'sirena', 'baliza', 'emergencia', 'evacuacion', 'seguridad', 'poste'],
    dimensions: { width: 0.50, height: 1.85, depth: 0.50 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_emergency_alarm_beacon_pillar.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_emergency_alarm_beacon_pillar',
      name: 'Columna Baliza de Alarma Sonora y Óptica',
      category: 'fixtures',
      description: 'Poste de emergencia para alerta de evacuación con sirena omnidireccional de bocina, luces de xenón rojas y pulsador tipo seta.',
      units: 'meters',
      dimensions: { width: 0.50, height: 1.85, depth: 0.50 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_pedestal_suelo',
          shape: 'box',
          size: [0.45, 0.08, 0.45],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'columna_franjas_seguridad',
          shape: 'box',
          size: [0.25, 1.45, 0.25],
          position: [0, 0.805, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'sirena_bocina_radial',
          shape: 'cylinder',
          size: [0.20, 0.20, 0.16, 12],
          position: [0, 1.58, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'baliza_xenon_roja',
          shape: 'cylinder',
          size: [0.12, 0.12, 0.15, 10],
          position: [0, 1.74, 0],
          color: '#ef4444',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'caja_pulsador_emergencia',
          shape: 'box',
          size: [0.14, 0.18, 0.06],
          position: [0, 1.10, 0.15],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'boton_seta_paro_sos',
          shape: 'cylinder',
          size: [0.045, 0.045, 0.04, 10],
          position: [0, 1.10, 0.19],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dc2626',
          roughness: 0.2,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 08. ARMERO DE SEGURIDAD MURAL PARA RIFLES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_weapon_lockbox_wall',
    family: 'sci_weapon_lockbox_wall',
    name: 'Armero de Seguridad Mural para Rifles',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Armero vertical blindado de pared con abrazaderas electromagnéticas para armas de asalto y teclado de código de seguridad.',
    tags: ['armero', 'armas', 'seguridad', 'mural', 'fusil', 'rifle', 'bloqueo'],
    dimensions: { width: 0.90, height: 1.55, depth: 0.35 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_weapon_lockbox_wall.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_weapon_lockbox_wall',
      name: 'Armero de Seguridad Mural para Rifles',
      category: 'fixtures',
      description: 'Armero vertical blindado de pared con abrazaderas electromagnéticas para armas de asalto y teclado de código de seguridad.',
      units: 'meters',
      dimensions: { width: 0.90, height: 1.55, depth: 0.35 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_caja_blindada_mural',
          shape: 'box',
          size: [0.85, 1.50, 0.25],
          position: [0, 0.85, 0],
          color: '#1e293b',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'panel_fondo_ranurado',
          shape: 'box',
          size: [0.78, 1.42, 0.02],
          position: [0, 0.85, -0.10],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.75
        },
        {
          name: 'abrazadera_arma_izq',
          shape: 'box',
          size: [0.18, 0.08, 0.12],
          position: [-0.22, 1.05, 0.02],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.2
        },
        {
          name: 'abrazadera_arma_der',
          shape: 'box',
          size: [0.18, 0.08, 0.12],
          position: [0.22, 1.05, 0.02],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.2
        },
        {
          name: 'rifle_tactico_slot_1',
          shape: 'box',
          size: [0.08, 0.85, 0.12],
          position: [-0.22, 0.85, 0.04],
          color: '#334155',
          texturePreset: 'carbon_fiber',
          roughness: 0.4,
          metalness: 0.6
        },
        {
          name: 'rifle_tactico_slot_2',
          shape: 'box',
          size: [0.08, 0.85, 0.12],
          position: [0.22, 0.85, 0.04],
          color: '#334155',
          texturePreset: 'carbon_fiber',
          roughness: 0.4,
          metalness: 0.6
        },
        {
          name: 'teclado_bloqueo_biometrico',
          shape: 'box',
          size: [0.14, 0.22, 0.04],
          position: [0, 1.35, 0.12],
          color: '#3b82f6',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 09. ARCO DETECTOR DE METALES Y RADIACIÓN
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_security_checkpoint_scanner',
    family: 'sci_security_checkpoint_scanner',
    name: 'Arco Detector de Seguridad y Radiación',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Pórtico detector de metales, armas y radiación gamma para control de personal con bobinas de inducción y baliza de alerta.',
    tags: ['arco', 'detector', 'escaner', 'metales', 'radiacion', 'control', 'checkpoint'],
    dimensions: { width: 1.25, height: 2.25, depth: 0.65 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_security_checkpoint_scanner.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_security_checkpoint_scanner',
      name: 'Arco Detector de Seguridad y Radiación',
      category: 'fixtures',
      description: 'Pórtico detector de metales, armas y radiación gamma para control de personal con bobinas de inducción y baliza de alerta.',
      units: 'meters',
      dimensions: { width: 1.25, height: 2.25, depth: 0.65 },
      palette: 'clean_lab',
      components: [
        {
          name: 'panel_lateral_izq',
          shape: 'box',
          size: [0.15, 2.20, 0.60],
          position: [-0.48, 1.10, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'panel_lateral_der',
          shape: 'box',
          size: [0.15, 2.20, 0.60],
          position: [0.48, 1.10, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'dintel_cabezal_superior',
          shape: 'box',
          size: [1.11, 0.20, 0.60],
          position: [0, 2.10, 0],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'alfombra_peso_calibrada',
          shape: 'box',
          size: [0.81, 0.02, 0.60],
          position: [0, 0.01, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'franja_led_zona_izq',
          shape: 'box',
          size: [0.02, 1.80, 0.02],
          position: [-0.39, 1.10, 0.28],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'franja_led_zona_der',
          shape: 'box',
          size: [0.02, 1.80, 0.02],
          position: [0.39, 1.10, 0.28],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'pantalla_diagnostico_cabezal',
          shape: 'box',
          size: [0.32, 0.12, 0.02],
          position: [0, 2.10, 0.31],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 10. TÓTEM DE SEÑALÉTICA TÁCTICA Y EVACUACIÓN
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_tactical_wayfinding_totem',
    family: 'sci_tactical_wayfinding_totem',
    name: 'Tótem de Señalética Táctica y Evacuación',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Columna luminosa de información para pasillos con mapa de sectores, flechas de evacuación y baliza de alerta superior.',
    tags: ['totem', 'senaletica', 'evacuacion', 'mapa', 'rutas', 'informacion', 'emergencia'],
    dimensions: { width: 0.65, height: 2.10, depth: 0.45 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_tactical_wayfinding_totem.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_tactical_wayfinding_totem',
      name: 'Tótem de Señalética Táctica y Evacuación',
      category: 'fixtures',
      description: 'Columna luminosa de información para pasillos con mapa de sectores, flechas de evacuación y baliza de alerta superior.',
      units: 'meters',
      dimensions: { width: 0.65, height: 2.10, depth: 0.45 },
      palette: 'clean_lab',
      components: [
        {
          name: 'plinto_base_lastrada',
          shape: 'box',
          size: [0.65, 0.08, 0.45],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'cuerpo_totem_vertical',
          shape: 'box',
          size: [0.55, 1.90, 0.25],
          position: [0, 1.03, 0],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.75
        },
        {
          name: 'panel_plano_sector_estacion',
          shape: 'box',
          size: [0.48, 0.65, 0.02],
          position: [0, 1.45, 0.13],
          color: '#0284c7',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'flecha_evacuacion_verde',
          shape: 'box',
          size: [0.48, 0.18, 0.02],
          position: [0, 0.95, 0.13],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'franja_hazard_base',
          shape: 'box',
          size: [0.55, 0.12, 0.02],
          position: [0, 0.20, 0.13],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'baliza_indicador_techo',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.08, 12],
          position: [0, 2.02, 0],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 11. EMISOR / RECEPTOR DE BARRERA LÁSER
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_laser_tripwire_emitter',
    family: 'sci_laser_tripwire_emitter',
    name: 'Emisor de Barrera Láser de Intrusión',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Poste compacto detector de intrusión mediante haz colimado de luz láser roja con lente prismática y transmisor cifrado.',
    tags: ['laser', 'barrera', 'intrusos', 'tripwire', 'sensor', 'alarma', 'infrarrojo'],
    dimensions: { width: 0.35, height: 1.10, depth: 0.35 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_laser_tripwire_emitter.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_laser_tripwire_emitter',
      name: 'Emisor de Barrera Láser de Intrusión',
      category: 'fixtures',
      description: 'Poste compacto detector de intrusión mediante haz colimado de luz láser roja con lente prismática y transmisor cifrado.',
      units: 'meters',
      dimensions: { width: 0.35, height: 1.10, depth: 0.35 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_anclaje_pernos',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.06, 8],
          position: [0, 0.03, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'columna_soporte_cilindrica',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.75, 10],
          position: [0, 0.43, 0],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'cabezal_emisor_prisma',
          shape: 'box',
          size: [0.16, 0.24, 0.18],
          position: [0, 0.92, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'lente_colimadora_laser',
          shape: 'cylinder',
          size: [0.045, 0.045, 0.04, 12],
          position: [0, 0.92, 0.10],
          rotation: [Math.PI / 2, 0, 0],
          color: '#ef4444',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'antena_transmisora_enlace',
          shape: 'cylinder',
          size: [0.008, 0.008, 0.20, 6],
          position: [0.05, 1.10, -0.05],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 12. ESTACIÓN DOSIMÉTRICA Y SENSOR GAMMA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_radiation_survey_meter_post',
    family: 'sci_radiation_survey_meter_post',
    name: 'Estación Dosimétrica y Sensor Gamma',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Poste industrial detector de radiación ionizante con cámara de gas sellada, tubo Geiger cilíndrico y pantalla digital en Sieverts.',
    tags: ['radiacion', 'geiger', 'gamma', 'dosimetro', 'nuclear', 'hazmat', 'sievert'],
    dimensions: { width: 0.45, height: 1.45, depth: 0.45 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_radiation_survey_meter_post.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_radiation_survey_meter_post',
      name: 'Estación Dosimétrica y Sensor Gamma',
      category: 'fixtures',
      description: 'Poste industrial detector de radiación ionizante con cámara de gas sellada, tubo Geiger cilíndrico y pantalla digital en Sieverts.',
      units: 'meters',
      dimensions: { width: 0.45, height: 1.45, depth: 0.45 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'pie_bancada_hierro',
          shape: 'box',
          size: [0.40, 0.08, 0.40],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'mastil_soporte_acero',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.85, 8],
          position: [0, 0.50, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'caja_contador_geiger',
          shape: 'box',
          size: [0.28, 0.35, 0.22],
          position: [0, 1.05, 0],
          color: '#facc15',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'tubo_detector_gamma_blindado',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.28, 12],
          position: [0.18, 1.05, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'pantalla_sieverts_lcd',
          shape: 'box',
          size: [0.18, 0.12, 0.01],
          position: [0, 1.10, 0.115],
          color: '#ef4444',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'rombo_trebol_radiacion',
          shape: 'box',
          size: [0.14, 0.14, 0.01],
          position: [0, 0.95, 0.115],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 13. CLÚSTER MURAL DE MONITORIZACIÓN CCTV
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_security_monitor_wall_cluster',
    family: 'sci_security_monitor_wall_cluster',
    name: 'Clúster Mural de Monitorización CCTV',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Matriz articulada de cuatro monitores de alta resolución para videovigilancia y control de accesos con brazo basculante VESA.',
    tags: ['cctv', 'monitores', 'seguridad', 'camaras', 'vigilancia', 'pantallas', 'video'],
    dimensions: { width: 1.55, height: 1.15, depth: 0.40 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_security_monitor_wall_cluster.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_security_monitor_wall_cluster',
      name: 'Clúster Mural de Monitorización CCTV',
      category: 'fixtures',
      description: 'Matriz articulada de cuatro monitores de alta resolución para videovigilancia y control de accesos con brazo basculante VESA.',
      units: 'meters',
      dimensions: { width: 1.55, height: 1.15, depth: 0.40 },
      palette: 'clean_lab',
      components: [
        {
          name: 'placa_anclaje_mural_vesa',
          shape: 'box',
          size: [0.45, 0.45, 0.05],
          position: [0, 0.60, -0.15],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'brazo_articulado_soporte',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.25, 8],
          position: [0, 0.60, -0.05],
          rotation: [Math.PI / 2, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'marco_matriz_4_monitores',
          shape: 'box',
          size: [1.45, 0.95, 0.04],
          position: [0, 0.60, 0.08],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pantalla_camara_1_so',
          shape: 'box',
          size: [0.65, 0.40, 0.01],
          position: [-0.35, 0.38, 0.105],
          color: '#0284c7',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'pantalla_camara_2_se',
          shape: 'box',
          size: [0.65, 0.40, 0.01],
          position: [0.35, 0.38, 0.105],
          color: '#0284c7',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'pantalla_camara_3_no',
          shape: 'box',
          size: [0.65, 0.40, 0.01],
          position: [-0.35, 0.82, 0.105],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'pantalla_camara_4_ne',
          shape: 'box',
          size: [0.65, 0.40, 0.01],
          position: [0.35, 0.82, 0.105],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 14. PILÓN SUPRESOR DE PULSO ELECTROMAGNÉTICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_emp_suppressor_pylon',
    family: 'sci_emp_suppressor_pylon',
    name: 'Pilón Supresor de Pulso Electromagnético',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Poste de protección contra ataques EMP con bobinas de choque toroidal en cascada, disipador a tierra y terminal de alto voltaje.',
    tags: ['emp', 'supresor', 'bobina', 'defensa', 'electricidad', 'proteccion', 'pilon'],
    dimensions: { width: 0.70, height: 1.95, depth: 0.70 },
    triBudget: '420-500',
    glbUrl: '/models/modular/sci_emp_suppressor_pylon.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_emp_suppressor_pylon',
      name: 'Pilón Supresor de Pulso Electromagnético',
      category: 'fixtures',
      description: 'Poste de protección contra ataques EMP con bobinas de choque toroidal en cascada, disipador a tierra y terminal de alto voltaje.',
      units: 'meters',
      dimensions: { width: 0.70, height: 1.95, depth: 0.70 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_zapata_aislada',
          shape: 'cylinder',
          size: [0.35, 0.35, 0.10, 8],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'columna_aislador_ceramico',
          shape: 'cylinder',
          size: [0.12, 0.12, 1.45, 12],
          position: [0, 0.825, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'bobina_toroidal_cobre_baja',
          shape: 'torus',
          size: [0.24, 0.05, 10, 16],
          position: [0, 0.45, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'bobina_toroidal_cobre_media',
          shape: 'torus',
          size: [0.24, 0.05, 10, 16],
          position: [0, 0.85, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'bobina_toroidal_cobre_alta',
          shape: 'torus',
          size: [0.24, 0.05, 10, 16],
          position: [0, 1.25, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'esfera_terminal_disipadora',
          shape: 'sphere',
          size: [0.18, 12, 12],
          position: [0, 1.70, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.15,
          metalness: 0.95
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 15. ARMERO DE ESCUDOS ANTIDISTURBIOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_tactical_shield_rack',
    family: 'sci_tactical_shield_rack',
    name: 'Armero de Escudos Antidisturbios',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Soporte de suelo para tres escudos balísticos transparentes reforzados con asas anatómicas y barras de carga inductiva.',
    tags: ['escudos', 'antidisturbios', 'balistica', 'armero', 'hangar', 'policia', 'seguridad'],
    dimensions: { width: 1.15, height: 1.25, depth: 0.65 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_tactical_shield_rack.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_tactical_shield_rack',
      name: 'Armero de Escudos Antidisturbios',
      category: 'fixtures',
      description: 'Soporte de suelo para tres escudos balísticos transparentes reforzados con asas anatómicas y barras de carga inductiva.',
      units: 'meters',
      dimensions: { width: 1.15, height: 1.25, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bancada_bastidor_tubular',
          shape: 'box',
          size: [1.10, 0.12, 0.60],
          position: [0, 0.06, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'guia_separador_vertical_1',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.90, 8],
          position: [-0.35, 0.55, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'guia_separador_vertical_2',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.90, 8],
          position: [0, 0.55, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'guia_separador_vertical_3',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.90, 8],
          position: [0.35, 0.55, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'escudo_balistico_1',
          shape: 'box',
          size: [0.28, 0.95, 0.04],
          position: [-0.20, 0.60, 0],
          color: '#38bdf8',
          texturePreset: 'reinforced_glass',
          opacity: 0.6,
          roughness: 0.15,
          metalness: 0.1
        },
        {
          name: 'escudo_balistico_2',
          shape: 'box',
          size: [0.28, 0.95, 0.04],
          position: [0.15, 0.60, 0],
          color: '#38bdf8',
          texturePreset: 'reinforced_glass',
          opacity: 0.6,
          roughness: 0.15,
          metalness: 0.1
        },
        {
          name: 'franja_alerta_frontal',
          shape: 'box',
          size: [1.12, 0.08, 0.02],
          position: [0, 0.08, 0.31],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 16. ESCÁNER DE RAYOS X PARA EQUIPAJES DE MANO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_contraband_cargo_scanner',
    family: 'sci_contraband_cargo_scanner',
    name: 'Escáner de Rayos X para Contrabando',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Túnel de inspección radiográfica con cortinillas plomadas, cinta transportadora y consola de análisis de densidad molecular.',
    tags: ['rayosx', 'escaner', 'contrabando', 'equipaje', 'tuv', 'seguridad', 'inspeccion'],
    dimensions: { width: 1.65, height: 1.45, depth: 0.85 },
    triBudget: '400-480',
    glbUrl: '/models/modular/sci_contraband_cargo_scanner.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_contraband_cargo_scanner',
      name: 'Escáner de Rayos X para Contrabando',
      category: 'fixtures',
      description: 'Túnel de inspección radiográfica con cortinillas plomadas, cinta transportadora y consola de análisis de densidad molecular.',
      units: 'meters',
      dimensions: { width: 1.65, height: 1.45, depth: 0.85 },
      palette: 'clean_lab',
      components: [
        {
          name: 'patas_bastidor_acero',
          shape: 'box',
          size: [1.55, 0.65, 0.75],
          position: [0, 0.325, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'cinta_transportadora_banda',
          shape: 'box',
          size: [1.65, 0.08, 0.55],
          position: [0, 0.69, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'tunel_blindado_rayosx',
          shape: 'box',
          size: [0.75, 0.65, 0.68],
          position: [0, 1.055, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.3,
          metalness: 0.15
        },
        {
          name: 'cortinilla_plomo_entrada',
          shape: 'box',
          size: [0.02, 0.55, 0.52],
          position: [-0.38, 1.01, 0],
          color: '#334155',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'cortinilla_plomo_salida',
          shape: 'box',
          size: [0.02, 0.55, 0.52],
          position: [0.38, 1.01, 0],
          color: '#334155',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'consola_pantalla_operador',
          shape: 'box',
          size: [0.35, 0.28, 0.04],
          position: [0, 1.25, 0.42],
          rotation: [-0.3, 0, 0],
          color: '#f59e0b',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 17. PEDESTAL TERMINAL DE AUTORIZACIÓN DE ESCLUSA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_airlock_authorization_keypad',
    family: 'sci_airlock_authorization_keypad',
    name: 'Pedestal Terminal de Autorización de Esclusa',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Consola ergonómica de control de paso para esclusas con teclado táctil, lector óptico de credencial y pantalla de estado de presurización.',
    tags: ['terminal', 'esclusa', 'autorizacion', 'credencial', 'acceso', 'pedestal', 'seguridad'],
    dimensions: { width: 0.55, height: 1.25, depth: 0.55 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_airlock_authorization_keypad.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_airlock_authorization_keypad',
      name: 'Pedestal Terminal de Autorización de Esclusa',
      category: 'fixtures',
      description: 'Consola ergonómica de control de paso para esclusas con teclado táctil, lector óptico de credencial y pantalla de estado de presurización.',
      units: 'meters',
      dimensions: { width: 0.55, height: 1.25, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_pedestal_angulada',
          shape: 'cylinder',
          size: [0.22, 0.22, 0.08, 8],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'fuste_columna_inclinada',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.85, 10],
          position: [0, 0.48, -0.05],
          rotation: [0.2, 0, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'cabezal_consola_tactil',
          shape: 'box',
          size: [0.36, 0.28, 0.08],
          position: [0, 0.98, 0.08],
          rotation: [-0.4, 0, 0],
          color: '#334155',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'pantalla_interfaz_autorizacion',
          shape: 'box',
          size: [0.30, 0.20, 0.01],
          position: [0, 0.99, 0.125],
          rotation: [-0.4, 0, 0],
          color: '#06b6d4',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'ranura_tarjeta_optica',
          shape: 'box',
          size: [0.12, 0.02, 0.04],
          position: [0, 0.88, 0.15],
          rotation: [-0.4, 0, 0],
          color: '#0f172a',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 18. TORRE FOCO HALÓGENO / LED DE ALTA POTENCIA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_perimeter_floodlight_tower',
    family: 'sci_perimeter_floodlight_tower',
    name: 'Torre Foco Halógeno / LED de Alta Potencia',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Foco de iluminación perimetral para pistas de aterrizaje y hangares con cabezal orientable de 4 focos LED y aletas disipadoras.',
    tags: ['foco', 'iluminacion', 'torre', 'led', 'perimetro', 'hangar', 'luz'],
    dimensions: { width: 0.85, height: 2.35, depth: 0.85 },
    triBudget: '400-480',
    glbUrl: '/models/modular/sci_perimeter_floodlight_tower.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_perimeter_floodlight_tower',
      name: 'Torre Foco Halógeno / LED de Alta Potencia',
      category: 'fixtures',
      description: 'Foco de iluminación perimetral para pistas de aterrizaje y hangares con cabezal orientable de 4 focos LED y aletas disipadoras.',
      units: 'meters',
      dimensions: { width: 0.85, height: 2.35, depth: 0.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_zapata_arriostrada',
          shape: 'box',
          size: [0.65, 0.10, 0.65],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'mastil_telescopico_acero',
          shape: 'cylinder',
          size: [0.06, 0.06, 1.95, 10],
          position: [0, 1.05, 0],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.8
        },
        {
          name: 'cruceta_soporte_focos',
          shape: 'box',
          size: [0.70, 0.06, 0.12],
          position: [0, 2.05, 0],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.85
        },
        {
          name: 'foco_led_izq_1',
          shape: 'box',
          size: [0.18, 0.14, 0.12],
          position: [-0.25, 2.15, 0.05],
          rotation: [0.2, 0, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'foco_led_der_1',
          shape: 'box',
          size: [0.18, 0.14, 0.12],
          position: [0.25, 2.15, 0.05],
          rotation: [0.2, 0, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'lente_emisor_luz_izq',
          shape: 'box',
          size: [0.16, 0.12, 0.01],
          position: [-0.25, 2.15, 0.115],
          rotation: [0.2, 0, 0],
          color: '#f8fafc',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'lente_emisor_luz_der',
          shape: 'box',
          size: [0.16, 0.12, 0.01],
          position: [0.25, 2.15, 0.115],
          rotation: [0.2, 0, 0],
          color: '#f8fafc',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 19. REPETIDOR DE COMUNICACIONES TÁCTICAS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_tactical_communications_relay',
    family: 'sci_tactical_communications_relay',
    name: 'Repetidor de Comunicaciones Tácticas',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Unidad portátil de enlace cifrado de campo con antena parabólica de bocina, analizador de radiofrecuencia y chasis militar rugerizado.',
    tags: ['comunicaciones', 'radio', 'antena', 'repetidor', 'cifrado', 'tactico', 'transmisor'],
    dimensions: { width: 0.80, height: 1.15, depth: 0.65 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_tactical_communications_relay.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_tactical_communications_relay',
      name: 'Repetidor de Comunicaciones Tácticas',
      category: 'fixtures',
      description: 'Unidad portátil de enlace cifrado de campo con antena parabólica de bocina, analizador de radiofrecuencia y chasis militar rugerizado.',
      units: 'meters',
      dimensions: { width: 0.80, height: 1.15, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_caja_rugerizada',
          shape: 'box',
          size: [0.65, 0.45, 0.45],
          position: [0, 0.225, 0],
          color: '#1e293b',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.75
        },
        {
          name: 'cantonera_goma_protectora_so',
          shape: 'box',
          size: [0.08, 0.47, 0.08],
          position: [-0.30, 0.235, -0.20],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cantonera_goma_protectora_se',
          shape: 'box',
          size: [0.08, 0.47, 0.08],
          position: [0.30, 0.235, -0.20],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'plato_parabolico_bocina',
          shape: 'cylinder',
          size: [0.24, 0.24, 0.08, 16],
          position: [0, 0.75, 0],
          rotation: [0.3, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.85
        },
        {
          name: 'alimentador_guiaondas_central',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.16, 8],
          position: [0, 0.82, 0.08],
          rotation: [0.3, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'pantalla_espectro_rf',
          shape: 'box',
          size: [0.22, 0.14, 0.01],
          position: [0, 0.28, 0.23],
          color: '#22c55e',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 20. SEÑAL HOLOGRÁFICA DE ADVERTENCIA DE PELIGRO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_hazard_warning_sign_hologram',
    family: 'sci_hazard_warning_sign_hologram',
    name: 'Señal Holográfica de Advertencia de Peligro',
    batch: 5,
    batchName: 'Seguridad, Sensores y Señalética',
    category: 'fixtures',
    description: 'Baliza de suelo proyectora de icono holográfico flotante de precaución con triángulo de advertencia y destellos estroboscópicos.',
    tags: ['holograma', 'senal', 'peligro', 'advertencia', 'precaucion', 'seguridad', 'baliza'],
    dimensions: { width: 0.60, height: 1.25, depth: 0.60 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_hazard_warning_sign_hologram.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_hazard_warning_sign_hologram',
      name: 'Señal Holográfica de Advertencia de Peligro',
      category: 'fixtures',
      description: 'Baliza de suelo proyectora de icono holográfico flotante de precaución con triángulo de advertencia y destellos estroboscópicos.',
      units: 'meters',
      dimensions: { width: 0.60, height: 1.25, depth: 0.60 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_disco_proyector_suelo',
          shape: 'cylinder',
          size: [0.28, 0.28, 0.08, 16],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'anillo_hazard_perimetral',
          shape: 'ring',
          size: [0.29, 0.04, 16],
          position: [0, 0.06, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'emisor_focal_laser_concavo',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.04, 12],
          position: [0, 0.09, 0],
          color: '#0284c7',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'holograma_triangulo_peligro',
          shape: 'cone',
          size: [0.25, 0.25, 0.35, 3],
          position: [0, 0.75, 0],
          rotation: [0, 0, Math.PI],
          color: '#eab308',
          opacity: 0.65,
          roughness: 0.05,
          metalness: 0.0
        },
        {
          name: 'signo_exclamacion_centro',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.16, 6],
          position: [0, 0.72, 0],
          color: '#0f172a',
          roughness: 0.2,
          metalness: 0.1
        }
      ]
    }
  }
];
