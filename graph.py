#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from node import *

class Graph(object):
    """docstring for """
    def __init__(self, states, initial_state, marked_states, transitions):
        # super(, self).__init__()
        self.states = {}

        # Dividindo string em lista de estados
        states = str.split(states, ',')
        marked_states = str.split(marked_states, ',')

        # Inicializa grafo apenas com os labels de cada estado sem suas transições
        for i,label in enumerate(states):
            self.states[label] = Node()

        # Marca nó inicial
        self.states[initial_state].start = True

        # Marca os nós finais
        for i,label in enumerate(marked_states):
            self.states[label].end = True

        # Dividindo lista de transições e adicionado cada transição ao seu nó
        # correspondente
        self.split_transitions(transitions)

    def split_transitions(self, transitions):
        """Separa a string em várias transições."""
        for i,trans in enumerate(transitions):
            list_trans = str.split(trans, '-')
            self.states[list_trans[0]].add_edge(list_trans[1], list_trans[2])


    def __str__(self):
        """Retorna uma representação em string do grafo"""
        no_str = "--------------------------------------------------\n"

        for i,key in enumerate(self.states):
            no_str += "Label = "
            no_str += str(key)
            no_str += "\nArestas = ["
            # String que representa uma transição
            no_str += str(self.states[key])
            no_str += "]\n\n"

        no_str += "--------------------------------------------------\n"

        return no_str
