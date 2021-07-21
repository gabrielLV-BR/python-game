#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

import math
from random import randint

import pygame
from pygame import Vector2 as vec2

from entities.bullet import Bullet

from utils.config import Config
from utils.input_manager import InputManager


class Ship():

    _explosion_gif = []

    def __init__(self, pos: vec2):
        for i in range(7):
            self._explosion_gif.append(pygame.image.load(
                f"res/images/explosao/{i+1}.gif"))
        self._explosion_gif.append(
            pygame.image.load("res/images/explosao/8.png"))

        self.VELOCITY = 10

        # carrega a imagem
        imagem = pygame.image.load("res/images/nave.png")
        self.imagem = pygame.transform.scale(imagem, (60, 80))
        self.rect = self.imagem.get_rect(center=pos)

        self.pode_atirar = True

        # Tempo de espera entre cada tiro
        self.MAX_COUNTDOWN = 10
        self.countdown = 0

        # O FRAME_TIME indica quantos milisegundos dura cada frame
        # (só utilizado se morto, quando temos que animar a explosão)
        self.FRAME_TIME = 80
        self.frame = 0

        # para limitar os tiros
        self.MAX_TIROS = 5
        self.tiros = [None] * self.MAX_TIROS
        self.angulo = 0

        self.tamanho = 1

    # atualiza a posição da espaçonave de acordo com a flag de movimento
    def atualiza(self, config: Config):
        for tiro in self.tiros:
            if tiro == None:
                continue
            tiro.atualiza(config)
            if (tiro.rect.centerx > config.width) or (tiro.rect.centerx < 0):
                self.remove_tiro(tiro)
        if not config.player_morto:
            esquerda = InputManager.get_key(pygame.K_a)
            direita = InputManager.get_key(pygame.K_d)
            cima = InputManager.get_key(pygame.K_w)
            baixo = InputManager.get_key(pygame.K_s)

            vel = vec2(
                (direita - esquerda),
                (baixo - cima)
            )

            vel_mag = vel.magnitude()

            # Normalizamos a velocidade, mas só a magnitude dela for diferente de 0
            if vel_mag != 0:
                vel = vel / vel_mag

            self.rect.centerx += vel.x * self.VELOCITY
            self.rect.centery += vel.y * self.VELOCITY

            # Pega a posição do mouse
            x, y = InputManager.get_mouse_pos()

            # Calcula o angulo dele em relação à nave
            self.angulo = math.atan2(
                y - self.rect.centery, x - self.rect.centerx)
            self.angulo = math.degrees(self.angulo)

            # print(f"X: {x} Y: {y} - A: {self.angulo}")
            if self.countdown < self.MAX_COUNTDOWN and not self.pode_atirar:
                self.countdown += 1
            else:
                self.countdown = 0
                self.pode_atirar = True

            # Se o botão 0 (esquerdo) foi apertado, atiramos
            if pygame.mouse.get_pressed()[0] and self.pode_atirar:
                self.atira(vec2(x, y))
                self.pode_atirar = False
        else:
            self.countdown += config.delta
            if self.countdown > self.FRAME_TIME:
                self.countdown = 0
                self.frame += 1
                if self.frame >= 7:
                    self.frame = 7
                    self.tamanho = 0.4
                    self.angulo += 1

            self.imagem = self._explosion_gif[self.frame]

    # desenha a nave na sua posição atual
    def desenha(self, tela):
        for tiro in self.tiros:
            if not tiro:
                continue
            tiro.desenha(tela)

        imagem_transformada = pygame.transform.rotozoom(
            self.imagem, -(self.angulo + 90), self.tamanho)
        new_rect = imagem_transformada.get_rect(center=self.rect.center)
        tela.blit(imagem_transformada, new_rect)

    def get_pos(self) -> vec2:
        return vec2(self.rect.centerx, self.rect.centery)

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
        # cirei minha "própria implementação²" para sustentar meu método de adição
        for i in range(len(self.tiros)):
            if self.tiros[i] == None:
                continue

            if self.tiros[i] == tiro:
                self.tiros[i] = None
