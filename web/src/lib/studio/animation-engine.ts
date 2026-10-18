import * as THREE from 'three';
import type {
  AnimationClipDef,
  AnimationTrackDef,
  AnimationKeyframeDef,
  AnimationPresetType,
  AnimationInterpolation
} from './types.ts';

export interface PresetOptions {
  targetComponent: string;
  name?: string;
  duration?: number;
  axis?: 'x' | 'y' | 'z';
  distance?: number;
  openAngleDeg?: number;
  pressDepth?: number;
  amplitude?: number;
  extendDistance?: number;
  deployAngleDeg?: number;
  initialPos?: [number, number, number];
  initialRot?: [number, number, number];
  initialScale?: [number, number, number];
  loop?: 'repeat' | 'pingpong' | 'once';
}

export class AnimationEngine {
  /**
   * Returns a map of user-friendly preset definitions with icons and descriptions.
   */
  public static getAvailablePresets(): Array<{
    type: AnimationPresetType;
    label: string;
    description: string;
    defaultDuration: number;
    icon: string;
  }> {
    return [
      {
        type: 'sliding_door',
        label: 'Puerta Corrediza / Compuerta',
        description: 'Desplazamiento lineal a lo largo de un eje que abre y cierra suavemente.',
        defaultDuration: 1.6,
        icon: '🚪'
      },
      {
        type: 'hinge_lid',
        label: 'Tapa con Bisagra / Escotilla',
        description: 'Rotación angular sobre un eje de bisagra (0° a 90° o ángulo personalizado).',
        defaultDuration: 1.8,
        icon: '🧰'
      },
      {
        type: 'button_press',
        label: 'Botón Pulsador / Palanca',
        description: 'Hundimiento mecánico rápido con retroceso elástico de muelle.',
        defaultDuration: 0.8,
        icon: '🔘'
      },
      {
        type: 'spin_continuous',
        label: 'Giro Continuo 360°',
        description: 'Rotación continua completa de 360° (hélices, radares, balizas o turbinas).',
        defaultDuration: 2.0,
        icon: '🔄'
      },
      {
        type: 'mechanical_deploy',
        label: 'Despliegue Mecánico (Tren/Ala)',
        description: 'Extensión combinada de posición y rotación sincronizada.',
        defaultDuration: 2.4,
        icon: '🚀'
      },
      {
        type: 'idle_hover',
        label: 'Flotación Idle / Levitación',
        description: 'Movimiento sinusoidal vertical suave para vehículos o naves en reposo.',
        defaultDuration: 2.5,
        icon: '🛸'
      }
    ];
  }

