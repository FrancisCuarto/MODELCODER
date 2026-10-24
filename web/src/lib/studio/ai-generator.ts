import * as THREE from 'three';
import type { ModelSpec, ComponentDef } from './types.ts';
import { ProceduralMemory } from './procedural-memory.ts';
import { ProceduralEngine } from './procedural-engine.ts';

export interface GenerationConfig {
  engine?: 'ai' | 'local';
  apiKey?: string;
  forceFresh?: boolean;
}

export class AIGenerator {
  /**
   * Generates a structured ModelSpec from a natural language user prompt.
   * - In AI Mode (Gemini): ALWAYS creates fresh, unique models. Never reuses or caches existing models.
   * - In Local Mode: Uses deterministic procedural blueprints, semantic synthesis, and persistent memory.
   */
  public static async generateModel(
    prompt: string,
    configOrKey?: string | GenerationConfig
  ): Promise<{ spec: ModelSpec; rawResponse?: string; source: 'gemini' | 'local' | 'local_memory' | 'cloud_memory' }> {
    const cleanPrompt = prompt.trim();
    if (!cleanPrompt) {
      throw new Error('El prompt no puede estar vacío.');
    }

    let engine: 'ai' | 'local' = 'local';
    let apiKey: string | undefined = undefined;
    let forceFresh = false;

    if (typeof configOrKey === 'string') {
      apiKey = configOrKey;
      engine = (apiKey && apiKey.trim().length > 10) ? 'ai' : 'local';
    } else if (configOrKey) {
      engine = configOrKey.engine || 'local';
      apiKey = configOrKey.apiKey;
      forceFresh = configOrKey.forceFresh ?? (engine === 'ai');
    }

    // =========================================================================
    // MODO IA (GOOGLE GEMINI)
    // REGLA ESTRICTA:
    // Si se usa la IA, NUNCA debe basarse en modelos existentes ni usar caché;
    // SIEMPRE debe crear un modelo 100% nuevo, original e innovador.
    // =========================================================================
    if (engine === 'ai') {
      if (!apiKey || apiKey.trim().length <= 10) {
        throw new Error('Para usar la IA Generativa necesitas ingresar tu clave gratuita de Google Gemini en el botón [🔑 CONECTAR GEMINI].');
      }

      // Llamada directa a Gemini sin consultar memoria ni presets existentes
      const geminiRes = await this.callGeminiAPI(cleanPrompt, apiKey.trim());
      const normalizedSpec = this.normalizeSpecGeometry(geminiRes.spec);
      return { spec: normalizedSpec, rawResponse: geminiRes.rawResponse, source: 'gemini' };
    }

    // =========================================================================
    // MODO MOTOR PROCEDURAL LOCAL
    // =========================================================================
    if (!forceFresh) {
      const learned = await ProceduralMemory.findLearnedModel(cleanPrompt);
      if (learned) {
        return { spec: this.normalizeSpecGeometry(learned.spec), source: learned.source };
      }
    }

    const rawSpec = this.synthesizeProceduralSpec(cleanPrompt);
    const spec = this.normalizeSpecGeometry(rawSpec);
    // Guarda en memoria local para acceso rápido offline
    await ProceduralMemory.recordLearnedModel(cleanPrompt, spec);
    return { spec, source: 'local' };
  }

  /**
   * Mathematically normalizes, sanitizes, and ground-aligns a ModelSpec.
   * Guarantees:
   * 1. All component names are unique and valid.
   * 2. Coordinates, sizes, and rotations are valid finite numbers in degrees/meters.
   * 3. Model is automatically grounded so its lowest contact point touches floor at Y = 0.
   * 4. Overall bounding box dimensions are verified.
   */
  /**
   * Converts world-space coordinates from generative models into clean Three.js
   * parent-local coordinates for all components with parentId.
   * This guarantees that hierarchical pieces appear at their exact intended
   * 3D world positions without doubling parent transforms.
   */
  public static convertWorldToLocalHierarchy(spec: ModelSpec): ModelSpec {
    if (!spec || !Array.isArray(spec.components) || spec.components.length === 0) {
      return spec;
    }

    const compMap = new Map<string, ComponentDef>();
    for (const comp of spec.components) {
      if (comp.name) compMap.set(comp.name, comp);
    }

    // Build parent-to-children adjacency map
    const childrenMap = new Map<string, ComponentDef[]>();
    const roots: ComponentDef[] = [];

    for (const comp of spec.components) {
      if (comp.parentId && compMap.has(comp.parentId) && comp.parentId !== comp.name) {
        if (!childrenMap.has(comp.parentId)) {
          childrenMap.set(comp.parentId, []);
        }
        childrenMap.get(comp.parentId)!.push(comp);
      } else {
        roots.push(comp);
      }
    }

    // If no parent-child relationships exist, nothing to convert
    if (childrenMap.size === 0) {
      return spec;
    }

    // Compute initial world matrices for all components assuming positions/rotations are in world space
    const worldMatrices = new Map<string, THREE.Matrix4>();
    for (const comp of spec.components) {
      const pos = new THREE.Vector3(
        Array.isArray(comp.position) && Number.isFinite(comp.position[0]) ? comp.position[0] : 0,
        Array.isArray(comp.position) && Number.isFinite(comp.position[1]) ? comp.position[1] : 0,
        Array.isArray(comp.position) && Number.isFinite(comp.position[2]) ? comp.position[2] : 0
      );
      const euler = new THREE.Euler(
        THREE.MathUtils.degToRad(Array.isArray(comp.rotation) && Number.isFinite(comp.rotation[0]) ? comp.rotation[0] : 0),
        THREE.MathUtils.degToRad(Array.isArray(comp.rotation) && Number.isFinite(comp.rotation[1]) ? comp.rotation[1] : 0),
        THREE.MathUtils.degToRad(Array.isArray(comp.rotation) && Number.isFinite(comp.rotation[2]) ? comp.rotation[2] : 0),
        'XYZ'
      );
      const quat = new THREE.Quaternion().setFromEuler(euler);
      const scale = new THREE.Vector3(
        Array.isArray(comp.scale) && Number.isFinite(comp.scale[0]) && comp.scale[0] > 0 ? comp.scale[0] : 1,
        Array.isArray(comp.scale) && Number.isFinite(comp.scale[1]) && comp.scale[1] > 0 ? comp.scale[1] : 1,
        Array.isArray(comp.scale) && Number.isFinite(comp.scale[2]) && comp.scale[2] > 0 ? comp.scale[2] : 1
      );
      const mat = new THREE.Matrix4().compose(pos, quat, scale);
      worldMatrices.set(comp.name, mat);
    }

    // Traverse breadth-first starting from root nodes
    const queue = [...roots];
    const visited = new Set<string>();

    while (queue.length > 0) {
      const parent = queue.shift()!;
      if (visited.has(parent.name)) continue;
      visited.add(parent.name);

      const children = childrenMap.get(parent.name) || [];
      const parentWorldMat = worldMatrices.get(parent.name)!;
      const invParentWorld = parentWorldMat.clone().invert();

      for (const child of children) {
        const childWorldMat = worldMatrices.get(child.name)!;
        // childLocal = inv(parentWorld) * childWorld
        const localMat = new THREE.Matrix4().multiplyMatrices(invParentWorld, childWorldMat);

        const localPos = new THREE.Vector3();
        const localQuat = new THREE.Quaternion();
        const localScale = new THREE.Vector3();
        localMat.decompose(localPos, localQuat, localScale);

        const localEuler = new THREE.Euler().setFromQuaternion(localQuat, 'XYZ');

        child.position = [
          parseFloat(localPos.x.toFixed(4)),
          parseFloat(localPos.y.toFixed(4)),
          parseFloat(localPos.z.toFixed(4))
        ];
        child.rotation = [
          parseFloat(THREE.MathUtils.radToDeg(localEuler.x).toFixed(2)),
          parseFloat(THREE.MathUtils.radToDeg(localEuler.y).toFixed(2)),
          parseFloat(THREE.MathUtils.radToDeg(localEuler.z).toFixed(2))
        ];

        queue.push(child);
      }
    }

    return spec;
  }

