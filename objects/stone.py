import pygame
from objects.player import Player
from collections import namedtuple


class Stone:
    STONE_RADIUS = 25
    HIGHLIGHT_COLOR = (255, 0, 0)
    BORDER_WIDTH = 4

    def __init__(self, player: Player):
        self._collider: pygame.Circle = None
        self._player: Player = player
        self._color: pygame.Color = player.color
        self._position: namedtuple = namedtuple("position", ["x", "y"])(0, 0)
        self._is_highlighted: bool = False

    @property
    def collider(self):
        return self._collider

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value: Player):
        self._player = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: pygame.Color):
        self._color = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]):
        self._position = namedtuple("position", ["x", "y"])(*value)

    @property
    def is_highlighted(self):
        return self._is_highlighted

    @is_highlighted.setter
    def is_highlighted(self, value: bool):
        self._is_highlighted = value

    def paint(self, surface: pygame.surface, position: tuple[int, int]):
        self.position = position

        self._collider = pygame.draw.circle(surface, self.color, (self.position.x, self.position.y), self.STONE_RADIUS)
        if self.is_highlighted:
            self.__highlight(surface)

    def paint_stone_in_home(self, surface: pygame.surface, position: tuple[int, int]):
        self.position = position

        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(self.position.x, self.position.y, self.STONE_RADIUS * 2, self.STONE_RADIUS // 2),
        )

    def __highlight(self, surface: pygame.surface):
        pygame.draw.circle(
            surface,
            self.HIGHLIGHT_COLOR,
            (self.position.x, self.position.y),
            self.STONE_RADIUS + self.BORDER_WIDTH - 1,
            width=self.BORDER_WIDTH,
        )
