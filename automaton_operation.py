#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from state import *
from automaton import *

class AutomatonOperation(object):
    """docstring for AutomatonOperation"""
    def __init__(self, automaton):
        # super(AutomatonOperation, self).__init__()

        # Cópia do autômato original
        self.automaton = copy.deepcopy(automaton)

    def accessibility(self):
        # Lista com os labels dos estados acessíveis
        accessibles = []

        # Cópia do autômato original
        automaton = copy.deepcopy(self.automaton)

        # Estado inicial do autômato
        initial_state = automaton.states[automaton.initial_state]

        # Estado inicial sempre será um autômato acessível
        accessibles.append(automaton.initial_state)

        # Pilha para salvar os estados que foram alcançados
        stack = []

        # Lista de todos os estados que o estado inicial alcança vai para a pilha
        for i,key in enumerate(initial_state.edges):
            stack += initial_state.edges[key]

        while stack:
            # Primeiro elemento da pilha
            first = stack.pop()

            # Testa se o elemento já foi colocado na lista
            if not first in accessibles:
                accessibles.append(first)

                current_state = automaton.states[first]

                # Lista de todos os estados que o estado atual alcança vai para a pilha
                for i,key in enumerate(current_state.edges):
                    stack += current_state.edges[key]

        return self.create_automaton(accessibles)
        

    def create_automaton(self, labels_list):
        '''
        Cria um autômato similar ao autômato original mas apenas com os estados
        dos labels da lista passada por parâmetro.
        '''

        # Lista com todos os labels do automato original
        automaton_labels = list(self.automaton.states.keys())

        # Lista com todos os estados que não pertencerão ao automato a ser criado
        states_to_remove = []

        # Cria lista com os estados do autômato original que não estão na lista
        # dos labels passada por parâmetro
        for i,value in enumerate(automaton_labels):
            if not value in labels_list:
                states_to_remove.append(value)

        # Copia do autômato original
        automaton = copy.deepcopy(self.automaton)

        # Remove os estados se a lista não for vazia
        if states_to_remove:
            for i,value in enumerate(states_to_remove):
                del automaton.states[value]

        return automaton




















    def __str__(self):
        """Retorna uma representação em string do automato"""
        no_str = str(self.automaton)

        return no_str
