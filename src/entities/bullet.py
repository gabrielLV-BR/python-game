#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "20/05/2019"

import math
from random import random
import pygame
from pygame import Vector2 as vec2

_GlobalID = 0

class Bullet:
	BulletImg = pygame.image.load("res/images/tiro.png")

	def __init__(self, pos, mouse):
		# pra eu ter acesso ao _GlobalID
		global _GlobalID

		# Isso aqui é pra cada bala ter um ID único, o que facilita na hora
		# da remoção

		# provavelmente só com o _GlobalID já servia, mas assim é mais uma
		# garantia
		self.id = f"{_GlobalID}-{random() * 1000}"
		_GlobalID += 1

		# crio um vetor apontando pro mouse
		tiro_dir = vec2(mouse.x - pos[0], mouse.y - pos[1])
		
		# normalizo ele pra que a velocidade da bala seja independente da distância
		# do mouse da nave
		tiro_dir = tiro_dir.normalize()

		angulo = math.degrees(math.atan2(tiro_dir.y, tiro_dir.x)) + 90

		self.image = pygame.transform.rotozoom(self.BulletImg, -angulo, 0.2)

		self.rect = self.image.get_rect(center = pos)
		self.SPEED = 3.0
		self.vel = tiro_dir * self.SPEED

	def atualiza(self, config):
		self.rect.centerx += self.vel.x * 10
		self.rect.centery += self.vel.y * 10
	
	def desenha(self, tela):
		tela.blit(self.image, self.rect)
