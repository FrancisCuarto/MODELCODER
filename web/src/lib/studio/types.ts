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

export interface ComponentDef {
  name: string;
  shape: ShapePrimitive;
  /**
   * Primary dimensions:
   * - box: [width, height, depth]
   * - cylinder: [radiusTop, radiusBottom, height, segments]
   * - sphere: [radius, widthSegments, heightSegments]
   * - plane: [width, height]
   * - cone: [radius, height, segments]
   * - torus: [radius, tube, radialSegments, tubularSegments]
   * - capsule: [radius, length, capSegments, radialSegments]
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
