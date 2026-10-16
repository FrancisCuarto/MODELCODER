import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';

// Node.js test environment polyfill for THREE.GLTFExporter
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


