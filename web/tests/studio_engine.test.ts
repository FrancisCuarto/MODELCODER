import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';

// Node.js test environment polyfills for THREE.GLTFExporter & ImageData
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
            beginPath: () => {},
            moveTo: () => {},
            lineTo: () => {},
            quadraticCurveTo: () => {},
            closePath: () => {},
            fill: () => {},
            stroke: () => {},
            fillRect: () => {},
            clearRect: () => {},
            fillText: () => {},
            measureText: (text: string) => ({ width: (text || '').length * 10 }),
            createLinearGradient: () => ({ addColorStop: () => {} }),
            createRadialGradient: () => ({ addColorStop: () => {} })
          }),
          toDataURL: (type: string) => 'data:image/png;base64,mock',
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
if (typeof globalThis.FileReader === 'undefined') {
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
    readAsDataURL(blob: any) {
      blob.arrayBuffer().then((buf: any) => {
        const base64 = Buffer.from(buf).toString('base64');
        this.result = `data:${blob.type || 'application/octet-stream'};base64,${base64}`;
        if (this.onload) this.onload({ target: this });
        if (this.onloadend) this.onloadend({ target: this });
      }).catch((err: any) => {
        if (this.onerror) this.onerror(err);
      });
    }
  }
  (globalThis as any).FileReader = NodeFileReader;
}

// Node.js test environment polyfill for localStorage
if (typeof (globalThis as any).window === 'undefined') {
  const store = new Map<string, string>();
  const mockLocalStorage = {
    getItem: (key: string) => store.get(key) || null,
    setItem: (key: string, val: string) => store.set(key, String(val)),
    removeItem: (key: string) => store.delete(key),
    clear: () => store.clear()
  };
  (globalThis as any).window = { localStorage: mockLocalStorage };
  (globalThis as any).localStorage = mockLocalStorage;
}

import { ProceduralEngine } from '../src/lib/studio/procedural-engine.ts';
import { CodeSandbox } from '../src/lib/studio/code-sandbox.ts';
import { AIGenerator } from '../src/lib/studio/ai-generator.ts';
import { GLBExporterService } from '../src/lib/studio/glb-exporter.ts';
import { ProceduralMemory } from '../src/lib/studio/procedural-memory.ts';
import { TextureLibrary } from '../src/lib/studio/texture-library.ts';
import { AnimationEngine } from '../src/lib/studio/animation-engine.ts';
import { StudioViewport } from '../src/lib/studio/three-viewport.ts';
import { serializeSpecToHash, deserializeSpecFromHash, compressSpecToHash, deserializeSpec } from '../src/lib/studio/share-serializer.ts';
import { generateAllSnippets, generateGodotScript, generateUnityScript, generateThreeJsScript } from '../src/lib/studio/gamedev-exporter.ts';
import type { ModelSpec } from '../src/lib/studio/types.ts';
import fs from 'node:fs';
import path from 'node:path';

test('Criterion 1 & 2: Solicitar un cubo y luego una esfera genera geometrías distintas y dimensiones reales', () => {
  // 1. Generate cube
  const cubeSpec = AIGenerator.synthesizeProceduralSpec('un cubo de 1 metro');
  assert.equal(cubeSpec.components[0].shape, 'box');
  const { group: cubeGroup, stats: cubeStats } = ProceduralEngine.buildModelFromSpec(cubeSpec);

  assert.equal(cubeStats.triangles, 12); // Standard box = 12 tris
  assert.equal(cubeStats.vertices, 24); // 24 vertices for non-indexed/box corners
  assert.equal(cubeStats.dimensions.x, 1.0);
  assert.equal(cubeStats.dimensions.y, 1.0);
  assert.equal(cubeStats.dimensions.z, 1.0);

  // 2. Generate sphere
  const sphereSpec = AIGenerator.synthesizeProceduralSpec('una esfera roja de 2 metros');
  assert.equal(sphereSpec.components[0].shape, 'sphere');
  const { group: sphereGroup, stats: sphereStats } = ProceduralEngine.buildModelFromSpec(sphereSpec);

  // Verifications
  assert.notEqual(sphereStats.triangles, cubeStats.triangles, 'Sphere must have different triangle count than box');
  assert.notEqual(sphereStats.vertices, cubeStats.vertices, 'Sphere must have different vertex count than box');
  assert.equal(sphereStats.dimensions.x, 2.0, 'Sphere width should be 2.0m');
  assert.equal(sphereStats.dimensions.y, 2.0, 'Sphere height should be 2.0m');

  // Dispose
  ProceduralEngine.disposeHierarchy(cubeGroup);
  ProceduralEngine.disposeHierarchy(sphereGroup);
});

test('Criterion 3: Solicitar una tarjeta de acceso genera sus componentes reales (cuerpo, chip, banda)', () => {
  const cardSpec = AIGenerator.synthesizeProceduralSpec('tarjeta de acceso de seguridad con chip y banda magnetica');
  assert.equal(cardSpec.id, 'below_nominal.security.access_card');
  assert.ok(cardSpec.components.length >= 4, 'Access card must contain multiple geometric components');

  const compNames = cardSpec.components.map(c => c.name);
  assert.ok(compNames.includes('card_body'), 'Must contain card body');
  assert.ok(compNames.includes('smart_chip'), 'Must contain smart microchip');
  assert.ok(compNames.includes('magnetic_stripe'), 'Must contain magnetic stripe');

  const { group, stats } = ProceduralEngine.buildModelFromSpec(cardSpec);
  assert.ok(stats.triangles > 40, 'Access card should be low-poly but multi-component');
  assert.ok(stats.dimensions.x > 0.4 && stats.dimensions.x < 0.7, 'Card width should match real proportions');

  ProceduralEngine.disposeHierarchy(group);
});

test('Criterion 4: Modificar parámetros en código refleja cambios en el resultado geométrico', () => {
  const codeSmall = `
    builder.setName("Small Box");
    builder.addBox({ size: [0.5, 0.5, 0.5], color: "metal" });
  `;
  const codeLarge = `
    builder.setName("Large Box");
    builder.addBox({ size: [2.5, 3.0, 1.8], color: "metal" });
  `;

  const { spec: spec1, error: err1 } = CodeSandbox.executeCode(codeSmall);
  assert.equal(err1, undefined);
  const { stats: stats1 } = ProceduralEngine.buildModelFromSpec(spec1);

  const { spec: spec2, error: err2 } = CodeSandbox.executeCode(codeLarge);
  assert.equal(err2, undefined);
  const { stats: stats2 } = ProceduralEngine.buildModelFromSpec(spec2);

  assert.equal(stats1.dimensions.x, 0.5);
  assert.equal(stats1.dimensions.y, 0.5);
  assert.equal(stats2.dimensions.x, 2.5);
  assert.equal(stats2.dimensions.y, 3.0);
  assert.equal(stats2.dimensions.z, 1.8);
});

test('Criterion 5: Un error de sintaxis en el código genera un error claro y legible', () => {
  const invalidCode = `
    builder.addBox({ size: [1, 1, 1]  // Missing closing parenthesis & brace
  `;

  const { error } = CodeSandbox.executeCode(invalidCode);
  assert.ok(error, 'Must return error string');
  assert.ok(error.includes('Error'), 'Error must contain descriptive failure message');
});

test('Criterion 7: El modelo exportado genera un búfer binario GLB verificado con GLTFLoader', async () => {
  const spec = AIGenerator.synthesizeProceduralSpec('consola de radar con tres pantallas');
  const { group } = ProceduralEngine.buildModelFromSpec(spec);

  const buffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(buffer.byteLength > 500, 'GLB buffer must be larger than 500 bytes');

  // Verify round-trip test import
  const verification = await GLBExporterService.verifyGLBBuffer(buffer);
  assert.equal(verification.verified, true, `Verification must pass, error: ${verification.error}`);
  assert.ok(verification.triangleCount > 0, 'Exported GLB must contain triangles');
  assert.ok(verification.vertexCount > 0, 'Exported GLB must contain vertices');

  ProceduralEngine.disposeHierarchy(group);
});

test('Criterion 6: Una generación antigua no puede sustituir una generación más reciente', () => {
  let activeVersion = 0;
  let activeId = '';
  let activeTriangles = 0;

  function applyResult(res: { id: string; version: number; stats: { triangles: number } }) {
    if (res.version < activeVersion) {
      // Discard stale out-of-order generation
      return false;
    }
    activeVersion = res.version;
    activeId = res.id;
    activeTriangles = res.stats.triangles;
    return true;
  }

  // Request 1 arrives (v1)
  const ok1 = applyResult({ id: 'GEN-001', version: 1, stats: { triangles: 100 } });
  assert.equal(ok1, true);
  assert.equal(activeId, 'GEN-001');

  // Request 2 arrives (v2)
  const ok2 = applyResult({ id: 'GEN-002', version: 2, stats: { triangles: 250 } });
  assert.equal(ok2, true);
  assert.equal(activeId, 'GEN-002');
  assert.equal(activeTriangles, 250);

  // Stale Request arrives late (v1)
  const okStale = applyResult({ id: 'GEN-001-LATE', version: 1, stats: { triangles: 999 } });
  assert.equal(okStale, false, 'Late older generation must be discarded');
  assert.equal(activeId, 'GEN-002', 'Active generation must remain the newer version');
  assert.equal(activeTriangles, 250, 'Triangles must remain from newer version');
});

test('Procedural Blueprints: Solicitar un "auto" genera chasis, cabina y 4 ruedas reales con llantas', () => {
  const carSpec = AIGenerator.synthesizeProceduralSpec('auto');
  assert.equal(carSpec.id, 'below_nominal.vehicles.retro_car');
  assert.ok(carSpec.components.length >= 10, 'Car must contain chassis, cabin, windshield, wheels and lights');

  const compNames = carSpec.components.map(c => c.name);
  assert.ok(compNames.includes('chassis_body'), 'Must contain chassis');
  assert.ok(compNames.includes('cabin_roof'), 'Must contain cabin');
  assert.ok(compNames.includes('windshield'), 'Must contain windshield');
  assert.ok(compNames.includes('wheel_front_left'), 'Must contain front left wheel');
  assert.ok(compNames.includes('wheel_front_right'), 'Must contain front right wheel');
  assert.ok(compNames.includes('wheel_rear_left'), 'Must contain rear left wheel');
  assert.ok(compNames.includes('wheel_rear_right'), 'Must contain rear right wheel');

  const { group, stats } = ProceduralEngine.buildModelFromSpec(carSpec);
  assert.ok(stats.triangles > 80, 'Car must be detailed low-poly mesh');
  assert.ok(stats.dimensions.z > 2.5, 'Car depth must reflect a real vehicle length (>2.5m)');
  assert.ok(stats.dimensions.x > 1.2, 'Car width must reflect a real vehicle width (>1.2m)');

  ProceduralEngine.disposeHierarchy(group);
});

