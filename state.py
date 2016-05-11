#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class State(object):
    """docstring for """
    def __init__(self, start=False, end=False):
        # super(, self).__init__()
        self.start = start  # Indica se é estado inicial
        self.end = end      # Indica se é estado final
        self.edges = {}  # Arestas a quem o nó se liga

    def __str__(self):
        """Retorna uma representação em string do no"""
        # no_str = "--------------------------------------------------\n"
        no_str = "Estado inicial? "
        no_str += str(self.start)
        no_str += ", Estado final? "
        no_str += str(self.end)
        no_str += ", Arestas = "
        no_str += str(self.edges)
        # no_str += "\nArestas = ["
        #
        # for i, edge in enumerate(self.edges):
        #     no_str += str(edge)
        #     # Não coloca vírgula na última transição
        #     if i < len(self.edges) - 1:
        #         no_str += ", "
        # no_str += "]"
        # no_str += "\n--------------------------------------------------\n"

        return no_str

    def add_edge(self, event, state):
        # Evento já existe
        if event in self.edges:
            self.edges[event].append(state)
        else:
            self.edges[event] = [state]
