#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from random import randint 
import math

class Alien:
	
	_alien_img = pygame.image.load("res/images/alien1.png")

	def __init__(self, pos):
		self.imagem = pygame.transform.scale(self._alien_img, (60, 80))
		# self.imagem = pygame.Surface((20,20))
		# self.imagem.fill((255, 0, 0))
		self.rect = self.imagem.get_rect(center = pos)	

		self.vel = 3

		self.timer = 0

	#desenha o alien na sua posição atual
	def desenha(self, tela):
		tela.blit(self.imagem, self.rect)

	#atualiza a posicao do alien
	def atualiza(self, config):
		pass