  public static normalizeSpecGeometry(spec: ModelSpec): ModelSpec {
    if (!spec || !Array.isArray(spec.components) || spec.components.length === 0) {
      return spec;
    }

    const usedNames = new Set<string>();
    for (let i = 0; i < spec.components.length; i++) {
      const comp = spec.components[i];
      if (!comp.name || typeof comp.name !== 'string' || comp.name.trim() === '') {
        comp.name = `comp_${i + 1}`;
      } else {
        comp.name = comp.name.trim().replace(/\s+/g, '_');
      }

      if (usedNames.has(comp.name)) {
        comp.name = `${comp.name}_${i + 1}`;
      }
      usedNames.add(comp.name);

      const validShapes = [
        'box',
        'cylinder',
        'sphere',
        'plane',
        'cone',
        'torus',
        'capsule',
        'wedge',
        'chamfer_box',
        'pipe',
        'prism',
        'pyramid',
        'mesh'
      ];
      if (!comp.shape || !validShapes.includes(comp.shape)) {
        comp.shape = 'box';
      }

      if (!Array.isArray(comp.size) || comp.size.length === 0) {
        comp.size = [1, 1, 1];
      } else {
        comp.size = comp.size.map((v) => (typeof v === 'number' && Number.isFinite(v) && v > 0.001 ? Math.abs(v) : 0.5));
      }

      if (comp.shape === 'box' || comp.shape === 'wedge') {
        while (comp.size.length < 3) comp.size.push(1);
      } else if (comp.shape === 'chamfer_box') {
        while (comp.size.length < 3) comp.size.push(1);
        if (comp.size.length < 4) comp.size.push(0.02);
        if (comp.size.length < 5) comp.size.push(1);
      } else if (comp.shape === 'cylinder') {
        while (comp.size.length < 3) comp.size.push(comp.size[0] || 0.5);
        if (comp.size.length < 4) comp.size.push(10);
      } else if (comp.shape === 'pipe') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(comp.size[0] * 0.7);
        if (comp.size.length < 3) comp.size.push(1.0);
        if (comp.size.length < 4) comp.size.push(12);
        if (comp.size[1] >= comp.size[0]) comp.size[1] = comp.size[0] * 0.7;
      } else if (comp.shape === 'prism') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(1.0);
        if (comp.size.length < 3) comp.size.push(6);
      } else if (comp.shape === 'pyramid') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(1.0);
        if (comp.size.length < 3) comp.size.push(4);
      } else if (comp.shape === 'sphere') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(10);
        if (comp.size.length < 3) comp.size.push(8);
      } else if (comp.shape === 'cone') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(1.0);
        if (comp.size.length < 3) comp.size.push(8);
      } else if (comp.shape === 'torus') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(0.15);
        if (comp.size.length < 3) comp.size.push(6);
        if (comp.size.length < 4) comp.size.push(12);
      } else if (comp.shape === 'capsule') {
        if (comp.size.length < 1) comp.size.push(0.25);
        if (comp.size.length < 2) comp.size.push(0.5);
        if (comp.size.length < 3) comp.size.push(4);
        if (comp.size.length < 4) comp.size.push(8);
      } else if (comp.shape === 'plane') {
        while (comp.size.length < 2) comp.size.push(1);
      }

      if (!Array.isArray(comp.position) || comp.position.length < 3) {
        comp.position = [0, 0, 0];
      } else {
        comp.position = [
          Number.isFinite(comp.position[0]) ? parseFloat(comp.position[0].toFixed(4)) : 0,
          Number.isFinite(comp.position[1]) ? parseFloat(comp.position[1].toFixed(4)) : 0,
          Number.isFinite(comp.position[2]) ? parseFloat(comp.position[2].toFixed(4)) : 0
        ];
      }

      if (!Array.isArray(comp.rotation) || comp.rotation.length < 3) {
        comp.rotation = [0, 0, 0];
      } else {
        comp.rotation = [
          Number.isFinite(comp.rotation[0]) ? parseFloat(comp.rotation[0].toFixed(2)) : 0,
          Number.isFinite(comp.rotation[1]) ? parseFloat(comp.rotation[1].toFixed(2)) : 0,
          Number.isFinite(comp.rotation[2]) ? parseFloat(comp.rotation[2].toFixed(2)) : 0
        ];
      }

      if (Array.isArray(comp.scale) && comp.scale.length >= 3) {
        comp.scale = [
          Number.isFinite(comp.scale[0]) && comp.scale[0] > 0.001 ? parseFloat(comp.scale[0].toFixed(3)) : 1,
          Number.isFinite(comp.scale[1]) && comp.scale[1] > 0.001 ? parseFloat(comp.scale[1].toFixed(3)) : 1,
          Number.isFinite(comp.scale[2]) && comp.scale[2] > 0.001 ? parseFloat(comp.scale[2].toFixed(3)) : 1
        ];
      } else if (comp.scale) {
        delete comp.scale;
      }

      // Hinge / Articulation Pivot offset
      if (Array.isArray(comp.pivot) && comp.pivot.length >= 3) {
        comp.pivot = [
          Number.isFinite(comp.pivot[0]) ? parseFloat(comp.pivot[0].toFixed(4)) : 0,
          Number.isFinite(comp.pivot[1]) ? parseFloat(comp.pivot[1].toFixed(4)) : 0,
          Number.isFinite(comp.pivot[2]) ? parseFloat(comp.pivot[2].toFixed(4)) : 0
        ];
      } else if (comp.pivot) {
        delete comp.pivot;
      }

      // Array Modifier sanitization
      if (comp.array && typeof comp.array === 'object') {
        const arr = comp.array;
        const isRadial = arr.type === 'radial';
        const count = Math.max(2, Math.min(64, Math.round(Number(arr.count) || 2)));
        if (isRadial) {
          comp.array = {
            enabled: arr.enabled !== false,
            type: 'radial',
            count,
            radialAxis: ['x', 'y', 'z'].includes(arr.radialAxis as any) ? arr.radialAxis : 'y',
            radialRadius: Number.isFinite(arr.radialRadius) ? Math.max(0, parseFloat((arr.radialRadius as number).toFixed(4))) : 0.5,
            radialAngle: Number.isFinite(arr.radialAngle) ? parseFloat((arr.radialAngle as number).toFixed(2)) : 360,
            radialRotateCopies: arr.radialRotateCopies !== false
          };
        } else {
          const off = Array.isArray(arr.offset) && arr.offset.length >= 3
            ? [
                Number.isFinite(arr.offset[0]) ? parseFloat(arr.offset[0].toFixed(4)) : 0,
                Number.isFinite(arr.offset[1]) ? parseFloat(arr.offset[1].toFixed(4)) : 0,
                Number.isFinite(arr.offset[2]) ? parseFloat(arr.offset[2].toFixed(4)) : 0
              ] as [number, number, number]
            : [0, 0.1, 0] as [number, number, number];
          comp.array = {
            enabled: arr.enabled !== false,
            type: 'linear',
            count,
            offset: off
          };
        }
      } else if (comp.array) {
        delete comp.array;
      }

      // Boolean Modifier sanitization
      if (comp.boolean && typeof comp.boolean === 'object') {
        const b = comp.boolean;
        const op = ['difference', 'union', 'intersection'].includes(b.operation) ? b.operation : 'difference';
        const target = typeof b.targetComponent === 'string' ? b.targetComponent.trim().replace(/\s+/g, '_') : '';
        if (target && target !== comp.name) {
          comp.boolean = {
            enabled: b.enabled !== false,
            operation: op as any,
            targetComponent: target,
            hideTarget: b.hideTarget !== false
          };
        } else {
          delete comp.boolean;
        }
      } else if (comp.boolean) {
        delete comp.boolean;
      }

      // Material weathering, relief & emissive
      if (typeof comp.wear === 'number' && Number.isFinite(comp.wear)) {
        comp.wear = Math.max(0, Math.min(1, parseFloat(comp.wear.toFixed(2))));
      }
      if (typeof comp.normalStrength === 'number' && Number.isFinite(comp.normalStrength)) {
        comp.normalStrength = Math.max(0, Math.min(2, parseFloat(comp.normalStrength.toFixed(2))));
      }
      if (comp.emissive && typeof comp.emissive === 'string') {
        comp.emissive = comp.emissive.trim();
        if (typeof comp.emissiveIntensity === 'number' && Number.isFinite(comp.emissiveIntensity)) {
          comp.emissiveIntensity = Math.max(0, parseFloat(comp.emissiveIntensity.toFixed(2)));
        } else {
          comp.emissiveIntensity = 1.0;
        }
      }

      if (!comp.color || typeof comp.color !== 'string') {
        comp.color = '#718096';
      }
    }

    // Second pass: Validate hierarchy parenting and boolean target cross-references
    const compNameSet = new Set(spec.components.map((c) => c.name));
    for (const comp of spec.components) {
      if (comp.parentId && typeof comp.parentId === 'string') {
        const cleanParent = comp.parentId.trim().replace(/\s+/g, '_');
        if (
          cleanParent !== comp.name &&
          compNameSet.has(cleanParent) &&
          !ProceduralEngine.wouldCreateCycle(spec.components, comp.name, cleanParent)
        ) {
          comp.parentId = cleanParent;
        } else {
          delete comp.parentId;
        }
      } else {
        delete comp.parentId;
      }

      if (comp.boolean?.targetComponent && !compNameSet.has(comp.boolean.targetComponent)) {
        delete comp.boolean;
      }
    }

    // Validate glTF exportable animation clips
    if (Array.isArray(spec.animations) && spec.animations.length > 0) {
      const validClips: any[] = [];
      for (const clip of spec.animations) {
        if (!clip || typeof clip !== 'object') continue;
        const validClip: any = {
          id: clip.id || `anim_${validClips.length + 1}`,
          name: clip.name || `Animation_${validClips.length + 1}`,
          duration: Number.isFinite(clip.duration) && clip.duration > 0 ? parseFloat(clip.duration.toFixed(2)) : 2.0,
          loop: ['repeat', 'pingpong', 'once'].includes(clip.loop) ? clip.loop : 'repeat',
          tracks: Array.isArray(clip.tracks) ? clip.tracks : []
        };
        if (
          clip.presetType &&
          ['sliding_door', 'hinge_lid', 'button_press', 'spin_continuous', 'mechanical_deploy', 'idle_hover'].includes(clip.presetType)
        ) {
          validClip.presetType = clip.presetType;
        }
        validClips.push(validClip);
      }
      spec.animations = validClips.length > 0 ? validClips : undefined;
    }

    // Auto-Grounding: measure true 3D bounding box to ground lowest contact points at Y = 0
    try {
      const { group } = ProceduralEngine.buildModelFromSpec(spec);
      const bbox = new THREE.Box3().setFromObject(group);

      if (!bbox.isEmpty()) {
        const minY = bbox.min.y;
        if (Math.abs(minY) > 0.002) {
          const shiftY = -minY;
          for (const comp of spec.components) {
            // Shift only root components (without parentId or with unparented roots)
            if (!comp.parentId || !spec.components.some((c) => c.name === comp.parentId)) {
              if (comp.position) {
                comp.position[1] = parseFloat((comp.position[1] + shiftY).toFixed(4));
              }
            }
          }
        }

        const sizeX = Math.max(0.1, bbox.max.x - bbox.min.x);
        const sizeY = Math.max(0.1, bbox.max.y - bbox.min.y);
        const sizeZ = Math.max(0.1, bbox.max.z - bbox.min.z);
        spec.dimensions = {
          width: parseFloat(sizeX.toFixed(3)),
          height: parseFloat(sizeY.toFixed(3)),
          depth: parseFloat(sizeZ.toFixed(3))
        };
      }
    } catch (e) {
      console.warn('[AIGenerator] Could not compute bounding box for auto-grounding:', e);
    }

    return spec;
  }

  /**
   * Calls Google Gemini API with structured JSON output schema and high spatial precision.
   */
  private static async callGeminiAPI(
    prompt: string,
    apiKey: string
  ): Promise<{ spec: ModelSpec; rawResponse: string }> {
    const uniqueNonce = `${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    const systemInstruction = `You are ModelCoder 3D Master Architect, an expert procedural 3D modeler for retro-modern, sci-fi, industrial, and cybernetic games.
Your mission is to construct realistic, physically coherent, mechanically solid 3D models with ZERO floating geometry, perfect ground alignment, high mechanical detail, and authentic retro materials.

### 5 ABSOLUTE LAWS OF 3D CONSTRUCTION (MANDATORY)

1. LAW OF SOLID GROUNDING (Ground Level Y = 0):
- The model must rest firmly on the floor at Y = 0.
- In Three.js, primitive positions are centered at their CENTROIDS (center of mass).
- If the lowest base/chassis/leg has height H, its Y position MUST be H/2 (e.g. height 0.20m -> position Y = 0.10m).
- NEVER place the lowest piece with bottom above Y = 0 (no hovering or floating machines).

2. LAW OF ZERO FLOATING GEOMETRY (Physical Stacking & Surface Contact):
- EVERY component must physically touch, connect to, or rest on another component or the floor.
- VERTICAL STACKING FORMULA:
  If Component A extends vertically from Y_bottom to Y_top (height H_A),
  and Component B (height H_B) sits ON TOP of Component A:
  -> Component B's center Y position = Y_top + (H_B / 2).
  -> Example: Base box from Y=0 to Y=0.60. A monitor of height 0.40m resting on it MUST have position Y = 0.60 + (0.40 / 2) = 0.80m.
- WALL & FACE MOUNTING FORMULA:
  If Component A has depth D centered at Z=0 (front face at Z = +D/2),
  and a control panel/dial/gauge of thickness T attaches to its front:
  -> The attached piece MUST have position Z = (D/2) + (T/2).
  -> NEVER let panels float 20cm away in mid-air from the machine body!

3. LAW OF ORTHOGONAL & PURPOSEFUL ROTATIONS (DEGREES):
- All rotations are in DEGREES: [rotX_deg, rotY_deg, rotZ_deg].
- 95% of components MUST have rotation: [0, 0, 0].
- NEVER use random, chaotic, or diagonal rotations (like [17, -33, 48]).
- Only use standard intentional rotations when mechanically required:
  * Horizontal cylinder/wheel/axle: [0, 0, 90] or [90, 0, 0]
  * Ergonomic display tilt / control wedge: [-15, 0, 0] or [15, 0, 0]
  * Door or solar panel swing: [0, 45, 0]

4. LAW OF MECHANICAL HIERARCHY & FUNCTIONAL ANATOMY:
- Design objects like real machines and structures:
  a) HEAVY FOUNDATION / CHASSIS / WHEELS: Heavy base at Y=0 (diamond plate, cast iron, rubber feet).
  b) MAIN HOUSING / BODY: Enclosed structural core (worn metal, beige plastic, painted metal, chamfer_box).
  c) MECHANICAL & ELECTRICAL PARTS: Tanks, vents, heat sinks, conduits, hydraulic pistons, pipes, prisms.
  d) INTERFACE & CONTROLS: Flush control panels, switches, CRT screens, gauges, dials, emergency stop buttons.
  e) ACCENTS & LIGHTS: Warning decals, hazard stripes, LED indicators with emissive glow.

5. LAW OF SYMMETRY & COHESIVE PROPORTIONS:
- Center main structures at X = 0.
- Bilateral parts (wheels, dual tanks, side handles, thrusters, legs) MUST be placed in symmetric pairs (+X and -X) with identical Y and Z.

### 12 PRIMITIVE SHAPES (METERS) & USAGE
- "box": size [width_X, height_Y, depth_Z]
  * Cuboid for structural framing, walls, steps, brackets, chassis cores.
