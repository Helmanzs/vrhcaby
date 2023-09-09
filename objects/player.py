import pygame


class Player:
    def __init__(self, name: str, color: pygame.Color):
        from objects.bar import Bar

        self._name: str = name
        self._color: pygame.Color = color
        self._home_tile: Bar = None
        self._bar_tile: Bar = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: pygame.Color):
        self._color = value

    @property
    def home_tile(self):
        return self._home_tile

    @home_tile.setter
    def home_tile(self, value):
        self._home_tile = value

    @property
    def bar_tile(self):
        return self._bar_tile

    @bar_tile.setter
    def bar_tile(self, value):
        self._bar_tile = value
