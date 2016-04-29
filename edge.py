#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Edge(object):
    """docstring for """
    def __init__(self, event, state):
        # super(, self).__init__()
        self.event = event  # Evento responsável pela transição
        self.state = state  # Estado destino após a transição

    def __str__(self):
        """Retorna uma representação em string da aresta"""
        edge_str = str(self.event)
        edge_str += " -> "
        edge_str += str(self.state)

        return edge_str
