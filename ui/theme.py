import customtkinter
import os
COLOR1 = '#282A36'
COLOR2 = '#44475A'
COLOR3 = '#F8F8F2'
COLOR4 = '#6272A4'
COLOR5 = '#3D4051'
COLOR6 = '#586794'
COLOR8 = '#E6A661'
COLOR7 = '#FFB86C'
COLOR9 = '#07070D'
COLOR10 = '#D8D8D2'
ENTRY_DIGIT_LIMIT = 16
DISPLAY_MAX_FONT = 36
DISPLAY_MIN_FONT = 24
DISPLAY_AVAILABLE_WIDTH = 299 - 2

def _get_ctk_scale() -> float:
    try:
        if hasattr(customtkinter, 'get_widget_scaling'):
            s = customtkinter.get_widget_scaling()
            if s:
                return float(s)
        if hasattr(customtkinter, 'get_window_scaling'):
            s = customtkinter.get_window_scaling()
            if s:
                return float(s)
    except Exception:
        pass
    return 1.0

def _px_to_grid_units(target_px: float) -> float:
    scale = _get_ctk_scale()
    try:
        return target_px / float(scale)
    except Exception:
        return target_px

def _env_float(name: str, default: float) -> float:
    try:
        v = os.getenv(name)
        if v is None:
            return default
        return float(v)
    except Exception:
        return default
H_VISUAL_BIAS_PX = _env_float('CALC_UI_H_VISUAL_BIAS_PX', -1.0)
V_VISUAL_BIAS_PX = _env_float('CALC_UI_V_VISUAL_BIAS_PX', 0.0)
BUTTON_PADX = max(0.0, _px_to_grid_units(3.0 + H_VISUAL_BIAS_PX))
BUTTON_PADY = max(0.0, _px_to_grid_units(3.0 + V_VISUAL_BIAS_PX))
EDGE_LEFT_BIAS_PX = _env_float('CALC_UI_EDGE_LEFT_BIAS_PX', 1.0)
EDGE_RIGHT_BIAS_PX = _env_float('CALC_UI_EDGE_RIGHT_BIAS_PX', 1.0)
EDGE_LEFT_ADJUST_UNITS = _px_to_grid_units(EDGE_LEFT_BIAS_PX)
EDGE_RIGHT_ADJUST_UNITS = _px_to_grid_units(EDGE_RIGHT_BIAS_PX)
LEFT_EDGE_PADX = max(0.0, BUTTON_PADX + EDGE_LEFT_ADJUST_UNITS)
RIGHT_EDGE_PADX = max(0.0, BUTTON_PADX + EDGE_RIGHT_ADJUST_UNITS)
FOOTER_MARGIN_PX = _env_float('CALC_UI_FOOTER_MARGIN_PX', 10.0)
FOOTER_PADX = max(0.0, _px_to_grid_units(FOOTER_MARGIN_PX))
FOOTER_PADY = max(0.0, _px_to_grid_units(FOOTER_MARGIN_PX))

def _darken_hex(hex_color: str, pct: float) -> str:
    try:
        s = hex_color.lstrip('#')
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        f = max(0.0, min(1.0, pct))
        r = max(0, min(255, int(r * (1.0 - f))))
        g = max(0, min(255, int(g * (1.0 - f))))
        b = max(0, min(255, int(b * (1.0 - f))))
        return f'#{r:02X}{g:02X}{b:02X}'
    except Exception:
        return hex_color

def hover_color_for(base_color: str) -> str:
    try:
        p = _env_float('CALC_UI_HOVER_DARKEN_PCT', 0.14)
    except Exception:
        p = 0.14
    return _darken_hex(base_color, p)

def _lighten_hex(hex_color: str, pct: float) -> str:
    try:
        s = hex_color.lstrip('#')
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        f = max(0.0, min(1.0, pct))
        r = max(0, min(255, int(r + (255 - r) * f)))
        g = max(0, min(255, int(g + (255 - g) * f)))
        b = max(0, min(255, int(b + (255 - b) * f)))
        return f'#{r:02X}{g:02X}{b:02X}'
    except Exception:
        return hex_color

def _relative_luminance(hex_color: str) -> float:
    try:
        s = hex_color.lstrip('#')
        r = int(s[0:2], 16) / 255.0
        g = int(s[2:4], 16) / 255.0
        b = int(s[4:6], 16) / 255.0

        def to_linear(c: float) -> float:
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        rl = to_linear(r)
        gl = to_linear(g)
        bl = to_linear(b)
        return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl
    except Exception:
        return 0.5

def smart_hover_color_for(base_color: str) -> str:
    try:
        t = _env_float('CALC_UI_HOVER_LUMA_THRESHOLD', 0.35)
    except Exception:
        t = 0.35
    try:
        lp = _env_float('CALC_UI_HOVER_LIGHTEN_PCT', 0.12)
    except Exception:
        lp = 0.12
    try:
        dp = _env_float('CALC_UI_HOVER_DARKEN_PCT', 0.14)
    except Exception:
        dp = 0.14
    return _lighten_hex(base_color, lp) if _relative_luminance(base_color) < t else _darken_hex(base_color, dp)

def apply_dark_theme() -> None:
    try:
        customtkinter.set_appearance_mode('dark')
    except Exception:
        pass

def apply_transparency(window) -> None:
    try:
        alpha = _env_float('CALC_UI_ALPHA', 0.99)
    except Exception:
        alpha = 1.0
    try:
        if alpha < 0.1:
            alpha = 0.1
        if alpha > 1.0:
            alpha = 1.0
    except Exception:
        pass
    try:
        window.attributes('-alpha', alpha)
    except Exception:
        pass

try:
    HISTORY_FONT_SIZE = int(_env_float('CALC_UI_HISTORY_FONT_SIZE', 16))
except Exception:
    HISTORY_FONT_SIZE = 16
try:
    if HISTORY_FONT_SIZE < 10:
        HISTORY_FONT_SIZE = 10
    if HISTORY_FONT_SIZE > 24:
        HISTORY_FONT_SIZE = 24
except Exception:
    pass
