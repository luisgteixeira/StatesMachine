#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from file_manager import *
from state import *
from automaton import *

def main():
    fm = FileManager()
    fm.reset_log()

	# Le os dados de entrada a partir de um arquivo texto
    file_content = fm.read_input('input2')
    # print(file_content)

    states = file_content[0]
    initial_state = file_content[1]
    marked_states = file_content[2]
    transitions = file_content[3:]

    # print(transitions)

    automaton = Automaton(states, initial_state, marked_states, transitions)

    print(automaton)


if __name__ == '__main__':
    main()
