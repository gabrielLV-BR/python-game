"""
	VERSÃO 6.0 POR: Gabriel Lovato Vianna
	GITHUB: gabrielLV-BR
"""

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from pygame import Vector2 as vec2

from random import randint
from entities.bullet import Bullet
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
        timer += config.delta

        # O InputManager.poll_events() retorna se a tela deve fechar ou não
        isRunning = not InputManager.poll_events()

        for inimigo in [x for x in enemyHandler.enemies if x]:
            # Checar se colidiu com tiro
            for tiro in [x for x in player.tiros if x]:
                if isinstance(inimigo, Frota):
                    # A função esta_colidindo da frota retorna o inimigo que está
                    # colidindo ou None se nenhum estiver.
                    inimigo_colidindo = inimigo.esta_colidindo(tiro.rect)
                    if inimigo_colidindo:
                        inimigo.kill_enemy(inimigo_colidindo)
                        player.remove_tiro(tiro)
                        continue

                if inimigo.esta_colidindo(tiro.rect):
                    enemyHandler.kill_enemy(inimigo)
                    player.remove_tiro(tiro)
                    break
            # Checar se colidiu com player
            if inimigo.esta_colidindo(player.rect):
                config.player_morto = True

        # Checar se as balas inimigas colidiram com o jogador
        for tiro in [x for x in enemyHandler.get_tiros() if x]:
            if tiro.rect.colliderect(player.rect):
                config.player_morto = True

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
        tela.fill((0, 0, 0))

        clock.tick(30)
        lastTime = now

    pygame.quit()


main()