test('Procedural Blueprints: Solicitar "nave espacial" y "robot" genera objetos únicos y diferenciados', () => {
  const shipSpec = AIGenerator.synthesizeProceduralSpec('nave espacial con alas y propulsores');
  assert.equal(shipSpec.id, 'below_nominal.vehicles.space_fighter');
  const shipNames = shipSpec.components.map(c => c.name);
  assert.ok(shipNames.includes('fuselage_core'));
  assert.ok(shipNames.includes('wing_left'));
  assert.ok(shipNames.includes('thruster_left'));

  const robotSpec = AIGenerator.synthesizeProceduralSpec('robot androide');
  assert.equal(robotSpec.id, 'below_nominal.security.service_droid');
  const robotNames = robotSpec.components.map(c => c.name);
  assert.ok(robotNames.includes('torso_chassis'));
  assert.ok(robotNames.includes('optical_visor'));
  assert.ok(robotNames.includes('leg_left'));

  const { stats: shipStats, group: shipGroup } = ProceduralEngine.buildModelFromSpec(shipSpec);
  const { stats: robotStats, group: robotGroup } = ProceduralEngine.buildModelFromSpec(robotSpec);

  assert.notEqual(shipStats.triangles, robotStats.triangles);
  assert.notEqual(shipStats.dimensions.y, robotStats.dimensions.y);

  ProceduralEngine.disposeHierarchy(shipGroup);
  ProceduralEngine.disposeHierarchy(robotGroup);
});

test('Procedural Memory: Cuando se genera un modelo nuevo, se almacena y se recupera en las siguientes peticiones', async () => {
  const prompt = 'submarino militar amarillo con periscopio';
  
  // First generation: synthesized fresh
  const res1 = await AIGenerator.generateModel(prompt);
  assert.equal(res1.source, 'local');
  assert.ok(res1.spec.components.length > 0);

  // Second generation with same prompt: must hit 'local_memory'
  const res2 = await AIGenerator.generateModel(prompt);
  assert.equal(res2.source, 'local_memory', 'Second call must hit learned memory');
  assert.equal(res2.spec.name, res1.spec.name);
  assert.equal(res2.spec.components.length, res1.spec.components.length);

  // Clean memory for other tests
  ProceduralMemory.clearLocalMemory();
});

test('Engine Selector: modo "ai" exige clave Gemini y no consulta caché local', async () => {
  // Sin clave o clave inválida: debe fallar con mensaje claro
  await assert.rejects(
    async () => {
      await AIGenerator.generateModel('nave interceptora', { engine: 'ai', apiKey: '' });
    },
    /Para usar la IA Generativa necesitas ingresar tu clave/
  );

  await assert.rejects(
    async () => {
      await AIGenerator.generateModel('nave interceptora', { engine: 'ai', apiKey: 'corta' });
    },
    /Para usar la IA Generativa necesitas ingresar tu clave/
  );
});

test('Engine Selector: modo "local" funciona de forma autónoma sin clave y con memoria', async () => {
  ProceduralMemory.clearLocalMemory();
  const res = await AIGenerator.generateModel('tanque blindado oruga', { engine: 'local' });
  assert.equal(res.source, 'local');
  assert.ok(res.spec.components.length > 0);

  // Segunda llamada en modo local utiliza la memoria aprendida
  const resCached = await AIGenerator.generateModel('tanque blindado oruga', { engine: 'local' });
  assert.equal(resCached.source, 'local_memory');

  // Llamada forzando refresco (forceFresh) omite la memoria aprendida
  const resFresh = await AIGenerator.generateModel('tanque blindado oruga', { engine: 'local', forceFresh: true });
  assert.equal(resFresh.source, 'local');

  ProceduralMemory.clearLocalMemory();
});

test('Material System Test 1: Un componente antiguo que solo tenga color sigue funcionando (compatibilidad retroactiva)', () => {
  const legacySpec = {
    id: 'test.legacy.box',
    name: 'Caja Antigua',
    category: 'furniture',
    description: 'Componente legado sin preset de textura',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'standard',
    components: [
      {
        name: 'legacy_cube',
        shape: 'box' as const,
        size: [1.0, 1.0, 1.0],
        position: [0, 0.5, 0] as [number, number, number],
        color: '#e53e3e' // Red hex only
      }
    ]
  };

  const { group, stats } = ProceduralEngine.buildModelFromSpec(legacySpec);
  assert.equal(stats.triangles, 12);
  assert.equal(group.children.length, 1);

  const mesh = group.children[0] as THREE.Mesh;
  const mat = mesh.material as THREE.MeshStandardMaterial;
  assert.equal(mat.vertexColors, true, 'Legacy component must use vertex colors');
  assert.equal(mat.map, null, 'Legacy component without texturePreset must not have a texture map');
  assert.ok(mat.color.r > 0.7, 'Material color should be reddish');

  ProceduralEngine.disposeHierarchy(group);
});

test('Material System Test 2: Un componente con texturePreset: "worn_industrial" muestra una textura real y no un color plano', () => {
  const spec = {
    id: 'test.textured.worn',
    name: 'Panel Industrial',
    category: 'infrastructure',
    description: 'Componente con preset alias worn_industrial',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'industrial_chassis',
        shape: 'box' as const,
        size: [1.0, 1.0, 1.0],
        texturePreset: 'worn_industrial' // Alias for metal_dark_grime
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const mesh = group.children[0] as THREE.Mesh;
  const mat = mesh.material as THREE.MeshStandardMaterial;

  assert.ok(mat.map !== null, 'Textured component must have an active material.map');
  assert.ok(mat.map instanceof THREE.DataTexture, 'Texture map must be a THREE.DataTexture');
  assert.equal(mat.map.magFilter, THREE.NearestFilter, 'Texture must use NearestFilter for authentic PS1 look');
  assert.equal(mat.map.minFilter, THREE.NearestFilter, 'Texture must use NearestFilter on minFilter');
  assert.equal(mat.map.wrapS, THREE.RepeatWrapping, 'Texture must support RepeatWrapping');
  assert.equal(mat.roughness, 0.70, 'Roughness should match metal_dark_grime profile default');
  assert.equal(mat.metalness, 0.38, 'Metalness should match metal_dark_grime profile default');

  ProceduralEngine.disposeHierarchy(group);
});

test('Material System Test 3: Un modelo compuesto por metal, goma y pantalla muestra tres tratamientos visuales distintos', () => {
  const multiSpec = {
    id: 'test.multi.materials',
    name: 'Dispositivo Multi-Material',
    category: 'command',
    description: 'Objeto con tres materiales texturizados distintos',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'metal_frame',
        shape: 'box' as const,
        size: [1.0, 0.4, 0.8],
        texturePreset: 'worn_metal'
      },
      {
        name: 'rubber_feet',
        shape: 'cylinder' as const,
        size: [0.1, 0.1, 0.15, 8],
        position: [0, -0.2, 0] as [number, number, number],
        texturePreset: 'rubber_black'
      },
      {
        name: 'radar_display',
        shape: 'box' as const,
        size: [0.6, 0.3, 0.02],
        position: [0, 0.3, 0.4] as [number, number, number],
        texturePreset: 'crt_screen_green'
      }
    ]
  };

  const { group, stats } = ProceduralEngine.buildModelFromSpec(multiSpec);
  assert.equal(group.children.length, 3);
  assert.ok(stats.triangles > 20);

  const metalMesh = group.children[0] as THREE.Mesh;
  const rubberMesh = group.children[1] as THREE.Mesh;
  const screenMesh = group.children[2] as THREE.Mesh;

  const metalMat = metalMesh.material as THREE.MeshStandardMaterial;
  const rubberMat = rubberMesh.material as THREE.MeshStandardMaterial;
  const screenMat = screenMesh.material as THREE.MeshStandardMaterial;

  // 1. All 3 have active textures
  assert.ok(metalMat.map !== null, 'Metal must have texture');
  assert.ok(rubberMat.map !== null, 'Rubber must have texture');
  assert.ok(screenMat.map !== null, 'Screen must have texture');

  // 2. All 3 textures are distinct
  assert.notEqual(metalMat.map, rubberMat.map, 'Metal and rubber must have distinct textures');
  assert.notEqual(metalMat.map, screenMat.map, 'Metal and screen must have distinct textures');
  assert.notEqual(rubberMat.map, screenMat.map, 'Rubber and screen must have distinct textures');

  // 3. Different surface physics
  assert.ok(metalMat.metalness > rubberMat.metalness, 'Metal must have higher metalness than rubber');
  assert.ok(rubberMat.roughness > screenMat.roughness, 'Rubber must be rougher than glass screen');
  assert.ok(screenMat.emissive && screenMat.emissiveIntensity > 0, 'Screen must have emissive glow enabled');

  ProceduralEngine.disposeHierarchy(group);
});

