#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame

from random import randint 

class Ship():
	
	def __init__(self, config):
		self.velocidade = config.nave_velocidade
		
		#carrega a imagem
		numero_imagem = randint(1,6)
		nome_imagem = 'imagens/nave' + str(numero_imagem) + '.png'
		self.imagem = pygame.image.load(nome_imagem)
		self.retangulo = self.imagem.get_rect()
		
	#desenha a nave na sua posição atual
	def desenha(self, tela):
		tela.blit(self.imagem, self.retangulo)

	#atualiza a posição da espaçonave de acordo com a flag de movimento
	def atualiza(self, config):
		pass	
