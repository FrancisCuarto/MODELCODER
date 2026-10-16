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
