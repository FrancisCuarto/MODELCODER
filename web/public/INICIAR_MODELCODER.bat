@echo off
chcp 65001 > nul
title ModelCoder 3D - Servidor Worker Local
cls

echo ===================================================================
echo     __  __  ____  _____  ______ _      _____ ____  _____  ______ _____  
echo    ^|  \/  ^|/ __ \^|  __ \^|  ____^| ^|    / ____/ __ \^|  __ \^|  ____^|  __ \ 
echo    ^| \  / ^| ^|  ^| ^| ^|  ^| ^| ^|__  ^| ^|   ^| ^|   ^| ^|  ^| ^| ^|  ^| ^| ^|__  ^| ^|__) ^|
echo    ^| ^|\/^| ^| ^|  ^| ^| ^|  ^| ^|  __^| ^| ^|   ^| ^|   ^| ^|  ^| ^| ^|  ^| ^|  __^| ^|  _  / 
echo    ^| ^|  ^| ^| ^|__^| ^| ^|__^| ^| ^|____^| ^|___^| ^|___^| ^|__^| ^| ^|__^| ^| ^|____^| ^| \ \ 
echo    ^|_^|  ^|_^|\____/^|_____/^|______^|______\_____\____/^|_____/^|______^|_^|  \_\
echo                    3D GENERATOR WORKER (LOCAL LANZADOR)
echo ===================================================================
echo.
echo [*] Verificando entorno de ejecucion...

:: 1. Detectar Python
set PYTHON_BIN=""
where python >nul 2>&1 && (
    for /f "tokens=*" %%i in ('where python') do (
        if not defined PYTHON_BIN set PYTHON_BIN="%%i"
    )
)

if %PYTHON_BIN%=="" (
    if exist "C:\Users\%USERNAME%\.local\bin\python3.11.exe" (
        set PYTHON_BIN="C:\Users\%USERNAME%\.local\bin\python3.11.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set PYTHON_BIN="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    ) else if exist "%PROGRAMFILES%\Python311\python.exe" (
        set PYTHON_BIN="%PROGRAMFILES%\Python311\python.exe"
    ) else (
        where py >nul 2>&1 && set PYTHON_BIN="py -3"
    )
)

if %PYTHON_BIN%=="" (
    echo [ERROR] No se encontro Python en el sistema.
    echo Por favor instala Python 3.10+ desde https://www.python.org/downloads/
    echo Asegurate de marcar la casilla "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo [OK] Python detectado: %PYTHON_BIN%

:: 2. Detectar Blender
set BLENDER_FOUND=0
if exist "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" (
    set BLENDER_FOUND=1
    echo [OK] Blender 5.0 detectado en Program Files.
) else if exist "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe" (
    set BLENDER_FOUND=1
    echo [OK] Blender 4.3 detectado en Program Files.
) else if exist "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" (
    set BLENDER_FOUND=1
    echo [OK] Blender 4.2 detectado en Program Files.
) else (
    where blender >nul 2>&1 && (
        set BLENDER_FOUND=1
        echo [OK] Blender detectado en el PATH del sistema.
    )
)

if %BLENDER_FOUND%==0 (
    echo [AVISO] No se detecto Blender instalado en las rutas estandar.
    echo El visor web funcionara en modo cliente (vistas previas y dimensiones).
    echo Para compilar mallas nuevas personalizadas, instala Blender desde:
    echo https://www.blender.org/download/
    echo.
)

:: 3. Instalar dependencias necesarias para el worker
echo [*] Comprobando librerias del worker (fastapi, uvicorn)...
%PYTHON_BIN% -m pip install -q fastapi uvicorn pydantic >nul 2>&1

:: 4. Iniciar navegador y servidor
echo.
echo ===================================================================
echo  [LISTO] Servidor Worker iniciando en: http://localhost:8000
echo  Abriendo ModelCoder en tu navegador predeterminado...
echo  (Manten esta ventana abierta mientras uses la pagina)
echo ===================================================================
echo.

:: Abrir navegador web
start https://modelcoder.vercel.app/

:: Ejecutar servidor worker
%PYTHON_BIN% server/main.py --port 8000

pause
