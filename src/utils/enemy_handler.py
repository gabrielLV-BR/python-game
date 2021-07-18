# Eu sei que eu estou abstraindo demais, mas eu não consigo me controlar...

# O enemies handler antes era só uma lista no main.py, mas daí teria todo o problema
# de ficar removendo e adicionando pra lista, então resolvi dar o mesmo remédio que
# eu dei pro ship.py. Virou uma classe própria pra que não fique código específico solto no main

from random import randint

from pygame import Vector2 as vec2
from entities.enemies.alien import Alien
from entities.enemies.dumb_alien import DumbAlien
from entities.enemies.frota import Frota
from utils.config import Config


class EnemyHandler:
    def __init__(self, preexistente=[]):
        self.enemies = preexistente
        self.timer = 0

    def atualiza(self, config: Config):
        self.timer += config.delta

        # # Lógica do spawn de inimigos
        if self.timer > 3000 and not config.player_morto:
            self.spawn_enemy(config)
            self.timer = 0

        for enemy in self.enemies:
            if (enemy == None):
                continue
            enemy.atualiza(config)
            if enemy.pode_ir():
                self.remove_enemy(enemy)

    def desenha(self, tela):
        for enemy in self.enemies:
            if enemy == None:
                continue
            enemy.desenha(tela)

    # Copiado diretamente do Ship.py
    def add_enemy(self, enemy):
        for i in range(len(self.enemies)):
            if self.enemies[i] == None:
                self.enemies[i] = enemy
                return

        if len(self.enemies) >= self.MAX_TIROS:
            return

        self.tiros.append(enemy)

    def remove_enemy(self, enemy):
        for i in range(len(self.enemies)):
            if self.enemies[i] == None:
                continue

            if self.enemies[i] == enemy:
                self.enemies[i] = None

    def kill_enemy(self, enemy):
        for i in self.enemies:
            if i == enemy:
                enemy.die()

    def spawn_enemy(self, config: Config):
        # coin = randint(0, 10)

        # self.enemies.add_enemy(Frota(vec2(10,10), 5))

        # 20% de chance de spawnar uma frota
        # if coin >= 8:
        # 	self.enemies.append(Frota(vec2(10, 10), 5))
        # else:
        x = randint(0, config.width)
        y = randint(0, config.height)
        self.enemies.append(Alien(vec2(x, y)))
