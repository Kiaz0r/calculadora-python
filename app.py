import customtkinter  # Biblioteca com estilos customizados 'CustomTkinter'

# Paleta de cores 'Dracula Theme'
COLOR1 = '#282A36'
COLOR2 = '#44475A'
COLOR3 = '#F8F8F2'
COLOR4 = '#6272A4'
COLOR5 = '#606580'
COLOR6 = '#434E71'
COLOR7 = '#FFB86C'
COLOR8 = '#CC9356'

# Configurações da Janela
window = customtkinter.CTk()
window.title('Calculadora')
window.geometry('319x394')
window.config(background=COLOR1)

# Aplicar o estilo 'Dark' do CustomTkinter
customtkinter.set_appearance_mode('dark')

# Funções para realizar os calculos
text_value = customtkinter.StringVar()
ALL_VALUE = ''  # Variável para armazenar todos os valores


def insert_value(event):
    global ALL_VALUE
    ALL_VALUE = ALL_VALUE + str(event)
    text_value.set(ALL_VALUE)


def calculate():
    global ALL_VALUE
    result = eval(ALL_VALUE)
    text_value.set(str(result))


def clean_screen():
    global ALL_VALUE
    ALL_VALUE = ''
    text_value.set('')


# Criando divisões na janela usando 'Frame' para o Visor e Corpo
frame_screen = customtkinter.CTkFrame(
    window, bg_color=COLOR1, fg_color=COLOR1,
    width=319, height=129, corner_radius=0)
frame_screen.grid(row=0, column=0)

frame_body = customtkinter.CTkFrame(
    window, bg_color=COLOR1, fg_color=COLOR1,
    width=319, height=265, corner_radius=0)
frame_body.grid(row=1, column=0)

# Criando visor para exibir as funções usando 'Label'
app_label = customtkinter.CTkLabel(
    frame_screen, textvariable=text_value,
    font=('Consolas', 50), text_color=COLOR3, fg_color=COLOR1,
    width=319, height=129, padx=11, anchor='e')
app_label.place(x=0, y=0)

# Criando Botões
Button1 = customtkinter.CTkButton(
    frame_body, command=clean_screen, text='CE',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button1.place(x=3, y=0)

# Botão 'C' para corrigir um valor inserido. Ainda não funciona corretamente.
Button2 = customtkinter.CTkButton(
    frame_body, text='C',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button2.place(x=82, y=0)

# Botão '%' para calcular porcentagem. Ainda não funciona corretamente.
Button3 = customtkinter.CTkButton(
    frame_body, text='%',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button3.place(x=161, y=0)

Button4 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('/'), text='÷',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button4.place(x=240, y=0)

Button5 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('7'), text='7',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button5.place(x=3, y=53)

Button6 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('8'), text='8',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button6.place(x=82, y=53)

Button7 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('9'), text='9',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button7.place(x=161, y=53)

Button8 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('*'), text='x',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button8.place(x=240, y=53)

Button9 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('4'), text='4',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button9.place(x=3, y=106)

Button10 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('5'), text='5',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button10.place(x=82, y=106)

Button11 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('6'), text='6',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button11.place(x=161, y=106)

Button12 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('-'), text='-',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button12.place(x=240, y=106)

Button13 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('1'), text='1',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button13.place(x=3, y=159)

Button14 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('2'), text='2',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button14.place(x=82, y=159)

Button15 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('3'), text='3',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button15.place(x=161, y=159)

Button16 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('+'), text='+',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button16.place(x=240, y=159)

Button17 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value(','), text=',',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button17.place(x=3, y=212)

Button18 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('0'), text='0',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR4,
    width=77, height=50, corner_radius=6, hover_color=COLOR6, cursor='hand2')
Button18.place(x=82, y=212)

Button19 = customtkinter.CTkButton(
    frame_body, command=lambda: insert_value('.'), text='.',
    font=('Calibri Bold', 18), text_color=COLOR3, fg_color=COLOR2,
    width=77, height=50, corner_radius=6, hover_color=COLOR5, cursor='hand2')
Button19.place(x=161, y=212)

Button20 = customtkinter.CTkButton(
    frame_body, command=calculate, text='=',
    font=('Calibri Bold', 18), text_color=COLOR1, fg_color=COLOR7,
    width=77, height=50, corner_radius=6, hover_color=COLOR8, cursor='hand2')
Button20.place(x=240, y=212)

window.mainloop()
