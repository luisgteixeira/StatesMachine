#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from automaton import *
from automaton_operation import *
from tab import *
from file_manager import *

class Application(tk.Frame):
    """Classe responsavel pela exibicao da interface grafica."""

    def __init__(self, master = None):
        """Construtor da classe Application."""
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title('FSM')
        self.grid(column = 1, row = 1, sticky = tk.NW)

        self.opened_tabs = [] # Lista de abas abertas
        self.opened_files = [] # Lista de arquivos abertos

        self.create_widgets()


    def create_widgets(self):
        """Cria todos os widgets da interface."""
        # Cria barra de menus
        self.create_menubar()

        # Cria frame de botoes
        self.create_buttons_frame()

        # Cria frame para exibicao dos automatos
        self.create_tabbed_frame()


    def create_tabbed_frame(self):
        """Cria o frame principal, onde sao exibidos os automatos."""
        self.tabbed_frame = ttk.Notebook(self, padding = '5 20 5 5')


    def add_tab(self, tab):
        """Adiciona uma aba ao frame principal."""
        if self.tabbed_frame.index('end') == 0:
            self.tabbed_frame.grid(column = 2, row = 1, sticky = tk.N)
        self.tabbed_frame.add(tab, text = tab.get_file_name())
        tab_id = self.tabbed_frame.index('end') - 1
        self.tabbed_frame.select(tab_id)


    def create_buttons_frame(self):
        """Cria o frame que abriga os botoes de operacoes."""
        self.tabbed_buttons_frame = ttk.Notebook(self, padding = '5 20 5 5')

        self.buttons_frame = tk.Frame(self.tabbed_buttons_frame)
        self.buttons_frame.pack()
        self.buttons_frame['pady'] = '4'
        self.buttons_frame['padx'] = '4'

        self.tabbed_buttons_frame.add(self.buttons_frame, text = 'Operações com automatos')
        self.tabbed_buttons_frame.grid(row = 1, column = 1, sticky = tk.N)

        self.create_buttons()


    def create_menubar(self):
        """Cria a barra de menus."""
        # Define opcoes para dialogo de selecao de arquivo
        self.file_opt = options = {}
        self.file_opt['filetypes'] = [('arquivos fsm', '.fsm')]
        self.file_opt['title'] = 'Selecione um arquivo'

        # Configura a barra de menus
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu = self.menubar)

        # Adiciona os elementos na barra de menus
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label = 'Novo automato')
        self.file_menu.add_command(label = 'Abrir automato', command = self.select_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Sair', command = self.exit)
        self.menubar.add_cascade(label = 'Arquivo', menu = self.file_menu)


    def create_buttons(self):
        """Cria os botoes de operacoes."""
        # Botao para conversao AFN -> AFD
        self.afn2afd_button = tk.Button(self.buttons_frame, text = 'AFN -> AFD')
        self.stylize_button(self.afn2afd_button)
        self.afn2afd_button.pack()

        # Botao para calculo da Acessibilidade
        self.accessibility_button = tk.Button(self.buttons_frame,
            text = 'Acessibilidade', command = self.op_accessibility)
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


    ###########################################################################
    # Acoes dos widgets
    ###########################################################################

    def select_file(self):
        """Abre caixa de dialogo para selecao do arquivo."""
        file_path = filedialog.askopenfilename(**self.file_opt)
        if file_path:
            # Verifica se o arquivo ja esta aberto
            if file_path in self.opened_files:
                self.tabbed_frame.select(self.opened_files.index(file_path))
                return

            automaton = self.open_file(file_path)

            tab = Tab(os.path.basename(file_path), automaton, self.tabbed_frame)
            self.add_tab(tab)
            self.opened_tabs.append(tab)
            self.opened_files.append(file_path)


    def open_file(self, file_path):
        """Abre o arquivo e constroi o automato."""
        fm = FileManager()
        file_content = fm.read_input(file_path)

        states = file_content[0]
        events = file_content[1]
        initial_state = file_content[2]
        marked_states = file_content[3]
        transitions = file_content[4:]

        automaton = Automaton(states, events, initial_state, marked_states, transitions)
        return automaton


    def exit(self):
        """Encerra a execucao do programa."""
        self.parent.destroy()


    def op_accessibility(self):
        print('Selecionada operacao de Acessibilidade.')
        if self.tabbed_frame.index('end') == 0:
            messagebox.showerror('Erro', 'Não há nenhum autômato aberto.')
        else:
            selected_tab_index = self.tabbed_frame.index('current')
            selected_tab = self.opened_tabs[selected_tab_index]
            automaton = selected_tab.get_automaton()
            aut_op = AutomatonOperation(automaton)
            access_aut = aut_op.accessibility()
            access_aut_name = 'accessible_' + selected_tab.get_file_name()
            tab = Tab(access_aut_name, access_aut, self.tabbed_frame)
            self.add_tab(tab)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
