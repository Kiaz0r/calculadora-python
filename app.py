import os
from pathlib import Path
import webbrowser
import customtkinter
from decimal import Decimal, getcontext, DivisionByZero
from core.engine import evaluate_decimal_expr, strip_trailing_ops, normalize_decimal_tokens, tokenize, apply_op, result_exceeds_limits, decimal_to_str
from core.formatting import format_display
from core.operations import percent_expr, reciprocal_expr, square_expr, sqrt_expr, toggle_sign_expr, clear_entry_expr, backspace_expr
from core.constants import APP_VERSION, APP_AUTHOR, APP_SITE
window = customtkinter.CTk()
window.title('Calculadora')
window.geometry('319x457')
window.resizable(False, False)
ICON_PATH = Path(__file__).parent / 'assets' / 'img' / 'icon.ico'
try:
    window.iconbitmap(str(ICON_PATH))
except Exception:
    pass
from ui.theme import COLOR1, COLOR2, COLOR3, COLOR4, COLOR5, COLOR6, COLOR7, COLOR8, COLOR9, COLOR10, ENTRY_DIGIT_LIMIT, DISPLAY_MAX_FONT, DISPLAY_MIN_FONT, DISPLAY_AVAILABLE_WIDTH, apply_dark_theme, BUTTON_PADX, BUTTON_PADY, LEFT_EDGE_PADX, RIGHT_EDGE_PADX, FOOTER_PADX, FOOTER_PADY, apply_transparency, HISTORY_FONT_SIZE
from ui.utils import get_current_entry, build_unary_overlay, adjust_display_font, format_history_ops, compute_display_entry
from ui.layout import create_buttons
apply_dark_theme()
apply_transparency(window)
window.config(background=COLOR1)
text_value = customtkinter.StringVar()
history_value = customtkinter.StringVar()
ALL_VALUE = ''
LAST_OP = None
LAST_OPERAND = None
getcontext().prec = 28
PENDING_HISTORY_OVERLAY = ''
SHOW_ENTRY_ONLY = False
ENTRY_STARTED = False

def insert_value(event):
    global ALL_VALUE, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, LAST_OP, LAST_OPERAND, ENTRY_STARTED
    ch = str(event)
    if ch == '.':
        return
    if ch.isdigit():
        current = get_current_entry(ALL_VALUE)
        digit_count = sum((1 for c in current if c.isdigit()))
        if digit_count >= ENTRY_DIGIT_LIMIT:
            return
    if ch == ',':
        current = get_current_entry(ALL_VALUE)
        if ',' in current:
            return
    if ch in '+-*/':
        if not ALL_VALUE:
            if ch == '-':
                ALL_VALUE = '0-'
                SHOW_ENTRY_ONLY = True
                ENTRY_STARTED = False
                update_display()
            return
        if ALL_VALUE[-1] in '+-*/':
            ALL_VALUE = ALL_VALUE[:-1] + ch
        else:
            op_map = {'*': '×', '/': '÷', '+': '+', '-': '-'}
            try:
                history_value.set(f"{format_display(get_current_entry(ALL_VALUE))} {op_map.get(ch, ch)} ")
            except Exception:
                history_value.set(f"{get_current_entry(ALL_VALUE)} {op_map.get(ch, ch)} ")
            SHOW_ENTRY_ONLY = True
            ENTRY_STARTED = False
            try:
                LAST_OP = ch
                ce = get_current_entry(ALL_VALUE)
                LAST_OPERAND = Decimal(ce.replace(',', '.'))
            except Exception:
                LAST_OPERAND = None
            ALL_VALUE = ALL_VALUE + ch
        update_display()
        return
    if (ch.isdigit() or ch == ',') and SHOW_ENTRY_ONLY:
        ENTRY_STARTED = True
    ALL_VALUE = ALL_VALUE + ch
    update_display()

