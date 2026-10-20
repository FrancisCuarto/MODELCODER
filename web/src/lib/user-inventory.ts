import type { ModelSpec } from './studio/types.ts';
import { getSupabase, getCurrentUser } from './supabase.ts';
import { isTauriDesktop, getTauriInvoke } from './tauri-bridge.ts';

export interface UserProjectDraft {
  id: string;
  name: string;
  category: string;
  description: string;
  spec: ModelSpec;
  thumbnail?: string; // Data URL PNG
  tri_count: number;
  components_count: number;
  created_at: string;
  updated_at: string;
}

export interface FavoriteItem {
  id: string; // family slug or community model id
  type: 'catalog' | 'community' | 'project';
  name: string;
  category: string;
  model_url?: string;
  added_at: string;
}

export interface UserCollection {
  id: string;
  name: string;
  description: string;
  color: string;
  model_ids: string[];
  created_at: string;
  updated_at: string;
}

const STORAGE_KEYS = {
  DRAFTS: 'modelcoder_user_drafts_v1',
  AUTOSAVE: 'modelcoder_autosave_draft_v1',
  FAVORITES: 'modelcoder_user_favorites_v1',
  COLLECTIONS: 'modelcoder_user_collections_v1',
};

// ============================================================================
// 1. GESTIÓN DE BORRADORES Y PROYECTOS EN CURSO (STUDIO DRAFTS)
// ============================================================================

export function getProjectDrafts(): UserProjectDraft[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.DRAFTS);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (e) {
    console.warn('[ModelCoder Inventory] Error al leer borradores locales:', e);
    return [];
  }
}

export function getProjectDraft(id: string): UserProjectDraft | null {
  const drafts = getProjectDrafts();
  return drafts.find((d) => d.id === id) || null;
}

function notifyChange(type: 'drafts' | 'favorites' | 'collections', data: any) {
  if (typeof window !== 'undefined') {
    try {
      window.dispatchEvent(new CustomEvent(`modelcoder:${type}-changed`, { detail: data }));
      window.dispatchEvent(new CustomEvent('modelcoder:inventory_updated', { detail: { type, data } }));
    } catch {}
  }
}

