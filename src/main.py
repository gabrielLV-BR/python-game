"""
	VERSÃO 6.0 POR: Gabriel Lovato Vianna
	GITHUB: gabrielLV-BR
"""

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from pygame import Vector2 as vec2

from random import randint
from entities.enemies.dumb_alien import DumbAlien

from utils.config import Config
from utils.input_manager import InputManager
from utils.enemy_handler import EnemyHandler

from entities.ship import Ship
from entities.enemies.alien import Alien
from entities.enemies.frota import Frota

clock = pygame.time.Clock()

def create_window(config):
	pygame.init()
	tela = pygame.display.set_mode((config.width, config.height))
	pygame.display.set_caption(config.title)
	return tela

def main():
	timer = 0
	lastTime = pygame.time.get_ticks()

	config = Config("Alien Invasion v6", 1000, 800)
	tela = create_window(config)

	player = Ship(vec2(config.width / 2, config.height / 2))

	enemyHandler = EnemyHandler()

	isRunning = True

	while isRunning:
		now = pygame.time.get_ticks()
		config.delta = now - lastTime

		# O InputManager.poll_events() retorna se a tela deve fechar ou não
		isRunning = not InputManager.poll_events()

		for inimigo in enemyHandler.enemies:
			if not inimigo or isinstance(inimigo, Frota): continue
			# Checar se colidiu com tiro
			for tiro in player.tiros:
				if not tiro: continue
				if inimigo.rect.colliderect(tiro.rect):
					enemyHandler.kill_enemy(inimigo)
					player.remove_tiro(tiro)
					break
			# Checar se colidiu com player
			if inimigo.rect.colliderect(player.rect) and not inimigo.morto:
				config.player_morto = True

		timer += config.delta

		config.player_pos = player.get_pos()

		player.atualiza(config)
		player.desenha(tela)

		# Lida com a lógica de spawn e atualiza inimigos
		enemyHandler.atualiza(config)

		# Renderiza os inimigos
		enemyHandler.desenha(tela)

		# Troca o screen buffer
		pygame.display.flip()

		# Limpa a tela
		tela.fill((0,0,0))

		clock.tick(30)
		lastTime = now

	pygame.quit()

main()
