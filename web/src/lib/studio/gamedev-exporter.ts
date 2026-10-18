import type { ModelSpec } from './types.ts';

/**
 * Sanitizes a model name to be a valid class identifier (PascalCase).
 */
export function toPascalCase(str: string): string {
  const clean = (str || 'ModelCoderAsset')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9_ ]/g, '')
    .trim();
  return clean
    .split(/[\s_-]+/)
    .filter(Boolean)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join('') || 'ModelCoderAsset';
}

/**
 * Generates an idiomatic Godot 4 GDScript integration snippet.
 */
export function generateGodotScript(spec: ModelSpec, filename?: string): string {
  const modelName = spec.name || 'ModelCoder Asset';
  const file = filename || (spec.id ? `${spec.id.split('.').pop()}.glb` : 'model.glb');
  const anims = spec.animations || [];
  const defaultAnim = anims.length > 0 ? anims[0].name : '';

  const animCode = anims.length > 0
    ? `
# Control de animaciones exportadas en GLB (${anims.map(a => `"${a.name}"`).join(', ')})
@onready var anim_player: AnimationPlayer = get_node_or_null("AnimationPlayer")

func _ready() -> void:
\tprint("[ModelCoder] ${modelName} inicializado en la escena.")
\tif anim_player:
\t\tif anim_player.has_animation("${defaultAnim}"):
\t\t\tanim_player.play("${defaultAnim}")
\t\t\tprint("[ModelCoder] Reproduciendo animación inicial: ${defaultAnim}")
\telse:
\t\tpush_warning("[ModelCoder] No se encontró AnimationPlayer en los hijos.")

func play_clip(clip_name: String) -> void:
\tif anim_player and anim_player.has_animation(clip_name):
\t\tanim_player.play(clip_name)
\telse:
\t\tpush_warning("[ModelCoder] Clip no encontrado: " + clip_name)

func stop_clip() -> void:
\tif anim_player:
\t\tanim_player.stop()
`
    : `
func _ready() -> void:
\tprint("[ModelCoder] ${modelName} instanciado correctamente.")
`;

  return `# ==============================================================================
# ModelCoder -> Godot 4 Integration Helper
# Asset: ${modelName}
# Archivo GLB: res://assets/${file}
# Piezas geométricas: ${spec.components.length} | Animaciones: ${anims.length}
# ==============================================================================
extends Node3D
class_name ${toPascalCase(modelName)}
${animCode.trim()}
`;
}

/**
 * Generates an idiomatic Unity C# MonoBehaviour component snippet.
 */
export function generateUnityScript(spec: ModelSpec, filename?: string): string {
  const modelName = spec.name || 'ModelCoder Asset';
  const className = `${toPascalCase(modelName)}Controller`;
  const file = filename || (spec.id ? `${spec.id.split('.').pop()}.glb` : 'model.glb');
  const anims = spec.animations || [];
  const defaultAnim = anims.length > 0 ? anims[0].name : '';

  const animCode = anims.length > 0
    ? `
    private Animator animator;

    void Awake()
    {
        animator = GetComponentInChildren<Animator>();
    }

    void Start()
    {
        Debug.Log("[ModelCoder] ${modelName} instanciado.");
        if (animator != null)
        {
            // Reproducir clip por defecto: "${defaultAnim}"
            animator.Play("${defaultAnim}");
        }
    }

    /// <summary>
    /// Reproduce cualquiera de las animaciones exportadas: ${anims.map(a => a.name).join(', ')}
    /// </summary>
    public void PlayClip(string clipName)
    {
        if (animator != null)
        {
            animator.Play(clipName);
        }
        else
        {
            Debug.LogWarning("[ModelCoder] Animator no asignado en " + gameObject.name);
        }
    }
`
    : `
    void Start()
    {
        Debug.Log("[ModelCoder] ${modelName} instanciado correctamente.");
    }
`;

  return `// ==============================================================================
// ModelCoder -> Unity Integration Component
// Asset: ${modelName}
// Archivo: Assets/${file}
// Piezas geométricas: ${spec.components.length} | Animaciones: ${anims.length}
// ==============================================================================
using UnityEngine;

[DisallowMultipleComponent]
public class ${className} : MonoBehaviour
{
${animCode.trim()}
}
`;
}

