"""
Unit test suite verifying PS1TextureAtlas UV texture resolution,
alias mapping, strict error handling, and generator UV integrity.
"""
import unittest
import sys
import os
import re
import warnings

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
import bmesh
from procedural_assets.core.texture_atlas import PS1TextureAtlas
from procedural_assets.generators.access_card_reader.generator import AccessCardReaderGenerator
from procedural_assets.generators.access_card_reader.config import AccessCardReaderConfig

class TestTextureAtlasUV(unittest.TestCase):
    """Test cases for PS1 texture atlas UV integrity and alias resolution."""

    def setUp(self):
        # Reset Blender scene before each test
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in list(bpy.data.meshes):
            bpy.data.meshes.remove(mesh, do_unlink=True)
        for mat in list(bpy.data.materials):
            bpy.data.materials.remove(mat, do_unlink=True)
        PS1TextureAtlas.STRICT_MODE = False

    def tearDown(self):
        PS1TextureAtlas.STRICT_MODE = False

    def test_rects_coordinates_and_bounds(self):
        """Every canonical rect must be non-empty and strictly inside [0.0, 1.0] without spanning entire atlas."""
        for name, rect in PS1TextureAtlas.RECTS.items():
            u0, v0, u1, v1 = rect
            self.assertGreaterEqual(u0, 0.0, f"{name}: u0 < 0")
            self.assertGreaterEqual(v0, 0.0, f"{name}: v0 < 0")
            self.assertLessEqual(u1, 1.0, f"{name}: u1 > 1.0")
            self.assertLessEqual(v1, 1.0, f"{name}: v1 > 1.0")
            self.assertLess(u0, u1, f"{name}: u0 >= u1")
            self.assertLess(v0, v1, f"{name}: v0 >= v1")
            
            # No sub-region should be the entire atlas (which caused the bug)
            self.assertNotEqual(
                (u0, v0, u1, v1), (0.0, 0.0, 1.0, 1.0),
                f"{name} cannot be the full atlas (0,0,1,1)"
            )

    def test_all_aliases_point_to_valid_canonical_rects(self):
        """Every alias in ALIASES must point to a defined key in RECTS."""
        for alias_name, canonical_target in PS1TextureAtlas.ALIASES.items():
            self.assertIn(
                canonical_target, PS1TextureAtlas.RECTS,
                f"Alias '{alias_name}' points to unknown target '{canonical_target}'"
            )

    def test_alias_resolution_returns_correct_rect(self):
        """Aliases must resolve to the identical rectangle of their target."""
        self.assertEqual(
            PS1TextureAtlas.get_rect("metal_plates_rivets"),
            PS1TextureAtlas.RECTS["metal_dark_grime"]
        )
        self.assertEqual(
            PS1TextureAtlas.get_rect("rubber_tread"),
            PS1TextureAtlas.RECTS["rubber_black"]
        )
        self.assertEqual(
            PS1TextureAtlas.get_rect("computer_screen_crt"),
            PS1TextureAtlas.RECTS["crt_screen_green"]
        )
        self.assertEqual(
            PS1TextureAtlas.get_rect("control_panel_buttons"),
            PS1TextureAtlas.RECTS["button_white"]
        )
        self.assertEqual(
            PS1TextureAtlas.get_rect("metal_vent_grate"),
            PS1TextureAtlas.RECTS["vent_grill"]
        )

    def test_unknown_name_strict_raises_key_error(self):
        """In strict mode, requesting an unknown texture must raise KeyError."""
        with self.assertRaises(KeyError) as ctx:
            PS1TextureAtlas.get_rect("nonexistent_random_texture_xyz", strict=True)
        self.assertIn("nonexistent_random_texture_xyz", str(ctx.exception))

        # Test global STRICT_MODE
        PS1TextureAtlas.STRICT_MODE = True
        with self.assertRaises(KeyError):
            PS1TextureAtlas.get_rect("another_fake_texture_123")
        PS1TextureAtlas.STRICT_MODE = False

    def test_unknown_name_non_strict_warns_and_never_returns_full_atlas(self):
        """In non-strict mode, unknown names must emit UserWarning and fallback to safe tile, never (0,0,1,1)."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            rect = PS1TextureAtlas.get_rect("bogus_unknown_material_name", strict=False)
            
            # Warning emitted
            self.assertTrue(any(issubclass(item.category, UserWarning) for item in w))
            # Must NOT be (0, 0, 1, 1)
            self.assertNotEqual(rect, (0.0, 0.0, 1.0, 1.0))
            # Must be the safe fallback metal_dark_grime
            self.assertEqual(rect, PS1TextureAtlas.RECTS["metal_dark_grime"])

    def test_all_generators_use_valid_texture_names(self):
        """Scan all generator source code and assert 100% of get_rect calls resolve to valid names."""
        pattern = re.compile(r'get_rect\(\s*["\']([^"\']+)["\']\s*\)')
        generators_dir = os.path.join(parent_dir, "procedural_assets", "generators")
        
        all_calls = []
        for dirpath, dirs, filenames in os.walk(generators_dir):
            for f in filenames:
                if f.endswith(".py"):
                    filepath = os.path.join(dirpath, f)
                    with open(filepath, "r", encoding="utf-8") as fh:
                        for idx, line in enumerate(fh, 1):
                            for match in pattern.finditer(line):
                                req_name = match.group(1)
                                all_calls.append((req_name, filepath, idx))
        
        self.assertGreater(len(all_calls), 0, "Should have found get_rect calls")
        
        unresolved = []
        for req_name, fpath, line_no in all_calls:
            if not PS1TextureAtlas.is_valid_name(req_name):
                unresolved.append(f"{fpath}:{line_no} -> '{req_name}'")
        
        self.assertEqual(
            len(unresolved), 0,
            f"Found {len(unresolved)} unresolved texture names in generators:\n" + "\n".join(unresolved)
        )

    def test_access_card_reader_uv_integrity(self):
        """Verify AccessCardReaderGenerator produces faces with valid sub-atlas UVs and no full-atlas faces."""
        cfg = AccessCardReaderConfig(
            name="test_card_reader_uv",
            reader_style="swipe_and_keypad",
            has_keypad=True,
            has_status_screen=True
        )
        gen = AccessCardReaderGenerator()
        obj = gen.generate(cfg)
        
        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        uv_layer = bm.loops.layers.uv.get("UVMap")
        self.assertIsNotNone(uv_layer, "UVMap layer must exist")
        
        full_atlas_faces = []
        for face_idx, face in enumerate(bm.faces):
            uvs = [loop[uv_layer].uv for loop in face.loops]
            u_coords = [uv[0] for uv in uvs]
            v_coords = [uv[1] for uv in uvs]
            
            min_u, max_u = min(u_coords), max(u_coords)
            min_v, max_v = min(v_coords), max(v_coords)
            
            # Check for silent full-atlas bug (face UVs spanning almost 0.0 to 1.0)
            if (min_u < 0.05 and max_u > 0.95 and min_v < 0.05 and max_v > 0.95):
                full_atlas_faces.append(face_idx)
            
            # Check all coords in 0.0 .. 1.0
            for u, v in uvs:
                self.assertGreaterEqual(u, -0.01, f"UV U underflow on face {face_idx}")
                self.assertLessEqual(u, 1.01, f"UV U overflow on face {face_idx}")
                self.assertGreaterEqual(v, -0.01, f"UV V underflow on face {face_idx}")
                self.assertLessEqual(v, 1.01, f"UV V overflow on face {face_idx}")
        
        self.assertEqual(
            len(full_atlas_faces), 0,
            f"Found {len(full_atlas_faces)} faces incorrectly mapped to the entire atlas!"
        )
        bm.free()

if __name__ == "__main__":
    unittest.main()
