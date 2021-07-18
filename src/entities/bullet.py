#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "20/05/2019"

import math
from random import random
import pygame
from pygame import Vector2 as vec2

from utils.config import Config


class Bullet:
	BulletImg = pygame.image.load("res/images/tiro.png")

	def __init__(self, pos: vec2, mouse: vec2):
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

	def atualiza(self, config: Config):
		self.rect.centerx += self.vel.x * 10
		self.rect.centery += self.vel.y * 10
	
	def desenha(self, tela):
		tela.blit(self.image, self.rect)
