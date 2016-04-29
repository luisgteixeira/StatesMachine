#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Node(object):
    """docstring for """
    def __init__(self, label, start, end, edges):
        # super(, self).__init__()
        self.label = label
        self.start = start  # Indica se é estado inicial
        self.end = end      # Indica se é estado final
        self.edges = edges  # Arestas a quem o nó se liga

    def __str__(self):
        """Retorna uma representação em string do no"""
        no_str = "--------------------------------------------------\n"
        no_str += "Label = "
        no_str += str(self.label)
        no_str += "\nEstado inicial? "
        no_str += str(self.start)
        no_str += "\nEstado final? "
        no_str += str(self.end)
        no_str += "\nArestas = ["

        for i, edge in enumerate(self.edges):
            no_str += str(edge)
            # Não coloca vírgula na última transição
            if i < len(self.edges) - 1:
                no_str += ", "
        no_str += "]"
        no_str += "\n--------------------------------------------------\n"

        return no_str
