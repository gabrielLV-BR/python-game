__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from pygame import Vector2 as vec2

from random import randint 

from entities.enemies.dumb_alien import DumbAlien

import math

from utils.config import Config

# O Alien está extendendo o DumbAlien porque suas funcionalidades são muito semelhantes,
# porém o Alien é esperto e segue o player sozinho.

class Alien(DumbAlien):
	def __init__(self, pos: vec2):
		super().__init__(pos, 9)

	#atualiza a posicao do alien
	def atualiza(self, config: Config):
		if not config.player_morto:
			super().set_target(config.player_pos)
		else:
			# Pego a distância daqui até o player e inverto ela, para que
			# a nave vá para longe
			longe : vec2 = (config.player_pos - self.get_pos()) * -1
			super().set_target(longe)

		super().atualiza(config)
		# direcao : vec2 = config.playerPos - self.rect.center
		# direcao = direcao.normalize()

		# # Calcula ângulo
		# self.angulo = math.atan2(config.player_pos.y - self.rect.centery, config.player_pos.x - self.rect.centerx)
		# self.angulo = math.degrees(self.angulo)

		# self.rect.centerx += direcao.x * self.VELOCITY
		# self.rect.centery += direcao.y * self.VELOCITY
