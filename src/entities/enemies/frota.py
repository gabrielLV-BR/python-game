# Uma frota é um bando de DumbAliens que seguem o líder, que seria o primeiro na lista.
# O lider sempre quer cercar o jogador.
from random import randint
from typing import cast
from pygame import Vector2 as vec2, mouse
import pygame
from entities.bullet import Bullet

from entities.enemies.dumb_alien import DumbAlien

from utils.config import Config
from utils.input_manager import InputManager

from enums import ShipStates


class Frota:
    def __init__(self, count: int, speed: float = 6.0):
        if count < 2:
            count = 2

        self.SPEED = speed
        self.MIN_TARGET_DISTANCE = 3

        self.enemies = []

        for i in range(count):
            self.enemies.append(
                DumbAlien(vec2(-10, -10), self.SPEED, randint(2, 5) * 1000))

        self.rotate_around = 0

    def atualiza(self, config: Config):
        for i in range(0, len(self.enemies)):
            enemy = self.enemies[i]
            if not enemy:
                continue
            elif enemy.pode_ir():
                self.enemies[i] = None
            elif enemy.esta_posicionado and enemy.state == ShipStates.READY:
                self.calcular_posicao(i, config)
                enemy.state = ShipStates.SET

            enemy.atualiza(config)

    def esta_colidindo(self, alvo: pygame.Rect):
        for enemy in [x for x in self.enemies if x]:
            if enemy.rect.colliderect(alvo) and not enemy.morto:
                return enemy
        return None

    def calcular_posicao(self, index: int, config: Config):
        enemy = self.enemies[index]
        step = 360 / len(self.enemies)
        enemy_angle = step * index
        enemy_pos = vec2(0, 0)
        enemy_pos.from_polar((400, enemy_angle))

        enemy_pos += vec2(config.width / 2, config.height / 2)

        enemy.set_pos(enemy_pos * -1.5)
        enemy.set_next_position(enemy_pos)
        enemy.set_target(config.player_pos)

    def desenha(self, tela):
        for enemy in self.enemies:
            if not enemy:
                continue
            enemy.desenha(tela)

    def pode_ir(self):
        return self.enemies.count(None) == len(self.enemies)

    def kill_enemy(self, enemy):
        try:
            indice = self.enemies.index(enemy)
            self.enemies[indice].morre()
        finally:
            return

    # Fiz uma property para poder só usar um enemy.tiros no enemy_handler
    @property
    def tiros(self) -> list[Bullet]:
        tiros = []
        for enemy in [x for x in self.enemies if x]:
            tiros.extend(enemy.tiros)
        return tiros

    def remove_enemy(self, enemy):
        for i in range(len(self.enemies)):
            if self.enemies[i] == None:
                continue

            if self.enemies[i] == enemy:
                self.enemies[i] = None
