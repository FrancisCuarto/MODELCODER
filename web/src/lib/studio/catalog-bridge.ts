import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { ProceduralEngine } from './procedural-engine.ts';
import type { ModelSpec, ComponentDef } from './types.ts';
import { AIGenerator } from './ai-generator.ts';
import catalog from '../../data/catalog.json' with { type: 'json' };

export interface CatalogTemplateInfo {
  family: string;
  name: string;
  category: string;
  description: string;
  defaultTriBudget?: string;
  tags?: string[];
  parameterCount: number;
}

export class CatalogBridge {
  /**
   * Retrieves all available catalog templates.
   */
  public static getCatalogTemplates(): CatalogTemplateInfo[] {
    return (catalog as any[]).map((item: any) => ({
      family: item.family,
      name: item.name,
      category: item.category || 'props',
      description: item.description,
      defaultTriBudget: item.export_capabilities?.target_tri_budget || '300-500',
      tags: item.tags || [],
      parameterCount: item.parameters?.length || 0
    }));
  }

  /**
   * Loads the authentic 3D GLB model from the catalog and deconstructs it
   * into genuine editable components in Studio (preserving meshes, positions, rotations, scales and materials).
   */
  public static async loadCatalogModelAsSpec(
    family: string,
    userParams?: Record<string, any>
  ): Promise<ModelSpec> {
    const entry = (catalog as any[]).find((c: any) => c.family === family) || {
      family,
      name: family.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
      category: 'props',
      description: 'Modelo original desglosado para edición modular.'
    };

    // Safe polyfills for GLTFLoader when running in headless Node.js tests
    if (typeof (globalThis as any).self === 'undefined') {
      (globalThis as any).self = globalThis;
    }

    try {
      let arrayBuffer: ArrayBuffer | null = null;
      let modelUrl = entry.model_url || `/models/${family}.glb`;

      // Check if a specific palette variant is requested
      if (userParams?.palette && userParams.palette !== 'industrial_hazard') {
        modelUrl = `/models/${family}_${userParams.palette}.glb`;
      }

      const isBrowser = typeof window !== 'undefined' && typeof window.location !== 'undefined' && Boolean(window.location.origin) && window.location.origin !== 'null';

      if (!isBrowser) {
        // Node.js environment (e.g. running unit tests)
        const fs = await import('node:fs');
        const path = await import('node:path');
        const candidatePaths = [
          path.resolve(`public/models/${family}.glb`),
          path.resolve(`web/public/models/${family}.glb`),
          path.resolve(`../web/public/models/${family}.glb`),
          path.resolve(`public${modelUrl}`),
          path.resolve(`web/public${modelUrl}`)
        ];

        let foundPath: string | null = null;
        for (const p of candidatePaths) {
          if (fs.existsSync(p)) {
            foundPath = p;
            break;
          }
        }

        if (foundPath) {
          const buf = fs.readFileSync(foundPath);
          arrayBuffer = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
        }
      } else {
        // Browser environment
        try {
          const res = await fetch(modelUrl);
          if (res.ok) {
            arrayBuffer = await res.arrayBuffer();
          } else if (modelUrl !== `/models/${family}.glb`) {
            // Fallback to base model if palette model 404s
            modelUrl = `/models/${family}.glb`;
            const baseRes = await fetch(modelUrl);
            if (baseRes.ok) {
              arrayBuffer = await baseRes.arrayBuffer();
            }
          }
        } catch (e) {
          console.warn(`[CatalogBridge] Error fetching ${modelUrl}:`, e);
        }
      }

      if (!arrayBuffer) {
        throw new Error(`No se pudo obtener el archivo GLB para ${family}`);
      }

      const loader = new GLTFLoader();
      const gltf = await loader.parseAsync(arrayBuffer, '');

      const scene = gltf.scene;
      scene.updateMatrixWorld(true);

      const bbox = new THREE.Box3().setFromObject(scene);
      const sizeVec = new THREE.Vector3();
      bbox.getSize(sizeVec);

      const components: ComponentDef[] = [];
      let meshIdx = 0;

      scene.traverse((node: any) => {
        if (node.isMesh && node.geometry) {
          meshIdx++;
          const meshName = node.name && !node.name.startsWith('Mesh') ? node.name : `parte_${meshIdx}`;
          const meshId = `catalog_${family}_${meshName}_${meshIdx}`;

          // Register geometry and material in ProceduralEngine
          ProceduralEngine.registerGeometry(meshId, node.geometry.clone());
          if (node.material) {
            ProceduralEngine.registerMaterial(meshId, node.material.clone ? node.material.clone() : node.material);
          }

          const worldPos = new THREE.Vector3();
          const worldQuat = new THREE.Quaternion();
          const worldScale = new THREE.Vector3();
          node.matrixWorld.decompose(worldPos, worldQuat, worldScale);
          const euler = new THREE.Euler().setFromQuaternion(worldQuat, 'XYZ');

          const comp: ComponentDef = {
            name: meshName,
            shape: 'mesh',
            meshId,
            sourceGlbUrl: modelUrl,
            position: [
              parseFloat(worldPos.x.toFixed(3)),
              parseFloat(worldPos.y.toFixed(3)),
              parseFloat(worldPos.z.toFixed(3))
            ],
            rotation: [
              parseFloat(THREE.MathUtils.radToDeg(euler.x).toFixed(1)),
              parseFloat(THREE.MathUtils.radToDeg(euler.y).toFixed(1)),
              parseFloat(THREE.MathUtils.radToDeg(euler.z).toFixed(1))
            ],
            scale: [
              parseFloat(worldScale.x.toFixed(3)),
              parseFloat(worldScale.y.toFixed(3)),
              parseFloat(worldScale.z.toFixed(3))
            ],
            color: node.material && node.material.color ? '#' + node.material.color.getHexString() : '#ffffff',
            roughness: node.material && typeof node.material.roughness === 'number' ? node.material.roughness : 0.7,
            metalness: node.material && typeof node.material.metalness === 'number' ? node.material.metalness : 0.2,
            visible: node.visible !== false
          };

          components.push(comp);
        }
      });

      if (components.length === 0) {
        throw new Error(`El modelo GLB de ${family} no contiene mallas.`);
      }

      const remixSpec: ModelSpec = {
        id: `remix.${family}.${Date.now().toString(36)}`,
        name: `${entry.name} (Remix)`,
        category: entry.category || 'props',
        description: `Versión editable y modular de ${entry.name}. Desarmada con sus mallas 3D originales para personalización en Studio.`,
        units: 'meters',
        dimensions: {
          width: parseFloat((sizeVec.x || 1.0).toFixed(3)),
          height: parseFloat((sizeVec.y || 1.0).toFixed(3)),
          depth: parseFloat((sizeVec.z || 1.0).toFixed(3))
        },
        palette: userParams?.palette || 'industrial_hazard',
        components
      };

      // Apply proportional scale adjustments if user supplied custom dimensions
      if (userParams && Object.keys(userParams).length > 0) {
        this.applyParametersToSpec(remixSpec, userParams, entry);
      }

      return remixSpec;
    } catch (err) {
      console.warn(`[CatalogBridge] Fallback a especificación procedural para ${family}:`, err);
      return this.buildSpecFromCatalog(family, userParams);
    }
  }

