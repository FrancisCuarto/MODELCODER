import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
from procedural_assets.generators import (
    TerminalConfig, TerminalGenerator,
    OxypodConfig, OxypodGenerator,
    DoorConfig, DoorGenerator,
    ServerRackConfig, ServerRackGenerator,
    CrateConfig, CrateGenerator,
    LockerConfig, LockerGenerator,
    PipeConfig, PipeGenerator,
    ElectricalPanelConfig, ElectricalPanelGenerator
)

class TestDeepVariants(unittest.TestCase):

    def setUp(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def test_terminal_variants(self):
        gen = TerminalGenerator()
        for t_type in ("wall", "desktop", "pedestal"):
            for state in ("active", "alarm", "damaged", "powered_off"):
                cfg = TerminalConfig(seed=12, terminal_type=t_type, state=state, keyboard_style="keypad_numeric")
                obj = gen.generate(cfg)
                rep = gen.validate(obj, cfg)
                self.assertTrue(rep.is_valid)

    def test_oxypod_variants(self):
        gen = OxypodGenerator()
        for s_type in ("wall_station", "portable_canister", "dual_tank_rig"):
            cfg = OxypodConfig(seed=24, station_type=s_type, oxygen_level=0.10, has_coiled_hose=True)
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)
            self.assertTrue(rep.is_valid)

    def test_door_jammed_and_airlock(self):
        gen = DoorGenerator()
        # Test jammed survival horror door (0.15 open)
        cfg = DoorConfig(seed=36, door_type="heavy_airlock", open_ratio=0.15, access_interface="manual_wheel")
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid)

    def test_server_rack_cryo(self):
        gen = ServerRackGenerator()
        cfg = ServerRackConfig(seed=48, rack_type="cryo_cooling_rack", cooling_system="cooling_pipes", has_service_terminal=True)
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid)

    def test_crate_battery_and_medical(self):
        gen = CrateGenerator()
        for c_type in ("battery_cell", "medical_crate", "chemical_drum"):
            cfg = CrateConfig(seed=60, crate_type=c_type, lid_state="ajar_open")
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)
            self.assertTrue(rep.is_valid)

    def test_locker_open_with_bench(self):
        gen = LockerGenerator()
        cfg = LockerConfig(seed=72, columns=3, door_state="one_open", has_integrated_bench=True)
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid)

    def test_pipes_elbow_and_insulation(self):
        gen = PipeGenerator()
        for p_type in ("elbow_90", "t_junction"):
            cfg = PipeConfig(seed=84, pipe_type=p_type, valve_type="lever_quarter_turn", has_insulation_layer=True)
            obj = gen.generate(cfg)
            rep = gen.validate(obj, cfg)
            self.assertTrue(rep.is_valid)

    def test_electrical_panel_knife_and_ajar(self):
        gen = ElectricalPanelGenerator()
        cfg = ElectricalPanelConfig(seed=96, has_knife_switch=True, door_ajar=True, has_digital_readout=True)
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)
        self.assertTrue(rep.is_valid)

if __name__ == "__main__":
    unittest.main()
