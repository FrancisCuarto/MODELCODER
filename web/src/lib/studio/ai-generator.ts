import * as THREE from 'three';
import type { ModelSpec, ComponentDef } from './types.ts';
import { ProceduralMemory } from './procedural-memory.ts';
import { ProceduralEngine } from './procedural-engine.ts';
import { CodeSandbox } from './code-sandbox.ts';
import {
  ProceduralKnowledgeDB,
  createSeededPRNG,
  hashPromptString,
  type WikidataKnowledgeResult,
  type KnowledgeSynthesisMetadata
} from './procedural-knowledge-db.ts';

export type AIProviderType =
  | 'gemini'
  | 'openai'
  | 'openrouter'
  | 'groq'
  | 'deepseek'
  | 'anthropic'
  | 'ollama'
  | 'custom';

export type AIOutputFormat = 'json' | 'dsl';
export type AIAgentMode = 'create' | 'agent' | 'vision_critique';

export interface AIProviderPreset {
  id: AIProviderType;
  label: string;
  baseUrl: string;
  requiresKey: boolean;
  keyPlaceholder: string;
  keyHelpUrl?: string;
  defaultModels: { id: string; label: string }[];
}

export interface AgentToolAction {
  action:
    | 'add_component'
    | 'update_component'
    | 'delete_component'
    | 'mirror_component'
    | 'reparent_component'
    | 'apply_material_all'
    | 'add_animation'
    | 'align_to_ground'
    | 'replace_spec';
  component?: Partial<ComponentDef>;
  targetName?: string;
  changes?: Partial<ComponentDef>;
  axis?: 'x' | 'y' | 'z';
  newName?: string;
  parentId?: string;
  texturePreset?: string;
  color?: string;
  wear?: number;
  roughness?: number;
  metalness?: number;
  animation?: any;
  preset?: string;
  duration?: number;
  spec?: ModelSpec;
}

export interface GenerationConfig {
  engine?: 'ai' | 'local';
  provider?: AIProviderType;
  apiKey?: string;
  baseUrl?: string;
  forceFresh?: boolean;
  model?: string;
  outputFormat?: AIOutputFormat;
  agentMode?: AIAgentMode;
  currentSpec?: ModelSpec;
  viewportImageBase64?: string;
  seed?: number;
  enableWikidataLookup?: boolean;
}

export class AIGenerator {
  public static readonly PROVIDER_PRESETS: Record<AIProviderType, AIProviderPreset> = {
    gemini: {
      id: 'gemini',
      label: 'Google Gemini',
      baseUrl: 'https://generativelanguage.googleapis.com/v1beta',
      requiresKey: true,
      keyPlaceholder: 'AIzaSy...',
      keyHelpUrl: 'https://aistudio.google.com/app/apikey',
      defaultModels: [
        { id: 'auto', label: '🔄 Automático (Cascada Resiliente)' },
        { id: 'gemini-2.5-flash', label: '🚀 Gemini 2.5 Flash (Recomendado)' },
        { id: 'gemini-2.5-pro', label: '🧠 Gemini 2.5 Pro (Máxima precisión 3D)' },
        { id: 'gemini-2.0-flash', label: '🌐 Gemini 2.0 Flash' },
        { id: 'gemini-3.8-flash', label: '⚡ Gemini 3.8 Flash' },
        { id: 'gemini-2.5-flash-lite', label: '⚡ Gemini 2.5 Flash-Lite' },
        { id: 'gemini-1.5-flash', label: '🛡️ Gemini 1.5 Flash' }
      ]
    },
    openai: {
      id: 'openai',
      label: 'OpenAI (GPT-4o / o3)',
      baseUrl: 'https://api.openai.com/v1',
      requiresKey: true,
      keyPlaceholder: 'sk-proj-...',
      keyHelpUrl: 'https://platform.openai.com/api-keys',
      defaultModels: [
        { id: 'gpt-4o', label: '🧠 GPT-4o (Multimodal + 3D)' },
        { id: 'gpt-4o-mini', label: '⚡ GPT-4o Mini (Rápido)' },
        { id: 'o3-mini', label: '🔬 o3-mini (Razonamiento Espacial)' },
        { id: 'gpt-4.1', label: '🚀 GPT-4.1' },
        { id: 'gpt-4.1-mini', label: '⚡ GPT-4.1 Mini' }
      ]
    },
    openrouter: {
      id: 'openrouter',
      label: 'OpenRouter (200+ Modelos)',
      baseUrl: 'https://openrouter.ai/api/v1',
      requiresKey: true,
      keyPlaceholder: 'sk-or-v1-...',
      keyHelpUrl: 'https://openrouter.ai/keys',
      defaultModels: [
        { id: 'anthropic/claude-3.7-sonnet', label: '🎭 Claude 3.7 Sonnet' },
        { id: 'google/gemini-2.5-pro-preview', label: '🧠 Gemini 2.5 Pro' },
        { id: 'deepseek/deepseek-chat-v3-0324:free', label: '🐳 DeepSeek V3 (Gratis)' },
        { id: 'qwen/qwen-2.5-coder-32b-instruct', label: '💻 Qwen 2.5 Coder 32B' },
        { id: 'meta-llama/llama-3.3-70b-instruct', label: '🦙 Llama 3.3 70B' },
        { id: 'openai/gpt-4o-mini', label: '⚡ GPT-4o Mini' }
      ]
    },
    groq: {
      id: 'groq',
      label: 'Groq (Inferencia Ultra-Rápida)',
      baseUrl: 'https://api.groq.com/openai/v1',
      requiresKey: true,
      keyPlaceholder: 'gsk_...',
      keyHelpUrl: 'https://console.groq.com/keys',
      defaultModels: [
        { id: 'llama-3.3-70b-versatile', label: '🦙 Llama 3.3 70B Versatile' },
        { id: 'deepseek-r1-distill-llama-70b', label: '🧠 DeepSeek R1 Distill 70B' },
        { id: 'qwen-qwq-32b', label: '💻 Qwen QwQ 32B' },
        { id: 'llama-3.1-8b-instant', label: '⚡ Llama 3.1 8B Instant' }
      ]
    },
    deepseek: {
      id: 'deepseek',
      label: 'DeepSeek (V3 / R1)',
      baseUrl: 'https://api.deepseek.com/v1',
      requiresKey: true,
      keyPlaceholder: 'sk-...',
      keyHelpUrl: 'https://platform.deepseek.com/api_keys',
      defaultModels: [
        { id: 'deepseek-chat', label: '🐳 DeepSeek V3 (Chat / Coder)' },
        { id: 'deepseek-reasoner', label: '🧠 DeepSeek R1 (Reasoner)' }
      ]
    },
    anthropic: {
      id: 'anthropic',
      label: 'Anthropic (Claude)',
      baseUrl: 'https://api.anthropic.com/v1',
      requiresKey: true,
      keyPlaceholder: 'sk-ant-...',
      keyHelpUrl: 'https://console.anthropic.com/settings/keys',
      defaultModels: [
        { id: 'claude-3-7-sonnet-latest', label: '🎭 Claude 3.7 Sonnet' },
        { id: 'claude-3-5-sonnet-latest', label: '🎭 Claude 3.5 Sonnet' },
        { id: 'claude-3-5-haiku-latest', label: '⚡ Claude 3.5 Haiku' }
      ]
    },
    ollama: {
      id: 'ollama',
      label: 'Ollama / LM Studio (IA Local)',
      baseUrl: 'http://localhost:11434/v1',
      requiresKey: false,
      keyPlaceholder: 'ollama (No requiere clave)',
      defaultModels: [
        { id: 'qwen2.5-coder:14b', label: '💻 Qwen 2.5 Coder 14B (Local)' },
        { id: 'qwen2.5-coder:7b', label: '💻 Qwen 2.5 Coder 7B (Local)' },
        { id: 'llama3.2:latest', label: '🦙 Llama 3.2 (Local)' },
        { id: 'deepseek-r1:14b', label: '🧠 DeepSeek R1 14B (Local)' },
        { id: 'mistral:latest', label: '🌪️ Mistral 7B (Local)' },
        { id: 'llava:latest', label: '👁️ LLaVA Vision (Local)' }
      ]
    },
    custom: {
      id: 'custom',
      label: 'Endpoint OpenAI-Compatible',
      baseUrl: 'http://localhost:1234/v1',
      requiresKey: false,
      keyPlaceholder: 'Clave API opcional...',
      defaultModels: [
        { id: 'local-model', label: '🖥️ Modelo Personalizado / Local' }
      ]
    }
  };

  /**
   * Generates or mutates a structured ModelSpec from a natural language user prompt.
   * Supports:
   * - Multi-Provider AI (Gemini, OpenAI, OpenRouter, Groq, DeepSeek, Anthropic, Ollama, Custom)
   * - JSON Spec synthesis OR JavaScript DSL (ProceduralBuilderContext) synthesis
   * - Conversational Agent Mode (incremental tool-calling edits over currentSpec)
   * - Multimodal Vision Self-Critique (inspects 3D viewport capture + spec to repair geometry)
   * - Deterministic Local Procedural Engine & Memory
   */
  public static async generateModel(
    prompt: string,
    configOrKey?: string | GenerationConfig
  ): Promise<{
    spec: ModelSpec;
    rawResponse?: string;
    dslCode?: string;
    synthesizedDsl?: string;
    agentActions?: AgentToolAction[];
    agentSummary?: string;
    source: 'gemini' | 'ai_provider' | 'llm_provider' | 'agent_edit' | 'local' | 'local_memory' | 'cloud_memory' | 'gemini_fallback';
    usedModel?: string;
    usedProvider?: AIProviderType;
    knowledgeMetadata?: KnowledgeSynthesisMetadata;
  }> {
    const cleanPrompt = prompt.trim();
    if (!cleanPrompt) {
      throw new Error('El prompt no puede estar vacío.');
    }

    let engine: 'ai' | 'local' = 'local';
    let provider: AIProviderType = 'gemini';
    let apiKey: string | undefined = undefined;
    let baseUrl: string | undefined = undefined;
    let forceFresh = false;
    let model: string | undefined = undefined;
    let outputFormat: AIOutputFormat = 'json';
    let agentMode: AIAgentMode = 'create';
    let currentSpec: ModelSpec | undefined = undefined;
    let viewportImageBase64: string | undefined = undefined;
    let seed: number | undefined = undefined;
    let enableWikidataLookup = false;

    if (typeof configOrKey === 'string') {
      apiKey = configOrKey;
      engine = (apiKey && apiKey.trim().length > 10) ? 'ai' : 'local';
    } else if (configOrKey) {
      engine = configOrKey.engine || 'local';
      provider = configOrKey.provider || 'gemini';
      apiKey = configOrKey.apiKey;
      baseUrl = configOrKey.baseUrl;
      forceFresh = configOrKey.forceFresh ?? (engine === 'ai');
      model = configOrKey.model;
      outputFormat = configOrKey.outputFormat || 'json';
      agentMode = configOrKey.agentMode || 'create';
      currentSpec = configOrKey.currentSpec;
      viewportImageBase64 = configOrKey.viewportImageBase64;
      seed = configOrKey.seed;
      enableWikidataLookup = configOrKey.enableWikidataLookup ?? false;
    }

    const preset = this.PROVIDER_PRESETS[provider] || this.PROVIDER_PRESETS.gemini;

    // =========================================================================
    // MODO IA MULTI-PROVEEDOR Y AGENTES
    // =========================================================================
    if (engine === 'ai') {
      if (preset.requiresKey && (!apiKey || apiKey.trim().length <= 5)) {
        if (provider === 'gemini') {
          throw new Error('Para usar la IA Generativa necesitas ingresar tu clave gratuita de Google Gemini en el botón [🔑 CONECTAR GEMINI].');
        }
        throw new Error(`Para usar ${preset.label} necesitas ingresar tu API Key en el panel [🔑 CONFIGURAR IA].`);
      }

      try {
        // 1. Conversational Agent Mode or Vision Self-Critique over an existing model
        if ((agentMode === 'agent' || agentMode === 'vision_critique') && currentSpec && currentSpec.components?.length > 0) {
          const agentRes = await this.runAgentTurn(cleanPrompt, currentSpec, {
            provider,
            apiKey: apiKey?.trim(),
            baseUrl: baseUrl?.trim() || preset.baseUrl,
            model,
            outputFormat,
            agentMode,
            viewportImageBase64
          });
          return {
            spec: agentRes.spec,
            rawResponse: agentRes.rawResponse,
            dslCode: agentRes.dslCode,
            synthesizedDsl: agentRes.dslCode,
            agentActions: agentRes.actions,
            agentSummary: agentRes.summary,
            source: provider === 'gemini' ? 'gemini' : 'ai_provider',
            usedModel: agentRes.usedModel,
            usedProvider: provider
          };
        }

        // 2. Fresh 3D Creation Mode (JSON Spec or Procedural DSL)
        const aiRes = await this.callMultiProviderLLM(cleanPrompt, {
          provider,
          apiKey: apiKey?.trim(),
          baseUrl: baseUrl?.trim() || preset.baseUrl,
          model,
          outputFormat,
          viewportImageBase64
        });
        const normalizedSpec = this.normalizeSpecGeometry(aiRes.spec);
        return {
          spec: normalizedSpec,
          rawResponse: aiRes.rawResponse,
          dslCode: aiRes.dslCode,
          synthesizedDsl: aiRes.dslCode,
          source: provider === 'gemini' ? 'gemini' : 'ai_provider',
          usedModel: aiRes.usedModel,
          usedProvider: provider
        };
      } catch (aiErr: any) {
        console.warn(`[AIGenerator] Proveedor ${provider} devolvió error o está saturado. Activando auto-fallback inteligente:`, aiErr);

        // If in Agent Mode and LLM failed, apply deterministic local agent edits over currentSpec
        if ((agentMode === 'agent' || agentMode === 'vision_critique') && currentSpec && currentSpec.components?.length > 0) {
          const localAgent = this.applyLocalHeuristicAgentEdit(cleanPrompt, currentSpec);
          return {
            spec: localAgent.spec,
            agentActions: localAgent.actions,
            agentSummary: localAgent.summary,
            source: 'gemini_fallback',
            rawResponse: aiErr.message,
            usedProvider: provider
          };
        }

        // Fallback procedural de alta fidelidad para garantizar que el usuario SIEMPRE obtenga su modelo 3D
        const rawSpec = this.synthesizeProceduralSpec(cleanPrompt, { seed });
        const spec = this.normalizeSpecGeometry(rawSpec);
        return {
          spec,
          source: 'gemini_fallback',
          rawResponse: aiErr.message,
          usedProvider: provider
        };
      }
    }

    // =========================================================================
    // MODO MOTOR PROCEDURAL LOCAL (CON BASE DE CONOCIMIENTO Y AGENTE HEURÍSTICO)
    // =========================================================================
    if ((agentMode === 'agent' || agentMode === 'vision_critique') && currentSpec && currentSpec.components?.length > 0) {
      const localAgent = this.applyLocalHeuristicAgentEdit(cleanPrompt, currentSpec);
      return {
        spec: localAgent.spec,
        agentActions: localAgent.actions,
        agentSummary: localAgent.summary,
        source: 'local'
      };
    }

    if (!forceFresh && seed === undefined) {
      const learned = await ProceduralMemory.findLearnedModel(cleanPrompt);
      if (learned) {
        return { spec: this.normalizeSpecGeometry(learned.spec), source: learned.source };
      }
    }

    // Optional live Wikidata knowledge lookup for real-world vehicles/objects
    let wikidataInfo: WikidataKnowledgeResult | null = null;
    if (enableWikidataLookup) {
      wikidataInfo = await ProceduralKnowledgeDB.queryWikidataKnowledge(cleanPrompt);
    }

    const rawSpec = this.synthesizeProceduralSpec(cleanPrompt, { seed, wikidata: wikidataInfo });
    const spec = this.normalizeSpecGeometry(rawSpec);
    if (seed === undefined) {
      await ProceduralMemory.recordLearnedModel(cleanPrompt, spec);
    }
    return {
      spec,
      source: 'local',
      knowledgeMetadata: (rawSpec as any)._knowledgeMetadata
    };
  }

  /**
   * Mathematically normalizes, sanitizes, and ground-aligns a ModelSpec.
   * Guarantees:
   * 1. All component names are unique and valid.
   * 2. Coordinates, sizes, and rotations are valid finite numbers in degrees/meters.
   * 3. Model is automatically grounded so its lowest contact point touches floor at Y = 0.
   * 4. Overall bounding box dimensions are verified.
   */
  /**
   * Converts world-space coordinates from generative models into clean Three.js
   * parent-local coordinates for all components with parentId.
   * This guarantees that hierarchical pieces appear at their exact intended
   * 3D world positions without doubling parent transforms.
   */
  public static convertWorldToLocalHierarchy(spec: ModelSpec): ModelSpec {
    if (!spec || !Array.isArray(spec.components) || spec.components.length === 0) {
      return spec;
    }

    const compMap = new Map<string, ComponentDef>();
    for (const comp of spec.components) {
      if (comp.name) compMap.set(comp.name, comp);
    }

    // Build parent-to-children adjacency map
    const childrenMap = new Map<string, ComponentDef[]>();
    const roots: ComponentDef[] = [];

    for (const comp of spec.components) {
      if (comp.parentId && compMap.has(comp.parentId) && comp.parentId !== comp.name) {
        if (!childrenMap.has(comp.parentId)) {
          childrenMap.set(comp.parentId, []);
        }
        childrenMap.get(comp.parentId)!.push(comp);
      } else {
        roots.push(comp);
      }
    }

    // If no parent-child relationships exist, nothing to convert
    if (childrenMap.size === 0) {
      return spec;
    }

    // Compute initial world matrices for all components assuming positions/rotations are in world space
    const worldMatrices = new Map<string, THREE.Matrix4>();
    for (const comp of spec.components) {
      const pos = new THREE.Vector3(
        Array.isArray(comp.position) && Number.isFinite(comp.position[0]) ? comp.position[0] : 0,
        Array.isArray(comp.position) && Number.isFinite(comp.position[1]) ? comp.position[1] : 0,
        Array.isArray(comp.position) && Number.isFinite(comp.position[2]) ? comp.position[2] : 0
      );
      const euler = new THREE.Euler(
        THREE.MathUtils.degToRad(Array.isArray(comp.rotation) && Number.isFinite(comp.rotation[0]) ? comp.rotation[0] : 0),
        THREE.MathUtils.degToRad(Array.isArray(comp.rotation) && Number.isFinite(comp.rotation[1]) ? comp.rotation[1] : 0),
        THREE.MathUtils.degToRad(Array.isArray(comp.rotation) && Number.isFinite(comp.rotation[2]) ? comp.rotation[2] : 0),
        'XYZ'
      );
      const quat = new THREE.Quaternion().setFromEuler(euler);
      const scale = new THREE.Vector3(
        Array.isArray(comp.scale) && Number.isFinite(comp.scale[0]) && comp.scale[0] > 0 ? comp.scale[0] : 1,
        Array.isArray(comp.scale) && Number.isFinite(comp.scale[1]) && comp.scale[1] > 0 ? comp.scale[1] : 1,
        Array.isArray(comp.scale) && Number.isFinite(comp.scale[2]) && comp.scale[2] > 0 ? comp.scale[2] : 1
      );
      const mat = new THREE.Matrix4().compose(pos, quat, scale);
      worldMatrices.set(comp.name, mat);
    }

    // Traverse breadth-first starting from root nodes
    const queue = [...roots];
    const visited = new Set<string>();

    while (queue.length > 0) {
      const parent = queue.shift()!;
      if (visited.has(parent.name)) continue;
      visited.add(parent.name);

      const children = childrenMap.get(parent.name) || [];
      const parentWorldMat = worldMatrices.get(parent.name)!;
      const invParentWorld = parentWorldMat.clone().invert();

      for (const child of children) {
        const childWorldMat = worldMatrices.get(child.name)!;
        // childLocal = inv(parentWorld) * childWorld
        const localMat = new THREE.Matrix4().multiplyMatrices(invParentWorld, childWorldMat);

        const localPos = new THREE.Vector3();
        const localQuat = new THREE.Quaternion();
        const localScale = new THREE.Vector3();
        localMat.decompose(localPos, localQuat, localScale);

        const localEuler = new THREE.Euler().setFromQuaternion(localQuat, 'XYZ');

        child.position = [
          parseFloat(localPos.x.toFixed(4)),
          parseFloat(localPos.y.toFixed(4)),
          parseFloat(localPos.z.toFixed(4))
        ];
        child.rotation = [
          parseFloat(THREE.MathUtils.radToDeg(localEuler.x).toFixed(2)),
          parseFloat(THREE.MathUtils.radToDeg(localEuler.y).toFixed(2)),
          parseFloat(THREE.MathUtils.radToDeg(localEuler.z).toFixed(2))
        ];

        queue.push(child);
      }
    }

    return spec;
  }

