from pygame import Vector2 as vec2

class Config:
    def __init__(self, title: str, width: int, height: int):
        self.title = title
        self.width = width
        self.height = height

        # Estes dados estão aqui no Config para que sejam facilmente acessadas
        # pelos inimimgos
        self.player_pos = vec2(0, 0)
        self.delta = 0
        self.player_morto = False