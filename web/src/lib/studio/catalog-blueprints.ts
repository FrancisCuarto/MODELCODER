import type { ModelSpec, ComponentDef } from './types.ts';

export type BlueprintFactory = (userParams?: Record<string, any>) => ModelSpec;

export class CatalogBlueprintRegistry {
  private static registry = new Map<string, BlueprintFactory>();

  public static register(family: string, factory: BlueprintFactory): void {
    this.registry.set(family, factory);
  }

  public static has(family: string): boolean {
    return this.registry.has(family);
  }

  public static get(family: string, userParams?: Record<string, any>): ModelSpec | null {
    const factory = this.registry.get(family);
    return factory ? factory(userParams) : null;
  }

  public static getRegisteredFamilies(): string[] {
    return Array.from(this.registry.keys());
  }
}

// ===========================================================================
// 1. ALARM SIREN & STROBE (Evacuation Beacon)
// ===========================================================================
CatalogBlueprintRegistry.register('alarm_siren', (params) => ({
  id: `remix.alarm_siren.${Date.now().toString(36)}`,
  name: 'Alarma Industrial y Luz Estroboscópica (Remix)',
  category: 'security',
  description: 'Alarma de evacuación modular con bocina acústica, cúpula Fresnel y jaula protectora.',
  units: 'meters',
  dimensions: { width: 0.22, height: 0.35, depth: 0.20 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'placa_mural',
      shape: 'box',
      size: [0.22, 0.24, 0.015],
      position: [0, 0.12, -0.0075],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'carcasa_principal',
      shape: 'box',
      size: [0.18, 0.20, 0.10],
      position: [0, 0.12, 0.05],
      color: '#ecc94b',
      texturePreset: 'hazard_stripes',
      roughness: 0.5,
      metalness: 0.2
    },
    {
      name: 'bocina_cuello',
      shape: 'cylinder',
      size: [0.036, 0.036, 0.05, 8],
      position: [0, 0.09, 0.125],
      rotation: [90, 0, 0],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.6,
      metalness: 0.6
    },
    {
      name: 'campana_bocina',
      shape: 'cylinder',
      size: [0.068, 0.036, 0.07, 8],
      position: [0, 0.09, 0.185],
      rotation: [90, 0, 0],
      color: '#e2e8f0',
      texturePreset: 'painted_metal_white',
      roughness: 0.4,
      metalness: 0.3
    },
    {
      name: 'tapon_acustico',
      shape: 'cylinder',
      size: [0.016, 0.016, 0.03, 6],
      position: [0, 0.09, 0.19],
      rotation: [90, 0, 0],
      color: '#a0aec0',
      texturePreset: 'metal_light_brushed',
      roughness: 0.3,
      metalness: 0.8
    },
    {
      name: 'anillo_reflector',
      shape: 'cylinder',
      size: [0.05, 0.05, 0.014, 8],
      position: [0, 0.227, 0.05],
      color: '#cbd5e0',
      texturePreset: 'chrome_mirror',
      roughness: 0.2,
      metalness: 0.9
    },
    {
      name: 'cupula_estroboscopica',
      shape: 'cylinder',
      size: [0.042, 0.042, 0.065, 8],
      position: [0, 0.265, 0.05],
      color: params?.strobe_color === 'amber' ? '#dd6b20' : (params?.strobe_color === 'blue' ? '#3182ce' : '#e53e3e'),
      emissive: params?.strobe_color === 'amber' ? '#dd6b20' : (params?.strobe_color === 'blue' ? '#3182ce' : '#e53e3e'),
      emissiveIntensity: 0.6,
      texturePreset: 'clean_glass',
      roughness: 0.1,
      metalness: 0.1
    },
    {
      name: 'aro_jaula_protectora',
      shape: 'cylinder',
      size: [0.057, 0.057, 0.008, 8],
      position: [0, 0.31, 0.05],
      color: '#4a5568',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.5
    },
    {
      name: 'varilla_jaula_izq',
      shape: 'box',
      size: [0.006, 0.08, 0.006],
      position: [-0.052, 0.27, 0.05],
      color: '#4a5568',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.5
    },
    {
      name: 'varilla_jaula_der',
      shape: 'box',
      size: [0.006, 0.08, 0.006],
      position: [0.052, 0.27, 0.05],
      color: '#4a5568',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.5
    },
    {
      name: 'conector_conduit',
      shape: 'cylinder',
      size: [0.014, 0.014, 0.03, 6],
      position: [0, 0.01, 0.05],
      color: '#718096',
      texturePreset: 'metal_dark_grime',
      roughness: 0.5,
      metalness: 0.7
    }
  ]
}));

// ===========================================================================
// 2. INDUSTRIAL DOOR & AIRLOCK (Security Bulkhead)
// ===========================================================================
CatalogBlueprintRegistry.register('door', (params) => {
  const fw = params?.width ?? 2.0;
  const fh = params?.height ?? 2.2;
  const fd = params?.frame_depth ?? 0.22;
  const thick = params?.frame_thickness ?? 0.14;
  const innerW = fw - (2.0 * thick);
  const leafW = (innerW / 2.0) + 0.03;
  const leafH = fh - thick;

  return {
    id: `remix.door.${Date.now().toString(36)}`,
    name: 'Puerta Industrial de Esclusa (Remix)',
    category: 'architecture',
    description: 'Puerta corrediza reforzada de seguridad con marco blindado, hojas dobles y teclado.',
    units: 'meters',
    dimensions: { width: fw, height: fh, depth: fd },
    palette: params?.palette || 'industrial_hazard',
    components: [
      {
        name: 'jamba_izquierda',
        shape: 'box',
        size: [thick, fh, fd],
        position: [-(fw / 2.0) + (thick / 2.0), fh / 2.0, 0],
        color: '#2d3748',
        texturePreset: 'steel_galvanized',
        roughness: 0.6,
        metalness: 0.6
      },
      {
        name: 'jamba_derecha',
        shape: 'box',
        size: [thick, fh, fd],
        position: [(fw / 2.0) - (thick / 2.0), fh / 2.0, 0],
        color: '#2d3748',
        texturePreset: 'steel_galvanized',
        roughness: 0.6,
        metalness: 0.6
      },
      {
        name: 'dintel_superior',
        shape: 'box',
        size: [fw, thick, fd * 1.08],
        position: [0, fh - (thick / 2.0), 0],
        color: '#d69e2e',
        texturePreset: 'hazard_stripes',
        roughness: 0.5,
        metalness: 0.3
      },
      {
        name: 'hoja_puerta_izq',
        shape: 'box',
        size: [leafW, leafH, fd * 0.24],
        position: [-(leafW / 2.0), leafH / 2.0, 0],
        color: '#4a5568',
        texturePreset: 'worn_metal',
        roughness: 0.7,
        metalness: 0.4
      },
      {
        name: 'hoja_puerta_der',
        shape: 'box',
        size: [leafW, leafH, fd * 0.24],
        position: [(leafW / 2.0), leafH / 2.0, 0],
        color: '#4a5568',
        texturePreset: 'worn_metal',
        roughness: 0.7,
        metalness: 0.4
      },
      {
        name: 'panel_blindaje_izq',
        shape: 'box',
        size: [leafW * 0.75, leafH * 0.45, 0.02],
        position: [-(leafW / 2.0), leafH * 0.55, 0.035],
        color: '#718096',
        texturePreset: 'diamond_plate',
        roughness: 0.4,
        metalness: 0.7
      },
      {
        name: 'panel_blindaje_der',
        shape: 'box',
        size: [leafW * 0.75, leafH * 0.45, 0.02],
        position: [(leafW / 2.0), leafH * 0.55, 0.035],
        color: '#718096',
        texturePreset: 'diamond_plate',
        roughness: 0.4,
        metalness: 0.7
      },
      {
        name: 'teclado_acceso',
        shape: 'box',
        size: [0.10, 0.22, 0.03],
        position: [(fw / 2.0) - (thick / 2.0), 1.25, fd * 0.52],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.8,
        metalness: 0.3
      },
      {
        name: 'indicador_led_verde',
        shape: 'box',
        size: [0.06, 0.02, 0.01],
        position: [(fw / 2.0) - (thick / 2.0), 1.38, fd * 0.536],
        color: '#38a169',
        emissive: '#38a169',
        emissiveIntensity: 0.8
      },
      {
        name: 'indicador_led_rojo',
        shape: 'box',
        size: [0.06, 0.02, 0.01],
        position: [(fw / 2.0) - (thick / 2.0), 1.34, fd * 0.536],
        color: '#e53e3e',
        emissive: '#e53e3e',
        emissiveIntensity: 0.8
      }
    ]
  };
});

// Alias for office_door and airlock_chamber
CatalogBlueprintRegistry.register('office_door', (params) => CatalogBlueprintRegistry.get('door', params)!);
CatalogBlueprintRegistry.register('service_lift_door', (params) => CatalogBlueprintRegistry.get('door', params)!);

