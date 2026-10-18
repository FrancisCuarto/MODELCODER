/**
 * Tools script to embed standard animation tracks into key public catalog GLBs.
 * Run with: node tools/embed_catalog_animations.js
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Node.js test environment polyfills for THREE.GLTFExporter & ImageData
if (typeof globalThis.self === 'undefined') {
  globalThis.self = globalThis;
}
if (typeof globalThis.ImageData === 'undefined') {
  globalThis.ImageData = class NodeImageData {
    constructor(data, width, height) {
      this.data = data;
      this.width = width;
      this.height = height;
    }
  };
}
if (typeof globalThis.document === 'undefined') {
  globalThis.document = {
    createElement: (tag) => {
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
            closePath: () => {},
            fill: () => {},
            stroke: () => {},
            fillRect: () => {},
            clearRect: () => {},
            fillText: () => {},
            measureText: (text) => ({ width: (text || '').length * 10 }),
            createLinearGradient: () => ({ addColorStop: () => {} }),
            createRadialGradient: () => ({ addColorStop: () => {} })
          }),
          toDataURL: () => 'data:image/png;base64,mock',
          toBlob: (cb, type) => {
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
    constructor() {
      this.onload = null;
      this.onloadend = null;
      this.onerror = null;
      this.result = null;
    }
    readAsArrayBuffer(blob) {
      blob.arrayBuffer().then((buf) => {
        this.result = buf;
        if (this.onload) this.onload({ target: this });
        if (this.onloadend) this.onloadend({ target: this });
      }).catch((err) => {
        if (this.onerror) this.onerror(err);
      });
    }
    readAsDataURL(blob) {
      blob.arrayBuffer().then((buf) => {
        const base64 = Buffer.from(buf).toString('base64');
        this.result = `data:${blob.type || 'application/octet-stream'};base64,${base64}`;
        if (this.onload) this.onload({ target: this });
        if (this.onloadend) this.onloadend({ target: this });
      }).catch((err) => {
        if (this.onerror) this.onerror(err);
      });
    }
  }
  globalThis.FileReader = NodeFileReader;
}

import * as THREE from '../web/node_modules/three/build/three.module.js';
import { GLTFLoader } from '../web/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import { GLTFExporter } from '../web/node_modules/three/examples/jsm/exporters/GLTFExporter.js';

const MODELS_DIR = path.resolve(__dirname, '../web/public/models');

/**
 * Creates a continuous 360 degree rotation track
 */
function createSpinTrack(targetName, duration, axis = 'y') {
  const times = [0, duration / 3, (duration * 2) / 3, duration];
  const quatValues = [];
  const euler = new THREE.Euler();
  const quat = new THREE.Quaternion();

  [0, 120, 240, 360].forEach((deg) => {
    const rx = axis === 'x' ? THREE.MathUtils.degToRad(deg) : 0;
    const ry = axis === 'y' ? THREE.MathUtils.degToRad(deg) : 0;
    const rz = axis === 'z' ? THREE.MathUtils.degToRad(deg) : 0;
    euler.set(rx, ry, rz, 'XYZ');
    quat.setFromEuler(euler);
    quatValues.push(quat.x, quat.y, quat.z, quat.w);
  });

  return new THREE.QuaternionKeyframeTrack(`${targetName}.quaternion`, times, quatValues);
}

/**
 * Creates an oscillating pan (sweep) rotation track
 */
function createPanTrack(targetName, duration, minDeg = -45, maxDeg = 45, axis = 'y') {
  const times = [0, duration * 0.25, duration * 0.5, duration * 0.75, duration];
  const quatValues = [];
  const euler = new THREE.Euler();
  const quat = new THREE.Quaternion();

  [0, maxDeg, 0, minDeg, 0].forEach((deg) => {
    const rx = axis === 'x' ? THREE.MathUtils.degToRad(deg) : 0;
    const ry = axis === 'y' ? THREE.MathUtils.degToRad(deg) : 0;
    const rz = axis === 'z' ? THREE.MathUtils.degToRad(deg) : 0;
    euler.set(rx, ry, rz, 'XYZ');
    quat.setFromEuler(euler);
    quatValues.push(quat.x, quat.y, quat.z, quat.w);
  });

  return new THREE.QuaternionKeyframeTrack(`${targetName}.quaternion`, times, quatValues);
}

/**
 * Creates a sliding door track (translation)
 */
function createSlideTrack(targetName, duration, distance = 2.0, axis = 'y') {
  const times = [0, duration * 0.45, duration * 0.55, duration];
  const values = [];
  const p0 = [0, 0, 0];
  const pOpen = [0, 0, 0];
  const axisIdx = axis === 'x' ? 0 : axis === 'y' ? 1 : 2;
  pOpen[axisIdx] = distance;

  values.push(...p0, ...pOpen, ...pOpen, ...p0);
  return new THREE.VectorKeyframeTrack(`${targetName}.position`, times, values);
}

