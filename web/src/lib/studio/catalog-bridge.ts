import type { ModelSpec, ComponentDef } from './types.ts';
import { AIGenerator } from './ai-generator.ts';
import catalog from '../../data/catalog.json' with { type: 'json' };

export interface CatalogTemplateInfo {
  family: string;
  name: string;
  category: string;
  description: string;
  defaultTriBudget?: string;
  tags?: string[];
  parameterCount: number;
}

export class CatalogBridge {
  /**
   * Retrieves all available catalog templates.
   */
  public static getCatalogTemplates(): CatalogTemplateInfo[] {
    return (catalog as any[]).map((item: any) => ({
      family: item.family,
      name: item.name,
      category: item.category || 'props',
      description: item.description,
      defaultTriBudget: item.export_capabilities?.target_tri_budget || '300-500',
      tags: item.tags || [],
      parameterCount: item.parameters?.length || 0
    }));
  }

  /**
   * Builds an authentic, fully editable procedural ModelSpec for any catalog family.
   * If custom parameter values are supplied (e.g. from the configurator sliders),
   * they are seamlessly injected and applied to the component hierarchy.
   */
  public static buildSpecFromCatalog(
    family: string,
    userParams?: Record<string, any>
  ): ModelSpec {
    const entry = (catalog as any[]).find((c: any) => c.family === family) || {
      family,
      name: family.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
      category: 'props',
      description: 'Modelo procedural desglosado para edición modular.'
    };

    // 1. Synthesize baseline procedural piece composition using title & family keywords
    const prompt = `${entry.name} ${entry.family.replace(/_/g, ' ')}`;
    const baseSpec = AIGenerator.synthesizeProceduralSpec(prompt);

    // 2. Clone and brand as a fresh remixable draft for the user
    const remixSpec: ModelSpec = JSON.parse(JSON.stringify(baseSpec));
    remixSpec.id = `remix.${family}.${Date.now().toString(36)}`;
    remixSpec.name = `${entry.name} (Remix)`;
    remixSpec.category = entry.category || baseSpec.category || 'props';
    remixSpec.description = `Versión editable y modular de ${entry.name}. Desarmada en componentes individuales para personalización en Studio 3D.`;

    // 3. Apply custom user parameters if provided (e.g. width, height, depth, thickness)
    if (userParams && Object.keys(userParams).length > 0) {
      this.applyParametersToSpec(remixSpec, userParams, entry);
    }

    return remixSpec;
  }

  /**
   * Proportionally scales dimensions and piece offsets based on user slider adjustments.
   */
  private static applyParametersToSpec(
    spec: ModelSpec,
    params: Record<string, any>,
    catalogEntry?: any
  ) {
    const origDims = spec.dimensions || { width: 1, height: 1, depth: 1 };
    let targetW = origDims.width;
    let targetH = origDims.height;
    let targetD = origDims.depth;

    if (params.width !== undefined && typeof params.width === 'number' && params.width > 0) {
      targetW = params.width;
    }
    if (params.height !== undefined && typeof params.height === 'number' && params.height > 0) {
      targetH = params.height;
    }
    if (params.depth !== undefined && typeof params.depth === 'number' && params.depth > 0) {
      targetD = params.depth;
    } else if (params.thickness !== undefined && typeof params.thickness === 'number' && params.thickness > 0) {
      targetD = params.thickness;
    }

    const scaleX = origDims.width > 0.001 ? targetW / origDims.width : 1;
    const scaleY = origDims.height > 0.001 ? targetH / origDims.height : 1;
    const scaleZ = origDims.depth > 0.001 ? targetD / origDims.depth : 1;

    // Apply scale to components if dimensions changed noticeably
    if (Math.abs(scaleX - 1) > 0.01 || Math.abs(scaleY - 1) > 0.01 || Math.abs(scaleZ - 1) > 0.01) {
      spec.components.forEach((comp) => {
        if (comp.size && comp.size.length >= 2) {
          if (comp.shape === 'box' || comp.shape === 'wedge') {
            comp.size[0] = parseFloat((comp.size[0] * scaleX).toFixed(3));
            comp.size[1] = parseFloat((comp.size[1] * scaleY).toFixed(3));
            if (comp.size[2] !== undefined) comp.size[2] = parseFloat((comp.size[2] * scaleZ).toFixed(3));
          } else if (comp.shape === 'cylinder' || comp.shape === 'cone') {
            const radScale = (scaleX + scaleZ) * 0.5;
            comp.size[0] = parseFloat((comp.size[0] * radScale).toFixed(3));
            if (comp.size[1] !== undefined) comp.size[1] = parseFloat((comp.size[1] * radScale).toFixed(3));
            if (comp.size[2] !== undefined) comp.size[2] = parseFloat((comp.size[2] * scaleY).toFixed(3));
          } else if (comp.shape === 'sphere') {
            const avgScale = (scaleX + scaleY + scaleZ) / 3;
            comp.size[0] = parseFloat((comp.size[0] * avgScale).toFixed(3));
          }
        }
        if (comp.position) {
          comp.position[0] = parseFloat((comp.position[0] * scaleX).toFixed(3));
          comp.position[1] = parseFloat((comp.position[1] * scaleY).toFixed(3));
          comp.position[2] = parseFloat((comp.position[2] * scaleZ).toFixed(3));
        }
      });

      spec.dimensions = {
        width: parseFloat(targetW.toFixed(3)),
        height: parseFloat(targetH.toFixed(3)),
        depth: parseFloat(targetD.toFixed(3))
      };
    }

    // Apply palette if specified in parameters
    if (params.palette && typeof params.palette === 'string') {
      spec.palette = params.palette;
    }
  }
}
