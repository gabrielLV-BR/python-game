from types import ClassMethodDescriptorType
from pygame.constants import *
import pygame
from pygame import Vector2 as vec2

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
    should_quit = False

    mouse_state = {
        "position": vec2(0, 0),
        "pressed": [False, False, False]
    }

    @classmethod
    def poll_events(cls):
        should_quit = False

        for event in pygame.event.get():
            should_quit = should_quit or (event.type == pygame.QUIT)

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key in cls.pressed_keys:
                    cls.pressed_keys[event.key] = (event.type == KEYDOWN)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                cls.mouse_state["pressed"][event.button -
                                           1] = event.type == pygame.MOUSEBUTTONDOWN

        cls.mouse_state["position"] = pygame.mouse.get_pos()

        return should_quit

    @classmethod
    def get_key(cls, key) -> bool:
        if key not in cls.pressed_keys:
            return False
        return cls.pressed_keys[key]

    @classmethod
    def get_mouse_pos(cls) -> vec2:
        return cls.mouse_state["position"]

    @classmethod
    def get_mouse_buttons(cls):
        return cls.mouse_state["pressed"]

    @classmethod
    def should_quit(cls):
        return cls.should_quit
