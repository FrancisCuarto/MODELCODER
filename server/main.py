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
try:
    from procedural_assets.generators import GENERATOR_REGISTRY
except ImportError:
    GENERATOR_REGISTRY = {k: True for k in discover_all_manifests().keys()}

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SERVER_DIR, "cache")
TMP_DIR = os.path.join(SERVER_DIR, "tmp")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

BLENDER_EXE = os.environ.get("BLENDER_BIN")
if not BLENDER_EXE or not os.path.isfile(BLENDER_EXE):
    candidates = [
        r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe",
        shutil.which("blender") or "blender"
    ]
    for c in candidates:
        if c and (os.path.isfile(c) or shutil.which(c)):
            BLENDER_EXE = c
            break

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
            "--name", f"gen_{family}_{req_id}"
        ]

        if params.get("collision") or params.get("add_collision_mesh"):
            cmd.append("--collision")

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
# MCP (MODEL CONTEXT PROTOCOL) & EXTERNAL AI AGENT TOOLS
# ==============================================================================
def get_mcp_tools() -> list:
    """Return Model Context Protocol (MCP) tool definitions for external AI agents."""
    families = sorted(list(GENERATOR_REGISTRY.keys()))
    return [
        {
            "name": "list_3d_families",
            "description": "Lista todas las familias de generadores 3D procedurales disponibles en ModelCoder junto con su descripción y presets.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "get_family_schema",
            "description": "Obtiene el esquema completo de parámetros, rangos y presets de una familia 3D específica.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "family": {
                        "type": "string",
                        "enum": families,
                        "description": "Nombre de la familia 3D a inspeccionar"
                    }
                },
                "required": ["family"]
            }
        },
        {
            "name": "generate_3d_glb",
            "description": "Genera un activo 3D GLB determinista en caché usando Blender Headless y devuelve la ruta y metadatos del archivo.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "family": {
                        "type": "string",
                        "enum": families,
                        "description": "Familia del generador 3D"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Diccionario de parámetros numéricos/booleanos del generador"
                    },
                    "preset": {
                        "type": "string",
                        "description": "Preset opcional de la familia"
                    }
                },
                "required": ["family"]
            }
        },
        {
            "name": "validate_scene_spec",
            "description": "Valida y audita un ModelSpec JSON de ModelCoder Studio (chequea colisión con suelo Y>=0, primitivas válidas y jerarquía parent).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "Objeto ModelSpec con name y components[]"
                    }
                },
                "required": ["spec"]
            }
        }
    ]


