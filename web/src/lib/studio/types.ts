/**
 * ModelCoder 3D Studio - Data Models and Type Contracts
 */

export type ShapePrimitive = 
  | 'box' 
  | 'cylinder' 
  | 'sphere' 
  | 'plane' 
  | 'cone' 
  | 'torus' 
  | 'capsule' 
  | 'wedge';

export type TexturePreset = 
  // Original 18 canonical presets (preserved for 100% backward compatibility)
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
  | 'red_paint_worn'
  | 'tinted_glass'
  | 'reinforced_glass'
  | 'clean_glass'
  | 'hologram_cyan'
  // Expanded Metals (16)
  | 'steel_polished'
  | 'steel_galvanized'
  | 'iron_cast'
  | 'iron_aged'
  | 'aluminum_anodized'
  | 'copper_polished'
  | 'copper_oxidized'
  | 'bronze_antique'
  | 'brass_burnished'
  | 'titanium_aerospace'
  | 'diamond_plate'
  | 'metal_perforated'
  | 'gold_contacts'
  | 'chrome_mirror'
  | 'lead_shielding'
  | 'painted_metal_blue'
  | 'painted_metal_olive'
  | 'painted_metal_yellow'
  // Expanded Construction & Industrial (14)
  | 'concrete_smooth'
  | 'concrete_rough'
  | 'concrete_cracked'
  | 'cinder_block'
  | 'brick_red'
  | 'brick_industrial'
  | 'stucco_plaster'
  | 'asphalt_road'
  | 'ceramic_tile_white'
  | 'industrial_tile_dirty'
  | 'nonslip_floor'
  | 'station_modular_panel'
  | 'corrugated_metal'
  | 'terrazzo_floor'
  // Expanded Woods (10)
  | 'wood_oak'
  | 'wood_pine'
  | 'wood_walnut'
  | 'wood_plywood'
  | 'wood_painted_worn'
  | 'wood_rustic_planks'
  | 'wood_varnished'
  | 'wood_parquet'
  | 'wood_bamboo'
  | 'wood_charred'
  // Expanded Stones & Minerals (12)
  | 'granite_grey'
  | 'granite_pink'
  | 'marble_white'
  | 'marble_black_gold'
  | 'slate_layered'
  | 'basalt_lunar'
  | 'limestone_sand'
  | 'sand_compacted'
  | 'gravel_mineral'
  | 'quartz_crystal'
  | 'energy_mineral'
  | 'obsidian_volcanic'
  // Expanded Plastics, Rubbers & Polymers (10)
  | 'plastic_abs_matte'
  | 'plastic_acrylic_gloss'
  | 'plastic_translucent'
  | 'rubber_ribbed_mat'
  | 'silicone_medical'
  | 'acoustic_foam'
  | 'polymer_tactical'
  | 'plastic_hazard_orange'
  | 'vinyl_grip'
  | 'teflon_white'
  // Expanded Tech, Sci-Fi, Screens & Signage (16)
  | 'pcb_green_gold'
  | 'pcb_black_hd'
  | 'pcb_blue_proto'
  | 'carbon_fiber'
  | 'hex_composite'
  | 'server_vent_panel'
  | 'thermal_tile_white'
  | 'thermal_tile_black'
  | 'solar_panel_blue'
  | 'laser_grid_red'
  | 'crt_screen_blue'
  | 'crt_data_matrix'
  | 'radiation_label'
  | 'biohazard_label'
  | 'high_voltage_label'
  | 'plasma_core_glow'
  // Expanded Glass & Transparencies (6)
  | 'frosted_glass'
  | 'cryo_glass_ice'
  | 'amber_lab_glass'
  | 'hologram_amber'
  | 'forcefield_hex'
  | 'visor_gold_mirror'
  // Expanded Fabrics, Leather, Paper & Organic/Weathered (14)
  | 'kevlar_ballistic'
  | 'canvas_military'
  | 'quilted_padding_white'
  | 'quilted_padding_orange'
  | 'synthetic_mesh'
  | 'leather_black_worn'
  | 'leather_brown_aged'
  | 'cardboard_corrugated'
  | 'blueprint_paper'
  | 'duct_tape_silver'
  | 'kapton_gold_foil'
  | 'moss_biological'
  | 'ash_dust_coating'
  | 'soil_mud_packed';

export type MaterialCategoryType =
  | 'metals'
  | 'construction'
  | 'woods'
  | 'stones'
  | 'plastics'
  | 'tech'
  | 'glass'
  | 'fabrics_organic'
  // Legacy category identifiers kept for compatibility
  | 'painted_metal'
  | 'steel'
  | 'plastic'
  | 'screen'
  | 'rubber'
  | 'ceramic';

export type PivotPresetType = 'center' | 'bottom' | 'top' | 'left' | 'right' | 'front' | 'back';

