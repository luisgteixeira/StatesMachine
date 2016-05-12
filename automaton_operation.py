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

    def accessibility(self, automaton=[]):
        # Lista com os labels dos estados acessíveis
        accessible = []

        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)

        # Estado inicial do autômato
        initial_state = automaton.states[automaton.initial_state]

        # Estado inicial sempre será um autômato acessível
        accessible.append(automaton.initial_state)

        # Pilha para salvar os estados que foram alcançados
        stack = []

        # Lista de todos os estados que o estado inicial alcança vai para a
        # pilha
        for i,key in enumerate(initial_state.edges):
            stack += initial_state.edges[key]

        while stack:
            # Primeiro elemento da pilha
            first = stack.pop()

            # Testa se o elemento já foi colocado na lista
            if not first in accessible:
                accessible.append(first)

                current_state = automaton.states[first]

                # Lista de todos os estados que o estado atual alcança vai para
                # a pilha
                for i,key in enumerate(current_state.edges):
                    stack += current_state.edges[key]

        return self.create_automaton(accessible)


    def co_accessibility(self, automaton=[]):
        # Lista com os labels dos estados que alcançam pelo menos um estado
        # final
        co_accessible = []

        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)


        # Todos os estados finais são co-acessíveis
        co_accessible += automaton.marked_states

        # Lista com todos os labels do automato original
        automaton_labels = list(automaton.states.keys())

        # Tamanho da lista de estados co-acessíveis
        current_size = len(co_accessible)
        previous_size = 0

        # Enquanto a quantidade de estados co-acessíveis aumentar
        while current_size > previous_size:
            for i,current_state in enumerate(automaton_labels):
                # Testa se o estado já é co-acessível
                if not current_state in co_accessible:
                    # Lista com os estados em que o estado atual se liga
                    edges = list(automaton.states[current_state].edges.values())

                    #
                    edges_list = []
                    for j in range(len(edges)):
                        edges_list += edges[j]

                    j = 0
                    while j < len(edges_list):
                        if edges_list[j] in co_accessible:
                            co_accessible.append(current_state)
                            break

                        j += 1

            # Atualização do tamanho da lista de estados co-acessíveis
            previous_size = current_size
            current_size = len(co_accessible)

        # Novo autômato apenas com os estados co-acessíveis
        new_automaton = self.create_automaton(co_accessible)

        for k,state in enumerate(new_automaton.states):
            # Novas transições apenas com os estados co-acessíveis
            new_transition = {}
            # Transições para estado não co-acessível são retiradas
            for i,transition in enumerate(new_automaton.states[state].edges):
                label = new_automaton.states[state].edges[transition].pop()
                # Se a transição for de um estado acessível, salva-se na nova
                # lista de transições
                if label in co_accessible:
                    new_transition[transition] = label

            new_automaton.states[state].edges = new_transition

        return new_automaton


    def trim(self):
        automaton = self.accessibility()
        return self.co_accessibility(automaton)


    def total(self, automaton=[]):
        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)

        # Novo estado a ser criado, se necessário
        new_state = []

        # Laço de todos os estados
        for state in automaton.states.values():
            # Lista de eventos permitidos pelo estado atual
            events_list = []

            # print(transition.edges.values())
            # Laço das transições de cada estado
            for transitions in state.edges.keys():
                if not transitions in events_list:
                    events_list += transitions

            # Cópia do alfabeto do autômato
            automaton_events = copy.deepcopy(automaton.events)
            # Deixa em 'automaton_events' apenas os eventos que não são
            # permitidos pelo estado
            for event in events_list:
                if event in automaton_events:
                    automaton_events.remove(event)

            # Novo estado só é criado se no estado atual falta pelo menos uma
            # transição utilizando algum evento do alfabeto
            if automaton_events:
                # Testa se o novo estado já foi ou não criado
                if not new_state:
                    new_state = State()
                    # Cria um ciclo no novo estado para todos os eventos do
                    # alfabeto
                    for event in automaton.events:
                        new_state.edges[event] = ['qTOTAL']

                # Laço dos eventos ausentes no estado atual
                for event in automaton_events:
                    state.edges[event] = 'qTOTAL'

        # Adiciona novo estado ao autômato, se o mesmo tiver sido criado
        # anteriormente
        if new_state:
            automaton.states['qTOTAL'] = new_state


        return automaton


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
