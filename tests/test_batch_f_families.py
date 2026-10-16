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
    ConveyorSegmentConfig,
    ForkliftCartConfig,
    SecurityCameraConfig,
    AccessCardReaderConfig,
    BiometricScannerConfig,
    AlarmSirenConfig,
    SpeakerIntercomConfig,
    EmergencyBeaconConfig,
    CameraMonitorConfig,
)
from procedural_assets.core.manifest import find_manifest_for_family
from procedural_assets.export.glb_exporter import GLBExporter

class TestBatchFFamilies(unittest.TestCase):
    """Test suite for Lote F: Security & Communications (81-89)."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_batch_f")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_081_conveyor_segment(self):
        cfg = ConveyorSegmentConfig(name="test_conveyor", length=2.0, has_side_rails=True, has_motor=True)
        _, gen_cls = GENERATOR_REGISTRY["conveyor_segment"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"ConveyorSegment validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("conveyor_segment")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_082_forklift_cart(self):
        cfg = ForkliftCartConfig(name="test_forklift", fork_length=1.15, has_load_backrest=True)
        _, gen_cls = GENERATOR_REGISTRY["forklift_cart"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"ForkliftCart validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("forklift_cart")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_083_security_camera(self):
        cfg = SecurityCameraConfig(name="test_camera", camera_type="bullet", pan_angle=25.0, tilt_angle=-20.0)
        _, gen_cls = GENERATOR_REGISTRY["security_camera"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"SecurityCamera validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 100)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("security_camera")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_084_access_card_reader(self):
        cfg = AccessCardReaderConfig(name="test_card_reader", reader_style="swipe_and_keypad", has_keypad=True)
        _, gen_cls = GENERATOR_REGISTRY["access_card_reader"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"AccessCardReader validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("access_card_reader")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_085_biometric_scanner(self):
        cfg = BiometricScannerConfig(name="test_biometric", mount_style="pedestal", scan_state="active_laser")
        _, gen_cls = GENERATOR_REGISTRY["biometric_scanner"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"BiometricScanner validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 120)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("biometric_scanner")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_086_alarm_siren(self):
        cfg = AlarmSirenConfig(name="test_siren", siren_type="dual_horn", has_wire_guard=True)
        _, gen_cls = GENERATOR_REGISTRY["alarm_siren"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"AlarmSiren validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("alarm_siren")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_087_speaker_intercom(self):
        cfg = SpeakerIntercomConfig(name="test_intercom", has_push_to_talk=True, has_station_label=True)
        _, gen_cls = GENERATOR_REGISTRY["speaker_intercom"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"SpeakerIntercom validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 120)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("speaker_intercom")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_088_emergency_beacon(self):
        cfg = EmergencyBeaconConfig(name="test_beacon", base_style="pedestal", has_protective_cage=True)
        _, gen_cls = GENERATOR_REGISTRY["emergency_beacon"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"EmergencyBeacon validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 150)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("emergency_beacon")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

    def test_089_camera_monitor(self):
        cfg = CameraMonitorConfig(name="test_monitor", screen_layout="quad_split", has_desk_swivel_stand=True)
        _, gen_cls = GENERATOR_REGISTRY["camera_monitor"]
        gen = gen_cls()
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid, f"CameraMonitor validation failed: {rep.errors}")
        self.assertGreater(rep.triangle_count, 180)
        self.assertLessEqual(rep.triangle_count / max(1, cfg.target_tri_budget), 1.20)
        self.assertTrue(rep.has_uv_map)
        self.assertTrue(rep.has_vertex_colors)

        m = find_manifest_for_family("camera_monitor")
        self.assertIsNotNone(m)
        self.assertGreaterEqual(len(m.presets), 2)

        # Export test verification
        out_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
        glb_p, json_p = GLBExporter.export(obj, cfg, rep, out_path, gen_cls.__name__)
        self.assertTrue(os.path.exists(glb_p))
        self.assertTrue(os.path.exists(json_p))

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