// ===========================================================================
// 3. BUNK BED (Stacked Crew Stasis Pods)
// ===========================================================================
CatalogBlueprintRegistry.register('bunk_bed', (params) => {
  const w = params?.width ?? 0.98;
  const l = params?.length ?? 1.98;
  const h = params?.height ?? 1.90;
  const halfW = w * 0.5;
  const halfL = l * 0.5;

  return {
    id: `remix.bunk_bed.${Date.now().toString(36)}`,
    name: 'Litera Doble de Tripulación (Remix)',
    category: 'furniture',
    description: 'Litera modular apilada de dos niveles con bastidores metálicos, colchones y escalera.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: l },
    palette: params?.palette || 'industrial_hazard',
    components: [
      {
        name: 'poste_fl',
        shape: 'box',
        size: [0.07, h, 0.07],
        position: [-halfW + 0.035, h * 0.5, -halfL + 0.035],
        color: '#4a5568',
        texturePreset: 'steel_polished',
        roughness: 0.5,
        metalness: 0.7
      },
      {
        name: 'poste_fr',
        shape: 'box',
        size: [0.07, h, 0.07],
        position: [halfW - 0.035, h * 0.5, -halfL + 0.035],
        color: '#4a5568',
        texturePreset: 'steel_polished',
        roughness: 0.5,
        metalness: 0.7
      },
      {
        name: 'poste_bl',
        shape: 'box',
        size: [0.07, h, 0.07],
        position: [-halfW + 0.035, h * 0.5, halfL - 0.035],
        color: '#4a5568',
        texturePreset: 'steel_polished',
        roughness: 0.5,
        metalness: 0.7
      },
      {
        name: 'poste_br',
        shape: 'box',
        size: [0.07, h, 0.07],
        position: [halfW - 0.035, h * 0.5, halfL - 0.035],
        color: '#4a5568',
        texturePreset: 'steel_polished',
        roughness: 0.5,
        metalness: 0.7
      },
      {
        name: 'bastidor_inferior',
        shape: 'box',
        size: [w, 0.10, l],
        position: [0, 0.45, 0],
        color: '#2d3748',
        texturePreset: 'worn_metal',
        roughness: 0.6,
        metalness: 0.5
      },
      {
        name: 'colchon_inferior',
        shape: 'box',
        size: [w * 0.88, 0.16, l * 0.94],
        position: [0, 0.58, 0],
        color: '#edf2f7',
        texturePreset: 'quilted_padding_white',
        roughness: 0.8,
        metalness: 0.1
      },
      {
        name: 'manta_inferior',
        shape: 'box',
        size: [w * 0.90, 0.04, l * 0.65],
        position: [0, 0.68, -l * 0.14],
        color: '#2b6cb0',
        texturePreset: 'canvas_military',
        roughness: 0.9,
        metalness: 0.0
      },
      {
        name: 'almohada_inferior',
        shape: 'box',
        size: [w * 0.70, 0.08, 0.35],
        position: [0, 0.68, halfL - 0.30],
        color: '#ffffff',
        texturePreset: 'quilted_padding_white',
        roughness: 0.9,
        metalness: 0.0
      },
      {
        name: 'bastidor_superior',
        shape: 'box',
        size: [w, 0.10, l],
        position: [0, 1.45, 0],
        color: '#2d3748',
        texturePreset: 'worn_metal',
        roughness: 0.6,
        metalness: 0.5
      },
      {
        name: 'colchon_superior',
        shape: 'box',
        size: [w * 0.88, 0.16, l * 0.94],
        position: [0, 1.58, 0],
        color: '#edf2f7',
        texturePreset: 'quilted_padding_white',
        roughness: 0.8,
        metalness: 0.1
      },
      {
        name: 'manta_superior',
        shape: 'box',
        size: [w * 0.90, 0.04, l * 0.65],
        position: [0, 1.68, -l * 0.14],
        color: '#2b6cb0',
        texturePreset: 'canvas_military',
        roughness: 0.9,
        metalness: 0.0
      },
      {
        name: 'almohada_superior',
        shape: 'box',
        size: [w * 0.70, 0.08, 0.35],
        position: [0, 1.68, halfL - 0.30],
        color: '#ffffff',
        texturePreset: 'quilted_padding_white',
        roughness: 0.9,
        metalness: 0.0
      },
      {
        name: 'escalera_riel_izq',
        shape: 'cylinder',
        size: [0.02, 0.02, 1.50, 6],
        position: [-0.20, 0.85, -halfL - 0.04],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'escalera_riel_der',
        shape: 'cylinder',
        size: [0.02, 0.02, 1.50, 6],
        position: [0.20, 0.85, -halfL - 0.04],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'escalera_peldano_1',
        shape: 'cylinder',
        size: [0.015, 0.015, 0.38, 6],
        position: [0, 0.40, -halfL - 0.04],
        rotation: [0, 0, 90],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'escalera_peldano_2',
        shape: 'cylinder',
        size: [0.015, 0.015, 0.38, 6],
        position: [0, 0.75, -halfL - 0.04],
        rotation: [0, 0, 90],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'escalera_peldano_3',
        shape: 'cylinder',
        size: [0.015, 0.015, 0.38, 6],
        position: [0, 1.10, -halfL - 0.04],
        rotation: [0, 0, 90],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'escalera_peldano_4',
        shape: 'cylinder',
        size: [0.015, 0.015, 0.38, 6],
        position: [0, 1.45, -halfL - 0.04],
        rotation: [0, 0, 90],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'luz_lectura_inf',
        shape: 'box',
        size: [0.14, 0.04, 0.06],
        position: [-halfW + 0.06, 0.90, halfL - 0.30],
        color: '#ecc94b',
        emissive: '#ecc94b',
        emissiveIntensity: 0.7
      },
      {
        name: 'luz_lectura_sup',
        shape: 'box',
        size: [0.14, 0.04, 0.06],
        position: [-halfW + 0.06, 1.85, halfL - 0.30],
        color: '#ecc94b',
        emissive: '#ecc94b',
        emissiveIntensity: 0.7
      },
      {
        name: 'cajon_almacenaje_1',
        shape: 'box',
        size: [w * 0.46, 0.30, l * 0.46],
        position: [-w * 0.24, 0.18, 0],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.4
      },
      {
        name: 'cajon_almacenaje_2',
        shape: 'box',
        size: [w * 0.46, 0.30, l * 0.46],
        position: [w * 0.24, 0.18, 0],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.4
      }
    ]
  };
});

CatalogBlueprintRegistry.register('crew_bed', (params) => CatalogBlueprintRegistry.get('bunk_bed', params)!);
CatalogBlueprintRegistry.register('quarantine_bed', (params) => CatalogBlueprintRegistry.get('bunk_bed', params)!);

// ===========================================================================
// 4. ACCESS CARD LVL 1 (Security ID Pass)
// ===========================================================================
CatalogBlueprintRegistry.register('access_card_lvl1', (params) => {
  const w = params?.width ?? 0.085;
  const h = params?.height ?? 0.055;
  const t = params?.thickness ?? 0.004;

  return {
    id: `remix.access_card_lvl1.${Date.now().toString(36)}`,
    name: 'Tarjeta de Acceso Nivel 1 (Remix)',
    category: 'fixtures',
    description: 'Pase de identificación PSX con microchip de contacto, banda magnética y franja de seguridad.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: t },
    palette: params?.palette || 'industrial_hazard',
    components: [
      {
        name: 'cuerpo_tarjeta',
        shape: 'box',
        size: [w, h, t],
        position: [0, h * 0.5, 0],
        color: '#edf2f7',
        texturePreset: 'painted_metal_white',
        roughness: 0.3,
        metalness: 0.2
      },
      {
        name: 'franja_seguridad',
        shape: 'box',
        size: [w * 0.96, h * 0.32, t * 1.05],
        position: [0, h * 0.80, 0],
        color: '#d69e2e',
        texturePreset: 'caution_label',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'chip_dorado',
        shape: 'box',
        size: [0.015, 0.015, t * 1.15],
        position: [-w * 0.22, h * 0.42, 0],
        color: '#ecc94b',
        texturePreset: 'gold_contacts',
        roughness: 0.2,
        metalness: 0.95
      },
      {
        name: 'banda_magnetica',
        shape: 'box',
        size: [w, h * 0.22, t * 1.05],
        position: [0, h * 0.70, -t * 0.05],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.5,
        metalness: 0.6
      }
    ]
  };
});

// ===========================================================================
// 5. ACCESS CARD READER (Keypad Wall Terminal)
// ===========================================================================
CatalogBlueprintRegistry.register('access_card_reader', (params) => ({
  id: `remix.access_card_reader.${Date.now().toString(36)}`,
  name: 'Lector de Tarjetas y Teclado (Remix)',
  category: 'security',
  description: 'Terminal de control de accesos con ranura magnética, teclado numérico y barra LED.',
  units: 'meters',
  dimensions: { width: 0.16, height: 0.28, depth: 0.08 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'placa_fijacion',
      shape: 'box',
      size: [0.16, 0.28, 0.012],
      position: [0, 0.14, 0.006],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'cuerpo_terminal',
      shape: 'box',
      size: [0.14, 0.25, 0.06],
      position: [0, 0.14, 0.042],
      color: '#4a5568',
      texturePreset: 'beige_plastic_worn',
      roughness: 0.6,
      metalness: 0.2
    },
    {
      name: 'ranura_deslizamiento',
      shape: 'box',
      size: [0.008, 0.20, 0.04],
      position: [0.055, 0.14, 0.055],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.8,
      metalness: 0.3
    },
    {
      name: 'zona_rfid',
      shape: 'box',
      size: [0.09, 0.08, 0.01],
      position: [-0.015, 0.20, 0.075],
      color: '#276749',
      texturePreset: 'pcb_green_gold',
      roughness: 0.4,
      metalness: 0.6
    },
    {
      name: 'teclado_bloque',
      shape: 'box',
      size: [0.08, 0.09, 0.015],
      position: [-0.015, 0.09, 0.075],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.1
    },
    {
      name: 'barra_led_estado',
      shape: 'box',
      size: [0.10, 0.015, 0.01],
      position: [-0.015, 0.25, 0.075],
      color: '#38a169',
      emissive: '#38a169',
      emissiveIntensity: 0.8
    }
  ]
}));

