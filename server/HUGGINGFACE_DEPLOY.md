# Despliegue del Worker Gratuito 24/7 en Hugging Face Spaces

Hugging Face ofrece **contenedores Docker gratuitos permanentes (2 vCPUs, 16 GB de RAM)** ideales para ejecutar Blender en la nube sin costo alguno.

---

### Pasos para Activar el Servidor en 2 Clics:

1. **Crear el Space en Hugging Face:**
   - Entra a [huggingface.co/new-space](https://huggingface.co/new-space).
   - Asigna un nombre: `modelcoder-worker`.
   - Selecciona **License:** MIT.
   - En **Space SDK:** Elige **Docker** -> **Blank**.
   - En **Space Hardware:** Deja el predeterminado **CPU Basic (Gratis · 2 vCPU · 16 GB RAM)**.
   - Haz clic en **Create Space**.

2. **Subir los Archivos o Conectar con GitHub:**
   - En tu nuevo Space, ve a la pestaña **Files** o conecta el repositorio de GitHub.
   - Copia el archivo `server/Dockerfile.hf` como el `Dockerfile` raíz del Space.
   - Copia los archivos del proyecto (`server/`, `procedural_assets/`, `generators/`).

3. **Obtener tu URL del Worker:**
   - Una vez que Hugging Face termine de compilar (tarda ~2 minutos), verás el estado en verde **Running**.
   - Tu URL pública será:
     `https://<tu-usuario>-modelcoder-worker.hf.space/api/generate`

4. **Conectarlo a la Web:**
   - En la web de ModelCoder ([modelcoder.vercel.app](https://modelcoder.vercel.app)), abre cualquier modelo.
   - Haz clic en **[ CONFIGURAR WORKER ]**.
   - Pega tu URL de Hugging Face y haz clic en **[ GUARDAR Y CONECTAR ]**.
   - ¡Listo! Ahora todos tus visitantes podrán generar mallas con Blender real en la nube sin costo.
