#!/usr/bin/env bash
set -e

echo "======================================================="
echo "   ModelCoder DevContainer: Setup Automatico Cloud"
echo "======================================================="

# 1. Dependencias de Python
echo "[*] Instalando dependencias de Python y servidor worker..."
pip install --no-cache-dir -r server/requirements.txt

# 2. Dependencias de Node.js / Astro
echo "[*] Instalando dependencias de la web (Astro)..."
cd web && npm install --silent && cd ..

# 3. Permisos de ejecucion
chmod +x tools/*.py || true

echo "======================================================="
echo "   [LISTO] Entorno configurado al 100%"
echo "   - Para iniciar el worker: python server/main.py --port 8000"
echo "   - Para iniciar la web:    cd web && npm run dev"
echo "======================================================="