def update_display():
    global ENTRY_STARTED
    try:
        s = compute_display_entry(ALL_VALUE, SHOW_ENTRY_ONLY, ENTRY_STARTED)
    except Exception:
        s = ALL_VALUE
    text_value.set(format_display(s))
    try:
        adjust_display_font(app_label, text_value.get(), DISPLAY_MIN_FONT, DISPLAY_MAX_FONT, DISPLAY_AVAILABLE_WIDTH)
    except Exception:
        pass

def calculate():
    global ALL_VALUE, LAST_OP, LAST_OPERAND, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, ENTRY_STARTED
    SHOW_ENTRY_ONLY = False
    ENTRY_STARTED = False
    try:
        expr_display = format_display(ALL_VALUE)
        expr_norm = strip_trailing_ops(normalize_decimal_tokens(ALL_VALUE))
        expr_eval = expr_norm.replace(',', '.')
        tokens = tokenize(expr_eval)
        if len(tokens) == 1 and tokens[0][0] == 'num' and LAST_OP and (LAST_OPERAND is not None):
            current = Decimal(tokens[0][1])
            res = apply_op(LAST_OP, current, LAST_OPERAND)
            if result_exceeds_limits(res):
                text_value.set('Erro')
                history_value.set('')
                return
            res_str = decimal_to_str(res)
            ALL_VALUE = res_str
            op_map = {'*': '×', '/': '÷', '+': '+', '-': '-'}
            current_disp = format_display(decimal_to_str(current))
            operand_disp = format_display(decimal_to_str(LAST_OPERAND))
            expr_hist = f'{current_disp} {op_map.get(LAST_OP, LAST_OP)} {operand_disp}'
            history_target = PENDING_HISTORY_OVERLAY if PENDING_HISTORY_OVERLAY else expr_hist
            history_value.set(f'{format_history_ops(history_target)} =')
            PENDING_HISTORY_OVERLAY = ''
            update_display()
            return
        if len(tokens) >= 3 and tokens[-1][0] == 'num' and (tokens[-2][0] == 'op'):
            LAST_OP = tokens[-2][1]
            LAST_OPERAND = Decimal(tokens[-1][1])
        res = evaluate_decimal_expr(ALL_VALUE)
        if result_exceeds_limits(res):
            text_value.set('Erro')
            history_value.set('')
            return
        res_str = decimal_to_str(res)
        ALL_VALUE = res_str
        history_target = PENDING_HISTORY_OVERLAY if PENDING_HISTORY_OVERLAY else format_history_ops(expr_display)
        history_value.set(f'{format_history_ops(history_target)} =')
        PENDING_HISTORY_OVERLAY = ''
        update_display()
    except DivisionByZero:
        text_value.set('Erro')
        history_value.set('')
    except Exception:
        text_value.set('Erro')
        history_value.set('')

def clean_screen():
    global ALL_VALUE, LAST_OP, LAST_OPERAND, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, ENTRY_STARTED
    ALL_VALUE = ''
    LAST_OP = None
    LAST_OPERAND = None
    PENDING_HISTORY_OVERLAY = ''
    SHOW_ENTRY_ONLY = False
    ENTRY_STARTED = False
    history_value.set('')
    update_display()

def handle_backspace():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY, ENTRY_STARTED
    PENDING_HISTORY_OVERLAY = ''
    try:
        last_ch = ALL_VALUE[-1] if ALL_VALUE else ''
    except Exception:
        last_ch = ''
    if SHOW_ENTRY_ONLY and ENTRY_STARTED and last_ch in '+-*/':
        update_display()
        return
    ALL_VALUE = backspace_expr(ALL_VALUE)
    try:
        last_ch = ALL_VALUE[-1] if ALL_VALUE else ''
    except Exception:
        last_ch = ''
    if SHOW_ENTRY_ONLY and last_ch in '+-*/':
        ENTRY_STARTED = True
    update_display()

def copy_to_clipboard():
    try:
        s = text_value.get() if text_value.get() else '0'
    except Exception:
        s = '0'
    try:
        window.clipboard_clear()
        window.clipboard_append(s)
    except Exception:
        pass

