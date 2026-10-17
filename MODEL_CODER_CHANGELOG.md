# MODEL CODER — Professional Polish & Product Completion (`MODEL_CODER_CHANGELOG.md`)

**Date:** 2026-10-17  
**Branch:** `polish/product-completion`

---

## 1. Summary of Changes Implemented

### Phase 1 — Technical & Functional Audit
- Created [`MODEL_CODER_AUDIT.md`](file:///d:/MODELCODER/MODEL_CODER_AUDIT.md) documenting the system architecture, baseline verification, and classified findings across **P0**, **P1**, **P2**, and **P3**, distinguishing proven defects from optimization opportunities.

### Phase 2 & 3 — Visual Polish, Responsive Design & Main User Flow
- **Non-Blocking HUD Feedback (`web/src/pages/studio.astro`, `web/src/layouts/Layout.astro`):**
  - Replaced jarring browser-native `alert()` dialogs (on empty AI prompt, Gemini key save/clear, GLB/ZIP export, and collection creation) with non-blocking HUD toast notifications (`showStudioToast`) and inline input focus/validation.
- **Responsive Header & Keyboard Focus States (`web/src/styles/global.css`):**
  - Added `flex-wrap: wrap` and responsive breakpoints (`@media (max-width: 1080px)` and `@media (max-width: 768px)`) to `.header-container` and `.nav-links` so the 8 navigation items never overflow horizontally on tablet or mobile screens.
  - Added visible `:focus-visible` outlines (`2px solid var(--ps1-cyan)`) for keyboard navigation across buttons and links.
- **Global Modal Keyboard Accessibility (`web/src/layouts/Layout.astro`):**
  - Added `Escape` key listener to cleanly dismiss `#ps1-inventory-modal` and `#ps1-auth-modal`.

### Phase 4 — Feature Completion (AI Fallback, Collections & 404 Recovery)
- **AI Generation Robustness & 1-Click Local Procedural Fallback (`web/src/lib/studio/ai-generator.ts`, `web/src/pages/studio.astro`):**
  - Added a 30-second network timeout (`AbortSignal.timeout(30000)`) in `AIGenerator.callGeminiAPI` with a clear Spanish error message on timeout.
  - Added automatic markdown code fence stripping (` ```json ... ``` `) before `JSON.parse` in `callGeminiAPI`.
  - Added an `isGeneratingAI` concurrency lock in `triggerAIGeneration` to prevent duplicate overlapping requests when pressing `Enter` or clicking prompt chips rapidly.
  - Added interactive recovery buttons (`🔄 REINTENTAR` and `🤖 GENERAR CON MOTOR PROCEDURAL LOCAL`) inside `#ai-loading-status` whenever AI generation fails, allowing 1-click fallback to the local procedural engine without losing the user's prompt.
- **Complete End-to-End Collections Workflow (`web/src/pages/generators/[family].astro`, `web/src/layouts/Layout.astro`, `web/src/lib/user-inventory.ts`):**
  - Added a `🗂️ COLECCIÓN` button and interactive popover next to `☆ FAVORITO` on every generator page (`[family].astro`), allowing users to toggle the active 3D model into any of their collections or create a new collection on the fly.
  - Updated `renderInvCollections` in `Layout.astro` so model tags (`#crate`, `#arcade_cabinet`, etc.) are clickable links to `/generators/{id}`, include an inline `✕` remove button (`toggleModelInCollection`), and provide an inline quick-add input per collection.
- **Custom 404 Recovery Page (`web/src/pages/404.astro`):**
  - Created a branded PS1/PSX 404 error page (`[ 404 // COORDENADA INEXISTENTE ]`) with direct navigation back to the 3D Catalog and Studio 3D.

### Phase 5 — Performance, Memory Management & Export Integrity
- **Lossless PBR Material Preservation on GLB Export (`web/src/lib/studio/three-viewport.ts`, `web/src/pages/studio.astro`):**
  - Fixed a P0 defect where exporting a `.glb` (or publishing to the community) while inspecting the model in `wireframe`, `normals`, `vertex_colors`, or `unlit` mode exported the temporary debug materials instead of the model's PBR materials and textures.
  - Added `StudioViewport.executeWithOriginalMaterials()` to temporarily restore original PBR materials during GLB serialization and restore the active inspection shading mode afterward.
- **Three.js Memory & Material Disposal Fixes (`web/src/lib/studio/three-viewport.ts`):**
  - Replaced `this.lastValidMesh = obj.clone()` (which retained dangling references to disposed `BufferGeometry` and `Material` instances after subsequent generations) with `this.lastValidStats: GeometricStats | null`.
  - Added `restoreOriginalMaterialsOnCurrentMesh()` to dispose temporary shading materials when switching shading modes and ensure original PBR materials/textures are properly disposed when replacing or destroying `currentMesh`.
- **Catalog `<model-viewer>` Viewport Culling (`web/src/pages/index.astro`):**
  - Added an `IntersectionObserver` (`viewerObserver`) that pauses `auto-rotate` on off-screen `<model-viewer>` cards and resumes rotation only when cards enter the viewport, reducing GPU/CPU contention across the 101+ catalog models.
- **Blob URL Cleanup (`web/src/pages/generators/[family].astro`, `web/src/pages/studio.astro`):**
  - Added `URL.revokeObjectURL` cleanup after custom `.glb` and `.zip` downloads and worker preview updates.

### Phase 6 — Security, Language Consistency & Regression Tests
- **XSS / DOM Injection Protection (`web/src/layouts/Layout.astro`, `web/src/pages/index.astro`, `web/src/pages/generators/[family].astro`):**
  - Added `escapeHtml()` sanitization across all dynamic `innerHTML` templates rendering user-supplied strings (community models, comments, drafts, favorites, and collections).
- **Spanish UI Consistency (`web/src/pages/index.astro`):**
  - Unified the catalog filter counter from `${visible} / ${cards.length} RECORDS` to `${visible} DE ${cards.length} MODELOS ENCONTRADOS`.
- **Automated Regression Tests (`web/tests/user_inventory.test.ts`):**
  - Added regression tests covering polymorphic `saveProjectDraft(spec, thumbnail, existingId)` and `saveCollection` initialization with `model_ids`.

### Phase 7 — Massive & Storage-Efficient PBR Texture Library Expansion (`MODEL_CODER_TEXTURE_LIBRARY.md`)
- **138 Ready-to-Use PBR Materials Across 8 Families (`web/src/lib/studio/texture-library.ts`, `web/src/lib/studio/types.ts`):**
  - Expanded `TextureLibrary` from 18 presets to **118 canonical procedural PBR base textures + 20 curated parametric variants (138 total materials)** across 8 complete material families: `metals` (29), `construction` (19), `woods` (12), `stones` (14), `plastics` (14), `tech` (22), `glass` (11), and `fabrics_organic` (17).
  - Added automatic tangent-space **Normal Map** generation (`TextureLibrary.getNormalTexture`) via wrapped Sobel gradient filtering and parametric surface weathering (`TextureLibrary.applyParametricWear`), while keeping **0 bytes** of external image files in `web/public/` and adding only **+7.29 KB gzipped** (`~53 bytes/material`) to the Studio JS bundle.
- **Interactive Visual Material Browser & Parametric Controls (`web/src/pages/studio.astro`, `web/src/lib/studio/procedural-engine.ts`):**
  - Upgraded the Studio Material Inspector with a searchable, category-filtered visual **Material Browser** displaying lazily generated `48×48` WebP thumbnails (`TextureLibrary.getThumbnailDataURL`) and PBR capability badges (`NORM`, `METAL`, `EMISSIVE`, `ALPHA`, `VAR`).
  - Added non-destructive vertex UV rotation (`comp.uvRotation` via `ProceduralEngine.applyUVRotation`), procedural wear/grime intensity (`comp.wear`), and normal relief intensity (`comp.normalStrength`).
- **Fast, Compact GLB Export with NormalMap Stashing (`web/src/lib/studio/glb-exporter.ts`):**
  - Fixed `GLBExporterService.exportSpec` to use `ProceduralEngine.buildModelFromSpec` and updated `exportToArrayBuffer` to temporarily stash `DataTexture` normal/roughness maps during `GLTFExporter.parse` and restore them immediately afterward, avoiding `GLTFExporter` `DataTexture` incompatibilities and keeping exported `.glb` files compact.

