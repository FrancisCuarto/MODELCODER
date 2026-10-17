import * as THREE from 'three';
import type { ModelSpec, ComponentDef, GeometricStats } from './types.ts';
import { TextureLibrary } from './texture-library.ts';

export class ProceduralEngine {
  /**
   * Translates a ModelSpec into a real Three.js Group with proper transforms,
   * vertex colors, flat-shaded materials, and PSX low-poly geometry.
   */
  public static buildModelFromSpec(spec: ModelSpec): { group: THREE.Group; stats: GeometricStats } {
    const group = new THREE.Group();
    group.name = spec.id || 'procedural_root';

    if (!spec.components || spec.components.length === 0) {
      throw new Error(`La especificación del modelo '${spec.name || 'Sin nombre'}' no contiene componentes geométricos.`);
    }

    for (let i = 0; i < spec.components.length; i++) {
      const comp = spec.components[i];
      const mesh = this.createComponentMesh(comp);
      mesh.userData = { componentIndex: i, componentDef: comp };
      if (comp.visible === false) {
        mesh.visible = false;
      }
      group.add(mesh);
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
            this.adjustBoxUVs(geom, w, h, d, comp.uvScale);
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
          this.adjustCylinderUVs(geom, (rt + rb) * 0.5, h, comp.uvScale);
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
        if (comp.uvScale) {
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
        geom = this.createWedgeGeometry(w, h, d, comp.uvScale);
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

    // Material and vertex color resolution
    const baseColor = this.resolveColor(comp.color);
    let mat: THREE.MeshStandardMaterial;

    if (comp.texturePreset) {
      // Procedural surface texture from unified TextureLibrary
      mat = TextureLibrary.getMaterial(comp, baseColor);
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

    // Optional text label / decal
    if (comp.label) {
      const labelBadge = this.createLabelBadge(comp.label, comp.labelColor || '#ffffff');
      labelBadge.position.set(0, 0, (s[2] ? s[2] * 0.5 : 0.5) + 0.005);
      mesh.add(labelBadge);
    }

    return mesh;
  }

  /**
   * Creates a triangular prism wedge geometry with explicit unstretched UV coordinates.
   */
  private static createWedgeGeometry(w: number, h: number, d: number, uvScale?: [number, number]): THREE.BufferGeometry {
    const hw = w * 0.5;
    const hh = h * 0.5;
    const hd = d * 0.5;

    const su = uvScale?.[0] ?? 1.0;
    const sv = uvScale?.[1] ?? 1.0;
    const hyp = Math.sqrt(w * w + h * h);

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
      w * su, 0,
      0, h * sv,

      // Back triangle
      w * su, 0,
      0, 0,
      0, h * sv,

      // Bottom quad
      0, 0,
      w * su, 0,
      w * su, d * sv,
      0, 0,
      w * su, d * sv,
      0, d * sv,

      // Back vertical quad
      0, 0,
      d * su, 0,
      d * su, h * sv,
      0, 0,
      d * su, h * sv,
      0, h * sv,

      // Sloped quad
      0, 0,
      0, d * sv,
      hyp * su, d * sv,
      0, 0,
      hyp * su, d * sv,
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
