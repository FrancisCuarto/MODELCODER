"""
Community Generator Security Scanner and Verification Engine for ModelCoder.
Performs AST static security analysis, JSON schema verification,
and sandbox execution checks on new community contributions.
"""

import ast
import os
import sys
import json
import subprocess
from typing import List, Tuple, Dict, Any, Optional

FORBIDDEN_MODULES = {
    "subprocess", "socket", "http", "urllib", "requests", "aiohttp",
    "ctypes", "multiprocessing", "pty", "telnetlib", "ftplib", "smtplib"
}

FORBIDDEN_CALLS = {
    "eval", "exec", "compile", "__import__",
    "os.system", "os.popen", "os.spawn", "os.exec",
    "shutil.rmtree"
}

ALLOWED_ROOT_PACKAGES = {
    "bpy", "bmesh", "math", "mathutils", "random", "dataclasses", "typing",
    "enum", "procedural_assets", "json"
}

class SecurityASTVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations: List[str] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            root_mod = alias.name.split(".")[0]
            if root_mod in FORBIDDEN_MODULES:
                self.violations.append(f"Forbidden module import '{alias.name}' at line {node.lineno}")
            elif root_mod not in ALLOWED_ROOT_PACKAGES:
                self.violations.append(f"Unapproved external library '{alias.name}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            root_mod = node.module.split(".")[0]
            if root_mod in FORBIDDEN_MODULES:
                self.violations.append(f"Forbidden module import from '{node.module}' at line {node.lineno}")
            elif node.level == 0 and root_mod not in ALLOWED_ROOT_PACKAGES:
                self.violations.append(f"Unapproved external library '{node.module}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        call_name = ""
        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            val = node.func.value
            if isinstance(val, ast.Name):
                call_name = f"{val.id}.{node.func.attr}"

        if call_name in FORBIDDEN_CALLS:
            self.violations.append(f"Forbidden system call '{call_name}()' at line {node.lineno}")
        self.generic_visit(node)

def audit_source_code(filepath: str) -> Tuple[bool, List[str]]:
    if not os.path.isfile(filepath):
        return True, []
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        tree = ast.parse(src, filename=filepath)
    except SyntaxError as e:
        return False, [f"SyntaxError in {filepath}: {e}"]

    visitor = SecurityASTVisitor(filepath)
    visitor.visit(tree)
    return len(visitor.violations) == 0, visitor.violations

def verify_manifest(manifest_path: str) -> Tuple[bool, List[str]]:
    errors = []
    if not os.path.isfile(manifest_path):
        return False, [f"Missing manifest.json at {manifest_path}"]
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Invalid JSON in manifest: {e}"]

    required_fields = ["id", "name", "version", "author", "license", "category", "parameters"]
    for rf in required_fields:
        if rf not in data:
            errors.append(f"Manifest missing required field: '{rf}'")

    # Author
    author = data.get("author", {})
    if not isinstance(author, dict) or not author.get("name"):
        errors.append("Manifest author must specify a 'name'")

    # License
    valid_licenses = ["CC-BY-4.0", "CC0-1.0", "MIT", "Apache-2.0", "GPL-3.0"]
    lic = data.get("license", "")
    if lic not in valid_licenses:
        errors.append(f"License '{lic}' is not in approved open licenses list: {valid_licenses}")

    # Parameters
    params = data.get("parameters", [])
    if not isinstance(params, list) or len(params) == 0:
        errors.append("Manifest must declare at least 1 parameter")
    for p in params:
        for req in ["key", "label", "type", "default"]:
            if req not in p:
                errors.append(f"Parameter missing '{req}' in parameter {p.get('key', '?')}")

    return len(errors) == 0, errors

def verify_family(family_name: str, blender_exe: Optional[str] = None) -> bool:
    print(f"\n==================================================")
    print(f" Auditing Generator Family: '{family_name}'")
    print(f"==================================================")

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    family_dir = os.path.join(current_dir, "procedural_assets", "generators", family_name)

    if not os.path.isdir(family_dir):
        print(f"[FAIL] Directory does not exist: {family_dir}")
        return False

    # 1. Manifest Validation
    manifest_path = os.path.join(family_dir, "manifest.json")
    m_ok, m_errs = verify_manifest(manifest_path)
    if not m_ok:
        print("[FAIL] Manifest validation failed:")
        for err in m_errs:
            print(f"  - {err}")
        return False
    print("  [PASS] Manifest specification and license contract valid.")

    # 2. AST Security Analysis
    py_files = [os.path.join(family_dir, f) for f in os.listdir(family_dir) if f.endswith(".py")]
    ast_passed = True
    for pyf in py_files:
        ok, violations = audit_source_code(pyf)
        if not ok:
            ast_passed = False
            print(f"[FAIL] Security AST violations in {os.path.basename(pyf)}:")
            for v in violations:
                print(f"  - {v}")
    if not ast_passed:
        return False
    print(f"  [PASS] AST Static Security Analysis: 0 forbidden imports or syscalls across {len(py_files)} files.")

    # 3. Sandbox Blender Execution
    if not blender_exe:
        blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
    if not os.path.isfile(blender_exe):
        blender_exe = "blender"

    print("  [INFO] Executing in headless Blender sandbox (timeout 15s)...")
    cmd = [
        blender_exe, "-b", "--python", os.path.join(current_dir, "generate.py"),
        "--", "--family", family_name, "--collision", "--seed", "42"
    ]
    try:
        res = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            print(f"[FAIL] Blender execution failed with exit code {res.returncode}")
            print(res.stderr[:500])
            return False
        print("  [PASS] Blender generated mesh and exported without errors.")
    except subprocess.TimeoutExpired:
        print("[FAIL] Execution timed out (>15s). Generator is too slow or has an infinite loop.")
        return False

    print(f"\n[SUCCESS] Generator '{family_name}' passed all community security and compliance gates!\n")
    return True

if __name__ == "__main__":
    raw_args = sys.argv
    cli_args = raw_args[raw_args.index("--") + 1:] if "--" in raw_args else raw_args[1:]
    target = cli_args[0] if cli_args else "autopsy_table"
    success = verify_family(target)
    sys.exit(0 if success else 1)
