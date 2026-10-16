# Auditoría Funcional y de Experiencia de Usuario (UX) — ModelCoder

> **Fecha:** 16 de Octubre de 2026  
> **Ámbito:** Plataforma web ModelCoder (`web/src`), integración con motor procedural (`procedural_assets/`), exportación GLB y Studio 3D.  
> **Objetivo:** Identificar bloqueos reales, fricciones cognitivas, redundancias y fallos en el flujo de usuario desde el descubrimiento hasta la descarga y reutilización.

---

## 1. Flujo Probado de Principio a Fin

Se auditó el flujo de una persona usuaria que llega a ModelCoder para obtener un activo 3D:
1. **Llegada y Descubrimiento:** Ingreso a la página de inicio (`/`), lectura de la propuesta de valor, uso de buscador y filtros por categoría.
2. **Selección y Navegación:** Clic en una tarjeta de generador (p. ej. `access_card_lvl1`, `door`, `terminal`).
3. **Inspección 3D y Personalización:**
   - Carga del visor interactivo `<model-viewer>`.
   - Manipulación de controles (cámara, rotación, zoom).
   - Cambio de presets predefinidos.
   - Modificación de parámetros numéricos, paletas de color y booleanos.
4. **Descarga del Modelo:**
   - Prueba de descarga directa y descarga de modelo personalizado.
   - Validación de qué archivo se descarga y su correspondencia con lo visto en pantalla.
5. **Post-Descarga y Reutilización:** Verificación de mensajes de confirmación y guías de importación a motores (Godot, Unity, Blender).
6. **Recorrido de Creación (Studio 3D):**
   - Acceso al Studio (`/studio`).
   - Flujo de generación por prompt con Gemini 3.8 Flash.
   - Requisitos de credenciales (API Key) y publicación a GitHub.

---

## 2. Problemas Confirmados y Clasificación por Prioridad

| ID | Área | Problema Confirmado | Impacto en el Usuario | Prioridad |
|---|---|---|---|---|
| **ISSUE-01** | Catálogo | Textos genéricos y nombres en inglés: 40+ generadores muestran `"Generador procedural paramétrico de [family] para Below Nominal."` y nombres sin traducir (`"Bridge Console Desk"`, `"Heavy Shelving"`). | Confusión inmediata; parece una consola de depuración interna en vez de una biblioteca usable. | **P1** |
| **ISSUE-02** | Catálogo / Layout | Desfase en contadores de telemetría: el header y hero indican `44 MODELOS LISTOS`, pero el catálogo cuenta con **45 generadores reales** activos (`access_card_lvl1` añadido). | Inconsistencia en la información visual mostrada al usuario. | **P1** |
| **ISSUE-03** | Ficha de Modelo | Duplicidad de botones de descarga con nombres confusos: existe `💾 DESCARGAR MODELO (.GLB)` bajo el visor y `💾 DESCARGAR GLB PERSONALIZADO` en el panel derecho. | El usuario duda sobre cuál botón refleja los cambios aplicados en pantalla. | **P1** |
| **ISSUE-04** | Ficha de Modelo | Falta de retroalimentación post-descarga: al presionar descargar no hay mensaje de confirmación claro (`"Tu modelo está listo..."`) ni guía accesible para abrirlo en Godot/Blender. | El usuario se queda sin saber cómo continuar tras obtener el archivo. | **P1** |
| **ISSUE-05** | Ficha de Modelo | Competencia visual entre opciones básicas y avanzadas: el formulario expone de golpe opciones de worker remoto, comando de terminal Blender CLI, código Python y manifiesto JSON sin agrupar. | Abruma a usuarios que solo quieren cambiar un color o tamaño y descargar el 3D. | **P1** |
| **ISSUE-06** | Navegación | Falta de separación entre el camino "Quiero usar un modelo" y "Quiero crear un generador": la barra de navegación y el inicio mezclan herramientas de código y lanzadores con el catálogo general. | No guía con claridad según la intención del visitante. | **P2** |
| **ISSUE-07** | Studio 3D | Explicación previa de requisitos de IA incompleta: la caja de prompt no explica de entrada que se requiere una clave gratuita de Google AI Studio ni sus capacidades/limitaciones antes de interactuar. | Fricción al toparse con el cajón de clave o errores de cuota sin contexto previo. | **P2** |
| **ISSUE-08** | Ficha de Modelo | Presets y controles no explican qué unidades o impacto tienen (ej. metros, porcentaje de desgaste) en algunos generadores. | Dificulta estimar la escala real del objeto en su motor. | **P3** |
| **ISSUE-09** | Ficha de Modelo | Falta de un mecanismo simple y privado para reportar fallos de un modelo específico (ej. malla rota o textura incorrecta). | Si un usuario encuentra un error, debe abrir GitHub manualmente sin contexto prellenado. | **P3** |

