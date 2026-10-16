-- ==============================================================================
-- MODELCODER — CONFIGURACIÓN DE TABLAS PARA COLABORADORES Y PUBLICACIÓN DIRECTA
-- Ejecuta este script en el SQL Editor de tu Dashboard de Supabase
-- (https://supabase.com/dashboard/project/jegdicdnhetdzmcuznqy/sql)
-- ==============================================================================

-- 1. Habilitar extensión pgcrypto para UUIDs si no está habilitada
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. TABLA: collaborators (Colaboradores y Administradores autorizados)
CREATE TABLE IF NOT EXISTS public.collaborators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    role TEXT NOT NULL DEFAULT 'collaborator' CHECK (role IN ('owner', 'admin', 'collaborator')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. TABLA: community_models (Modelos subidos directamente sin pasar por GitHub)
CREATE TABLE IF NOT EXISTS public.community_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'furniture',
    description TEXT DEFAULT '',
    spec JSONB NOT NULL,
    tri_count INTEGER DEFAULT 0,
    author_name TEXT NOT NULL,
    author_email TEXT NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT true,
    glb_data TEXT, -- Base64 Data URL del binario .GLB para render y descarga instantánea
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_community_models_slug ON public.community_models(slug);
CREATE INDEX IF NOT EXISTS idx_community_models_category ON public.community_models(category);
CREATE INDEX IF NOT EXISTS idx_community_models_public ON public.community_models(is_public);
CREATE INDEX IF NOT EXISTS idx_collaborators_email ON public.collaborators(email);

-- 4. Habilitar Row Level Security (RLS)
ALTER TABLE public.collaborators ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_models ENABLE ROW LEVEL SECURITY;

-- 5. POLÍTICAS DE ACCESO (Permitir lectura y gestión con la clave anon pública)
-- Permitir lectura de colaboradores para validar permisos
DROP POLICY IF EXISTS "Permitir lectura publica de colaboradores" ON public.collaborators;
CREATE POLICY "Permitir lectura publica de colaboradores" ON public.collaborators
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Permitir gestion de colaboradores" ON public.collaborators;
CREATE POLICY "Permitir gestion de colaboradores" ON public.collaborators
    FOR ALL USING (true) WITH CHECK (true);

-- Permitir lectura de modelos públicos para todo el mundo
DROP POLICY IF EXISTS "Lectura de modelos publicos" ON public.community_models;
CREATE POLICY "Lectura de modelos publicos" ON public.community_models
    FOR SELECT USING (true);

-- Permitir inserción, actualización y borrado de modelos
DROP POLICY IF EXISTS "Gestion de modelos" ON public.community_models;
CREATE POLICY "Gestion de modelos" ON public.community_models
    FOR ALL USING (true) WITH CHECK (true);

-- 6. Insertar al Creador como OWNER por defecto (cambia o agrega tu correo exacto aquí)
INSERT INTO public.collaborators (email, name, role)
VALUES 
    ('franciscuarto@ivorbitgames.online', 'Franciscuarto (Dueño)', 'owner'),
    ('admin@modelcoder.space', 'Admin', 'owner')
ON CONFLICT (email) DO NOTHING;