export function saveProjectDraft(
  arg1: {
    id?: string;
    name?: string;
    category?: string;
    description?: string;
    spec: ModelSpec;
    thumbnail?: string;
    tri_count?: number;
  } | ModelSpec,
  nameArg?: string,
  categoryArg?: string,
  descriptionArg?: string,
  thumbnailArg?: string,
  triCountArg?: number
): UserProjectDraft {
  let draftData: {
    id?: string;
    name: string;
    category?: string;
    description?: string;
    spec: ModelSpec;
    thumbnail?: string;
    tri_count?: number;
  };

  if (arg1 && 'components' in arg1) {
    if (typeof nameArg === 'string' && nameArg.startsWith('data:image/')) {
      // Shorthand positional call: saveProjectDraft(spec, thumbnailDataUrl, existingId)
      draftData = {
        id: categoryArg,
        spec: arg1,
        name: arg1.name || 'Proyecto Sin Nombre',
        category: arg1.category || 'furniture',
        description: arg1.description || 'Modelo procedural en desarrollo.',
        thumbnail: nameArg,
      };
    } else {
      // Positional parameters call from studio.astro: saveProjectDraft(spec, name, category, description, thumbnail, tri_count)
      draftData = {
        spec: arg1,
        name: nameArg || arg1.name || 'Proyecto Sin Nombre',
        category: categoryArg || arg1.category || 'furniture',
        description: descriptionArg || arg1.description || 'Modelo procedural en desarrollo.',
        thumbnail: thumbnailArg,
        tri_count: triCountArg,
      };
    }
  } else {
    const obj = arg1 as any;
    draftData = {
      id: obj?.id,
      name: obj?.name || obj?.spec?.name || 'Proyecto Sin Nombre',
      category: obj?.category || obj?.spec?.category || 'furniture',
      description: obj?.description || obj?.spec?.description || 'Modelo procedural en desarrollo.',
      spec: obj?.spec,
      thumbnail: obj?.thumbnail,
      tri_count: obj?.tri_count,
    };
  }

  if (!draftData.spec || !Array.isArray(draftData.spec.components)) {
    throw new Error('La especificación del modelo es inválida o no contiene componentes.');
  }

  const drafts = getProjectDrafts();
  const now = new Date().toISOString();
  const id = draftData.id || `proj_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
  const existingIdx = drafts.findIndex((d) => d.id === id);

  const componentsCount = draftData.spec.components.length;
  const triCount = draftData.tri_count || 50;

  const newDraft: UserProjectDraft = {
    id,
    name: draftData.name,
    category: draftData.category || 'furniture',
    description: draftData.description || 'Modelo procedural en desarrollo.',
    spec: JSON.parse(JSON.stringify(draftData.spec)),
    thumbnail: draftData.thumbnail || (existingIdx >= 0 ? drafts[existingIdx].thumbnail : undefined),
    tri_count: triCount,
    components_count: componentsCount,
    created_at: existingIdx >= 0 ? drafts[existingIdx].created_at : now,
    updated_at: now,
  };

  if (existingIdx >= 0) {
    drafts[existingIdx] = newDraft;
  } else {
    drafts.unshift(newDraft);
  }

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEYS.DRAFTS, JSON.stringify(drafts));
      notifyChange('drafts', { drafts });
    } catch (e) {
      console.warn('[ModelCoder Inventory] Quota exceeded, guardando versión ligera sin miniaturas base64:', e);
      try {
        const lightweightDrafts = drafts.map((d, idx) => (idx > 2 ? { ...d, thumbnail: undefined } : d));
        localStorage.setItem(STORAGE_KEYS.DRAFTS, JSON.stringify(lightweightDrafts));
        notifyChange('drafts', { drafts: lightweightDrafts });
      } catch (err2) {
        console.error('[ModelCoder Inventory] Error fatal guardando en localStorage:', err2);
      }
    }
  }

  // Backup to Supabase profile in background if logged in
  syncDraftsToCloud(drafts).catch(() => {});

  return newDraft;
}

export function deleteProjectDraft(id: string): boolean {
  const drafts = getProjectDrafts();
  const filtered = drafts.filter((d) => d.id !== id);
  if (filtered.length === drafts.length) return false;

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEYS.DRAFTS, JSON.stringify(filtered));
      notifyChange('drafts', { drafts: filtered });
    } catch {}
  }

  syncDraftsToCloud(filtered).catch(() => {});
  return true;
}

export function duplicateProjectDraft(id: string): UserProjectDraft | null {
  const draft = getProjectDraft(id);
  if (!draft) return null;

  return saveProjectDraft({
    name: `${draft.name} (Copia)`,
    category: draft.category,
    description: draft.description,
    spec: draft.spec,
    thumbnail: draft.thumbnail,
    tri_count: draft.tri_count,
  });
}

// --- AUTOGUARDADO TEMPORAL EN STUDIO ---
export function saveAutoDraft(spec: ModelSpec, thumbnail?: string): void {
  if (typeof window === 'undefined') return;
  try {
    const payload = {
      spec: JSON.parse(JSON.stringify(spec)),
      thumbnail,
      updated_at: new Date().toISOString(),
    };
    localStorage.setItem(STORAGE_KEYS.AUTOSAVE, JSON.stringify(payload));
  } catch (e) {
    console.warn('[ModelCoder Inventory] Error en autoguardado:', e);
  }
}

export function getAutoDraft(): { spec: ModelSpec; updated_at: string; thumbnail?: string } | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.AUTOSAVE);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearAutoDraft(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(STORAGE_KEYS.AUTOSAVE);
}

// ============================================================================
// 2. SISTEMA DE FAVORITOS (CATÁLOGO & COMUNIDAD)
// ============================================================================

export function getFavorites(): FavoriteItem[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.FAVORITES);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function getFavoriteIds(): string[] {
  return getFavorites().map((f) => f.id);
}

export function isFavorite(id: string): boolean {
  const favorites = getFavorites();
  return favorites.some((f) => f.id === id);
}

export function toggleFavorite(item: {
  id: string;
  type?: 'catalog' | 'community' | 'project';
  name: string;
  category?: string;
  model_url?: string;
}): boolean {
  const favorites = getFavorites();
  const existingIdx = favorites.findIndex((f) => f.id === item.id);
  let isNowFavorite = false;

  if (existingIdx >= 0) {
    favorites.splice(existingIdx, 1);
    isNowFavorite = false;
  } else {
    favorites.unshift({
      id: item.id,
      type: item.type || 'catalog',
      name: item.name,
      category: item.category || 'general',
      model_url: item.model_url,
      added_at: new Date().toISOString(),
    });
    isNowFavorite = true;
  }

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));
      notifyChange('favorites', { id: item.id, isFavorite: isNowFavorite, favorites });
    } catch {}
  }

  syncFavoritesToCloud(favorites).catch(() => {});
  return isNowFavorite;
}

// ============================================================================
// 3. COLECCIONES PERSONALIZADAS DE MODELOS (INVENTARIO)
// ============================================================================

export function getCollections(): UserCollection[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.COLLECTIONS);
    if (!raw) return getDefaultCollections();
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed) || parsed.length === 0) return getDefaultCollections();
    return parsed;
  } catch {
    return getDefaultCollections();
  }
}

function getDefaultCollections(): UserCollection[] {
  return [
    {
      id: 'col_default_1',
      name: 'Props de Estación',
      description: 'Mobiliario, consolas y paneles para interiores espaciales.',
      color: '#00f0ff',
      model_ids: ['crate', 'terminal', 'server_rack'],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: 'col_default_2',
      name: 'Médica y Biología',
      description: 'Equipo de enfermería, criogénicos y descontaminación.',
      color: '#ffcc00',
      model_ids: ['oxypod', 'crash_cart', 'biohazard_bin'],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];
}

export function saveCollection(collection: {
  id?: string;
  name: string;
  description?: string;
  color?: string;
  model_ids?: string[];
}): UserCollection {
  const collections = getCollections();
  const now = new Date().toISOString();
  const id = collection.id || `col_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;
  const existingIdx = collections.findIndex((c) => c.id === id);

  const updated: UserCollection = {
    id,
    name: collection.name.trim() || 'Colección Sin Nombre',
    description: collection.description || '',
    color: collection.color || '#00f0ff',
    model_ids: Array.isArray(collection.model_ids) ? Array.from(new Set(collection.model_ids)) : [],
    created_at: existingIdx >= 0 ? collections[existingIdx].created_at : now,
    updated_at: now,
  };

  if (existingIdx >= 0) {
    collections[existingIdx] = updated;
  } else {
    collections.push(updated);
  }

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEYS.COLLECTIONS, JSON.stringify(collections));
      notifyChange('collections', { collections });
    } catch {}
  }

  syncCollectionsToCloud(collections).catch(() => {});
  return updated;
}

