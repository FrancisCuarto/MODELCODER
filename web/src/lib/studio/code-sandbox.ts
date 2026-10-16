import type { ModelSpec, ComponentDef, ShapePrimitive } from './types';

export class ProceduralBuilderContext {
  public spec: ModelSpec;

  constructor(initialName = 'Custom Model') {
    this.spec = {
      id: 'below_nominal.custom.user_model',
      name: initialName,
      category: 'furniture',
      description: 'Generador procedural creado en ModelCoder Studio',
      units: 'meters',
      dimensions: { width: 1.0, depth: 1.0, height: 1.0 },
      palette: 'industrial_hazard',
      components: []
    };
  }

  public setName(name: string): this {
    this.spec.name = name;
    return this;
  }

  public setCategory(cat: string): this {
    this.spec.category = cat;
    return this;
  }

  public setDescription(desc: string): this {
    this.spec.description = desc;
    return this;
  }

  public addComponent(comp: ComponentDef): this {
    this.spec.components.push(comp);
    return this;
  }

  public addBox(opts: {
    name?: string;
    size?: [number, number, number];
    position?: [number, number, number];
    rotation?: [number, number, number];
    color?: string;
    roughness?: number;
    metalness?: number;
    wireframe?: boolean;
    label?: string;
  }): this {
    return this.addComponent({
      name: opts.name || `box_${this.spec.components.length + 1}`,
      shape: 'box',
      size: opts.size || [1, 1, 1],
      position: opts.position || [0, 0, 0],
      rotation: opts.rotation || [0, 0, 0],
      color: opts.color || '#4a5568',
      roughness: opts.roughness,
      metalness: opts.metalness,
      wireframe: opts.wireframe,
      label: opts.label
    });
  }

  public addCylinder(opts: {
    name?: string;
    radius?: number;
    height?: number;
    segments?: number;
    size?: [number, number, number, number];
    position?: [number, number, number];
    rotation?: [number, number, number];
    color?: string;
    roughness?: number;
    metalness?: number;
  }): this {
    const s = opts.size || [opts.radius || 0.4, opts.radius || 0.4, opts.height || 1.0, opts.segments || 8];
    return this.addComponent({
      name: opts.name || `cylinder_${this.spec.components.length + 1}`,
      shape: 'cylinder',
      size: s,
      position: opts.position || [0, 0, 0],
      rotation: opts.rotation || [0, 0, 0],
      color: opts.color || '#2d3748',
      roughness: opts.roughness,
      metalness: opts.metalness
    });
  }

  public addSphere(opts: {
    name?: string;
    radius?: number;
    segments?: number;
    size?: [number, number, number];
    position?: [number, number, number];
    rotation?: [number, number, number];
    color?: string;
    roughness?: number;
    metalness?: number;
  }): this {
    const s = opts.size || [opts.radius || 0.5, opts.segments || 8, Math.max(4, Math.round((opts.segments || 8) * 0.75))];
    return this.addComponent({
      name: opts.name || `sphere_${this.spec.components.length + 1}`,
      shape: 'sphere',
      size: s,
      position: opts.position || [0, 0, 0],
      rotation: opts.rotation || [0, 0, 0],
      color: opts.color || '#e53e3e',
      roughness: opts.roughness,
      metalness: opts.metalness
    });
  }

  public addWedge(opts: {
    name?: string;
    size?: [number, number, number];
    position?: [number, number, number];
    rotation?: [number, number, number];
    color?: string;
  }): this {
    return this.addComponent({
      name: opts.name || `wedge_${this.spec.components.length + 1}`,
      shape: 'wedge',
      size: opts.size || [1, 1, 1],
      position: opts.position || [0, 0, 0],
      rotation: opts.rotation || [0, 0, 0],
      color: opts.color || '#4a5568'
    });
  }
}

export class CodeSandbox {
  /**
   * Safely parses code (JSON or JavaScript procedural builder) in an isolated sandbox.
   * Never evaluates with unrestricted access to window/document/secrets.
   */
  public static executeCode(codeStr: string): { spec: ModelSpec; error?: string; errorLine?: number } {
    const trimmed = codeStr.trim();
    if (!trimmed) {
      return {
        spec: this.createEmptySpec(),
        error: 'El editor de código está vacío. Escribe una especificación o usa el builder procedural.'
      };
    }

    // 1. Try parsing as JSON Specification
    if (trimmed.startsWith('{') && trimmed.endsWith('}')) {
      try {
        const parsed = JSON.parse(trimmed);
        if (!parsed.components || !Array.isArray(parsed.components)) {
          return {
            spec: this.createEmptySpec(),
            error: "La especificación JSON debe contener una lista válida de 'components': []"
          };
        }
        return { spec: parsed as ModelSpec };
      } catch (jsonErr: any) {
        // Find line number of JSON parse error if possible
        const lineMatch = jsonErr.message.match(/at position (\d+)/);
        let errorLine: number | undefined;
        if (lineMatch) {
          const pos = parseInt(lineMatch[1], 10);
          errorLine = trimmed.substring(0, pos).split('\n').length;
        }
        return {
          spec: this.createEmptySpec(),
          error: `Error de sintaxis JSON: ${jsonErr.message}`,
          errorLine
        };
      }
    }

    // 2. Execute as Sandboxed JavaScript Procedural DSL
    const builder = new ProceduralBuilderContext();

    let sandboxedRunner: Function;
    try {
      sandboxedRunner = new Function(
        'builder',
        'window',
        'document',
        'fetch',
        'localStorage',
        'sessionStorage',
        `
        "use strict";
        ${codeStr}
        `
      );
    } catch (syntaxErr: any) {
      return {
        spec: builder.spec,
        error: `Error de sintaxis en el código: ${syntaxErr.message}`
      };
    }

    try {
      sandboxedRunner(builder, null, null, null, null, null);

      if (builder.spec.components.length === 0) {
        return {
          spec: builder.spec,
          error: 'El código ejecutó sin errores pero no añadió ningún componente (usa builder.addBox, builder.addCylinder, etc.)'
        };
      }

      return { spec: builder.spec };
    } catch (err: any) {
      let errorLine: number | undefined;
      // Extract line number from stack trace
      if (err.stack) {
        const stackMatch = err.stack.match(/<anonymous>:(\d+):(\d+)/);
        if (stackMatch) {
          // Adjust for header lines in wrapper
          errorLine = Math.max(1, parseInt(stackMatch[1], 10) - 2);
        }
      }

      return {
        spec: builder.spec,
        error: `Error de ejecución en código: ${err.message}`,
        errorLine
      };
    }
  }

  public static createEmptySpec(): ModelSpec {
    return {
      id: 'below_nominal.custom.empty',
      name: 'Sin Componentes',
      category: 'furniture',
      description: 'Modelo vacío',
      units: 'meters',
      dimensions: { width: 0, depth: 0, height: 0 },
      palette: 'industrial_hazard',
      components: []
    };
  }
}
