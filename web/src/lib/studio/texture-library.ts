import * as THREE from 'three';
import type { ComponentDef } from './types.ts';

export type TexturePresetName =
  | 'worn_metal'
  | 'metal_dark_grime'
  | 'metal_light_brushed'
  | 'painted_metal_white'
  | 'beige_plastic_worn'
  | 'rubber_black'
  | 'rust_heavy'
  | 'hazard_stripes'
  | 'vent_grill'
  | 'crt_screen_green'
  | 'crt_screen_amber'
  | 'crt_screen_off'
  | 'caution_label'
  | 'red_paint_worn';

export interface TexturePresetProfile {
  name: TexturePresetName;
  label: string;
  roughness: number;
  metalness: number;
  tintColor: string;
  emissive?: string;
  emissiveIntensity?: number;
  isDecal?: boolean; // If true, UVs use 0..1 clamp rather than aspect ratio tiling
}

export class TextureLibrary {
  private static textures = new Map<string, THREE.DataTexture>();
  private static presetTextures = new Set<THREE.Texture>();

  /**
   * Canonical texture profiles calibrated to Below Nominal PS1 industrial aesthetics.
   */
  public static readonly PROFILES: Record<TexturePresetName, TexturePresetProfile> = {
    worn_metal: {
      name: 'worn_metal',
      label: 'Metal Desgastado',
      roughness: 0.68,
      metalness: 0.35,
      tintColor: '#ffffff'
    },
    metal_dark_grime: {
      name: 'metal_dark_grime',
      label: 'Acero Estructural Oscuro',
      roughness: 0.70,
      metalness: 0.38,
      tintColor: '#ffffff'
    },
    metal_light_brushed: {
      name: 'metal_light_brushed',
      label: 'Metal Cepillado',
      roughness: 0.38,
      metalness: 0.85,
      tintColor: '#ffffff'
    },
    painted_metal_white: {
      name: 'painted_metal_white',
      label: 'Esmalte Blanco Desgastado',
      roughness: 0.65,
      metalness: 0.15,
      tintColor: '#ffffff'
    },
    beige_plastic_worn: {
      name: 'beige_plastic_worn',
      label: 'Plástico Beige Retro (90s)',
      roughness: 0.55,
      metalness: 0.05,
      tintColor: '#ffffff'
    },
    rubber_black: {
      name: 'rubber_black',
      label: 'Goma Negra Vulcanizada',
      roughness: 0.90,
      metalness: 0.02,
      tintColor: '#ffffff'
    },
    rust_heavy: {
      name: 'rust_heavy',
      label: 'Óxido Pesado Corrosivo',
      roughness: 0.88,
      metalness: 0.10,
      tintColor: '#ffffff'
    },
    hazard_stripes: {
      name: 'hazard_stripes',
      label: 'Rayas de Peligro (Amarillo/Negro)',
      roughness: 0.70,
      metalness: 0.05,
      tintColor: '#ffffff'
    },
    vent_grill: {
      name: 'vent_grill',
      label: 'Rejilla de Ventilación',
      roughness: 0.75,
      metalness: 0.40,
      tintColor: '#ffffff'
    },
    crt_screen_green: {
      name: 'crt_screen_green',
      label: 'Monitor CRT Fósforo Verde',
      roughness: 0.22,
      metalness: 0.0,
      tintColor: '#ffffff',
      emissive: '#26f259',
      emissiveIntensity: 1.5,
      isDecal: true
    },
    crt_screen_amber: {
      name: 'crt_screen_amber',
      label: 'Monitor CRT Fósforo Ámbar',
      roughness: 0.22,
      metalness: 0.0,
      tintColor: '#ffffff',
      emissive: '#f29915',
      emissiveIntensity: 1.5,
      isDecal: true
    },
    crt_screen_off: {
      name: 'crt_screen_off',
      label: 'Pantalla CRT Apagada',
      roughness: 0.18,
      metalness: 0.05,
      tintColor: '#ffffff',
      isDecal: true
    },
    caution_label: {
      name: 'caution_label',
      label: 'Etiqueta de Precaución',
      roughness: 0.60,
      metalness: 0.05,
      tintColor: '#ffffff',
      isDecal: true
    },
    red_paint_worn: {
      name: 'red_paint_worn',
      label: 'Pintura Roja Industrial',
      roughness: 0.65,
      metalness: 0.12,
      tintColor: '#ffffff'
    }
  };

  /**
   * Historical aliases mapping legacy or conversational names to canonical presets.
   */
  public static readonly ALIASES: Record<string, TexturePresetName> = {
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
    plastic: 'beige_plastic_worn'
  };

