from utils.vector import vec2
from pygame.constants import *
import pygame

# Essa classe é para ser um Singleton, porém ela ainda pode ser
# instanciada. Como nenhuma instância vai ter variáveis próprias,
# resolvi permitir

class InputManager:
  pressed_keys = {
    K_w: False, 
    K_a: False, 
    K_s: False, 
    K_d: False,
    K_e: False,
    K_LEFT: False, 
    K_RIGHT: False, 
    K_UP: False, 
    K_DOWN: False, 
    K_SPACE: False
  }

  mouse_pos = vec2(0, 0)

  @classmethod
  def poll_events(cls):
    for event in pygame.events.get():
      if event.key in cls.pressed_keys:
        cls.pressed_keys[event.key] = event.type == KEYUP
    cls.mouse_pos.x, cls.mouse_pos.y = pygame.mouse.get_pos()

  @classmethod
  def get_key(cls, key) -> bool:
    if key not in cls.pressed_keys:
      return False
    return cls.pressed_keys[key]

  @classmethod
  def get_mouse_pos(cls) -> vec2:
    return cls.mouse_pos
    