def paste_from_clipboard():
    try:
        s = window.clipboard_get()
    except Exception:
        return
    for ch in s:
        if ch.isdigit():
            insert_value(ch)
        elif ch in '+-*/':
            insert_value(ch)
        elif ch == ',':
            insert_value(',')
        elif ch == '.':
            insert_value(',')
        elif ch == '%':
            handle_percent()
        elif ch == '=':
            calculate()
    update_display()

def handle_keypress(e):
    ch = getattr(e, 'char', '')
    ks = getattr(e, 'keysym', '')
    if ch and ch.isdigit():
        insert_value(ch)
        return
    if ch in '+-*/':
        insert_value(ch)
        return
    if ch == ',' or ch == '.':
        insert_value(',')
        return
    if ch == '%':
        handle_percent()
        return
    if ch == '=':
        calculate()
        return
    if ks in ('KP_Add', 'plus'):
        insert_value('+')
        return
    if ks in ('KP_Subtract', 'minus'):
        insert_value('-')
        return
    if ks in ('KP_Multiply', 'asterisk'):
        insert_value('*')
        return
    if ks in ('KP_Divide', 'slash'):
        insert_value('/')
        return
    if ks in ('KP_Decimal', 'period', 'comma'):
        insert_value(',')
        return
window.bind('<BackSpace>', lambda e: handle_backspace())
window.bind('<Return>', lambda e: calculate())
window.bind('<KP_Enter>', lambda e: calculate())
window.bind('<Escape>', lambda e: clean_screen())
window.bind('<Delete>', lambda e: clear_entry())
window.bind('<F9>', lambda e: toggle_sign())
window.bind('<Control-c>', lambda e: copy_to_clipboard())
window.bind('<Control-v>', lambda e: paste_from_clipboard())
window.bind_all('<Key>', handle_keypress)

def handle_reciprocal():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, ENTRY_STARTED
    orig_expr = ALL_VALUE
    new_expr, error = reciprocal_expr(orig_expr)
    if error:
        text_value.set('Erro')
        history_value.set('')
        return
    ALL_VALUE = new_expr
    overlay = build_unary_overlay(orig_expr, 'reciprocal')
    PENDING_HISTORY_OVERLAY = overlay
    history_value.set(f'{format_history_ops(overlay)} =')
    SHOW_ENTRY_ONLY = True
    ENTRY_STARTED = True
    PENDING_HISTORY_OVERLAY = ''
    update_display()

def handle_square():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, ENTRY_STARTED
    orig_expr = ALL_VALUE
    new_expr, error = square_expr(orig_expr)
    if error:
        text_value.set('Erro')
        history_value.set('')
        return
    ALL_VALUE = new_expr
    overlay = build_unary_overlay(orig_expr, 'square')
    PENDING_HISTORY_OVERLAY = overlay
    history_value.set(f'{format_history_ops(overlay)} =')
    SHOW_ENTRY_ONLY = True
    ENTRY_STARTED = True
    PENDING_HISTORY_OVERLAY = ''
    update_display()

def handle_sqrt():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, ENTRY_STARTED
    orig_expr = ALL_VALUE
    new_expr, error = sqrt_expr(orig_expr)
    if error:
        overlay = build_unary_overlay(orig_expr, 'sqrt_err')
        history_value.set(f'{format_history_ops(overlay)} =')
        text_value.set('Erro')
        PENDING_HISTORY_OVERLAY = ''
        return
    ALL_VALUE = new_expr
    overlay = build_unary_overlay(orig_expr, 'sqrt')
    PENDING_HISTORY_OVERLAY = overlay
    history_value.set(f'{format_history_ops(overlay)} =')
    SHOW_ENTRY_ONLY = True
    ENTRY_STARTED = True
    PENDING_HISTORY_OVERLAY = ''
    update_display()

def clear_entry():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY
    PENDING_HISTORY_OVERLAY = ''
    ALL_VALUE = clear_entry_expr(ALL_VALUE)
    update_display()

