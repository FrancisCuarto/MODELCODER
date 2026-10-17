import type { ModelSpec } from './studio/types.ts';
import { getSupabase, getCurrentUser } from './supabase.ts';

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

export function saveProjectDraft(draftData: {
  id?: string;
  name: string;
  category?: string;
  description?: string;
  spec: ModelSpec;
  thumbnail?: string;
  tri_count?: number;
}): UserProjectDraft {
  const drafts = getProjectDrafts();
  const now = new Date().toISOString();
  const id = draftData.id || `proj_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
  const existingIdx = drafts.findIndex((d) => d.id === id);

  const componentsCount = draftData.spec.components?.length || 0;
  const triCount = draftData.tri_count || 50;

  const newDraft: UserProjectDraft = {
    id,
    name: draftData.name || draftData.spec.name || 'Proyecto Sin Nombre',
    category: draftData.category || draftData.spec.category || 'furniture',
    description: draftData.description || draftData.spec.description || 'Modelo procedural en desarrollo.',
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
      // Notify other components or tabs
      window.dispatchEvent(new CustomEvent('modelcoder:drafts-changed', { detail: { drafts } }));
    } catch (e) {
      console.warn('[ModelCoder Inventory] Almacenamiento lleno o no disponible:', e);
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
      window.dispatchEvent(new CustomEvent('modelcoder:drafts-changed', { detail: { drafts: filtered } }));
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
      window.dispatchEvent(
        new CustomEvent('modelcoder:favorites-changed', {
          detail: { id: item.id, isFavorite: isNowFavorite, favorites },
        })
      );
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
      window.dispatchEvent(new CustomEvent('modelcoder:collections-changed', { detail: { collections } }));
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
      window.dispatchEvent(new CustomEvent('modelcoder:collections-changed', { detail: { collections: filtered } }));
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
      window.dispatchEvent(new CustomEvent('modelcoder:collections-changed', { detail: { collections } }));
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
