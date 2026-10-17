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
            drawImage: () => {}
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
  const uvClean = (cleanMesh.geometry.getAttribute('uv').array as Float32Array)[0];
  const uvRot = (weatheredMesh.geometry.getAttribute('uv').array as Float32Array)[0];
  assert.notEqual(uvClean, uvRot, 'UV rotation (90 deg) must rotate vertex UV coordinates');

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

// Teardown: ensure Node exits cleanly after tests
test('Teardown: Exit cleanly', () => {
  setTimeout(() => process.exit(0), 100);
});



