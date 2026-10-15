import unittest
import os
import shutil
import bpy

from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    CrewBedConfig,
    BunkBedConfig,
    NightstandConfig,
    RadiatorHeaterConfig,
    OfficeDoorConfig
)
from procedural_assets.export.glb_exporter import GLBExporter

class TestLivingQuartersFamilies(unittest.TestCase):
    """Test suite for Crew Bed, Bunk Bed, Nightstand, Radiator Heater, and Office Door families."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_living_quarters")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_crew_bed_generation_and_variants(self):
        # 1. Standard crew cot
        cfg_cot = CrewBedConfig(
            seed=101,
            name="test_crew_cot",
            bed_type="crew_cot",
            mattress_state="rumpled_disheveled",
            has_under_drawers=True,
            blanket_color="emergency_orange"
        )
        _, gen_cls = GENERATOR_REGISTRY["crew_bed"]
        gen = gen_cls()
        obj_cot = gen.generate(cfg_cot)
        rep_cot = gen.validate(obj_cot, cfg_cot)
        self.assertTrue(rep_cot.is_valid)
        self.assertGreater(rep_cot.triangle_count, 80)
        self.assertLessEqual(rep_cot.triangle_count, cfg_cot.target_tri_budget * 1.35)

        # 2. Medical gurney with inclined headrest and guardrails
        cfg_gurney = CrewBedConfig(
            seed=102,
            name="test_medical_gurney",
            bed_type="medical_gurney",
            headrest_incline=25.0,
            has_guardrails=True,
            blanket_color="medical_blue"
        )
        obj_gurney = gen.generate(cfg_gurney)
        rep_gurney = gen.validate(obj_gurney, cfg_gurney)
        self.assertTrue(rep_gurney.is_valid)
        self.assertGreater(rep_gurney.triangle_count, 120)

        # 3. Enclosed pod
        cfg_pod = CrewBedConfig(
            seed=103,
            name="test_enclosed_pod",
            bed_type="enclosed_pod"
        )
        obj_pod = gen.generate(cfg_pod)
        rep_pod = gen.validate(obj_pod, cfg_pod)
        self.assertTrue(rep_pod.is_valid)

    def test_bunk_bed_generation_and_variants(self):
        # 1. Tubular metal bunk bed
        cfg_metal = BunkBedConfig(
            seed=201,
            name="test_bunk_metal",
            frame_style="tubular_metal",
            ladder_position="front_right",
            upper_guardrail=True,
            has_reading_lights=True,
            has_storage_lockers=True,
            blanket_color="station_gray"
        )
        _, gen_cls = GENERATOR_REGISTRY["bunk_bed"]
        gen = gen_cls()
        obj_metal = gen.generate(cfg_metal)
        rep_metal = gen.validate(obj_metal, cfg_metal)
        self.assertTrue(rep_metal.is_valid)
        self.assertGreater(rep_metal.triangle_count, 150)
        self.assertLessEqual(rep_metal.triangle_count, cfg_metal.target_tri_budget * 1.35)

        # 2. Bulkhead integrated capsule bunk
        cfg_bulkhead = BunkBedConfig(
            seed=202,
            name="test_bunk_bulkhead",
            frame_style="reinforced_bulkhead",
            lower_bunk_state="bare_foam_stained",
            upper_bunk_state="empty_storage"
        )
        obj_bulkhead = gen.generate(cfg_bulkhead)
        rep_bulkhead = gen.validate(obj_bulkhead, cfg_bulkhead)
        self.assertTrue(rep_bulkhead.is_valid)

    def test_nightstand_generation_and_variants(self):
        # 1. Crew locker cubby with lamp
        cfg_cubby = NightstandConfig(
            seed=301,
            name="test_nightstand_cubby",
            stand_type="crew_locker_cubby",
            drawer_count=2,
            drawer_open_ratio=0.25,
            has_raised_rim=True,
            has_bedside_lamp=True,
            lamp_state="flickering"
        )
        _, gen_cls = GENERATOR_REGISTRY["nightstand"]
        gen = gen_cls()
        obj_cubby = gen.generate(cfg_cubby)
        rep_cubby = gen.validate(obj_cubby, cfg_cubby)
        self.assertTrue(rep_cubby.is_valid)
        self.assertGreater(rep_cubby.triangle_count, 60)
        self.assertLessEqual(rep_cubby.triangle_count, cfg_cubby.target_tri_budget * 1.35)

        # 2. Medical tray cart with swivel tray
        cfg_cart = NightstandConfig(
            seed=302,
            name="test_nightstand_cart",
            stand_type="medical_tray_cart",
            has_swivel_tray=True,
            has_bedside_lamp=False
        )
        obj_cart = gen.generate(cfg_cart)
        rep_cart = gen.validate(obj_cart, cfg_cart)
        self.assertTrue(rep_cart.is_valid)

    def test_radiator_heater_generation_and_variants(self):
        # 1. Wall radiator fins
        cfg_rad = RadiatorHeaterConfig(
            seed=401,
            name="test_radiator_fins",
            heater_type="wall_radiator_fins",
            fin_count=10,
            has_thermostat_dial=True,
            has_steam_pipe=True,
            is_operational=True
        )
        _, gen_cls = GENERATOR_REGISTRY["radiator_heater"]
        gen = gen_cls()
        obj_rad = gen.generate(cfg_rad)
        rep_rad = gen.validate(obj_rad, cfg_rad)
        self.assertTrue(rep_rad.is_valid)
        self.assertGreater(rep_rad.triangle_count, 80)
        self.assertLessEqual(rep_rad.triangle_count, cfg_rad.target_tri_budget * 1.35)

        # 2. Convector blower
        cfg_convector = RadiatorHeaterConfig(
            seed=402,
            name="test_convector_blower",
            heater_type="convector_blower",
            damage_state="battered_bent_fins"
        )
        obj_convector = gen.generate(cfg_convector)
        rep_convector = gen.validate(obj_convector, cfg_convector)
        self.assertTrue(rep_convector.is_valid)

        # 3. Space tower heater
        cfg_tower = RadiatorHeaterConfig(
            seed=403,
            name="test_space_tower",
            heater_type="space_tower_heater",
            fin_count=6
        )
        obj_tower = gen.generate(cfg_tower)
        rep_tower = gen.validate(obj_tower, cfg_tower)
        self.assertTrue(rep_tower.is_valid)

    def test_office_door_generation_and_variants(self):
        # 1. Single swing door ajar
        cfg_single = OfficeDoorConfig(
            seed=501,
            name="test_office_door_single",
            door_style="single_swing",
            glass_type="wired_safety_glass",
            open_angle_deg=35.0,
            handle_type="horizontal_push_bar",
            has_kickplate=True,
            has_transom=True
        )
        _, gen_cls = GENERATOR_REGISTRY["office_door"]
        gen = gen_cls()
        obj_single = gen.generate(cfg_single)
        rep_single = gen.validate(obj_single, cfg_single)
        self.assertTrue(rep_single.is_valid)
        self.assertGreater(rep_single.triangle_count, 80)
        self.assertLessEqual(rep_single.triangle_count, cfg_single.target_tri_budget * 1.35)

        # 2. Double swing door open
        cfg_double = OfficeDoorConfig(
            seed=502,
            name="test_office_door_double",
            door_style="double_swing",
            open_angle_deg=60.0,
            glass_damage="cracked_spiderweb"
        )
        obj_double = gen.generate(cfg_double)
        rep_double = gen.validate(obj_double, cfg_double)
        self.assertTrue(rep_double.is_valid)

        # 3. Sliding pocket door
        cfg_sliding = OfficeDoorConfig(
            seed=503,
            name="test_office_door_sliding",
            door_style="sliding_pocket",
            open_angle_deg=45.0
        )
        obj_sliding = gen.generate(cfg_sliding)
        rep_sliding = gen.validate(obj_sliding, cfg_sliding)
        self.assertTrue(rep_sliding.is_valid)

    def test_export_and_reimport_all_five_families(self):
        """Verify all 5 living quarters / office families export cleanly to GLB + JSON and re-import."""
        sample_configs = [
            CrewBedConfig(name="exp_crew_bed", seed=111),
            BunkBedConfig(name="exp_bunk_bed", seed=222),
            NightstandConfig(name="exp_nightstand", seed=333),
            RadiatorHeaterConfig(name="exp_radiator_heater", seed=444),
            OfficeDoorConfig(name="exp_office_door", seed=555),
        ]

        for cfg in sample_configs:
            family_key = "_".join(cfg.name.split("_")[1:])
            self.assertIn(family_key, GENERATOR_REGISTRY, f"Generator {family_key} not in registry")

            _, gen_cls = GENERATOR_REGISTRY[family_key]
            gen = gen_cls()
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)

            glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
            out_glb, out_json = GLBExporter.export(obj, cfg, rep, glb_path, gen_cls.__name__)

            self.assertTrue(os.path.exists(out_glb), f"GLB does not exist: {out_glb}")
            self.assertTrue(os.path.exists(out_json), f"JSON does not exist: {out_json}")
            self.assertGreater(os.path.getsize(out_glb), 1000)

            # Re-import into Blender to verify GLB compatibility
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=out_glb)
            imported_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            self.assertGreaterEqual(len(imported_objs), 1, f"Failed re-importing {cfg.name}")

if __name__ == "__main__":
    unittest.main()