  /**
   * Generates a declarative AnimationClipDef based on standard mechanical presets.
   */
  public static createPresetClip(
    type: AnimationPresetType,
    opts: PresetOptions
  ): AnimationClipDef {
    const target = opts.targetComponent;
    const duration = Math.max(0.2, opts.duration ?? 2.0);
    const loop = opts.loop ?? (type === 'spin_continuous' || type === 'idle_hover' ? 'repeat' : 'pingpong');
    const id = `anim_${type}_${Date.now()}_${Math.floor(Math.random() * 1000)}`;
    const axis = opts.axis || (type === 'hinge_lid' ? 'x' : type === 'idle_hover' ? 'y' : 'x');
    const initPos = opts.initialPos ? [...opts.initialPos] as [number, number, number] : [0, 0, 0];
    const initRot = opts.initialRot ? [...opts.initialRot] as [number, number, number] : [0, 0, 0];

    const axisIdx = axis === 'x' ? 0 : axis === 'y' ? 1 : 2;

    switch (type) {
      case 'sliding_door': {
        const dist = opts.distance ?? 1.2;
        const openPos: [number, number, number] = [...initPos];
        openPos[axisIdx] += dist;

        return {
          id,
          name: opts.name || `Open_${target}`,
          duration,
          loop,
          presetType: type,
          tracks: [
            {
              targetComponent: target,
              targetName: target,
              property: 'position',
              keyframes: [
                { time: 0, value: [...initPos], interpolation: 'linear' },
                { time: Number((duration * 0.5).toFixed(2)), value: openPos, interpolation: 'linear' },
                { time: Number(duration.toFixed(2)), value: [...initPos], interpolation: 'linear' }
              ]
            }
          ]
        };
      }

      case 'hinge_lid': {
        const angle = opts.openAngleDeg ?? 90;
        const openRot: [number, number, number] = [...initRot];
        openRot[axisIdx] += angle;

        return {
          id,
          name: opts.name || `Hinge_${target}`,
          duration,
          loop,
          presetType: type,
          tracks: [
            {
              targetComponent: target,
              targetName: target,
              property: 'rotation',
              keyframes: [
                { time: 0, value: [...initRot], interpolation: 'linear' },
                { time: Number((duration * 0.5).toFixed(2)), value: openRot, interpolation: 'linear' },
                { time: Number(duration.toFixed(2)), value: [...initRot], interpolation: 'linear' }
              ]
            }
          ]
        };
      }

      case 'button_press': {
        const depth = opts.pressDepth ?? -0.08;
        const pressedPos: [number, number, number] = [...initPos];
        pressedPos[axisIdx] += depth;

        return {
          id,
          name: opts.name || `Press_${target}`,
          duration,
          loop,
          presetType: type,
          tracks: [
            {
              targetComponent: target,
              targetName: target,
              property: 'position',
              keyframes: [
                { time: 0, value: [...initPos], interpolation: 'linear' },
                { time: Number((duration * 0.25).toFixed(2)), value: pressedPos, interpolation: 'linear' },
                { time: Number((duration * 0.5).toFixed(2)), value: [...initPos], interpolation: 'linear' },
                { time: Number(duration.toFixed(2)), value: [...initPos], interpolation: 'linear' }
              ]
            }
          ]
        };
      }

      case 'spin_continuous': {
        // Continuous 360 degree rotation using 4 intermediate keyframes for clean slerp
        const r0 = [...initRot] as [number, number, number];
        const r1 = [...initRot] as [number, number, number];
        const r2 = [...initRot] as [number, number, number];
        const r3 = [...initRot] as [number, number, number];
        r1[axisIdx] += 120;
        r2[axisIdx] += 240;
        r3[axisIdx] += 360;

        return {
          id,
          name: opts.name || `Spin_${target}`,
          duration,
          loop: 'repeat',
          presetType: type,
          tracks: [
            {
              targetComponent: target,
              targetName: target,
              property: 'rotation',
              keyframes: [
                { time: 0, value: r0, interpolation: 'linear' },
                { time: Number((duration / 3).toFixed(2)), value: r1, interpolation: 'linear' },
                { time: Number(((duration * 2) / 3).toFixed(2)), value: r2, interpolation: 'linear' },
                { time: Number(duration.toFixed(2)), value: r3, interpolation: 'linear' }
              ]
            }
          ]
        };
      }

      case 'mechanical_deploy': {
        const extDist = opts.extendDistance ?? 0.6;
        const deployAngle = opts.deployAngleDeg ?? 45;

        const deployedPos: [number, number, number] = [...initPos];
        deployedPos[axisIdx] += extDist;

        const deployedRot: [number, number, number] = [...initRot];
        deployedRot[(axisIdx + 1) % 3] += deployAngle;

        return {
          id,
          name: opts.name || `Deploy_${target}`,
          duration,
          loop,
          presetType: type,
          tracks: [
            {
              targetComponent: target,
              targetName: target,
              property: 'position',
              keyframes: [
                { time: 0, value: [...initPos], interpolation: 'linear' },
                { time: Number((duration * 0.5).toFixed(2)), value: deployedPos, interpolation: 'linear' },
                { time: Number(duration.toFixed(2)), value: [...initPos], interpolation: 'linear' }
              ]
            },
            {
              targetComponent: target,
              targetName: target,
              property: 'rotation',
              keyframes: [
                { time: 0, value: [...initRot], interpolation: 'linear' },
                { time: Number((duration * 0.5).toFixed(2)), value: deployedRot, interpolation: 'linear' },
                { time: Number(duration.toFixed(2)), value: [...initRot], interpolation: 'linear' }
              ]
            }
          ]
        };
      }

      case 'idle_hover': {
        const amp = opts.amplitude ?? 0.12;
        const upPos: [number, number, number] = [...initPos];
        const downPos: [number, number, number] = [...initPos];
        upPos[1] += amp;
        downPos[1] -= amp;

        return {
          id,
          name: opts.name || `Hover_${target}`,
          duration,
          loop: 'repeat',
          presetType: type,
          tracks: [
            {
              targetComponent: target,
              targetName: target,
              property: 'position',
              keyframes: [
                { time: 0, value: [...initPos], interpolation: 'cubic' },
                { time: Number((duration * 0.25).toFixed(2)), value: upPos, interpolation: 'cubic' },
                { time: Number((duration * 0.5).toFixed(2)), value: [...initPos], interpolation: 'cubic' },
                { time: Number((duration * 0.75).toFixed(2)), value: downPos, interpolation: 'cubic' },
                { time: Number(duration.toFixed(2)), value: [...initPos], interpolation: 'cubic' }
              ]
            }
          ]
        };
      }
    }
  }

