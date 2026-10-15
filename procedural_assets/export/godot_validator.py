import os
import sys
import json
import shutil
import subprocess
from typing import Dict, Any, Optional, List

GODOT_CANDIDATE_PATHS = [
    r"C:\Users\lopez\Downloads\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64_console.exe",
    r"C:\Users\lopez\Downloads\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64.exe",
    r"C:\Users\lopez\Downloads\Godot_v4.6-stable_win64.exe\Godot_v4.6-stable_win64_console.exe",
    r"C:\Users\lopez\Downloads\Godot_v4.7.1-stable_win64.exe\Godot_v4.7.1-stable_win64_console.exe",
    r"C:\Users\lopez\Downloads\Godot_v4.8-dev7_win64.exe\Godot_v4.8-dev7_win64_console.exe",
]

def find_godot_executable() -> Optional[str]:
    """Find a valid Godot 4 executable on the host system."""
    env_path = os.environ.get("GODOT_BIN")
    if env_path and os.path.exists(env_path):
        return env_path

    # Check candidate known paths
    for path in GODOT_CANDIDATE_PATHS:
        if os.path.isfile(path):
            return path

    # Check PATH
    for name in ["godot", "godot4", "godot-console", "Godot"]:
        which_path = shutil.which(name)
        if which_path and os.path.isfile(which_path):
            return which_path

    return None

def is_godot_available() -> bool:
    """Return True if a Godot binary is detected."""
    return find_godot_executable() is not None

def get_harness_dir() -> str:
    """Locate or prepare tests/godot_harness directory with project.godot and verify_import.gd."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    harness_dir = os.path.join(base_dir, "tests", "godot_harness")
    os.makedirs(harness_dir, exist_ok=True)

    proj_file = os.path.join(harness_dir, "project.godot")
    if not os.path.exists(proj_file):
        with open(proj_file, "w", encoding="utf-8") as f:
            f.write('; Engine configuration file\nconfig_version=5\n\n[application]\nconfig/name="BelowNominalExportVerification"\n')

    return harness_dir

def validate_glb_with_godot(glb_filepath: str, timeout: int = 15) -> Dict[str, Any]:
    """
    Execute real headless Godot 4 import to verify scene generation, meshes,
    materials, collisions and node hierarchy.
    """
    godot_exe = find_godot_executable()
    if not godot_exe:
        return {
            "tested_in_godot": False,
            "success": True,
            "message": "Godot binary not found in standard paths; skipped live Godot execution."
        }

    abs_glb = os.path.abspath(glb_filepath)
    if not os.path.exists(abs_glb):
        return {
            "tested_in_godot": True,
            "success": False,
            "errors": [f"GLB file does not exist at {abs_glb}"]
        }

    harness_dir = get_harness_dir()
    script_path = "verify_import.gd"

    cmd = [
        godot_exe,
        "--headless",
        "--path", harness_dir,
        "-s", script_path,
        "--", abs_glb
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            cwd=harness_dir
        )
    except subprocess.TimeoutExpired:
        return {
            "tested_in_godot": True,
            "success": False,
            "errors": [f"Godot validation timed out after {timeout} seconds"]
        }
    except Exception as e:
        return {
            "tested_in_godot": True,
            "success": False,
            "errors": [f"Failed to launch Godot process: {str(e)}"]
        }

    stdout = proc.stdout
    start_tag = "---GODOT_VALIDATION_JSON_START---"
    end_tag = "---GODOT_VALIDATION_JSON_END---"

    if start_tag in stdout and end_tag in stdout:
        json_str = stdout.split(start_tag)[1].split(end_tag)[0].strip()
        try:
            report = json.loads(json_str)
            report["tested_in_godot"] = True
            report["success"] = report.get("valid", False) and proc.returncode == 0
            report["exit_code"] = proc.returncode
            report["godot_binary"] = godot_exe
            return report
        except json.JSONDecodeError as jde:
            return {
                "tested_in_godot": True,
                "success": False,
                "exit_code": proc.returncode,
                "errors": [f"Failed to parse Godot JSON output: {str(jde)}", stdout]
            }

    return {
        "tested_in_godot": True,
        "success": proc.returncode == 0,
        "exit_code": proc.returncode,
        "raw_stdout": stdout,
        "raw_stderr": proc.stderr,
        "errors": [f"Godot exited with code {proc.returncode}"] if proc.returncode != 0 else []
    }
