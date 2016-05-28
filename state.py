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
        """Retorna uma representação em string do estado"""
        state_str = "Estado inicial? "
        state_str += str(self.start)
        state_str += ", Estado final? "
        state_str += str(self.end)
        state_str += ", Arestas = "
        state_str += str(self.edges)

        return state_str

    def add_edge(self, event, state):
        """Adiciona trasicoes ao automato."""
        # Evento já existe
        if event in self.edges:
            self.edges[event].append(state)
        else:
            self.edges[event] = [state]

        self.edges[event].sort()
