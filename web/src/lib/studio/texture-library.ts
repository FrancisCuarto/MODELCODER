import * as THREE from 'three';
import type { ComponentDef, TexturePreset } from './types.ts';

export type TexturePresetName = TexturePreset;

export type MaterialFamilyCategory =
  | 'metals'
  | 'construction'
  | 'woods'
  | 'stones'
  | 'plastics'
  | 'tech'
  | 'glass'
  | 'fabrics_organic';

export type ProceduralPatternKind =
  | 'legacy_switch'
  | 'brushed_metal'
  | 'galvanized_spangle'
  | 'cast_rough'
  | 'oxidized_patina'
  | 'diamond_plate'
  | 'perforated_grid'
  | 'painted_chipped'
  | 'concrete_surface'
  | 'cracked_masonry'
  | 'brick_wall'
  | 'ceramic_tiles'
  | 'corrugated_ridges'
  | 'terrazzo_speckle'
  | 'wood_grain'
  | 'wood_planks'
  | 'wood_parquet'
  | 'marble_veins'
  | 'granite_crystal'
  | 'slate_strata'
  | 'lunar_craters'
  | 'gravel_pebbles'
  | 'acoustic_pyramid'
  | 'knurled_polymer'
  | 'pcb_traces'
  | 'carbon_weave'
  | 'hex_honeycomb'
  | 'solar_array'
  | 'thermal_tiles'
  | 'crt_display'
  | 'stencil_badge'
  | 'frosted_crystal'
  | 'forcefield_grid'
  | 'woven_fabric'
  | 'quilted_padded'
  | 'leather_grain'
  | 'blueprint_grid'
  | 'organic_weathering';

export interface PatternSynthesisSpec {
  kind: ProceduralPatternKind;
  c1: [number, number, number]; // Primary RGB (0..255)
  c2: [number, number, number]; // Secondary/feature RGB (0..255)
  c3?: [number, number, number]; // Accent/detail RGB (0..255)
  scale?: number; // Pattern frequency multiplier
  noise?: number; // Grain/noise amplitude (0..60)
  alpha?: number; // Base alpha (0..255)
  param?: number; // Pattern-specific tweak parameter
}

export interface TexturePresetProfile {
  name: TexturePresetName;
  label: string;
  category: MaterialFamilyCategory;
  roughness: number;
  metalness: number;
  tintColor: string;
  emissive?: string;
  emissiveIntensity?: number;
  isDecal?: boolean; // If true, UVs use 0..1 clamp rather than aspect ratio tiling
  transparent?: boolean;
  opacity?: number;
  normalStrength?: number; // Tangent-space normal map relief intensity (0..1.5)
  tags?: string[];
  license?: string;
  pattern?: PatternSynthesisSpec;
}

export interface ParametricMaterialVariant {
  id: string;
  label: string;
  category: MaterialFamilyCategory;
  basePreset: TexturePresetName;
  tintColor: string;
  roughness: number;
  metalness: number;
  uvScale?: [number, number];
  uvRotation?: number;
  wear?: number;
  emissive?: string;
  emissiveIntensity?: number;
  transparent?: boolean;
  opacity?: number;
  tags: string[];
}

export const MATERIAL_CATEGORY_LABELS: Record<MaterialFamilyCategory, { label: string; icon: string }> = {
  metals: { label: 'Metales & Aleaciones', icon: '⚙️' },
  construction: { label: 'Construcción & Obra', icon: '🧱' },
  woods: { label: 'Maderas & Carpintería', icon: '🪵' },
  stones: { label: 'Piedras & Minerales', icon: '🪨' },
  plastics: { label: 'Plásticos & Gomas', icon: '🧪' },
  tech: { label: 'Tecnología, Sci-Fi & Pantallas', icon: '📟' },
  glass: { label: 'Vidrios & Transparencias', icon: '🪟' },
  fabrics_organic: { label: 'Telas, Cuero, Papel & Desgaste', icon: '🧵' }
};

export class TextureLibrary {
  private static textures = new Map<string, THREE.DataTexture>();
  private static normalTextures = new Map<string, THREE.DataTexture>();
  private static roughnessTextures = new Map<string, THREE.DataTexture>();
  private static materialCache = new Map<string, THREE.MeshStandardMaterial>();
  private static presetTextures = new Set<THREE.Texture>();
  private static thumbnailCache = new Map<string, string>();
  private static customTextures = new Map<string, THREE.Texture>();
  private static customDataUrls = new Map<string, string>();

  public static clearMaterialCache(): void {
    this.materialCache.clear();
  }

  public static registerCustomTexture(id: string, dataUrl: string): THREE.Texture {
    this.customDataUrls.set(id, dataUrl);
    if (typeof Image !== 'undefined') {
      const img = new Image();
      const texture = new THREE.Texture(img);
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.wrapS = THREE.RepeatWrapping;
      texture.wrapT = THREE.RepeatWrapping;
      img.onload = () => {
        texture.needsUpdate = true;
      };
      img.src = dataUrl;
      this.customTextures.set(id, texture);
      return texture;
    } else {
      const texture = new THREE.DataTexture(new Uint8Array(4), 1, 1);
      this.customTextures.set(id, texture);
      return texture;
    }
  }

  public static getCustomTexture(id: string): THREE.Texture | undefined {
    return this.customTextures.get(id);
  }

  public static getCustomDataUrl(id: string): string | undefined {
    return this.customDataUrls.get(id);
  }

  public static hasCustomTexture(id: string): boolean {
    return this.customTextures.has(id);
  }


