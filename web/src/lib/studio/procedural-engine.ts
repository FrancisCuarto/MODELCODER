import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { Evaluator, Brush, SUBTRACTION, ADDITION, INTERSECTION } from 'three-bvh-csg';
import type { BooleanOperationType } from './types.ts';
import type { ModelSpec, ComponentDef, GeometricStats, ShapePrimitive, PivotPresetType } from './types.ts';
import { TextureLibrary } from './texture-library.ts';

export class ProceduralEngine {
  private static geometryRegistry = new Map<string, THREE.BufferGeometry>();
  private static materialRegistry = new Map<string, THREE.Material>();

  public static registerGeometry(id: string, geom: THREE.BufferGeometry): void {
    this.geometryRegistry.set(id, geom);
  }

  public static getRegisteredGeometry(id: string): THREE.BufferGeometry | undefined {
    return this.geometryRegistry.get(id);
  }

  public static registerMaterial(id: string, mat: THREE.Material): void {
    this.materialRegistry.set(id, mat);
  }

  public static getRegisteredMaterial(id: string): THREE.Material | undefined {
    return this.materialRegistry.get(id);
  }

  public static clearRegistries(): void {
    this.geometryRegistry.clear();
    this.materialRegistry.clear();
  }

  /**
   * Translates a ModelSpec into a real Three.js Group with proper transforms,
   * vertex colors, flat-shaded materials, and PSX low-poly geometry.
   */
  /**
   * Checks whether setting potentialParentName as parent of childName would create a cyclic dependency.
   */
  public static wouldCreateCycle(
    components: ComponentDef[],
    childName: string,
    potentialParentName: string | undefined
  ): boolean {
    if (!potentialParentName || potentialParentName === '') return false;
    if (childName === potentialParentName) return true;

    let current: string | undefined = potentialParentName;
    const visited = new Set<string>();

    while (current) {
      if (current === childName) return true;
      if (visited.has(current)) return true;
      visited.add(current);
      const parentComp = components.find((c) => c.name === current);
      current = parentComp?.parentId;
    }

    return false;
  }

  /**
   * Reparents a component to a new parent (or to root if newParentName is undefined)
   * while recalculating position, rotation, and scale so that its world-space transform
   * is 100% preserved. The 3D piece does NOT move or shift in the scene.
   */
  public static reparentComponentPreservingWorldTransform(
    components: ComponentDef[],
    childName: string,
    newParentName: string | undefined
  ): boolean {
    const childComp = components.find((c) => c.name === childName);
    if (!childComp) return false;

    const currentParent = childComp.parentId || undefined;
    const targetParent = newParentName && newParentName.trim() !== '' ? newParentName.trim() : undefined;
    if (currentParent === targetParent) return true;

    // Cycle check
    if (targetParent && this.wouldCreateCycle(components, childName, targetParent)) {
      return false;
    }

    // Build the existing hierarchy to capture the exact current world matrices
    const dummySpec: ModelSpec = {
      id: 'temp_reparent',
      name: 'Temp',
      category: 'fixtures',
      description: 'Temp',
      units: 'meters',
      dimensions: { width: 1, depth: 1, height: 1 },
      palette: 'industrial_hazard',
      components
    };

    let group: THREE.Group | null = null;
    try {
      const built = this.buildModelFromSpec(dummySpec);
      group = built.group;
      group.updateMatrixWorld(true);

      let childMesh: THREE.Object3D | null = null;
      let targetParentMesh: THREE.Object3D | null = null;

      group.traverse((obj) => {
        if (obj.name === childName) childMesh = obj;
        if (targetParent && obj.name === targetParent) targetParentMesh = obj;
      });

      if (!childMesh) return false;
      if (targetParent && !targetParentMesh) return false;

      const childWorldMatrix = (childMesh as THREE.Object3D).matrixWorld.clone();

      let newLocalMatrix: THREE.Matrix4;
      if (targetParentMesh) {
        // Local matrix relative to the new parent: inv(newParentWorld) * childWorld
        const invParentWorld = (targetParentMesh as THREE.Object3D).matrixWorld.clone().invert();
        newLocalMatrix = new THREE.Matrix4().multiplyMatrices(invParentWorld, childWorldMatrix);
      } else {
        // Target is root (unparenting): world matrix becomes the new local matrix
        newLocalMatrix = childWorldMatrix;
      }

      const newPos = new THREE.Vector3();
      const newQuat = new THREE.Quaternion();
      const newScale = new THREE.Vector3();
      newLocalMatrix.decompose(newPos, newQuat, newScale);

      const newEuler = new THREE.Euler().setFromQuaternion(newQuat, 'XYZ');
      const rotDeg: [number, number, number] = [
        parseFloat(THREE.MathUtils.radToDeg(newEuler.x).toFixed(1)),
        parseFloat(THREE.MathUtils.radToDeg(newEuler.y).toFixed(1)),
        parseFloat(THREE.MathUtils.radToDeg(newEuler.z).toFixed(1))
      ];

      const posArr: [number, number, number] = [
        parseFloat(newPos.x.toFixed(3)),
        parseFloat(newPos.y.toFixed(3)),
        parseFloat(newPos.z.toFixed(3))
      ];

      const scaleArr: [number, number, number] = [
        parseFloat(newScale.x.toFixed(3)),
        parseFloat(newScale.y.toFixed(3)),
        parseFloat(newScale.z.toFixed(3))
      ];

      if (targetParent) {
        childComp.parentId = targetParent;
      } else {
        delete childComp.parentId;
      }

      childComp.position = posArr;
      childComp.rotation = rotDeg;
      if (childComp.scale || Math.abs(scaleArr[0] - 1) > 0.001 || Math.abs(scaleArr[1] - 1) > 0.001 || Math.abs(scaleArr[2] - 1) > 0.001) {
        childComp.scale = scaleArr;
      }

      return true;
    } finally {
      if (group) {
        this.disposeHierarchy(group);
      }
    }
  }

  /**
   * Calculates the standard pivot offset [ox, oy, oz] in meters for a given shape and dimensions.
   */
  /**
   * Computes the world-space bounding box for a specific component in a ModelSpec hierarchy.
   */
  public static computeComponentWorldBounds(
    spec: ModelSpec,
    compIndex: number
  ): { min: THREE.Vector3; max: THREE.Vector3; size: THREE.Vector3; center: THREE.Vector3 } | null {
    if (compIndex < 0 || compIndex >= spec.components.length) return null;
    const targetComp = spec.components[compIndex];

    let group: THREE.Group | null = null;
    try {
      const built = this.buildModelFromSpec(spec);
      group = built.group;
      group.updateMatrixWorld(true);

      let targetMesh: THREE.Object3D | null = null;
      group.traverse((obj) => {
        if (targetMesh) return;
        if (obj.userData && obj.userData.componentIndex === compIndex) {
          targetMesh = obj;
        } else if (obj.name === targetComp.name) {
          targetMesh = obj;
        }
      });

      if (!targetMesh) return null;

      const box = new THREE.Box3().setFromObject(targetMesh);
      const size = new THREE.Vector3();
      const center = new THREE.Vector3();
      box.getSize(size);
      box.getCenter(center);

      return {
        min: box.min.clone(),
        max: box.max.clone(),
        size,
        center
      };
    } finally {
      if (group) {
        this.disposeHierarchy(group);
      }
    }
  }

