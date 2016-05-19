#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
    """docstring for Application"""
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        master.title("FSM")
        self.pack(side = "left")
        self.create_widgets()


    def create_widgets(self):
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack()
        self.create_buttons()


    def create_buttons(self):
        # Botao para conversao AFN -> AFD
        self.afn2afd_button = tk.Button(self, text = "AFN -> AFD")
        self.stylize_button(self.afn2afd_button)
        self.afn2afd_button.pack()

        # Botao para calculo da Acessibilidade
        self.accessibility_button = tk.Button(self, text = "Acessibilidade")
        self.stylize_button(self.accessibility_button)
        self.accessibility_button.pack()

        # Botao para o calculo da Co-acessibilidade
        self.co_accessibility_button = tk.Button(self, text = "Co-acessibilidade")
        self.stylize_button(self.co_accessibility_button)
        self.co_accessibility_button.pack()

        # Botao para o calculo do Trim
        self.trim_button = tk.Button(self, text = "Trim")
        self.stylize_button(self.trim_button)
        self.trim_button.pack()


        self.parallel_composition_button = tk.Button(self, text = "Composição paralela")
        self.stylize_button(self.parallel_composition_button)
        self.parallel_composition_button.pack()

        self.product_button = tk.Button(self, text = "Produto")
        self.stylize_button(self.product_button)
        self.product_button.pack()

        self.minimization_button = tk.Button(self, text = "Minimização")
        self.stylize_button(self.minimization_button)
        self.minimization_button.pack()


    def stylize_button(self, button):
        BUTTON_WIDTH = "20"
        BUTTON_HEIGHT = "2"

        button["width"] = BUTTON_WIDTH
        button["height"] = BUTTON_HEIGHT



if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
