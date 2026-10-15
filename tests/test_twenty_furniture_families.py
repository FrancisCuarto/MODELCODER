import unittest
import os
import shutil
import bpy

from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    AutopsyTableConfig,
    MedicalScreenConfig,
    MorgueGurneyConfig,
    ChemicalCabinetConfig,
    RestraintChairConfig,
    MessTableConfig,
    RationAutomatConfig,
    CanteenCounterConfig,
    FileCabinetConfig,
    LockerBenchConfig,
    WorkBenchConfig,
    HeavyShelvingConfig,
    ToolChestCartConfig,
    SafetyShowerConfig,
    HydroponicTrayBedConfig,
    SecurityDeskConfig,
    WeaponsRackConfig,
    BridgeConsoleDeskConfig,
    SpaceToiletConfig,
    ScrubSinkConfig,
)
from procedural_assets.export.glb_exporter import GLBExporter

class TestTwentyFurnitureFamilies(unittest.TestCase):
    """Test suite for the 20 new station furniture families."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_twenty_furniture")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_group1_medical_and_restraint(self):
        # 1. autopsy_table
        cfg_autopsy = AutopsyTableConfig(name="test_autopsy", restraint_straps="buckled", overhead_lamp=True)
        _, gen_cls = GENERATOR_REGISTRY["autopsy_table"]
        gen = gen_cls()
        obj = gen.generate(cfg_autopsy)
        rep = gen.validate(obj, cfg_autopsy)
        self.assertTrue(rep.is_valid)
        self.assertGreater(rep.triangle_count, 100)

        # 2. medical_screen
        cfg_screen = MedicalScreenConfig(name="test_screen", screen_type="three_panel", curtain_damage="blood_splatter")
        _, gen_cls = GENERATOR_REGISTRY["medical_screen"]
        gen = gen_cls()
        obj = gen.generate(cfg_screen)
        rep = gen.validate(obj, cfg_screen)
        self.assertTrue(rep.is_valid)

        # 3. morgue_gurney
        cfg_gurney = MorgueGurneyConfig(name="test_morgue_gurney", gurney_type="body_bag_closed")
        _, gen_cls = GENERATOR_REGISTRY["morgue_gurney"]
        gen = gen_cls()
        obj = gen.generate(cfg_gurney)
        rep = gen.validate(obj, cfg_gurney)
        self.assertTrue(rep.is_valid)

        # 4. chemical_cabinet
        cfg_chem = ChemicalCabinetConfig(name="test_chem_cab", door_state="left_open", has_padlock=True)
        _, gen_cls = GENERATOR_REGISTRY["chemical_cabinet"]
        gen = gen_cls()
        obj = gen.generate(cfg_chem)
        rep = gen.validate(obj, cfg_chem)
        self.assertTrue(rep.is_valid)

        # 5. restraint_chair
        cfg_chair = RestraintChairConfig(name="test_restraint_chair", arm_straps="torn", iv_pole=True)
        _, gen_cls = GENERATOR_REGISTRY["restraint_chair"]
        gen = gen_cls()
        obj = gen.generate(cfg_chair)
        rep = gen.validate(obj, cfg_chair)
        self.assertTrue(rep.is_valid)

    def test_group2_canteen_and_office(self):
        # 6. mess_table
        cfg_mess = MessTableConfig(name="test_mess_table", stool_count=4, stool_swing_state="random_pulled")
        _, gen_cls = GENERATOR_REGISTRY["mess_table"]
        gen = gen_cls()
        obj = gen.generate(cfg_mess)
        rep = gen.validate(obj, cfg_mess)
        self.assertTrue(rep.is_valid)

        # 7. ration_automat
        cfg_automat = RationAutomatConfig(name="test_automat", dispenser_state="jammed_door")
        _, gen_cls = GENERATOR_REGISTRY["ration_automat"]
        gen = gen_cls()
        obj = gen.generate(cfg_automat)
        rep = gen.validate(obj, cfg_automat)
        self.assertTrue(rep.is_valid)

        # 8. canteen_counter
        cfg_canteen = CanteenCounterConfig(name="test_canteen", roll_up_shutter="half_open", has_tray_rails=True)
        _, gen_cls = GENERATOR_REGISTRY["canteen_counter"]
        gen = gen_cls()
        obj = gen.generate(cfg_canteen)
        rep = gen.validate(obj, cfg_canteen)
        self.assertTrue(rep.is_valid)

        # 9. file_cabinet
        cfg_file = FileCabinetConfig(name="test_file_cab", drawer_open_mode="looted_papers")
        _, gen_cls = GENERATOR_REGISTRY["file_cabinet"]
        gen = gen_cls()
        obj = gen.generate(cfg_file)
        rep = gen.validate(obj, cfg_file)
        self.assertTrue(rep.is_valid)

        # 10. locker_bench
        cfg_bench = LockerBenchConfig(name="test_locker_bench", bench_type="perforated_metal", has_forgotten_gear=True)
        _, gen_cls = GENERATOR_REGISTRY["locker_bench"]
        gen = gen_cls()
        obj = gen.generate(cfg_bench)
        rep = gen.validate(obj, cfg_bench)
        self.assertTrue(rep.is_valid)

    def test_group3_maintenance_and_botanical(self):
        # 11. work_bench
        cfg_wb = WorkBenchConfig(name="test_workbench", has_vise=True, has_overhead_light=True)
        _, gen_cls = GENERATOR_REGISTRY["work_bench"]
        gen = gen_cls()
        obj = gen.generate(cfg_wb)
        rep = gen.validate(obj, cfg_wb)
        self.assertTrue(rep.is_valid)

        # 12. heavy_shelving
        cfg_shelving = HeavyShelvingConfig(name="test_shelving", shelf_type="cargo_storage", bent_shelf_index=1)
        _, gen_cls = GENERATOR_REGISTRY["heavy_shelving"]
        gen = gen_cls()
        obj = gen.generate(cfg_shelving)
        rep = gen.validate(obj, cfg_shelving)
        self.assertTrue(rep.is_valid)

        # 13. tool_chest_cart
        cfg_toolcart = ToolChestCartConfig(name="test_toolcart", drawer_open_style="top_drawer_open")
        _, gen_cls = GENERATOR_REGISTRY["tool_chest_cart"]
        gen = gen_cls()
        obj = gen.generate(cfg_toolcart)
        rep = gen.validate(obj, cfg_toolcart)
        self.assertTrue(rep.is_valid)

        # 14. safety_shower
        cfg_shower = SafetyShowerConfig(name="test_shower", has_pull_chain=True, has_eyewash_bowl=True)
        _, gen_cls = GENERATOR_REGISTRY["safety_shower"]
        gen = gen_cls()
        obj = gen.generate(cfg_shower)
        rep = gen.validate(obj, cfg_shower)
        self.assertTrue(rep.is_valid)

        # 15. hydroponic_tray_bed
        cfg_hydro = HydroponicTrayBedConfig(name="test_hydro", plant_state="healthy_green", uv_light_state="on_violet")
        _, gen_cls = GENERATOR_REGISTRY["hydroponic_tray_bed"]
        gen = gen_cls()
        obj = gen.generate(cfg_hydro)
        rep = gen.validate(obj, cfg_hydro)
        self.assertTrue(rep.is_valid)

    def test_group4_security_and_sanitation(self):
        # 16. security_desk
        cfg_sec = SecurityDeskConfig(name="test_sec_desk", has_cctv_monitor=True, bulletproof_glass=True)
        _, gen_cls = GENERATOR_REGISTRY["security_desk"]
        gen = gen_cls()
        obj = gen.generate(cfg_sec)
        rep = gen.validate(obj, cfg_sec)
        self.assertTrue(rep.is_valid)

        # 17. weapons_rack
        cfg_weapons = WeaponsRackConfig(name="test_weapons_rack", is_locked=True, occupancy_ratio=0.8)
        _, gen_cls = GENERATOR_REGISTRY["weapons_rack"]
        gen = gen_cls()
        obj = gen.generate(cfg_weapons)
        rep = gen.validate(obj, cfg_weapons)
        self.assertTrue(rep.is_valid)

        # 18. bridge_console_desk
        cfg_bridge = BridgeConsoleDeskConfig(name="test_bridge_console", crt_count=3, chair_included=True)
        _, gen_cls = GENERATOR_REGISTRY["bridge_console_desk"]
        gen = gen_cls()
        obj = gen.generate(cfg_bridge)
        rep = gen.validate(obj, cfg_bridge)
        self.assertTrue(rep.is_valid)

        # 19. space_toilet
        cfg_toilet = SpaceToiletConfig(name="test_space_toilet", lid_state="closed", has_thigh_restraints=True)
        _, gen_cls = GENERATOR_REGISTRY["space_toilet"]
        gen = gen_cls()
        obj = gen.generate(cfg_toilet)
        rep = gen.validate(obj, cfg_toilet)
        self.assertTrue(rep.is_valid)

        # 20. scrub_sink
        cfg_sink = ScrubSinkConfig(name="test_scrub_sink", drain_state="blood_stained", faucet_type="elbow_blade_levers")
        _, gen_cls = GENERATOR_REGISTRY["scrub_sink"]
        gen = gen_cls()
        obj = gen.generate(cfg_sink)
        rep = gen.validate(obj, cfg_sink)
        self.assertTrue(rep.is_valid)

    def test_export_all_twenty_to_glb_and_reimport(self):
        """Verify each of the 20 new families exports to a valid GLB and reimports into Blender."""
        configs = [
            AutopsyTableConfig(name="exp_autopsy_table", seed=10),
            MedicalScreenConfig(name="exp_medical_screen", seed=20),
            MorgueGurneyConfig(name="exp_morgue_gurney", seed=30),
            ChemicalCabinetConfig(name="exp_chemical_cabinet", seed=40),
            RestraintChairConfig(name="exp_restraint_chair", seed=50),
            MessTableConfig(name="exp_mess_table", seed=60),
            RationAutomatConfig(name="exp_ration_automat", seed=70),
            CanteenCounterConfig(name="exp_canteen_counter", seed=80),
            FileCabinetConfig(name="exp_file_cabinet", seed=90),
            LockerBenchConfig(name="exp_locker_bench", seed=100),
            WorkBenchConfig(name="exp_work_bench", seed=110),
            HeavyShelvingConfig(name="exp_heavy_shelving", seed=120),
            ToolChestCartConfig(name="exp_tool_chest_cart", seed=130),
            SafetyShowerConfig(name="exp_safety_shower", seed=140),
            HydroponicTrayBedConfig(name="exp_hydroponic_tray_bed", seed=150),
            SecurityDeskConfig(name="exp_security_desk", seed=160),
            WeaponsRackConfig(name="exp_weapons_rack", seed=170),
            BridgeConsoleDeskConfig(name="exp_bridge_console_desk", seed=180),
            SpaceToiletConfig(name="exp_space_toilet", seed=190),
            ScrubSinkConfig(name="exp_scrub_sink", seed=200),
        ]

        for cfg in configs:
            family_key = cfg.name.replace("exp_", "")
            self.assertIn(family_key, GENERATOR_REGISTRY, f"Family {family_key} not in registry")

            _, gen_cls = GENERATOR_REGISTRY[family_key]
            gen = gen_cls()
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)

            glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
            out_glb, out_json = GLBExporter.export(obj, cfg, rep, glb_path, gen_cls.__name__)

            self.assertTrue(os.path.exists(out_glb), f"Missing GLB for {cfg.name}")
            self.assertTrue(os.path.exists(out_json), f"Missing JSON for {cfg.name}")
            self.assertGreater(os.path.getsize(out_glb), 500)

            # Re-import test
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=out_glb)
            imported_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            self.assertGreaterEqual(len(imported_objs), 1, f"Failed re-importing {cfg.name}")

if __name__ == "__main__":
    unittest.main()
