#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
    """docstring for Application."""
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title('FSM')

        self.pack(side = 'left')
        self.create_widgets()


    def create_widgets(self):
        # Cria barra de menus
        self.create_menubar()

        # Cria frame de botoes
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side = 'left')

        self.operations_label = tk.Label(self.buttons_frame)
        self.operations_label['text'] = 'Operaçoes com automatos'
        self.operations_label['justify'] = 'center'
        self.operations_label['pady'] = '5'
        self.operations_label['padx'] = '5'
        self.operations_label['font'] = 'bold 10'
        self.operations_label['fg'] = '#006400'
        self.operations_label.pack()

        self.create_buttons()

        # Cria frame de abas
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side = 'left')
        self.empty_content_label = tk.Label(self.content_frame)
        self.empty_content_label['text'] = 'Frame de abas'
        self.empty_content_label.pack()




    def create_menubar(self):
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu = self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label = 'Novo automato')
        self.file_menu.add_command(label = 'Abrir automato')
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Sair', command = self.exit)
        self.menubar.add_cascade(label = 'Arquivo', menu = self.file_menu)


    def create_buttons(self):
        # Botao para conversao AFN -> AFD
        self.afn2afd_button = tk.Button(self.buttons_frame, text = 'AFN -> AFD')
        self.stylize_button(self.afn2afd_button)
        self.afn2afd_button.pack()

        # Botao para calculo da Acessibilidade
        self.accessibility_button = tk.Button(self.buttons_frame, text = 'Acessibilidade')
        self.stylize_button(self.accessibility_button)
        self.accessibility_button.pack()

        # Botao para o calculo da Co-acessibilidade
        self.co_accessibility_button = tk.Button(self.buttons_frame, text = 'Co-acessibilidade')
        self.stylize_button(self.co_accessibility_button)
        self.co_accessibility_button.pack()

        # Botao para o calculo do Trim
        self.trim_button = tk.Button(self.buttons_frame, text = 'Trim')
        self.stylize_button(self.trim_button)
        self.trim_button.pack()

        # Botao para o calculo da composicao paralela
        self.parallel_composition_button = tk.Button(self.buttons_frame, text = 'Composição paralela')
        self.stylize_button(self.parallel_composition_button)
        self.parallel_composition_button.pack()

        # Botao para o calculo do produto
        self.product_button = tk.Button(self.buttons_frame, text = 'Produto')
        self.stylize_button(self.product_button)
        self.product_button.pack()

        # Botao para o calculo da minimizacao
        self.minimization_button = tk.Button(self.buttons_frame, text = 'Minimização')
        self.stylize_button(self.minimization_button)
        self.minimization_button.pack()


    def stylize_button(self, button):
        """Aplica a estilizacao aos botoes."""
        BUTTON_WIDTH = '20'
        BUTTON_HEIGHT = '2'

        button['width'] = BUTTON_WIDTH
        button['height'] = BUTTON_HEIGHT


    def exit(self):
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
