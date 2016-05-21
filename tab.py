#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from file_manager import *
from automaton import *
import os.path
from PIL import ImageTk, Image

class Tab(tk.Frame):
    """docstring for Tab"""
    def __init__(self, file_path, master = None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.file_path = file_path
        self.open_file()

        self.create_widgets()

        self.pack()

    def open_file(self):
        fm = FileManager()
        file_content = fm.read_input(self.file_path)

        states = file_content[0]
        events = file_content[1]
        initial_state = file_content[2]
        marked_states = file_content[3]
        transitions = file_content[4:]

        self.file_name = os.path.basename(self.file_path)

        self.automaton = Automaton(states, events, initial_state, marked_states, transitions)
        self.automaton.draw(self.file_name)


    def create_widgets(self):
        self.image = ImageTk.PhotoImage(Image.open(self.file_name + ".gv.png").convert("RGB"))
        label_image = tk.Label(self, image = self.image)
        label_image.pack()


    def get_file_name(self):
        return self.file_name
