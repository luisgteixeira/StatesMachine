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

        return self.create_automaton(accessible, automaton)


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
        new_automaton = self.create_automaton(co_accessible, automaton)

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


    def trim(self, automaton=[]):
        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)

        automaton = self.accessibility(automaton)
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
        # Lista com labels ordenada
        states.sort()

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
                        pair_xe_ye = [state_i, state_j]
                        pair_xe_ye.sort()
                        pair_xe_ye1 = ', '.join(pair_xe_ye)

                        pair_x_y = [states[i], states[j]]
                        pair_x_y.sort()
                        pair_x_y1 = ', '.join(pair_x_y)


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

        # Cria automato similar ao original, mas retirando os pares equivalentes
        automaton = self.create_automaton_minimized(all_pairs, marked_pairs, automaton)

        # Exclusão dos estados inúteis
        automaton = self.co_accessibility(automaton)

        return automaton


    def product_composition(self, automaton_1, automaton_2=[]):
        # Cópia do autômato original
        if not automaton_2:
            automaton_2 = copy.deepcopy(self.automaton)
        else:
            automaton_2 = copy.deepcopy(automaton_2)

        # Novos estados a serem criados
        new_states = {}
        # Estados que serão os novos estados finais
        marked_states = []
        # Lista com as transições do autômato
        transitions = []

        for key_1 in automaton_1.states:
            for key_2 in automaton_2.states:
                # Label do novo estado a ser criado
                new_st = key_1 + ';' + key_2

                # Estado será inicial quando os dois estados que o origina forem
                # estados iniciais
                if key_1 == automaton_1.initial_state:
                    if key_2 == automaton_2.initial_state:
                        initial_state = new_st

                # Estado será final quando os dois estados que o origina forem
                # estados finais
                if key_1 in automaton_1.marked_states:
                    if key_2 in automaton_2.marked_states:
                        marked_states.append(new_st)

                # Criando lista com união dos eventos do automaton_1 e do
                # automaton_2
                all_events = automaton_1.events
                for event in automaton_2.events:
                    # Se é o evento não existia no alfabeto do automaton_1,
                    # então adiciona na lista
                    if not event in all_events:
                        all_events.append(event)

                for event in all_events:
                    # Retorna transição para determinado evento, se o evento
                    # for do alfabeto do autômato
                    if event in automaton_1.states[key_1].edges.keys():
                        transition_1 = automaton_1.states[key_1].edges[event][0]
                    else:
                        continue
                    if event in automaton_2.states[key_2].edges.keys():
                        transition_2 = automaton_2.states[key_2].edges[event][0]
                    else:
                        continue

                    # Se não houver transição para determinado evento, será
                    # utilizado o próprio estado para criar a nova transição
                    new_trans = transition_1
                    new_trans += ';' + transition_2

                    # É adicionado ao dicionário o novo estado com a sua nova
                    # transição
                    new_states[new_st] = [new_trans]

                    transitions.append(new_st + '-' + event + '-' + new_trans)

        # Criando uma string com os eventos separados por vírgula
        all_events = ','.join(all_events)
        # Criando uma string com os novos estados separados por vírgula
        new_states = ','.join(new_states.keys())
        # Criando uma string com os estados finais separados por vírgula
        marked_states = ','.join(marked_states)

        # Criando o autômato inicial
        automaton = Automaton(new_states, all_events, initial_state, marked_states, transitions)
        automaton = self.accessibility(automaton)

        return automaton


    def parallel_composition(self, automaton_1, automaton_2=[]):
        # Cópia do autômato original
        if not automaton_2:
            automaton_2 = copy.deepcopy(self.automaton)
        else:
            automaton_2 = copy.deepcopy(automaton_2)

        # Novos estados a serem criados
        new_states = {}
        # Estados que serão os novos estados finais
        marked_states = []
        # Lista com as transições do autômato
        transitions = []

        for key_1 in automaton_1.states:
            for key_2 in automaton_2.states:
                # Label do novo estado a ser criado
                new_st = key_1 + ';' + key_2

                # Estado será inicial quando os dois estados que o origina forem
                # estados iniciais
                if key_1 == automaton_1.initial_state:
                    if key_2 == automaton_2.initial_state:
                        initial_state = new_st

                # Estado será final quando os dois estados que o origina forem
                # estados finais
                if key_1 in automaton_1.marked_states:
                    if key_2 in automaton_2.marked_states:
                        marked_states.append(new_st)

                # Criando lista com união dos eventos do automaton_1 e do
                # automaton_2
                all_events = automaton_1.events
                for event in automaton_2.events:
                    # Se é o evento não existia no alfabeto do automaton_1,
                    # então adiciona na lista
                    if not event in all_events:
                        all_events.append(event)

                for event in all_events:
                    transition_1 = []
                    transition_2 = []
                    # Retorna transição para determinado evento, se o evento
                    # for do alfabeto do autômato
                    if event in automaton_1.states[key_1].edges.keys():
                        transition_1 = automaton_1.states[key_1].edges[event][0]
                    if event in automaton_2.states[key_2].edges.keys():
                        transition_2 = automaton_2.states[key_2].edges[event][0]

                    # Se não houver transição para determinado evento, será
                    # utilizado o próprio estado para criar a nova transição
                    if transition_1:
                        new_trans = transition_1
                    elif not event in automaton_1.events:
                        new_trans = key_1
                    else:
                        continue;

                    if transition_2:
                        new_trans += ';' + transition_2
                    elif (transition_1) and (not event in automaton_2.events):
                        new_trans += ';' + key_2
                    else:
                        continue

                    # É adicionado ao dicionário o novo estado com a sua nova
                    # transição
                    new_states[new_st] = [new_trans]

                    transitions.append(new_st + '-' + event + '-' + new_trans)

        # Criando uma string com os eventos separados por vírgula
        all_events = ','.join(all_events)
        # Criando uma string com os novos estados separados por vírgula
        new_states = ','.join(new_states.keys())
        # Criando uma string com os estados finais separados por vírgula
        marked_states = ','.join(marked_states)

        # Criando o autômato inicial
        automaton = Automaton(new_states, all_events, initial_state, marked_states, transitions)
        automaton = self.accessibility(automaton)

        return automaton


    def create_automaton(self, labels_list, automaton=[]):
        '''
        Cria um autômato similar ao autômato original mas apenas com os estados
        dos labels da lista passada por parâmetro.
        '''

        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)

        # Lista com todos os labels do automato original
        automaton_labels = list(automaton.states.keys())

        # Lista com todos os estados que não pertencerão ao automato a ser criado
        states_to_remove = []

        # Cria lista com os estados do autômato original que não estão na lista
        # dos labels passada por parâmetro
        for i,value in enumerate(automaton_labels):
            if not value in labels_list:
                states_to_remove.append(value)

        # Remove os estados se a lista não for vazia
        if states_to_remove:
            for i,value in enumerate(states_to_remove):
                del automaton.states[value]

        return automaton


    def create_automaton_minimized(self, all_pairs, marked_pairs, automaton):
        '''
        Cria um autômato minimizado a partir das marcações feitas
        anteriormente.
        '''
        # Lista com todos os pares que não foram marcados
        no_marked = all_pairs

        # Remove pares marcados, resultando em uma lista com todos os pares
        # que não foram marcados
        for pair in marked_pairs:
            if pair in no_marked:
                no_marked.remove(pair)

        # Copia do autômato original
        automaton = copy.deepcopy(automaton)

        while no_marked:
            # Novo estado a ser criado
            new_state = no_marked.pop(0)
            # Indices a serem removidos da lista de não marcados
            indexs = []

            # Varre a lista de pares não marcados
            for i,n_st in enumerate(no_marked):
                # Caso um dos estados já esteja na lista do novo estado, o outro
                # estado do par é considerado equivalente
                if n_st[0] in new_state:
                    # Índice é guardado para excluir o par posteriormente
                    indexs.append(i)
                    if not n_st[1] in new_state:
                        new_state.append(n_st[1])
                elif n_st[1] in new_state:
                    indexs.append(i)
                    new_state.append(n_st[0])

            # Índices são ordenados de forma decrescente para posterior exclusão
            indexs.sort()
            indexs.reverse()

            # Pares equivalentes são excluídos da lista
            for i in indexs:
                no_marked.pop(i)

            # Cria label a partir dos nós equivalentes
            new_label = ';'.join(new_state)

            # Percorre todos os estados do automato com a finalidade de mudar
            # as transições para o novo estado (new_label)
            for state in automaton.states.values():
                # Percorre os estados alcançáveis pelo estado atual
                for transition in state.edges.values():
                    # Se a transição for para um dos pares equivalentes, a
                    # transição mudará para o novo par
                    if transition[0] in new_state:
                        transition[0] = new_label

            # Cria novo estado similar a um dos estados do par se ainda não
            # existir
            if not new_label in automaton.states.keys():
                automaton.states[new_label] = automaton.states[new_state[0]]

            # Remove os estados equivalentes
            for n_st in new_state:
                if n_st in automaton.states:
                    del automaton.states[n_st]

                # Coloca novo estado como inicial, caso algum dos estados seja
                if n_st == automaton.initial_state:
                    automaton.initial_state = new_label

                # Coloca novo estado na lista dos estados finais e retira da
                # lista de finais os estados equivalentes
                if n_st in automaton.marked_states:
                    automaton.marked_states.remove(n_st)
                    if not new_label in automaton.marked_states:
                        automaton.marked_states.append(new_label)

        return automaton


    def __str__(self):
        """Retorna uma representação em string do automato"""
        no_str = str(self.automaton)

        return no_str









    def afn2afd(self, automaton=[]):
        # Cópia do autômato original
        if not automaton:
            automaton = copy.deepcopy(self.automaton)
        else:
            automaton = copy.deepcopy(automaton)

        print(automaton)

        transitions_table = {}

        # Armazena os estados originais do automato
        original_states = list(automaton.states.keys())

        new_states = []      # Amazena os novos estados do automato

        events = []

        # state_label = rotulo do estado, state = objeto estado
        for state_label, state in automaton.states.items():
            transitions_table[state_label] = {}
            # event = rotulo do evento, states_dest = lista de destinos pra o evento
            for event, states_dest in state.edges.items():
                if event not in events:
                    events.append(event)

                transitions_table[state_label][event] = states_dest

                new_state = ';'.join(states_dest)
                if new_state not in transitions_table.keys():
                    transitions_table[new_state] = {}
                    new_states.append(new_state)


        for new_state in new_states:
            splited_states = new_state.split(';')

            for event in events:
                destinations = []

                for sp_state in splited_states:

                    if event in transitions_table[sp_state].keys():
                        transitions = transitions_table[sp_state][event]
                        if transitions:
                            destinations += transitions
                            destinations = list(set(destinations))
                            destinations.sort()

                    if len(destinations) > 0:
                        transitions_table[new_state][event] = destinations


        for state, transitions in transitions_table.items():
            for event, dest_states in transitions.items():
                transitions_table[state][event] = ';'.join(dest_states)


        final_temp_states = original_states + new_states
        final_states = []


        # Obtem os estados que devem parmanecer ao final
        for final_temp_state in final_temp_states:
            temp_states = []
            for transitions in transitions_table.values():
                for dest_state in transitions.values():
                    temp_states.append(dest_state)

            temp_states = list(set(temp_states))

            if final_temp_state in temp_states:
                final_states.append(final_temp_state)


        # Obtem os estados marcados
        marked_states = []
        for final_state in final_states:
            for mk in automaton.marked_states:
                if final_state.__contains__(mk):
                    marked_states.append(final_state)


        # Remove os estados inalcansaveis
        for final_temp_state in final_temp_states:
            if final_temp_state not in final_states:
                transitions_table.pop(final_temp_state)


        transitions = []
        for state_label, state_transitions in transitions_table.items():
            print(state_label)
            for event, dest_states in state_transitions.items():
                transitions.append(state_label + '-' + event + '-' + dest_states)

        print(transitions)

        for key, value in transitions_table.items():
            print(key, ':', value)




        result_automaton = Automaton(','.join(final_states),
                                     ','.join(automaton.events),
                                     automaton.initial_state,
                                     ','.join(marked_states),
                                     transitions)
        return result_automaton




























# ggfg
