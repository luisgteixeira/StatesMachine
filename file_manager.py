#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import csv
import os.path
from time import asctime

class FileManager(object):
	"""FileManager e a classe responsavel por ler e escrever em arquivos"""

	def reset_log(self):
		"""
		Sobrescreve o arquivo de log, caso exista. Caso contrario, ele eh criado
		"""
		self.write_log(self.__get_time_log() + " Execucao iniciada.\n", True)


	@staticmethod
	def write_log(text, reset=False):
		"""Escreve o texto passado no parametro text no arquivo de log."""
		if reset:
			log = open('log', 'w')
		else:
			log = open('log', 'a') # Abre o arquivo para adicao de conteudo
		log.write(text)        # Escreve text no arquivo
		log.close()            # Fecha o arquivo, salvando as alteracoes


	def __get_time_log(self):
		"""Retorna o tempo para ser inserido no log."""
		return "[" + asctime() + "]"


	def read_input(self, input_file):
		"""
		Le o arquivo de entrada. Retorna uma lista onde cada elemento
		corresponde a uma linha do arquivo.
		"""
		content = None  # Inicializa o conteudo como nulo

		# Verifica de o arquivo existe
		if os.path.exists(input_file):
			# Verifica se eh, de fato, um arquivo (pode ser diretorio)
			if os.path.isfile(input_file):
				# Inicializa o manipulador do arquivo de entrada como nulo
				input_handler = None
				try:
					# Abre o arquivo em modo de leitura (padrao)
					input_handler = open(input_file)
					# Le cada linha do arquivo para uma lista
					content = input_handler.readlines()
					for i, line in enumerate(content):
						line = line.replace(" ", "")
						content[i] = line.replace("\n", "")
				except Exception as e:
					# Caso ocorra alguma excecao, uma mensagem de erro eh
					# adicionada ao arquivo de log e exibida no termonal
					# juntamente com a excecao ocorrida
					content = None
					error_time = self.__get_time_log
					error_message = "Erro ao abrir o arquivo de entrada."
					error_message = error_time + " " + error_message + "\n"
					error_message += str(sys.exc_info()[1]) + "\n"
					self.write_log(error_message)
					raise
				finally:
					# Realiza o fechamento do arquivo caso o mesmo tenha sido
					# aberto com sucesso
					if input_handler is not None:
						input_handler.close()

		# Retorna o conteudo do arquivo em uma lista onde cada item corresponde
		# a uma linha. Caso tenha ocorrido algum erro, retorn None
		return content
