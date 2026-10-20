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

import { isTauriDesktop } from './tauri-bridge.ts';

export async function signInWithGitHub() {
  const supabase = getSupabase();
  if (!supabase) throw new Error('Supabase no está configurado aún.');
  const redirectTo = `${window.location.origin}/studio`;
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
  const emailRedirectTo = isTauriDesktop()
    ? 'https://modelcoder.vercel.app/studio'
    : `${window.location.origin}/studio`;
  const { data, error } = await supabase.auth.signUp({
    email,
    password: pass,
    options: {
      emailRedirectTo,
    }
  });
  if (error) throw error;
  return data;
}

export async function getSessionExportCode(): Promise<string | null> {
  const supabase = getSupabase();
  if (!supabase) return null;
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.access_token || !session?.refresh_token) return null;
  const payload = JSON.stringify({
    a: session.access_token,
    r: session.refresh_token,
  });
  return btoa(payload);
}

export async function importSessionFromCode(code: string): Promise<User | null> {
  const supabase = getSupabase();
  if (!supabase) throw new Error('Supabase no está disponible.');
  let payload: { a: string; r: string };
  try {
    payload = JSON.parse(atob(code.trim()));
  } catch {
    throw new Error('Código de sesión inválido o dañado.');
  }
  if (!payload.a || !payload.r) {
    throw new Error('Formato de sesión no reconocido.');
  }
  const { data, error } = await supabase.auth.setSession({
    access_token: payload.a,
    refresh_token: payload.r,
  });
  if (error) throw error;
  return data.user;
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
  status?: 'pending' | 'approved' | 'rejected';
  glb_data?: string;
  created_at: string;
  updated_at?: string;
}

export interface ModelComment {
  id: string;
  model_slug: string;
  author_name: string;
  content: string;
  created_at: string;
}

const LOCAL_COLLAB_KEY = 'modelcoder_collaborators_cache';
const LOCAL_MODELS_KEY = 'modelcoder_community_models_cache';
const LOCAL_COMMENTS_KEY = 'modelcoder_comments_cache';

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
    },
    {
      id: 'owner-github',
      email: 'franciscuarto',
      name: 'FrancisCuarto (GitHub)',
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
    if (raw) {
      const parsed: CommunityModel[] = JSON.parse(raw);
      // Filtrar el modelo de prueba técnico inicial
      return parsed.filter(m => m.slug !== 'test_connection_1792201558636' && m.name !== 'Test Model');
    }
  } catch {}
  return [];
}

function saveLocalCommunityModels(list: CommunityModel[]) {
  if (typeof window === 'undefined') return;
  const existingLocal = getLocalCommunityModels();
  const pendingLocal = existingLocal.filter(m => !m.is_public || m.status === 'pending' || m.spec?._submission_status === 'pending');

  const map = new Map<string, CommunityModel>();
  for (const item of list) {
    if (item.slug && item.slug !== 'test_connection_1792201558636' && item.name !== 'Test Model') {
      map.set(item.slug, item);
    }
  }
  for (const pending of pendingLocal) {
    if (!map.has(pending.slug)) {
      map.set(pending.slug, pending);
    }
  }

  const merged = Array.from(map.values());
  localStorage.setItem(LOCAL_MODELS_KEY, JSON.stringify(merged));
}

/**
 * Comprueba el rol del usuario actual por correo electrónico o identificador de GitHub.
 */
