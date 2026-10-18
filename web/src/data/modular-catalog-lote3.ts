import type { ModularModelEntry } from './modular-catalog.ts';

export const MODULAR_MODELS_LOTE_3: ModularModelEntry[] = [
  // -------------------------------------------------------------------------
  // 01. CÁPSULA CRIOGÉNICA DE ESTASIS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cryo_stasis_capsule',
    family: 'sci_cryo_stasis_capsule',
    name: 'Cápsula Criogénica de Estasis',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Cápsula vertical de hibernación con cilindro de cryo-glass tintado, columna dorsal de refrigerante, display biométrico y anillo base sellado.',
    tags: ['criogenia', 'estasis', 'capsula', 'hibernacion', 'medico', 'laboratorio', 'vida'],
    dimensions: { width: 1.10, height: 2.15, depth: 1.10 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_cryo_stasis_capsule.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cryo_stasis_capsule',
      name: 'Cápsula Criogénica de Estasis',
      category: 'medical',
      description: 'Cápsula vertical de hibernación con cilindro de cryo-glass tintado, columna dorsal de refrigerante, display biométrico y anillo base sellado.',
      units: 'meters',
      dimensions: { width: 1.10, height: 2.15, depth: 1.10 },
      palette: 'clean_lab',
      components: [
        {
          name: 'base_anillo_sellado',
          shape: 'cylinder',
          size: [0.55, 0.55, 0.12, 16],
          position: [0, 0.06, 0],
          color: '#1a202c',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'pedestal_plataforma_interior',
          shape: 'cylinder',
          size: [0.44, 0.44, 0.08, 16],
          position: [0, 0.16, 0],
          color: '#111827',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'columna_dorsal_soporte',
          shape: 'box',
          size: [0.42, 1.95, 0.28],
          position: [0, 1.12, -0.36],
          color: '#e2e8f0',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'tubo_refrigerante_izq',
          shape: 'cylinder',
          size: [0.035, 0.035, 1.80, 8],
          position: [-0.18, 1.10, -0.42],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'tubo_refrigerante_der',
          shape: 'cylinder',
          size: [0.035, 0.035, 1.80, 8],
          position: [0.18, 1.10, -0.42],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'cilindro_camara_vidrio',
          shape: 'cylinder',
          size: [0.46, 0.46, 1.60, 16],
          position: [0, 1.00, 0],
          color: '#67e8f9',
          texturePreset: 'cryo_glass_ice',
          opacity: 0.65,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'lecho_anatomico_respaldo',
          shape: 'box',
          size: [0.36, 1.45, 0.08],
          position: [0, 1.05, -0.16],
          color: '#cbd5e1',
          texturePreset: 'silicone_medical',
          roughness: 0.4,
          metalness: 0.05
        },
        {
          name: 'cabezal_presurizador_cupula',
          shape: 'cylinder',
          size: [0.52, 0.52, 0.22, 16],
          position: [0, 1.91, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'panel_diagnostico_lateral',
          shape: 'box',
          size: [0.16, 0.28, 0.04],
          position: [0.48, 1.25, 0.12],
          color: '#334155',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'pantalla_vitales_led',
          shape: 'box',
          size: [0.13, 0.18, 0.01],
          position: [0.48, 1.27, 0.145],
          color: '#00e5ff',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 02. CAMILLA QUIRÚRGICA SERVOASISTIDA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_surgical_operating_pod',
    family: 'sci_surgical_operating_pod',
    name: 'Camilla Quirúrgica Servoasistida',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Mesa de cirugía robótica automatizada con base telescópica, lecho anatómico segmentado, brazo de microcirugía superior y monitor ECG.',
    tags: ['camilla', 'cirugia', 'robot', 'medico', 'quirofano', 'hospital', 'servo'],
    dimensions: { width: 1.00, height: 1.95, depth: 2.05 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_surgical_operating_pod.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_surgical_operating_pod',
      name: 'Camilla Quirúrgica Servoasistida',
      category: 'medical',
      description: 'Mesa de cirugía robótica automatizada con base telescópica, lecho anatómico segmentado, brazo de microcirugía superior y monitor ECG.',
      units: 'meters',
      dimensions: { width: 1.00, height: 1.95, depth: 2.05 },
      palette: 'clean_lab',
      components: [
        {
          name: 'base_hidraulica_suelo',
          shape: 'box',
          size: [0.85, 0.12, 1.40],
          position: [0, 0.06, 0],
          color: '#1a202c',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'columna_elevacion_telescopica',
          shape: 'cylinder',
          size: [0.16, 0.16, 0.60, 12],
          position: [0, 0.42, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'bastidor_lecho_acero',
          shape: 'box',
          size: [0.70, 0.08, 1.90],
          position: [0, 0.76, 0],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.75
        },
        {
          name: 'colchon_quirurgico_torso',
          shape: 'box',
          size: [0.62, 0.09, 1.10],
          position: [0, 0.845, -0.05],
          color: '#0284c7',
          texturePreset: 'silicone_medical',
          roughness: 0.35,
          metalness: 0.05
        },
        {
          name: 'colchon_quirurgico_piernas',
          shape: 'box',
          size: [0.58, 0.08, 0.65],
          position: [0, 0.84, 0.85],
          color: '#0284c7',
          texturePreset: 'silicone_medical',
          roughness: 0.35,
          metalness: 0.05
        },
        {
          name: 'reposacabezas_articulado',
          shape: 'box',
          size: [0.32, 0.08, 0.28],
          position: [0, 0.88, -0.76],
          color: '#0369a1',
          texturePreset: 'silicone_medical',
          roughness: 0.35,
          metalness: 0.05
        },
        {
          name: 'poste_soporte_brazo_quirurgico',
          shape: 'cylinder',
          size: [0.05, 0.05, 1.15, 8],
          position: [-0.42, 1.30, -0.50],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'brazo_robotico_segmento_1',
          shape: 'box',
          size: [0.08, 0.08, 0.55],
          position: [-0.22, 1.85, -0.40],
          rotation: [0.2, 0.3, 0],
          color: '#475569',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.3
        },
        {
          name: 'cabezal_instrumental_laser',
          shape: 'cylinder',
          size: [0.09, 0.09, 0.20, 8],
          position: [0, 1.62, -0.15],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'emisor_luz_focal_led',
          shape: 'cylinder',
          size: [0.07, 0.07, 0.02, 12],
          position: [0, 1.51, -0.15],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'monitor_signos_vitales',
          shape: 'box',
          size: [0.32, 0.24, 0.04],
          position: [0.44, 1.25, -0.30],
          color: '#1e293b',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 03. CENTRÍFUGA DE LABORATORIO CLÍNICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_centrifuge_bench_analyzer',
    family: 'sci_centrifuge_bench_analyzer',
    name: 'Centrífuga de Laboratorio Clínico',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Centrífuga analítica de alta velocidad para tubos de ensayo con tambor rotatorio, tapa acrílica con cierre electromagnético y panel digital.',
    tags: ['centrifuga', 'laboratorio', 'tubos', 'analisis', 'clinico', 'sangre', 'rpm'],
    dimensions: { width: 0.60, height: 0.46, depth: 0.60 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_centrifuge_bench_analyzer.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_centrifuge_bench_analyzer',
      name: 'Centrífuga de Laboratorio Clínico',
      category: 'medical',
      description: 'Centrífuga analítica de alta velocidad para tubos de ensayo con tambor rotatorio, tapa acrílica con cierre electromagnético y panel digital.',
      units: 'meters',
      dimensions: { width: 0.60, height: 0.46, depth: 0.60 },
      palette: 'clean_lab',
      components: [
        {
          name: 'patas_goma_antivibracion',
          shape: 'box',
          size: [0.56, 0.03, 0.56],
          position: [0, 0.015, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cuerpo_chasis_principal',
          shape: 'box',
          size: [0.58, 0.34, 0.58],
          position: [0, 0.20, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'anillo_superior_biselado',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.04, 16],
          position: [0, 0.39, 0.04],
          color: '#94a3b8',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'tapa_acrilica_centrifuga',
          shape: 'cylinder',
          size: [0.24, 0.24, 0.03, 16],
          position: [0, 0.425, 0.04],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.55,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'tambor_rotores_interno',
          shape: 'cylinder',
          size: [0.20, 0.20, 0.16, 12],
          position: [0, 0.27, 0.04],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'panel_control_inclinado',
          shape: 'box',
          size: [0.38, 0.10, 0.12],
          position: [0, 0.32, 0.26],
          rotation: [-0.4, 0, 0],
          color: '#1e293b',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'pantalla_lcd_rpm',
          shape: 'box',
          size: [0.18, 0.06, 0.01],
          position: [0, 0.33, 0.29],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'rejilla_ventilacion_trasera',
          shape: 'box',
          size: [0.44, 0.18, 0.02],
          position: [0, 0.22, -0.295],
          color: '#334155',
          texturePreset: 'server_vent_panel',
          roughness: 0.5,
          metalness: 0.7
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 04. SECUENCIADOR GENÉTICO DE TORRE
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_dna_sequencer_tower',
    family: 'sci_dna_sequencer_tower',
    name: 'Secuenciador Genético de Torre',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Unidad vertical de análisis molecular NGS con cámara de reactivos refrigerada, bahía para microchips y pantalla vertical de telemetría génica.',
    tags: ['adn', 'secuenciador', 'genetica', 'ngs', 'laboratorio', 'biologia', 'molecular'],
    dimensions: { width: 0.65, height: 1.62, depth: 0.70 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_dna_sequencer_tower.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_dna_sequencer_tower',
      name: 'Secuenciador Genético de Torre',
      category: 'medical',
      description: 'Unidad vertical de análisis molecular NGS con cámara de reactivos refrigerada, bahía para microchips y pantalla vertical de telemetría génica.',
      units: 'meters',
      dimensions: { width: 0.65, height: 1.62, depth: 0.70 },
      palette: 'clean_lab',
      components: [
        {
          name: 'plinto_soporte_antideslizante',
          shape: 'box',
          size: [0.65, 0.06, 0.70],
          position: [0, 0.03, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'torre_chasis_laboratorio',
          shape: 'box',
          size: [0.60, 1.45, 0.65],
          position: [0, 0.785, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'camara_reactivos_frontal',
          shape: 'box',
          size: [0.50, 0.36, 0.12],
          position: [0, 0.45, 0.29],
          color: '#334155',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'tapa_refrigerada_visor',
          shape: 'box',
          size: [0.46, 0.28, 0.02],
          position: [0, 0.45, 0.355],
          color: '#f59e0b',
          texturePreset: 'amber_lab_glass',
          opacity: 0.7,
          roughness: 0.15,
          metalness: 0.1
        },
        {
          name: 'bahia_celdas_flujo',
          shape: 'box',
          size: [0.32, 0.08, 0.10],
          position: [0, 0.74, 0.30],
          color: '#94a3b8',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'pantalla_tactil_vertical',
          shape: 'box',
          size: [0.38, 0.52, 0.03],
          position: [0, 1.14, 0.32],
          color: '#0f172a',
          texturePreset: 'tinted_glass',
          roughness: 0.1,
          metalness: 0.2
        },
        {
          name: 'display_curva_genomica',
          shape: 'box',
          size: [0.34, 0.46, 0.01],
          position: [0, 1.14, 0.34],
          color: '#3b82f6',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'bocacartuchos_lateral',
          shape: 'box',
          size: [0.06, 0.30, 0.22],
          position: [0.31, 0.90, 0],
          color: '#475569',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'conducto_evacuacion_superior',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.12, 8],
          position: [0, 1.57, -0.15],
          color: '#cbd5e1',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 05. DUCHA DE DESCONTAMINACIÓN QUÍMICA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_decontamination_airlock_shower',
    family: 'sci_decontamination_airlock_shower',
    name: 'Ducha de Descontaminación Química',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Cabina abierta de desinfección con plataforma de rejilla drenante, 4 columnas tubulares, arco de rociadores atomizadores y tanque químico.',
    tags: ['descontaminacion', 'ducha', 'quimica', 'hazmat', 'bioseguridad', 'seguridad', 'rociador'],
    dimensions: { width: 1.25, height: 2.25, depth: 1.10 },
    triBudget: '400-500',
    glbUrl: '/models/modular/sci_decontamination_airlock_shower.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_decontamination_airlock_shower',
      name: 'Ducha de Descontaminación Química',
      category: 'medical',
      description: 'Cabina abierta de desinfección con plataforma de rejilla drenante, 4 columnas tubulares, arco de rociadores atomizadores y tanque químico.',
      units: 'meters',
      dimensions: { width: 1.25, height: 2.25, depth: 1.10 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bandeja_receptora_sumidero',
          shape: 'box',
          size: [1.10, 0.08, 1.10],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'rejilla_drenaje_antideslizante',
          shape: 'box',
          size: [0.98, 0.03, 0.98],
          position: [0, 0.095, 0],
          color: '#64748b',
          texturePreset: 'metal_galvanized',
          roughness: 0.5,
          metalness: 0.85
        },
        {
          name: 'columna_tubular_so',
          shape: 'cylinder',
          size: [0.03, 0.03, 2.15, 8],
          position: [-0.46, 1.175, -0.46],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'columna_tubular_se',
          shape: 'cylinder',
          size: [0.03, 0.03, 2.15, 8],
          position: [0.46, 1.175, -0.46],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'columna_tubular_no',
          shape: 'cylinder',
          size: [0.03, 0.03, 2.15, 8],
          position: [-0.46, 1.175, 0.46],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'columna_tubular_ne',
          shape: 'cylinder',
          size: [0.03, 0.03, 2.15, 8],
          position: [0.46, 1.175, 0.46],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'arco_distribuidor_superior',
          shape: 'box',
          size: [0.96, 0.06, 0.96],
          position: [0, 2.22, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'rociador_cono_central',
          shape: 'cone',
          size: [0.12, 0.12, 0.09, 8],
          position: [0, 2.15, 0],
          rotation: [Math.PI, 0, 0],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'tanque_solucion_desinfectante',
          shape: 'cylinder',
          size: [0.14, 0.14, 0.70, 10],
          position: [-0.56, 1.20, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'palanca_activacion_emergencia',
          shape: 'box',
          size: [0.04, 0.26, 0.06],
          position: [0.48, 1.30, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.35,
          metalness: 0.4
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 06. AUTOCLAVE ESTERILIZADOR PRESURIZADO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_autoclave_sterilizer',
    family: 'sci_autoclave_sterilizer',
    name: 'Autoclave Esterilizador Presurizado',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Esterilizador a vapor cilíndrico de alta presión con compuerta circular reforzada, volante de cierre estanco, manómetros dobles y válvula de escape.',
    tags: ['autoclave', 'esterilizador', 'presion', 'vapor', 'quirurgico', 'limpieza', 'hospital'],
    dimensions: { width: 0.75, height: 1.35, depth: 1.20 },
    triBudget: '420-500',
    glbUrl: '/models/modular/sci_autoclave_sterilizer.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_autoclave_sterilizer',
      name: 'Autoclave Esterilizador Presurizado',
      category: 'medical',
      description: 'Esterilizador a vapor cilíndrico de alta presión con compuerta circular reforzada, volante de cierre estanco, manómetros dobles y válvula de escape.',
      units: 'meters',
      dimensions: { width: 0.75, height: 1.35, depth: 1.20 },
      palette: 'clean_lab',
      components: [
        {
          name: 'bancada_bastidor_tubular',
          shape: 'box',
          size: [0.75, 0.48, 1.10],
          position: [0, 0.24, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'cilindro_camara_autoclave',
          shape: 'cylinder',
          size: [0.34, 0.34, 1.15, 16],
          position: [0, 0.82, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'abrazadera_refuerzo_1',
          shape: 'cylinder',
          size: [0.36, 0.36, 0.06, 16],
          position: [0, 0.82, -0.30],
          rotation: [Math.PI / 2, 0, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'abrazadera_refuerzo_2',
          shape: 'cylinder',
          size: [0.36, 0.36, 0.06, 16],
          position: [0, 0.82, 0.30],
          rotation: [Math.PI / 2, 0, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'puerta_circular_masiva',
          shape: 'cylinder',
          size: [0.35, 0.35, 0.08, 16],
          position: [0, 0.82, 0.60],
          rotation: [Math.PI / 2, 0, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'volante_bloqueo_estrella',
          shape: 'ring',
          size: [0.18, 0.04, 8],
          position: [0, 0.82, 0.66],
          rotation: [0, 0, 0],
          color: '#eab308',
          texturePreset: 'hazard_stripes',
          roughness: 0.4,
          metalness: 0.5
        },
        {
          name: 'manometro_presion_vapor',
          shape: 'cylinder',
          size: [0.06, 0.06, 0.04, 12],
          position: [-0.22, 1.20, 0.35],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'valvula_alivio_seguridad',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.16, 8],
          position: [0.18, 1.22, -0.15],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'consola_mandos_digital',
          shape: 'box',
          size: [0.26, 0.22, 0.08],
          position: [0.38, 0.82, 0.40],
          color: '#334155',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 07. BIORREACTOR DE CULTIVO CELULAR
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_bioreactor_culture_vat',
    family: 'sci_bioreactor_culture_vat',
    name: 'Biorreactor de Cultivo Celular',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Biorreactor vertical para síntesis celular y fermentación microbiológica, con tanque acristalado, eje de agitación magnética y sondas de pH.',
    tags: ['biorreactor', 'cultivo', 'celulas', 'fermentacion', 'biologia', 'microbio', 'laboratorio'],
    dimensions: { width: 0.70, height: 1.45, depth: 0.70 },
    triBudget: '400-480',
    glbUrl: '/models/modular/sci_bioreactor_culture_vat.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_bioreactor_culture_vat',
      name: 'Biorreactor de Cultivo Celular',
      category: 'medical',
      description: 'Biorreactor vertical para síntesis celular y fermentación microbiológica, con tanque acristalado, eje de agitación magnética y sondas de pH.',
      units: 'meters',
      dimensions: { width: 0.70, height: 1.45, depth: 0.70 },
      palette: 'clean_lab',
      components: [
        {
          name: 'soporte_base_tripode',
          shape: 'cylinder',
          size: [0.35, 0.35, 0.14, 12],
          position: [0, 0.07, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'motor_agitador_magnetico',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.16, 10],
          position: [0, 0.22, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'tanque_cristal_borosilicato',
          shape: 'cylinder',
          size: [0.28, 0.28, 0.90, 16],
          position: [0, 0.75, 0],
          color: '#a7f3d0',
          texturePreset: 'clean_glass',
          opacity: 0.5,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'liquido_medio_cultivo',
          shape: 'cylinder',
          size: [0.25, 0.25, 0.65, 12],
          position: [0, 0.65, 0],
          color: '#10b981',
          opacity: 0.75,
          roughness: 0.2,
          metalness: 0.0
        },
        {
          name: 'eje_paletas_dispersion',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.85, 6],
          position: [0, 0.78, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'tapa_cabezal_brida_acero',
          shape: 'cylinder',
          size: [0.30, 0.30, 0.08, 16],
          position: [0, 1.24, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'puertos_muestreo_manifold',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.14, 8],
          position: [0.10, 1.34, 0.08],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'columna_control_ph_oxigeno',
          shape: 'box',
          size: [0.18, 0.65, 0.16],
          position: [0.38, 0.70, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'pantalla_grafica_bioproceso',
          shape: 'box',
          size: [0.14, 0.20, 0.01],
          position: [0.47, 0.82, 0],
          color: '#06b6d4',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 08. CARRITO DE PARO Y REANIMACIÓN
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_defibrillator_crash_cart',
    family: 'sci_defibrillator_crash_cart',
    name: 'Carrito de Paro y Reanimación',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Carro rodante de emergencias médicas con módulo desfibrilador bifásico, pantalla ECG, palas de choque y cajones sellados de fármacos.',
    tags: ['desfibrilador', 'urgencias', 'medico', 'paro', 'farmacos', 'oxigeno', 'hospital'],
    dimensions: { width: 0.80, height: 1.15, depth: 0.60 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_defibrillator_crash_cart.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_defibrillator_crash_cart',
      name: 'Carrito de Paro y Reanimación',
      category: 'medical',
      description: 'Carro rodante de emergencias médicas con módulo desfibrilador bifásico, pantalla ECG, palas de choque y cajones sellados de fármacos.',
      units: 'meters',
      dimensions: { width: 0.80, height: 1.15, depth: 0.60 },
      palette: 'clean_lab',
      components: [
        {
          name: 'plataforma_chasis_con_ruedas',
          shape: 'box',
          size: [0.65, 0.10, 0.55],
          position: [0, 0.08, 0],
          color: '#1e293b',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'cajonera_fármacos_rojo',
          shape: 'box',
          size: [0.58, 0.62, 0.48],
          position: [0, 0.44, 0],
          color: '#dc2626',
          roughness: 0.35,
          metalness: 0.15
        },
        {
          name: 'tiradores_aluminio_cajones',
          shape: 'box',
          size: [0.42, 0.03, 0.03],
          position: [0, 0.58, 0.25],
          color: '#e2e8f0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'mesa_bandeja_superior',
          shape: 'box',
          size: [0.62, 0.04, 0.52],
          position: [0, 0.77, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'modulo_desfibrilador',
          shape: 'box',
          size: [0.36, 0.26, 0.28],
          position: [-0.08, 0.92, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'pantalla_ecg_trazo',
          shape: 'box',
          size: [0.24, 0.15, 0.01],
          position: [-0.08, 0.94, 0.145],
          color: '#22c55e',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'soporte_palas_descarga',
          shape: 'box',
          size: [0.14, 0.16, 0.08],
          position: [0.18, 0.90, 0.05],
          color: '#0f172a',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'botella_oxigeno_lateral',
          shape: 'cylinder',
          size: [0.07, 0.07, 0.55, 10],
          position: [0.35, 0.50, -0.10],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'manija_empuje_tubular',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.50, 8],
          position: [-0.34, 0.88, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 09. MICROSCOPIO ELECTRÓNICO DE TRANSMISIÓN
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_electron_microscope_station',
    family: 'sci_electron_microscope_station',
    name: 'Microscopio Electrónico de Transmisión',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Estación de análisis nanométrico con columna de vacío apantallada contra campos electromagnéticos, goniómetro y consola doble de enfoque.',
    tags: ['microscopio', 'electronico', 'nanometros', 'vacio', 'laboratorio', 'investigacion', 'muestra'],
    dimensions: { width: 1.25, height: 1.95, depth: 0.90 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_electron_microscope_station.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_electron_microscope_station',
      name: 'Microscopio Electrónico de Transmisión',
      category: 'medical',
      description: 'Estación de análisis nanométrico con columna de vacío apantallada contra campos electromagnéticos, goniómetro y consola doble de enfoque.',
      units: 'meters',
      dimensions: { width: 1.25, height: 1.95, depth: 0.90 },
      palette: 'clean_lab',
      components: [
        {
          name: 'mesa_antivibratoria_pesada',
          shape: 'box',
          size: [1.20, 0.72, 0.85],
          position: [0, 0.36, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'tablero_superficie_laboratorio',
          shape: 'box',
          size: [1.24, 0.05, 0.89],
          position: [0, 0.745, 0],
          color: '#f8fafc',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.25,
          metalness: 0.05
        },
        {
          name: 'camara_vacio_muestras',
          shape: 'cylinder',
          size: [0.24, 0.24, 0.28, 12],
          position: [0, 0.91, -0.05],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'columna_haz_electrones',
          shape: 'cylinder',
          size: [0.15, 0.15, 0.85, 16],
          position: [0, 1.47, -0.05],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'anillos_deflexion_magnetica',
          shape: 'cylinder',
          size: [0.19, 0.19, 0.08, 16],
          position: [0, 1.40, -0.05],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'visor_binocular_ergonomico',
          shape: 'box',
          size: [0.18, 0.12, 0.14],
          position: [0, 1.05, 0.18],
          rotation: [-0.4, 0, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.8,
          metalness: 0.1
        },
        {
          name: 'panel_joysticks_goniometro',
          shape: 'box',
          size: [0.36, 0.08, 0.20],
          position: [-0.35, 0.80, 0.22],
          color: '#334155',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'pantalla_nanoscopia_alta_res',
          shape: 'box',
          size: [0.45, 0.32, 0.04],
          position: [0.35, 1.02, 0.15],
          rotation: [0, -0.2, 0],
          color: '#1e293b',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'display_reticula_muestra',
          shape: 'box',
          size: [0.40, 0.26, 0.01],
          position: [0.33, 1.02, 0.17],
          rotation: [0, -0.2, 0],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 10. ARMARIO INCUBADOR DE CULTIVOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_incubator_specimen_cabinet',
    family: 'sci_incubator_specimen_cabinet',
    name: 'Armario Incubador de Cultivos',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Cámara térmica y ambiental controlada con puerta de vidrio calefactable, bandejas de cultivo celular, inyección de CO2 y display de parámetros.',
    tags: ['incubador', 'cultivo', 'microbiologia', 'temperatura', 'co2', 'laboratorio', 'armario'],
    dimensions: { width: 0.85, height: 1.75, depth: 0.75 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_incubator_specimen_cabinet.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_incubator_specimen_cabinet',
      name: 'Armario Incubador de Cultivos',
      category: 'medical',
      description: 'Cámara térmica y ambiental controlada con puerta de vidrio calefactable, bandejas de cultivo celular, inyección de CO2 y display de parámetros.',
      units: 'meters',
      dimensions: { width: 0.85, height: 1.75, depth: 0.75 },
      palette: 'clean_lab',
      components: [
        {
          name: 'base_plinto_niveladores',
          shape: 'box',
          size: [0.85, 0.10, 0.75],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'chasis_isotermico_doble_pared',
          shape: 'box',
          size: [0.80, 1.55, 0.70],
          position: [0, 0.875, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'puerta_vidrio_visor',
          shape: 'box',
          size: [0.72, 1.25, 0.04],
          position: [0, 0.85, 0.35],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.6,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'marco_sellado_magnetico',
          shape: 'box',
          size: [0.76, 1.29, 0.03],
          position: [0, 0.85, 0.34],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'bandeja_perforada_nivel_1',
          shape: 'box',
          size: [0.68, 0.02, 0.55],
          position: [0, 0.55, 0],
          color: '#94a3b8',
          texturePreset: 'metal_perforated',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'bandeja_perforada_nivel_2',
          shape: 'box',
          size: [0.68, 0.02, 0.55],
          position: [0, 0.85, 0],
          color: '#94a3b8',
          texturePreset: 'metal_perforated',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'bandeja_perforada_nivel_3',
          shape: 'box',
          size: [0.68, 0.02, 0.55],
          position: [0, 1.15, 0],
          color: '#94a3b8',
          texturePreset: 'metal_perforated',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'modulo_control_superior',
          shape: 'box',
          size: [0.72, 0.18, 0.08],
          position: [0, 1.54, 0.32],
          color: '#334155',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'display_co2_humedad',
          shape: 'box',
          size: [0.24, 0.08, 0.01],
          position: [0, 1.54, 0.365],
          color: '#f59e0b',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'filtro_hepa_superior',
          shape: 'cylinder',
          size: [0.16, 0.16, 0.08, 12],
          position: [0, 1.69, 0],
          color: '#64748b',
          texturePreset: 'server_vent_panel',
          roughness: 0.5,
          metalness: 0.7
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 11. POSTE DE INFUSIÓN Y BOMBA PERISTÁLTICA
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_iv_fluid_drip_station',
    family: 'sci_iv_fluid_drip_station',
    name: 'Poste de Infusión y Bomba Peristáltica',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Pie de gotero rodante de 5 patas con poste telescópico de acero, bomba inteligente de microinfusión y bolsas suspendidas de plasma/suero.',
    tags: ['suero', 'plasma', 'gotero', 'infusion', 'bomba', 'enfermeria', 'medico'],
    dimensions: { width: 0.55, height: 1.95, depth: 0.55 },
    triBudget: '320-380',
    glbUrl: '/models/modular/sci_iv_fluid_drip_station.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_iv_fluid_drip_station',
      name: 'Poste de Infusión y Bomba Peristáltica',
      category: 'medical',
      description: 'Pie de gotero rodante de 5 patas con poste telescópico de acero, bomba inteligente de microinfusión y bolsas suspendidas de plasma/suero.',
      units: 'meters',
      dimensions: { width: 0.55, height: 1.95, depth: 0.55 },
      palette: 'clean_lab',
      components: [
        {
          name: 'base_estrella_5_ruedas',
          shape: 'cylinder',
          size: [0.32, 0.32, 0.06, 10],
          position: [0, 0.05, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'vastago_mastil_inferior',
          shape: 'cylinder',
          size: [0.03, 0.03, 0.90, 8],
          position: [0, 0.52, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'vastago_mastil_superior',
          shape: 'cylinder',
          size: [0.022, 0.022, 0.95, 8],
          position: [0, 1.35, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'bomba_peristaltica_infusion',
          shape: 'box',
          size: [0.18, 0.24, 0.14],
          position: [0, 1.05, 0.08],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'pantalla_dosificacion_ml',
          shape: 'box',
          size: [0.12, 0.08, 0.01],
          position: [0, 1.08, 0.155],
          color: '#06b6d4',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'arbol_ganchos_doble',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.36, 8],
          position: [0, 1.82, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'bolsa_suero_solucion_salina',
          shape: 'box',
          size: [0.10, 0.22, 0.04],
          position: [-0.14, 1.68, 0],
          color: '#bae6fd',
          texturePreset: 'clean_glass',
          opacity: 0.7,
          roughness: 0.2,
          metalness: 0.05
        },
        {
          name: 'bolsa_plasma_sanguineo',
          shape: 'box',
          size: [0.10, 0.20, 0.04],
          position: [0.14, 1.69, 0],
          color: '#991b1b',
          opacity: 0.8,
          roughness: 0.3,
          metalness: 0.05
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 12. ESCÁNER ANATÓMICO HOLOGRÁFICO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_holographic_anatomical_scanner',
    family: 'sci_holographic_anatomical_scanner',
    name: 'Escáner Anatómico Holográfico',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Plataforma de proyección tridimensional de órganos y tejidos biológicos con plato de emisión láser y consola médica de diagnóstico.',
    tags: ['holograma', 'escaner', 'diagnostico', 'organos', 'laser', '3d', 'medico'],
    dimensions: { width: 1.15, height: 1.45, depth: 1.15 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_holographic_anatomical_scanner.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_holographic_anatomical_scanner',
      name: 'Escáner Anatómico Holográfico',
      category: 'medical',
      description: 'Plataforma de proyección tridimensional de órganos y tejidos biológicos con plato de emisión láser y consola médica de diagnóstico.',
      units: 'meters',
      dimensions: { width: 1.15, height: 1.45, depth: 1.15 },
      palette: 'clean_lab',
      components: [
        {
          name: 'plato_emisor_holografico_base',
          shape: 'cylinder',
          size: [0.55, 0.55, 0.10, 16],
          position: [0, 0.05, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'aro_laser_proyector_concavo',
          shape: 'cylinder',
          size: [0.44, 0.44, 0.04, 16],
          position: [0, 0.11, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'foco_emisor_volumetrico',
          shape: 'sphere',
          size: [0.10, 8, 8],
          position: [0, 0.15, 0],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'holograma_proyectado_organo',
          shape: 'sphere',
          size: [0.22, 12, 12],
          position: [0, 0.85, 0],
          color: '#00e5ff',
          opacity: 0.45,
          roughness: 0.05,
          metalness: 0.0
        },
        {
          name: 'poste_articulado_consola',
          shape: 'cylinder',
          size: [0.04, 0.04, 0.90, 8],
          position: [0.48, 0.55, 0.25],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'consola_medico_volante',
          shape: 'box',
          size: [0.38, 0.24, 0.04],
          position: [0.42, 1.05, 0.22],
          rotation: [-0.3, -0.4, 0],
          color: '#334155',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'interfaz_tactil_medica',
          shape: 'box',
          size: [0.32, 0.18, 0.01],
          position: [0.42, 1.06, 0.23],
          rotation: [-0.3, -0.4, 0],
          color: '#3b82f6',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 13. BÓVEDA DE RESIDUOS BIOPELIGROSOS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_biohazard_disposal_vault',
    family: 'sci_biohazard_disposal_vault',
    name: 'Bóveda de Residuos Biopeligrosos',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Contenedor blindado para aislamiento y desecho de patógenos de nivel 4 con pedal neumático, junta de hermeticidad y dosímetro.',
    tags: ['biohazard', 'residuos', 'patogenos', 'blindado', 'peligro', 'bioseguridad', 'desecho'],
    dimensions: { width: 0.70, height: 0.95, depth: 0.70 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_biohazard_disposal_vault.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_biohazard_disposal_vault',
      name: 'Bóveda de Residuos Biopeligrosos',
      category: 'medical',
      description: 'Contenedor blindado para aislamiento y desecho de patógenos de nivel 4 con pedal neumático, junta de hermeticidad y dosímetro.',
      units: 'meters',
      dimensions: { width: 0.70, height: 0.95, depth: 0.70 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'base_pesada_contrapeso',
          shape: 'cylinder',
          size: [0.35, 0.35, 0.08, 12],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'pedal_neumatico_apertura',
          shape: 'box',
          size: [0.12, 0.04, 0.16],
          position: [0, 0.04, 0.32],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.25,
          metalness: 0.85
        },
        {
          name: 'cuerpo_cilindrico_blindado',
          shape: 'cylinder',
          size: [0.30, 0.30, 0.75, 16],
          position: [0, 0.45, 0],
          color: '#eab308',
          roughness: 0.35,
          metalness: 0.3
        },
        {
          name: 'franja_senial_biohazard',
          shape: 'cylinder',
          size: [0.305, 0.305, 0.18, 16],
          position: [0, 0.52, 0],
          color: '#ffffff',
          texturePreset: 'biohazard_label',
          roughness: 0.4,
          metalness: 0.1
        },
        {
          name: 'cuello_estanqueidad_goma',
          shape: 'cylinder',
          size: [0.28, 0.28, 0.06, 14],
          position: [0, 0.84, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'tapa_hermetica_pivotante',
          shape: 'cylinder',
          size: [0.32, 0.32, 0.07, 16],
          position: [0, 0.89, 0],
          color: '#334155',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.45,
          metalness: 0.2
        },
        {
          name: 'dosimetro_radiacion_digital',
          shape: 'box',
          size: [0.12, 0.14, 0.03],
          position: [0, 0.70, 0.30],
          color: '#475569',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'pantalla_dosimetro_lcd',
          shape: 'box',
          size: [0.08, 0.06, 0.01],
          position: [0, 0.70, 0.32],
          color: '#ef4444',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 14. FRASCO DEWAR CRIOGÉNICO DE NITRÓGENO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_cryogenic_dewar_flask',
    family: 'sci_cryogenic_dewar_flask',
    name: 'Frasco Dewar Criogénico de Nitrógeno',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Tanque térmico al vacío para preservación de muestras a -196°C con cuerpo de aluminio pulido, asas reforzadas y tapón aislante.',
    tags: ['dewar', 'nitrogeno', 'criogenico', 'frio', 'termo', 'muestras', 'aluminio'],
    dimensions: { width: 0.55, height: 1.05, depth: 0.55 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_cryogenic_dewar_flask.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_cryogenic_dewar_flask',
      name: 'Frasco Dewar Criogénico de Nitrógeno',
      category: 'medical',
      description: 'Tanque térmico al vacío para preservación de muestras a -196°C con cuerpo de aluminio pulido, asas reforzadas y tapón aislante.',
      units: 'meters',
      dimensions: { width: 0.55, height: 1.05, depth: 0.55 },
      palette: 'clean_lab',
      components: [
        {
          name: 'anillo_base_apoyo_goma',
          shape: 'cylinder',
          size: [0.26, 0.26, 0.05, 12],
          position: [0, 0.025, 0],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'cuerpo_dewar_aluminio',
          shape: 'cylinder',
          size: [0.25, 0.25, 0.68, 16],
          position: [0, 0.39, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'hombro_conico_reductor',
          shape: 'cone',
          size: [0.25, 0.14, 0.12, 16],
          position: [0, 0.78, 0],
          color: '#f8fafc',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'cuello_aislante_estrecho',
          shape: 'cylinder',
          size: [0.13, 0.13, 0.14, 12],
          position: [0, 0.89, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'tapon_esferico_aislante',
          shape: 'sphere',
          size: [0.09, 10, 10],
          position: [0, 0.98, 0],
          color: '#1e293b',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.5,
          metalness: 0.1
        },
        {
          name: 'asa_tubular_transporte_izq',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.24, 6],
          position: [-0.22, 0.72, 0],
          rotation: [0, 0, 0.5],
          color: '#cbd5e1',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'asa_tubular_transporte_der',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.24, 6],
          position: [0.22, 0.72, 0],
          rotation: [0, 0, -0.5],
          color: '#cbd5e1',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'valvula_seguridad_presion',
          shape: 'cylinder',
          size: [0.025, 0.025, 0.08, 6],
          position: [0.08, 0.88, 0.09],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 15. ULTRACONGELADOR DE MUESTRAS -80°C
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_sample_freezer_ultra_low',
    family: 'sci_sample_freezer_ultra_low',
    name: 'Ultracongelador de Muestras -80°C',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Armario vertical de ultra-baja temperatura con aislamiento al vacío de poliuretano, cerrojo de palanca hermético y registrador circular.',
    tags: ['ultracongelador', 'freezer', 'muestras', 'crio', 'termico', 'hospital', 'adn'],
    dimensions: { width: 0.95, height: 1.98, depth: 0.90 },
    triBudget: '380-460',
    glbUrl: '/models/modular/sci_sample_freezer_ultra_low.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_sample_freezer_ultra_low',
      name: 'Ultracongelador de Muestras -80°C',
      category: 'medical',
      description: 'Armario vertical de ultra-baja temperatura con aislamiento al vacío de poliuretano, cerrojo de palanca hermético y registrador circular.',
      units: 'meters',
      dimensions: { width: 0.95, height: 1.98, depth: 0.90 },
      palette: 'clean_lab',
      components: [
        {
          name: 'plinto_soporte_reforzado',
          shape: 'box',
          size: [0.95, 0.12, 0.85],
          position: [0, 0.06, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'gabinete_cuerpo_aislado',
          shape: 'box',
          size: [0.90, 1.85, 0.80],
          position: [0, 1.045, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'puerta_masiva_isotermica',
          shape: 'box',
          size: [0.86, 1.40, 0.10],
          position: [0, 1.18, 0.43],
          color: '#f1f5f9',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'manija_palanca_compresion',
          shape: 'box',
          size: [0.05, 0.35, 0.06],
          position: [0.38, 1.25, 0.50],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'panel_alarma_temperatura',
          shape: 'box',
          size: [0.36, 0.22, 0.04],
          position: [-0.15, 1.55, 0.49],
          color: '#334155',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'display_temperatura_menos80',
          shape: 'box',
          size: [0.20, 0.08, 0.01],
          position: [-0.15, 1.55, 0.515],
          color: '#38bdf8',
          roughness: 0.1,
          metalness: 0.0
        },
        {
          name: 'rejilla_compresor_inferior',
          shape: 'box',
          size: [0.82, 0.32, 0.02],
          position: [0, 0.28, 0.41],
          color: '#475569',
          texturePreset: 'server_vent_panel',
          roughness: 0.5,
          metalness: 0.7
        },
        {
          name: 'registrador_grafico_disco',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.02, 12],
          position: [0.22, 1.55, 0.49],
          color: '#e2e8f0',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.8
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 16. CAMILLA DE BIOCONTENCIÓN Y AISLAMIENTO
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_quarantine_isolation_stretcher',
    family: 'sci_quarantine_isolation_stretcher',
    name: 'Camilla de Biocontención y Aislamiento',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Camilla móvil con burbuja hermética de biocontención, sistema de presión negativa con filtro HEPA y guantes de manipulación interna.',
    tags: ['camilla', 'aislamiento', 'cuarentena', 'biocontencion', 'virus', 'patogeno', 'hepa'],
    dimensions: { width: 0.85, height: 1.25, depth: 2.05 },
    triBudget: '400-500',
    glbUrl: '/models/modular/sci_quarantine_isolation_stretcher.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_quarantine_isolation_stretcher',
      name: 'Camilla de Biocontención y Aislamiento',
      category: 'medical',
      description: 'Camilla móvil con burbuja hermética de biocontención, sistema de presión negativa con filtro HEPA y guantes de manipulación interna.',
      units: 'meters',
      dimensions: { width: 0.85, height: 1.25, depth: 2.05 },
      palette: 'industrial_hazard',
      components: [
        {
          name: 'bastidor_rodante_tijera',
          shape: 'box',
          size: [0.75, 0.45, 1.95],
          position: [0, 0.225, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.4,
          metalness: 0.8
        },
        {
          name: 'bandeja_colchoneta_aislada',
          shape: 'box',
          size: [0.70, 0.08, 1.88],
          position: [0, 0.49, 0],
          color: '#0284c7',
          texturePreset: 'silicone_medical',
          roughness: 0.35,
          metalness: 0.05
        },
        {
          name: 'arco_soporte_cupula',
          shape: 'cylinder',
          size: [0.32, 0.32, 1.80, 16],
          position: [0, 0.85, 0],
          rotation: [Math.PI / 2, 0, 0],
          color: '#bae6fd',
          texturePreset: 'clean_glass',
          opacity: 0.45,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'modulo_presion_negativa_pie',
          shape: 'box',
          size: [0.45, 0.28, 0.25],
          position: [0, 0.65, 0.90],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'puerto_guante_manipulacion_izq',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.05, 10],
          position: [-0.34, 0.82, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'puerto_guante_manipulacion_der',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.05, 10],
          position: [0.34, 0.82, 0],
          rotation: [0, 0, Math.PI / 2],
          color: '#0f172a',
          texturePreset: 'rubber_black',
          roughness: 0.9,
          metalness: 0.1
        },
        {
          name: 'manillar_direccion_cabecera',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.65, 8],
          position: [0, 0.82, -0.96],
          rotation: [0, 0, Math.PI / 2],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 17. CARRUSEL DE PIPETAS Y DISPENSADOR
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_pipette_workbench_carousel',
    family: 'sci_pipette_workbench_carousel',
    name: 'Carrusel de Pipetas y Dispensador',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Soporte rotatorio de sobremesa para 6 micropipetas volumétricas de precisión con portapuntas esterilizadas y bandeja de reactivos.',
    tags: ['pipeta', 'micropipeta', 'dispensador', 'puntas', 'mesa', 'laboratorio', 'reactivos'],
    dimensions: { width: 0.45, height: 0.45, depth: 0.45 },
    triBudget: '320-400',
    glbUrl: '/models/modular/sci_pipette_workbench_carousel.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_pipette_workbench_carousel',
      name: 'Carrusel de Pipetas y Dispensador',
      category: 'medical',
      description: 'Soporte rotatorio de sobremesa para 6 micropipetas volumétricas de precisión con portapuntas esterilizadas y bandeja de reactivos.',
      units: 'meters',
      dimensions: { width: 0.45, height: 0.45, depth: 0.45 },
      palette: 'clean_lab',
      components: [
        {
          name: 'base_circular_lastrada',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.04, 16],
          position: [0, 0.02, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'mastil_eje_rotatorio',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.38, 8],
          position: [0, 0.22, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'disco_soporte_perchas',
          shape: 'cylinder',
          size: [0.16, 0.16, 0.03, 12],
          position: [0, 0.39, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.3,
          metalness: 0.85
        },
        {
          name: 'micropipeta_p2',
          shape: 'box',
          size: [0.03, 0.24, 0.04],
          position: [0.11, 0.30, 0],
          color: '#0f172a',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'micropipeta_p20',
          shape: 'box',
          size: [0.03, 0.24, 0.04],
          position: [-0.11, 0.30, 0],
          color: '#ea580c',
          texturePreset: 'plastic_hazard_orange',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'micropipeta_p200',
          shape: 'box',
          size: [0.03, 0.24, 0.04],
          position: [0, 0.30, 0.11],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'micropipeta_p1000',
          shape: 'box',
          size: [0.035, 0.24, 0.04],
          position: [0, 0.30, -0.11],
          color: '#0284c7',
          texturePreset: 'silicone_medical',
          roughness: 0.35,
          metalness: 0.05
        },
        {
          name: 'caja_puntas_filtro',
          shape: 'box',
          size: [0.12, 0.06, 0.09],
          position: [0.24, 0.03, 0.05],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.6,
          roughness: 0.15,
          metalness: 0.1
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 18. SEPARADOR DE PLASMA Y AFÉRESIS
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_plasma_separator_module',
    family: 'sci_plasma_separator_module',
    name: 'Separador de Plasma y Aféresis',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Dispositivo de procesamiento hematológico con centrífuga continua para separación de eritrocitos, plaquetas y plasma rico en factores.',
    tags: ['plasma', 'aferesis', 'sangre', 'centrifuga', 'hematologia', 'hospital', 'laboratorio'],
    dimensions: { width: 0.65, height: 1.45, depth: 0.60 },
    triBudget: '360-440',
    glbUrl: '/models/modular/sci_plasma_separator_module.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_plasma_separator_module',
      name: 'Separador de Plasma y Aféresis',
      category: 'medical',
      description: 'Dispositivo de procesamiento hematológico con centrífuga continua para separación de eritrocitos, plaquetas y plasma rico en factores.',
      units: 'meters',
      dimensions: { width: 0.65, height: 1.45, depth: 0.60 },
      palette: 'clean_lab',
      components: [
        {
          name: 'chasis_rodante_gabinete',
          shape: 'box',
          size: [0.65, 0.85, 0.55],
          position: [0, 0.425, 0],
          color: '#f8fafc',
          texturePreset: 'plastic_medical_white',
          roughness: 0.3,
          metalness: 0.1
        },
        {
          name: 'camara_rotor_aferesis',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.12, 16],
          position: [0, 0.90, -0.05],
          color: '#94a3b8',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'tapa_transparente_rotor',
          shape: 'cylinder',
          size: [0.17, 0.17, 0.02, 16],
          position: [0, 0.97, -0.05],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.6,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'valvulas_manifold_tubos',
          shape: 'box',
          size: [0.28, 0.08, 0.05],
          position: [0, 0.88, 0.16],
          color: '#334155',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'poste_percha_bolsas',
          shape: 'cylinder',
          size: [0.015, 0.015, 0.55, 8],
          position: [0.25, 1.15, -0.15],
          color: '#cbd5e1',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.85
        },
        {
          name: 'bolsa_colectora_plasma',
          shape: 'box',
          size: [0.08, 0.16, 0.03],
          position: [0.25, 1.25, -0.15],
          color: '#facc15',
          opacity: 0.8,
          roughness: 0.3,
          metalness: 0.05
        },
        {
          name: 'pantalla_tactil_procesos',
          shape: 'box',
          size: [0.30, 0.20, 0.03],
          position: [-0.12, 1.05, 0.10],
          rotation: [-0.3, 0, 0],
          color: '#1e293b',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        },
        {
          name: 'interfaz_flujo_volumen',
          shape: 'box',
          size: [0.26, 0.16, 0.01],
          position: [-0.12, 1.05, 0.12],
          rotation: [-0.3, 0, 0],
          color: '#10b981',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 19. CAMPANA DE EXTRACCIÓN DE GASES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_hazard_fume_hood',
    family: 'sci_hazard_fume_hood',
    name: 'Campana de Extracción de Gases',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Cabina de bioseguridad para contención de vapores químicos y reactivos tóxicos con guillotina de vidrio deslizante y extractor superior.',
    tags: ['campana', 'extraccion', 'gases', 'fume', 'quimica', 'reactivos', 'seguridad', 'laboratorio'],
    dimensions: { width: 1.25, height: 2.70, depth: 0.90 },
    triBudget: '420-520',
    glbUrl: '/models/modular/sci_hazard_fume_hood.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_hazard_fume_hood',
      name: 'Campana de Extracción de Gases',
      category: 'medical',
      description: 'Cabina de bioseguridad para contención de vapores químicos y reactivos tóxicos con guillotina de vidrio deslizante y extractor superior.',
      units: 'meters',
      dimensions: { width: 1.25, height: 2.70, depth: 0.90 },
      palette: 'clean_lab',
      components: [
        {
          name: 'armario_inferior_reactivos',
          shape: 'box',
          size: [1.20, 0.75, 0.85],
          position: [0, 0.375, 0],
          color: '#334155',
          texturePreset: 'metal_galvanized',
          roughness: 0.5,
          metalness: 0.8
        },
        {
          name: 'encimera_resina_ceramica',
          shape: 'box',
          size: [1.24, 0.06, 0.89],
          position: [0, 0.78, 0],
          color: '#f8fafc',
          texturePreset: 'ceramic_tile_white',
          roughness: 0.2,
          metalness: 0.05
        },
        {
          name: 'cabina_camara_trabajo',
          shape: 'box',
          size: [1.20, 1.25, 0.85],
          position: [0, 1.435, 0],
          color: '#f1f5f9',
          texturePreset: 'plastic_medical_white',
          roughness: 0.35,
          metalness: 0.1
        },
        {
          name: 'guillotina_cristal_deslizante',
          shape: 'box',
          size: [1.12, 0.70, 0.02],
          position: [0, 1.40, 0.42],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.5,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'modulo_extractor_centrifugo',
          shape: 'box',
          size: [1.16, 0.35, 0.80],
          position: [0, 2.235, 0],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'conducto_evacuacion_techo',
          shape: 'cylinder',
          size: [0.18, 0.18, 0.40, 12],
          position: [0, 2.50, 0],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'torreta_griferia_vacio_gas',
          shape: 'cylinder',
          size: [0.02, 0.02, 0.22, 6],
          position: [0.46, 0.92, -0.25],
          color: '#dd6b20',
          texturePreset: 'copper_polished',
          roughness: 0.25,
          metalness: 0.9
        },
        {
          name: 'interruptores_flujo_aire',
          shape: 'box',
          size: [0.22, 0.12, 0.03],
          position: [-0.46, 0.90, 0.435],
          color: '#1e293b',
          texturePreset: 'beige_plastic_worn',
          roughness: 0.5,
          metalness: 0.2
        }
      ]
    }
  },

  // -------------------------------------------------------------------------
  // 20. CALIBRADOR DE SONDAS NEURONALES
  // -------------------------------------------------------------------------
  {
    id: 'modular.sci_neural_probe_calibrator',
    family: 'sci_neural_probe_calibrator',
    name: 'Calibrador de Sondas Neuronales',
    batch: 3,
    batchName: 'Medicina, Laboratorio y Criogenia',
    category: 'medical',
    description: 'Banco de pruebas de alta precisión para implantes cerebrales y microelectrodos con cámara blindada y osciloscopio bioeléctrico.',
    tags: ['neural', 'sonda', 'implante', 'cerebro', 'calibrador', 'bioelectrico', 'microelectrodo'],
    dimensions: { width: 0.55, height: 0.42, depth: 0.45 },
    triBudget: '340-420',
    glbUrl: '/models/modular/sci_neural_probe_calibrator.glb',
    isModular: true,
    spec: {
      id: 'modular.sci_neural_probe_calibrator',
      name: 'Calibrador de Sondas Neuronales',
      category: 'medical',
      description: 'Banco de pruebas de alta precisión para implantes cerebrales y microelectrodos con cámara blindada y osciloscopio bioeléctrico.',
      units: 'meters',
      dimensions: { width: 0.55, height: 0.42, depth: 0.45 },
      palette: 'clean_lab',
      components: [
        {
          name: 'base_platina_micrometrica',
          shape: 'box',
          size: [0.55, 0.08, 0.45],
          position: [0, 0.04, 0],
          color: '#1e293b',
          texturePreset: 'iron_cast',
          roughness: 0.7,
          metalness: 0.8
        },
        {
          name: 'torre_actuador_nanoposicionador',
          shape: 'cylinder',
          size: [0.08, 0.08, 0.32, 10],
          position: [-0.15, 0.24, -0.05],
          color: '#475569',
          texturePreset: 'aluminum_anodized',
          roughness: 0.35,
          metalness: 0.8
        },
        {
          name: 'brazo_sujecion_sonda',
          shape: 'box',
          size: [0.18, 0.03, 0.03],
          position: [-0.06, 0.38, -0.05],
          color: '#e2e8f0',
          texturePreset: 'steel_polished',
          roughness: 0.2,
          metalness: 0.9
        },
        {
          name: 'microelectrodo_oro',
          shape: 'cylinder',
          size: [0.006, 0.006, 0.10, 6],
          position: [0.03, 0.32, -0.05],
          color: '#eab308',
          texturePreset: 'gold_clean',
          roughness: 0.2,
          metalness: 0.95
        },
        {
          name: 'placa_matriz_silicio',
          shape: 'box',
          size: [0.10, 0.02, 0.10],
          position: [0.03, 0.09, -0.05],
          color: '#16a34a',
          texturePreset: 'pcb_green_gold',
          roughness: 0.36,
          metalness: 0.45
        },
        {
          name: 'cupula_atmosfera_inerte',
          shape: 'sphere',
          size: [0.16, 12, 12],
          position: [0.03, 0.22, -0.05],
          color: '#38bdf8',
          texturePreset: 'clean_glass',
          opacity: 0.4,
          roughness: 0.1,
          metalness: 0.1
        },
        {
          name: 'modulo_osciloscopio_bio',
          shape: 'box',
          size: [0.24, 0.28, 0.22],
          position: [0.25, 0.22, 0.08],
          color: '#334155',
          texturePreset: 'plastic_abs_matte',
          roughness: 0.4,
          metalness: 0.2
        },
        {
          name: 'pantalla_potencial_accion',
          shape: 'box',
          size: [0.18, 0.14, 0.01],
          position: [0.25, 0.24, 0.195],
          color: '#a855f7',
          roughness: 0.1,
          metalness: 0.0
        }
      ]
    }
  }
];