// ===========================================================================
// 6. CRATE & CARGO CHEST
// ===========================================================================
CatalogBlueprintRegistry.register('crate', (params) => {
  const w = params?.width ?? 1.0;
  const h = params?.height ?? 0.85;
  const d = params?.depth ?? 1.0;
  const hw = w * 0.5;
  const hd = d * 0.5;

  return {
    id: `remix.crate.${Date.now().toString(36)}`,
    name: 'Caja de Carga Modular (Remix)',
    category: 'cargo',
    description: 'Contenedor de almacenamiento reforzado con esquineros metálicos y manijas.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: d },
    palette: params?.palette || 'industrial_hazard',
    components: [
      {
        name: 'cuerpo_contenedor',
        shape: 'box',
        size: [w, h, d],
        position: [0, h * 0.5, 0],
        color: '#4a5568',
        texturePreset: 'corrugated_metal',
        roughness: 0.7,
        metalness: 0.3
      },
      {
        name: 'reborde_tapa',
        shape: 'box',
        size: [w * 1.04, h * 0.14, d * 1.04],
        position: [0, h * 0.93, 0],
        color: '#d69e2e',
        texturePreset: 'hazard_stripes',
        roughness: 0.5,
        metalness: 0.2
      },
      {
        name: 'esquinero_fl',
        shape: 'box',
        size: [w * 0.14, h * 1.02, d * 0.14],
        position: [-hw + (w * 0.07), h * 0.51, -hd + (d * 0.07)],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.5
      },
      {
        name: 'esquinero_fr',
        shape: 'box',
        size: [w * 0.14, h * 1.02, d * 0.14],
        position: [hw - (w * 0.07), h * 0.51, -hd + (d * 0.07)],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.5
      },
      {
        name: 'esquinero_bl',
        shape: 'box',
        size: [w * 0.14, h * 1.02, d * 0.14],
        position: [-hw + (w * 0.07), h * 0.51, hd - (d * 0.07)],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.5
      },
      {
        name: 'esquinero_br',
        shape: 'box',
        size: [w * 0.14, h * 1.02, d * 0.14],
        position: [hw - (w * 0.07), h * 0.51, hd - (d * 0.07)],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.5
      },
      {
        name: 'manija_izq',
        shape: 'box',
        size: [0.04, 0.08, d * 0.24],
        position: [-hw - 0.02, h * 0.55, 0],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'manija_der',
        shape: 'box',
        size: [0.04, 0.08, d * 0.24],
        position: [hw + 0.02, h * 0.55, 0],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.8
      },
      {
        name: 'cierre_frontal',
        shape: 'box',
        size: [w * 0.12, 0.14, 0.03],
        position: [0, h * 0.85, hd + 0.015],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.9
      }
    ]
  };
});

CatalogBlueprintRegistry.register('chemical_drum', (params) => {
  const h = params?.height ?? 0.95;
  const r = (params?.width ?? 0.6) * 0.5;

  return {
    id: `remix.chemical_drum.${Date.now().toString(36)}`,
    name: 'Barril de Químicos (Remix)',
    category: 'cargo',
    description: 'Tambor cilíndrico de materiales peligrosos con aros de rodadura y tapón de venteo.',
    units: 'meters',
    dimensions: { width: r * 2, height: h, depth: r * 2 },
    palette: params?.palette || 'industrial_hazard',
    components: [
      {
        name: 'cuerpo_barril',
        shape: 'cylinder',
        size: [r, r, h, 8],
        position: [0, h * 0.5, 0],
        color: '#d69e2e',
        texturePreset: 'corrugated_metal',
        roughness: 0.6,
        metalness: 0.3
      },
      {
        name: 'aro_rodadura_inf',
        shape: 'cylinder',
        size: [r * 1.06, r * 1.06, 0.04, 8],
        position: [0, h * 0.30, 0],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.5
      },
      {
        name: 'aro_rodadura_sup',
        shape: 'cylinder',
        size: [r * 1.06, r * 1.06, 0.04, 8],
        position: [0, h * 0.70, 0],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.5
      },
      {
        name: 'tapon_roscado',
        shape: 'cylinder',
        size: [0.04, 0.04, 0.025, 6],
        position: [r * 0.45, h + 0.012, 0],
        color: '#718096',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      }
    ]
  };
});

// ===========================================================================
// 7. CARGO CONTAINER (Shipping Cargo Module)
// ===========================================================================
CatalogBlueprintRegistry.register('cargo_container', (params) => ({
  id: `remix.cargo_container.${Date.now().toString(36)}`,
  name: 'Contenedor Intermodal Blindado (Remix)',
  category: 'cargo',
  description: 'Módulo de transporte espacial con paredes corrugadas y puertas dobles de cierre hermético.',
  units: 'meters',
  dimensions: { width: 2.4, height: 2.4, depth: 5.8 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'chasis_contenedor',
      shape: 'box',
      size: [2.4, 2.4, 5.8],
      position: [0, 1.2, 0],
      color: '#2b6cb0',
      texturePreset: 'corrugated_metal',
      roughness: 0.7,
      metalness: 0.3
    },
    {
      name: 'marco_frontal',
      shape: 'box',
      size: [2.48, 2.48, 0.16],
      position: [0, 1.2, 2.85],
      color: '#1a202c',
      texturePreset: 'worn_metal',
      roughness: 0.6,
      metalness: 0.5
    },
    {
      name: 'marco_trasero',
      shape: 'box',
      size: [2.48, 2.48, 0.16],
      position: [0, 1.2, -2.85],
      color: '#1a202c',
      texturePreset: 'worn_metal',
      roughness: 0.6,
      metalness: 0.5
    },
    {
      name: 'puerta_izquierda',
      shape: 'box',
      size: [1.12, 2.30, 0.08],
      position: [-0.58, 1.2, 2.91],
      color: '#2c5282',
      texturePreset: 'worn_metal',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'puerta_derecha',
      shape: 'box',
      size: [1.12, 2.30, 0.08],
      position: [0.58, 1.2, 2.91],
      color: '#2c5282',
      texturePreset: 'worn_metal',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'barra_cierre_1',
      shape: 'cylinder',
      size: [0.025, 0.025, 2.35, 6],
      position: [-0.20, 1.2, 2.96],
      color: '#cbd5e0',
      texturePreset: 'metal_light_brushed',
      roughness: 0.4,
      metalness: 0.8
    },
    {
      name: 'barra_cierre_2',
      shape: 'cylinder',
      size: [0.025, 0.025, 2.35, 6],
      position: [0.20, 1.2, 2.96],
      color: '#cbd5e0',
      texturePreset: 'metal_light_brushed',
      roughness: 0.4,
      metalness: 0.8
    },
    {
      name: 'placa_peligro',
      shape: 'box',
      size: [0.60, 0.60, 0.02],
      position: [0.58, 1.6, 2.96],
      color: '#d69e2e',
      texturePreset: 'caution_label',
      roughness: 0.5,
      metalness: 0.2
    }
  ]
}));

// ===========================================================================
// 8. SECURITY CAMERA (CCTV Surveillance Mount)
// ===========================================================================
CatalogBlueprintRegistry.register('security_camera', (params) => ({
  id: `remix.security_camera.${Date.now().toString(36)}`,
  name: 'Cámara de Seguridad CCTV (Remix)',
  category: 'security',
  description: 'Unidad de vigilancia mural con óptica, sensor infrarrojo y cabezal articulado.',
  units: 'meters',
  dimensions: { width: 0.20, height: 0.25, depth: 0.45 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'soporte_mural',
      shape: 'box',
      size: [0.14, 0.14, 0.02],
      position: [0, 0.10, -0.15],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'brazo_articulado',
      shape: 'cylinder',
      size: [0.025, 0.025, 0.18, 6],
      position: [0, 0.10, -0.06],
      rotation: [90, 0, 0],
      color: '#718096',
      texturePreset: 'metal_light_brushed',
      roughness: 0.4,
      metalness: 0.8
    },
    {
      name: 'rotula_giro',
      shape: 'sphere',
      size: [0.045, 8, 6],
      position: [0, 0.10, 0.04],
      color: '#4a5568',
      texturePreset: 'metal_light_brushed',
      roughness: 0.5,
      metalness: 0.7
    },
    {
      name: 'cuerpo_camara',
      shape: 'cylinder',
      size: [0.065, 0.065, 0.26, 8],
      position: [0, 0.10, 0.18],
      rotation: [90, 0, 0],
      color: '#edf2f7',
      texturePreset: 'beige_plastic_worn',
      roughness: 0.4,
      metalness: 0.2
    },
    {
      name: 'visera_parasol',
      shape: 'box',
      size: [0.15, 0.02, 0.28],
      position: [0, 0.17, 0.18],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.6,
      metalness: 0.5
    },
    {
      name: 'lente_optico',
      shape: 'cylinder',
      size: [0.045, 0.045, 0.02, 8],
      position: [0, 0.10, 0.31],
      rotation: [90, 0, 0],
      color: '#1a202c',
      texturePreset: 'clean_glass',
      roughness: 0.1,
      metalness: 0.9
    },
    {
      name: 'led_infrarrojo_1',
      shape: 'sphere',
      size: [0.008, 6, 4],
      position: [0.035, 0.10, 0.312],
      color: '#e53e3e',
      emissive: '#e53e3e',
      emissiveIntensity: 0.9
    },
    {
      name: 'led_infrarrojo_2',
      shape: 'sphere',
      size: [0.008, 6, 4],
      position: [-0.035, 0.10, 0.312],
      color: '#e53e3e',
      emissive: '#e53e3e',
      emissiveIntensity: 0.9
    },
    {
      name: 'led_actividad',
      shape: 'box',
      size: [0.015, 0.015, 0.01],
      position: [0, 0.14, 0.31],
      color: '#38a169',
      emissive: '#38a169',
      emissiveIntensity: 0.9
    }
  ]
}));

