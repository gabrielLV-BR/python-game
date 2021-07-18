# Uma frota é um bando de DumbAliens que seguem o líder, que seria o primeiro na lista.
# O lider sempre quer cercar o jogador.

from pygame import Vector2 as vec2

from entities.enemies.dumb_alien import DumbAlien
from utils.config import Config

class Frota:
    def __init__(self, pos: vec2, count: int, speed: float = 3.0):
        if count < 2:
            count = 2

        self.SPEED = speed

        self.enemies = ([DumbAlien(pos, speed)] * count)

        self.target = pos
        self.vel = vec2(10, 10)

        self.iter = 0

    def atualiza(self, config: Config):
        # distance_to_target = self.target - self.enemies[0].get_pos()
        # if distance_to_target.magnitude() < 2:
        #     self.get_new_target(config)

        self.segue_o_lider()

        self.enemies[0].rect.centerx += self.vel.x
        self.enemies[0].rect.centery += self.vel.y

        self.get_new_target(config)

    def desenha(self, tela):
        print(f"ITER Nº {self.iter}")
        for enemy in self.enemies:
            if not enemy: continue
            print(enemy._target)
            self.iter += 1
            enemy.desenha(tela)
        print("-"*6)

    def segue_o_lider(self):
        for i in range(len(self.enemies)-1, 0, -1):
            proximo = self.enemies[i-1]
            if proximo == None:
                continue
            self.enemies[i].set_target(proximo.get_pos())
            
    def get_new_target(self, config: Config):
        to_player = config.player_pos - self.enemies[0].get_pos()
        self.target = config.player_pos
        self.vel = to_player.normalize() * self.SPEED
        # to_player = config.player_pos - self.enemies[0].get_pos()
        # new_target = to_player.rotate(20)
        # to_new_target = new_target - self.enemies[0].get_pos()

        # mag = to_new_target.magnitude()
        # if mag != 0:
        #     to_new_target /= mag

        # self.vel = to_new_target

    # De novo, peguei do ship.py
    def remove_enemy(self, enemy):
        for i in range(len(self.enemies)):
            if self.enemies[i] == None:
                continue

            if self.enemies[i] == enemy:
                self.enemies[i] = None