- "chamfer_box": size [width_X, height_Y, depth_Z, bevelRadius, bevelSegments]
  * Box with beveled/rounded edges. Ideal for cybernetic armor, electronics consoles, smooth sci-fi crates, high-tech furniture.
  * Low-poly rule: keep bevelRadius ~0.02-0.05 and bevelSegments 1 or 2 (e.g. [0.60, 0.40, 0.50, 0.02, 1]).
- "cylinder": size [radiusTop, radiusBottom, height_Y, radialSegments]
  * Solid cylinder/column. Wheels, tanks, hydraulic pistons, columns, barrels (e.g. [0.15, 0.15, 0.60, 12]).
- "pipe": size [radiusOuter, radiusInner, height_Y, radialSegments]
  * HOLLOW tube/nozzle! Outer radius and inner radius. Perfect for jet thrusters, rocket nozzles, exhaust pipes, gun barrels, intake conduits, ring mounts (e.g. [0.20, 0.16, 0.40, 12]). Note: radiusInner MUST be less than radiusOuter.
- "prism": size [radius, height_Y, sides]
  * Regular N-sided polygonal prism (height along Y). Use for hexagonal armor plates, sci-fi pylons, heavy bolts/nuts, octagonal columns (e.g. [0.25, 0.80, 6] for a hex pylon).
- "pyramid": size [radius, height_Y, sides]
  * N-sided pyramid tapering to a tip (height along Y). Use for stealth facets, angular deflector plating, nosecones, sensor caps (e.g. [0.30, 0.45, 4] for a 4-sided pyramid).
- "wedge": size [width_X, height_Y, depth_Z]
  * Sloped triangular prism for ergonomic control consoles, ramps, cowcatchers, sloped vehicle hoods.
- "sphere": size [radius, widthSegments, heightSegments]
  * Domes, radar bubbles, cockpit spheres, robotics joint bearings (e.g. [0.20, 12, 8]).
- "capsule": size [radius, length_Y, capSegments, radialSegments]
  * Pressurized tanks, gas cylinders, medical cryo-pods, pill capsules (e.g. [0.10, 0.40, 4, 8]).
- "torus": size [radius, tubeRadius, radSegs, tubSegs]
  * Steering wheels, circular conduits, reactor containment rings, gaskets (e.g. [0.25, 0.04, 6, 12]).
- "cone": size [radius, height_Y, radialSegments]
  * Warning cones, sharp spikes, spotlights, antenna tips (e.g. [0.15, 0.40, 8]).
- "plane": size [width_X, height_Y]
  * Thin display sheets, solar panels, backing plates (e.g. [0.50, 0.30]).

### HIERARCHICAL PARENTING ("parentId") & ARTICULATION PIVOTS ("pivot")
- "parentId": Link child components to their logical parent (e.g. wheels attached to "main_chassis", cannons to "turret_head", doors to "door_frame").
  * This creates clean transform hierarchies so rotating the parent moves all child parts together!
- "pivot": [offsetX, offsetY, offsetZ] (meters relative to component center).
  * Defines where hinges, joints, and articulation axes rotate:
  * Left-hinged door (width W): pivot = [-W/2, 0, 0]
  * Bottom-hinged hatch / folding ramp (height H): pivot = [0, -H/2, 0]
  * Rear-hinged lid (depth D): pivot = [0, 0, -D/2]
  * Elevating gun / antenna base: pivot = [0, -H/2, 0]

### MODIFIERS: REPETITION ARRAYS & CSG BOOLEAN CUTS
- "array": Instantiates multiple copies along an axis or in a circle without duplicating code:
  * Linear Array: "array": { "enabled": true, "type": "linear", "count": 4, "offset": [0, 0.08, 0] }
    -> Ideal for heat sink cooling fins, ladder rungs, radiator slats, ventilation louvers, steps.
  * Radial Array: "array": { "enabled": true, "type": "radial", "count": 6, "radialAxis": "y", "radialRadius": 0.35, "radialAngle": 360, "radialRotateCopies": true }
    -> Ideal for multi-thruster nozzle rings, circular bolt patterns, dial ticks, spoke rims.
- "boolean": Non-destructive CSG difference/union/intersection:
  * "boolean": { "enabled": true, "operation": "difference", "targetComponent": "<cutter_component_name>", "hideTarget": true }
    -> Ideal for cutting cockpit cavities out of fuselages, hollow intake vents, recessed access ports.

### TEXTURES, WEATHERING & EMISSIVE GLOW (138 PBR PRESETS)
- 138 authentic presets across 8 categories:
  * Metals: "worn_metal", "steel_polished", "steel_galvanized", "iron_cast", "copper_polished", "copper_oxidized", "bronze_antique", "brass_burnished", "titanium_aerospace", "diamond_plate", "metal_perforated", "gold_contacts", "chrome_mirror", "painted_metal_white", "painted_metal_blue", "painted_metal_olive", "red_paint_worn"
  * Tech/Screens: "pcb_green_gold", "pcb_black_hd", "carbon_fiber", "server_vent_panel", "solar_panel_blue", "vent_grill", "crt_screen_green", "crt_screen_amber", "crt_screen_blue", "crt_data_matrix", "plasma_core_glow", "radiation_label", "biohazard_label", "caution_label"
  * Industrial/Construction: "concrete_smooth", "asphalt_road", "corrugated_metal", "hazard_stripes", "rubber_black", "rubber_ribbed_mat", "plastic_abs_matte", "polymer_tactical", "station_modular_panel", "nonslip_floor"
  * Glass/Transparencies: "clean_glass", "tinted_glass", "reinforced_glass", "frosted_glass", "hologram_cyan", "visor_gold_mirror"
- Surface Weathering: "wear": 0.0 (factory new) to 0.8 (gritty battle-worn).
- Relief Depth: "normalStrength": 0.5 to 1.5.
- Emissive Lighting: "emissive": "#00ffcc" (or "#ff3300", "#39ff14", "#ffb700") with "emissiveIntensity": 1.2 to 2.5 for CRT monitors, LED status beacons, power cores, thruster fire.

### EXPORTABLE glTF ANIMATIONS ("animations")
When mechanically appropriate, include animation clips:
- "presetType": "spin_continuous" -> continuous 360° spin for radars, rotors, warning beacons, turbine fans.
- "presetType": "idle_hover" -> subtle floating vertical oscillation for hovering drones, hovercraft, alien relics.
- "presetType": "sliding_door" -> automated linear open/close for airlocks, blast gates, elevator doors.
- "presetType": "hinge_lid" -> angular swing for inspection hatches, cockpit canopies, storage crates.
- "presetType": "button_press" -> tactile mechanical depression for switches, buttons.
- "presetType": "mechanical_deploy" -> unfolding action for landing gear, solar panels, weapon bays.

### FEW-SHOT REFERENCE: INDUSTRIAL WELDING & POWER STATION ("máquina de soldar / generador")
Notice how every piece connects with exact mathematical contact, leveraging hierarchy, chamfers, and arrays:
{
  "id": "below_nominal.generated.welder_reference",
  "name": "Estación de Energía y Soldadura Arc-Core 500",
  "category": "infrastructure",
  "description": "Unidad de potencia industrial con chasis biselado, tobera de escape hueca, radiador lineal, escotilla articulada y pantalla CRT emisiva.",
  "units": "meters",
  "dimensions": { "width": 0.90, "height": 0.85, "depth": 0.70 },
  "palette": "industrial_hazard",
  "components": [
    {
      "name": "base_skid",
      "shape": "box",
      "size": [0.80, 0.06, 0.65],
      "position": [0, 0.03, 0],
      "rotation": [0, 0, 0],
      "color": "#1a202c",
      "texturePreset": "steel_galvanized",
      "wear": 0.4
    },
    {
      "name": "main_chassis",
      "shape": "chamfer_box",
      "size": [0.65, 0.48, 0.54, 0.03, 1],
      "position": [0, 0.30, 0],
      "rotation": [0, 0, 0],
      "color": "#dd6b20",
      "texturePreset": "worn_metal",
      "roughness": 0.6,
      "metalness": 0.4,
      "wear": 0.3
    },
    {
      "name": "cooling_radiator_slat",
      "shape": "box",
      "size": [0.015, 0.03, 0.40],
      "position": [0.33, 0.20, 0],
      "rotation": [0, 0, 0],
      "color": "#2d3748",
      "texturePreset": "steel_polished",
      "parentId": "main_chassis",
      "array": {
        "enabled": true,
        "type": "linear",
        "count": 5,
        "offset": [0, 0.05, 0]
      }
    },
    {
      "name": "exhaust_pipe",
      "shape": "pipe",
      "size": [0.09, 0.07, 0.22, 12],
      "position": [-0.18, 0.65, -0.12],
      "rotation": [0, 0, 0],
      "color": "#718096",
      "texturePreset": "iron_cast",
      "parentId": "main_chassis",
      "wear": 0.6
    },
    {
      "name": "power_coupler_hex",
      "shape": "prism",
      "size": [0.08, 0.10, 6],
      "position": [0.18, 0.59, -0.12],
      "rotation": [0, 0, 0],
      "color": "#ecc94b",
      "texturePreset": "brass_burnished",
      "parentId": "main_chassis"
    },
    {
      "name": "front_console_wedge",
      "shape": "wedge",
      "size": [0.55, 0.32, 0.08],
      "position": [0, 0.30, 0.31],
      "rotation": [0, 0, 0],
      "color": "#2d3748",
      "texturePreset": "plastic_abs_matte",
      "parentId": "main_chassis"
    },
    {
      "name": "crt_telemetry_screen",
      "shape": "box",
      "size": [0.22, 0.14, 0.01],
      "position": [-0.12, 0.34, 0.355],
      "rotation": [0, 0, 0],
      "color": "#00ffcc",
      "texturePreset": "crt_screen_green",
      "emissive": "#00ffcc",
      "emissiveIntensity": 1.6,
      "parentId": "main_chassis"
    },
    {
      "name": "status_lamp_warning",
      "shape": "cylinder",
      "size": [0.02, 0.02, 0.02, 10],
      "position": [0.14, 0.38, 0.355],
      "rotation": [90, 0, 0],
      "color": "#ff3300",
      "emissive": "#ff3300",
      "emissiveIntensity": 2.0,
      "parentId": "main_chassis"
    },
    {
      "name": "inspection_hatch_door",
      "shape": "box",
      "size": [0.24, 0.20, 0.02],
      "position": [0, 0.55, 0.12],
      "rotation": [0, 0, 0],
      "pivot": [0, 0, -0.10],
      "color": "#4a5568",
      "texturePreset": "diamond_plate",
      "parentId": "main_chassis"
    }
  ],
  "animations": [
    {
      "id": "anim_hatch_open",
      "name": "InspectHatchOpen",
      "duration": 2.0,
      "loop": "pingpong",
      "presetType": "hinge_lid",
      "tracks": [
        {
          "targetComponent": "inspection_hatch_door",
          "property": "rotation",
          "keyframes": [
            { "time": 0.0, "value": [0, 0, 0] },
            { "time": 2.0, "value": [-65, 0, 0] }
          ]
        }
      ]
    }
  ]
}