  /**
   * 118 Canonical Procedural PBR Profiles across 8 material families.
   * Zero external image dependencies; 100% deterministic in-memory synthesis (CC0 / MIT).
   */
  public static readonly PROFILES: Record<TexturePresetName, TexturePresetProfile> = {
    // =========================================================================
    // ORIGINAL 18 PRESETS (Preserved with exact physics & pixel compatibility)
    // =========================================================================
    worn_metal: {
      name: 'worn_metal',
      label: 'Metal Desgastado',
      category: 'metals',
      roughness: 0.68,
      metalness: 0.35,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['metal', 'acero', 'desgastado', 'industrial', 'worn']
    },
    metal_dark_grime: {
      name: 'metal_dark_grime',
      label: 'Acero Estructural Oscuro',
      category: 'metals',
      roughness: 0.70,
      metalness: 0.38,
      tintColor: '#ffffff',
      normalStrength: 0.60,
      tags: ['metal', 'oscuro', 'sucio', 'acero', 'grime', 'estructural']
    },
    metal_light_brushed: {
      name: 'metal_light_brushed',
      label: 'Metal Cepillado',
      category: 'metals',
      roughness: 0.38,
      metalness: 0.85,
      tintColor: '#ffffff',
      normalStrength: 0.35,
      tags: ['metal', 'cepillado', 'inoxidable', 'brushed', 'steel']
    },
    painted_metal_white: {
      name: 'painted_metal_white',
      label: 'Esmalte Blanco Desgastado',
      category: 'metals',
      roughness: 0.65,
      metalness: 0.15,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['metal', 'pintado', 'blanco', 'esmalte', 'carcasa']
    },
    beige_plastic_worn: {
      name: 'beige_plastic_worn',
      label: 'Plástico Beige Retro (90s)',
      category: 'plastics',
      roughness: 0.55,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['plastico', 'beige', 'retro', 'computadora', '90s']
    },
    rubber_black: {
      name: 'rubber_black',
      label: 'Goma Negra Vulcanizada',
      category: 'plastics',
      roughness: 0.90,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.40,
      tags: ['goma', 'caucho', 'negro', 'neumatico', 'rubber']
    },
    rust_heavy: {
      name: 'rust_heavy',
      label: 'Óxido Pesado Corrosivo',
      category: 'fabrics_organic',
      roughness: 0.88,
      metalness: 0.10,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['oxido', 'corrosion', 'herrumbre', 'rust', 'desgaste']
    },
    hazard_stripes: {
      name: 'hazard_stripes',
      label: 'Rayas de Peligro (Amarillo/Negro)',
      category: 'construction',
      roughness: 0.70,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.35,
      tags: ['peligro', 'rayas', 'amarillo', 'seguridad', 'hazard']
    },
    vent_grill: {
      name: 'vent_grill',
      label: 'Rejilla de Ventilación',
      category: 'tech',
      roughness: 0.75,
      metalness: 0.40,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['rejilla', 'ventilacion', 'conducto', 'vent', 'grill']
    },
    crt_screen_green: {
      name: 'crt_screen_green',
      label: 'Monitor CRT Fósforo Verde',
      category: 'tech',
      roughness: 0.22,
      metalness: 0.0,
      tintColor: '#ffffff',
      emissive: '#26f259',
      emissiveIntensity: 1.5,
      isDecal: true,
      normalStrength: 0.10,
      tags: ['pantalla', 'crt', 'monitor', 'verde', 'radar', 'consola']
    },
    crt_screen_amber: {
      name: 'crt_screen_amber',
      label: 'Monitor CRT Fósforo Ámbar',
      category: 'tech',
      roughness: 0.22,
      metalness: 0.0,
      tintColor: '#ffffff',
      emissive: '#f29915',
      emissiveIntensity: 1.5,
      isDecal: true,
      normalStrength: 0.10,
      tags: ['pantalla', 'crt', 'monitor', 'ambar', 'telemetria']
    },
    crt_screen_off: {
      name: 'crt_screen_off',
      label: 'Pantalla CRT Apagada',
      category: 'tech',
      roughness: 0.18,
      metalness: 0.05,
      tintColor: '#ffffff',
      isDecal: true,
      normalStrength: 0.08,
      tags: ['pantalla', 'crt', 'apagada', 'cristal', 'monitor']
    },
    caution_label: {
      name: 'caution_label',
      label: 'Etiqueta de Precaución',
      category: 'tech',
      roughness: 0.60,
      metalness: 0.05,
      tintColor: '#ffffff',
      isDecal: true,
      normalStrength: 0.20,
      tags: ['etiqueta', 'cartel', 'precaucion', 'aviso', 'caution']
    },
    red_paint_worn: {
      name: 'red_paint_worn',
      label: 'Pintura Roja Industrial',
      category: 'metals',
      roughness: 0.65,
      metalness: 0.12,
      tintColor: '#ffffff',
      normalStrength: 0.50,
      tags: ['pintura', 'rojo', 'emergencia', 'metal', 'desgastado']
    },
    tinted_glass: {
      name: 'tinted_glass',
      label: 'Vidrio Polarizado / Visor',
      category: 'glass',
      roughness: 0.12,
      metalness: 0.15,
      tintColor: '#4a7c92',
      transparent: true,
      opacity: 0.50,
      normalStrength: 0.10,
      tags: ['vidrio', 'polarizado', 'visor', 'cabina', 'cristal']
    },
    reinforced_glass: {
      name: 'reinforced_glass',
      label: 'Vidrio Blindado con Malla',
      category: 'glass',
      roughness: 0.20,
      metalness: 0.35,
      tintColor: '#718096',
      transparent: true,
      opacity: 0.65,
      normalStrength: 0.45,
      tags: ['vidrio', 'blindado', 'malla', 'armado', 'seguridad']
    },
    clean_glass: {
      name: 'clean_glass',
      label: 'Vidrio Transparente',
      category: 'glass',
      roughness: 0.05,
      metalness: 0.05,
      tintColor: '#a0c4e2',
      transparent: true,
      opacity: 0.35,
      normalStrength: 0.05,
      tags: ['vidrio', 'transparente', 'ventana', 'limpio', 'cristal']
    },
    hologram_cyan: {
      name: 'hologram_cyan',
      label: 'Holograma / HUD Sci-Fi',
      category: 'glass',
      roughness: 0.20,
      metalness: 0.0,
      tintColor: '#00f0ff',
      emissive: '#00f0ff',
      emissiveIntensity: 2.0,
      transparent: true,
      opacity: 0.60,
      normalStrength: 0.15,
      tags: ['holograma', 'hud', 'cian', 'energia', 'scifi']
    },

    // =========================================================================
    // 1. EXPANDED METALS & ALLOYS (18 New Presets)
    // =========================================================================
    steel_polished: {
      name: 'steel_polished',
      label: 'Acero Inoxidable Pulido',
      category: 'metals',
      roughness: 0.18,
      metalness: 0.92,
      tintColor: '#ffffff',
      normalStrength: 0.20,
      tags: ['acero', 'pulido', 'inoxidable', 'brillante', 'steel'],
      pattern: { kind: 'brushed_metal', c1: [210, 216, 224], c2: [180, 188, 198], noise: 6, scale: 1 }
    },
    steel_galvanized: {
      name: 'steel_galvanized',
      label: 'Acero Galvanizado (Cincado)',
      category: 'metals',
      roughness: 0.48,
      metalness: 0.78,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['acero', 'galvanizado', 'zinc', 'chapa', 'conducto'],
      pattern: { kind: 'galvanized_spangle', c1: [168, 176, 184], c2: [130, 138, 148], c3: [200, 208, 215], scale: 6, noise: 10 }
    },
    iron_cast: {
      name: 'iron_cast',
      label: 'Hierro Fundido Rugoso',
      category: 'metals',
      roughness: 0.82,
      metalness: 0.55,
      tintColor: '#ffffff',
      normalStrength: 0.75,
      tags: ['hierro', 'fundido', 'forja', 'pesado', 'cast iron'],
      pattern: { kind: 'cast_rough', c1: [54, 56, 60], c2: [36, 38, 42], noise: 22, scale: 2 }
    },
    iron_aged: {
      name: 'iron_aged',
      label: 'Hierro Envejecido Forjado',
      category: 'metals',
      roughness: 0.76,
      metalness: 0.48,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['hierro', 'antiguo', 'envejecido', 'forjado', 'iron'],
      pattern: { kind: 'oxidized_patina', c1: [68, 66, 64], c2: [110, 62, 36], c3: [40, 38, 38], noise: 18, param: 0.35 }
    },
    aluminum_anodized: {
      name: 'aluminum_anodized',
      label: 'Aluminio Anodizado Mate',
      category: 'metals',
      roughness: 0.34,
      metalness: 0.82,
      tintColor: '#ffffff',
      normalStrength: 0.25,
      tags: ['aluminio', 'anodizado', 'ligero', 'aeroespacial', 'aluminum'],
      pattern: { kind: 'brushed_metal', c1: [192, 198, 205], c2: [172, 178, 186], noise: 8, scale: 2 }
    },
    copper_polished: {
      name: 'copper_polished',
      label: 'Cobre Electrolítico Pulido',
      category: 'metals',
      roughness: 0.26,
      metalness: 0.90,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['cobre', 'bobina', 'tuberia', 'conductor', 'copper'],
      pattern: { kind: 'brushed_metal', c1: [218, 122, 74], c2: [184, 92, 52], noise: 10, scale: 1 }
    },
    copper_oxidized: {
      name: 'copper_oxidized',
      label: 'Cobre Oxidado (Pátina Verde)',
      category: 'metals',
      roughness: 0.72,
      metalness: 0.42,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['cobre', 'patina', 'cardenillo', 'oxidado', 'verdigris'],
      pattern: { kind: 'oxidized_patina', c1: [165, 90, 55], c2: [72, 158, 132], c3: [52, 118, 98], noise: 16, param: 0.58 }
    },
    bronze_antique: {
      name: 'bronze_antique',
      label: 'Bronce Industrial Antiguo',
      category: 'metals',
      roughness: 0.46,
      metalness: 0.80,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['bronce', 'valvula', 'engrane', 'antiguo', 'bronze'],
      pattern: { kind: 'oxidized_patina', c1: [156, 116, 62], c2: [92, 68, 36], c3: [188, 146, 84], noise: 12, param: 0.30 }
    },
    brass_burnished: {
      name: 'brass_burnished',
      label: 'Latón Bruñido Maquinado',
      category: 'metals',
      roughness: 0.30,
      metalness: 0.88,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['laton', 'dorado', 'maquinado', 'instrumento', 'brass'],
      pattern: { kind: 'brushed_metal', c1: [215, 178, 82], c2: [182, 144, 58], noise: 9, scale: 1 }
    },
    titanium_aerospace: {
      name: 'titanium_aerospace',
      label: 'Titanio Aeroespacial',
      category: 'metals',
      roughness: 0.32,
      metalness: 0.86,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['titanio', 'nave', 'blindaje', 'aeroespacial', 'titanium'],
      pattern: { kind: 'brushed_metal', c1: [148, 154, 164], c2: [122, 128, 138], noise: 10, scale: 2 }
    },
    diamond_plate: {
      name: 'diamond_plate',
      label: 'Chapa Diamantada Antideslizante',
      category: 'metals',
      roughness: 0.45,
      metalness: 0.80,
      tintColor: '#ffffff',
      normalStrength: 0.90,
      tags: ['chapa', 'diamantada', 'piso', 'rampa', 'industrial', 'diamond plate'],
      pattern: { kind: 'diamond_plate', c1: [118, 126, 136], c2: [176, 186, 196], c3: [74, 80, 88], scale: 8, noise: 10 }
    },
    metal_perforated: {
      name: 'metal_perforated',
      label: 'Malla Metálica Perforada',
      category: 'metals',
      roughness: 0.55,
      metalness: 0.70,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['malla', 'perforado', 'rejilla', 'filtro', 'mesh'],
      pattern: { kind: 'perforated_grid', c1: [128, 134, 142], c2: [18, 20, 24], scale: 4, noise: 8 }
    },
    gold_contacts: {
      name: 'gold_contacts',
      label: 'Oro de Contactos Electrónicos',
      category: 'metals',
      roughness: 0.20,
      metalness: 0.96,
      tintColor: '#ffffff',
      normalStrength: 0.20,
      tags: ['oro', 'dorado', 'contacto', 'chip', 'gold'],
      pattern: { kind: 'brushed_metal', c1: [246, 198, 56], c2: [214, 162, 34], noise: 6, scale: 1 }
    },
    chrome_mirror: {
      name: 'chrome_mirror',
      label: 'Cromo Espejo Hidráulico',
      category: 'metals',
      roughness: 0.08,
      metalness: 0.98,
      tintColor: '#ffffff',
      normalStrength: 0.10,
      tags: ['cromo', 'espejo', 'piston', 'hidraulico', 'chrome'],
      pattern: { kind: 'brushed_metal', c1: [232, 238, 245], c2: [200, 210, 222], noise: 4, scale: 1 }
    },
    lead_shielding: {
      name: 'lead_shielding',
      label: 'Plomo de Blindaje Radiológico',
      category: 'metals',
      roughness: 0.78,
      metalness: 0.60,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['plomo', 'blindaje', 'nuclear', 'reactor', 'lead'],
      pattern: { kind: 'cast_rough', c1: [76, 82, 92], c2: [56, 62, 70], noise: 14, scale: 2 }
    },
    painted_metal_blue: {
      name: 'painted_metal_blue',
      label: 'Metal Pintado Azul Maquinaria',
      category: 'metals',
      roughness: 0.58,
      metalness: 0.22,
      tintColor: '#ffffff',
      normalStrength: 0.50,
      tags: ['metal', 'pintado', 'azul', 'maquinaria', 'generador'],
      pattern: { kind: 'painted_chipped', c1: [42, 92, 152], c2: [58, 62, 68], c3: [120, 158, 204], noise: 12 }
    },
    painted_metal_olive: {
      name: 'painted_metal_olive',
      label: 'Metal Pintado Verde Militar',
      category: 'metals',
      roughness: 0.68,
      metalness: 0.18,
      tintColor: '#ffffff',
      normalStrength: 0.50,
      tags: ['metal', 'pintado', 'verde', 'militar', 'tactico', 'olive'],
      pattern: { kind: 'painted_chipped', c1: [74, 88, 58], c2: [52, 54, 56], c3: [110, 82, 48], noise: 14 }
    },
    painted_metal_yellow: {
      name: 'painted_metal_yellow',
      label: 'Metal Pintado Amarillo Grúa',
      category: 'metals',
      roughness: 0.56,
      metalness: 0.20,
      tintColor: '#ffffff',
      normalStrength: 0.50,
      tags: ['metal', 'pintado', 'amarillo', 'grua', 'industrial'],
      pattern: { kind: 'painted_chipped', c1: [218, 162, 24], c2: [62, 58, 54], c3: [142, 76, 32], noise: 14 }
    },

    // =========================================================================
    // 2. CONSTRUCTION, CONCRETE, BRICK & INDUSTRIAL FLOORS (14 New Presets)
    // =========================================================================
    concrete_smooth: {
      name: 'concrete_smooth',
      label: 'Hormigón Alisado Arquitectónico',
      category: 'construction',
      roughness: 0.80,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['hormigon', 'concreto', 'cemento', 'liso', 'pared', 'concrete'],
      pattern: { kind: 'concrete_surface', c1: [148, 150, 148], c2: [124, 126, 124], noise: 16, param: 0.1 }
    },
    concrete_rough: {
      name: 'concrete_rough',
      label: 'Hormigón Rugoso de Búnker',
      category: 'construction',
      roughness: 0.92,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['hormigon', 'rugoso', 'bunker', 'brutalista', 'concreto'],
      pattern: { kind: 'concrete_surface', c1: [112, 114, 110], c2: [78, 80, 76], noise: 32, param: 0.4 }
    },
    concrete_cracked: {
      name: 'concrete_cracked',
      label: 'Hormigón Agrietado Desgastado',
      category: 'construction',
      roughness: 0.94,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.90,
      tags: ['hormigon', 'agrietado', 'grietas', 'ruina', 'deteriorado'],
      pattern: { kind: 'cracked_masonry', c1: [122, 120, 116], c2: [38, 36, 34], c3: [92, 90, 86], noise: 24 }
    },
    cinder_block: {
      name: 'cinder_block',
      label: 'Muro de Bloques de Cemento',
      category: 'construction',
      roughness: 0.90,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['bloque', 'cemento', 'muro', 'pared', 'cinder block'],
      pattern: { kind: 'brick_wall', c1: [136, 138, 136], c2: [82, 84, 82], scale: 2, noise: 22, param: 1 }
    },
    brick_red: {
      name: 'brick_red',
      label: 'Ladrillo Rojo Visto Tradicional',
      category: 'construction',
      roughness: 0.88,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['ladrillo', 'rojo', 'pared', 'mamposteria', 'brick'],
      pattern: { kind: 'brick_wall', c1: [164, 68, 48], c2: [188, 182, 170], c3: [132, 50, 36], scale: 4, noise: 18 }
    },
    brick_industrial: {
      name: 'brick_industrial',
      label: 'Ladrillo Refractario Oscuro',
      category: 'construction',
      roughness: 0.86,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['ladrillo', 'industrial', 'refractario', 'horno', 'fabrica'],
      pattern: { kind: 'brick_wall', c1: [96, 62, 52], c2: [52, 50, 48], c3: [124, 82, 64], scale: 4, noise: 20 }
    },
    stucco_plaster: {
      name: 'stucco_plaster',
      label: 'Revoque / Estuco Texturizado',
      category: 'construction',
      roughness: 0.85,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['revoque', 'estuco', 'yeso', 'pared', 'fachada'],
      pattern: { kind: 'concrete_surface', c1: [216, 210, 196], c2: [188, 180, 166], noise: 22, param: 0.2 }
    },
    asphalt_road: {
      name: 'asphalt_road',
      label: 'Asfalto Vial Bituminoso',
      category: 'construction',
      roughness: 0.92,
      metalness: 0.03,
      tintColor: '#ffffff',
      normalStrength: 0.75,
      tags: ['asfalto', 'calle', 'pavimento', 'pista', 'asphalt'],
      pattern: { kind: 'terrazzo_speckle', c1: [44, 46, 50], c2: [78, 80, 86], c3: [26, 28, 30], noise: 24, param: 0.25 }
    },
    ceramic_tile_white: {
      name: 'ceramic_tile_white',
      label: 'Baldosas Cerámicas de Laboratorio',
      category: 'construction',
      roughness: 0.24,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['baldosa', 'ceramica', 'azulejo', 'laboratorio', 'blanco', 'tile'],
      pattern: { kind: 'ceramic_tiles', c1: [228, 234, 238], c2: [140, 148, 154], scale: 4, noise: 6 }
    },
    industrial_tile_dirty: {
      name: 'industrial_tile_dirty',
      label: 'Baldosas Industriales Sucias',
      category: 'construction',
      roughness: 0.68,
      metalness: 0.08,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['baldosa', 'piso', 'sucio', 'industrial', 'subterraneo'],
      pattern: { kind: 'ceramic_tiles', c1: [118, 124, 116], c2: [48, 50, 46], c3: [88, 76, 58], scale: 4, noise: 22 }
    },
    nonslip_floor: {
      name: 'nonslip_floor',
      label: 'Piso Industrial Antideslizante',
      category: 'construction',
      roughness: 0.78,
      metalness: 0.25,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['piso', 'antideslizante', 'pasarela', 'plataforma', 'floor'],
      pattern: { kind: 'perforated_grid', c1: [72, 78, 86], c2: [112, 118, 128], scale: 6, noise: 14, param: 1 }
    },
    station_modular_panel: {
      name: 'station_modular_panel',
      label: 'Panel Modular de Estación Espacial',
      category: 'construction',
      roughness: 0.45,
      metalness: 0.40,
      tintColor: '#ffffff',
      normalStrength: 0.70,
      tags: ['panel', 'modular', 'estacion', 'pared', 'mamparo', 'bulkhead'],
      pattern: { kind: 'thermal_tiles', c1: [176, 182, 190], c2: [68, 74, 82], c3: [138, 146, 156], scale: 2, noise: 8 }
    },
    corrugated_metal: {
      name: 'corrugated_metal',
      label: 'Chapa Acanalada de Contenedor',
      category: 'construction',
      roughness: 0.58,
      metalness: 0.65,
      tintColor: '#ffffff',
      normalStrength: 0.90,
      tags: ['chapa', 'acanalada', 'contenedor', 'techo', 'corrugated'],
      pattern: { kind: 'corrugated_ridges', c1: [132, 140, 148], c2: [64, 70, 76], scale: 8, noise: 12 }
    },
    terrazzo_floor: {
      name: 'terrazzo_floor',
      label: 'Piso Terrazo Granítico Pulido',
      category: 'construction',
      roughness: 0.32,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.35,
      tags: ['terrazo', 'mosaico', 'piso', 'institucional', 'terrazzo'],
      pattern: { kind: 'terrazzo_speckle', c1: [196, 192, 184], c2: [92, 86, 78], c3: [232, 228, 220], noise: 10, param: 0.35 }
    },

    // =========================================================================
    // 3. WOODS & CARPENTRY (10 New Presets)
    // =========================================================================
    wood_oak: {
      name: 'wood_oak',
      label: 'Madera de Roble Natural',
      category: 'woods',
      roughness: 0.62,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['madera', 'roble', 'mueble', 'natural', 'oak', 'wood'],
      pattern: { kind: 'wood_grain', c1: [168, 118, 68], c2: [122, 78, 42], scale: 5, noise: 10 }
    },
    wood_pine: {
      name: 'wood_pine',
      label: 'Madera de Pino Claro',
      category: 'woods',
      roughness: 0.68,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.50,
      tags: ['madera', 'pino', 'caja', 'claro', 'pine', 'crate'],
      pattern: { kind: 'wood_grain', c1: [214, 176, 118], c2: [176, 132, 78], scale: 4, noise: 12 }
    },
    wood_walnut: {
      name: 'wood_walnut',
      label: 'Madera de Nogal Oscuro',
      category: 'woods',
      roughness: 0.52,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.50,
      tags: ['madera', 'nogal', 'oscuro', 'escritorio', 'walnut'],
      pattern: { kind: 'wood_grain', c1: [96, 58, 34], c2: [58, 32, 18], scale: 6, noise: 8 }
    },
    wood_plywood: {
      name: 'wood_plywood',
      label: 'Contrachapado Industrial (Plywood)',
      category: 'woods',
      roughness: 0.78,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['madera', 'contrachapado', 'embalaje', 'tablero', 'plywood'],
      pattern: { kind: 'wood_grain', c1: [198, 162, 112], c2: [162, 124, 78], scale: 2, noise: 18 }
    },
    wood_painted_worn: {
      name: 'wood_painted_worn',
      label: 'Madera Pintada Descascarada',
      category: 'woods',
      roughness: 0.74,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.70,
      tags: ['madera', 'pintada', 'desgastada', 'vieja', 'vintage'],
      pattern: { kind: 'painted_chipped', c1: [188, 194, 186], c2: [112, 78, 46], c3: [148, 152, 144], noise: 16 }
    },
    wood_rustic_planks: {
      name: 'wood_rustic_planks',
      label: 'Tablones de Madera Rústica',
      category: 'woods',
      roughness: 0.84,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['madera', 'tablones', 'rustico', 'tarima', 'pallet', 'planks'],
      pattern: { kind: 'wood_planks', c1: [132, 94, 58], c2: [42, 30, 20], c3: [104, 72, 44], scale: 4, noise: 16 }
    },
    wood_varnished: {
      name: 'wood_varnished',
      label: 'Madera Barnizada Brillante (Caoba)',
      category: 'woods',
      roughness: 0.22,
      metalness: 0.04,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['madera', 'barnizada', 'caoba', 'brillante', 'instrumento'],
      pattern: { kind: 'wood_grain', c1: [138, 56, 28], c2: [88, 30, 14], scale: 5, noise: 6 }
    },
    wood_parquet: {
      name: 'wood_parquet',
      label: 'Parquet / Piso de Madera Entablonada',
      category: 'woods',
      roughness: 0.42,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.60,
      tags: ['madera', 'parquet', 'piso', 'duela', 'interior'],
      pattern: { kind: 'wood_parquet', c1: [174, 124, 72], c2: [132, 88, 48], c3: [68, 44, 24], scale: 4, noise: 10 }
    },
    wood_bamboo: {
      name: 'wood_bamboo',
      label: 'Bambú Laminado Técnico',
      category: 'woods',
      roughness: 0.50,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['madera', 'bambu', 'claro', 'ecologico', 'bamboo'],
      pattern: { kind: 'wood_planks', c1: [208, 178, 112], c2: [156, 126, 68], c3: [188, 158, 94], scale: 8, noise: 8 }
    },
    wood_charred: {
      name: 'wood_charred',
      label: 'Madera Carbonizada (Shou Sugi Ban)',
      category: 'woods',
      roughness: 0.88,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['madera', 'quemada', 'carbonizada', 'negra', 'ceniza'],
      pattern: { kind: 'wood_grain', c1: [36, 34, 32], c2: [18, 16, 16], scale: 7, noise: 16 }
    },

    // =========================================================================
    // 4. STONES, ROCKS & MINERALS (12 New Presets)
    // =========================================================================
    granite_grey: {
      name: 'granite_grey',
      label: 'Granito Gris Cristalino',
      category: 'stones',
      roughness: 0.45,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['piedra', 'granito', 'gris', 'mesada', 'monumento', 'granite'],
      pattern: { kind: 'granite_crystal', c1: [138, 142, 146], c2: [52, 56, 60], c3: [212, 216, 220], noise: 24 }
    },
    granite_pink: {
      name: 'granite_pink',
      label: 'Granito Rosado Feldespato',
      category: 'stones',
      roughness: 0.48,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['piedra', 'granito', 'rosado', 'feldespato', 'arquitectura'],
      pattern: { kind: 'granite_crystal', c1: [186, 134, 124], c2: [68, 62, 64], c3: [224, 212, 206], noise: 22 }
    },
    marble_white: {
      name: 'marble_white',
      label: 'Mármol Blanco Carrara Veteado',
      category: 'stones',
      roughness: 0.20,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.25,
      tags: ['piedra', 'marmol', 'blanco', 'carrara', 'lujo', 'marble'],
      pattern: { kind: 'marble_veins', c1: [238, 240, 242], c2: [128, 134, 142], scale: 3, noise: 6 }
    },
    marble_black_gold: {
      name: 'marble_black_gold',
      label: 'Mármol Negro Portoro con Vetas Doradas',
      category: 'stones',
      roughness: 0.18,
      metalness: 0.15,
      tintColor: '#ffffff',
      normalStrength: 0.25,
      tags: ['piedra', 'marmol', 'negro', 'dorado', 'portoro'],
      pattern: { kind: 'marble_veins', c1: [26, 28, 32], c2: [204, 162, 64], scale: 3, noise: 8 }
    },
    slate_layered: {
      name: 'slate_layered',
      label: 'Pizarra Estratificada Oscura',
      category: 'stones',
      roughness: 0.78,
      metalness: 0.06,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['piedra', 'pizarra', 'laja', 'roca', 'slate'],
      pattern: { kind: 'slate_strata', c1: [64, 70, 78], c2: [42, 46, 52], scale: 6, noise: 16 }
    },
    basalt_lunar: {
      name: 'basalt_lunar',
      label: 'Roca Basáltica / Regolito Lunar',
      category: 'stones',
      roughness: 0.94,
      metalness: 0.04,
      tintColor: '#ffffff',
      normalStrength: 0.90,
      tags: ['roca', 'basalto', 'lunar', 'asteroide', 'meteorito', 'crater'],
      pattern: { kind: 'lunar_craters', c1: [86, 88, 92], c2: [44, 46, 50], c3: [124, 126, 130], noise: 26 }
    },
    limestone_sand: {
      name: 'limestone_sand',
      label: 'Piedra Caliza / Arenisca',
      category: 'stones',
      roughness: 0.86,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.70,
      tags: ['piedra', 'caliza', 'arenisca', 'bloque', 'limestone'],
      pattern: { kind: 'slate_strata', c1: [208, 192, 158], c2: [176, 158, 124], scale: 4, noise: 18 }
    },
    sand_compacted: {
      name: 'sand_compacted',
      label: 'Arena Compactada / Duna',
      category: 'stones',
      roughness: 0.92,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['arena', 'desierto', 'terreno', 'suelo', 'sand'],
      pattern: { kind: 'corrugated_ridges', c1: [216, 188, 134], c2: [184, 154, 102], scale: 5, noise: 18 }
    },
    gravel_mineral: {
      name: 'gravel_mineral',
      label: 'Grava Mineral / Balasto',
      category: 'stones',
      roughness: 0.95,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.95,
      tags: ['grava', 'piedras', 'ripio', 'suelo', 'gravel'],
      pattern: { kind: 'gravel_pebbles', c1: [112, 110, 106], c2: [64, 62, 58], c3: [156, 152, 146], noise: 28 }
    },
    quartz_crystal: {
      name: 'quartz_crystal',
      label: 'Cristal de Cuarzo Mineral',
      category: 'stones',
      roughness: 0.25,
      metalness: 0.15,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['cuarzo', 'cristal', 'mineral', 'geoda', 'quartz'],
      pattern: { kind: 'frosted_crystal', c1: [228, 220, 238], c2: [178, 162, 204], c3: [250, 248, 255], noise: 14 }
    },
    energy_mineral: {
      name: 'energy_mineral',
      label: 'Mineral Energético Bioluminiscente',
      category: 'stones',
      roughness: 0.35,
      metalness: 0.25,
      tintColor: '#ffffff',
      emissive: '#38ef7d',
      emissiveIntensity: 1.2,
      normalStrength: 0.80,
      tags: ['mineral', 'energia', 'cristal', 'uranio', 'alien', 'scifi'],
      pattern: { kind: 'marble_veins', c1: [34, 48, 44], c2: [56, 242, 136], scale: 4, noise: 16 }
    },
    obsidian_volcanic: {
      name: 'obsidian_volcanic',
      label: 'Obsidiana Volcánica Vítrea',
      category: 'stones',
      roughness: 0.14,
      metalness: 0.20,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['obsidiana', 'volcanica', 'roca', 'negra', 'cristal'],
      pattern: { kind: 'frosted_crystal', c1: [24, 22, 32], c2: [54, 46, 68], c3: [14, 12, 18], noise: 8 }
    },

    // =========================================================================
    // 5. PLASTICS, RUBBERS & POLYMERS (10 New Presets)
    // =========================================================================
    plastic_abs_matte: {
      name: 'plastic_abs_matte',
      label: 'Plástico ABS Mate Industrial',
      category: 'plastics',
      roughness: 0.60,
      metalness: 0.04,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['plastico', 'abs', 'mate', 'carcasa', 'impresion 3d'],
      pattern: { kind: 'cast_rough', c1: [72, 78, 86], c2: [60, 66, 74], noise: 10, scale: 1 }
    },
    plastic_acrylic_gloss: {
      name: 'plastic_acrylic_gloss',
      label: 'Acrílico Brillante de Alta Densidad',
      category: 'plastics',
      roughness: 0.12,
      metalness: 0.06,
      tintColor: '#ffffff',
      normalStrength: 0.10,
      tags: ['plastico', 'acrilico', 'brillante', 'polimero', 'acrylic'],
      pattern: { kind: 'brushed_metal', c1: [230, 234, 240], c2: [215, 220, 228], noise: 4, scale: 1 }
    },
    plastic_translucent: {
      name: 'plastic_translucent',
      label: 'Polímero Translúcido de Laboratorio',
      category: 'plastics',
      roughness: 0.35,
      metalness: 0.02,
      tintColor: '#e2e8f0',
      transparent: true,
      opacity: 0.72,
      normalStrength: 0.20,
      tags: ['plastico', 'translucido', 'bidon', 'envase', 'laboratorio'],
      pattern: { kind: 'frosted_crystal', c1: [215, 226, 236], c2: [188, 204, 218], noise: 10, alpha: 185 }
    },
    rubber_ribbed_mat: {
      name: 'rubber_ribbed_mat',
      label: 'Caucho Acanalado para Pisos',
      category: 'plastics',
      roughness: 0.88,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['goma', 'caucho', 'acanalado', 'alfombra', 'antideslizante'],
      pattern: { kind: 'corrugated_ridges', c1: [38, 40, 44], c2: [18, 20, 22], scale: 12, noise: 8 }
    },
    silicone_medical: {
      name: 'silicone_medical',
      label: 'Silicona Médica / Sello Hermético',
      category: 'plastics',
      roughness: 0.48,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.25,
      tags: ['silicona', 'medica', 'junta', 'sello', 'tubo'],
      pattern: { kind: 'cast_rough', c1: [186, 212, 218], c2: [164, 194, 202], noise: 6, scale: 1 }
    },
    acoustic_foam: {
      name: 'acoustic_foam',
      label: 'Espuma Acústica Piramidal',
      category: 'plastics',
      roughness: 0.96,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.95,
      tags: ['espuma', 'acustica', 'insonorizacion', 'estudio', 'foam'],
      pattern: { kind: 'acoustic_pyramid', c1: [52, 54, 60], c2: [20, 22, 26], scale: 8, noise: 10 }
    },
    polymer_tactical: {
      name: 'polymer_tactical',
      label: 'Polímero Táctico Moleteado (Grip)',
      category: 'plastics',
      roughness: 0.78,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['polimero', 'tactico', 'grip', 'empuñadura', 'moleteado'],
      pattern: { kind: 'knurled_polymer', c1: [46, 48, 44], c2: [26, 28, 24], scale: 4, noise: 10 }
    },
    plastic_hazard_orange: {
      name: 'plastic_hazard_orange',
      label: 'Plástico Naranja Vial / Emergencia',
      category: 'plastics',
      roughness: 0.42,
      metalness: 0.04,
      tintColor: '#ffffff',
      normalStrength: 0.30,
      tags: ['plastico', 'naranja', 'cono', 'baliza', 'emergencia'],
      pattern: { kind: 'cast_rough', c1: [238, 102, 22], c2: [204, 78, 14], noise: 10, scale: 1 }
    },
    vinyl_grip: {
      name: 'vinyl_grip',
      label: 'Vinilo Texturizado Antideslizante',
      category: 'plastics',
      roughness: 0.72,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['vinilo', 'recubrimiento', 'funda', 'aislante', 'vinyl'],
      pattern: { kind: 'knurled_polymer', c1: [62, 68, 78], c2: [40, 44, 52], scale: 6, noise: 12 }
    },
    teflon_white: {
      name: 'teflon_white',
      label: 'Teflón / PTFE Técnico Blanco',
      category: 'plastics',
      roughness: 0.28,
      metalness: 0.02,
      tintColor: '#ffffff',
      normalStrength: 0.15,
      tags: ['teflon', 'ptfe', 'blanco', 'aislador', 'valvula'],
      pattern: { kind: 'cast_rough', c1: [242, 244, 246], c2: [226, 230, 234], noise: 5, scale: 1 }
    },

    // =========================================================================
    // 6. TECH, SCI-FI, PCB, SCREENS & SIGNAGE (16 New Presets)
    // =========================================================================
    pcb_green_gold: {
      name: 'pcb_green_gold',
      label: 'Placa Circuito Impreso (PCB Verde/Oro)',
      category: 'tech',
      roughness: 0.36,
      metalness: 0.45,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['pcb', 'circuito', 'electronica', 'placa', 'motherboard'],
      pattern: { kind: 'pcb_traces', c1: [22, 92, 48], c2: [224, 178, 54], c3: [14, 58, 30], scale: 4, noise: 6 }
    },
    pcb_black_hd: {
      name: 'pcb_black_hd',
      label: 'PCB Negro Alta Densidad (GPU/Server)',
      category: 'tech',
      roughness: 0.32,
      metalness: 0.50,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['pcb', 'negro', 'circuito', 'servidor', 'hardware'],
      pattern: { kind: 'pcb_traces', c1: [24, 26, 30], c2: [196, 204, 214], c3: [188, 142, 44], scale: 4, noise: 6 }
    },
    pcb_blue_proto: {
      name: 'pcb_blue_proto',
      label: 'PCB Azul Prototipo / Microcontrolador',
      category: 'tech',
      roughness: 0.36,
      metalness: 0.45,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['pcb', 'azul', 'arduino', 'prototipo', 'electronica'],
      pattern: { kind: 'pcb_traces', c1: [24, 72, 148], c2: [218, 182, 68], c3: [14, 44, 98], scale: 4, noise: 6 }
    },
    carbon_fiber: {
      name: 'carbon_fiber',
      label: 'Fibra de Carbono Tejida 3K',
      category: 'tech',
      roughness: 0.28,
      metalness: 0.35,
      tintColor: '#ffffff',
      normalStrength: 0.70,
      tags: ['carbono', 'fibra', 'compuesto', 'aeroespacial', 'carbon fiber'],
      pattern: { kind: 'carbon_weave', c1: [32, 34, 38], c2: [68, 72, 80], scale: 4, noise: 6 }
    },
    hex_composite: {
      name: 'hex_composite',
      label: 'Panel Compuesto Hexagonal Sci-Fi',
      category: 'tech',
      roughness: 0.38,
      metalness: 0.60,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['hexagonal', 'panal', 'blindaje', 'scifi', 'composite'],
      pattern: { kind: 'hex_honeycomb', c1: [64, 72, 84], c2: [28, 32, 38], c3: [104, 116, 132], scale: 8, noise: 8 }
    },
    server_vent_panel: {
      name: 'server_vent_panel',
      label: 'Frontal de Rack de Servidor Ventilado',
      category: 'tech',
      roughness: 0.50,
      metalness: 0.65,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['servidor', 'rack', 'ventilacion', 'datacenter', 'server'],
      pattern: { kind: 'perforated_grid', c1: [44, 48, 54], c2: [12, 14, 18], scale: 4, noise: 6 }
    },
    thermal_tile_white: {
      name: 'thermal_tile_white',
      label: 'Escudo Térmico Cerámico Blanco (Orbital)',
      category: 'tech',
      roughness: 0.72,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.75,
      tags: ['termico', 'ceramico', 'loseta', 'espacial', 'shuttle'],
      pattern: { kind: 'thermal_tiles', c1: [232, 230, 224], c2: [78, 76, 72], c3: [204, 200, 192], scale: 4, noise: 12 }
    },
    thermal_tile_black: {
      name: 'thermal_tile_black',
      label: 'Escudo Térmico de Reentrada (Carbono)',
      category: 'tech',
      roughness: 0.76,
      metalness: 0.15,
      tintColor: '#ffffff',
      normalStrength: 0.80,
      tags: ['termico', 'escudo', 'loseta', 'negro', 'nave'],
      pattern: { kind: 'thermal_tiles', c1: [42, 44, 48], c2: [16, 18, 20], c3: [62, 64, 70], scale: 4, noise: 14 }
    },
    solar_panel_blue: {
      name: 'solar_panel_blue',
      label: 'Panel Solar Fotovoltaico Satelital',
      category: 'tech',
      roughness: 0.18,
      metalness: 0.65,
      tintColor: '#ffffff',
      normalStrength: 0.55,
      tags: ['solar', 'panel', 'celda', 'satelite', 'energia'],
      pattern: { kind: 'solar_array', c1: [24, 58, 136], c2: [192, 204, 220], c3: [16, 38, 96], scale: 8, noise: 6 }
    },
    laser_grid_red: {
      name: 'laser_grid_red',
      label: 'Rejilla Emisora Láser / Contención',
      category: 'tech',
      roughness: 0.25,
      metalness: 0.30,
      tintColor: '#ffffff',
      emissive: '#ff2a2a',
      emissiveIntensity: 1.8,
      normalStrength: 0.40,
      tags: ['laser', 'rojo', 'energia', 'seguridad', 'emisor'],
      pattern: { kind: 'forcefield_grid', c1: [36, 12, 14], c2: [255, 48, 48], scale: 8, noise: 6 }
    },
    crt_screen_blue: {
      name: 'crt_screen_blue',
      label: 'Monitor CRT Diagnóstico Azul',
      category: 'tech',
      roughness: 0.22,
      metalness: 0.0,
      tintColor: '#ffffff',
      emissive: '#38b2ff',
      emissiveIntensity: 1.5,
      isDecal: true,
      normalStrength: 0.10,
      tags: ['pantalla', 'crt', 'azul', 'monitor', 'bios', 'diagnostico'],
      pattern: { kind: 'crt_display', c1: [14, 36, 78], c2: [80, 200, 255], param: 1 }
    },
    crt_data_matrix: {
      name: 'crt_data_matrix',
      label: 'Pantalla Terminal Matriz de Datos',
      category: 'tech',
      roughness: 0.20,
      metalness: 0.0,
      tintColor: '#ffffff',
      emissive: '#00ff88',
      emissiveIntensity: 1.6,
      isDecal: true,
      normalStrength: 0.10,
      tags: ['pantalla', 'terminal', 'codigo', 'datos', 'matrix'],
      pattern: { kind: 'crt_display', c1: [8, 28, 18], c2: [40, 255, 140], param: 2 }
    },
    radiation_label: {
      name: 'radiation_label',
      label: 'Cartel Peligro Radiación Nuclear',
      category: 'tech',
      roughness: 0.55,
      metalness: 0.08,
      tintColor: '#ffffff',
      isDecal: true,
      normalStrength: 0.25,
      tags: ['radiacion', 'nuclear', 'cartel', 'peligro', 'etiqueta'],
      pattern: { kind: 'stencil_badge', c1: [232, 184, 20], c2: [24, 24, 24], param: 1 }
    },
    biohazard_label: {
      name: 'biohazard_label',
      label: 'Cartel Riesgo Biológico (Biohazard)',
      category: 'tech',
      roughness: 0.55,
      metalness: 0.08,
      tintColor: '#ffffff',
      isDecal: true,
      normalStrength: 0.25,
      tags: ['biohazard', 'biologico', 'peligro', 'laboratorio', 'cartel'],
      pattern: { kind: 'stencil_badge', c1: [228, 84, 24], c2: [20, 20, 20], param: 2 }
    },
    high_voltage_label: {
      name: 'high_voltage_label',
      label: 'Cartel Alta Tensión Eléctrica',
      category: 'tech',
      roughness: 0.55,
      metalness: 0.08,
      tintColor: '#ffffff',
      isDecal: true,
      normalStrength: 0.25,
      tags: ['electrico', 'alta tension', 'voltaje', 'peligro', 'cartel'],
      pattern: { kind: 'stencil_badge', c1: [236, 236, 236], c2: [204, 32, 32], c3: [24, 24, 24], param: 3 }
    },
    plasma_core_glow: {
      name: 'plasma_core_glow',
      label: 'Núcleo de Plasma / Reactor Emisivo',
      category: 'tech',
      roughness: 0.15,
      metalness: 0.10,
      tintColor: '#ffffff',
      emissive: '#a855f7',
      emissiveIntensity: 2.2,
      normalStrength: 0.30,
      tags: ['plasma', 'reactor', 'energia', 'nucleo', 'emissive'],
      pattern: { kind: 'forcefield_grid', c1: [58, 18, 96], c2: [216, 112, 255], scale: 6, noise: 12 }
    },

    // =========================================================================
    // 7. GLASS & TRANSPARENCIES (6 New Presets)
    // =========================================================================
    frosted_glass: {
      name: 'frosted_glass',
      label: 'Vidrio Esmerilado al Ácido',
      category: 'glass',
      roughness: 0.45,
      metalness: 0.05,
      tintColor: '#d8e8f2',
      transparent: true,
      opacity: 0.68,
      normalStrength: 0.35,
      tags: ['vidrio', 'esmerilado', 'opaco', 'mampara', 'frosted'],
      pattern: { kind: 'frosted_crystal', c1: [210, 226, 236], c2: [184, 204, 218], noise: 18, alpha: 175 }
    },
    cryo_glass_ice: {
      name: 'cryo_glass_ice',
      label: 'Vidrio de Criogenia Escarchado',
      category: 'glass',
      roughness: 0.38,
      metalness: 0.10,
      tintColor: '#a5f3fc',
      transparent: true,
      opacity: 0.62,
      normalStrength: 0.55,
      tags: ['vidrio', 'criogenia', 'hielo', 'escarcha', 'cryo'],
      pattern: { kind: 'frosted_crystal', c1: [164, 232, 248], c2: [224, 248, 255], noise: 24, alpha: 160 }
    },
    amber_lab_glass: {
      name: 'amber_lab_glass',
      label: 'Vidrio Ámbar de Frasco Químico',
      category: 'glass',
      roughness: 0.08,
      metalness: 0.08,
      tintColor: '#d97706',
      transparent: true,
      opacity: 0.55,
      normalStrength: 0.10,
      tags: ['vidrio', 'ambar', 'quimico', 'frasco', 'laboratorio'],
      pattern: { kind: 'frosted_crystal', c1: [196, 112, 24], c2: [148, 76, 12], noise: 6, alpha: 140 }
    },
    hologram_amber: {
      name: 'hologram_amber',
      label: 'Holograma Táctico Ámbar / Alerta',
      category: 'glass',
      roughness: 0.20,
      metalness: 0.0,
      tintColor: '#ff9900',
      emissive: '#ff9900',
      emissiveIntensity: 2.0,
      transparent: true,
      opacity: 0.60,
      normalStrength: 0.15,
      tags: ['holograma', 'ambar', 'naranja', 'alerta', 'hud'],
      pattern: { kind: 'forcefield_grid', c1: [120, 56, 8], c2: [255, 168, 24], scale: 6, noise: 8, alpha: 155 }
    },
    forcefield_hex: {
      name: 'forcefield_hex',
      label: 'Campo de Fuerza Hexagonal Energético',
      category: 'glass',
      roughness: 0.15,
      metalness: 0.0,
      tintColor: '#38bdf8',
      emissive: '#0ea5e9',
      emissiveIntensity: 2.2,
      transparent: true,
      opacity: 0.52,
      normalStrength: 0.35,
      tags: ['campo de fuerza', 'escudo', 'hexagonal', 'energia', 'forcefield'],
      pattern: { kind: 'hex_honeycomb', c1: [14, 72, 128], c2: [80, 224, 255], scale: 8, noise: 6, alpha: 135 }
    },
    visor_gold_mirror: {
      name: 'visor_gold_mirror',
      label: 'Visor Dorado Reflectivo de Traje Espacial',
      category: 'glass',
      roughness: 0.10,
      metalness: 0.85,
      tintColor: '#fbbf24',
      transparent: true,
      opacity: 0.78,
      normalStrength: 0.10,
      tags: ['visor', 'dorado', 'astronauta', 'casco', 'espacial'],
      pattern: { kind: 'brushed_metal', c1: [242, 186, 42], c2: [196, 138, 18], noise: 5, alpha: 200 }
    },

    // =========================================================================
    // 8. FABRICS, LEATHER, PAPER & WEATHERED SURFACES (14 New Presets)
    // =========================================================================
    kevlar_ballistic: {
      name: 'kevlar_ballistic',
      label: 'Tejido Kevlar / Aramida Balística',
      category: 'fabrics_organic',
      roughness: 0.72,
      metalness: 0.08,
      tintColor: '#ffffff',
      normalStrength: 0.75,
      tags: ['kevlar', 'tela', 'balistico', 'chaleco', 'blindaje'],
      pattern: { kind: 'carbon_weave', c1: [198, 164, 58], c2: [148, 118, 36], scale: 4, noise: 10 }
    },
    canvas_military: {
      name: 'canvas_military',
      label: 'Lona Militar Impermeable de Carga',
      category: 'fabrics_organic',
      roughness: 0.88,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.70,
      tags: ['lona', 'tela', 'militar', 'carpa', 'bolso', 'canvas'],
      pattern: { kind: 'woven_fabric', c1: [88, 96, 68], c2: [66, 72, 50], scale: 2, noise: 12 }
    },
    quilted_padding_white: {
      name: 'quilted_padding_white',
      label: 'Acolchado Térmico Espacial Blanco (Beta Cloth)',
      category: 'fabrics_organic',
      roughness: 0.68,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['acolchado', 'tapizado', 'termico', 'espacial', 'capitone'],
      pattern: { kind: 'quilted_padded', c1: [228, 230, 234], c2: [148, 154, 162], scale: 12, noise: 8 }
    },
    quilted_padding_orange: {
      name: 'quilted_padding_orange',
      label: 'Tapizado Acolchado Naranja Industrial',
      category: 'fabrics_organic',
      roughness: 0.70,
      metalness: 0.04,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['acolchado', 'naranja', 'asiento', 'cabina', 'tapizado'],
      pattern: { kind: 'quilted_padded', c1: [214, 98, 34], c2: [128, 52, 16], scale: 12, noise: 10 }
    },
    synthetic_mesh: {
      name: 'synthetic_mesh',
      label: 'Malla Textil Sintética Transpirable',
      category: 'fabrics_organic',
      roughness: 0.82,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.75,
      tags: ['malla', 'tela', 'asiento', 'silla', 'sintetico'],
      pattern: { kind: 'perforated_grid', c1: [58, 64, 72], c2: [24, 28, 34], scale: 4, noise: 8 }
    },
    leather_black_worn: {
      name: 'leather_black_worn',
      label: 'Cuero Negro Gastado de Butaca',
      category: 'fabrics_organic',
      roughness: 0.54,
      metalness: 0.06,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['cuero', 'negro', 'asiento', 'sillon', 'leather'],
      pattern: { kind: 'leather_grain', c1: [38, 38, 42], c2: [20, 20, 24], noise: 14 }
    },
    leather_brown_aged: {
      name: 'leather_brown_aged',
      label: 'Cuero Marrón Envejecido',
      category: 'fabrics_organic',
      roughness: 0.58,
      metalness: 0.05,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['cuero', 'marron', 'valija', 'funda', 'envejecido'],
      pattern: { kind: 'leather_grain', c1: [118, 68, 38], c2: [76, 42, 22], noise: 16 }
    },
    cardboard_corrugated: {
      name: 'cardboard_corrugated',
      label: 'Cartón Corrugado de Caja de Embalaje',
      category: 'fabrics_organic',
      roughness: 0.86,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.60,
      tags: ['carton', 'caja', 'embalaje', 'paquete', 'cardboard'],
      pattern: { kind: 'corrugated_ridges', c1: [188, 148, 98], c2: [154, 118, 74], scale: 4, noise: 14 }
    },
    blueprint_paper: {
      name: 'blueprint_paper',
      label: 'Papel Técnico / Plano Cianotipo (Blueprint)',
      category: 'fabrics_organic',
      roughness: 0.78,
      metalness: 0.0,
      tintColor: '#ffffff',
      isDecal: true,
      normalStrength: 0.20,
      tags: ['papel', 'plano', 'blueprint', 'mapa', 'documento'],
      pattern: { kind: 'blueprint_grid', c1: [26, 78, 148], c2: [218, 236, 255], scale: 8, noise: 6 }
    },
    duct_tape_silver: {
      name: 'duct_tape_silver',
      label: 'Cinta Adhesiva Entelada Gris (Duct Tape)',
      category: 'fabrics_organic',
      roughness: 0.42,
      metalness: 0.35,
      tintColor: '#ffffff',
      normalStrength: 0.45,
      tags: ['cinta', 'duct tape', 'reparacion', 'gris', 'adhesiva'],
      pattern: { kind: 'woven_fabric', c1: [168, 174, 180], c2: [144, 150, 156], scale: 2, noise: 8 }
    },
    kapton_gold_foil: {
      name: 'kapton_gold_foil',
      label: 'Aislamiento Térmico Dorado (Mylar / Kapton)',
      category: 'fabrics_organic',
      roughness: 0.24,
      metalness: 0.88,
      tintColor: '#ffffff',
      normalStrength: 0.75,
      tags: ['mylar', 'kapton', 'dorado', 'satelite', 'termico', 'foil'],
      pattern: { kind: 'quilted_padded', c1: [236, 172, 28], c2: [168, 108, 12], scale: 8, noise: 14 }
    },
    moss_biological: {
      name: 'moss_biological',
      label: 'Superficie con Moho y Humedad Biológica',
      category: 'fabrics_organic',
      roughness: 0.94,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['moho', 'musgo', 'humedad', 'organico', 'contaminacion'],
      pattern: { kind: 'organic_weathering', c1: [64, 88, 48], c2: [38, 52, 28], c3: [96, 112, 62], noise: 24 }
    },
    ash_dust_coating: {
      name: 'ash_dust_coating',
      label: 'Superficie Cubierta de Polvo / Ceniza',
      category: 'fabrics_organic',
      roughness: 0.96,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.65,
      tags: ['polvo', 'ceniza', 'suciedad', 'abandonado', 'ash'],
      pattern: { kind: 'organic_weathering', c1: [134, 130, 124], c2: [96, 92, 88], c3: [164, 160, 154], noise: 22 }
    },
    soil_mud_packed: {
      name: 'soil_mud_packed',
      label: 'Tierra / Barro Seco Compactado',
      category: 'fabrics_organic',
      roughness: 0.94,
      metalness: 0.0,
      tintColor: '#ffffff',
      normalStrength: 0.85,
      tags: ['tierra', 'barro', 'suelo', 'lodo', 'terreno'],
      pattern: { kind: 'cracked_masonry', c1: [98, 72, 48], c2: [48, 34, 22], c3: [122, 92, 64], noise: 24 }
    }
  };

