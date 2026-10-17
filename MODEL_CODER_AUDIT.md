# MODEL CODER — Technical & Functional Audit (`MODEL_CODER_AUDIT.md`)

**Date:** 2026-10-17  
**Branch:** `polish/product-completion`  
**Baseline Status:** `npm --prefix web test` (27/27 assertions passing) | `npm --prefix web run build` (105 static pages built cleanly)

---

## 1. Architecture & System Overview

ModelCoder is a dual-stack 3D content creation and management platform combining:
1. **Python Parametric Engine (`generators/`, `framework/`, `textures/`):** 101 procedural 3D asset generators organized across 11 categories (`props`, `industrial`, `structural`, `nature`, `scifi`, `interiors`, `vehicles`, `characters`, `weapons`, `food`, `retro_tech`) with procedural PBR textures and an export pipeline generating `.glb` assets and `catalog_manifest.json`.
2. **Astro + Three.js Web Application (`web/`):**
   - **Catalog (`web/src/pages/index.astro`):** Searchable, filterable grid of 101 procedural generators + community models with `<model-viewer>` previews.
   - **Generator Inspector (`web/src/pages/generators/[family].astro`):** Interactive 3D viewer, real-time PBR texture/material customizer, UV projection scale, vertex painting, custom `.glb` export, favorites, collections, and community comments.
   - **Studio 3D (`web/src/pages/studio.astro` & `web/src/lib/studio/`):** Full-screen Blender-style 3D procedural & AI modeling suite (`AIGenerator`, `ProceduralEngine`, `StudioViewport`, `GLBExporterService`, `StudioTextureLibrary`, `CodeSandbox`) with Outliner, Transform Gizmos, PBR Material Library, Code Sandbox, Render Capture, and Draft Persistence.
   - **Community & Moderation (`web/src/pages/contribute.astro`, `web/src/pages/colaboradores.astro`):** Direct `.glb` submission queue and collaborator moderation dashboard backed by Supabase + local fallback.
   - **Global Inventory & Auth (`web/src/layouts/Layout.astro`, `web/src/lib/user-inventory.ts`):** Unified persistent system for Studio drafts (`modelcoder_project_drafts_v1`), Favorite models (`modelcoder_favorites_v1`), and custom Collections (`modelcoder_collections_v1`) with local + cloud sync.

---

## 2. Classification of Findings (P0 – P3)

### P0 — Blocking Defects, Data/Asset Loss, or Severe Risk

#### [P0-01] **Proven Defect:** GLB Export Material & Texture Loss When Viewport is in Inspection Shading Mode
- **Location:** `web/src/lib/studio/three-viewport.ts` (lines 494–545) & `web/src/pages/studio.astro` (lines 2856–2876)
- **Evidence:** When a user switches the Studio 3D viewport shading mode to `wireframe`, `normals`, `vertex_colors`, or `unlit`, `StudioViewport.setShadingMode()` replaces `mesh.material` in-place on `this.currentMesh` with temporary inspection materials (e.g., `THREE.MeshNormalMaterial` or cyan wireframe `MeshBasicMaterial`), storing original PBR materials in `this.currentShadingMaterialsBackup`. When the user clicks `💾 EXPORTAR GLB`, `exportGlbBtn` calls `viewport.getVisibleObject()` directly. Because `GLTFExporter` does not support `MeshNormalMaterial` (and treats wireframe debug materials as the actual mesh surface), exporting while in any non-`material` shading mode strips PBR textures/materials or exports a flat cyan wireframe.
- **Recommended Solution:** Add `executeWithOriginalMaterials<T>(fn: (root: THREE.Object3D) => Promise<T>): Promise<T>` (and proper disposal of temporary shading materials) in `StudioViewport` so GLB export always restores original PBR materials before serializing and restores the active inspection shading mode immediately afterward.

---

### P1 — Broken Functionality or Critical Engineering / Security Issue

