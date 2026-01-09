from typing import Optional, Tuple
from tkinter import font as tkfont
from core.formatting import format_display
import re

def get_current_entry(expr: str) -> str:
    if not expr:
        return ''
    i = len(expr) - 1
    while i >= 0 and (not (expr[i].isdigit() or expr[i] == ',')):
        i -= 1
    if i < 0:
        return ''
    end = i + 1
    j = i
    while j >= 0 and (expr[j].isdigit() or expr[j] == ','):
        j -= 1
    if j >= 0 and expr[j] == '-' and (j == 0 or expr[j - 1] in '+-*/'):
        start = j
    else:
        start = j + 1
    return expr[start:end]

def get_current_entry_span(expr: str) -> Optional[Tuple[int, int]]:
    if not expr:
        return None
    i = len(expr) - 1
    while i >= 0 and (not (expr[i].isdigit() or expr[i] == ',')):
        i -= 1
    if i < 0:
        return None
    end = i + 1
    j = i
    while j >= 0 and (expr[j].isdigit() or expr[j] == ','):
        j -= 1
    if j >= 0 and expr[j] == '-' and (j == 0 or expr[j - 1] in '+-*/'):
        start = j
    else:
        start = j + 1
    return (start, end)

def build_unary_overlay(expr: str, kind: str) -> str:
    span = get_current_entry_span(expr)
    if not span:
        return format_display(expr)
    start, end = span
    prefix_raw = expr[:start]
    suffix_raw = expr[end:]
    prefix = format_display(prefix_raw) if prefix_raw else ''
    suffix = format_display(suffix_raw) if suffix_raw else ''
    num = expr[start:end]
    num_disp = format_display(num)
    if kind == 'reciprocal':
        mid = f'1/({num_disp})'
    elif kind == 'square':
        mid = f'({num_disp})²'
    elif kind == 'percent':
        mid = f'{num_disp}%'
    elif kind == 'sqrt_err':
        mid = f'√({num_disp})'
    elif kind == 'sqrt':
        mid = f'√({num_disp})'
    else:
        mid = num_disp
    return prefix + mid + suffix

def get_available_width(app_label, fallback_width: int) -> int:
    try:
        info = app_label.configure()
        width = info.get('width')
        pad = info.get('padx')
        if isinstance(pad, tuple):
            pad = sum(pad)
        else:
            pad = 11
        if not width or width <= 0:
            return fallback_width
        return max(10, int(width) - pad * 2 - 2)
    except Exception:
        return fallback_width

def adjust_display_font(app_label, text: str, min_size: int, max_size: int, fallback_width: int) -> None:
    avail = get_available_width(app_label, fallback_width)
    low = min_size
    high = max_size
    best = low
    while low <= high:
        mid = (low + high) // 2
        f = tkfont.Font(family='Segoe UI', size=mid, weight='bold')
        width_px = f.measure(text)
        if width_px <= avail:
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    try:
        app_label.configure(font=('Segoe UI', best, 'bold'))
    except Exception:
        pass

def format_history_ops(expr: str) -> str:
    if not expr:
        return ''
    s = expr
    s = re.sub(r"\s*\*\s*", " × ", s)
    s = re.sub(r"\s*/\s*", " ÷ ", s)
    s = re.sub(r"(?<=[0-9),²%])\s*\+\s*(?=[0-9(√])", " + ", s)
    s = re.sub(r"(?<=[0-9),²%])\s*-\s*(?=[0-9(√])", " - ", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def compute_display_entry(all_value: str, show_entry_only: bool, entry_started: bool) -> str:
    try:
        last_ch = all_value[-1] if all_value else ''
    except Exception:
        last_ch = ''
    if show_entry_only:
        if entry_started and last_ch in '+-*/':
            return '0'
        try:
            return get_current_entry(all_value)
        except Exception:
            return all_value
    return all_value
