import type { ModelSpec } from '../lib/studio/types.ts';

export interface ModularModelEntry {
  id: string;
  family: string;
  name: string;
  batch: number;
  batchName: string;
  category: string;
  description: string;
  tags: string[];
  dimensions: { width: number; height: number; depth: number };
  triBudget: string;
  glbUrl: string;
  isModular: true;
  spec: ModelSpec;
}

export const MODULAR_MODELS_LOTE_1: ModularModelEntry[] = [
  // -------------------------------------------------------------------------
  // 01. ESCRITORIO DE MANDO MODULAR
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_desk_executive',
    family: 'sci_desk_executive',
    name: 'Escritorio de Mando Modular',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Puesto de mando con tablero biselado, estructura metálica en ángulo, cajonera suspendida, pasacables y faldón de privacidad.',
    tags: ['escritorio', 'mando', 'oficina', 'mueble', 'consola', 'mesa'],
    dimensions: { width: 1.50, height: 0.76, depth: 0.85 },
    triBudget: '280-360',
    glbUrl: '/models/modular/sci_desk_executive.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_desk_executive',
      name: 'Escritorio de Mando Modular',
      category: 'furniture',
      description: 'Puesto de mando con tablero biselado, estructura metálica en ángulo, cajonera suspendida, pasacables y faldón de privacidad.',
      units: 'meters',
      dimensions: { width: 1.50, height: 0.76, depth: 0.85 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'tablero_principal',
          shape: 'box',
          size: [1.50, 0.05, 0.85],
          position: [0, 0.735, 0],
          color: '#2d3748',
          texturePreset: 'wood_dark_panel',
          roughness: 0.4,
          metalness: 0.1
        },
        {
          name: 'marco_soporte_acero',
          shape: 'box',
          size: [1.44, 0.04, 0.80],
          position: [0, 0.69, 0],
          color: '#1a202c',
          texturePreset: 'titanium_aerospace',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'pata_angulo_izq',
          shape: 'box',
          size: [0.06, 0.67, 0.80],
          position: [-0.69, 0.335, 0],
          color: '#a0aec0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'modulo_cajonera_der',
          shape: 'box',
          size: [0.42, 0.58, 0.74],
          position: [0.50, 0.38, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'frente_cajon_superior',
          shape: 'box',
          size: [0.38, 0.16, 0.02],
          position: [0.50, 0.56, 0.38],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.6
        },
        {
          name: 'frente_cajon_medio',
          shape: 'box',
          size: [0.38, 0.16, 0.02],
          position: [0.50, 0.37, 0.38],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.6
        },
        {
          name: 'frente_cajon_inferior',
          shape: 'box',
          size: [0.38, 0.16, 0.02],
          position: [0.50, 0.18, 0.38],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.6
        },
        {
          name: 'tirador_cajon_1',
          shape: 'box',
          size: [0.12, 0.02, 0.02],
          position: [0.50, 0.56, 0.40],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'tirador_cajon_2',
          shape: 'box',
          size: [0.12, 0.02, 0.02],
          position: [0.50, 0.37, 0.40],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'tirador_cajon_3',
          shape: 'box',
          size: [0.12, 0.02, 0.02],
          position: [0.50, 0.18, 0.40],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'faldon_privacidad',
          shape: 'box',
          size: [0.95, 0.42, 0.02],
          position: [-0.20, 0.46, -0.36],
          color: '#4a5568',
          texturePreset: 'metal_perforated',
          roughness: 0.6,
          metalness: 0.5
        },
        {
          name: 'pasacables_embutido',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.06, 6],
          position: [-0.45, 0.74, -0.28],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 02. SILLA ERGONÓMICA DE COMANDO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_chair_captain',
    family: 'sci_chair_captain',
    name: 'Silla Ergonómica de Comando',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Silla de mando con estrella de 5 radios rodante, pistón telescópico neumático, tapizado técnico y reposacabezas integrado.',
    tags: ['silla', 'asiento', 'oficina', 'ergonomica', 'comando', 'nave'],
    dimensions: { width: 0.68, height: 1.15, depth: 0.68 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_chair_captain.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_chair_captain',
      name: 'Silla Ergonómica de Comando',
      category: 'furniture',
      description: 'Silla de mando con estrella de 5 radios rodante, pistón telescópico neumático, tapizado técnico y reposacabezas integrado.',
      units: 'meters',
      dimensions: { width: 0.68, height: 1.15, depth: 0.68 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'estrella_cinco_radios',
          shape: 'cylinder',
          size: [0.32, 0.32, 0.05, 5],
          position: [0, 0.06, 0],
          color: '#a0aec0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'rueda_1',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.025, 6],
          position: [0.28, 0.03, 0],
          rotation: [0, 0, 90],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rueda_2',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.025, 6],
          position: [-0.28, 0.03, 0],
          rotation: [0, 0, 90],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rueda_3',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.025, 6],
          position: [0, 0.03, 0.28],
          rotation: [90, 0, 0],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rueda_4',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.025, 6],
          position: [0, 0.03, -0.28],
          rotation: [90, 0, 0],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'piston_telescopico',
          shape: 'cylinder',
          size: [0.032, 0.032, 0.35, 8],
          position: [0, 0.24, 0],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'asiento_ergonomico',
          shape: 'box',
          size: [0.52, 0.09, 0.50],
          position: [0, 0.44, 0.02],
          color: '#1a202c',
          texturePreset: 'leather_black_worn',
          roughness: 0.7,
          metalness: 0.1
        },
        {
          name: 'soporte_respaldo_lumbar',
          shape: 'box',
          size: [0.06, 0.35, 0.05],
          position: [0, 0.65, -0.22],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'respaldo_alto',
          shape: 'box',
          size: [0.48, 0.62, 0.08],
          position: [0, 0.80, -0.24],
          rotation: [-6, 0, 0],
          color: '#1a202c',
          texturePreset: 'leather_black_worn',
          roughness: 0.7,
          metalness: 0.1
        },
        {
          name: 'reposacabezas',
          shape: 'box',
          size: [0.32, 0.16, 0.07],
          position: [0, 1.08, -0.27],
          rotation: [-8, 0, 0],
          color: '#2d3748',
          texturePreset: 'synthetic_mesh',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'apoyabrazos_izq',
          shape: 'box',
          size: [0.07, 0.04, 0.32],
          position: [-0.29, 0.64, 0.04],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'apoyabrazos_der',
          shape: 'box',
          size: [0.07, 0.04, 0.32],
          position: [0.29, 0.64, 0.04],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'soporte_brazo_izq',
          shape: 'cylinder',
          size: [0.016, 0.016, 0.18, 6],
          position: [-0.29, 0.53, 0.04],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'soporte_brazo_der',
          shape: 'cylinder',
          size: [0.016, 0.016, 0.18, 6],
          position: [0.29, 0.53, 0.04],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 03. LITERA DE TRIPULACIÓN HERMÉTICA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_bunk_crew_pod',
    family: 'sci_bunk_crew_pod',
    name: 'Litera de Tripulación Hermética',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Litera de dos niveles para camarotes espaciales con estructura tubular, escalera estriada, taquilla baja y apliques de luz.',
    tags: ['litera', 'cama', 'tripulacion', 'descanso', 'camarote', 'espacio'],
    dimensions: { width: 1.05, height: 2.05, depth: 2.15 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_bunk_crew_pod.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_bunk_crew_pod',
      name: 'Litera de Tripulación Hermética',
      category: 'furniture',
      description: 'Litera de dos niveles para camarotes espaciales con estructura tubular, escalera estriada, taquilla baja y apliques de luz.',
      units: 'meters',
      dimensions: { width: 1.05, height: 2.05, depth: 2.15 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'columna_esquina_1',
          shape: 'box',
          size: [0.08, 2.05, 0.08],
          position: [-0.48, 1.025, -1.03],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'columna_esquina_2',
          shape: 'box',
          size: [0.08, 2.05, 0.08],
          position: [0.48, 1.025, -1.03],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'columna_esquina_3',
          shape: 'box',
          size: [0.08, 2.05, 0.08],
          position: [-0.48, 1.025, 1.03],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'columna_esquina_4',
          shape: 'box',
          size: [0.08, 2.05, 0.08],
          position: [0.48, 1.025, 1.03],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'bastidor_cama_inferior',
          shape: 'box',
          size: [1.00, 0.12, 2.10],
          position: [0, 0.45, 0],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.6,
          metalness: 0.5
        },
        {
          name: 'colchon_inferior',
          shape: 'box',
          size: [0.92, 0.15, 2.00],
          position: [0, 0.58, 0],
          color: '#dd6b20',
          texturePreset: 'quilted_padding_orange',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'manta_tripulante_inferior',
          shape: 'box',
          size: [0.94, 0.06, 1.40],
          position: [0, 0.64, 0.28],
          color: '#2b6cb0',
          texturePreset: 'canvas_military',
          roughness: 0.9,
          metalness: 0.0
        },
        {
          name: 'almohada_inferior',
          shape: 'box',
          size: [0.65, 0.08, 0.38],
          position: [0, 0.68, -0.75],
          color: '#edf2f7',
          texturePreset: 'quilted_padding_white',
          roughness: 0.7,
          metalness: 0.0
        },
        {
          name: 'bastidor_cama_superior',
          shape: 'box',
          size: [1.00, 0.12, 2.10],
          position: [0, 1.45, 0],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.6,
          metalness: 0.5
        },
        {
          name: 'colchon_superior',
          shape: 'box',
          size: [0.92, 0.15, 2.00],
          position: [0, 1.58, 0],
          color: '#dd6b20',
          texturePreset: 'quilted_padding_orange',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'manta_tripulante_superior',
          shape: 'box',
          size: [0.94, 0.06, 1.40],
          position: [0, 1.64, 0.28],
          color: '#2b6cb0',
          texturePreset: 'canvas_military',
          roughness: 0.9,
          metalness: 0.0
        },
        {
          name: 'almohada_superior',
          shape: 'box',
          size: [0.65, 0.08, 0.38],
          position: [0, 1.68, -0.75],
          color: '#edf2f7',
          texturePreset: 'quilted_padding_white',
          roughness: 0.7,
          metalness: 0.0
        },
        {
          name: 'escalera_montante_izq',
          shape: 'box',
          size: [0.03, 1.90, 0.04],
          position: [0.52, 0.95, -0.22],
          color: '#a0aec0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'escalera_montante_der',
          shape: 'box',
          size: [0.03, 1.90, 0.04],
          position: [0.52, 0.95, 0.22],
          color: '#a0aec0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'escalera_peldano_1',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.40, 6],
          position: [0.52, 0.35, 0],
          rotation: [90, 0, 0],
          color: '#cbd5e0',
          texturePreset: 'metal_light_brushed',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'escalera_peldano_2',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.40, 6],
          position: [0.52, 0.70, 0],
          rotation: [90, 0, 0],
          color: '#cbd5e0',
          texturePreset: 'metal_light_brushed',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'escalera_peldano_3',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.40, 6],
          position: [0.52, 1.05, 0],
          rotation: [90, 0, 0],
          color: '#cbd5e0',
          texturePreset: 'metal_light_brushed',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'escalera_peldano_4',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.40, 6],
          position: [0.52, 1.40, 0],
          rotation: [90, 0, 0],
          color: '#cbd5e0',
          texturePreset: 'metal_light_brushed',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'taquilla_baja_guardado',
          shape: 'box',
          size: [0.92, 0.32, 1.90],
          position: [0, 0.16, 0],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'luz_lectura_inferior',
          shape: 'box',
          size: [0.15, 0.04, 0.05],
          position: [-0.44, 0.85, -0.75],
          color: '#bee3f8',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#bee3f8',
          emissiveIntensity: 0.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 04. ARMARIO DOBLE DE TRIPULANTE
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_locker_double',
    family: 'sci_locker_double',
    name: 'Armario Doble de Tripulante',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Taquilla metálica de doble cuerpo para efectos personales con rejillas de aireación troqueladas y dial digital.',
    tags: ['armario', 'taquilla', 'locker', 'tripulante', 'almacenamiento', 'ropa'],
    dimensions: { width: 0.85, height: 1.95, depth: 0.55 },
    triBudget: '280-360',
    glbUrl: '/models/modular/sci_locker_double.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_locker_double',
      name: 'Armario Doble de Tripulante',
      category: 'furniture',
      description: 'Taquilla metálica de doble cuerpo para efectos personales con rejillas de aireación troqueladas y dial digital.',
      units: 'meters',
      dimensions: { width: 0.85, height: 1.95, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'gabinete_estructura',
          shape: 'box',
          size: [0.85, 1.82, 0.55],
          position: [0, 0.99, 0],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'zocalo_base_elevado',
          shape: 'box',
          size: [0.87, 0.08, 0.57],
          position: [0, 0.04, 0],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.2
        },
        {
          name: 'puerta_izquierda',
          shape: 'box',
          size: [0.39, 1.76, 0.03],
          position: [-0.21, 0.99, 0.28],
          color: '#4a5568',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'puerta_derecha',
          shape: 'box',
          size: [0.39, 1.76, 0.03],
          position: [0.21, 0.99, 0.28],
          color: '#4a5568',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'rejilla_louver_izq_sup',
          shape: 'box',
          size: [0.28, 0.12, 0.005],
          position: [-0.21, 1.70, 0.30],
          color: '#1a202c',
          texturePreset: 'server_vent_panel',
          roughness: 0.6,
          metalness: 0.4
        },
        {
          name: 'rejilla_louver_izq_inf',
          shape: 'box',
          size: [0.28, 0.12, 0.005],
          position: [-0.21, 0.28, 0.30],
          color: '#1a202c',
          texturePreset: 'server_vent_panel',
          roughness: 0.6,
          metalness: 0.4
        },
        {
          name: 'rejilla_louver_der_sup',
          shape: 'box',
          size: [0.28, 0.12, 0.005],
          position: [0.21, 1.70, 0.30],
          color: '#1a202c',
          texturePreset: 'server_vent_panel',
          roughness: 0.6,
          metalness: 0.4
        },
        {
          name: 'rejilla_louver_der_inf',
          shape: 'box',
          size: [0.28, 0.12, 0.005],
          position: [0.21, 0.28, 0.30],
          color: '#1a202c',
          texturePreset: 'server_vent_panel',
          roughness: 0.6,
          metalness: 0.4
        },
        {
          name: 'tirador_embutido_izq',
          shape: 'box',
          size: [0.03, 0.16, 0.015],
          position: [-0.04, 1.05, 0.30],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.9
        },
        {
          name: 'tirador_embutido_der',
          shape: 'box',
          size: [0.03, 0.16, 0.015],
          position: [0.04, 1.05, 0.30],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.9
        },
        {
          name: 'dial_seguridad_izq',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.015, 8],
          position: [-0.04, 1.25, 0.30],
          rotation: [90, 0, 0],
          color: '#ecc94b',
          texturePreset: 'brass_burnished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'dial_seguridad_der',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.015, 8],
          position: [0.04, 1.25, 0.30],
          rotation: [90, 0, 0],
          color: '#ecc94b',
          texturePreset: 'brass_burnished',
          roughness: 0.3,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 05. BANCO DE TRABAJO INDUSTRIAL PESADO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_workbench_heavy',
    family: 'sci_workbench_heavy',
    name: 'Banco de Trabajo Técnico',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Mesa de taller con estructura reforzada en H, encimera de caucho industrial, panel perforado de herramientas y bandeja inferior.',
    tags: ['banco', 'taller', 'herramientas', 'trabajo', 'mantenimiento', 'mecanica'],
    dimensions: { width: 1.60, height: 1.65, depth: 0.80 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_workbench_heavy.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_workbench_heavy',
      name: 'Banco de Trabajo Técnico',
      category: 'furniture',
      description: 'Mesa de taller con estructura reforzada en H, encimera de caucho industrial, panel perforado de herramientas y bandeja inferior.',
      units: 'meters',
      dimensions: { width: 1.60, height: 1.65, depth: 0.80 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'tablero_trabajo_pesado',
          shape: 'box',
          size: [1.60, 0.06, 0.80],
          position: [0, 0.85, 0],
          color: '#1a202c',
          texturePreset: 'rubber_ribbed_mat',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'reborde_acero_tablero',
          shape: 'box',
          size: [1.62, 0.02, 0.82],
          position: [0, 0.81, 0],
          color: '#718096',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pata_tubular_1',
          shape: 'box',
          size: [0.08, 0.82, 0.08],
          position: [-0.72, 0.41, 0.32],
          color: '#2d3748',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'pata_tubular_2',
          shape: 'box',
          size: [0.08, 0.82, 0.08],
          position: [0.72, 0.41, 0.32],
          color: '#2d3748',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'pata_tubular_3',
          shape: 'box',
          size: [0.08, 0.82, 0.08],
          position: [-0.72, 0.41, -0.32],
          color: '#2d3748',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'pata_tubular_4',
          shape: 'box',
          size: [0.08, 0.82, 0.08],
          position: [0.72, 0.41, -0.32],
          color: '#2d3748',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'balda_inferior_carga',
          shape: 'box',
          size: [1.44, 0.03, 0.64],
          position: [0, 0.22, 0],
          color: '#4a5568',
          texturePreset: 'diamond_plate',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'panel_posterior_herramientas',
          shape: 'box',
          size: [1.60, 0.72, 0.03],
          position: [0, 1.24, -0.38],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.6,
          metalness: 0.3
        },
        {
          name: 'repisa_superior_herramientas',
          shape: 'box',
          size: [1.60, 0.03, 0.20],
          position: [0, 1.62, -0.28],
          color: '#2d3748',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.7
        },
        {
          name: 'luminaria_lineal_taller',
          shape: 'box',
          size: [1.40, 0.03, 0.06],
          position: [0, 1.58, -0.26],
          color: '#f7fafc',
          texturePreset: 'painted_metal_white',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#edf2f7',
          emissiveIntensity: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 06. ESTANTERÍA DE CARGA PESADA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_storage_shelf',
    family: 'sci_storage_shelf',
    name: 'Estantería de Carga Pesada',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Módulo de almacenamiento industrial con 4 montantes ranurados, 4 baldas reforzadas y tirantes diagonales de estabilización.',
    tags: ['estanteria', 'almacen', 'carga', 'baldas', 'estante', 'deposito'],
    dimensions: { width: 1.30, height: 2.10, depth: 0.60 },
    triBudget: '300-380',
    glbUrl: '/models/modular/sci_storage_shelf.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_storage_shelf',
      name: 'Estantería de Carga Pesada',
      category: 'furniture',
      description: 'Módulo de almacenamiento industrial con 4 montantes ranurados, 4 baldas reforzadas y tirantes diagonales de estabilización.',
      units: 'meters',
      dimensions: { width: 1.30, height: 2.10, depth: 0.60 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'montante_ant_izq',
          shape: 'box',
          size: [0.06, 2.10, 0.06],
          position: [-0.62, 1.05, 0.27],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'montante_ant_der',
          shape: 'box',
          size: [0.06, 2.10, 0.06],
          position: [0.62, 1.05, 0.27],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'montante_post_izq',
          shape: 'box',
          size: [0.06, 2.10, 0.06],
          position: [-0.62, 1.05, -0.27],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'montante_post_der',
          shape: 'box',
          size: [0.06, 2.10, 0.06],
          position: [0.62, 1.05, -0.27],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'balda_nivel_1_suelo',
          shape: 'box',
          size: [1.28, 0.04, 0.58],
          position: [0, 0.16, 0],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'balda_nivel_2',
          shape: 'box',
          size: [1.28, 0.04, 0.58],
          position: [0, 0.75, 0],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'balda_nivel_3',
          shape: 'box',
          size: [1.28, 0.04, 0.58],
          position: [0, 1.35, 0],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'balda_nivel_4_techo',
          shape: 'box',
          size: [1.28, 0.04, 0.58],
          position: [0, 1.95, 0],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'tirante_cruzado_post_1',
          shape: 'box',
          size: [1.40, 0.02, 0.01],
          position: [0, 1.05, -0.29],
          rotation: [0, 0, 32],
          color: '#718096',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'tirante_cruzado_post_2',
          shape: 'box',
          size: [1.40, 0.02, 0.01],
          position: [0, 1.05, -0.29],
          rotation: [0, 0, -32],
          color: '#718096',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 07. MESA DE OPERACIONES TÁCTICA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_briefing_table',
    family: 'sci_briefing_table',
    name: 'Mesa de Operaciones Táctica',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Mesa de deliberación con pedestal central doble, tablero biselado facetado y proyector holográfico circular embutido.',
    tags: ['mesa', 'tactica', 'briefing', 'holograma', 'operaciones', 'reunion'],
    dimensions: { width: 2.20, height: 0.78, depth: 1.20 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_briefing_table.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_briefing_table',
      name: 'Mesa de Operaciones Táctica',
      category: 'furniture',
      description: 'Mesa de deliberación con pedestal central doble, tablero biselado facetado y proyector holográfico circular embutido.',
      units: 'meters',
      dimensions: { width: 2.20, height: 0.78, depth: 1.20 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'tablero_facetado',
          shape: 'box',
          size: [2.20, 0.08, 1.20],
          position: [0, 0.74, 0],
          color: '#1a202c',
          texturePreset: 'scifi_hull_plates',
          roughness: 0.5,
          metalness: 0.6
        },
        {
          name: 'bisel_perimetral_aluminio',
          shape: 'box',
          size: [2.24, 0.03, 1.24],
          position: [0, 0.70, 0],
          color: '#a0aec0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'pedestal_central_izq',
          shape: 'cylinder',
          size: [0.18, 0.24, 0.68, 6],
          position: [-0.60, 0.34, 0],
          color: '#2d3748',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'pedestal_central_der',
          shape: 'cylinder',
          size: [0.18, 0.24, 0.68, 6],
          position: [0.60, 0.34, 0],
          color: '#2d3748',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'base_suelo_izq',
          shape: 'cylinder',
          size: [0.36, 0.36, 0.05, 6],
          position: [-0.60, 0.025, 0],
          color: '#171923',
          texturePreset: 'rubber_black',
          roughness: 0.7,
          metalness: 0.3
        },
        {
          name: 'base_suelo_der',
          shape: 'cylinder',
          size: [0.36, 0.36, 0.05, 6],
          position: [0.60, 0.025, 0],
          color: '#171923',
          texturePreset: 'rubber_black',
          roughness: 0.7,
          metalness: 0.3
        },
        {
          name: 'proyector_holografico_central',
          shape: 'cylinder',
          size: [0.35, 0.35, 0.02, 12],
          position: [0, 0.782, 0],
          color: '#319795',
          texturePreset: 'hologram_cyan',
          roughness: 0.1,
          metalness: 0.2,
          emissive: '#4fd1c5',
          emissiveIntensity: 0.95
        },
        {
          name: 'anillo_emisor_holo',
          shape: 'cylinder',
          size: [0.42, 0.42, 0.01, 12],
          position: [0, 0.781, 0],
          color: '#cbd5e0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'pantalla_tactil_lateral_1',
          shape: 'box',
          size: [0.45, 0.01, 0.24],
          position: [-0.65, 0.782, 0.38],
          color: '#22543d',
          texturePreset: 'crt_screen_green',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 0.6
        },
        {
          name: 'pantalla_tactil_lateral_2',
          shape: 'box',
          size: [0.45, 0.01, 0.24],
          position: [0.65, 0.782, -0.38],
          color: '#22543d',
          texturePreset: 'crt_screen_green',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 0.6
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 08. CONJUNTO DE COMEDOR Y BANCOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_canteen_bench',
    family: 'sci_canteen_bench',
    name: 'Conjunto de Mesa y Bancos de Comedor',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Conjunto modular unificado para comedores espaciales con mesa central y 2 bancos de comensales integrados en bastidor monocasco.',
    tags: ['comedor', 'mesa', 'banco', 'cantina', 'almuerzo', 'nave'],
    dimensions: { width: 1.60, height: 0.75, depth: 1.40 },
    triBudget: '280-360',
    glbUrl: '/models/modular/sci_canteen_bench.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_canteen_bench',
      name: 'Conjunto de Mesa y Bancos de Comedor',
      category: 'furniture',
      description: 'Conjunto modular unificado para comedores espaciales con mesa central y 2 bancos de comensales integrados en bastidor monocasco.',
      units: 'meters',
      dimensions: { width: 1.60, height: 0.75, depth: 1.40 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'tablero_mesa_comedor',
          shape: 'box',
          size: [1.60, 0.05, 0.65],
          position: [0, 0.725, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.3,
          metalness: 0.2
        },
        {
          name: 'banco_asiento_frontal',
          shape: 'box',
          size: [1.50, 0.04, 0.30],
          position: [0, 0.44, 0.50],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.6,
          metalness: 0.4
        },
        {
          name: 'banco_asiento_trasero',
          shape: 'box',
          size: [1.50, 0.04, 0.30],
          position: [0, 0.44, -0.50],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.6,
          metalness: 0.4
        },
        {
          name: 'puente_bastidor_izq',
          shape: 'box',
          size: [0.08, 0.06, 1.20],
          position: [-0.60, 0.03, 0],
          color: '#4a5568',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'puente_bastidor_der',
          shape: 'box',
          size: [0.08, 0.06, 1.20],
          position: [0.60, 0.03, 0],
          color: '#4a5568',
          texturePreset: 'steel_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'pilar_mesa_izq',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.66, 6],
          position: [-0.60, 0.37, 0],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'pilar_mesa_der',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.66, 6],
          position: [0.60, 0.37, 0],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'pilar_banco_ant_izq',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.38, 6],
          position: [-0.60, 0.23, 0.50],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'pilar_banco_ant_der',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.38, 6],
          position: [0.60, 0.23, 0.50],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'pilar_banco_post_izq',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.38, 6],
          position: [-0.60, 0.23, -0.50],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        },
        {
          name: 'pilar_banco_post_der',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.38, 6],
          position: [0.60, 0.23, -0.50],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 09. BANQUETA NEUMÁTICA DE TALLER
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_stool_workshop',
    family: 'sci_stool_workshop',
    name: 'Banqueta Neumática de Taller',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Taburete técnico giratorio con base de fundición pesada, pistón regulable, reposapiés perimetral y asiento de poliuretano estriado.',
    tags: ['banqueta', 'taburete', 'taller', 'asiento', 'giratorio', 'mecanico'],
    dimensions: { width: 0.48, height: 0.68, depth: 0.48 },
    triBudget: '240-300',
    glbUrl: '/models/modular/sci_stool_workshop.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_stool_workshop',
      name: 'Banqueta Neumática de Taller',
      category: 'furniture',
      description: 'Taburete técnico giratorio con base de fundición pesada, pistón regulable, reposapiés perimetral y asiento de poliuretano estriado.',
      units: 'meters',
      dimensions: { width: 0.48, height: 0.68, depth: 0.48 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_pesada_fundicion',
          shape: 'cylinder',
          size: [0.24, 0.24, 0.05, 8],
          position: [0, 0.025, 0],
          color: '#1a202c',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'aro_reposapies',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.02, 8],
          position: [0, 0.18, 0],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'radio_reposapies_1',
          shape: 'box',
          size: [0.36, 0.015, 0.02],
          position: [0, 0.18, 0],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'radio_reposapies_2',
          shape: 'box',
          size: [0.02, 0.015, 0.36],
          position: [0, 0.18, 0],
          color: '#4a5568',
          texturePreset: 'steel_polished',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'cilindro_piston',
          shape: 'cylinder',
          size: [0.035, 0.035, 0.55, 8],
          position: [0, 0.32, 0],
          color: '#cbd5e0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'asiento_circular_poliuretano',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.07, 10],
          position: [0, 0.63, 0],
          color: '#1a202c',
          texturePreset: 'rubber_ribbed_mat',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'palanca_ajuste_altura',
          shape: 'box',
          size: [0.14, 0.015, 0.02],
          position: [0.12, 0.58, 0],
          rotation: [0, 0, -10],
          color: '#e53e3e',
          texturePreset: 'painted_metal_red',
          roughness: 0.4,
          metalness: 0.4
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 10. ARMARIO MURAL SUSPENDIDO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_wall_cabinet',
    family: 'sci_wall_cabinet',
    name: 'Armario Mural Suspendido',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Armario de pared estanco para herramientas y suministros con puerta abatible de pistón y visor de policarbonato ahumado.',
    tags: ['armario', 'mural', 'pared', 'suspendido', 'botiquin', 'suministros'],
    dimensions: { width: 0.90, height: 0.55, depth: 0.35 },
    triBudget: '220-280',
    glbUrl: '/models/modular/sci_wall_cabinet.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_wall_cabinet',
      name: 'Armario Mural Suspendido',
      category: 'furniture',
      description: 'Armario de pared estanco para herramientas y suministros con puerta abatible de pistón y visor de policarbonato ahumado.',
      units: 'meters',
      dimensions: { width: 0.90, height: 0.55, depth: 0.35 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_gabinete_mural',
          shape: 'box',
          size: [0.90, 0.55, 0.35],
          position: [0, 0.275, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'placa_anclaje_trasera',
          shape: 'box',
          size: [0.94, 0.59, 0.015],
          position: [0, 0.275, -0.18],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'puerta_basculante',
          shape: 'box',
          size: [0.84, 0.48, 0.025],
          position: [0, 0.275, 0.18],
          color: '#a0aec0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'ventana_visor_policarbonato',
          shape: 'box',
          size: [0.60, 0.22, 0.01],
          position: [0, 0.275, 0.195],
          color: '#2d3748',
          texturePreset: 'tinted_glass',
          roughness: 0.1,
          metalness: 0.2,
          transparent: true,
          opacity: 0.45
        },
        {
          name: 'tirador_inferior_aluminio',
          shape: 'box',
          size: [0.30, 0.025, 0.03],
          position: [0, 0.08, 0.20],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'led_indicador_bloqueo',
          shape: 'box',
          size: [0.04, 0.02, 0.01],
          position: [0.35, 0.46, 0.195],
          color: '#38a169',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#38a169',
          emissiveIntensity: 0.85
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 11. MÓDULO ARCHIVADOR APILABLE
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_filing_pod',
    family: 'sci_filing_pod',
    name: 'Módulo Archivador de Datos',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Archivador apilable de tres cajones para unidades de cristal óptico y documentos físicos con cantoneras reforzadas.',
    tags: ['archivador', 'cajonera', 'datos', 'ficheros', 'documentos', 'almacen'],
    dimensions: { width: 0.50, height: 1.05, depth: 0.65 },
    triBudget: '260-320',
    glbUrl: '/models/modular/sci_filing_pod.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_filing_pod',
      name: 'Módulo Archivador de Datos',
      category: 'furniture',
      description: 'Archivador apilable de tres cajones para unidades de cristal óptico y documentos físicos con cantoneras reforzadas.',
      units: 'meters',
      dimensions: { width: 0.50, height: 1.05, depth: 0.65 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_archivador',
          shape: 'box',
          size: [0.50, 1.05, 0.65],
          position: [0, 0.525, 0],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.5,
          metalness: 0.6
        },
        {
          name: 'cajon_1_superior',
          shape: 'box',
          size: [0.44, 0.28, 0.02],
          position: [0, 0.86, 0.33],
          color: '#4a5568',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'cajon_2_medio',
          shape: 'box',
          size: [0.44, 0.28, 0.02],
          position: [0, 0.53, 0.33],
          color: '#4a5568',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'cajon_3_inferior',
          shape: 'box',
          size: [0.44, 0.28, 0.02],
          position: [0, 0.20, 0.33],
          color: '#4a5568',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.4
        },
        {
          name: 'tirador_barra_1',
          shape: 'box',
          size: [0.22, 0.025, 0.025],
          position: [0, 0.86, 0.35],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'tirador_barra_2',
          shape: 'box',
          size: [0.22, 0.025, 0.025],
          position: [0, 0.53, 0.35],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'tirador_barra_3',
          shape: 'box',
          size: [0.22, 0.025, 0.025],
          position: [0, 0.20, 0.35],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'visor_etiqueta_led_1',
          shape: 'box',
          size: [0.12, 0.03, 0.005],
          position: [0, 0.94, 0.345],
          color: '#48bb78',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 0.7
        },
        {
          name: 'visor_etiqueta_led_2',
          shape: 'box',
          size: [0.12, 0.03, 0.005],
          position: [0, 0.61, 0.345],
          color: '#48bb78',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 0.7
        },
        {
          name: 'visor_etiqueta_led_3',
          shape: 'box',
          size: [0.12, 0.03, 0.005],
          position: [0, 0.28, 0.345],
          color: '#48bb78',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#48bb78',
          emissiveIntensity: 0.7
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 12. ESTACIÓN DE LABORATORIO CON FREGADERO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_lab_bench_sink',
    family: 'sci_lab_bench_sink',
    name: 'Estación de Laboratorio con Fregadero',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Mueble de laboratorio químico con encimera de resina resistente a ácidos, fregadero de acero inoxidable y grifo de cuello de cisne.',
    tags: ['laboratorio', 'fregadero', 'quimica', 'pila', 'grifo', 'limpieza'],
    dimensions: { width: 1.40, height: 1.10, depth: 0.75 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_lab_bench_sink.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_lab_bench_sink',
      name: 'Estación de Laboratorio con Fregadero',
      category: 'furniture',
      description: 'Mueble de laboratorio químico con encimera de resina resistente a ácidos, fregadero de acero inoxidable y grifo de cuello de cisne.',
      units: 'meters',
      dimensions: { width: 1.40, height: 1.10, depth: 0.75 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'mueble_inferior_estanco',
          shape: 'box',
          size: [1.40, 0.80, 0.75],
          position: [0, 0.40, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'encimera_resina_epoxi',
          shape: 'box',
          size: [1.44, 0.05, 0.79],
          position: [0, 0.825, 0],
          color: '#1a202c',
          texturePreset: 'ceramic_tiles',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'cuenca_fregadero_acero',
          shape: 'box',
          size: [0.50, 0.02, 0.40],
          position: [0.35, 0.84, 0],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'grifo_columna_vertical',
          shape: 'cylinder',
          size: [0.018, 0.018, 0.22, 6],
          position: [0.35, 0.96, -0.22],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'grifo_cuello_cisne_arco',
          shape: 'box',
          size: [0.018, 0.02, 0.14],
          position: [0.35, 1.07, -0.15],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'valvula_mando_agua',
          shape: 'cylinder',
          size: [0.025, 0.025, 0.04, 6],
          position: [0.26, 0.89, -0.22],
          rotation: [90, 0, 0],
          color: '#3182ce',
          texturePreset: 'painted_metal_blue',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'puerta_armario_izq',
          shape: 'box',
          size: [0.42, 0.70, 0.02],
          position: [-0.44, 0.40, 0.38],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.6
        },
        {
          name: 'puerta_armario_der',
          shape: 'box',
          size: [0.42, 0.70, 0.02],
          position: [0.02, 0.40, 0.38],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.6
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 13. CÁPSULA DE DESCANSO INDIVIDUAL
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_sleeping_capsule',
    family: 'sci_sleeping_capsule',
    name: 'Cápsula de Descanso Individual',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Vaina horizontal presurizada de hibernación y sueño profundo con compuerta corredera y panel de monitorización biofísica.',
    tags: ['capsula', 'sueño', 'descanso', 'hibernacion', 'camarote', 'espacio'],
    dimensions: { width: 1.15, height: 1.25, depth: 2.25 },
    triBudget: '440-540',
    glbUrl: '/models/modular/sci_sleeping_capsule.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_sleeping_capsule',
      name: 'Cápsula de Descanso Individual',
      category: 'furniture',
      description: 'Vaina horizontal presurizada de hibernación y sueño profundo con compuerta corredera y panel de monitorización biofísica.',
      units: 'meters',
      dimensions: { width: 1.15, height: 1.25, depth: 2.25 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuna_soporte_suelo',
          shape: 'box',
          size: [1.15, 0.15, 2.20],
          position: [0, 0.075, 0],
          color: '#1a202c',
          texturePreset: 'metal_dark_grime',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'casco_cilindro_vaina',
          shape: 'cylinder',
          size: [0.55, 0.55, 2.20, 10],
          position: [0, 0.68, 0],
          rotation: [90, 0, 0],
          color: '#edf2f7',
          texturePreset: 'painted_metal_white',
          roughness: 0.3,
          metalness: 0.3
        },
        {
          name: 'escotilla_corredera',
          shape: 'box',
          size: [0.85, 0.70, 1.40],
          position: [0, 0.78, 0.10],
          color: '#2b6cb0',
          texturePreset: 'scifi_hull_plates',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'visor_cristal_escotilla',
          shape: 'box',
          size: [0.60, 0.25, 0.80],
          position: [0, 1.05, 0.10],
          color: '#bee3f8',
          texturePreset: 'tinted_glass',
          roughness: 0.1,
          metalness: 0.2,
          transparent: true,
          opacity: 0.40
        },
        {
          name: 'panel_control_ambiental',
          shape: 'box',
          size: [0.18, 0.24, 0.05],
          position: [0.56, 0.75, -0.70],
          color: '#2d3748',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.2,
          emissive: '#48bb78',
          emissiveIntensity: 0.75
        },
        {
          name: 'colchon_interior_visco',
          shape: 'box',
          size: [0.75, 0.10, 1.95],
          position: [0, 0.26, 0],
          color: '#dd6b20',
          texturePreset: 'quilted_padding_orange',
          roughness: 0.8,
          metalness: 0.0
        },
        {
          name: 'anillo_presurizacion_frontal',
          shape: 'cylinder',
          size: [0.57, 0.57, 0.06, 10],
          position: [0, 0.68, 1.10],
          rotation: [90, 0, 0],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.5,
          metalness: 0.4
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 14. DISPENSADOR AUTOMÁTICO DE RACIONES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_mess_dispenser',
    family: 'sci_mess_dispenser',
    name: 'Dispensador de Raciones y Nutrientes',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Torre dispensadora automática con bandeja de descarga protegida, panel numérico táctil y display CRT ámbar.',
    tags: ['dispensador', 'comida', 'raciones', 'automat', 'cantina', 'nutricion'],
    dimensions: { width: 0.70, height: 1.85, depth: 0.60 },
    triBudget: '300-380',
    glbUrl: '/models/modular/sci_mess_dispenser.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_mess_dispenser',
      name: 'Dispensador de Raciones y Nutrientes',
      category: 'furniture',
      description: 'Torre dispensadora automática con bandeja de descarga protegida, panel numérico táctil y display CRT ámbar.',
      units: 'meters',
      dimensions: { width: 0.70, height: 1.85, depth: 0.60 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'torre_carcasa_principal',
          shape: 'box',
          size: [0.70, 1.85, 0.60],
          position: [0, 0.925, 0],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.6,
          metalness: 0.5
        },
        {
          name: 'boca_descarga_alimentos',
          shape: 'box',
          size: [0.52, 0.32, 0.25],
          position: [0, 0.52, 0.20],
          color: '#1a202c',
          texturePreset: 'steel_galvanized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'compuerta_basculante_boca',
          shape: 'box',
          size: [0.48, 0.28, 0.02],
          position: [0, 0.52, 0.31],
          rotation: [-15, 0, 0],
          color: '#718096',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'pantalla_crt_ambar',
          shape: 'box',
          size: [0.38, 0.22, 0.02],
          position: [0, 1.25, 0.31],
          color: '#dd6b20',
          texturePreset: 'crt_screen_amber',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#dd6b20',
          emissiveIntensity: 0.85
        },
        {
          name: 'teclado_seleccion_matricial',
          shape: 'box',
          size: [0.28, 0.18, 0.02],
          position: [0, 0.98, 0.31],
          color: '#a0aec0',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.6,
          metalness: 0.2
        },
        {
          name: 'ranura_tarjeta_identificacion',
          shape: 'box',
          size: [0.12, 0.015, 0.03],
          position: [0.22, 0.98, 0.31],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rotulo_dispensador_raciones',
          shape: 'box',
          size: [0.55, 0.12, 0.01],
          position: [0, 1.62, 0.31],
          color: '#ecc94b',
          texturePreset: 'caution_label',
          roughness: 0.4,
          metalness: 0.3
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 15. CARRO MÓVIL DE HERRAMIENTAS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_tool_cart_mobile',
    family: 'sci_tool_cart_mobile',
    name: 'Carro Móvil de Herramientas',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Carro de taller sobre 4 ruedas de goma reforzada con 4 cajones deslizantes, bandeja superior con reborde y asa de empuje.',
    tags: ['carro', 'herramientas', 'taller', 'mecanica', 'ruedas', 'mantenimiento'],
    dimensions: { width: 0.75, height: 0.95, depth: 0.52 },
    triBudget: '300-380',
    glbUrl: '/models/modular/sci_tool_cart_mobile.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_tool_cart_mobile',
      name: 'Carro Móvil de Herramientas',
      category: 'furniture',
      description: 'Carro de taller sobre 4 ruedas de goma reforzada con 4 cajones deslizantes, bandeja superior con reborde y asa de empuje.',
      units: 'meters',
      dimensions: { width: 0.75, height: 0.95, depth: 0.52 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'cuerpo_carro_rojo',
          shape: 'box',
          size: [0.65, 0.75, 0.48],
          position: [0, 0.48, 0],
          color: '#e53e3e',
          texturePreset: 'red_paint_worn',
          roughness: 0.4,
          metalness: 0.4
        },
        {
          name: 'bandeja_superior_goma',
          shape: 'box',
          size: [0.67, 0.03, 0.50],
          position: [0, 0.87, 0],
          color: '#1a202c',
          texturePreset: 'rubber_ribbed_mat',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'asa_tubular_empuje',
          shape: 'cylinder',
          size: [0.016, 0.016, 0.38, 6],
          position: [-0.38, 0.85, 0],
          rotation: [90, 0, 0],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'soporte_asa_izq',
          shape: 'box',
          size: [0.08, 0.02, 0.02],
          position: [-0.34, 0.85, 0.18],
          color: '#718096',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'soporte_asa_der',
          shape: 'box',
          size: [0.08, 0.02, 0.02],
          position: [-0.34, 0.85, -0.18],
          color: '#718096',
          texturePreset: 'steel_polished',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'cajon_1',
          shape: 'box',
          size: [0.58, 0.14, 0.02],
          position: [0, 0.74, 0.25],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.5
        },
        {
          name: 'cajon_2',
          shape: 'box',
          size: [0.58, 0.14, 0.02],
          position: [0, 0.57, 0.25],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.5
        },
        {
          name: 'cajon_3',
          shape: 'box',
          size: [0.58, 0.14, 0.02],
          position: [0, 0.40, 0.25],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.5
        },
        {
          name: 'cajon_4',
          shape: 'box',
          size: [0.58, 0.18, 0.02],
          position: [0, 0.21, 0.25],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.5,
          metalness: 0.5
        },
        {
          name: 'rueda_ant_izq',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.03, 6],
          position: [-0.25, 0.05, 0.18],
          rotation: [0, 0, 90],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rueda_ant_der',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.03, 6],
          position: [0.25, 0.05, 0.18],
          rotation: [0, 0, 90],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rueda_post_izq',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.03, 6],
          position: [-0.25, 0.05, -0.18],
          rotation: [0, 0, 90],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'rueda_post_der',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.03, 6],
          position: [0.25, 0.05, -0.18],
          rotation: [0, 0, 90],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 16. PANEL DIVISORIO MODULAR
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_partition_screen',
    family: 'sci_partition_screen',
    name: 'Panel Divisorio Modular',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Mampara divisoria autoportante con perfilería de aluminio extruido, pies de acero y panel fonoabsorbente con patrón hexagonal.',
    tags: ['panel', 'mampara', 'separador', 'oficina', 'divisor', 'privacidad'],
    dimensions: { width: 1.20, height: 1.85, depth: 0.40 },
    triBudget: '220-280',
    glbUrl: '/models/modular/sci_partition_screen.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_partition_screen',
      name: 'Panel Divisorio Modular',
      category: 'furniture',
      description: 'Mampara divisoria autoportante con perfilería de aluminio extruido, pies de acero y panel fonoabsorbente con patrón hexagonal.',
      units: 'meters',
      dimensions: { width: 1.20, height: 1.85, depth: 0.40 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'marco_perimetral_aluminio',
          shape: 'box',
          size: [1.20, 1.80, 0.05],
          position: [0, 0.95, 0],
          color: '#cbd5e0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        },
        {
          name: 'panel_central_acustico',
          shape: 'box',
          size: [1.12, 1.72, 0.03],
          position: [0, 0.95, 0],
          color: '#2d3748',
          texturePreset: 'hex_composite',
          roughness: 0.7,
          metalness: 0.3
        },
        {
          name: 'pie_soporte_izq',
          shape: 'box',
          size: [0.08, 0.04, 0.40],
          position: [-0.48, 0.02, 0],
          color: '#1a202c',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'pie_soporte_der',
          shape: 'box',
          size: [0.08, 0.04, 0.40],
          position: [0.48, 0.02, 0],
          color: '#1a202c',
          texturePreset: 'iron_cast',
          roughness: 0.6,
          metalness: 0.7
        },
        {
          name: 'franja_vidrio_superior',
          shape: 'box',
          size: [1.06, 0.22, 0.01],
          position: [0, 1.62, 0],
          color: '#bee3f8',
          texturePreset: 'tinted_glass',
          roughness: 0.1,
          metalness: 0.2,
          transparent: true,
          opacity: 0.45
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 17. ARMERO MURAL TÁCTICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_gun_rack_wall',
    family: 'sci_gun_rack_wall',
    name: 'Armero Táctico Mural',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Soporte mural de almacenamiento vertical para 4 fusiles o herramientas con cunas de goma y barra transversal de seguridad.',
    tags: ['armero', 'armas', 'seguridad', 'mural', 'soporte', 'fusiles'],
    dimensions: { width: 1.10, height: 1.30, depth: 0.28 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_gun_rack_wall.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_gun_rack_wall',
      name: 'Armero Táctico Mural',
      category: 'furniture',
      description: 'Soporte mural de almacenamiento vertical para 4 fusiles o herramientas con cunas de goma y barra transversal de seguridad.',
      units: 'meters',
      dimensions: { width: 1.10, height: 1.30, depth: 0.28 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'placa_dorsal_mural',
          shape: 'box',
          size: [1.10, 1.30, 0.03],
          position: [0, 0.65, -0.12],
          color: '#2d3748',
          texturePreset: 'metal_dark_grime',
          roughness: 0.7,
          metalness: 0.6
        },
        {
          name: 'repisa_inferior_culatas',
          shape: 'box',
          size: [1.04, 0.06, 0.24],
          position: [0, 0.09, 0],
          color: '#1a202c',
          texturePreset: 'rubber_ribbed_mat',
          roughness: 0.8,
          metalness: 0.2
        },
        {
          name: 'guia_superior_canones',
          shape: 'box',
          size: [1.04, 0.05, 0.16],
          position: [0, 1.05, -0.04],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'cuna_arma_1',
          shape: 'box',
          size: [0.04, 0.08, 0.12],
          position: [-0.36, 1.05, 0.04],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cuna_arma_2',
          shape: 'box',
          size: [0.04, 0.08, 0.12],
          position: [-0.12, 1.05, 0.04],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cuna_arma_3',
          shape: 'box',
          size: [0.04, 0.08, 0.12],
          position: [0.12, 1.05, 0.04],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cuna_arma_4',
          shape: 'box',
          size: [0.04, 0.08, 0.12],
          position: [0.36, 1.05, 0.04],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'barra_seguridad_bloqueo',
          shape: 'cylinder',
          size: [0.015, 0.015, 1.06, 6],
          position: [0, 0.65, 0.08],
          rotation: [0, 0, 90],
          color: '#ecc94b',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'candado_digital_magnetico',
          shape: 'box',
          size: [0.08, 0.12, 0.05],
          position: [0.48, 0.65, 0.08],
          color: '#1a202c',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.5,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 18. MESA DE PROCEDIMIENTOS QUIRÚRGICOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cremate_table',
    family: 'sci_cremate_table',
    name: 'Mesa de Procedimientos Quirúrgicos',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Mesa clínica motorizada de acero inoxidable pulido con columna hidráulica central, canaleta de drenaje y apoyacabezas articulado.',
    tags: ['mesa', 'quirurgica', 'autopsia', 'medico', 'clinica', 'hidraulico'],
    dimensions: { width: 0.85, height: 0.90, depth: 2.10 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_cremate_table.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cremate_table',
      name: 'Mesa de Procedimientos Quirúrgicos',
      category: 'furniture',
      description: 'Mesa clínica motorizada de acero inoxidable pulido con columna hidráulica central, canaleta de drenaje y apoyacabezas articulado.',
      units: 'meters',
      dimensions: { width: 0.85, height: 0.90, depth: 2.10 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_suelo_pesada',
          shape: 'box',
          size: [0.70, 0.08, 1.10],
          position: [0, 0.04, 0],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'columna_hidraulica_telescopica',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.65, 8],
          position: [0, 0.40, 0],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'bandeja_quirurgica_acero',
          shape: 'box',
          size: [0.85, 0.06, 2.05],
          position: [0, 0.75, 0],
          color: '#edf2f7',
          texturePreset: 'steel_polished',
          roughness: 0.15,
          metalness: 0.95
        },
        {
          name: 'reborde_drenaje_perimetral',
          shape: 'box',
          size: [0.87, 0.02, 2.07],
          position: [0, 0.78, 0],
          color: '#cbd5e0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'apoyacabezas_articulado',
          shape: 'box',
          size: [0.35, 0.05, 0.28],
          position: [0, 0.80, -0.85],
          rotation: [10, 0, 0],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'riel_accesorios_izq',
          shape: 'box',
          size: [0.02, 0.03, 1.80],
          position: [-0.44, 0.74, 0],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'riel_accesorios_der',
          shape: 'box',
          size: [0.02, 0.03, 1.80],
          position: [0.44, 0.74, 0],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 19. ESTACIÓN DE TRIAJE DE RESIDUOS 3 BOCAS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_waste_sorter',
    family: 'sci_waste_sorter',
    name: 'Estación de Triaje de Residuos 3 Bocas',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Estación de clasificación y reciclaje hermético con 3 tolvas basculantes codificadas por color (orgánico, metales, biológico).',
    tags: ['residuos', 'reciclaje', 'basura', 'triaje', 'ecologia', 'estacion'],
    dimensions: { width: 1.25, height: 0.85, depth: 0.50 },
    triBudget: '280-360',
    glbUrl: '/models/modular/sci_waste_sorter.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_waste_sorter',
      name: 'Estación de Triaje de Residuos 3 Bocas',
      category: 'furniture',
      description: 'Estación de clasificación y reciclaje hermético con 3 tolvas basculantes codificadas por color (orgánico, metales, biológico).',
      units: 'meters',
      dimensions: { width: 1.25, height: 0.85, depth: 0.50 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'chasis_triple_estanco',
          shape: 'box',
          size: [1.25, 0.80, 0.50],
          position: [0, 0.40, 0],
          color: '#2d3748',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.6,
          metalness: 0.5
        },
        {
          name: 'zocalo_suelo_goma',
          shape: 'box',
          size: [1.27, 0.05, 0.52],
          position: [0, 0.025, 0],
          color: '#1a202c',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.2
        },
        {
          name: 'tolva_1_organico_verde',
          shape: 'box',
          size: [0.35, 0.24, 0.03],
          position: [-0.40, 0.62, 0.25],
          rotation: [-20, 0, 0],
          color: '#2f855a',
          texturePreset: 'painted_metal_white',
          roughness: 0.4,
          metalness: 0.4
        },
        {
          name: 'tolva_2_metales_azul',
          shape: 'box',
          size: [0.35, 0.24, 0.03],
          position: [0, 0.62, 0.25],
          rotation: [-20, 0, 0],
          color: '#2b6cb0',
          texturePreset: 'painted_metal_blue',
          roughness: 0.4,
          metalness: 0.4
        },
        {
          name: 'tolva_3_biologico_rojo',
          shape: 'box',
          size: [0.35, 0.24, 0.03],
          position: [0.40, 0.62, 0.25],
          rotation: [-20, 0, 0],
          color: '#c53030',
          texturePreset: 'red_paint_worn',
          roughness: 0.4,
          metalness: 0.4
        },
        {
          name: 'tirador_tolva_1',
          shape: 'box',
          size: [0.15, 0.02, 0.025],
          position: [-0.40, 0.70, 0.28],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'tirador_tolva_2',
          shape: 'box',
          size: [0.15, 0.02, 0.025],
          position: [0, 0.70, 0.28],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'tirador_tolva_3',
          shape: 'box',
          size: [0.15, 0.02, 0.025],
          position: [0.40, 0.70, 0.28],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.2,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 20. MÓDULO DE HIDRATACIÓN Y ESTIMULANTES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_coffee_station',
    family: 'sci_coffee_station',
    name: 'Módulo de Hidratación y Estimulantes',
    batch: 1,
    batchName: 'Mobiliario y Descanso Sci-Fi',
    category: 'furniture',
    description: 'Estación de café y electrolitos de tripulación con mueble bajo, grifos de suministro presurizado, bandeja antigoteo y estante de termos.',
    tags: ['cafe', 'hidratacion', 'bebidas', 'cantina', 'cafetera', 'estimulantes'],
    dimensions: { width: 0.95, height: 1.20, depth: 0.55 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_coffee_station.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_coffee_station',
      name: 'Módulo de Hidratación y Estimulantes',
      category: 'furniture',
      description: 'Estación de café y electrolitos de tripulación con mueble bajo, grifos de suministro presurizado, bandeja antigoteo y estante de termos.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.20, depth: 0.55 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'aparador_inferior',
          shape: 'box',
          size: [0.95, 0.75, 0.55],
          position: [0, 0.375, 0],
          color: '#2d3748',
          texturePreset: 'wood_dark_panel',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'encimera_servicio_acero',
          shape: 'box',
          size: [0.98, 0.04, 0.58],
          position: [0, 0.77, 0],
          color: '#cbd5e0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'maquina_dispensadora_estimulantes',
          shape: 'box',
          size: [0.55, 0.38, 0.32],
          position: [0, 0.98, -0.06],
          color: '#1a202c',
          texturePreset: 'scifi_trim_dark',
          roughness: 0.4,
          metalness: 0.6
        },
        {
          name: 'bandeja_antigoteo_rejilla',
          shape: 'box',
          size: [0.45, 0.02, 0.16],
          position: [0, 0.80, 0.12],
          color: '#a0aec0',
          texturePreset: 'metal_grate',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'grifo_dispensador_1',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.08, 6],
          position: [-0.08, 0.94, 0.10],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'grifo_dispensador_2',
          shape: 'cylinder',
          size: [0.012, 0.012, 0.08, 6],
          position: [0.08, 0.94, 0.10],
          color: '#e2e8f0',
          texturePreset: 'chrome_mirror',
          roughness: 0.1,
          metalness: 0.95
        },
        {
          name: 'display_temperatura_led',
          shape: 'box',
          size: [0.14, 0.04, 0.01],
          position: [0, 1.10, 0.105],
          color: '#38a169',
          texturePreset: 'crt_display_phosphor',
          roughness: 0.2,
          metalness: 0.1,
          emissive: '#38a169',
          emissiveIntensity: 0.8
        },
        {
          name: 'termo_aluminio_1',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.16, 8],
          position: [-0.34, 0.87, 0.10],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'termo_aluminio_2',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.16, 8],
          position: [0.34, 0.87, 0.10],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.3,
          metalness: 0.85
        }
      ]
    }
  }
];

import { MODULAR_MODELS_LOTE_2 } from './modular-catalog-lote2.ts';

export { MODULAR_MODELS_LOTE_2 };

export const ALL_MODULAR_MODELS: ModularModelEntry[] = [
  ...MODULAR_MODELS_LOTE_1,
  ...MODULAR_MODELS_LOTE_2
];

export function getModularModelByFamily(family: string): ModularModelEntry | undefined {
  return ALL_MODULAR_MODELS.find((m) => m.family === family);
}

export function getAllModularModels(): ModularModelEntry[] {
  return ALL_MODULAR_MODELS;
}

