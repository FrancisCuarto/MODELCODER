"""
ModelCoder High-Performance On-Demand 3D Generation Server.
Exposes a REST API with parameter validation, SHA256 caching,
and sandbox Blender 5.0 execution for real-time in-browser 3D asset generation.
Supports both FastAPI/Uvicorn and standard library HTTP server fallback.
"""

import os
import sys
import json
import time
import uuid
import hashlib
import shutil
import subprocess
from typing import Dict, Any, Optional

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.core import find_manifest_for_family, discover_all_manifests
from procedural_assets.generators import GENERATOR_REGISTRY

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SERVER_DIR, "cache")
TMP_DIR = os.path.join(SERVER_DIR, "tmp")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

BLENDER_EXE = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
if not os.path.isfile(BLENDER_EXE):
    BLENDER_EXE = "blender"

def compute_cache_key(family: str, params: Dict[str, Any], preset: Optional[str] = None) -> str:
    """Generate deterministic SHA256 key for a family + parameter combination."""
    canonical = {
        "family": family,
        "preset": preset or "",
        "parameters": {k: params[k] for k in sorted(params.keys())}
    }
    raw = json.dumps(canonical, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def execute_generation(family: str, params: Dict[str, Any], preset: Optional[str] = None) -> bytes:
    """Execute generator in isolated sandbox and return GLB binary data."""
    if family not in GENERATOR_REGISTRY:
        raise ValueError(f"Unknown generator family: '{family}'")

    manifest = find_manifest_for_family(family)
    if manifest:
        is_valid, errors = manifest.validate_parameters(params)
        if not is_valid:
            raise ValueError(f"Invalid parameters for {family}: {'; '.join(errors)}")

    cache_key = compute_cache_key(family, params, preset)
    cached_glb_path = os.path.join(CACHE_DIR, f"{cache_key}.glb")

    # Check cache hit
    if os.path.isfile(cached_glb_path):
        with open(cached_glb_path, "rb") as f:
            return f.read(), True

    # Sandbox execution
    req_id = str(uuid.uuid4())[:8]
    work_dir = os.path.join(TMP_DIR, req_id)
    os.makedirs(work_dir, exist_ok=True)

    try:
        generate_script = os.path.join(current_dir, "generate.py")
        cmd = [
            BLENDER_EXE, "-b", "--python", generate_script,
            "--", "--family", family, "--output-dir", work_dir,
            "--name", f"gen_{family}_{req_id}", "--collision"
        ]

        if preset:
            cmd.extend(["--preset", preset])

        for k, v in params.items():
            flag = f"--{k.replace('_', '-')}"
            if isinstance(v, bool):
                if v:
                    cmd.append(flag)
                else:
                    cmd.append(f"--no-{k.replace('_', '-')}")
            elif v is not None:
                cmd.extend([flag, str(v)])

        res = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True, timeout=20)
        if res.returncode != 0:
            err_msg = res.stderr[-500:] if res.stderr else res.stdout[-500:]
            raise RuntimeError(f"Blender generation failed (code {res.returncode}): {err_msg}")

        # Locate output GLB
        target_glb = None
        for fname in os.listdir(work_dir):
            if fname.endswith(".glb"):
                target_glb = os.path.join(work_dir, fname)
                break

        if not target_glb or not os.path.isfile(target_glb):
            raise RuntimeError("Blender completed but no GLB file was produced.")

        # Read and save to persistent cache
        with open(target_glb, "rb") as f:
            glb_data = f.read()

        shutil.copy2(target_glb, cached_glb_path)
        return glb_data, False

    finally:
        # Cleanup temp directory
        if os.path.isdir(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)

# ==============================================================================
# FASTAPI APPLICATION (When fastapi & uvicorn are available)
# ==============================================================================
try:
    from fastapi import FastAPI, HTTPException, Response, Request
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="ModelCoder 3D Generation API",
        version="1.0.0",
        description="On-demand procedural 3D model generation microservice"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class GenerateRequest(BaseModel):
        family: str
        parameters: Dict[str, Any] = {}
        preset: Optional[str] = None

    @app.get("/api/health")
    def health_check():
        cached_count = len([f for f in os.listdir(CACHE_DIR) if f.endswith(".glb")])
        return {
            "status": "healthy",
            "blender_path": BLENDER_EXE,
            "cached_models": cached_count,
            "families_available": len(GENERATOR_REGISTRY)
        }

    @app.get("/api/generators")
    def list_generators():
        manifests = discover_all_manifests()
        return {k: m.to_dict() for k, m in manifests.items()}

    @app.post("/api/generate")
    def generate_model(req: GenerateRequest):
        try:
            glb_bytes, is_cached = execute_generation(req.family, req.parameters, req.preset)
            headers = {
                "Content-Disposition": f'attachment; filename="{req.family}_custom.glb"',
                "X-Cache": "HIT" if is_cached else "MISS",
                "Access-Control-Expose-Headers": "X-Cache"
            }
            return Response(content=glb_bytes, media_type="model/gltf-binary", headers=headers)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

except ImportError:
    app = None

# ==============================================================================
# STANDALONE HTTP SERVER FALLBACK (Zero external dependencies)
# ==============================================================================
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class StandaloneHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Expose-Headers", "X-Cache")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            cached_count = len([f for f in os.listdir(CACHE_DIR) if f.endswith(".glb")])
            data = {
                "status": "healthy",
                "blender_path": BLENDER_EXE,
                "cached_models": cached_count,
                "families_available": len(GENERATOR_REGISTRY)
            }
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/api/generators":
            manifests = discover_all_manifests()
            data = {k: m.to_dict() for k, m in manifests.items()}
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            try:
                data = json.loads(raw_body.decode("utf-8"))
                family = data.get("family", "")
                params = data.get("parameters", {})
                preset = data.get("preset")

                glb_bytes, is_cached = execute_generation(family, params, preset)

                self.send_response(200)
                self.send_header("Content-Type", "model/gltf-binary")
                self.send_header("Content-Length", str(len(glb_bytes)))
                self.send_header("Content-Disposition", f'attachment; filename="{family}_custom.glb"')
                self.send_header("X-Cache", "HIT" if is_cached else "MISS")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(glb_bytes)

            except ValueError as e:
                err_body = json.dumps({"detail": str(e)}).encode("utf-8")
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(err_body)
            except Exception as e:
                err_body = json.dumps({"detail": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(err_body)
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port: int = 8000):
    if app:
        import uvicorn
        print(f"Starting ModelCoder FastAPI generation server on http://localhost:{port}...")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        print(f"Starting ModelCoder Standalone generation server on http://localhost:{port}...")
        server = HTTPServer(("0.0.0.0", port), StandaloneHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()

if __name__ == "__main__":
    port = 8000
    for idx, arg in enumerate(sys.argv):
        if arg == "--port" and idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    run_server(port)
