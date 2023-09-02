import pygame
from stone import Stone
from typing import List


class Tile:
    TILE_WIDTH = 85

    def __init__(self, x_pos: int, y_pos: int, color: pygame.Color, inverted: bool):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.inverted = inverted
        self.stones: List[Stone] = []

    def add_stone(self, stone: Stone):
        self.stones.append(stone)

    def paint(self, surface: pygame.surface, surface_height: int):
        pygame.draw.polygon(
            surface,
            self.color,
            [
                [self.x_pos, self.y_pos],
                [self.x_pos + self.TILE_WIDTH, self.y_pos],
                [
                    (self.x_pos + (self.TILE_WIDTH // 2)),
                    self.y_pos + ((surface_height // 3) * (-1 if self.inverted else 1)),
                ],
            ],
        )

        spacing = 2.1 if len(self.stones) < 6 else 2.1 - (0.1 * len(self.stones))
        if spacing < 0:
            spacing = 0.1

        for stone in self.stones:
            x_pos = self.x_pos + (self.TILE_WIDTH // 2)
            y_pos = self.y_pos + ((self.stones.index(stone) + 0.6) * spacing * stone.STONE_RADIUS) * (
                -1 if self.inverted else 1
            )
            stone.paint(
                surface,
                x_pos,
                y_pos,
            )
