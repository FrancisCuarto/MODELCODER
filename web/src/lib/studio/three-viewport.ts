import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { ProceduralEngine } from './procedural-engine';
import type { ShadingMode, GenerationState, GeometricStats, GenerationResult } from './types';

export class StudioViewport {
  private container: HTMLElement;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;
  private gridHelper: THREE.GridHelper;
  private dirLight: THREE.DirectionalLight;
  private ambientLight: THREE.AmbientLight;

  private currentMesh: THREE.Object3D | null = null;
  private lastValidMesh: THREE.Object3D | null = null;
  private activeShadingMode: ShadingMode = 'shaded';
  private currentShadingMaterialsBackup: Map<THREE.Mesh, THREE.Material | THREE.Material[]> = new Map();

  // Concurrency and generation tracking
  private activeRequestId = '';
  private activeVersion = 0;
  private currentState: GenerationState = 'idle';

  // HUD Callback
  private onStatsUpdate?: (stats: GeometricStats | null, result: GenerationResult | null) => void;

  constructor(
    container: HTMLElement,
    onStatsUpdate?: (stats: GeometricStats | null, result: GenerationResult | null) => void
  ) {
    this.container = container;
    this.onStatsUpdate = onStatsUpdate;

    // 1. Scene setup
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0d14);

