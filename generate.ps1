# PowerShell wrapper to run asset generation with Blender
$BlenderPath = if (Get-Command blender -ErrorAction SilentlyContinue) {
    (Get-Command blender).Source
} elseif (Test-Path "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe") {
    "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
} else {
    throw "Blender executable not found. Please install Blender or add it to PATH."
}

& $BlenderPath -b --python generate.py -- $args
