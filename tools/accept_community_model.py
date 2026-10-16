"""
Accept Community Model CLI & Automation Tool for ModelCoder.
Parses community model proposals from GitHub Issue Markdown bodies or event JSON,
validates AST security and schema integrity, installs the files into
procedural_assets/generators/<family>/, and synchronizes the web catalog.
"""

import os
import sys
import re
import json
import argparse
from typing import Dict, Any, Optional, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from tools.verify_community_generator import audit_source_code, verify_manifest
from tools.sync_web_catalog import sync_catalog



def extract_code_block(markdown_text: str, heading_pattern: str, lang: str) -> Optional[str]:
    """Extract code block content following a specific markdown section heading."""
    pattern = rf"{heading_pattern}[\s\S]*?```{lang}[^\n]*\n([\s\S]*?)```"
    match = re.search(pattern, markdown_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_files_from_issue_body(issue_body: str) -> Dict[str, str]:
    """Extract manifest.json, generator.py, and config.py from GitHub Issue text."""
    manifest_raw = extract_code_block(issue_body, r"manifest\.json", "json")
    if not manifest_raw:
        # Fallback: find any json code block
        match = re.search(r"```json[^\n]*\n([\s\S]*?)```", issue_body)
        if match:
            manifest_raw = match.group(1).strip()

    generator_raw = extract_code_block(issue_body, r"generator\.py", "python")
    config_raw = extract_code_block(issue_body, r"config\.py", "python")

    # If generator and config were in generic python blocks without matching headings
    if not generator_raw or not config_raw:
        py_blocks = re.findall(r"```python[^\n]*\n([\s\S]*?)```", issue_body)
        for block in py_blocks:
            if "BaseAssetGenerator" in block and not generator_raw:
                generator_raw = block.strip()
            elif ("BaseAssetConfig" in block or "@dataclass" in block) and not config_raw:
                config_raw = block.strip()
        
        # If still missing and exactly 2 python blocks exist, assume 1st is generator, 2nd is config (or vice versa)
        if len(py_blocks) == 2 and (not generator_raw or not config_raw):
            b1, b2 = py_blocks[0].strip(), py_blocks[1].strip()
            if "Generator" in b1:
                generator_raw = generator_raw or b1
                config_raw = config_raw or b2
            else:
                config_raw = config_raw or b1
                generator_raw = generator_raw or b2

    if not manifest_raw:
        raise ValueError("No se encontró el bloque ```json con manifest.json en el Issue.")
    if not generator_raw:
        raise ValueError("No se encontró el código Python de generator.py en el Issue.")
    if not config_raw:
        raise ValueError("No se encontró el código Python de config.py en el Issue.")

    return {
        "manifest": manifest_raw,
        "generator": generator_raw,
        "config": config_raw
    }

def install_model(manifest_text: str, generator_text: str, config_text: str, author_login: str = "", readme_text: str = "") -> Tuple[str, str]:
    """Install model into procedural_assets/generators/<family>/ and run verification."""
    manifest_data = json.loads(manifest_text)
    manifest_id = manifest_data.get("id", "")
    parts = manifest_id.split(".")
    family_name = parts[-1] if parts else "community_model"

    if not family_name or not re.match(r"^[a-z0-9_]+$", family_name):
        raise ValueError(f"Identificador de familia inválido en manifest: '{family_name}' (solo minúsculas y guiones bajos)")

    model_display_name = manifest_data.get("name", family_name.replace("_", " ").title())

    # Credit GitHub author if provided and not explicitly customized
    if author_login:
        author_info = manifest_data.get("author")
        if not author_info or not isinstance(author_info, dict) or author_info.get("name") in ["Community", "Tu Nombre"]:
            manifest_data["author"] = {
                "name": author_login,
                "github": author_login
            }
        elif isinstance(author_info, dict) and not author_info.get("github"):
            author_info["github"] = author_login

    target_dir = os.path.join(current_dir, "procedural_assets", "generators", family_name)
    os.makedirs(target_dir, exist_ok=True)

    manifest_path = os.path.join(target_dir, "manifest.json")
    generator_path = os.path.join(target_dir, "generator.py")
    config_path = os.path.join(target_dir, "config.py")
    init_path = os.path.join(target_dir, "__init__.py")
    readme_path = os.path.join(target_dir, "README.md")

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest_data, indent=2, ensure_ascii=False) + "\n")

    with open(generator_path, "w", encoding="utf-8") as f:
        f.write(generator_text.replace("\r\n", "\n").strip() + "\n")

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_text.replace("\r\n", "\n").strip() + "\n")

    with open(init_path, "w", encoding="utf-8") as f:
        f.write("from .config import *\nfrom .generator import *\n")

    if not readme_text:
        author_name = manifest_data.get("author", {}).get("name", "Community")
        readme_text = f"# {model_display_name}\n\n{manifest_data.get('description', '')}\n\n- **Autor**: {author_name}\n- **Licencia**: {manifest_data.get('license', 'CC-BY-4.0')}\n"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_text.replace("\r\n", "\n").strip() + "\n")

    # Run AST Security Audit
    for pyf in [generator_path, config_path, init_path]:
        ok, violations = audit_source_code(pyf)
        if not ok:
            raise SecurityError(f"Violación de seguridad AST en {os.path.basename(pyf)}: {', '.join(violations)}")

    # Run Manifest Schema Check
    m_ok, m_errs = verify_manifest(manifest_path)
    if not m_ok:
        raise ValueError(f"Error de validación en manifest.json: {', '.join(m_errs)}")

    # Update web catalog
    print(f"[OK] Generador '{family_name}' instalado y verificado con exito.")
    print("Sincronizando catalogo de la web...")
    sync_catalog()

    # Write outputs for GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        try:
            with open(github_output, "a", encoding="utf-8") as f:
                f.write(f"family={family_name}\n")
                f.write(f"name={model_display_name}\n")
        except Exception as e:
            print(f"Warning: could not write to GITHUB_OUTPUT: {e}")

    return family_name, model_display_name

class SecurityError(Exception):
    pass

def main():
    parser = argparse.ArgumentParser(description="Accept community model and integrate into ModelCoder.")
    parser.add_argument("--event-path", type=str, help="Path to GitHub event.json file")
    parser.add_argument("--issue-body", type=str, help="Raw Markdown body from GitHub Issue")
    parser.add_argument("--issue-file", type=str, help="Path to text file containing Issue body")
    parser.add_argument("--author", type=str, default="", help="GitHub handle of issue creator")
    args = parser.parse_args()

    body = args.issue_body
    author = args.author

    if args.event_path and os.path.isfile(args.event_path):
        try:
            with open(args.event_path, "r", encoding="utf-8") as f:
                event_data = json.load(f)
            body = event_data.get("issue", {}).get("body", "")
            if not author:
                author = event_data.get("issue", {}).get("user", {}).get("login", "")
        except Exception as e:
            print(f"ERROR reading event-path: {e}", file=sys.stderr)
            sys.exit(1)

    if not body and args.issue_file and os.path.isfile(args.issue_file):
        with open(args.issue_file, "r", encoding="utf-8") as f:
            body = f.read()

    if not body:
        print("ERROR: Se requiere --event-path, --issue-body o --issue-file.", file=sys.stderr)
        sys.exit(1)

    try:
        files = extract_files_from_issue_body(body)
        family, model_name = install_model(files["manifest"], files["generator"], files["config"], author_login=author)
        print(f"SUCCESS: Modelo '{model_name}' ({family}) incorporado correctamente.")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: No se pudo incorporar el modelo: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
