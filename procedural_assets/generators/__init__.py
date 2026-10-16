from .electrical_panel import ElectricalPanelConfig, ElectricalPanelGenerator
from .terminal import TerminalConfig, TerminalGenerator
from .oxypod import OxypodConfig, OxypodGenerator
from .door import DoorConfig, DoorGenerator
from .server_rack import ServerRackConfig, ServerRackGenerator
from .crate import CrateConfig, CrateGenerator
from .locker import LockerConfig, LockerGenerator
from .pipes import PipeConfig, PipeGenerator
from .crash_cart import CrashCartConfig, CrashCartGenerator
from .office_desk import OfficeDeskConfig, OfficeDeskGenerator
from .office_chair import OfficeChairConfig, OfficeChairGenerator
from .sign_placard import SignPlacardConfig, SignPlacardGenerator
from .trash_bin import TrashBinConfig, TrashBinGenerator
from .light_fixture import LightFixtureConfig, LightFixtureGenerator
from .fire_extinguisher import FireExtinguisherConfig, FireExtinguisherGenerator
from .vent_grate import VentGrateConfig, VentGrateGenerator
from .cable_bundle import CableBundleConfig, CableBundleGenerator
from .station_corridor import StationCorridorConfig, StationCorridorGenerator
from .station_room import StationRoomConfig, StationRoomGenerator
from .crew_bed import CrewBedConfig, CrewBedGenerator
from .bunk_bed import BunkBedConfig, BunkBedGenerator
from .nightstand import NightstandConfig, NightstandGenerator
from .radiator_heater import RadiatorHeaterConfig, RadiatorHeaterGenerator
from .office_door import OfficeDoorConfig, OfficeDoorGenerator

# 20 New Station Furniture Families
from .autopsy_table import AutopsyTableConfig, AutopsyTableGenerator
from .medical_screen import MedicalScreenConfig, MedicalScreenGenerator
from .morgue_gurney import MorgueGurneyConfig, MorgueGurneyGenerator
from .chemical_cabinet import ChemicalCabinetConfig, ChemicalCabinetGenerator
from .restraint_chair import RestraintChairConfig, RestraintChairGenerator
from .mess_table import MessTableConfig, MessTableGenerator
from .ration_automat import RationAutomatConfig, RationAutomatGenerator
from .canteen_counter import CanteenCounterConfig, CanteenCounterGenerator
from .file_cabinet import FileCabinetConfig, FileCabinetGenerator
from .locker_bench import LockerBenchConfig, LockerBenchGenerator
from .work_bench import WorkBenchConfig, WorkBenchGenerator
from .heavy_shelving import HeavyShelvingConfig, HeavyShelvingGenerator
from .tool_chest_cart import ToolChestCartConfig, ToolChestCartGenerator
from .safety_shower import SafetyShowerConfig, SafetyShowerGenerator
from .hydroponic_tray_bed import HydroponicTrayBedConfig, HydroponicTrayBedGenerator
from .security_desk import SecurityDeskConfig, SecurityDeskGenerator
from .weapons_rack import WeaponsRackConfig, WeaponsRackGenerator
from .bridge_console_desk import BridgeConsoleDeskConfig, BridgeConsoleDeskGenerator
from .space_toilet import SpaceToiletConfig, SpaceToiletGenerator
from .scrub_sink import ScrubSinkConfig, ScrubSinkGenerator

# Lote B: Soporte Vital & Narrativa (Familias 45-53)
from .cryo_stasis_pod import CryoStasisPodConfig, CryoStasisPodGenerator
from .consciousness_archive import ConsciousnessArchiveConfig, ConsciousnessArchiveGenerator
from .neural_interface_chair import NeuralInterfaceChairConfig, NeuralInterfaceChairGenerator
from .memory_extraction_terminal import MemoryExtractionTerminalConfig, MemoryExtractionTerminalGenerator
from .oxygen_regulator import OxygenRegulatorConfig, OxygenRegulatorGenerator
from .oxygen_tank import OxygenTankConfig, OxygenTankGenerator
from .pressure_door_control import PressureDoorControlConfig, PressureDoorControlGenerator
from .airlock_chamber import AirlockChamberConfig, AirlockChamberGenerator
from .pressure_indicator import PressureIndicatorConfig, PressureIndicatorGenerator

