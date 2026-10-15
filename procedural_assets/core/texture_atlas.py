"""
Procedural PS1 Weathered Texture Atlas Engine for Below Nominal.
Generates an authentic low-resolution (256x256 or 128x128) pixel-art texture atlas
packed with weathered metal, chipped paint, rust clusters, dirt gradients, hazard chevrons,
CRT scanlines, and retro dials using vectorized NumPy operations.
"""

from typing import Dict, Tuple, Optional
import math
import numpy as np
import bpy

# UV Rectangle: (u_min, v_min, u_max, v_max) in 0.0 .. 1.0 range
# Matches the authentic PS1/prop.ts specification: type Rect = [u0, v0, u1, v1]
Rect = Tuple[float, float, float, float]

class PS1TextureAtlas:
    """Procedural texture atlas generator optimized for authentic PS1 retro horror aesthetics."""

    WIDTH = 256
    HEIGHT = 256

    # 4x4 Grid of 64x64 sub-regions + subdivided 32x32 tiles
    # In Blender UV space: U = x / WIDTH, V = y / HEIGHT (V=0 is bottom, V=1 is top)
    RECTS: Dict[str, Rect] = {
        # Row 0 (bottom: y = 0..63)
        "red_paint_worn": (0.00, 0.00, 0.25, 0.25),          # (0, 0) -> (64, 64)
        "metal_dark_grime": (0.25, 0.00, 0.50, 0.25),        # (64, 0) -> (128, 64)
        "metal_light_brushed": (0.50, 0.00, 0.75, 0.25),     # (128, 0) -> (192, 64)
        "beige_plastic_worn": (0.75, 0.00, 1.00, 0.25),      # (192, 0) -> (256, 64)

        # Row 1 (y = 64..127)
        "hazard_stripes": (0.00, 0.25, 0.25, 0.50),          # (0, 64) -> (64, 128)
        "rust_heavy": (0.25, 0.25, 0.50, 0.50),              # (64, 64) -> (128, 128)
        "vent_grill": (0.50, 0.25, 0.75, 0.50),              # (128, 64) -> (192, 128)
        "gauge_meter": (0.75, 0.25, 0.875, 0.375),           # (192, 64) -> (224, 96)
        "caution_label": (0.875, 0.25, 1.00, 0.375),         # (224, 64) -> (256, 96)
        "fluorescent_lit": (0.75, 0.375, 0.875, 0.50),       # (192, 96) -> (224, 128)
        "door_seal_red": (0.875, 0.375, 1.00, 0.50),         # (224, 96) -> (256, 128)

        # Row 2 (y = 128..191) - CRTs, Glazed Surfaces & Transparent Panels
        "crt_screen_green": (0.00, 0.50, 0.25, 0.75),        # (0, 128) -> (64, 192)
        "crt_screen_amber": (0.25, 0.50, 0.50, 0.75),        # (64, 128) -> (128, 192)
        "crt_screen_off": (0.50, 0.50, 0.75, 0.75),          # (128, 128) -> (192, 192)
        "oxygen_cyan_glow": (0.75, 0.50, 0.875, 0.625),      # (192, 128) -> (224, 160)
        "ceramic_tile_white": (0.875, 0.50, 1.00, 0.625),    # (224, 128) -> (256, 160)
        "glass_reinforced": (0.75, 0.625, 0.875, 0.75),      # (192, 160) -> (224, 192)
        "painted_metal_white": (0.875, 0.625, 1.00, 0.75),   # (224, 160) -> (256, 192)

        # Row 3 (top: y = 192..255) - Controls & Accents
        "rubber_black": (0.00, 0.75, 0.25, 1.00),            # (0, 192) -> (64, 256)
        "button_red": (0.25, 0.75, 0.375, 0.875),            # (64, 192) -> (96, 224)
        "button_yellow": (0.375, 0.75, 0.50, 0.875),         # (96, 192) -> (128, 224)
        "button_blue": (0.25, 0.875, 0.375, 1.00),           # (64, 224) -> (96, 256)
        "button_white": (0.375, 0.875, 0.50, 1.00),          # (96, 224) -> (128, 256)
        "led_green": (0.50, 0.75, 0.625, 0.875),             # (128, 192) -> (160, 224)
        "led_red": (0.625, 0.75, 0.75, 0.875),               # (160, 192) -> (192, 224)
        "led_yellow": (0.50, 0.875, 0.625, 1.00),            # (128, 224) -> (160, 256)
        "switch_metal": (0.625, 0.875, 0.75, 1.00),          # (160, 224) -> (192, 256)
        "cartridge_amber": (0.75, 0.75, 0.875, 0.875),       # (192, 192) -> (224, 224)
        "chair_vinyl_dark": (0.875, 0.75, 1.00, 0.875),      # (224, 192) -> (256, 224)
        "sign_exit_green": (0.75, 0.875, 0.875, 1.00),       # (192, 224) -> (224, 256)
        "sign_sector_blue": (0.875, 0.875, 1.00, 1.00),      # (224, 224) -> (256, 256)
    }

    @classmethod
    def get_rect(cls, name: str) -> Rect:
        """Retrieve UV rect bounds for a given texture chunk."""
        return cls.RECTS.get(name, (0.0, 0.0, 1.0, 1.0))

    @classmethod
    def generate_atlas_pixels(cls, wear_level: float = 0.5, seed: int = 42) -> np.ndarray:
        """
        Generate procedural 256x256 RGBA pixel data as a NumPy array.
        wear_level: 0.0 = factory clean, 1.0 = heavy rust, chipped paint and grime.
        """
        rng = np.random.default_rng(seed)
        w, h = cls.WIDTH, cls.HEIGHT
        atlas = np.zeros((h, w, 4), dtype=np.float32)
        atlas[:, :, 3] = 1.0  # Fully opaque alpha

        # Helper to get pixel slice
        def pslice(rect: Rect):
            u0, v0, u1, v1 = rect
            x0 = int(round(u0 * w))
            y0 = int(round(v0 * h))
            x1 = int(round(u1 * w))
            y1 = int(round(v1 * h))
            return y0, y1, x0, x1

        # --- 1. RED PAINT WORN (Crash Cart / Emergency Panel red) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["red_paint_worn"])
        tw, th = x1 - x0, y1 - y0
        base_red = np.array([0.58, 0.10, 0.08], dtype=np.float32)
        subtle_noise = rng.uniform(0.90, 1.05, (th, tw, 1)).astype(np.float32)
        tile = base_red * subtle_noise

        # Vertical grime gradient and streaks
        y_grad = np.linspace(0.85, 1.0, th)[:, None, None].astype(np.float32)
        tile *= y_grad

        # Chipped paint & rust specks based on wear_level
        if wear_level > 0.05:
            # Noise mask for paint chipping
            chip_prob = 0.04 + wear_level * 0.18
            chip_mask = rng.uniform(0.0, 1.0, (th, tw)) < chip_prob
            # Rust color inside chips
            rust_color = np.array([0.28, 0.14, 0.08], dtype=np.float32)
            tile[chip_mask] = rust_color * rng.uniform(0.7, 1.1, (np.sum(chip_mask), 1))

            # Edge darkening / dirt in corners
            for i in range(4):
                tile[i, :] *= 0.65
                tile[th - 1 - i, :] *= 0.70
                tile[:, i] *= 0.65
                tile[:, tw - 1 - i] *= 0.70

        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 2. METAL DARK GRIME (Chassis, panel interiors, steel structural frame) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["metal_dark_grime"])
        tw, th = x1 - x0, y1 - y0
        base_metal = np.array([0.22, 0.24, 0.26], dtype=np.float32)
        noise = rng.uniform(0.88, 1.12, (th, tw, 1)).astype(np.float32)
        tile = base_metal * noise
        if wear_level > 0.1:
            rust_flecks = rng.uniform(0.0, 1.0, (th, tw)) < (wear_level * 0.08)
            tile[rust_flecks] = np.array([0.35, 0.18, 0.08], dtype=np.float32)
        # Vignette border
        tile[0, :] *= 0.5; tile[th-1, :] *= 0.5; tile[:, 0] *= 0.5; tile[:, tw-1] *= 0.5
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 3. METAL LIGHT BRUSHED (Handles, drawer slides, switch plates, bolts) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["metal_light_brushed"])
        tw, th = x1 - x0, y1 - y0
        base_brushed = np.array([0.65, 0.68, 0.72], dtype=np.float32)
        # Horizontal brushed metal streaks
        streaks = rng.uniform(0.92, 1.08, (th, 1, 1)).astype(np.float32)
        tile = np.repeat(streaks, tw, axis=1) * base_brushed
        if wear_level > 0.2:
            scratches = rng.uniform(0.0, 1.0, (th, tw)) < (wear_level * 0.05)
            tile[scratches] *= 0.55
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 4. BEIGE PLASTIC WORN (CRT bezels, computer housing, medical cart top) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["beige_plastic_worn"])
        tw, th = x1 - x0, y1 - y0
        base_beige = np.array([0.72, 0.70, 0.62], dtype=np.float32)
        tile = base_beige * rng.uniform(0.94, 1.04, (th, tw, 1)).astype(np.float32)
        # Crevice dirt
        tile[0:2, :] *= 0.6; tile[th-2:th, :] *= 0.6; tile[:, 0:2] *= 0.6; tile[:, tw-2:tw] *= 0.6
        if wear_level > 0.2:
            dirt = rng.uniform(0.0, 1.0, (th, tw)) < (wear_level * 0.07)
            tile[dirt] = np.array([0.38, 0.35, 0.28], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 5. HAZARD CHEVRONS (Yellow & Black diagonal warning stripes) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["hazard_stripes"])
        tw, th = x1 - x0, y1 - y0
        stripe_w = 8
        coords_x, coords_y = np.meshgrid(np.arange(tw), np.arange(th))
        stripe_pattern = ((coords_x + coords_y) // stripe_w) % 2
        yellow = np.array([0.88, 0.68, 0.08], dtype=np.float32)
        black = np.array([0.10, 0.10, 0.11], dtype=np.float32)
        tile = np.where(stripe_pattern[:, :, None] == 0, yellow, black)
        # Add grit/weathering
        tile *= rng.uniform(0.85, 1.05, (th, tw, 1)).astype(np.float32)
        if wear_level > 0.15:
            scuff = rng.uniform(0.0, 1.0, (th, tw)) < (wear_level * 0.12)
            tile[scuff] = np.array([0.30, 0.25, 0.20], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 6. RUST HEAVY (Deep oxidized corrosion) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["rust_heavy"])
        tw, th = x1 - x0, y1 - y0
        base_rust = np.array([0.48, 0.18, 0.06], dtype=np.float32)
        tile = base_rust * rng.uniform(0.65, 1.35, (th, tw, 1)).astype(np.float32)
        dark_crust = rng.uniform(0.0, 1.0, (th, tw)) < 0.35
        tile[dark_crust] = np.array([0.22, 0.09, 0.04], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 7. VENT GRILL (Horizontal ventilation slats) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["vent_grill"])
        tw, th = x1 - x0, y1 - y0
        slat_h = 4
        slat_pattern = (np.arange(th) // slat_h) % 2
        slat_lit = np.array([0.32, 0.35, 0.38], dtype=np.float32)
        slat_shadow = np.array([0.05, 0.05, 0.06], dtype=np.float32)
        tile = np.where(slat_pattern[:, None, None] == 0, slat_lit, slat_shadow)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 8. GAUGE METER (Analog circular pressure/vacuum dial) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["gauge_meter"])
        tw, th = x1 - x0, y1 - y0
        cx, cy = tw / 2.0, th / 2.0
        coords_x, coords_y = np.meshgrid(np.arange(tw), np.arange(th))
        dist = np.sqrt((coords_x - cx)**2 + (coords_y - cy)**2)
        dial_bg = np.array([0.88, 0.86, 0.80], dtype=np.float32)
        bezel = np.array([0.15, 0.16, 0.18], dtype=np.float32)
        tile = np.where(dist[:, :, None] < (cx - 2), dial_bg, bezel)
        # Red warning zone arc
        angle = np.arctan2(coords_y - cy, coords_x - cx)
        red_zone = (dist < (cx - 4)) & (dist > (cx - 8)) & (angle > 0.3) & (angle < 1.8)
        tile[red_zone] = np.array([0.80, 0.12, 0.08], dtype=np.float32)
        # Red Needle
        needle = (np.abs(coords_x - cx) < 1.5) & (coords_y > cy - 2) & (coords_y < cy + cx * 0.7)
        tile[needle] = np.array([0.90, 0.05, 0.05], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 9. CAUTION LABEL (Yellow badge with black border & stencil mark) ---
        y0, y1, x0, x1 = pslice(cls.RECTS["caution_label"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.85, 0.65, 0.05], dtype=np.float32)
        tile[0:2, :] = [0.1, 0.1, 0.1]; tile[th-2:th, :] = [0.1, 0.1, 0.1]
        tile[:, 0:2] = [0.1, 0.1, 0.1]; tile[:, tw-2:tw] = [0.1, 0.1, 0.1]
        # Text simulation bars
        tile[th//2-1:th//2+2, 4:tw-4] = [0.1, 0.1, 0.1]
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 10. FLUORESCENT LIT & DOOR SEAL RED ---
        y0, y1, x0, x1 = pslice(cls.RECTS["fluorescent_lit"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.85, 0.95, 0.98], dtype=np.float32)
        tile *= rng.uniform(0.92, 1.05, (th, tw, 1)).astype(np.float32)
        tile[0:2, :] *= 0.6; tile[th-2:th, :] *= 0.6
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        y0, y1, x0, x1 = pslice(cls.RECTS["door_seal_red"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.70, 0.12, 0.10], dtype=np.float32)
        tile *= rng.uniform(0.9, 1.1, (th, tw, 1)).astype(np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 11. CRT SCREENS (Green, Amber, Off) ---
        # CRT Green Lit
        y0, y1, x0, x1 = pslice(cls.RECTS["crt_screen_green"])
        tw, th = x1 - x0, y1 - y0
        scan_1d = (np.arange(th) % 2 == 0).astype(np.float32)[:, None, None]
        scanlines = np.repeat(scan_1d, tw, axis=1)
        crt_green_base = np.array([0.08, 0.38, 0.12], dtype=np.float32)
        tile = crt_green_base * (0.8 + 0.3 * scanlines)
        tile += rng.uniform(0.0, 0.06, (th, tw, 1)).astype(np.float32)
        # Simulated oscilloscope wave or text rows
        tile[th//2 - 2:th//2 + 2, tw//4:3*tw//4] = np.array([0.25, 0.95, 0.35], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # CRT Amber Lit
        y0, y1, x0, x1 = pslice(cls.RECTS["crt_screen_amber"])
        tw, th = x1 - x0, y1 - y0
        crt_amber_base = np.array([0.45, 0.22, 0.04], dtype=np.float32)
        tile = crt_amber_base * (0.8 + 0.3 * scanlines)
        tile += rng.uniform(0.0, 0.05, (th, tw, 1)).astype(np.float32)
        tile[th//2 - 2:th//2 + 2, tw//4:3*tw//4] = np.array([0.95, 0.60, 0.08], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # CRT Off (Dark dirty glass)
        y0, y1, x0, x1 = pslice(cls.RECTS["crt_screen_off"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.06, 0.07, 0.08], dtype=np.float32)
        tile += rng.uniform(0.0, 0.03, (th, tw, 1)).astype(np.float32)
        # Subtle dust/glare diagonal
        coords_x, coords_y = np.meshgrid(np.arange(tw), np.arange(th))
        glare = np.exp(-((coords_x - coords_y) / 12.0)**2)[:, :, None] * 0.10
        tile += glare
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Oxygen Cyan Glow (32x32)
        y0, y1, x0, x1 = pslice(cls.RECTS["oxygen_cyan_glow"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.08, 0.72, 0.85], dtype=np.float32)
        tile += rng.uniform(-0.04, 0.04, (th, tw, 1)).astype(np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Ceramic Tile White (32x32: glazed porcelain with grout border and specular gloss)
        y0, y1, x0, x1 = pslice(cls.RECTS["ceramic_tile_white"])
        tw, th = x1 - x0, y1 - y0
        base_ceramic = np.array([0.88, 0.90, 0.90], dtype=np.float32)
        tile = np.full((th, tw, 3), base_ceramic, dtype=np.float32)
        coords_x, coords_y = np.meshgrid(np.arange(tw), np.arange(th))
        gloss = np.exp(-((coords_x - coords_y) / 8.0)**2)[:, :, None] * 0.08
        tile += gloss
        tile[0, :] = [0.35, 0.36, 0.38]
        tile[th - 1, :] = [0.35, 0.36, 0.38]
        tile[:, 0] = [0.35, 0.36, 0.38]
        tile[:, tw - 1] = [0.35, 0.36, 0.38]
        if wear_level > 0.2:
            scum = rng.uniform(0.0, 1.0, (th, tw)) < (wear_level * 0.06)
            tile[scum] = np.array([0.45, 0.40, 0.30], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Glass Reinforced (32x32: translucent wired security glass with steel mesh)
        y0, y1, x0, x1 = pslice(cls.RECTS["glass_reinforced"])
        tw, th = x1 - x0, y1 - y0
        coords_x, coords_y = np.meshgrid(np.arange(tw), np.arange(th))
        tile = np.full((th, tw, 3), [0.18, 0.28, 0.32], dtype=np.float32)
        wire_grid = ((coords_x + coords_y) % 6 == 0) | ((coords_x - coords_y) % 6 == 0)
        tile[wire_grid] = np.array([0.55, 0.58, 0.62], dtype=np.float32)
        glare = np.exp(-((coords_x * 0.5 - coords_y * 0.5) / 5.0)**2)[:, :, None] * 0.12
        tile += glare
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Painted Metal White (32x32: clinical medical off-white enamel with chip wear)
        y0, y1, x0, x1 = pslice(cls.RECTS["painted_metal_white"])
        tw, th = x1 - x0, y1 - y0
        base_white = np.array([0.84, 0.85, 0.86], dtype=np.float32)
        tile = base_white * rng.uniform(0.96, 1.04, (th, tw, 1)).astype(np.float32)
        tile[0, :] *= 0.75; tile[th - 1, :] *= 0.75; tile[:, 0] *= 0.75; tile[:, tw - 1] *= 0.75
        if wear_level > 0.1:
            chip_prob = wear_level * 0.09
            chips = rng.uniform(0.0, 1.0, (th, tw)) < chip_prob
            tile[chips] = np.array([0.22, 0.22, 0.24], dtype=np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # --- 12. CONTROLS, ACCENTS & HARDWARE ---
        # Rubber Black (Tires, feet, thick cables)
        y0, y1, x0, x1 = pslice(cls.RECTS["rubber_black"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.12, 0.12, 0.13], dtype=np.float32)
        tile *= rng.uniform(0.92, 1.08, (th, tw, 1)).astype(np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Buttons (Red, Yellow, Blue, White)
        for b_name, b_col in [
            ("button_red", [0.75, 0.12, 0.10]),
            ("button_yellow", [0.85, 0.62, 0.08]),
            ("button_blue", [0.15, 0.38, 0.68]),
            ("button_white", [0.78, 0.80, 0.82]),
        ]:
            y0, y1, x0, x1 = pslice(cls.RECTS[b_name])
            tw, th = x1 - x0, y1 - y0
            tile = np.full((th, tw, 3), b_col, dtype=np.float32)
            # Bevel border
            tile[0, :] *= 0.6; tile[th-1, :] *= 1.3; tile[:, 0] *= 0.7; tile[:, tw-1] *= 1.2
            atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # LEDs (Green, Red, Yellow with bright center)
        for led_name, led_col in [
            ("led_green", [0.15, 0.95, 0.25]),
            ("led_red", [0.95, 0.15, 0.10]),
            ("led_yellow", [0.95, 0.85, 0.10]),
        ]:
            y0, y1, x0, x1 = pslice(cls.RECTS[led_name])
            tw, th = x1 - x0, y1 - y0
            tile = np.full((th, tw, 3), led_col, dtype=np.float32)
            atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Switch metal
        y0, y1, x0, x1 = pslice(cls.RECTS["switch_metal"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.75, 0.78, 0.82], dtype=np.float32)
        tile[0:2, :] *= 0.5; tile[:, 0:2] *= 0.5
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Memory Cartridge Amber
        y0, y1, x0, x1 = pslice(cls.RECTS["cartridge_amber"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.82, 0.48, 0.10], dtype=np.float32)
        tile *= rng.uniform(0.9, 1.1, (th, tw, 1)).astype(np.float32)
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Chair Vinyl Dark
        y0, y1, x0, x1 = pslice(cls.RECTS["chair_vinyl_dark"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.16, 0.18, 0.20], dtype=np.float32)
        tile *= rng.uniform(0.85, 1.15, (th, tw, 1)).astype(np.float32)
        tile[th//2, :] *= 0.6
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Sign Exit Green
        y0, y1, x0, x1 = pslice(cls.RECTS["sign_exit_green"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.08, 0.65, 0.25], dtype=np.float32)
        tile[0:2, :] = [0.05, 0.1, 0.05]; tile[th-2:th, :] = [0.05, 0.1, 0.05]
        tile[:, 0:2] = [0.05, 0.1, 0.05]; tile[:, tw-2:tw] = [0.05, 0.1, 0.05]
        tile[th//3:2*th//3, tw//4:3*tw//4] = [0.92, 0.95, 0.92]
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        # Sign Sector Blue
        y0, y1, x0, x1 = pslice(cls.RECTS["sign_sector_blue"])
        tw, th = x1 - x0, y1 - y0
        tile = np.full((th, tw, 3), [0.10, 0.28, 0.55], dtype=np.float32)
        tile[0:2, :] = [0.05, 0.1, 0.2]; tile[th-2:th, :] = [0.05, 0.1, 0.2]
        tile[:, 0:2] = [0.05, 0.1, 0.2]; tile[:, tw-2:tw] = [0.05, 0.1, 0.2]
        tile[th//3:2*th//3, tw//4:3*tw//4] = [0.95, 0.95, 0.95]
        atlas[y0:y1, x0:x1, :3] = np.clip(tile, 0.0, 1.0)

        return atlas

    @classmethod
    def get_or_create_blender_image(cls, wear_level: float = 0.5, seed: int = 42) -> bpy.types.Image:
        """
        Creates or updates a packed Blender Image with procedural PS1 pixel atlas.
        """
        image_name = f"ps1_atlas_w{int(wear_level * 100)}_s{seed}"
        if image_name in bpy.data.images:
            return bpy.data.images[image_name]

        # Generate pixel data
        pixels_array = cls.generate_atlas_pixels(wear_level=wear_level, seed=seed)
        flat_pixels = pixels_array.flatten()

        image = bpy.data.images.new(image_name, width=cls.WIDTH, height=cls.HEIGHT)
        image.pixels.foreach_set(flat_pixels)
        image.pack()
        return image