  /**
   * Compiles declarative AnimationClipDef definitions into runtime THREE.AnimationClip instances
   * ready for THREE.AnimationMixer and GLTFExporter export.
   */
  public static compileClipToThree(
    clipDef: AnimationClipDef,
    _root?: THREE.Object3D
  ): THREE.AnimationClip {
    const tracks: THREE.KeyframeTrack[] = [];
    const clipDuration = Math.max(0.1, clipDef.duration || 1.0);

    for (const trackDef of clipDef.tracks) {
      if (!trackDef.keyframes || trackDef.keyframes.length === 0) continue;

      // Sort keyframes by time
      const sortedKfs = [...trackDef.keyframes].sort((a, b) => a.time - b.time);
      const times: number[] = [];

      // Determine track interpolation
      const firstInterp = sortedKfs[0]?.interpolation || 'linear';
      let interpolationMode = THREE.InterpolateLinear;
      if (firstInterp === 'step') interpolationMode = THREE.InterpolateDiscrete;
      else if (firstInterp === 'cubic') interpolationMode = THREE.InterpolateSmooth;

      const targetName = trackDef.targetComponent || trackDef.targetName || 'component';

      if (trackDef.property === 'position') {
        const values: number[] = [];
        for (const kf of sortedKfs) {
          times.push(Math.max(0, kf.time));
          values.push(kf.value[0], kf.value[1], kf.value[2]);
        }
        const trackName = `${targetName}.position`;
        tracks.push(new THREE.VectorKeyframeTrack(trackName, times, values, interpolationMode));
      } else if (trackDef.property === 'scale') {
        const values: number[] = [];
        for (const kf of sortedKfs) {
          times.push(Math.max(0, kf.time));
          values.push(kf.value[0], kf.value[1], kf.value[2]);
        }
        const trackName = `${targetName}.scale`;
        tracks.push(new THREE.VectorKeyframeTrack(trackName, times, values, interpolationMode));
      } else if (trackDef.property === 'rotation') {
        // Convert Euler degrees [degX, degY, degZ] to Quaternions [qx, qy, qz, qw]
        const quatValues: number[] = [];
        const euler = new THREE.Euler();
        const quat = new THREE.Quaternion();

        for (const kf of sortedKfs) {
          times.push(Math.max(0, kf.time));
          euler.set(
            THREE.MathUtils.degToRad(kf.value[0]),
            THREE.MathUtils.degToRad(kf.value[1]),
            THREE.MathUtils.degToRad(kf.value[2]),
            'XYZ'
          );
          quat.setFromEuler(euler);
          quatValues.push(quat.x, quat.y, quat.z, quat.w);
        }
        const trackName = `${targetName}.quaternion`;
        tracks.push(new THREE.QuaternionKeyframeTrack(trackName, times, quatValues, interpolationMode));
      }
    }

    const clip = new THREE.AnimationClip(clipDef.name || 'Action', clipDuration, tracks);
    clip.userData = {
      id: clipDef.id,
      loop: clipDef.loop || 'repeat',
      presetType: clipDef.presetType
    };

    return clip;
  }

  /**
   * Compiles an array of clip definitions into Three.js clips.
   */
  public static compileClipsToThree(
    clips?: AnimationClipDef[],
    root?: THREE.Object3D
  ): THREE.AnimationClip[] {
    if (!clips || clips.length === 0) return [];
    return clips.map((clip) => this.compileClipToThree(clip, root));
  }

  /**
   * Clones a clip definition cleanly.
   */
  public static cloneClipDef(clip: AnimationClipDef): AnimationClipDef {
    return {
      id: `anim_${Date.now()}_${Math.floor(Math.random() * 1000)}`,
      name: `${clip.name}_copy`,
      duration: clip.duration,
      loop: clip.loop,
      presetType: clip.presetType,
      tracks: clip.tracks.map((t) => ({
        targetComponent: t.targetComponent || (t as any).targetName,
        targetName: (t as any).targetName || t.targetComponent,
        property: t.property,
        keyframes: t.keyframes.map((k) => ({
          time: k.time,
          value: [...k.value] as [number, number, number],
          interpolation: k.interpolation
        }))
      }))
    };
  }