export async function checkUserRole(userOrEmail?: string | any): Promise<{ 
  isCollaborator: boolean; 
  role: 'owner' | 'admin' | 'collaborator' | null;
  identifier: string;
}> {
  if (!userOrEmail) return { isCollaborator: false, role: null, identifier: '' };

  let email = '';
  let githubUser = '';
  let displayName = '';

  if (typeof userOrEmail === 'string') {
    email = userOrEmail.trim().toLowerCase();
    if (email.startsWith('@')) {
      githubUser = email.slice(1);
    }
  } else if (typeof userOrEmail === 'object') {
    email = (userOrEmail.email || userOrEmail.user_metadata?.email || '').trim().toLowerCase();
    githubUser = (
      userOrEmail.user_metadata?.user_name || 
      userOrEmail.user_metadata?.preferred_username || 
      userOrEmail.identities?.[0]?.identity_data?.user_name || 
      userOrEmail.identities?.[0]?.identity_data?.preferred_username || 
      ''
    ).trim().toLowerCase();
    displayName = (
      userOrEmail.user_metadata?.name || 
      userOrEmail.user_metadata?.full_name || 
      userOrEmail.identities?.[0]?.identity_data?.name || 
      ''
    ).trim().toLowerCase();
  }

  const primaryIdentifier = githubUser ? `@${githubUser}` : email;

  // 1. Detección automática del Creador / Dueño (Franciscuarto / IV Orbit Games)
  const isOwner = 
    githubUser === 'franciscuarto' || 
    githubUser.includes('franciscuarto') ||
    email.includes('franciscuarto') || 
    email.includes('ivorbitgames') || 
    displayName.includes('franciscuarto') ||
    email.startsWith('admin@') ||
    (typeof window !== 'undefined' && localStorage.getItem('modelcoder_claimed_owner') === 'true');

  if (isOwner) {
    return { isCollaborator: true, role: 'owner', identifier: primaryIdentifier };
  }

  // 2. Consulta en base de datos Supabase
  const supabase = getSupabase();
  if (supabase) {
    try {
      let query = supabase.from('collaborators').select('*');
      if (email && githubUser) {
        query = query.or(`email.eq.${email},email.eq.${githubUser},email.eq.@${githubUser},name.ilike.%${githubUser}%`);
      } else if (email) {
        query = query.or(`email.eq.${email},email.eq.@${email}`);
      } else if (githubUser) {
        query = query.or(`email.eq.${githubUser},email.eq.@${githubUser},name.ilike.%${githubUser}%`);
      }

      const { data, error } = await query.maybeSingle();
      if (!error && data) {
        return { isCollaborator: true, role: data.role as any, identifier: primaryIdentifier };
      }
    } catch {}
  }

  // 3. Respaldo en almacenamiento local
  const localList = getLocalCollaborators();
  const match = localList.find((c) => {
    const cEmail = c.email.toLowerCase();
    const cName = (c.name || '').toLowerCase();
    return (
      (email && (cEmail === email || cEmail.includes(email))) ||
      (githubUser && (cEmail === githubUser || cEmail === `@${githubUser}` || cName.includes(githubUser)))
    );
  });

  if (match) {
    return { isCollaborator: true, role: match.role, identifier: primaryIdentifier };
  }

  return { isCollaborator: false, role: null, identifier: primaryIdentifier };
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
  if (!normalizedEmail) {
    return { success: false, error: 'Identificador o correo inválido.' };
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
 * Publica un modelo o envía una solicitud de publicación a revisión.
 * - Si isCollaborator es true: status = 'approved', is_public = true (publicación inmediata)
 * - Si isCollaborator es false: status = 'pending', is_public = false (solicitud pendiente de moderación)
 */
export async function publishCommunityModel(modelData: {
  name: string;
  category?: string;
  description?: string;
  spec: any;
  tri_count?: number;
  author_name: string;
  author_email?: string;
  is_public?: boolean;
  status?: 'pending' | 'approved';
  glb_data?: string;
  isCollaborator?: boolean;
}): Promise<{ 
  success: boolean; 
  model?: CommunityModel; 
  isPendingReview: boolean; 
  isLocalFallback?: boolean; 
  error?: string 
}> {
  // Exigir registro e inicio de sesión obligatorio para publicar
  const user = await getCurrentUser();
  if (!user) {
    return {
      success: false,
      isPendingReview: false,
      error: 'Debes iniciar sesión con tu cuenta de piloto para enviar modelos a revisión o publicarlos en el catálogo.'
    };
  }

  const isCollaborator = !!modelData.isCollaborator;
  const status: 'pending' | 'approved' = modelData.status || (isCollaborator ? 'approved' : 'pending');
  const isPublic = isCollaborator ? (modelData.is_public ?? true) : false;

  const slug = (modelData.name.toLowerCase().replace(/[^a-z0-9]+/g, '_') + '_' + Date.now().toString(36)).replace(/^_+|_+$/g, '');

  const specWithStatus = {
    ...modelData.spec,
    _submission_status: status
  };

  const authorEmail = user.email || modelData.author_email || 'piloto@modelcoder.community';
  const authorName = modelData.author_name?.trim() || 
    user.user_metadata?.user_name || 
    user.user_metadata?.preferred_username || 
    user.email?.split('@')[0] || 
    'Piloto Registrado';

  const newModel: CommunityModel = {
    id: 'model-' + Date.now(),
    slug,
    name: modelData.name,
    category: modelData.category || 'furniture',
    description: modelData.description || '',
    spec: specWithStatus,
    tri_count: modelData.tri_count || 350,
    author_name: authorName,
    author_email: authorEmail,
    is_public: isPublic,
    status,
    glb_data: modelData.glb_data,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  const supabase = getSupabase();
  let supabaseSuccess = false;
  let supabaseErrorMsg = '';

  if (supabase) {
    try {
      const insertPayload: any = {
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
      };

      // Se inserta directamente sin .select().single() para evitar que la política RLS de SELECT
      // aborte la transacción con código 42501 en modelos pendientes
      const { error } = await supabase
        .from('community_models')
        .insert([insertPayload]);

      if (error) {
        supabaseErrorMsg = error.message;
        console.warn('[ModelCoder] Fallo inserción en Supabase:', error.message);
      } else {
        supabaseSuccess = true;
      }
    } catch (err: any) {
      supabaseErrorMsg = err?.message || String(err);
      console.warn('[ModelCoder] Excepción en inserción en Supabase:', err);
    }
  }

  // Guardar siempre copia en la caché local para persistencia inmediata
  const localList = getLocalCommunityModels().filter((m) => m.slug !== newModel.slug);
  localList.unshift(newModel);
  saveLocalCommunityModels(localList);

  if (!supabaseSuccess && supabaseErrorMsg) {
    return { 
      success: false, 
      model: newModel, 
      isPendingReview: !isCollaborator,
      isLocalFallback: true,
      error: `No se pudo registrar la solicitud en la base de datos de Supabase (${supabaseErrorMsg}).`
    };
  }

  return { 
    success: true, 
    model: newModel, 
    isPendingReview: !isCollaborator,
    isLocalFallback: false 
  };
}

/**
 * Obtiene modelos de la comunidad.
 * - onlyPublic: true -> SOLO modelos aprobados y públicos (para el catálogo principal).
 * - status: 'pending' -> SOLO solicitudes pendientes de aprobación (para moderadores).
 * - status: 'approved' -> SOLO modelos aprobados.
 */
export async function getCommunityModels(options?: { 
  onlyPublic?: boolean; 
  status?: 'all' | 'pending' | 'approved' 
}): Promise<CommunityModel[]> {
  const supabase = getSupabase();
  let remoteModels: CommunityModel[] = [];

  if (supabase) {
    try {
      let query = supabase.from('community_models').select('*').order('created_at', { ascending: false });
      
      if (options?.onlyPublic) {
        query = query.eq('is_public', true);
      }

      const { data, error } = await query;
      if (!error && data && data.length > 0) {
        remoteModels = data.map((item: any) => {
          const itemStatus = item.status || item.spec?._submission_status || (item.is_public ? 'approved' : 'pending');
          return {
            ...item,
            status: itemStatus
          };
        });
      }
    } catch (err) {
      console.warn('[ModelCoder] Error consultando modelos remotos en Supabase:', err);
    }
  }

  // Combinar modelos remotos de Supabase con solicitudes locales
  const localModels = getLocalCommunityModels();
  const map = new Map<string, CommunityModel>();

  // 1. Añadir locales primero
  for (const m of localModels) {
    if (m.slug && m.slug !== 'test_connection_1792201558636' && m.name !== 'Test Model') {
      map.set(m.slug, m);
    }
  }
  // 2. Superponer remotos de Supabase
  for (const m of remoteModels) {
    if (m.slug && m.slug !== 'test_connection_1792201558636' && m.name !== 'Test Model') {
      map.set(m.slug, m);
    }
  }

  let models = Array.from(map.values());

  // Filtro de seguridad: purgar modelo de test ping si existiese
  models = models.filter((m) => m.slug !== 'test_connection_1792201558636' && m.name !== 'Test Model');

  if (options?.onlyPublic) {
    return models.filter((m) => m.is_public && m.status !== 'pending' && m.spec?._submission_status !== 'pending');
  }

  if (options?.status === 'pending') {
    return models.filter((m) => !m.is_public || m.status === 'pending' || m.spec?._submission_status === 'pending');
  }

  if (options?.status === 'approved') {
    return models.filter((m) => m.is_public && (m.status === 'approved' || !m.status) && m.spec?._submission_status !== 'pending');
  }

  return models;
}

/**
 * Obtiene todas las solicitudes de publicación pendientes de moderación.
 */
export async function getPendingCommunityModels(): Promise<CommunityModel[]> {
  return getCommunityModels({ onlyPublic: false, status: 'pending' });
}

/**
 * Aprueba una solicitud de publicación y la hace visible en el catálogo público.
 */
export async function approveCommunityModel(id: string): Promise<{ success: boolean; error?: string }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      const { data: existing } = await supabase.from('community_models').select('*').or(`id.eq.${id},slug.eq.${id}`).maybeSingle();
      const updatedSpec = existing?.spec ? { ...existing.spec, _submission_status: 'approved' } : undefined;

      const updatePayload: any = { is_public: true };
      if (updatedSpec) updatePayload.spec = updatedSpec;

      await supabase.from('community_models').update(updatePayload).or(`id.eq.${id},slug.eq.${id}`);
    } catch (err: any) {
      console.warn('[ModelCoder] Error approving model in Supabase:', err);
    }
  }

  const localList = getLocalCommunityModels();
  const match = localList.find((m) => m.id === id || m.slug === id);
  if (match) {
    match.is_public = true;
    match.status = 'approved';
    if (match.spec) match.spec._submission_status = 'approved';
    saveLocalCommunityModels(localList);
  }

  return { success: true };
}

