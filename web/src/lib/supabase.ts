import { createClient, type SupabaseClient, type User, type Session } from '@supabase/supabase-js';

// Default public configuration with graceful fallback for production & client-side
const DEFAULT_SUPABASE_URL = (import.meta as any).env?.PUBLIC_SUPABASE_URL || 'https://jegdicdnhetdzmcuznqy.supabase.co';
const DEFAULT_SUPABASE_ANON_KEY = (import.meta as any).env?.PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImplZ2RpY2RuaGV0ZHptY3V6bnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIwOTE2NzcsImV4cCI6MjEwNzY2NzY3N30.TqgYHx1dNY4MQD0CbhJ33ApVa9B5i4WLlQ4PkjXKW5M';

let clientInstance: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient | null {
  if (typeof window === 'undefined') {
    if (DEFAULT_SUPABASE_URL && DEFAULT_SUPABASE_ANON_KEY) {
      return createClient(DEFAULT_SUPABASE_URL, DEFAULT_SUPABASE_ANON_KEY);
    }
    return null;
  }

  if (clientInstance) return clientInstance;

  const url = localStorage.getItem('modelcoder_supabase_url') || DEFAULT_SUPABASE_URL;
  const anonKey = localStorage.getItem('modelcoder_supabase_anon_key') || DEFAULT_SUPABASE_ANON_KEY;

  if (!url || !anonKey) {
    return null;
  }

  try {
    clientInstance = createClient(url, anonKey, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true,
      }
    });
    return clientInstance;
  } catch (err) {
    console.warn('[ModelCoder] Could not initialize Supabase client:', err);
    return null;
  }
}

export async function signInWithGitHub() {
  const supabase = getSupabase();
  if (!supabase) throw new Error('Supabase no está configurado aún.');
  const redirectTo = window.location.origin;
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo,
    }
  });
  if (error) throw error;
  return data;
}

export async function signInWithEmail(email: string, pass: string) {
  const supabase = getSupabase();
  if (!supabase) throw new Error('Supabase no está disponible.');
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password: pass,
  });
  if (error) throw error;
  return data;
}

export async function signUpWithEmail(email: string, pass: string) {
  const supabase = getSupabase();
  if (!supabase) throw new Error('Supabase no está disponible.');
  const { data, error } = await supabase.auth.signUp({
    email,
    password: pass,
    options: {
      emailRedirectTo: window.location.origin,
    }
  });
  if (error) throw error;
  return data;
}

export async function signOut() {
  const supabase = getSupabase();
  if (!supabase) return;
  await supabase.auth.signOut();
  window.location.reload();
}

export async function getCurrentUser(): Promise<User | null> {
  const supabase = getSupabase();
  if (!supabase) return null;
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}

export function onAuthStateChange(callback: (user: User | null, session: Session | null) => void) {
  const supabase = getSupabase();
  if (!supabase) return () => {};
  const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
    callback(session?.user || null, session);
  });
  return () => {
    subscription.unsubscribe();
  };
}

// ==============================================================================
// GESTIÓN DE COLABORADORES & PUBLICACIÓN DIRECTA
// ==============================================================================

export interface Collaborator {
  id: string;
  email: string;
  name?: string;
  role: 'owner' | 'admin' | 'collaborator';
  created_at?: string;
}

export interface CommunityModel {
  id: string;
  slug: string;
  name: string;
  category: string;
  description: string;
  spec: any;
  tri_count: number;
  author_name: string;
  author_email: string;
  is_public: boolean;
  glb_data?: string;
  created_at: string;
  updated_at?: string;
}

const LOCAL_COLLAB_KEY = 'modelcoder_collaborators_cache';
const LOCAL_MODELS_KEY = 'modelcoder_community_models_cache';

// Obtiene los colaboradores locales de respaldo
function getLocalCollaborators(): Collaborator[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(LOCAL_COLLAB_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return [
    {
      id: 'owner-default',
      email: 'franciscuarto@ivorbitgames.online',
      name: 'Franciscuarto (Dueño)',
      role: 'owner',
      created_at: new Date().toISOString()
    }
  ];
}

function saveLocalCollaborators(list: Collaborator[]) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(LOCAL_COLLAB_KEY, JSON.stringify(list));
}

function getLocalCommunityModels(): CommunityModel[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(LOCAL_MODELS_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return [];
}

function saveLocalCommunityModels(list: CommunityModel[]) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(LOCAL_MODELS_KEY, JSON.stringify(list));
}

/**
 * Comprueba el rol del usuario actual por correo electrónico.
 */
export async function checkUserRole(email?: string): Promise<{ isCollaborator: boolean; role: 'owner' | 'admin' | 'collaborator' | null }> {
  if (!email) return { isCollaborator: false, role: null };
  const normalizedEmail = email.trim().toLowerCase();

  // Comprobación de Dueño conocida (Franciscuarto / Admin)
  if (normalizedEmail.includes('franciscuarto') || normalizedEmail.includes('ivorbitgames') || normalizedEmail.startsWith('admin@')) {
    return { isCollaborator: true, role: 'owner' };
  }

  const supabase = getSupabase();
  if (supabase) {
    try {
      const { data, error } = await supabase
        .from('collaborators')
        .select('*')
        .eq('email', normalizedEmail)
        .maybeSingle();

      if (!error && data) {
        return { isCollaborator: true, role: data.role as any };
      }
    } catch {}
  }

  // Respaldo en almacenamiento local
  const localList = getLocalCollaborators();
  const match = localList.find((c) => c.email.toLowerCase() === normalizedEmail);
  if (match) {
    return { isCollaborator: true, role: match.role };
  }

  return { isCollaborator: false, role: null };
}

/**
 * Obtiene la lista completa de colaboradores (para el panel de administración).
 */