  /**
   * Curated Parametric Material Variants that reuse existing procedural textures
   * with specialized color tints, roughness/metalness calibrations, UV transforms, and wear levels.
   * Zero additional pixel storage required.
   */
  public static readonly PARAMETRIC_VARIANTS: Record<string, ParametricMaterialVariant> = {
    // Metals variants
    steel_blue_tempered: {
      id: 'steel_blue_tempered',
      label: 'Acero Templado Azulado',
      category: 'metals',
      basePreset: 'metal_light_brushed',
      tintColor: '#90cdf4',
      roughness: 0.30,
      metalness: 0.88,
      tags: ['acero', 'templado', 'azul', 'metal']
    },
    steel_blackened_gunmetal: {
      id: 'steel_blackened_gunmetal',
      label: 'Acero Pavonado Oscuro (Gunmetal)',
      category: 'metals',
      basePreset: 'metal_light_brushed',
      tintColor: '#4a5568',
      roughness: 0.36,
      metalness: 0.86,
      tags: ['gunmetal', 'pavonado', 'oscuro', 'armamento']
    },
    aluminum_red_anodized: {
      id: 'aluminum_red_anodized',
      label: 'Aluminio Anodizado Rojo',
      category: 'metals',
      basePreset: 'aluminum_anodized',
      tintColor: '#f56565',
      roughness: 0.32,
      metalness: 0.84,
      tags: ['aluminio', 'anodizado', 'rojo']
    },
    aluminum_blue_anodized: {
      id: 'aluminum_blue_anodized',
      label: 'Aluminio Anodizado Azul Cobalto',
      category: 'metals',
      basePreset: 'aluminum_anodized',
      tintColor: '#4299e1',
      roughness: 0.32,
      metalness: 0.84,
      tags: ['aluminio', 'anodizado', 'azul']
    },
    diamond_plate_rusted: {
      id: 'diamond_plate_rusted',
      label: 'Chapa Diamantada Oxidada',
      category: 'metals',
      basePreset: 'diamond_plate',
      tintColor: '#d69e2e',
      roughness: 0.68,
      metalness: 0.55,
      wear: 0.55,
      tags: ['chapa', 'diamantada', 'oxidada', 'piso']
    },
    copper_aged_dark: {
      id: 'copper_aged_dark',
      label: 'Cobre Oscurecido Térmico',
      category: 'metals',
      basePreset: 'copper_polished',
      tintColor: '#9c4221',
      roughness: 0.45,
      metalness: 0.78,
      wear: 0.35,
      tags: ['cobre', 'oscuro', 'caldera']
    },
    // Construction variants
    concrete_wet_dark: {
      id: 'concrete_wet_dark',
      label: 'Hormigón Húmedo Oscuro',
      category: 'construction',
      basePreset: 'concrete_rough',
      tintColor: '#718096',
      roughness: 0.45,
      metalness: 0.08,
      tags: ['hormigon', 'humedo', 'mojado']
    },
    brick_whitewashed: {
      id: 'brick_whitewashed',
      label: 'Ladrillo Visto Pintado de Blanco',
      category: 'construction',
      basePreset: 'brick_red',
      tintColor: '#edf2f7',
      roughness: 0.82,
      metalness: 0.02,
      wear: 0.25,
      tags: ['ladrillo', 'blanco', 'pintado']
    },
    ceramic_tile_hospital_green: {
      id: 'ceramic_tile_hospital_green',
      label: 'Azulejo Sanitario Verde Quirófano',
      category: 'construction',
      basePreset: 'ceramic_tile_white',
      tintColor: '#9ae6b4',
      roughness: 0.22,
      metalness: 0.05,
      tags: ['azulejo', 'verde', 'hospital', 'laboratorio']
    },
    corrugated_rusted_roof: {
      id: 'corrugated_rusted_roof',
      label: 'Chapa Acanalada Oxidada de Galpón',
      category: 'construction',
      basePreset: 'corrugated_metal',
      tintColor: '#c05621',
      roughness: 0.78,
      metalness: 0.35,
      wear: 0.65,
      tags: ['chapa', 'acanalada', 'oxidada', 'techo']
    },
    // Woods variants
    wood_cherry_red: {
      id: 'wood_cherry_red',
      label: 'Madera de Cerezo Rojizo',
      category: 'woods',
      basePreset: 'wood_oak',
      tintColor: '#e53e3e',
      roughness: 0.45,
      metalness: 0.02,
      tags: ['madera', 'cerezo', 'rojizo']
    },
    wood_weathered_grey: {
      id: 'wood_weathered_grey',
      label: 'Madera Grisácea a la Intemperie',
      category: 'woods',
      basePreset: 'wood_rustic_planks',
      tintColor: '#a0aec0',
      roughness: 0.88,
      metalness: 0.0,
      wear: 0.50,
      tags: ['madera', 'gris', 'intemperie', 'muelle']
    },
    // Stones variants
    marble_emerald_green: {
      id: 'marble_emerald_green',
      label: 'Mármol Verde Esmeralda Imperial',
      category: 'stones',
      basePreset: 'marble_white',
      tintColor: '#48bb78',
      roughness: 0.20,
      metalness: 0.08,
      tags: ['marmol', 'verde', 'esmeralda']
    },
    crystal_amethyst_purple: {
      id: 'crystal_amethyst_purple',
      label: 'Cristal de Amatista Violeta',
      category: 'stones',
      basePreset: 'quartz_crystal',
      tintColor: '#b794f4',
      roughness: 0.22,
      metalness: 0.18,
      tags: ['amatista', 'cristal', 'violeta', 'mineral']
    },
    // Plastics variants
    plastic_cyber_yellow: {
      id: 'plastic_cyber_yellow',
      label: 'Polímero ABS Amarillo Ciberpunk',
      category: 'plastics',
      basePreset: 'plastic_abs_matte',
      tintColor: '#f6e05e',
      roughness: 0.45,
      metalness: 0.05,
      tags: ['plastico', 'amarillo', 'cyberpunk']
    },
    plastic_medical_white: {
      id: 'plastic_medical_white',
      label: 'Plástico Clínico Antibacterial Blanco',
      category: 'plastics',
      basePreset: 'plastic_abs_matte',
      tintColor: '#f7fafc',
      roughness: 0.35,
      metalness: 0.04,
      tags: ['plastico', 'blanco', 'medico', 'clinico']
    },
    // Tech variants
    carbon_fiber_gold_weave: {
      id: 'carbon_fiber_gold_weave',
      label: 'Fibra de Carbono Híbrida con Hilo de Oro',
      category: 'tech',
      basePreset: 'carbon_fiber',
      tintColor: '#ecc94b',
      roughness: 0.26,
      metalness: 0.55,
      tags: ['carbono', 'oro', 'compuesto']
    },
    hologram_green_tactical: {
      id: 'hologram_green_tactical',
      label: 'Holograma Táctico Verde Esmeralda',
      category: 'glass',
      basePreset: 'hologram_cyan',
      tintColor: '#48bb78',
      emissive: '#38a169',
      emissiveIntensity: 2.0,
      roughness: 0.20,
      metalness: 0.0,
      transparent: true,
      opacity: 0.60,
      tags: ['holograma', 'verde', 'tactico', 'hud']
    },
    // Fabrics variants
    kevlar_olive_tactical: {
      id: 'kevlar_olive_tactical',
      label: 'Kevlar Táctico Verde Oliva',
      category: 'fabrics_organic',
      basePreset: 'kevlar_ballistic',
      tintColor: '#68d391',
      roughness: 0.76,
      metalness: 0.05,
      tags: ['kevlar', 'verde', 'militar', 'tactico']
    },
    leather_burgundy_luxury: {
      id: 'leather_burgundy_luxury',
      label: 'Cuero Bordó / Borgoña Clásico',
      category: 'fabrics_organic',
      basePreset: 'leather_brown_aged',
      tintColor: '#fc8181',
      roughness: 0.50,
      metalness: 0.06,
      tags: ['cuero', 'bordo', 'rojo', 'butaca']
    }
  };

