#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from state import *
from graphviz import Digraph
import os
import os.path
from file_manager import *
from copy import deepcopy

class Automaton(object):
    """docstring for """
    def __init__(self, states, events, initial_state, marked_states, transitions):
        # super(, self).__init__()
        self.initial_state = initial_state
        self.states = {}
        self.events = str.split(events, ',')

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


    def to_file_format(self):
        states = list(self.states.keys())
        states.sort()
        states = ','.join(states)

        events = deepcopy(self.events)
        events.sort()
        events = ','.join(events)

        initial_state = self.initial_state

        marked_states = deepcopy(self.marked_states)
        marked_states.sort()
        marked_states = ','.join(marked_states)

        final_content = states + '\n' + events + '\n'
        final_content += initial_state + '\n' + marked_states

        for state_label, state in self.states.items():
            for event, dest_states_list in state.edges.items():
                for edge in dest_states_list:
                    final_content += '\n'
                    final_content += state_label + '-' + event + '-' + edge

        return final_content


    def draw(self, name, output_dir):
        # Cria grafo direcionado e define o estilo padrao dos nos
        dot = Digraph(name = name)
        dot.graph_attr['rankdir'] = 'LR'
        dot.graph_attr['pad'] = '0.5,0.5'
        dot.node_attr['shape'] = 'circle'
        dot.node_attr['style'] = 'filled'
        dot.node_attr['fillcolor'] = 'aquamarine4'
        dot.format = 'png'

        # Obtem os rotulos dos estados e os coloca em ordem alfabetica
        states = list(self.states.keys())
        states.sort()

        # Adicionana cada estado como um no do grafo
        for state in states:
            # Estilo do estado inicial
            if state == self.initial_state:
                # Estilo diferenciado caso o estado inicial seja tambem final
                if state in self.marked_states:
                    dot.node(state, shape = 'doublecircle', fillcolor = 'cornflowerblue', color = 'cornflowerblue')
                else:
                    dot.node(state, fillcolor = 'cornflowerblue')
            elif state in self.marked_states:
                # Estili diferenciado para os estados finais
                dot.node(state, shape = 'doublecircle', fillcolor = 'brown1', color = 'brown1')
            else:
                # Adiciona estados com o estilo padrao
                dot.node(state)

        # Adiciona no que aponta para o estado inicial
        dot.node('', shape = 'point', fillcolor = '#000000')
        dot.edge('', self.initial_state)

        # Adciona os eventos
        for state_label, state in self.states.items():
            for event, edges in state.edges.items():
                for edge in edges:
                    dot.edge(state_label, edge, label = event)

        # Verifica se o diretoria output existe, caso nao exista ele e criado
        if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        # Renderiza a imagem do automato
        dot.render(output_dir + os.sep + name)

        # Remove os arquivos desnecessarios apos renderizacao
        os.remove(output_dir + os.sep + name)

        # os.system('shotwell ' + self.OUTPUT_DIR + os.sep + name + '.png')