  public static normalizeSpecGeometry(spec: ModelSpec): ModelSpec {
    if (!spec || !Array.isArray(spec.components) || spec.components.length === 0) {
      return spec;
    }

    const usedNames = new Set<string>();
    for (let i = 0; i < spec.components.length; i++) {
      const comp = spec.components[i];
      if (!comp.name || typeof comp.name !== 'string' || comp.name.trim() === '') {
        comp.name = `comp_${i + 1}`;
      } else {
        comp.name = comp.name.trim().replace(/\s+/g, '_');
      }

      if (usedNames.has(comp.name)) {
        comp.name = `${comp.name}_${i + 1}`;
      }
      usedNames.add(comp.name);

      const validShapes = [
        'box',
        'cylinder',
        'sphere',
        'plane',
        'cone',
        'torus',
        'capsule',
        'wedge',
        'chamfer_box',
        'pipe',
        'prism',
        'pyramid',
        'mesh'
      ];
      if (!comp.shape || !validShapes.includes(comp.shape)) {
        comp.shape = 'box';
      }

      if (!Array.isArray(comp.size) || comp.size.length === 0) {
        comp.size = [1, 1, 1];
      } else {
        comp.size = comp.size.map((v) => (typeof v === 'number' && Number.isFinite(v) && v > 0.001 ? Math.abs(v) : 0.5));
      }

      if (comp.shape === 'box' || comp.shape === 'wedge') {
        while (comp.size.length < 3) comp.size.push(1);
      } else if (comp.shape === 'chamfer_box') {
        while (comp.size.length < 3) comp.size.push(1);
        if (comp.size.length < 4) comp.size.push(0.02);
        if (comp.size.length < 5) comp.size.push(1);
      } else if (comp.shape === 'cylinder') {
        while (comp.size.length < 3) comp.size.push(comp.size[0] || 0.5);
        if (comp.size.length < 4) comp.size.push(10);
      } else if (comp.shape === 'pipe') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(comp.size[0] * 0.7);
        if (comp.size.length < 3) comp.size.push(1.0);
        if (comp.size.length < 4) comp.size.push(12);
        if (comp.size[1] >= comp.size[0]) comp.size[1] = comp.size[0] * 0.7;
      } else if (comp.shape === 'prism') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(1.0);
        if (comp.size.length < 3) comp.size.push(6);
      } else if (comp.shape === 'pyramid') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(1.0);
        if (comp.size.length < 3) comp.size.push(4);
      } else if (comp.shape === 'sphere') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(10);
        if (comp.size.length < 3) comp.size.push(8);
      } else if (comp.shape === 'cone') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(1.0);
        if (comp.size.length < 3) comp.size.push(8);
      } else if (comp.shape === 'torus') {
        if (comp.size.length < 1) comp.size.push(0.5);
        if (comp.size.length < 2) comp.size.push(0.15);
        if (comp.size.length < 3) comp.size.push(6);
        if (comp.size.length < 4) comp.size.push(12);
      } else if (comp.shape === 'capsule') {
        if (comp.size.length < 1) comp.size.push(0.25);
        if (comp.size.length < 2) comp.size.push(0.5);
        if (comp.size.length < 3) comp.size.push(4);
        if (comp.size.length < 4) comp.size.push(8);
      } else if (comp.shape === 'plane') {
        while (comp.size.length < 2) comp.size.push(1);
      }

      if (!Array.isArray(comp.position) || comp.position.length < 3) {
        comp.position = [0, 0, 0];
      } else {
        comp.position = [
          Number.isFinite(comp.position[0]) ? parseFloat(comp.position[0].toFixed(4)) : 0,
          Number.isFinite(comp.position[1]) ? parseFloat(comp.position[1].toFixed(4)) : 0,
          Number.isFinite(comp.position[2]) ? parseFloat(comp.position[2].toFixed(4)) : 0
        ];
      }

      if (!Array.isArray(comp.rotation) || comp.rotation.length < 3) {
        comp.rotation = [0, 0, 0];
      } else {
        let rx = Number.isFinite(comp.rotation[0]) ? parseFloat(comp.rotation[0].toFixed(2)) : 0;
        let ry = Number.isFinite(comp.rotation[1]) ? parseFloat(comp.rotation[1].toFixed(2)) : 0;
        let rz = Number.isFinite(comp.rotation[2]) ? parseFloat(comp.rotation[2].toFixed(2)) : 0;

        const snapOrthogonal = (deg: number): number | null => {
          const d = ((deg % 360) + 360) % 360;
          if (Math.abs(d - 0) < 5 || Math.abs(d - 360) < 5) return 0;
          if (Math.abs(d - 90) < 5) return 90;
          if (Math.abs(d - 180) < 5) return 180;
          if (Math.abs(d - 270) < 5) return -90;
          return null;
        };

        const rxSnap = snapOrthogonal(rx);
        if (rxSnap !== null) rx = rxSnap;
        else if (Math.abs(rx) <= 30) rx = parseFloat(rx.toFixed(1));
        else rx = 0;

        const rySnap = snapOrthogonal(ry);
        if (rySnap !== null) ry = rySnap;
        else ry = 0;

        const rzSnap = snapOrthogonal(rz);
        if (rzSnap !== null) rz = rzSnap;
        else rz = 0;

        comp.rotation = [rx, ry, rz];
      }

      if (Array.isArray(comp.scale) && comp.scale.length >= 3) {
        comp.scale = [
          Number.isFinite(comp.scale[0]) && comp.scale[0] > 0.001 ? parseFloat(comp.scale[0].toFixed(3)) : 1,
          Number.isFinite(comp.scale[1]) && comp.scale[1] > 0.001 ? parseFloat(comp.scale[1].toFixed(3)) : 1,
          Number.isFinite(comp.scale[2]) && comp.scale[2] > 0.001 ? parseFloat(comp.scale[2].toFixed(3)) : 1
        ];
      } else if (comp.scale) {
        delete comp.scale;
      }

      // Hinge / Articulation Pivot offset
      if (Array.isArray(comp.pivot) && comp.pivot.length >= 3) {
        comp.pivot = [
          Number.isFinite(comp.pivot[0]) ? parseFloat(comp.pivot[0].toFixed(4)) : 0,
          Number.isFinite(comp.pivot[1]) ? parseFloat(comp.pivot[1].toFixed(4)) : 0,
          Number.isFinite(comp.pivot[2]) ? parseFloat(comp.pivot[2].toFixed(4)) : 0
        ];
      } else if (comp.pivot) {
        delete comp.pivot;
      }

      // Array Modifier sanitization
      if (comp.array && typeof comp.array === 'object') {
        const arr = comp.array;
        const isRadial = arr.type === 'radial';
        const count = Math.max(2, Math.min(64, Math.round(Number(arr.count) || 2)));
        if (isRadial) {
          comp.array = {
            enabled: arr.enabled !== false,
            type: 'radial',
            count,
            radialAxis: ['x', 'y', 'z'].includes(arr.radialAxis as any) ? arr.radialAxis : 'y',
            radialRadius: Number.isFinite(arr.radialRadius) ? Math.min(0.40, Math.max(0, parseFloat((arr.radialRadius as number).toFixed(4)))) : 0.35,
            radialAngle: Number.isFinite(arr.radialAngle) ? parseFloat((arr.radialAngle as number).toFixed(2)) : 360,
            radialRotateCopies: arr.radialRotateCopies !== false
          };
        } else {
          const off = Array.isArray(arr.offset) && arr.offset.length >= 3
            ? [
                Number.isFinite(arr.offset[0]) ? parseFloat(arr.offset[0].toFixed(4)) : 0,
                Number.isFinite(arr.offset[1]) ? parseFloat(arr.offset[1].toFixed(4)) : 0,
                Number.isFinite(arr.offset[2]) ? parseFloat(arr.offset[2].toFixed(4)) : 0
              ] as [number, number, number]
            : [0, 0.1, 0] as [number, number, number];
          comp.array = {
            enabled: arr.enabled !== false,
            type: 'linear',
            count,
            offset: off
          };
        }
      } else if (comp.array) {
        delete comp.array;
      }

      // Boolean Modifier sanitization
      if (comp.boolean && typeof comp.boolean === 'object') {
        const b = comp.boolean;
        const op = ['difference', 'union', 'intersection'].includes(b.operation) ? b.operation : 'difference';
        const target = typeof b.targetComponent === 'string' ? b.targetComponent.trim().replace(/\s+/g, '_') : '';
        if (target && target !== comp.name) {
          comp.boolean = {
            enabled: b.enabled !== false,
            operation: op as any,
            targetComponent: target,
            hideTarget: b.hideTarget !== false
          };
        } else {
          delete comp.boolean;
        }
      } else if (comp.boolean) {
        delete comp.boolean;
      }

      // Material weathering, relief & emissive
      if (typeof comp.wear === 'number' && Number.isFinite(comp.wear)) {
        comp.wear = Math.max(0, Math.min(1, parseFloat(comp.wear.toFixed(2))));
      }
      if (typeof comp.normalStrength === 'number' && Number.isFinite(comp.normalStrength)) {
        comp.normalStrength = Math.max(0, Math.min(2, parseFloat(comp.normalStrength.toFixed(2))));
      }
      if (comp.emissive && typeof comp.emissive === 'string') {
        comp.emissive = comp.emissive.trim();
        if (typeof comp.emissiveIntensity === 'number' && Number.isFinite(comp.emissiveIntensity)) {
          comp.emissiveIntensity = Math.max(0, parseFloat(comp.emissiveIntensity.toFixed(2)));
        } else {
          comp.emissiveIntensity = 1.0;
        }
      }

      if (!comp.color || typeof comp.color !== 'string') {
        comp.color = '#718096';
      }
    }

    // Second pass: Validate hierarchy parenting and boolean target cross-references
    const compNameSet = new Set(spec.components.map((c) => c.name));
    for (const comp of spec.components) {
      if (comp.parentId && typeof comp.parentId === 'string') {
        const cleanParent = comp.parentId.trim().replace(/\s+/g, '_');
        if (
          cleanParent !== comp.name &&
          compNameSet.has(cleanParent) &&
          !ProceduralEngine.wouldCreateCycle(spec.components, comp.name, cleanParent)
        ) {
          comp.parentId = cleanParent;
        } else {
          delete comp.parentId;
        }
      } else {
        delete comp.parentId;
      }

      if (comp.boolean?.targetComponent && !compNameSet.has(comp.boolean.targetComponent)) {
        delete comp.boolean;
      }
    }

    // -------------------------------------------------------------------------
    // Automatic Spatial Clustering & Outlier Clamp
    // Prevents rogue / disconnected components (like distant feet or satellite pads)
    // from being scattered meters away across the room.
    // -------------------------------------------------------------------------
    let maxBodyArea = 0;
    let bodyW = 1.0;
    let bodyD = 1.0;

    for (const c of spec.components) {
      const s = Array.isArray(c.size) ? c.size : [1, 1, 1];
      const w = s[0] || 1;
      const d = (c.shape === 'cylinder' || c.shape === 'sphere' || c.shape === 'cone') ? w : (s[2] || s[1] || 1);
      const area = w * d;
      const isNearCenter = Math.abs(c.position?.[0] || 0) < 0.6 && Math.abs(c.position?.[2] || 0) < 0.6;
      if (isNearCenter && area > maxBodyArea) {
        maxBodyArea = area;
        bodyW = w;
        bodyD = d;
      }
    }

    const isVehicle = spec.category === 'vehicles';
    const maxAllowedX = Math.max(0.9, bodyW * (isVehicle ? 1.6 : 0.85) + (isVehicle ? 0.6 : 0.25));
    const maxAllowedZ = Math.max(0.9, bodyD * (isVehicle ? 1.6 : 0.85) + (isVehicle ? 0.6 : 0.25));

    for (const c of spec.components) {
      if (!c.position) continue;
      if (Math.abs(c.position[0]) > maxAllowedX) {
        c.position[0] = parseFloat((Math.sign(c.position[0]) * (bodyW * 0.42)).toFixed(3));
      }
      if (Math.abs(c.position[2]) > maxAllowedZ) {
        c.position[2] = parseFloat((Math.sign(c.position[2]) * (bodyD * 0.42)).toFixed(3));
      }
    }

    // Convert world-space coordinates into parent-relative coordinates so that Three.js
    // scene graph transforms match the exact intended world positions without doubling.
    this.convertWorldToLocalHierarchy(spec);

    // Validate glTF exportable animation clips
    if (Array.isArray(spec.animations) && spec.animations.length > 0) {
      const validClips: any[] = [];
      for (const clip of spec.animations) {
        if (!clip || typeof clip !== 'object') continue;
        const validClip: any = {
          id: clip.id || `anim_${validClips.length + 1}`,
          name: clip.name || `Animation_${validClips.length + 1}`,
          duration: Number.isFinite(clip.duration) && clip.duration > 0 ? parseFloat(clip.duration.toFixed(2)) : 2.0,
          loop: ['repeat', 'pingpong', 'once'].includes(clip.loop) ? clip.loop : 'repeat',
          tracks: Array.isArray(clip.tracks) ? clip.tracks : []
        };
        if (
          clip.presetType &&
          ['sliding_door', 'hinge_lid', 'button_press', 'spin_continuous', 'mechanical_deploy', 'idle_hover'].includes(clip.presetType)
        ) {
          validClip.presetType = clip.presetType;
        }
        validClips.push(validClip);
      }
      spec.animations = validClips.length > 0 ? validClips : undefined;
    }

    // Auto-Grounding: measure true 3D bounding box to ground lowest contact points at Y = 0
    try {
      const { group } = ProceduralEngine.buildModelFromSpec(spec);
      const bbox = new THREE.Box3().setFromObject(group);

      if (!bbox.isEmpty()) {
        const minY = bbox.min.y;
        if (Math.abs(minY) > 0.002) {
          const shiftY = -minY;
          for (const comp of spec.components) {
            // Shift only root components (without parentId or with unparented roots)
            if (!comp.parentId || !spec.components.some((c) => c.name === comp.parentId)) {
              if (comp.position) {
                comp.position[1] = parseFloat((comp.position[1] + shiftY).toFixed(4));
              }
            }
          }
        }

        const sizeX = Math.max(0.1, bbox.max.x - bbox.min.x);
        const sizeY = Math.max(0.1, bbox.max.y - bbox.min.y);
        const sizeZ = Math.max(0.1, bbox.max.z - bbox.min.z);
        spec.dimensions = {
          width: parseFloat(sizeX.toFixed(3)),
          height: parseFloat(sizeY.toFixed(3)),
          depth: parseFloat(sizeZ.toFixed(3))
        };
      }
    } catch (e) {
      console.warn('[AIGenerator] Could not compute bounding box for auto-grounding:', e);
    }

    return spec;
  }

  /**
   * Calls Google Gemini API with structured JSON output schema and high spatial precision.
   */
  private static async callGeminiAPI(
    prompt: string,
    apiKey: string,
    preferredModel?: string
  ): Promise<{ spec: ModelSpec; rawResponse: string; usedModel: string }> {
    const uniqueNonce = `${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    const systemInstruction = `You are ModelCoder 3D Master Architect, an expert procedural 3D modeler for retro-modern, sci-fi, industrial, and cybernetic games.
Your mission is to construct realistic, physically coherent, mechanically solid 3D models with ZERO floating geometry, perfect ground alignment, high mechanical detail, and authentic retro materials.

### 5 ABSOLUTE LAWS OF 3D CONSTRUCTION (MANDATORY)

1. LAW OF SOLID GROUNDING (Ground Level Y = 0):
- The model must rest firmly on the floor at Y = 0.
- In Three.js, primitive positions are centered at their CENTROIDS (center of mass).
- If the lowest base/chassis/leg has height H, its Y position MUST be H/2 (e.g. height 0.20m -> position Y = 0.10m).
- NEVER place the lowest piece with bottom above Y = 0 (no hovering or floating machines).

2. LAW OF ZERO FLOATING GEOMETRY (Physical Stacking & Surface Contact):
- EVERY component must physically touch, connect to, or rest on another component or the floor.
- VERTICAL STACKING FORMULA:
  If Component A extends vertically from Y_bottom to Y_top (height H_A),
  and Component B (height H_B) sits ON TOP of Component A:
  -> Component B's center Y position = Y_top + (H_B / 2).
  -> Example: Base box from Y=0 to Y=0.60. A monitor of height 0.40m resting on it MUST have position Y = 0.60 + (0.40 / 2) = 0.80m.
- WALL & FACE MOUNTING FORMULA:
  If Component A has depth D centered at Z=0 (front face at Z = +D/2),
  and a control panel/dial/gauge of thickness T attaches to its front:
  -> The attached piece MUST have position Z = (D/2) + (T/2).
  -> NEVER let panels float 20cm away in mid-air from the machine body!

3. LAW OF ORTHOGONAL & PURPOSEFUL ROTATIONS (DEGREES):
- All rotations are in DEGREES: [rotX_deg, rotY_deg, rotZ_deg].
- 95% of components MUST have rotation: [0, 0, 0].
- NEVER use random, chaotic, or diagonal rotations (like [17, -33, 48]).
- Only use standard intentional rotations when mechanically required:
  * Horizontal cylinder/wheel/axle: [0, 0, 90] or [90, 0, 0]
  * Ergonomic display tilt / control wedge: [-15, 0, 0] or [15, 0, 0]
  * Door or solar panel swing: [0, 45, 0]

4. LAW OF MECHANICAL HIERARCHY & FUNCTIONAL ANATOMY:
- Design objects like real machines and structures:
  a) HEAVY FOUNDATION / CHASSIS / WHEELS: Heavy base at Y=0 (diamond plate, cast iron, rubber feet).
  b) MAIN HOUSING / BODY: Enclosed structural core (worn metal, beige plastic, painted metal, chamfer_box).
  c) MECHANICAL & ELECTRICAL PARTS: Tanks, vents, heat sinks, conduits, hydraulic pistons, pipes, prisms.
  d) INTERFACE & CONTROLS: Flush control panels, switches, CRT screens, gauges, dials, emergency stop buttons.
  e) ACCENTS & LIGHTS: Warning decals, hazard stripes, LED indicators with emissive glow.

5. LAW OF SYMMETRY & COHESIVE PROPORTIONS:
- Center main structures at X = 0.
- Bilateral parts (wheels, dual tanks, side handles, thrusters, legs) MUST be placed in symmetric pairs (+X and -X) with identical Y and Z.