export function deleteCollection(id: string): boolean {
  const collections = getCollections();
  const filtered = collections.filter((c) => c.id !== id);
  if (filtered.length === collections.length) return false;

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEYS.COLLECTIONS, JSON.stringify(filtered));
      notifyChange('collections', { collections: filtered });
    } catch {}
  }

  syncCollectionsToCloud(filtered).catch(() => {});
  return true;
}

export function toggleModelInCollection(collectionId: string, modelId: string): boolean {
  const collections = getCollections();
  const col = collections.find((c) => c.id === collectionId);
  if (!col) return false;

  const idx = col.model_ids.indexOf(modelId);
  let isIn = false;
  if (idx >= 0) {
    col.model_ids.splice(idx, 1);
    isIn = false;
  } else {
    col.model_ids.push(modelId);
    isIn = true;
  }
  col.updated_at = new Date().toISOString();

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEYS.COLLECTIONS, JSON.stringify(collections));
      notifyChange('collections', { collections });
    } catch {}
  }

  syncCollectionsToCloud(collections).catch(() => {});
  return isIn;
}

// ============================================================================
// 4. NUBE: SINCRONIZACIÓN AUTOMÁTICA CON SUPABASE (METADATA DE USUARIO)
// ============================================================================

async function syncDraftsToCloud(drafts: UserProjectDraft[]): Promise<void> {
  const supabase = getSupabase();
  const user = await getCurrentUser();
  if (!supabase || !user) return;

  try {
    // We store lightweight meta or backup in user_metadata
    await supabase.auth.updateUser({
      data: {
        modelcoder_drafts_count: drafts.length,
        modelcoder_last_draft: drafts[0]?.name || null,
        modelcoder_synced_at: new Date().toISOString(),
      },
    });
  } catch (err) {
    // Silent failover to local storage
  }
}

