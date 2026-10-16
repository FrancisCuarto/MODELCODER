import type { ModelSpec } from './types.ts';
import { getSupabase } from '../supabase.ts';

const LOCAL_STORAGE_KEY = 'modelcoder_procedural_memory_v1';

export interface LearnedBlueprintRecord {
  prompt: string;
  normalizedKeywords: string[];
  spec: ModelSpec;
  timestamp: number;
  source: 'local' | 'cloud';
}

export class ProceduralMemory {
  /**
   * Normalizes a prompt into searchable keywords (e.g. "auto de carreras rojo" -> ["auto", "carreras", "rojo"]).
   */
  public static extractKeywords(prompt: string): string[] {
    return prompt
      .toLowerCase()
      .replace(/[^\w\sáéíóúñ]/g, ' ')
      .split(/\s+/)
      .filter((w) => w.length > 2 && !['con', 'para', 'los', 'las', 'una', 'uno', 'del', 'por', 'que'].includes(w));
  }

  /**
   * Searches local browser storage for a previously learned blueprint.
   */
  public static searchLocalMemory(prompt: string): ModelSpec | null {
    if (typeof window === 'undefined' || !window.localStorage) return null;

    try {
      const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (!raw) return null;

      const records: LearnedBlueprintRecord[] = JSON.parse(raw);
      const queryKeywords = this.extractKeywords(prompt);
      if (queryKeywords.length === 0) return null;

      // 1. Exact prompt match
      const exact = records.find((r) => r.prompt.toLowerCase() === prompt.trim().toLowerCase());
      if (exact) return exact.spec;

      // 2. Keyword match (find blueprint sharing the highest number of keywords)
      let bestMatch: LearnedBlueprintRecord | null = null;
      let highestOverlap = 0;

      for (const rec of records) {
        const overlap = queryKeywords.filter((k) => rec.normalizedKeywords.includes(k)).length;
        if (overlap > highestOverlap && overlap >= Math.min(2, queryKeywords.length)) {
          highestOverlap = overlap;
          bestMatch = rec;
        }
      }

      return bestMatch ? bestMatch.spec : null;
    } catch (err) {
      console.warn('[ProceduralMemory] Error leyendo memoria local:', err);
      return null;
    }
  }

  /**
   * Saves a newly created or refined blueprint into local persistent browser memory.
   */
  public static saveToLocalMemory(prompt: string, spec: ModelSpec): void {
    if (typeof window === 'undefined' || !window.localStorage) return;

    try {
      const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
      const records: LearnedBlueprintRecord[] = raw ? JSON.parse(raw) : [];

      const keywords = this.extractKeywords(prompt);

      // Remove previous entry with same prompt if exists
      const filtered = records.filter((r) => r.prompt.toLowerCase() !== prompt.trim().toLowerCase());

      filtered.unshift({
        prompt: prompt.trim(),
        normalizedKeywords: keywords,
        spec,
        timestamp: Date.now(),
        source: 'local'
      });

      // Keep up to 100 learned models locally
      const trimmed = filtered.slice(0, 100);
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(trimmed));
    } catch (err) {
      console.warn('[ProceduralMemory] Error guardando en memoria local:', err);
    }
  }

  /**
   * Searches the shared Supabase cloud community table if available.
   */
  public static async searchCloudMemory(prompt: string): Promise<ModelSpec | null> {
    try {
      const supabase = getSupabase();
      if (!supabase) return null;

      const keywords = this.extractKeywords(prompt);
      if (keywords.length === 0) return null;

      const mainKeyword = keywords[0];

      // Query community_blueprints by prompt ILIKE
      const { data, error } = await supabase
        .from('community_blueprints')
        .select('spec, prompt')
        .or(`prompt.ilike.%${mainKeyword}%,name.ilike.%${mainKeyword}%`)
        .limit(1)
        .maybeSingle();

      if (error || !data) {
        return null;
      }

      return data.spec as ModelSpec;
    } catch {
      // Graceful fallback if table does not exist or network unavailable
      return null;
    }
  }

  /**
   * Publishes / auto-persists a learned blueprint to Supabase so other users can find it.
   */
  public static async saveToCloudMemory(prompt: string, spec: ModelSpec): Promise<boolean> {
    try {
      const supabase = getSupabase();
      if (!supabase) return false;

      const keywords = this.extractKeywords(prompt);

      const { error } = await supabase.from('community_blueprints').upsert(
        {
          id: spec.id || `custom_${Date.now()}`,
          name: spec.name,
          prompt: prompt.trim(),
          keywords,
          spec,
          updated_at: new Date().toISOString()
        },
        { onConflict: 'prompt' }
      );

      return !error;
    } catch {
      return false;
    }
  }

  /**
   * Unified lookup: Checks Local Memory first, then Cloud Memory.
   */
  public static async findLearnedModel(
    prompt: string
  ): Promise<{ spec: ModelSpec; source: 'local_memory' | 'cloud_memory' } | null> {
    // 1. Check local storage
    const localSpec = this.searchLocalMemory(prompt);
    if (localSpec) {
      return { spec: localSpec, source: 'local_memory' };
    }

    // 2. Check Supabase shared community
    const cloudSpec = await this.searchCloudMemory(prompt);
    if (cloudSpec) {
      // Also cache it locally for instant offline reuse
      this.saveToLocalMemory(prompt, cloudSpec);
      return { spec: cloudSpec, source: 'cloud_memory' };
    }

    return null;
  }

  /**
   * Unified store: Saves to local memory and attempts cloud sync.
   */
  public static async recordLearnedModel(prompt: string, spec: ModelSpec): Promise<void> {
    this.saveToLocalMemory(prompt, spec);
    // Fire-and-forget cloud upload so user never waits
    this.saveToCloudMemory(prompt, spec).catch(() => {});
  }

  /**
   * Retrieves all blueprints currently memorized in this browser.
   */
  public static getAllLocalRecords(): LearnedBlueprintRecord[] {
    if (typeof window === 'undefined' || !window.localStorage) return [];
    try {
      const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  /**
   * Clears local procedural memory.
   */
  public static clearLocalMemory(): void {
    if (typeof window === 'undefined' || !window.localStorage) return;
    localStorage.removeItem(LOCAL_STORAGE_KEY);
  }
}