  /**
   * Resolves a texture preset name through aliases to canonical name.
   */
  public static resolvePresetName(rawName?: string): TexturePresetName | null {
    if (!rawName) return null;
    const clean = rawName.toLowerCase().trim();
    if (this.PROFILES[clean as TexturePresetName]) {
      return clean as TexturePresetName;
    }
    if (this.ALIASES[clean]) {
      return this.ALIASES[clean];
    }
    return null;
  }

  /**
   * Checks if a texture instance belongs to the shared preset library.
   */
  public static isPresetTexture(tex: THREE.Texture): boolean {
    return this.presetTextures.has(tex);
  }

  /**
   * Retrieves or creates a cached Three.js DataTexture for the given preset.
   */
  public static getTexture(preset: TexturePresetName): THREE.DataTexture {
    if (this.textures.has(preset)) {
      return this.textures.get(preset)!;
    }

    const size = 64;
    const pixels = new Uint8Array(size * size * 4);
    this.generatePixelsForPreset(preset, pixels, size, size);

    const tex = new THREE.DataTexture(pixels, size, size, THREE.RGBAFormat);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.NearestFilter;
    tex.generateMipmaps = false;
    tex.needsUpdate = true;

    this.textures.set(preset, tex);
    this.presetTextures.add(tex);
    return tex;
  }

  /**
   * Builds an authentic PS1 Three.js MeshStandardMaterial for a component.
   */
  public static getMaterial(comp: ComponentDef, baseColor: THREE.Color): THREE.MeshStandardMaterial {
    const presetName = this.resolvePresetName(comp.texturePreset);
    if (!presetName) {
      // Legacy color-only material
      return new THREE.MeshStandardMaterial({
        color: baseColor,
        roughness: comp.roughness ?? 0.75,
        metalness: comp.metalness ?? 0.25,
        flatShading: true,
        vertexColors: true,
        wireframe: Boolean(comp.wireframe)
      });
    }

    const profile = this.PROFILES[presetName];
    const texture = this.getTexture(presetName);

    // Determine material color tint
    let matColor: THREE.Color;
    if (comp.color && !comp.color.startsWith('default')) {
      matColor = baseColor;
    } else {
      matColor = new THREE.Color(profile.tintColor);
    }

    const mat = new THREE.MeshStandardMaterial({
      map: texture,
      color: matColor,
      roughness: comp.roughness ?? profile.roughness,
      metalness: comp.metalness ?? profile.metalness,
      flatShading: true,
      vertexColors: false, // Pure crisp texture rendering
      wireframe: Boolean(comp.wireframe)
    });

    // Emissive setup for CRTs and lit indicators
    const emissiveHex = comp.emissive ?? profile.emissive;
    if (emissiveHex) {
      mat.emissive = new THREE.Color(emissiveHex);
      mat.emissiveIntensity = comp.emissiveIntensity ?? profile.emissiveIntensity ?? 1.5;
    }

    return mat;
  }

