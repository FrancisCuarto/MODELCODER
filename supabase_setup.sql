-- ==============================================================================
-- MODELCODER — CONFIGURACIÓN DE TABLAS PARA COLABORADORES, MODERACIÓN & COMENTARIOS
-- Ejecuta este script en el SQL Editor de tu Dashboard de Supabase:
-- https://supabase.com/dashboard/project/jegdicdnhetdzmcuznqy/sql
-- ==============================================================================

-- 1. Habilitar extensión pgcrypto para UUIDs si no está habilitada
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. TABLA: collaborators (Colaboradores y Administradores autorizados)
CREATE TABLE IF NOT EXISTS public.collaborators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL, -- Puede ser un email (ej: usuario@gmail.com) o usuario de GitHub (ej: @pepito)
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
    status TEXT NOT NULL DEFAULT 'approved' CHECK (status IN ('pending', 'approved', 'rejected')),
    glb_data TEXT, -- Base64 Data URL del binario .GLB para render y descarga instantánea
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Asegurar columna status si la tabla ya existía
ALTER TABLE public.community_models ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'approved' CHECK (status IN ('pending', 'approved', 'rejected'));

-- 4. TABLA: model_comments (Terminal de transmisiones y feedback sobre modelos)
CREATE TABLE IF NOT EXISTS public.model_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_slug TEXT NOT NULL,
    author_name TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_community_models_slug ON public.community_models(slug);
CREATE INDEX IF NOT EXISTS idx_community_models_category ON public.community_models(category);
CREATE INDEX IF NOT EXISTS idx_community_models_public ON public.community_models(is_public);
CREATE INDEX IF NOT EXISTS idx_community_models_status ON public.community_models(status);
CREATE INDEX IF NOT EXISTS idx_collaborators_email ON public.collaborators(email);
CREATE INDEX IF NOT EXISTS idx_model_comments_slug ON public.model_comments(model_slug);

-- 5. Habilitar Row Level Security (RLS) en todas las tablas
ALTER TABLE public.collaborators ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_models ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.model_comments ENABLE ROW LEVEL SECURITY;

-- 6. FUNCIONES DE SEGURIDAD EN POSTGRESQL (Para validar dueño y colaboradores)
CREATE OR REPLACE FUNCTION public.is_owner_or_admin()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (
    -- Caso A: El usuario conectado por GitHub es FrancisCuarto o contiene franciscuarto
    lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', '')) = 'franciscuarto'
    OR lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'preferred_username', '')) = 'franciscuarto'
    OR lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'name', '')) LIKE '%franciscuarto%'
    OR lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'full_name', '')) LIKE '%franciscuarto%'
    -- Caso B: El correo contiene franciscuarto o ivorbitgames
    OR lower(coalesce(auth.jwt() ->> 'email', '')) LIKE '%franciscuarto%'
    OR lower(coalesce(auth.jwt() ->> 'email', '')) LIKE '%ivorbitgames%'
    -- Caso C: Está registrado en la tabla con rol 'owner' o 'admin'
    OR EXISTS (
      SELECT 1 FROM public.collaborators
      WHERE (
        email = lower(auth.jwt() ->> 'email')
        OR email = lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', ''))
        OR email = '@' || lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', ''))
        OR email = lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'preferred_username', ''))
      ) AND role IN ('owner', 'admin')
    )
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION public.is_collaborator()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (
    public.is_owner_or_admin()
    OR EXISTS (
      SELECT 1 FROM public.collaborators
      WHERE email = lower(auth.jwt() ->> 'email')
         OR email = lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', ''))
         OR email = '@' || lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', ''))
         OR email = lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'preferred_username', ''))
    )
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 7. POLÍTICAS DE ACCESO BLINDADAS (RLS)
-- A. TABLA: collaborators
DROP POLICY IF EXISTS "Lectura publica de colaboradores" ON public.collaborators;
DROP POLICY IF EXISTS "Gestion exclusiva de colaboradores para owner y admin" ON public.collaborators;

CREATE POLICY "Lectura publica de colaboradores" 
ON public.collaborators FOR SELECT 
USING (true);

CREATE POLICY "Gestion exclusiva de colaboradores para owner y admin" 
ON public.collaborators FOR ALL 
TO authenticated
USING (public.is_owner_or_admin())
WITH CHECK (public.is_owner_or_admin());

-- B. TABLA: community_models
DROP POLICY IF EXISTS "Lectura de modelos publicos o privados de equipo" ON public.community_models;
DROP POLICY IF EXISTS "Publicacion de modelos en comunidad" ON public.community_models;
DROP POLICY IF EXISTS "Edicion de modelos" ON public.community_models;
DROP POLICY IF EXISTS "Eliminacion de modelos" ON public.community_models;

-- 1. Lectura: Modelos públicos para todos; privados/pendientes para moderadores o el autor
CREATE POLICY "Lectura de modelos publicos o privados de equipo" 
ON public.community_models FOR SELECT 
USING (true);

-- 2. Inserción: Permitir que cualquier visitante o colaborador envíe modelos
CREATE POLICY "Publicacion de modelos en comunidad" 
ON public.community_models FOR INSERT 
WITH CHECK (true);

-- 3. Modificación: Dueño/admin puede aprobar/modificar cualquier modelo; autor puede editar el suyo
CREATE POLICY "Edicion de modelos" 
ON public.community_models FOR UPDATE 
TO authenticated
USING (
  public.is_owner_or_admin() 
  OR author_email = (auth.jwt() ->> 'email')
  OR author_name ILIKE ('%' || coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', 'xyz_none') || '%')
);

-- 4. Eliminación: Solo dueño/admin o el autor
CREATE POLICY "Eliminacion de modelos" 
ON public.community_models FOR DELETE 
TO authenticated
USING (
  public.is_owner_or_admin() 
  OR author_email = (auth.jwt() ->> 'email')
  OR author_name ILIKE ('%' || coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', 'xyz_none') || '%')
);

-- C. TABLA: model_comments
DROP POLICY IF EXISTS "Lectura publica de comentarios" ON public.model_comments;
DROP POLICY IF EXISTS "Publicacion de comentarios" ON public.model_comments;
DROP POLICY IF EXISTS "Eliminacion de comentarios" ON public.model_comments;

CREATE POLICY "Lectura publica de comentarios" 
ON public.model_comments FOR SELECT 
USING (true);

CREATE POLICY "Publicacion de comentarios" 
ON public.model_comments FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Eliminacion de comentarios" 
ON public.model_comments FOR DELETE 
TO authenticated 
USING (public.is_owner_or_admin());

-- 8. Purgar modelo de prueba técnico si existiese en la base de datos
DELETE FROM public.community_models WHERE slug = 'test_connection_1792201558636' OR name = 'Test Model';

-- 9. Insertar al Creador (Franciscuarto) por defecto
INSERT INTO public.collaborators (email, name, role)
VALUES 
    ('franciscuarto@ivorbitgames.online', 'Franciscuarto (Dueño)', 'owner'),
    ('franciscuarto', 'Franciscuarto (GitHub)', 'owner'),
    ('@franciscuarto', 'Franciscuarto (GitHub Handle)', 'owner')
ON CONFLICT (email) DO NOTHING;
