import pygame
from tile import Tile
from typing import List
from stone import Stone
from player import Player


class Bar(Tile):
    TILE_WIDTH = Stone.STONE_RADIUS * 2 + 10
    BORDER_WIDTH = 3

    def __init__(self, x_pos: int, y_pos: int, color: pygame.Color, player: Player, inverted: bool):
        super().__init__(x_pos, y_pos, color, inverted)
        self.player = player
        self.stones: List[Stone] = []

    def paint(self, surface: pygame.surface, surface_height: int):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(
                self.x_pos,
                0 if self.y_pos == 0 else self.y_pos - (surface_height // 3),
                self.TILE_WIDTH,
                surface_height // 3,
            ),
            width=self.BORDER_WIDTH,
        )

        for stone in self.stones:
            x_pos = self.x_pos + 5
            y_pos = self.y_pos + (
                (self.stones.index(stone) + 1.2) * (Stone.STONE_RADIUS // 5 * 3) * (-1 if self.inverted else 1)
            )

            stone.paint_home(surface, x_pos, y_pos)
