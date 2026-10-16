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
    SuitRackConfig,
    EvaSuitStandConfig,
    HelmetStorageConfig,
    DeconChamberConfig,
    QuarantineBedConfig,
    SpecimenFreezerConfig,
    BiohazardBinConfig,
    SurgicalLightConfig,
    MicroscopeConfig,
)
from procedural_assets.core.manifest import find_manifest_for_family
from procedural_assets.export.glb_exporter import GLBExporter

class TestBatchCFamilies(unittest.TestCase):
    """Test suite for Lote C: Medical, Biosecurity, EVA Equipment & Research Laboratory (54-62)."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_batch_c")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_054_suit_rack(self):
        cfg = SuitRackConfig(name="test_suit_rack", suit_positions=4, occupied_suits=3)
        _, gen_cls = GENERATOR_REGISTRY["suit_rack"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"SuitRack validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("suit_rack")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.fixtures.suit_rack")
        self.assertGreaterEqual(len(m.presets), 2)

    def test_055_eva_suit_stand(self):
        cfg = EvaSuitStandConfig(name="test_suit_stand", has_suit_mounted=True, has_service_umbilical=True)
        _, gen_cls = GENERATOR_REGISTRY["eva_suit_stand"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"EvaSuitStand validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("eva_suit_stand")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.fixtures.eva_suit_stand")

    def test_056_helmet_storage(self):
        cfg = HelmetStorageConfig(name="test_helmet_storage", grid_rows=3, grid_cols=2, helmet_density=0.65)
        _, gen_cls = GENERATOR_REGISTRY["helmet_storage"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"HelmetStorage validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("helmet_storage")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.furniture.helmet_storage")

    def test_057_decon_chamber(self):
        cfg = DeconChamberConfig(name="test_decon_chamber", door_open_angle=0.0, cycle_state="idle")
        _, gen_cls = GENERATOR_REGISTRY["decon_chamber"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"DeconChamber validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 250)

        m = find_manifest_for_family("decon_chamber")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.medical.decon_chamber")

    def test_058_quarantine_bed(self):
        cfg = QuarantineBedConfig(name="test_quarantine_bed", rails_raised=True, has_restraint_straps=True)
        _, gen_cls = GENERATOR_REGISTRY["quarantine_bed"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"QuarantineBed validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("quarantine_bed")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.medical.quarantine_bed")

    def test_059_specimen_freezer(self):
        cfg = SpecimenFreezerConfig(name="test_specimen_freezer", door_open_angle=0.0, tray_count=4)
        _, gen_cls = GENERATOR_REGISTRY["specimen_freezer"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"SpecimenFreezer validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 200)

        m = find_manifest_for_family("specimen_freezer")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.laboratory.specimen_freezer")

    def test_060_biohazard_bin(self):
        cfg = BiohazardBinConfig(name="test_biohazard_bin", lid_open_angle=0.0, has_foot_pedal=True)
        _, gen_cls = GENERATOR_REGISTRY["biohazard_bin"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"BiohazardBin validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 100)

        m = find_manifest_for_family("biohazard_bin")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.medical.biohazard_bin")

    def test_061_surgical_light(self):
        cfg = SurgicalLightConfig(name="test_surgical_light", dish_diameter=0.75, reflector_count=4)
        _, gen_cls = GENERATOR_REGISTRY["surgical_light"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"SurgicalLight validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("surgical_light")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.medical.surgical_light")

    def test_062_microscope(self):
        cfg = MicroscopeConfig(name="test_microscope", objective_count=3, eyepiece_type="binocular")
        _, gen_cls = GENERATOR_REGISTRY["microscope"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"Microscope validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)

        m = find_manifest_for_family("microscope")
        self.assertIsNotNone(m)
        self.assertEqual(m.id, "below_nominal.laboratory.microscope")

    def test_glb_export_batch_c(self):
        cfg = BiohazardBinConfig(name="export_biohazard_bin")
        _, gen_cls = GENERATOR_REGISTRY["biohazard_bin"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
        glb_out, json_out = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="BiohazardBinGenerator"
        )
        self.assertTrue(os.path.exists(glb_out))
        self.assertGreater(os.path.getsize(glb_out), 500)
        self.assertTrue(os.path.exists(json_out))

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
