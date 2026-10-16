"""
Unit tests for ModelCoder On-Demand Generation Worker and Caching Server.
Tests deterministic cache keys, sandbox execution, GLB production, and cache hit logic.
"""

import unittest
import os
import sys

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from server.main import compute_cache_key, execute_generation, CACHE_DIR, TMP_DIR

class TestServerWorker(unittest.TestCase):

    def test_cache_key_determinism(self):
        # Parameters inserted in different key orders
        p1 = {"table_type": "standard_autopsy", "length": 2.2, "overhead_lamp": True}
        p2 = {"overhead_lamp": True, "length": 2.2, "table_type": "standard_autopsy"}

        key1 = compute_cache_key("autopsy_table", p1, preset="sterile_autopsy")
        key2 = compute_cache_key("autopsy_table", p2, preset="sterile_autopsy")

        self.assertEqual(key1, key2, "Cache key must be identical regardless of dict key insertion order")

    def test_execute_generation_and_caching(self):
        params = {
            "table_type": "standard_autopsy",
            "length": 2.15,
            "overhead_lamp": True,
            "seed": 99999
        }
        key = compute_cache_key("autopsy_table", params, preset="sterile_autopsy")
        test_cache_file = os.path.join(CACHE_DIR, f"{key}.glb")
        if os.path.exists(test_cache_file):
            os.remove(test_cache_file)

        # 1. First execution: MISS
        glb_data, is_cached = execute_generation("autopsy_table", params, preset="sterile_autopsy")
        self.assertFalse(is_cached, "First generation should be a cache MISS")
        self.assertGreater(len(glb_data), 1000, "GLB binary data should be non-empty")
        self.assertTrue(glb_data.startswith(b"glTF"), "GLB data must start with glTF magic header")

        # 2. Second execution: HIT
        glb_cached, is_cached_2 = execute_generation("autopsy_table", params, preset="sterile_autopsy")
        self.assertTrue(is_cached_2, "Second generation with identical params must be a cache HIT")
        self.assertEqual(glb_data, glb_cached, "Cached GLB data must match original exactly")

    def test_invalid_parameters_rejected(self):
        invalid_params = {
            "length": 99.0 # Exceeds max 3.0 in manifest
        }
        with self.assertRaises(ValueError) as ctx:
            execute_generation("autopsy_table", invalid_params)
        self.assertTrue(
            "less than minimum" in str(ctx.exception) or
            "exceeds maximum" in str(ctx.exception) or
            "Invalid parameters" in str(ctx.exception)
        )

    def test_temp_cleanup(self):
        # Verify that TMP_DIR has no lingering temporary worker directories
        remaining = [f for f in os.listdir(TMP_DIR) if os.path.isdir(os.path.join(TMP_DIR, f))]
        self.assertEqual(len(remaining), 0, f"Temporary directories should be cleaned up, found: {remaining}")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