  /**
   * Historical & semantic aliases mapping legacy or conversational names to canonical presets.
   */
  public static readonly ALIASES: Record<string, TexturePresetName> = {
    // Original aliases (100% preserved)
    metal_plates_rivets: 'metal_dark_grime',
    floor_metal: 'metal_dark_grime',
    rubber_tread: 'rubber_black',
    computer_screen_crt: 'crt_screen_green',
    screen_crt: 'crt_screen_green',
    screen_green: 'crt_screen_green',
    steel_stainless: 'metal_light_brushed',
    control_panel_buttons: 'beige_plastic_worn',
    casing_panel_clean: 'painted_metal_white',
    painted_casing: 'painted_metal_white',
    metal_vent_grate: 'vent_grill',
    vent: 'vent_grill',
    generic_label: 'caution_label',
    stripe_hazard_yellow: 'hazard_stripes',
    hazard_yellow: 'hazard_stripes',
    door_emergency_red: 'red_paint_worn',
    worn_industrial: 'metal_dark_grime',
    metal: 'worn_metal',
    rubber: 'rubber_black',
    screen: 'crt_screen_green',
    hazard: 'hazard_stripes',
    rust: 'rust_heavy',
    plastic: 'beige_plastic_worn',
    glass: 'clean_glass',
    cristal: 'clean_glass',
    vidrio: 'clean_glass',
    ventana: 'clean_glass',
    window: 'clean_glass',
    cockpit_glass: 'tinted_glass',
    visor: 'tinted_glass',
    glass_wire: 'reinforced_glass',
    reinforced: 'reinforced_glass',
    hologram: 'hologram_cyan',
    holograma: 'hologram_cyan',
    hud: 'hologram_cyan',

    // New conversational & Spanish/English aliases for AI & user scripts
    acero: 'steel_polished',
    steel: 'steel_polished',
    hierro: 'iron_cast',
    iron: 'iron_cast',
    aluminio: 'aluminum_anodized',
    aluminum: 'aluminum_anodized',
    cobre: 'copper_polished',
    copper: 'copper_polished',
    bronce: 'bronze_antique',
    bronze: 'bronze_antique',
    laton: 'brass_burnished',
    brass: 'brass_burnished',
    titanio: 'titanium_aerospace',
    titanium: 'titanium_aerospace',
    oro: 'gold_contacts',
    gold: 'gold_contacts',
    cromo: 'chrome_mirror',
    chrome: 'chrome_mirror',
    hormigon: 'concrete_smooth',
    concreto: 'concrete_smooth',
    concrete: 'concrete_smooth',
    cemento: 'concrete_rough',
    ladrillo: 'brick_red',
    brick: 'brick_red',
    brick_wall: 'brick_red',
    asfalto: 'asphalt_road',
    asphalt: 'asphalt_road',
    baldosa: 'ceramic_tile_white',
    tile: 'ceramic_tile_white',
    madera: 'wood_oak',
    wood: 'wood_oak',
    oak_wood: 'wood_oak',
    roble: 'wood_oak',
    pino: 'wood_pine',
    nogal: 'wood_walnut',
    plywood: 'wood_plywood',
    parquet: 'wood_parquet',
    piedra: 'granite_grey',
    stone: 'granite_grey',
    granito: 'granite_grey',
    marmol: 'marble_white',
    marble: 'marble_white',
    pizarra: 'slate_layered',
    roca: 'basalt_lunar',
    arena: 'sand_compacted',
    sand: 'sand_compacted',
    grava: 'gravel_mineral',
    cuarzo: 'quartz_crystal',
    obsidiana: 'obsidian_volcanic',
    pcb: 'pcb_green_gold',
    circuito: 'pcb_green_gold',
    carbon: 'carbon_fiber',
    fibra_carbono: 'carbon_fiber',
    solar: 'solar_panel_blue',
    panel_solar: 'solar_panel_blue',
    kevlar: 'kevlar_ballistic',
    lona: 'canvas_military',
    canvas: 'canvas_military',
    cuero: 'leather_black_worn',
    leather: 'leather_black_worn',
    carton: 'cardboard_corrugated',
    cardboard: 'cardboard_corrugated',
    blueprint: 'blueprint_paper',
    moho: 'moss_biological',
    barro: 'soil_mud_packed'
  };