  /**
   * Adjusts a component's position so that its lowest point in world coordinates sits exactly on Y = 0.
   * If the component has a parent, the shift is accurately transformed into the parent's local coordinate space.
   */
  public static alignComponentToGround(
    spec: ModelSpec,
    compIndex: number
  ): [number, number, number] | null {
    if (compIndex < 0 || compIndex >= spec.components.length) return null;
    const comp = spec.components[compIndex];

    let group: THREE.Group | null = null;
    try {
      const built = this.buildModelFromSpec(spec);
      group = built.group;
      group.updateMatrixWorld(true);

      let targetMesh: THREE.Object3D | null = null;
      group.traverse((obj) => {
        if (targetMesh) return;
        if (obj.userData && obj.userData.componentIndex === compIndex) {
          targetMesh = obj;
        } else if (obj.name === comp.name) {
          targetMesh = obj;
        }
      });

      if (!targetMesh) return null;

      const box = new THREE.Box3().setFromObject(targetMesh);
      const deltaWorldY = -box.min.y;

      if (targetMesh.parent && targetMesh.parent !== group) {
        const invParent = targetMesh.parent.matrixWorld.clone().invert();
        const localDelta = new THREE.Vector3(0, deltaWorldY, 0).transformDirection(invParent);
        const curPos = comp.position || [0, 0, 0];
        const newPos: [number, number, number] = [
          parseFloat((curPos[0] + localDelta.x).toFixed(3)),
          parseFloat((curPos[1] + localDelta.y).toFixed(3)),
          parseFloat((curPos[2] + localDelta.z).toFixed(3))
        ];
        comp.position = newPos;
        return newPos;
      } else {
        const curPos = comp.position || [0, 0, 0];
        const newPos: [number, number, number] = [
          curPos[0],
          parseFloat((curPos[1] + deltaWorldY).toFixed(3)),
          curPos[2]
        ];
        comp.position = newPos;
        return newPos;
      }
    } finally {
      if (group) {
        this.disposeHierarchy(group);
      }
    }
  }

  /**
   * Centers a component on the scene origin (X = 0, Z = 0) based on its bounding box center.
   */
  public static centerComponentOnOrigin(
    spec: ModelSpec,
    compIndex: number,
    axes: 'xz' | 'x' | 'z' = 'xz'
  ): [number, number, number] | null {
    if (compIndex < 0 || compIndex >= spec.components.length) return null;
    const comp = spec.components[compIndex];

    let group: THREE.Group | null = null;
    try {
      const built = this.buildModelFromSpec(spec);
      group = built.group;
      group.updateMatrixWorld(true);

      let targetMesh: THREE.Object3D | null = null;
      group.traverse((obj) => {
        if (targetMesh) return;
        if (obj.userData && obj.userData.componentIndex === compIndex) {
          targetMesh = obj;
        } else if (obj.name === comp.name) {
          targetMesh = obj;
        }
      });

      if (!targetMesh) return null;

      const box = new THREE.Box3().setFromObject(targetMesh);
      const center = new THREE.Vector3();
      box.getCenter(center);

      const deltaWorld = new THREE.Vector3(
        (axes === 'xz' || axes === 'x') ? -center.x : 0,
        0,
        (axes === 'xz' || axes === 'z') ? -center.z : 0
      );

      if (targetMesh.parent && targetMesh.parent !== group) {
        const invParent = targetMesh.parent.matrixWorld.clone().invert();
        const localDelta = deltaWorld.transformDirection(invParent);
        const curPos = comp.position || [0, 0, 0];
        const newPos: [number, number, number] = [
          parseFloat((curPos[0] + localDelta.x).toFixed(3)),
          parseFloat((curPos[1] + localDelta.y).toFixed(3)),
          parseFloat((curPos[2] + localDelta.z).toFixed(3))
        ];
        comp.position = newPos;
        return newPos;
      } else {
        const curPos = comp.position || [0, 0, 0];
        const newPos: [number, number, number] = [
          parseFloat((curPos[0] + deltaWorld.x).toFixed(3)),
          curPos[1],
          parseFloat((curPos[2] + deltaWorld.z).toFixed(3))
        ];
        comp.position = newPos;
        return newPos;
      }
    } finally {
      if (group) {
        this.disposeHierarchy(group);
      }
    }
  }

  /**
   * Snaps a child component flush against one of its parent's 6 bounding faces (+X, -X, +Y, -Y, +Z, -Z).
   */
  public static alignComponentToParentFace(
    spec: ModelSpec,
    compIndex: number,
    face: '+x' | '-x' | '+y' | '-y' | '+z' | '-z'
  ): [number, number, number] | null {
    if (compIndex < 0 || compIndex >= spec.components.length) return null;
    const comp = spec.components[compIndex];
    if (!comp.parentId) return null;

    let group: THREE.Group | null = null;
    try {
      const built = this.buildModelFromSpec(spec);
      group = built.group;
      group.updateMatrixWorld(true);

      let targetMesh: THREE.Object3D | null = null;
      let parentMesh: THREE.Object3D | null = null;

      group.traverse((obj) => {
        if (obj.userData && obj.userData.componentIndex === compIndex) {
          targetMesh = obj;
        } else if (obj.name === comp.name) {
          targetMesh = obj;
        }
        if (obj.name === comp.parentId) {
          parentMesh = obj;
        }
      });

      if (!targetMesh || !parentMesh) return null;

      const parentBox = new THREE.Box3();
      parentMesh.traverse((child) => {
        if (child === targetMesh || targetMesh.children.includes(child)) return;
        if ((child as THREE.Mesh).isMesh && (child as THREE.Mesh).geometry) {
          const geom = (child as THREE.Mesh).geometry;
          if (!geom.boundingBox) geom.computeBoundingBox();
          if (geom.boundingBox) {
            const m = new THREE.Matrix4();
            let curr: THREE.Object3D | null = child;
            while (curr && curr !== parentMesh) {
              m.premultiply(curr.matrix);
              curr = curr.parent;
            }
            parentBox.union(geom.boundingBox.clone().applyMatrix4(m));
          }
        }
      });

      if (parentBox.isEmpty()) {
        const parentComp = spec.components.find((c) => c.name === comp.parentId);
        const ps = parentComp?.size || [1, 1, 1];
        parentBox.set(
          new THREE.Vector3(-ps[0] / 2, -ps[1] / 2, -ps[2] / 2),
          new THREE.Vector3(ps[0] / 2, ps[1] / 2, ps[2] / 2)
        );
      }

      targetMesh.updateMatrix();
      const childBox = new THREE.Box3();
      targetMesh.traverse((child) => {
        if ((child as THREE.Mesh).isMesh && (child as THREE.Mesh).geometry) {
          const geom = (child as THREE.Mesh).geometry;
          if (!geom.boundingBox) geom.computeBoundingBox();
          if (geom.boundingBox) {
            const m = new THREE.Matrix4();
            let curr: THREE.Object3D | null = child;
            while (curr && curr !== parentMesh) {
              m.premultiply(curr.matrix);
              curr = curr.parent;
            }
            childBox.union(geom.boundingBox.clone().applyMatrix4(m));
          }
        }
      });

      let deltaX = 0;
      let deltaY = 0;
      let deltaZ = 0;

      switch (face) {
        case '+y':
          deltaY = parentBox.max.y - childBox.min.y;
          break;
        case '-y':
          deltaY = parentBox.min.y - childBox.max.y;
          break;
        case '+x':
          deltaX = parentBox.max.x - childBox.min.x;
          break;
        case '-x':
          deltaX = parentBox.min.x - childBox.max.x;
          break;
        case '+z':
          deltaZ = parentBox.max.z - childBox.min.z;
          break;
        case '-z':
          deltaZ = parentBox.min.z - childBox.max.z;
          break;
      }

      const curPos = comp.position || [0, 0, 0];
      const newPos: [number, number, number] = [
        parseFloat((curPos[0] + deltaX).toFixed(3)),
        parseFloat((curPos[1] + deltaY).toFixed(3)),
        parseFloat((curPos[2] + deltaZ).toFixed(3))
      ];
      comp.position = newPos;
      return newPos;
    } finally {
      if (group) {
        this.disposeHierarchy(group);
      }
    }
  }

