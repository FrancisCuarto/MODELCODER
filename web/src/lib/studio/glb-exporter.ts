import * as THREE from 'three';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { ProceduralEngine } from './procedural-engine.ts';
import { AnimationEngine } from './animation-engine.ts';
import type { ModelSpec } from './types.ts';

export interface ExportVerificationResult {
  verified: boolean;
  sizeBytes: number;
  triangleCount: number;
  vertexCount: number;
  animationCount?: number;
  animationNames?: string[];
  error?: string;
}

export class GLBExporterService {
  /**
   * Safe polyfills for GLTFExporter/GLTFLoader when running in headless Node.js tests.
   */
  private static ensureNodePolyfills(): void {
    if (typeof (globalThis as any).self === 'undefined') {
      (globalThis as any).self = globalThis;
    }
    if (typeof (globalThis as any).ImageData === 'undefined') {
      (globalThis as any).ImageData = class NodeImageData {
        data: Uint8ClampedArray;
        width: number;
        height: number;
        constructor(data: any, width: number, height: number) {
          this.data = data;
          this.width = width;
          this.height = height;
        }
      };
    }
    if (typeof (globalThis as any).FileReader === 'undefined') {
      class NodeFileReader {
        onload: any = null;
        onloadend: any = null;
        onerror: any = null;
        result: any = null;
        readAsArrayBuffer(blob: any) {
          blob.arrayBuffer().then((buf: any) => {
            this.result = buf;
            if (this.onload) this.onload({ target: this });
            if (this.onloadend) this.onloadend({ target: this });
          }).catch((err: any) => {
            if (this.onerror) this.onerror(err);
          });
        }
      }
      (globalThis as any).FileReader = NodeFileReader;
    }
    if (typeof (globalThis as any).document === 'undefined') {
      (globalThis as any).document = {
        createElement: (tag: string) => {
          if (tag === 'canvas') {
            return {
              width: 0,
              height: 0,
              getContext: () => ({
                translate: () => {},
                scale: () => {},
                putImageData: () => {},
                drawImage: () => {},
                getImageData: (_x: number, _y: number, w = 64, h = 64) => ({
                  data: new Uint8ClampedArray(w * h * 4),
                  width: w,
                  height: h
                }),
                createImageData: (w = 64, h = 64) => ({
                  data: new Uint8ClampedArray(w * h * 4),
                  width: w,
                  height: h
                })
              }),
              toBlob: (cb: any, type: string) => {
                const png1x1 = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==', 'base64');
                cb(new Blob([png1x1], { type: type || 'image/png' }));
              }
            };
          }
          return {};
        }
      };
    }
  }

  /**
   * Exports an exact Three.js object hierarchy to binary GLB,
   * performs a MANDATORY test-import verification, and triggers browser download.
   */
  public static async exportAndVerifyGLB(
    rootObj: THREE.Object3D,
    filename = 'modelcoder_asset',
    options?: { animations?: THREE.AnimationClip[] }
  ): Promise<ExportVerificationResult> {
    if (!rootObj) {
      throw new Error('No hay ningún objeto 3D activo para exportar.');
    }

    // 1. Export scene to binary GLB ArrayBuffer with optional animation tracks
    const glbBuffer = await this.exportToArrayBuffer(rootObj, options);

    // 2. Mandatory Verification Step: Test-import the exported GLB buffer
    const verification = await this.verifyGLBBuffer(glbBuffer);
    if (!verification.verified) {
      throw new Error(`Fallo de verificación en exportación GLB: ${verification.error}`);
    }

    // 3. Trigger clean browser download of the verified file
    if (typeof document !== 'undefined' && document.body) {
      const blob = new Blob([glbBuffer], { type: 'model/gltf-binary' });
      const blobUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = filename.endsWith('.glb') ? filename : `${filename}.glb`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => URL.revokeObjectURL(blobUrl), 15000);
    }

