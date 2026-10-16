"""
Declarative Generator Manifest and Parameter Contract System for Below Nominal.
Provides specification, JSON schema validation, dynamic argparse integration,
and config serialization for community and official procedural 3D asset generators.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Union
import json
import os
import argparse

@dataclass
class ParameterDef:
    """Definition of an individual parameter exposed by a generator."""
    key: str
    label: str
    type: str  # "float", "int", "boolean", "enum", "color_rgba", "seed", "string"
    default: Any
    description: str = ""
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    options: Optional[List[Dict[str, str]]] = None  # [{"value": "val", "label": "Label"}, ...]
    group: str = "General"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParameterDef":
        return cls(
            key=data["key"],
            label=data.get("label", data["key"]),
            type=data.get("type", "string"),
            default=data.get("default"),
            description=data.get("description", ""),
            min=float(data["min"]) if "min" in data and data["min"] is not None else None,
            max=float(data["max"]) if "max" in data and data["max"] is not None else None,
            step=float(data["step"]) if "step" in data and data["step"] is not None else None,
            options=data.get("options"),
            group=data.get("group", "General")
        )

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "key": self.key,
            "label": self.label,
            "type": self.type,
            "default": self.default,
            "group": self.group
        }
        if self.description:
            d["description"] = self.description
        if self.min is not None:
            d["min"] = self.min
        if self.max is not None:
            d["max"] = self.max
        if self.step is not None:
            d["step"] = self.step
        if self.options is not None:
            d["options"] = self.options
        return d

    def validate_value(self, val: Any) -> Tuple[bool, Optional[str]]:
        """Validate if a runtime value conforms to type, bounds, and enum options."""
        if val is None:
            return True, None

        if self.type == "float":
            try:
                num = float(val)
                if self.min is not None and num < self.min:
                    return False, f"Value {num} for '{self.key}' is less than minimum {self.min}"
                if self.max is not None and num > self.max:
                    return False, f"Value {num} for '{self.key}' exceeds maximum {self.max}"
            except (ValueError, TypeError):
                return False, f"Expected float for '{self.key}', got {type(val).__name__}"

        elif self.type == "int" or self.type == "seed":
            try:
                num = int(val)
                if self.min is not None and num < self.min:
                    return False, f"Value {num} for '{self.key}' is less than minimum {self.min}"
                if self.max is not None and num > self.max:
                    return False, f"Value {num} for '{self.key}' exceeds maximum {self.max}"
            except (ValueError, TypeError):
                return False, f"Expected int for '{self.key}', got {type(val).__name__}"

        elif self.type == "boolean":
            if not isinstance(val, bool) and val not in (0, 1, "true", "false", "True", "False"):
                return False, f"Expected boolean for '{self.key}', got {val}"

        elif self.type == "enum":
            if self.options:
                valid_vals = [opt["value"] for opt in self.options]
                if str(val) not in valid_vals:
                    return False, f"Value '{val}' for '{self.key}' is not in allowed options: {valid_vals}"

        elif self.type == "color_rgba":
            if not isinstance(val, (list, tuple)) or len(val) != 4:
                return False, f"Expected 4-element RGBA list/tuple for '{self.key}', got {val}"
            for c in val:
                if not isinstance(c, (int, float)) or c < 0.0 or c > 1.0:
                    return False, f"RGBA component in '{self.key}' out of range [0.0, 1.0]: {c}"

        return True, None

@dataclass
class AuthorDef:
    name: str
    github: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Any) -> "AuthorDef":
        if isinstance(data, str):
            return cls(name=data)
        if isinstance(data, dict):
            return cls(
                name=data.get("name", "Unknown Author"),
                github=data.get("github"),
                url=data.get("url")
            )
        return cls(name=str(data))

    def to_dict(self) -> Dict[str, Any]:
        d = {"name": self.name}
        if self.github:
            d["github"] = self.github
        if self.url:
            d["url"] = self.url
        return d

@dataclass
class PresetDef:
    id: str
    name: str
    values: Dict[str, Any]
    description: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PresetDef":
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            values=data.get("values", {}),
            description=data.get("description", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "name": self.name,
            "values": self.values
        }
        if self.description:
            d["description"] = self.description
        return d

@dataclass
class GeneratorManifest:
    """Full metadata and contract specification for a procedural 3D model generator."""
    id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: Optional[AuthorDef] = None
    license: str = "CC-BY-4.0"
    category: str = "props"
    tags: List[str] = field(default_factory=list)
    parameters: List[ParameterDef] = field(default_factory=list)
    presets: List[PresetDef] = field(default_factory=list)
    compatibility: Dict[str, str] = field(default_factory=dict)
    export_capabilities: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneratorManifest":
        author = AuthorDef.from_dict(data["author"]) if "author" in data and data["author"] else None
        parameters = [ParameterDef.from_dict(p) for p in data.get("parameters", [])]
        presets = [PresetDef.from_dict(pr) for pr in data.get("presets", [])]

        return cls(
            id=data["id"],
            name=data["name"],
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            author=author,
            license=data.get("license", "CC-BY-4.0"),
            category=data.get("category", "props"),
            tags=data.get("tags", []),
            parameters=parameters,
            presets=presets,
            compatibility=data.get("compatibility", {}),
            export_capabilities=data.get("export_capabilities", {})
        )

    @classmethod
    def from_file(cls, filepath: str) -> "GeneratorManifest":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "license": self.license,
            "category": self.category,
            "tags": self.tags,
            "parameters": [p.to_dict() for p in self.parameters],
            "presets": [pr.to_dict() for pr in self.presets],
            "compatibility": self.compatibility,
            "export_capabilities": self.export_capabilities
        }
        if self.author:
            d["author"] = self.author.to_dict()
        return d

    def save_to_file(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    def get_parameter(self, key: str) -> Optional[ParameterDef]:
        for p in self.parameters:
            if p.key == key:
                return p
        return None

    def get_default_values(self) -> Dict[str, Any]:
        """Extract a dictionary of parameter keys and their default values."""
        defaults = {}
        for p in self.parameters:
            defaults[p.key] = p.default
        return defaults

    def validate_parameters(self, values: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate an arbitrary dictionary of parameter inputs against manifest definitions."""
        errors: List[str] = []
        for key, val in values.items():
            param = self.get_parameter(key)
            if not param:
                continue
            is_valid, err_msg = param.validate_value(val)
            if not is_valid and err_msg:
                errors.append(err_msg)
        return (len(errors) == 0, errors)

    def add_to_argparse(self, parser: argparse.ArgumentParser, cli_prefix: str = "") -> None:
        """Dynamically registers CLI arguments into an ArgumentParser based on parameter definitions."""
        for p in self.parameters:
            cli_flag = f"--{p.key.replace('_', '-')}"
            if cli_prefix:
                cli_flag = f"--{cli_prefix}-{p.key.replace('_', '-')}"

            # Skip common top-level flags already parsed by generate.py
            if p.key in ("seed", "name", "target_tri_budget", "wear_level", "palette_name"):
                continue

            # Avoid collision if flag already exists in parser
            if hasattr(parser, "_option_string_actions") and cli_flag in parser._option_string_actions:
                continue

            help_text = p.description or f"{p.label} (Default: {p.default})"

            if p.type == "float":
                parser.add_argument(
                    cli_flag,
                    type=float,
                    default=None,
                    help=help_text
                )
            elif p.type == "int" or p.type == "seed":
                parser.add_argument(
                    cli_flag,
                    type=int,
                    default=None,
                    help=help_text
                )
            elif p.type == "boolean":
                # Support both --flag and --no-flag
                parser.add_argument(
                    cli_flag,
                    action="store_true",
                    default=None,
                    help=f"Enable {p.label}"
                )
                neg_flag = cli_flag.replace("--", "--no-")
                if not (hasattr(parser, "_option_string_actions") and neg_flag in parser._option_string_actions):
                    parser.add_argument(
                        neg_flag,
                        action="store_true",
                        default=None,
                        help=f"Disable {p.label}"
                    )
            elif p.type == "enum":
                choices = [opt["value"] for opt in p.options] if p.options else None
                parser.add_argument(
                    cli_flag,
                    type=str,
                    choices=choices,
                    default=None,
                    help=help_text
                )
            elif p.type == "color_rgba":
                parser.add_argument(
                    cli_flag,
                    type=float,
                    nargs=4,
                    default=None,
                    help=f"{help_text} [4 floats: R G B A]"
                )
            elif p.type == "string":
                parser.add_argument(
                    cli_flag,
                    type=str,
                    default=None,
                    help=help_text
                )

    def build_config_kwargs(self, parsed_args: argparse.Namespace) -> Dict[str, Any]:
        """Extract populated parameter values from parsed CLI arguments namespace."""
        kwargs = {}
        for p in self.parameters:
            arg_attr = p.key
            if hasattr(parsed_args, arg_attr):
                val = getattr(parsed_args, arg_attr)
                if val is not None:
                    kwargs[p.key] = val
            # Handle boolean negation flags like --no-<key>
            neg_attr = f"no_{p.key}"
            if p.type == "boolean" and hasattr(parsed_args, neg_attr):
                if getattr(parsed_args, neg_attr) is True:
                    kwargs[p.key] = False
        return kwargs

def find_manifest_for_family(family_name: str, base_generators_dir: Optional[str] = None) -> Optional[GeneratorManifest]:
    """Check if a generator family contains an official manifest.json."""
    if not base_generators_dir:
        base_generators_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "generators"
        )
    manifest_path = os.path.join(base_generators_dir, family_name, "manifest.json")
    if os.path.isfile(manifest_path):
        try:
            return GeneratorManifest.from_file(manifest_path)
        except Exception as e:
            print(f"[WARN] Failed to parse manifest at {manifest_path}: {e}")
    return None

def discover_all_manifests(base_generators_dir: Optional[str] = None) -> Dict[str, GeneratorManifest]:
    """Scan all family subdirectories in generators/ and return a dict of family_name -> GeneratorManifest."""
    if not base_generators_dir:
        base_generators_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "generators"
        )
    results = {}
    if not os.path.isdir(base_generators_dir):
        return results

    for entry in os.listdir(base_generators_dir):
        family_dir = os.path.join(base_generators_dir, entry)
        if os.path.isdir(family_dir) and not entry.startswith("_"):
            manifest = find_manifest_for_family(entry, base_generators_dir)
            if manifest:
                results[entry] = manifest

    return results