#### [P1-01] **Proven Defect:** Shallow Clone Dangling Disposed Geometry Reference in `StudioViewport`
- **Location:** `web/src/lib/studio/three-viewport.ts` (line 267)
- **Evidence:** `this.lastValidMesh = obj.clone();` performs a shallow clone of the `THREE.Object3D` hierarchy, sharing `BufferGeometry` and `Material` instances with `this.currentMesh`. On the subsequent generation, `ProceduralEngine.disposeHierarchy(this.currentMesh)` disposes all geometries and materials in `this.currentMesh`, leaving `this.lastValidMesh` holding references to disposed WebGL buffers and textures in memory.
- **Recommended Solution:** Replace `lastValidMesh: THREE.Object3D | null` with `lastValidStats: GeometricStats | null`, caching only the validated geometric statistics for recovery without retaining disposed Three.js object graphs.

#### [P1-02] **Proven Defect:** Incomplete Collections Workflow (Cannot Add/Remove Models or Navigate from Collections)
- **Location:** `web/src/lib/user-inventory.ts` (line 394), `web/src/layouts/Layout.astro` (lines 586–622), `web/src/pages/generators/[family].astro` (lines 71–80)
- **Evidence:** `toggleModelInCollection(collectionId, modelId)` is implemented and unit-tested in `user-inventory.ts`, but is never imported or invoked anywhere in the UI. Users can create empty collections in `🎒 Inventario -> 🗂️ Colecciones`, yet have no button on generator pages (`[family].astro`) or inside the Inventory modal to add/remove models to a collection. Furthermore, model badges inside a collection render as non-interactive `<span>` tags instead of links to `/generators/{id}`.
- **Recommended Solution:**
  1. Add a `🗂️ COLECCIÓN` selector popover next to `☆ FAVORITO` in `web/src/pages/generators/[family].astro` allowing users to toggle the current model across their collections or create a new collection on the fly.
  2. In `web/src/layouts/Layout.astro`, make collection model badges clickable links (`/generators/{id}`) with a quick remove (`✕`) button and an inline model adder selector per collection.

#### [P1-03] **Proven Defect:** Unescaped HTML Injection (DOM Corruption / XSS Risk) in Dynamic Lists
- **Location:** `web/src/pages/index.astro` (lines 524–576), `web/src/pages/generators/[family].astro` (lines 1228–1249), `web/src/layouts/Layout.astro` (lines 500–620)
- **Evidence:** User-supplied strings (`c.author_name`, `c.content` in comments; `m.name`, `m.author`, `m.description` in community models; `draft.name`, `coll.name`, `coll.description` in inventory) are interpolated directly into `innerHTML` templates without HTML entity escaping. Any `<` or `"` character breaks the layout or executes injected markup.
- **Recommended Solution:** Introduce and apply a strict `escapeHtml()` helper across all dynamic `innerHTML` templates in `Layout.astro`, `index.astro`, and `[family].astro`.

#### [P1-04] **Proven Defect:** AI Generation Missing Network Timeout, Markdown Fence Stripping, Duplicate Submission Lock, and 1-Click Local Fallback UI
- **Location:** `web/src/lib/studio/ai-generator.ts` (lines 129–171) & `web/src/pages/studio.astro` (lines 2530–2595)
- **Evidence:**
  1. `callGeminiAPI` invokes `fetch` without an `AbortSignal.timeout`, risking indefinite UI hang on stalled connections.
  2. `JSON.parse(candidateText)` does not strip optional markdown code fences (````json ... ````) that LLMs occasionally emit even with `responseMimeType: "application/json"`.
  3. `triggerAIGeneration` lacks an in-flight guard (`isGeneratingAI`), so pressing `Enter` in `#ai-prompt-input` or clicking `.ai-chip` while a request is active triggers overlapping generations.
  4. When AI generation fails (missing API key, quota exceeded, or network error), the error banner does not offer a 1-click recovery button to immediately generate with the local procedural engine (`🤖 Usar Motor Procedural Local`).