/**
 * Cambia la visibilidad pública / privada de un modelo.
 */
export async function toggleModelVisibility(id: string, is_public: boolean): Promise<{ success: boolean }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      await supabase.from('community_models').update({ is_public }).or(`id.eq.${id},slug.eq.${id}`);
    } catch {}
  }

  const localList = getLocalCommunityModels();
  const match = localList.find((m) => m.id === id || m.slug === id);
  if (match) {
    match.is_public = is_public;
    saveLocalCommunityModels(localList);
  }
  return { success: true };
}

/**
 * Elimina o rechaza un modelo de la comunidad (por el creador o administrador).
 */
export async function deleteCommunityModel(id: string): Promise<{ success: boolean; error?: string }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      await supabase.from('community_models').delete().or(`id.eq.${id},slug.eq.${id}`);
    } catch (err: any) {
      console.warn('[ModelCoder] Error deleting from Supabase:', err);
    }
  }

  const localList = getLocalCommunityModels().filter((m) => m.id !== id && m.slug !== id);
  saveLocalCommunityModels(localList);
  return { success: true };
}

// ==============================================================================
// SISTEMA NATIVO DE COMENTARIOS Y TRANSMISIONES
// ==============================================================================

function getLocalComments(modelSlug: string): ModelComment[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(`${LOCAL_COMMENTS_KEY}_${modelSlug}`);
    if (raw) return JSON.parse(raw);
  } catch {}
  
  return [
    {
      id: 'seed-welcome-' + modelSlug,
      model_slug: modelSlug,
      author_name: 'FrancisCuarto (Creador)',
      content: '¡Canal de comunicación abierto para este modelo! Reporta detalles de malla, sugerencias de paletas o cómo lo integraste en tu proyecto.',
      created_at: new Date(Date.now() - 3600000 * 48).toISOString()
    }
  ];
}

