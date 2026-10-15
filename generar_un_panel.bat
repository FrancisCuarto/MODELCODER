@echo off
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"

if not exist "%BLENDER%" (
    echo [ERROR] No se encontro Blender en %BLENDER%
    pause
    exit /b
)

echo ======================================================
echo    GENERADOR PROCEDURAL PSX - BELOW NOMINAL
echo ======================================================
echo Generando un nuevo panel electrico en output/...
echo.

"%BLENDER%" -b --python generate.py -- --seed %RANDOM% --name "panel_generado_%RANDOM%" --save-blend

echo.
echo [COMPLETADO] El modelo se genero con exito en la carpeta 'output'.
echo Contiene:
echo   - Archivo .glb (arrastralo a Godot 4)
echo   - Archivo .json (parametros tecnicos)
echo   - Archivo .blend (para abrirlo y editarlo en Blender)
echo.
pause
