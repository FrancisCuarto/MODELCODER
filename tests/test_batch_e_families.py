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
    CableTrayConfig,
    OverheadPipeSupportConfig,
    FloorGratingConfig,
    MaintenanceHatchConfig,
    LadderConfig,
    ServiceLiftDoorConfig,
    CargoPalletConfig,
    CargoContainerConfig,
)
from procedural_assets.core.manifest import find_manifest_for_family
from procedural_assets.export.glb_exporter import GLBExporter

class TestBatchEFamilies(unittest.TestCase):
    """Test suite for Lote E: Modular Infrastructure & Logistics (73-80)."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_batch_e")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_073_cable_tray(self):
        cfg = CableTrayConfig(name="test_cable_tray", has_cover=False, has_suspension_rods=True, cable_density=0.70, has_hanging_cables=True)
        _, gen_cls = GENERATOR_REGISTRY["cable_tray"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CableTray validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("cable_tray")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.infrastructure.cable_tray")
        self.assertGreaterEqual(len(m.presets), 2)

    def test_074_overhead_pipe_support(self):
        cfg = OverheadPipeSupportConfig(name="test_pipe_support", pipe_slots=3, pipe_tier_count=1, has_pipes_included=True, hanger_state="nominal")
        _, gen_cls = GENERATOR_REGISTRY["overhead_pipe_support"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"OverheadPipeSupport validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("overhead_pipe_support")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.infrastructure.overhead_pipe_support")

    def test_075_floor_grating(self):
        cfg = FloorGratingConfig(name="test_floor_grating", bar_density=8, is_raised=False, trench_state="flush", has_warning_stripe=True)
        _, gen_cls = GENERATOR_REGISTRY["floor_grating"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"FloorGrating validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("floor_grating")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.architecture.floor_grating")

    def test_076_maintenance_hatch(self):
        cfg = MaintenanceHatchConfig(name="test_maintenance_hatch", hatch_shape="square", open_angle=0.0, dogging_mechanism="central_wheel", has_interlock_light=True)
        _, gen_cls = GENERATOR_REGISTRY["maintenance_hatch"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"MaintenanceHatch validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("maintenance_hatch")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.architecture.maintenance_hatch")

    def test_077_ladder(self):
        cfg = LadderConfig(name="test_ladder", has_safety_cage=True, has_walkthrough_top=True, ladder_condition="nominal")
        _, gen_cls = GENERATOR_REGISTRY["ladder"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"Ladder validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("ladder")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.architecture.ladder")

    def test_078_service_lift_door(self):
        cfg = ServiceLiftDoorConfig(name="test_service_lift_door", door_state="closed", has_call_station=True, has_capacity_sign=True)
        _, gen_cls = GENERATOR_REGISTRY["service_lift_door"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"ServiceLiftDoor validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("service_lift_door")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.architecture.service_lift_door")

    def test_079_cargo_pallet(self):
        cfg = CargoPalletConfig(name="test_cargo_pallet", deck_style="slotted_deck", has_cargo_payload=True, has_strap_down=True)
        _, gen_cls = GENERATOR_REGISTRY["cargo_pallet"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CargoPallet validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 120)

        m = find_manifest_for_family("cargo_pallet")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.cargo.cargo_pallet")

    def test_080_cargo_container(self):
        cfg = CargoContainerConfig(name="test_cargo_container", corrugation_ribs=5, doors_open_angle=0.0, cargo_class="general_supplies")
        _, gen_cls = GENERATOR_REGISTRY["cargo_container"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CargoContainer validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("cargo_container")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.cargo.cargo_container")

    def test_glb_export_batch_e(self):
        cfg = CargoPalletConfig(name="export_cargo_pallet")
        _, gen_cls = GENERATOR_REGISTRY["cargo_pallet"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
        glb_out, json_out = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="CargoPalletGenerator"
        )
        self.assertTrue(os.path.exists(glb_out))
        self.assertGreater(os.path.getsize(glb_out), 500)
        self.assertTrue(os.path.exists(json_out))

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
