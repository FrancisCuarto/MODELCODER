from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class AccessCardReaderConfig(BaseAssetConfig):
    """Configuration for wall-mounted security access card reader and keypad."""
    name: str = "access_card_reader"
    family_id: str = "access_card_reader"
    category: str = "security"
    reader_style: str = "swipe_and_keypad"  # swipe_and_keypad, rfid_tap, keypad_only
    status_state: str = "granted"           # standby, granted, denied, offline
    has_keypad: bool = True
    has_status_screen: bool = True
    weather_shroud: bool = False
    wear_level: float = 0.3
    target_tri_budget: int = 260

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "reader_style": self.reader_style,
            "status_state": self.status_state,
            "has_keypad": self.has_keypad,
            "has_status_screen": self.has_status_screen,
            "weather_shroud": self.weather_shroud,
        })
        return d
