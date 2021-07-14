"""
	VERSÃO 6.0 POR: Gabriel Lovato Vianna
	GITHUB: gabrielLV-BR
"""

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from pygame import Vector2 as vec2

from utils.config import Config
from entities.ship import Ship
from entities.alien import Alien
from utils.input_manager import InputManager

clock = pygame.time.Clock()

inimigos = [Alien(vec2(20, 20))]

delta = 0


def createWindow(config):
	pygame.init()
	tela = pygame.display.set_mode((config.width, config.height))
	pygame.display.set_caption(config.title)
	return tela

def main():
	timer = 0
	last_time = pygame.time.get_ticks()

	config = Config("Alien Invasion v6", 1000, 800)
	tela = createWindow(config)

	player = Ship(10)

	isRunning = True

	while isRunning:
		now = pygame.time.get_ticks()
		config.delta = now - last_time

		# O InputManager.poll_events() retorna se a tela deve fechar ou não
		isRunning = not InputManager.poll_events()

		# # Lógica do spawn de inimigos
		# if timer > 3000:
		# 	inimigos.append(Alien(pygame.Vector2(config.width - 10, config.height - 10)))

		player.atualiza(config)
		player.desenha(tela)

		# Atualiza os inimigos
		for alien in inimigos:
			alien.atualiza(config)

		# Renderiza eles os inimigos
		for alien in inimigos:
			alien.desenha(tela)

		# Troca o screen buffer
		pygame.display.flip()

		# Limpa a tela
		tela.fill((0,0,0))

		clock.tick(30)
		last_time = now

	pygame.quit()

main()
