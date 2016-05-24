#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from automaton import *
import os.path
import os
from PIL import ImageTk, Image

class Tab(tk.Frame):
    """Classe que comporta o conteudo de uma aba da interface."""

    def __init__(self, automaton, file_path, master = None):
        """Construtor da classe tab."""
        tk.Frame.__init__(self, master)
        self.parent = master
        self.file_path = file_path
        self.set_file_name()
        self.automaton = automaton
        self.create_widgets()
        self.pack()


    def create_widgets(self):
        """Carrega e exibe a imagem."""
        self.OUTPUT_DIR = 'output'
        self.automaton.draw(self.get_file_name(), self.OUTPUT_DIR)
        image_path = self.OUTPUT_DIR + os.sep + self.get_file_name() + ".png"
        self.image = ImageTk.PhotoImage(Image.open(image_path).convert("RGB"))
        label_image = tk.Label(self, image = self.image)
        label_image.pack(side = 'left') # melhor substituir por grid


    def set_file_path(self, file_path):
        """Configura o caminho absoluto do arquivo associado a aba."""
        self.file_path = file_path


    def set_file_name(self):
        """Configura o nome, sem extensao, do arquivo associado a aba."""
        if self.file_path.endswith('.fsm'):
            self.file_name = os.path.basename(self.file_path)[:-4]
        else:
            self.file_name = os.path.basename(self.file_path)


    def get_file_name(self):
        """Retorna o nome do arquivo associado a aba."""
        return self.file_name


    def get_file_path(self):
        """Retorna o caminho absoluto do arquivo associado a aba."""
        return self.file_path


    def get_automaton(self):
        """Retorna o automato contido na aba."""
        return self.automaton