    // 2. Camera setup
    const aspect = container.clientWidth / (container.clientHeight || 1);
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.05, 100);
    this.camera.position.set(2.2, 1.8, 2.8);

    // 3. Renderer setup
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: true
    });
    this.renderer.setSize(container.clientWidth, container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Clear previous children in container and append renderer canvas
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    container.appendChild(this.renderer.domElement);

    // 4. Controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.maxDistance = 25;
    this.controls.minDistance = 0.2;
    this.controls.target.set(0, 0.4, 0);

    // 5. Lighting
    this.ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    this.scene.add(this.ambientLight);

    this.dirLight = new THREE.DirectionalLight(0xfff8ee, 1.4);
    this.dirLight.position.set(5, 8, 4);
    this.dirLight.castShadow = true;
    this.dirLight.shadow.mapSize.width = 1024;
    this.dirLight.shadow.mapSize.height = 1024;
    this.scene.add(this.dirLight);

    const fillLight = new THREE.DirectionalLight(0x63b3ed, 0.4);
    fillLight.position.set(-5, -2, -4);
    this.scene.add(fillLight);

    // 6. Retro Ground Grid
    this.gridHelper = new THREE.GridHelper(6, 24, 0x00f0ff, 0x1f2937);
    this.gridHelper.position.y = -0.001;
    this.scene.add(this.gridHelper);

    // 7. Event listeners & Render loop
    window.addEventListener('resize', this.handleResize);
    this.animate();
  }

  private handleResize = (): void => {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    if (width === 0 || height === 0) return;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  };

  private animate = (): void => {
    requestAnimationFrame(this.animate);
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  };

  /**
   * Updates the viewport with a genuine new generated 3D object.
   * Disposes previous geometry cleanly and guards against stale race conditions.
   */
  public displayGeneratedMesh(
    obj: THREE.Object3D,
    reqId: string,
    version: number,
    stats: GeometricStats,
    mode: 'ai' | 'visual' | 'code'
  ): void {
    // Guard against older out-of-order responses overwriting newer generations
    if (this.activeVersion > version) {
      console.warn(`[StudioViewport] Descartada generación tardía (v${version} vs actual v${this.activeVersion})`);
      ProceduralEngine.disposeHierarchy(obj);
      return;
    }

    this.activeRequestId = reqId;
    this.activeVersion = version;
    this.currentState = 'completed';

    // Dispose old active mesh
    if (this.currentMesh) {
      this.scene.remove(this.currentMesh);
      ProceduralEngine.disposeHierarchy(this.currentMesh);
      this.currentMesh = null;
    }

    this.currentMesh = obj;
    this.lastValidMesh = obj.clone(); // Keep backup for safe error fallback
    this.scene.add(obj);

    // Backup original materials for shading toggles
    this.currentShadingMaterialsBackup.clear();
    obj.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        this.currentShadingMaterialsBackup.set(mesh, mesh.material);
      }
    });

    // Apply active shading mode
    this.applyShadingMode(this.activeShadingMode);

    // Notify HUD
    if (this.onStatsUpdate) {
      this.onStatsUpdate(stats, {
        id: reqId,
        version,
        timestamp: Date.now(),
        success: true,
        mode,
        stats
      });
    }
  }

  /**
   * Handles error state clearly without pretending success or showing demo models.
   */
  public displayError(errorMsg: string, reqId: string, version: number, mode: 'ai' | 'visual' | 'code'): void {
    this.currentState = 'error';

    // If we have a previous valid mesh, retain it but clearly notify HUD that it's previous
    const previousStats = this.lastValidMesh ? ProceduralEngine.computeGroupStats(this.lastValidMesh) : null;

    if (this.onStatsUpdate) {
      this.onStatsUpdate(previousStats, {
        id: reqId,
        version,
        timestamp: Date.now(),
        success: false,
        mode,
        error: errorMsg,
        stats: previousStats || undefined,
        isPreviousResultFallback: Boolean(this.lastValidMesh)
      });
    }
  }

  /**
   * Changes the 3D shading mode (Flat Shaded, Wireframe, Normals, Vertex Colors, Unlit).
   */
  public setShadingMode(mode: ShadingMode): void {
    this.activeShadingMode = mode;
    this.applyShadingMode(mode);
  }

  private applyShadingMode(mode: ShadingMode): void {
    if (!this.currentMesh) return;

    this.currentMesh.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        const originalMat = this.currentShadingMaterialsBackup.get(mesh);

        switch (mode) {
          case 'wireframe': {
            mesh.material = new THREE.MeshStandardMaterial({
              color: 0x00f0ff,
              wireframe: true
            });
            break;
          }
          case 'normals': {
            mesh.material = new THREE.MeshNormalMaterial({
              flatShading: true
            });
            break;
          }
          case 'vertex_colors': {
            mesh.material = new THREE.MeshBasicMaterial({
              vertexColors: true
            });
            break;
          }
          case 'unlit': {
            const baseColor = (originalMat as any)?.color || new THREE.Color(0xcccccc);
            mesh.material = new THREE.MeshBasicMaterial({
              color: baseColor
            });
            break;
          }
          case 'shaded':
          default: {
            if (originalMat) {
              mesh.material = originalMat;
            }
            break;
          }
        }
      }
    });
  }

  /**
   * Re-frames the camera to center the current model smoothly.
   */
  public resetCameraAndFrame(): void {
    if (!this.currentMesh) {
      this.camera.position.set(2.2, 1.8, 2.8);
      this.controls.target.set(0, 0.4, 0);
      this.controls.update();
      return;
    }

    const box = new THREE.Box3().setFromObject(this.currentMesh);
    if (box.isEmpty()) return;

    const center = new THREE.Vector3();
    const size = new THREE.Vector3();
    box.getCenter(center);
    box.getSize(size);

    const maxDim = Math.max(size.x, size.y, size.z, 0.5);
    const fov = this.camera.fov * (Math.PI / 180);
    const cameraDistance = (maxDim / 2) / Math.tan(fov / 2) * 1.5;

    this.camera.position.set(center.x + cameraDistance * 0.8, center.y + cameraDistance * 0.6, center.z + cameraDistance * 1.1);
    this.controls.target.copy(center);
    this.controls.update();
  }

  /**
   * Returns the exact root object currently visible for export.
   */
  public getVisibleObject(): THREE.Object3D | null {
    return this.currentMesh;
  }

  public getActiveRequestId(): string {
    return this.activeRequestId;
  }

  public getActiveVersion(): number {
    return this.activeVersion;
  }

  public destroy(): void {
    window.removeEventListener('resize', this.handleResize);
    if (this.currentMesh) {
      ProceduralEngine.disposeHierarchy(this.currentMesh);
    }
    if (this.lastValidMesh) {
      ProceduralEngine.disposeHierarchy(this.lastValidMesh);
    }
    this.renderer.dispose();
  }
}