async function syncFavoritesToCloud(favorites: FavoriteItem[]): Promise<void> {
  const supabase = getSupabase();
  const user = await getCurrentUser();
  if (!supabase || !user) return;

  try {
    await supabase.auth.updateUser({
      data: {
        modelcoder_favorites: favorites.map((f) => f.id),
      },
    });
  } catch (err) {}
}

async function syncCollectionsToCloud(collections: UserCollection[]): Promise<void> {
  const supabase = getSupabase();
  const user = await getCurrentUser();
  if (!supabase || !user) return;

  try {
    await supabase.auth.updateUser({
      data: {
        modelcoder_collections_count: collections.length,
      },
    });
  } catch (err) {}
}

// ============================================================================
// 5. IMPORTACIÓN / EXPORTACIÓN DE ESPECIFICACIONES (.JSON)
// ============================================================================

export function exportProjectAsJSON(draftOrSpec: UserProjectDraft | ModelSpec): void {
  const spec = (draftOrSpec as any).spec || draftOrSpec;
  const name = (draftOrSpec as any).name || spec.name || 'model_spec';
  const jsonStr = JSON.stringify(spec, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${name.toLowerCase().replace(/[^a-z0-9_-]/g, '_')}_spec.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Permite al usuario elegir exactamente la carpeta y nombre de archivo para guardar el proyecto (.json).
 * En la app de escritorio usa el diálogo nativo del sistema (Tauri).
 * En navegadores modernos usa la API oficial showSaveFilePicker().
 * Con fallback transparente a descarga estándar si no están disponibles.
 */
export async function saveProjectToFilePicker(
  draftOrSpec: UserProjectDraft | ModelSpec
): Promise<{ success: boolean; filePath?: string; cancelled?: boolean }> {
  const spec = (draftOrSpec as any).spec || draftOrSpec;
  const name = (draftOrSpec as any).name || spec.name || 'model_spec';
  const cleanName = `${name.toLowerCase().replace(/[^a-z0-9_-]/g, '_')}_spec.json`;
  const jsonStr = JSON.stringify(spec, null, 2);

  // 1. Si estamos en la app de escritorio (Tauri)
  if (isTauriDesktop()) {
    const invoke = getTauriInvoke();
    if (invoke) {
      try {
        const filePath = (await invoke('save_project_dialog', {
          defaultName: cleanName,
          content: jsonStr,
        })) as string | null;

        if (filePath) {
          return { success: true, filePath };
        } else {
          return { success: false, cancelled: true };
        }
      } catch (err) {
        console.warn('[ModelCoder] Error en diálogo nativo de guardado de Tauri:', err);
      }
    }
  }

  // 2. Si el navegador soporta el selector oficial de archivos (Chrome, Edge, Opera)
  if (typeof window !== 'undefined' && 'showSaveFilePicker' in window) {
    try {
      const handle = await (window as any).showSaveFilePicker({
        suggestedName: cleanName,
        types: [
          {
            description: 'ModelCoder Spec JSON (*.json)',
            accept: {
              'application/json': ['.json'],
            },
          },
        ],
      });
      const writable = await handle.createWritable();
      await writable.write(jsonStr);
      await writable.close();
      return { success: true, filePath: handle.name };
    } catch (err: any) {
      if (err.name === 'AbortError') {
        return { success: false, cancelled: true };
      }
      console.warn('[ModelCoder] showSaveFilePicker falló o no fue permitido:', err);
    }
  }

  // 3. Fallback: descarga directa tradicional
  exportProjectAsJSON(draftOrSpec);
  return { success: true, filePath: cleanName };
}

export function importProjectFromJSON(jsonText: string): UserProjectDraft {
  const parsed = JSON.parse(jsonText);
  if (!parsed || typeof parsed !== 'object') {
    throw new Error('El archivo no contiene un JSON válido.');
  }

  // Handle either a full draft wrapper or a raw ModelSpec
  const spec: ModelSpec = parsed.spec && Array.isArray(parsed.spec.components) ? parsed.spec : parsed;

  if (!Array.isArray(spec.components)) {
    throw new Error('El archivo JSON no contiene un arreglo de componentes 3D válido.');
  }

  return saveProjectDraft({
    name: spec.name || parsed.name || 'Modelo Importado',
    category: spec.category || parsed.category || 'furniture',
    description: spec.description || parsed.description || 'Importado desde archivo externo.',
    spec,
  });
}