6. LAW OF MECHANICAL DENSITY (15-30 COMPONENTS MINIMUM):
- A convincing low-poly 3D asset MUST NOT be a solitary simple box with a lone antenna or floating badge.
- Break machines and objects into modular parts: base plate/frame, structural chassis, housing shell, ventilation grills/louvers, pipes/hoses/cables (using pipe/torus/cylinder), brackets/fixtures, access hatches, tactile control interfaces (buttons, dials, emergency switch), warning beacons, and CRT displays.
- MANDATORY: Generate between 15 and 30 components for standard models (and minimum 12 for compact items). More detail creates professional retro/sci-fi aesthetics.
- MANDATORY PBR TEXTURE PRESET: Every component MUST specify a valid "texturePreset" (e.g. "painted_metal_white", "painted_metal_blue", "diamond_plate", "crt_screen_green", "vent_grill", "rubber_black", "hazard_stripes", etc.). DO NOT leave components with plain flat colors and no texture.

7. LAW OF COMPACT ASSEMBLY & SOLID FOOTPRINT:
- The asset MUST be ONE single, compact, solid machine or prop. NEVER scatter pieces or pads meters away across the floor!
- All feet, pads, conduits, and accessories must remain physically attached within the base perimeter (width <= 1.50m, depth <= 1.50m).
- All control consoles, CRT screens, and displays must face directly forward towards the player (+Z). NEVER twist consoles diagonally with random Y/Z rotations.

### 12 PRIMITIVE SHAPES (METERS) & USAGE
- "box": size [width_X, height_Y, depth_Z]
  * Cuboid for structural framing, walls, steps, brackets, chassis cores.
- "chamfer_box": size [width_X, height_Y, depth_Z, bevelRadius, bevelSegments]
  * Box with beveled/rounded edges. Ideal for cybernetic armor, electronics consoles, smooth sci-fi crates, high-tech furniture.
  * Low-poly rule: keep bevelRadius ~0.02-0.05 and bevelSegments 1 or 2 (e.g. [0.60, 0.40, 0.50, 0.02, 1]).
- "cylinder": size [radiusTop, radiusBottom, height_Y, radialSegments]
  * Solid cylinder/column. Wheels, tanks, hydraulic pistons, columns, barrels (e.g. [0.15, 0.15, 0.60, 12]).
- "pipe": size [radiusOuter, radiusInner, height_Y, radialSegments]
  * HOLLOW tube/nozzle! Outer radius and inner radius. Perfect for jet thrusters, rocket nozzles, exhaust pipes, gun barrels, intake conduits, ring mounts (e.g. [0.20, 0.16, 0.40, 12]). Note: radiusInner MUST be less than radiusOuter.
- "prism": size [radius, height_Y, sides]
  * Regular N-sided polygonal prism (height along Y). Use for hexagonal armor plates, sci-fi pylons, heavy bolts/nuts, octagonal columns (e.g. [0.25, 0.80, 6] for a hex pylon).
- "pyramid": size [radius, height_Y, sides]
  * N-sided pyramid tapering to a tip (height along Y). Use for stealth facets, angular deflector plating, nosecones, sensor caps (e.g. [0.30, 0.45, 4] for a 4-sided pyramid).
- "wedge": size [width_X, height_Y, depth_Z]
  * Sloped triangular prism for ergonomic control consoles, ramps, cowcatchers, sloped vehicle hoods.
- "sphere": size [radius, widthSegments, heightSegments]
  * Domes, radar bubbles, cockpit spheres, robotics joint bearings (e.g. [0.20, 12, 8]).
- "capsule": size [radius, length_Y, capSegments, radialSegments]
  * Pressurized tanks, gas cylinders, medical cryo-pods, pill capsules (e.g. [0.10, 0.40, 4, 8]).
- "torus": size [radius, tubeRadius, radSegs, tubSegs]
  * Steering wheels, circular conduits, reactor containment rings, gaskets (e.g. [0.25, 0.04, 6, 12]).
- "cone": size [radius, height_Y, radialSegments]
  * Warning cones, sharp spikes, spotlights, antenna tips (e.g. [0.15, 0.40, 8]).
- "plane": size [width_X, height_Y]
  * Thin display sheets, solar panels, backing plates (e.g. [0.50, 0.30]).

### HIERARCHICAL PARENTING ("parentId") & ARTICULATION PIVOTS ("pivot")
- "parentId": Link child components to their logical parent (e.g. wheels attached to "main_chassis", cannons to "turret_head", doors to "door_frame").
  * This creates clean transform hierarchies so rotating the parent moves all child parts together!
- "pivot": [offsetX, offsetY, offsetZ] (meters relative to component center).
  * Defines where hinges, joints, and articulation axes rotate:
  * Left-hinged door (width W): pivot = [-W/2, 0, 0]
  * Bottom-hinged hatch / folding ramp (height H): pivot = [0, -H/2, 0]
  * Rear-hinged lid (depth D): pivot = [0, 0, -D/2]
  * Elevating gun / antenna base: pivot = [0, -H/2, 0]

### MODIFIERS: REPETITION ARRAYS & CSG BOOLEAN CUTS
- "array": Instantiates multiple copies along an axis or in a circle without duplicating code:
  * Linear Array: "array": { "enabled": true, "type": "linear", "count": 4, "offset": [0, 0.08, 0] }
    -> Ideal for heat sink cooling fins, ladder rungs, radiator slats, ventilation louvers, steps.
  * Radial Array: "array": { "enabled": true, "type": "radial", "count": 6, "radialAxis": "y", "radialRadius": 0.35, "radialAngle": 360, "radialRotateCopies": true }
    -> Ideal for multi-thruster nozzle rings, circular bolt patterns, dial ticks, spoke rims.
- "boolean": Non-destructive CSG difference/union/intersection:
  * "boolean": { "enabled": true, "operation": "difference", "targetComponent": "<cutter_component_name>", "hideTarget": true }
    -> Ideal for cutting cockpit cavities out of fuselages, hollow intake vents, recessed access ports.

### TEXTURES, WEATHERING & EMISSIVE GLOW (138 PBR PRESETS)
- 138 authentic presets across 8 categories:
  * Metals: "worn_metal", "steel_polished", "steel_galvanized", "iron_cast", "copper_polished", "copper_oxidized", "bronze_antique", "brass_burnished", "titanium_aerospace", "diamond_plate", "metal_perforated", "gold_contacts", "chrome_mirror", "painted_metal_white", "painted_metal_blue", "painted_metal_olive", "red_paint_worn"
  * Tech/Screens: "pcb_green_gold", "pcb_black_hd", "carbon_fiber", "server_vent_panel", "solar_panel_blue", "vent_grill", "crt_screen_green", "crt_screen_amber", "crt_screen_blue", "crt_data_matrix", "plasma_core_glow", "radiation_label", "biohazard_label", "caution_label"
  * Industrial/Construction: "concrete_smooth", "asphalt_road", "corrugated_metal", "hazard_stripes", "rubber_black", "rubber_ribbed_mat", "plastic_abs_matte", "polymer_tactical", "station_modular_panel", "nonslip_floor"
  * Glass/Transparencies: "clean_glass", "tinted_glass", "reinforced_glass", "frosted_glass", "hologram_cyan", "visor_gold_mirror"
- Surface Weathering: "wear": 0.0 (factory new) to 0.8 (gritty battle-worn).
- Relief Depth: "normalStrength": 0.5 to 1.5.
- Emissive Lighting: "emissive": "#00ffcc" (or "#ff3300", "#39ff14", "#ffb700") with "emissiveIntensity": 1.2 to 2.5 for CRT monitors, LED status beacons, power cores, thruster fire.

### EXPORTABLE glTF ANIMATIONS ("animations")
When mechanically appropriate, include animation clips:
- "presetType": "spin_continuous" -> continuous 360° spin for radars, rotors, warning beacons, turbine fans.
- "presetType": "idle_hover" -> subtle floating vertical oscillation for hovering drones, hovercraft, alien relics.
- "presetType": "sliding_door" -> automated linear open/close for airlocks, blast gates, elevator doors.
- "presetType": "hinge_lid" -> angular swing for inspection hatches, cockpit canopies, storage crates.
- "presetType": "button_press" -> tactile mechanical depression for switches, buttons.
- "presetType": "mechanical_deploy" -> unfolding action for landing gear, solar panels, weapon bays.

### FEW-SHOT REFERENCE: INDUSTRIAL WELDING & POWER STATION ("máquina de soldar / generador")
Notice how every piece connects with exact mathematical contact, leveraging hierarchy, chamfers, and arrays:
{
  "id": "below_nominal.generated.welder_reference",
  "name": "Estación de Energía y Soldadura Arc-Core 500",
  "category": "infrastructure",
  "description": "Unidad de potencia industrial con chasis biselado, tobera de escape hueca, radiador lineal, escotilla articulada y pantalla CRT emisiva.",
  "units": "meters",
  "dimensions": { "width": 0.90, "height": 0.85, "depth": 0.70 },
  "palette": "industrial_hazard",
  "components": [
    {
      "name": "base_skid",
      "shape": "box",
      "size": [0.80, 0.06, 0.65],
      "position": [0, 0.03, 0],
      "rotation": [0, 0, 0],
      "color": "#1a202c",
      "texturePreset": "steel_galvanized",
      "wear": 0.4
    },
    {
      "name": "main_chassis",
      "shape": "chamfer_box",
      "size": [0.65, 0.48, 0.54, 0.03, 1],
      "position": [0, 0.30, 0],
      "rotation": [0, 0, 0],
      "color": "#dd6b20",
      "texturePreset": "worn_metal",
      "roughness": 0.6,
      "metalness": 0.4,
      "wear": 0.3
    },
    {
      "name": "cooling_radiator_slat",
      "shape": "box",
      "size": [0.015, 0.03, 0.40],
      "position": [0.33, 0.20, 0],
      "rotation": [0, 0, 0],
      "color": "#2d3748",
      "texturePreset": "steel_polished",
      "parentId": "main_chassis",
      "array": {
        "enabled": true,
        "type": "linear",
        "count": 5,
        "offset": [0, 0.05, 0]
      }
    },
    {
      "name": "exhaust_pipe",
      "shape": "pipe",
      "size": [0.09, 0.07, 0.22, 12],
      "position": [-0.18, 0.65, -0.12],
      "rotation": [0, 0, 0],
      "color": "#718096",
      "texturePreset": "iron_cast",
      "parentId": "main_chassis",
      "wear": 0.6
    },
    {
      "name": "power_coupler_hex",
      "shape": "prism",
      "size": [0.08, 0.10, 6],
      "position": [0.18, 0.59, -0.12],
      "rotation": [0, 0, 0],
      "color": "#ecc94b",
      "texturePreset": "brass_burnished",
      "parentId": "main_chassis"
    },
    {
      "name": "front_console_wedge",
      "shape": "wedge",
      "size": [0.55, 0.32, 0.08],
      "position": [0, 0.30, 0.31],
      "rotation": [0, 0, 0],
      "color": "#2d3748",
      "texturePreset": "plastic_abs_matte",
      "parentId": "main_chassis"
    },
    {
      "name": "crt_telemetry_screen",
      "shape": "box",
      "size": [0.22, 0.14, 0.01],
      "position": [-0.12, 0.34, 0.355],
      "rotation": [0, 0, 0],
      "color": "#00ffcc",
      "texturePreset": "crt_screen_green",
      "emissive": "#00ffcc",
      "emissiveIntensity": 1.6,
      "parentId": "main_chassis"
    },
    {
      "name": "status_lamp_warning",
      "shape": "cylinder",
      "size": [0.02, 0.02, 0.02, 10],
      "position": [0.14, 0.38, 0.355],
      "rotation": [90, 0, 0],
      "color": "#ff3300",
      "emissive": "#ff3300",
      "emissiveIntensity": 2.0,
      "parentId": "main_chassis"
    },
    {
      "name": "inspection_hatch_door",
      "shape": "box",
      "size": [0.24, 0.20, 0.02],
      "position": [0, 0.55, 0.12],
      "rotation": [0, 0, 0],
      "pivot": [0, 0, -0.10],
      "color": "#4a5568",
      "texturePreset": "diamond_plate",
      "parentId": "main_chassis"
    }
  ],
  "animations": [
    {
      "id": "anim_hatch_open",
      "name": "InspectHatchOpen",
      "duration": 2.0,
      "loop": "pingpong",
      "presetType": "hinge_lid",
      "tracks": [
        {
          "targetComponent": "inspection_hatch_door",
          "property": "rotation",
          "keyframes": [
            { "time": 0.0, "value": [0, 0, 0] },
            { "time": 2.0, "value": [-65, 0, 0] }
          ]
        }
      ]
    }
  ]
}

