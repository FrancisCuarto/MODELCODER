import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { TransformControls } from 'three/examples/jsm/controls/TransformControls.js';
import { ProceduralEngine } from './procedural-engine';
import type { ShadingMode, GenerationState, GeometricStats, GenerationResult, TransformGizmoMode, CameraViewPreset } from './types';

export class StudioViewport {
  private container: HTMLElement;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;
  private transformControls: TransformControls;
  private gridHelper: THREE.GridHelper;
  private axesHelper: THREE.AxesHelper;
  private selectionBox: THREE.BoxHelper;
  private raycaster: THREE.Raycaster;
  private dirLight: THREE.DirectionalLight;
  private ambientLight: THREE.AmbientLight;

  private currentMesh: THREE.Object3D | null = null;
  private lastValidMesh: THREE.Object3D | null = null;
  private activeShadingMode: ShadingMode = 'shaded';
  private currentShadingMaterialsBackup: Map<THREE.Mesh, THREE.Material | THREE.Material[]> = new Map();

  // Selection & Gizmo state
  private selectedComponentIndex: number | null = null;
  private selectedMesh: THREE.Object3D | null = null;
  private currentGizmoMode: TransformGizmoMode = 'translate';
  private isTransformDragging = false;
  private pointerDownPos = { x: 0, y: 0, time: 0 };

  // Concurrency and generation tracking
  private activeRequestId = '';
  private activeVersion = 0;
  private currentState: GenerationState = 'idle';

  // Callbacks
  private onStatsUpdate?: (stats: GeometricStats | null, result: GenerationResult | null) => void;
  private onComponentSelected?: (index: number | null) => void;
  private onComponentTransformChange?: (index: number, pos: [number, number, number], rot: [number, number, number], scale: [number, number, number]) => void;

  constructor(
    container: HTMLElement,
    onStatsUpdate?: (stats: GeometricStats | null, result: GenerationResult | null) => void,
    onComponentSelected?: (index: number | null) => void,
    onComponentTransformChange?: (index: number, pos: [number, number, number], rot: [number, number, number], scale: [number, number, number]) => void
  ) {
    this.container = container;
    this.onStatsUpdate = onStatsUpdate;
    this.onComponentSelected = onComponentSelected;
    this.onComponentTransformChange = onComponentTransformChange;

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

    // 6. Retro Ground Grid & Axes
    this.gridHelper = new THREE.GridHelper(8, 32, 0x00f0ff, 0x1f2937);
    this.gridHelper.position.y = -0.001;
    this.scene.add(this.gridHelper);

    this.axesHelper = new THREE.AxesHelper(2.5);
    this.axesHelper.position.y = 0.001;
    this.axesHelper.visible = true;
    this.scene.add(this.axesHelper);

    // 7. Selection Highlight BoxHelper
    const dummy = new THREE.Mesh(new THREE.BufferGeometry());
    this.selectionBox = new THREE.BoxHelper(dummy, 0x00f0ff);
    this.selectionBox.visible = false;
    this.scene.add(this.selectionBox);

    // 8. TransformControls (Gizmos)
    this.transformControls = new TransformControls(this.camera, this.renderer.domElement);
    this.transformControls.size = 0.75;
    this.transformControls.addEventListener('dragging-changed', (event) => {
      this.controls.enabled = !event.value;
      this.isTransformDragging = Boolean(event.value);
    });
    this.transformControls.addEventListener('objectChange', () => {
      if (this.selectedMesh && this.selectedComponentIndex !== null) {
        const pos: [number, number, number] = [
          parseFloat(this.selectedMesh.position.x.toFixed(3)),
          parseFloat(this.selectedMesh.position.y.toFixed(3)),
          parseFloat(this.selectedMesh.position.z.toFixed(3))
        ];
        const rot: [number, number, number] = [
          parseFloat(THREE.MathUtils.radToDeg(this.selectedMesh.rotation.x).toFixed(1)),
          parseFloat(THREE.MathUtils.radToDeg(this.selectedMesh.rotation.y).toFixed(1)),
          parseFloat(THREE.MathUtils.radToDeg(this.selectedMesh.rotation.z).toFixed(1))
        ];
        const scale: [number, number, number] = [
          parseFloat(this.selectedMesh.scale.x.toFixed(3)),
          parseFloat(this.selectedMesh.scale.y.toFixed(3)),
          parseFloat(this.selectedMesh.scale.z.toFixed(3))
        ];
        this.selectionBox.setFromObject(this.selectedMesh);
        if (this.onComponentTransformChange) {
          this.onComponentTransformChange(this.selectedComponentIndex, pos, rot, scale);
        }
      }
    });
    const gizmoHelper = typeof this.transformControls.getHelper === 'function'
      ? this.transformControls.getHelper()
      : (this.transformControls as any);
    this.scene.add(gizmoHelper);

    // 9. Raycasting for Direct 3D Selection
    this.raycaster = new THREE.Raycaster();
    this.renderer.domElement.addEventListener('pointerdown', (e) => {
      this.pointerDownPos = { x: e.clientX, y: e.clientY, time: Date.now() };
    });
    this.renderer.domElement.addEventListener('pointerup', (e) => {
      if (this.isTransformDragging) return;
      const dist = Math.hypot(e.clientX - this.pointerDownPos.x, e.clientY - this.pointerDownPos.y);
      const duration = Date.now() - this.pointerDownPos.time;
      if (dist > 6 || duration > 400) return; // Orbit or pan movement, not a click

      const rect = this.renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );
      this.raycaster.setFromCamera(mouse, this.camera);
      if (this.currentMesh) {
        const hits = this.raycaster.intersectObjects(this.currentMesh.children, true);
        let matchedIdx: number | null = null;
        for (const hit of hits) {
          if (!hit.object.visible) continue;
          let curr: THREE.Object3D | null = hit.object;
          while (curr && curr !== this.currentMesh) {
            if (curr.userData && typeof curr.userData.componentIndex === 'number') {
              matchedIdx = curr.userData.componentIndex;
              break;
            }
            curr = curr.parent;
          }
          if (matchedIdx !== null) break;
        }

        if (matchedIdx !== null) {
          this.selectComponent(matchedIdx);
          if (this.onComponentSelected) {
            this.onComponentSelected(matchedIdx);
          }
        }
      }
    });