export async function getCollaborators(): Promise<Collaborator[]> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      const { data, error } = await supabase.from('collaborators').select('*').order('created_at', { ascending: true });
      if (!error && data && data.length > 0) {
        saveLocalCollaborators(data);
        return data;
      }
    } catch {}
  }
  return getLocalCollaborators();
}

/**
 * Agrega un nuevo colaborador.
 */
export async function addCollaborator(email: string, name = '', role: 'collaborator' | 'admin' = 'collaborator'): Promise<{ success: boolean; error?: string }> {
  const normalizedEmail = email.trim().toLowerCase();
  if (!normalizedEmail || !normalizedEmail.includes('@')) {
    return { success: false, error: 'Correo electrónico inválido.' };
  }

  const newCollab: Collaborator = {
    id: 'collab-' + Date.now(),
    email: normalizedEmail,
    name: name.trim() || normalizedEmail.split('@')[0],
    role,
    created_at: new Date().toISOString()
  };

  const supabase = getSupabase();
  if (supabase) {
    try {
      const { error } = await supabase.from('collaborators').insert([
        {
          email: normalizedEmail,
          name: newCollab.name,
          role: newCollab.role
        }
      ]);
      if (!error) {
        const localList = getLocalCollaborators().filter((c) => c.email !== normalizedEmail);
        localList.push(newCollab);
        saveLocalCollaborators(localList);
        return { success: true };
      }
    } catch {}
  }

  // Respaldo local
  const localList = getLocalCollaborators().filter((c) => c.email !== normalizedEmail);
  localList.push(newCollab);
  saveLocalCollaborators(localList);
  return { success: true };
}

/**
 * Elimina un colaborador por ID o correo.
 */
export async function removeCollaborator(idOrEmail: string): Promise<{ success: boolean; error?: string }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      await supabase.from('collaborators').delete().or(`id.eq.${idOrEmail},email.eq.${idOrEmail}`);
    } catch {}
  }

  const localList = getLocalCollaborators().filter((c) => c.id !== idOrEmail && c.email !== idOrEmail);
  saveLocalCollaborators(localList);
  return { success: true };
}

/**
 * Publica un modelo directamente en la base de datos comunitaria.
 */
export async function publishCommunityModel(modelData: {
  name: string;
  category?: string;
  description?: string;
  spec: any;
  tri_count?: number;
  author_name: string;
  author_email: string;
  is_public?: boolean;
  glb_data?: string;
}): Promise<{ success: boolean; model?: CommunityModel; error?: string }> {
  const slug = (modelData.name.toLowerCase().replace(/[^a-z0-9]+/g, '_') + '_' + Date.now().toString(36)).replace(/^_+|_+$/g, '');

  const newModel: CommunityModel = {
    id: 'model-' + Date.now(),
    slug,
    name: modelData.name,
    category: modelData.category || 'furniture',
    description: modelData.description || '',
    spec: modelData.spec,
    tri_count: modelData.tri_count || 350,
    author_name: modelData.author_name || 'Colaborador',
    author_email: modelData.author_email || 'colaborador@modelcoder.space',
    is_public: modelData.is_public ?? true,
    glb_data: modelData.glb_data,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  const supabase = getSupabase();
  if (supabase) {
    try {
      const { data, error } = await supabase.from('community_models').insert([
        {
          slug: newModel.slug,
          name: newModel.name,
          category: newModel.category,
          description: newModel.description,
          spec: newModel.spec,
          tri_count: newModel.tri_count,
          author_name: newModel.author_name,
          author_email: newModel.author_email,
          is_public: newModel.is_public,
          glb_data: newModel.glb_data
        }
      ]).select().single();

      if (!error && data) {
        newModel.id = data.id;
      }
    } catch (err) {
      console.warn('[ModelCoder] Guardando en cache local por fallo en Supabase:', err);
    }
  }

  // Siempre persistir también en respaldo local
  const localList = getLocalCommunityModels().filter((m) => m.slug !== newModel.slug);
  localList.unshift(newModel);
  saveLocalCommunityModels(localList);

  return { success: true, model: newModel };
}

/**
 * Obtiene los modelos subidos por la comunidad / colaboradores.
 */
export async function getCommunityModels(options?: { onlyPublic?: boolean }): Promise<CommunityModel[]> {
  const supabase = getSupabase();
  let models: CommunityModel[] = [];

  if (supabase) {
    try {
      let query = supabase.from('community_models').select('*').order('created_at', { ascending: false });
      if (options?.onlyPublic) {
        query = query.eq('is_public', true);
      }
      const { data, error } = await query;
      if (!error && data && data.length > 0) {
        models = data;
      }
    } catch {}
  }

  if (models.length === 0) {
    models = getLocalCommunityModels();
    if (options?.onlyPublic) {
      models = models.filter((m) => m.is_public);
    }
  }

  return models;
}

/**
 * Cambia la visibilidad pública / privada de un modelo.
 */
export async function toggleModelVisibility(id: string, is_public: boolean): Promise<{ success: boolean }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      await supabase.from('community_models').update({ is_public }).eq('id', id);
    } catch {}
  }

  const localList = getLocalCommunityModels();
  const match = localList.find((m) => m.id === id);
  if (match) {
    match.is_public = is_public;
    saveLocalCommunityModels(localList);
  }
  return { success: true };
}

/**
 * Elimina un modelo de la comunidad.
 */
export async function deleteCommunityModel(id: string): Promise<{ success: boolean }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      await supabase.from('community_models').delete().eq('id', id);
    } catch {}
  }

  const localList = getLocalCommunityModels().filter((m) => m.id !== id);
  saveLocalCommunityModels(localList);
  return { success: true };
}