/**
 * Generates an idiomatic Three.js / Web loader snippet.
 */
export function generateThreeJsScript(spec: ModelSpec, filename?: string): string {
  const modelName = spec.name || 'ModelCoder Asset';
  const file = filename || (spec.id ? `${spec.id.split('.').pop()}.glb` : 'model.glb');
  const fnName = `load${toPascalCase(modelName)}`;
  const anims = spec.animations || [];

  return `// ==============================================================================
// ModelCoder -> Three.js / Web Loader
// Asset: ${modelName}
// Archivo: /models/${file}
// ==============================================================================
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export interface LoadedModelCoderAsset {
  scene: THREE.Group;
  mixer: THREE.AnimationMixer | null;
  clips: THREE.AnimationClip[];
  playClip: (name: string) => void;
  update: (deltaSeconds: number) => void;
}

/**
 * Carga e inicializa ${modelName} con soporte completo para sus ${anims.length} animación(es).
 */
export async function ${fnName}(
  targetScene: THREE.Scene,
  url = '/models/${file}'
): Promise<LoadedModelCoderAsset> {
  const loader = new GLTFLoader();
  const gltf = await loader.loadAsync(url);
  targetScene.add(gltf.scene);

  let mixer: THREE.AnimationMixer | null = null;
  const actionsMap = new Map<string, THREE.AnimationAction>();

  if (gltf.animations && gltf.animations.length > 0) {
    mixer = new THREE.AnimationMixer(gltf.scene);
    gltf.animations.forEach((clip) => {
      const action = mixer!.clipAction(clip);
      actionsMap.set(clip.name, action);
    });

    // Reproducir primera animación por defecto
    const firstClip = gltf.animations[0];
    actionsMap.get(firstClip.name)?.play();
  }

  return {
    scene: gltf.scene,
    mixer,
    clips: gltf.animations || [],
    playClip: (clipName: string) => {
      const action = actionsMap.get(clipName);
      if (action) {
        action.reset().play();
      }
    },
    update: (delta: number) => {
      if (mixer) mixer.update(delta);
    }
  };
}
`;
}

/**
 * Generates an idiomatic Godot 4 Scene (.tscn) with StaticBody3D and CollisionShape3D.
 */
export function generateGodotScene(spec: ModelSpec, filename?: string): string {
  const modelName = spec.name || 'ModelCoder Asset';
  const cleanId = (spec.id ? spec.id.split('.').pop() : 'model') || 'model';
  const glbFile = filename || `${cleanId}.glb`;
  const pascalName = toPascalCase(modelName);

  const dims = spec.dimensions || { width: 1.0, height: 1.0, depth: 1.0 };
  const w = Number(dims.width) || 1.0;
  const h = Number(dims.height) || 1.0;
  const d = Number(dims.depth) || 1.0;
  const centerY = (h / 2).toFixed(4);

  return `[gd_scene load_steps=3 format=3 uid="uid://modelcoder_${cleanId}"]

[ext_resource type="PackedScene" uid="uid://mesh_${cleanId}" path="res://assets/${glbFile}" id="1_mesh"]

[sub_resource type="BoxShape3D" id="BoxShape3D_root"]
size = Vector3(${w.toFixed(4)}, ${h.toFixed(4)}, ${d.toFixed(4)})

[node name="${pascalName}" type="StaticBody3D"]

[node name="${pascalName}Mesh" parent="." instance=ExtResource("1_mesh")]

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, ${centerY}, 0)
shape = SubResource("BoxShape3D_root")
`;
}

/**
 * Generates snippets for all game engine platforms and scene configurations.
 */
export function generateAllSnippets(spec: ModelSpec, filename?: string) {
  return {
    godot: generateGodotScript(spec, filename),
    godotScene: generateGodotScene(spec, filename),
    unity: generateUnityScript(spec, filename),
    threejs: generateThreeJsScript(spec, filename)
  };
}