  /**
   * Builds an authentic, fully editable procedural ModelSpec for any catalog family (synchronous fallback).
   */
  public static buildSpecFromCatalog(
    family: string,
    userParams?: Record<string, any>
  ): ModelSpec {
    const entry = (catalog as any[]).find((c: any) => c.family === family) || {
      family,
      name: family.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
      category: 'props',
      description: 'Modelo procedural desglosado para edición modular.'
    };

    // 1. Synthesize baseline procedural piece composition using title & family keywords
    const prompt = `${entry.name} ${entry.family.replace(/_/g, ' ')}`;
    const baseSpec = AIGenerator.synthesizeProceduralSpec(prompt);

    // 2. Clone and brand as a fresh remixable draft for the user
    const remixSpec: ModelSpec = JSON.parse(JSON.stringify(baseSpec));
    remixSpec.id = `remix.${family}.${Date.now().toString(36)}`;
    remixSpec.name = `${entry.name} (Remix)`;
    remixSpec.category = entry.category || baseSpec.category || 'props';
    remixSpec.description = `Versión editable y modular de ${entry.name}. Desarmada en componentes individuales para personalización en Studio 3D.`;

    // 3. Apply custom user parameters if provided (e.g. width, height, depth, thickness)
    if (userParams && Object.keys(userParams).length > 0) {
      this.applyParametersToSpec(remixSpec, userParams, entry);
    }

    return remixSpec;
  }