// ===========================================================================
// 9. TERMINAL & WORKSTATION (CRT Command Desk)
// ===========================================================================
CatalogBlueprintRegistry.register('terminal', (params) => ({
  id: `remix.terminal.${Date.now().toString(36)}`,
  name: 'Terminal de Extracción de Datos (Remix)',
  category: 'command',
  description: 'Puesto informático retro con monitor CRT verde fósforo, teclado y bastidor de control.',
  units: 'meters',
  dimensions: { width: 1.20, height: 1.25, depth: 0.75 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'escritorio_base',
      shape: 'box',
      size: [1.20, 0.72, 0.70],
      position: [0, 0.36, 0],
      color: '#2d3748',
      texturePreset: 'worn_metal',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'pedestal_izquierdo',
      shape: 'box',
      size: [0.32, 0.68, 0.65],
      position: [-0.40, 0.34, 0],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.8,
      metalness: 0.4
    },
    {
      name: 'consola_pantalla',
      shape: 'box',
      size: [0.55, 0.42, 0.40],
      position: [0, 0.95, -0.05],
      color: '#cbd5e0',
      texturePreset: 'beige_plastic_worn',
      roughness: 0.5,
      metalness: 0.2
    },
    {
      name: 'pantalla_crt',
      shape: 'plane',
      size: [0.42, 0.32],
      position: [0, 0.95, 0.152],
      color: '#276749',
      texturePreset: 'crt_screen_green',
      emissive: '#38a169',
      emissiveIntensity: 0.7
    },
    {
      name: 'teclado',
      shape: 'wedge',
      size: [0.48, 0.05, 0.22],
      position: [0, 0.74, 0.22],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.1
    },
    {
      name: 'servidor_bastidor',
      shape: 'box',
      size: [0.26, 0.55, 0.60],
      position: [0.40, 0.34, 0],
      color: '#1a202c',
      texturePreset: 'vent_grill',
      roughness: 0.8,
      metalness: 0.5
    },
    {
      name: 'ranura_disquete',
      shape: 'box',
      size: [0.12, 0.02, 0.02],
      position: [0, 0.78, 0.16],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.9,
      metalness: 0.2
    }
  ]
}));

CatalogBlueprintRegistry.register('memory_extraction_terminal', (params) => CatalogBlueprintRegistry.get('terminal', params)!);
CatalogBlueprintRegistry.register('bridge_console_desk', (params) => CatalogBlueprintRegistry.get('terminal', params)!);
CatalogBlueprintRegistry.register('nav_console', (params) => CatalogBlueprintRegistry.get('terminal', params)!);

// ===========================================================================
// 10. LADDER (Vertical Service Stile)
// ===========================================================================
CatalogBlueprintRegistry.register('ladder', (params) => {
  const h = params?.height ?? 3.0;
  const w = params?.width ?? 0.50;
  const hw = w * 0.5;

  const comps: ComponentDef[] = [
    {
      name: 'montante_izquierdo',
      shape: 'cylinder',
      size: [0.025, 0.025, h, 6],
      position: [-hw, h * 0.5, 0],
      color: '#cbd5e0',
      texturePreset: 'steel_polished',
      roughness: 0.4,
      metalness: 0.8
    },
    {
      name: 'montante_derecho',
      shape: 'cylinder',
      size: [0.025, 0.025, h, 6],
      position: [hw, h * 0.5, 0],
      color: '#cbd5e0',
      texturePreset: 'steel_polished',
      roughness: 0.4,
      metalness: 0.8
    },
    {
      name: 'soporte_mural_inf',
      shape: 'box',
      size: [w + 0.10, 0.04, 0.18],
      position: [0, h * 0.20, -0.09],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.5
    },
    {
      name: 'soporte_mural_sup',
      shape: 'box',
      size: [w + 0.10, 0.04, 0.18],
      position: [0, h * 0.80, -0.09],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.5
    }
  ];

  // 8 rungs
  const rungCount = 8;
  for (let i = 1; i <= rungCount; i++) {
    const ry = (h / (rungCount + 1)) * i;
    comps.push({
      name: `peldano_${i}`,
      shape: 'cylinder',
      size: [0.016, 0.016, w - 0.04, 6],
      position: [0, ry, 0],
      rotation: [0, 0, 90],
      color: '#ecc94b',
      texturePreset: 'nonslip_floor',
      roughness: 0.5,
      metalness: 0.7
    });
  }

  return {
    id: `remix.ladder.${Date.now().toString(36)}`,
    name: 'Escalera de Servicio Vertical (Remix)',
    category: 'fixtures',
    description: 'Escalera mural con peldaños estriados antideslizantes y anclajes estructurales.',
    units: 'meters',
    dimensions: { width: w + 0.10, height: h, depth: 0.20 },
    palette: params?.palette || 'industrial_hazard',
    components: comps
  };
});

// ===========================================================================
// 11. LIGHT FIXTURE (Fluorescent Luminaire)
// ===========================================================================
CatalogBlueprintRegistry.register('light_fixture', (params) => ({
  id: `remix.light_fixture.${Date.now().toString(36)}`,
  name: 'Luminaria Fluorescente Industrial (Remix)',
  category: 'fixtures',
  description: 'Luminaria de techo con reflector esmaltado, tubos fluorescentes y rejilla de protección.',
  units: 'meters',
  dimensions: { width: 1.30, height: 0.12, depth: 0.24 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'carcasa_luminaria',
      shape: 'box',
      size: [1.30, 0.08, 0.22],
      position: [0, 0.04, 0],
      color: '#edf2f7',
      texturePreset: 'painted_metal_white',
      roughness: 0.4,
      metalness: 0.3
    },
    {
      name: 'reflector_interior',
      shape: 'box',
      size: [1.24, 0.03, 0.18],
      position: [0, 0.015, 0],
      color: '#ffffff',
      texturePreset: 'chrome_mirror',
      roughness: 0.1,
      metalness: 0.95
    },
    {
      name: 'tubo_fluorescente_1',
      shape: 'cylinder',
      size: [0.018, 0.018, 1.20, 8],
      position: [-0.045, -0.01, 0],
      rotation: [0, 0, 90],
      color: '#e2f5e8',
      emissive: '#e2f5e8',
      emissiveIntensity: 1.0
    },
    {
      name: 'tubo_fluorescente_2',
      shape: 'cylinder',
      size: [0.018, 0.018, 1.20, 8],
      position: [0.045, -0.01, 0],
      rotation: [0, 0, 90],
      color: '#e2f5e8',
      emissive: '#e2f5e8',
      emissiveIntensity: 1.0
    },
    {
      name: 'tapa_extremo_izq',
      shape: 'box',
      size: [0.04, 0.09, 0.23],
      position: [-0.64, 0.04, 0],
      color: '#4a5568',
      texturePreset: 'metal_dark_grime',
      roughness: 0.6,
      metalness: 0.5
    },
    {
      name: 'tapa_extremo_der',
      shape: 'box',
      size: [0.04, 0.09, 0.23],
      position: [0.64, 0.04, 0],
      color: '#4a5568',
      texturePreset: 'metal_dark_grime',
      roughness: 0.6,
      metalness: 0.5
    },
    {
      name: 'rejilla_protectora',
      shape: 'box',
      size: [1.22, 0.01, 0.19],
      position: [0, -0.035, 0],
      color: '#718096',
      texturePreset: 'vent_grill',
      roughness: 0.6,
      metalness: 0.7
    }
  ]
}));

