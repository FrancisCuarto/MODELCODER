from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class SpeakerIntercomConfig(BaseAssetConfig):
    """Configuration for two-way wall intercom station."""
    name: str = "speaker_intercom"
    family_id: str = "speaker_intercom"
    category: str = "comms"
    intercom_shape: str = "rectangular"  # rectangular, slant_face, rugged_box
    has_push_to_talk: bool = True
    has_call_speaker: bool = True
    status_light: str = "online"         # online, calling, muted, dead
    has_station_label: bool = True
    wear_level: float = 0.35
    target_tri_budget: int = 240

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "intercom_shape": self.intercom_shape,
            "has_push_to_talk": self.has_push_to_talk,
            "has_call_speaker": self.has_call_speaker,
            "status_light": self.status_light,
            "has_station_label": self.has_station_label,
        })
        return d