/**
 * Creates a hinge open track (angular rotation)
 */
function createHingeTrack(targetName, duration, angleDeg = 85, axis = 'x') {
  const times = [0, duration * 0.45, duration * 0.55, duration];
  const quatValues = [];
  const euler = new THREE.Euler();
  const quat = new THREE.Quaternion();

  [0, angleDeg, angleDeg, 0].forEach((deg) => {
    const rx = axis === 'x' ? THREE.MathUtils.degToRad(deg) : 0;
    const ry = axis === 'y' ? THREE.MathUtils.degToRad(deg) : 0;
    const rz = axis === 'z' ? THREE.MathUtils.degToRad(deg) : 0;
    euler.set(rx, ry, rz, 'XYZ');
    quat.setFromEuler(euler);
    quatValues.push(quat.x, quat.y, quat.z, quat.w);
  });

  return new THREE.QuaternionKeyframeTrack(`${targetName}.quaternion`, times, quatValues);
}

const CATALOG_ANIMATIONS = [
  {
    file: 'antenna_dish.glb',
    targetName: 'antenna_dish',
    clipName: 'Giro_Escaner',
    duration: 3.2,
    builder: (target, dur) => [createSpinTrack(target, dur, 'y')]
  },
  {
    file: 'alarm_siren.glb',
    targetName: 'alarm_siren',
    clipName: 'Baliza_Giro',
    duration: 1.2,
    builder: (target, dur) => [createSpinTrack(target, dur, 'y')]
  },
  {
    file: 'security_camera.glb',
    targetName: 'security_camera',
    clipName: 'Vigilancia_Pan',
    duration: 4.0,
    builder: (target, dur) => [createPanTrack(target, dur, -50, 50, 'y')]
  },
  {
    file: 'door.glb',
    targetName: 'airlock_door',
    clipName: 'Abrir_Puerta',
    duration: 2.6,
    builder: (target, dur) => [createSlideTrack(target, dur, 2.0, 'y')]
  },
  {
    file: 'maintenance_hatch.glb',
    targetName: 'maintenance_hatch',
    clipName: 'Abrir_Escotilla',
    duration: 2.2,
    builder: (target, dur) => [createHingeTrack(target, dur, 85, 'x')]
  },
  {
    file: 'crate.glb',
    targetName: 'crate',
    clipName: 'Inspeccion_Flotante',
    duration: 2.8,
    builder: (target, dur) => {
      const times = [0, dur * 0.25, dur * 0.5, dur * 0.75, dur];
      const values = [
        0, 0, 0,
        0, 0.12, 0,
        0, 0, 0,
        0, -0.12, 0,
        0, 0, 0
      ];
      return [new THREE.VectorKeyframeTrack(`${target}.position`, times, values)];
    }
  }
];

async function processModel(animDef) {
  const filePath = path.join(MODELS_DIR, animDef.file);
  if (!fs.existsSync(filePath)) {
    console.warn(`[Skip] Model not found: ${filePath}`);
    return;
  }

  const rawBuf = fs.readFileSync(filePath);
  const arrayBuf = rawBuf.buffer.slice(rawBuf.byteOffset, rawBuf.byteOffset + rawBuf.byteLength);

  const loader = new GLTFLoader();
  const gltf = await loader.parseAsync(arrayBuf, '');

  const tracks = animDef.builder(animDef.targetName, animDef.duration);
  const clip = new THREE.AnimationClip(animDef.clipName, animDef.duration, tracks);

  const exporter = new GLTFExporter();
  const glbBuffer = await new Promise((resolve, reject) => {
    exporter.parse(
      gltf.scene,
      (res) => resolve(res),
      (err) => reject(err),
      { binary: true, animations: [clip] }
    );
  });

  fs.writeFileSync(filePath, Buffer.from(glbBuffer));

  // Verification step
  const verifyLoader = new GLTFLoader();
  const verifyGltf = await verifyLoader.parseAsync(glbBuffer, '');
  const animNames = verifyGltf.animations.map((a) => a.name);

  console.log(`✅ ${animDef.file} -> Animación añadida: [${animNames.join(', ')}] (${glbBuffer.byteLength} bytes)`);
}

async function main() {
  console.log('=== Incrustando animaciones cinemáticas en modelos del catálogo ===\n');
  for (const item of CATALOG_ANIMATIONS) {
    try {
      await processModel(item);
    } catch (err) {
      console.error(`❌ Error al procesar ${item.file}:`, err);
    }
  }
  console.log('\n=== Proceso completado exitosamente ===');
}

main();
