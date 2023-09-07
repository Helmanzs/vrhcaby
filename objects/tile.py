import pygame
from typing import List
from collections import namedtuple
from objects.stone import Stone
from objects.player import Player


class Tile:
    TILE_WIDTH = 85
    BORDER_WIDTH = 3
    HIGHLIGHT_COLOR = (255, 0, 0)

    def __init__(self, position: tuple[int, int], color: pygame.Color, inverted: bool):
        self._color: pygame.Color = color
        self._position: namedtuple = namedtuple("position", ["x", "y"])(position[0], position[1])
        self._stones: List[Stone] = []
        self._collider: pygame.Polygon = None
        self._current_player_owner: Player = None
        self._is_highlighted: bool = False
        self._inverted: bool = inverted

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]):
        self._position = namedtuple("position", ["x", "y"])(*value)

    @property
    def collider(self):
        return self._collider

    @property
    def stone_collider(self):
        return self.get_stone().collider

    @property
    def stones(self):
        return self._stones

    @property
    def current_player_owner(self):
        return self._current_player_owner

    @property
    def is_highlighted(self):
        return self._is_highlighted

    @is_highlighted.setter
    def is_highlighted(self, value: bool):
        self._is_highlighted = value

    def add_stone(self, stone: Stone):
        self._stones.append(stone)
        self._current_player_owner = stone._player

    def get_stone(self):
        if len(self.stones) != 0:
            return self.stones[-1]
        return None

    def pop_stone(self, index: int = -1):
        if len(self.stones) != 0:
            return self.stones.pop(index)
        return None

    def paint(self, surface: pygame.surface):
        self.__paint_tile(surface)
        self.__paint_stone(surface)

    def __paint_tile(self, surface: pygame.surface):
        self._collider = pygame.draw.polygon(
            surface,
            self._color,
            [
                [self.position.x, self.position.y],
                [self.position.x + self.TILE_WIDTH, self.position.y],
                [
                    (self.position.x + (self.TILE_WIDTH // 2)),
                    self.position.y + ((surface.get_height() // 3) * (-1 if self._inverted else 1)),
                ],
            ],
        )
        if self.is_highlighted:
            self.__highlight(surface)

    def __paint_stone(self, surface: pygame.Surface):
        spacing = 2.1 if len(self.stones) < 6 else 2.1 - (0.1 * len(self.stones))
        if spacing < 0:
            spacing = 0.1

        for stone in self.stones:
            x_pos = self.position.x + (self.TILE_WIDTH // 2)
            y_pos = self.position.y + ((self.stones.index(stone) + 0.6) * spacing * stone.STONE_RADIUS) * (
                -1 if self._inverted else 1
            )
            stone.paint(surface, (x_pos, y_pos))

    def __highlight(self, surface: pygame.surface):
        pygame.draw.polygon(
            surface,
            self.HIGHLIGHT_COLOR,
            [
                [self.position.x, self.position.y],
                [self.position.x + self.TILE_WIDTH, self.position.y],
                [
                    (self.position.x + (self.TILE_WIDTH // 2)),
                    self.position.y + ((surface.get_height() // 3) * (-1 if self._inverted else 1)),
                ],
            ],
            width=self.BORDER_WIDTH * 2,
        )