GENERATOR_REGISTRY = {
    # Environment & Architectural Tiles
    "station_corridor": (StationCorridorConfig, StationCorridorGenerator),
    "station_room": (StationRoomConfig, StationRoomGenerator),

    # Living Quarters & Core Fixtures
    "crew_bed": (CrewBedConfig, CrewBedGenerator),
    "bunk_bed": (BunkBedConfig, BunkBedGenerator),
    "nightstand": (NightstandConfig, NightstandGenerator),
    "radiator_heater": (RadiatorHeaterConfig, RadiatorHeaterGenerator),
    "office_door": (OfficeDoorConfig, OfficeDoorGenerator),

    # Medical & Research Lab
    "autopsy_table": (AutopsyTableConfig, AutopsyTableGenerator),
    "medical_screen": (MedicalScreenConfig, MedicalScreenGenerator),
    "morgue_gurney": (MorgueGurneyConfig, MorgueGurneyGenerator),
    "chemical_cabinet": (ChemicalCabinetConfig, ChemicalCabinetGenerator),
    "restraint_chair": (RestraintChairConfig, RestraintChairGenerator),
    "scrub_sink": (ScrubSinkConfig, ScrubSinkGenerator),

    # Habitation & Canteen
    "mess_table": (MessTableConfig, MessTableGenerator),
    "ration_automat": (RationAutomatConfig, RationAutomatGenerator),
    "canteen_counter": (CanteenCounterConfig, CanteenCounterGenerator),
    "locker_bench": (LockerBenchConfig, LockerBenchGenerator),
    "space_toilet": (SpaceToiletConfig, SpaceToiletGenerator),

    # Engineering, Cargo & Workshop
    "work_bench": (WorkBenchConfig, WorkBenchGenerator),
    "heavy_shelving": (HeavyShelvingConfig, HeavyShelvingGenerator),
    "tool_chest_cart": (ToolChestCartConfig, ToolChestCartGenerator),
    "safety_shower": (SafetyShowerConfig, SafetyShowerGenerator),
    "hydroponic_tray_bed": (HydroponicTrayBedConfig, HydroponicTrayBedGenerator),

    # Security & Operations Bridge
    "security_desk": (SecurityDeskConfig, SecurityDeskGenerator),
    "weapons_rack": (WeaponsRackConfig, WeaponsRackGenerator),
    "bridge_console_desk": (BridgeConsoleDeskConfig, BridgeConsoleDeskGenerator),
    "file_cabinet": (FileCabinetConfig, FileCabinetGenerator),

    # Industrial Props & Facilities
    "crash_cart": (CrashCartConfig, CrashCartGenerator),
    "office_desk": (OfficeDeskConfig, OfficeDeskGenerator),
    "office_chair": (OfficeChairConfig, OfficeChairGenerator),
    "sign_placard": (SignPlacardConfig, SignPlacardGenerator),
    "trash_bin": (TrashBinConfig, TrashBinGenerator),
    "light_fixture": (LightFixtureConfig, LightFixtureGenerator),
    "fire_extinguisher": (FireExtinguisherConfig, FireExtinguisherGenerator),
    "vent_grate": (VentGrateConfig, VentGrateGenerator),
    "cable_bundle": (CableBundleConfig, CableBundleGenerator),
    "electrical_panel": (ElectricalPanelConfig, ElectricalPanelGenerator),
    "terminal": (TerminalConfig, TerminalGenerator),
    "oxypod": (OxypodConfig, OxypodGenerator),
    "door": (DoorConfig, DoorGenerator),
    "server_rack": (ServerRackConfig, ServerRackGenerator),
    "crate": (CrateConfig, CrateGenerator),
    "locker": (LockerConfig, LockerGenerator),
    "pipes": (PipeConfig, PipeGenerator),

    # Lote B: Soporte Vital & Narrativa (Familias 45-53)
    "cryo_stasis_pod": (CryoStasisPodConfig, CryoStasisPodGenerator),
    "consciousness_archive": (ConsciousnessArchiveConfig, ConsciousnessArchiveGenerator),
    "neural_interface_chair": (NeuralInterfaceChairConfig, NeuralInterfaceChairGenerator),
    "memory_extraction_terminal": (MemoryExtractionTerminalConfig, MemoryExtractionTerminalGenerator),
    "oxygen_regulator": (OxygenRegulatorConfig, OxygenRegulatorGenerator),
    "oxygen_tank": (OxygenTankConfig, OxygenTankGenerator),
    "pressure_door_control": (PressureDoorControlConfig, PressureDoorControlGenerator),
    "airlock_chamber": (AirlockChamberConfig, AirlockChamberGenerator),
    "pressure_indicator": (PressureIndicatorConfig, PressureIndicatorGenerator),
}

# Dynamic auto-discovery for community-contributed generator families
import os as _os
import importlib as _importlib

