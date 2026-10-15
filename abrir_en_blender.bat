@echo off
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"

if not exist "%BLENDER%" (
    echo [ERROR] No se encontro Blender 5.0 en %BLENDER%
    pause
    exit /b
)

echo [INICIANDO] Abriendo Blender con el Generador PSX interactivo...
start "" "%BLENDER%" --python "%~dp0blender_addon.py"
