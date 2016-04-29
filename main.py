#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from file_manager import *
from matrix import *
from node import *
from edge import *

def main():
    fm = FileManager()

	# Le os dados de entrada a partir de um arquivo csv
    file_content = fm.read_csv("States.csv")

    # Lista de nós que representam a Máquina de Estados (ME) completa
    nodes = []

    # Cria os nós de acordo com o arquivo de entrada
    for i,line in enumerate(file_content):

        if line[1].upper() == "TRUE":
            line[1] = True
        else:
            line[1] = False

        if line[2].upper() == "TRUE":
            line[2] = True
        else:
            line[2] = False

        # Cria lista com as arestas de acordo com o arquivo de entrada
        # for j,value in enumerate(line[3]):

        # Lista de arestas utilizada para teste
        es = []
        e = Edge('a', 0)
        es.append(e)
        e = Edge('b', 0)
        es.append(e)
        # -------------------------------------

        # Nó criado a partir da linha atual de entrada
        n = Node(int(line[0]), line[1], line[2], es)

        # Nó atual eh adicionado a lista de nós da ME
        nodes.append(n)

    print(nodes[0])

if __name__ == '__main__':
    main()
