import type { ModularModelEntry } from './modular-catalog.ts';

export const MODULAR_MODELS_LOTE_4: ModularModelEntry[] = [
  // -------------------------------------------------------------------------
  // 01. CONTENEDOR DE CARGA PRESURIZADO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cargo_container_pressurized',
    family: 'sci_cargo_container_pressurized',
    name: 'Contenedor de Carga Presurizado',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Contenedor intermodal estanco con costillas estructurales de refuerzo, esquineros de izado magnético y display de presurización.',
    tags: ['contenedor', 'carga', 'presurizado', 'intermodal', 'hangar', 'almacen', 'logistica'],
    dimensions: { width: 1.66, height: 1.45, depth: 2.45 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_cargo_container_pressurized.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cargo_container_pressurized',
      name: 'Contenedor de Carga Presurizado',
      category: 'infrastructure',
      description: 'Contenedor intermodal estanco con costillas estructurales de refuerzo, esquineros de izado magnético y display de presurización.',
      units: 'meters',
      dimensions: { width: 1.66, height: 1.45, depth: 2.45 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_cuerpo_principal',
          shape: 'box',
          size: [1.60, 1.40, 2.40],
          position: [0, 0.70, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'costilla_refuerzo_1',
          shape: 'box',
          size: [1.66, 1.44, 0.12],
          position: [0, 0.70, -0.70],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'costilla_refuerzo_2',
          shape: 'box',
          size: [1.66, 1.44, 0.12],
          position: [0, 0.70, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'costilla_refuerzo_3',
          shape: 'box',
          size: [1.66, 1.44, 0.12],
          position: [0, 0.70, 0.70],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'esquinero_izado_inferior_so',
          shape: 'box',
          size: [0.18, 0.18, 0.18],
          position: [-0.74, 0.09, -1.14],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'esquinero_izado_inferior_se',
          shape: 'box',
          size: [0.18, 0.18, 0.18],
          position: [0.74, 0.09, -1.14],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'esquinero_izado_inferior_no',
          shape: 'box',
          size: [0.18, 0.18, 0.18],
          position: [-0.74, 0.09, 1.14],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'esquinero_izado_inferior_ne',
          shape: 'box',
          size: [0.18, 0.18, 0.18],
          position: [0.74, 0.09, 1.14],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'puerta_doble_estanca_frontal',
          shape: 'box',
          size: [1.44, 1.28, 0.06],
          position: [0, 0.70, 1.21],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'franja_seguridad_borde',
          shape: 'box',
          size: [1.44, 0.12, 0.07],
          position: [0, 0.14, 1.215],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'valvula_manometro_presion',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.05, 12],
          position: [0.45, 1.05, 1.25],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 02. CARRETILLA ELEVADORA AGV AUTÓNOMA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_heavy_forklift_dolly',
    family: 'sci_heavy_forklift_dolly',
    name: 'Carretilla Elevadora AGV Autónoma',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Vehículo industrial autónomo de transporte de palets con escáner LiDAR, mástil hidráulico de elevación y contrapeso fundido.',
    tags: ['carretilla', 'toro', 'agv', 'forklift', 'palets', 'almacen', 'robotica', 'transporte'],
    dimensions: { width: 0.95, height: 1.85, depth: 1.80 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_heavy_forklift_dolly.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_heavy_forklift_dolly',
      name: 'Carretilla Elevadora AGV Autónoma',
      category: 'infrastructure',
      description: 'Vehículo industrial autónomo de transporte de palets con escáner LiDAR, mástil hidráulico de elevación y contrapeso fundido.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.85, depth: 1.80 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bloque_contrapeso_trasero',
          shape: 'box',
          size: [0.90, 0.65, 0.75],
          position: [0, 0.40, -0.65],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'chasis_baterias_central',
          shape: 'box',
          size: [0.82, 0.50, 0.70],
          position: [0, 0.35, 0.05],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'mastil_vertical_doble_acero',
          shape: 'box',
          size: [0.65, 1.65, 0.10],
          position: [0, 0.90, 0.45],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.85
        },
        {
          name: 'carro_portahorquillas',
          shape: 'box',
          size: [0.72, 0.22, 0.06],
          position: [0, 0.45, 0.52],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.9
        },
        {
          name: 'horquilla_acero_izq',
          shape: 'box',
          size: [0.10, 0.04, 1.05],
          position: [-0.22, 0.10, 1.02],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'horquilla_acero_der',
          shape: 'box',
          size: [0.10, 0.04, 1.05],
          position: [0.22, 0.10, 1.02],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'sensor_lidar_frontal',
          shape: 'cylinder',
          size: [0.09, 0.09, 0.08, 12],
          position: [0, 0.68, 0.46],
          color: '#111827',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'baliza_estroboscopica_techo',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.10, 10],
          position: [0, 1.78, 0.45],
          color: '#f59e0b',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'rueda_motriz_trasera_izq',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.10, 12],
          position: [-0.44, 0.14, -0.65],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'rueda_motriz_trasera_der',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.10, 12],
          position: [0.44, 0.14, -0.65],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 03. PALET DE RETENCIÓN ANTIDERRAME PARA 4 BIDONES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_drum_pallet_containment',
    family: 'sci_drum_pallet_containment',
    name: 'Palet de Retención Antiderrame para 4 Bidones',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Plataforma modular estanca para recogida de fugas con rejilla de polietileno desmontable y 4 bidones químicos de alta resistencia.',
    tags: ['antiderrame', 'bidones', 'quimica', 'retencion', 'palet', 'hazmat', 'seguridad'],
    dimensions: { width: 1.30, height: 1.25, depth: 1.30 },
    triBudget: '400-500',
    glbUrl: '/models/modular/sci_drum_pallet_containment.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_drum_pallet_containment',
      name: 'Palet de Retención Antiderrame para 4 Bidones',
      category: 'infrastructure',
      description: 'Plataforma modular estanca para recogida de fugas con rejilla de polietileno desmontable y 4 bidones químicos de alta resistencia.',
      units: 'meters',
      dimensions: { width: 1.30, height: 1.25, depth: 1.30 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cubeta_retencion_polietileno',
          shape: 'box',
          size: [1.30, 0.28, 1.30],
          position: [0, 0.14, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'rejilla_superior_drenaje',
          shape: 'box',
          size: [1.22, 0.04, 1.22],
          position: [0, 0.29, 0],
          color: '#334155',
          texturePreset: 'metal_perforated',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'bidon_quimico_so',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.88, 16],
          position: [-0.34, 0.75, -0.34],
          color: '#2563eb',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'bidon_quimico_se',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.88, 16],
          position: [0.34, 0.75, -0.34],
          color: '#2563eb',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'bidon_quimico_no',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.88, 16],
          position: [-0.34, 0.75, 0.34],
          color: '#dc2626',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'bidon_quimico_ne',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.88, 16],
          position: [0.34, 0.75, 0.34],
          color: '#16a34a',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'tapon_roscado_so',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.04, 8],
          position: [-0.26, 1.21, -0.34],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'tapon_roscado_se',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.04, 8],
          position: [0.26, 1.21, -0.34],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'franja_peligro_cubeta',
          shape: 'box',
          size: [1.31, 0.08, 0.02],
          position: [0, 0.20, 0.655],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 04. ESFERA DE COMBUSTIBLE CRIOGÉNICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cryo_fuel_storage_sphere',
    family: 'sci_cryo_fuel_storage_sphere',
    name: 'Esfera de Combustible Criogénico',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Tanque esférico de contención térmica de doble casco al vacío para propelente, montado sobre cuna de acero de 4 apoyos arriostrados.',
    tags: ['combustible', 'criogenico', 'esfera', 'propelente', 'hidrogeno', 'tanque', 'energia'],
    dimensions: { width: 1.40, height: 2.05, depth: 1.40 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_cryo_fuel_storage_sphere.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cryo_fuel_storage_sphere',
      name: 'Esfera de Combustible Criogénico',
      category: 'infrastructure',
      description: 'Tanque esférico de contención térmica de doble casco al vacío para propelente, montado sobre cuna de acero de 4 apoyos arriostrados.',
      units: 'meters',
      dimensions: { width: 1.40, height: 2.05, depth: 1.40 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'plinto_cimientos_hormigon',
          shape: 'box',
          size: [1.40, 0.12, 1.40],
          position: [0, 0.06, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'pata_cuna_soporte_so',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.75, 8],
          position: [-0.45, 0.45, -0.45],
          rotation: [0.2, 0, -0.2],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pata_cuna_soporte_se',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.75, 8],
          position: [0.45, 0.45, -0.45],
          rotation: [0.2, 0, 0.2],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pata_cuna_soporte_no',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.75, 8],
          position: [-0.45, 0.45, 0.45],
          rotation: [-0.2, 0, -0.2],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pata_cuna_soporte_ne',
          shape: 'cylinder',
          size: [0.05, 0.05, 0.75, 8],
          position: [0.45, 0.45, 0.45],
          rotation: [-0.2, 0, 0.2],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'esfera_tanque_principal',
          shape: 'sphere',
          size: [0.65, 16, 16],
          position: [0, 1.15, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'anillo_ecuatorial_soldadura',
          shape: 'ring',
          size: [0.66, 0.05, 16],
          position: [0, 1.15, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'tubo_carga_inferior',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.55, 8],
          position: [0, 0.35, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'valvula_venteo_superior',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.25, 8],
          position: [0, 1.88, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'panel_telemetria_presion',
          shape: 'box',
          size: [0.20, 0.16, 0.04],
          position: [0.55, 0.95, 0.35],
          color: '#334155',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 05. RAMPA HIDRÁULICA DE MUELLE DE CARGA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_hydraulic_loading_dock_ramp',
    family: 'sci_hydraulic_loading_dock_ramp',
    name: 'Rampa Hidráulica de Muelle de Carga',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Plataforma basculante con chapa lagrimada antideslizante, labios articulados de acople a vehículos y defensas de impacto laterales.',
    tags: ['rampa', 'muelle', 'carga', 'hidraulica', 'camion', 'hangar', 'plataforma'],
    dimensions: { width: 1.60, height: 0.65, depth: 1.85 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_hydraulic_loading_dock_ramp.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_hydraulic_loading_dock_ramp',
      name: 'Rampa Hidráulica de Muelle de Carga',
      category: 'infrastructure',
      description: 'Plataforma basculante con chapa lagrimada antideslizante, labios articulados de acople a vehículos y defensas de impacto laterales.',
      units: 'meters',
      dimensions: { width: 1.60, height: 0.65, depth: 1.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'foso_marco_empotrado',
          shape: 'box',
          size: [1.40, 0.35, 1.80],
          position: [0, 0.175, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'plataforma_chapa_lagrimada',
          shape: 'box',
          size: [1.25, 0.08, 1.50],
          position: [0, 0.34, -0.10],
          color: '#64748b',
          texturePreset: 'diamond_plate',
          roughness: 0.45,
          metalness: 0.85
        },
        {
          name: 'labio_articulado_acople',
          shape: 'wedge',
          size: [1.20, 0.06, 0.35],
          position: [0, 0.33, 0.75],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'cilindro_hidraulico_central',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.45, 8],
          position: [0, 0.18, -0.15],
          rotation: [0.4, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'defensa_impacto_izq',
          shape: 'box',
          size: [0.12, 0.38, 0.18],
          position: [-0.68, 0.20, 0.88],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'defensa_impacto_der',
          shape: 'box',
          size: [0.12, 0.38, 0.18],
          position: [0.68, 0.20, 0.88],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'franja_seguridad_amarilla',
          shape: 'box',
          size: [1.26, 0.07, 0.02],
          position: [0, 0.34, -0.86],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'botonera_mando_pared',
          shape: 'box',
          size: [0.14, 0.22, 0.06],
          position: [0.75, 0.55, 0.10],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 06. POLIPASTO DE PUENTE GRÚA DE GRAN TONELAJE
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_heavy_overhead_crane_trolley',
    family: 'sci_heavy_overhead_crane_trolley',
    name: 'Polipasto de Puente Grúa de Gran Tonelaje',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Carro rodante de suspensión para viga de hangar con motorreductor eléctrico, tambor de cable de acero y gancho forjado de carga pesada.',
    tags: ['polipasto', 'grua', 'gancho', 'cable', 'elevacion', 'hangar', 'puente grua'],
    dimensions: { width: 1.80, height: 2.10, depth: 0.55 },
    triBudget: '380-480',
    glbUrl: '/models/modular/sci_heavy_overhead_crane_trolley.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_heavy_overhead_crane_trolley',
      name: 'Polipasto de Puente Grúa de Gran Tonelaje',
      category: 'infrastructure',
      description: 'Carro rodante de suspensión para viga de hangar con motorreductor eléctrico, tambor de cable de acero y gancho forjado de carga pesada.',
      units: 'meters',
      dimensions: { width: 1.80, height: 2.10, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'viga_carril_perfil_ipn',
          shape: 'box',
          size: [1.80, 0.24, 0.28],
          position: [0, 1.95, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'carro_placas_laterales',
          shape: 'box',
          size: [0.65, 0.28, 0.46],
          position: [0, 1.84, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'tambor_arrollamiento_cable',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.38, 12],
          position: [0, 1.55, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'motorreductor_blindado',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.32, 10],
          position: [0.38, 1.55, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'cable_doble_acero',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.65, 6],
          position: [0, 1.10, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'moton_polea_gancho',
          shape: 'box',
          size: [0.20, 0.22, 0.14],
          position: [0, 0.72, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'gancho_doble_forja',
          shape: 'torus',
          size: [0.11, 0.035, 12, 12],
          position: [0, 0.46, 0],
          rotation: [0, Math.PI / 2, 0],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 07. COMPUERTA ESCLUSA ESTANCA DE MAMPARO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_pressure_bulkhead_airlock',
    family: 'sci_pressure_bulkhead_airlock',
    name: 'Compuerta Esclusa Estanca de Mamparo',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Marco de mamparo para túnel de carga con compuerta corredera seccional, junta de presurización neumática y cerradura pasante.',
    tags: ['mamparo', 'esclusa', 'puerta', 'estanca', 'presion', 'hangar', 'blindaje'],
    dimensions: { width: 1.85, height: 2.25, depth: 0.35 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_pressure_bulkhead_airlock.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_pressure_bulkhead_airlock',
      name: 'Compuerta Esclusa Estanca de Mamparo',
      category: 'infrastructure',
      description: 'Marco de mamparo para túnel de carga con compuerta corredera seccional, junta de presurización neumática y cerradura pasante.',
      units: 'meters',
      dimensions: { width: 1.85, height: 2.25, depth: 0.35 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'marco_portal_reforzado',
          shape: 'box',
          size: [1.85, 2.25, 0.28],
          position: [0, 1.125, 0],
          color: '#1e293b',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'hueco_paso_interior',
          shape: 'box',
          size: [1.25, 1.85, 0.30],
          position: [0, 0.95, 0],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.8,
          metalness: 0.7
        },
        {
          name: 'hoja_puerta_seccion_izq',
          shape: 'box',
          size: [0.65, 1.82, 0.10],
          position: [-0.30, 0.95, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.85
        },
        {
          name: 'hoja_puerta_seccion_der',
          shape: 'box',
          size: [0.65, 1.82, 0.10],
          position: [0.30, 0.95, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.85
        },
        {
          name: 'guia_carril_superior_corredera',
          shape: 'box',
          size: [1.65, 0.14, 0.16],
          position: [0, 1.95, 0.08],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'franja_diagonal_peligro',
          shape: 'box',
          size: [1.25, 0.14, 0.02],
          position: [0, 0.10, 0.06],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'volante_bloqueo_emergencia',
          shape: 'ring',
          size: [0.18, 0.035, 8],
          position: [0, 1.05, 0.07],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'panel_luces_presion_led',
          shape: 'box',
          size: [0.12, 0.28, 0.04],
          position: [0.72, 1.45, 0.15],
          color: '#ef4444',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 08. ARMARIO BLINDADO DE MATERIALES PELIGROSOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_hazardous_materials_locker',
    family: 'sci_hazardous_materials_locker',
    name: 'Armario Blindado de Materiales Peligrosos',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Gabinete ignífugo de seguridad industrial con doble pared de chapa aislada, bandeja antiderrames inferior y etiquetado Hazmat.',
    tags: ['armario', 'hazmat', 'inflamables', 'seguridad', 'quimicos', 'almacen', 'ignifugo'],
    dimensions: { width: 1.05, height: 1.80, depth: 0.65 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_hazardous_materials_locker.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_hazardous_materials_locker',
      name: 'Armario Blindado de Materiales Peligrosos',
      category: 'infrastructure',
      description: 'Gabinete ignífugo de seguridad industrial con doble pared de chapa aislada, bandeja antiderrames inferior y etiquetado Hazmat.',
      units: 'meters',
      dimensions: { width: 1.05, height: 1.80, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_plinto_nivelacion',
          shape: 'box',
          size: [1.05, 0.08, 0.65],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'cuerpo_armario_ignifugo',
          shape: 'box',
          size: [1.00, 1.70, 0.60],
          position: [0, 0.93, 0],
          color: '#facc15',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'puerta_doble_falleba',
          shape: 'box',
          size: [0.96, 1.58, 0.05],
          position: [0, 0.94, 0.31],
          color: '#eab308',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'manija_cierre_3_puntos',
          shape: 'box',
          size: [0.04, 0.32, 0.05],
          position: [0, 0.95, 0.35],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'bandeja_receptora_fugas',
          shape: 'box',
          size: [0.90, 0.06, 0.50],
          position: [0, 0.20, 0.02],
          color: '#64748b',
          texturePreset: 'metal_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'balda_perforada_intermedia',
          shape: 'box',
          size: [0.90, 0.03, 0.50],
          position: [0, 0.78, 0.02],
          color: '#94a3b8',
          texturePreset: 'metal_perforated',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'rejilla_ventilacion_antillamas',
          shape: 'box',
          size: [0.22, 0.12, 0.02],
          position: [-0.40, 1.62, 0.315],
          color: '#334155',
          texturePreset: 'server_vent_panel',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'rombo_nfpa_pictograma',
          shape: 'box',
          size: [0.18, 0.18, 0.01],
          position: [0.25, 1.45, 0.34],
          color: '#ffffff',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 09. ESTACIÓN DE TRANSFERENCIA Y RODILLOS TRANSPORTADORES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_conveyor_transfer_station',
    family: 'sci_conveyor_transfer_station',
    name: 'Estación de Transferencia y Rodillos Transportadores',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Módulo transportador motorizado para cajas pesadas con rodillos galvanizados, guías laterales y motorreductor de tracción.',
    tags: ['transportador', 'rodillos', 'conveyor', 'almacen', 'logistica', 'motor', 'paquetes'],
    dimensions: { width: 1.20, height: 0.90, depth: 1.85 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_conveyor_transfer_station.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_conveyor_transfer_station',
      name: 'Estación de Transferencia y Rodillos Transportadores',
      category: 'infrastructure',
      description: 'Módulo transportador motorizado para cajas pesadas con rodillos galvanizados, guías laterales y motorreductor de tracción.',
      units: 'meters',
      dimensions: { width: 1.20, height: 0.90, depth: 1.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'patas_bastidor_tubular_izq',
          shape: 'box',
          size: [0.08, 0.65, 0.85],
          position: [-0.55, 0.325, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'patas_bastidor_tubular_der',
          shape: 'box',
          size: [0.08, 0.65, 0.85],
          position: [0.55, 0.325, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'larguero_soporte_izq',
          shape: 'box',
          size: [0.05, 0.12, 1.80],
          position: [-0.50, 0.68, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'larguero_soporte_der',
          shape: 'box',
          size: [0.05, 0.12, 1.80],
          position: [0.50, 0.68, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'cama_rodillos_galvanizados',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.94, 12],
          position: [0, 0.72, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'rodillo_secundario_frontal',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.94, 12],
          position: [0, 0.72, 0.45],
          rotation: [0, 0, Math.PI / 2],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'rodillo_secundario_trasero',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.94, 12],
          position: [0, 0.72, -0.45],
          rotation: [0, 0, Math.PI / 2],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'motorreductor_lateral',
          shape: 'cylinder',
          size: [0.12, 0.12, 0.22, 10],
          position: [-0.58, 0.62, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'guia_lateral_regulable_izq',
          shape: 'box',
          size: [0.03, 0.10, 1.80],
          position: [-0.44, 0.82, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'guia_lateral_regulable_der',
          shape: 'box',
          size: [0.03, 0.10, 1.80],
          position: [0.44, 0.82, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 10. ESTANTERÍA DE PALETIZACIÓN PARA CARGAS PESADAS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_pallet_stacker_rack_heavy',
    family: 'sci_pallet_stacker_rack_heavy',
    name: 'Estantería de Paletización para Cargas Pesadas',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Estructura industrial de gran altura con montantes ranurados, largueros de seguridad y dos palets cargados con cajas flejadas.',
    tags: ['estanteria', 'rack', 'paletizacion', 'almacen', 'cargas', 'industrial', 'cajas'],
    dimensions: { width: 1.65, height: 2.30, depth: 0.95 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_pallet_stacker_rack_heavy.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_pallet_stacker_rack_heavy',
      name: 'Estantería de Paletización para Cargas Pesadas',
      category: 'infrastructure',
      description: 'Estructura industrial de gran altura con montantes ranurados, largueros de seguridad y dos palets cargados con cajas flejadas.',
      units: 'meters',
      dimensions: { width: 1.65, height: 2.30, depth: 0.95 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'montante_celosia_izq',
          shape: 'box',
          size: [0.10, 2.30, 0.90],
          position: [-0.75, 1.15, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'montante_celosia_der',
          shape: 'box',
          size: [0.10, 2.30, 0.90],
          position: [0.75, 1.15, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'larguero_viga_nivel_1',
          shape: 'box',
          size: [1.44, 0.10, 0.08],
          position: [0, 0.20, 0.40],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'larguero_viga_nivel_2',
          shape: 'box',
          size: [1.44, 0.10, 0.08],
          position: [0, 1.25, 0.40],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'palet_madera_nivel_1',
          shape: 'box',
          size: [1.20, 0.12, 0.80],
          position: [0, 0.31, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'caja_carga_pesada_1',
          shape: 'box',
          size: [1.10, 0.75, 0.75],
          position: [0, 0.74, 0],
          color: '#64748b',
          texturePreset: 'metal_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'palet_madera_nivel_2',
          shape: 'box',
          size: [1.20, 0.12, 0.80],
          position: [0, 1.36, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'cajas_apiladas_nivel_2',
          shape: 'box',
          size: [1.05, 0.65, 0.70],
          position: [0, 1.74, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'placas_anclaje_suelo',
          shape: 'box',
          size: [1.65, 0.04, 0.95],
          position: [0, 0.02, 0],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.8,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 11. TURBINA CENTRÍFUGA DE EXTRACCIÓN DE VAHO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_industrial_ventilation_blower',
    family: 'sci_industrial_ventilation_blower',
    name: 'Turbina Centrífuga de Extracción de Vaho',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Extractor industrial de alta presión con voluta helicoidal de acero, motor eléctrico trifásico blindado y tobera de impulsión.',
    tags: ['turbina', 'ventilacion', 'extractor', 'voluta', 'motor', 'industrial', 'aire'],
    dimensions: { width: 0.95, height: 1.10, depth: 1.15 },
    triBudget: '400-480',
    glbUrl: '/models/modular/sci_industrial_ventilation_blower.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_industrial_ventilation_blower',
      name: 'Turbina Centrífuga de Extracción de Vaho',
      category: 'infrastructure',
      description: 'Extractor industrial de alta presión con voluta helicoidal de acero, motor eléctrico trifásico blindado y tobera de impulsión.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.10, depth: 1.15 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bancada_chasis_amortiguacion',
          shape: 'box',
          size: [0.90, 0.10, 1.10],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'carcasa_voluta_espiral',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.35, 16],
          position: [-0.15, 0.55, 0.10],
          rotation: [Math.PI / 2, 0, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.8
        },
        {
          name: 'conducto_salida_tangencial',
          shape: 'box',
          size: [0.35, 0.45, 0.34],
          position: [-0.15, 0.85, 0.10],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.55,
          metalness: 0.8
        },
        {
          name: 'tobera_admision_circular',
          shape: 'cylinder',
          size: [0.28, 0.28, 0.14, 16],
          position: [-0.15, 0.55, 0.34],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.85
        },
        {
          name: 'rejilla_malla_protectora',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.02, 16],
          position: [-0.15, 0.55, 0.42],
          color: '#94a3b8',
          texturePreset: 'metal_perforated',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'motor_electrico_trifasico',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.42, 12],
          position: [0.28, 0.45, -0.15],
          rotation: [0, 0, Math.PI / 2],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'aletas_refrigeracion_motor',
          shape: 'cylinder',
          size: [0.20, 0.20, 0.30, 12],
          position: [0.28, 0.45, -0.15],
          rotation: [0, 0, Math.PI / 2],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.85
        },
        {
          name: 'caja_bornes_conexion',
          shape: 'box',
          size: [0.14, 0.12, 0.10],
          position: [0.28, 0.68, -0.15],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 12. CELDA DE CONTENCIÓN MAGNÉTICA DE PLASMA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_magnetic_containment_cell',
    family: 'sci_magnetic_containment_cell',
    name: 'Celda de Contención Magnética de Plasma',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Cámara cilíndrica de confinamiento de plasma energético con bobinas superconductoras toroidales y visor de vidrio reforzado.',
    tags: ['confinamiento', 'plasma', 'fusion', 'magnetico', 'energia', 'reactor', 'exotico'],
    dimensions: { width: 1.40, height: 1.65, depth: 1.40 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_magnetic_containment_cell.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_magnetic_containment_cell',
      name: 'Celda de Contención Magnética de Plasma',
      category: 'infrastructure',
      description: 'Cámara cilíndrica de confinamiento de plasma energético con bobinas superconductoras toroidales y visor de vidrio reforzado.',
      units: 'meters',
      dimensions: { width: 1.40, height: 1.65, depth: 1.40 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_plataforma_hexagonal',
          shape: 'cylinder',
          size: [0.70, 0.70, 0.14, 6],
          position: [0, 0.07, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'cilindro_vacio_camara',
          shape: 'cylinder',
          size: [0.42, 0.42, 1.25, 16],
          position: [0, 0.76, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'visor_cristal_confinamiento',
          shape: 'cylinder',
          size: [0.36, 0.36, 0.85, 16],
          position: [0, 0.76, 0],
          color: '#c084fc',
          texturePreset: 'reinforced_glass',
          opacity: 0.55,
          roughness: 0.15,
          metalness: 0.1
        },
        {
          name: 'nucleo_plasma_luminiscente',
          shape: 'sphere',
          size: [0.18, 12, 12],
          position: [0, 0.76, 0],
          color: '#8b5cf6',
          roughness: 0.05,
          metalness: 0.0
        },
        {
          name: 'bobina_toroidal_cobre_1',
          shape: 'torus',
          size: [0.46, 0.05, 10, 16],
          position: [0, 0.45, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'bobina_toroidal_cobre_2',
          shape: 'torus',
          size: [0.46, 0.05, 10, 16],
          position: [0, 1.05, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'cabezal_nodo_presurizador',
          shape: 'cylinder',
          size: [0.55, 0.55, 0.18, 12],
          position: [0, 1.45, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'conducto_cables_potencia',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.85, 8],
          position: [0.48, 0.50, 0.20],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 13. PUENTE PÓRTICO PORTATUBERÍAS Y PASARELA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_gantry_pipe_bridge',
    family: 'sci_gantry_pipe_bridge',
    name: 'Puente Pórtico Portatuberías y Pasarela',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Pórtico estructural de hangar con haces de tuberías pesadas para combustible/refrigerante y pasarela técnica de mantenimiento.',
    tags: ['portico', 'tuberias', 'pasarela', 'hangar', 'puente', 'combustible', 'industrial'],
    dimensions: { width: 1.95, height: 2.45, depth: 0.65 },
    triBudget: '400-500',
    glbUrl: '/models/modular/sci_gantry_pipe_bridge.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_gantry_pipe_bridge',
      name: 'Puente Pórtico Portatuberías y Pasarela',
      category: 'infrastructure',
      description: 'Pórtico estructural de hangar con haces de tuberías pesadas para combustible/refrigerante y pasarela técnica de mantenimiento.',
      units: 'meters',
      dimensions: { width: 1.95, height: 2.45, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'columna_portico_izq',
          shape: 'box',
          size: [0.18, 2.40, 0.25],
          position: [-0.90, 1.20, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'columna_portico_der',
          shape: 'box',
          size: [0.18, 2.40, 0.25],
          position: [0.90, 1.20, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'viga_dintel_superior',
          shape: 'box',
          size: [1.95, 0.22, 0.35],
          position: [0, 2.30, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'tuberia_hidrogeno_diametro_grande',
          shape: 'cylinder',
          size: [0.10, 0.10, 1.95, 12],
          position: [0, 2.05, -0.08],
          rotation: [0, 0, Math.PI / 2],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.85
        },
        {
          name: 'tuberia_refrigerante_cobre',
          shape: 'cylinder',
          size: [0.06, 0.06, 1.95, 10],
          position: [0, 1.92, 0.08],
          rotation: [0, 0, Math.PI / 2],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'pasarela_rejilla_transeuntes',
          shape: 'box',
          size: [1.90, 0.05, 0.55],
          position: [0, 1.70, 0],
          color: '#64748b',
          texturePreset: 'diamond_plate',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'barandilla_seguridad_acero',
          shape: 'box',
          size: [1.90, 0.40, 0.03],
          position: [0, 1.92, 0.26],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'anclaje_zapata_suelo_izq',
          shape: 'box',
          size: [0.35, 0.08, 0.40],
          position: [-0.90, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'anclaje_zapata_suelo_der',
          shape: 'box',
          size: [0.35, 0.08, 0.40],
          position: [0.90, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 14. GENERADOR ELÉCTRICO MÓVIL SOBRE REMOLQUE
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_mobile_generator_trailer',
    family: 'sci_mobile_generator_trailer',
    name: 'Generador Eléctrico Móvil sobre Remolque',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Generador auxiliar diésel/fusión insonorizado sobre chasis de remolque con enganche, silenciador vertical y cuadro de distribución.',
    tags: ['generador', 'remolque', 'diesel', 'fusion', 'movil', 'energia', 'electricidad'],
    dimensions: { width: 1.15, height: 1.65, depth: 1.95 },
    triBudget: '400-480',
    glbUrl: '/models/modular/sci_mobile_generator_trailer.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_mobile_generator_trailer',
      name: 'Generador Eléctrico Móvil sobre Remolque',
      category: 'infrastructure',
      description: 'Generador auxiliar diésel/fusión insonorizado sobre chasis de remolque con enganche, silenciador vertical y cuadro de distribución.',
      units: 'meters',
      dimensions: { width: 1.15, height: 1.65, depth: 1.95 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_remolque_perfiles',
          shape: 'box',
          size: [0.85, 0.12, 1.85],
          position: [0, 0.25, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.85
        },
        {
          name: 'timon_enganche_remolque',
          shape: 'box',
          size: [0.20, 0.08, 0.65],
          position: [0, 0.25, 1.20],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.9
        },
        {
          name: 'rueda_neumatica_izq',
          shape: 'cylinder',
          size: [0.22, 0.22, 0.14, 12],
          position: [-0.50, 0.22, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'rueda_neumatica_der',
          shape: 'cylinder',
          size: [0.22, 0.22, 0.14, 12],
          position: [0.50, 0.22, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cabina_insonorizada_generador',
          shape: 'box',
          size: [0.75, 0.85, 1.35],
          position: [0, 0.73, -0.10],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'silenciador_escape_vertical',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.60, 8],
          position: [0.26, 1.35, -0.55],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'panel_tomas_corriente_trifasicas',
          shape: 'box',
          size: [0.45, 0.28, 0.04],
          position: [0, 0.75, -0.78],
          color: '#334155',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'paragolpes_trasero_senalizado',
          shape: 'box',
          size: [0.85, 0.10, 0.04],
          position: [0, 0.25, -0.95],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 15. PUERTA CIRCULAR DE BÓVEDA ACORAZADA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_secure_vault_door_vault',
    family: 'sci_secure_vault_door_vault',
    name: 'Puerta Circular de Bóveda Acorazada',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Puerta masiva estanca de aleación de carburo con pernos radiales de cierre, timón de maniobra cromado y bisagra articulada pesada.',
    tags: ['boveda', 'acorazada', 'puerta', 'seguridad', 'carburo', 'blindaje', 'timon'],
    dimensions: { width: 1.80, height: 2.00, depth: 0.40 },
    triBudget: '400-500',
    glbUrl: '/models/modular/sci_secure_vault_door_vault.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_secure_vault_door_vault',
      name: 'Puerta Circular de Bóveda Acorazada',
      category: 'infrastructure',
      description: 'Puerta masiva estanca de aleación de carburo con pernos radiales de cierre, timón de maniobra cromado y bisagra articulada pesada.',
      units: 'meters',
      dimensions: { width: 1.80, height: 2.00, depth: 0.40 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'marco_cuadrado_empotrado',
          shape: 'box',
          size: [1.80, 2.00, 0.25],
          position: [0, 1.00, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'anillo_estanqueidad_cerco',
          shape: 'cylinder',
          size: [0.65, 0.65, 0.10, 16],
          position: [0, 1.00, 0.08],
          rotation: [Math.PI / 2, 0, 0],
          color: '#64748b',
          texturePreset: 'steel_galvanized',
          roughness: 0.45,
          metalness: 0.85
        },
        {
          name: 'disco_puerta_acorazada',
          shape: 'cylinder',
          size: [0.62, 0.62, 0.14, 16],
          position: [0, 1.00, 0.15],
          rotation: [Math.PI / 2, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'timon_giro_maniobra',
          shape: 'ring',
          size: [0.26, 0.04, 8],
          position: [0, 1.00, 0.24],
          color: '#f8fafc',
          texturePreset: 'aluminum_anodized',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'eje_central_cerradura',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.12, 10],
          position: [0, 1.00, 0.26],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'brazo_bisagra_portante',
          shape: 'box',
          size: [0.35, 1.20, 0.15],
          position: [0.72, 1.00, 0.14],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.9
        },
        {
          name: 'perno_radial_superior',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.20, 8],
          position: [0, 1.62, 0.15],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'perno_radial_inferior',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.20, 8],
          position: [0, 0.38, 0.15],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 16. BATERÍA MANIFOLD DE BOTELLAS DE GAS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_high_pressure_gas_manifold',
    family: 'sci_high_pressure_gas_manifold',
    name: 'Batería Manifold de Botellas de Gas',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Rack mural para 6 cilindros de gas comprimido a alta presión con colector común de latón, manómetro central y cadenas de retención.',
    tags: ['manifold', 'gas', 'botellas', 'oxigeno', 'argon', 'presion', 'industrial'],
    dimensions: { width: 1.25, height: 1.55, depth: 0.55 },
    triBudget: '400-500',
    glbUrl: '/models/modular/sci_high_pressure_gas_manifold.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_high_pressure_gas_manifold',
      name: 'Batería Manifold de Botellas de Gas',
      category: 'infrastructure',
      description: 'Rack mural para 6 cilindros de gas comprimido a alta presión con colector común de latón, manómetro central y cadenas de retención.',
      units: 'meters',
      dimensions: { width: 1.25, height: 1.55, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bancada_marco_acero',
          shape: 'box',
          size: [1.25, 0.10, 0.55],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'columna_vertical_apoyo',
          shape: 'box',
          size: [1.20, 1.45, 0.06],
          position: [0, 0.80, -0.22],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'botella_gas_1',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.25, 10],
          position: [-0.45, 0.72, 0],
          color: '#16a34a',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'botella_gas_2',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.25, 10],
          position: [-0.27, 0.72, 0],
          color: '#16a34a',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'botella_gas_3',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.25, 10],
          position: [-0.09, 0.72, 0],
          color: '#dc2626',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'botella_gas_4',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.25, 10],
          position: [0.09, 0.72, 0],
          color: '#dc2626',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'botella_gas_5',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.25, 10],
          position: [0.27, 0.72, 0],
          color: '#2563eb',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'botella_gas_6',
          shape: 'cylinder',
          size: [0.08, 0.08, 1.25, 10],
          position: [0.45, 0.72, 0],
          color: '#2563eb',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.2
        },
        {
          name: 'barra_colector_cobre',
          shape: 'cylinder',
          size: [0.02, 0.02, 1.10, 8],
          position: [0, 1.38, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'manometro_regulador_general',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.04, 12],
          position: [0, 1.48, 0.05],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 17. CARRO DE CONTROL DE DERRAMES QUÍMICOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_spill_response_cart',
    family: 'sci_spill_response_cart',
    name: 'Carro de Control de Derrames Químicos',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Estación móvil de intervención rápida ante fugas químicas con dispensador de absorbente en rollo y contenedor estanco.',
    tags: ['derrames', 'emergencia', 'quimica', 'absorbente', 'carro', 'hazmat', 'intervencion'],
    dimensions: { width: 0.85, height: 1.15, depth: 0.65 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_spill_response_cart.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_spill_response_cart',
      name: 'Carro de Control de Derrames Químicos',
      category: 'infrastructure',
      description: 'Estación móvil de intervención rápida ante fugas químicas con dispensador de absorbente en rollo y contenedor estanco.',
      units: 'meters',
      dimensions: { width: 0.85, height: 1.15, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_polietileno_amarillo',
          shape: 'box',
          size: [0.70, 0.85, 0.55],
          position: [0, 0.50, 0],
          color: '#facc15',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'rueda_industrial_goma_izq',
          shape: 'cylinder',
          size: [0.12, 0.12, 0.08, 10],
          position: [-0.38, 0.12, -0.15],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'rueda_industrial_goma_der',
          shape: 'cylinder',
          size: [0.12, 0.12, 0.08, 10],
          position: [0.38, 0.12, -0.15],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'tapa_superior_abatible',
          shape: 'box',
          size: [0.68, 0.06, 0.52],
          position: [0, 0.95, 0],
          color: '#eab308',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'dispensador_rollo_absorbente',
          shape: 'cylinder',
          size: [0.10, 0.10, 0.50, 12],
          position: [0, 0.65, 0.32],
          rotation: [0, 0, Math.PI / 2],
          color: '#cbd5e1',
          texturePreset: 'silicone_medical',
          roughness: 0.5,
          metalness: 0.05
        },
        {
          name: 'asa_tubular_maniobra',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.60, 8],
          position: [0, 1.05, -0.28],
          rotation: [0, 0, Math.PI / 2],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'rotulo_pictograma_hazmat',
          shape: 'box',
          size: [0.35, 0.18, 0.01],
          position: [0, 0.45, 0.28],
          color: '#ffffff',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 18. CONTENEDOR CISTERNA INTERMODAL ISO TANK
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_intermodal_liquid_tank_container',
    family: 'sci_intermodal_liquid_tank_container',
    name: 'Contenedor Cisterna Intermodal ISO Tank',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Cisterna cilíndrica de acero inoxidable al vacío montada dentro de un bastidor cúbico ISO de 20 pies con pasarela y bocas de llenado.',
    tags: ['cisterna', 'iso tank', 'intermodal', 'liquidos', 'quimica', 'transporte', 'contenedor'],
    dimensions: { width: 1.45, height: 1.50, depth: 2.45 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_intermodal_liquid_tank_container.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_intermodal_liquid_tank_container',
      name: 'Contenedor Cisterna Intermodal ISO Tank',
      category: 'infrastructure',
      description: 'Cisterna cilíndrica de acero inoxidable al vacío montada dentro de un bastidor cúbico ISO de 20 pies con pasarela y bocas de llenado.',
      units: 'meters',
      dimensions: { width: 1.45, height: 1.50, depth: 2.45 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bastidor_cubico_iso',
          shape: 'box',
          size: [1.45, 1.45, 2.45],
          position: [0, 0.725, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.85
        },
        {
          name: 'tanque_cilindrico_cisterna',
          shape: 'cylinder',
          size: [0.58, 0.58, 2.30, 16],
          position: [0, 0.725, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'anillo_refuerzo_tanque_1',
          shape: 'cylinder',
          size: [0.60, 0.60, 0.05, 16],
          position: [0, 0.725, -0.60],
          rotation: [Math.PI / 2, 0, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'anillo_refuerzo_tanque_2',
          shape: 'cylinder',
          size: [0.60, 0.60, 0.05, 16],
          position: [0, 0.725, 0.60],
          rotation: [Math.PI / 2, 0, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'boca_hombre_inspeccion',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.08, 12],
          position: [0, 1.35, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'pasarela_superior_rejilla',
          shape: 'box',
          size: [0.55, 0.04, 2.20],
          position: [0, 1.38, 0],
          color: '#64748b',
          texturePreset: 'diamond_plate',
          roughness: 0.5,
          metalness: 0.85
        },
        {
          name: 'valvula_descarga_inferior',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.15, 8],
          position: [0, 0.18, 1.15],
          rotation: [Math.PI / 2, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'placa_caracteristicas_tecnicas',
          shape: 'box',
          size: [0.35, 0.22, 0.02],
          position: [0.73, 0.75, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 19. BARRICADA BLINDADA DEFLECTORA DE ONDA EXPANSIVA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_blast_shield_barrier',
    family: 'sci_blast_shield_barrier',
    name: 'Barricada Blindada Deflectora de Onda Expansiva',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Pantalla balística y antiexplosión en cuña con placas solapadas de aleación pesada, ranuras para carretilla y franjas de peligro.',
    tags: ['barricada', 'deflectora', 'blindaje', 'antiexplosion', 'hangar', 'defensa', 'balistica'],
    dimensions: { width: 1.60, height: 1.45, depth: 0.85 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_blast_shield_barrier.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_blast_shield_barrier',
      name: 'Barricada Blindada Deflectora de Onda Expansiva',
      category: 'infrastructure',
      description: 'Pantalla balística y antiexplosión en cuña con placas solapadas de aleación pesada, ranuras para carretilla y franjas de peligro.',
      units: 'meters',
      dimensions: { width: 1.60, height: 1.45, depth: 0.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_lastrada_pesada',
          shape: 'box',
          size: [1.60, 0.18, 0.85],
          position: [0, 0.09, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'ranura_horquilla_izq',
          shape: 'box',
          size: [0.18, 0.08, 0.88],
          position: [-0.40, 0.09, 0],
          color: '#64748b',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'ranura_horquilla_der',
          shape: 'box',
          size: [0.18, 0.08, 0.88],
          position: [0.40, 0.09, 0],
          color: '#64748b',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'placa_blindada_inferior',
          shape: 'box',
          size: [1.50, 0.65, 0.12],
          position: [0, 0.45, 0.05],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'placa_deflectora_inclinada',
          shape: 'wedge',
          size: [1.50, 0.75, 0.25],
          position: [0, 0.95, -0.05],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'ranura_visor_balistico',
          shape: 'box',
          size: [0.65, 0.10, 0.18],
          position: [0, 1.15, -0.02],
          color: '#38bdf8',
          texturePreset: 'reinforced_glass',
          opacity: 0.6,
          roughness: 0.2,
          metalness: 0.1
        },
        {
          name: 'franja_senalizacion_peligro',
          shape: 'box',
          size: [1.52, 0.12, 0.02],
          position: [0, 0.72, 0.12],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 20. CABRESTANTE ELÉCTRICO DE ARRASTRE PESADO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_industrial_cable_winch_skid',
    family: 'sci_industrial_cable_winch_skid',
    name: 'Cabrestante Eléctrico de Arrastre Pesado',
    batch: 4,
    batchName: 'Contención, Carga e Infraestructura',
    category: 'infrastructure',
    description: 'Torno eléctrico industrial sobre patín de vigas con bobina de cable trenzado, reductor epicicloidal, freno y guía de rodillos.',
    tags: ['cabrestante', 'winch', 'torno', 'cable', 'arrastre', 'hangar', 'traccion'],
    dimensions: { width: 0.95, height: 0.70, depth: 1.30 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_industrial_cable_winch_skid.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_industrial_cable_winch_skid',
      name: 'Cabrestante Eléctrico de Arrastre Pesado',
      category: 'infrastructure',
      description: 'Torno eléctrico industrial sobre patín de vigas con bobina de cable trenzado, reductor epicicloidal, freno y guía de rodillos.',
      units: 'meters',
      dimensions: { width: 0.95, height: 0.70, depth: 1.30 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'patin_vigas_skid_suelo',
          shape: 'box',
          size: [0.95, 0.10, 1.25],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'soportes_chumaceras_tambor',
          shape: 'box',
          size: [0.75, 0.45, 0.10],
          position: [0, 0.30, 0],
          color: '#334155',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.8
        },
        {
          name: 'tambor_arrollador_cable',
          shape: 'cylinder',
          size: [0.22, 0.22, 0.52, 16],
          position: [0, 0.42, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'reductor_epicicloidal_cilindrico',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.22, 12],
          position: [0.38, 0.42, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.85
        },
        {
          name: 'motor_electrico_traccion',
          shape: 'cylinder',
          size: [0.16, 0.16, 0.32, 12],
          position: [-0.38, 0.42, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'caja_freno_disco',
          shape: 'cylinder',
          size: [0.19, 0.19, 0.06, 12],
          position: [-0.20, 0.42, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.85
        },
        {
          name: 'guia_rodillos_salida_cable',
          shape: 'box',
          size: [0.35, 0.25, 0.12],
          position: [0, 0.32, 0.48],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'gancho_cable_arrastre',
          shape: 'torus',
          size: [0.08, 0.025, 8, 12],
          position: [0, 0.32, 0.65],
          rotation: [Math.PI / 2, 0, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        }
      ]
    }
  }
];