// ===========================================================================
// 12. FIRE EXTINGUISHER
// ===========================================================================
CatalogBlueprintRegistry.register('fire_extinguisher', (params) => ({
  id: `remix.fire_extinguisher.${Date.now().toString(36)}`,
  name: 'Extintor de Incendios Presurizado (Remix)',
  category: 'fixtures',
  description: 'Extintor rojo de polvo químico presurizado con manómetro, palanca y boquilla.',
  units: 'meters',
  dimensions: { width: 0.22, height: 0.72, depth: 0.20 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'cuerpo_tanque',
      shape: 'cylinder',
      size: [0.09, 0.09, 0.45, 8],
      position: [0, 0.32, 0],
      color: '#e53e3e',
      texturePreset: 'red_paint_worn',
      roughness: 0.4,
      metalness: 0.3
    },
    {
      name: 'domo_superior',
      shape: 'sphere',
      size: [0.09, 8, 6],
      position: [0, 0.545, 0],
      color: '#e53e3e',
      texturePreset: 'red_paint_worn',
      roughness: 0.4,
      metalness: 0.3
    },
    {
      name: 'base_apoyo',
      shape: 'cylinder',
      size: [0.096, 0.096, 0.05, 8],
      position: [0, 0.025, 0],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.1
    },
    {
      name: 'valvula_laton',
      shape: 'cylinder',
      size: [0.022, 0.022, 0.06, 6],
      position: [0, 0.65, 0],
      color: '#d69e2e',
      texturePreset: 'brass_burnished',
      roughness: 0.3,
      metalness: 0.9
    },
    {
      name: 'palanca_accionador',
      shape: 'box',
      size: [0.03, 0.015, 0.16],
      position: [0, 0.68, 0.05],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.6,
      metalness: 0.6
    },
    {
      name: 'manometro_presion',
      shape: 'cylinder',
      size: [0.022, 0.022, 0.015, 6],
      position: [0.03, 0.64, 0],
      rotation: [0, 0, 90],
      color: '#ffffff',
      texturePreset: 'clean_glass',
      roughness: 0.2,
      metalness: 0.8
    },
    {
      name: 'manguera_goma',
      shape: 'cylinder',
      size: [0.014, 0.014, 0.38, 6],
      position: [0.08, 0.40, 0.06],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.9,
      metalness: 0.1
    },
    {
      name: 'boquilla_difusora',
      shape: 'cone',
      size: [0.026, 0.08, 6],
      position: [0.08, 0.18, 0.06],
      rotation: [180, 0, 0],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.9,
      metalness: 0.1
    },
    {
      name: 'etiqueta_instrucciones',
      shape: 'box',
      size: [0.12, 0.18, 0.01],
      position: [0, 0.35, 0.092],
      color: '#edf2f7',
      texturePreset: 'caution_label',
      roughness: 0.4,
      metalness: 0.2
    }
  ]
}));

// ===========================================================================
// 13. LOCKER (Crew Equipment Cabinet)
// ===========================================================================
CatalogBlueprintRegistry.register('locker', (params) => ({
  id: `remix.locker.${Date.now().toString(36)}`,
  name: 'Casillero Metálico de Estación (Remix)',
  category: 'furniture',
  description: 'Taquilla de almacenamiento con puertas ventiladas, dial numérico y zócalo.',
  units: 'meters',
  dimensions: { width: 0.45, height: 1.85, depth: 0.50 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'gabinete_estructura',
      shape: 'box',
      size: [0.45, 1.85, 0.50],
      position: [0, 0.925, 0],
      color: '#4a5568',
      texturePreset: 'worn_metal',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'zocalo_base',
      shape: 'box',
      size: [0.44, 0.10, 0.48],
      position: [0, 0.05, 0],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.8,
      metalness: 0.4
    },
    {
      name: 'puerta_taquilla',
      shape: 'box',
      size: [0.41, 1.68, 0.02],
      position: [0, 0.95, 0.255],
      color: '#3182ce',
      texturePreset: 'painted_metal_blue',
      roughness: 0.6,
      metalness: 0.3
    },
    {
      name: 'rejilla_ventilacion_sup',
      shape: 'box',
      size: [0.26, 0.14, 0.005],
      position: [0, 1.65, 0.266],
      color: '#1a202c',
      texturePreset: 'vent_grill',
      roughness: 0.8,
      metalness: 0.5
    },
    {
      name: 'rejilla_ventilacion_inf',
      shape: 'box',
      size: [0.26, 0.14, 0.005],
      position: [0, 0.30, 0.266],
      color: '#1a202c',
      texturePreset: 'vent_grill',
      roughness: 0.8,
      metalness: 0.5
    },
    {
      name: 'manija_embutida',
      shape: 'box',
      size: [0.04, 0.14, 0.025],
      position: [0.15, 0.95, 0.26],
      color: '#cbd5e0',
      texturePreset: 'metal_light_brushed',
      roughness: 0.4,
      metalness: 0.8
    },
    {
      name: 'dial_combinacion',
      shape: 'cylinder',
      size: [0.025, 0.025, 0.015, 6],
      position: [0.15, 1.06, 0.27],
      rotation: [90, 0, 0],
      color: '#edf2f7',
      texturePreset: 'chrome_mirror',
      roughness: 0.2,
      metalness: 0.9
    },
    {
      name: 'placa_identificacion',
      shape: 'box',
      size: [0.10, 0.04, 0.004],
      position: [0, 1.45, 0.266],
      color: '#ecc94b',
      texturePreset: 'metal_light_brushed',
      roughness: 0.3,
      metalness: 0.8
    }
  ]
}));

// ===========================================================================
// 14. OFFICE CHAIR (Ergonomic Desk Swivel Chair)
// ===========================================================================
CatalogBlueprintRegistry.register('office_chair', (params) => ({
  id: `remix.office_chair.${Date.now().toString(36)}`,
  name: 'Silla Giratoria de Oficina (Remix)',
  category: 'furniture',
  description: 'Silla ergonómica de control con base rodante de 5 radios, asiento acolchado y apoyabrazos.',
  units: 'meters',
  dimensions: { width: 0.65, height: 1.05, depth: 0.65 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'estrella_base',
      shape: 'box',
      size: [0.65, 0.06, 0.65],
      position: [0, 0.06, 0],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.2
    },
    {
      name: 'columna_piston',
      shape: 'cylinder',
      size: [0.035, 0.035, 0.32, 6],
      position: [0, 0.22, 0],
      color: '#cbd5e0',
      texturePreset: 'chrome_mirror',
      roughness: 0.2,
      metalness: 0.95
    },
    {
      name: 'asiento_cojin',
      shape: 'box',
      size: [0.48, 0.08, 0.46],
      position: [0, 0.42, 0],
      color: '#2d3748',
      texturePreset: 'leather_black_worn',
      roughness: 0.7,
      metalness: 0.1
    },
    {
      name: 'respaldo',
      shape: 'box',
      size: [0.44, 0.52, 0.06],
      position: [0, 0.72, -0.21],
      color: '#2d3748',
      texturePreset: 'leather_black_worn',
      roughness: 0.7,
      metalness: 0.1
    },
    {
      name: 'soporte_respaldo',
      shape: 'box',
      size: [0.08, 0.30, 0.04],
      position: [0, 0.52, -0.22],
      color: '#1a202c',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.6
    },
    {
      name: 'apoyabrazos_izq',
      shape: 'box',
      size: [0.06, 0.22, 0.28],
      position: [-0.26, 0.54, 0],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.2
    },
    {
      name: 'apoyabrazos_der',
      shape: 'box',
      size: [0.06, 0.22, 0.28],
      position: [0.26, 0.54, 0],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.2
    }
  ]
}));

// ===========================================================================
// 15. OFFICE DESK (Workstation Desk)
// ===========================================================================
CatalogBlueprintRegistry.register('office_desk', (params) => ({
  id: `remix.office_desk.${Date.now().toString(36)}`,
  name: 'Escritorio de Oficina y Puesto Técnico (Remix)',
  category: 'furniture',
  description: 'Mesa de trabajo con tablero de madera, cajonera metálica y pasacables.',
  units: 'meters',
  dimensions: { width: 1.40, height: 0.75, depth: 0.75 },
  palette: params?.palette || 'industrial_hazard',
  components: [
    {
      name: 'tablero_escritorio',
      shape: 'box',
      size: [1.40, 0.06, 0.75],
      position: [0, 0.72, 0],
      color: '#7b341e',
      texturePreset: 'wood_oak',
      roughness: 0.6,
      metalness: 0.1
    },
    {
      name: 'cajonera_pedestal',
      shape: 'box',
      size: [0.38, 0.68, 0.68],
      position: [-0.45, 0.35, 0],
      color: '#4a5568',
      texturePreset: 'worn_metal',
      roughness: 0.6,
      metalness: 0.4
    },
    {
      name: 'frente_cajon_1',
      shape: 'box',
      size: [0.34, 0.18, 0.02],
      position: [-0.45, 0.58, 0.35],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'frente_cajon_2',
      shape: 'box',
      size: [0.34, 0.18, 0.02],
      position: [-0.45, 0.38, 0.35],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'frente_cajon_3',
      shape: 'box',
      size: [0.34, 0.18, 0.02],
      position: [-0.45, 0.18, 0.35],
      color: '#2d3748',
      texturePreset: 'metal_dark_grime',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'pata_lateral_der',
      shape: 'box',
      size: [0.06, 0.68, 0.68],
      position: [0.62, 0.35, 0],
      color: '#2d3748',
      texturePreset: 'steel_polished',
      roughness: 0.5,
      metalness: 0.7
    },
    {
      name: 'panel_modestia',
      shape: 'box',
      size: [1.20, 0.40, 0.02],
      position: [0.10, 0.48, -0.32],
      color: '#2d3748',
      texturePreset: 'worn_metal',
      roughness: 0.7,
      metalness: 0.4
    },
    {
      name: 'pasacables',
      shape: 'cylinder',
      size: [0.03, 0.03, 0.065, 6],
      position: [0.55, 0.72, -0.25],
      color: '#1a202c',
      texturePreset: 'rubber_black',
      roughness: 0.8,
      metalness: 0.1
    }
  ]
}));

CatalogBlueprintRegistry.register('work_bench', (params) => CatalogBlueprintRegistry.get('office_desk', params)!);
CatalogBlueprintRegistry.register('lab_workstation', (params) => CatalogBlueprintRegistry.get('office_desk', params)!);

