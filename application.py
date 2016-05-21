#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from automaton import *
from tab import *

class Application(tk.Frame):
    """docstring for Application."""

    def __init__(self, master = None):
        """"""
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title('FSM')
        self.grid(column = 1, row = 1, sticky = tk.NW)

        self.create_widgets()


    def create_widgets(self):
        """"""
        # Cria barra de menus
        self.create_menubar()

        # Cria frame de botoes
        self.create_buttons_frame()

        # Cria frame para exibicao dos automatos
        self.create_tabbed_frame()


    def create_tabbed_frame(self):
        """"""
        self.tabbed_frame = ttk.Notebook(self, padding = '5 20 5 5')


    def add_tab(self, tab):
        """"""
        if len(self.tabbed_frame.tabs()) == 0:
            self.tabbed_frame.grid(column = 2, row = 1, sticky = tk.N)
        self.tabbed_frame.add(tab, text = tab.get_file_name())


    def create_buttons_frame(self):
        """"""
        self.tabbed_buttons_frame = ttk.Notebook(self, padding = '5 20 5 5')

        self.buttons_frame = tk.Frame(self.tabbed_buttons_frame)
        self.buttons_frame.pack()
        self.buttons_frame['pady'] = '4'
        self.buttons_frame['padx'] = '4'

        self.tabbed_buttons_frame.add(self.buttons_frame, text = 'Operações com automatos')
        self.tabbed_buttons_frame.grid(row = 1, column = 1, sticky = tk.N)

        self.create_buttons()


    def create_menubar(self):
        """"""
        self.file_opt = options = {}
        self.file_opt['filetypes'] = [('arquivos fsm', '.fsm')]
        self.file_opt['title'] = 'Selecione um arquivo'

        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu = self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label = 'Novo automato')
        self.file_menu.add_command(label = 'Abrir automato', command = self.select_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Sair', command = self.exit)
        self.menubar.add_cascade(label = 'Arquivo', menu = self.file_menu)


    def create_buttons(self):
        """"""
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


    def select_file(self):
        """Abre caixa de dialogo para selecao do arquivo"""
        file_name = filedialog.askopenfilename(**self.file_opt)
        if file_name:
            tab = Tab(file_name, self.tabbed_frame)
            self.add_tab(tab)



    def stylize_button(self, button):
        """Aplica a estilizacao aos botoes."""
        BUTTON_WIDTH = '20'
        BUTTON_HEIGHT = '2'
        button['width'] = BUTTON_WIDTH
        button['height'] = BUTTON_HEIGHT


    def exit(self):
        """"""
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