def execute_mcp_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute an MCP tool call from an external AI agent (Claude Code, Cursor, Codex, etc.)."""
    if name == "list_3d_families":
        manifests = discover_all_manifests()
        summary = {}
        for fam, manifest in manifests.items():
            d = manifest.to_dict()
            summary[fam] = {
                "description": d.get("description", ""),
                "presets": list(d.get("presets", {}).keys()),
                "parameter_count": len(d.get("parameters", {}))
            }
        return {"families": summary, "total": len(summary)}

    if name == "get_family_schema":
        family = arguments.get("family", "")
        manifest = find_manifest_for_family(family)
        if not manifest:
            raise ValueError(f"Familia 3D no encontrada: '{family}'")
        return manifest.to_dict()

    if name == "generate_3d_glb":
        family = arguments.get("family", "")
        params = arguments.get("parameters") or {}
        preset = arguments.get("preset")
        glb_bytes, is_cached = execute_generation(family, params, preset)
        cache_key = compute_cache_key(family, params, preset)
        cached_glb_path = os.path.join(CACHE_DIR, f"{cache_key}.glb")
        return {
            "family": family,
            "cached": is_cached,
            "size_bytes": len(glb_bytes),
            "cache_key": cache_key,
            "glb_path": cached_glb_path
        }

    if name == "validate_scene_spec":
        spec = arguments.get("spec") or {}
        comps = spec.get("components") or []
        valid_shapes = {
            "box", "chamfer_box", "cylinder", "pipe", "prism", "sphere",
            "pyramid", "cone", "wedge", "torus", "capsule", "plane"
        }
        issues = []
        comp_names = {c.get("name") for c in comps if isinstance(c, dict) and c.get("name")}
        min_bottom_y = None
        for idx, c in enumerate(comps):
            if not isinstance(c, dict):
                issues.append(f"Componente #{idx} no es un objeto.")
                continue
            cname = c.get("name", f"Pieza_{idx}")
            shape = c.get("shape", "box")
            if shape not in valid_shapes:
                issues.append(f"Componente '{cname}' usa shape inválido '{shape}'.")
            parent = c.get("parent")
            if parent and parent not in comp_names:
                issues.append(f"Componente '{cname}' referencia un parent inexistente '{parent}'.")
            pos = c.get("position") or [0, 0, 0]
            size = c.get("size") or [1, 1, 1]
            if not parent and len(pos) >= 2 and len(size) >= 2:
                bottom = float(pos[1]) - abs(float(size[1])) * 0.5
                if min_bottom_y is None or bottom < min_bottom_y:
                    min_bottom_y = bottom
        if min_bottom_y is not None and (min_bottom_y < -0.08 or min_bottom_y > 0.35):
            issues.append(f"Desalineación vertical respecto al suelo Y=0 (min_bottom_y={min_bottom_y:.3f}).")
        return {
            "valid": len(issues) == 0,
            "component_count": len(comps),
            "min_bottom_y": min_bottom_y,
            "issues": issues
        }

    raise ValueError(f"Herramienta MCP desconocida: '{name}'")


# ==============================================================================
# FASTAPI APPLICATION (When fastapi & uvicorn are available)
# ==============================================================================
try:
    from fastapi import FastAPI, HTTPException, Response, Request
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="ModelCoder 3D Generation & MCP Agent API",
        version="2.0.0",
        description="On-demand procedural 3D model generation & MCP Agent microservice"
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

    class MCPCallRequest(BaseModel):
        name: str
        arguments: Dict[str, Any] = {}

    @app.get("/api/health")
    def health_check():
        cached_count = len([f for f in os.listdir(CACHE_DIR) if f.endswith(".glb")])
        return {
            "status": "healthy",
            "blender_path": BLENDER_EXE,
            "cached_models": cached_count,
            "families_available": len(GENERATOR_REGISTRY),
            "mcp_enabled": True
        }

    @app.get("/api/generators")
    def list_generators():
        manifests = discover_all_manifests()
        return {k: m.to_dict() for k, m in manifests.items()}

    @app.get("/api/mcp/tools")
    def mcp_list_tools():
        return {"tools": get_mcp_tools()}

    @app.post("/api/mcp/call")
    def mcp_call_tool(req: MCPCallRequest):
        try:
            result = execute_mcp_tool(req.name, req.arguments)
            return {"ok": True, "result": result}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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
                "families_available": len(GENERATOR_REGISTRY),
                "mcp_enabled": True
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
        elif parsed.path == "/api/mcp/tools":
            body = json.dumps({"tools": get_mcp_tools()}).encode("utf-8")
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
        elif parsed.path == "/api/mcp/call":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            try:
                data = json.loads(raw_body.decode("utf-8"))
                result = execute_mcp_tool(data.get("name", ""), data.get("arguments") or {})
                body = json.dumps({"ok": True, "result": result}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(body)
            except ValueError as e:
                err_body = json.dumps({"ok": False, "detail": str(e)}).encode("utf-8")
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(err_body)
            except Exception as e:
                err_body = json.dumps({"ok": False, "detail": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(err_body)
        else:
            self.send_response(404)
            self.end_headers()


def run_mcp_stdio_server():
    """Run standard Model Context Protocol (MCP) JSON-RPC 2.0 server over STDIO."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method", "")
            req_id = req.get("id")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "modelcoder-mcp", "version": "2.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": get_mcp_tools()}
                }
            elif method == "tools/call":
                params = req.get("params") or {}
                tool_res = execute_mcp_tool(params.get("name", ""), params.get("arguments") or {})
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(tool_res, ensure_ascii=False)}]
                    }
                }
            else:
                if req_id is None:
                    continue
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                }
        except Exception as exc:
            resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if isinstance(req, dict) else None,
                "error": {"code": -32000, "message": str(exc)}
            }
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


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
    if "--mcp" in sys.argv:
        run_mcp_stdio_server()
        sys.exit(0)
    port = int(os.environ.get("PORT", 8000))
    for idx, arg in enumerate(sys.argv):
        if arg == "--port" and idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    run_server(port)