  /**
   * Proportionally scales dimensions and piece offsets based on user slider adjustments.
   */
  private static applyParametersToSpec(
    spec: ModelSpec,
    params: Record<string, any>,
    catalogEntry?: any
  ) {
    const origDims = spec.dimensions || { width: 1, height: 1, depth: 1 };
    let targetW = origDims.width;
    let targetH = origDims.height;
    let targetD = origDims.depth;

    if (params.width !== undefined && typeof params.width === 'number' && params.width > 0) {
      targetW = params.width;
    }
    if (params.height !== undefined && typeof params.height === 'number' && params.height > 0) {
      targetH = params.height;
    }
    if (params.depth !== undefined && typeof params.depth === 'number' && params.depth > 0) {
      targetD = params.depth;
    } else if (params.thickness !== undefined && typeof params.thickness === 'number' && params.thickness > 0) {
      targetD = params.thickness;
    }

    const scaleX = origDims.width > 0.001 ? targetW / origDims.width : 1;
    const scaleY = origDims.height > 0.001 ? targetH / origDims.height : 1;
    const scaleZ = origDims.depth > 0.001 ? targetD / origDims.depth : 1;

    // Apply scale to components if dimensions changed noticeably
    if (Math.abs(scaleX - 1) > 0.01 || Math.abs(scaleY - 1) > 0.01 || Math.abs(scaleZ - 1) > 0.01) {
      spec.components.forEach((comp) => {
        if (comp.shape === 'mesh') {
          if (!comp.scale) comp.scale = [1, 1, 1];
          comp.scale[0] = parseFloat((comp.scale[0] * scaleX).toFixed(3));
          comp.scale[1] = parseFloat((comp.scale[1] * scaleY).toFixed(3));
          comp.scale[2] = parseFloat((comp.scale[2] * scaleZ).toFixed(3));
        } else if (comp.size && comp.size.length >= 2) {
          if (comp.shape === 'box' || comp.shape === 'wedge') {
            comp.size[0] = parseFloat((comp.size[0] * scaleX).toFixed(3));
            comp.size[1] = parseFloat((comp.size[1] * scaleY).toFixed(3));
            if (comp.size[2] !== undefined) comp.size[2] = parseFloat((comp.size[2] * scaleZ).toFixed(3));
          } else if (comp.shape === 'cylinder' || comp.shape === 'cone') {
            const radScale = (scaleX + scaleZ) * 0.5;
            comp.size[0] = parseFloat((comp.size[0] * radScale).toFixed(3));
            if (comp.size[1] !== undefined) comp.size[1] = parseFloat((comp.size[1] * radScale).toFixed(3));
            if (comp.size[2] !== undefined) comp.size[2] = parseFloat((comp.size[2] * scaleY).toFixed(3));
          } else if (comp.shape === 'sphere') {
            const avgScale = (scaleX + scaleY + scaleZ) / 3;
            comp.size[0] = parseFloat((comp.size[0] * avgScale).toFixed(3));
          }
        }
        if (comp.position) {
          comp.position[0] = parseFloat((comp.position[0] * scaleX).toFixed(3));
          comp.position[1] = parseFloat((comp.position[1] * scaleY).toFixed(3));
          comp.position[2] = parseFloat((comp.position[2] * scaleZ).toFixed(3));
        }
      });

      spec.dimensions = {
        width: parseFloat(targetW.toFixed(3)),
        height: parseFloat(targetH.toFixed(3)),
        depth: parseFloat(targetD.toFixed(3))
      };
    }

    // Apply palette if specified in parameters
    if (params.palette && typeof params.palette === 'string') {
      spec.palette = params.palette;
    }
  }
}
