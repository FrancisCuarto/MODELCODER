import unittest
import os
import sys
import shutil
import bpy

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    CommsAntennaConfig,
    AntennaDishConfig,
    NavConsoleConfig,
    StarChartDisplayConfig,
    HydroponicTankConfig,
    NutrientPumpConfig,
    WaterRecyclerConfig,
    FoodStorageUnitConfig,
    CrewShowerConfig,
    WallClockConfig,
    PersonalEffectsBoxConfig,
)
from procedural_assets.core.manifest import find_manifest_for_family
from procedural_assets.export.glb_exporter import GLBExporter

class TestBatchGFamilies(unittest.TestCase):
    """Test suite for Lote G: Navigation & Habitation (90-100) - Final Roadmap Batch."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_batch_g")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_090_comms_antenna(self):
        cfg = CommsAntennaConfig(name="test_antenna", height=1.8, dipole_pairs=3, has_tuning_box=True)
        _, gen_cls = GENERATOR_REGISTRY["comms_antenna"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CommsAntenna validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("comms_antenna")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_091_antenna_dish(self):
        cfg = AntennaDishConfig(name="test_dish", dish_diameter=0.8, dish_depth=0.18, has_sub_reflector=True, mount_type="pedestal")
        _, gen_cls = GENERATOR_REGISTRY["antenna_dish"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"AntennaDish validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("antenna_dish")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_092_nav_console(self):
        cfg = NavConsoleConfig(name="test_nav_console", width=1.4, depth=0.95, height=1.15, screen_count=3, has_joystick=True, has_throttle=True)
        _, gen_cls = GENERATOR_REGISTRY["nav_console"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"NavConsole validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 180)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("nav_console")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_093_star_chart_display(self):
        cfg = StarChartDisplayConfig(name="test_star_chart", width=1.35, height=0.85, depth=0.08, display_mode="orbital_plot", has_control_strip=True, has_corner_brackets=True)
        _, gen_cls = GENERATOR_REGISTRY["star_chart_display"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"StarChartDisplay validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 120)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("star_chart_display")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_094_hydroponic_tank(self):
        cfg = HydroponicTankConfig(name="test_hydro_tank", tank_height=1.3, tank_radius=0.40, liquid_level=0.75, tank_shape="cylindrical", has_sight_glass=True, has_feed_pipes=True)
        _, gen_cls = GENERATOR_REGISTRY["hydroponic_tank"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"HydroponicTank validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 180)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("hydroponic_tank")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_095_nutrient_pump(self):
        cfg = NutrientPumpConfig(name="test_nutrient_pump", pump_size=0.45, motor_type="electric_finned", has_filter_canister=True, has_pressure_dial=True)
        _, gen_cls = GENERATOR_REGISTRY["nutrient_pump"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"NutrientPump validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("nutrient_pump")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_096_water_recycler(self):
        cfg = WaterRecyclerConfig(name="test_water_recycler", height=1.6, width=0.95, depth=0.65, filter_stage_count=3, has_purity_monitor=True, has_bypass_valves=True)
        _, gen_cls = GENERATOR_REGISTRY["water_recycler"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"WaterRecycler validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 180)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("water_recycler")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_097_food_storage_unit(self):
        cfg = FoodStorageUnitConfig(name="test_food_storage", height=1.75, width=0.85, depth=0.55, compartment_rows=4, has_latch_bars=True, has_ration_trays=True)
        _, gen_cls = GENERATOR_REGISTRY["food_storage_unit"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"FoodStorageUnit validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 180)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("food_storage_unit")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_098_crew_shower(self):
        cfg = CrewShowerConfig(name="test_crew_shower", width=0.90, depth=0.90, height=2.10, has_curtain=True, has_grab_rail=True, shower_head_type="fixed_overhead")
        _, gen_cls = GENERATOR_REGISTRY["crew_shower"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CrewShower validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("crew_shower")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_099_wall_clock(self):
        cfg = WallClockConfig(name="test_wall_clock", diameter=0.30, depth=0.05, bezel_type="circular", clock_state="running", has_glass=True, has_wall_bracket=True)
        _, gen_cls = GENERATOR_REGISTRY["wall_clock"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"WallClock validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("wall_clock")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_100_personal_effects_box(self):
        cfg = PersonalEffectsBoxConfig(name="test_box", width=0.44, depth=0.32, height=0.22, box_state="closed", has_latches=True, has_handle=True)
        _, gen_cls = GENERATOR_REGISTRY["personal_effects_box"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"PersonalEffectsBox validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("personal_effects_box")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

        # Export test verification
        out_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
        glb_p, json_p = GLBExporter.export(obj, cfg, rep, out_path, gen_cls.__name__)
        self.assertTrue(os.path.exists(glb_p))
        self.assertTrue(os.path.exists(json_p))

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
