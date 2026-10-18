# Propuestas Iniciales de Publicación — ModelCoder Instagram (`@modelcoder`)

---

## Propuesta 1 — Reel de Lanzamiento & Demostración de Producto
* **Pilar:** A. Generadores y resultados (35%)
* **Formato:** Video vertical 9:16 (Reel)
* **Duración orientativa:** 15 segundos
* **Objetivo:** Dar a conocer qué es ModelCoder en menos de 15 segundos mostrando el flujo real de personalización y descarga.

### Estructura y Guion del Video:
1. **0–2 s (Gancho visual):** Primer plano de un modelo 3D low-poly rotando en pantalla (*Carro de Paro Médico* o *Mesa Quirúrgica*).  
   *Texto en pantalla:* "¿Necesitás modelos 3D para tu videojuego sin modelar desde cero?"
2. **2–8 s (Demostración interactiva):** El cursor mueve un slider de altura y activa cajones abiertos en `/generators/crash_cart`. El modelo se transforma en tiempo real con estética PS1.  
   *Texto en pantalla:* "Elegí parámetros, variá formas y colores al instante."
3. **8–12 s (Exportación y motor):** Clic en `[BAJAR .GLB]`. En una fracción de segundo, se muestra el archivo arrastrándose a Godot 4 (o Blender), con sus colisiones listas.  
   *Texto en pantalla:* "Descarga directa en .GLB lista para Godot o Unity."
4. **12–15 s (Cierre y llamada a la acción):** Pantalla final con el logo de ModelCoder y la URL.  
   *Texto en pantalla:* "Probá el catálogo gratis en modelcoder.vercel.app"

### Copy propuesto (Caption):
> ¿Y si pudieras generar y personalizar objetos 3D low-poly para tu juego en segundos? 🎮👾
>
> ModelCoder es una herramienta procedural abierta pensada para desarrolladores de videojuegos. En lugar de modelar cada variante a mano, ajustás parámetros reales (medidas, paletas de color y accesorios) y descargás tu modelo en formato **.GLB** listo para importar en Godot 4, Unity o Blender.
>
> 📦 Hay más de 100 modelos disponibles en el catálogo web: mobiliario, dispositivos, computadoras, mamparos y equipo médico.
>
> 🔗 Link en bio para probarlo gratis desde el navegador: `modelcoder.vercel.app`
>
> ¿Qué objeto te gustaría ver en la próxima demo? Te leemos en comentarios 👇
>
> `#gamedev #indiedev #godotengine #lowpoly #psxrender #blender3d #3dmodeling #madewithgodot`

### Assets necesarios:
- Grabación de pantalla limpia (1080x1920) del visor interactivo en `https://modelcoder.vercel.app/generators/crash_cart`.
- Clip corto (3 segundos) arrastrando el GLB generado a una escena 3D en Godot 4.
- Logo en alta resolución (`web/public/logo.png`).

---

## Propuesta 2 — Carrusel Educativo: "¿Qué es un modelo procedural?"
* **Pilar:** C. Educación y desarrollo de videojuegos (15%)
* **Formato:** Carrusel de imágenes (4 a 5 slides cuadradas / 4:5 verticales)
* **Objetivo:** Explicar el concepto de generación procedural a principiantes y posicionar a ModelCoder como una solución práctica.

### Estructura de Slides:
* **Slide 1 (Portada):**  
  *Título:* "¿Qué significa que un modelo 3D sea PROCEDURAL? (Y cómo te ahorra horas de trabajo en tu juego)"  
  *Visual:* Comparación visual de tres variaciones del mismo objeto sobre fondo oscuro retro-tech.
* **Slide 2 (El problema):**  
  *Texto:* "El modelado tradicional exige crear cada mesa, taquilla o consola una por una. Si necesitás 10 variantes para un nivel, modelás 10 veces."  
  *Visual:* Silueta esquemática de trabajo repetitivo.
* **Slide 3 (La solución procedural):**  
  *Texto:* "Un generador procedural define **reglas matemáticas y parámetros**: altura, divisiones, cajones o desgaste. El código construye la malla automáticamente."  
  *Visual:* Captura de los sliders de ModelCoder alterando un modelo.