  /**
   * Generates procedural low-res 64x64 RGBA pixel art for each industrial preset.
   */
  private static generatePixelsForPreset(
    preset: TexturePresetName,
    pixels: Uint8Array,
    w: number,
    h: number
  ): void {
    const rng = this.createRNG(preset.split('').reduce((acc, c) => acc + c.charCodeAt(0), 42));

    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const idx = (y * w + x) * 4;
        let r = 0, g = 0, b = 0, a = 255;

        switch (preset) {
          case 'worn_metal':
          case 'metal_dark_grime': {
            // Dark weathered structural metal with perimeter vignette & rust flecks
            const base = preset === 'worn_metal' ? 62 : 48;
            const noise = (rng() - 0.5) * 16;
            let val = Math.max(10, Math.min(245, base + noise));
            r = val;
            g = val * 1.04;
            b = val * 1.08;

            // Rust flecks
            if (rng() < 0.05) {
              r = 95 + rng() * 30;
              g = 48 + rng() * 15;
              b = 20 + rng() * 10;
            }

            // Perimeter vignette
            if (x < 2 || x >= w - 2 || y < 2 || y >= h - 2) {
              r *= 0.65; g *= 0.65; b *= 0.65;
            }
            break;
          }

          case 'metal_light_brushed': {
            // Brushed steel with horizontal machining lines
            const lineBrightness = 160 + ((y * 11) % 23) * 1.8 + (rng() - 0.5) * 14;
            r = lineBrightness * 0.95;
            g = lineBrightness * 0.98;
            b = lineBrightness * 1.05;
            // Fine horizontal scratches
            if (rng() < 0.03) {
              r *= 0.75; g *= 0.75; b *= 0.78;
            }
            break;
          }

          case 'painted_metal_white': {
            // Off-white enamel with chip wear exposing darker primer
            const noise = (rng() - 0.5) * 12;
            let val = 215 + noise;
            r = val; g = val * 1.01; b = val * 1.02;

            // Chipped paint at corners/edges
            const isEdge = x < 3 || x >= w - 3 || y < 3 || y >= h - 3;
            if (isEdge && rng() < 0.15) {
              r = 52; g = 54; b = 58; // Dark under-metal
            }
            break;
          }

          case 'beige_plastic_worn': {
            // 90s retro computing housing with crevice grime
            const noise = (rng() - 0.5) * 10;
            r = 184 + noise;
            g = 179 + noise * 0.95;
            b = 158 + noise * 0.85;

            // Crevice border grime
            if (x < 2 || x >= w - 2 || y < 2 || y >= h - 2) {
              r *= 0.75; g *= 0.72; b *= 0.65;
            }
            break;
          }

          case 'rubber_black': {
            // Matte vulcanized synthetic tire elastomer with fine grain
            const noise = (rng() - 0.5) * 8;
            const val = 30 + noise;
            r = val; g = val; b = val * 1.05;
            break;
          }

          case 'rust_heavy': {
            // Deep oxidized corrosion clusters
            const cluster = Math.sin(x * 0.15) * Math.cos(y * 0.15) + (rng() - 0.5) * 0.8;
            if (cluster > 0.3) {
              // Bright iron orange
              r = 180 + rng() * 30;
              g = 80 + rng() * 20;
              b = 25 + rng() * 10;
            } else if (cluster < -0.2) {
              // Dark crust
              r = 56 + rng() * 15;
              g = 24 + rng() * 10;
              b = 10 + rng() * 5;
            } else {
              // Medium rust
              r = 125 + rng() * 20;
              g = 48 + rng() * 15;
              b = 18 + rng() * 10;
            }
            break;
          }

          case 'hazard_stripes': {
            // 45-degree bold diagonal safety chevron stripes
            const stripeWidth = 8;
            const isStripe = Math.floor((x + y) / stripeWidth) % 2 === 0;
            if (isStripe) {
              // Vibrant hazard yellow with slight grit
              const grit = 0.95 + rng() * 0.1;
              r = Math.min(255, 225 * grit);
              g = Math.min(255, 175 * grit);
              b = Math.min(255, 20 * grit);
            } else {
              // Contrast black/dark charcoal
              const darkGrit = 26 + rng() * 6;
              r = darkGrit; g = darkGrit; b = darkGrit * 1.05;
            }
            break;
          }

          case 'vent_grill': {
            // Horizontal ventilation slats with shadow grooves
            const slatH = 4;
            const isSlatLit = Math.floor(y / slatH) % 2 === 0;
            if (isSlatLit) {
              const metalGrit = 82 + (rng() - 0.5) * 10;
              r = metalGrit; g = metalGrit * 1.05; b = metalGrit * 1.12;
            } else {
              // Deep recessed cavity
              r = 14; g = 14; b = 16;
            }
            break;
          }

          case 'crt_screen_green': {
            // CRT monitor phosphor green with horizontal scanlines & oscilloscope line
            const scanline = y % 2 === 0 ? 1.35 : 0.82;
            let baseG = (28 + rng() * 8) * scanline;
            let baseR = 12 * scanline;
            let baseB = 16 * scanline;

            // Central oscilloscope waveform / telemetry row
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
            // CRT monitor amber phosphor with scanlines & radar arc
            const scanline = y % 2 === 0 ? 1.35 : 0.82;
            let baseR = (115 + rng() * 12) * scanline;
            let baseG = (58 + rng() * 8) * scanline;
            let baseB = 12 * scanline;

            // Central telemetry text row
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
            // Dark powered-off curved glass with diagonal reflection glare
            const glare = Math.exp(-Math.pow((x - y) / 10, 2)) * 35;
            r = 16 + glare;
            g = 18 + glare * 1.05;
            b = 22 + glare * 1.15;
            break;
          }

          case 'caution_label': {
            // Yellow badge with black border & simulated stencil text bars
            const isBorder = x < 2 || x >= w - 2 || y < 2 || y >= h - 2;
            const isTextBar = (y >= 26 && y <= 28 && x >= 10 && x <= 54) ||
                              (y >= 36 && y <= 38 && x >= 14 && x <= 50);

            if (isBorder || isTextBar) {
              r = 24; g = 24; b = 24;
            } else {
              // Safety caution yellow
              r = 220; g = 170; b = 15;
            }
            break;
          }

          case 'red_paint_worn': {
            // Emergency red paint with wear & rust
            const noise = (rng() - 0.5) * 16;
            r = Math.min(255, 148 + noise);
            g = Math.max(0, 26 + noise * 0.3);
            b = Math.max(0, 20 + noise * 0.2);

            // Chipped rust specks
            if (rng() < 0.08) {
              r = 75; g = 38; b = 22;
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
    this.textures.clear();
    this.presetTextures.clear();
  }
}
