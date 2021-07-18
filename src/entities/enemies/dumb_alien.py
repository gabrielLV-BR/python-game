#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from pygame import Vector2 as vec2

from random import randint
import math

from utils.config import Config


# O DumbAlien vai ser utilizado pela frota, e para não repetir o código,
# resolvi fazer o Alien extender o DumbAlien e sobrescrever o método de atualizar.
# O único objetivo do DumbAlien é ir em direção ao target

class DumbAlien:
    _alien_image = pygame.image.load("res/images/alien1.png")
    _explosion_gif = []

    def __init__(self, pos: vec2, vel=5):
        for i in range(7):
            self._explosion_gif.append(pygame.image.load(
                f"res/images/explosao/{i+1}.gif"))

        self.imagem = pygame.transform.scale(self._alien_image, (50, 60))
        self.rect = self.imagem.get_rect(center=pos)

        self.morto = False

        self.timer = 0
        self._target = pos

        self.size = 1
        self.angulo = 0
        self.vel = vec2(0, 0)

        self.VELOCITY = vel

        self.FRAME_TIME = 80
        self.frame = 0
        self.countdown = 0

    def set_target(self, new_target: vec2):
        self._target = new_target

        self.vel: vec2 = new_target - self.rect.center

        vel_mag = self.vel.magnitude()

        # Mesmo problema que tinha dado no player, não podemos normalizar
        # um vetor de magnitude 0
        if vel_mag != 0:
            self.vel = self.vel.normalize()

        self.angulo = math.atan2(
            new_target.y - self.rect.centery, new_target.x - self.rect.centerx
        )

        self.angulo = -math.degrees(self.angulo) + 90

    def atualiza(self, config: Config):
        if not self.morto:
            self.rect.center += self.vel * self.VELOCITY
        else:
            self.countdown += config.delta

            if self.countdown > self.FRAME_TIME and self.frame < 6:
                self.countdown = 0
                self.frame += 1
            
            self.imagem = self._explosion_gif[self.frame]

    def desenha(self, tela):
        imagem_transformada = pygame.transform.rotozoom(self.imagem, self.angulo, self.size)
        tela.blit(imagem_transformada, self.rect)

    def die(self):
        self.morto = True
        self.size = 0.4
        self.angulo = randint(0, 360)

    def pode_ir(self) -> bool:
        return (self.morto and (self.countdown >= self.FRAME_TIME))

    def get_pos(self) -> vec2:
        return vec2(self.rect.centerx, self.rect.centery)