* **Slide 4 (El resultado):**  
  *Texto:* "Mismo generador, infinitas posibilidades. Podés poblar toda una estación espacial con piezas coherentes que comparten un solo atlas de textura retro de 256×256."  
  *Visual:* 4 variantes del mismo generador colocadas juntas en una escena.
* **Slide 5 (Cierre / CTA):**  
  *Texto:* "Descubrí los 103 generadores disponibles en ModelCoder. Gratis y en tu navegador. Guardá este post para cuando diseñes tus escenarios."  
  *Visual:* Isotipo ModelCoder + Icono de Guardar y Compartir.

### Copy propuesto (Caption):
> Crear escenarios para tu juego no tiene por qué significar modelar cada objeto desde cero 💡
>
> La generación procedural permite que una sola pieza de código cree decenas de variaciones de un mismo prop ajustando medidas, accesorios o nivel de óxido.
>
> En ModelCoder aplicamos esta lógica con estética retro PS1: mallas livianas, texturas optimizadas y exportación estándar en .GLB para que tu juego corra fluido en cualquier plataforma.
>
> Deslizá el carrusel para ver la diferencia y guardá el post si estás armando el arte de tu próximo prototipo 📌
>
> `#indiegamedev #desarrollodevideojuegos #3dlowpoly #godot4 #blendercommunity #procedural3d`

### Assets necesarios:
- 4 capturas de pantalla de alta fidelidad tomadas desde `/generators/bunk_bed` o `/generators/terminal` mostrando distintas semillas y paletas.
- Gráficos o marcos con tipografía retro y los colores de la marca.

---

## Propuesta 3 — Reel de Funcionalidad: "Creando props con IA en el navegador"
* **Pilar:** B. Tutoriales y demostraciones (25%)
* **Formato:** Video vertical 9:16 (Reel)
* **Duración orientativa:** 18 segundos
* **Objetivo:** Demostrar la capacidad del Studio 3D web de ModelCoder y su integración con Gemini 3.8 Flash para crear piezas en tiempo real.

### Estructura y Guion del Video:
1. **0–3 s (Gancho):** Vista de la interfaz del Studio 3D de ModelCoder.  
   *Texto en pantalla:* "¿Podés diseñar modelos 3D procedurales describiéndolos con texto?"
2. **3–8 s (Acción):** En la pestaña `[⚡ MODO IA]`, se escribe un prompt simple (ej. *"Caja de suministros blindada con franjas de peligro y manijas laterales"*). Clic en generar.
3. **8–13 s (Resultado inmediato):** En segundos, el árbol de piezas del Studio se puebla (`crate_hull`, `reinforced_band`, etc.) y el viewport Three.js muestra el modelo 3D completamente renderizado en sombreado PSX.
4. **13–18 s (Ajuste y exportación):** El usuario ajusta un gizmo de rotación, cambia el preset de textura a `hazard_stripes` y hace clic en `[💾 EXPORTAR GLB]`.  
   *Texto en pantalla:* "Sin instalar programas. Directo desde tu navegador a tu juego."

### Copy propuesto (Caption):
> ¿Generar modelos 3D procedurales directamente desde el navegador? ⚡
>
> En el Studio 3D de ModelCoder podés combinar tres formas de trabajo:
> 1. Describir lo que necesitás con lenguaje natural gracias al motor asistido por IA (Gemini 3.8 Flash).
> 2. Editar cada pieza visualmente con gizmos, primitivas y presets de textura industrial.
> 3. O modificar el código procedural Python directamente si preferís control absoluto.
>
> Al terminar, descargás el archivo .GLB con un clic y lo llevás a tu motor.
>
> 🚀 Entrá a `modelcoder.vercel.app/studio` y probalo gratis hoy mismo.
>
> ¿Qué tipo de prop te gustaría que creemos en vivo en el próximo video?
>
> `#generativeai #gamedev #threejs #indiedev #blender3d #godotengine #lowpoly3d`

### Assets necesarios:
- Video capturado de la pestaña abierta de `https://modelcoder.vercel.app/studio` mostrando la interacción con el Modelo IA y los gizmos 3D.