_generators_dir = _os.path.dirname(_os.path.abspath(__file__))
for _item in _os.listdir(_generators_dir):
    _item_path = _os.path.join(_generators_dir, _item)
    if _os.path.isdir(_item_path) and not _item.startswith(("_", ".")) and _item not in GENERATOR_REGISTRY:
        try:
            _mod = _importlib.import_module(f".{_item}", package=__name__)
            _cfg_cls = None
            _gen_cls = None
            for _attr_name in dir(_mod):
                if _attr_name.endswith("Config") and _attr_name != "BaseAssetConfig":
                    _cfg_cls = getattr(_mod, _attr_name)
                elif _attr_name.endswith("Generator") and _attr_name != "BaseAssetGenerator":
                    _gen_cls = getattr(_mod, _attr_name)
            if _cfg_cls and _gen_cls:
                GENERATOR_REGISTRY[_item] = (_cfg_cls, _gen_cls)
        except Exception:
            pass

__all__ = [
    "GENERATOR_REGISTRY",
    "StationCorridorConfig", "StationCorridorGenerator",
    "StationRoomConfig", "StationRoomGenerator",
    "CrewBedConfig", "CrewBedGenerator",
    "BunkBedConfig", "BunkBedGenerator",
    "NightstandConfig", "NightstandGenerator",
    "RadiatorHeaterConfig", "RadiatorHeaterGenerator",
    "OfficeDoorConfig", "OfficeDoorGenerator",
    "AutopsyTableConfig", "AutopsyTableGenerator",
    "MedicalScreenConfig", "MedicalScreenGenerator",
    "MorgueGurneyConfig", "MorgueGurneyGenerator",
    "ChemicalCabinetConfig", "ChemicalCabinetGenerator",
    "RestraintChairConfig", "RestraintChairGenerator",
    "ScrubSinkConfig", "ScrubSinkGenerator",
    "MessTableConfig", "MessTableGenerator",
    "RationAutomatConfig", "RationAutomatGenerator",
    "CanteenCounterConfig", "CanteenCounterGenerator",
    "LockerBenchConfig", "LockerBenchGenerator",
    "SpaceToiletConfig", "SpaceToiletGenerator",
    "WorkBenchConfig", "WorkBenchGenerator",
    "HeavyShelvingConfig", "HeavyShelvingGenerator",
    "ToolChestCartConfig", "ToolChestCartGenerator",
    "SafetyShowerConfig", "SafetyShowerGenerator",
    "HydroponicTrayBedConfig", "HydroponicTrayBedGenerator",
    "SecurityDeskConfig", "SecurityDeskGenerator",
    "WeaponsRackConfig", "WeaponsRackGenerator",
    "BridgeConsoleDeskConfig", "BridgeConsoleDeskGenerator",
    "FileCabinetConfig", "FileCabinetGenerator",
    "CrashCartConfig", "CrashCartGenerator",
    "OfficeDeskConfig", "OfficeDeskGenerator",
    "OfficeChairConfig", "OfficeChairGenerator",
    "SignPlacardConfig", "SignPlacardGenerator",
    "TrashBinConfig", "TrashBinGenerator",
    "LightFixtureConfig", "LightFixtureGenerator",
    "FireExtinguisherConfig", "FireExtinguisherGenerator",
    "VentGrateConfig", "VentGrateGenerator",
    "CableBundleConfig", "CableBundleGenerator",
    "ElectricalPanelConfig", "ElectricalPanelGenerator",
    "TerminalConfig", "TerminalGenerator",
    "OxypodConfig", "OxypodGenerator",
    "DoorConfig", "DoorGenerator",
    "ServerRackConfig", "ServerRackGenerator",
    "CrateConfig", "CrateGenerator",
    "LockerConfig", "LockerGenerator",
    "PipeConfig", "PipeGenerator",
    "CryoStasisPodConfig", "CryoStasisPodGenerator",
    "ConsciousnessArchiveConfig", "ConsciousnessArchiveGenerator",
    "NeuralInterfaceChairConfig", "NeuralInterfaceChairGenerator",
    "MemoryExtractionTerminalConfig", "MemoryExtractionTerminalGenerator",
    "OxygenRegulatorConfig", "OxygenRegulatorGenerator",
    "OxygenTankConfig", "OxygenTankGenerator",
    "PressureDoorControlConfig", "PressureDoorControlGenerator",
    "AirlockChamberConfig", "AirlockChamberGenerator",
    "PressureIndicatorConfig", "PressureIndicatorGenerator",
]

