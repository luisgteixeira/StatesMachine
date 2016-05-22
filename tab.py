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

    def __init__(self, file_name, automaton, master = None):
        """Construtor da classe tab."""
        tk.Frame.__init__(self, master)
        self.parent = master
        self.file_name = file_name
        self.automaton = automaton

        self.create_widgets()

        self.pack()


    def create_widgets(self):
        """Carrega e exibe a imagem."""
        self.OUTPUT_DIR = 'output'
        self.automaton.draw(self.file_name, self.OUTPUT_DIR)
        image_path = self.OUTPUT_DIR + os.sep + self.file_name + ".png"
        self.image = ImageTk.PhotoImage(Image.open(image_path).convert("RGB"))
        label_image = tk.Label(self, image = self.image)
        label_image.pack()


    def get_file_name(self):
        """"""
        return self.file_name


    def get_automaton(self):
        """"""
        return self.automaton