- **Recommended Solution:** Add a 30-second timeout and markdown fence sanitizer in `callGeminiAPI`, enforce an `isGeneratingAI` lock in `studio.astro`, and provide interactive `[ 🔄 REINTENTAR ]` and `[ 🤖 USAR MOTOR LOCAL ]` recovery buttons directly in `#ai-loading-status`.

---

### P2 — UX, Performance, and Quality Improvements

#### [P2-01] **Proven Defect:** Blocking Native `alert()` Dialogs Disrupting Creative Workflow
- **Location:** `web/src/pages/studio.astro` (lines 2533, 2850, 2900) & `web/src/layouts/Layout.astro` (line 631)
- **Evidence:** Submitting an empty prompt, saving an unnamed draft, or creating an unnamed collection triggers browser-native `alert()` dialogs that freeze the WebGL render loop and break visual immersion.
- **Recommended Solution:** Replace all blocking `alert()` calls with non-blocking HUD toast notifications (`showStudioToast`) and inline input validation/focus.

#### [P2-02] **Proven Defect:** Header Navigation Overflow on Tablet & Mobile Viewports
- **Location:** `web/src/styles/global.css` (lines 164–292)
- **Evidence:** `.header-container` has a fixed `height: 60px` and `.nav-links` has no `flex-wrap` or responsive breakpoint under `960px`, causing the 8 navigation items (`Catálogo`, `Studio 3D`, `Subir Modelo`, `Colaboradores`, `Inventario`, `Motor IA`, `GitHub`, `Acceso`) to overflow horizontally on smaller screens.
- **Recommended Solution:** Add responsive flex wrapping and compact mobile/tablet padding rules in `global.css`.

#### [P2-03] **Improvement Opportunity:** 101 Concurrent `<model-viewer auto-rotate>` Instances on Catalog Page
- **Location:** `web/src/pages/index.astro` (lines 159–169, 444–498)
- **Evidence:** All 101 catalog cards declare `auto-rotate` simultaneously. Even with `loading="lazy"`, once scrolled through, dozens of active WebGL/canvas rotation loops compete for GPU frame time.
- **Recommended Solution:** Attach an `IntersectionObserver` in `index.astro` so `<model-viewer>` instances only enable `auto-rotate` while intersecting the viewport and pause when scrolled off-screen.

#### [P2-04] **Improvement Opportunity:** Unrevoked Blob URLs on Custom GLB Download in Generator Page
- **Location:** `web/src/pages/generators/[family].astro` (lines 931–938, 1042)
- **Evidence:** `URL.createObjectURL(blob)` in `downloadCustomGlbBtn` and `applyTexturesBtn` creates object URLs in memory that are never revoked via `URL.revokeObjectURL`.
- **Recommended Solution:** Track and revoke previous custom GLB object URLs cleanly after download/re-application.

---

### P3 — Aesthetic Polish, Consistency & Accessibility Details

#### [P3-01] **Proven Defect:** Language Inconsistency on Catalog Results Counter & Missing Custom 404 Page
- **Location:** `web/src/pages/index.astro` (line 466) & `web/src/pages/404.astro` (missing)
- **Evidence:** Filtering the catalog updates `#results-count` to `${visible} / ${cards.length} RECORDS` (English) while initial SSR renders `${totalGenerators} MODELOS ENCONTRADOS` (Spanish). Additionally, navigating to an unknown route serves a bare default 404 instead of a branded PS1/PSX recovery screen.
- **Recommended Solution:** Unify the counter text in Spanish (`${visible} DE ${cards.length} MODELOS ENCONTRADOS`) and create `web/src/pages/404.astro` with direct navigation back to the Catalog and Studio 3D.

#### [P3-02] **Improvement Opportunity:** Modal Keyboard Accessibility (`Escape` to Close)
- **Location:** `web/src/layouts/Layout.astro`
- **Evidence:** `#ps1-auth-modal` and `#ps1-inventory-modal` cannot be dismissed with the `Escape` key.
- **Recommended Solution:** Add a global `keydown` listener for `Escape` to close open modals in `Layout.astro`.