def handle_percent():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY, SHOW_ENTRY_ONLY, ENTRY_STARTED
    orig_expr = ALL_VALUE
    new_expr, error = percent_expr(orig_expr)
    if error:
        text_value.set('Erro')
        history_value.set('')
        return
    ALL_VALUE = new_expr
    overlay = build_unary_overlay(orig_expr, 'percent')
    PENDING_HISTORY_OVERLAY = overlay
    history_value.set(f'{format_history_ops(overlay)} =')
    SHOW_ENTRY_ONLY = True
    ENTRY_STARTED = True
    PENDING_HISTORY_OVERLAY = ''
    update_display()

def toggle_sign():
    global ALL_VALUE, PENDING_HISTORY_OVERLAY
    PENDING_HISTORY_OVERLAY = ''
    ALL_VALUE = toggle_sign_expr(ALL_VALUE)
    update_display()
frame_screen = customtkinter.CTkFrame(window, bg_color=COLOR1, fg_color=COLOR1, width=319, height=114, corner_radius=0)
frame_screen.grid(row=0, column=0)
app_label = customtkinter.CTkLabel(frame_screen, textvariable=text_value, font=('Segoe UI', 36, 'bold'), text_color=COLOR3, fg_color=COLOR1, width=299, height=47, padx=0, anchor='e')
app_label.place(x=10, y=57)
history_font = customtkinter.CTkFont(family='Segoe UI', size=HISTORY_FONT_SIZE)
history_label = customtkinter.CTkLabel(frame_screen, textvariable=history_value, font=history_font, text_color=COLOR10, fg_color=COLOR1, width=299, height=32, padx=0, anchor='e')
history_label.place(x=10, y=10)
frame_body = customtkinter.CTkFrame(window, bg_color=COLOR1, fg_color=COLOR1, width=319, height=305, corner_radius=0)
frame_body.grid(row=1, column=0)
frame_footer = customtkinter.CTkFrame(window, bg_color=COLOR1, fg_color=COLOR1, width=319, corner_radius=0)
frame_footer.grid(row=2, column=0, sticky='nsew', pady=(0, FOOTER_PADY))
frame_footer.grid_columnconfigure(0, weight=1)
frame_footer.grid_columnconfigure(1, weight=0)
frame_footer.grid_columnconfigure(2, weight=1)
content_footer = customtkinter.CTkFrame(frame_footer, fg_color=COLOR1)
content_footer.grid(row=0, column=1, padx=0, pady=0, sticky='nsew')
content_center = customtkinter.CTkFrame(content_footer, fg_color=COLOR1)
content_center.pack(expand=True)
base_font = customtkinter.CTkFont(family='Segoe UI', size=11)
bold_font = customtkinter.CTkFont(family='Segoe UI', size=11, weight='bold')
version_bold_label = customtkinter.CTkLabel(content_center, text=f'v{APP_VERSION}', font=bold_font, text_color=COLOR3, fg_color=COLOR1)
version_bold_label.pack(side='left')
text_before_label = customtkinter.CTkLabel(content_center, text=' — Projeto desenvolvido em ', font=base_font, text_color=COLOR3, fg_color=COLOR1)
text_before_label.pack(side='left')
python_bold_label = customtkinter.CTkLabel(content_center, text='Python', font=bold_font, text_color=COLOR3, fg_color=COLOR1)
python_bold_label.pack(side='left')
text_por_label = customtkinter.CTkLabel(content_center, text=' por ', font=base_font, text_color=COLOR3, fg_color=COLOR1)
text_por_label.pack(side='left')
author_label = customtkinter.CTkLabel(content_center, text=APP_AUTHOR, font=bold_font, text_color=COLOR3, fg_color=COLOR1, cursor='hand2')
author_label.pack(side='left')
author_label.bind('<Button-1>', lambda e: webbrowser.open(APP_SITE))
create_buttons(frame_body, insert_value, toggle_sign, calculate, clear_entry, clean_screen, handle_backspace, handle_percent, handle_reciprocal, handle_square, handle_sqrt)
if __name__ == '__main__':
    window.mainloop()
