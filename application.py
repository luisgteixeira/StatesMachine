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
        self.create_context_menu()
        self.tabbed_frame.bind('<Button-3>', self.show_context_menu)


    def create_context_menu(self):
        self.context_menu = tk.Menu(self.tabbed_frame, tearoff=0)
        self.context_menu.add_command(label = 'Fechar', command = self.close_tab)


    def add_tab(self, tab):
        """Adiciona uma aba ao frame principal."""
        if self.tabbed_frame.index('end') == 0:
            self.tabbed_frame.grid(column = 2, row = 1, sticky = tk.N)
        self.tabbed_frame.add(tab, text = tab.get_file_name())
        self.opened_tabs.append(tab)
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
        self.file_menu.add_command(label = 'Salvar automato', command = self.save_file)
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
        self.co_accessibility_button = tk.Button(self.buttons_frame,
            text = 'Co-acessibilidade', command = self.op_co_accessibility)
        self.stylize_button(self.co_accessibility_button)
        self.co_accessibility_button.pack()

        # Botao para o calculo do Trim
        self.trim_button = tk.Button(self.buttons_frame,
            text = 'Trim', command = self.op_trim)
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
        self.minimization_button = tk.Button(self.buttons_frame,
            text = 'Minimização', command = self.op_minimization)
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
            for index, tab in enumerate(self.opened_tabs):
                if file_path == tab.get_file_path():
                    self.tabbed_frame.select(index)
                    return

            automaton = self.open_file(file_path)

            tab = Tab(automaton, file_path, self.tabbed_frame)
            self.add_tab(tab)


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


    def show_context_menu(self, event):
        print('Exibir menu de contexto.')
        self.context_menu.post(event.x_root, event.y_root)


    def exit(self):
        """Encerra a execucao do programa."""
        answer = messagebox.askyesno(message = 'Deseja encerrar o programa?', title = 'Sair')
        if answer:
            self.parent.destroy()


    def execute_operation(self, operation):
        """"""
        if self.tabbed_frame.index('end') == 0:
            messagebox.showerror('Erro', 'Não há nenhum autômato aberto.')
        else:
            selected_tab_index = self.tabbed_frame.index('current')
            selected_tab = self.opened_tabs[selected_tab_index]
            automaton = selected_tab.get_automaton()
            aut_op = AutomatonOperation(automaton)
            automaton_name = operation + '_' + selected_tab.get_file_name()
            result_automaton = None

            if operation == 'accessibility':
                result_automaton = aut_op.accessibility()
            elif operation == 'trim':
                result_automaton = aut_op.trim()
            elif operation == 'co_accessibility':
                result_automaton = aut_op.co_accessibility()
            elif operation == 'minimization':
                result_automaton = aut_op.minimization()
            else:
                print('Operacao invalida.')

            tab = Tab(result_automaton, automaton_name, self.tabbed_frame)
            self.add_tab(tab)


    def close_tab(self):
        selected_tab_index = self.tabbed_frame.index('current')
        print('Fechar aba:', selected_tab_index)
        self.tabbed_frame.forget(selected_tab_index)
        if self.tabbed_frame.index('end') == 0:
            self.tabbed_frame.destroy()
            self.create_tabbed_frame()


    def save_file(self):
        """"""
        if self.tabbed_frame.index('end') == 0:
            messagebox.showerror('Erro', 'Não há nenhum autômato aberto.')
        else:

            file_path = filedialog.asksaveasfilename()
            if file_path != '':
                if not file_path.endswith('.fsm'):
                    file_path += '.fsm'
                selected_tab_index = self.tabbed_frame.index('current')
                selected_tab = self.opened_tabs[selected_tab_index]
                automaton = selected_tab.get_automaton()
                automaton.save(file_path)


    def op_accessibility(self):
        """"""
        self.execute_operation('accessibility')


    def op_co_accessibility(self):
        """"""
        self.execute_operation('co_accessibility')


    def op_trim(self):
        """"""
        self.execute_operation('trim')


    def op_minimization(self):
        """"""
        self.execute_operation('minimization')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