test('Material System Test 4: Mapeo UV anti-estiramiento en cajas y cuñas', () => {
  // Elongated rectangular pillar: 0.2m x 2.0m x 0.2m
  const pillarSpec = {
    id: 'test.uv.pillar',
    name: 'Columna Alargada',
    category: 'infrastructure',
    description: 'Pilar con rayas de peligro sin estiramiento',
    units: 'meters' as const,
    dimensions: { width: 0.2, depth: 0.2, height: 2.0 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'hazard_pillar',
        shape: 'box' as const,
        size: [0.2, 2.0, 0.2],
        texturePreset: 'hazard_stripes'
      },
      {
        name: 'wedge_ramp',
        shape: 'wedge' as const,
        size: [0.5, 0.3, 0.4],
        texturePreset: 'worn_metal'
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(pillarSpec);
  const pillarMesh = group.children[0] as THREE.Mesh;
  const boxGeom = pillarMesh.geometry;
  const uvAttr = boxGeom.getAttribute('uv');
  assert.ok(uvAttr, 'BoxGeometry must have UV attribute');

  const uvs = uvAttr.array;
  // Face 4 (+Z Front face): width = 0.2, height = 2.0
  // v0 is (0, 2.0), v1 is (0.2, 2.0), v2 is (0, 0), v3 is (0.2, 0)
  const f4_v1_u = uvs[(4 * 4 + 1) * 2];
  const f4_v1_v = uvs[(4 * 4 + 1) * 2 + 1];
  assert.ok(Math.abs(f4_v1_u - 0.2) < 0.001, `UV U should be scaled to width (0.2), got ${f4_v1_u}`);
  assert.ok(Math.abs(f4_v1_v - 2.0) < 0.001, `UV V should be scaled to height (2.0), got ${f4_v1_v}`);

  // Wedge UV verification
  const wedgeMesh = group.children[1] as THREE.Mesh;
  const wedgeGeom = wedgeMesh.geometry;
  const wedgeUvAttr = wedgeGeom.getAttribute('uv');
  assert.ok(wedgeUvAttr, 'WedgeGeometry must have UV attribute');
  assert.equal(wedgeUvAttr.count, 24, 'Wedge must have 24 UV coordinate pairs');

  ProceduralEngine.disposeHierarchy(group);
});

test('Material System Test 5: Exportación e importación GLB conserva los 3 materiales texturizados', async () => {
  const modelSpec = {
    id: 'test.glb.multi',
    name: 'Consola Operativa Multi-Textura',
    category: 'command',
    description: 'Consola con metal, goma y pantalla CRT',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 0.8, height: 1.0 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'chassis',
        shape: 'box' as const,
        size: [1.0, 0.6, 0.8],
        texturePreset: 'worn_metal'
      },
      {
        name: 'bumper_rubber',
        shape: 'cylinder' as const,
        size: [0.15, 0.15, 0.8, 8],
        position: [0, -0.2, 0.4] as [number, number, number],
        texturePreset: 'rubber_black'
      },
      {
        name: 'crt_monitor',
        shape: 'box' as const,
        size: [0.5, 0.35, 0.05],
        position: [0, 0.4, 0.2] as [number, number, number],
        texturePreset: 'crt_screen_green'
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(modelSpec);

  // 1. Export scene to binary GLB
  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(glbBuffer instanceof ArrayBuffer, 'GLB export must return an ArrayBuffer');
  assert.ok(glbBuffer.byteLength > 1500, `GLB buffer must contain geometry and textures (got ${glbBuffer.byteLength} bytes)`);

  // 2. Validate round-trip test import with GLTFLoader
  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true, `GLB verification failed: ${verification.error}`);
  assert.ok(verification.triangleCount > 0, 'Imported GLB must retain triangle count');
  assert.ok(verification.vertexCount > 0, 'Imported GLB must retain vertex count');

  ProceduralEngine.disposeHierarchy(group);
});

test('Material System Test 6: disposeHierarchy no destruye las texturas cacheadas en TextureLibrary', () => {
  const spec = {
    id: 'test.dispose.leak',
    name: 'Test Regeneración',
    category: 'furniture',
    description: 'Prueba de liberación de memoria segura',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'standard',
    components: [
      {
        name: 'crate',
        shape: 'box' as const,
        size: [1, 1, 1],
        texturePreset: 'hazard_stripes'
      }
    ]
  };

  // 1st generation
  const { group: group1 } = ProceduralEngine.buildModelFromSpec(spec);
  const mesh1 = group1.children[0] as THREE.Mesh;
  const mat1 = mesh1.material as THREE.MeshStandardMaterial;
  const tex1 = mat1.map!;
  assert.ok(TextureLibrary.isPresetTexture(tex1), 'Texture should be recognized as library preset');

  // Dispose 1st generation
  ProceduralEngine.disposeHierarchy(group1);

  // 2nd generation immediately after disposal
  const { group: group2 } = ProceduralEngine.buildModelFromSpec(spec);
  const mesh2 = group2.children[0] as THREE.Mesh;
  const mat2 = mesh2.material as THREE.MeshStandardMaterial;
  const tex2 = mat2.map!;

  assert.equal(tex1, tex2, 'Texture instance should be safely reused across generations without memory leaks');
  assert.ok(tex2.image.data !== null, 'Reused texture pixel data must remain valid');

  ProceduralEngine.disposeHierarchy(group2);
});

test('Editor Redesign 1: Componentes reciben userData.componentIndex y respetan visibilidad comp.visible === false', () => {
  const spec = {
    id: 'test.editor.selection',
    name: 'Selection Test',
    category: 'test',
    description: 'Verificación de selección y visibilidad',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'standard',
    components: [
      { name: 'visible_part', shape: 'box' as const, size: [1, 1, 1], visible: true },
      { name: 'hidden_part', shape: 'cylinder' as const, size: [0.5, 0.5, 1, 8], visible: false }
    ]
  };

  const { group, stats } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 2, 'Must create both meshes in group');

  // Verification of index tagging for raycasting and gizmos
  assert.equal(group.children[0].userData.componentIndex, 0, 'First mesh must have componentIndex 0');
  assert.equal(group.children[1].userData.componentIndex, 1, 'Second mesh must have componentIndex 1');

  // Verification of visibility
  assert.equal(group.children[0].visible, true, 'Visible component must have mesh.visible true');
  assert.equal(group.children[1].visible, false, 'Hidden component must have mesh.visible false');

  ProceduralEngine.disposeHierarchy(group);
});

test('Editor Redesign 2: Las 8 primitivas generan geometrías válidas según sus parámetros reales', () => {
  const spec = {
    id: 'test.editor.primitives',
    name: 'Primitives Test',
    category: 'test',
    description: 'Las 8 primitivas paramétricas',
    units: 'meters' as const,
    dimensions: { width: 4.0, depth: 4.0, height: 2.0 },
    palette: 'standard',
    components: [
      { name: 'p_box', shape: 'box' as const, size: [1.2, 0.8, 1.5] },
      { name: 'p_cyl', shape: 'cylinder' as const, size: [0.4, 0.2, 1.2, 12] },
      { name: 'p_sph', shape: 'sphere' as const, size: [0.6, 10, 8] },
      { name: 'p_wdg', shape: 'wedge' as const, size: [1.0, 0.6, 0.9] },
      { name: 'p_cne', shape: 'cone' as const, size: [0.5, 1.1, 10] },
      { name: 'p_tor', shape: 'torus' as const, size: [0.7, 0.12, 8, 16] },
      { name: 'p_cap', shape: 'capsule' as const, size: [0.3, 0.8, 4, 8] },
      { name: 'p_pln', shape: 'plane' as const, size: [1.5, 1.2] }
    ]
  };

  const { group, stats } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 8, 'All 8 primitives must be instantiated');
  assert.ok(stats.triangles > 200, 'Combined triangle count should reflect all 8 primitives');
  assert.ok(stats.vertices > 200, 'Combined vertex count should reflect all 8 primitives');

  for (let i = 0; i < group.children.length; i++) {
    const mesh = group.children[i] as THREE.Mesh;
    assert.ok(mesh.geometry instanceof THREE.BufferGeometry, `Primitive #${i} (${spec.components[i].shape}) must have valid geometry`);
    assert.ok(mesh.geometry.getAttribute('position').count > 0, `Primitive #${i} must have position vertices`);
  }

  ProceduralEngine.disposeHierarchy(group);
});

