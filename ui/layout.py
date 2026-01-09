import customtkinter
from ui.theme import COLOR1, COLOR2, COLOR3, COLOR4, COLOR5, COLOR6, COLOR7, BUTTON_PADX, BUTTON_PADY, LEFT_EDGE_PADX, RIGHT_EDGE_PADX, EDGE_LEFT_ADJUST_UNITS, EDGE_RIGHT_ADJUST_UNITS, smart_hover_color_for
import os

def create_buttons(frame_body, insert_value, toggle_sign, calculate, clear_entry, clean_screen, handle_backspace, handle_percent, handle_reciprocal, handle_square, handle_sqrt):
    for c in range(4):
        try:
            frame_body.grid_columnconfigure(c, weight=0)
        except Exception:
            pass
    for r in range(6):
        try:
            frame_body.grid_rowconfigure(r, weight=0)
        except Exception:
            pass

    def make_btn(text, cmd, font_family, text_color, fg_color):
        return customtkinter.CTkButton(frame_body, command=cmd, text=text, font=(font_family, 18), text_color=text_color, fg_color=fg_color, width=77, height=50, corner_radius=6, hover_color=smart_hover_color_for(fg_color), cursor='hand2')
    make_btn('%', handle_percent, 'Segoe UI Symbol', COLOR3, COLOR2).grid(row=0, column=0, padx=(LEFT_EDGE_PADX, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('CE', clear_entry, 'Segoe UI', COLOR3, COLOR2).grid(row=0, column=1, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('C', clean_screen, 'Segoe UI', COLOR3, COLOR2).grid(row=0, column=2, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('⌫', handle_backspace, 'Segoe UI Symbol', COLOR3, COLOR2).grid(row=0, column=3, padx=(0, RIGHT_EDGE_PADX), pady=(0, BUTTON_PADY))
    make_btn('⅟𝑥', handle_reciprocal, 'Segoe UI', COLOR3, COLOR2).grid(row=1, column=0, padx=(LEFT_EDGE_PADX, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('𝑥²', handle_square, 'Segoe UI', COLOR3, COLOR2).grid(row=1, column=1, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('²√𝑥', handle_sqrt, 'Segoe UI', COLOR3, COLOR2).grid(row=1, column=2, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('÷', lambda: insert_value('/'), 'Segoe UI', COLOR3, COLOR2).grid(row=1, column=3, padx=(0, RIGHT_EDGE_PADX), pady=(0, BUTTON_PADY))
    make_btn('7', lambda: insert_value('7'), 'Segoe UI', COLOR3, COLOR4).grid(row=2, column=0, padx=(LEFT_EDGE_PADX, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('8', lambda: insert_value('8'), 'Segoe UI', COLOR3, COLOR4).grid(row=2, column=1, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('9', lambda: insert_value('9'), 'Segoe UI', COLOR3, COLOR4).grid(row=2, column=2, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('×', lambda: insert_value('*'), 'Segoe UI Symbol', COLOR3, COLOR2).grid(row=2, column=3, padx=(0, RIGHT_EDGE_PADX), pady=(0, BUTTON_PADY))
    make_btn('4', lambda: insert_value('4'), 'Segoe UI', COLOR3, COLOR4).grid(row=3, column=0, padx=(LEFT_EDGE_PADX, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('5', lambda: insert_value('5'), 'Segoe UI', COLOR3, COLOR4).grid(row=3, column=1, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('6', lambda: insert_value('6'), 'Segoe UI', COLOR3, COLOR4).grid(row=3, column=2, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('−', lambda: insert_value('-'), 'Segoe UI Symbol', COLOR3, COLOR2).grid(row=3, column=3, padx=(0, RIGHT_EDGE_PADX), pady=(0, BUTTON_PADY))
    make_btn('1', lambda: insert_value('1'), 'Segoe UI', COLOR3, COLOR4).grid(row=4, column=0, padx=(LEFT_EDGE_PADX, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('2', lambda: insert_value('2'), 'Segoe UI', COLOR3, COLOR4).grid(row=4, column=1, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('3', lambda: insert_value('3'), 'Segoe UI', COLOR3, COLOR4).grid(row=4, column=2, padx=(0, BUTTON_PADX), pady=(0, BUTTON_PADY))
    make_btn('+', lambda: insert_value('+'), 'Segoe UI Symbol', COLOR3, COLOR2).grid(row=4, column=3, padx=(0, RIGHT_EDGE_PADX), pady=(0, BUTTON_PADY))
    make_btn('±', toggle_sign, 'Segoe UI Symbol', COLOR3, COLOR2).grid(row=5, column=0, padx=(LEFT_EDGE_PADX, BUTTON_PADX), pady=(0, 0))
    make_btn('0', lambda: insert_value('0'), 'Segoe UI', COLOR3, COLOR4).grid(row=5, column=1, padx=(0, BUTTON_PADX), pady=(0, 0))
    make_btn(',', lambda: insert_value(','), 'Segoe UI', COLOR3, COLOR2).grid(row=5, column=2, padx=(0, BUTTON_PADX), pady=(0, 0))
    customtkinter.CTkButton(frame_body, command=calculate, text='=', font=('Segoe UI Symbol', 18), text_color=COLOR1, fg_color=COLOR7, width=77, height=50, corner_radius=6, hover_color=smart_hover_color_for(COLOR7), cursor='hand2').grid(row=5, column=3, padx=(0, RIGHT_EDGE_PADX), pady=(0, 0))
    try:
        auto = os.getenv('CALC_UI_AUTO_CALIBRATE') == '1'
    except Exception:
        auto = False
    if auto:
        try:
            frame_body.update_idletasks()
            h_spaces = []
            v_spaces = []
            for r in range(6):
                for c in range(3):
                    a = frame_body.grid_slaves(row=r, column=c)
                    b = frame_body.grid_slaves(row=r, column=c + 1)
                    if a and b:
                        h_spaces.append(b[0].winfo_x() - (a[0].winfo_x() + a[0].winfo_width()))
            for r in range(5):
                for c in range(4):
                    a = frame_body.grid_slaves(row=r, column=c)
                    b = frame_body.grid_slaves(row=r + 1, column=c)
                    if a and b:
                        v_spaces.append(b[0].winfo_y() - (a[0].winfo_y() + a[0].winfo_height()))
            t = 3.0
            avg_h = sum(h_spaces) / len(h_spaces) if h_spaces else t
            avg_v = sum(v_spaces) / len(v_spaces) if v_spaces else t
            scale = 1.0
            try:
                if hasattr(customtkinter, 'get_widget_scaling'):
                    s = customtkinter.get_widget_scaling()
                    if s:
                        scale = float(s)
                elif hasattr(customtkinter, 'get_window_scaling'):
                    s = customtkinter.get_window_scaling()
                    if s:
                        scale = float(s)
            except Exception:
                pass
            delta_padx = (t - avg_h) / scale
            delta_pady = (t - avg_v) / scale
            new_padx = max(0.0, BUTTON_PADX + delta_padx)
            new_pady = max(0.0, BUTTON_PADY + delta_pady)
            try:
                rows = []
                for w in frame_body.grid_slaves():
                    info = w.grid_info()
                    if 'row' in info:
                        rows.append(int(info['row']))
                last_row = max(rows) if rows else 5
            except Exception:
                last_row = 5
            for r in range(last_row):
                for c in range(4):
                    cells = frame_body.grid_slaves(row=r, column=c)
                    if cells:
                        try:
                            cells[0].grid_configure(padx=(new_padx + EDGE_LEFT_ADJUST_UNITS, new_padx) if c == 0 else (0, new_padx + EDGE_RIGHT_ADJUST_UNITS) if c == 3 else (0, new_padx), pady=(0, new_pady))
                        except Exception:
                            pass
            for c in range(4):
                cells = frame_body.grid_slaves(row=last_row, column=c)
                if cells:
                    try:
                        cells[0].grid_configure(pady=(0, 0))
                    except Exception:
                        pass
        except Exception:
            pass
