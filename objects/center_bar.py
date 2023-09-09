import pygame
from collections import namedtuple
from objects.player import Player
from objects.stone import Stone


class Center_Bar:
    BORDER_WIDTH = 4

    def __init__(self, position: tuple[int, int]):
        self._position: namedtuple = namedtuple("position", ["x", "y"])(position[0], position[1])
        self._stone: Stone = None
        self._collider: pygame.Rect = None
        self._current_player_owner: Player = None

    @property
    def stone(self):
        return self._stone

    @stone.setter
    def stone(self, value: Stone):
        self._stone = value
        self._current_player_owner = value.player if value is not None else None

    def pop_stone(self):
        stone = self._stone
        self.stone = None
        return stone

    @property
    def collider(self):
        return self._collider

    def paint(self, surface: pygame.surface):
        if self.stone is None:
            return

        self._collider = pygame.draw.rect(
            surface,
            self._current_player_owner.color,
            pygame.Rect(self._position.x - 38, self._position.y - 38, 75, 75),
            width=self.BORDER_WIDTH,
        )
        self.stone.paint(surface, self._position)