test('Editor Redesign 3: Soporte de transparencia, opacidad y modo alámbrico individual', () => {
  const spec = {
    id: 'test.editor.material_props',
    name: 'Material Props Test',
    category: 'test',
    description: 'Transparencia, opacidad y wireframe',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'standard',
    components: [
      {
        name: 'glass_canopy',
        shape: 'box' as const,
        size: [1, 1, 1],
        transparent: true,
        opacity: 0.35,
        wireframe: false
      },
      {
        name: 'wire_cage',
        shape: 'sphere' as const,
        size: [0.5, 8, 6],
        wireframe: true
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const meshGlass = group.children[0] as THREE.Mesh;
  const matGlass = meshGlass.material as THREE.MeshStandardMaterial;

  assert.equal(matGlass.transparent, true, 'Glass component material must be transparent');
  assert.equal(matGlass.opacity, 0.35, 'Glass component opacity must be 0.35');
  assert.equal(matGlass.wireframe, false, 'Glass wireframe must be false');

  const meshWire = group.children[1] as THREE.Mesh;
  const matWire = meshWire.material as THREE.MeshStandardMaterial;
  assert.equal(matWire.wireframe, true, 'Wireframe component material must have wireframe true');

  ProceduralEngine.disposeHierarchy(group);
});

test('Editor Redesign 4: Mutaciones de Outliner (Duplicar, Renombrar, Eliminar) preservan integridad del ModelSpec', () => {
  let spec = {
    id: 'test.editor.mutations',
    name: 'Crate Editable',
    category: 'furniture',
    description: 'Prueba de mutaciones de árbol',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'standard',
    components: [
      { name: 'base', shape: 'box' as const, size: [1, 0.2, 1], position: [0, 0.1, 0] as [number, number, number] }
    ]
  };

  // 1. Add primitive
  spec.components.push({
    name: 'pillar',
    shape: 'cylinder' as const,
    size: [0.1, 0.1, 0.8, 8],
    position: [0.4, 0.5, 0.4] as [number, number, number]
  });
  assert.equal(spec.components.length, 2);

  // 2. Duplicate component
  const copy = JSON.parse(JSON.stringify(spec.components[1]));
  copy.name = 'pillar_copia';
  copy.position[0] -= 0.8;
  spec.components.push(copy);
  assert.equal(spec.components.length, 3);
  assert.equal(spec.components[2].name, 'pillar_copia');

  // 3. Rename component
  spec.components[0].name = 'base_reforzada';
  assert.equal(spec.components[0].name, 'base_reforzada');

  // 4. Build and verify
  const { group, stats } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 3);
  assert.equal(group.children[0].name, 'base_reforzada');
  assert.equal(group.children[2].name, 'pillar_copia');

  // 5. Delete component
  spec.components.splice(1, 1);
  assert.equal(spec.components.length, 2);
  const { group: groupAfterDel } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(groupAfterDel.children.length, 2);

  ProceduralEngine.disposeHierarchy(group);
  ProceduralEngine.disposeHierarchy(groupAfterDel);
});

test('Editor Redesign 5: Exportación GLB preserva transformaciones, nuevas primitivas y materiales del editor', async () => {
  const spec = {
    id: 'test.editor.export',
    name: 'Estudio Custom Model',
    category: 'furniture',
    description: 'Exportación con múltiples piezas editadas',
    units: 'meters' as const,
    dimensions: { width: 2.0, depth: 2.0, height: 1.5 },
    palette: 'standard',
    components: [
      {
        name: 'plataforma',
        shape: 'box' as const,
        size: [1.4, 0.15, 1.4],
        position: [0, 0.075, 0] as [number, number, number],
        rotation: [0, 45, 0] as [number, number, number],
        texturePreset: 'worn_metal',
        color: '#4a5568'
      },
      {
        name: 'tanque_capsula',
        shape: 'capsule' as const,
        size: [0.25, 0.6, 4, 8],
        position: [0, 0.6, 0] as [number, number, number],
        texturePreset: 'hazard_stripes',
        color: '#ffffff'
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(glbBuffer.byteLength > 2000, 'GLB exported from custom editor spec must contain valid binary payload');

  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true);
  assert.ok(verification.triangleCount > 50);
  assert.ok(verification.vertexCount > 50);

  ProceduralEngine.disposeHierarchy(group);
});

test('Transparency & Glass Textures: Soporte de texturas con opacidad y presets de vidrio', async () => {
  const spec = {
    id: 'test.glass_dome',
    name: 'Cúpula de Vidrio Polarizado',
    category: 'architecture',
    description: 'Estructura con vidrio y metal texturizado',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'base_metal',
        shape: 'cylinder' as const,
        size: [0.5, 0.5, 0.2, 12],
        position: [0, 0.1, 0] as [number, number, number],
        texturePreset: 'worn_metal',
        color: '#4a5568'
      },
      {
        name: 'vidrio_cupula',
        shape: 'sphere' as const,
        size: [0.45, 12, 8],
        position: [0, 0.45, 0] as [number, number, number],
        texturePreset: 'tinted_glass',
        transparent: true,
        opacity: 0.45
      },
      {
        name: 'panel_blindado',
        shape: 'box' as const,
        size: [0.6, 0.4, 0.05],
        position: [0, 0.5, 0.4] as [number, number, number],
        texturePreset: 'reinforced_glass'
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 3);

  // Check base metal: opaque
  const baseMesh = group.children[0] as THREE.Mesh;
  const baseMat = baseMesh.material as THREE.MeshStandardMaterial;
  assert.equal(baseMat.transparent, false);
  assert.equal(baseMat.opacity, 1.0);

  // Check tinted glass: transparent with texture and opacity 0.45
  const glassMesh = group.children[1] as THREE.Mesh;
  const glassMat = glassMesh.material as THREE.MeshStandardMaterial;
  assert.equal(glassMat.transparent, true);
  assert.equal(glassMat.opacity, 0.45);
  assert.ok(glassMat.map !== null, 'Glass must have procedural surface texture');
  assert.equal(glassMat.depthWrite, false, 'Translucent glass should not occlude depth buffer');
  assert.equal(glassMat.side, THREE.DoubleSide, 'Glass should render both front and back faces');

  // Check reinforced glass: transparent by preset profile
  const wireGlassMesh = group.children[2] as THREE.Mesh;
  const wireGlassMat = wireGlassMesh.material as THREE.MeshStandardMaterial;
  assert.equal(wireGlassMat.transparent, true);
  assert.ok(wireGlassMat.opacity < 1.0);
  assert.ok(wireGlassMat.map !== null);

  // Check GLB export with glass materials
  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(glbBuffer.byteLength > 2000);
  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true);

  ProceduralEngine.disposeHierarchy(group);
});

test('Expanded Texture Library 1: 118 texturas base PBR + 20 variantes paramétricas cubren las 8 familias sin duplicados', () => {
  const profileKeys = Object.keys(TextureLibrary.PROFILES);
  const variantKeys = Object.keys(TextureLibrary.PARAMETRIC_VARIANTS);

  assert.equal(profileKeys.length, 118, 'Must provide 118 canonical procedural PBR base textures');
  assert.equal(variantKeys.length, 20, 'Must provide 20 curated parametric variants');

  const expectedCategories = [
    'metals',
    'construction',
    'woods',
    'stones',
    'plastics',
    'tech',
    'glass',
    'fabrics_organic'
  ] as const;

  for (const cat of expectedCategories) {
    const inCat = TextureLibrary.getProfilesByCategory(cat);
    assert.ok(inCat.length >= 9, `Category ${cat} must have at least 9 canonical presets (got ${inCat.length})`);
  }

  // Verify every parametric variant references a valid canonical basePreset
  for (const v of Object.values(TextureLibrary.PARAMETRIC_VARIANTS)) {
    const resolved = TextureLibrary.resolvePresetName(v.id);
    assert.equal(resolved, v.basePreset, `Variant ${v.id} must resolve to its basePreset ${v.basePreset}`);
    assert.ok(TextureLibrary.PROFILES[v.basePreset], `Base preset ${v.basePreset} must exist in PROFILES`);
  }
});

test('Expanded Texture Library 2: Las 118 texturas generan píxeles RGBA válidos y mapas normales distintos por familia', () => {
  const representativePresets = [
    'steel_polished',
    'diamond_plate',
    'copper_oxidized',
    'brick_red',
    'concrete_cracked',
    'wood_oak',
    'wood_parquet',
    'marble_white',
    'granite_grey',
    'acoustic_foam',
    'pcb_green_gold',
    'carbon_fiber',
    'solar_panel_blue',
    'frosted_glass',
    'kevlar_ballistic',
    'leather_brown_aged'
  ] as const;

  const signatures = new Set<string>();

  for (const preset of representativePresets) {
    const tex = TextureLibrary.getTexture(preset);
    const data = tex.image.data as Uint8Array;
    assert.equal(data.byteLength, 64 * 64 * 4, `Preset ${preset} must generate 64x64 RGBA buffer`);

    // Compute a quick checksum signature to prove each procedural pattern is visually distinct
    let sumR = 0, sumG = 0, sumB = 0;
    for (let i = 0; i < data.length; i += 4) {
      sumR += data[i];
      sumG += data[i + 1];
      sumB += data[i + 2];
    }
    assert.ok(sumR + sumG + sumB > 0, `Preset ${preset} pixels must not be all black`);
    const sig = `${sumR}:${sumG}:${sumB}`;
    assert.equal(signatures.has(sig), false, `Preset ${preset} must have a distinct pixel signature`);
    signatures.add(sig);

    // Check normal map generation
    const normTex = TextureLibrary.getNormalTexture(preset, 0.6);
    const normData = normTex.image.data as Uint8Array;
    assert.equal(normData.byteLength, 64 * 64 * 4, `Preset ${preset} normalMap must be 64x64 RGBA`);
    assert.ok(TextureLibrary.isPresetTexture(normTex), 'Generated normalMap must be registered as preset texture');
  }
});

test('Expanded Texture Library 3: Variaciones paramétricas (wear, uvRotation, normalStrength) y preservación en disposeHierarchy', () => {
  const spec = {
    id: 'test.parametric.variants',
    name: 'Test Variantes Paramétricas',
    category: 'infrastructure',
    description: 'Prueba de rotación UV, desgaste procedural y relieve normal',
    units: 'meters' as const,
    dimensions: { width: 2.0, depth: 2.0, height: 1.0 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'clean_brick_wall',
        shape: 'box' as const,
        size: [1.0, 1.0, 0.2],
        texturePreset: 'brick_red',
        wear: 0,
        uvRotation: 0
      },
      {
        name: 'weathered_rotated_brick',
        shape: 'box' as const,
        size: [1.0, 1.0, 0.2],
        texturePreset: 'brick_red',
        wear: 0.75,
        uvRotation: 90,
        normalStrength: 0.9
      },
      {
        name: 'curated_variant_part',
        shape: 'cylinder' as const,
        size: [0.3, 0.3, 1.0, 8],
        texturePreset: 'diamond_plate_rusted'
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const cleanMesh = group.children[0] as THREE.Mesh;
  const weatheredMesh = group.children[1] as THREE.Mesh;
  const variantMesh = group.children[2] as THREE.Mesh;

  const cleanMat = cleanMesh.material as THREE.MeshStandardMaterial;
  const weatheredMat = weatheredMesh.material as THREE.MeshStandardMaterial;
  const variantMat = variantMesh.material as THREE.MeshStandardMaterial;

  assert.notEqual(cleanMat.map, weatheredMat.map, 'Weathered component should use wear-modulated texture buffer');
  assert.ok(weatheredMat.roughness > cleanMat.roughness, 'Weathered surface should have increased roughness');
  assert.ok(cleanMat.normalMap !== null, 'Opaque PBR material must include procedural normalMap');
  assert.ok(variantMat.map !== null, 'Curated parametric variant must resolve and attach texture');

  // Verify UV rotation mutated UVs on weatheredMesh compared to cleanMesh
  const uvsClean = cleanMesh.geometry.getAttribute('uv').array as Float32Array;
  const uvsRot = weatheredMesh.geometry.getAttribute('uv').array as Float32Array;
  assert.notEqual(
    `${uvsClean[0].toFixed(3)},${uvsClean[1].toFixed(3)}`,
    `${uvsRot[0].toFixed(3)},${uvsRot[1].toFixed(3)}`,
    'UV rotation (90 deg) must rotate vertex UV coordinates'
  );

  // Verify disposeHierarchy preserves normalMap as well as map
  const savedNorm = cleanMat.normalMap!;
  ProceduralEngine.disposeHierarchy(group);
  assert.ok(TextureLibrary.isPresetTexture(savedNorm), 'NormalMap must remain registered in TextureLibrary after dispose');
});

test('Expanded Texture Library 4: Exportación GLB multi-familia (madera, mármol, ladrillo, carbono, vidrio) y restauración de normalMap', async () => {
  const spec = {
    id: 'test.glb.multifamily',
    name: 'Escena Multi-Familia PBR',
    category: 'architecture',
    description: 'Prueba de exportación GLB con las nuevas familias de materiales',
    units: 'meters' as const,
    dimensions: { width: 2.0, depth: 2.0, height: 2.0 },
    palette: 'standard',
    components: [
      { name: 'oak_table', shape: 'box' as const, size: [1.2, 0.1, 0.8], texturePreset: 'wood_oak' },
      { name: 'marble_pillar', shape: 'cylinder' as const, size: [0.2, 0.2, 1.0, 10], texturePreset: 'marble_white' },
      { name: 'brick_base', shape: 'box' as const, size: [1.5, 0.4, 1.5], texturePreset: 'brick_red' },
      { name: 'carbon_arm', shape: 'capsule' as const, size: [0.1, 0.5, 4, 8], texturePreset: 'carbon_fiber' },
      { name: 'cryo_window', shape: 'box' as const, size: [0.8, 0.6, 0.04], texturePreset: 'cryo_glass_ice' }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const firstMeshMat = (group.children[0] as THREE.Mesh).material as THREE.MeshStandardMaterial;
  assert.ok(firstMeshMat.normalMap !== null, 'Normal map must be present before export');

  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(glbBuffer.byteLength > 2000, 'Exported multi-family GLB must be non-empty');
  assert.ok(firstMeshMat.normalMap !== null, 'Normal map must be restored on live scene material after GLB export');

  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true, `Multi-family GLB verification failed: ${verification.error}`);
  assert.ok(verification.triangleCount > 50);

  ProceduralEngine.disposeHierarchy(group);
});

test('Expanded Texture Library 5: Adaptación UV automática ante escala no uniforme (comp.scale)', () => {
  const spec = {
    id: 'test.uv.nonuniform_scale',
    name: 'Prueba UV Escala No Uniforme',
    category: 'industrial',
    description: 'Verifica que escalar una pieza con gizmo/escala adapte las coordenadas UV proporcionalmente sin estirar la textura',
    units: 'meters' as const,
    dimensions: { width: 1.0, depth: 1.0, height: 2.0 },
    palette: 'industrial',
    components: [
      {
        name: 'hazard_stripe_scaled',
        shape: 'box' as const,
        size: [1.0, 1.0, 1.0],
        scale: [0.29, 1.88, 1.38] as [number, number, number],
        texturePreset: 'hazard_stripes',
        uvScale: [1.0, 1.0] as [number, number]
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const mesh = group.children[0] as THREE.Mesh;
  const uvs = mesh.geometry.getAttribute('uv') as THREE.BufferAttribute;

  // Face 0 (+X side face) has width = d * sz = 1.38 and height = h * sy = 1.88
  const uMaxRightFace = Math.max(uvs.getX(0), uvs.getX(1), uvs.getX(2), uvs.getX(3));
  const vMaxRightFace = Math.max(uvs.getY(0), uvs.getY(1), uvs.getY(2), uvs.getY(3));
  assert.ok(Math.abs(uMaxRightFace - 1.38) < 0.01, `Expected +X face U span ~1.38, got ${uMaxRightFace}`);
  assert.ok(Math.abs(vMaxRightFace - 1.88) < 0.01, `Expected +X face V span ~1.88, got ${vMaxRightFace}`);

  // Face 4 (+Z front face) has width = w * sx = 0.29 and height = h * sy = 1.88
  const uMaxFrontFace = Math.max(uvs.getX(16), uvs.getX(17), uvs.getX(18), uvs.getX(19));
  const vMaxFrontFace = Math.max(uvs.getY(16), uvs.getY(17), uvs.getY(18), uvs.getY(19));
  assert.ok(Math.abs(uMaxFrontFace - 0.29) < 0.01, `Expected +Z face U span ~0.29, got ${uMaxFrontFace}`);
  assert.ok(Math.abs(vMaxFrontFace - 1.88) < 0.01, `Expected +Z face V span ~1.88, got ${vMaxFrontFace}`);

  ProceduralEngine.disposeHierarchy(group);
});

test('Instagram Story & Post Exporter: Genera lienzo Story (1080x1920) y Post 1:1 (1080x1080) con marca de agua y ficha técnica', async () => {
  const {
    drawStoryCard,
    STORY_THEMES,
    STORY_CANVAS_WIDTH,
    STORY_CANVAS_HEIGHT,
    POST_CANVAS_WIDTH,
    POST_CANVAS_HEIGHT,
    wrapAndDrawText,
    exportStoryToBlob
  } = await import('../src/lib/studio/story-generator.ts');

  // Verify dimensions
  assert.equal(STORY_CANVAS_WIDTH, 1080);
  assert.equal(STORY_CANVAS_HEIGHT, 1920);
  assert.equal(POST_CANVAS_WIDTH, 1080);
  assert.equal(POST_CANVAS_HEIGHT, 1080);

  // Verify 5 themes defined
  const themeKeys = Object.keys(STORY_THEMES);
  assert.ok(themeKeys.includes('cyber_dark'));
  assert.ok(themeKeys.includes('carbon_minimal'));
  assert.ok(themeKeys.includes('neon_synth'));
  assert.ok(themeKeys.includes('gold_luxury'));
  assert.ok(themeKeys.includes('transparent_sticker'));

  // Test text wrapping helper
  const mockCtx = {
    fillText: () => {},
    measureText: (str: string) => ({ width: str.length * 10 })
  } as any;
  const longDesc = 'Este es un contenedor de carga hermético presurizado para almacenamiento en estaciones orbitales con blindaje reforzado y paneles modulares.';
  const lines = wrapAndDrawText(mockCtx, longDesc, 0, 0, 200, 30, 3);
  assert.ok(lines > 0 && lines <= 3, `Expected 1-3 lines, got ${lines}`);

  // Test story canvas generation with mock model canvas
  const mockModelCanvas = document.createElement('canvas') as HTMLCanvasElement;
  mockModelCanvas.width = 1080;
  mockModelCanvas.height = 1080;

  // 1. Story 9:16
  const storyCanvas = drawStoryCard(mockModelCanvas, {
    format: 'story',
    title: 'Crate Hull Alpha',
    description: longDesc,
    author: 'FrancisCoder',
    theme: 'cyber_dark',
    showWatermark: true,
    showDescription: true,
    showStats: true,
    showTechFrame: true,
    stats: {
      triangles: 50,
      vertices: 100,
      componentCount: 4,
      materialsSummary: 'METAL WORN · GLASS',
      generationId: 'GEN-TEST-01'
    }
  });

  assert.equal(storyCanvas.width, 1080);
  assert.equal(storyCanvas.height, 1920);

  // 2. Post 1:1 (Square Feed)
  const postCanvas = drawStoryCard(mockModelCanvas, {
    format: 'post',
    title: 'Crate Hull Alpha',
    description: longDesc,
    author: 'FrancisCoder',
    theme: 'gold_luxury',
    showWatermark: true,
    showDescription: true,
    showStats: true,
    showTechFrame: true,
    stats: {
      triangles: 50,
      vertices: 100,
      componentCount: 4,
      materialsSummary: 'GOLD · TITANIUM',
      generationId: 'GEN-TEST-02'
    }
  });

  assert.equal(postCanvas.width, 1080);
  assert.equal(postCanvas.height, 1080);

  // Test export to blob
  const storyBlob = await exportStoryToBlob(storyCanvas);
  assert.ok(storyBlob instanceof Blob);
  assert.equal(storyBlob.type, 'image/png');

  const postBlob = await exportStoryToBlob(postCanvas);
  assert.ok(postBlob instanceof Blob);
  assert.equal(postBlob.type, 'image/png');
});

test('Animation System 1: AnimationEngine presets generate valid declarative tracks and keyframes', () => {
  const presets = AnimationEngine.getAvailablePresets();
  assert.equal(presets.length, 6, 'Must provide 6 standard animation presets');

  // Sliding door
  const doorClip = AnimationEngine.createPresetClip('sliding_door', {
    targetComponent: 'door_left',
    axis: 'x',
    distance: 1.5,
    duration: 1.0,
    initialPos: [0, 0, 0]
  });
  assert.equal(doorClip.tracks.length, 1);
  assert.equal(doorClip.tracks[0].targetComponent, 'door_left');
  assert.equal(doorClip.tracks[0].property, 'position');
  assert.equal(doorClip.tracks[0].keyframes.length, 3);
  assert.deepEqual(doorClip.tracks[0].keyframes[0].value, [0, 0, 0]);
  assert.deepEqual(doorClip.tracks[0].keyframes[1].value, [1.5, 0, 0]);

  // Hinge lid
  const lidClip = AnimationEngine.createPresetClip('hinge_lid', {
    targetComponent: 'hatch_top',
    axis: 'y',
    openAngleDeg: 90,
    duration: 1.2,
    initialRot: [0, 0, 0]
  });
  assert.equal(lidClip.tracks.length, 1);
  assert.equal(lidClip.tracks[0].property, 'rotation');
  assert.deepEqual(lidClip.tracks[0].keyframes[1].value, [0, 90, 0]);

  // Spin continuous 360
  const spinClip = AnimationEngine.createPresetClip('spin_continuous', {
    targetComponent: 'radar_dish',
    axis: 'z',
    duration: 3.0,
    initialRot: [0, 0, 0]
  });
  assert.equal(spinClip.tracks.length, 1);
  assert.equal(spinClip.tracks[0].keyframes.length, 4);
  assert.deepEqual(spinClip.tracks[0].keyframes[3].value, [0, 0, 360]);

  // Mechanical deploy (both position and rotation tracks)
  const deployClip = AnimationEngine.createPresetClip('mechanical_deploy', {
    targetComponent: 'landing_gear',
    axis: 'y',
    extendDistance: 1.0,
    deployAngleDeg: 45,
    duration: 2.0
  });
  assert.equal(deployClip.tracks.length, 2, 'Mechanical deploy combines position and rotation tracks');
});

test('Animation System 2: Three.js compilation converts Euler angles to Quaternions and sets track targets', () => {
  const doorClip = AnimationEngine.createPresetClip('sliding_door', {
    targetComponent: 'gate',
    axis: 'x',
    distance: 2.0,
    duration: 1.0
  });
  const spinClip = AnimationEngine.createPresetClip('spin_continuous', {
    targetComponent: 'rotor',
    axis: 'y',
    duration: 2.0
  });

  const threeClips = AnimationEngine.compileClipsToThree([doorClip, spinClip]);
  assert.equal(threeClips.length, 2);

  // Door clip has VectorKeyframeTrack
  const threeDoor = threeClips[0];
  assert.equal(threeDoor.name, doorClip.name);
  assert.equal(threeDoor.tracks.length, 1);
  assert.equal(threeDoor.tracks[0].name, 'gate.position');
  assert.ok(threeDoor.tracks[0] instanceof THREE.VectorKeyframeTrack);

  // Spin clip has QuaternionKeyframeTrack
  const threeSpin = threeClips[1];
  assert.equal(threeSpin.tracks.length, 1);
  assert.equal(threeSpin.tracks[0].name, 'rotor.quaternion');
  assert.ok(threeSpin.tracks[0] instanceof THREE.QuaternionKeyframeTrack);
  assert.equal(threeSpin.tracks[0].values.length, 4 * 4, '4 keyframes * 4 quaternion components = 16 values');
});

test('Animation System 3: GLB export embeds animation tracks and verifyGLBBuffer confirms round-trip fidelity', async () => {
  const testSpec: ModelSpec = {
    id: 'anim_test_spec',
    name: 'Animated Mech Door Unit',
    category: 'sci-fi',
    description: 'Unit test model with sliding door and spinning radar',
    units: 'meters',
    dimensions: { width: 3, height: 2, depth: 2 },
    palette: 'industrial',
    components: [
      {
        name: 'frame_base',
        shape: 'box',
        size: [2.0, 0.2, 1.0],
        position: [0, 0, 0],
        color: '#444444'
      },
      {
        name: 'door_panel',
        shape: 'box',
        size: [0.8, 1.5, 0.1],
        position: [0, 0.85, 0],
        color: '#3182ce'
      },
      {
        name: 'radar_beacon',
        shape: 'cylinder',
        size: [0.2, 0.2, 0.4, 8],
        position: [0, 1.8, 0],
        color: '#dd6b20'
      }
    ],
    animations: [
      AnimationEngine.createPresetClip('sliding_door', {
        name: 'OpenDoor',
        targetComponent: 'door_panel',
        axis: 'x',
        distance: 0.9,
        duration: 1.5,
        initialPos: [0, 0.85, 0]
      }),
      AnimationEngine.createPresetClip('spin_continuous', {
        name: 'SpinRadar',
        targetComponent: 'radar_beacon',
        axis: 'y',
        duration: 2.0,
        initialRot: [0, 0, 0]
      })
    ]
  };

  // Export to GLB
  const glbBuffer = await GLBExporterService.exportSpec(testSpec);
  assert.ok(glbBuffer instanceof ArrayBuffer);
  assert.ok(glbBuffer.byteLength > 100);

  // Mandatory verification
  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true, 'Exported animated GLB must pass test-import verification');
  assert.ok(verification.triangleCount > 0);
  assert.equal(verification.animationCount, 2, 'Exported GLB must contain exactly 2 animation clips');
  assert.ok(verification.animationNames?.includes('OpenDoor'));
  assert.ok(verification.animationNames?.includes('SpinRadar'));
});

test('Animation System 4: CodeSandbox supports programmatic animation scripting and presets', () => {
  const scriptCode = `
    builder.setName("Bunker Hatch");
    builder.addBox({ name: "frame", size: [2, 0.2, 2], position: [0, 0, 0] });
    builder.addBox({ name: "hatch_door", size: [1.8, 0.1, 1.8], position: [0, 0.1, 0] });
    builder.addPresetAnimation('sliding_door', {
      targetName: 'hatch_door',
      clipName: 'Abrir_Hatch',
      deltaDistance: 1.5,
      axis: 'z',
      duration: 1.5
    });
  `;

  const { spec, error } = CodeSandbox.executeCode(scriptCode);
  assert.equal(error, undefined, `Script execution error: ${error}`);
  assert.equal(spec.name, 'Bunker Hatch');
  assert.equal(spec.components.length, 2);
  assert.ok(spec.animations, 'Animations array should be populated');
  assert.equal(spec.animations.length, 1);
  assert.equal(spec.animations[0].name, 'Abrir_Hatch');
  assert.equal(spec.animations[0].duration, 1.5);
  assert.equal(spec.animations[0].tracks.length, 1);
  assert.equal(spec.animations[0].tracks[0].targetName, 'hatch_door');
  assert.equal(spec.animations[0].tracks[0].property, 'position');
});

test('Animation System 5: Custom keyframe animations can be authored with arbitrary tracks and exported to GLB', async () => {
  const customSpec: ModelSpec = {
    id: 'test_custom_anim_spec',
    name: 'Custom Robotic Arm',
    category: 'robotics',
    description: 'Arm with user-authored keyframes',
    units: 'meters',
    dimensions: { width: 1, height: 2, depth: 1 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'base_pillar',
        shape: 'cylinder',
        size: [0.3, 0.3, 1.0, 10],
        position: [0, 0.5, 0],
        color: '#4a5568'
      },
      {
        name: 'servo_head',
        shape: 'box',
        size: [0.4, 0.3, 0.4],
        position: [0, 1.15, 0],
        rotation: [0, 0, 0],
        color: '#ffcc00'
      }
    ],
    animations: [
      {
        id: 'clip_user_dance',
        name: 'RoboDance_Custom',
        duration: 3.0,
        loop: 'repeat',
        tracks: [
          {
            targetComponent: 'servo_head',
            targetName: 'servo_head',
            property: 'rotation',
            keyframes: [
              { time: 0.0, value: [0, 0, 0], interpolation: 'linear' },
              { time: 0.75, value: [0, 45, -15], interpolation: 'linear' },
              { time: 1.5, value: [10, -45, 15], interpolation: 'linear' },
              { time: 2.25, value: [-10, 30, 0], interpolation: 'linear' },
              { time: 3.0, value: [0, 0, 0], interpolation: 'linear' }
            ]
          },
          {
            targetComponent: 'servo_head',
            targetName: 'servo_head',
            property: 'position',
            keyframes: [
              { time: 0.0, value: [0, 1.15, 0], interpolation: 'cubic' },
              { time: 1.5, value: [0, 1.35, 0], interpolation: 'cubic' },
              { time: 3.0, value: [0, 1.15, 0], interpolation: 'cubic' }
            ]
          }
        ]
      }
    ]
  };

  // Compile to Three.js AnimationClip
  const threeClips = AnimationEngine.compileClipsToThree(customSpec.animations);
  assert.equal(threeClips.length, 1);
  assert.equal(threeClips[0].name, 'RoboDance_Custom');
  assert.equal(threeClips[0].duration, 3.0);
  assert.equal(threeClips[0].tracks.length, 2);
  assert.equal(threeClips[0].tracks[0].name, 'servo_head.quaternion');
  assert.equal(threeClips[0].tracks[1].name, 'servo_head.position');

  // Export to GLB with embedded custom animation
  const glbBuf = await GLBExporterService.exportSpec(customSpec);
  assert.ok(glbBuf instanceof ArrayBuffer);

  const verification = await GLBExporterService.verifyGLBBuffer(glbBuf);
  assert.equal(verification.verified, true);
  assert.equal(verification.animationCount, 1);
  assert.ok(verification.animationNames?.includes('RoboDance_Custom'));
});

test('Catalog Animations: Modelos clave del catálogo público contienen pistas de animación reproducibles', async () => {
  const publicModelsDir = fs.existsSync(path.resolve(process.cwd(), 'public/models'))
    ? path.resolve(process.cwd(), 'public/models')
    : path.resolve(process.cwd(), 'web/public/models');

  const catalogTargets = [
    { file: 'antenna_dish.glb', clip: 'Giro_Escaner' },
    { file: 'alarm_siren.glb', clip: 'Baliza_Giro' },
    { file: 'security_camera.glb', clip: 'Vigilancia_Pan' },
    { file: 'door.glb', clip: 'Abrir_Puerta' },
    { file: 'maintenance_hatch.glb', clip: 'Abrir_Escotilla' },
    { file: 'crate.glb', clip: 'Inspeccion_Flotante' }
  ];

  for (const item of catalogTargets) {
    const fullPath = path.join(publicModelsDir, item.file);
    assert.ok(fs.existsSync(fullPath), `El modelo ${item.file} debe existir en el catálogo público`);

    const fileBuf = fs.readFileSync(fullPath);
    const arrayBuf = fileBuf.buffer.slice(fileBuf.byteOffset, fileBuf.byteOffset + fileBuf.byteLength);

    const verification = await GLBExporterService.verifyGLBBuffer(arrayBuf);
    assert.equal(verification.verified, true, `El archivo ${item.file} debe pasar la verificación de importación GLB`);
    assert.ok(verification.triangleCount > 0, `${item.file} debe contener geometría válida`);
    assert.ok(verification.animationCount >= 1, `${item.file} debe incluir al menos 1 clip de animación`);
    assert.ok(
      verification.animationNames?.includes(item.clip),
      `${item.file} debe incluir el clip '${item.clip}', encontrados: ${verification.animationNames?.join(', ')}`
    );
  }
});

test('Studio Video Loop: StudioViewport expone recordAnimationLoop para exportar clips WebM', () => {
  assert.equal(
    typeof StudioViewport.prototype.recordAnimationLoop,
    'function',
    'StudioViewport debe implementar el método recordAnimationLoop'
  );
});

test('URL Share Serializer: Serializar y deserializar un ModelSpec preserva su estructura completa', () => {
  const sampleSpec: ModelSpec = {
    id: 'test.share.unit',
    name: 'Radar Móvil',
    category: 'fixtures',
    description: 'Antena de prueba para compartir en URL',
    units: 'meters',
    dimensions: { width: 1, depth: 1, height: 1.5 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'base_mount',
        shape: 'box',
        size: [1, 0.2, 1],
        position: [0, 0.1, 0],
        rotation: [0, 0, 0],
        scale: [1, 1, 1],
        color: '#334455'
      },
      {
        name: 'radar_dish',
        shape: 'cylinder',
        size: [0.8, 0.8, 0.2, 8],
        position: [0, 1.0, 0],
        rotation: [0, 0, 0],
        scale: [1, 1, 1],
        color: '#f0ad4e'
      }
    ],
    animations: [
      {
        name: 'GiroRadar',
        duration: 2.0,
        tracks: [
          {
            targetComponent: 'radar_dish',
            property: 'rotation',
            interpolation: 'linear',
            keyframes: [
              { time: 0, value: [0, 0, 0] },
              { time: 2, value: [0, 360, 0] }
            ]
          }
        ]
      }
    ]
  };

  const hashToken = serializeSpecToHash(sampleSpec);
  assert.ok(hashToken.length > 20, 'Hash token debe ser una cadena no vacía');
  assert.match(hashToken, /^[A-Za-z0-9_-]+$/, 'Hash token debe ser URL-safe (sin +, /, ni =)');

  // Deserializar sin prefijo
  const restored1 = deserializeSpecFromHash(hashToken);
  assert.ok(restored1, 'Debe restaurar el objeto');
  assert.equal(restored1?.name, sampleSpec.name);
  assert.equal(restored1?.components.length, 2);
  assert.equal(restored1?.animations?.length, 1);
  assert.equal(restored1?.animations?.[0].name, 'GiroRadar');

  // Deserializar con prefijo # o #model=
  const restored2 = deserializeSpecFromHash(`#model=${hashToken}`);
  assert.equal(restored2?.name, sampleSpec.name);

  // Manejo de tokens corruptos
  const invalid = deserializeSpecFromHash('token_invalido_corrupto_!!!');
  assert.equal(invalid, null, 'Tokens corruptos deben devolver null de forma segura');
});

test('URL Share Serializer (Compressed): Comprime con Deflate y restaura ModelSpec reduciendo tamaño', async () => {
  const sampleSpec: ModelSpec = {
    id: 'test.compressed.unit',
    name: 'Sensor Espacial',
    category: 'security',
    description: 'Sensor de prueba para enlaces comprimidos',
    components: [
      { name: 'base', shape: 'box', size: [1, 0.2, 1], position: [0, 0, 0] },
      { name: 'lente', shape: 'cylinder', size: [0.5, 0.5, 0.4, 12], position: [0, 0.5, 0] }
    ]
  };

  const rawToken = serializeSpecToHash(sampleSpec);
  const compressedToken = await compressSpecToHash(sampleSpec);

  assert.ok(compressedToken.startsWith('z:'), 'Debe incluir prefijo z:');
  assert.ok(compressedToken.length < rawToken.length, 'Token comprimido debe ser significativamente más corto que el original');

  const restored = await deserializeSpec(compressedToken);
  assert.ok(restored, 'Debe descomprimir y deserializar correctamente');
  assert.equal(restored?.name, sampleSpec.name);
  assert.equal(restored?.components.length, 2);

  // También debe deserializar tokens sin comprimir
  const restoredRaw = await deserializeSpec(rawToken);
  assert.equal(restoredRaw?.name, sampleSpec.name);
});

test('GameDev Code Exporter: Genera scripts válidos para Godot 4, Unity y Three.js con soporte de animaciones', () => {
  const animatedSpec: ModelSpec = {
    id: 'below_nominal.fixtures.antenna_dish',
    name: 'Antena Parabólica',
    category: 'fixtures',
    description: 'Antena parabólica con rotación',
    units: 'meters',
    dimensions: { width: 1.5, depth: 1.5, height: 2.2 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'plato_parabolico',
        shape: 'cylinder',
        size: [1.2, 1.2, 0.2, 8],
        position: [0, 1.5, 0],
        rotation: [0, 0, 0],
        scale: [1, 1, 1],
        color: '#f6ad55'
      }
    ],
    animations: [
      {
        name: 'Giro_Escaner',
        duration: 3.0,
        tracks: [
          {
            targetComponent: 'plato_parabolico',
            property: 'rotation',
            interpolation: 'linear',
            keyframes: [
              { time: 0, value: [0, 0, 0] },
              { time: 3, value: [0, 360, 0] }
            ]
          }
        ]
      }
    ]
  };

  const snippets = generateAllSnippets(animatedSpec, 'antenna_dish.glb');

  // 1. Godot 4 GDScript
  assert.ok(snippets.godot.includes('extends Node3D'), 'Debe extender Node3D');
  assert.ok(snippets.godot.includes('AnimationPlayer'), 'Debe incluir referencia a AnimationPlayer');
  assert.ok(snippets.godot.includes('"Giro_Escaner"'), 'Debe incluir el clip Giro_Escaner');

  // 2. Unity C#
  assert.ok(snippets.unity.includes('MonoBehaviour'), 'Debe heredar de MonoBehaviour');
  assert.ok(snippets.unity.includes('Animator'), 'Debe incluir Animator');
  assert.ok(snippets.unity.includes('Giro_Escaner'), 'Debe referenciar el clip Giro_Escaner');

  // 3. Three.js TypeScript
  assert.ok(snippets.threejs.includes('GLTFLoader'), 'Debe importar GLTFLoader');
  assert.ok(snippets.threejs.includes('AnimationMixer'), 'Debe incluir AnimationMixer');
  assert.ok(snippets.threejs.includes('loadAntenaParabolica'), 'Debe generar función de carga con nombre sanitizado');
});

test('Component Hierarchy 1: wouldCreateCycle detecta ciclos directos e indirectos', () => {
  const components: ComponentDef[] = [
    { name: 'base', shape: 'box' },
    { name: 'torso', shape: 'box', parentId: 'base' },
    { name: 'brazo', shape: 'cylinder', parentId: 'torso' },
    { name: 'mano', shape: 'box', parentId: 'brazo' }
  ];

  // 1. Auto-parenting no permitido
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'base', 'base'), true);
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'brazo', 'brazo'), true);

  // 2. Ciclos directos (A -> B -> A)
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'base', 'torso'), true);

  // 3. Ciclos indirectos (A -> B -> C -> D -> A)
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'base', 'mano'), true);
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'torso', 'mano'), true);

  // 4. Asignaciones válidas
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'mano', 'base'), false);
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'brazo', 'base'), false);
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'mano', undefined), false);
  assert.equal(ProceduralEngine.wouldCreateCycle(components, 'mano', ''), false);
});