Return ONLY valid JSON matching this schema:
{
  "id": "below_nominal.generated.${uniqueNonce}",
  "name": "<Human Readable Name in Spanish>",
  "category": "vehicles" | "furniture" | "infrastructure" | "command" | "medical" | "security" | "weapons",
  "description": "<Descriptive sentence in Spanish>",
  "units": "meters",
  "dimensions": { "width": <float>, "depth": <float>, "height": <float> },
  "palette": "industrial_hazard",
  "components": [
    {
      "name": "<unique_component_name>",
      "shape": "box" | "chamfer_box" | "cylinder" | "pipe" | "prism" | "pyramid" | "wedge" | "sphere" | "capsule" | "torus" | "cone" | "plane",
      "size": [<numbers>],
      "position": [<x>, <y>, <z>],
      "rotation": [<deg_x>, <deg_y>, <deg_z>],
      "color": "<hex_or_palette_name>",
      "parentId": "<optional_parent_component_name>",
      "pivot": [<optional_offsetX>, <optional_offsetY>, <optional_offsetZ>],
      "texturePreset": "<valid texturePreset>",
      "roughness": 0.7,
      "metalness": 0.2,
      "wear": 0.3,
      "normalStrength": 1.0,
      "emissive": "<optional_hex_color>",
      "emissiveIntensity": 1.5,
      "array": {
        "enabled": true,
        "type": "linear" | "radial",
        "count": <int_2_to_64>,
        "offset": [<dx>, <dy>, <dz>],
        "radialAxis": "x" | "y" | "z",
        "radialRadius": <float>,
        "radialAngle": <degrees_default_360>,
        "radialRotateCopies": true
      },
      "boolean": {
        "enabled": true,
        "operation": "difference" | "union" | "intersection",
        "targetComponent": "<other_component_name>",
        "hideTarget": true
      }
    }
  ],
  "animations": [
    {
      "id": "<clip_id>",
      "name": "<ClipName>",
      "duration": <seconds_float>,
      "loop": "repeat" | "pingpong" | "once",
      "presetType": "spin_continuous" | "idle_hover" | "sliding_door" | "hinge_lid" | "button_press" | "mechanical_deploy",
      "tracks": [
        {
          "targetComponent": "<target_component_name>",
          "property": "position" | "rotation" | "scale",
          "keyframes": [
            { "time": <sec>, "value": [<x>, <y>, <z>] }
          ]
        }
      ]
    }
  ]
}`;

    const payload = {
      system_instruction: {
        parts: [{ text: systemInstruction }]
      },
      contents: [{
        role: 'user',
        parts: [{
          text: `USER PROMPT: ${prompt}\nCREATION_ID: ${uniqueNonce}\nINSTRUCTION: Synthesize a brand-new, mechanically coherent, grounded 3D model with ZERO floating geometry.`
        }]
      }],
      generationConfig: {
        responseMimeType: 'application/json',
        temperature: 0.2
      }
    };

    // Google Gemini API production models in priority order.
    // Si el usuario especificó un modelo en el selector, se intenta primero.
    const defaultModels = [
      'gemini-3.8-flash',
      'gemini-3.5-flash-lite',
      'gemini-3.1-flash-lite',
      'gemini-2.5-flash',
      'gemini-2.5-flash-lite',
      'gemini-2.0-flash',
      'gemini-1.5-flash',
      'gemini-3.6-flash'
    ];

    let candidateModels: string[];
    if (preferredModel && preferredModel !== 'auto') {
      candidateModels = [preferredModel, ...defaultModels.filter(m => m !== preferredModel)];
    } else {
      candidateModels = defaultModels;
    }
    let lastError: Error | null = null;

    for (const modelName of candidateModels) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
        const signal = typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function'
          ? AbortSignal.timeout(20000)
          : undefined;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal
        });

        if (!res.ok) {
          const errText = await res.text();
          lastError = new Error(`Gemini API error (${res.status}): ${errText}`);
          if (
            res.status === 404 ||
            res.status === 400 ||
            res.status === 429 ||
            res.status >= 500 ||
            errText.includes('NOT_FOUND') ||
            errText.includes('no longer available') ||
            errText.includes('high demand') ||
            errText.includes('UNAVAILABLE')
          ) {
            console.warn(`[AIGenerator] Intento con ${modelName} devolvió HTTP ${res.status}. Probando siguiente modelo de respaldo en cascada...`);
            if (res.status === 503 || res.status === 429) {
              await new Promise(r => setTimeout(r, 600));
            }
            continue;
          }
          throw lastError;
        }

        const data = await res.json();
        const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
        if (!candidateText) {
          throw new Error(`Gemini (${modelName}) no devolvió texto en la respuesta.`);
        }

        const parsedResult = this.parseModelOrDslOutput(String(candidateText));
        const normalized = this.normalizeSpecGeometry(parsedResult.spec);
        return {
          spec: normalized,
          rawResponse: parsedResult.rawResponse,
          dslCode: parsedResult.dslCode,
          usedModel: modelName
        };
      } catch (err: any) {
        lastError = err;
        console.warn(`[AIGenerator] Intento con ${modelName} falló:`, err);
        if (
          err?.name === 'TimeoutError' ||
          err?.name === 'AbortError' ||
          err?.message?.includes('404') ||
          err?.message?.includes('503') ||
          err?.message?.includes('429') ||
          err?.message?.includes('NOT_FOUND') ||
          err?.message?.includes('UNAVAILABLE') ||
          err?.message?.includes('high demand') ||
          err?.message?.includes('no longer available')
        ) {
          continue;
        }
        throw err;
      }
    }

    if (lastError?.name === 'TimeoutError' || lastError?.name === 'AbortError') {
      throw new Error('Tiempo de espera agotado al conectar con Gemini API. Verifica tu conexión a internet o genera con el Motor Procedural Local.');
    }

    throw lastError || new Error('No se pudo conectar con ningún modelo de Gemini disponible.');
  }

  /**
   * Parses either a JSON ModelSpec or JavaScript ProceduralBuilderContext DSL script from an LLM response.
   */
  public static parseModelOrDslOutput(rawText: string, _fallbackPrompt?: string): {
    spec: ModelSpec;
    rawResponse: string;
    dslCode?: string;
    synthesizedDsl?: string;
  } {
    const trimmed = String(rawText || '').trim();

    // Strip reasoning tags (<think>...</think> from DeepSeek R1 / QwQ)
    const withoutThink = trimmed.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();

    // Check if fenced code block or raw builder DSL script
    const fencedMatch = withoutThink.match(/```(?:javascript|js|ts|json)?\s*([\s\S]*?)```/i);
    const candidateContent = fencedMatch ? fencedMatch[1].trim() : withoutThink;

    // 1. Check if it is ProceduralBuilderContext DSL code (contains `builder.`)
    if (candidateContent.includes('builder.')) {
      const execRes = CodeSandbox.executeCode(candidateContent);
      if (execRes.error || !execRes.spec.components || execRes.spec.components.length === 0) {
        throw new Error(execRes.error || 'El código DSL generado por la IA no produjo componentes válidos.');
      }
      return {
        spec: execRes.spec,
        rawResponse: JSON.stringify(execRes.spec, null, 2),
        dslCode: candidateContent,
        synthesizedDsl: candidateContent
      };
    }

    // 2. Extract JSON object if surrounded by extra text
    let jsonStr = candidateContent;
    const firstBrace = jsonStr.indexOf('{');
    const lastBrace = jsonStr.lastIndexOf('}');
    if (firstBrace !== -1 && lastBrace > firstBrace) {
      jsonStr = jsonStr.substring(firstBrace, lastBrace + 1);
    }

    const parsed = JSON.parse(jsonStr) as any;

    // Check if the LLM returned `{ "dsl": "builder.setName(...)" }`
    if (typeof parsed.dsl === 'string' && parsed.dsl.includes('builder.')) {
      const execRes = CodeSandbox.executeCode(parsed.dsl);
      if (execRes.error || !execRes.spec.components || execRes.spec.components.length === 0) {
        throw new Error(execRes.error || 'El código DSL incluido en JSON no produjo componentes válidos.');
      }
      return {
        spec: execRes.spec,
        rawResponse: JSON.stringify(execRes.spec, null, 2),
        dslCode: parsed.dsl,
        synthesizedDsl: parsed.dsl
      };
    }

    if (!parsed.components || !Array.isArray(parsed.components) || parsed.components.length === 0) {
      throw new Error('La respuesta de la IA no incluye componentes geométricos.');
    }

    return {
      spec: parsed as ModelSpec,
      rawResponse: jsonStr
    };
  }

  /**
   * Builds the system prompt for either JSON ModelSpec output or JavaScript DSL output.
   */
  public static build3DSystemPrompt(outputFormat: AIOutputFormat = 'json'): string {
    const uniqueNonce = `${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    if (outputFormat === 'dsl') {
      return `You are ModelCoder 3D Master Architect & Procedural Coder.
Write clean, executable JavaScript code using the global \`builder\` (ProceduralBuilderContext) object to construct a grounded, detailed 3D model (12 to 28 components) with ZERO floating geometry and floor level at Y = 0.

AVAILABLE BUILDER API METHODS:
- builder.setName("Nombre en Español").setCategory("infrastructure").setDescription("Descripción en español");
- builder.addBox({ name, size: [w, h, d], position: [x, y, z], rotation: [rx, ry, rz], color, texturePreset, parentId, pivot, wear, emissive, emissiveIntensity });
- builder.addChamferBox({ name, size: [w, h, d, bevelRadius, bevelSegs], position: [x, y, z], color, texturePreset, parentId });
- builder.addCylinder({ name, size: [rTop, rBottom, height, segs], position: [x, y, z], rotation: [rx, ry, rz], color, texturePreset, parentId });
- builder.addPipe({ name, size: [rOuter, rInner, height, segs], position: [x, y, z], rotation: [rx, ry, rz], color, texturePreset, parentId });
- builder.addPrism({ name, size: [radius, height, sides], position: [x, y, z], color, texturePreset, parentId });
- builder.addPyramid({ name, size: [radius, height, sides], position: [x, y, z], color, texturePreset, parentId });
- builder.addWedge({ name, size: [w, h, d], position: [x, y, z], rotation: [rx, ry, rz], color, texturePreset, parentId });
- builder.addSphere({ name, size: [radius, wSegs, hSegs], position: [x, y, z], color, texturePreset, parentId });
- builder.addCapsule({ name, size: [radius, length, capSegs, radSegs], position: [x, y, z], color, texturePreset, parentId });
- builder.addCone({ name, size: [radius, height, segs], position: [x, y, z], color, texturePreset, parentId });
- builder.addTorus({ name, size: [radius, tubeRadius, radSegs, tubSegs], position: [x, y, z], rotation: [rx, ry, rz], color, texturePreset, parentId });
- builder.addPlane({ name, size: [w, h], position: [x, y, z], rotation: [rx, ry, rz], color, texturePreset, parentId });
- builder.mirror("left_part_name", "x", "right_part_name"); // Bilateral symmetry!
- builder.setPivot("door_name", "left" | "bottom" | [ox, oy, oz]);
- builder.addPresetAnimation("spin_continuous" | "hinge_lid" | "sliding_door" | "idle_hover", { targetComponent: "part_name", name: "AnimName", duration: 2.0, axis: "y" });

MANDATORY RULES:
1. Ground Y = 0: Lowest component of height H must have position Y = H/2.
2. You may use standard JavaScript loops (for) and math variables to arrange ribs, vents, wheels, bolts, or steps with exact mathematical precision!
3. Every component MUST include a valid \`texturePreset\` ("worn_metal", "steel_galvanized", "diamond_plate", "painted_metal_blue", "painted_metal_white", "iron_cast", "brass_burnished", "plastic_abs_matte", "crt_screen_green", "hazard_stripes", "rubber_black", "clean_glass", "plasma_core_glow", "vent_grill").
4. Output ONLY executable JavaScript code using \`builder.*\`. Do not wrap in markdown explanations.`;
    }

    return `You are ModelCoder 3D Master Architect, an expert procedural 3D modeler for retro-modern, sci-fi, industrial, and cybernetic games.
Construct realistic, mechanically solid 3D models with ZERO floating geometry, ground alignment at Y = 0, 14-28 components, and authentic PBR texturePresets.
Allowed shapes: "box", "chamfer_box", "cylinder", "pipe", "prism", "pyramid", "wedge", "sphere", "capsule", "torus", "cone", "plane".
Allowed texturePresets: "worn_metal", "steel_polished", "steel_galvanized", "iron_cast", "copper_polished", "brass_burnished", "titanium_aerospace", "diamond_plate", "painted_metal_white", "painted_metal_blue", "painted_metal_olive", "red_paint_worn", "pcb_green_gold", "carbon_fiber", "solar_panel_blue", "vent_grill", "crt_screen_green", "crt_screen_amber", "plasma_core_glow", "hazard_stripes", "rubber_black", "plastic_abs_matte", "polymer_tactical", "clean_glass", "hologram_cyan".
Return ONLY valid JSON matching the ModelSpec schema with id "below_nominal.generated.${uniqueNonce}", name, category, description, dimensions, palette, components[], and optional animations[].`;
  }

  /**
   * Unified Multi-Provider LLM dispatcher supporting:
   * - Google Gemini (REST v1beta with multimodal vision support)
   * - OpenAI / OpenRouter / Groq / DeepSeek / Ollama / LM Studio (OpenAI Chat Completions v1)
   * - Anthropic Claude (Messages API v1 or via local proxy)
   */
  public static async callMultiProviderLLM(
    prompt: string,
    options: {
      provider: AIProviderType;
      apiKey?: string;
      baseUrl?: string;
      model?: string;
      outputFormat?: AIOutputFormat;
      viewportImageBase64?: string;
    }
  ): Promise<{ spec: ModelSpec; rawResponse: string; dslCode?: string; usedModel: string }> {
    const { provider, apiKey = '', baseUrl, model, outputFormat = 'json', viewportImageBase64 } = options;

    if (provider === 'gemini' && outputFormat === 'json' && !viewportImageBase64) {
      return await this.callGeminiAPI(prompt, apiKey, model);
    }

    const systemPrompt = this.build3DSystemPrompt(outputFormat);
    const userInstruction = outputFormat === 'dsl'
      ? `USER PROMPT: ${prompt}\nINSTRUCTION: Write the complete JavaScript ProceduralBuilderContext (builder.*) script to build this 3D model.`
      : `USER PROMPT: ${prompt}\nINSTRUCTION: Synthesize a brand-new, mechanically coherent, grounded 3D model JSON spec with ZERO floating geometry.`;

    const rawTextResponse = await this.dispatchRawLLMRequest({
      provider,
      apiKey,
      baseUrl,
      model,
      systemPrompt,
      userPrompt: userInstruction,
      jsonMode: outputFormat === 'json',
      imageBase64: viewportImageBase64
    });

    const parsed = this.parseModelOrDslOutput(rawTextResponse.text);
    return {
      spec: parsed.spec,
      rawResponse: parsed.rawResponse,
      dslCode: parsed.dslCode,
      usedModel: rawTextResponse.usedModel
    };
  }

  /**
   * Dispatches a raw chat/completion request to any supported provider and returns `{ text, usedModel }`.
   */
  public static async dispatchRawLLMRequest(params: {
    provider: AIProviderType;
    apiKey?: string;
    baseUrl?: string;
    model?: string;
    systemPrompt: string;
    userPrompt: string;
    jsonMode?: boolean;
    imageBase64?: string;
  }): Promise<{ text: string; usedModel: string }> {
    const preset = this.PROVIDER_PRESETS[params.provider] || this.PROVIDER_PRESETS.gemini;
    const chosenModel = (params.model && params.model !== 'auto')
      ? params.model
      : (preset.defaultModels.find(m => m.id !== 'auto')?.id || preset.defaultModels[0].id);
    const endpointBase = (params.baseUrl || preset.baseUrl).replace(/\/+$/, '');
    const signal = typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function'
      ? AbortSignal.timeout(28000)
      : undefined;

    // 1. GOOGLE GEMINI (including DSL or Multimodal Vision)
    if (params.provider === 'gemini') {
      const geminiModel = chosenModel === 'auto' ? 'gemini-2.5-flash' : chosenModel;
      const parts: any[] = [{ text: params.userPrompt }];
      if (params.imageBase64) {
        const cleanB64 = params.imageBase64.replace(/^data:image\/\w+;base64,/, '');
        parts.push({
          inline_data: {
            mime_type: 'image/jpeg',
            data: cleanB64
          }
        });
      }
      const payload: any = {
        system_instruction: { parts: [{ text: params.systemPrompt }] },
        contents: [{ role: 'user', parts }],
        generationConfig: {
          temperature: 0.2,
          ...(params.jsonMode ? { responseMimeType: 'application/json' } : {})
        }
      };
      const url = `${endpointBase}/models/${geminiModel}:generateContent?key=${params.apiKey || ''}`;
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal
      });
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Gemini error (${res.status}): ${errText}`);
      }
      const data = await res.json();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
      if (!text) throw new Error('Gemini devolvió una respuesta vacía.');
      return { text, usedModel: geminiModel };
    }

    // 2. ANTHROPIC CLAUDE (Direct or via CORS header)
    if (params.provider === 'anthropic') {
      const url = endpointBase.endsWith('/messages') ? endpointBase : `${endpointBase}/messages`;
      const userContent: any[] = [{ type: 'text', text: params.userPrompt }];
      if (params.imageBase64) {
        const cleanB64 = params.imageBase64.replace(/^data:image\/\w+;base64,/, '');
        userContent.unshift({
          type: 'image',
          source: {
            type: 'base64',
            media_type: 'image/jpeg',
            data: cleanB64
          }
        });
      }
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': params.apiKey || '',
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true'
        },
        body: JSON.stringify({
          model: chosenModel,
          max_tokens: 4096,
          temperature: 0.2,
          system: params.systemPrompt,
          messages: [{ role: 'user', content: userContent }]
        }),
        signal
      });
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Anthropic API error (${res.status}): ${errText}`);
      }
      const data = await res.json();
      const text = data.content?.find((c: any) => c.type === 'text')?.text || '';
      if (!text) throw new Error('Anthropic Claude devolvió una respuesta vacía.');
      return { text, usedModel: chosenModel };
    }

    // 3. OPENAI-COMPATIBLE (OpenAI, OpenRouter, Groq, DeepSeek, Ollama, LM Studio, Custom)
    const chatUrl = endpointBase.endsWith('/chat/completions')
      ? endpointBase
      : `${endpointBase}/chat/completions`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };
    if (params.apiKey && params.apiKey.trim()) {
      headers['Authorization'] = `Bearer ${params.apiKey.trim()}`;
    }
    if (params.provider === 'openrouter') {
      headers['HTTP-Referer'] = 'https://modelcoder.ivorbitgames.online';
      headers['X-Title'] = 'ModelCoder 3D Studio';
    }

    let userContent: any = params.userPrompt;
    if (params.imageBase64) {
      const dataUrl = params.imageBase64.startsWith('data:')
        ? params.imageBase64
        : `data:image/jpeg;base64,${params.imageBase64}`;
      userContent = [
        { type: 'text', text: params.userPrompt },
        { type: 'image_url', image_url: { url: dataUrl } }
      ];
    }

    const body: any = {
      model: chosenModel,
      temperature: 0.2,
      messages: [
        { role: 'system', content: params.systemPrompt },
        { role: 'user', content: userContent }
      ]
    };

    if (params.jsonMode && params.provider !== 'ollama' && params.provider !== 'custom' && !chosenModel.includes('reasoner') && !chosenModel.includes('r1')) {
      body.response_format = { type: 'json_object' };
    }

    const res = await fetch(chatUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`${preset.label} API error (${res.status}): ${errText}`);
    }

    const data = await res.json();
    const text = data.choices?.[0]?.message?.content || '';
    if (!text) {
      throw new Error(`${preset.label} (${chosenModel}) no devolvió contenido.`);
    }

    return { text, usedModel: data.model || chosenModel };
  }

  // ===========================================================================
  // CONVERSATIONAL 3D AGENT & VISION SELF-CRITIQUE ENGINE
  // ===========================================================================
  /**
   * Runs an incremental Agent Turn over an existing `currentSpec`.
   * Instead of destroying the model, the agent inspects the current components and emits
   * structured tool actions (`add_component`, `update_component`, `delete_component`,
   * `mirror_component`, `apply_material_all`, `add_animation`, `align_to_ground`) or a refined spec.
   */
  public static async runAgentTurn(
    instruction: string,
    currentSpec: ModelSpec,
    options: {
      provider: AIProviderType;
      apiKey?: string;
      baseUrl?: string;
      model?: string;
      outputFormat?: AIOutputFormat;
      agentMode?: AIAgentMode;
      viewportImageBase64?: string;
    }
  ): Promise<{
    spec: ModelSpec;
    actions: AgentToolAction[];
    summary: string;
    rawResponse: string;
    dslCode?: string;
    usedModel: string;
  }> {
    const isVisionCritique = options.agentMode === 'vision_critique';

    // Build a compact summary of the current scene so the LLM has exact spatial coordinates
    const compactScene = {
      name: currentSpec.name,
      category: currentSpec.category,
      dimensions: currentSpec.dimensions,
      components: currentSpec.components.map((c) => ({
        name: c.name,
        shape: c.shape,
        size: c.size,
        position: c.position,
        rotation: c.rotation,
        color: c.color,
        texturePreset: c.texturePreset,
        parentId: c.parentId,
        pivot: c.pivot,
        wear: c.wear,
        emissive: c.emissive
      })),
      animations: currentSpec.animations || []
    };

    const agentSystemPrompt = `You are ModelCoder Autonomous 3D Agent & Spatial Inspector.
You modify an EXISTING 3D model in real time by returning a JSON object with tool actions.

AVAILABLE TOOL ACTIONS (in "actions" array):
1. { "action": "add_component", "component": { "name": "<unique_name>", "shape": "box"|"chamfer_box"|"cylinder"|"pipe"|"prism"|"pyramid"|"wedge"|"sphere"|"capsule"|"torus"|"cone"|"plane", "size": [...], "position": [x, y, z], "rotation": [rx, ry, rz], "color": "#hex", "texturePreset": "<preset>", "parentId": "<optional_parent>", "emissive": "<optional_hex>", "emissiveIntensity": 1.5 } }
2. { "action": "update_component", "targetName": "<existing_name>", "changes": { "size": [...], "position": [x,y,z], "rotation": [rx,ry,rz], "color": "#hex", "texturePreset": "<preset>", "wear": 0.5, "emissive": "#hex" } }
3. { "action": "delete_component", "targetName": "<existing_name>" }
4. { "action": "mirror_component", "targetName": "<existing_name>", "axis": "x"|"y"|"z", "newName": "<mirrored_name>" }
5. { "action": "reparent_component", "targetName": "<child_name>", "parentId": "<parent_name>" }
6. { "action": "apply_material_all", "texturePreset": "<preset>", "color": "<optional_hex>", "wear": <optional_0_to_1> }
7. { "action": "add_animation", "animation": { "name": "<ClipName>", "duration": 2.0, "loop": "repeat"|"pingpong", "presetType": "spin_continuous"|"hinge_lid"|"sliding_door"|"idle_hover", "tracks": [{ "targetComponent": "<comp_name>", "property": "rotation"|"position", "keyframes": [{ "time": 0, "value": [0,0,0] }, { "time": 2.0, "value": [0,360,0] }] }] } }
8. { "action": "align_to_ground" }

SPATIAL STACKING LAWS:
- Ground is at Y = 0.
- To place a new component of height H on top of a parent/base whose top is at Y_top, set position Y = Y_top + H/2.
- Valid texturePresets: "worn_metal", "steel_polished", "steel_galvanized", "iron_cast", "brass_burnished", "titanium_aerospace", "diamond_plate", "painted_metal_white", "painted_metal_blue", "painted_metal_olive", "red_paint_worn", "carbon_fiber", "solar_panel_blue", "vent_grill", "crt_screen_green", "crt_screen_amber", "plasma_core_glow", "hazard_stripes", "rubber_black", "plastic_abs_matte", "clean_glass", "hologram_cyan".

Return ONLY valid JSON with this structure:
{
  "summary": "<Brief explanation in Spanish of the modifications applied>",
  "actions": [ ... ]
}`;

    const userPrompt = isVisionCritique
      ? `CURRENT 3D SCENE SPEC:\n${JSON.stringify(compactScene)}\n\nVISION & SPATIAL SELF-CRITIQUE TASK: ${instruction || 'Inspecciona el modelo actual, corrige cualquier pieza flotante o desalineada, mejora el nivel de detalle mecánico añadiendo piezas complementarias (rejillas, conductos, indicadores LED o soportes) y asegura materiales PBR coherentes.'}`
      : `CURRENT 3D SCENE SPEC:\n${JSON.stringify(compactScene)}\n\nUSER EDIT INSTRUCTION: ${instruction}\nApply the requested modifications to the current 3D model using the tool actions.`;

    const llmRes = await this.dispatchRawLLMRequest({
      provider: options.provider,
      apiKey: options.apiKey,
      baseUrl: options.baseUrl,
      model: options.model,
      systemPrompt: agentSystemPrompt,
      userPrompt,
      jsonMode: true,
      imageBase64: options.viewportImageBase64
    });

    const withoutThink = llmRes.text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
    const firstBrace = withoutThink.indexOf('{');
    const lastBrace = withoutThink.lastIndexOf('}');
    const jsonText = (firstBrace !== -1 && lastBrace > firstBrace)
      ? withoutThink.substring(firstBrace, lastBrace + 1)
      : withoutThink;

    const parsed = JSON.parse(jsonText);

    // If the model returned a full replacement spec instead of actions
    if (Array.isArray(parsed.components) && parsed.components.length > 0 && !Array.isArray(parsed.actions)) {
      const norm = this.normalizeSpecGeometry(parsed as ModelSpec);
      return {
        spec: norm,
        actions: [{ action: 'replace_spec', spec: norm }],
        summary: `Modelo actualizado (${norm.components.length} piezas).`,
        rawResponse: JSON.stringify(norm, null, 2),
        usedModel: llmRes.usedModel
      };
    }

    const actions: AgentToolAction[] = Array.isArray(parsed.actions) ? parsed.actions : [];
    const execRes = this.executeAgentTools(currentSpec, actions, parsed.summary);

    return {
      spec: execRes.spec,
      actions,
      summary: execRes.summary,
      rawResponse: JSON.stringify(execRes.spec, null, 2),
      usedModel: llmRes.usedModel
    };
  }

  /**
   * Executes an array of `AgentToolAction` deterministically over a cloned `ModelSpec`.
   */
  public static executeAgentTools(
    baseSpec: ModelSpec,
    actions: AgentToolAction[],
    customSummary?: string
  ): { spec: ModelSpec; actions: AgentToolAction[]; summary: string } {
    const spec: ModelSpec = JSON.parse(JSON.stringify(baseSpec));
    if (!Array.isArray(spec.components)) {
      spec.components = [];
    }

    for (const act of actions) {
      if (!act || typeof act !== 'object') continue;

      switch (act.action) {
        case 'add_component': {
          if (act.component) {
            const c = act.component;
            const newName = (c.name || `pieza_${spec.components.length + 1}`).trim().replace(/\s+/g, '_');
            spec.components.push({
              name: newName,
              shape: (c.shape as any) || 'box',
              size: Array.isArray(c.size) ? c.size : [0.4, 0.4, 0.4],
              position: Array.isArray(c.position) && c.position.length >= 3 ? [c.position[0], c.position[1], c.position[2]] : [0, 0.5, 0],
              rotation: Array.isArray(c.rotation) && c.rotation.length >= 3 ? [c.rotation[0], c.rotation[1], c.rotation[2]] : [0, 0, 0],
              color: c.color || '#718096',
              texturePreset: c.texturePreset || 'worn_metal',
              roughness: c.roughness ?? 0.65,
              metalness: c.metalness ?? 0.3,
              wear: c.wear,
              parentId: c.parentId || (c as any).parent,
              pivot: c.pivot,
              emissive: c.emissive,
              emissiveIntensity: c.emissiveIntensity,
              array: c.array,
              boolean: c.boolean
            });
          }
          break;
        }

        case 'update_component': {
          const target = spec.components.find(
            (c) => c.name.toLowerCase() === (act.targetName || '').toLowerCase()
          );
          if (target && act.changes) {
            Object.assign(target, act.changes);
          }
          break;
        }

        case 'delete_component': {
          if (spec.components.length > 1 && act.targetName) {
            const targetLower = act.targetName.toLowerCase();
            spec.components = spec.components.filter((c) => c.name.toLowerCase() !== targetLower);
          }
          break;
        }

        case 'mirror_component': {
          const orig = spec.components.find(
            (c) => c.name.toLowerCase() === (act.targetName || '').toLowerCase()
          );
          if (orig) {
            const axis = act.axis || 'x';
            const copy = ProceduralEngine.createMirroredComponent(orig, axis, act.newName);
            spec.components.push(copy);
          }
          break;
        }

        case 'reparent_component': {
          if (act.targetName) {
            ProceduralEngine.reparentComponentPreservingWorldTransform(
              spec.components,
              act.targetName,
              act.parentId || undefined
            );
          }
          break;
        }

        case 'apply_material_all': {
          for (const comp of spec.components) {
            if (act.texturePreset) comp.texturePreset = act.texturePreset;
            if (act.color) comp.color = act.color;
            if (typeof act.wear === 'number') comp.wear = act.wear;
            if (typeof act.roughness === 'number') comp.roughness = act.roughness;
            if (typeof act.metalness === 'number') comp.metalness = act.metalness;
          }
          break;
        }

        case 'add_animation': {
          if (!Array.isArray(spec.animations)) spec.animations = [];
          if (act.animation) {
            spec.animations.push(act.animation);
          } else if (act.targetName) {
            const dur = act.duration || 2.5;
            const axis = act.axis || 'y';
            const endVal: [number, number, number] = axis === 'x' ? [360, 0, 0] : axis === 'z' ? [0, 0, 360] : [0, 360, 0];
            spec.animations.push({
              id: `anim_${spec.animations.length + 1}`,
              name: `${act.preset || 'Spin'}_${act.targetName}`,
              duration: dur,
              loop: 'repeat',
              presetType: (act.preset as any) || 'spin_continuous',
              tracks: [
                {
                  targetComponent: act.targetName,
                  property: 'rotation',
                  keyframes: [
                    { time: 0, value: [0, 0, 0] },
                    { time: dur, value: endVal }
                  ]
                }
              ]
            });
          }
          break;
        }

        case 'replace_spec': {
          if (act.spec && Array.isArray(act.spec.components) && act.spec.components.length > 0) {
            const normReplaced = this.normalizeSpecGeometry(act.spec);
            return {
              spec: normReplaced,
              actions,
              summary: customSummary || `Modelo reemplazado (${normReplaced.components.length} piezas).`
            };
          }
          break;
        }

        case 'align_to_ground':
        default:
          break;
      }
    }

    const normSpec = this.normalizeSpecGeometry(spec);
    return {
      spec: normSpec,
      actions,
      summary: customSummary || `Agente aplicó ${actions.length} acción(es) sobre "${normSpec.name}".`
    };
  }

  /**
   * Local deterministic Agent Heuristic Engine:
   * Accepts `(prompt, currentSpec)` OR `(currentSpec, prompt)` so both Studio and unit tests can invoke it seamlessly.
   */
  public static applyLocalHeuristicAgentEdit(
    firstArg: string | ModelSpec,
    secondArg: ModelSpec | string
  ): { spec: ModelSpec; actions: AgentToolAction[]; summary: string } {
    const prompt = typeof firstArg === 'string' ? firstArg : (secondArg as string);
    const currentSpec = typeof firstArg === 'string' ? (secondArg as ModelSpec) : firstArg;
    const lower = String(prompt || '').toLowerCase();
    const actions: AgentToolAction[] = [];
    const summaries: string[] = [];

    // Compute current bounding box to place new parts accurately on top or sides
    const { group } = ProceduralEngine.buildModelFromSpec(currentSpec);
    const bbox = new THREE.Box3().setFromObject(group);
    const maxY = !bbox.isEmpty() ? bbox.max.y : 0.8;
    const maxX = !bbox.isEmpty() ? Math.max(0.25, bbox.max.x) : 0.4;
    const maxZ = !bbox.isEmpty() ? Math.max(0.25, bbox.max.z) : 0.4;
    const rootParent = currentSpec.components[0]?.name;

    // 1. Add antenna / radar / sensor on top
    if (/(antena|radar|parab[oó]lica|sensor|baliza|faro|luz|sirena)/.test(lower)) {
      const mastName = `antena_mastil_${currentSpec.components.length + 1}`;
      const beaconName = `baliza_superior_${currentSpec.components.length + 2}`;
      actions.push({
        action: 'add_component',
        component: {
          name: mastName,
          shape: 'cylinder',
          size: [0.025, 0.035, 0.45, 10],
          position: [0, parseFloat((maxY + 0.225).toFixed(3)), 0],
          rotation: [0, 0, 0],
          color: '#a0aec0',
          texturePreset: 'steel_polished',
          parentId: rootParent
        }
      });
      actions.push({
        action: 'add_component',
        component: {
          name: beaconName,
          shape: 'sphere',
          size: [0.06, 12, 8],
          position: [0, parseFloat((maxY + 0.48).toFixed(3)), 0],
          rotation: [0, 0, 0],
          color: '#00ffcc',
          texturePreset: 'plasma_core_glow',
          emissive: '#00ffcc',
          emissiveIntensity: 2.2,
          parentId: mastName
        }
      });
      summaries.push('se añadió mástil de antena y baliza emisiva en la parte superior');
    }

    // 2. Add wheels / tires
    if (/(rueda|llanta|neum[aá]tico|tren de rodaje)/.test(lower)) {
      const wheelPositions: [string, [number, number, number]][] = [
        ['rueda_del_izq', [-maxX, 0.14, maxZ * 0.65]],
        ['rueda_del_der', [maxX, 0.14, maxZ * 0.65]],
        ['rueda_tras_izq', [-maxX, 0.14, -maxZ * 0.65]],
        ['rueda_tras_der', [maxX, 0.14, -maxZ * 0.65]]
      ];
      for (const [wName, wPos] of wheelPositions) {
        actions.push({
          action: 'add_component',
          component: {
            name: wName,
            shape: 'cylinder',
            size: [0.14, 0.14, 0.10, 14],
            position: wPos,
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          }
        });
      }
      summaries.push('se instalaron 4 ruedas simétricas con neumáticos de caucho');
    }

    // 3. Add CRT screen / monitor / console
    if (/(pantalla|monitor|crt|consola|display|visor)/.test(lower)) {
      actions.push({
        action: 'add_component',
        component: {
          name: `pantalla_crt_${currentSpec.components.length + 1}`,
          shape: 'box',
          size: [0.32, 0.22, 0.03],
          position: [0, parseFloat((maxY * 0.65).toFixed(3)), parseFloat((maxZ + 0.015).toFixed(3))],
          rotation: [0, 0, 0],
          color: '#00ffcc',
          texturePreset: 'crt_screen_green',
          emissive: '#00ffcc',
          emissiveIntensity: 1.8
        }
      });
      summaries.push('se montó una pantalla CRT frontal de telemetría');
    }

    // 4. Add exhaust pipe / thruster / cannon / turret
    if (/(ca[ñn][oó]n|tobera|propulsor|escape|tubo|torreta)/.test(lower)) {
      actions.push({
        action: 'add_component',
        component: {
          name: `tobera_conducto_${currentSpec.components.length + 1}`,
          shape: 'pipe',
          size: [0.10, 0.07, 0.35, 12],
          position: [0, parseFloat((maxY + 0.12).toFixed(3)), parseFloat((maxZ * 0.4).toFixed(3))],
          rotation: [90, 0, 0],
          color: '#4a5568',
          texturePreset: 'titanium_aerospace'
        }
      });
      summaries.push('se integró un conducto/tobera tubular');
    }

    // 5. Weathering / rust / wear adjustments
    if (/(oxid|desgast|viej|batalla|sucio|usado)/.test(lower)) {
      actions.push({
        action: 'apply_material_all',
        wear: 0.72,
        texturePreset: 'metal_rusted'
      });
      summaries.push('se aplicó desgaste de batalla (72%) y metal oxidado');
    } else if (/(nuevo|limpio|f[aá]brica|pulido|brillante|cromado)/.test(lower)) {
      actions.push({
        action: 'apply_material_all',
        wear: 0.0,
        texturePreset: 'steel_polished',
        roughness: 0.25,
        metalness: 0.85
      });
      summaries.push('se restauró el acabado a acero pulido de fábrica');
    }

    // 6. Color changes
    const colorMap: [RegExp, string, string, string][] = [
      [/(rojo|red|escarlata)/, '#e53e3e', 'red_paint_worn', 'rojo'],
      [/(azul|blue|cobalto)/, '#3182ce', 'painted_metal_blue', 'azul'],
      [/(verde|green|militar|oliva)/, '#38a169', 'painted_metal_olive', 'verde'],
      [/(blanco|white|[aá]rtico)/, '#edf2f7', 'painted_metal_white', 'blanco'],
      [/(dorado|oro|gold|lat[oó]n)/, '#ecc94b', 'brass_burnished', 'dorado'],
      [/(negro|black|oscuro|carbono)/, '#1a202c', 'carbon_fiber', 'negro carbono'],
      [/(amarillo|peligro|hazard)/, '#eab308', 'hazard_stripes', 'amarillo industrial']
    ];
    for (const [regex, hex, preset, label] of colorMap) {
      if (regex.test(lower)) {
        actions.push({
          action: 'apply_material_all',
          color: hex,
          texturePreset: preset
        });
        summaries.push(`se actualizó el acabado a ${label}`);
        break;
      }
    }

    // 7. Add animation
    if (/(anim|gir|rotar|spin|radar|h[eé]lice)/.test(lower)) {
      const targetComp = currentSpec.components[currentSpec.components.length - 1]?.name || currentSpec.components[0]?.name || 'Base';
      actions.push({
        action: 'add_animation',
        animation: {
          id: `anim_agent_${Date.now().toString().slice(-4)}`,
          name: 'Giro_Continuo_IA',
          duration: 2.5,
          loop: 'repeat',
          presetType: 'spin_continuous',
          tracks: [
            {
              targetComponent: targetComp,
              property: 'rotation',
              keyframes: [
                { time: 0, value: [0, 0, 0] },
                { time: 2.5, value: [0, 360, 0] }
              ]
            }
          ]
        }
      });
      summaries.push(`se añadió animación de giro continuo sobre "${targetComp}"`);
    }

    // 8. Default detail enhancement (if vision critique or general improvement requested)
    if (actions.length === 0) {
      actions.push({
        action: 'add_component',
        component: {
          name: `rejilla_ventilacion_${currentSpec.components.length + 1}`,
          shape: 'box',
          size: [0.28, 0.14, 0.02],
          position: [0, parseFloat((maxY * 0.5).toFixed(3)), parseFloat((maxZ + 0.01).toFixed(3))],
          rotation: [0, 0, 0],
          color: '#2d3748',
          texturePreset: 'vent_grill'
        }
      });
      actions.push({
        action: 'add_component',
        component: {
          name: `indicador_estado_${currentSpec.components.length + 2}`,
          shape: 'cylinder',
          size: [0.025, 0.025, 0.02, 10],
          position: [0.16, parseFloat((maxY * 0.72).toFixed(3)), parseFloat((maxZ + 0.01).toFixed(3))],
          rotation: [90, 0, 0],
          color: '#39ff14',
          emissive: '#39ff14',
          emissiveIntensity: 2.0
        }
      });
      summaries.push('se optimizó el asentamiento a suelo (Y=0) y se añadieron detalles mecánicos (rejilla de ventilación e indicador LED)');
    }

    return this.executeAgentTools(currentSpec, actions, `Agente 3D: ${summaries.join(', ')}.`);
  }

  /**
   * Knowledge-Driven Local Procedural Synthesizer V2:
   * Connects to:
   * 1. The 100 Modular Models Catalog (`ALL_MODULAR_MODELS` + `catalog.json` parameters/presets)
   * 2. Neufert / ISO Engineering Archetypes (Tanks, Helicopters, Cyberbikes, Arcade Cabinets, Spider Mechs, Fortified Towers)
   * 3. Live Wikidata Knowledge Graph (`queryWikidataKnowledge`) for real-world dimensions & classifications
   * 4. Socket-based Kitbashing & Material Biome Post-Processor (`enhanceSpecWithKnowledgeAndKitbash`)
   */
  public static synthesizeProceduralSpec(
    prompt: string,
    options?: {
      seed?: number;
      wikidata?: WikidataKnowledgeResult | null;
    }
  ): ModelSpec {
    const lower = prompt.toLowerCase();
    const seed = options?.seed ?? hashPromptString(prompt);
    const rng = createSeededPRNG(seed);

    // Extract potential custom dimensions (e.g. "2 metros", "0.5m", "1.5x2")
    const dimMatch = lower.match(/(\d+(?:\.\d+)?)\s*(?:m|metros?|metres?)/);
    const baseDim = dimMatch ? Math.max(0.2, parseFloat(dimMatch[1])) : 1.0;

    // Detect primary color
    let mainColor = '#4a5568';
    if (/rojo|red|carmesí/.test(lower)) mainColor = '#e53e3e';
    else if (/azul|blue|celeste/.test(lower)) mainColor = '#3182ce';
    else if (/verde|green|militar/.test(lower)) mainColor = '#38a169';
    else if (/amarillo|yellow/.test(lower)) mainColor = '#d69e2e';
    else if (/naranja|orange/.test(lower)) mainColor = '#dd6b20';
    else if (/blanco|white|plateado/.test(lower)) mainColor = '#edf2f7';
    else if (/negro|dark|black|oscuro/.test(lower)) mainColor = '#1a202c';
    else if (/dorado|gold|oro/.test(lower)) mainColor = '#ecc94b';
    else if (/cian|cyan|turquesa/.test(lower)) mainColor = '#319795';
    else if (/gris|metal|acero|grey|gray/.test(lower)) mainColor = '#718096';
    else if (/marron|brown|oxido|rust/.test(lower)) mainColor = '#7b341e';

    // Helper to finalize a base spec with Kitbashing sockets, Wikidata proportions, Material Biomes & Seed variations
    const finalizeWithKnowledge = (baseSpec: ModelSpec, extraMeta?: Partial<KnowledgeSynthesisMetadata>): ModelSpec => {
      const enhanced = ProceduralKnowledgeDB.enhanceSpecWithKnowledgeAndKitbash(baseSpec, prompt, options);
      (enhanced.spec as any)._knowledgeMetadata = {
        ...enhanced.metadata,
        ...extraMeta
      };
      return enhanced.spec;
    };

    // -------------------------------------------------------------
    // 0A. SEARCH 100 MODULAR MODELS CATALOG + CATALOG.JSON MANIFESTS
    // -------------------------------------------------------------
    const catalogMatch = ProceduralKnowledgeDB.searchModularCatalogMatch(prompt);
    if (catalogMatch) {
      if (dimMatch) {
        ProceduralKnowledgeDB.scaleSpecToDimensions(catalogMatch.spec, {
          width: (catalogMatch.spec.dimensions?.width || 1) * baseDim,
          height: (catalogMatch.spec.dimensions?.height || 1) * baseDim,
          depth: (catalogMatch.spec.dimensions?.depth || 1) * baseDim
        });
      }
      if (mainColor !== '#4a5568' && catalogMatch.spec.components.length > 0) {
        catalogMatch.spec.components[0].color = mainColor;
      }
      return finalizeWithKnowledge(catalogMatch.spec, {
        matchedCatalogFamily: catalogMatch.family
      });
    }

    // -------------------------------------------------------------
    // 0B. NEUFERT / ISO ENGINEERING ARCHETYPES (12 PRIMITIVES + ARRAYS)
    // -------------------------------------------------------------
    const engArchetype = ProceduralKnowledgeDB.synthesizeEngineeringArchetype(
      prompt,
      baseDim,
      mainColor,
      rng,
      options?.wikidata
    );
    if (engArchetype) {
      return finalizeWithKnowledge(engArchetype.spec, {
        matchedArchetype: engArchetype.archetypeName
      });
    }

    // -------------------------------------------------------------
    // 1. VEHICLES: CAR / AUTO / COCHE / CARRO / VEHICULO
    // -------------------------------------------------------------
    if (/auto|coche|carro|automovil|vehiculo|car\b|buggy|rover/.test(lower) || options?.wikidata?.inferredCategory === 'car') {
      const cw = 1.6 * baseDim;
      const cd = 3.2 * baseDim;
      const ch = 0.45 * baseDim;
      const cabinH = 0.5 * baseDim;
      const wheelR = 0.32 * baseDim;
      const wheelW = 0.22 * baseDim;
      const axleX = cw * 0.52;
      const axleZ = cd * 0.30;

      return finalizeWithKnowledge({
        id: 'below_nominal.vehicles.retro_car',
        name: options?.wikidata?.label ? `Vehículo ${options.wikidata.label}` : 'Auto Terrestre PSX',
        category: 'vehicles',
        description: `Vehículo terrestre retro con chasis de ${cd.toFixed(1)}m, cabina acristalada y cuatro ruedas con llantas metálicas.`,
        units: 'meters',
        dimensions: { width: cw * 1.15, depth: cd, height: ch + cabinH + wheelR * 0.4 },
        palette: 'industrial_hazard',
        components: [
          // Lower chassis body
          {
            name: 'chassis_body',
            shape: 'box',
            size: [cw, ch, cd],
            position: [0, wheelR * 0.65 + ch * 0.5, 0],
            color: mainColor,
            texturePreset: 'worn_metal',
            roughness: 0.6,
            metalness: 0.3
          },
          // Cabin / Passenger roof
          {
            name: 'cabin_roof',
            shape: 'box',
            size: [cw * 0.85, cabinH, cd * 0.52],
            position: [0, wheelR * 0.65 + ch + cabinH * 0.5, -cd * 0.05],
            color: '#2d3748',
            texturePreset: 'painted_metal_white',
            roughness: 0.5,
            metalness: 0.4
          },
          // Slanted Windshield (wedge)
          {
            name: 'windshield',
            shape: 'wedge',
            size: [cw * 0.82, cabinH * 0.95, cd * 0.22],
            position: [0, wheelR * 0.65 + ch + cabinH * 0.5, cd * 0.32],
            color: '#319795', // Tinted glass
            roughness: 0.2,
            metalness: 0.1
          },
          // Slanted Rear Window
          {
            name: 'rear_window',
            shape: 'wedge',
            size: [cw * 0.82, cabinH * 0.95, cd * 0.18],
            position: [0, wheelR * 0.65 + ch + cabinH * 0.5, -cd * 0.40],
            rotation: [0, 180, 0],
            color: '#319795',
            roughness: 0.2
          },
          // 4 Wheels
          {
            name: 'wheel_front_left',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [-axleX, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          {
            name: 'wheel_front_right',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [axleX, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          {
            name: 'wheel_rear_left',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [-axleX, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          {
            name: 'wheel_rear_right',
            shape: 'cylinder',
            size: [wheelR, wheelR, wheelW, 10],
            position: [axleX, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9
          },
          // 4 Metallic Rims
          {
            name: 'rim_fl',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [-axleX - 0.01, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          {
            name: 'rim_fr',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [axleX + 0.01, wheelR, axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          {
            name: 'rim_rl',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [-axleX - 0.01, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          {
            name: 'rim_rr',
            shape: 'cylinder',
            size: [wheelR * 0.55, wheelR * 0.55, wheelW * 1.05, 6],
            position: [axleX + 0.01, wheelR, -axleZ],
            rotation: [0, 0, 90],
            color: '#cbd5e0',
            texturePreset: 'metal_light_brushed',
            metalness: 0.8
          },
          // Front Headlights
          {
            name: 'headlight_left',
            shape: 'box',
            size: [cw * 0.18, ch * 0.35, 0.06],
            position: [-cw * 0.32, wheelR * 0.65 + ch * 0.65, cd * 0.505],
            color: '#ecc94b', // Yellow light
            roughness: 0.2
          },
          {
            name: 'headlight_right',
            shape: 'box',
            size: [cw * 0.18, ch * 0.35, 0.06],
            position: [cw * 0.32, wheelR * 0.65 + ch * 0.65, cd * 0.505],
            color: '#ecc94b',
            roughness: 0.2
          },
          // Rear Taillights
          {
            name: 'taillight_left',
            shape: 'box',
            size: [cw * 0.2, ch * 0.3, 0.06],
            position: [-cw * 0.32, wheelR * 0.65 + ch * 0.65, -cd * 0.505],
            color: '#e53e3e', // Red brake light
            roughness: 0.2
          },
          {
            name: 'taillight_right',
            shape: 'box',
            size: [cw * 0.2, ch * 0.3, 0.06],
            position: [cw * 0.32, wheelR * 0.65 + ch * 0.65, -cd * 0.505],
            color: '#e53e3e',
            roughness: 0.2
          },
          // Heavy Front Bumper
          {
            name: 'front_bumper',
            shape: 'box',
            size: [cw * 1.05, ch * 0.4, 0.2],
            position: [0, wheelR * 0.8, cd * 0.55],
            color: '#1a202c',
            metalness: 0.6
          }
        ]
      }, { matchedArchetype: 'retro_car' });
    }

    // -------------------------------------------------------------
    // 2. SPACESHIP / NAVE / COHETE / SHUTTLE / CAZA
    // -------------------------------------------------------------
    if (/nave|spaceship|cohete|rocket|shuttle|caza|aerodeslizador/.test(lower)) {
      const sw = 1.0 * baseDim;
      const sl = 3.6 * baseDim;
      const sh = 0.65 * baseDim;
      const wingSpan = 2.8 * baseDim;

      return {
        id: 'below_nominal.vehicles.space_fighter',
        name: 'Caza Espacial Interceptor',
        category: 'vehicles',
        description: 'Nave interceptora orbital con cabina presurizada, alas en cuña y propulsores dobles.',
        units: 'meters',
        dimensions: { width: wingSpan, depth: sl, height: sh * 1.8 },
        palette: 'command_bridge',
        components: [
          // Main Fuselage
          {
            name: 'fuselage_core',
            shape: 'box',
            size: [sw, sh, sl * 0.75],
            position: [0, sh * 0.9, -sl * 0.05],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Aerodynamic Nose Cone
          {
            name: 'nose_cone',
            shape: 'cone',
            size: [sw * 0.5, sl * 0.35, 8],
            position: [0, sh * 0.9, sl * 0.45],
            rotation: [90, 0, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Cockpit Canopy (wedge glass)
          {
            name: 'cockpit_canopy',
            shape: 'wedge',
            size: [sw * 0.65, sh * 0.65, sl * 0.28],
            position: [0, sh * 1.45, sl * 0.08],
            color: '#319795',
            roughness: 0.2
          },
          // Left Wing (wedge)
          {
            name: 'wing_left',
            shape: 'wedge',
            size: [wingSpan * 0.45, 0.08, sl * 0.45],
            position: [-sw * 0.5 - wingSpan * 0.22, sh * 0.85, -sl * 0.12],
            rotation: [0, 15, 0],
            color: mainColor,
            roughness: 0.6
          },
          // Right Wing (wedge)
          {
            name: 'wing_right',
            shape: 'wedge',
            size: [wingSpan * 0.45, 0.08, sl * 0.45],
            position: [sw * 0.5 + wingSpan * 0.22, sh * 0.85, -sl * 0.12],
            rotation: [0, -15, 0],
            color: mainColor,
            roughness: 0.6
          },
          // Vertical Stabilizer Fin
          {
            name: 'tail_fin',
            shape: 'wedge',
            size: [0.08, sh * 1.1, sl * 0.35],
            position: [0, sh * 1.7, -sl * 0.32],
            color: '#1a202c'
          },
          // Dual Thrusters
          {
            name: 'thruster_left',
            shape: 'cylinder',
            size: [sw * 0.22, sw * 0.25, sl * 0.2, 8],
            position: [-sw * 0.32, sh * 0.9, -sl * 0.45],
            rotation: [90, 0, 0],
            color: '#718096',
            metalness: 0.8
          },
          {
            name: 'thruster_right',
            shape: 'cylinder',
            size: [sw * 0.22, sw * 0.25, sl * 0.2, 8],
            position: [sw * 0.32, sh * 0.9, -sl * 0.45],
            rotation: [90, 0, 0],
            color: '#718096',
            metalness: 0.8
          },
          // Plasma Exhaust Plumes
          {
            name: 'plasma_left',
            shape: 'cone',
            size: [sw * 0.16, sl * 0.18, 6],
            position: [-sw * 0.32, sh * 0.9, -sl * 0.58],
            rotation: [-90, 0, 0],
            color: '#3182ce'
          },
          {
            name: 'plasma_right',
            shape: 'cone',
            size: [sw * 0.16, sl * 0.18, 6],
            position: [sw * 0.32, sh * 0.9, -sl * 0.58],
            rotation: [-90, 0, 0],
            color: '#3182ce'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 3. ROBOT / MECH / ANDROIDE / AUTÓMATA
    // -------------------------------------------------------------
    if (/robot|mech|androide|automata|droide/.test(lower)) {
      const rw = 0.8 * baseDim;
      const rh = 1.9 * baseDim;
      const rd = 0.5 * baseDim;

      return {
        id: 'below_nominal.security.service_droid',
        name: 'Unidad Robótica Bípeda',
        category: 'security',
        description: 'Autómata procedural con torso reforzado, visor óptico y extremidades mecánicas.',
        units: 'meters',
        dimensions: { width: rw * 1.5, depth: rd * 1.2, height: rh },
        palette: 'industrial_hazard',
        components: [
          // Torso Core
          {
            name: 'torso_chassis',
            shape: 'box',
            size: [rw, rh * 0.35, rd],
            position: [0, rh * 0.65, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Head Unit
          {
            name: 'head_unit',
            shape: 'box',
            size: [rw * 0.5, rh * 0.18, rd * 0.8],
            position: [0, rh * 0.92, 0],
            color: '#2d3748',
            roughness: 0.7
          },
          // Optical Visor LED
          {
            name: 'optical_visor',
            shape: 'box',
            size: [rw * 0.42, rh * 0.05, 0.05],
            position: [0, rh * 0.92, rd * 0.42],
            color: '#e53e3e',
            roughness: 0.2
          },
          // Head Antenna
          {
            name: 'comm_antenna',
            shape: 'cylinder',
            size: [0.015, 0.015, rh * 0.18, 4],
            position: [rw * 0.2, rh * 1.08, 0],
            color: '#cbd5e0'
          },
          // Pelvis Mount
          {
            name: 'pelvis_mount',
            shape: 'box',
            size: [rw * 0.75, rh * 0.1, rd * 0.85],
            position: [0, rh * 0.43, 0],
            color: '#1a202c'
          },
          // Legs
          {
            name: 'leg_left',
            shape: 'box',
            size: [rw * 0.24, rh * 0.38, rd * 0.5],
            position: [-rw * 0.26, rh * 0.2, 0],
            color: mainColor,
            metalness: 0.5
          },
          {
            name: 'leg_right',
            shape: 'box',
            size: [rw * 0.24, rh * 0.38, rd * 0.5],
            position: [rw * 0.26, rh * 0.2, 0],
            color: mainColor,
            metalness: 0.5
          },
          // Feet Plates
          {
            name: 'foot_left',
            shape: 'box',
            size: [rw * 0.28, 0.06, rd * 0.9],
            position: [-rw * 0.26, 0.03, rd * 0.15],
            color: '#1a202c'
          },
          {
            name: 'foot_right',
            shape: 'box',
            size: [rw * 0.28, 0.06, rd * 0.9],
            position: [rw * 0.26, 0.03, rd * 0.15],
            color: '#1a202c'
          },
          // Arms
          {
            name: 'arm_left',
            shape: 'box',
            size: [rw * 0.18, rh * 0.35, rd * 0.4],
            position: [-rw * 0.62, rh * 0.62, 0],
            color: '#4a5568'
          },
          {
            name: 'arm_right',
            shape: 'box',
            size: [rw * 0.18, rh * 0.35, rd * 0.4],
            position: [rw * 0.62, rh * 0.62, 0],
            color: '#4a5568'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 4. WEAPON / PISTOLA / BLASTER / ARMA / RIFLE
    // -------------------------------------------------------------
    if (/arma|pistola|blaster|rifle|fusil|laser|gun|canon|torreta/.test(lower)) {
      const gw = 0.12 * baseDim;
      const gh = 0.45 * baseDim;
      const gl = 0.95 * baseDim;

      return {
        id: 'below_nominal.weapons.plasma_blaster',
        name: 'Blaster de Plasma Retro',
        category: 'weapons',
        description: 'Arma de energía con empuñadura ergonómica, cañón reforzado y celda de plasma.',
        units: 'meters',
        dimensions: { width: gw * 1.5, depth: gl, height: gh },
        palette: 'industrial_hazard',
        components: [
          // Handle / Grip
          {
            name: 'grip_handle',
            shape: 'box',
            size: [gw * 0.8, gh * 0.55, gl * 0.2],
            position: [0, gh * 0.28, -gl * 0.25],
            rotation: [15, 0, 0],
            color: '#1a202c',
            roughness: 0.9
          },
          // Receiver Body
          {
            name: 'receiver_core',
            shape: 'box',
            size: [gw, gh * 0.4, gl * 0.65],
            position: [0, gh * 0.65, gl * 0.05],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Barrel Cylinder
          {
            name: 'plasma_barrel',
            shape: 'cylinder',
            size: [gw * 0.4, gw * 0.4, gl * 0.45, 8],
            position: [0, gh * 0.68, gl * 0.55],
            rotation: [90, 0, 0],
            color: '#718096',
            metalness: 0.8
          },
          // Muzzle Flash Hider
          {
            name: 'muzzle_tip',
            shape: 'cylinder',
            size: [gw * 0.48, gw * 0.45, gl * 0.08, 8],
            position: [0, gh * 0.68, gl * 0.8],
            rotation: [90, 0, 0],
            color: '#1a202c',
            metalness: 0.9
          },
          // Optical Scope
          {
            name: 'targeting_scope',
            shape: 'box',
            size: [gw * 0.6, gh * 0.18, gl * 0.32],
            position: [0, gh * 0.92, -gl * 0.02],
            color: '#e53e3e',
            roughness: 0.3
          },
          // Energy Cell Magazine
          {
            name: 'energy_magazine',
            shape: 'box',
            size: [gw * 0.75, gh * 0.3, gl * 0.18],
            position: [0, gh * 0.35, gl * 0.08],
            color: '#319795',
            roughness: 0.3
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 5. CHAIR / SILLA / ASIENTO / BUTACA / SOFA
    // -------------------------------------------------------------
    if (/silla|chair|asiento|butaca|sofa|sillon|banco/.test(lower) && !/mesa|consola/.test(lower)) {
      const sw = 0.65 * baseDim;
      const sd = 0.65 * baseDim;
      const sh = 0.95 * baseDim;
      const seatH = 0.45 * baseDim;

      return {
        id: 'below_nominal.furniture.station_chair',
        name: 'Silla Operativa de Mando',
        category: 'furniture',
        description: 'Asiento ergonómico reforzado con respaldo curvo y base tubular.',
        units: 'meters',
        dimensions: { width: sw, depth: sd, height: sh },
        palette: 'standard',
        components: [
          // Seat Pad
          {
            name: 'seat_cushion',
            shape: 'box',
            size: [sw, 0.08, sd],
            position: [0, seatH, 0],
            color: mainColor,
            roughness: 0.7
          },
          // Backrest
          {
            name: 'backrest',
            shape: 'box',
            size: [sw * 0.92, sh - seatH, 0.08],
            position: [0, seatH + (sh - seatH) * 0.5, -sd * 0.45],
            color: mainColor,
            roughness: 0.7
          },
          // 4 Legs
          {
            name: 'leg_front_left',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [-sw * 0.4, (seatH - 0.04) * 0.5, sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          },
          {
            name: 'leg_front_right',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [sw * 0.4, (seatH - 0.04) * 0.5, sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          },
          {
            name: 'leg_rear_left',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [-sw * 0.4, (seatH - 0.04) * 0.5, -sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          },
          {
            name: 'leg_rear_right',
            shape: 'cylinder',
            size: [0.03, 0.03, seatH - 0.04, 6],
            position: [sw * 0.4, (seatH - 0.04) * 0.5, -sd * 0.38],
            color: '#2d3748',
            metalness: 0.7
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 6. DOOR / PUERTA / COMPUERTA / AIRLOCK / HATCH
    // -------------------------------------------------------------
    if (/puerta|door|compuerta|airlock|hatch/.test(lower)) {
      const dw = 1.4 * baseDim;
      const dh = 2.2 * baseDim;
      const dd = 0.25 * baseDim;

      return {
        id: 'below_nominal.infrastructure.airlock_door',
        name: 'Compuerta de Presión Blindada',
        category: 'infrastructure',
        description: 'Puerta hermética de doble hoja con marco blindado y panel de control de acceso.',
        units: 'meters',
        dimensions: { width: dw, depth: dd, height: dh },
        palette: 'industrial_hazard',
        components: [
          // Left Door Frame
          {
            name: 'frame_left',
            shape: 'box',
            size: [dw * 0.12, dh, dd],
            position: [-dw * 0.44, dh * 0.5, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Right Door Frame
          {
            name: 'frame_right',
            shape: 'box',
            size: [dw * 0.12, dh, dd],
            position: [dw * 0.44, dh * 0.5, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Top Frame Header
          {
            name: 'frame_top',
            shape: 'box',
            size: [dw, dh * 0.08, dd],
            position: [0, dh * 0.96, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Left Sliding Panel
          {
            name: 'panel_left',
            shape: 'box',
            size: [dw * 0.38, dh * 0.88, dd * 0.4],
            position: [-dw * 0.19, dh * 0.48, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Right Sliding Panel
          {
            name: 'panel_right',
            shape: 'box',
            size: [dw * 0.38, dh * 0.88, dd * 0.4],
            position: [dw * 0.19, dh * 0.48, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Keypad / Access Reader
          {
            name: 'access_keypad',
            shape: 'box',
            size: [0.15, 0.25, 0.04],
            position: [dw * 0.48, dh * 0.55, dd * 0.52],
            color: '#319795',
            roughness: 0.3
          },
          // Status LED Beacon (Green)
          {
            name: 'status_beacon',
            shape: 'box',
            size: [0.12, 0.06, 0.04],
            position: [0, dh * 0.94, dd * 0.52],
            color: '#38a169',
            roughness: 0.2
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 7. DRONE / CUADRICÓPTERO / DRON
    // -------------------------------------------------------------
    if (/dron|drone|cuadricoptero|probeta|sensor orbital/.test(lower)) {
      const bw = 0.45 * baseDim;
      const armL = 0.5 * baseDim;
      const rotR = 0.25 * baseDim;

      return {
        id: 'below_nominal.security.survey_drone',
        name: 'Dron de Vigilancia Orbital',
        category: 'security',
        description: 'Sonda voladora autónoma con 4 rotores perimetrales y sensor fotónico inferior.',
        units: 'meters',
        dimensions: { width: armL * 2.8, depth: armL * 2.8, height: bw * 1.2 },
        palette: 'industrial_hazard',
        components: [
          // Central Core
          {
            name: 'core_fuselage',
            shape: 'cylinder',
            size: [bw * 0.5, bw * 0.5, bw * 0.6, 8],
            position: [0, bw * 0.8, 0],
            color: mainColor,
            metalness: 0.4
          },
          // Sensor Dome (eye)
          {
            name: 'sensor_eye',
            shape: 'sphere',
            size: [bw * 0.25, 8, 6],
            position: [0, bw * 0.48, 0],
            color: '#319795'
          },
          // 4 Carbon Arms in X
          {
            name: 'arm_fl',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [-armL * 0.5, bw * 0.8, armL * 0.5],
            rotation: [0, 45, 0],
            color: '#1a202c'
          },
          {
            name: 'arm_fr',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [armL * 0.5, bw * 0.8, armL * 0.5],
            rotation: [0, -45, 0],
            color: '#1a202c'
          },
          {
            name: 'arm_rl',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [-armL * 0.5, bw * 0.8, -armL * 0.5],
            rotation: [0, -45, 0],
            color: '#1a202c'
          },
          {
            name: 'arm_rr',
            shape: 'box',
            size: [0.05, 0.04, armL],
            position: [armL * 0.5, bw * 0.8, -armL * 0.5],
            rotation: [0, 45, 0],
            color: '#1a202c'
          },
          // 4 Rotors
          {
            name: 'rotor_fl',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [-armL * 0.85, bw * 0.86, armL * 0.85],
            color: '#718096'
          },
          {
            name: 'rotor_fr',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [armL * 0.85, bw * 0.86, armL * 0.85],
            color: '#718096'
          },
          {
            name: 'rotor_rl',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [-armL * 0.85, bw * 0.86, -armL * 0.85],
            color: '#718096'
          },
          {
            name: 'rotor_rr',
            shape: 'cylinder',
            size: [rotR, rotR, 0.02, 8],
            position: [armL * 0.85, bw * 0.86, -armL * 0.85],
            color: '#718096'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 8. BED / CAMA / LITERA / CAMILLA
    // -------------------------------------------------------------
    if (/cama|litera|camilla|stasis|cryo/.test(lower)) {
      const bw = 1.0 * baseDim;
      const bl = 2.1 * baseDim;
      const bh = 0.55 * baseDim;

      return {
        id: 'below_nominal.furniture.station_bed',
        name: 'Cama / Camilla de Estación',
        category: 'furniture',
        description: 'Litera modular de tripulación con colchón higiénico y cabecero integrado.',
        units: 'meters',
        dimensions: { width: bw, depth: bl, height: bh * 1.5 },
        palette: 'standard',
        components: [
          // Frame Base
          {
            name: 'bed_frame',
            shape: 'box',
            size: [bw, bh * 0.5, bl],
            position: [0, bh * 0.25, 0],
            color: '#2d3748',
            metalness: 0.5
          },
          // Mattress
          {
            name: 'mattress',
            shape: 'box',
            size: [bw * 0.94, bh * 0.35, bl * 0.94],
            position: [0, bh * 0.65, 0],
            color: mainColor,
            roughness: 0.8
          },
          // Pillow
          {
            name: 'pillow',
            shape: 'box',
            size: [bw * 0.75, bh * 0.18, bl * 0.2],
            position: [0, bh * 0.88, -bl * 0.35],
            color: '#edf2f7',
            roughness: 0.9
          },
          // Headboard
          {
            name: 'headboard',
            shape: 'box',
            size: [bw, bh * 0.9, 0.1],
            position: [0, bh * 0.8, -bl * 0.48],
            color: '#1a202c'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // LIFE SUPPORT / OXYGEN RECHARGE STATION / ESTACIÓN DE OXÍGENO
    // -------------------------------------------------------------
    if (/oxigeno|oxígeno|soporte vital|traje.*oxigen|llenar.*oxigen|recarga.*oxigen|tanque.*oxigen|oxygen|life_?support|respirador/.test(lower)) {
      const sw = 1.10 * baseDim;
      const sd = 0.85 * baseDim;
      const sh = 1.80 * baseDim;

      return {
        id: 'below_nominal.station.oxygen_recharge_station',
        name: 'Estación de Recarga de Oxígeno EVA',
        category: 'medical',
        description: 'Unidad industrial de presurización y recarga de oxígeno para trajes espaciales y tanques portátiles con display de telemetría y manómetros.',
        units: 'meters',
        dimensions: { width: sw, depth: sd, height: sh },
        palette: 'medical_bay',
        components: [
          // 1. Heavy Base Plinth
          {
            name: 'heavy_base',
            shape: 'chamfer_box',
            size: [sw, 0.12, sd],
            position: [0, 0.06, 0],
            color: '#1a202c',
            roughness: 0.9,
            texturePreset: 'metal_dark'
          },
          // 2. EVA Suit Foot Plate / Non-slip platform
          {
            name: 'dock_footplate',
            shape: 'box',
            size: [sw * 0.55, 0.03, sd * 0.45],
            position: [0, 0.135, sd * 0.18],
            color: '#2d3748',
            texturePreset: 'metal_dark'
          },
          // 3. Central Equipment Cabinet
          {
            name: 'main_cabinet',
            shape: 'chamfer_box',
            size: [sw * 0.65, sh * 0.75, sd * 0.42],
            position: [0, 0.12 + (sh * 0.75) / 2, -sd * 0.18],
            color: mainColor || '#e2e8f0',
            roughness: 0.4,
            texturePreset: 'panel_beige'
          },
          // 4. Dual High-Pressure Oxygen Tanks (Vertical Cylinders)
          {
            name: 'tank_left',
            shape: 'cylinder',
            size: [0.12 * baseDim, 0.12 * baseDim, sh * 0.60, 12],
            position: [-sw * 0.42, 0.12 + (sh * 0.60) / 2, -sd * 0.12],
            color: '#2b6cb0',
            roughness: 0.3,
            metalness: 0.4,
            texturePreset: 'painted_metal'
          },
          {
            name: 'tank_right',
            shape: 'cylinder',
            size: [0.12 * baseDim, 0.12 * baseDim, sh * 0.60, 12],
            position: [sw * 0.42, 0.12 + (sh * 0.60) / 2, -sd * 0.12],
            color: '#2b6cb0',
            roughness: 0.3,
            metalness: 0.4,
            texturePreset: 'painted_metal'
          },
          // 5. Tank Domes / Caps
          {
            name: 'tank_dome_left',
            shape: 'sphere',
            size: [0.12 * baseDim, 0.12 * baseDim, 0.12 * baseDim],
            position: [-sw * 0.42, 0.12 + sh * 0.60, -sd * 0.12],
            color: '#e2e8f0',
            metalness: 0.6
          },
          {
            name: 'tank_dome_right',
            shape: 'sphere',
            size: [0.12 * baseDim, 0.12 * baseDim, 0.12 * baseDim],
            position: [sw * 0.42, 0.12 + sh * 0.60, -sd * 0.12],
            color: '#e2e8f0',
            metalness: 0.6
          },
          // 6. Tank Retaining Steel Brackets
          {
            name: 'bracket_lower_left',
            shape: 'box',
            size: [0.10 * baseDim, 0.05, 0.18 * baseDim],
            position: [-sw * 0.38, 0.45 * baseDim, -sd * 0.15],
            color: '#4a5568',
            metalness: 0.8
          },
          {
            name: 'bracket_upper_left',
            shape: 'box',
            size: [0.10 * baseDim, 0.05, 0.18 * baseDim],
            position: [-sw * 0.38, 0.95 * baseDim, -sd * 0.15],
            color: '#4a5568',
            metalness: 0.8
          },
          {
            name: 'bracket_lower_right',
            shape: 'box',
            size: [0.10 * baseDim, 0.05, 0.18 * baseDim],
            position: [sw * 0.38, 0.45 * baseDim, -sd * 0.15],
            color: '#4a5568',
            metalness: 0.8
          },
          {
            name: 'bracket_upper_right',
            shape: 'box',
            size: [0.10 * baseDim, 0.05, 0.18 * baseDim],
            position: [sw * 0.38, 0.95 * baseDim, -sd * 0.15],
            color: '#4a5568',
            metalness: 0.8
          },
          // 7. Telemetry & Control Screen Housing (with upward tilt for ergonomic viewing)
          {
            name: 'screen_housing',
            shape: 'chamfer_box',
            size: [sw * 0.50, sh * 0.22, 0.07],
            position: [0, sh * 0.68, 0.04],
            rotation: [-14, 0, 0],
            color: '#2d3748',
            roughness: 0.8
          },
          // 8. Active O2 Digital Display Screen
          {
            name: 'screen_display',
            shape: 'box',
            size: [sw * 0.44, sh * 0.18, 0.015],
            position: [0, sh * 0.68, 0.08],
            rotation: [-14, 0, 0],
            color: '#319795',
            roughness: 0.2
          },
          // 9. Dual Pressure Gauges / Manometers
          {
            name: 'gauge_o2_flow',
            shape: 'cylinder',
            size: [0.06 * baseDim, 0.06 * baseDim, 0.025, 10],
            position: [-sw * 0.15, sh * 0.48, 0.04],
            rotation: [90, 0, 0],
            color: '#edf2f7',
            metalness: 0.7
          },
          {
            name: 'gauge_o2_pressure',
            shape: 'cylinder',
            size: [0.06 * baseDim, 0.06 * baseDim, 0.025, 10],
            position: [sw * 0.15, sh * 0.48, 0.04],
            rotation: [90, 0, 0],
            color: '#edf2f7',
            metalness: 0.7
          },
          // 10. Emergency Cutoff Safety Valve
          {
            name: 'emergency_valve',
            shape: 'cylinder',
            size: [0.05 * baseDim, 0.05 * baseDim, 0.035, 8],
            position: [0, sh * 0.48, 0.045],
            rotation: [90, 0, 0],
            color: '#e53e3e',
            roughness: 0.4
          },
          // 11. Dual Hanging Oxygen Hoses / Fill Conduits
          {
            name: 'hose_eva_left',
            shape: 'pipe',
            size: [0.02 * baseDim, 0.02 * baseDim, 0.38 * baseDim, 8],
            position: [-sw * 0.18, sh * 0.28, 0.06],
            color: '#1a202c',
            roughness: 0.8
          },
          {
            name: 'hose_eva_right',
            shape: 'pipe',
            size: [0.02 * baseDim, 0.02 * baseDim, 0.38 * baseDim, 8],
            position: [sw * 0.18, sh * 0.28, 0.06],
            color: '#1a202c',
            roughness: 0.8
          },
          // 12. Warning Decal Banner
          {
            name: 'hazard_strip',
            shape: 'box',
            size: [sw * 0.65, 0.05, 0.015],
            position: [0, sh * 0.84, 0.035],
            color: '#ecc94b',
            texturePreset: 'hazard_stripes'
          },
          // 13. System Status LED
          {
            name: 'status_led',
            shape: 'box',
            size: [0.08, 0.03, 0.02],
            position: [sw * 0.20, sh * 0.78, 0.04],
            color: '#38a169',
            roughness: 0.1
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 9. COMPUTER / LAPTOP / MONITOR / PANTALLA
    // -------------------------------------------------------------
    if (/computadora|computador|laptop|monitor|pantalla|display|pc/.test(lower) && !/consola/.test(lower)) {
      const lw = 0.6 * baseDim;
      const ld = 0.45 * baseDim;

      return {
        id: 'below_nominal.command.terminal_screen',
        name: 'Terminal de Pantalla y Teclado',
        category: 'command',
        description: 'Unidad de computación personal con display fosfórico y teclado integrado.',
        units: 'meters',
        dimensions: { width: lw, depth: ld, height: lw * 0.8 },
        palette: 'command_bridge',
        components: [
          // Keyboard Base
          {
            name: 'keyboard_base',
            shape: 'box',
            size: [lw, 0.04, ld * 0.65],
            position: [0, 0.02, ld * 0.15],
            color: '#1a202c',
            roughness: 0.8
          },
          // Slanted Screen Housing
          {
            name: 'screen_housing',
            shape: 'box',
            size: [lw * 0.95, lw * 0.65, 0.05],
            position: [0, lw * 0.38, -ld * 0.2],
            rotation: [-15, 0, 0],
            color: mainColor,
            metalness: 0.3
          },
          // Active Display (Cyan phosphor)
          {
            name: 'screen_display',
            shape: 'box',
            size: [lw * 0.85, lw * 0.52, 0.01],
            position: [0, lw * 0.38, -ld * 0.17],
            rotation: [-15, 0, 0],
            color: '#319795',
            roughness: 0.2
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 10. SERVER RACK / SERVIDOR
    // -------------------------------------------------------------
    if (/servidor|server|rack|rack de servidores/.test(lower)) {
      const rw = 0.8 * baseDim;
      const rh = 2.0 * baseDim;
      const rd = 0.9 * baseDim;

      return {
        id: 'below_nominal.command.server_rack',
        name: 'Rack de Servidores Principal',
        category: 'command',
        description: 'Gabinete vertical de cómputo con bahías ventiladas y telemetría LED.',
        units: 'meters',
        dimensions: { width: rw, depth: rd, height: rh },
        palette: 'command_bridge',
        components: [
          // Main Server Cabinet
          {
            name: 'rack_cabinet',
            shape: 'box',
            size: [rw, rh, rd],
            position: [0, rh * 0.5, 0],
            color: '#1a202c',
            metalness: 0.7
          },
          // Server Blade Bay 1
          {
            name: 'blade_bay_1',
            shape: 'box',
            size: [rw * 0.88, rh * 0.12, 0.02],
            position: [0, rh * 0.8, rd * 0.505],
            color: mainColor,
            metalness: 0.5
          },
          // Server Blade Bay 2
          {
            name: 'blade_bay_2',
            shape: 'box',
            size: [rw * 0.88, rh * 0.12, 0.02],
            position: [0, rh * 0.62, rd * 0.505],
            color: mainColor,
            metalness: 0.5
          },
          // Server Blade Bay 3
          {
            name: 'blade_bay_3',
            shape: 'box',
            size: [rw * 0.88, rh * 0.12, 0.02],
            position: [0, rh * 0.44, rd * 0.505],
            color: mainColor,
            metalness: 0.5
          },
          // LED Status Lights
          {
            name: 'led_array_1',
            shape: 'box',
            size: [0.12, 0.03, 0.01],
            position: [-rw * 0.3, rh * 0.8, rd * 0.52],
            color: '#38a169'
          },
          {
            name: 'led_array_2',
            shape: 'box',
            size: [0.12, 0.03, 0.01],
            position: [-rw * 0.3, rh * 0.62, rd * 0.52],
            color: '#ecc94b'
          },
          {
            name: 'led_array_3',
            shape: 'box',
            size: [0.12, 0.03, 0.01],
            position: [-rw * 0.3, rh * 0.44, rd * 0.52],
            color: '#3182ce'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 11. BARREL / BARRIL / TANQUE / DRUM
    // -------------------------------------------------------------
    if (/barril|barrel|drum|bidon|tanque de combustible/.test(lower) && !/columna/.test(lower)) {
      const br = 0.35 * baseDim;
      const bh = 1.0 * baseDim;

      return {
        id: 'below_nominal.infrastructure.chemical_drum',
        name: 'Barril Químico Estriado',
        category: 'infrastructure',
        description: 'Contenedor cilíndrico estriado para fluidos presurizados con aros de refuerzo.',
        units: 'meters',
        dimensions: { width: br * 2.2, depth: br * 2.2, height: bh },
        palette: 'industrial_hazard',
        components: [
          // Main Drum Body
          {
            name: 'drum_body',
            shape: 'cylinder',
            size: [br, br, bh, 10],
            position: [0, bh * 0.5, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.4
          },
          // Top Reinforcement Rib
          {
            name: 'rib_top',
            shape: 'cylinder',
            size: [br * 1.06, br * 1.06, 0.06, 10],
            position: [0, bh * 0.75, 0],
            color: '#1a202c'
          },
          // Bottom Reinforcement Rib
          {
            name: 'rib_bottom',
            shape: 'cylinder',
            size: [br * 1.06, br * 1.06, 0.06, 10],
            position: [0, bh * 0.25, 0],
            color: '#1a202c'
          },
          // Valve Cap
          {
            name: 'valve_cap',
            shape: 'cylinder',
            size: [br * 0.2, br * 0.2, 0.05, 6],
            position: [br * 0.45, bh + 0.02, 0],
            color: '#d69e2e',
            metalness: 0.7
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 11B. WELDING MACHINE / SOLDADORA / GENERADOR / INVERTER
    // -------------------------------------------------------------
    if (/soldar|soldadora|soldadura|generador|soldador|maquina de soldar|planta electrica|inverter|compresor/.test(lower)) {
      const sw = 0.72 * baseDim;
      const sh = 0.54 * baseDim;
      const sd = 0.52 * baseDim;

      return {
        id: 'below_nominal.infrastructure.industrial_welder',
        name: 'Unidad de Soldadura Industrial Inverter ARC-400',
        category: 'infrastructure',
        description: 'Estación de soldadura industrial pesada con panel de control digital, tanque de argón y asa de transporte.',
        units: 'meters',
        dimensions: { width: sw * 1.15, depth: sd * 1.1, height: sh * 1.3 },
        palette: 'industrial_hazard',
        components: [
          // Lower Chassis Base Plinth
          {
            name: 'chassis_plinth',
            shape: 'box',
            size: [sw, 0.06 * baseDim, sd],
            position: [0, 0.03 * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'diamond_plate',
            metalness: 0.7,
            roughness: 0.5
          },
          // 4 Ground Dampeners (Rubber Feet)
          {
            name: 'rubber_foot_fl',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [-sw * 0.42, 0.02 * baseDim, sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          {
            name: 'rubber_foot_fr',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [sw * 0.42, 0.02 * baseDim, sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          {
            name: 'rubber_foot_bl',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [-sw * 0.42, 0.02 * baseDim, -sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          {
            name: 'rubber_foot_br',
            shape: 'cylinder',
            size: [0.035 * baseDim, 0.035 * baseDim, 0.04 * baseDim, 8],
            position: [sw * 0.42, 0.02 * baseDim, -sd * 0.40],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          // Main Transformer Housing
          {
            name: 'inverter_housing',
            shape: 'box',
            size: [sw * 0.92, sh * 0.85, sd * 0.88],
            position: [0, (0.06 + sh * 0.425) * baseDim, 0],
            color: mainColor || '#dd6b20',
            texturePreset: 'worn_metal',
            metalness: 0.4,
            roughness: 0.6
          },
          // Front Control Panel Plate (Flush mounted)
          {
            name: 'front_control_plate',
            shape: 'box',
            size: [sw * 0.80, sh * 0.70, 0.02 * baseDim],
            position: [0, (0.06 + sh * 0.425) * baseDim, (sd * 0.44 + 0.01) * baseDim],
            color: '#2d3748',
            texturePreset: 'plastic_abs_matte',
            roughness: 0.8
          },
          // Digital Amperage Display Screen
          {
            name: 'digital_screen',
            shape: 'box',
            size: [0.20 * baseDim, 0.10 * baseDim, 0.01 * baseDim],
            position: [-0.14 * baseDim, (0.06 + sh * 0.55) * baseDim, (sd * 0.44 + 0.025) * baseDim],
            color: '#38a169',
            texturePreset: 'crt_screen_green'
          },
          // Rotary Control Dial
          {
            name: 'amperage_rotary_dial',
            shape: 'cylinder',
            size: [0.045 * baseDim, 0.045 * baseDim, 0.03 * baseDim, 12],
            position: [0.14 * baseDim, (0.06 + sh * 0.55) * baseDim, (sd * 0.44 + 0.035) * baseDim],
            rotation: [90, 0, 0],
            color: '#ecc94b',
            texturePreset: 'brass_burnished'
          },
          // Negative Ground Dinse Connector
          {
            name: 'terminal_ground_dinse',
            shape: 'cylinder',
            size: [0.03 * baseDim, 0.03 * baseDim, 0.04 * baseDim, 10],
            position: [-0.16 * baseDim, (0.06 + sh * 0.22) * baseDim, (sd * 0.44 + 0.04) * baseDim],
            rotation: [90, 0, 0],
            color: '#1a202c',
            texturePreset: 'rubber_black'
          },
          // Positive Electrode Dinse Connector
          {
            name: 'terminal_electrode_dinse',
            shape: 'cylinder',
            size: [0.03 * baseDim, 0.03 * baseDim, 0.04 * baseDim, 10],
            position: [0.16 * baseDim, (0.06 + sh * 0.22) * baseDim, (sd * 0.44 + 0.04) * baseDim],
            rotation: [90, 0, 0],
            color: '#e53e3e',
            texturePreset: 'red_paint_worn'
          },
          // Top Ergonomic Carry Handle
          {
            name: 'top_handle_grip',
            shape: 'box',
            size: [0.38 * baseDim, 0.045 * baseDim, 0.04 * baseDim],
            position: [0, (0.06 + sh * 0.85 + 0.08) * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'rubber_ribbed_mat'
          },
          {
            name: 'handle_riser_front',
            shape: 'box',
            size: [0.04 * baseDim, 0.08 * baseDim, 0.04 * baseDim],
            position: [0, (0.06 + sh * 0.85 + 0.04) * baseDim, 0.16 * baseDim],
            color: '#718096',
            texturePreset: 'steel_polished'
          },
          {
            name: 'handle_riser_back',
            shape: 'box',
            size: [0.04 * baseDim, 0.08 * baseDim, 0.04 * baseDim],
            position: [0, (0.06 + sh * 0.85 + 0.04) * baseDim, -0.16 * baseDim],
            color: '#718096',
            texturePreset: 'steel_polished'
          },
          // Side Exhaust Vent Grill
          {
            name: 'side_cooling_vent_left',
            shape: 'box',
            size: [0.01 * baseDim, sh * 0.50, sd * 0.60],
            position: [-sw * 0.465 * baseDim, (0.06 + sh * 0.425) * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'vent_grill'
          },
          {
            name: 'side_cooling_vent_right',
            shape: 'box',
            size: [0.01 * baseDim, sh * 0.50, sd * 0.60],
            position: [sw * 0.465 * baseDim, (0.06 + sh * 0.425) * baseDim, 0],
            color: '#1a202c',
            texturePreset: 'vent_grill'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 12. CRATE / CAJA / CONTENEDOR / BAUL
    // -------------------------------------------------------------
    if (/caja|crate|contenedor|container|baul|cofre|cargo/.test(lower)) {
      const cw = 1.0 * baseDim;
      const ch = 0.85 * baseDim;
      const cd = 1.0 * baseDim;

      return {
        id: 'below_nominal.infrastructure.cargo_crate',
        name: 'Contenedor de Carga Reforzado',
        category: 'infrastructure',
        description: 'Caja cúbica de transporte con cantoneras de acero y nervaduras diagonales.',
        units: 'meters',
        dimensions: { width: cw, depth: cd, height: ch },
        palette: 'industrial_hazard',
        components: [
          // Main Crate Core
          {
            name: 'crate_core',
            shape: 'box',
            size: [cw, ch, cd],
            position: [0, ch * 0.5, 0],
            color: mainColor,
            roughness: 0.7
          },
          // Top Rim Frame
          {
            name: 'rim_top',
            shape: 'box',
            size: [cw * 1.04, 0.08, cd * 1.04],
            position: [0, ch * 0.96, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Bottom Rim Frame
          {
            name: 'rim_bottom',
            shape: 'box',
            size: [cw * 1.04, 0.08, cd * 1.04],
            position: [0, 0.04, 0],
            color: '#1a202c',
            metalness: 0.6
          },
          // Front Cross Stiffener
          {
            name: 'front_latch',
            shape: 'box',
            size: [cw * 0.25, ch * 0.15, 0.04],
            position: [0, ch * 0.5, cd * 0.51],
            color: '#ecc94b',
            metalness: 0.8
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 13. LAMP / FOCO / LINTERNA / BALIZA / LUZ
    // -------------------------------------------------------------
    if (/lampara|foco|linterna|luz|baliza|farola|sirena/.test(lower)) {
      const lh = 1.8 * baseDim;
      const lr = 0.04 * baseDim;

      return {
        id: 'below_nominal.fixtures.light_post',
        name: 'Poste de Iluminación Industrial',
        category: 'fixtures',
        description: 'Luminaria vertical con pie estabilizador y cabezal difusor de alta emisión.',
        units: 'meters',
        dimensions: { width: 0.6 * baseDim, depth: 0.6 * baseDim, height: lh },
        palette: 'standard',
        components: [
          // Base Pedestal
          {
            name: 'pedestal',
            shape: 'cylinder',
            size: [0.25, 0.28, 0.08, 8],
            position: [0, 0.04, 0],
            color: '#1a202c'
          },
          // Pole
          {
            name: 'lamp_pole',
            shape: 'cylinder',
            size: [lr, lr, lh * 0.8, 6],
            position: [0, lh * 0.44, 0],
            color: '#4a5568',
            metalness: 0.6
          },
          // Lamp Housing
          {
            name: 'lamp_housing',
            shape: 'box',
            size: [0.45, 0.15, 0.3],
            position: [0, lh * 0.88, 0],
            color: mainColor,
            metalness: 0.4
          },
          // Bright Emissive Lens
          {
            name: 'emissive_lens',
            shape: 'box',
            size: [0.4, 0.06, 0.26],
            position: [0, lh * 0.82, 0],
            color: '#ecc94b',
            roughness: 0.1
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 14. ANTENNA / RADAR / DISH
    // -------------------------------------------------------------
    if (/antena|radar|dish|parabolica|comunicaciones/.test(lower)) {
      const ah = 2.4 * baseDim;
      const dishR = 0.8 * baseDim;

      return {
        id: 'below_nominal.infrastructure.radar_dish',
        name: 'Antena Parabólica de Enlace',
        category: 'infrastructure',
        description: 'Receptor parabólico orbital con mástil orientable y emisor focal.',
        units: 'meters',
        dimensions: { width: dishR * 2, depth: dishR * 2, height: ah },
        palette: 'standard',
        components: [
          // Base Tripod Mount
          {
            name: 'mount_base',
            shape: 'cylinder',
            size: [0.4, 0.5, 0.15, 6],
            position: [0, 0.075, 0],
            color: '#1a202c'
          },
          // Mast
          {
            name: 'antenna_mast',
            shape: 'cylinder',
            size: [0.06, 0.06, ah * 0.6, 6],
            position: [0, ah * 0.35, 0],
            color: '#718096',
            metalness: 0.7
          },
          // Dish Back Frame
          {
            name: 'dish_frame',
            shape: 'cylinder',
            size: [dishR, dishR * 0.3, 0.12, 10],
            position: [0, ah * 0.75, 0],
            rotation: [30, 0, 0],
            color: mainColor,
            metalness: 0.5
          },
          // Focal Feed Horn
          {
            name: 'feed_horn',
            shape: 'cylinder',
            size: [0.04, 0.08, 0.35, 6],
            position: [0, ah * 0.85, dishR * 0.4],
            rotation: [30, 0, 0],
            color: '#e53e3e',
            metalness: 0.8
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 15. SWORD / ESPADA / SABLE / CUCHILLO
    // -------------------------------------------------------------
    if (/espada|sable|sword|cuchillo|daga/.test(lower)) {
      const swL = 1.1 * baseDim;

      return {
        id: 'below_nominal.weapons.energy_blade',
        name: 'Sable de Plasma Táctico',
        category: 'weapons',
        description: 'Hoja cuerpo a cuerpo de alta frecuencia con guarda transversal y empuñadura aislante.',
        units: 'meters',
        dimensions: { width: 0.35 * baseDim, depth: 0.1 * baseDim, height: swL },
        palette: 'standard',
        components: [
          // Blade
          {
            name: 'blade_edge',
            shape: 'box',
            size: [0.06, swL * 0.72, 0.02],
            position: [0, swL * 0.62, 0],
            color: mainColor === '#4a5568' ? '#319795' : mainColor,
            roughness: 0.2,
            metalness: 0.9
          },
          // Crossguard
          {
            name: 'crossguard',
            shape: 'box',
            size: [0.28, 0.04, 0.06],
            position: [0, swL * 0.25, 0],
            color: '#1a202c',
            metalness: 0.8
          },
          // Hilt
          {
            name: 'hilt_grip',
            shape: 'cylinder',
            size: [0.025, 0.025, swL * 0.2, 8],
            position: [0, swL * 0.14, 0],
            color: '#2d3748',
            roughness: 0.8
          },
          // Pommel
          {
            name: 'pommel_sphere',
            shape: 'sphere',
            size: [0.035, 6, 4],
            position: [0, swL * 0.03, 0],
            color: '#ecc94b',
            metalness: 0.8
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 16. SPHERE / ESFERA / ORBE
    // -------------------------------------------------------------
    if (/esfera|sphere|pelota|bola|orb|globo/.test(lower)) {
      const r = Math.max(0.1, baseDim * 0.5);
      return {
        id: 'below_nominal.custom.procedural_sphere',
        name: 'Esfera Procedural Calibrada',
        category: 'fixtures',
        description: `Esfera procedural de radio ${r}m con color ${mainColor}.`,
        units: 'meters',
        dimensions: { width: r * 2, depth: r * 2, height: r * 2 },
        palette: 'standard',
        components: [
          {
            name: 'main_sphere',
            shape: 'sphere',
            size: [r, 12, 8],
            position: [0, r, 0],
            color: mainColor,
            roughness: 0.6,
            metalness: 0.2
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 17. CUBE / CUBO / BLOQUE / DADO
    // -------------------------------------------------------------
    if (/cubo|cube|bloque|dado/.test(lower) && !/tarjeta|consola/.test(lower)) {
      const s = Math.max(0.1, baseDim);
      return {
        id: 'below_nominal.custom.procedural_cube',
        name: 'Cubo Procedural Preciso',
        category: 'furniture',
        description: `Cubo procedural de lado ${s}m con color ${mainColor}.`,
        units: 'meters',
        dimensions: { width: s, depth: s, height: s },
        palette: 'standard',
        components: [
          {
            name: 'main_box',
            shape: 'box',
            size: [s, s, s],
            position: [0, s * 0.5, 0],
            color: mainColor,
            roughness: 0.7,
            metalness: 0.3
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 18. CYLINDER / CILINDRO / COLUMNA
    // -------------------------------------------------------------
    if (/cilindro|cylinder|columna|pilar/.test(lower)) {
      const r = Math.max(0.05, baseDim * 0.3);
      const h = Math.max(0.1, baseDim * 1.2);
      return {
        id: 'below_nominal.custom.procedural_cylinder',
        name: 'Columna Industrial Cilíndrica',
        category: 'infrastructure',
        description: `Columna procedural de altura ${h}m y radio ${r}m.`,
        units: 'meters',
        dimensions: { width: r * 2, depth: r * 2, height: h },
        palette: 'standard',
        components: [
          {
            name: 'base_pedestal',
            shape: 'box',
            size: [r * 2.4, 0.06, r * 2.4],
            position: [0, 0.03, 0],
            color: '#1a202c',
            roughness: 0.8
          },
          {
            name: 'column_body',
            shape: 'cylinder',
            size: [r, r, h - 0.06, 8],
            position: [0, (h + 0.06) * 0.5, 0],
            color: mainColor,
            roughness: 0.65,
            metalness: 0.4
          },
          {
            name: 'top_cap',
            shape: 'cylinder',
            size: [r * 1.1, r * 1.1, 0.04, 8],
            position: [0, h - 0.02, 0],
            color: '#718096',
            metalness: 0.5
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 19. ACCESS CARD / TARJETA DE SEGURIDAD (Criterion 3)
    // -------------------------------------------------------------
    if (/tarjeta|card|keycard|credencial|badge|pase|acceso/.test(lower)) {
      const w = 0.54 * baseDim;
      const h = 0.86 * baseDim;
      const thick = 0.025;
      return {
        id: 'below_nominal.security.access_card',
        name: 'Tarjeta de Acceso Nivel 1',
        category: 'security',
        description: 'Tarjeta de acceso magnética y biométrica con chip dorado y banda magnética.',
        units: 'meters',
        dimensions: { width: w, depth: thick, height: h },
        palette: 'standard',
        components: [
          {
            name: 'card_body',
            shape: 'box',
            size: [w, h, thick],
            position: [0, h * 0.5, 0],
            color: mainColor === '#4a5568' ? '#ffffff' : mainColor,
            texturePreset: 'painted_metal_white',
            roughness: 0.8,
            metalness: 0.1
          },
          {
            name: 'security_header',
            shape: 'box',
            size: [w * 0.96, h * 0.22, thick * 1.05],
            position: [0, h * 0.82, 0],
            color: '#e53e3e',
            roughness: 0.5
          },
          {
            name: 'smart_chip',
            shape: 'box',
            size: [w * 0.28, h * 0.16, thick * 1.15],
            position: [-w * 0.22, h * 0.52, thick * 0.2],
            color: '#ecc94b',
            texturePreset: 'metal_light_brushed',
            roughness: 0.3,
            metalness: 0.8
          },
          {
            name: 'photo_placeholder',
            shape: 'box',
            size: [w * 0.32, h * 0.25, thick * 1.1],
            position: [w * 0.20, h * 0.48, thick * 0.15],
            color: '#2d3748',
            roughness: 0.9
          },
          {
            name: 'magnetic_stripe',
            shape: 'box',
            size: [w * 0.98, h * 0.18, thick * 1.05],
            position: [0, h * 0.70, -thick * 0.1],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.9,
            metalness: 0.3
          },
          {
            name: 'lanyard_slot',
            shape: 'box',
            size: [w * 0.24, 0.03, thick * 1.3],
            position: [0, h * 0.93, 0],
            color: '#1a202c'
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 20. CONSOLE / TERMINAL / WORKSTATION
    // -------------------------------------------------------------
    if (/consola|console|workstation|radar|terminal|panel de control/.test(lower)) {
      const cw = 1.2 * baseDim;
      const ch = 1.0 * baseDim;
      const cd = 0.8 * baseDim;
      return {
        id: 'below_nominal.command.flight_console',
        name: 'Consola de Telemetría CRT',
        category: 'command',
        description: 'Puesto de operaciones con teclado angular y pantallas CRT.',
        units: 'meters',
        dimensions: { width: cw, depth: cd, height: ch },
        palette: 'command_bridge',
        components: [
          {
            name: 'desk_base',
            shape: 'box',
            size: [cw, ch * 0.65, cd * 0.85],
            position: [0, ch * 0.325, 0],
            color: mainColor,
            texturePreset: 'worn_metal',
            roughness: 0.75,
            metalness: 0.3
          },
          {
            name: 'slanted_tray',
            shape: 'box',
            size: [cw * 0.92, 0.06, cd * 0.35],
            position: [0, ch * 0.68, cd * 0.25],
            rotation: [-15, 0, 0],
            color: '#1a202c',
            texturePreset: 'rubber_black',
            roughness: 0.85
          },
          {
            name: 'crt_housing',
            shape: 'box',
            size: [cw * 0.85, ch * 0.35, cd * 0.45],
            position: [0, ch * 0.85, -cd * 0.15],
            color: '#2d3748',
            texturePreset: 'beige_plastic_worn',
            roughness: 0.7
          },
          {
            name: 'crt_screen',
            shape: 'box',
            size: [cw * 0.70, ch * 0.26, 0.02],
            position: [0, ch * 0.85, cd * 0.08],
            color: '#319795',
            texturePreset: 'crt_screen_green',
            roughness: 0.2,
            metalness: 0.1
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 21. TABLE / MESA / ESCRITORIO
    // -------------------------------------------------------------
    if (/mesa|table|desk|mesada/.test(lower)) {
      const tw = 1.4 * baseDim;
      const td = 0.8 * baseDim;
      const th = 0.75 * baseDim;
      const topThick = 0.06;
      const legR = 0.035;
      const legH = th - topThick;
      return {
        id: 'below_nominal.furniture.table',
        name: 'Mesa de Trabajo Modular',
        category: 'furniture',
        description: 'Mesa de operaciones con tablero reforzado y cuatro patas tubulares.',
        units: 'meters',
        dimensions: { width: tw, depth: td, height: th },
        palette: 'standard',
        components: [
          {
            name: 'tabletop',
            shape: 'box',
            size: [tw, topThick, td],
            position: [0, th - topThick * 0.5, 0],
            color: mainColor,
            roughness: 0.65,
            metalness: 0.2
          },
          {
            name: 'leg_fl',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [-tw * 0.42, legH * 0.5, -td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          },
          {
            name: 'leg_fr',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [tw * 0.42, legH * 0.5, -td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          },
          {
            name: 'leg_bl',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [-tw * 0.42, legH * 0.5, td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          },
          {
            name: 'leg_br',
            shape: 'cylinder',
            size: [legR, legR, legH, 6],
            position: [tw * 0.42, legH * 0.5, td * 0.40],
            color: '#2d3748',
            metalness: 0.6
          }
        ]
      };
    }

    // -------------------------------------------------------------
    // 22. DYNAMIC PROCEDURAL SYNTHESIZER (For Any Unlisted Prompt)
    // Generates a genuinely custom, multi-tier composite asset based on
    // word semantics, attributes, and shapes extracted from the prompt.
    // -------------------------------------------------------------
    const components: ComponentDef[] = [];
    const words = lower.split(/\s+/);
    const hash = words.reduce((acc, w) => acc + w.charCodeAt(0), 0);

    // Dynamic dimensions derived from prompt words
    const pW = (0.8 + ((hash * 7) % 50) / 100) * baseDim;
    const pH = (0.7 + ((hash * 13) % 60) / 100) * baseDim;
    const pD = (0.8 + ((hash * 19) % 50) / 100) * baseDim;

    // 1. Foundation Base Plinth
    components.push({
      name: 'pedestal_plinth',
      shape: 'box',
      size: [pW * 1.1, 0.08, pD * 1.1],
      position: [0, 0.04, 0],
      color: '#1a202c',
      roughness: 0.8,
      metalness: 0.5
    });

    // 2. Primary Body Structure
    const hasCylinderShape = /cilindr|tub|redond|circular/.test(lower);
    const hasWedgeShape = /cuñ|rampa|triangul|inclinad/.test(lower);

    if (hasCylinderShape) {
      components.push({
        name: 'primary_core',
        shape: 'cylinder',
        size: [pW * 0.45, pW * 0.45, pH * 0.75, 10],
        position: [0, 0.08 + pH * 0.375, 0],
        color: mainColor,
        roughness: 0.6,
        metalness: 0.3
      });
    } else if (hasWedgeShape) {
      components.push({
        name: 'primary_core',
        shape: 'wedge',
        size: [pW, pH * 0.75, pD],
        position: [0, 0.08 + pH * 0.375, 0],
        color: mainColor,
        roughness: 0.6,
        metalness: 0.3
      });
    } else {
      components.push({
        name: 'primary_core',
        shape: 'box',
        size: [pW, pH * 0.75, pD],
        position: [0, 0.08 + pH * 0.375, 0],
        color: mainColor,
        roughness: 0.6,
        metalness: 0.3
      });
    }

    // 3. Technical Upper Trim / Crown
    components.push({
      name: 'upper_trim',
      shape: 'box',
      size: [pW * 0.85, 0.06, pD * 0.85],
      position: [0, 0.08 + pH * 0.75 + 0.03, 0],
      color: '#2d3748',
      metalness: 0.7
    });

    // 4. Feature Enhancements based on words in prompt
    if (/rueda|ruedas|wheel/.test(lower)) {
      // User asked for wheels!
      const wr = 0.22 * baseDim;
      components.push(
        { name: 'dyn_wheel_fl', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [-pW * 0.55, wr, pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' },
        { name: 'dyn_wheel_fr', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [pW * 0.55, wr, pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' },
        { name: 'dyn_wheel_rl', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [-pW * 0.55, wr, -pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' },
        { name: 'dyn_wheel_rr', shape: 'cylinder', size: [wr, wr, 0.15, 8], position: [pW * 0.55, wr, -pD * 0.35], rotation: [0, 0, 90], color: '#1a202c' }
      );
    }

    if (/ala|alas|aleron|wing/.test(lower)) {
      components.push(
        { name: 'dyn_wing_l', shape: 'wedge', size: [pW * 0.8, 0.06, pD * 0.6], position: [-pW * 0.8, pH * 0.5, 0], color: mainColor },
        { name: 'dyn_wing_r', shape: 'wedge', size: [pW * 0.8, 0.06, pD * 0.6], position: [pW * 0.8, pH * 0.5, 0], color: mainColor }
      );
    }

    if (/pantalla|display|monitor|screen/.test(lower)) {
      components.push({
        name: 'dyn_display',
        shape: 'box',
        size: [pW * 0.65, pH * 0.35, 0.02],
        position: [0, pH * 0.5, pD * 0.51],
        color: '#319795',
        roughness: 0.2
      });
    }

    if (/luz|led|faro|brillo|emisor/.test(lower)) {
      components.push(
        { name: 'dyn_light_1', shape: 'box', size: [0.12, 0.08, 0.02], position: [-pW * 0.3, pH * 0.7, pD * 0.51], color: '#ecc94b' },
        { name: 'dyn_light_2', shape: 'box', size: [0.12, 0.08, 0.02], position: [pW * 0.3, pH * 0.7, pD * 0.51], color: '#ecc94b' }
      );
    }

    if (/antena|sensor|mástil/.test(lower)) {
      components.push({
        name: 'dyn_antenna',
        shape: 'cylinder',
        size: [0.02, 0.02, pH * 0.4, 4],
        position: [pW * 0.3, 0.08 + pH * 0.75 + pH * 0.2, 0],
        color: '#cbd5e0',
        metalness: 0.8
      });
    }

    // Default decorative technical detail if no extra features triggered
    if (components.length <= 3) {
      components.push({
        name: 'front_instrument_panel',
        shape: 'box',
        size: [pW * 0.7, pH * 0.25, 0.025],
        position: [0, pH * 0.45, pD * 0.51],
        color: '#2d3748',
        roughness: 0.8
      });
      components.push({
        name: 'status_indicator',
        shape: 'box',
        size: [pW * 0.2, 0.04, 0.03],
        position: [0, pH * 0.45, pD * 0.52],
        color: '#319795',
        roughness: 0.2
      });
    }

    const cleanTitle = prompt
      .replace(/^(un|una|el|la|los|las|de|con|para)\s+/gi, '')
      .trim();
    const titleCapitalized = cleanTitle.charAt(0).toUpperCase() + cleanTitle.slice(1);

    return finalizeWithKnowledge({
      id: `below_nominal.custom.${cleanTitle.toLowerCase().replace(/[^a-z0-9]/g, '_').substring(0, 32)}`,
      name: options?.wikidata?.label ? `${options.wikidata.label} (${titleCapitalized})` : `${titleCapitalized} Procedural`,
      category: 'furniture',
      description: options?.wikidata?.description || `Modelo procedural sintetizado para '${prompt}'.`,
      units: 'meters',
      dimensions: { width: pW * 1.15, depth: pD * 1.15, height: pH * 1.1 },
      palette: 'industrial_hazard',
      components
    }, { matchedArchetype: 'dynamic_composite' });
  }
}