// ===========================================================================
// 16. SERVER RACK & CONSCIOUSNESS ARCHIVE
// ===========================================================================
CatalogBlueprintRegistry.register('server_rack', (params) => {
  const p = params || {};
  const w = p.width || 0.85;
  const h = p.height || 2.10;
  const d = p.depth || 0.90;

  return {
    id: `remix.server_rack.${Date.now().toString(36)}`,
    name: 'Bastidor de Servidores y Archivo Central (Remix)',
    category: 'electronics',
    description: 'Armario de servidores industrial 42U con módulos de cómputo en rack, bahía de discos y consola de mantenimiento retráctil.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: d },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'gabinete_exterior',
        shape: 'box',
        size: [w, h, d],
        position: [0, h / 2, 0],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.6
      },
      {
        name: 'zocalo_base',
        shape: 'box',
        size: [w * 1.04, 0.08, d * 1.04],
        position: [0, 0.04, 0],
        color: '#171923',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'rejilla_ventilacion_techo',
        shape: 'box',
        size: [w * 0.75, 0.02, d * 0.75],
        position: [0, h + 0.01, 0],
        color: '#2d3748',
        texturePreset: 'metal_grate',
        roughness: 0.6,
        metalness: 0.5
      },
      {
        name: 'unidad_servidor_1',
        shape: 'box',
        size: [w * 0.86, 0.22, 0.04],
        position: [0, h * 0.82, d / 2 + 0.01],
        color: '#2d3748',
        texturePreset: 'scifi_panel_vent',
        roughness: 0.5,
        metalness: 0.4
      },
      {
        name: 'unidad_servidor_2',
        shape: 'box',
        size: [w * 0.86, 0.22, 0.04],
        position: [0, h * 0.68, d / 2 + 0.01],
        color: '#2d3748',
        texturePreset: 'scifi_panel_vent',
        roughness: 0.5,
        metalness: 0.4
      },
      {
        name: 'consola_terminal_servicio',
        shape: 'box',
        size: [w * 0.86, 0.16, 0.14],
        position: [0, h * 0.52, d / 2 + 0.06],
        color: '#4a5568',
        texturePreset: 'scifi_trim_dark',
        roughness: 0.4,
        metalness: 0.5
      },
      {
        name: 'pantalla_crt_terminal',
        shape: 'box',
        size: [0.24, 0.11, 0.02],
        position: [-0.18, h * 0.52, d / 2 + 0.135],
        color: '#48bb78',
        texturePreset: 'crt_display_phosphor',
        roughness: 0.1,
        metalness: 0.1,
        emissive: '#48bb78',
        emissiveIntensity: 0.9
      },
      {
        name: 'teclado_terminal',
        shape: 'wedge',
        size: [0.32, 0.02, 0.10],
        position: [0.15, h * 0.47, d / 2 + 0.12],
        rotation: [15, 0, 0],
        color: '#cbd5e0',
        texturePreset: 'plastic_rugged',
        roughness: 0.5,
        metalness: 0.2
      },
      {
        name: 'bahia_almacenamiento_san',
        shape: 'box',
        size: [w * 0.86, 0.28, 0.04],
        position: [0, h * 0.34, d / 2 + 0.01],
        color: '#2d3748',
        texturePreset: 'scifi_panel_circuit',
        roughness: 0.5,
        metalness: 0.5
      },
      {
        name: 'matriz_discos_nvme',
        shape: 'box',
        size: [w * 0.86, 0.22, 0.04],
        position: [0, h * 0.18, d / 2 + 0.01],
        color: '#2d3748',
        texturePreset: 'metal_grate',
        roughness: 0.6,
        metalness: 0.4
      },
      {
        name: 'barra_led_actividad',
        shape: 'box',
        size: [0.03, h * 0.85, 0.01],
        position: [w * 0.41, h / 2, d / 2 + 0.015],
        color: '#38a169',
        roughness: 0.2,
        metalness: 0.2,
        emissive: '#38a169',
        emissiveIntensity: 0.8
      }
    ]
  };
});

CatalogBlueprintRegistry.register('consciousness_archive', (params) => CatalogBlueprintRegistry.get('server_rack', params)!);

// ===========================================================================
// 17. BATTERY BANK & POWER ACCUMULATOR
// ===========================================================================
CatalogBlueprintRegistry.register('battery_bank', (params) => {
  const p = params || {};
  const w = p.width || 1.10;
  const h = p.height || 1.30;
  const d = p.depth || 0.70;

  return {
    id: `remix.battery_bank.${Date.now().toString(36)}`,
    name: 'Banco de Baterías de Reserva (Remix)',
    category: 'power',
    description: 'Sistema acumulador de energía industrial con 4 celdas electroquímicas de alto voltaje, barras colectoras de cobre y manómetro de tensión.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: d },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'chasis_portante_acero',
        shape: 'box',
        size: [w, 0.12, d],
        position: [0, 0.06, 0],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.6
      },
      {
        name: 'bastidor_posterior',
        shape: 'box',
        size: [w, h, 0.08],
        position: [0, h / 2, -d / 2 + 0.04],
        color: '#1a202c',
        texturePreset: 'metal_dark_grime',
        roughness: 0.8,
        metalness: 0.5
      },
      {
        name: 'celda_potencia_1',
        shape: 'cylinder',
        size: [0.11, 0.11, 0.75, 8],
        position: [-0.36, 0.52, 0.05],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'celda_potencia_2',
        shape: 'cylinder',
        size: [0.11, 0.11, 0.75, 8],
        position: [-0.12, 0.52, 0.05],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'celda_potencia_3',
        shape: 'cylinder',
        size: [0.11, 0.11, 0.75, 8],
        position: [0.12, 0.52, 0.05],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'celda_potencia_4',
        shape: 'cylinder',
        size: [0.11, 0.11, 0.75, 8],
        position: [0.36, 0.52, 0.05],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'barra_colectora_positiva',
        shape: 'box',
        size: [w * 0.88, 0.03, 0.04],
        position: [0, 0.92, -0.04],
        color: '#dd6b20',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.9
      },
      {
        name: 'barra_colectora_negativa',
        shape: 'box',
        size: [w * 0.88, 0.03, 0.04],
        position: [0, 0.92, 0.14],
        color: '#4a5568',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      },
      {
        name: 'voltimetro_analogico',
        shape: 'cylinder',
        size: [0.08, 0.08, 0.05, 8],
        position: [0, 1.12, -d / 2 + 0.11],
        rotation: [90, 0, 0],
        color: '#e2e8f0',
        texturePreset: 'gauge_radial_fuel',
        roughness: 0.3,
        metalness: 0.4
      },
      {
        name: 'placa_advertencia_alta_tension',
        shape: 'box',
        size: [0.30, 0.14, 0.01],
        position: [0, 0.22, d / 2 + 0.005],
        color: '#d69e2e',
        texturePreset: 'caution_label',
        roughness: 0.5,
        metalness: 0.2
      }
    ]
  };
});

CatalogBlueprintRegistry.register('power_transformer', (params) => CatalogBlueprintRegistry.get('battery_bank', params)!);

// ===========================================================================
// 18. BIOHAZARD BIN & CLINICAL STEP CAN
// ===========================================================================
CatalogBlueprintRegistry.register('biohazard_bin', (params) => {
  const p = params || {};
  const diameter = p.bin_diameter || 0.45;
  const height = p.bin_height || 0.72;
  const radius = diameter / 2;

  return {
    id: `remix.biohazard_bin.${Date.now().toString(36)}`,
    name: 'Contenedor de Residuos Biológicos (Remix)',
    category: 'medical',
    description: 'Cubo sanitario estanco de accionamiento a pedal con cuerpo octogonal reforzado, bolsa biológica visible y tapa batiente.',
    units: 'meters',
    dimensions: { width: diameter, height, depth: diameter },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'collar_base_antideslizante',
        shape: 'cylinder',
        size: [radius * 1.08, radius * 1.08, 0.05, 8],
        position: [0, 0.025, 0],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'cuerpo_canister_rojo',
        shape: 'cylinder',
        size: [radius, radius, height * 0.78, 8],
        position: [0, 0.05 + (height * 0.78) / 2, 0],
        color: '#e53e3e',
        texturePreset: 'painted_metal_red',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'reborde_bolsa_bioseguridad',
        shape: 'cylinder',
        size: [radius * 1.04, radius * 1.04, 0.04, 8],
        position: [0, 0.05 + height * 0.78, 0],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.6,
        metalness: 0.1
      },
      {
        name: 'tapa_estanca',
        shape: 'cylinder',
        size: [radius * 1.05, radius * 1.05, 0.035, 8],
        position: [0, height * 0.94, 0],
        color: '#c53030',
        texturePreset: 'painted_metal_red',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'asa_tirador_tapa',
        shape: 'box',
        size: [0.12, 0.02, 0.04],
        position: [0, height * 0.97, radius * 0.6],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.6,
        metalness: 0.7
      },
      {
        name: 'pedal_accionamiento',
        shape: 'box',
        size: [0.12, 0.015, 0.08],
        position: [0, 0.025, radius + 0.04],
        color: '#a0aec0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      },
      {
        name: 'varilla_transmision_pedal',
        shape: 'cylinder',
        size: [0.01, 0.01, height * 0.75, 6],
        position: [0, 0.05 + (height * 0.75) / 2, -radius - 0.015],
        color: '#4a5568',
        texturePreset: 'metal_dark_grime',
        roughness: 0.5,
        metalness: 0.8
      },
      {
        name: 'asa_lateral_izquierda',
        shape: 'box',
        size: [0.03, 0.08, 0.03],
        position: [-radius - 0.015, height * 0.55, 0],
        color: '#2d3748',
        texturePreset: 'rubber_black',
        roughness: 0.7,
        metalness: 0.3
      },
      {
        name: 'asa_lateral_derecha',
        shape: 'box',
        size: [0.03, 0.08, 0.03],
        position: [radius + 0.015, height * 0.55, 0],
        color: '#2d3748',
        texturePreset: 'rubber_black',
        roughness: 0.7,
        metalness: 0.3
      },
      {
        name: 'placa_simbolo_biohazard',
        shape: 'box',
        size: [0.16, 0.16, 0.005],
        position: [0, height * 0.48, radius + 0.003],
        color: '#ecc94b',
        texturePreset: 'caution_label',
        roughness: 0.5,
        metalness: 0.2
      }
    ]
  };
});

