#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import os.path

class FileManager(object):
	"""FileManager e a classe responsavel por ler e escrever em arquivos"""

	def read_csv(self, ipt):
		"""
		Retorna o conteudo do arquivo de entrada csv
		na forma de uma lista de listas (matriz)
		"""
		if os.path.exists(ipt) and os.path.isfile(ipt):
			try:
				data = csv.reader(open(ipt), delimiter=';')
				return list(data)
			except Exception as e:
				print("Nao foi possivel abrir o arquivo: %s" % ipt)
				raise e
