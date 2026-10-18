import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { TransformControls } from 'three/examples/jsm/controls/TransformControls.js';
import { ProceduralEngine } from './procedural-engine.ts';
import { AnimationEngine } from './animation-engine.ts';
import type { ShadingMode, GenerationState, GeometricStats, GenerationResult, TransformGizmoMode, CameraViewPreset, AnimationClipDef } from './types.ts';

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
  private lastValidStats: GeometricStats | null = null;
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

  // Animation System state
  private clock = new THREE.Clock();
  private mixer: THREE.AnimationMixer | null = null;
  private animationActions: Map<string, THREE.AnimationAction> = new Map();
  private compiledClips: THREE.AnimationClip[] = [];
  private activeAction: THREE.AnimationAction | null = null;
  private activeClipName: string | null = null;
  private isAnimationPlaying = false;
  private animationSpeed = 1.0;
  private playbackLoopMode: 'repeat' | 'once' | 'pingpong' = 'repeat';
  private onAnimationProgress?: (time: number, duration: number, isPlaying: boolean, clipName: string) => void;

  // Callbacks
  private onStatsUpdate?: (stats: GeometricStats | null, result: GenerationResult | null) => void;
  private onComponentSelected?: (index: number | null) => void;
  private onComponentTransformChange?: (
    index: number,
    pos: [number, number, number],
    rot: [number, number, number],
    scale: [number, number, number],
    isCommit?: boolean
  ) => void;
  private resizeObserver: ResizeObserver | null = null;

  constructor(
    container: HTMLElement,
    onStatsUpdate?: (stats: GeometricStats | null, result: GenerationResult | null) => void,
    onComponentSelected?: (index: number | null) => void,
    onComponentTransformChange?: (
      index: number,
      pos: [number, number, number],
      rot: [number, number, number],
      scale: [number, number, number],
      isCommit?: boolean
    ) => void
  ) {
    this.container = container;
    this.onStatsUpdate = onStatsUpdate;
    this.onComponentSelected = onComponentSelected;
    this.onComponentTransformChange = onComponentTransformChange;

    // 1. Scene setup
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0d14);

    // 2. Camera setup
    const initialParent = container.parentElement || container;
    const initialWidth = initialParent.clientWidth || container.clientWidth || 800;
    const initialHeight = initialParent.clientHeight || container.clientHeight || 520;
    const aspect = initialWidth / (initialHeight || 1);
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.05, 100);
    this.camera.position.set(2.2, 1.8, 2.8);

    // 3. Renderer setup (with multi-tier fallback for constrained GPUs / WebGL context limits)
    try {
      this.renderer = new THREE.WebGLRenderer({
        antialias: true,
        powerPreference: 'high-performance',
        preserveDrawingBuffer: true,
        alpha: true
      });
    } catch {
      try {
        this.renderer = new THREE.WebGLRenderer({
          antialias: false,
          preserveDrawingBuffer: true,
          alpha: true
        });
      } catch {
        this.renderer = new THREE.WebGLRenderer({ alpha: true });
      }
    }
    this.renderer.setSize(initialWidth, initialHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFShadowMap;

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
    const emitTransformUpdate = (isCommit: boolean) => {
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
          this.onComponentTransformChange(this.selectedComponentIndex, pos, rot, scale, isCommit);
        }
      }
    };
    this.transformControls.addEventListener('dragging-changed', (event) => {
      this.controls.enabled = !event.value;
      this.isTransformDragging = Boolean(event.value);
      if (!event.value) {
        emitTransformUpdate(true);
      }
    });
    this.transformControls.addEventListener('objectChange', () => {
      emitTransformUpdate(false);
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

    // Auto-observe container/parent surface for layout, tab, and fullscreen transitions
    const targetObserved = this.container.parentElement || this.container;
    if (typeof ResizeObserver !== 'undefined' && targetObserved) {
      this.resizeObserver = new ResizeObserver(() => {
        this.handleResize();
      });
      this.resizeObserver.observe(targetObserved);
    }

    this.animate();
  }

  private handleResize = (): void => {
    if (!this.container || !this.renderer || !this.camera) return;
    const parentEl = this.container.parentElement;
    const width = (parentEl && parentEl.clientWidth > 0) ? parentEl.clientWidth : this.container.clientWidth;
    const height = (parentEl && parentEl.clientHeight > 0) ? parentEl.clientHeight : this.container.clientHeight;
    if (width === 0 || height === 0) return;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  };

  private animate = (): void => {
    requestAnimationFrame(this.animate);
    const delta = this.clock.getDelta();
    if (this.mixer && this.isAnimationPlaying && this.activeAction) {
      this.mixer.update(delta * this.animationSpeed);
      if (this.selectedMesh && this.selectionBox.visible) {
        this.selectionBox.update();
      }
      if (this.onAnimationProgress) {
        const dur = this.activeAction.getClip().duration || 1.0;
        let curTime: number;
        if (this.playbackLoopMode === 'once') {
          curTime = Math.min(dur, Math.max(0, this.activeAction.time));
          if (curTime >= dur && !this.activeAction.isRunning()) {
            this.isAnimationPlaying = false;
          }
        } else {
          curTime = this.activeAction.time % dur;
        }
        this.onAnimationProgress(curTime, dur, this.isAnimationPlaying, this.activeClipName || '');
      }
    }
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  };

  private createMixer(root: THREE.Object3D): THREE.AnimationMixer {
    if (this.mixer) {
      this.mixer.stopAllAction();
      if (this.currentMesh) {
        this.mixer.uncacheRoot(this.currentMesh);
      }
    }
    const mixer = new THREE.AnimationMixer(root);
    mixer.addEventListener('finished', () => {
      this.isAnimationPlaying = false;
      if (this.activeAction && this.onAnimationProgress) {
        const dur = this.activeAction.getClip().duration || 1.0;
        this.onAnimationProgress(dur, dur, false, this.activeClipName || '');
      }
    });
    return mixer;
  }

  /**
   * Updates the viewport with a genuine new generated 3D object.
   * Disposes previous geometry cleanly and guards against stale race conditions.
   */
  public displayGeneratedMesh(
    obj: THREE.Object3D,
    reqId: string,
    version: number,
    stats: GeometricStats,
    mode: 'ai' | 'visual' | 'code',
    animations?: AnimationClipDef[]
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

    // Dispose old animation mixer and actions
    if (this.mixer) {
      this.mixer.stopAllAction();
      if (this.currentMesh) {
        this.mixer.uncacheRoot(this.currentMesh);
      }
      this.mixer = null;
    }
    this.animationActions.clear();
    this.compiledClips = [];
    this.activeAction = null;
    this.activeClipName = null;
    this.isAnimationPlaying = false;

    // Dispose old active mesh (after restoring original PBR materials so textures are not leaked)
    if (this.currentMesh) {
      this.restoreOriginalMaterialsOnCurrentMesh();
      this.scene.remove(this.currentMesh);
      ProceduralEngine.disposeHierarchy(this.currentMesh);
      this.currentMesh = null;
    }

    this.currentMesh = obj;
    this.lastValidStats = stats; // Cache validated stats for safe error fallback without dangling BufferGeometry refs
    this.scene.add(obj);

    // Initialize mixer and load animations if present
    this.mixer = this.createMixer(obj);
    if (animations && animations.length > 0) {
      this.loadAnimations(animations);
    }

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

  // ---------------------------------------------------------------------------
  // Animation System Viewport Control Methods
  // ---------------------------------------------------------------------------

  public setOnAnimationProgressCallback(
    cb: (time: number, duration: number, isPlaying: boolean, clipName: string) => void
  ): void {
    this.onAnimationProgress = cb;
  }

  public loadAnimations(animations?: AnimationClipDef[]): void {
    if (this.mixer) {
      this.mixer.stopAllAction();
    }
    this.animationActions.clear();
    this.compiledClips = [];
    this.activeAction = null;
    this.activeClipName = null;
    this.isAnimationPlaying = false;

    if (!this.currentMesh) return;
    if (!this.mixer) {
      this.mixer = this.createMixer(this.currentMesh);
    }

    if (!animations || animations.length === 0) return;

    this.compiledClips = AnimationEngine.compileClipsToThree(animations, this.currentMesh);
    for (const clip of this.compiledClips) {
      const action = this.mixer.clipAction(clip);
      const loopType = this.playbackLoopMode === 'once'
        ? 'once'
        : this.playbackLoopMode === 'pingpong'
          ? 'pingpong'
          : (clip.userData.loop || 'repeat');
      if (loopType === 'pingpong') {
        action.setLoop(THREE.LoopPingPong, Infinity);
        action.clampWhenFinished = false;
      } else if (loopType === 'once') {
        action.setLoop(THREE.LoopOnce, 1);
        action.clampWhenFinished = true;
      } else {
        action.setLoop(THREE.LoopRepeat, Infinity);
        action.clampWhenFinished = false;
      }
      this.animationActions.set(clip.name, action);
    }

    if (this.compiledClips.length > 0) {
      const firstClip = this.compiledClips[0];
      this.activeClipName = firstClip.name;
      this.activeAction = this.animationActions.get(firstClip.name) || null;
      if (this.activeAction) {
        this.activeAction.time = 0;
        this.mixer.update(0);
      }
    }
  }

  public setPlaybackLoopMode(mode: 'repeat' | 'once' | 'pingpong'): void {
    this.playbackLoopMode = mode;
    for (const action of this.animationActions.values()) {
      if (mode === 'once') {
        action.setLoop(THREE.LoopOnce, 1);
        action.clampWhenFinished = true;
      } else if (mode === 'pingpong') {
        action.setLoop(THREE.LoopPingPong, Infinity);
        action.clampWhenFinished = false;
      } else {
        action.setLoop(THREE.LoopRepeat, Infinity);
        action.clampWhenFinished = false;
      }
    }
  }

  public getPlaybackLoopMode(): 'repeat' | 'once' | 'pingpong' {
    return this.playbackLoopMode;
  }

  public playAnimation(clipName?: string): void {
    if (!this.mixer || this.compiledClips.length === 0) return;

    let targetName = clipName || this.activeClipName || this.compiledClips[0]?.name;
    if (!targetName) return;

    const nextAction = this.animationActions.get(targetName);
    if (!nextAction) return;

    if (this.activeAction && this.activeAction !== nextAction) {
      this.activeAction.fadeOut(0.15);
      nextAction.reset().fadeIn(0.15);
    }

    this.activeClipName = targetName;
    this.activeAction = nextAction;

    // Reset to start if already at the end or if LoopOnce has completed
    const dur = this.activeAction.getClip().duration || 1.0;
    if (this.activeAction.time >= dur - 0.03 || !this.activeAction.isRunning()) {
      this.activeAction.reset();
      this.activeAction.time = 0;
    }

    this.activeAction.paused = false;
    this.activeAction.play();
    this.isAnimationPlaying = true;
  }

  public pauseAnimation(): void {
    if (this.activeAction) {
      this.activeAction.paused = true;
    }
    this.isAnimationPlaying = false;
    if (this.onAnimationProgress && this.activeAction) {
      this.onAnimationProgress(
        this.activeAction.time,
        this.activeAction.getClip().duration,
        false,
        this.activeClipName || ''
      );
    }
  }

  public stopAnimation(): void {
    if (this.mixer) {
      this.mixer.stopAllAction();
      this.mixer.setTime(0);
    }
    this.isAnimationPlaying = false;
    if (this.activeAction) {
      this.activeAction.time = 0;
    }
    if (this.onAnimationProgress && this.activeAction) {
      this.onAnimationProgress(0, this.activeAction.getClip().duration, false, this.activeClipName || '');
    }
    this.renderer.render(this.scene, this.camera);
  }

  public seekAnimation(timeInSeconds: number): void {
    if (!this.mixer || !this.activeAction) return;
    const dur = this.activeAction.getClip().duration || 1.0;
    const clamped = Math.max(0, Math.min(dur, timeInSeconds));

    this.activeAction.time = clamped;
    this.activeAction.paused = true;
    this.isAnimationPlaying = false;
    this.mixer.update(0);
    if (this.selectedMesh && this.selectionBox.visible) {
      this.selectionBox.update();
    }
    this.renderer.render(this.scene, this.camera);

    if (this.onAnimationProgress) {
      this.onAnimationProgress(clamped, dur, false, this.activeClipName || '');
    }
  }

  public setAnimationSpeed(speedMultiplier: number): void {
    this.animationSpeed = Math.max(0.1, Math.min(5.0, speedMultiplier));
    if (this.activeAction) {
      this.activeAction.setEffectiveTimeScale(this.animationSpeed);
    }
  }

  public getActiveClipInfo(): {
    name: string;
    duration: number;
    time: number;
    isPlaying: boolean;
    speed: number;
    clipCount: number;
    clipNames: string[];
  } | null {
    if (!this.activeAction || !this.activeClipName) {
      return {
        name: '',
        duration: 0,
        time: 0,
        isPlaying: false,
        speed: this.animationSpeed,
        clipCount: this.compiledClips.length,
        clipNames: this.compiledClips.map((c) => c.name)
      };
    }
    return {
      name: this.activeClipName,
      duration: this.activeAction.getClip().duration,
      time: this.activeAction.time % (this.activeAction.getClip().duration || 1),
      isPlaying: this.isAnimationPlaying,
      speed: this.animationSpeed,
      clipCount: this.compiledClips.length,
      clipNames: this.compiledClips.map((c) => c.name)
    };
  }

  /**
   * Handles error state clearly without pretending success or showing demo models.
   */
  public displayError(errorMsg: string, reqId: string, version: number, mode: 'ai' | 'visual' | 'code'): void {
    this.currentState = 'error';

    // If we have a previous valid mesh, retain it but clearly notify HUD that it's previous
    const previousStats = this.lastValidStats;

    if (this.onStatsUpdate) {
      this.onStatsUpdate(previousStats, {
        id: reqId,
        version,
        timestamp: Date.now(),
        success: false,
        mode,
        error: errorMsg,
        stats: previousStats || undefined,
        isPreviousResultFallback: Boolean(this.currentMesh && previousStats)
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

  /**
   * Restores the original PBR materials onto currentMesh and disposes any temporary debug shading materials.
   */
  private restoreOriginalMaterialsOnCurrentMesh(): void {
    if (!this.currentMesh) return;
    this.currentMesh.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        const originalMat = this.currentShadingMaterialsBackup.get(mesh);
        if (originalMat && mesh.material !== originalMat) {
          const tempMat = mesh.material;
          mesh.material = originalMat;
          if (Array.isArray(tempMat)) {
            tempMat.forEach((m) => m.dispose());
          } else if (tempMat) {
            tempMat.dispose();
          }
        }
      }
    });
  }

  private applyShadingMode(mode: ShadingMode): void {
    if (!this.currentMesh) return;

    // First restore original materials and dispose any previous temporary shading materials
    this.restoreOriginalMaterialsOnCurrentMesh();

    if (mode === 'shaded') return;

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
          default:
            break;
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

  /**
   * Temporarily restores original PBR materials on the active mesh while running an export callback,
   * then re-applies the active inspection shading mode (e.g., wireframe, normals) afterward.
   */
  public async executeWithOriginalMaterials<T>(fn: (root: THREE.Object3D) => Promise<T>): Promise<T> {
    if (!this.currentMesh) {
      throw new Error('No hay ningún objeto 3D activo en el visor.');
    }
    const modeBeforeExport = this.activeShadingMode;
    try {
      if (modeBeforeExport !== 'shaded') {
        this.restoreOriginalMaterialsOnCurrentMesh();
      }
      return await fn(this.currentMesh);
    } finally {
      if (modeBeforeExport !== 'shaded') {
        this.applyShadingMode(modeBeforeExport);
      }
    }
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

  /**
   * Captures a clean, compact PNG/JPEG thumbnail data URL for project drafts and inventory.
   * Resizes to 160x160 to prevent localStorage quota exhaustion.
   */
  public getThumbnailDataURL(): string {
    const prevGizmoHelper = typeof this.transformControls.getHelper === 'function'
      ? this.transformControls.getHelper()
      : (this.transformControls as any);
    const wasGizmoVisible = prevGizmoHelper ? prevGizmoHelper.visible : false;
    const wasSelectionVisible = this.selectionBox.visible;

    try {
      if (prevGizmoHelper) prevGizmoHelper.visible = false;
      this.selectionBox.visible = false;

      this.renderer.render(this.scene, this.camera);

      // Create a 160x160 canvas to keep thumbnail under 10KB
      const thumbCanvas = document.createElement('canvas');
      thumbCanvas.width = 160;
      thumbCanvas.height = 160;
      const ctx = thumbCanvas.getContext('2d');
      if (ctx && this.renderer.domElement.width > 0) {
        ctx.drawImage(this.renderer.domElement, 0, 0, 160, 160);
        return thumbCanvas.toDataURL('image/jpeg', 0.82);
      }

      return this.renderer.domElement.toDataURL('image/jpeg', 0.7);
    } catch (e) {
      console.warn('[StudioViewport] Failed to generate thumbnail:', e);
      return '';
    } finally {
      if (prevGizmoHelper) prevGizmoHelper.visible = wasGizmoVisible;
      this.selectionBox.visible = wasSelectionVisible;
    }
  }

  /**
   * Captures an offscreen high-definition render of the 3D model for Instagram Stories (9:16)
   * or social sharing. Hides gizmos, grid, and axes, restores original PBR materials,
   * and renders with a clean transparent background.
   */
  public async captureStoryRender(options: {
    width?: number;
    height?: number;
    autoFrame?: boolean;
  } = {}): Promise<HTMLCanvasElement> {
    const targetWidth = options.width || 1080;
    const targetHeight = options.height || 1080;
    const autoFrame = Boolean(options.autoFrame);

    if (!this.currentMesh) {
      const emptyCanvas = document.createElement('canvas');
      emptyCanvas.width = targetWidth;
      emptyCanvas.height = targetHeight;
      return emptyCanvas;
    }

    return await this.executeWithOriginalMaterials(async () => {
      const prevGizmoHelper = typeof this.transformControls.getHelper === 'function'
        ? this.transformControls.getHelper()
        : (this.transformControls as any);
      const wasGizmoVisible = prevGizmoHelper ? prevGizmoHelper.visible : false;
      const wasSelectionVisible = this.selectionBox.visible;
      const wasAxesVisible = this.axesHelper.visible;
      const wasGridVisible = this.gridHelper.visible;

      const prevBackground = this.scene.background;
      const prevClearColor = new THREE.Color();
      this.renderer.getClearColor(prevClearColor);
      const prevClearAlpha = this.renderer.getClearAlpha();
      const prevCamPos = this.camera.position.clone();
      const prevTarget = this.controls.target.clone();
      const prevAspect = this.camera.aspect;
      const prevPixelRatio = this.renderer.getPixelRatio();

      try {
        if (prevGizmoHelper) prevGizmoHelper.visible = false;
        this.selectionBox.visible = false;
        this.axesHelper.visible = false;
        this.gridHelper.visible = false;

        this.scene.background = null;
        this.renderer.setClearColor(0x000000, 0);

        if (autoFrame && this.currentMesh) {
          const box = new THREE.Box3().setFromObject(this.currentMesh);
          if (!box.isEmpty()) {
            const center = new THREE.Vector3();
            const size = new THREE.Vector3();
            box.getCenter(center);
            box.getSize(size);
            const maxDim = Math.max(size.x, size.y, size.z, 0.5);
            const fov = this.camera.fov * (Math.PI / 180);
            const cameraDistance = (maxDim / 2) / Math.tan(fov / 2) * 1.45;
            this.camera.position.set(
              center.x + cameraDistance * 0.85,
              center.y + cameraDistance * 0.65,
              center.z + cameraDistance * 1.15
            );
            this.controls.target.copy(center);
            this.controls.update();
          }
        }

        this.renderer.setPixelRatio(1);
        this.renderer.setSize(targetWidth, targetHeight, false);
        this.camera.aspect = targetWidth / targetHeight;
        this.camera.updateProjectionMatrix();

        this.renderer.render(this.scene, this.camera);

        const outCanvas = document.createElement('canvas');
        outCanvas.width = targetWidth;
        outCanvas.height = targetHeight;
        const ctx = outCanvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(this.renderer.domElement, 0, 0);
        }
        return outCanvas;
      } finally {
        if (prevGizmoHelper) prevGizmoHelper.visible = wasGizmoVisible;
        this.selectionBox.visible = wasSelectionVisible;
        this.axesHelper.visible = wasAxesVisible;
        this.gridHelper.visible = wasGridVisible;

        this.scene.background = prevBackground;
        this.renderer.setClearColor(prevClearColor, prevClearAlpha);
        this.camera.position.copy(prevCamPos);
        this.controls.target.copy(prevTarget);
        this.controls.update();
        this.camera.aspect = prevAspect;
        this.camera.updateProjectionMatrix();
        this.renderer.setPixelRatio(prevPixelRatio);
        this.handleResize();
        this.renderer.render(this.scene, this.camera);
      }
    });
  }

  public setOnComponentSelected(cb: (index: number | null) => void): void {
    this.onComponentSelected = cb;
  }

  public setOnComponentTransformChange(cb: (index: number, pos: [number, number, number], rot: [number, number, number], scale: [number, number, number]) => void): void {
    this.onComponentTransformChange = cb;
  }

  /**
   * Records the viewport during animation playback (or a smooth 360° turntable orbit)
   * directly into a WebM video Blob.
   * Automatically disables gizmos and selection boxes during capture and restores them when finished.
   */
  public async recordAnimationLoop(options: {
    duration?: number;
    fps?: number;
    onProgress?: (progress01: number) => void;
  } = {}): Promise<Blob> {
    if (!this.currentMesh) {
      throw new Error('No hay ningún modelo en el visor para grabar.');
    }

    if (typeof (globalThis as any).MediaRecorder === 'undefined') {
      throw new Error('MediaRecorder no está soportado en este entorno o navegador.');
    }

    const canvas = this.renderer.domElement;
    if (typeof (canvas as any).captureStream !== 'function') {
      throw new Error('captureStream no está disponible en este canvas.');
    }

    const prevGizmoHelper = typeof this.transformControls.getHelper === 'function'
      ? this.transformControls.getHelper()
      : (this.transformControls as any);
    const wasGizmoVisible = prevGizmoHelper ? prevGizmoHelper.visible : false;
    const wasSelectionVisible = this.selectionBox.visible;

    try {
      if (prevGizmoHelper) prevGizmoHelper.visible = false;
      this.selectionBox.visible = false;

      // Determine duration
      let targetDuration = options.duration;
      const isTurntableOnly = !this.activeAction && this.compiledClips.length === 0;

      if (!targetDuration || targetDuration <= 0) {
        if (this.activeAction && this.activeAction.getClip().duration > 0) {
          targetDuration = this.activeAction.getClip().duration;
        } else if (this.compiledClips.length > 0 && this.compiledClips[0].duration > 0) {
          targetDuration = this.compiledClips[0].duration;
        } else {
          targetDuration = 3.0; // 3-second 360-turntable spin
        }
      }

      // If animation is loaded, restart from time 0 and play at 1.0x
      if (this.activeAction) {
        this.activeAction.time = 0;
        this.activeAction.paused = false;
        this.activeAction.play();
        this.isAnimationPlaying = true;
      }

      const prevRotation = this.currentMesh.rotation.y;
      const fps = options.fps || 30;
      const stream = (canvas as any).captureStream(fps);

      let mimeType = 'video/webm;codecs=vp9';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = 'video/webm;codecs=vp8';
      }
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = 'video/webm';
      }

      const recorder = new MediaRecorder(stream, {
        mimeType,
        videoBitsPerSecond: 5_000_000
      });

      const chunks: BlobPart[] = [];
      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      return await new Promise<Blob>((resolve, reject) => {
        recorder.onstop = () => {
          if (isTurntableOnly && this.currentMesh) {
            this.currentMesh.rotation.y = prevRotation;
          }
          const blob = new Blob(chunks, { type: mimeType });
          resolve(blob);
        };
        recorder.onerror = (e) => reject(e);

        recorder.start();
        const startTime = performance.now();
        const totalMs = targetDuration! * 1000;

        const intervalId = setInterval(() => {
          const elapsed = performance.now() - startTime;
          const prog = Math.min(1.0, elapsed / totalMs);

          if (isTurntableOnly && this.currentMesh) {
            this.currentMesh.rotation.y = prevRotation + prog * Math.PI * 2;
          }

          if (options.onProgress) {
            options.onProgress(prog);
          }
          if (elapsed >= totalMs) {
            clearInterval(intervalId);
            if (recorder.state === 'recording') {
              recorder.stop();
            }
          }
        }, 33);
      });
    } finally {
      if (prevGizmoHelper) prevGizmoHelper.visible = wasGizmoVisible;
      this.selectionBox.visible = wasSelectionVisible;
    }
  }

  public destroy(): void {
    window.removeEventListener('resize', this.handleResize);
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
    this.transformControls.dispose();
    this.selectionBox.dispose();
    if (this.currentMesh) {
      this.restoreOriginalMaterialsOnCurrentMesh();
      ProceduralEngine.disposeHierarchy(this.currentMesh);
      this.currentMesh = null;
    }
    this.currentShadingMaterialsBackup.clear();
    this.renderer.dispose();
  }
}
