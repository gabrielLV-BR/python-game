#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import pygame
from pygame import Color, Vector2 as vec2
from entities.bullet import Bullet

from enums import ShipStates

from random import randint
import math

from utils.config import Config
from utils.input_manager import InputManager

# O DumbAlien vai ser utilizado pela frota, e para não repetir o código,
# resolvi fazer o Alien extender o DumbAlien e sobrescrever o método de atualizar.
# O único objetivo do DumbAlien é ir em direção ao target


class DumbAlien:
    _alien_image = pygame.image.load("res/images/alien1.png")
    _explosion_gif = []

    def __init__(self, pos: vec2, vel=5, max_fire_countdown=1000):
        for i in range(7):
            self._explosion_gif.append(pygame.image.load(
                f"res/images/explosao/{i+1}.gif"))

        self.imagem = pygame.transform.scale(self._alien_image, (50, 60))
        self.rect = self.imagem.get_rect(center=pos)

        # DEBUG
        self.target_img = pygame.Surface((10, 10))
        self.target_img.fill(Color(255, 0, 0, 255))
        self.target_rect = pygame.Rect(0, 0, 0, 0)
        #

        self.morto = False

        self.timer = 0

        # O target é pra onde o alien vai apontar e atirar
        self.target = pos

        # O next_position é pra onde o alien vai querer ir
        self.next_position = pos

        self.size = 1
        self.angulo = 0
        self.vel = vec2(0, 0)

        # Esses states servem pra eles serem gerenciados no Frota
        self.state = ShipStates.READY

        self.VELOCITY = vel
        self.esta_posicionado = False

        self.FRAME_TIME = 80
        self.MAX_FIRE_COUNTDOWN = max_fire_countdown
        self.frame = 0
        self.countdown = 0

        self.MAX_TIROS = 3
        self.tiros = []

    def set_target(self, new_target: vec2):
        self.target = new_target
        self.olhe_para(self.target)

    def set_next_position(self, new_target: vec2):
        self.esta_posicionado = False
        self.next_position = new_target

        # DEBUG
        self.target_rect = pygame.Rect(
            self.next_position.x,
            self.next_position.y,
            self.next_position.x + self.target_img.get_width(),
            self.next_position.y + self.target_img.get_height(),
        )
        #

    def atualiza(self, config: Config):
        for tiro in self.tiros:
            if tiro == None:
                continue
            tiro.atualiza(config)
            if (tiro.rect.centerx > config.width) or (tiro.rect.centerx < 0):
                self.remove_tiro(tiro)

        self.countdown += config.delta

        if not self.morto:
            self.olhe_para(config.player_pos)

            if self.countdown > self.MAX_FIRE_COUNTDOWN:
                self.atira(config.player_pos)
                self.countdown = 0

            if not self.esta_posicionado:
                self.vel: vec2 = self.next_position - self.get_pos()
                vel_mag = self.vel.magnitude()

                # Mesmo problema que tinha dado no player, não podemos normalizar
                # um vetor de magnitude 0
                if vel_mag < 2.0:
                    # Estou fazendo desse jeito para que eu sempre saiba quando eu estou
                    # em posição. Dou uma margem de distância para evitar erros.
                    self.esta_posicionado = True
                else:
                    self.esta_posicionado = False
                    self.vel = self.vel / vel_mag
                self.rect.center += self.vel * self.VELOCITY

        else:
            if self.countdown > self.FRAME_TIME and self.frame < 6:
                self.countdown = 0
                self.frame += 1

            self.imagem = self._explosion_gif[self.frame]

    # Agora, sabemos se estamos posicionados ou não ao consultar a variável self.esta_posicionado
    # def esta_no_target(self):
    #     # return ((self.get_pos() - self.target).magnitude_squared()) < (margem ** 2)

    def desenha(self, tela):
        for tiro in self.tiros:
            if not tiro:
                continue
            tiro.desenha(tela)

        imagem_transformada = pygame.transform.rotozoom(
            self.imagem, self.angulo + 180, self.size
        )

        new_rect = imagem_transformada.get_rect(center=self.rect.center)

        tela.blit(imagem_transformada, new_rect)
        # DEBUG
        tela.blit(self.target_img, self.target_rect)
        #

    def morre(self):
        print("MORREU")
        self.morto = True
        self.size = 0.4
        self.angulo = randint(0, 360)
        self.countdown = 0
        self.imagem = self._explosion_gif[0]

    def pode_ir(self) -> bool:
        return (self.morto and (self.countdown >= self.FRAME_TIME))

    def olhe_para(self, ponto: vec2):
        self.angulo = math.atan2(
            ponto.y - self.rect.centery,
            ponto.x - self.rect.centerx
        )

        self.angulo = -math.degrees(self.angulo) + 90

    def get_pos(self) -> vec2:
        return vec2(self.rect.centerx, self.rect.centery)

    def set_pos(self, new_pos: vec2):
        self.rect.centerx = new_pos.x
        self.rect.centery = new_pos.y

    def esta_colidindo(self, alvo: pygame.Rect) -> bool:
        return self.rect.colliderect(alvo)

    # Roubado completamente do ship.py

    def atira(self, mouse: vec2):
        # crio o objeto Bullet
        novo_tiro = Bullet(self.rect.center, mouse)

        # adiciono o novo_tiro à lista de tiros
        self.add_tiro(novo_tiro)

    def add_tiro(self, tiro: Bullet):
        # criei minha "própria implementação" pra evitar ficar realocando a memória toda a hora
        # para não estourar o limite

        for i in range(len(self.tiros)):
            if self.tiros[i] == None:
                self.tiros[i] = tiro
                return

        if len(self.tiros) >= self.MAX_TIROS:
            return

        self.tiros.append(tiro)

    def remove_tiro(self, tiro: Bullet):
        # criei minha "própria implementação²" para sustentar meu método de adição
        for i in range(len(self.tiros)):
            if self.tiros[i] == None:
                continue

            if self.tiros[i] == tiro:
                self.tiros[i] = None
