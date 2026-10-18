import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { MODULAR_MODELS_LOTE_1 } from '../src/data/modular-catalog.ts';
import { GLBExporterService } from '../src/lib/studio/glb-exporter.ts';
import { ProceduralEngine } from '../src/lib/studio/procedural-engine.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  const outputDir = path.resolve(__dirname, '../public/models/modular');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`📁 Directorio creado: ${outputDir}`);
  }

  console.log(`🚀 Iniciando horneado de ${MODULAR_MODELS_LOTE_1.length} modelos modulares (Lote 1)...`);
  let successCount = 0;

  for (const entry of MODULAR_MODELS_LOTE_1) {
    const filename = `${entry.family}.glb`;
    const outputPath = path.join(outputDir, filename);

    const { group, stats } = ProceduralEngine.buildModelFromSpec(entry.spec);
    try {
      const buffer = await GLBExporterService.exportSpec(entry.spec);
      fs.writeFileSync(outputPath, Buffer.from(buffer));
      const sizeKb = (buffer.byteLength / 1024).toFixed(1);
      console.log(`  ✅ [${entry.batchName}] ${entry.name} -> ${filename} (${stats.triangles} tris, ${stats.partsCount} piezas, ${sizeKb} KB)`);
      successCount++;
    } catch (err: any) {
      console.error(`  ❌ Error horneando ${entry.family}:`, err.message);
    } finally {
      ProceduralEngine.disposeHierarchy(group);
    }
  }

  console.log(`\n🎉 Horneado finalizado con éxito: ${successCount}/${MODULAR_MODELS_LOTE_1.length} modelos generados en ${outputDir}`);
}

main().catch((err) => {
  console.error('Fatal error baking modular models:', err);
  process.exit(1);
});
