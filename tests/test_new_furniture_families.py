import unittest
import os
import shutil
import bpy

from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    OfficeDeskConfig,
    OfficeChairConfig,
    SignPlacardConfig,
    TrashBinConfig,
    LightFixtureConfig,
    FireExtinguisherConfig,
    VentGrateConfig,
    CableBundleConfig
)
from procedural_assets.export.glb_exporter import GLBExporter

class TestNewFurnitureFamilies(unittest.TestCase):
    """Test suite for the 8 new facility furniture, props, signs, lights, and fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_new_families")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_office_desk_generation(self):
        config = OfficeDeskConfig(
            seed=101,
            name="test_desk",
            leg_style="panel_sides",
            pedestal_layout="dual_pedestals",
            drawer_open_style="top_open",
            has_partition_screen=True
        )
        _, gen_cls = GENERATOR_REGISTRY["office_desk"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 100)
        self.assertLessEqual(report.triangle_count, config.target_tri_budget * 1.25)
        self.assertAlmostEqual(report.dimensions[0], config.width, delta=0.08)

    def test_office_chair_generation_and_variants(self):
        # Test broken armrest variant
        config = OfficeChairConfig(
            seed=202,
            name="test_chair",
            base_style="five_star_casters",
            armrest_style="one_broken",
            backrest_style="high_back_headrest"
        )
        _, gen_cls = GENERATOR_REGISTRY["office_chair"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 150)
        self.assertLessEqual(report.triangle_count, config.target_tri_budget * 1.25)

    def test_sign_placard_damage_and_hanging(self):
        config = SignPlacardConfig(
            seed=303,
            name="test_sign",
            sign_type="hazard_biohazard",
            mount_type="ceiling_hanging",
            damage_style="hanging_crooked"
        )
        _, gen_cls = GENERATOR_REGISTRY["sign_placard"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 20)

    def test_trash_bin_pedal_and_overflowing(self):
        config = TrashBinConfig(
            seed=404,
            name="test_trash",
            bin_type="pedal_can",
            lid_state="ajar",
            has_foot_pedal=True,
            has_overflowing_trash=True
        )
        _, gen_cls = GENERATOR_REGISTRY["trash_bin"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 80)

    def test_light_fixture_flickering(self):
        config = LightFixtureConfig(
            seed=505,
            name="test_light",
            fixture_type="fluorescent_troffer",
            lighting_state="flickering_one_dead",
            has_wire_guard=True,
            has_dangling_wire=True
        )
        _, gen_cls = GENERATOR_REGISTRY["light_fixture"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 80)

    def test_fire_extinguisher_cabinet(self):
        config = FireExtinguisherConfig(
            seed=606,
            name="test_extinguisher",
            mount_style="emergency_cabinet",
            cabinet_glass_state="broken_shattered"
        )
        _, gen_cls = GENERATOR_REGISTRY["fire_extinguisher"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 120)

    def test_vent_grate_hanging_escape(self):
        config = VentGrateConfig(
            seed=707,
            name="test_vent",
            grate_state="hanging_by_one_screw",
            has_fan_blades=True
        )
        _, gen_cls = GENERATOR_REGISTRY["vent_grate"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 80)

    def test_cable_bundle_ladder_and_severed(self):
        config = CableBundleConfig(
            seed=808,
            name="test_cables",
            bundle_type="ladder_rack_tray",
            cable_count=4,
            has_severed_wire=True
        )
        _, gen_cls = GENERATOR_REGISTRY["cable_bundle"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 80)

    def test_export_and_reimport_all_new_families(self):
        """Verify all 8 new families export cleanly to GLB + JSON and re-import into Blender."""
        sample_configs = [
            (OfficeDeskConfig(name="exp_office_desk", seed=11), "office_desk"),
            (OfficeChairConfig(name="exp_office_chair", seed=22), "office_chair"),
            (SignPlacardConfig(name="exp_sign", seed=33), "sign_placard"),
            (TrashBinConfig(name="exp_trash", seed=44), "trash_bin"),
            (LightFixtureConfig(name="exp_light", seed=55), "light_fixture"),
            (FireExtinguisherConfig(name="exp_extinguisher", seed=66), "fire_extinguisher"),
            (VentGrateConfig(name="exp_vent", seed=77), "vent_grate"),
            (CableBundleConfig(name="exp_cable", seed=88), "cable_bundle"),
        ]

        for cfg, family_key in sample_configs:
            _, gen_cls = GENERATOR_REGISTRY[family_key]
            gen = gen_cls()
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)

            glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
            out_glb, out_json = GLBExporter.export(obj, cfg, rep, glb_path, gen_cls.__name__)

            self.assertTrue(os.path.exists(out_glb))
            self.assertTrue(os.path.exists(out_json))
            self.assertGreater(os.path.getsize(out_glb), 1000)

            # Re-import into Blender
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=out_glb)
            imported_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            self.assertGreaterEqual(len(imported_objs), 1)

if __name__ == "__main__":
    unittest.main()
