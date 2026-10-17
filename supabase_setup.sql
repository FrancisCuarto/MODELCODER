-- ==============================================================================
-- MODELCODER — CONFIGURACIÓN DE TABLAS PARA COLABORADORES Y PUBLICACIÓN DIRECTA
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
    glb_data TEXT, -- Base64 Data URL del binario .GLB para render y descarga instantánea
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_community_models_slug ON public.community_models(slug);
CREATE INDEX IF NOT EXISTS idx_community_models_category ON public.community_models(category);
CREATE INDEX IF NOT EXISTS idx_community_models_public ON public.community_models(is_public);
CREATE INDEX IF NOT EXISTS idx_collaborators_email ON public.collaborators(email);

-- 4. Habilitar Row Level Security (RLS) en ambas tablas
ALTER TABLE public.collaborators ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_models ENABLE ROW LEVEL SECURITY;

-- 5. FUNCIONES DE SEGURIDAD EN POSTGRESQL (Para validar dueño y colaboradores)
CREATE OR REPLACE FUNCTION public.is_owner_or_admin()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (
    -- Caso A: El usuario conectado por GitHub es FrancisCuarto
    lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', '')) = 'franciscuarto'
    OR lower(coalesce(auth.jwt() -> 'user_metadata' ->> 'preferred_username', '')) = 'franciscuarto'
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
    )
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 6. POLÍTICAS DE ACCESO BLINDADAS (RLS)
-- Limpiar políticas anteriores si existían
DROP POLICY IF EXISTS "Permitir lectura publica de colaboradores" ON public.collaborators;
DROP POLICY IF EXISTS "Permitir gestion de colaboradores" ON public.collaborators;
DROP POLICY IF EXISTS "Lectura publica de colaboradores" ON public.collaborators;
DROP POLICY IF EXISTS "Gestion exclusiva de colaboradores para owner y admin" ON public.collaborators;

-- A. TABLA: collaborators
-- 1. Lectura pública (para que el frontend reconozca quién es colaborador)
CREATE POLICY "Lectura publica de colaboradores" 
ON public.collaborators FOR SELECT 
USING (true);

-- 2. Solo el DUEÑO o ADMINISTRADORES pueden agregar o quitar colaboradores
CREATE POLICY "Gestion exclusiva de colaboradores para owner y admin" 
ON public.collaborators FOR ALL 
TO authenticated
USING (public.is_owner_or_admin())
WITH CHECK (public.is_owner_or_admin());

-- B. TABLA: community_models
DROP POLICY IF EXISTS "Lectura de modelos publicos" ON public.community_models;
DROP POLICY IF EXISTS "Gestion de modelos" ON public.community_models;
DROP POLICY IF EXISTS "Lectura de modelos publicos o privados de equipo" ON public.community_models;
DROP POLICY IF EXISTS "Publicacion exclusiva de colaboradores" ON public.community_models;
DROP POLICY IF EXISTS "Edicion y borrado de modelos" ON public.community_models;
DROP POLICY IF EXISTS "Eliminacion de modelos" ON public.community_models;

-- 1. Lectura: Público para todos si is_public=true; si es privado, solo colaboradores
CREATE POLICY "Lectura de modelos publicos o privados de equipo" 
ON public.community_models FOR SELECT 
USING (is_public = true OR public.is_collaborator());

-- 2. Inserción: Solo colaboradores y dueño pueden publicar modelos directamente
CREATE POLICY "Publicacion exclusiva de colaboradores" 
ON public.community_models FOR INSERT 
TO authenticated
WITH CHECK (public.is_collaborator());

-- 3. Modificación: Solo el dueño/admin o el propio autor del modelo
CREATE POLICY "Edicion de modelos" 
ON public.community_models FOR UPDATE 
TO authenticated
USING (
  public.is_owner_or_admin() 
  OR author_email = (auth.jwt() ->> 'email')
  OR author_name ILIKE ('%' || coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', 'xyz_none') || '%')
);

-- 4. Eliminación: Solo el dueño/admin o el autor
CREATE POLICY "Eliminacion de modelos" 
ON public.community_models FOR DELETE 
TO authenticated
USING (
  public.is_owner_or_admin() 
  OR author_email = (auth.jwt() ->> 'email')
  OR author_name ILIKE ('%' || coalesce(auth.jwt() -> 'user_metadata' ->> 'user_name', 'xyz_none') || '%')
);

-- 7. Insertar al Creador (Franciscuarto) por defecto
INSERT INTO public.collaborators (email, name, role)
VALUES 
    ('franciscuarto@ivorbitgames.online', 'Franciscuarto (Dueño)', 'owner'),
    ('franciscuarto', 'Franciscuarto (GitHub)', 'owner'),
    ('@franciscuarto', 'Franciscuarto (GitHub Handle)', 'owner')
ON CONFLICT (email) DO NOTHING;
