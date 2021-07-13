#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

from bullet import Bullet
import math
import pygame
from pygame import Vector2 as vec2

from input_manager import InputManager
from random import randint 

class Ship():
	
	def __init__(self, vel):
		self.vel = vel
		
		# carrega a imagem
		imagem = pygame.image.load("images/nave.png")
		self.imagem = pygame.transform.scale(imagem, (40, 60))

		self.rect = self.imagem.get_rect()
		self.rect.centerx = 139
		self.rect.centery = 139
		
		self.pode_atirar = True

		self.MAX_COUNTDOWN = 10
		self.countdown_atirar = 0

		# para limitar os tiros
		self.MAX_TIROS = 5
		self.tiros = [None] * self.MAX_TIROS
		self.angulo = 0

		print(self.tiros)

	# desenha a nave na sua posição atual
	def desenha(self, tela):
		for tiro in self.tiros:
			if not tiro: continue
			tiro.desenha(tela)

		imagem_transformada = pygame.transform.rotozoom(self.imagem, -(self.angulo + 90), 1)	
		new_rect = imagem_transformada.get_rect(center = self.rect.center)
		tela.blit(imagem_transformada, new_rect)

	# atualiza a posição da espaçonave de acordo com a flag de movimento
	def atualiza(self, config):
		for tiro in self.tiros:
			if tiro == None: continue
			tiro.atualiza(config)
			if (tiro.rect.centerx > config.width) or (tiro.rect.centerx < 0):
				self.removeTiro(tiro)

		esquerda = InputManager.get_key(pygame.K_a)
		direita = InputManager.get_key(pygame.K_d)
		cima = InputManager.get_key(pygame.K_w)
		baixo = InputManager.get_key(pygame.K_s)

		velx = (direita - esquerda) * self.vel
		vely = (baixo - cima) * self.vel

		self.rect.centerx += velx
		self.rect.centery += vely

		# Pega a posição do mouse
		x, y = InputManager.get_mouse_pos()

		# Calcula o angulo dele em relação à nave
		self.angulo = math.atan2(y - self.rect.centery, x - self.rect.centerx)
		self.angulo = math.degrees(self.angulo)

		if self.countdown_atirar < self.MAX_COUNTDOWN and not self.pode_atirar:
			self.countdown_atirar += 1
		else:
			self.countdown_atirar = 0
			self.pode_atirar = True

		# Se o botão 0 (esquerdo) foi apertado, atiramos
		if pygame.mouse.get_pressed()[0] and self.pode_atirar:
			self.atira(vec2(x, y))
			print(len(self.tiros))
			self.pode_atirar = False

	def atira(self, mouse):
		# crio o objeto Bullet
		novo_tiro = Bullet(self.rect.center, mouse)

		# adiciono o novo_tiro à lista de tiros
		self.addTiro(novo_tiro)
	
	def addTiro(self, tiro):
		# criei minha "própria implementação" pra evitar ficar realocando a memória toda a hora


		# para não estourar o limite

		for i in range(len(self.tiros)):
			if self.tiros[i] == None:
				self.tiros[i] = tiro
				print(self.tiros)
				return

		if len(self.tiros) >= self.MAX_TIROS:
			return

		self.tiros.append(tiro)

	def removeTiro(self, tiro):
		# cirei minha "própria implementação²" para sustentar meu método de adição
		for i in range(len(self.tiros)):
			if self.tiros[i] == None: continue

			if self.tiros[i].id == tiro.id:
				self.tiros[i] = None