Return ONLY valid JSON matching this schema:
{
  "id": "below_nominal.generated.${uniqueNonce}",
  "name": "<Human Readable Name in Spanish>",
  "category": "vehicles" | "furniture" | "infrastructure" | "command" | "medical" | "security" | "weapons",
  "description": "<Descriptive sentence in Spanish>",
  "units": "meters",
  "dimensions": { "width": <float>, "depth": <float>, "height": <float> },
  "palette": "industrial_hazard",
  "components": [
    {
      "name": "<unique_component_name>",
      "shape": "box" | "chamfer_box" | "cylinder" | "pipe" | "prism" | "pyramid" | "wedge" | "sphere" | "capsule" | "torus" | "cone" | "plane",
      "size": [<numbers>],
      "position": [<x>, <y>, <z>],
      "rotation": [<deg_x>, <deg_y>, <deg_z>],
      "color": "<hex_or_palette_name>",
      "parentId": "<optional_parent_component_name>",
      "pivot": [<optional_offsetX>, <optional_offsetY>, <optional_offsetZ>],
      "texturePreset": "<valid texturePreset>",
      "roughness": 0.7,
      "metalness": 0.2,
      "wear": 0.3,
      "normalStrength": 1.0,
      "emissive": "<optional_hex_color>",
      "emissiveIntensity": 1.5,
      "array": {
        "enabled": true,
        "type": "linear" | "radial",
        "count": <int_2_to_64>,
        "offset": [<dx>, <dy>, <dz>],
        "radialAxis": "x" | "y" | "z",
        "radialRadius": <float>,
        "radialAngle": <degrees_default_360>,
        "radialRotateCopies": true
      },
      "boolean": {
        "enabled": true,
        "operation": "difference" | "union" | "intersection",
        "targetComponent": "<other_component_name>",
        "hideTarget": true
      }
    }
  ],
  "animations": [
    {
      "id": "<clip_id>",
      "name": "<ClipName>",
      "duration": <seconds_float>,
      "loop": "repeat" | "pingpong" | "once",
      "presetType": "spin_continuous" | "idle_hover" | "sliding_door" | "hinge_lid" | "button_press" | "mechanical_deploy",
      "tracks": [
        {
          "targetComponent": "<target_component_name>",
          "property": "position" | "rotation" | "scale",
          "keyframes": [
            { "time": <sec>, "value": [<x>, <y>, <z>] }
          ]
        }
      ]
    }
  ]
}`;

    const payload = {
      system_instruction: {
        parts: [{ text: systemInstruction }]
      },
      contents: [{
        role: 'user',
        parts: [{
          text: `USER PROMPT: ${prompt}\nCREATION_ID: ${uniqueNonce}\nINSTRUCTION: Synthesize a brand-new, mechanically coherent, grounded 3D model with ZERO floating geometry.`
        }]
      }],
      generationConfig: {
        responseMimeType: 'application/json',
        temperature: 0.2
      }
    };

    // Google Gemini API production models in priority order (los modelos 1.5/2.0/2.5 fueron retirados y devuelven 404).
    // gemini-3.8-flash es el Flash estable actual; 3.7 y 3.6 quedan como respaldo si el primero no está disponible.
    const candidateModels = [
      'gemini-3.8-flash',
      'gemini-3.7-flash',
      'gemini-3.6-flash'
    ];
    let lastError: Error | null = null;

    for (const modelName of candidateModels) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
        const signal = typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function'
          ? AbortSignal.timeout(20000)
          : undefined;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal
        });

        if (!res.ok) {
          const errText = await res.text();
          lastError = new Error(`Gemini API error (${res.status}): ${errText}`);
          if (res.status === 404 || res.status === 400 || res.status === 429 || res.status >= 500 || errText.includes('NOT_FOUND') || errText.includes('no longer available')) {
            console.warn(`[AIGenerator] Intento con ${modelName} devolvió HTTP ${res.status}. Probando siguiente modelo de respaldo...`);
            continue;
          }
          throw lastError;
        }

        const data = await res.json();
        const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
        if (!candidateText) {
          throw new Error(`Gemini (${modelName}) no devolvió texto en la respuesta.`);
        }

        const cleanedJsonText = String(candidateText)
          .trim()
          .replace(/^```(?:json)?\s*/i, '')
          .replace(/\s*```$/i, '')
          .trim();

        const parsed = JSON.parse(cleanedJsonText) as ModelSpec;
        if (!parsed.components || parsed.components.length === 0) {
          throw new Error('La respuesta de Gemini no incluye componentes geométricos.');
        }

        const normalized = this.normalizeSpecGeometry(parsed);
        return { spec: normalized, rawResponse: cleanedJsonText };
      } catch (err: any) {
        lastError = err;
        console.warn(`[AIGenerator] Intento con ${modelName} falló:`, err);
        if (err?.name === 'TimeoutError' || err?.name === 'AbortError' || err?.message?.includes('404') || err?.message?.includes('NOT_FOUND') || err?.message?.includes('no longer available')) {
          continue;
        }
        throw err;
      }
    }

    if (lastError?.name === 'TimeoutError' || lastError?.name === 'AbortError') {
      throw new Error('Tiempo de espera agotado al conectar con Gemini API. Verifica tu conexión a internet o genera con el Motor Procedural Local.');
    }

    throw lastError || new Error('No se pudo conectar con ningún modelo de Gemini disponible.');
  }

  /**
   * Deterministic local procedural synthesizer that turns natural language phrases
   * into genuine, recognizable 3D models with proper components, proportions and colors.
   */
  public static synthesizeProceduralSpec(prompt: string): ModelSpec {
    const lower = prompt.toLowerCase();

    // Extract potential custom dimensions (e.g. "2 metros", "0.5m", "1.5x2")
    const dimMatch = lower.match(/(\d+(?:\.\d+)?)\s*(?:m|metros?|metres?)/);
    const baseDim = dimMatch ? Math.max(0.2, parseFloat(dimMatch[1])) : 1.0;

    // Detect primary color
    let mainColor = '#4a5568';
    if (/rojo|red|carmesí/.test(lower)) mainColor = '#e53e3e';
    else if (/azul|blue|celeste/.test(lower)) mainColor = '#3182ce';
    else if (/verde|green|militar/.test(lower)) mainColor = '#38a169';
    else if (/amarillo|yellow/.test(lower)) mainColor = '#d69e2e';
    else if (/naranja|orange/.test(lower)) mainColor = '#dd6b20';
    else if (/blanco|white|plateado/.test(lower)) mainColor = '#edf2f7';
    else if (/negro|dark|black|oscuro/.test(lower)) mainColor = '#1a202c';
    else if (/dorado|gold|oro/.test(lower)) mainColor = '#ecc94b';
    else if (/cian|cyan|turquesa/.test(lower)) mainColor = '#319795';
    else if (/gris|metal|acero|grey|gray/.test(lower)) mainColor = '#718096';
    else if (/marron|brown|oxido|rust/.test(lower)) mainColor = '#7b341e';

    // -------------------------------------------------------------
    // 1. VEHICLES: CAR / AUTO / COCHE / CARRO / VEHICULO
    // -------------------------------------------------------------
    if (/auto|coche|carro|automovil|vehiculo|car\b|buggy|rover/.test(lower)) {
      const cw = 1.6 * baseDim;
      const cd = 3.2 * baseDim;
      const ch = 0.45 * baseDim;
      const cabinH = 0.5 * baseDim;
      const wheelR = 0.32 * baseDim;
      const wheelW = 0.22 * baseDim;
      const axleX = cw * 0.52;
      const axleZ = cd * 0.30;

      return {
        id: 'below_nominal.vehicles.retro_car',
        name: 'Auto Terrestre PSX',
        category: 'vehicles',
        description: `Vehículo terrestre retro con chasis de ${cd.toFixed(1)}m, cabina acristalada y cuatro ruedas con llantas metálicas.`,
        units: 'meters',
        dimensions: { width: cw * 1.15, depth: cd, height: ch + cabinH + wheelR * 0.4 },
        palette: 'industrial_hazard',
        components: [
          // Lower chassis body
          {
            name: 'chassis_body',
            shape: 'box',
            size: [cw, ch, cd],
            position: [0, wheelR * 0.65 + ch * 0.5, 0],
            color: mainColor,
            texturePreset: 'worn_metal',
            roughness: 0.6,
            metalness: 0.3
          },
          // Cabin / Passenger roof
          {
            name: 'cabin_roof',
            shape: 'box',
            size: [cw * 0.85, cabinH, cd * 0.52],
            position: [0, wheelR * 0.65 + ch + cabinH * 0.5, -cd * 0.05],
            color: '#2d3748',
            texturePreset: 'painted_metal_white',
            roughness: 0.5,
            metalness: 0.4
          },
          // Slanted Windshield (wedge)
          {
            name: 'windshield',
            shape: 'wedge',
            size: [cw * 0.82, cabinH * 0.95, cd * 0.22],
            position: [0, wheelR * 0.65 + ch + cabinH * 0.5, cd * 0.32],
            color: '#319795', // Tinted glass
            roughness: 0.2,
            metalness: 0.1
          },
          // Slanted Rear Window
          {
            name: 'rear_window',
            shape: 'wedge',
            size: [cw * 0.82, cabinH * 0.95, cd * 0.18],
            position: [0, wheelR * 0.65 + ch + cabinH * 0.5, -cd * 0.40],
            rotation: [0, 180, 0],
            color: '#319795',
            roughness: 0.2
          },
          // 4 Wheels
          {
            name: 'wheel_front_left',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [-axleX, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          {
            name: 'wheel_front_right',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [axleX, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          {
            name: 'wheel_rear_left',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [-axleX, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          {
            name: 'wheel_rear_right',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [axleX, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          // 4 Metallic Rims
          {
            name: 'rim_fl',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [-axleX - 0.01, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          {
            name: 'rim_fr',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [axleX + 0.01, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          {
            name: 'rim_rl',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [-axleX - 0.01, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          {
            name: 'rim_rr',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [axleX + 0.01, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          // Front Headlights
          {
            name: 'headlight_left',
            shape: 'box',
            size: [cw * 0.18, ch * 0.35, 0.06],
            position: [-cw * 0.32, wheelR * 0.65 + ch * 0.65, cd * 0.505],
            color: '#ecc94b', // Yellow light
            roughness: 0.2
          },
          {
            name: 'headlight_right',
            shape: 'box',
            size: [cw * 0.18, ch * 0.35, 0.06],
            position: [cw * 0.32, wheelR * 0.65 + ch * 0.65, cd * 0.505],
            color: '#ecc94b',
            roughness: 0.2
          },
          // Rear Taillights
          {
            name: 'taillight_left',
            shape: 'box',
            size: [cw * 0.2, ch * 0.3, 0.06],
            position: [-cw * 0.32, wheelR * 0.65 + ch * 0.65, -cd * 0.505],
            color: '#e53e3e', // Red brake light
            roughness: 0.2
          },
          {
            name: 'taillight_right',
            shape: 'box',
            size: [cw * 0.2, ch * 0.3, 0.06],
            position: [cw * 0.32, wheelR * 0.65 + ch * 0.65, -cd * 0.505],
            color: '#e53e3e',
            roughness: 0.2
          },
          // Heavy Front Bumper
          {
            name: 'front_bumper',
            shape: 'box',
            size: [cw * 1.05, ch * 0.4, 0.2],
            position: [0, wheelR * 0.8, cd * 0.55],
            color: '#1a202c',
            metalness: 0.6
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 2. SPACESHIP / NAVE / COHETE / SHUTTLE / CAZA
    // -------------------------------------------------------------
    if (/nave|spaceship|cohete|rocket|shuttle|caza|aerodeslizador/.test(lower)) {
      const sw = 1.0 * baseDim;
      const sl = 3.6 * baseDim;
      const sh = 0.65 * baseDim;
      const wingSpan = 2.8 * baseDim;

      return {
        id: 'below_nominal.vehicles.space_fighter',
        name: 'Caza Espacial Interceptor',
        category: 'vehicles',
        description: 'Nave interceptora orbital con cabina presurizada, alas en cuña y propulsores dobles.',
        units: 'meters',
        dimensions: { width: wingSpan, depth: sl, height: sh * 1.8 },
        palette: 'command_bridge',
        components: [
          // Main Fuselage
          {
            name: 'fuselage_core',
            shape: 'box',
            size: [sw, sh, sl * 0.75],
            position: [0, sh * 0.9, -sl * 0.05],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Aerodynamic Nose Cone
          {
            name: 'nose_cone',
            shape: 'cone',
            size: [sw * 0.5, sl * 0.35, 8],
            position: [0, sh * 0.9, sl * 0.45],
            rotation: [90, 0, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Cockpit Canopy (wedge glass)
          {
            name: 'cockpit_canopy',
            shape: 'wedge',
            size: [sw * 0.65, sh * 0.65, sl * 0.28],
            position: [0, sh * 1.45, sl * 0.08],
            color: '#319795',
            roughness: 0.2
          },
          // Left Wing (wedge)
          {
            name: 'wing_left',
            shape: 'wedge',
            size: [wingSpan * 0.45, 0.08, sl * 0.45],
            position: [-sw * 0.5 - wingSpan * 0.22, sh * 0.85, -sl * 0.12],
            rotation: [0, 15, 0],
            color: mainColor,
            roughness: 0.6
          },
          // Right Wing (wedge)
          {
            name: 'wing_right',
            shape: 'wedge',
            size: [wingSpan * 0.45, 0.08, sl * 0.45],
            position: [sw * 0.5 + wingSpan * 0.22, sh * 0.85, -sl * 0.12],
            rotation: [0, -15, 0],
            color: mainColor,
            roughness: 0.6
          },
          // Vertical Stabilizer Fin
          {
            name: 'tail_fin',
            shape: 'wedge',
            size: [0.08, sh * 1.1, sl * 0.35],
            position: [0, sh * 1.7, -sl * 0.32],
            color: '#1a202c'
          },
          // Dual Thrusters
          {
            name: 'thruster_left',
            shape: 'cylinder',
            size: [sw * 0.22, sw * 0.25, sl * 0.2, 8],
            position: [-sw * 0.32, sh * 0.9, -sl * 0.45],
            rotation: [90, 0, 0],
            color: '#718096',
            metalness: 0.8
          },
          {
            name: 'thruster_right',
            shape: 'cylinder',
            size: [sw * 0.22, sw * 0.25, sl * 0.2, 8],
            position: [sw * 0.32, sh * 0.9, -sl * 0.45],
            rotation: [90, 0, 0],
            color: '#718096',
            metalness: 0.8
          },
          // Plasma Exhaust Plumes
          {
            name: 'plasma_left',
            shape: 'cone',
            size: [sw * 0.16, sl * 0.18, 6],
            position: [-sw * 0.32, sh * 0.9, -sl * 0.58],
            rotation: [-90, 0, 0],
            color: '#3182ce'
          },
          {
            name: 'plasma_right',
            shape: 'cone',
            size: [sw * 0.16, sl * 0.18, 6],
            position: [sw * 0.32, sh * 0.9, -sl * 0.58],
            rotation: [-90, 0, 0],
            color: '#3182ce'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 3. ROBOT / MECH / ANDROIDE / AUTÓMATA
    // -------------------------------------------------------------
    if (/robot|mech|androide|automata|droide/.test(lower)) {
      const rw = 0.8 * baseDim;
      const rh = 1.9 * baseDim;
      const rd = 0.5 * baseDim;

      return {
        id: 'below_nominal.security.service_droid',
        name: 'Unidad Robótica Bípeda',
        category: 'security',
        description: 'Autómata procedural con torso reforzado, visor óptico y extremidades mecánicas.',
        units: 'meters',
        dimensions: { width: rw * 1.5, depth: rd * 1.2, height: rh },
        palette: 'industrial_hazard',
        components: [
          // Torso Core
          {
            name: 'torso_chassis',
            shape: 'box',
            size: [rw, rh * 0.35, rd],
            position: [0, rh * 0.65, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Head Unit
          {
            name: 'head_unit',
            shape: 'box',
            size: [rw * 0.5, rh * 0.18, rd * 0.8],
            position: [0, rh * 0.92, 0],
            color: '#2d3748',
            roughness: 0.7
          },
          // Optical Visor LED
          {
            name: 'optical_visor',
            shape: 'box',
            size: [rw * 0.42, rh * 0.05, 0.05],
            position: [0, rh * 0.92, rd * 0.42],
            color: '#e53e3e',
            roughness: 0.2
          },
          // Head Antenna
          {
            name: 'comm_antenna',
            shape: 'cylinder',
            size: [0.015, 0.015, rh * 0.18, 4],
            position: [rw * 0.2, rh * 1.08, 0],
            color: '#cbd5e0'
          },
          // Pelvis Mount
          {
            name: 'pelvis_mount',
            shape: 'box',
            size: [rw * 0.75, rh * 0.1, rd * 0.85],
            position: [0, rh * 0.43, 0],
            color: '#1a202c'
          },
          // Legs
          {
            name: 'leg_left',
            shape: 'box',
            size: [rw * 0.24, rh * 0.38, rd * 0.5],
            position: [-rw * 0.26, rh * 0.2, 0],
            color: mainColor,
            metalness: 0.5
          },
          {
            name: 'leg_right',
            shape: 'box',
            size: [rw * 0.24, rh * 0.38, rd * 0.5],
            position: [rw * 0.26, rh * 0.2, 0],
            color: mainColor,
            metalness: 0.5
          },
          // Feet Plates
          {
            name: 'foot_left',
            shape: 'box',
            size: [rw * 0.28, 0.06, rd * 0.9],
            position: [-rw * 0.26, 0.03, rd * 0.15],
            color: '#1a202c'
          },
          {
            name: 'foot_right',
            shape: 'box',
            size: [rw * 0.28, 0.06, rd * 0.9],
            position: [rw * 0.26, 0.03, rd * 0.15],
            color: '#1a202c'
          },
          // Arms
          {
            name: 'arm_left',
            shape: 'box',
            size: [rw * 0.18, rh * 0.35, rd * 0.4],
            position: [-rw * 0.62, rh * 0.62, 0],
            color: '#4a5568'
          },
          {
            name: 'arm_right',
            shape: 'box',
            size: [rw * 0.18, rh * 0.35, rd * 0.4],
            position: [rw * 0.62, rh * 0.62, 0],
            color: '#4a5568'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 4. WEAPON / PISTOLA / BLASTER / ARMA / RIFLE
    // -------------------------------------------------------------
    if (/arma|pistola|blaster|rifle|fusil|laser|gun|canon|torreta/.test(lower)) {
      const gw = 0.12 * baseDim;
      const gh = 0.45 * baseDim;
      const gl = 0.95 * baseDim;

      return {
        id: 'below_nominal.weapons.plasma_blaster',
        name: 'Blaster de Plasma Retro',
        category: 'weapons',
        description: 'Arma de energía con empuñadura ergonómica, cañón reforzado y celda de plasma.',
        units: 'meters',
        dimensions: { width: gw * 1.5, depth: gl, height: gh },
        palette: 'industrial_hazard',
        components: [
          // Handle / Grip
          {
            name: 'grip_handle',
            shape: 'box',
            size: [gw * 0.8, gh * 0.55, gl * 0.2],
            position: [0, gh * 0.28, -gl * 0.25],
            rotation: [15, 0, 0],
            color: '#1a202c',
            roughness: 0.9
          },
          // Receiver Body
          {
            name: 'receiver_core',
            shape: 'box',
            size: [gw, gh * 0.4, gl * 0.65],
            position: [0, gh * 0.65, gl * 0.05],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Barrel Cylinder
          {
            name: 'plasma_barrel',
            shape: 'cylinder',
            size: [gw * 0.4, gw * 0.4, gl * 0.45, 8],
            position: [0, gh * 0.68, gl * 0.55],
            rotation: [90, 0, 0],
            color: '#718096',
            metalness: 0.8
          },
          // Muzzle Flash Hider
          {
            name: 'muzzle_tip',
            shape: 'cylinder',
            size: [gw * 0.48, gw * 0.45, gl * 0.08, 8],
            position: [0, gh * 0.68, gl * 0.8],
            rotation: [90, 0, 0],
            color: '#1a202c',
            metalness: 0.9
          },
          // Optical Scope
          {
            name: 'targeting_scope',
            shape: 'box',
            size: [gw * 0.6, gh * 0.18, gl * 0.32],
            position: [0, gh * 0.92, -gl * 0.02],
            color: '#e53e3e',
            roughness: 0.3
          },
          // Energy Cell Magazine
          {
            name: 'energy_magazine',
            shape: 'box',
            size: [gw * 0.75, gh * 0.3, gl * 0.18],
            position: [0, gh * 0.35, gl * 0.08],
            color: '#319795',
            roughness: 0.3
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 5. CHAIR / SILLA / ASIENTO / BUTACA / SOFA
    // -------------------------------------------------------------
    if (/silla|chair|asiento|butaca|sofa|sillon|banco/.test(lower) && !/mesa|consola/.test(lower)) {
      const sw = 0.65 * baseDim;
      const sd = 0.65 * baseDim;
      const sh = 0.95 * baseDim;
      const seatH = 0.45 * baseDim;

      return {
        id: 'below_nominal.furniture.station_chair',
        name: 'Silla Operativa de Mando',
        category: 'furniture',
        description: 'Asiento ergonómico reforzado con respaldo curvo y base tubular.',
        units: 'meters',
        dimensions: { width: sw, depth: sd, height: sh },
        palette: 'standard',
        components: [
          // Seat Pad
          {
            name: 'seat_cushion',
            shape: 'box',
            size: [sw, 0.08, sd],
            position: [0, seatH, 0],
            color: mainColor,
            roughness: 0.7
          },
          // Backrest
          {
            name: 'backrest',
            shape: 'box',
            size: [sw * 0.92, sh - seatH, 0.08],
            position: [0, seatH + (sh - seatH) * 0.5, -sd * 0.45],
            color: mainColor,
            roughness: 0.7
          },
          // 4 Legs
          {
            name: 'leg_front_left',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [-sw * 0.4, (seatH - 0.04) * 0.5, sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          },
          {
            name: 'leg_front_right',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [sw * 0.4, (seatH - 0.04) * 0.5, sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          },
          {
            name: 'leg_rear_left',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [-sw * 0.4, (seatH - 0.04) * 0.5, -sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          },
          {
            name: 'leg_rear_right',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [sw * 0.4, (seatH - 0.04) * 0.5, -sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 6. DOOR / PUERTA / COMPUERTA / AIRLOCK / HATCH
    // -------------------------------------------------------------
    if (/puerta|door|compuerta|airlock|hatch/.test(lower)) {
      const dw = 1.4 * baseDim;
      const dh = 2.2 * baseDim;
      const dd = 0.25 * baseDim;

      return {
        id: 'below_nominal.infrastructure.airlock_door',
        name: 'Compuerta de Presión Blindada',
        category: 'infrastructure',
        description: 'Puerta hermética de doble hoja con marco blindado y panel de control de acceso.',
        units: 'meters',
        dimensions: { width: dw, depth: dd, height: dh },
        palette: 'industrial_hazard',
        components: [
          // Left Door Frame
          {
            name: 'frame_left',
            shape: 'box',
            size: [dw * 0.12, dh, dd],
            position: [-dw * 0.44, dh * 0.5, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Right Door Frame
          {
            name: 'frame_right',
            shape: 'box',
            size: [dw * 0.12, dh, dd],
            position: [dw * 0.44, dh * 0.5, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Top Frame Header
          {
            name: 'frame_top',
            shape: 'box',
            size: [dw, dh * 0.08, dd],
            position: [0, dh * 0.96, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Left Sliding Panel
          {
            name: 'panel_left',
            shape: 'box',
            size: [dw * 0.38, dh * 0.88, dd * 0.4],
            position: [-dw * 0.19, dh * 0.48, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Right Sliding Panel
          {
            name: 'panel_right',
            shape: 'box',
            size: [dw * 0.38, dh * 0.88, dd * 0.4],
            position: [dw * 0.19, dh * 0.48, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Keypad / Access Reader
          {
            name: 'access_keypad',
            shape: 'box',
            size: [0.15, 0.25, 0.04],
            position: [dw * 0.48, dh * 0.55, dd * 0.52],
            color: '#319795',
            roughness: 0.3
          },
          // Status LED Beacon (Green)
          {
            name: 'status_beacon',
            shape: 'box',
            size: [0.12, 0.06, 0.04],
            position: [0, dh * 0.94, dd * 0.52],
            color: '#38a169',
            roughness: 0.2
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 7. DRONE / CUADRICÓPTERO / DRON
    // -------------------------------------------------------------
    if (/dron|drone|cuadricoptero|probeta|sensor orbital/.test(lower)) {
      const bw = 0.45 * baseDim;
      const armL = 0.5 * baseDim;
      const rotR = 0.25 * baseDim;

      return {
        id: 'below_nominal.security.survey_drone',
        name: 'Dron de Vigilancia Orbital',
        category: 'security',
        description: 'Sonda voladora autónoma con 4 rotores perimetrales y sensor fotónico inferior.',
        units: 'meters',
        dimensions: { width: armL * 2.8, depth: armL * 2.8, height: bw * 1.2 },
        palette: 'industrial_hazard',
        components: [
          // Central Core
          {
            name: 'core_fuselage',
            shape: 'cylinder',
            size: [bw * 0.5, bw * 0.5, bw * 0.6, 8],
            position: [0, bw * 0.8, 0],
            color: mainColor,
            metalness: 0.4
          },
          // Sensor Dome (eye)
          {
            name: 'sensor_eye',
            shape: 'sphere',
            size: [bw * 0.25, 8, 6],
            position: [0, bw * 0.48, 0],
            color: '#319795'
          },
          // 4 Carbon Arms in X
          {
            name: 'arm_fl',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [-armL * 0.5, bw * 0.8, armL * 0.5],
            rotation: [0, 45, 0],
            color: '#1a202c'
          },
          {
            name: 'arm_fr',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [armL * 0.5, bw * 0.8, armL * 0.5],
            rotation: [0, -45, 0],
            color: '#1a202c'
          },
          {
            name: 'arm_rl',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [-armL * 0.5, bw * 0.8, -armL * 0.5],
            rotation: [0, -45, 0],
            color: '#1a202c'
          },
          {
            name: 'arm_rr',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [armL * 0.5, bw * 0.8, -armL * 0.5],
            rotation: [0, 45, 0],
            color: '#1a202c'
          },
          // 4 Rotors
          {
            name: 'rotor_fl',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [-armL * 0.85, bw * 0.86, armL * 0.85],
            color: '#718096'
          },
          {
            name: 'rotor_fr',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [armL * 0.85, bw * 0.86, armL * 0.85],
            color: '#718096'
          },
          {
            name: 'rotor_rl',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [-armL * 0.85, bw * 0.86, -armL * 0.85],
            color: '#718096'
          },
          {
            name: 'rotor_rr',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [armL * 0.85, bw * 0.86, -armL * 0.85],
            color: '#718096'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 8. BED / CAMA / LITERA / CAMILLA
    // -------------------------------------------------------------
    if (/cama|litera|camilla|stasis|cryo/.test(lower)) {
      const bw = 1.0 * baseDim;
      const bl = 2.1 * baseDim;
      const bh = 0.55 * baseDim;

      return {
        id: 'below_nominal.furniture.station_bed',
        name: 'Cama / Camilla de Estación',
        category: 'furniture',
        description: 'Litera modular de tripulación con colchón higiénico y cabecero integrado.',
        units: 'meters',
        dimensions: { width: bw, depth: bl, height: bh * 1.5 },
        palette: 'standard',
        components: [
          // Frame Base
          {
            name: 'bed_frame',
            shape: 'box',
            size: [bw, bh * 0.5, bl],
            position: [0, bh * 0.25, 0],
            color: '#2d3748',
            metalness: 0.5
          },
          // Mattress
          {
            name: 'mattress',
            shape: 'box',
            size: [bw * 0.94, bh * 0.35, bl * 0.94],
            position: [0, bh * 0.65, 0],
            color: mainColor,
            roughness: 0.8
          },
          // Pillow
          {
            name: 'pillow',
            shape: 'box',
            size: [bw * 0.75, bh * 0.18, bl * 0.2],
            position: [0, bh * 0.88, -bl * 0.35],
            color: '#edf2f7',
            roughness: 0.9
          },
          // Headboard
          {
            name: 'headboard',
            shape: 'box',
            size: [bw, bh * 0.9, 0.1],
            position: [0, bh * 0.8, -bl * 0.48],
            color: '#1a202c'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 9. COMPUTER / LAPTOP / MONITOR / PANTALLA
    // -------------------------------------------------------------
    if (/computadora|computador|laptop|monitor|pantalla|display|pc/.test(lower) && !/consola/.test(lower)) {
      const lw = 0.6 * baseDim;
      const ld = 0.45 * baseDim;

      return {
        id: 'below_nominal.command.terminal_screen',
        name: 'Terminal de Pantalla y Teclado',
        category: 'command',
        description: 'Unidad de computación personal con display fosfórico y teclado integrado.',
        units: 'meters',
        dimensions: { width: lw, depth: ld, height: lw * 0.8 },
        palette: 'command_bridge',
        components: [
          // Keyboard Base
          {
            name: 'keyboard_base',
            shape: 'box',
            size: [lw, 0.04, ld * 0.65],
            position: [0, 0.02, ld * 0.15],
            color: '#1a202c',
            roughness: 0.8
          },
          // Slanted Screen Housing
          {
            name: 'screen_housing',
            shape: 'box',
            size: [lw * 0.95, lw * 0.65, 0.05],
            position: [0, lw * 0.38, -ld * 0.2],
            rotation: [-15, 0, 0],
            color: mainColor,
            metalness: 0.3
          },
          // Active Display (Cyan phosphor)
          {
            name: 'screen_display',
            shape: 'box',
            size: [lw * 0.85, lw * 0.52, 0.01],
            position: [0, lw * 0.38, -ld * 0.17],
            rotation: [-15, 0, 0],
            color: '#319795',
            roughness: 0.2
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 10. SERVER RACK / SERVIDOR
    // -------------------------------------------------------------
    if (/servidor|server|rack|rack de servidores/.test(lower)) {
      const rw = 0.8 * baseDim;
      const rh = 2.0 * baseDim;
      const rd = 0.9 * baseDim;

      return {
        id: 'below_nominal.command.server_rack',
        name: 'Rack de Servidores Principal',
        category: 'command',
        description: 'Gabinete vertical de cómputo con bahías ventiladas y telemetría LED.',
        units: 'meters',
        dimensions: { width: rw, depth: rd, height: rh },
        palette: 'command_bridge',
        components: [
          // Main Server Cabinet
          {
            name: 'rack_cabinet',
            shape: 'box',
            size: [rw, rh, rd],
            position: [0, rh * 0.5, 0],
            color: '#1a202c',
            metalness: 0.7
          },
          // Server Blade Bay 1
          {
            name: 'blade_bay_1',
            shape: 'box',
            size: [rw * 0.88, rh * 0.12, 0.02],
            position: [0, rh * 0.8, rd * 0.505],
            color: mainColor,
            metalness: 0.5
          },
          // Server Blade Bay 2
          {
            name: 'blade_bay_2',
            shape: 'box',
            size: [rw * 0.88, rh * 0.12, 0.02],
            position: [0, rh * 0.62, rd * 0.505],
            color: mainColor,
            metalness: 0.5
          },
          // Server Blade Bay 3
          {
            name: 'blade_bay_3',
            shape: 'box',
            size: [rw * 0.88, rh * 0.12, 0.02],
            position: [0, rh * 0.44, rd * 0.505],
            color: mainColor,
            metalness: 0.5
          },
          // LED Status Lights
          {
            name: 'led_array_1',
            shape: 'box',
            size: [0.12, 0.03, 0.01],
            position: [-rw * 0.3, rh * 0.8, rd * 0.52],
            color: '#38a169'
          },
          {
            name: 'led_array_2',
            shape: 'box',
            size: [0.12, 0.03, 0.01],
            position: [-rw * 0.3, rh * 0.62, rd * 0.52],
            color: '#ecc94b'
          },
          {
            name: 'led_array_3',
            shape: 'box',
            size: [0.12, 0.03, 0.01],
            position: [-rw * 0.3, rh * 0.44, rd * 0.52],
            color: '#3182ce'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 11. BARREL / BARRIL / TANQUE / DRUM
    // -------------------------------------------------------------
    if (/barril|barrel|drum|bidon|tanque de combustible/.test(lower) && !/columna/.test(lower)) {
      const br = 0.35 * baseDim;
      const bh = 1.0 * baseDim;

      return {
        id: 'below_nominal.infrastructure.chemical_drum',
        name: 'Barril Químico Estriado',
        category: 'infrastructure',
        description: 'Contenedor cilíndrico estriado para fluidos presurizados con aros de refuerzo.',
        units: 'meters',
        dimensions: { width: br * 2.2, depth: br * 2.2, height: bh },
        palette: 'industrial_hazard',
        components: [
          // Main Drum Body
          {
            name: 'drum_body',
            shape: 'cylinder',
            size: [br, br, bh, 10],
            position: [0, bh * 0.5, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Top Reinforcement Rib
          {
            name: 'rib_top',
            shape: 'cylinder',
            size: [br * 1.06, br * 1.06, 0.06, 10],
            position: [0, bh * 0.75, 0],
            color: '#1a202c'
          },
          // Bottom Reinforcement Rib
          {
            name: 'rib_bottom',
            shape: 'cylinder',
            size: [br * 1.06, br * 1.06, 0.06, 10],
            position: [0, bh * 0.25, 0],
            color: '#1a202c'
          },
          // Valve Cap
          {
            name: 'valve_cap',
            shape: 'cylinder',
            size: [br * 0.2, br * 0.2, 0.05, 6],
            position: [br * 0.45, bh + 0.02, 0],
            color: '#d69e2e',
            metalness: 0.7
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 11B. WELDING MACHINE / SOLDADORA / GENERADOR / INVERTER
    // -------------------------------------------------------------
    if (/soldar|soldadora|soldadura|generador|soldador|maquina de soldar|planta electrica|inverter|compresor/.test(lower)) {
      const sw = 0.72 * baseDim;
      const sh = 0.54 * baseDim;
      const sd = 0.52 * baseDim;

      return {
        id: 'below_nominal.infrastructure.industrial_welder',
        name: 'Unidad de Soldadura Industrial Inverter ARC-400',
        category: 'infrastructure',
        description: 'Estación de soldadura industrial pesada con panel de control digital, tanque de argón y asa de transporte.',
        units: 'meters',
        dimensions: { width: sw * 1.15, depth: sd * 1.1, height: sh * 1.3 },
        palette: 'industrial_hazard',
        components: [
          // Lower Chassis Base Plinth
          {
            name: 'chassis_plinth',
            shape: 'box',
            size: [sw, 0.06 * baseDim, sd],
            position: [0, 0.03 * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'diamond_plate',
            metalness: 0.7,
            roughness: 0.5
          },
          // 4 Ground Dampeners (Rubber Feet)
          {
            name: 'rubber_foot_fl',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [-sw * 0.42, 0.02 * baseDim, sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          {
            name: 'rubber_foot_fr',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [sw * 0.42, 0.02 * baseDim, sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          {
            name: 'rubber_foot_bl',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [-sw * 0.42, 0.02 * baseDim, -sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          {
            name: 'rubber_foot_br',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [sw * 0.42, 0.02 * baseDim, -sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          // Main Transformer Housing
          {
            name: 'inverter_housing',
            shape: 'box',
            size: [sw * 0.92, sh * 0.85, sd * 0.88],
            position: [0, (0.06 + sh * 0.425) * baseDim, 0],
            color: mainColor || '#dd6b20',
            texturePreset: 'worn_metal',
            metalness: 0.4,
            roughness: 0.6
          },
          // Front Control Panel Plate (Flush mounted)
          {
            name: 'front_control_plate',
            shape: 'box',
            size: [sw * 0.80, sh * 0.70, 0.02 * baseDim],
            position: [0, (0.06 + sh * 0.425) * baseDim, (sd * 0.44 + 0.01) * baseDim],
            color: '#2d3748',
            texturePreset: 'plastic_abs_matte',
            roughness: 0.8
          },
          // Digital Amperage Display Screen
          {
            name: 'digital_screen',
            shape: 'box',
            size: [0.20 * baseDim, 0.10 * baseDim, 0.01 * baseDim],
            position: [-0.14 * baseDim, (0.06 + sh * 0.55) * baseDim, (sd * 0.44 + 0.025) * baseDim],
            color: '#38a169',
            texturePreset: 'crt_screen_green'
          },
          // Rotary Control Dial
          {
            name: 'amperage_rotary_dial',
            shape: 'cylinder',
            size: [0.045 * baseDim, 0.045 * baseDim, 0.03 * baseDim, 12],
            position: [0.14 * baseDim, (0.06 + sh * 0.55) * baseDim, (sd * 0.44 + 0.035) * baseDim],
            rotation: [90, 0, 0],
            color: '#ecc94b',
            texturePreset: 'brass_burnished'
          },
          // Negative Ground Dinse Connector
          {
            name: 'terminal_ground_dinse',
            shape: 'cylinder',
            size: [0.03 * baseDim, 0.03 * baseDim, 0.04 * baseDim, 10],
            position: [-0.16 * baseDim, (0.06 + sh * 0.22) * baseDim, (sd * 0.44 + 0.04) * baseDim],
            rotation: [90, 0, 0],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          // Positive Electrode Dinse Connector
          {
            name: 'terminal_electrode_dinse',
            shape: 'cylinder',
            size: [0.03 * baseDim, 0.03 * baseDim, 0.04 * baseDim, 10],
            position: [0.16 * baseDim, (0.06 + sh * 0.22) * baseDim, (sd * 0.44 + 0.04) * baseDim],
            rotation: [90, 0, 0],
            color: '#e53e3e',
            texturePreset: 'red_paint_worn'
          },
          // Top Ergonomic Carry Handle
          {
            name: 'top_handle_grip',
            shape: 'box',
            size: [0.38 * baseDim, 0.045 * baseDim, 0.04 * baseDim],
            position: [0, (0.06 + sh * 0.85 + 0.08) * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'rubber_ribbed_mat'
          },
          {
            name: 'handle_riser_front',
            shape: 'box',
            size: [0.04 * baseDim, 0.08 * baseDim, 0.04 * baseDim],
            position: [0, (0.06 + sh * 0.85 + 0.04) * baseDim, 0.16 * baseDim],
            color: '#718096',
            texturePreset: 'steel_polished'
          },
          {
            name: 'handle_riser_back',
            shape: 'box',
            size: [0.04 * baseDim, 0.08 * baseDim, 0.04 * baseDim],
            position: [0, (0.06 + sh * 0.85 + 0.04) * baseDim, -0.16 * baseDim],
            color: '#718096',
            texturePreset: 'steel_polished'
          },
          // Side Exhaust Vent Grill
          {
            name: 'side_cooling_vent_left',
            shape: 'box',
            size: [0.01 * baseDim, sh * 0.50, sd * 0.60],
            position: [-sw * 0.465 * baseDim, (0.06 + sh * 0.425) * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'vent_grill'
          },
          {
            name: 'side_cooling_vent_right',
            shape: 'box',
            size: [0.01 * baseDim, sh * 0.50, sd * 0.60],
            position: [sw * 0.465 * baseDim, (0.06 + sh * 0.425) * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'vent_grill'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 12. CRATE / CAJA / CONTENEDOR / BAUL
    // -------------------------------------------------------------
    if (/caja|crate|contenedor|container|baul|cofre|cargo/.test(lower)) {
      const cw = 1.0 * baseDim;
      const ch = 0.85 * baseDim;
      const cd = 1.0 * baseDim;

      return {
        id: 'below_nominal.infrastructure.cargo_crate',
        name: 'Contenedor de Carga Reforzado',
        category: 'infrastructure',
        description: 'Caja cúbica de transporte con cantoneras de acero y nervaduras diagonales.',
        units: 'meters',
        dimensions: { width: cw, depth: cd, height: ch },
        palette: 'industrial_hazard',
        components: [
          // Main Crate Core
          {
            name: 'crate_core',
            shape: 'box',
            size: [cw, ch, cd],
            position: [0, ch * 0.5, 0],
            color: mainColor,
            roughness: 0.7
          },
          // Top Rim Frame
          {
            name: 'rim_top',
            shape: 'box',
            size: [cw * 1.04, 0.08, cd * 1.04],
            position: [0, ch * 0.96, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Bottom Rim Frame
          {
            name: 'rim_bottom',
            shape: 'box',
            size: [cw * 1.04, 0.08, cd * 1.04],
            position: [0, 0.04, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Front Cross Stiffener
          {
            name: 'front_latch',
            shape: 'box',
            size: [cw * 0.25, ch * 0.15, 0.04],
            position: [0, ch * 0.5, cd * 0.51],
            color: '#ecc94b',
            metalness: 0.8
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 13. LAMP / FOCO / LINTERNA / BALIZA / LUZ
    // -------------------------------------------------------------
    if (/lampara|foco|linterna|luz|baliza|farola|sirena/.test(lower)) {
      const lh = 1.8 * baseDim;
      const lr = 0.04 * baseDim;

      return {
        id: 'below_nominal.fixtures.light_post',
        name: 'Poste de Iluminación Industrial',
        category: 'fixtures',
        description: 'Luminaria vertical con pie estabilizador y cabezal difusor de alta emisión.',
        units: 'meters',
        dimensions: { width: 0.6 * baseDim, depth: 0.6 * baseDim, height: lh },
        palette: 'standard',
        components: [
          // Base Pedestal
          {
            name: 'pedestal',
            shape: 'cylinder',
            size: [0.25, 0.28, 0.08, 8],
            position: [0, 0.04, 0],
            color: '#1a202c'
          },
          // Pole
          {
            name: 'lamp_pole',
            shape: 'cylinder',
            size: [lr, lr, lh * 0.8, 6],
            position: [0, lh * 0.44, 0],
            color: '#4a5568',
            metalness: 0.6
          },
          // Lamp Housing
          {
            name: 'lamp_housing',
            shape: 'box',
            size: [0.45, 0.15, 0.3],
            position: [0, lh * 0.88, 0],
            color: mainColor,
            metalness: 0.4
          },
          // Bright Emissive Lens
          {
            name: 'emissive_lens',
            shape: 'box',
            size: [0.4, 0.06, 0.26],
            position: [0, lh * 0.82, 0],
            color: '#ecc94b',
            roughness: 0.1
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 14. ANTENNA / RADAR / DISH
    // -------------------------------------------------------------
    if (/antena|radar|dish|parabolica|comunicaciones/.test(lower)) {
      const ah = 2.4 * baseDim;
      const dishR = 0.8 * baseDim;

      return {
        id: 'below_nominal.infrastructure.radar_dish',
        name: 'Antena Parabólica de Enlace',
        category: 'infrastructure',
        description: 'Receptor parabólico orbital con mástil orientable y emisor focal.',
        units: 'meters',
        dimensions: { width: dishR * 2, depth: dishR * 2, height: ah },
        palette: 'standard',
        components: [
          // Base Tripod Mount
          {
            name: 'mount_base',
            shape: 'cylinder',
            size: [0.4, 0.5, 0.15, 6],
            position: [0, 0.075, 0],
            color: '#1a202c'
          },
          // Mast
          {
            name: 'antenna_mast',
            shape: 'cylinder',
            size: [0.06, 0.06, ah * 0.6, 6],
            position: [0, ah * 0.35, 0],
            color: '#718096',
            metalness: 0.7
          },
          // Dish Back Frame
          {
            name: 'dish_frame',
            shape: 'cylinder',
            size: [dishR, dishR * 0.3, 0.12, 10],
            position: [0, ah * 0.75, 0],
            rotation: [30, 0, 0],
            color: mainColor,
            metalness: 0.5
          },
          // Focal Feed Horn
          {
            name: 'feed_horn',
            shape: 'cylinder',
            size: [0.04, 0.08, 0.35, 6],
            position: [0, ah * 0.85, dishR * 0.4],
            rotation: [30, 0, 0],
            color: '#e53e3e',
            metalness: 0.8
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 15. SWORD / ESPADA / SABLE / CUCHILLO
    // -------------------------------------------------------------
    if (/espada|sable|sword|cuchillo|daga/.test(lower)) {
      const swL = 1.1 * baseDim;

      return {
        id: 'below_nominal.weapons.energy_blade',
        name: 'Sable de Plasma Táctico',
        category: 'weapons',
        description: 'Hoja cuerpo a cuerpo de alta frecuencia con guarda transversal y empuñadura aislante.',
        units: 'meters',
        dimensions: { width: 0.35 * baseDim, depth: 0.1 * baseDim, height: swL },
        palette: 'standard',
        components: [
          // Blade
          {
            name: 'blade_edge',
            shape: 'box',
            size: [0.06, swL * 0.72, 0.02],
            position: [0, swL * 0.62, 0],
            color: mainColor === '#4a5568' ? '#319795' : mainColor,
            roughness: 0.2,
            metalness: 0.9
          },
          // Crossguard
          {
            name: 'crossguard',
            shape: 'box',
            size: [0.28, 0.04, 0.06],
            position: [0, swL * 0.25, 0],
            color: '#1a202c',
            metalness: 0.8
          },
          // Hilt
          {
            name: 'hilt_grip',
            shape: 'cylinder',
            size: [0.025, 0.025, swL * 0.2, 8],
            position: [0, swL * 0.14, 0],
            color: '#2d3748',
            roughness: 0.8
          },
          // Pommel
          {
            name: 'pommel_sphere',
            shape: 'sphere',
            size: [0.035, 6, 4],
            position: [0, swL * 0.03, 0],
            color: '#ecc94b',
            metalness: 0.8
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 16. SPHERE / ESFERA / ORBE
    // -------------------------------------------------------------
    if (/esfera|sphere|pelota|bola|orb|globo/.test(lower)) {
      const r = Math.max(0.1, baseDim * 0.5);
      return {
        id: 'below_nominal.custom.procedural_sphere',
        name: 'Esfera Procedural Calibrada',
        category: 'fixtures',
        description: `Esfera procedural de radio ${r}m con color ${mainColor}.`,
        units: 'meters',
        dimensions: { width: r * 2, depth: r * 2, height: r * 2 },
        palette: 'standard',
        components: [
          {
            name: 'main_sphere',
            shape: 'sphere',
            size: [r, 12, 8],
            position: [0, r, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.2
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 17. CUBE / CUBO / BLOQUE / DADO
    // -------------------------------------------------------------
    if (/cubo|cube|bloque|dado/.test(lower) && !/tarjeta|consola/.test(lower)) {
      const s = Math.max(0.1, baseDim);
      return {
        id: 'below_nominal.custom.procedural_cube',
        name: 'Cubo Procedural Preciso',
        category: 'furniture',
        description: `Cubo procedural de lado ${s}m con color ${mainColor}.`,
        units: 'meters',
        dimensions: { width: s, depth: s, height: s },
        palette: 'standard',
        components: [
          {
            name: 'main_box',
            shape: 'box',
            size: [s, s, s],
            position: [0, s * 0.5, 0],
            color: mainColor,
            roughness: 0.7,
            metalness: 0.3
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 18. CYLINDER / CILINDRO / COLUMNA
    // -------------------------------------------------------------
    if (/cilindro|cylinder|columna|pilar/.test(lower)) {
      const r = Math.max(0.05, baseDim * 0.3);
      const h = Math.max(0.1, baseDim * 1.2);
      return {
        id: 'below_nominal.custom.procedural_cylinder',
        name: 'Columna Industrial Cilíndrica',
        category: 'infrastructure',
        description: `Columna procedural de altura ${h}m y radio ${r}m.`,
        units: 'meters',
        dimensions: { width: r * 2, depth: r * 2, height: h },
        palette: 'standard',
        components: [
          {
            name: 'base_pedestal',
            shape: 'box',
            size: [r * 2.4, 0.06, r * 2.4],
            position: [0, 0.03, 0],
            color: '#1a202c',
            roughness: 0.8
          },
          {
            name: 'column_body',
            shape: 'cylinder',
            size: [r, r, h - 0.06, 8],
            position: [0, (h + 0.06) * 0.5, 0],
            color: mainColor,
            roughness: 0.65,
            metalness: 0.4
          },
          {
            name: 'top_cap',
            shape: 'cylinder',
            size: [r * 1.1, r * 1.1, 0.04, 8],
            position: [0, h - 0.02, 0],
            color: '#718096',
            metalness: 0.5
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 19. ACCESS CARD / TARJETA DE SEGURIDAD (Criterion 3)
    // -------------------------------------------------------------
    if (/tarjeta|card|keycard|credencial|badge|pase|acceso/.test(lower)) {
      const w = 0.54 * baseDim;
      const h = 0.86 * baseDim;
      const thick = 0.025;
      return {
        id: 'below_nominal.security.access_card',
        name: 'Tarjeta de Acceso Nivel 1',
        category: 'security',
        description: 'Tarjeta de acceso magnética y biométrica con chip dorado y banda magnética.',
        units: 'meters',
        dimensions: { width: w, depth: thick, height: h },
        palette: 'standard',
        components: [
          {
            name: 'card_body',
            shape: 'box',
            size: [w, h, thick],
            position: [0, h * 0.5, 0],
            color: mainColor === '#4a5568' ? '#ffffff' : mainColor,
            texturePreset: 'painted_metal_white',
            roughness: 0.8,
            metalness: 0.1
          },
          {
            name: 'security_header',
            shape: 'box',
            size: [w * 0.96, h * 0.22, thick * 1.05],
            position: [0, h * 0.82, 0],
            color: '#e53e3e',
            roughness: 0.5
          },
          {
            name: 'smart_chip',
            shape: 'box',
            size: [w * 0.28, h * 0.16, thick * 1.15],
            position: [-w * 0.22, h * 0.52, thick * 0.2],
            color: '#ecc94b',
            texturePreset: 'metal_light_brushed',
            roughness: 0.3,
            metalness: 0.8
          },
          {
            name: 'photo_placeholder',
            shape: 'box',
            size: [w * 0.32, h * 0.25, thick * 1.1],
            position: [w * 0.20, h * 0.48, thick * 0.15],
            color: '#2d3748',
            roughness: 0.9
          },
          {
            name: 'magnetic_stripe',
            shape: 'box',
            size: [w * 0.98, h * 0.18, thick * 1.05],
            position: [0, h * 0.70, -thick * 0.1],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9,
            metalness: 0.3
          },
          {
            name: 'lanyard_slot',
            shape: 'box',
            size: [w * 0.24, 0.03, thick * 1.3],
            position: [0, h * 0.93, 0],
            color: '#1a202c'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 20. CONSOLE / TERMINAL / WORKSTATION
    // -------------------------------------------------------------
    if (/consola|console|workstation|radar|terminal|panel de control/.test(lower)) {
      const cw = 1.2 * baseDim;
      const ch = 1.0 * baseDim;
      const cd = 0.8 * baseDim;
      return {
        id: 'below_nominal.command.flight_console',
        name: 'Consola de Telemetría CRT',
        category: 'command',
        description: 'Puesto de operaciones con teclado angular y pantallas CRT.',
        units: 'meters',
        dimensions: { width: cw, depth: cd, height: ch },
        palette: 'command_bridge',
        components: [
          {
            name: 'desk_base',
            shape: 'box',
            size: [cw, ch * 0.65, cd * 0.85],
            position: [0, ch * 0.325, 0],
            color: mainColor,
            texturePreset: 'worn_metal',
            roughness: 0.75,
            metalness: 0.3
          },
          {
            name: 'slanted_tray',
            shape: 'box',
            size: [cw * 0.92, 0.06, cd * 0.35],
            position: [0, ch * 0.68, cd * 0.25],
            rotation: [-15, 0, 0],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.85
          },
          {
            name: 'crt_housing',
            shape: 'box',
            size: [cw * 0.85, ch * 0.35, cd * 0.45],
            position: [0, ch * 0.85, -cd * 0.15],
            color: '#2d3748',
            texturePreset: 'beige_plastic_worn',
            roughness: 0.7
          },
          {
            name: 'crt_screen',
            shape: 'box',
            size: [cw * 0.70, ch * 0.26, 0.02],
            position: [0, ch * 0.85, cd * 0.08],
            color: '#319795',
            texturePreset: 'crt_screen_green',
            roughness: 0.2,
            metalness: 0.1
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 21. TABLE / MESA / ESCRITORIO
    // -------------------------------------------------------------
    if (/mesa|table|desk|mesada/.test(lower)) {
      const tw = 1.4 * baseDim;
      const td = 0.8 * baseDim;
      const th = 0.75 * baseDim;
      const topThick = 0.06;
      const legR = 0.035;
      const legH = th - topThick;
      return {
        id: 'below_nominal.furniture.table',
        name: 'Mesa de Trabajo Modular',
        category: 'furniture',
        description: 'Mesa de operaciones con tablero reforzado y cuatro patas tubulares.',
        units: 'meters',
        dimensions: { width: tw, depth: td, height: th },
        palette: 'standard',
        components: [
          {
            name: 'tabletop',
            shape: 'box',
            size: [tw, topThick, td],
            position: [0, th - topThick * 0.5, 0],
            color: mainColor,
            roughness: 0.65,
            metalness: 0.2
          },
          {
            name: 'leg_fl',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [-tw * 0.42, legH * 0.5, -td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          },
          {
            name: 'leg_fr',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [tw * 0.42, legH * 0.5, -td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          },
          {
            name: 'leg_bl',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [-tw * 0.42, legH * 0.5, td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          },
          {
            name: 'leg_br',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [tw * 0.42, legH * 0.5, td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 22. DYNAMIC PROCEDURAL SYNTHESIZER (For Any Unlisted Prompt)
    // Generates a genuinely custom, multi-tier composite asset based on
    // word semantics, attributes, and shapes extracted from the prompt.
    // -------------------------------------------------------------
    const components: ComponentDef[] = [];
    const words = lower.split(/\s+/);
    const hash = words.reduce((acc, w) => acc + w.charCodeAt(0), 0);

    // Dynamic dimensions derived from prompt words
    const pW = (0.8 + ((hash * 7) % 50) / 100) * baseDim;
    const pH = (0.7 + ((hash * 13) % 60) / 100) * baseDim;
    const pD = (0.8 + ((hash * 19) % 50) / 100) * baseDim;

    // 1. Foundation Base Plinth
    components.push({
      name: 'pedestal_plinth',
      shape: 'box',
      size: [pW * 1.1, 0.08, pD * 1.1],
      position: [0, 0.04, 0],
      color: '#1a202c',
      roughness: 0.8,
      metalness: 0.5
    });

    // 2. Primary Body Structure
    const hasCylinderShape = /cilindr|tub|redond|circular/.test(lower);
    const hasWedgeShape = /cuñ|rampa|triangul|inclinad/.test(lower);

    if (hasCylinderShape) {
      components.push({
        name: 'primary_core',
        shape: 'cylinder',
        size: [pW * 0.45, pW * 0.45, pH * 0.75, 10],
        position: [0, 0.08 + pH * 0.375, 0],
        color: mainColor,
        roughness: 0.6,
        metalness: 0.3
      });
    } else if (hasWedgeShape) {
      components.push({
        name: 'primary_core',
        shape: 'wedge',
        size: [pW, pH * 0.75, pD],
        position: [0, 0.08 + pH * 0.375, 0],
        color: mainColor,
        roughness: 0.6,
        metalness: 0.3
      });
    } else {
      components.push({
        name: 'primary_core',
        shape: 'box',
        size: [pW, pH * 0.75, pD],
        position: [0, 0.08 + pH * 0.375, 0],
        color: mainColor,
        roughness: 0.6,
        metalness: 0.3
      });
    }

    // 3. Technical Upper Trim / Crown
    components.push({
      name: 'upper_trim',
      shape: 'box',
      size: [pW * 0.85, 0.06, pD * 0.85],
      position: [0, 0.08 + pH * 0.75 + 0.03, 0],
      color: '#2d3748',
      metalness: 0.7
    });

    // 4. Feature Enhancements based on words in prompt
    if (/rueda|ruedas|wheel/.test(lower)) {
      // User asked for wheels!
      const wr = 0.22 * baseDim;
      components.push(
        { name: 'dyn_wheel_fl', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [-pW * 0.55, wr, pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' },
        { name: 'dyn_wheel_fr', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [pW * 0.55, wr, pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' },
        { name: 'dyn_wheel_rl', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [-pW * 0.55, wr, -pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' },
        { name: 'dyn_wheel_rr', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [pW * 0.55, wr, -pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' }
      );
    }

    if (/ala|alas|aleron|wing/.test(lower)) {
      components.push(
        { name: 'dyn_wing_l', shape: 'wedge', size: [pW * 0.8, 0.06, pD * 0.6], position: [-pW * 0.8, pH * 0.5, 0], color: mainColor },
        { name: 'dyn_wing_r', shape: 'wedge', size: [pW * 0.8, 0.06, pD * 0.6], position: [pW * 0.8, pH * 0.5, 0], color: mainColor }
      );
    }

    if (/pantalla|display|monitor|screen/.test(lower)) {
      components.push({
        name: 'dyn_display',
        shape: 'box',
        size: [pW * 0.65, pH * 0.35, 0.02],
        position: [0, pH * 0.5, pD * 0.51],
        color: '#319795',
        roughness: 0.2
      });
    }

    if (/luz|led|faro|brillo|emisor/.test(lower)) {
      components.push(
        { name: 'dyn_light_1', shape: 'box', size: [0.12, 0.08, 0.02], position: [-pW * 0.3, pH * 0.7, pD * 0.51], color: '#ecc94b' },
        { name: 'dyn_light_2', shape: 'box', size: [0.12, 0.08, 0.02], position: [pW * 0.3, pH * 0.7, pD * 0.51], color: '#ecc94b' }
      );
    }

    if (/antena|sensor|mástil/.test(lower)) {
      components.push({
        name: 'dyn_antenna',
        shape: 'cylinder',
        size: [0.02, 0.02, pH * 0.4, 4],
        position: [pW * 0.3, 0.08 + pH * 0.75 + pH * 0.2, 0],
        color: '#cbd5e0',
        metalness: 0.8
      });
    }

    // Default decorative technical detail if no extra features triggered
    if (components.length <= 3) {
      components.push({
        name: 'front_instrument_panel',
        shape: 'box',
        size: [pW * 0.7, pH * 0.25, 0.025],
        position: [0, pH * 0.45, pD * 0.51],
        color: '#2d3748',
        roughness: 0.8
      });
      components.push({
        name: 'status_indicator',
        shape: 'box',
        size: [pW * 0.2, 0.04, 0.03],
        position: [0, pH * 0.45, pD * 0.52],
        color: '#319795',
        roughness: 0.2
      });
    }

    const cleanTitle = prompt
      .replace(/^(un|una|el|la|los|las|de|con|para)\s+/gi, '')
      .trim();
    const titleCapitalized = cleanTitle.charAt(0).toUpperCase() + cleanTitle.slice(1);

    return {
      id: `below_nominal.custom.${cleanTitle.toLowerCase().replace(/[^a-z0-9]/g, '_').substring(0, 32)}`,
      name: `${titleCapitalized} Procedural`,
      category: 'furniture',
      description: `Modelo procedural sintetizado para '${prompt}'.`,
      units: 'meters',
      dimensions: { width: pW * 1.15, depth: pD * 1.15, height: pH * 1.1 },
      palette: 'industrial_hazard',
      components
    };
  }
}