    return verification;
  }

  /**
   * Generates a Three.js hierarchy from a ModelSpec and exports it to a binary GLB ArrayBuffer.
   */
  public static async exportSpec(
    spec: ModelSpec,
    options?: { animations?: THREE.AnimationClip[] }
  ): Promise<ArrayBuffer> {
    const { group } = ProceduralEngine.buildModelFromSpec(spec);
    try {
      let anims = options?.animations;
      if (!anims && spec.animations && spec.animations.length > 0) {
        anims = AnimationEngine.compileClipsToThree(spec.animations, group);
      }
      return await this.exportToArrayBuffer(group, anims && anims.length > 0 ? { animations: anims } : undefined);
    } finally {
      ProceduralEngine.disposeHierarchy(group);
    }
  }

  /**
   * Converts a Three.js hierarchy to an ArrayBuffer using GLTFExporter.
   */
  public static exportToArrayBuffer(
    obj: THREE.Object3D,
    options?: { animations?: THREE.AnimationClip[] }
  ): Promise<ArrayBuffer> {
    this.ensureNodePolyfills();
    const stashedMaps: Array<{ mat: any; normalMap: any; roughnessMap: any }> = [];
    obj.traverse((node: any) => {
      if (node.isMesh && node.material) {
        const mats = Array.isArray(node.material) ? node.material : [node.material];
        for (const m of mats) {
          if ((m.normalMap && m.normalMap.isDataTexture) || (m.roughnessMap && m.roughnessMap.isDataTexture)) {
            stashedMaps.push({ mat: m, normalMap: m.normalMap, roughnessMap: m.roughnessMap });
            if (m.normalMap?.isDataTexture) m.normalMap = null;
            if (m.roughnessMap?.isDataTexture) m.roughnessMap = null;
          }
        }
      }
    });
    const restoreMaps = () => {
      for (const item of stashedMaps) {
        item.mat.normalMap = item.normalMap;
        item.mat.roughnessMap = item.roughnessMap;
      }
    };

    return new Promise((resolve, reject) => {
      const exporter = new GLTFExporter();
      const exportOptions: any = {
        binary: true,
        embedImages: true,
        includeCustomExtensions: true
      };
      if (options?.animations && options.animations.length > 0) {
        exportOptions.animations = options.animations;
      }

      exporter.parse(
        obj,
        (result) => {
          restoreMaps();
          if (result instanceof ArrayBuffer) {
            resolve(result);
          } else {
            // Convert string JSON to buffer if not binary
            const jsonStr = JSON.stringify(result);
            const enc = new TextEncoder();
            resolve(enc.encode(jsonStr).buffer as ArrayBuffer);
          }
        },
        (error) => {
          restoreMaps();
          reject(new Error(`Error durante exportación GLTFExporter: ${error}`));
        },
        exportOptions
      );
    });
  }

  /**
   * Performs an immediate round-trip test import using GLTFLoader
   * to guarantee the GLB binary is well-formed, readable, and retains geometry.
   */
  public static async verifyGLBBuffer(buffer: ArrayBuffer): Promise<ExportVerificationResult> {
    this.ensureNodePolyfills();
    if (!buffer || buffer.byteLength < 20) {
      return {
        verified: false,
        sizeBytes: buffer ? buffer.byteLength : 0,
        triangleCount: 0,
        vertexCount: 0,
        error: 'El búfer GLB está vacío o corrupto (menor a 20 bytes).'
      };
    }

    // Validate GLB Magic Header 'glTF' (0x46546C67)
    const view = new DataView(buffer);
    const magic = view.getUint32(0, true);
    if (magic !== 0x46546c67) {
      return {
        verified: false,
        sizeBytes: buffer.byteLength,
        triangleCount: 0,
        vertexCount: 0,
        error: 'El archivo generado no contiene la cabecera binaria mágica válida de glTF (glTF).'
      };
    }

    try {
      const loader = new GLTFLoader();
      const gltf = await loader.parseAsync(buffer, '');

      if (!gltf.scene) {
        return {
          verified: false,
          sizeBytes: buffer.byteLength,
          triangleCount: 0,
          vertexCount: 0,
          error: 'El archivo GLB no contiene una escena 3D válida tras importación de prueba.'
        };
      }

      let triCount = 0;
      let vertCount = 0;

      gltf.scene.traverse((node: any) => {
        if (node.isMesh && node.geometry) {
          const pos = node.geometry.getAttribute('position');
          if (pos) {
            vertCount += pos.count;
            triCount += node.geometry.index ? node.geometry.index.count / 3 : pos.count / 3;
          }
        }
      });

      if (vertCount === 0) {
        return {
          verified: false,
          sizeBytes: buffer.byteLength,
          triangleCount: 0,
          vertexCount: 0,
          error: 'El modelo GLB importado de prueba no contiene vértices.'
        };
      }

      const animCount = gltf.animations ? gltf.animations.length : 0;
      const animNames = gltf.animations ? gltf.animations.map((a: any) => a.name) : [];

      return {
        verified: true,
        sizeBytes: buffer.byteLength,
        triangleCount: Math.round(triCount),
        vertexCount: Math.round(vertCount),
        animationCount: animCount,
        animationNames: animNames
      };
    } catch (err: any) {
      return {
        verified: false,
        sizeBytes: buffer.byteLength,
        triangleCount: 0,
        vertexCount: 0,
        error: `Fallo durante el análisis de re-importación con GLTFLoader: ${err.message}`
      };
    }
  }
}
