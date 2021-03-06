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
        self.selection_options = [] # Lista de checkbuttons para selecaos
        self.selection_values = [] # Indica os valores de cada checkbutton

        self.create_widgets()


    def create_widgets(self):
        """Cria todos os widgets da interface."""
        # Cria barra de menus
        self.create_menubar()

        # Cria frame de botoes
        self.create_buttons_frame()

        # Cria frame para exibicao dos automatos
        self.create_tabbed_frame()

        # Cria frame de selecao de automatos para operacoes
        self.create_selection_frame()


    def create_tabbed_frame(self):
        """Cria o frame principal, onde sao exibidos os automatos."""
        self.tabbed_frame = ttk.Notebook(self, padding = '5 20 5 5')
        self.create_context_menu()
        self.tabbed_frame.bind('<Button-3>', self.show_context_menu)


    def create_selection_frame(self):
        """Cria o frame para selecao de automatos para operacoes nao unarias."""
        self.selection_frame = tk.Frame(self)
        self.selection_frame['pady'] = '15'
        self.selection_frame['padx'] = '5'

        self.selection_label = tk.Label(self.selection_frame, text = 'Selecione os autômatos:')
        self.selection_label['pady'] = '5'
        self.selection_label.pack()


    def add_selection_option(self, name):
        """"""
        var = tk.IntVar()
        self.selection_values.append(var)
        selection_option = tk.Checkbutton(self.selection_frame, text = name, variable=var)
        self.selection_options.append(selection_option)
        selection_option.pack()


    def create_context_menu(self):
        """"""
        self.context_menu = tk.Menu(self.tabbed_frame, tearoff=0)
        self.context_menu.add_command(label = 'Fechar', command = self.close_tab)


    def add_tab(self, tab):
        """Adiciona uma aba ao frame principal."""
        if self.tabbed_frame.index('end') == 0:
            self.tabbed_frame.grid(column = 2, row = 1, sticky = tk.N)
            self.selection_frame.grid(column = 3, row = 1, sticky = tk.NW)

        self.tabbed_frame.add(tab, text = tab.get_file_name())
        self.opened_tabs.append(tab)
        tab_id = self.tabbed_frame.index('end') - 1
        self.tabbed_frame.select(tab_id)

        self.add_selection_option(tab.get_file_name())


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
        self.afn2afd_button = tk.Button(self.buttons_frame,
            text = 'AFN -> AFD', command = self.op_convertion)
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
        self.parallel_composition_button = tk.Button(self.buttons_frame,
            text = 'Composição paralela', command = self.op_parallel_composition)
        self.stylize_button(self.parallel_composition_button)
        self.parallel_composition_button.pack()

        # Botao para o calculo do produto
        self.product_button = tk.Button(self.buttons_frame,
            text = 'Produto', command = self.op_product)
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
        """Exibe o menu de contexto."""
        self.context_menu.post(event.x_root, event.y_root)


    def exit(self):
        """Encerra a execucao do programa."""
        answer = messagebox.askyesno(message = 'Deseja encerrar o programa?', title = 'Sair')
        if answer:
            self.parent.destroy()


    def execute_operation(self, operation):
        """Executa operacoes com apenas um automato."""
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
            elif operation == 'convertion':
                result_automaton = aut_op.convertion()
            else:
                print('Operacao invalida.')

            tab = Tab(result_automaton, automaton_name, self.tabbed_frame)
            self.add_tab(tab)


    def get_selected_checkbuttons(self):
        """Retorna os indices das abas selecionadas no checkbox."""
        selected_automatons_indexes = []
        for index, var in enumerate(self.selection_values):
            if var.get() == 1:
                selected_automatons_indexes.append(index)

        return selected_automatons_indexes


    def execute_composition(self, composition):
        """"""
        """Executa operacoes com apenas um automato."""
        selected_tabs_indexes = self.get_selected_checkbuttons()
        if len(selected_tabs_indexes) < 2:
            messagebox.showerror('Erro', 'Você deve selecionar ao menos dois automatos.')
        else:
            selected_automatons = []
            for selected_tab_index in selected_tabs_indexes:
                tab = self.opened_tabs[selected_tab_index]
                automaton = tab.get_automaton()
                selected_automatons.append(automaton)

            aut_op = AutomatonOperation(selected_automatons[0])
            automaton_name = composition #+ '_' + selected_tab.get_file_name()
            result_automaton = None

            if composition == 'product':
                result_automaton = selected_automatons[0]
                for i in range(1, len(selected_automatons)):
                    result_automaton = aut_op.product_composition(result_automaton, selected_automatons[i])
            elif composition == 'parallel_composition':
                result_automaton = selected_automatons[0]
                for i in range(1, len(selected_automatons)):
                    result_automaton = aut_op.parallel_composition(result_automaton, selected_automatons[i])
            else:
                print('Operacao invalida.')

            tab = Tab(result_automaton, automaton_name, self.tabbed_frame)
            self.add_tab(tab)


    def close_tab(self):
        """Fecha a aba selecionada."""
        selected_tab_index = self.tabbed_frame.index('current')
        self.tabbed_frame.forget(selected_tab_index)
        self.opened_tabs.pop(selected_tab_index)
        self.selection_options[selected_tab_index].destroy()
        self.selection_options.pop(selected_tab_index)
        self.selection_values.pop(selected_tab_index)
        if self.tabbed_frame.index('end') == 0:
            self.tabbed_frame.destroy()
            self.create_tabbed_frame()
            self.selection_frame.destroy()
            self.create_selection_frame()


    def save_file(self):
        """Obtem o caminho de destino e salva o automato."""
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
                final_content = automaton.to_file_format()

                fm = FileManager()
                fm.write_automaton(final_content, file_path)


    def op_accessibility(self):
        """Executa a operacao de Acessibilidade."""
        self.execute_operation('accessibility')


    def op_co_accessibility(self):
        """Executa a operacao de Co-acessibilidade."""
        self.execute_operation('co_accessibility')


    def op_trim(self):
        """Executa a operacao de Trim."""
        self.execute_operation('trim')


    def op_minimization(self):
        """Executa a operacao de minimizacao."""
        self.execute_operation('minimization')


    def op_convertion(self):
        """Converte um automato nao-deterministico em deterministico."""
        self.execute_operation('convertion')


    def op_product(self):
        """Faz a composicao de automatos atraves da operacao de produto."""
        self.execute_composition('product')


    def op_parallel_composition(self):
        """
        Faz a composicao de automatos atraves da operacao de composicao
        paralela.
        """
        self.execute_composition('parallel_composition')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
