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
    LabWorkstationConfig,
    SampleAnalyzerConfig,
    ChemicalDrumConfig,
    CoolantPumpConfig,
    ReactorControlConsoleConfig,
    PowerTransformerConfig,
    FuseBoxConfig,
    BatteryBankConfig,
    GeneratorUnitConfig,
    CoolantPipeJunctionConfig,
)
from procedural_assets.core.manifest import find_manifest_for_family
from procedural_assets.export.glb_exporter import GLBExporter

class TestBatchDFamilies(unittest.TestCase):
    """Test suite for Lote D: Engineering, Fluid Loops, Reactor Controls & Power Distribution (63-72)."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_batch_d")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_063_lab_workstation(self):
        cfg = LabWorkstationConfig(name="test_lab_workstation", has_sink=True, has_upper_shelf=True, has_terminal_screen=True, drawer_units=2)
        _, gen_cls = GENERATOR_REGISTRY["lab_workstation"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"LabWorkstation validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("lab_workstation")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.laboratory.lab_workstation")
        self.assertGreaterEqual(len(m.presets), 2)

    def test_064_sample_analyzer(self):
        cfg = SampleAnalyzerConfig(name="test_sample_analyzer", tray_extended=0.15, analyzer_state="processing", has_barcode_scanner=True, has_thermal_printer=True)
        _, gen_cls = GENERATOR_REGISTRY["sample_analyzer"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"SampleAnalyzer validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("sample_analyzer")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.laboratory.sample_analyzer")

    def test_065_chemical_drum(self):
        cfg = ChemicalDrumConfig(name="test_chemical_drum", rib_count=2, hazard_type="toxic", has_bung_caps=True, has_spill_residue=True)
        _, gen_cls = GENERATOR_REGISTRY["chemical_drum"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"ChemicalDrum validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 100)

        m = find_manifest_for_family("chemical_drum")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.cargo.chemical_drum")

    def test_066_coolant_pump(self):
        cfg = CoolantPumpConfig(name="test_coolant_pump", has_pressure_gauge=True, has_bypass_valve=True, motor_fins_count=5, pump_status="nominal")
        _, gen_cls = GENERATOR_REGISTRY["coolant_pump"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CoolantPump validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("coolant_pump")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.engineering.coolant_pump")

    def test_067_reactor_control_console(self):
        cfg = ReactorControlConsoleConfig(name="test_reactor_console", screen_count=3, has_scram_switch=True, dial_gauge_count=4, reactor_state="nominal")
        _, gen_cls = GENERATOR_REGISTRY["reactor_control_console"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"ReactorControlConsole validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 250)

        m = find_manifest_for_family("reactor_control_console")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.engineering.reactor_control_console")

    def test_068_power_transformer(self):
        cfg = PowerTransformerConfig(name="test_power_transformer", insulator_count=3, cooling_radiators_sides=True, has_expansion_tank=True)
        _, gen_cls = GENERATOR_REGISTRY["power_transformer"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"PowerTransformer validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 250)

        m = find_manifest_for_family("power_transformer")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.engineering.power_transformer")

    def test_069_fuse_box(self):
        cfg = FuseBoxConfig(name="test_fuse_box", door_open_angle=0.0, fuse_rows=2, fuses_per_row=4, missing_fuse=True, has_main_switch=True)
        _, gen_cls = GENERATOR_REGISTRY["fuse_box"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"FuseBox validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 120)

        m = find_manifest_for_family("fuse_box")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.engineering.fuse_box")

    def test_070_battery_bank(self):
        cfg = BatteryBankConfig(name="test_battery_bank", tier_count=3, batteries_per_tier=4, has_busbars=True, has_charge_monitor=True, charge_state="nominal")
        _, gen_cls = GENERATOR_REGISTRY["battery_bank"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"BatteryBank validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("battery_bank")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.engineering.battery_bank")

    def test_071_generator_unit(self):
        cfg = GeneratorUnitConfig(name="test_generator_unit", has_exhaust_stack=True, has_control_panel=True, has_service_hatch=True, generator_status="running")
        _, gen_cls = GENERATOR_REGISTRY["generator_unit"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"GeneratorUnit validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("generator_unit")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.engineering.generator_unit")

    def test_072_coolant_pipe_junction(self):
        cfg = CoolantPipeJunctionConfig(name="test_coolant_pipe_junction", junction_type="cross_4way", has_isolation_valves=True, has_pressure_sensor=True, has_thermal_insulation=True)
        _, gen_cls = GENERATOR_REGISTRY["coolant_pipe_junction"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CoolantPipeJunction validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("coolant_pipe_junction")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.infrastructure.coolant_pipe_junction")

    def test_glb_export_batch_d(self):
        cfg = ChemicalDrumConfig(name="export_chemical_drum")
        _, gen_cls = GENERATOR_REGISTRY["chemical_drum"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
        glb_out, json_out = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="ChemicalDrumGenerator"
        )
        self.assertTrue(os.path.exists(glb_out))
        self.assertGreater(os.path.getsize(glb_out), 500)
        self.assertTrue(os.path.exists(json_out))

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