    // 10. Event listeners & Render loop
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

    // Detach gizmos before disposing old mesh
    this.transformControls.detach();
    this.selectionBox.visible = false;

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

    // Restore selection on updated geometry
    if (this.selectedComponentIndex !== null) {
      this.selectComponent(this.selectedComponentIndex);
    }

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
   * Selects an individual component by index, highlights it with BoxHelper, and attaches gizmo.
   */
  public selectComponent(index: number | null): void {
    this.selectedComponentIndex = index;

    if (index === null || !this.currentMesh) {
      this.selectedMesh = null;
      this.transformControls.detach();
      this.selectionBox.visible = false;
      return;
    }

    const target = this.getMeshByComponentIndex(index);
    if (!target) {
      this.selectedMesh = null;
      this.transformControls.detach();
      this.selectionBox.visible = false;
      return;
    }

    this.selectedMesh = target;
    if (this.currentGizmoMode !== 'none') {
      this.transformControls.attach(target);
    }
    this.selectionBox.setFromObject(target);
    this.selectionBox.visible = true;
  }

  public getSelectedComponentIndex(): number | null {
    return this.selectedComponentIndex;
  }

  /**
   * Sets gizmo transformation mode (translate, rotate, scale, or none).
   */
  public setGizmoMode(mode: TransformGizmoMode): void {
    this.currentGizmoMode = mode;
    if (mode === 'none') {
      this.transformControls.detach();
    } else {
      this.transformControls.setMode(mode);
      if (this.selectedMesh) {
        this.transformControls.attach(this.selectedMesh);
      }
    }
  }

  /**
   * Configures grid & rotation snapping on gizmos.
   */
  public setSnap(enableSnap: boolean, translationSnap: number = 0.1, rotationSnapDeg: number = 15): void {
    if (enableSnap) {
      this.transformControls.setTranslationSnap(translationSnap);
      this.transformControls.setRotationSnap(THREE.MathUtils.degToRad(rotationSnapDeg));
      this.transformControls.setScaleSnap(0.1);
    } else {
      this.transformControls.setTranslationSnap(null);
      this.transformControls.setRotationSnap(null);
      this.transformControls.setScaleSnap(null);
    }
  }

  /**
   * Toggles visibility of the ground grid.
   */
  public setGridVisible(visible: boolean): void {
    this.gridHelper.visible = visible;
  }

  /**
   * Toggles visibility of the XYZ coordinate axes.
   */
  public setAxesVisible(visible: boolean): void {
    this.axesHelper.visible = visible;
  }

  /**
   * Predefined camera viewpoints (front, side, top, isometric).
   */
  public setViewPreset(preset: CameraViewPreset): void {
    const center = new THREE.Vector3(0, 0.4, 0);
    let dist = 3.2;

    if (this.currentMesh) {
      const box = new THREE.Box3().setFromObject(this.currentMesh);
      if (!box.isEmpty()) {
        box.getCenter(center);
        const size = new THREE.Vector3();
        box.getSize(size);
        const maxDim = Math.max(size.x, size.y, size.z, 0.5);
        const fov = this.camera.fov * (Math.PI / 180);
        dist = (maxDim / 2) / Math.tan(fov / 2) * 1.6;
      }
    }

    this.controls.target.copy(center);
    switch (preset) {
      case 'front':
        this.camera.position.set(center.x, center.y, center.z + dist);
        break;
      case 'side':
        this.camera.position.set(center.x + dist, center.y, center.z);
        break;
      case 'top':
        this.camera.position.set(center.x, center.y + dist, center.z + 0.001);
        break;
      case 'isometric':
      case 'perspective':
      default:
        this.camera.position.set(
          center.x + dist * 0.7,
          center.y + dist * 0.55,
          center.z + dist * 0.75
        );
        break;
    }
    this.controls.update();
  }