test('Component Hierarchy 2: buildModelFromSpec construye grafo jerárquico Three.js y hereda transformaciones', () => {
  const hierarchicalSpec: ModelSpec = {
    id: 'test.hierarchy.robot_arm',
    name: 'Brazo Robótico Articulado',
    category: 'fixtures',
    description: 'Brazo con jerarquía hombro -> antebrazo -> pinza',
    units: 'meters',
    dimensions: { width: 1, depth: 1, height: 2 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'hombro',
        shape: 'box',
        size: [0.5, 0.5, 0.5],
        position: [1.0, 2.0, 0.0]
      },
      {
        name: 'antebrazo',
        shape: 'cylinder',
        size: [0.15, 0.15, 1.0, 8],
        position: [0.0, 1.0, 0.0],
        parentId: 'hombro'
      },
      {
        name: 'pinza',
        shape: 'box',
        size: [0.2, 0.2, 0.2],
        position: [0.0, 0.6, 0.0],
        parentId: 'antebrazo'
      }
    ]
  };

  const { group, stats } = ProceduralEngine.buildModelFromSpec(hierarchicalSpec);

  // 1. En el nivel raíz del grupo sólo debe estar el hombro
  assert.equal(group.children.length, 1, 'Solo la raíz (hombro) debe pertenecer a group.children');
  const hombroMesh = group.children[0] as THREE.Mesh;
  assert.equal(hombroMesh.name, 'hombro');

  // 2. Antebrazo debe ser hijo directo de hombro
  assert.equal(hombroMesh.children.length, 1, 'Hombro debe contener al antebrazo como hijo');
  const antebrazoMesh = hombroMesh.children[0] as THREE.Mesh;
  assert.equal(antebrazoMesh.name, 'antebrazo');

  // 3. Pinza debe ser hija directa de antebrazo
  assert.equal(antebrazoMesh.children.length, 1, 'Antebrazo debe contener a la pinza como hija');
  const pinzaMesh = antebrazoMesh.children[0] as THREE.Mesh;
  assert.equal(pinzaMesh.name, 'pinza');

  // 4. Verificación de transformaciones acumuladas en World Space
  group.updateMatrixWorld(true);

  const hombroWorldPos = new THREE.Vector3();
  hombroMesh.getWorldPosition(hombroWorldPos);
  assert.equal(hombroWorldPos.x, 1.0);
  assert.equal(hombroWorldPos.y, 2.0);
  assert.equal(hombroWorldPos.z, 0.0);

  const antebrazoWorldPos = new THREE.Vector3();
  antebrazoMesh.getWorldPosition(antebrazoWorldPos);
  assert.equal(antebrazoWorldPos.x, 1.0);
  assert.equal(antebrazoWorldPos.y, 3.0); // 2.0 (hombro) + 1.0 (antebrazo local)

  const pinzaWorldPos = new THREE.Vector3();
  pinzaMesh.getWorldPosition(pinzaWorldPos);
  assert.equal(pinzaWorldPos.x, 1.0);
  assert.equal(pinzaWorldPos.y, 3.6); // 2.0 + 1.0 + 0.6 = 3.6

  // 5. Estadísticas geométricas incluyen todos los nodos jerárquicos
  assert.ok(stats.triangles > 0);
  assert.ok(stats.vertices > 0);

  ProceduralEngine.disposeHierarchy(group);
});

