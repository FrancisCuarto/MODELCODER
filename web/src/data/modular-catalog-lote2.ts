import type { ModularModelEntry } from './modular-catalog.ts';

export const MODULAR_MODELS_LOTE_2: ModularModelEntry[] = [
  // -------------------------------------------------------------------------
  // 01. RACK DE SERVIDORES VERTICAL DE ALTA DENSIDAD
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_server_rack_tall',
    family: 'sci_server_rack_tall',
    name: 'Rack de Servidores de Alta Densidad',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Armario vertical 42U para centro de datos con guías de montaje, bahías de discos, extractor triple superior y leds de telemetría.',
    tags: ['servidor', 'rack', 'redes', 'datos', 'computo', 'infraestructura', 'led'],
    dimensions: { width: 0.80, height: 2.12, depth: 0.90 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_server_rack_tall.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_server_rack_tall',
      name: 'Rack de Servidores de Alta Densidad',
      category: 'infrastructure',
      description: 'Armario vertical 42U para centro de datos con guías de montaje, bahías de discos, extractor triple superior y leds de telemetría.',
      units: 'meters',
      dimensions: { width: 0.80, height: 2.12, depth: 0.90 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_exterior_acero',
          shape: 'box',
          size: [0.80, 2.08, 0.90],
          position: [0, 1.05, 0],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.65,
          metalness: 0.7
        },
        {
          name: 'marco_frontal_montantes',
          shape: 'box',
          size: [0.74, 2.02, 0.04],
          position: [0, 1.05, 0.44],
          color: '#2d3748',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'servidor_blade_1',
          shape: 'box',
          size: [0.68, 0.28, 0.82],
          position: [0, 0.32, 0.02],
          color: '#4a5568',
          texturePreset: 'server_vent_panel',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'servidor_blade_2',
          shape: 'box',
          size: [0.68, 0.28, 0.82],
          position: [0, 0.64, 0.02],
          color: '#4a5568',
          texturePreset: 'server_vent_panel',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'servidor_blade_3_matriz',
          shape: 'box',
          size: [0.68, 0.32, 0.82],
          position: [0, 0.98, 0.02],
          color: '#2d3748',
          texturePreset: 'server_vent_panel',
          roughness: 0.35,
          metalness: 0.85
        },
        {
          name: 'servidor_blade_4',
          shape: 'box',
          size: [0.68, 0.28, 0.82],
          position: [0, 1.32, 0.02],
          color: '#4a5568',
          texturePreset: 'server_vent_panel',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'unidad_switch_fibra',
          shape: 'box',
          size: [0.68, 0.16, 0.82],
          position: [0, 1.58, 0.02],
          color: '#1a365d',
          texturePreset: 'pcb_blue_proto',
          roughness: 0.3,
          metalness: 0.5
        },
        {
          name: 'consola_lcd_diagnostico',
          shape: 'box',
          size: [0.32, 0.14, 0.02],
          position: [0, 1.78, 0.44],
          color: '#0d1b2a',
          texturePreset: 'crt_screen_green',
          roughness: 0.15,
          metalness: 0.05,
          emissive: '#22c55e',
          emissiveIntensity: 1.2
        },
        {
          name: 'techo_extractores_triple',
          shape: 'box',
          size: [0.74, 0.04, 0.84],
          position: [0, 2.10, 0],
          color: '#1a202c',
          texturePreset: 'metal_perforated',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'ventilador_ext_1',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.02, 12],
          position: [-0.20, 2.12, 0],
          color: '#2d3748',
          texturePreset: 'vent_grill',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'ventilador_ext_2',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.02, 12],
          position: [0, 2.12, 0],
          color: '#2d3748',
          texturePreset: 'vent_grill',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'ventilador_ext_3',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.02, 12],
          position: [0.20, 2.12, 0],
          color: '#2d3748',
          texturePreset: 'vent_grill',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'led_actividad_datos_1',
          shape: 'box',
          size: [0.02, 0.015, 0.01],
          position: [-0.28, 0.98, 0.44],
          color: '#38a169',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 1.5
        },
        {
          name: 'led_actividad_datos_2',
          shape: 'box',
          size: [0.02, 0.015, 0.01],
          position: [-0.24, 0.98, 0.44],
          color: '#d69e2e',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#ecc94b',
          emissiveIntensity: 1.5
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 02. CONSOLA DE NAVEGACIÓN CURVA DE PUENTE
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_bridge_console_curved',
    family: 'sci_bridge_console_curved',
    name: 'Consola de Navegación de Puente',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Puesto de pilotaje táctico con base monolítica, superficie ergonómica, pantalla radar central y monitores laterales angulados.',
    tags: ['consola', 'puente', 'navegacion', 'pantalla', 'piloto', 'radar', 'tactico'],
    dimensions: { width: 1.80, height: 1.18, depth: 1.10 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_bridge_console_curved.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_bridge_console_curved',
      name: 'Consola de Navegación de Puente',
      category: 'fixtures',
      description: 'Puesto de pilotaje táctico con base monolítica, superficie ergonómica, pantalla radar central y monitores laterales angulados.',
      units: 'meters',
      dimensions: { width: 1.80, height: 1.18, depth: 1.10 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'plinto_suelo_reforzado',
          shape: 'box',
          size: [1.64, 0.06, 0.88],
          position: [0, 0.03, 0],
          color: '#1a202c',
          texturePreset: 'diamond_plate',
          roughness: 0.8,
          metalness: 0.7
        },
        {
          name: 'cuerpo_pedestal_central',
          shape: 'box',
          size: [1.50, 0.64, 0.78],
          position: [0, 0.38, 0],
          color: '#171923',
          texturePreset: 'iron_cast',
          roughness: 0.75,
          metalness: 0.8
        },
        {
          name: 'rejilla_ventilacion_frontal',
          shape: 'box',
          size: [0.80, 0.22, 0.02],
          position: [0, 0.35, 0.40],
          color: '#2d3748',
          texturePreset: 'vent_grill',
          roughness: 0.6,
          metalness: 0.5
        },
        {
          name: 'panel_mantenimiento_izq',
          shape: 'box',
          size: [0.30, 0.28, 0.02],
          position: [-0.48, 0.35, 0.40],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'panel_mantenimiento_der',
          shape: 'box',
          size: [0.30, 0.28, 0.02],
          position: [0.48, 0.35, 0.40],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'banda_aviso_pedestal',
          shape: 'box',
          size: [1.52, 0.04, 0.02],
          position: [0, 0.67, 0.40],
          color: '#d69e2e',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'viga_soporte_subframe',
          shape: 'box',
          size: [1.60, 0.05, 0.74],
          position: [0, 0.70, 0.02],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'tablero_central_teclado',
          shape: 'box',
          size: [0.60, 0.06, 0.70],
          position: [0, 0.73, 0.05],
          color: '#2d3748',
          texturePreset: 'carbon_fiber',
          roughness: 0.35,
          metalness: 0.4
        },
        {
          name: 'ala_izquierda_inclinada',
          shape: 'box',
          size: [0.55, 0.06, 0.70],
          position: [-0.55, 0.73, 0.12],
          rotation: [0, 0.26, 0],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'ala_derecha_inclinada',
          shape: 'box',
          size: [0.55, 0.06, 0.70],
          position: [0.55, 0.73, 0.12],
          rotation: [0, -0.26, 0],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'borde_ergonomico_goma',
          shape: 'box',
          size: [1.70, 0.03, 0.04],
          position: [0, 0.75, 0.40],
          color: '#111827',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'riel_soporte_monitores',
          shape: 'box',
          size: [1.45, 0.04, 0.04],
          position: [0, 0.77, -0.22],
          color: '#718096',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'soporte_vertical_radar',
          shape: 'box',
          size: [0.06, 0.16, 0.04],
          position: [0, 0.85, -0.22],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'chasis_monitor_radar',
          shape: 'box',
          size: [0.54, 0.36, 0.06],
          position: [0, 0.98, -0.20],
          rotation: [-0.25, 0, 0],
          color: '#d1d5db',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.6,
          metalness: 0.2
        },
        {
          name: 'pantalla_radar_central',
          shape: 'box',
          size: [0.48, 0.30, 0.01],
          position: [0, 0.98, -0.165],
          rotation: [-0.25, 0, 0],
          color: '#0d1b2a',
          texturePreset: 'crt_screen_green',
          roughness: 0.15,
          metalness: 0.05,
          emissive: '#22c55e',
          emissiveIntensity: 1.5
        },
        {
          name: 'brazo_monitor_izq',
          shape: 'box',
          size: [0.05, 0.16, 0.04],
          position: [-0.54, 0.85, -0.16],
          rotation: [0, 0.35, 0],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'chasis_monitor_izq',
          shape: 'box',
          size: [0.48, 0.30, 0.06],
          position: [-0.54, 0.98, -0.14],
          rotation: [-0.22, 0.35, 0],
          color: '#d1d5db',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.6,
          metalness: 0.2
        },
        {
          name: 'pantalla_telemetria_izq',
          shape: 'box',
          size: [0.42, 0.24, 0.01],
          position: [-0.54, 0.98, -0.105],
          rotation: [-0.22, 0.35, 0],
          color: '#1a1405',
          texturePreset: 'crt_screen_amber',
          roughness: 0.15,
          metalness: 0.05,
          emissive: '#f59e0b',
          emissiveIntensity: 1.5
        },
        {
          name: 'brazo_monitor_der',
          shape: 'box',
          size: [0.05, 0.16, 0.04],
          position: [0.54, 0.85, -0.16],
          rotation: [0, -0.35, 0],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'chasis_monitor_der',
          shape: 'box',
          size: [0.48, 0.30, 0.06],
          position: [0.54, 0.98, -0.14],
          rotation: [-0.22, -0.35, 0],
          color: '#d1d5db',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.6,
          metalness: 0.2
        },
        {
          name: 'pantalla_comms_der',
          shape: 'box',
          size: [0.42, 0.24, 0.01],
          position: [0.54, 0.98, -0.105],
          rotation: [-0.22, -0.35, 0],
          color: '#051b24',
          texturePreset: 'crt_screen_blue',
          roughness: 0.15,
          metalness: 0.05,
          emissive: '#06b6d4',
          emissiveIntensity: 1.5
        },
        {
          name: 'teclado_tactil_central',
          shape: 'box',
          size: [0.42, 0.015, 0.18],
          position: [0, 0.765, 0.16],
          color: '#111827',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'trackball_radar_izq',
          shape: 'sphere',
          size: [0.07, 0.07, 0.07],
          position: [-0.50, 0.775, 0.18],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'base_palanca_propulsor',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.02, 12],
          position: [0.50, 0.765, 0.18],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'palanca_propulsor_der',
          shape: 'cylinder',
          size: [0.025, 0.025, 0.10, 8],
          position: [0.50, 0.82, 0.18],
          color: '#cbd5e1',
          texturePreset: 'titanium_aerospace',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'empunadura_propulsor',
          shape: 'box',
          size: [0.06, 0.03, 0.04],
          position: [0.50, 0.88, 0.18],
          color: '#1f2937',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'corona_amarilla_seta',
          shape: 'cylinder',
          size: [0.07, 0.07, 0.01, 12],
          position: [0.22, 0.765, 0.28],
          color: '#d69e2e',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'seta_parada_emergencia',
          shape: 'cylinder',
          size: [0.045, 0.045, 0.035, 12],
          position: [0.22, 0.785, 0.28],
          color: '#e53e3e',
          texturePreset: 'red_paint_worn',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'barra_indicadores_led',
          shape: 'box',
          size: [0.36, 0.02, 0.02],
          position: [0, 0.765, -0.05],
          color: '#38bdf8',
          texturePreset: 'gold_contacts',
          roughness: 0.2,
          metalness: 0.8,
          emissive: '#38bdf8',
          emissiveIntensity: 1.2
        },
        {
          name: 'conector_cables_potencia',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.24, 8],
          position: [0.30, 0.58, -0.38],
          color: '#111827',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 03. UNIDAD DE DISTRIBUCIÓN DE ENERGÍA PDU
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_power_distribution_unit',
    family: 'sci_power_distribution_unit',
    name: 'Unidad de Distribución de Energía PDU',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Armario de distribución eléctrica de alta potencia con franja de alta tensión, 3 voltímetros analógicos y palanca seccionadora.',
    tags: ['electricidad', 'energia', 'pdu', 'transformador', 'voltimetro', 'palanca', 'alta_tension'],
    dimensions: { width: 0.95, height: 1.88, depth: 0.55 },
    triBudget: '280-350',
    glbUrl: '/models/modular/sci_power_distribution_unit.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_power_distribution_unit',
      name: 'Unidad de Distribución de Energía PDU',
      category: 'infrastructure',
      description: 'Armario de distribución eléctrica de alta potencia con franja de alta tensión, 3 voltímetros analógicos y palanca seccionadora.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.88, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_armario_electrico',
          shape: 'box',
          size: [0.95, 1.80, 0.55],
          position: [0, 0.92, 0],
          color: '#2d3748',
          texturePreset: 'steel_galvanized',
          roughness: 0.6,
          metalness: 0.65
        },
        {
          name: 'franja_hazard_superior',
          shape: 'box',
          size: [0.955, 0.10, 0.555],
          position: [0, 1.68, 0],
          color: '#d69e2e',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'puerta_izq_blindada',
          shape: 'box',
          size: [0.44, 1.35, 0.03],
          position: [-0.22, 0.88, 0.285],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'puerta_der_blindada',
          shape: 'box',
          size: [0.44, 1.35, 0.03],
          position: [0.22, 0.88, 0.285],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'voltimetro_fase_r',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.02, 12],
          position: [-0.22, 1.42, 0.305],
          color: '#edf2f7',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'voltimetro_fase_s',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.02, 12],
          position: [0, 1.42, 0.305],
          color: '#edf2f7',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'voltimetro_fase_t',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.02, 12],
          position: [0.22, 1.42, 0.305],
          color: '#edf2f7',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'palanca_corte_general',
          shape: 'box',
          size: [0.04, 0.26, 0.04],
          position: [0.42, 1.10, 0.32],
          rotation: [-0.42, 0, 0],
          color: '#e53e3e',
          texturePreset: 'red_paint_worn',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'base_aislante_baquelita',
          shape: 'box',
          size: [0.88, 0.12, 0.48],
          position: [0, 0.06, 0],
          color: '#2a1a08',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.5,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 04. CAJA DE EMPALMES ELÉCTRICOS BLINDADA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_junction_box_heavy',
    family: 'sci_junction_box_heavy',
    name: 'Caja de Empalmes Blindada',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Caja estanca de fundición con pernos perimetrales de seguridad, 5 racores de tubo conduit de cobre y luz piloto de presencia de tensión.',
    tags: ['empalmes', 'caja', 'conduit', 'electricidad', 'alta_tension', 'mural'],
    dimensions: { width: 0.60, height: 0.94, depth: 0.28 },
    triBudget: '240-300',
    glbUrl: '/models/modular/sci_junction_box_heavy.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_junction_box_heavy',
      name: 'Caja de Empalmes Blindada',
      category: 'fixtures',
      description: 'Caja estanca de fundición con pernos perimetrales de seguridad, 5 racores de tubo conduit de cobre y luz piloto de presencia de tensión.',
      units: 'meters',
      dimensions: { width: 0.60, height: 0.94, depth: 0.28 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_caja_fundicion',
          shape: 'box',
          size: [0.60, 0.72, 0.26],
          position: [0, 0.48, 0],
          color: '#4a5568',
          texturePreset: 'iron_cast',
          roughness: 0.75,
          metalness: 0.8
        },
        {
          name: 'tapa_frontal_atornillada',
          shape: 'box',
          size: [0.55, 0.67, 0.03],
          position: [0, 0.48, 0.14],
          color: '#718096',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.75
        },
        {
          name: 'racor_inferior_1',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.10, 10],
          position: [-0.18, 0.07, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'racor_inferior_2',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.10, 10],
          position: [0, 0.07, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'racor_inferior_3',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.10, 10],
          position: [0.18, 0.07, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'racor_superior_1',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.10, 10],
          position: [-0.14, 0.89, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'racor_superior_2',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.10, 10],
          position: [0.14, 0.89, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'placa_advertencia_rayo',
          shape: 'box',
          size: [0.18, 0.15, 0.01],
          position: [0, 0.52, 0.16],
          color: '#d69e2e',
          texturePreset: 'high_voltage_label',
          roughness: 0.4,
          metalness: 0.1
        },
        {
          name: 'piloto_tension_rojo',
          shape: 'cylinder',
          size: [0.025, 0.025, 0.03, 10],
          position: [0.20, 0.72, 0.155],
          color: '#e53e3e',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#e53e3e',
          emissiveIntensity: 1.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 05. TERMINAL DE CONSULTA HOLOGRÁFICA DE PEDESTAL
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_holographic_terminal',
    family: 'sci_holographic_terminal',
    name: 'Terminal Holográfica de Pedestal',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Pilar de consulta interactiva con base cónica, columna con aletas de disipación, lente de emisión holográfico y plano volumétrico azul.',
    tags: ['holograma', 'terminal', 'pedestal', 'consulta', 'azul', 'tecnologia', 'visor'],
    dimensions: { width: 0.65, height: 1.35, depth: 0.65 },
    triBudget: '280-360',
    glbUrl: '/models/modular/sci_holographic_terminal.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_holographic_terminal',
      name: 'Terminal Holográfica de Pedestal',
      category: 'fixtures',
      description: 'Pilar de consulta interactiva con base cónica, columna con aletas de disipación, lente de emisión holográfico y plano volumétrico azul.',
      units: 'meters',
      dimensions: { width: 0.65, height: 1.35, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_anclaje_octogonal',
          shape: 'cylinder',
          size: [0.32, 0.32, 0.08, 8],
          position: [0, 0.04, 0],
          color: '#1a202c',
          texturePreset: 'iron_cast',
          roughness: 0.75,
          metalness: 0.8
        },
        {
          name: 'columna_cilindrica_disipador',
          shape: 'cylinder',
          size: [0.10, 0.10, 0.85, 12],
          position: [0, 0.50, 0],
          color: '#2d3748',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'anillo_disipador_inf',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.02, 12],
          position: [0, 0.35, 0],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'anillo_disipador_med',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.02, 12],
          position: [0, 0.52, 0],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'anillo_disipador_sup',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.02, 12],
          position: [0, 0.68, 0],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'cabezal_emisor_conico',
          shape: 'cylinder',
          size: [0.24, 0.12, 0.20, 8],
          position: [0, 0.98, 0],
          color: '#1a365d',
          texturePreset: 'metal_dark_grime',
          roughness: 0.4,
          metalness: 0.75
        },
        {
          name: 'lente_emisor_zafiro',
          shape: 'cylinder',
          size: [0.16, 0.16, 0.02, 16],
          position: [0, 1.09, 0],
          color: '#63b3ed',
          texturePreset: 'tinted_glass',
          roughness: 0.1,
          metalness: 0.2,
          emissive: '#3182ce',
          emissiveIntensity: 1.8
        },
        {
          name: 'disco_holografico_flotante',
          shape: 'cylinder',
          size: [0.28, 0.28, 0.04, 16],
          position: [0, 1.25, 0],
          color: '#63b3ed',
          texturePreset: 'hologram_cyan',
          roughness: 0.1,
          metalness: 0.1,
          transparent: true,
          opacity: 0.45,
          emissive: '#63b3ed',
          emissiveIntensity: 2.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 06. PANEL MURAL DE FIBRA ÓPTICA Y PUERTOS DE RED
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_wall_data_panel',
    family: 'sci_wall_data_panel',
    name: 'Panel Mural de Fibra Óptica',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Punto de interconexión de red de alta velocidad con puerta acrílica ahumada, bahías de patch panels y barra de tráfico de paquetes.',
    tags: ['fibra', 'red', 'datos', 'ethernet', 'mural', 'patch_panel', 'led'],
    dimensions: { width: 0.85, height: 0.65, depth: 0.22 },
    triBudget: '220-280',
    glbUrl: '/models/modular/sci_wall_data_panel.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_wall_data_panel',
      name: 'Panel Mural de Fibra Óptica',
      category: 'fixtures',
      description: 'Punto de interconexión de red de alta velocidad con puerta acrílica ahumada, bahías de patch panels y barra de tráfico de paquetes.',
      units: 'meters',
      dimensions: { width: 0.85, height: 0.65, depth: 0.22 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_distribucion_mural',
          shape: 'box',
          size: [0.80, 0.60, 0.20],
          position: [0, 0.325, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.45,
          metalness: 0.35
        },
        {
          name: 'placa_anclaje_posterior',
          shape: 'box',
          size: [0.85, 0.65, 0.02],
          position: [0, 0.325, -0.10],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'puerta_acrilico_ahumado',
          shape: 'box',
          size: [0.76, 0.56, 0.02],
          position: [0, 0.325, 0.11],
          color: '#2d3748',
          texturePreset: 'tinted_glass',
          roughness: 0.12,
          metalness: 0.2,
          transparent: true,
          opacity: 0.55
        },
        {
          name: 'bahia_patch_fila_1',
          shape: 'box',
          size: [0.68, 0.08, 0.04],
          position: [0, 0.18, 0.05],
          color: '#2b6cb0',
          texturePreset: 'pcb_blue_proto',
          roughness: 0.3,
          metalness: 0.6
        },
        {
          name: 'bahia_patch_fila_2',
          shape: 'box',
          size: [0.68, 0.08, 0.04],
          position: [0, 0.30, 0.05],
          color: '#2b6cb0',
          texturePreset: 'pcb_blue_proto',
          roughness: 0.3,
          metalness: 0.6
        },
        {
          name: 'bahia_patch_fila_3',
          shape: 'box',
          size: [0.68, 0.08, 0.04],
          position: [0, 0.42, 0.05],
          color: '#276749',
          texturePreset: 'pcb_green_gold',
          roughness: 0.3,
          metalness: 0.6
        },
        {
          name: 'barra_led_trafico_red',
          shape: 'box',
          size: [0.12, 0.02, 0.01],
          position: [0.28, 0.54, 0.105],
          color: '#38a169',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 1.6
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 07. RACK DE CÓMPUTO CUÁNTICO CON CÁMARA CRIOGÉNICA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_quantum_core_rack',
    family: 'sci_quantum_core_rack',
    name: 'Rack de Cómputo Cuántico',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Unidad de procesamiento cuántico aislada al vacío con cámara criogénica de helio líquido, 4 anillos superconductores dorados y bombas turbomoleculares.',
    tags: ['cuantico', 'criogenia', 'computo', 'helio', 'superconductor', 'nucleo', 'oro'],
    dimensions: { width: 1.10, height: 2.22, depth: 1.10 },
    triBudget: '360-460',
    glbUrl: '/models/modular/sci_quantum_core_rack.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_quantum_core_rack',
      name: 'Rack de Cómputo Cuántico',
      category: 'infrastructure',
      description: 'Unidad de procesamiento cuántico aislada al vacío con cámara criogénica de helio líquido, 4 anillos superconductores dorados y bombas turbomoleculares.',
      units: 'meters',
      dimensions: { width: 1.10, height: 2.22, depth: 1.10 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'exoesqueleto_hexagonal',
          shape: 'box',
          size: [1.10, 2.18, 1.10],
          position: [0, 1.10, 0],
          color: '#0f172a',
          texturePreset: 'carbon_fiber',
          roughness: 0.45,
          metalness: 0.65
        },
        {
          name: 'camara_criogenica_central',
          shape: 'cylinder',
          size: [0.36, 0.36, 1.60, 16],
          position: [0, 1.15, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.15,
          metalness: 0.95
        },
        {
          name: 'anillo_superconductor_1',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.06, 16],
          position: [0, 0.65, 0],
          color: '#d69e2e',
          texturePreset: 'gold_contacts',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'anillo_superconductor_2',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.06, 16],
          position: [0, 1.00, 0],
          color: '#d69e2e',
          texturePreset: 'gold_contacts',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'anillo_superconductor_3',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.06, 16],
          position: [0, 1.35, 0],
          color: '#d69e2e',
          texturePreset: 'gold_contacts',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'anillo_superconductor_4',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.06, 16],
          position: [0, 1.70, 0],
          color: '#d69e2e',
          texturePreset: 'gold_contacts',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'linea_refrigerante_izq',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.90, 8],
          position: [-0.44, 1.15, 0.26],
          color: '#63b3ed',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'linea_refrigerante_der',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.90, 8],
          position: [0.44, 1.15, 0.26],
          color: '#63b3ed',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'bancada_bombas_vacio',
          shape: 'box',
          size: [0.95, 0.22, 0.95],
          position: [0, 0.11, 0],
          color: '#1a202c',
          texturePreset: 'metal_perforated',
          roughness: 0.55,
          metalness: 0.75
        },
        {
          name: 'display_temperatura_kelvin',
          shape: 'box',
          size: [0.24, 0.12, 0.02],
          position: [0, 1.95, 0.54],
          color: '#1a1405',
          texturePreset: 'crt_screen_amber',
          roughness: 0.2,
          metalness: 0.05,
          emissive: '#d97706',
          emissiveIntensity: 1.5
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 08. BANCO DE BATERÍAS DE EMERGENCIA UPS HOT-SWAP
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_ups_battery_bank',
    family: 'sci_ups_battery_bank',
    name: 'Banco de Baterías UPS Hot-Swap',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Sistema de respaldo ininterrumpido con 4 módulos de celdas de iones de litio extraíbles, tiradores abatibles y barra LED de autonomía.',
    tags: ['bateria', 'ups', 'energia', 'respaldo', 'acumulador', 'hot_swap', 'autonomia'],
    dimensions: { width: 0.90, height: 1.62, depth: 0.70 },
    triBudget: '290-370',
    glbUrl: '/models/modular/sci_ups_battery_bank.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_ups_battery_bank',
      name: 'Banco de Baterías UPS Hot-Swap',
      category: 'infrastructure',
      description: 'Sistema de respaldo ininterrumpido con 4 módulos de celdas de iones de litio extraíbles, tiradores abatibles y barra LED de autonomía.',
      units: 'meters',
      dimensions: { width: 0.90, height: 1.62, depth: 0.70 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_gabinete_pesado',
          shape: 'box',
          size: [0.90, 1.60, 0.70],
          position: [0, 0.81, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.75
        },
        {
          name: 'modulo_bateria_1',
          shape: 'box',
          size: [0.78, 0.25, 0.64],
          position: [0, 0.22, 0.02],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'modulo_bateria_2',
          shape: 'box',
          size: [0.78, 0.25, 0.64],
          position: [0, 0.52, 0.02],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'modulo_bateria_3',
          shape: 'box',
          size: [0.78, 0.25, 0.64],
          position: [0, 0.82, 0.02],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'modulo_bateria_4',
          shape: 'box',
          size: [0.78, 0.25, 0.64],
          position: [0, 1.12, 0.02],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'tirador_bateria_1',
          shape: 'box',
          size: [0.24, 0.03, 0.04],
          position: [0, 0.22, 0.35],
          color: '#e2e8f0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'tirador_bateria_2',
          shape: 'box',
          size: [0.24, 0.03, 0.04],
          position: [0, 0.52, 0.35],
          color: '#e2e8f0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'tirador_bateria_3',
          shape: 'box',
          size: [0.24, 0.03, 0.04],
          position: [0, 0.82, 0.35],
          color: '#e2e8f0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'tirador_bateria_4',
          shape: 'box',
          size: [0.24, 0.03, 0.04],
          position: [0, 1.12, 0.35],
          color: '#e2e8f0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'panel_indicador_autonomia',
          shape: 'box',
          size: [0.48, 0.14, 0.02],
          position: [0, 1.44, 0.35],
          color: '#064e3b',
          texturePreset: 'crt_screen_green',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#10b981',
          emissiveIntensity: 1.5
        },
        {
          name: 'borne_desconexion_rojo',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.06, 12],
          position: [0.32, 1.44, 0.36],
          color: '#dc2626',
          texturePreset: 'red_paint_worn',
          roughness: 0.35,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 09. MATRIZ DE COMUNICACIONES Y ANTENA INTERNA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_telecom_array_indoor',
    family: 'sci_telecom_array_indoor',
    name: 'Matriz de Telecomunicaciones',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Poste de radiofrecuencia para transmisión interna con trípode de anclaje, bobina helicoidal de carga, 4 dipolos cruzados y baliza de pulso.',
    tags: ['antena', 'telecomunicaciones', 'radio', 'frecuencia', 'comms', 'dipolos', 'baliza'],
    dimensions: { width: 0.80, height: 2.10, depth: 0.80 },
    triBudget: '280-360',
    glbUrl: '/models/modular/sci_telecom_array_indoor.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_telecom_array_indoor',
      name: 'Matriz de Telecomunicaciones',
      category: 'fixtures',
      description: 'Poste de radiofrecuencia para transmisión interna con trípode de anclaje, bobina helicoidal de carga, 4 dipolos cruzados y baliza de pulso.',
      units: 'meters',
      dimensions: { width: 0.80, height: 2.10, depth: 0.80 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'plato_base_tripode',
          shape: 'cylinder',
          size: [0.38, 0.38, 0.06, 12],
          position: [0, 0.03, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'columna_tubular_mastil',
          shape: 'cylinder',
          size: [0.07, 0.07, 1.20, 12],
          position: [0, 0.65, 0],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.75
        },
        {
          name: 'caja_sintonia_rf',
          shape: 'box',
          size: [0.38, 0.32, 0.28],
          position: [0, 1.10, 0],
          color: '#0f172a',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'bobina_carga_cobre_1',
          shape: 'cylinder',
          size: [0.15, 0.15, 0.04, 16],
          position: [0, 1.34, 0],
          color: '#b45309',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'bobina_carga_cobre_2',
          shape: 'cylinder',
          size: [0.15, 0.15, 0.04, 16],
          position: [0, 1.42, 0],
          color: '#b45309',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'bobina_carga_cobre_3',
          shape: 'cylinder',
          size: [0.15, 0.15, 0.04, 16],
          position: [0, 1.50, 0],
          color: '#b45309',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'dipolo_eje_x',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.74, 8],
          position: [0, 1.78, 0],
          rotation: [0, 0, 1.57],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'dipolo_eje_z',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.74, 8],
          position: [0, 1.78, 0],
          rotation: [1.57, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'cupula_radomo_dielectrico',
          shape: 'cylinder',
          size: [0.10, 0.10, 0.18, 12],
          position: [0, 1.95, 0],
          color: '#f8fafc',
          texturePreset: 'painted_metal_white',
          roughness: 0.3,
          metalness: 0.4
        },
        {
          name: 'baliza_sincronismo_azul',
          shape: 'sphere',
          size: [0.035, 0.035, 0.035],
          position: [0, 2.06, 0],
          color: '#3b82f6',
          roughness: 0.15,
          metalness: 0.1,
          emissive: '#3b82f6',
          emissiveIntensity: 1.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 10. ESTACIÓN DE FUSIBLES INDUSTRIALES MURAL
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_fuse_station_wall',
    family: 'sci_fuse_station_wall',
    name: 'Estación de Fusibles Industriales',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Tablero mural seccionable con 3 cartuchos cerámicos de media tensión, contactos elásticos de cobre y palanca exterior de disparo.',
    tags: ['fusibles', 'mural', 'corte', 'seguridad', 'ceramica', 'electricidad', 'media_tension'],
    dimensions: { width: 0.70, height: 0.92, depth: 0.28 },
    triBudget: '240-300',
    glbUrl: '/models/modular/sci_fuse_station_wall.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_fuse_station_wall',
      name: 'Estación de Fusibles Industriales',
      category: 'infrastructure',
      description: 'Tablero mural seccionable con 3 cartuchos cerámicos de media tensión, contactos elásticos de cobre y palanca exterior de disparo.',
      units: 'meters',
      dimensions: { width: 0.70, height: 0.92, depth: 0.28 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'caja_gabinete_mural',
          shape: 'box',
          size: [0.70, 0.90, 0.22],
          position: [0, 0.46, 0],
          color: '#334155',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'fondo_esteatita_aislante',
          shape: 'box',
          size: [0.62, 0.82, 0.02],
          position: [0, 0.46, 0.06],
          color: '#f8fafc',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.4,
          metalness: 0.1
        },
        {
          name: 'fusible_ceramico_fase_1',
          shape: 'cylinder',
          size: [0.055, 0.055, 0.45, 12],
          position: [-0.18, 0.46, 0.14],
          color: '#e2e8f0',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'fusible_ceramico_fase_2',
          shape: 'cylinder',
          size: [0.055, 0.055, 0.45, 12],
          position: [0, 0.46, 0.14],
          color: '#e2e8f0',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'fusible_ceramico_fase_3',
          shape: 'cylinder',
          size: [0.055, 0.055, 0.45, 12],
          position: [0.18, 0.46, 0.14],
          color: '#e2e8f0',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'pinza_contacto_sup_1',
          shape: 'box',
          size: [0.06, 0.06, 0.08],
          position: [-0.18, 0.70, 0.14],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'pinza_contacto_sup_2',
          shape: 'box',
          size: [0.06, 0.06, 0.08],
          position: [0, 0.70, 0.14],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'pinza_contacto_sup_3',
          shape: 'box',
          size: [0.06, 0.06, 0.08],
          position: [0.18, 0.70, 0.14],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'palanca_corte_lateral',
          shape: 'box',
          size: [0.035, 0.30, 0.035],
          position: [0.38, 0.46, 0.06],
          rotation: [0.35, 0, 0],
          color: '#dc2626',
          texturePreset: 'red_paint_worn',
          roughness: 0.4,
          metalness: 0.25
        },
        {
          name: 'franja_alerta_inferior',
          shape: 'box',
          size: [0.66, 0.08, 0.01],
          position: [0, 0.12, 0.12],
          color: '#d69e2e',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 11. TABLERO MURAL DE ESTADO TÁCTICO TRI-PANTALLA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_tactical_status_board',
    family: 'sci_tactical_status_board',
    name: 'Tablero Mural Táctico Tri-Pantalla',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Display panorámico de monitoreo de subsistemas dividido en 3 pantallas LED tácticas independientes con balizas de alerta.',
    tags: ['pantalla', 'tactico', 'estado', 'telemetria', 'mural', 'alarma', 'casco'],
    dimensions: { width: 1.60, height: 0.92, depth: 0.14 },
    triBudget: '220-280',
    glbUrl: '/models/modular/sci_tactical_status_board.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_tactical_status_board',
      name: 'Tablero Mural Táctico Tri-Pantalla',
      category: 'fixtures',
      description: 'Display panorámico de monitoreo de subsistemas dividido en 3 pantallas LED tácticas independientes con balizas de alerta.',
      units: 'meters',
      dimensions: { width: 1.60, height: 0.92, depth: 0.14 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'marco_duraluminio_panoramico',
          shape: 'box',
          size: [1.60, 0.90, 0.12],
          position: [0, 0.46, 0],
          color: '#0f172a',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pantalla_sector_casco_izq',
          shape: 'box',
          size: [0.46, 0.74, 0.02],
          position: [-0.48, 0.46, 0.065],
          color: '#064e3b',
          texturePreset: 'crt_screen_green',
          roughness: 0.2,
          metalness: 0.05,
          emissive: '#22c55e',
          emissiveIntensity: 1.3
        },
        {
          name: 'pantalla_reactor_potencia_cen',
          shape: 'box',
          size: [0.46, 0.74, 0.02],
          position: [0, 0.46, 0.065],
          color: '#451a03',
          texturePreset: 'crt_screen_amber',
          roughness: 0.2,
          metalness: 0.05,
          emissive: '#f59e0b',
          emissiveIntensity: 1.3
        },
        {
          name: 'pantalla_sensores_der',
          shape: 'box',
          size: [0.46, 0.74, 0.02],
          position: [0.48, 0.46, 0.065],
          color: '#082f49',
          texturePreset: 'crt_screen_blue',
          roughness: 0.2,
          metalness: 0.05,
          emissive: '#0ea5e9',
          emissiveIntensity: 1.3
        },
        {
          name: 'baliza_alerta_1_verde',
          shape: 'box',
          size: [0.04, 0.03, 0.02],
          position: [-0.60, 0.86, 0.065],
          color: '#22c55e',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#22c55e',
          emissiveIntensity: 1.6
        },
        {
          name: 'baliza_alerta_2_ambar',
          shape: 'box',
          size: [0.04, 0.03, 0.02],
          position: [0, 0.86, 0.065],
          color: '#f59e0b',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#f59e0b',
          emissiveIntensity: 1.6
        },
        {
          name: 'baliza_alerta_3_rojo',
          shape: 'box',
          size: [0.04, 0.03, 0.02],
          position: [0.60, 0.86, 0.065],
          color: '#ef4444',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#ef4444',
          emissiveIntensity: 1.6
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 12. ESTACIÓN DE BOBINA Y CARRETE DE CABLE PESADO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cable_reel_station',
    family: 'sci_cable_reel_station',
    name: 'Estación de Carrete de Cable Pesado',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Carrete industrial de acero con bastidor en A, tambor con cable trifásico reforzado enrollado, freno de disco y manivela.',
    tags: ['cable', 'carrete', 'bobina', 'trifasico', 'tambor', 'taller', 'electricidad'],
    dimensions: { width: 1.10, height: 1.08, depth: 0.85 },
    triBudget: '300-380',
    glbUrl: '/models/modular/sci_cable_reel_station.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cable_reel_station',
      name: 'Estación de Carrete de Cable Pesado',
      category: 'infrastructure',
      description: 'Carrete industrial de acero con bastidor en A, tambor con cable trifásico reforzado enrollado, freno de disco y manivela.',
      units: 'meters',
      dimensions: { width: 1.10, height: 1.08, depth: 0.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bastidor_a_izq',
          shape: 'box',
          size: [0.08, 0.95, 0.75],
          position: [-0.42, 0.48, 0],
          color: '#eab308',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'bastidor_a_der',
          shape: 'box',
          size: [0.08, 0.95, 0.75],
          position: [0.42, 0.48, 0],
          color: '#eab308',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'eje_central_giro',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.95, 12],
          position: [0, 0.58, 0],
          rotation: [0, 0, 1.57],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'disco_lateral_carrete_izq',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.04, 16],
          position: [-0.32, 0.58, 0],
          rotation: [0, 0, 1.57],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.75
        },
        {
          name: 'disco_lateral_carrete_der',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.04, 16],
          position: [0.32, 0.58, 0],
          rotation: [0, 0, 1.57],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.75
        },
        {
          name: 'tambor_cable_enrollado',
          shape: 'cylinder',
          size: [0.34, 0.34, 0.58, 16],
          position: [0, 0.58, 0],
          rotation: [0, 0, 1.57],
          color: '#1e293b',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.15
        },
        {
          name: 'manivela_brazo',
          shape: 'box',
          size: [0.03, 0.22, 0.03],
          position: [0.48, 0.65, 0],
          color: '#dc2626',
          texturePreset: 'red_paint_worn',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'manivela_pomo',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.06, 10],
          position: [0.48, 0.74, 0.04],
          color: '#1a202c',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'disco_freno_friccion',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.03, 12],
          position: [-0.38, 0.58, 0],
          rotation: [0, 0, 1.57],
          color: '#475569',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 13. SUBESTACIÓN DE TRANSFORMADOR SECO DE POTENCIA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_transformer_substation',
    family: 'sci_transformer_substation',
    name: 'Transformador Seco de Potencia',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Transformador trifásico encapsulado en resina epoxi con 3 columnas de núcleo magnético, aisladores cerámicos y tejadillo de disipación.',
    tags: ['transformador', 'subestacion', 'potencia', 'epoxi', 'bobinas', 'ceramica', 'alta_tension'],
    dimensions: { width: 1.30, height: 1.58, depth: 0.85 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_transformer_substation.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_transformer_substation',
      name: 'Transformador Seco de Potencia',
      category: 'infrastructure',
      description: 'Transformador trifásico encapsulado en resina epoxi con 3 columnas de núcleo magnético, aisladores cerámicos y tejadillo de disipación.',
      units: 'meters',
      dimensions: { width: 1.30, height: 1.58, depth: 0.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bancada_perfiles_u',
          shape: 'box',
          size: [1.30, 0.12, 0.85],
          position: [0, 0.06, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.75,
          metalness: 0.8
        },
        {
          name: 'nucleo_ferromagnetico_laminado',
          shape: 'box',
          size: [1.10, 0.95, 0.35],
          position: [0, 0.65, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'bobina_epoxi_roja_1',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.75, 14],
          position: [-0.34, 0.65, 0],
          color: '#b91c1c',
          texturePreset: 'red_paint_worn',
          roughness: 0.45,
          metalness: 0.2
        },
        {
          name: 'bobina_epoxi_roja_2',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.75, 14],
          position: [0, 0.65, 0],
          color: '#b91c1c',
          texturePreset: 'red_paint_worn',
          roughness: 0.45,
          metalness: 0.2
        },
        {
          name: 'bobina_epoxi_roja_3',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.75, 14],
          position: [0.34, 0.65, 0],
          color: '#b91c1c',
          texturePreset: 'red_paint_worn',
          roughness: 0.45,
          metalness: 0.2
        },
        {
          name: 'aislador_porcelana_1',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.28, 10],
          position: [-0.34, 1.26, 0],
          color: '#f8fafc',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'aislador_porcelana_2',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.28, 10],
          position: [0, 1.26, 0],
          color: '#f8fafc',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'aislador_porcelana_3',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.28, 10],
          position: [0.34, 1.26, 0],
          color: '#f8fafc',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'caperuza_tejadillo_disipacion',
          shape: 'box',
          size: [1.22, 0.16, 0.78],
          position: [0, 1.48, 0],
          color: '#2d3748',
          texturePreset: 'metal_perforated',
          roughness: 0.5,
          metalness: 0.75
        },
        {
          name: 'placa_caracteristicas_tecnicas',
          shape: 'box',
          size: [0.20, 0.14, 0.01],
          position: [0, 0.65, 0.43],
          color: '#d69e2e',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 14. NODO DISTRIBUIDOR DE TUBERÍA CONDUIT 4 VÍAS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_conduit_junction_node',
    family: 'sci_conduit_junction_node',
    name: 'Distribuidor Conduit 4 Vías',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Nodo estanco de derivación en cruz para tendido de cables pesados con tapa de registro circular hermética y bridas roscadas.',
    tags: ['conduit', 'nodo', 'distribuidor', 'tubo', 'derivacion', 'blindado', 'cruce'],
    dimensions: { width: 0.82, height: 0.82, depth: 0.32 },
    triBudget: '260-320',
    glbUrl: '/models/modular/sci_conduit_junction_node.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_conduit_junction_node',
      name: 'Distribuidor Conduit 4 Vías',
      category: 'infrastructure',
      description: 'Nodo estanco de derivación en cruz para tendido de cables pesados con tapa de registro circular hermética y bridas roscadas.',
      units: 'meters',
      dimensions: { width: 0.82, height: 0.82, depth: 0.32 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_nodal_octogonal',
          shape: 'cylinder',
          size: [0.24, 0.24, 0.24, 8],
          position: [0, 0.41, 0],
          rotation: [1.57, 0, 0],
          color: '#475569',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'tapa_circular_registro',
          shape: 'cylinder',
          size: [0.21, 0.21, 0.03, 16],
          position: [0, 0.41, 0.135],
          rotation: [1.57, 0, 0],
          color: '#718096',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.8
        },
        {
          name: 'boca_roscada_norte',
          shape: 'cylinder',
          size: [0.065, 0.065, 0.20, 12],
          position: [0, 0.65, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'boca_roscada_sur',
          shape: 'cylinder',
          size: [0.065, 0.065, 0.20, 12],
          position: [0, 0.17, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'boca_roscada_este',
          shape: 'cylinder',
          size: [0.065, 0.065, 0.20, 12],
          position: [0.24, 0.41, 0],
          rotation: [0, 0, 1.57],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'boca_roscada_oeste',
          shape: 'cylinder',
          size: [0.065, 0.065, 0.20, 12],
          position: [-0.24, 0.41, 0],
          rotation: [0, 0, 1.57],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.35,
          metalness: 0.9
        },
        {
          name: 'orejeta_anclaje_1',
          shape: 'box',
          size: [0.08, 0.08, 0.02],
          position: [-0.22, 0.63, -0.10],
          color: '#334155',
          texturePreset: 'steel_galvanized',
          roughness: 0.6,
          metalness: 0.75
        },
        {
          name: 'orejeta_anclaje_2',
          shape: 'box',
          size: [0.08, 0.08, 0.02],
          position: [0.22, 0.63, -0.10],
          color: '#334155',
          texturePreset: 'steel_galvanized',
          roughness: 0.6,
          metalness: 0.75
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 15. ARMARIO DE RELÉS DE AUTOMATIZACIÓN DOBLE PUERTA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_relay_cabinet_dual',
    family: 'sci_relay_cabinet_dual',
    name: 'Armario de Relés de Automatización',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Armario de control lógico con puertas dobles, zócalo de ventilación, tejadillo inclinado y baliza tri-color de estado operativo.',
    tags: ['reles', 'automatizacion', 'armario', 'control', 'plc', 'baliza', 'puertas'],
    dimensions: { width: 1.20, height: 2.12, depth: 0.60 },
    triBudget: '310-390',
    glbUrl: '/models/modular/sci_relay_cabinet_dual.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_relay_cabinet_dual',
      name: 'Armario de Relés de Automatización',
      category: 'infrastructure',
      description: 'Armario de control lógico con puertas dobles, zócalo de ventilación, tejadillo inclinado y baliza tri-color de estado operativo.',
      units: 'meters',
      dimensions: { width: 1.20, height: 2.12, depth: 0.60 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'gabinete_acero_doble',
          shape: 'box',
          size: [1.20, 1.95, 0.60],
          position: [0, 1.045, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.45,
          metalness: 0.4
        },
        {
          name: 'zocalo_elevacion_inferior',
          shape: 'box',
          size: [1.16, 0.14, 0.56],
          position: [0, 0.07, 0],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.8,
          metalness: 0.7
        },
        {
          name: 'puerta_izquierda_chapa',
          shape: 'box',
          size: [0.56, 1.70, 0.03],
          position: [-0.28, 1.07, 0.31],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'puerta_derecha_chapa',
          shape: 'box',
          size: [0.56, 1.70, 0.03],
          position: [0.28, 1.07, 0.31],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'maneta_bloqueo_izq',
          shape: 'box',
          size: [0.035, 0.18, 0.045],
          position: [-0.04, 1.07, 0.35],
          color: '#cbd5e1',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'maneta_bloqueo_der',
          shape: 'box',
          size: [0.035, 0.18, 0.045],
          position: [0.04, 1.07, 0.35],
          color: '#cbd5e1',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'tejadillo_inclinado_antipolvo',
          shape: 'box',
          size: [1.24, 0.06, 0.64],
          position: [0, 2.03, 0],
          rotation: [0.05, 0, 0],
          color: '#1e293b',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'baliza_tricolor_torre',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.18, 10],
          position: [0.45, 2.12, 0],
          color: '#22c55e',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#22c55e',
          emissiveIntensity: 1.6
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 16. TERMINAL DE ACOPLAMIENTO Y CARGA DE DRONES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_drone_dock_terminal',
    family: 'sci_drone_dock_terminal',
    name: 'Estación de Carga de Drones',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Plataforma de aterrizaje por inducción con marcas tácticas de alineación, 4 electrodos de cobre y pantalla de estado de batería.',
    tags: ['dron', 'dock', 'carga', 'induccion', 'plataforma', 'mira', 'autonomo'],
    dimensions: { width: 1.00, height: 1.25, depth: 1.00 },
    triBudget: '310-380',
    glbUrl: '/models/modular/sci_drone_dock_terminal.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_drone_dock_terminal',
      name: 'Estación de Carga de Drones',
      category: 'fixtures',
      description: 'Plataforma de aterrizaje por inducción con marcas tácticas de alineación, 4 electrodos de cobre y pantalla de estado de batería.',
      units: 'meters',
      dimensions: { width: 1.00, height: 1.25, depth: 1.00 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'pedestal_conico_soporte',
          shape: 'cylinder',
          size: [0.35, 0.22, 0.80, 8],
          position: [0, 0.40, 0],
          color: '#334155',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'plataforma_aterrizaje_octogonal',
          shape: 'cylinder',
          size: [0.48, 0.48, 0.08, 8],
          position: [0, 0.84, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'electrodo_induccion_norte',
          shape: 'box',
          size: [0.12, 0.02, 0.12],
          position: [0, 0.89, 0.25],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'electrodo_induccion_sur',
          shape: 'box',
          size: [0.12, 0.02, 0.12],
          position: [0, 0.89, -0.25],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'electrodo_induccion_este',
          shape: 'box',
          size: [0.12, 0.02, 0.12],
          position: [0.25, 0.89, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'electrodo_induccion_oeste',
          shape: 'box',
          size: [0.12, 0.02, 0.12],
          position: [-0.25, 0.89, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.95
        },
        {
          name: 'brazo_centrado_izq',
          shape: 'box',
          size: [0.06, 0.16, 0.55],
          position: [-0.38, 0.96, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'brazo_centrado_der',
          shape: 'box',
          size: [0.06, 0.16, 0.55],
          position: [0.38, 0.96, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'monitor_telemetria_dron',
          shape: 'box',
          size: [0.24, 0.18, 0.03],
          position: [0.38, 1.12, -0.25],
          rotation: [-0.3, -0.3, 0],
          color: '#064e3b',
          texturePreset: 'crt_screen_green',
          roughness: 0.2,
          metalness: 0.05,
          emissive: '#22c55e',
          emissiveIntensity: 1.4
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 17. POSTE SENSOR DE ATMÓSFERA, PRESIÓN Y RADIACIÓN
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_environmental_scanner_post',
    family: 'sci_environmental_scanner_post',
    name: 'Poste Sensor de Atmósfera y Radiación',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Mástil de monitorización ambiental con tubo Geiger, anemómetro ultrasónico, display cilíndrico de PPM y baliza de peligro radiológico.',
    tags: ['sensor', 'radiacion', 'geiger', 'atmosfera', 'poste', 'presion', 'alerta'],
    dimensions: { width: 0.45, height: 1.95, depth: 0.45 },
    triBudget: '260-320',
    glbUrl: '/models/modular/sci_environmental_scanner_post.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_environmental_scanner_post',
      name: 'Poste Sensor de Atmósfera y Radiación',
      category: 'fixtures',
      description: 'Mástil de monitorización ambiental con tubo Geiger, anemómetro ultrasónico, display cilíndrico de PPM y baliza de peligro radiológico.',
      units: 'meters',
      dimensions: { width: 0.45, height: 1.95, depth: 0.45 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_anclaje_cuadrada',
          shape: 'box',
          size: [0.45, 0.08, 0.45],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'fuste_cilindrico_mastil',
          shape: 'cylinder',
          size: [0.065, 0.065, 1.40, 12],
          position: [0, 0.78, 0],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.75
        },
        {
          name: 'display_cilindrico_ppm',
          shape: 'cylinder',
          size: [0.12, 0.12, 0.18, 12],
          position: [0, 1.20, 0],
          color: '#451a03',
          texturePreset: 'crt_screen_amber',
          roughness: 0.2,
          metalness: 0.05,
          emissive: '#f59e0b',
          emissiveIntensity: 1.5
        },
        {
          name: 'anemometro_anular_flujo',
          shape: 'cylinder',
          size: [0.22, 0.22, 0.08, 12],
          position: [0, 1.48, 0],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'tubo_camara_geiger',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.22, 10],
          position: [0.12, 1.48, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'baliza_estroboscopica_roja',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.14, 12],
          position: [0, 1.88, 0],
          color: '#ef4444',
          roughness: 0.15,
          metalness: 0.1,
          emissive: '#ef4444',
          emissiveIntensity: 1.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 18. BÓVEDA CRIPTOGRÁFICA MURAL CON TECLADO NUMÉRICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_crypto_key_vault',
    family: 'sci_crypto_key_vault',
    name: 'Bóveda Criptográfica Mural',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Caja fuerte blindada de titanio para llaves de encriptación con volante de cerrojos, teclado de acceso biométrico y ranuras de módulos cuánticos.',
    tags: ['boveda', 'criptografia', 'seguridad', 'llaves', 'titanio', 'volante', 'mural'],
    dimensions: { width: 0.65, height: 0.82, depth: 0.36 },
    triBudget: '270-340',
    glbUrl: '/models/modular/sci_crypto_key_vault.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_crypto_key_vault',
      name: 'Bóveda Criptográfica Mural',
      category: 'fixtures',
      description: 'Caja fuerte blindada de titanio para llaves de encriptación con volante de cerrojos, teclado de acceso biométrico y ranuras de módulos cuánticos.',
      units: 'meters',
      dimensions: { width: 0.65, height: 0.82, depth: 0.36 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_blindado_boveda',
          shape: 'box',
          size: [0.65, 0.80, 0.32],
          position: [0, 0.41, 0],
          color: '#0f172a',
          texturePreset: 'carbon_fiber',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'puerta_titanio_maciza',
          shape: 'box',
          size: [0.55, 0.70, 0.05],
          position: [0, 0.41, 0.185],
          color: '#cbd5e1',
          texturePreset: 'titanium_aerospace',
          roughness: 0.3,
          metalness: 0.95
        },
        {
          name: 'volante_cerrojos_central',
          shape: 'cylinder',
          size: [0.15, 0.15, 0.03, 16],
          position: [-0.08, 0.41, 0.225],
          rotation: [1.57, 0, 0],
          color: '#f8fafc',
          texturePreset: 'chrome_mirror',
          roughness: 0.15,
          metalness: 0.95
        },
        {
          name: 'teclado_biometrico_acceso',
          shape: 'box',
          size: [0.14, 0.22, 0.02],
          position: [0.16, 0.41, 0.22],
          color: '#1e293b',
          texturePreset: 'pcb_black_hd',
          roughness: 0.35,
          metalness: 0.5,
          emissive: '#0ea5e9',
          emissiveIntensity: 0.6
        },
        {
          name: 'ranura_cartucho_llave_1',
          shape: 'box',
          size: [0.08, 0.025, 0.02],
          position: [0.16, 0.58, 0.22],
          color: '#eab308',
          texturePreset: 'gold_contacts',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'ranura_cartucho_llave_2',
          shape: 'box',
          size: [0.08, 0.025, 0.02],
          position: [0.16, 0.24, 0.22],
          color: '#eab308',
          texturePreset: 'gold_contacts',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'led_bloqueo_hermetico',
          shape: 'box',
          size: [0.03, 0.03, 0.02],
          position: [-0.08, 0.62, 0.22],
          color: '#e11d48',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#e11d48',
          emissiveIntensity: 1.7
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 19. PASARELA AÉREA PORTA-CABLES EN CELOSÍA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cable_bridge_overhang',
    family: 'sci_cable_bridge_overhang',
    name: 'Bandeja Portacables en Celosía',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'infrastructure',
    description: 'Pasarela colgante suspendida para canalización de líneas troncales de energía con 3 mangueras multifilares y tirantes al techo.',
    tags: ['cables', 'bandeja', 'pasarela', 'canaleta', 'aerea', 'suspension', 'conduccion'],
    dimensions: { width: 2.20, height: 0.55, depth: 0.62 },
    triBudget: '310-380',
    glbUrl: '/models/modular/sci_cable_bridge_overhang.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cable_bridge_overhang',
      name: 'Bandeja Portacables en Celosía',
      category: 'infrastructure',
      description: 'Pasarela colgante suspendida para canalización de líneas troncales de energía con 3 mangueras multifilares y tirantes al techo.',
      units: 'meters',
      dimensions: { width: 2.20, height: 0.55, depth: 0.62 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'larguero_viga_u_izq',
          shape: 'box',
          size: [2.20, 0.08, 0.04],
          position: [0, 0.20, -0.28],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'larguero_viga_u_der',
          shape: 'box',
          size: [2.20, 0.08, 0.04],
          position: [0, 0.20, 0.28],
          color: '#475569',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'travesano_escalerilla_1',
          shape: 'box',
          size: [0.04, 0.03, 0.56],
          position: [-0.90, 0.18, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.55,
          metalness: 0.75
        },
        {
          name: 'travesano_escalerilla_2',
          shape: 'box',
          size: [0.04, 0.03, 0.56],
          position: [-0.45, 0.18, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.55,
          metalness: 0.75
        },
        {
          name: 'travesano_escalerilla_3',
          shape: 'box',
          size: [0.04, 0.03, 0.56],
          position: [0, 0.18, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.55,
          metalness: 0.75
        },
        {
          name: 'travesano_escalerilla_4',
          shape: 'box',
          size: [0.04, 0.03, 0.56],
          position: [0.45, 0.18, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.55,
          metalness: 0.75
        },
        {
          name: 'travesano_escalerilla_5',
          shape: 'box',
          size: [0.04, 0.03, 0.56],
          position: [0.90, 0.18, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.55,
          metalness: 0.75
        },
        {
          name: 'cable_troncal_rojo',
          shape: 'cylinder',
          size: [0.04, 0.04, 2.20, 10],
          position: [0, 0.24, -0.12],
          rotation: [0, 0, 1.57],
          color: '#b91c1c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.15
        },
        {
          name: 'cable_troncal_negro',
          shape: 'cylinder',
          size: [0.045, 0.045, 2.20, 10],
          position: [0, 0.245, 0],
          rotation: [0, 0, 1.57],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.85,
          metalness: 0.1
        },
        {
          name: 'cable_troncal_azul',
          shape: 'cylinder',
          size: [0.04, 0.04, 2.20, 10],
          position: [0, 0.24, 0.12],
          rotation: [0, 0, 1.57],
          color: '#1d4ed8',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.15
        },
        {
          name: 'tirante_suspension_izq',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.35, 8],
          position: [-0.80, 0.38, 0],
          color: '#94a3b8',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'tirante_suspension_der',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.35, 8],
          position: [0.80, 0.38, 0],
          color: '#94a3b8',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 20. COLUMNA DE MEGAFONÍA Y COMUNICADOR DE EMERGENCIA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_audio_intercom_pillar',
    family: 'sci_audio_intercom_pillar',
    name: 'Columna de Megafonía e Interfono',
    batch: 2,
    batchName: 'Consolas, Racks y Red Eléctrica',
    category: 'fixtures',
    description: 'Poste vertical de comunicaciones de seguridad con altavoz de bocina superior, intercomunicador con micrófono y pulsador rojo de pánico.',
    tags: ['megafonia', 'interfono', 'audio', 'emergencia', 'altavoz', 'panico', 'seguridad'],
    dimensions: { width: 0.40, height: 1.88, depth: 0.40 },
    triBudget: '280-350',
    glbUrl: '/models/modular/sci_audio_intercom_pillar.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_audio_intercom_pillar',
      name: 'Columna de Megafonía e Interfono',
      category: 'fixtures',
      description: 'Poste vertical de comunicaciones de seguridad con altavoz de bocina superior, intercomunicador con micrófono y pulsador rojo de pánico.',
      units: 'meters',
      dimensions: { width: 0.40, height: 1.88, depth: 0.40 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_pedestal_pesada',
          shape: 'cylinder',
          size: [0.20, 0.20, 0.08, 12],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.75,
          metalness: 0.8
        },
        {
          name: 'columna_cilindrica_vertical',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.40, 12],
          position: [0, 0.78, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'modulo_interfono_rejilla',
          shape: 'box',
          size: [0.22, 0.35, 0.15],
          position: [0, 1.30, 0.04],
          color: '#0f172a',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.7
        },
        {
          name: 'pulsador_panico_emergencia',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.035, 12],
          position: [0, 1.22, 0.135],
          rotation: [1.57, 0, 0],
          color: '#e11d48',
          texturePreset: 'red_paint_worn',
          roughness: 0.35,
          metalness: 0.25,
          emissive: '#e11d48',
          emissiveIntensity: 1.2
        },
        {
          name: 'altavoz_bocina_exponencial',
          shape: 'cylinder',
          size: [0.16, 0.08, 0.22, 12],
          position: [0, 1.68, 0.06],
          rotation: [0.25, 0, 0],
          color: '#334155',
          texturePreset: 'metal_perforated',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'luz_estroboscopica_aviso',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.08, 10],
          position: [0, 1.84, 0],
          color: '#38bdf8',
          roughness: 0.15,
          metalness: 0.1,
          emissive: '#38bdf8',
          emissiveIntensity: 1.7
        }
      ]
    }
  }
];