---

## 3. Funciones que Funcionan Correctamente (Línea Base)

- **Renderizado 3D WebGL:** `<model-viewer>` carga de forma fluida los archivos `.glb` pre-empaquetados en `web/public/models/`.
- **Rotación e Interacción:** Controles táctiles y de ratón (órbita, encuadre, zoom) funcionan según lo previsto.
- **Cambio de Presets en Vivo:** Al pulsar un preset en la ficha, los campos del formulario se actualizan y disparan el reescalado dinámico.
- **Exportación en el Navegador:** `viewer.exportScene({ binary: true })` genera un blob binario GLB descargable sin necesidad de backend externo.
- **Búsqueda y Filtros en Catálogo:** El filtrado por texto y categorías responde instantáneamente en el cliente.
- **Suite de Pruebas Automatizadas:** 68 tests unitarios pasando en Blender 5.0 (`run_tests.ps1`) y build estático de Astro 100% exitoso.

---

## 4. Funciones que No se Pudieron Comprobar en Remoto (o que dependen de entorno)

- **Worker Remoto Localhost (`http://localhost:8000/api/generate`):** Depende de que el usuario tenga una instancia local de Python/Blender corriendo. En el navegador web estático (Vercel), opera adecuadamente en modo autónomo mediante `exportScene`.
- **Publicación directa con GitHub PAT:** Depende de un Personal Access Token con permisos en el repositorio; el flujo recomendado de 1-clic por GitHub Issues es el canal predeterminado y seguro.

---

## 5. Plan de Acción y Componentes Afectados

### Prioridad 1 (P1) — Catálogo, Textos y Descarga Inequívoca
1. **Unificar nombres y descripciones en español en los manifiestos:**
   - Actualizar los archivos `procedural_assets/generators/*/manifest.json` con nombres cotidianos legibles y descripciones orientadas a la personalización útil (sin jerga interna de "Below Nominal").
   - Ejecutar `tools/sync_web_catalog.py` para sincronizar `web/src/data/catalog.json`.
2. **Corregir contadores y consistencia en el Catálogo:**
   - Actualizar `web/src/pages/index.astro` y `web/src/layouts/Layout.astro` para calcular dinámicamente `{catalog.length}` (45 modelos) en lugar de cadenas hardcodeadas.
3. **Jerarquía y Descarga en Ficha de Generador (`web/src/pages/generators/[family].astro`):**
   - Establecer una **única acción principal de descarga**: `"Descargar modelo personalizado (.GLB)"`.
   - Si se desea el archivo base sin alteraciones, proveer un enlace secundario y diferenciado (`"Descargar versión original"`).
   - Añadir mensaje de confirmación post-descarga claro con modal/acordeón `"¿Cómo uso este archivo?"` con pasos para Godot 4, Unity y Blender.
   - Reorganizar el panel derecho: agrupar los parámetros por intención (Medidas, Estilo, Accesorios) y colocar herramientas técnicas (CLI, Manifest JSON, Código Python, Worker) en una sección secundaria colapsable `"Herramientas avanzadas"`.

### Prioridad 2 (P2) — Separación de Recorridos y Studio con IA
1. **Navegación e Inicio:**
   - Diferenciar visualmente `"Quiero usar un modelo"` (recorrido guiado estándar) y `"Quiero crear un generador"` (Studio, documentación y código).
2. **Claridad en Studio 3D (`web/src/pages/studio.astro`):**
   - Presentar antes del prompt qué hace la IA (genera código procedural low-poly para Blender), qué requiere (API Key gratuita de Google AI Studio guardada localmente) y sus limitaciones.

### Prioridad 3 (P3) — Guías de Integración y Reporte de Problemas
1. **Módulo de Reporte de Problemas:** Enlace preconfigurado para reportar incidencias del modelo en GitHub Issues sin tokens ni datos sensibles.
2. **Compartir configuración:** Posibilidad de copiar enlace directo con los parámetros activos en la URL para compartir o reutilizar.
