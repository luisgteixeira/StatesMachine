#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from state import *
from graphviz import Digraph

class Automaton(object):
    """docstring for """
    def __init__(self, states, events, initial_state, marked_states, transitions):
        # super(, self).__init__()
        self.initial_state = initial_state
        self.states = {}
        self.events = events

        # Dividindo string em lista de estados
        states = str.split(states, ',')
        self.marked_states = str.split(marked_states, ',')

        # Inicializa grafo apenas com os labels de cada estado sem suas transições
        for i,label in enumerate(states):
            self.states[label] = State()

        # Marca nó inicial
        self.states[self.initial_state].start = True

        # Marca os nós finais
        for i,label in enumerate(self.marked_states):
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
        """Retorna uma representação em string do automato"""
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

    def draw(self, name):
        dot = Digraph(name = name, node_attr = {'shape': 'circle', 'style' : 'filled', 'fillcolor':'aquamarine4'})
        dot.graph_attr['rankdir'] = 'LR'
        dot.graph_attr['pad'] = '0.5,0.5'

        states = list(self.states.keys())
        states.sort()

        for state in states:
            if state in self.marked_states:
                dot.node(state, shape = 'doublecircle', fillcolor = 'brown1', color = 'brown1')
            elif state == self.initial_state:
                dot.node(state, fillcolor = 'cornflowerblue')
            else:
                dot.node(state)

        dot.node('', shape = 'point', fillcolor = '#000000')
        dot.edge('', self.initial_state)

        for state_label, state in self.states.items():
            for event, edges in state.edges.items():
                for edge in edges:
                    dot.edge(state_label, edge, label = event)


        dot.format = 'png'
        dot.render()