  /**
   * Resolves a texture preset name (or parametric variant ID or alias) to its canonical TexturePresetName.
   */
  public static resolvePresetName(rawName?: string): TexturePresetName | null {
    if (!rawName) return null;
    const clean = rawName.toLowerCase().trim();
    if (this.PROFILES[clean as TexturePresetName]) {
      return clean as TexturePresetName;
    }
    if (this.PARAMETRIC_VARIANTS[clean]) {
      return this.PARAMETRIC_VARIANTS[clean].basePreset;
    }
    if (this.ALIASES[clean]) {
      return this.ALIASES[clean];
    }
    return null;
  }

  /**
   * Returns a parametric variant descriptor if rawName matches one.
   */
  public static getParametricVariant(rawName?: string): ParametricMaterialVariant | null {
    if (!rawName) return null;
    const clean = rawName.toLowerCase().trim();
    return this.PARAMETRIC_VARIANTS[clean] || null;
  }

  /**
   * Checks if a texture instance belongs to the shared preset library (BaseColor, Normal, or Roughness).
   */
  public static isPresetTexture(tex?: THREE.Texture | null): boolean {
    if (!tex) return false;
    return this.presetTextures.has(tex);
  }

  /**
   * Lists all canonical profiles grouped or filtered by category and search query.
   */
  public static getProfilesByCategory(category?: MaterialFamilyCategory | 'all', searchQuery?: string): TexturePresetProfile[] {
    const q = (searchQuery || '').toLowerCase().trim();
    return Object.values(this.PROFILES).filter((p) => {
      if (category && category !== 'all' && p.category !== category) {
        return false;
      }
      if (!q) return true;
      const inName = p.name.toLowerCase().includes(q);
      const inLabel = p.label.toLowerCase().includes(q);
      const inTags = (p.tags || []).some((t) => t.toLowerCase().includes(q));
      return inName || inLabel || inTags;
    });
  }