  public static computePresetPivot(
    preset: PivotPresetType,
    shape: ShapePrimitive,
    size?: number[]
  ): [number, number, number] {
    const s = size || [1, 1, 1];
    let w = 1, h = 1, d = 1;
    switch (shape) {
      case 'box':
      case 'wedge':
      case 'chamfer_box':
        w = s[0] ?? 1;
        h = s[1] ?? 1;
        d = s[2] ?? 1;
        break;
      case 'cylinder':
      case 'pipe':
      case 'prism':
        w = (s[0] ?? 0.5) * 2;
        h = s[2] ?? 1;
        d = (s[1] ?? (s[0] ?? 0.5)) * 2;
        break;
      case 'sphere':
        w = (s[0] ?? 0.5) * 2;
        h = w;
        d = w;
        break;
      case 'cone':
      case 'pyramid':
        w = (s[0] ?? 0.5) * 2;
        h = s[1] ?? 1;
        d = w;
        break;
      case 'capsule':
        w = (s[0] ?? 0.25) * 2;
        h = (s[1] ?? 0.5) + (s[0] ?? 0.25) * 2;
        d = w;
        break;
      case 'torus':
        w = ((s[0] ?? 0.5) + (s[1] ?? 0.15)) * 2;
        h = (s[1] ?? 0.15) * 2;
        d = w;
        break;
      case 'plane':
        w = s[0] ?? 1;
        h = s[1] ?? 1;
        d = 0.01;
        break;
      case 'mesh': {
        const cachedGeom = (comp as any)?.meshId ? this.getRegisteredGeometry((comp as any).meshId) : null;
        if (cachedGeom) {
          if (!cachedGeom.boundingBox) cachedGeom.computeBoundingBox();
          if (cachedGeom.boundingBox) {
            w = cachedGeom.boundingBox.max.x - cachedGeom.boundingBox.min.x;
            h = cachedGeom.boundingBox.max.y - cachedGeom.boundingBox.min.y;
            d = cachedGeom.boundingBox.max.z - cachedGeom.boundingBox.min.z;
            break;
          }
        }
        w = s[0] ?? 1;
        h = s[1] ?? 1;
        d = s[2] ?? 1;
        break;
      }
      default:
        w = s[0] ?? 1;
        h = s[1] ?? 1;
        d = s[2] ?? 1;
    }

    switch (preset) {
      case 'bottom':
        return [0, -h * 0.5, 0];
      case 'top':
        return [0, h * 0.5, 0];
      case 'left':
        return [-w * 0.5, 0, 0];
      case 'right':
        return [w * 0.5, 0, 0];
      case 'back':
        return [0, 0, -d * 0.5];
      case 'front':
        return [0, 0, d * 0.5];
      case 'center':
      default:
        return [0, 0, 0];
    }
  }

  /**
   * Creates a mirrored duplicate of a component across a given axis ('x' | 'y' | 'z').
   */
  public static createMirroredComponent(
    comp: ComponentDef,
    axis: 'x' | 'y' | 'z' = 'x',
    newName?: string
  ): ComponentDef {
    const copy: ComponentDef = JSON.parse(JSON.stringify(comp));
    const generatedName = newName || `${comp.name}_mirror_${axis}`;
    copy.name = generatedName;

    // 1. Invert position on axis
    if (!copy.position) copy.position = [0, 0, 0];
    const axisIdx = axis === 'x' ? 0 : axis === 'y' ? 1 : 2;
    copy.position[axisIdx] = -copy.position[axisIdx];

    // 2. Invert complementary rotations for symmetric reflection
    if (!copy.rotation) copy.rotation = [0, 0, 0];
    if (axis === 'x') {
      copy.rotation[1] = -copy.rotation[1];
      copy.rotation[2] = -copy.rotation[2];
    } else if (axis === 'y') {
      copy.rotation[0] = -copy.rotation[0];
      copy.rotation[2] = -copy.rotation[2];
    } else if (axis === 'z') {
      copy.rotation[0] = -copy.rotation[0];
      copy.rotation[1] = -copy.rotation[1];
    }

    // 3. Invert pivot on axis
    if (copy.pivot) {
      copy.pivot[axisIdx] = -copy.pivot[axisIdx];
    }

    return copy;
  }

  public static buildModelFromSpec(spec: ModelSpec): { group: THREE.Group; stats: GeometricStats } {
    const group = new THREE.Group();
    group.name = spec.id || 'procedural_root';

    if (!spec.components || spec.components.length === 0) {
      throw new Error(`La especificación del modelo '${spec.name || 'Sin nombre'}' no contiene componentes geométricos.`);
    }

    const meshMap = new Map<string, THREE.Object3D>();
    const meshes: THREE.Object3D[] = [];

    for (let i = 0; i < spec.components.length; i++) {
      const comp = spec.components[i];
      const mesh = this.createComponentMesh(comp);
      mesh.name = comp.name;
      mesh.userData = { componentIndex: i, componentDef: comp };
      if (comp.visible === false) {
        mesh.visible = false;
      }
      meshMap.set(comp.name, mesh);
      meshes.push(mesh);
    }

    // Attach hierarchy respecting parentId without cyclic loops
    for (let i = 0; i < spec.components.length; i++) {
      const comp = spec.components[i];
      const mesh = meshes[i];
      if (
        comp.parentId &&
        comp.parentId !== comp.name &&
        meshMap.has(comp.parentId) &&
        !this.wouldCreateCycle(spec.components, comp.name, comp.parentId)
      ) {
        const parentMesh = meshMap.get(comp.parentId)!;
        parentMesh.add(mesh);
      } else {
        group.add(mesh);
      }
    }

    // Ensure world matrices are fully computed across hierarchy before CSG operations
    group.updateMatrixWorld(true);

    // Apply non-destructive Boolean (CSG) modifiers
    for (let i = 0; i < spec.components.length; i++) {
      const comp = spec.components[i];
      if (
        comp.boolean &&
        comp.boolean.enabled &&
        comp.boolean.targetComponent &&
        comp.boolean.targetComponent !== comp.name &&
        meshMap.has(comp.name) &&
        meshMap.has(comp.boolean.targetComponent)
      ) {
        const meshA = meshMap.get(comp.name)!;
        const meshB = meshMap.get(comp.boolean.targetComponent)!;

        this.applyBooleanToMesh(meshA, meshB, comp.boolean.operation);

        if (comp.boolean.hideTarget !== false) {
          meshB.visible = false;
          meshB.userData.isBooleanCutter = true;
          meshB.userData.cutterBaseComp = comp.name;
        }
      }
    }

    // Measure real geometry statistics
    const stats = this.computeGroupStats(group);

    return { group, stats };
  }