// ===========================================================================
// 19. AIRLOCK CHAMBER & BULKHEAD VAULT
// ===========================================================================
CatalogBlueprintRegistry.register('airlock_chamber', (params) => {
  const p = params || {};
  const l = p.chamber_length || 2.40;
  const w = p.chamber_width || 2.20;
  const h = p.chamber_height || 2.50;

  return {
    id: `remix.airlock_chamber.${Date.now().toString(36)}`,
    name: 'Cámara de Esclusa de Descompresión (Remix)',
    category: 'structures',
    description: 'Módulo de transición presurizado con compuertas dobles de mamparo, piso de rejilla de drenaje de vacío y conductos de descompresión.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: l },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'plataforma_suelo_estructural',
        shape: 'box',
        size: [w, 0.12, l],
        position: [0, 0.06, 0],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.6
      },
      {
        name: 'rejilla_suelo_transitable',
        shape: 'box',
        size: [w * 0.65, 0.02, l * 0.88],
        position: [0, 0.13, 0],
        color: '#1a202c',
        texturePreset: 'metal_grate',
        roughness: 0.6,
        metalness: 0.5
      },
      {
        name: 'techo_camara',
        shape: 'box',
        size: [w, 0.12, l],
        position: [0, h - 0.06, 0],
        color: '#2d3748',
        texturePreset: 'scifi_hull_plates',
        roughness: 0.6,
        metalness: 0.5
      },
      {
        name: 'pared_lateral_izquierda',
        shape: 'box',
        size: [0.15, h - 0.24, l],
        position: [-w / 2 + 0.075, h / 2, 0],
        color: '#4a5568',
        texturePreset: 'scifi_hull_plates',
        roughness: 0.5,
        metalness: 0.4
      },
      {
        name: 'pared_lateral_derecha',
        shape: 'box',
        size: [0.15, h - 0.24, l],
        position: [w / 2 - 0.075, h / 2, 0],
        color: '#4a5568',
        texturePreset: 'scifi_hull_plates',
        roughness: 0.5,
        metalness: 0.4
      },
      {
        name: 'marco_mamparo_frontal',
        shape: 'box',
        size: [w, h, 0.18],
        position: [0, h / 2, l / 2 - 0.09],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.5,
        metalness: 0.3
      },
      {
        name: 'hoja_puerta_izquierda',
        shape: 'box',
        size: [w * 0.38, h * 0.76, 0.08],
        position: [-w * 0.20, h * 0.46, l / 2 - 0.09],
        color: '#2b6cb0',
        texturePreset: 'painted_metal_blue',
        roughness: 0.4,
        metalness: 0.5
      },
      {
        name: 'hoja_puerta_derecha',
        shape: 'box',
        size: [w * 0.38, h * 0.76, 0.08],
        position: [w * 0.20, h * 0.46, l / 2 - 0.09],
        color: '#2b6cb0',
        texturePreset: 'painted_metal_blue',
        roughness: 0.4,
        metalness: 0.5
      },
      {
        name: 'pasamanos_seguridad_eva',
        shape: 'cylinder',
        size: [0.02, 0.02, l * 0.75, 6],
        position: [-w / 2 + 0.20, 1.05, 0],
        rotation: [90, 0, 0],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.4,
        metalness: 0.7
      },
      {
        name: 'panel_control_presion',
        shape: 'box',
        size: [0.18, 0.28, 0.05],
        position: [w / 2 - 0.16, 1.35, 0],
        color: '#1a202c',
        texturePreset: 'crt_display_green',
        roughness: 0.3,
        metalness: 0.5,
        emissive: '#48bb78',
        emissiveIntensity: 0.6
      }
    ]
  };
});

CatalogBlueprintRegistry.register('decon_chamber', (params) => CatalogBlueprintRegistry.get('airlock_chamber', params)!);
CatalogBlueprintRegistry.register('station_corridor', (params) => CatalogBlueprintRegistry.get('airlock_chamber', params)!);
CatalogBlueprintRegistry.register('station_room', (params) => CatalogBlueprintRegistry.get('airlock_chamber', params)!);

// ===========================================================================
// 20. TRASH BIN & WASTE RECEPTACLE
// ===========================================================================
CatalogBlueprintRegistry.register('trash_bin', (params) => {
  const p = params || {};
  const diameter = p.diameter || 0.40;
  const height = p.height || 0.70;
  const radius = diameter / 2;

  return {
    id: `remix.trash_bin.${Date.now().toString(36)}`,
    name: 'Papelera y Contenedor de Residuos (Remix)',
    category: 'props',
    description: 'Contenedor cilíndrico estandarizado con reborde protector y tapa basculante de resorte.',
    units: 'meters',
    dimensions: { width: diameter, height, depth: diameter },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'base_goma',
        shape: 'cylinder',
        size: [radius * 1.05, radius * 1.05, 0.04, 8],
        position: [0, 0.02, 0],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'cuerpo_cilindrico',
        shape: 'cylinder',
        size: [radius, radius, height * 0.82, 8],
        position: [0, 0.04 + (height * 0.82) / 2, 0],
        color: '#4a5568',
        texturePreset: 'metal_dark_grime',
        roughness: 0.6,
        metalness: 0.5
      },
      {
        name: 'anillo_superior',
        shape: 'cylinder',
        size: [radius * 1.04, radius * 1.04, 0.04, 8],
        position: [0, 0.04 + height * 0.82, 0],
        color: '#718096',
        texturePreset: 'metal_light_brushed',
        roughness: 0.4,
        metalness: 0.7
      },
      {
        name: 'tapa_basculante',
        shape: 'cylinder',
        size: [radius * 0.92, radius * 0.92, 0.02, 8],
        position: [0, height * 0.88, 0],
        rotation: [15, 0, 0],
        color: '#2d3748',
        texturePreset: 'plastic_rugged',
        roughness: 0.5,
        metalness: 0.3
      }
    ]
  };
});

// ===========================================================================
// 21. CRASH CART & MEDICAL EMERGENCY TROLLEY
// ===========================================================================
CatalogBlueprintRegistry.register('crash_cart', (params) => {
  const p = params || {};
  const w = p.width || 0.75;
  const h = p.height || 1.15;
  const d = p.depth || 0.55;

  return {
    id: `remix.crash_cart.${Date.now().toString(36)}`,
    name: 'Carro de Emergencias y Paro Cardíaco (Remix)',
    category: 'medical',
    description: 'Carro sanitario móvil rodante con 4 cajoneras con cerradura, soporte de suero IV, desfibrilador y monitor ECG.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: d },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'base_chasis',
        shape: 'box',
        size: [w, 0.06, d],
        position: [0, 0.10, 0],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.6,
        metalness: 0.6
      },
      {
        name: 'rueda_frontal_izq',
        shape: 'cylinder',
        size: [0.04, 0.04, 0.03, 6],
        position: [-w / 2 + 0.06, 0.05, d / 2 - 0.06],
        rotation: [0, 0, 90],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'rueda_frontal_der',
        shape: 'cylinder',
        size: [0.04, 0.04, 0.03, 6],
        position: [w / 2 - 0.06, 0.05, d / 2 - 0.06],
        rotation: [0, 0, 90],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'rueda_trasera_izq',
        shape: 'cylinder',
        size: [0.04, 0.04, 0.03, 6],
        position: [-w / 2 + 0.06, 0.05, -d / 2 + 0.06],
        rotation: [0, 0, 90],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'rueda_trasera_der',
        shape: 'cylinder',
        size: [0.04, 0.04, 0.03, 6],
        position: [w / 2 - 0.06, 0.05, -d / 2 + 0.06],
        rotation: [0, 0, 90],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.8,
        metalness: 0.2
      },
      {
        name: 'bloque_cajoneras',
        shape: 'box',
        size: [w * 0.90, h * 0.68, d * 0.90],
        position: [0, 0.13 + (h * 0.68) / 2, 0],
        color: '#e53e3e',
        texturePreset: 'painted_metal_red',
        roughness: 0.4,
        metalness: 0.4
      },
      {
        name: 'encimera_quirurgica',
        shape: 'box',
        size: [w, 0.04, d],
        position: [0, 0.13 + h * 0.68 + 0.02, 0],
        color: '#e2e8f0',
        texturePreset: 'chrome_mirror',
        roughness: 0.2,
        metalness: 0.9
      },
      {
        name: 'barra_manillar_empuje',
        shape: 'cylinder',
        size: [0.016, 0.016, d * 0.75, 6],
        position: [-w / 2 - 0.04, 0.13 + h * 0.68, 0],
        rotation: [90, 0, 0],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.9
      },
      {
        name: 'poste_portasueros_iv',
        shape: 'cylinder',
        size: [0.012, 0.012, 0.65, 6],
        position: [w / 2 - 0.06, 0.13 + h * 0.68 + 0.32, -d / 2 + 0.06],
        color: '#e2e8f0',
        texturePreset: 'chrome_mirror',
        roughness: 0.2,
        metalness: 0.9
      },
      {
        name: 'monitor_desfibrilador',
        shape: 'box',
        size: [0.26, 0.20, 0.18],
        position: [0.05, 0.13 + h * 0.68 + 0.12, 0],
        color: '#2d3748',
        texturePreset: 'scifi_trim_dark',
        roughness: 0.5,
        metalness: 0.3
      },
      {
        name: 'pantalla_ecg',
        shape: 'box',
        size: [0.18, 0.12, 0.01],
        position: [0.05, 0.13 + h * 0.68 + 0.13, 0.095],
        color: '#38a169',
        texturePreset: 'crt_display_green',
        roughness: 0.2,
        metalness: 0.1,
        emissive: '#38a169',
        emissiveIntensity: 0.9
      }
    ]
  };
});

