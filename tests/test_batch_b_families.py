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
    CryoStasisPodConfig,
    ConsciousnessArchiveConfig,
    NeuralInterfaceChairConfig,
    MemoryExtractionTerminalConfig,
    OxygenRegulatorConfig,
    OxygenTankConfig,
    PressureDoorControlConfig,
    AirlockChamberConfig,
    PressureIndicatorConfig,
)
from procedural_assets.core.manifest import find_manifest_for_family
from procedural_assets.export.glb_exporter import GLBExporter

class TestBatchBFamilies(unittest.TestCase):
    """Test suite for Lote B: Core Life Support & Narrative Families (45-53)."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_batch_b")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_045_cryo_stasis_pod(self):
        cfg = CryoStasisPodConfig(name="test_cryo", pod_state="occupied", door_open_angle=30.0, frost_level=0.6)
        _, gen_cls = GENERATOR_REGISTRY["cryo_stasis_pod"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CryoStasisPod validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        # Manifest check
        m = find_manifest_for_family("cryo_stasis_pod")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.medical.cryo_stasis_pod")
        self.assertGreaterEqual(len(m.presets), 2)

    def test_046_consciousness_archive(self):
        cfg = ConsciousnessArchiveConfig(name="test_archive", bay_rows=5, cartridge_density=0.8)
        _, gen_cls = GENERATOR_REGISTRY["consciousness_archive"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"ConsciousnessArchive validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        # Manifest check
        m = find_manifest_for_family("consciousness_archive")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.infrastructure.consciousness_archive")

    def test_047_neural_interface_chair(self):
        cfg = NeuralInterfaceChairConfig(name="test_chair", backrest_angle=25.0, has_sensor_arch=True)
        _, gen_cls = GENERATOR_REGISTRY["neural_interface_chair"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"NeuralInterfaceChair validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 120)

        # Manifest check
        m = find_manifest_for_family("neural_interface_chair")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.medical.neural_interface_chair")

    def test_048_memory_extraction_terminal(self):
        cfg = MemoryExtractionTerminalConfig(name="test_terminal", mount_style="pedestal", screen_color="amber")
        _, gen_cls = GENERATOR_REGISTRY["memory_extraction_terminal"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"MemoryExtractionTerminal validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        # Manifest check
        m = find_manifest_for_family("memory_extraction_terminal")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.infrastructure.memory_extraction_terminal")

    def test_049_oxygen_regulator(self):
        cfg = OxygenRegulatorConfig(name="test_regulator", gauge_count=2, has_brass_valves=True)
        _, gen_cls = GENERATOR_REGISTRY["oxygen_regulator"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"OxygenRegulator validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 100)

        # Manifest check
        m = find_manifest_for_family("oxygen_regulator")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.fixtures.oxygen_regulator")

    def test_050_oxygen_tank(self):
        cfg = OxygenTankConfig(name="test_tank", tank_height=1.2, tank_color="cyan")
        _, gen_cls = GENERATOR_REGISTRY["oxygen_tank"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"OxygenTank validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 80)

        # Manifest check
        m = find_manifest_for_family("oxygen_tank")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.fixtures.oxygen_tank")

    def test_051_pressure_door_control(self):
        cfg = PressureDoorControlConfig(name="test_control", status_light="green", has_keypad=True)
        _, gen_cls = GENERATOR_REGISTRY["pressure_door_control"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"PressureDoorControl validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 60)

        # Manifest check
        m = find_manifest_for_family("pressure_door_control")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.fixtures.pressure_door_control")

    def test_052_airlock_chamber(self):
        cfg = AirlockChamberConfig(name="test_airlock", inner_door_open=0.0, outer_door_open=0.5)
        _, gen_cls = GENERATOR_REGISTRY["airlock_chamber"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"AirlockChamber validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 250)

        # Manifest check
        m = find_manifest_for_family("airlock_chamber")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.architecture.airlock_chamber")

    def test_053_pressure_indicator(self):
        cfg = PressureIndicatorConfig(name="test_indicator", diameter=0.5, needle_angle=45.0)
        _, gen_cls = GENERATOR_REGISTRY["pressure_indicator"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"PressureIndicator validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 60)

        # Manifest check
        m = find_manifest_for_family("pressure_indicator")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.fixtures.pressure_indicator")

    def test_glb_export_batch_b(self):
        cfg = OxygenTankConfig(name="export_tank", tank_color="white")
        _, gen_cls = GENERATOR_REGISTRY["oxygen_tank"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
        glb_out, json_out = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="OxygenTankGenerator"
        )
        self.assertTrue(os.path.exists(glb_out))
        self.assertGreater(os.path.getsize(glb_out), 500)
        self.assertTrue(os.path.exists(json_out))

if __name__ == "__main__":
    unittest.main()