  /**
   * Validates a clip definition to guarantee integrity before compiling or exporting.
   */
  public static validateClipDef(clip: AnimationClipDef): { valid: boolean; errors: string[] } {
    const errors: string[] = [];
    if (!clip.name || clip.name.trim() === '') {
      errors.push('El nombre de la animación no puede estar vacío.');
    }
    if (typeof clip.duration !== 'number' || clip.duration <= 0) {
      errors.push('La duración de la animación debe ser mayor a 0 segundos.');
    }
    if (!clip.tracks || clip.tracks.length === 0) {
      errors.push('La animación debe contener al menos una pista de componente.');
    } else {
      clip.tracks.forEach((track, i) => {
        const target = track.targetComponent || (track as any).targetName;
        if (!target) {
          errors.push(`La pista ${i + 1} no tiene un componente objetivo definido.`);
        }
        if (!track.keyframes || track.keyframes.length === 0) {
          errors.push(`La pista "${target || 'sin_nombre'}" no tiene fotogramas clave (keyframes).`);
        }
      });
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Generates a set of keyframes between startVal and endVal over duration
   * according to a selected easing / acceleration profile.
   */
  public static applyEasingProfile(
    profile: EasingProfileType,
    duration: number,
    startVal: [number, number, number],
    endVal: [number, number, number]
  ): Array<{ time: number; value: [number, number, number]; interpolation: AnimationInterpolation }> {
    const dur = Math.max(0.1, duration);
    const dX = endVal[0] - startVal[0];
    const dY = endVal[1] - startVal[1];
    const dZ = endVal[2] - startVal[2];

    const lerp = (_tNorm: number, factor: number): [number, number, number] => [
      Number((startVal[0] + dX * factor).toFixed(2)),
      Number((startVal[1] + dY * factor).toFixed(2)),
      Number((startVal[2] + dZ * factor).toFixed(2))
    ];

    switch (profile) {
      case 'linear':
        return [
          { time: 0, value: [...startVal], interpolation: 'linear' },
          { time: Number(dur.toFixed(2)), value: [...endVal], interpolation: 'linear' }
        ];

      case 'ease-in-out':
        return [
          { time: 0, value: [...startVal], interpolation: 'cubic' },
          { time: Number((dur * 0.25).toFixed(2)), value: lerp(0.25, 0.15), interpolation: 'cubic' },
          { time: Number((dur * 0.50).toFixed(2)), value: lerp(0.50, 0.50), interpolation: 'cubic' },
          { time: Number((dur * 0.75).toFixed(2)), value: lerp(0.75, 0.85), interpolation: 'cubic' },
          { time: Number(dur.toFixed(2)), value: [...endVal], interpolation: 'cubic' }
        ];

      case 'bounce':
        // Mechanical spring/bounce with realistic overshoot (18%) and subtle recoil settling (-5%)
        return [
          { time: 0, value: [...startVal], interpolation: 'linear' },
          { time: Number((dur * 0.38).toFixed(2)), value: lerp(0.38, 0.70), interpolation: 'linear' },
          { time: Number((dur * 0.68).toFixed(2)), value: lerp(0.68, 1.18), interpolation: 'linear' },
          { time: Number((dur * 0.86).toFixed(2)), value: lerp(0.86, 0.95), interpolation: 'linear' },
          { time: Number(dur.toFixed(2)), value: [...endVal], interpolation: 'linear' }
        ];

      case 'ease-out':
        // Fast dynamic burst that decelerates smoothly into the target pose
        return [
          { time: 0, value: [...startVal], interpolation: 'cubic' },
          { time: Number((dur * 0.20).toFixed(2)), value: lerp(0.20, 0.55), interpolation: 'cubic' },
          { time: Number((dur * 0.50).toFixed(2)), value: lerp(0.50, 0.85), interpolation: 'cubic' },
          { time: Number((dur * 0.80).toFixed(2)), value: lerp(0.80, 0.97), interpolation: 'cubic' },
          { time: Number(dur.toFixed(2)), value: [...endVal], interpolation: 'cubic' }
        ];

      case 'step':
        return [
          { time: 0, value: [...startVal], interpolation: 'step' },
          { time: Number((dur * 0.50).toFixed(2)), value: lerp(0.50, 0.50), interpolation: 'step' },
          { time: Number(dur.toFixed(2)), value: [...endVal], interpolation: 'step' }
        ];

      default:
        return [
          { time: 0, value: [...startVal], interpolation: 'linear' },
          { time: Number(dur.toFixed(2)), value: [...endVal], interpolation: 'linear' }
        ];
    }
  }
}

export type EasingProfileType = 'ease-in-out' | 'bounce' | 'ease-out' | 'linear' | 'step';