  /**
   * Constructs an individual Three.js mesh for a given component definition.
   */
  public static createComponentMesh(comp: ComponentDef): THREE.Object3D {
    const shape = comp.shape || 'box';
    const s = comp.size || [1, 1, 1];
    const sx = Math.max(0.01, Math.abs(comp.scale?.[0] ?? 1.0));
    const sy = Math.max(0.01, Math.abs(comp.scale?.[1] ?? 1.0));
    const sz = Math.max(0.01, Math.abs(comp.scale?.[2] ?? 1.0));
    let geom: THREE.BufferGeometry;

    switch (shape) {
      case 'box': {
        const w = Math.max(0.01, s[0] ?? 1.0);
        const h = Math.max(0.01, s[1] ?? 1.0);
        const d = Math.max(0.01, s[2] ?? 1.0);
        geom = new THREE.BoxGeometry(w, h, d);
        if (comp.texturePreset) {
          const presetName = TextureLibrary.resolvePresetName(comp.texturePreset);
          const profile = presetName ? TextureLibrary.PROFILES[presetName] : null;
          if (!profile?.isDecal) {
            this.adjustBoxUVs(geom, w * sx, h * sy, d * sz, comp.uvScale);
          } else if (comp.uvScale) {
            this.applyUVScale(geom, comp.uvScale);
          }
        }
        break;
      }
      case 'cylinder': {
        const rt = Math.max(0.005, s[0] ?? 0.5);
        const rb = Math.max(0.005, s[1] ?? rt);
        const h = Math.max(0.01, s[2] ?? 1.0);
        const segs = Math.max(4, Math.min(32, Math.round(s[3] ?? 8)));
        geom = new THREE.CylinderGeometry(rt, rb, h, segs);
        if (comp.texturePreset) {
          const avgScaleR = (sx + sz) * 0.5;
          this.adjustCylinderUVs(geom, (rt + rb) * 0.5 * avgScaleR, h * sy, comp.uvScale);
        }
        break;
      }
      case 'sphere': {
        const r = Math.max(0.01, s[0] ?? 0.5);
        const wsegs = Math.max(4, Math.min(32, Math.round(s[1] ?? 8)));
        const hsegs = Math.max(3, Math.min(24, Math.round(s[2] ?? 6)));
        geom = new THREE.SphereGeometry(r, wsegs, hsegs);
        if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'plane': {
        const w = Math.max(0.01, s[0] ?? 1.0);
        const h = Math.max(0.01, s[1] ?? 1.0);
        geom = new THREE.PlaneGeometry(w, h);
        if (comp.texturePreset) {
          const presetName = TextureLibrary.resolvePresetName(comp.texturePreset);
          const profile = presetName ? TextureLibrary.PROFILES[presetName] : null;
          if (!profile?.isDecal) {
            const su = comp.uvScale?.[0] ?? 1.0;
            const sv = comp.uvScale?.[1] ?? 1.0;
            this.applyUVScale(geom, [w * sx * su, h * sy * sv]);
          } else if (comp.uvScale) {
            this.applyUVScale(geom, comp.uvScale);
          }
        } else if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'cone': {
        const r = Math.max(0.01, s[0] ?? 0.5);
        const h = Math.max(0.01, s[1] ?? 1.0);
        const segs = Math.max(4, Math.min(32, Math.round(s[2] ?? 8)));
        geom = new THREE.ConeGeometry(r, h, segs);
        if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'torus': {
        const r = Math.max(0.02, s[0] ?? 0.5);
        const tube = Math.max(0.005, s[1] ?? 0.15);
        const radSegs = Math.max(4, Math.min(24, Math.round(s[2] ?? 6)));
        const tubSegs = Math.max(6, Math.min(32, Math.round(s[3] ?? 10)));
        geom = new THREE.TorusGeometry(r, tube, radSegs, tubSegs);
        if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'capsule': {
        const r = Math.max(0.01, s[0] ?? 0.25);
        const len = Math.max(0.01, s[1] ?? 0.5);
        const capSegs = Math.max(2, Math.min(16, Math.round(s[2] ?? 4)));
        const radSegs = Math.max(4, Math.min(24, Math.round(s[3] ?? 8)));
        geom = new THREE.CapsuleGeometry(r, len, capSegs, radSegs);
        if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'wedge': {
        // Triangular prism wedge (PSX industrial wedge)
        const w = Math.max(0.01, s[0] ?? 1.0);
        const h = Math.max(0.01, s[1] ?? 1.0);
        const d = Math.max(0.01, s[2] ?? 1.0);
        geom = this.createWedgeGeometry(w, h, d, comp.uvScale, [sx, sy, sz]);
        break;
      }
      case 'chamfer_box': {
        const w = Math.max(0.01, s[0] ?? 1.0);
        const h = Math.max(0.01, s[1] ?? 1.0);
        const d = Math.max(0.01, s[2] ?? 1.0);
        const maxR = Math.min(w, h, d) * 0.49;
        const r = Math.max(0.001, Math.min(maxR, s[3] ?? 0.05));
        const segs = Math.max(1, Math.min(8, Math.round(s[4] ?? 2)));
        geom = new RoundedBoxGeometry(w, h, d, segs, r);
        if (comp.texturePreset) {
          this.adjustBoxUVs(geom, w * sx, h * sy, d * sz, comp.uvScale);
        } else if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'pipe': {
        const rOuter = Math.max(0.01, s[0] ?? 0.5);
        const rInner = Math.max(0.005, Math.min(rOuter - 0.005, s[1] ?? (rOuter * 0.7)));
        const h = Math.max(0.01, s[2] ?? 1.0);
        const segs = Math.max(4, Math.min(32, Math.round(s[3] ?? 12)));
        geom = this.createPipeGeometry(rOuter, rInner, h, segs, comp.uvScale);
        break;
      }
      case 'prism': {
        const r = Math.max(0.01, s[0] ?? 0.5);
        const h = Math.max(0.01, s[1] ?? 1.0);
        const sides = Math.max(3, Math.min(16, Math.round(s[2] ?? 6)));
        geom = new THREE.CylinderGeometry(r, r, h, sides);
        if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'pyramid': {
        const r = Math.max(0.01, s[0] ?? 0.5);
        const h = Math.max(0.01, s[1] ?? 1.0);
        const sides = Math.max(3, Math.min(16, Math.round(s[2] ?? 4)));
        geom = new THREE.ConeGeometry(r, h, sides);
        if (comp.uvScale) {
          this.applyUVScale(geom, comp.uvScale);
        }
        break;
      }
      case 'mesh': {
        const cachedGeom = comp.meshId ? this.getRegisteredGeometry(comp.meshId) : null;
        if (cachedGeom) {
          geom = cachedGeom.clone();
        } else {
          geom = new THREE.BoxGeometry(1, 1, 1);
        }
        break;
      }
      default: {
        geom = new THREE.BoxGeometry(1, 1, 1);
        break;
      }
    }

    if (comp.uvRotation && Math.abs(comp.uvRotation) > 0.01) {
      this.applyUVRotation(geom, comp.uvRotation);
    }

    // Pivot / Hinge / Articulation Offset
    // If a pivot is specified, translate geometry vertices so the mesh origin (0, 0, 0) is situated at the pivot point
    if (comp.pivot && (comp.pivot[0] !== 0 || comp.pivot[1] !== 0 || comp.pivot[2] !== 0)) {
      geom.translate(-comp.pivot[0], -comp.pivot[1], -comp.pivot[2]);
      geom.computeBoundingBox();
      geom.computeBoundingSphere();
    }

    // Material and vertex color resolution
    const baseColor = this.resolveColor(comp.color);
    let mat: THREE.MeshStandardMaterial;

    if (comp.texturePreset) {
      // Procedural surface texture from unified TextureLibrary
      mat = TextureLibrary.getMaterial(comp, baseColor);
    } else if (comp.shape === 'mesh' && comp.meshId && this.getRegisteredMaterial(comp.meshId)) {
      // Native material preserved from the original catalog GLB model
      const origMat = this.getRegisteredMaterial(comp.meshId) as THREE.MeshStandardMaterial;
      mat = origMat.clone ? (origMat.clone() as THREE.MeshStandardMaterial) : origMat;
      if (comp.color && comp.color !== '#ffffff' && comp.color !== 'casing') {
        mat.color = baseColor;
      }
      if (comp.roughness !== undefined) mat.roughness = comp.roughness;
      if (comp.metalness !== undefined) mat.metalness = comp.metalness;
      if (comp.wireframe !== undefined) mat.wireframe = Boolean(comp.wireframe);
    } else {
      // Legacy untextured / flat-colored component
      this.bakeVertexColors(geom, baseColor);
      mat = new THREE.MeshStandardMaterial({
        color: baseColor,
        roughness: comp.roughness ?? 0.75,
        metalness: comp.metalness ?? 0.25,
        flatShading: true,
        vertexColors: true,
        wireframe: Boolean(comp.wireframe)
      });
    }

    // Material transparency, opacity, depth writing, and double-sided glass rendering
    const isTransp = Boolean(mat.transparent || comp.transparent || (comp.opacity !== undefined && comp.opacity < 1.0));
    if (isTransp) {
      mat.transparent = true;
      mat.opacity = comp.opacity !== undefined ? Math.max(0.0, Math.min(1.0, comp.opacity)) : (mat.opacity < 1.0 ? mat.opacity : 0.8);
      if (mat.opacity < 0.9) {
        mat.depthWrite = false;
        mat.side = THREE.DoubleSide;
      }
    }
    if (comp.wireframe !== undefined) {
      mat.wireframe = Boolean(comp.wireframe);
    }

    const mesh = new THREE.Mesh(geom, mat);
    mesh.name = comp.name || `comp_${shape}`;
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    // Position
    if (comp.position && comp.position.length >= 3) {
      mesh.position.set(comp.position[0], comp.position[1], comp.position[2]);
    }

    // Rotation (Euler degrees to radians)
    if (comp.rotation && comp.rotation.length >= 3) {
      mesh.rotation.set(
        THREE.MathUtils.degToRad(comp.rotation[0]),
        THREE.MathUtils.degToRad(comp.rotation[1]),
        THREE.MathUtils.degToRad(comp.rotation[2])
      );
    }

    // Scale
    if (comp.scale && comp.scale.length >= 3) {
      mesh.scale.set(comp.scale[0], comp.scale[1], comp.scale[2]);
    }

    // Optional text label / decal (respecting pivot offset)
    if (comp.label) {
      const labelBadge = this.createLabelBadge(comp.label, comp.labelColor || '#ffffff');
      const pivX = comp.pivot?.[0] ?? 0;
      const pivY = comp.pivot?.[1] ?? 0;
      const pivZ = comp.pivot?.[2] ?? 0;
      labelBadge.position.set(
        -pivX,
        -pivY,
        (s[2] ? s[2] * 0.5 : 0.5) + 0.005 - pivZ
      );
      mesh.add(labelBadge);
    }

    // Array Modifier (linear or radial instance generation)
    if (comp.array && comp.array.enabled && comp.array.count > 1) {
      const arrayGroup = new THREE.Group();
      arrayGroup.name = comp.name || `comp_${shape}`;

      // Base instance placed at origin relative to arrayGroup
      mesh.position.set(0, 0, 0);
      mesh.rotation.set(0, 0, 0);
      mesh.scale.set(1, 1, 1);
      mesh.name = `${comp.name}_0`;
      arrayGroup.add(mesh);

      const count = Math.max(2, Math.min(64, Math.round(comp.array.count)));
      const type = comp.array.type || 'linear';

      if (type === 'linear') {
        const [dx, dy, dz] = comp.array.offset || [1, 0, 0];
        for (let c = 1; c < count; c++) {
          const copy = mesh.clone();
          copy.name = `${comp.name}_${c}`;
          copy.position.set(dx * c, dy * c, dz * c);
          copy.userData = { isArrayInstance: true, instanceIndex: c };
          arrayGroup.add(copy);
        }
      } else if (type === 'radial') {
        const axis = comp.array.radialAxis || 'y';
        const radius = comp.array.radialRadius ?? 0;
        const totalAngle = (comp.array.radialAngle ?? 360) * (Math.PI / 180);
        const rotateCopies = comp.array.radialRotateCopies !== false;
        const stepAngle = totalAngle / (Math.abs(totalAngle - 2 * Math.PI) < 0.01 ? count : Math.max(1, count - 1));

        for (let c = 1; c < count; c++) {
          const copy = mesh.clone();
          const angle = stepAngle * c;
          copy.name = `${comp.name}_${c}`;
          copy.userData = { isArrayInstance: true, instanceIndex: c };

          if (axis === 'y') {
            if (radius > 0) {
              copy.position.set(Math.sin(angle) * radius, 0, (Math.cos(angle) - 1) * radius);
            }
            if (rotateCopies) {
              copy.rotation.y = angle;
            }
          } else if (axis === 'x') {
            if (radius > 0) {
              copy.position.set(0, Math.sin(angle) * radius, (Math.cos(angle) - 1) * radius);
            }
            if (rotateCopies) {
              copy.rotation.x = angle;
            }
          } else if (axis === 'z') {
            if (radius > 0) {
              copy.position.set(Math.sin(angle) * radius, (Math.cos(angle) - 1) * radius, 0);
            }
            if (rotateCopies) {
              copy.rotation.z = angle;
            }
          }
          arrayGroup.add(copy);
        }
      }

      // Root position, rotation, scale onto the array group
      if (comp.position && comp.position.length >= 3) {
        arrayGroup.position.set(comp.position[0], comp.position[1], comp.position[2]);
      }
      if (comp.rotation && comp.rotation.length >= 3) {
        arrayGroup.rotation.set(
          THREE.MathUtils.degToRad(comp.rotation[0]),
          THREE.MathUtils.degToRad(comp.rotation[1]),
          THREE.MathUtils.degToRad(comp.rotation[2])
        );
      }
      if (comp.scale && comp.scale.length >= 3) {
        arrayGroup.scale.set(comp.scale[0], comp.scale[1], comp.scale[2]);
      }

      return arrayGroup;
    }

    return mesh;
  }

  /**
   * Creates a watertight hollow pipe (cylinder with concentric bore) using ExtrudeGeometry.
   */
  /**
   * Evaluates a Boolean CSG operation (difference, union, intersection) between two meshes.
   * Updates meshA's geometry in its local coordinate space.
   */
  public static applyBooleanToMesh(
    meshA: THREE.Object3D,
    meshB: THREE.Object3D,
    operation: BooleanOperationType = 'difference'
  ): void {
    if (!meshA || !meshB) return;

    meshA.updateWorldMatrix(true, true);
    meshB.updateWorldMatrix(true, true);

    let actualMeshA: THREE.Mesh | null = null;
    let actualMeshB: THREE.Mesh | null = null;

    meshA.traverse((child) => {
      if (!actualMeshA && (child as THREE.Mesh).isMesh && (child as THREE.Mesh).geometry) {
        actualMeshA = child as THREE.Mesh;
      }
    });

    meshB.traverse((child) => {
      if (!actualMeshB && (child as THREE.Mesh).isMesh && (child as THREE.Mesh).geometry) {
        actualMeshB = child as THREE.Mesh;
      }
    });

    if (!actualMeshA || !actualMeshB) return;

    try {
      const invA = (actualMeshA as THREE.Mesh).matrixWorld.clone().invert();
      const relB = new THREE.Matrix4().multiplyMatrices(invA, (actualMeshB as THREE.Mesh).matrixWorld);

      const geomA = (actualMeshA as THREE.Mesh).geometry.clone();
      const geomB = (actualMeshB as THREE.Mesh).geometry.clone();

      if (!geomA.attributes.normal) geomA.computeVertexNormals();
      if (!geomB.attributes.normal) geomB.computeVertexNormals();

      const brushA = new Brush(geomA, (actualMeshA as THREE.Mesh).material);
      const brushB = new Brush(geomB, (actualMeshB as THREE.Mesh).material);

      brushA.position.set(0, 0, 0);
      brushA.quaternion.identity();
      brushA.scale.set(1, 1, 1);
      brushA.updateMatrix();
      brushA.updateMatrixWorld(true);

      brushB.position.set(0, 0, 0);
      brushB.quaternion.identity();
      brushB.scale.set(1, 1, 1);
      relB.decompose(brushB.position, brushB.quaternion, brushB.scale);
      brushB.updateMatrix();
      brushB.updateMatrixWorld(true);

      let opCode = SUBTRACTION;
      if (operation === 'union') opCode = ADDITION;
      else if (operation === 'intersection') opCode = INTERSECTION;

      const evaluator = new Evaluator();
      evaluator.useGroups = false;
      const result = evaluator.evaluate(brushA, brushB, opCode);

      if (result && result.geometry) {
        result.geometry.computeVertexNormals();
        result.geometry.computeBoundingBox();
        result.geometry.computeBoundingSphere();
        (actualMeshA as THREE.Mesh).geometry = result.geometry;
      }
    } catch (err) {
      console.warn('[ProceduralEngine] Error al evaluar operación booleana CSG:', err);
    }
  }

  /**
   * Bakes a Boolean CSG modifier into a permanent custom mesh ('shape: mesh').
   * Registers the resulting geometry and optionally deletes the cutter target component.
   */
  public static bakeBooleanOperation(
    spec: ModelSpec,
    compIndex: number,
    deleteTarget: boolean = true
  ): ModelSpec {
    if (compIndex < 0 || compIndex >= spec.components.length) return spec;
    const copy: ModelSpec = JSON.parse(JSON.stringify(spec));
    const compA = copy.components[compIndex];
    if (!compA || !compA.boolean || !compA.boolean.targetComponent) return spec;

    const targetName = compA.boolean.targetComponent;

    let group: THREE.Group | null = null;
    try {
      const built = this.buildModelFromSpec(copy);
      group = built.group;

      let bakedMesh: THREE.Mesh | null = null;
      group.traverse((obj) => {
        if (!bakedMesh && (obj.userData?.componentIndex === compIndex || obj.name === compA.name)) {
          if ((obj as THREE.Mesh).isMesh && (obj as THREE.Mesh).geometry) {
            bakedMesh = obj as THREE.Mesh;
          } else {
            obj.traverse((child) => {
              if (!bakedMesh && (child as THREE.Mesh).isMesh && (child as THREE.Mesh).geometry) {
                bakedMesh = child as THREE.Mesh;
              }
            });
          }
        }
      });

      if (bakedMesh && (bakedMesh as THREE.Mesh).geometry) {
        const meshId = `baked_csg_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
        this.registerGeometry(meshId, (bakedMesh as THREE.Mesh).geometry.clone());
        compA.shape = 'mesh';
        compA.meshId = meshId;
      }
    } finally {
      if (group) {
        this.disposeHierarchy(group);
      }
    }

    delete compA.boolean;

    if (deleteTarget) {
      copy.components = copy.components.filter((c) => c.name !== targetName);
    }

    return copy;
  }

  public static createPipeGeometry(
    rOuter: number,
    rInner: number,
    height: number,
    segments: number = 12,
    uvScale?: [number, number]
  ): THREE.BufferGeometry {
    const shape = new THREE.Shape();
    shape.absarc(0, 0, rOuter, 0, Math.PI * 2, false);
    const hole = new THREE.Path();
    hole.absarc(0, 0, rInner, 0, Math.PI * 2, true);
    shape.holes.push(hole);

    const geom = new THREE.ExtrudeGeometry(shape, {
      depth: height,
      bevelEnabled: false,
      curveSegments: Math.max(4, segments),
    });
    geom.center();
    geom.rotateX(Math.PI / 2);
    geom.computeVertexNormals();

    if (uvScale) {
      this.applyUVScale(geom, uvScale);
    }
    return geom;
  }

  /**
   * Unrolls/bakes an array modifier into distinct independent ComponentDef pieces in the ModelSpec.
   */
  public static unrollArrayModifier(spec: ModelSpec, componentIndex: number): ModelSpec {
    if (!spec.components || componentIndex < 0 || componentIndex >= spec.components.length) {
      return spec;
    }
    const comp = spec.components[componentIndex];
    if (!comp.array || !comp.array.enabled || comp.array.count <= 1) {
      return spec;
    }

    const count = Math.max(2, Math.min(64, Math.round(comp.array.count)));
    const type = comp.array.type || 'linear';
    const newComponents: ComponentDef[] = [];

    // Base component with array removed
    const baseComp = JSON.parse(JSON.stringify(comp)) as ComponentDef;
    delete baseComp.array;
    newComponents.push(baseComp);

    const baseRot = baseComp.rotation || [0, 0, 0];
    const basePos = baseComp.position || [0, 0, 0];
    const euler = new THREE.Euler(
      THREE.MathUtils.degToRad(baseRot[0]),
      THREE.MathUtils.degToRad(baseRot[1]),
      THREE.MathUtils.degToRad(baseRot[2])
    );

    if (type === 'linear') {
      const [dx, dy, dz] = comp.array.offset || [1, 0, 0];
      for (let c = 1; c < count; c++) {
        const copyComp = JSON.parse(JSON.stringify(baseComp)) as ComponentDef;
        copyComp.name = `${baseComp.name}_${c + 1}`;
        const offsetVec = new THREE.Vector3(dx * c, dy * c, dz * c).applyEuler(euler);
        copyComp.position = [
          basePos[0] + offsetVec.x,
          basePos[1] + offsetVec.y,
          basePos[2] + offsetVec.z
        ];
        newComponents.push(copyComp);
      }
    } else if (type === 'radial') {
      const axis = comp.array.radialAxis || 'y';
      const radius = comp.array.radialRadius ?? 0;
      const totalAngle = (comp.array.radialAngle ?? 360) * (Math.PI / 180);
      const rotateCopies = comp.array.radialRotateCopies !== false;
      const stepAngle = totalAngle / (Math.abs(totalAngle - 2 * Math.PI) < 0.01 ? count : Math.max(1, count - 1));

      for (let c = 1; c < count; c++) {
        const copyComp = JSON.parse(JSON.stringify(baseComp)) as ComponentDef;
        copyComp.name = `${baseComp.name}_${c + 1}`;
        const angle = stepAngle * c;
        const localPos = new THREE.Vector3();

        if (axis === 'y') {
          if (radius > 0) {
            localPos.set(Math.sin(angle) * radius, 0, (Math.cos(angle) - 1) * radius);
          }
          if (rotateCopies) {
            copyComp.rotation = [baseRot[0], baseRot[1] + THREE.MathUtils.radToDeg(angle), baseRot[2]];
          }
        } else if (axis === 'x') {
          if (radius > 0) {
            localPos.set(0, Math.sin(angle) * radius, (Math.cos(angle) - 1) * radius);
          }
          if (rotateCopies) {
            copyComp.rotation = [baseRot[0] + THREE.MathUtils.radToDeg(angle), baseRot[1], baseRot[2]];
          }
        } else if (axis === 'z') {
          if (radius > 0) {
            localPos.set(Math.sin(angle) * radius, (Math.cos(angle) - 1) * radius, 0);
          }
          if (rotateCopies) {
            copyComp.rotation = [baseRot[0], baseRot[1], baseRot[2] + THREE.MathUtils.radToDeg(angle)];
          }
        }

        localPos.applyEuler(euler);
        copyComp.position = [
          basePos[0] + localPos.x,
          basePos[1] + localPos.y,
          basePos[2] + localPos.z
        ];
        newComponents.push(copyComp);
      }
    }

    const updatedComponents = [
      ...spec.components.slice(0, componentIndex),
      ...newComponents,
      ...spec.components.slice(componentIndex + 1)
    ];

    return {
      ...spec,
      components: updatedComponents
    };
  }

  /**
   * Creates a triangular prism wedge geometry with explicit unstretched UV coordinates.
   */
  private static createWedgeGeometry(
    w: number,
    h: number,
    d: number,
    uvScale?: [number, number],
    scale?: [number, number, number]
  ): THREE.BufferGeometry {
    const hw = w * 0.5;
    const hh = h * 0.5;
    const hd = d * 0.5;

    const sx = scale?.[0] ?? 1.0;
    const sy = scale?.[1] ?? 1.0;
    const sz = scale?.[2] ?? 1.0;
    const ew = w * sx;
    const eh = h * sy;
    const ed = d * sz;

    const su = uvScale?.[0] ?? 1.0;
    const sv = uvScale?.[1] ?? 1.0;
    const hyp = Math.sqrt(ew * ew + eh * eh);

    // 24 vertices of a triangular prism
    const positions = new Float32Array([
      // Front triangle
      -hw, -hh,  hd,
       hw, -hh,  hd,
      -hw,  hh,  hd,

      // Back triangle
       hw, -hh, -hd,
      -hw, -hh, -hd,
      -hw,  hh, -hd,

      // Bottom quad (2 tris)
      -hw, -hh, -hd,
       hw, -hh, -hd,
       hw, -hh,  hd,
      -hw, -hh, -hd,
       hw, -hh,  hd,
      -hw, -hh,  hd,

      // Back vertical quad (2 tris)
      -hw, -hh, -hd,
      -hw, -hh,  hd,
      -hw,  hh,  hd,
      -hw, -hh, -hd,
      -hw,  hh,  hd,
      -hw,  hh, -hd,

      // Sloped quad (2 tris)
      -hw,  hh, -hd,
      -hw,  hh,  hd,
       hw, -hh,  hd,
      -hw,  hh, -hd,
       hw, -hh,  hd,
       hw, -hh, -hd,
    ]);

    const uvs = new Float32Array([
      // Front triangle
      0, 0,
      ew * su, 0,
      0, eh * sv,

      // Back triangle
      ew * su, 0,
      0, 0,
      0, eh * sv,

      // Bottom quad
      0, 0,
      ew * su, 0,
      ew * su, ed * sv,
      0, 0,
      ew * su, ed * sv,
      0, ed * sv,

      // Back vertical quad
      0, 0,
      ed * su, 0,
      ed * su, eh * sv,
      0, 0,
      ed * su, eh * sv,
      0, eh * sv,

      // Sloped quad
      0, 0,
      0, ed * sv,
      hyp * su, ed * sv,
      0, 0,
      hyp * su, ed * sv,
      hyp * su, 0,
    ]);

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
    geom.computeVertexNormals();
    return geom;
  }

  /**
   * Bakes RGB vertex colors into the geometry buffer attribute ('color').
   */
  public static bakeVertexColors(geom: THREE.BufferGeometry, color: THREE.Color): void {
    const pos = geom.getAttribute('position');
    if (!pos) return;

    const count = pos.count;
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      // Subtle vertex shade jitter for authentic PSX retro lighting
      const jitter = 0.95 + (i % 7) * 0.015;
      colors[i * 3]     = Math.min(1.0, color.r * jitter);
      colors[i * 3 + 1] = Math.min(1.0, color.g * jitter);
      colors[i * 3 + 2] = Math.min(1.0, color.b * jitter);
    }

    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  }

  /**
   * Parses hex or semantic retro color name to THREE.Color.
   */
  public static resolveColor(colorStr?: string): THREE.Color {
    if (!colorStr) return new THREE.Color(0x718096);

    const paletteMap: Record<string, number> = {
      casing: 0x2d3748,
      metal: 0x4a5568,
      metal_light: 0xa0aec0,
      accent: 0xe53e3e,
      hazard: 0xd69e2e,
      screen: 0x319795,
      glass: 0x63b3ed,
      red: 0xe53e3e,
      blue: 0x3182ce,
      green: 0x38a169,
      yellow: 0xd69e2e,
      orange: 0xdd6b20,
      white: 0xedf2f7,
      dark: 0x1a202c,
      rust: 0x9c4221
    };

    const clean = colorStr.toLowerCase().trim();
    if (paletteMap[clean] !== undefined) {
      return new THREE.Color(paletteMap[clean]);
    }

    try {
      return new THREE.Color(colorStr);
    } catch {
      return new THREE.Color(0x718096);
    }
  }

  /**
   * Creates a canvas-based text badge decal for labeling models.
   */
  private static createLabelBadge(text: string, textColor: string): THREE.Mesh {
    if (typeof document === 'undefined') {
      return new THREE.Mesh();
    }
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.fillStyle = '#111827';
      ctx.fillRect(0, 0, 256, 64);
      ctx.strokeStyle = '#4b5563';
      ctx.lineWidth = 4;
      ctx.strokeRect(2, 2, 252, 60);

      ctx.font = 'bold 24px monospace';
      ctx.fillStyle = textColor;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text.substring(0, 16).toUpperCase(), 128, 32);
    }

    const texture = new THREE.CanvasTexture(canvas);
    texture.magFilter = THREE.NearestFilter;
    texture.minFilter = THREE.NearestFilter;

    const planeGeom = new THREE.PlaneGeometry(0.3, 0.08);
    const planeMat = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
    return new THREE.Mesh(planeGeom, planeMat);
  }

  /**
   * Computes accurate geometric statistics from a Three.js hierarchy.
   */
  public static computeGroupStats(obj: THREE.Object3D): GeometricStats {
    let triangles = 0;
    let vertices = 0;

    obj.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        const geom = mesh.geometry;
        if (geom) {
          const pos = geom.getAttribute('position');
          if (pos) {
            vertices += pos.count;
            if (geom.index) {
              triangles += geom.index.count / 3;
            } else {
              triangles += pos.count / 3;
            }
          }
        }
      }
    });

    const box = new THREE.Box3().setFromObject(obj);
    const size = new THREE.Vector3();
    if (!box.isEmpty()) {
      box.getSize(size);
    }

    return {
      triangles: Math.round(triangles),
      vertices: Math.round(vertices),
      dimensions: {
        x: parseFloat(size.x.toFixed(3)),
        y: parseFloat(size.y.toFixed(3)),
        z: parseFloat(size.z.toFixed(3))
      }
    };
  }

  /**
   * Adjusts UV coordinates on BoxGeometry faces to avoid visible stretching.
   */
  public static adjustBoxUVs(
    geom: THREE.BufferGeometry,
    width: number,
    height: number,
    depth: number,
    uvScale?: [number, number]
  ): void {
    const uvAttr = geom.getAttribute('uv');
    if (!uvAttr) return;

    const uvs = uvAttr.array as Float32Array;
    const su = uvScale?.[0] ?? 1.0;
    const sv = uvScale?.[1] ?? 1.0;

    // 6 faces * 4 vertices = 24 vertices
    // Face 0 (+X, right): depth x height
    // Face 1 (-X, left): depth x height
    // Face 2 (+Y, top): width x depth
    // Face 3 (-Y, bottom): width x depth
    // Face 4 (+Z, front): width x height
    // Face 5 (-Z, back): width x height
    const faceDims: Array<[number, number]> = [
      [depth, height],
      [depth, height],
      [width, depth],
      [width, depth],
      [width, height],
      [width, height]
    ];

    for (let f = 0; f < 6; f++) {
      const [fw, fh] = faceDims[f];
      const scaleU = Math.max(0.01, fw) * su;
      const scaleV = Math.max(0.01, fh) * sv;

      for (let v = 0; v < 4; v++) {
        const idx = (f * 4 + v) * 2;
        uvs[idx] = uvs[idx] * scaleU;
        uvs[idx + 1] = uvs[idx + 1] * scaleV;
      }
    }

    uvAttr.needsUpdate = true;
  }

  /**
   * Adjusts UV coordinates on CylinderGeometry to maintain authentic square texture tiling.
   */
  public static adjustCylinderUVs(
    geom: THREE.BufferGeometry,
    radius: number,
    height: number,
    uvScale?: [number, number]
  ): void {
    const uvAttr = geom.getAttribute('uv');
    if (!uvAttr) return;

    const uvs = uvAttr.array as Float32Array;
    const su = uvScale?.[0] ?? 1.0;
    const sv = uvScale?.[1] ?? 1.0;

    const circumference = 2 * Math.PI * Math.max(0.01, radius);
    const scaleU = circumference * su;
    const scaleV = Math.max(0.01, height) * sv;

    for (let i = 0; i < uvs.length; i += 2) {
      uvs[i] = uvs[i] * scaleU;
      uvs[i + 1] = uvs[i + 1] * scaleV;
    }

    uvAttr.needsUpdate = true;
  }

  /**
   * Scales existing UV attributes uniformly or by axis factor.
   */
  public static applyUVScale(geom: THREE.BufferGeometry, uvScale: [number, number]): void {
    const uvAttr = geom.getAttribute('uv');
    if (!uvAttr) return;

    const uvs = uvAttr.array as Float32Array;
    const su = uvScale[0] ?? 1.0;
    const sv = uvScale[1] ?? 1.0;

    for (let i = 0; i < uvs.length; i += 2) {
      uvs[i] = uvs[i] * su;
      uvs[i + 1] = uvs[i + 1] * sv;
    }

    uvAttr.needsUpdate = true;
  }

  /**
   * Rotates existing UV coordinates by angleDeg degrees around (0.5, 0.5) without duplicating textures.
   */
  public static applyUVRotation(geom: THREE.BufferGeometry, angleDeg: number): void {
    const uvAttr = geom.getAttribute('uv');
    if (!uvAttr) return;

    const uvs = uvAttr.array as Float32Array;
    const rad = THREE.MathUtils.degToRad(angleDeg);
    const cos = Math.cos(rad);
    const sin = Math.sin(rad);

    for (let i = 0; i < uvs.length; i += 2) {
      const u = uvs[i] - 0.5;
      const v = uvs[i + 1] - 0.5;
      uvs[i] = u * cos - v * sin + 0.5;
      uvs[i + 1] = u * sin + v * cos + 0.5;
    }

    uvAttr.needsUpdate = true;
  }

  /**
   * Safely frees and disposes all GPU memory allocated by an Object3D subtree,
   * while keeping reusable texture presets (BaseColor, Normal, Roughness) cached in TextureLibrary.
   */
  public static disposeHierarchy(obj: THREE.Object3D): void {
    obj.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        if (mesh.geometry) {
          mesh.geometry.dispose();
        }
        if (mesh.material) {
          const mats = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
          mats.forEach((m: any) => {
            if (m.map && !TextureLibrary.isPresetTexture(m.map)) {
              m.map.dispose();
            }
            if (m.normalMap && !TextureLibrary.isPresetTexture(m.normalMap)) {
              m.normalMap.dispose();
            }
            if (m.roughnessMap && !TextureLibrary.isPresetTexture(m.roughnessMap)) {
              m.roughnessMap.dispose();
            }
            if (m.emissiveMap && !TextureLibrary.isPresetTexture(m.emissiveMap)) {
              m.emissiveMap.dispose();
            }
            m.dispose();
          });
        }
      }
    });
  }
}