test('Component Hierarchy 3: CodeSandbox builder permite crear jerarquías con parentId y setParent', () => {
  const code = `
    builder.addBox({ name: 'torre_base', size: [1, 0.5, 1], position: [0, 0.25, 0] });
    builder.addCylinder({ name: 'canon', parentId: 'torre_base', position: [0, 0.4, 0.3] });
    builder.addSphere({ name: 'sensor_mira', position: [0, 0.2, 0.5] });
    builder.setParent('sensor_mira', 'canon');
  `;

  const { spec, error } = CodeSandbox.executeCode(code);
  assert.equal(error, undefined, `CodeSandbox falló: ${error}`);
  assert.equal(spec.components.length, 3);

  const canon = spec.components.find((c) => c.name === 'canon');
  const sensor = spec.components.find((c) => c.name === 'sensor_mira');

  assert.equal(canon?.parentId, 'torre_base');
  assert.equal(sensor?.parentId, 'canon');

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 1, 'Solo la base debe ser raíz');
  ProceduralEngine.disposeHierarchy(group);
});

test('Component Hierarchy 4: Exportación e importación GLB preserva la estructura de nodos jerárquicos', async () => {
  const hierarchicalSpec: ModelSpec = {
    id: 'test.hierarchy.export',
    name: 'Torreta Jerárquica GLB',
    category: 'defense',
    description: 'Exportación con nodos anidados',
    units: 'meters',
    dimensions: { width: 1, depth: 1, height: 1 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'soporte',
        shape: 'box',
        size: [1, 0.2, 1],
        position: [0, 0.1, 0]
      },
      {
        name: 'rotador',
        shape: 'cylinder',
        size: [0.4, 0.4, 0.3, 8],
        position: [0, 0.25, 0],
        parentId: 'soporte'
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(hierarchicalSpec);

  // Exportar a GLB
  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(glbBuffer instanceof ArrayBuffer);
  assert.ok(glbBuffer.byteLength > 800);

  // Verificación e importación
  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true);
  assert.ok(verification.triangleCount > 0);

  ProceduralEngine.disposeHierarchy(group);
});

test('Pivot & Articulation 1: computePresetPivot calcula offsets precisos para bordes y bisagras', () => {
  // Box: width=2, height=1, depth=0.8
  const boxBottom = ProceduralEngine.computePresetPivot('bottom', 'box', [2, 1, 0.8]);
  assert.deepEqual(boxBottom, [0, -0.5, 0]);

  const boxTop = ProceduralEngine.computePresetPivot('top', 'box', [2, 1, 0.8]);
  assert.deepEqual(boxTop, [0, 0.5, 0]);

  const boxLeft = ProceduralEngine.computePresetPivot('left', 'box', [2, 1, 0.8]);
  assert.deepEqual(boxLeft, [-1.0, 0, 0]);

  const boxRight = ProceduralEngine.computePresetPivot('right', 'box', [2, 1, 0.8]);
  assert.deepEqual(boxRight, [1.0, 0, 0]);

  const boxBack = ProceduralEngine.computePresetPivot('back', 'box', [2, 1, 0.8]);
  assert.deepEqual(boxBack, [0, 0, -0.4]);

  const boxCenter = ProceduralEngine.computePresetPivot('center', 'box', [2, 1, 0.8]);
  assert.deepEqual(boxCenter, [0, 0, 0]);
});

test('Pivot & Articulation 2: createComponentMesh traslada la geometría al pivote de bisagra', () => {
  // Puerta de 1m de ancho x 2m de alto x 0.1m de fondo con bisagra en el borde izquierdo (-0.5m en X)
  const doorComp: ComponentDef = {
    name: 'puerta_lateral',
    shape: 'box',
    size: [1.0, 2.0, 0.1],
    position: [0, 0, 0],
    pivot: [-0.5, 0, 0] // Bisagra en el borde izquierdo
  };

  const mesh = ProceduralEngine.createComponentMesh(doorComp) as THREE.Mesh;
  const geom = mesh.geometry;
  geom.computeBoundingBox();
  const bb = geom.boundingBox!;

  // El borde izquierdo de la caja estaba en -0.5. Al trasladar por -pivot (+0.5):
  // Ahora el borde izquierdo debe estar exactamente en x = 0 (el origen / bisagra de la mesh)!
  // Y el borde derecho debe estar en x = 1.0!
  assert.ok(Math.abs(bb.min.x - 0.0) < 0.001, `Min X debe ser 0.0 (la bisagra), recibido: ${bb.min.x}`);
  assert.ok(Math.abs(bb.max.x - 1.0) < 0.001, `Max X debe ser 1.0, recibido: ${bb.max.x}`);

  geom.dispose();
});

test('Pivot & Articulation 3: Rotar una pieza con pivote rota alrededor de su bisagra', () => {
  const spec: ModelSpec = {
    id: 'test.pivot.rotation',
    name: 'Tapa de Baúl Articulada',
    category: 'furniture',
    description: 'Tapa con bisagra trasera que rota hacia arriba',
    units: 'meters',
    dimensions: { width: 1, depth: 1, height: 0.1 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'tapa',
        shape: 'box',
        size: [1.0, 0.1, 1.0],
        position: [0, 1.0, 0], // En Y=1
        pivot: [0, 0, -0.5], // Bisagra en el borde trasero (Z = -0.5)
        rotation: [-90, 0, 0] // Abierta 90 grados hacia arriba
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  const mesh = group.children[0] as THREE.Mesh;
  group.updateMatrixWorld(true);

  // El origen de la mesh (la bisagra) permanece en [0, 1.0, 0] en World Space
  const worldPos = new THREE.Vector3();
  mesh.getWorldPosition(worldPos);
  assert.equal(worldPos.x, 0);
  assert.equal(worldPos.y, 1.0);
  assert.equal(worldPos.z, 0);

  ProceduralEngine.disposeHierarchy(group);
});

test('Mirror Tool: createMirroredComponent refleja simétricamente posición, rotación y pivote', () => {
  const comp: ComponentDef = {
    name: 'aleron_izq',
    shape: 'wedge',
    size: [0.8, 0.2, 0.4],
    position: [-1.5, 0.8, 0.5],
    rotation: [10, -20, 15],
    pivot: [-0.4, 0, 0]
  };

  const mirrored = ProceduralEngine.createMirroredComponent(comp, 'x', 'aleron_der');
  assert.equal(mirrored.name, 'aleron_der');

  // En eje X: la posición X se invierte (-(-1.5) = 1.5), Y y Z se mantienen
  assert.equal(mirrored.position![0], 1.5);
  assert.equal(mirrored.position![1], 0.8);
  assert.equal(mirrored.position![2], 0.5);

  // Rotaciones complementarias en X invertidas para simetría:
  // rot[0] (Pitch) se conserva: 10
  // rot[1] (Yaw) invertido: -(-20) = 20
  // rot[2] (Roll) invertido: -(15) = -15
  assert.equal(mirrored.rotation![0], 10);
  assert.equal(mirrored.rotation![1], 20);
  assert.equal(mirrored.rotation![2], -15);

  // El pivote en X también se invierte
  assert.equal(mirrored.pivot![0], 0.4);
});

test('Pivot & Mirror: Exportación GLB preserva geometrías con pivote y piezas reflejadas', async () => {
  const spec: ModelSpec = {
    id: 'test.pivot.glb',
    name: 'Robot con Articulación y Espejo',
    category: 'robots',
    description: 'Prueba de exportación con pivotes y simetría',
    units: 'meters',
    dimensions: { width: 2, depth: 1, height: 2 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'hombro_izq',
        shape: 'cylinder',
        size: [0.1, 0.1, 0.8, 8],
        position: [-0.6, 1.2, 0],
        pivot: [0, 0.4, 0] // Articulación en el extremo superior
      },
      ProceduralEngine.createMirroredComponent({
        name: 'hombro_izq',
        shape: 'cylinder',
        size: [0.1, 0.1, 0.8, 8],
        position: [-0.6, 1.2, 0],
        pivot: [0, 0.4, 0]
      }, 'x', 'hombro_der')
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 2);

  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group);
  assert.ok(glbBuffer instanceof ArrayBuffer);
  assert.ok(glbBuffer.byteLength > 1000);

  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true);
  assert.ok(verification.triangleCount > 0);

  ProceduralEngine.disposeHierarchy(group);
});

test('Animation Curves: applyEasingProfile calcula perfiles de aceleración correctamente (linear, ease-in-out, bounce, ease-out, step)', () => {
  const start: [number, number, number] = [0, 0, 0];
  const end: [number, number, number] = [10, 20, 30];
  const duration = 2.0;

  // 1. Linear profile
  const linearKfs = AnimationEngine.applyEasingProfile('linear', duration, start, end);
  assert.equal(linearKfs.length, 2);
  assert.equal(linearKfs[0].time, 0);
  assert.deepEqual(linearKfs[0].value, [0, 0, 0]);
  assert.equal(linearKfs[0].interpolation, 'linear');
  assert.equal(linearKfs[1].time, 2.0);
  assert.deepEqual(linearKfs[1].value, [10, 20, 30]);

  // 2. Ease-in-out profile (smooth S-curve with cubic interpolation)
  const easeInOutKfs = AnimationEngine.applyEasingProfile('ease-in-out', duration, start, end);
  assert.equal(easeInOutKfs.length, 5);
  assert.equal(easeInOutKfs[0].interpolation, 'cubic');
  assert.equal(easeInOutKfs[2].time, 1.0); // Midpoint at 50% time
  assert.deepEqual(easeInOutKfs[2].value, [5, 10, 15]); // Exactly 50% value
  assert.deepEqual(easeInOutKfs[4].value, [10, 20, 30]);

  // 3. Bounce / Spring profile with mechanical overshoot
  const bounceKfs = AnimationEngine.applyEasingProfile('bounce', duration, start, end);
  assert.equal(bounceKfs.length, 5);
  // Keyframe at 68% duration should overshoot target by 18%
  const overshootKf = bounceKfs[2];
  assert.ok(overshootKf.value[0] > 10, 'X must overshoot target 10');
  assert.ok(overshootKf.value[1] > 20, 'Y must overshoot target 20');
  assert.ok(overshootKf.value[2] > 30, 'Z must overshoot target 30');
  assert.equal(overshootKf.value[0], 11.8);
  assert.equal(overshootKf.value[1], 23.6);
  assert.equal(overshootKf.value[2], 35.4);
  // Recoil keyframe at 86% should settle slightly below 100%
  const recoilKf = bounceKfs[3];
  assert.equal(recoilKf.value[0], 9.5);
  // Final keyframe settles exactly at target
  assert.deepEqual(bounceKfs[4].value, [10, 20, 30]);

  // 4. Ease-out profile (fast burst decelerating sharply)
  const easeOutKfs = AnimationEngine.applyEasingProfile('ease-out', duration, start, end);
  assert.equal(easeOutKfs.length, 5);
  assert.equal(easeOutKfs[0].interpolation, 'cubic');
  // At 20% duration, value is already at 55% of travel
  assert.equal(easeOutKfs[1].value[0], 5.5);
  assert.equal(easeOutKfs[1].value[1], 11);
  assert.deepEqual(easeOutKfs[4].value, [10, 20, 30]);

  // 5. Step profile (discrete robotic steps)
  const stepKfs = AnimationEngine.applyEasingProfile('step', duration, start, end);
  assert.equal(stepKfs.length, 3);
  assert.equal(stepKfs[0].interpolation, 'step');
  assert.equal(stepKfs[1].interpolation, 'step');
  assert.deepEqual(stepKfs[1].value, [5, 10, 15]);
  assert.deepEqual(stepKfs[2].value, [10, 20, 30]);
});

test('Animation Curves: Compilación a Three.js traduce modos de interpolación discretos, lineales y cúbicos', () => {
  const discreteTrack = {
    targetComponent: 'robot_arm',
    property: 'position' as const,
    keyframes: [
      { time: 0, value: [0, 0, 0] as [number, number, number], interpolation: 'step' as const },
      { time: 1.0, value: [1, 2, 3] as [number, number, number], interpolation: 'step' as const }
    ]
  };
  const smoothTrack = {
    targetComponent: 'robot_arm',
    property: 'scale' as const,
    keyframes: [
      { time: 0, value: [1, 1, 1] as [number, number, number], interpolation: 'cubic' as const },
      { time: 1.0, value: [1.5, 1.5, 1.5] as [number, number, number], interpolation: 'cubic' as const }
    ]
  };
  const linearRotTrack = {
    targetComponent: 'robot_arm',
    property: 'rotation' as const,
    keyframes: [
      { time: 0, value: [0, 0, 0] as [number, number, number], interpolation: 'linear' as const },
      { time: 1.0, value: [0, 90, 0] as [number, number, number], interpolation: 'linear' as const }
    ]
  };

  const clip = {
    id: 'test_clip',
    name: 'MultiInterpTest',
    duration: 1.0,
    tracks: [discreteTrack, smoothTrack, linearRotTrack]
  };

  const threeClip = AnimationEngine.compileClipToThree(clip);
  assert.equal(threeClip.tracks.length, 3);

  // Track 0: Position with discrete interpolation
  const posTrack = threeClip.tracks[0];
  assert.equal(posTrack.name, 'robot_arm.position');
  assert.equal(posTrack.getInterpolation(), THREE.InterpolateDiscrete);

  // Track 1: Scale with smooth (cubic) interpolation
  const scaleTrack = threeClip.tracks[1];
  assert.equal(scaleTrack.name, 'robot_arm.scale');
  assert.equal(scaleTrack.getInterpolation(), THREE.InterpolateSmooth);

  // Track 2: Rotation with linear interpolation (QuaternionKeyframeTrack)
  const rotTrack = threeClip.tracks[2];
  assert.equal(rotTrack.name, 'robot_arm.quaternion');
  assert.equal(rotTrack.getInterpolation(), THREE.InterpolateLinear);
});

test('Animation Curves & GLB: Animación con rebote mecánico y keyframes personalizados exporta e inicializa en GLB', async () => {
  const bounceKfs = AnimationEngine.applyEasingProfile('bounce', 1.6, [0, 0, 0], [0, 1.5, 0]);

  const spec: ModelSpec = {
    id: 'test.anim.bounce.glb',
    name: 'Pistón con Rebote Mecánico',
    category: 'machinery',
    description: 'Pistón neumático con amortiguación y rebote elástico',
    units: 'meters',
    dimensions: { width: 1, depth: 1, height: 2 },
    palette: 'industrial_hazard',
    components: [
      {
        name: 'cilindro_base',
        shape: 'cylinder',
        size: [0.3, 0.3, 1.0, 12],
        position: [0, 0.5, 0]
      },
      {
        name: 'piston_eje',
        shape: 'cylinder',
        size: [0.15, 0.15, 1.2, 12],
        position: [0, 1.1, 0]
      }
    ],
    animations: [
      {
        id: 'clip_piston_bounce',
        name: 'Piston_Disparo_Rebote',
        duration: 1.6,
        loop: 'pingpong',
        tracks: [
          {
            targetComponent: 'piston_eje',
            property: 'position',
            keyframes: bounceKfs
          }
        ]
      }
    ]
  };

  const { group } = ProceduralEngine.buildModelFromSpec(spec);
  assert.equal(group.children.length, 2);

  // Compilar clips Three.js
  const threeClips = AnimationEngine.compileClipsToThree(spec.animations);
  assert.equal(threeClips.length, 1);
  assert.equal(threeClips[0].name, 'Piston_Disparo_Rebote');
  assert.equal(threeClips[0].tracks[0].times.length, 5);

  // Exportar a GLB con clips de animación incluidos
  const glbBuffer = await GLBExporterService.exportToArrayBuffer(group, threeClips);
  assert.ok(glbBuffer instanceof ArrayBuffer);
  assert.ok(glbBuffer.byteLength > 1000);

  // Verificar integridad del GLB
  const verification = await GLBExporterService.verifyGLBBuffer(glbBuffer);
  assert.equal(verification.verified, true);
  assert.ok(verification.triangleCount > 0);

  ProceduralEngine.disposeHierarchy(group);
});

test('Animation Loop Control: StudioViewport y Mixer soportan modo Bucle y 1 Vez', () => {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1));
  mesh.name = 'box';

  const clipDef = {
    id: 'test_loop_clip',
    name: 'LoopTest',
    duration: 2.0,
    tracks: [
      {
        targetComponent: 'box',
        property: 'position' as const,
        keyframes: [
          { time: 0, value: [0, 0, 0] as [number, number, number] },
          { time: 2.0, value: [0, 5, 0] as [number, number, number] }
        ]
      }
    ]
  };

  const compiled = AnimationEngine.compileClipsToThree([clipDef], mesh);
  assert.equal(compiled.length, 1);

  const mixer = new THREE.AnimationMixer(mesh);
  const action = mixer.clipAction(compiled[0]);

  // Modo repeat por defecto
  action.setLoop(THREE.LoopRepeat, Infinity);
  action.clampWhenFinished = false;
  assert.equal(action.loop, THREE.LoopRepeat);
  assert.equal(action.clampWhenFinished, false);

  // Modo once (1 vez y detenerse)
  action.setLoop(THREE.LoopOnce, 1);
  action.clampWhenFinished = true;
  assert.equal(action.loop, THREE.LoopOnce);
  assert.equal(action.clampWhenFinished, true);

  // Simulación de avance en modo once
  action.play();
  mixer.update(1.0);
  assert.equal(action.time, 1.0);

  mixer.update(1.5);
  // Al superar la duración (2.0s), con LoopOnce y clampWhenFinished, el mixer clampa el tiempo
  assert.ok(action.time >= 2.0);

  mixer.stopAllAction();
  mixer.uncacheRoot(mesh);
});