function saveLocalComments(modelSlug: string, list: ModelComment[]) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(`${LOCAL_COMMENTS_KEY}_${modelSlug}`, JSON.stringify(list));
  } catch {}
}

export async function getModelComments(modelSlug: string): Promise<ModelComment[]> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      const { data, error } = await supabase
        .from('model_comments')
        .select('*')
        .eq('model_slug', modelSlug)
        .order('created_at', { ascending: true });
      if (!error && data && data.length > 0) {
        saveLocalComments(modelSlug, data);
        return data;
      }
    } catch {}
  }
  return getLocalComments(modelSlug);
}

export async function addModelComment(
  modelSlug: string, 
  authorName: string, 
  content: string
): Promise<{ success: boolean; comment?: ModelComment; error?: string }> {
  const trimmedAuthor = authorName.trim() || 'Piloto de la Comunidad';
  const trimmedContent = content.trim();

  if (!trimmedContent) {
    return { success: false, error: 'El mensaje de transmisión no puede estar vacío.' };
  }

  const newComment: ModelComment = {
    id: 'comm-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6),
    model_slug: modelSlug,
    author_name: trimmedAuthor,
    content: trimmedContent,
    created_at: new Date().toISOString()
  };

  const supabase = getSupabase();
  if (supabase) {
    try {
      const { data, error } = await supabase
        .from('model_comments')
        .insert([{
          model_slug: newComment.model_slug,
          author_name: newComment.author_name,
          content: newComment.content
        }])
        .select()
        .single();
      if (!error && data) {
        newComment.id = data.id;
      }
    } catch {}
  }

  const list = getLocalComments(modelSlug);
  list.push(newComment);
  saveLocalComments(modelSlug, list);

  return { success: true, comment: newComment };
}

export async function deleteModelComment(commentId: string, modelSlug: string): Promise<{ success: boolean }> {
  const supabase = getSupabase();
  if (supabase) {
    try {
      await supabase.from('model_comments').delete().eq('id', commentId);
    } catch {}
  }

  const list = getLocalComments(modelSlug).filter((c) => c.id !== commentId);
  saveLocalComments(modelSlug, list);
  return { success: true };
}
