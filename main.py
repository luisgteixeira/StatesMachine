#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from file_manager import *
from state import *
from automaton import *
from automaton_operation import *

def main():
    fm = FileManager()
    fm.reset_log()

	# Le os dados de entrada a partir de um arquivo texto
    file_content = fm.read_input('inputs/input6.fsm')
    # print(file_content)

    states = file_content[0]
    events = file_content[1]
    initial_state = file_content[2]
    marked_states = file_content[3]
    transitions = file_content[4:]

    # Criando o autômato inicial
    automaton = Automaton(states, events, initial_state, marked_states, transitions)

    # Le os dados de entrada a partir de um arquivo texto
    file_content = fm.read_input('inputs/input7.fsm')
    # print(file_content)

    states = file_content[0]
    events = file_content[1]
    initial_state = file_content[2]
    marked_states = file_content[3]
    transitions = file_content[4:]

    # Criando o autômato inicial
    automaton_2 = Automaton(states, events, initial_state, marked_states, transitions)

    # Instanciando classe em que serão feitas as operações no autômato
    aut = AutomatonOperation(automaton)

    # print('AUTOMATO ORIGINAL:')
    # print(automaton)
    # automaton.draw('Original1', 'output')
    # automaton_2.draw('Original2', 'output')

    # print('AUTOMATO ACESSIVEL:')
    # print(aut.accessibility())
    # print('AUTOMATO CO-ACESSIVEL:')
    # print(aut.co_accessibility())
    # print('AUTOMATO TRIM:')
    # print(aut.trim())

    # aut.accessibility().draw('Acessibilidade')
    # aut.co_accessibility().draw('Co-acessibilidade')
    # aut.trim().draw('Trim')
    # aut.total().draw('Total')
    # aut.minimization().draw('Minimizacao')
    # aut.product_composition(automaton, automaton_2).draw('Composição_por_produto', 'output')
    aut.parallel_composition(automaton, automaton_2).draw('Composição_paralela', 'output')


if __name__ == '__main__':
    main()
