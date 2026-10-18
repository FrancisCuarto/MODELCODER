# Inventario de Recursos y Auditoría de Activos — ModelCoder

**Fecha de auditoría:** 17 de octubre de 2026  
**Responsable:** Antigravity (Asistente de Contenido y Operaciones)  
**Proyecto:** ModelCoder (IV Orbit Games)  
**Canal:** Instagram (`@modelcoder`)  
**Web Oficial:** https://modelcoder.vercel.app/  

---

## 1. Estado de la Cuenta de Instagram (`@modelcoder`)

- **Handle:** `@modelcoder` (nombre de usuario oficial exacto).
- **Nombre de perfil:** `Model Coder`.
- **Foto de perfil:** Configurada con el isotipo / logo oficial de ModelCoder.
- **Biografía actual:** Vacía (pendiente de configuración inicial).
- **Enlace actual:** Ninguno (pendiente de agregar `https://modelcoder.vercel.app/`).
- **Publicaciones:** 0 publicaciones (cuenta lista para lanzamiento / clean slate).
- **Seguidores / Seguidos:** 0 / 0.
- **Tipo de cuenta:** Personal (se recomienda migrar a cuenta Profesional / Creador para acceder a estadísticas e Insights).

---

## 2. Recursos Visuales y de Software Disponibles

### A. Plataforma Web y Studio 3D (`https://modelcoder.vercel.app/`)
- **Catálogo interactivo en vivo:** 103 modelos procedurales listos para previsualizar y descargar en formato `.glb`.
- **Visor 3D en navegador:** Basado en `<model-viewer>` y Three.js, con rotación orbital suave, sombra e iluminación calibrada.
- **Fichas individuales (`/generators/[family]`):**
  - Controles de cámara: Rotación (20°/s), Centrado y Botón nativo de Captura de Pantalla (`#screenshot-btn`).
  - Selectores de presets rápidos (ej. versiones limpias, desgastadas, de emergencia).
  - Selectores de las 5 paletas de sector.
  - Sliders interactivos de parámetros (ancho, alto, accesorios).
  - Descarga de `.glb` y metadatos `.json`.
- **ModelCoder Studio 3D (`/studio`):**
  - **Modo IA:** Generación por prompts en lenguaje natural usando **Gemini 3.8 Flash**.
  - **Editor 3D Visual:** Árbol de piezas (outliner), gizmos de mover/rotar/escalar, modos de sombreado PSX, rejilla y snap.
  - **Editor de Código:** Edición en vivo y compilación directa con Three.js y Blender.
  - Modelo por defecto en viewport: Contenedor modular de carga (`crate_hull`).

### B. Motor Procedural en Python / Blender (`d:\MODELCODER`)
- **44 Familias de generadores modulares:**
  - *Mobiliario:* `office_desk`, `office_chair`, `crew_bed`, `bunk_bed`, `nightstand`, `mess_table`, `locker_bench`, `locker`, etc.
  - *Médico & Laboratorio:* `autopsy_table`, `crash_cart`, `medical_screen`, `morgue_gurney`, `chemical_cabinet`, `restraint_chair`, `scrub_sink`, `oxypod`.
  - *Infraestructura & Dispositivos:* `electrical_panel`, `pipes`, `cable_bundle`, `vent_grate`, `crate`, `terminal`, `server_rack`, `door`, `airlock_door`.
  - *Arquitectura:* `station_corridor` (pasillos rectos, cruces, vanos), `station_room` (habitaciones modulares completas).
- **Archivos exportados preexistentes:** Decenas de archivos `.glb`, `.blend`, `.json` y reportes en `exports/` y `output/`.
- **Atlas de textura PS1:** Atlas procedural 256×256 con protección anti-bleeding y sombreado retro PSX.
- **Pipeline de exportación Godot 4:** Mallas de colisión automáticas (`-convcolonly`) y sockets (`socket_*`).

### C. Identidad de Marca y Activos Gráficos
- **Logo:** `d:\MODELCODER\web\public\logo.png`.
- **Paleta de marca:** Retro industrial sci-fi (dorado PS1 `#d4a373`, cian terminal `#26d9f2`, verde ámbar, gris acorazado y negro carbón).
- **Tipografía y estilo:** Estética retro-tech / terminal de sistemas / low-poly de quinta generación.
- **Conexión narrativa:** Props y escenografía oficial del videojuego *Below Nominal* (IV Orbit Games).

---

## 3. Materiales Reutilizables de Inmediato para Producción

1. **Renders y Modelos 3D Preexistentes:**
   - 103 modelos `.glb` optimizados en `web/public/models/`.
   - Vistas interactivas de 360 grados capturables directamente desde el navegador o mediante script headless de Blender.
2. **Capturas de Pantalla Limpias:**
   - Capturas del catálogo con filtros activos (ej. "Mobiliario", "Médico").
   - Capturas del Studio 3D mostrando los gizmos, el árbol de componentes y la generación asistida por IA.
3. **Grabaciones de Pantalla en Video (para Reels):**
   - Recorrido de 15 segundos ajustando sliders en `/generators/crash_cart` o `/generators/autopsy_table` y descargando el `.glb`.
   - Importación de un `.glb` recién generado en Godot 4 arrastrando el archivo a la escena 3D.
