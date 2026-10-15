## Resumen del Generador / Contribution Summary

- **Nombre del Generador**: [ej. Generador de Consola Médica]
- **Familia (`family`)**: [ej. `medical_terminal`]
- **Categoría**: [ ] furniture  [ ] medical  [ ] fixtures  [ ] architecture  [ ] infrastructure  [ ] props
- **Autor / GitHub**: [@usuario]
- **Licencia**: [ ] CC-BY-4.0  [ ] MIT  [ ] CC0-1.0

---

## Checklist de Verificación Comunitaria

- [ ] Incluye `manifest.json` válido conforme a `schemas/generator-v1.json`.
- [ ] Implementa `config.py` y `generator.py` heredando de `BaseAssetGenerator`.
- [ ] Registrado en `procedural_assets/generators/__init__.py`.
- [ ] Respeta el presupuesto de triángulos (PSX low-poly: < 1200 tris).
- [ ] Pasa la auditoría de seguridad AST local:
  ```bash
  blender -b --python tools/verify_community_generator.py -- mi_familia
  ```
- [ ] Ejecutada la suite completa de pruebas unitarias (`blender -b --python run_tests.py`).
- [ ] Sincronizado el catálogo web (`npm run build` en `web/` sin errores).
