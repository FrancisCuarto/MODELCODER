# ModelCoder 3D Studio - Native Desktop App 🚀

Aplicación de escritorio nativa para **ModelCoder 3D Studio**, construida con **Tauri v2** y **Rust**.

---

## 🎯 Por qué una versión de escritorio

1. **Texturas Locales sin límites de cuota**:
   - En navegadores web, el almacenamiento de texturas pesadas o colecciones grandes está restringido por cuotas de `localStorage` o `IndexedDB` (~50-100MB máx).
   - En la versión de escritorio, las texturas personalizadas se guardan directamente en el disco duro del usuario:
     `Documentos/ModelCoder/Textures/`.
   - Carga instantánea a velocidad de bus NVMe/SSD sin depender de la nube.

2. **Rendimiento Acelerado por Hardware**:
   - Corre sobre el motor **WebView2** nativo de Windows (o WebKit en macOS/Linux), consumiendo menos de ~50 MB de RAM (a diferencia de Electron que consume 300MB+).
   - Renderizado Three.js con WebGL 2.0 y aceleración directa por GPU.

3. **Exportación Directa a Motores (Godot / Unity / Unreal)**:
   - Permite guardar los modelos `.gltf`, `.obj` y escenas `.tscn` (con sus mallas de colisión calculadas) directamente dentro de la carpeta de assets de tu proyecto de Godot sin tener que pasar por el diálogo de descargas del navegador ni descomprimir zips.

---

## 🛡️ Principio de Aislamiento Web

La carpeta `web/` permanece **100% independiente e intocada**.
- La versión web desplegada en Vercel sigue funcionando tal cual sin dependencias de Rust ni Tauri.
- La versión de escritorio simplemente toma el artefacto estático compilado en `web/dist/` y lo envuelve en la ventana nativa de Tauri.

---

## 🛠️ Cómo Generar el Instalador (.exe / .msi)

### Opción A: Compilación Automática en la Nube (GitHub Actions) ⭐ RECOMENDADA
No necesitas tener Rust ni Visual Studio C++ instalados en tu computadora local:
1. Ve a la pestaña **Actions** en tu repositorio de GitHub: `https://github.com/FrancisCuarto/MODELCODER/actions`
2. Selecciona **Build & Release Desktop App**.
3. Haz clic en **Run workflow**.
4. GitHub Actions compilará en una máquina virtual de Windows limpia y publicará el archivo `.exe` y `.msi` para descargar directamente.

O simplemente crea un tag de versión:
```bash
git tag v2.5.0
git push origin v2.5.0
```

### Opción B: Compilación Local (Windows)
Si deseas compilar o probar en modo desarrollador localmente:
1. Instala Rust (si aún no lo tienes):
   ```powershell
   winget install Rustlang.Rustup
   ```
2. Instala dependencias y arranca el entorno:
   ```powershell
   cd desktop
   npm install
   npm run dev
   ```
3. Para compilar el `.exe` final:
   ```powershell
   npm run build
   ```
   El instalador se generará en `desktop/src-tauri/target/release/bundle/nsis/`.