  /**
   * Centers and frames the selected component in the viewport camera.
   */
  public focusComponent(index: number): void {
    const mesh = this.getMeshByComponentIndex(index);
    if (!mesh) return;

    const box = new THREE.Box3().setFromObject(mesh);
    if (box.isEmpty()) return;

    const center = new THREE.Vector3();
    const size = new THREE.Vector3();
    box.getCenter(center);
    box.getSize(size);

    const maxDim = Math.max(size.x, size.y, size.z, 0.25);
    const fov = this.camera.fov * (Math.PI / 180);
    const dist = (maxDim / 2) / Math.tan(fov / 2) * 2.0;

    this.controls.target.copy(center);
    this.camera.position.set(
      center.x + dist * 0.7,
      center.y + dist * 0.6,
      center.z + dist * 0.7
    );
    this.controls.update();
  }

  /**
   * Updates selection helper box when component moves or resizes.
   */
  public updateSelectionBox(): void {
    if (this.selectedMesh && this.selectionBox.visible) {
      this.selectionBox.setFromObject(this.selectedMesh);
    }
  }

  private getMeshByComponentIndex(index: number): THREE.Object3D | null {
    if (!this.currentMesh) return null;
    let match: THREE.Object3D | null = null;
    this.currentMesh.traverse((child) => {
      if (match) return;
      if (child.userData && child.userData.componentIndex === index) {
        match = child;
      }
    });
    return match;
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
   * Re-frames the camera to center the whole model smoothly.
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

    this.camera.position.set(
      center.x + cameraDistance * 0.8,
      center.y + cameraDistance * 0.6,
      center.z + cameraDistance * 1.1
    );
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

  /**
   * Triggers an immediate recalculation of viewport bounds and projection.
   */
  public resize(): void {
    this.handleResize();
  }

  /**
   * Toggles smooth continuous 360 turntable auto-rotation around the model.
   */
  public setTurntable(enabled: boolean, speedMultiplier: number = 1.0): void {
    this.controls.autoRotate = enabled;
    this.controls.autoRotateSpeed = 2.0 * speedMultiplier;
  }

  public isTurntableEnabled(): boolean {
    return this.controls.autoRotate;
  }

  /**
   * Sets the 3D environment backdrop mode.
   */
  public setBackgroundMode(mode: 'dark' | 'studio' | 'transparent'): void {
    if (mode === 'transparent') {
      this.scene.background = null;
      this.renderer.setClearColor(0x000000, 0);
      this.gridHelper.visible = false;
    } else if (mode === 'studio') {
      this.scene.background = new THREE.Color(0x1a202c);
      this.renderer.setClearColor(0x1a202c, 1);
      this.gridHelper.visible = true;
    } else {
      // 'dark' (Default Retro Space)
      this.scene.background = new THREE.Color(0x0a0d14);
      this.renderer.setClearColor(0x0a0d14, 1);
      this.gridHelper.visible = true;
    }
  }

  /**
   * Captures a clean high-definition PNG screenshot without editor gizmos or overlays.
   */
  public captureRenderScreenshot(filename: string = 'model_render.png'): void {
    const prevGizmoHelper = typeof this.transformControls.getHelper === 'function'
      ? this.transformControls.getHelper()
      : (this.transformControls as any);
    const wasGizmoVisible = prevGizmoHelper ? prevGizmoHelper.visible : false;
    const wasSelectionVisible = this.selectionBox.visible;

    if (prevGizmoHelper) prevGizmoHelper.visible = false;
    this.selectionBox.visible = false;

    this.renderer.render(this.scene, this.camera);
    const dataUrl = this.renderer.domElement.toDataURL('image/png');

    if (prevGizmoHelper) prevGizmoHelper.visible = wasGizmoVisible;
    this.selectionBox.visible = wasSelectionVisible;

    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  public setOnComponentSelected(cb: (index: number | null) => void): void {
    this.onComponentSelected = cb;
  }

  public setOnComponentTransformChange(cb: (index: number, pos: [number, number, number], rot: [number, number, number], scale: [number, number, number]) => void): void {
    this.onComponentTransformChange = cb;
  }

  public destroy(): void {
    window.removeEventListener('resize', this.handleResize);
    this.transformControls.dispose();
    this.selectionBox.dispose();
    if (this.currentMesh) {
      ProceduralEngine.disposeHierarchy(this.currentMesh);
    }
    if (this.lastValidMesh) {
      ProceduralEngine.disposeHierarchy(this.lastValidMesh);
    }
    this.renderer.dispose();
  }
}