export interface ComponentDef {
  name: string;
  shape: ShapePrimitive;
  parentId?: string; // Optional parent component name (for hierarchical transform parenting)
  pivot?: [number, number, number]; // [offsetX, offsetY, offsetZ] in meters relative to shape center (pivot / hinge / articulation origin)
  /**
   * Primary dimensions:
   * - box: [width, height, depth]
   * - cylinder: [radiusTop, radiusBottom, height, segments]
   * - sphere: [radius, widthSegments, heightSegments]
   * - plane: [width, height]
   * - cone: [radius, height, segments]
   * - torus: [radius, tube, radialSegments, tubularSegments]
   * - capsule: [radius, length, capSegments, radialSegments]
   * - wedge: [width, height, depth]
   */
  size?: number[];
  position?: [number, number, number];
  rotation?: [number, number, number]; // Euler angles in degrees
  scale?: [number, number, number];
  color?: string; // Hex e.g. '#2b6cb0' or retro color name
  roughness?: number;
  metalness?: number;
  wireframe?: boolean;
  label?: string; // Text string for decal / stencil plate
  labelColor?: string;

  // Component State & Visibility
  visible?: boolean;
  locked?: boolean;
  opacity?: number;
  transparent?: boolean;

  // Authentic PS1 & PBR Material & Texture Preset Extension (optional, backward-compatible)
  texturePreset?: TexturePreset | string;
  materialType?: MaterialCategoryType | string;
  emissive?: string; // Hex color for CRT glows, LED lights or status lamps
  emissiveIntensity?: number;
  uvScale?: [number, number]; // [scaleU, scaleV] frequency modifier to prevent stretching
  uvRotation?: number; // UV rotation angle in degrees (0..360)
  wear?: number; // Parametric surface weathering/grime intensity (0..1)
  normalStrength?: number; // Normal map relief intensity (0..2)
}

// ---------------------------------------------------------------------------
// Animation Data Models (Exportable glTF/GLB Animation Tracks)
// ---------------------------------------------------------------------------

export type AnimationInterpolation = 'linear' | 'step' | 'cubic';

export type AnimationTrackProperty = 'position' | 'rotation' | 'scale';

export interface AnimationKeyframeDef {
  time: number; // in seconds (e.g. 0.0, 0.5, 1.2)
  value: [number, number, number]; // [x, y, z] for pos/scale, or Euler degrees [degX, degY, degZ] for rotation
  interpolation?: AnimationInterpolation;
}

export interface AnimationTrackDef {
  targetComponent: string; // Target mesh name matching component.name
  targetName?: string; // Developer convenience alias matching targetComponent
  property: AnimationTrackProperty; // 'position' | 'rotation' | 'scale'
  keyframes: AnimationKeyframeDef[];
}

export type AnimationPresetType =
  | 'sliding_door'
  | 'hinge_lid'
  | 'button_press'
  | 'spin_continuous'
  | 'mechanical_deploy'
  | 'idle_hover';

export interface AnimationClipDef {
  id: string;
  name: string; // glTF animation name shown in game engines (e.g. 'OpenDoor', 'DeployGear', 'IdleSpin')
  duration: number; // Total length in seconds
  loop?: 'repeat' | 'pingpong' | 'once';
  tracks: AnimationTrackDef[];
  presetType?: AnimationPresetType;
}

export interface ModelSpec {
  id: string;
  name: string;
  category: string;
  description: string;
  units: 'meters';
  dimensions: {
    width: number;
    depth: number;
    height: number;
  };
  palette: string;
  components: ComponentDef[];
  animations?: AnimationClipDef[]; // Exportable glTF animation clips
  parameters?: Array<{
    key: string;
    label: string;
    type: 'float' | 'int' | 'boolean' | 'enum';
    default: any;
    min?: number;
    max?: number;
    step?: number;
    options?: Array<{ value: string; label: string }> | string[];
  }>;
}

export type GenerationMode = 'ai' | 'visual' | 'code';
export type GenerationState = 'idle' | 'pending' | 'generating' | 'completed' | 'error';
export type ShadingMode = 'shaded' | 'wireframe' | 'normals' | 'vertex_colors' | 'unlit';
export type TransformGizmoMode = 'translate' | 'rotate' | 'scale' | 'none';
export type CameraViewPreset = 'front' | 'side' | 'top' | 'isometric' | 'perspective';

export interface GeometricStats {
  triangles: number;
  vertices: number;
  dimensions: {
    x: number; // width
    y: number; // height
    z: number; // depth
  };
}

export interface GenerationRequest {
  id: string;
  version: number;
  timestamp: number;
  mode: GenerationMode;
  prompt?: string;
  spec?: ModelSpec;
  code?: string;
}

export interface GenerationResult {
  id: string;
  version: number;
  timestamp: number;
  success: boolean;
  mode: GenerationMode;
  stats?: GeometricStats;
  spec?: ModelSpec;
  error?: string;
  errorDetails?: string;
  warnings?: string[];
  isPreviousResultFallback?: boolean;
}