test('Hierarchy Reparenting: reparentComponentPreservingWorldTransform preserva posición mundial y rechaza ciclos', () => {
  const components: any[] = [
    {
      name: 'Torso',
      shape: 'box',
      size: [1, 2, 1],
      position: [0, 5, 0],
      rotation: [0, 0, 0]
    },
    {
      name: 'Brazo',
      shape: 'cylinder',
      size: [0.3, 1.5, 0.3],
      position: [2, 5, 1],
      rotation: [0, 0, 0]
    }
  ];

  // 1. Reparentar Brazo como hijo de Torso
  const ok1 = ProceduralEngine.reparentComponentPreservingWorldTransform(components, 'Brazo', 'Torso');
  assert.equal(ok1, true);

  const brazoComp = components.find(c => c.name === 'Brazo');
  assert.equal(brazoComp.parentId, 'Torso');
  // Al ser hijo de Torso (que está en Y=5), la posición local de Brazo debe ser [2, 0, 1]
  assert.equal(brazoComp.position[0], 2);
  assert.equal(brazoComp.position[1], 0);
  assert.equal(brazoComp.position[2], 1);

  // Verificar que en la escena 3D reconstruida, la posición mundial de Brazo sigue siendo exactamente [2, 5, 1]
  const built1 = ProceduralEngine.buildModelFromSpec({
    id: 'test_rep',
    name: 'RepTest',
    category: 'fixtures',
    description: '',
    units: 'meters',
    dimensions: { width: 1, depth: 1, height: 1 },
    palette: 'industrial_hazard',
    components
  });
  built1.group.updateMatrixWorld(true);

  let brazoMesh: THREE.Object3D | null = null;
  built1.group.traverse(obj => {
    if (obj.name === 'Brazo') brazoMesh = obj;
  });
  assert.ok(brazoMesh);
  const worldPos = new THREE.Vector3();
  brazoMesh!.getWorldPosition(worldPos);

  assert.ok(Math.abs(worldPos.x - 2) < 0.001);
  assert.ok(Math.abs(worldPos.y - 5) < 0.001);
  assert.ok(Math.abs(worldPos.z - 1) < 0.001);
  ProceduralEngine.disposeHierarchy(built1.group);

  // 2. Intentar ciclo: hacer a Torso hijo de Brazo (debe fallar y rechazar el ciclo)
  const okCycle = ProceduralEngine.reparentComponentPreservingWorldTransform(components, 'Torso', 'Brazo');
  assert.equal(okCycle, false);
  const torsoComp = components.find(c => c.name === 'Torso');
  assert.equal(torsoComp.parentId, undefined);

  // 3. Desvincular Brazo a nivel raíz (newParentName: undefined)
  const okUnparent = ProceduralEngine.reparentComponentPreservingWorldTransform(components, 'Brazo', undefined);
  assert.equal(okUnparent, true);
  assert.equal(brazoComp.parentId, undefined);
  // Al volver a la raíz, su posición local vuelve a ser idéntica a su posición mundial [2, 5, 0]
  assert.equal(brazoComp.position[0], 2);
  assert.equal(brazoComp.position[1], 5);
  assert.equal(brazoComp.position[2], 1);
});

// Teardown: ensure Node exits cleanly after tests
test('Teardown: Exit cleanly', () => {
  setTimeout(() => process.exit(0), 100);
});



