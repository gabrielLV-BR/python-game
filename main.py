"""
	VERSÃO 6.0 POR: Gabriel Lovato Vianna
	GITHUB: gabrielLV-BR
"""

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame

from config import Config
from ship import Ship
from input_manager import InputManager

clock = pygame.time.Clock()

def createWindow(config):
	pygame.init()
	tela = pygame.display.set_mode((config.width, config.height))
	pygame.display.set_caption(config.title)
	return tela

def main():
	config = Config("Alien Invasion v6", 500, 300)
	tela = createWindow(config)

	player = Ship(10)

	isRunning = True

	while isRunning:
		# O InputManager.poll_events() retorna se a tela deve fechar ou não
		isRunning = not InputManager.poll_events()

		player.atualiza(config)
		player.desenha(tela)

		# Troca o screen buffer
		pygame.display.flip()

		# Limpa a tela
		tela.fill((0,0,0))

		clock.tick(30)

	pygame.quit()

main()
