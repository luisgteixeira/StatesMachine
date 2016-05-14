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

        for state in new_automaton.states:
            # Novas transições apenas com os estados co-acessíveis
            new_transition = {}
            # Transições para estado não co-acessível são retiradas
            for transition in new_automaton.states[state].edges:
                # Lista para salvar a lista de labels da transição
                labels = []

                # Estado que pode ser alcançado para cada evento
                for event in new_automaton.states[state].edges[transition]:
                    # Se a transição for de um estado acessível, salva-se na
                    # nova lista de transições
                    if event in co_accessible:
                        labels.append(event)

                # Salva lista apenas com os estados có-acessíveis
                if labels:
                    new_transition[transition] = labels

            # Salva nova lista de transições, sem os estados que não são
            # co-acessíveis
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
                    state.edges[event] = ['qTOTAL']

        # Adiciona novo estado ao autômato, se o mesmo tiver sido criado
        # anteriormente
        if new_state:
            automaton.states['qTOTAL'] = new_state


        return automaton


    def minimization(self, automaton=[]):
        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)

        # automaton = self.convert(automaton)
        automaton = self.accessibility(automaton)
        automaton = self.total(automaton)

        # Lista com labels de todos os estados
        states = list(automaton.states.keys())

        # Lista com todos os possíveis pares
        all_pairs = []
        # Lista com os pares que serão marcados
        marked_pairs = []

        # Marca todo par de estado nas condições -> (final, não final)
        for i in range(len(states)):
            j = i + 1
            while j < len(states):
                if states[i] in automaton.marked_states:
                    if not states[j] in automaton.marked_states:
                        marked_pairs.append([states[i], states[j]])
                elif states[j] in automaton.marked_states:
                    if not states[i] in automaton.marked_states:
                        marked_pairs.append([states[i], states[j]])

                all_pairs.append([states[i], states[j]])
                j += 1

        # Dicionário com os estados que talvez serão marcados
        dict_ij = {}


        for i in range(len(states)):
            j = i + 1

            while j < len(states):
                # Para todo par não marcado anteriormente
                if not [states[i], states[j]] in marked_pairs:
                    # Para todos os eventos do alfabeto
                    for event in automaton.events:
                        # Estados alcançados pelo par de estados
                        state_i = automaton.states[states[i]].edges[event]
                        state_j = automaton.states[states[j]].edges[event]

                        # Retira estados da lista
                        state_i = state_i[0]
                        state_j = state_j[0]

                        # Auxilia no posicionamento certo do par da transição
                        # pois o dicionário em Python não garante a posição
                        # correta
                        if states.index(state_i) < states.index(state_j):
                            pair_xe_ye = [state_i, state_j]
                            pair_xe_ye1 = state_i + ', ' + state_j
                            pair_x_y = [states[i], states[j]]
                            pair_x_y1 = states[i] + ', ' + states[j]
                        else:
                            pair_xe_ye = [state_j, state_i]
                            pair_xe_ye1 = state_j + ', ' + state_i
                            pair_x_y = [states[j], states[i]]
                            pair_x_y1 = states[j] + ', ' + states[i]


                        # Se o par de estados alcançados já for marcado
                        if pair_xe_ye in marked_pairs:
                            # Adiciona a lista de pares a lista de marcados
                            marked_pairs.append(pair_x_y)
                            if pair_x_y1 in dict_ij.keys():
                                for state in dict_ij[pair_x_y1]:
                                    marked_pairs.append(state)

                            break
                        else:
                            # Acrescentar os pares (states[i], states[j]) à
                            # lista de (state_i, state_j)
                            if state_i != state_j:
                            # Marcar todos os pares da lista
                                if not pair_xe_ye1 in dict_ij.keys():
                                    dict_ij[pair_xe_ye1] = [pair_x_y]
                                elif not pair_x_y in dict_ij[pair_xe_ye1]:
                                    pair_aux = dict_ij.get(pair_xe_ye1)
                                    pair_aux.append(pair_x_y)
                                    dict_ij[pair_xe_ye1] = pair_aux

                j += 1

        automaton = create_automaton_minimized(all_pairs, marked_pairs)

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