  /**
   * Retrieves or creates a cached Three.js DataTexture (BaseColor) for the given preset and optional wear level.
   */
  public static getTexture(preset: TexturePresetName, wearLevel = 0): THREE.DataTexture {
    const wearStep = wearLevel > 0.02 ? Math.min(20, Math.round(wearLevel * 20)) : 0;
    const cacheKey = wearStep > 0 ? `${preset}__wear_${wearStep}` : preset;

    if (this.textures.has(cacheKey)) {
      return this.textures.get(cacheKey)!;
    }

    const size = 64;
    const pixels = new Uint8Array(size * size * 4);
    this.generatePixelsForPreset(preset, pixels, size, size);

    if (wearStep > 0) {
      this.applyParametricWear(preset, pixels, size, size, wearStep / 20);
    }

    const tex = new THREE.DataTexture(pixels, size, size, THREE.RGBAFormat);
    tex.name = `T_${preset}${wearStep > 0 ? `_w${wearStep}` : ''}`;
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.NearestFilter;
    tex.generateMipmaps = false;
    tex.needsUpdate = true;

    this.textures.set(cacheKey, tex);
    this.presetTextures.add(tex);
    return tex;
  }

  /**
   * Generates or retrieves a cached 64x64 tangent-space Normal Map derived from the preset's luminance relief.
   */
  public static getNormalTexture(preset: TexturePresetName, strength = 0.55): THREE.DataTexture {
    const step = Math.round(strength * 20);
    const cacheKey = `${preset}__norm_${step}`;
    if (this.normalTextures.has(cacheKey)) {
      return this.normalTextures.get(cacheKey)!;
    }

    const baseTex = this.getTexture(preset, 0);
    const src = baseTex.image.data as Uint8Array;
    const size = 64;
    const normPixels = new Uint8Array(size * size * 4);

    const getHeight = (x: number, y: number): number => {
      const wx = ((x % size) + size) % size;
      const wy = ((y % size) + size) % size;
      const idx = (wy * size + wx) * 4;
      return (src[idx] * 0.299 + src[idx + 1] * 0.587 + src[idx + 2] * 0.114) / 255;
    };

    const invZ = 1.0 / Math.max(0.15, strength * 3.2);

    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        // Sobel gradient filter on wrapped tile coordinates
        const tl = getHeight(x - 1, y - 1);
        const t  = getHeight(x,     y - 1);
        const tr = getHeight(x + 1, y - 1);
        const l  = getHeight(x - 1, y);
        const r  = getHeight(x + 1, y);
        const bl = getHeight(x - 1, y + 1);
        const b  = getHeight(x,     y + 1);
        const br = getHeight(x + 1, y + 1);

        const dX = (tr + 2 * r + br) - (tl + 2 * l + bl);
        const dY = (bl + 2 * b + br) - (tl + 2 * t + tr);
        const dZ = invZ;

        const len = Math.sqrt(dX * dX + dY * dY + dZ * dZ) || 1;
        const nx = -dX / len;
        const ny = -dY / len;
        const nz = dZ / len;

        const idx = (y * size + x) * 4;
        normPixels[idx + 0] = Math.min(255, Math.max(0, Math.round((nx * 0.5 + 0.5) * 255)));
        normPixels[idx + 1] = Math.min(255, Math.max(0, Math.round((ny * 0.5 + 0.5) * 255)));
        normPixels[idx + 2] = Math.min(255, Math.max(128, Math.round((nz * 0.5 + 0.5) * 255)));
        normPixels[idx + 3] = 255;
      }
    }

    const normTex = new THREE.DataTexture(normPixels, size, size, THREE.RGBAFormat);
    normTex.name = `N_${preset}_s${step}`;
    normTex.wrapS = THREE.RepeatWrapping;
    normTex.wrapT = THREE.RepeatWrapping;
    normTex.magFilter = THREE.NearestFilter;
    normTex.minFilter = THREE.NearestFilter;
    normTex.generateMipmaps = false;
    normTex.needsUpdate = true;

    this.normalTextures.set(cacheKey, normTex);
    this.presetTextures.add(normTex);
    return normTex;
  }

  /**
   * Generates a compact 48x48 preview data URL (WebP/PNG) lazily on demand for the Studio Material Browser.
   */
  public static getThumbnailDataURL(presetOrVariant: string): string {
    if (this.thumbnailCache.has(presetOrVariant)) {
      return this.thumbnailCache.get(presetOrVariant)!;
    }

    const presetName = this.resolvePresetName(presetOrVariant) || 'worn_metal';
    const variant = this.getParametricVariant(presetOrVariant);
    const profile = this.PROFILES[presetName];
    const tex = this.getTexture(presetName, variant?.wear ?? 0);
    const src = tex.image.data as Uint8Array;

    if (typeof document === 'undefined') {
      return '';
    }

    const canvas = document.createElement('canvas');
    canvas.width = 48;
    canvas.height = 48;
    const ctx = canvas.getContext('2d');
    if (!ctx || typeof ctx.createImageData !== 'function') {
      return '';
    }

    const tintHex = variant?.tintColor || profile.tintColor || '#ffffff';
    const tint = new THREE.Color(tintHex);
    const imgData = ctx.createImageData(48, 48);
    const dst = imgData.data;

    for (let y = 0; y < 48; y++) {
      for (let x = 0; x < 48; x++) {
        const sx = Math.floor((x / 48) * 64);
        const sy = Math.floor((y / 48) * 64);
        const sIdx = (sy * 64 + sx) * 4;
        const dIdx = (y * 48 + x) * 4;

        // Subtle diagonal lighting sheen to preview metallic/roughness character
        const diag = (x + y) / 96;
        const sheen = (variant?.metalness ?? profile.metalness) * Math.exp(-Math.pow((diag - 0.45) * 4.5, 2)) * 42;

        dst[dIdx + 0] = Math.min(255, Math.round(src[sIdx + 0] * tint.r + sheen));
        dst[dIdx + 1] = Math.min(255, Math.round(src[sIdx + 1] * tint.g + sheen));
        dst[dIdx + 2] = Math.min(255, Math.round(src[sIdx + 2] * tint.b + sheen));
        dst[dIdx + 3] = src[sIdx + 3];
      }
    }

    ctx.putImageData(imgData, 0, 0);
    let dataUrl = '';
    try {
      dataUrl = canvas.toDataURL('image/webp', 0.85);
      if (!dataUrl.startsWith('data:image/')) {
        dataUrl = canvas.toDataURL('image/png');
      }
    } catch {
      dataUrl = '';
    }

    if (dataUrl) {
      this.thumbnailCache.set(presetOrVariant, dataUrl);
    }
    return dataUrl;
  }

  /**
   * Builds an authentic PS1 / PBR Three.js MeshStandardMaterial for a component.
   */
  public static getMaterial(comp: ComponentDef, baseColor: THREE.Color): THREE.MeshStandardMaterial {
    if (comp.texturePreset && (comp.texturePreset.startsWith('local:') || comp.texturePreset.startsWith('custom:') || this.customTextures.has(comp.texturePreset))) {
      const texKey = comp.texturePreset.replace(/^(local|custom):/, '');
      const customTex = this.customTextures.get(texKey) || this.customTextures.get(comp.texturePreset);
      if (customTex) {
        if (comp.uvScale) {
          customTex.repeat.set(comp.uvScale[0], comp.uvScale[1]);
        }
        const cleanCustomKey = texKey.replace(/[^a-zA-Z0-9_]/g, '_');
        customTex.name = `T_custom_${cleanCustomKey}`;
        const matCustomKey = `custom_${cleanCustomKey}_${comp.color || 'def'}_${comp.roughness ?? 0.6}_${comp.metalness ?? 0.2}_${Boolean(comp.wireframe)}`;
        if (this.materialCache.has(matCustomKey)) {
          return this.materialCache.get(matCustomKey)!;
        }
        const customMat = new THREE.MeshStandardMaterial({
          name: `M_custom_${cleanCustomKey}`,
          color: comp.color && !comp.color.startsWith('default') ? baseColor : new THREE.Color('#ffffff'),
          roughness: comp.roughness ?? 0.6,
          metalness: comp.metalness ?? 0.2,
          flatShading: false,
          map: customTex,
          wireframe: Boolean(comp.wireframe),
          transparent: Boolean(comp.transparent || (comp.opacity !== undefined && comp.opacity < 1.0)),
          opacity: comp.opacity ?? 1.0
        });
        this.materialCache.set(matCustomKey, customMat);
        return customMat;
      }
    }

    const presetName = this.resolvePresetName(comp.texturePreset);
    if (!presetName) {
      // Legacy color-only material
      const colHex = baseColor.getHexString();
      const legacyKey = `legacy_${colHex}_${comp.roughness ?? 0.75}_${comp.metalness ?? 0.25}_${Boolean(comp.wireframe)}`;
      if (this.materialCache.has(legacyKey)) {
        return this.materialCache.get(legacyKey)!;
      }
      const legacyMat = new THREE.MeshStandardMaterial({
        name: `M_solid_${colHex}`,
        color: baseColor,
        roughness: comp.roughness ?? 0.75,
        metalness: comp.metalness ?? 0.25,
        flatShading: true,
        vertexColors: true,
        wireframe: Boolean(comp.wireframe)
      });
      this.materialCache.set(legacyKey, legacyMat);
      return legacyMat;
    }

    const variant = this.getParametricVariant(comp.texturePreset);
    const profile = this.PROFILES[presetName];
    const wearAmount = Math.max(0, Math.min(1, comp.wear ?? variant?.wear ?? 0));
    const texture = this.getTexture(presetName, wearAmount);

    // Determine material color tint
    let matColor: THREE.Color;
    if (comp.color && !comp.color.startsWith('default')) {
      matColor = baseColor;
    } else if (variant?.tintColor) {
      matColor = new THREE.Color(variant.tintColor);
    } else {
      matColor = new THREE.Color(profile.tintColor);
    }

    const isTransp = Boolean(
      comp.transparent ||
      variant?.transparent ||
      profile.transparent ||
      (comp.opacity !== undefined && comp.opacity < 1.0)
    );
    const targetOpacity = comp.opacity !== undefined
      ? Math.max(0.0, Math.min(1.0, comp.opacity))
      : (variant?.opacity ?? profile.opacity ?? 1.0);

    const baseRoughness = comp.roughness ?? variant?.roughness ?? profile.roughness;
    const baseMetalness = comp.metalness ?? variant?.metalness ?? profile.metalness;
    // If wear > 0 and user didn't hard-override roughness, slightly roughen weathered surfaces
    const effectiveRoughness = comp.roughness !== undefined
      ? baseRoughness
      : Math.min(1.0, baseRoughness + wearAmount * 0.14);

    const normStrength = comp.normalStrength ?? profile.normalStrength ?? 0.5;
    const hasNorm = normStrength > 0.05 && !isTransp;
    const emissiveHex = comp.emissive ?? variant?.emissive ?? profile.emissive;
    const emissiveIntensity = comp.emissiveIntensity ?? variant?.emissiveIntensity ?? profile.emissiveIntensity ?? 1.5;
    const isWireframe = Boolean(comp.wireframe);

    // Deduplication cache key: share identical PBR materials across multiple components
    const cleanPreset = presetName.replace(/[^a-zA-Z0-9_]/g, '_');
    const matKey = `${cleanPreset}__c_${matColor.getHexString()}__r_${effectiveRoughness.toFixed(2)}__m_${baseMetalness.toFixed(2)}__w_${wearAmount.toFixed(2)}__n_${hasNorm ? normStrength.toFixed(2) : '0'}__e_${emissiveHex || '0'}_${emissiveHex ? emissiveIntensity.toFixed(1) : '0'}__o_${isTransp ? targetOpacity.toFixed(2) : '1'}__wf_${isWireframe}`;

    if (this.materialCache.has(matKey)) {
      return this.materialCache.get(matKey)!;
    }

    const mat = new THREE.MeshStandardMaterial({
      name: `M_${cleanPreset}_${matColor.getHexString()}`,
      map: texture,
      color: matColor,
      roughness: effectiveRoughness,
      metalness: baseMetalness,
      flatShading: true,
      vertexColors: false, // Pure crisp texture rendering
      wireframe: isWireframe,
      transparent: isTransp,
      opacity: targetOpacity,
      depthWrite: isTransp && targetOpacity < 0.9 ? false : true,
      side: isTransp ? THREE.DoubleSide : THREE.FrontSide
    });

    // Attach procedural Normal Map for surface relief (strength baked into normal map so normalScale stays 1,1 for fast GLB export)
    if (hasNorm) {
      mat.normalMap = this.getNormalTexture(presetName, normStrength);
    }

    // Emissive setup for CRTs, holograms, energy minerals and lit indicators
    if (emissiveHex) {
      mat.emissive = new THREE.Color(emissiveHex);
      mat.emissiveIntensity = emissiveIntensity;
    }

    this.materialCache.set(matKey, mat);
    return mat;
  }

  /**
   * Blends procedural edge chipping, oxidation, and grime onto an existing RGBA pixel buffer.
   */
  private static applyParametricWear(
    preset: string,
    pixels: Uint8Array,
    w: number,
    h: number,
    wear: number
  ): void {
    const rng = this.createRNG(preset.length * 1337 + Math.round(wear * 100));
    const edgeBand = Math.max(2, Math.round(2 + wear * 5));

    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const idx = (y * w + x) * 4;
        const edgeDist = Math.min(x, w - 1 - x, y, h - 1 - y);
        const isEdge = edgeDist < edgeBand;

        // Edge chipping & crevice darkening
        if (isEdge && rng() < wear * 0.55) {
          pixels[idx + 0] = Math.round(pixels[idx + 0] * 0.55 + 24);
          pixels[idx + 1] = Math.round(pixels[idx + 1] * 0.52 + 20);
          pixels[idx + 2] = Math.round(pixels[idx + 2] * 0.48 + 18);
        } else if (rng() < wear * 0.18) {
          // Surface oxidation / dust speckles
          const isRust = rng() < 0.5;
          if (isRust) {
            pixels[idx + 0] = Math.round(pixels[idx + 0] * (1 - wear * 0.5) + 128 * (wear * 0.5));
            pixels[idx + 1] = Math.round(pixels[idx + 1] * (1 - wear * 0.5) + 64 * (wear * 0.5));
            pixels[idx + 2] = Math.round(pixels[idx + 2] * (1 - wear * 0.5) + 32 * (wear * 0.5));
          } else {
            const grime = 0.68 + rng() * 0.15;
            pixels[idx + 0] = Math.round(pixels[idx + 0] * grime);
            pixels[idx + 1] = Math.round(pixels[idx + 1] * grime);
            pixels[idx + 2] = Math.round(pixels[idx + 2] * grime);
          }
        }
      }
    }
  }

  /**
   * Generates procedural low-res 64x64 RGBA pixel art for each canonical preset.
   */
  private static generatePixelsForPreset(
    preset: TexturePresetName,
    pixels: Uint8Array,
    w: number,
    h: number
  ): void {
    const profile = this.PROFILES[preset];
    if (profile?.pattern && profile.pattern.kind !== 'legacy_switch') {
      this.synthesizePatternPixels(preset, profile.pattern, pixels, w, h);
      return;
    }

    const rng = this.createRNG(preset.split('').reduce((acc, c) => acc + c.charCodeAt(0), 42));

    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const idx = (y * w + x) * 4;
        let r = 0, g = 0, b = 0, a = 255;

        switch (preset) {
          case 'worn_metal':
          case 'metal_dark_grime': {
            const base = preset === 'worn_metal' ? 62 : 48;
            const noise = (rng() - 0.5) * 16;
            const val = Math.max(10, Math.min(245, base + noise));
            r = val;
            g = val * 1.04;
            b = val * 1.08;

            if (rng() < 0.05) {
              r = 95 + rng() * 30;
              g = 48 + rng() * 15;
              b = 20 + rng() * 10;
            }

            if (x < 2 || x >= w - 2 || y < 2 || y >= h - 2) {
              r *= 0.65; g *= 0.65; b *= 0.65;
            }
            break;
          }

          case 'metal_light_brushed': {
            const lineBrightness = 160 + ((y * 11) % 23) * 1.8 + (rng() - 0.5) * 14;
            r = lineBrightness * 0.95;
            g = lineBrightness * 0.98;
            b = lineBrightness * 1.05;
            if (rng() < 0.03) {
              r *= 0.75; g *= 0.75; b *= 0.78;
            }
            break;
          }

          case 'painted_metal_white': {
            const noise = (rng() - 0.5) * 12;
            const val = 215 + noise;
            r = val; g = val * 1.01; b = val * 1.02;

            const isEdge = x < 3 || x >= w - 3 || y < 3 || y >= h - 3;
            if (isEdge && rng() < 0.15) {
              r = 52; g = 54; b = 58;
            }
            break;
          }

          case 'beige_plastic_worn': {
            const noise = (rng() - 0.5) * 10;
            r = 184 + noise;
            g = 179 + noise * 0.95;
            b = 158 + noise * 0.85;

            if (x < 2 || x >= w - 2 || y < 2 || y >= h - 2) {
              r *= 0.75; g *= 0.72; b *= 0.65;
            }
            break;
          }

          case 'rubber_black': {
            const noise = (rng() - 0.5) * 8;
            const val = 30 + noise;
            r = val; g = val; b = val * 1.05;
            break;
          }

          case 'rust_heavy': {
            const cluster = Math.sin(x * 0.15) * Math.cos(y * 0.15) + (rng() - 0.5) * 0.8;
            if (cluster > 0.3) {
              r = 180 + rng() * 30;
              g = 80 + rng() * 20;
              b = 25 + rng() * 10;
            } else if (cluster < -0.2) {
              r = 56 + rng() * 15;
              g = 24 + rng() * 10;
              b = 10 + rng() * 5;
            } else {
              r = 125 + rng() * 20;
              g = 48 + rng() * 15;
              b = 18 + rng() * 10;
            }
            break;
          }

          case 'hazard_stripes': {
            const stripeWidth = 8;
            const isStripe = Math.floor((x + y) / stripeWidth) % 2 === 0;
            if (isStripe) {
              const grit = 0.95 + rng() * 0.1;
              r = Math.min(255, 225 * grit);
              g = Math.min(255, 175 * grit);
              b = Math.min(255, 20 * grit);
            } else {
              const darkGrit = 26 + rng() * 6;
              r = darkGrit; g = darkGrit; b = darkGrit * 1.05;
            }
            break;
          }

          case 'vent_grill': {
            const slatH = 4;
            const isSlatLit = Math.floor(y / slatH) % 2 === 0;
            if (isSlatLit) {
              const metalGrit = 82 + (rng() - 0.5) * 10;
              r = metalGrit; g = metalGrit * 1.05; b = metalGrit * 1.12;
            } else {
              r = 14; g = 14; b = 16;
            }
            break;
          }

          case 'crt_screen_green': {
            const scanline = y % 2 === 0 ? 1.35 : 0.82;
            let baseG = (28 + rng() * 8) * scanline;
            let baseR = 12 * scanline;
            let baseB = 16 * scanline;

            const waveY = Math.round(32 + Math.sin(x * 0.25) * 8);
            if (Math.abs(y - waveY) <= 1 && x >= 10 && x <= 54) {
              baseR = 70;
              baseG = 245;
              baseB = 100;
            }

            r = Math.min(255, baseR);
            g = Math.min(255, baseG);
            b = Math.min(255, baseB);
            break;
          }

          case 'crt_screen_amber': {
            const scanline = y % 2 === 0 ? 1.35 : 0.82;
            let baseR = (115 + rng() * 12) * scanline;
            let baseG = (58 + rng() * 8) * scanline;
            let baseB = 12 * scanline;

            if (y >= 28 && y <= 30 && x >= 12 && x <= 52) {
              baseR = 250;
              baseG = 165;
              baseB = 25;
            }

            r = Math.min(255, baseR);
            g = Math.min(255, baseG);
            b = Math.min(255, baseB);
            break;
          }

          case 'crt_screen_off': {
            const glare = Math.exp(-Math.pow((x - y) / 10, 2)) * 35;
            r = 16 + glare;
            g = 18 + glare * 1.05;
            b = 22 + glare * 1.15;
            break;
          }

          case 'caution_label': {
            const isBorder = x < 2 || x >= w - 2 || y < 2 || y >= h - 2;
            const isTextBar = (y >= 26 && y <= 28 && x >= 10 && x <= 54) ||
                              (y >= 36 && y <= 38 && x >= 14 && x <= 50);

            if (isBorder || isTextBar) {
              r = 24; g = 24; b = 24;
            } else {
              r = 220; g = 170; b = 15;
            }
            break;
          }

          case 'red_paint_worn': {
            const noise = (rng() - 0.5) * 16;
            r = Math.min(255, 148 + noise);
            g = Math.max(0, 26 + noise * 0.3);
            b = Math.max(0, 20 + noise * 0.2);

            if (rng() < 0.08) {
              r = 75; g = 38; b = 22;
            }
            break;
          }

          case 'tinted_glass': {
            const glare = Math.exp(-Math.pow((x - y * 0.9) / 12, 2)) * 55;
            const noise = (rng() - 0.5) * 8;
            r = Math.min(255, 45 + glare * 0.8 + noise);
            g = Math.min(255, 75 + glare * 0.9 + noise);
            b = Math.min(255, 110 + glare * 1.1 + noise);
            a = Math.min(255, Math.max(30, Math.round(90 + glare * 2.2)));
            break;
          }

          case 'reinforced_glass': {
            const isWire = (x % 8 === 0) || (y % 8 === 0);
            if (isWire) {
              const wireGrit = 70 + (rng() - 0.5) * 14;
              r = wireGrit;
              g = wireGrit * 1.02;
              b = wireGrit * 1.05;
              a = 255;
            } else {
              const glare = Math.exp(-Math.pow((x - y) / 14, 2)) * 40;
              r = Math.min(255, 60 + glare);
              g = Math.min(255, 95 + glare * 1.1);
              b = Math.min(255, 90 + glare * 1.05);
              a = 120;
            }
            break;
          }

          case 'clean_glass': {
            const edgeDist = Math.min(x, w - 1 - x, y, h - 1 - y);
            const edgeSheen = edgeDist < 3 ? (3 - edgeDist) * 35 : 0;
            const noise = (rng() - 0.5) * 4;
            r = Math.min(255, 140 + edgeSheen + noise);
            g = Math.min(255, 190 + edgeSheen + noise);
            b = Math.min(255, 230 + edgeSheen + noise);
            a = Math.min(255, Math.max(20, Math.round(45 + edgeSheen * 1.5)));
            break;
          }

          case 'hologram_cyan': {
            const isScan = y % 3 === 0;
            if (isScan) {
              r = 30;
              g = 245;
              b = 255;
              a = 210;
            } else {
              r = 10;
              g = 110;
              b = 160;
              a = 65;
            }
            break;
          }
        }

        pixels[idx + 0] = Math.round(r);
        pixels[idx + 1] = Math.round(g);
        pixels[idx + 2] = Math.round(b);
        pixels[idx + 3] = a;
      }
    }
  }

  /**
   * Modular Procedural Pattern Synthesizer for the 100 new PBR material presets.
   */
  private static synthesizePatternPixels(
    seedKey: string,
    spec: PatternSynthesisSpec,
    pixels: Uint8Array,
    w: number,
    h: number
  ): void {
    const seed = seedKey.split('').reduce((acc, c, i) => acc + c.charCodeAt(0) * (i + 17), 101);
    const rng = this.createRNG(seed);
    const { c1, c2, c3 = c2, scale = 4, noise = 10, alpha = 255, param = 0.5 } = spec;

    const lerp = (a: number, b: number, t: number) => a + (b - a) * Math.max(0, Math.min(1, t));

    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const idx = (y * w + x) * 4;
        const n = (rng() - 0.5) * noise;
        let r = c1[0], g = c1[1], b = c1[2], a = alpha;

        switch (spec.kind) {
          case 'brushed_metal': {
            const streak = Math.sin((y * scale * 0.7) + Math.sin(x * 0.15) * 1.5) * 0.5 + 0.5;
            const scratch = ((y * 13 + x * 3) % 19 === 0) ? 0.85 : 1.0;
            r = lerp(c1[0], c2[0], streak) * scratch + n;
            g = lerp(c1[1], c2[1], streak) * scratch + n;
            b = lerp(c1[2], c2[2], streak) * scratch + n;
            break;
          }

          case 'galvanized_spangle': {
            const cellX = Math.floor(x / scale);
            const cellY = Math.floor(y / scale);
            const cellHash = ((cellX * 73856093) ^ (cellY * 19349663)) & 0xff;
            const t = (cellHash % 3 === 0) ? 0.85 : (cellHash % 3 === 1 ? 0.2 : 0.5);
            const col = cellHash % 2 === 0 ? c2 : c3;
            r = lerp(c1[0], col[0], t) + n;
            g = lerp(c1[1], col[1], t) + n;
            b = lerp(c1[2], col[2], t) + n;
            break;
          }

          case 'cast_rough': {
            const wave = Math.sin(x * 0.35 * scale) * Math.cos(y * 0.35 * scale) * 0.5 + 0.5;
            r = lerp(c1[0], c2[0], wave) + n * 1.3;
            g = lerp(c1[1], c2[1], wave) + n * 1.3;
            b = lerp(c1[2], c2[2], wave) + n * 1.3;
            break;
          }

          case 'oxidized_patina': {
            const patch = Math.sin(x * 0.14 + Math.cos(y * 0.18) * 2.2) * Math.cos(y * 0.16 - Math.sin(x * 0.12) * 1.8);
            const mask = (patch + 1) * 0.5;
            if (mask < param) {
              const sub = mask / Math.max(0.05, param);
              r = lerp(c2[0], c3[0], sub) + n;
              g = lerp(c2[1], c3[1], sub) + n;
              b = lerp(c2[2], c3[2], sub) + n;
            } else {
              r = c1[0] + n;
              g = c1[1] + n;
              b = c1[2] + n;
            }
            break;
          }

          case 'diamond_plate': {
            const cx = (x % scale) - scale * 0.5;
            const cy = (y % scale) - scale * 0.5;
            const alt = ((Math.floor(x / scale) + Math.floor(y / scale)) % 2) === 0;
            const lug = alt
              ? (Math.abs(cx - cy) <= 1.2 && Math.abs(cx + cy) <= scale * 0.38)
              : (Math.abs(cx + cy) <= 1.2 && Math.abs(cx - cy) <= scale * 0.38);
            const col = lug ? c2 : c1;
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'perforated_grid': {
            const gx = x % scale;
            const gy = y % scale;
            const isHole = gx >= 1 && gx < scale - 1 && gy >= 1 && gy < scale - 1;
            const col = (param === 1 ? !isHole : isHole) ? c2 : c1;
            r = col[0] + n * 0.6;
            g = col[1] + n * 0.6;
            b = col[2] + n * 0.6;
            break;
          }

          case 'painted_chipped': {
            const isBorder = x < 3 || x >= w - 3 || y < 3 || y >= h - 3;
            const chipField = Math.sin(x * 0.22) * Math.cos(y * 0.25) + (rng() - 0.5) * 0.9;
            if ((isBorder && rng() < 0.35) || chipField > 0.68) {
              r = c2[0] + n;
              g = c2[1] + n;
              b = c2[2] + n;
            } else if (chipField > 0.45) {
              r = c3[0] + n;
              g = c3[1] + n;
              b = c3[2] + n;
            } else {
              r = c1[0] + n;
              g = c1[1] + n;
              b = c1[2] + n;
            }
            break;
          }

          case 'concrete_surface': {
            const blotch = (Math.sin(x * 0.12) + Math.cos(y * 0.15) + Math.sin((x + y) * 0.09)) / 6 + 0.5;
            const pore = rng() < param * 0.15 ? -22 : 0;
            r = lerp(c1[0], c2[0], blotch) + n + pore;
            g = lerp(c1[1], c2[1], blotch) + n + pore;
            b = lerp(c1[2], c2[2], blotch) + n + pore;
            break;
          }

          case 'cracked_masonry': {
            const crack1 = Math.abs(Math.sin(x * 0.11 + Math.sin(y * 0.18) * 1.6));
            const crack2 = Math.abs(Math.cos(y * 0.13 + Math.cos(x * 0.15) * 1.4));
            const isCrack = crack1 < 0.07 || crack2 < 0.06;
            if (isCrack) {
              r = c2[0] + n * 0.5;
              g = c2[1] + n * 0.5;
              b = c2[2] + n * 0.5;
            } else {
              const t = (crack1 + crack2) * 0.5;
              r = lerp(c1[0], c3[0], t) + n;
              g = lerp(c1[1], c3[1], t) + n;
              b = lerp(c1[2], c3[2], t) + n;
            }
            break;
          }

          case 'brick_wall': {
            const rowH = Math.max(4, Math.floor(h / (scale * 2)));
            const brickW = Math.max(8, Math.floor(w / scale));
            const row = Math.floor(y / rowH);
            const offsetX = (row % 2) * Math.floor(brickW / 2);
            const bx = (x + offsetX) % brickW;
            const by = y % rowH;
            const isMortar = bx === 0 || by === 0 || (param === 1 && (bx === 1 || by === 1));
            if (isMortar) {
              r = c2[0] + n * 0.5;
              g = c2[1] + n * 0.5;
              b = c2[2] + n * 0.5;
            } else {
              const brickSeed = ((row * 31 + Math.floor((x + offsetX) / brickW) * 17) % 5) / 5;
              r = lerp(c1[0], c3[0], brickSeed) + n;
              g = lerp(c1[1], c3[1], brickSeed) + n;
              b = lerp(c1[2], c3[2], brickSeed) + n;
            }
            break;
          }

          case 'ceramic_tiles': {
            const tileSpan = Math.max(4, Math.floor(w / scale));
            const tx = x % tileSpan;
            const ty = y % tileSpan;
            const isGrout = tx === 0 || ty === 0;
            if (isGrout) {
              r = c2[0] + n * 0.4;
              g = c2[1] + n * 0.4;
              b = c2[2] + n * 0.4;
            } else {
              const stain = c3 !== c2 && rng() < 0.08 ? 0.5 : 0;
              r = lerp(c1[0], c3[0], stain) + n;
              g = lerp(c1[1], c3[1], stain) + n;
              b = lerp(c1[2], c3[2], stain) + n;
            }
            break;
          }

          case 'corrugated_ridges': {
            const wave = Math.sin((x / w) * Math.PI * 2 * scale) * 0.5 + 0.5;
            r = lerp(c2[0], c1[0], wave) + n;
            g = lerp(c2[1], c1[1], wave) + n;
            b = lerp(c2[2], c1[2], wave) + n;
            break;
          }

          case 'terrazzo_speckle': {
            const p = rng();
            const col = p < param * 0.5 ? c2 : (p < param ? c3 : c1);
            r = col[0] + n * 0.6;
            g = col[1] + n * 0.6;
            b = col[2] + n * 0.6;
            break;
          }

          case 'wood_grain': {
            const wobble = Math.sin(y * 0.12) * 2.5 + Math.cos(x * 0.08) * 1.5;
            const ring = Math.sin((x * 0.45 * (scale / 4)) + wobble) * 0.5 + 0.5;
            const fiber = ((y * 7 + x) % 11 === 0) ? -8 : 0;
            r = lerp(c1[0], c2[0], ring) + n + fiber;
            g = lerp(c1[1], c2[1], ring) + n + fiber;
            b = lerp(c1[2], c2[2], ring) + n + fiber;
            break;
          }

          case 'wood_planks': {
            const plankW = Math.max(6, Math.floor(w / scale));
            const px = x % plankW;
            const plankIdx = Math.floor(x / plankW);
            const jointY = (plankIdx * 23) % h;
            if (px === 0 || y === jointY) {
              r = c2[0]; g = c2[1]; b = c2[2];
            } else {
              const grain = Math.sin(x * 0.8 + Math.sin(y * 0.15) * 2) * 0.5 + 0.5;
              const col = plankIdx % 2 === 0 ? c1 : c3;
              r = lerp(col[0], c2[0], grain * 0.35) + n;
              g = lerp(col[1], c2[1], grain * 0.35) + n;
              b = lerp(col[2], c2[2], grain * 0.35) + n;
            }
            break;
          }

          case 'wood_parquet': {
            const cell = Math.max(8, Math.floor(w / scale));
            const cx = Math.floor(x / cell);
            const cy = Math.floor(y / cell);
            const lx = x % cell;
            const ly = y % cell;
            const horiz = (cx + cy) % 2 === 0;
            if (lx === 0 || ly === 0 || (horiz ? ly === Math.floor(cell / 2) : lx === Math.floor(cell / 2))) {
              r = c3[0]; g = c3[1]; b = c3[2];
            } else {
              const col = horiz ? c1 : c2;
              r = col[0] + n;
              g = col[1] + n;
              b = col[2] + n;
            }
            break;
          }

          case 'marble_veins': {
            const turb = Math.sin(x * 0.14 + Math.sin(y * 0.14) * 2.5) + Math.cos(y * 0.11 + Math.cos(x * 0.12) * 2.0);
            const vein = Math.pow(Math.max(0, 1 - Math.abs(turb) * 1.4), 3);
            r = lerp(c1[0], c2[0], vein) + n;
            g = lerp(c1[1], c2[1], vein) + n;
            b = lerp(c1[2], c2[2], vein) + n;
            break;
          }

          case 'granite_crystal': {
            const cell = ((x * 37 + y * 13 + Math.floor(rng() * 5)) % 7);
            const col = cell === 0 ? c2 : (cell <= 2 ? c3 : c1);
            r = col[0] + n * 0.5;
            g = col[1] + n * 0.5;
            b = col[2] + n * 0.5;
            break;
          }

          case 'slate_strata': {
            const layer = (Math.sin(y * 0.35 * (scale / 4) + Math.sin(x * 0.1) * 1.5) + 1) * 0.5;
            const step = Math.floor(layer * 4) / 3;
            r = lerp(c1[0], c2[0], step) + n;
            g = lerp(c1[1], c2[1], step) + n;
            b = lerp(c1[2], c2[2], step) + n;
            break;
          }

          case 'lunar_craters': {
            const dx1 = x - 20, dy1 = y - 22;
            const dx2 = x - 46, dy2 = y - 42;
            const d1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
            const d2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
            const isRim = Math.abs(d1 - 9) < 1.8 || Math.abs(d2 - 7) < 1.6;
            const isPit = d1 < 7.2 || d2 < 5.4;
            const col = isRim ? c3 : (isPit ? c2 : c1);
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'gravel_pebbles': {
            const gx = (x % 6) - 3;
            const gy = (y % 6) - 3;
            const dist = gx * gx + gy * gy;
            const col = dist > 7 ? c2 : (dist < 2 ? c3 : c1);
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'acoustic_pyramid': {
            const cell = Math.max(4, scale);
            const lx = (x % cell) / cell;
            const ly = (y % cell) / cell;
            const pyramid = 1 - Math.max(Math.abs(lx - 0.5), Math.abs(ly - 0.5)) * 2;
            r = lerp(c2[0], c1[0], pyramid) + n * 0.5;
            g = lerp(c2[1], c1[1], pyramid) + n * 0.5;
            b = lerp(c2[2], c1[2], pyramid) + n * 0.5;
            break;
          }

          case 'knurled_polymer': {
            const knurl = ((x + y) % scale === 0) || ((x - y + 64) % scale === 0);
            const col = knurl ? c2 : c1;
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'pcb_traces': {
            const isPad = (x % 16 >= 6 && x % 16 <= 9 && y % 16 >= 6 && y % 16 <= 9);
            const isTrace = !isPad && ((y % 8 === 2 && x % 16 < 12) || (x % 8 === 4 && y % 16 >= 4));
            const col = isPad ? c2 : (isTrace ? c3 : c1);
            r = col[0] + n * 0.5;
            g = col[1] + n * 0.5;
            b = col[2] + n * 0.5;
            break;
          }

          case 'carbon_weave': {
            const step = Math.max(2, scale);
            const twill = ((Math.floor(x / step) + Math.floor(y / step)) % 2) === 0;
            const sheen = ((x + y) % step) / step;
            const col = twill ? c1 : c2;
            r = col[0] + sheen * 16 + n;
            g = col[1] + sheen * 16 + n;
            b = col[2] + sheen * 16 + n;
            break;
          }

          case 'hex_honeycomb': {
            const hx = x % scale;
            const hy = (y + Math.floor(x / scale) * Math.floor(scale / 2)) % scale;
            const isWall = hx === 0 || hy === 0 || (hx + hy === scale);
            const col = isWall ? c2 : c1;
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'solar_array': {
            const isBusbar = x % 16 === 0 || y % 8 === 0;
            const isFineLine = y % 4 === 0;
            const col = isBusbar ? c2 : (isFineLine ? c3 : c1);
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'thermal_tiles': {
            const span = Math.max(8, Math.floor(w / scale));
            const isSeam = (x % span === 0) || (y % span === 0);
            const isBevel = (x % span === 1) || (y % span === 1);
            const col = isSeam ? c2 : (isBevel ? c3 : c1);
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'crt_display': {
            const scan = y % 2 === 0 ? 1.25 : 0.80;
            const isData = param === 2
              ? (x >= 8 && x <= 56 && y % 4 === 0 && ((x * 7 + y * 13) % 5 !== 0))
              : (x >= 8 && x <= 56 && (y === 16 || y === 32 || y === 48 || (x === 32 && y >= 12 && y <= 52)));
            const col = isData ? c2 : c1;
            r = col[0] * scan + n * 0.4;
            g = col[1] * scan + n * 0.4;
            b = col[2] * scan + n * 0.4;
            break;
          }

          case 'stencil_badge': {
            const isBorder = x < 3 || x >= w - 3 || y < 3 || y >= h - 3;
            const dx = x - 32, dy = y - 32;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx);
            const sector = Math.floor(((angle + Math.PI) / (Math.PI * 2)) * 6) % 2 === 0;
            const isSymbol = (dist > 6 && dist < 20 && sector) || dist < 4;
            const col = (isBorder || isSymbol) ? c2 : c1;
            r = col[0] + n * 0.5;
            g = col[1] + n * 0.5;
            b = col[2] + n * 0.5;
            break;
          }

          case 'frosted_crystal': {
            const facet = Math.sin(x * 0.35 + rng() * 0.5) * Math.cos(y * 0.35 + rng() * 0.5) * 0.5 + 0.5;
            r = lerp(c1[0], c2[0], facet) + n;
            g = lerp(c1[1], c2[1], facet) + n;
            b = lerp(c1[2], c2[2], facet) + n;
            break;
          }

          case 'forcefield_grid': {
            const isGrid = (x % scale === 0) || (y % scale === 0);
            const col = isGrid ? c2 : c1;
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            if (alpha < 255) {
              a = isGrid ? Math.min(255, alpha + 75) : Math.max(35, alpha - 55);
            }
            break;
          }

          case 'woven_fabric': {
            const warp = (x + y) % Math.max(2, scale) === 0;
            const col = warp ? c1 : c2;
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }

          case 'quilted_padded': {
            const span = Math.max(6, scale);
            const d1 = Math.abs(((x + y) % span) - span * 0.5);
            const d2 = Math.abs(((x - y + 64) % span) - span * 0.5);
            const isSeam = d1 < 1.2 || d2 < 1.2;
            const puff = Math.min(d1, d2) / (span * 0.5);
            const col = isSeam ? c2 : c1;
            r = col[0] * (0.85 + puff * 0.22) + n;
            g = col[1] * (0.85 + puff * 0.22) + n;
            b = col[2] * (0.85 + puff * 0.22) + n;
            break;
          }

          case 'leather_grain': {
            const pebble = Math.sin(x * 0.65 + Math.cos(y * 0.55) * 2.0) * Math.cos(y * 0.65 - Math.sin(x * 0.55) * 2.0);
            const t = pebble < -0.35 ? 1.0 : 0.2;
            r = lerp(c1[0], c2[0], t) + n;
            g = lerp(c1[1], c2[1], t) + n;
            b = lerp(c1[2], c2[2], t) + n;
            break;
          }

          case 'blueprint_grid': {
            const isMajor = (x % 16 === 0) || (y % 16 === 0);
            const isMinor = (x % 4 === 0) || (y % 4 === 0);
            const t = isMajor ? 0.9 : (isMinor ? 0.35 : 0.0);
            r = lerp(c1[0], c2[0], t) + n;
            g = lerp(c1[1], c2[1], t) + n;
            b = lerp(c1[2], c2[2], t) + n;
            break;
          }

          case 'organic_weathering':
          default: {
            const blob = (Math.sin(x * 0.16) * Math.cos(y * 0.16) + Math.sin((x - y) * 0.11) + 2) * 0.25;
            const col = blob > 0.62 ? c3 : (blob < 0.38 ? c2 : c1);
            r = col[0] + n;
            g = col[1] + n;
            b = col[2] + n;
            break;
          }
        }

        pixels[idx + 0] = Math.min(255, Math.max(0, Math.round(r)));
        pixels[idx + 1] = Math.min(255, Math.max(0, Math.round(g)));
        pixels[idx + 2] = Math.min(255, Math.max(0, Math.round(b)));
        pixels[idx + 3] = Math.min(255, Math.max(0, Math.round(a)));
      }
    }
  }

  /**
   * Deterministic Mulberry32 pseudorandom number generator for consistent procedural textures.
   */
  private static createRNG(seed: number): () => number {
    let s = seed | 0;
    return () => {
      s = (s + 0x6d2b79f5) | 0;
      let t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /**
   * Disposes all GPU texture allocations.
   */
  public static clearCache(): void {
    this.textures.forEach((tex) => tex.dispose());
    this.normalTextures.forEach((tex) => tex.dispose());
    this.roughnessTextures.forEach((tex) => tex.dispose());
    this.textures.clear();
    this.normalTextures.clear();
    this.roughnessTextures.clear();
    this.presetTextures.clear();
    this.thumbnailCache.clear();
  }
}
