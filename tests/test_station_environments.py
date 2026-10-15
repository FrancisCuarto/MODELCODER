import unittest
import os
import shutil
import json
import bpy

from procedural_assets.generators import (
    GENERATOR_REGISTRY,
    StationCorridorConfig,
    StationRoomConfig
)
from procedural_assets.export.glb_exporter import GLBExporter

class TestStationEnvironments(unittest.TestCase):
    """Test suite for modular space station corridors, rooms, and Godot 4 connection sockets."""

    @classmethod
    def setUpClass(cls):
        cls.test_export_dir = os.path.join(os.path.dirname(__file__), "export_temp_environments")
        os.makedirs(cls.test_export_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_export_dir):
            shutil.rmtree(cls.test_export_dir)

    def test_corridor_straight_and_sockets(self):
        config = StationCorridorConfig(
            seed=1001,
            name="test_corridor_straight",
            corridor_type="straight",
            width=3.0,
            length=4.0,
            height=3.0,
            has_integrated_lighting=True,
            has_hazard_stripes=True
        )
        _, gen_cls = GENERATOR_REGISTRY["station_corridor"]
        gen = gen_cls()
        obj = gen.generate(config)
        report = gen.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 100)
        self.assertLessEqual(report.triangle_count, config.target_tri_budget * 1.35)
        # Sockets
        self.assertEqual(len(config.connection_sockets), 2)
        socket_names = [s["name"] for s in config.connection_sockets]
        self.assertIn("socket_south", socket_names)
        self.assertIn("socket_north", socket_names)

    def test_corridor_variants(self):
        # Corner 90
        cfg_corner = StationCorridorConfig(name="corridor_corner", corridor_type="corner_90")
        _, gen_cls = GENERATOR_REGISTRY["station_corridor"]
        gen = gen_cls()
        obj_corner = gen.generate(cfg_corner)
        rep_corner = gen.validate(obj_corner, cfg_corner)
        self.assertTrue(rep_corner.is_valid)
        self.assertIn("socket_east", [s["name"] for s in cfg_corner.connection_sockets])

        # T-Junction
        cfg_t = StationCorridorConfig(name="corridor_t", corridor_type="t_junction")
        obj_t = gen.generate(cfg_t)
        rep_t = gen.validate(obj_t, cfg_t)
        self.assertTrue(rep_t.is_valid)
        self.assertEqual(len(cfg_t.connection_sockets), 3)

        # Doorway Arch
        cfg_arch = StationCorridorConfig(name="corridor_arch", corridor_type="doorway_arch")
        obj_arch = gen.generate(cfg_arch)
        rep_arch = gen.validate(obj_arch, cfg_arch)
        self.assertTrue(rep_arch.is_valid)

        # Damage state: collapsed ceiling wires
        cfg_dmg = StationCorridorConfig(name="corridor_dmg", damage_state="collapsed_ceiling_wires")
        obj_dmg = gen.generate(cfg_dmg)
        rep_dmg = gen.validate(obj_dmg, cfg_dmg)
        self.assertTrue(rep_dmg.is_valid)

    def test_room_archetypes_and_features(self):
        # Medbay Lab with floor drain
        cfg_medbay = StationRoomConfig(
            seed=2002,
            name="test_medbay",
            room_archetype="medbay_lab",
            width=6.0,
            depth=8.0,
            door_north=True,
            door_south=True
        )
        _, gen_cls = GENERATOR_REGISTRY["station_room"]
        gen = gen_cls()
        obj_med = gen.generate(cfg_medbay)
        rep_med = gen.validate(obj_med, cfg_medbay)

        self.assertTrue(rep_med.is_valid)
        self.assertGreater(rep_med.triangle_count, 150)
        self.assertLessEqual(rep_med.triangle_count, cfg_medbay.target_tri_budget * 1.35)
        self.assertEqual(len(cfg_medbay.doorway_sockets), 2)

        # Control Hub with observation window & raised platform
        cfg_hub = StationRoomConfig(
            seed=3003,
            name="test_control_hub",
            room_archetype="control_hub",
            width=8.0,
            depth=10.0,
            has_observation_window=True,
            door_north=False,
            door_south=True,
            door_east=True
        )
        obj_hub = gen.generate(cfg_hub)
        rep_hub = gen.validate(obj_hub, cfg_hub)
        self.assertTrue(rep_hub.is_valid)
        hub_socket_names = [s["name"] for s in cfg_hub.doorway_sockets]
        self.assertIn("door_south", hub_socket_names)
        self.assertIn("door_east", hub_socket_names)
        self.assertNotIn("door_north", hub_socket_names)

        # Cargo Bay with overhead gantry
        cfg_cargo = StationRoomConfig(
            seed=4004,
            name="test_cargo_bay",
            room_archetype="cargo_bay",
            has_overhead_gantry=True
        )
        obj_cargo = gen.generate(cfg_cargo)
        rep_cargo = gen.validate(obj_cargo, cfg_cargo)
        self.assertTrue(rep_cargo.is_valid)

    def test_export_and_reimport_station_environments(self):
        """Verify GLB export and JSON metadata sidecar containing sockets for Godot 4."""
        configs = [
            StationCorridorConfig(name="exp_corridor", seed=5050),
            StationRoomConfig(name="exp_room", seed=6060)
        ]

        for cfg in configs:
            fam_key = "station_corridor" if "corridor" in cfg.name else "station_room"
            _, gen_cls = GENERATOR_REGISTRY[fam_key]
            gen = gen_cls()
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)

            glb_path = os.path.join(self.test_export_dir, f"{cfg.name}.glb")
            out_glb, out_json = GLBExporter.export(obj, cfg, rep, glb_path, gen_cls.__name__)

            self.assertTrue(os.path.exists(out_glb))
            self.assertTrue(os.path.exists(out_json))
            self.assertGreater(os.path.getsize(out_glb), 1500)

            # Check JSON contents for Godot 4 sockets
            with open(out_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("config_parameters", data)
            if fam_key == "station_corridor":
                self.assertIn("connection_sockets", data["config_parameters"])
                self.assertGreater(len(data["config_parameters"]["connection_sockets"]), 0)
            else:
                self.assertIn("doorway_sockets", data["config_parameters"])
                self.assertGreater(len(data["config_parameters"]["doorway_sockets"]), 0)

            # Re-import into Blender
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=out_glb)
            imported_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
            self.assertGreaterEqual(len(imported_objs), 1)

if __name__ == "__main__":
    unittest.main()