CatalogBlueprintRegistry.register('autopsy_table', (params) => CatalogBlueprintRegistry.get('crash_cart', params)!);
CatalogBlueprintRegistry.register('morgue_gurney', (params) => CatalogBlueprintRegistry.get('crash_cart', params)!);
CatalogBlueprintRegistry.register('tool_chest_cart', (params) => CatalogBlueprintRegistry.get('crash_cart', params)!);

// ===========================================================================
// 22. SIGN PLACARD & INDUSTRIAL WARNING SIGN
// ===========================================================================
CatalogBlueprintRegistry.register('sign_placard', (params) => {
  const p = params || {};
  const w = p.width || 0.45;
  const h = p.height || 0.30;
  const t = 0.015;

  return {
    id: `remix.sign_placard.${Date.now().toString(36)}`,
    name: 'Cartel de Señalización y Peligro (Remix)',
    category: 'props',
    description: 'Rótulo mural metálico con franja de advertencia superior, biselado de seguridad y remaches perimetrales.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: t },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'placa_base',
        shape: 'box',
        size: [w, h, t],
        position: [0, h / 2, 0],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.7,
        metalness: 0.6
      },
      {
        name: 'franja_aviso_cabecera',
        shape: 'box',
        size: [w * 0.94, h * 0.32, 0.005],
        position: [0, h * 0.76, t / 2 + 0.003],
        color: '#ecc94b',
        texturePreset: 'hazard_stripes',
        roughness: 0.5,
        metalness: 0.2
      },
      {
        name: 'panel_texto_pictograma',
        shape: 'box',
        size: [w * 0.94, h * 0.52, 0.005],
        position: [0, h * 0.32, t / 2 + 0.003],
        color: '#e2e8f0',
        texturePreset: 'caution_label',
        roughness: 0.4,
        metalness: 0.2
      },
      {
        name: 'remache_sup_izq',
        shape: 'cylinder',
        size: [0.012, 0.012, 0.008, 6],
        position: [-w / 2 + 0.025, h - 0.025, t / 2 + 0.004],
        rotation: [90, 0, 0],
        color: '#a0aec0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      },
      {
        name: 'remache_sup_der',
        shape: 'cylinder',
        size: [0.012, 0.012, 0.008, 6],
        position: [w / 2 - 0.025, h - 0.025, t / 2 + 0.004],
        rotation: [90, 0, 0],
        color: '#a0aec0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      },
      {
        name: 'remache_inf_izq',
        shape: 'cylinder',
        size: [0.012, 0.012, 0.008, 6],
        position: [-w / 2 + 0.025, 0.025, t / 2 + 0.004],
        rotation: [90, 0, 0],
        color: '#a0aec0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      },
      {
        name: 'remache_inf_der',
        shape: 'cylinder',
        size: [0.012, 0.012, 0.008, 6],
        position: [w / 2 - 0.025, 0.025, t / 2 + 0.004],
        rotation: [90, 0, 0],
        color: '#a0aec0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      }
    ]
  };
});

// ===========================================================================
// 23. WALL CLOCK & TIMEPIECE
// ===========================================================================
CatalogBlueprintRegistry.register('wall_clock', (params) => {
  const p = params || {};
  const diameter = p.diameter || 0.38;
  const depth = 0.06;
  const radius = diameter / 2;

  return {
    id: `remix.wall_clock.${Date.now().toString(36)}`,
    name: 'Reloj Mural Analógico (Remix)',
    category: 'props',
    description: 'Reloj industrial analógico con marco de acero estampado, esfera fosforada, agujas horarias y cristal frontal protector.',
    units: 'meters',
    dimensions: { width: diameter, height: diameter, depth },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'carcasa_bisel_acero',
        shape: 'cylinder',
        size: [radius, radius, depth, 12],
        position: [0, radius, depth / 2],
        rotation: [90, 0, 0],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.5,
        metalness: 0.7
      },
      {
        name: 'esfera_cuadrante',
        shape: 'cylinder',
        size: [radius * 0.88, radius * 0.88, 0.005, 12],
        position: [0, radius, depth - 0.015],
        rotation: [90, 0, 0],
        color: '#f7fafc',
        texturePreset: 'gauge_radial_fuel',
        roughness: 0.4,
        metalness: 0.2
      },
      {
        name: 'aguja_horaria',
        shape: 'box',
        size: [0.018, radius * 0.45, 0.004],
        position: [0.03, radius + radius * 0.15, depth - 0.008],
        rotation: [0, 0, -35],
        color: '#1a202c',
        texturePreset: 'rubber_black',
        roughness: 0.5,
        metalness: 0.6
      },
      {
        name: 'aguja_minutero',
        shape: 'box',
        size: [0.012, radius * 0.68, 0.004],
        position: [-0.04, radius + radius * 0.28, depth - 0.006],
        rotation: [0, 0, 20],
        color: '#e53e3e',
        texturePreset: 'painted_metal_red',
        roughness: 0.4,
        metalness: 0.4
      },
      {
        name: 'pivote_central',
        shape: 'cylinder',
        size: [0.014, 0.014, 0.012, 8],
        position: [0, radius, depth - 0.004],
        rotation: [90, 0, 0],
        color: '#ecc94b',
        texturePreset: 'metal_light_brushed',
        roughness: 0.2,
        metalness: 0.9
      },
      {
        name: 'cristal_protector',
        shape: 'cylinder',
        size: [radius * 0.92, radius * 0.92, 0.004, 12],
        position: [0, radius, depth],
        rotation: [90, 0, 0],
        color: '#bee3f8',
        texturePreset: 'glass_transparent',
        roughness: 0.1,
        metalness: 0.1,
        transparent: true,
        opacity: 0.35
      }
    ]
  };
});

// ===========================================================================
// 24. MEDICAL SCREEN & VITAL SIGNS MONITOR
// ===========================================================================
CatalogBlueprintRegistry.register('medical_screen', (params) => {
  const p = params || {};
  const w = p.width || 0.65;
  const h = p.height || 1.45;
  const d = p.depth || 0.50;

  return {
    id: `remix.medical_screen.${Date.now().toString(36)}`,
    name: 'Monitor Médico de Signos Vitales (Remix)',
    category: 'medical',
    description: 'Monitor clínico móvil con columna telescópica sobre base rodante de 5 radios, pantalla LCD orientable y panel de telemetría.',
    units: 'meters',
    dimensions: { width: w, height: h, depth: d },
    palette: p.palette || 'industrial_hazard',
    components: [
      {
        name: 'base_estrella_rodante',
        shape: 'cylinder',
        size: [0.26, 0.26, 0.06, 5],
        position: [0, 0.05, 0],
        color: '#2d3748',
        texturePreset: 'metal_dark_grime',
        roughness: 0.6,
        metalness: 0.6
      },
      {
        name: 'columna_telescopica',
        shape: 'cylinder',
        size: [0.035, 0.035, 0.95, 8],
        position: [0, 0.55, 0],
        color: '#cbd5e0',
        texturePreset: 'metal_light_brushed',
        roughness: 0.3,
        metalness: 0.8
      },
      {
        name: 'carcasa_monitor',
        shape: 'box',
        size: [0.48, 0.36, 0.12],
        position: [0, 1.15, 0.04],
        rotation: [-10, 0, 0],
        color: '#edf2f7',
        texturePreset: 'painted_metal_white',
        roughness: 0.4,
        metalness: 0.3
      },
      {
        name: 'pantalla_lcd_telemetria',
        shape: 'box',
        size: [0.40, 0.26, 0.01],
        position: [0, 1.15, 0.105],
        rotation: [-10, 0, 0],
        color: '#319795',
        texturePreset: 'crt_display_green',
        roughness: 0.2,
        metalness: 0.1,
        emissive: '#319795',
        emissiveIntensity: 0.8
      },
      {
        name: 'teclado_membrana',
        shape: 'box',
        size: [0.38, 0.04, 0.01],
        position: [0, 0.99, 0.08],
        rotation: [-10, 0, 0],
        color: '#4a5568',
        texturePreset: 'plastic_rugged',
        roughness: 0.6,
        metalness: 0.2
      },
      {
        name: 'alarma_indicador_led',
        shape: 'box',
        size: [0.12, 0.02, 0.015],
        position: [0, 1.32, 0.02],
        color: '#ecc94b',
        roughness: 0.2,
        metalness: 0.1,
        emissive: '#ecc94b',
        emissiveIntensity: 0.9
      }
    ]
  };
});

