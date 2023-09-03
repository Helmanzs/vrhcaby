import pygame
from stone import Stone
from typing import List


class Tile:
    TILE_WIDTH = 85
    HIGHLIGHT_COLOR = (255, 0, 0)
    BORDER_WIDTH = 3

    def __init__(self, x_pos: int, y_pos: int, color: pygame.Color, inverted: bool):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.inverted = inverted
        self.stones: List[Stone] = []
        self.surface_height = 0
        self.collider = None
        self.currentPlayerOwner = None
        self.is_highlighted = False

    def add_stone(self, stone: Stone):
        self.stones.append(stone)
        self.currentPlayerOwner = stone.player

    def get_last_stone(self):
        if len(self.stones) != 0:
            return self.stones[-1]
        return None

    def paint(self, surface: pygame.surface, surface_height: int):
        self.surface_height = surface_height
        self.collider = pygame.draw.polygon(
            surface,
            self.color,
            [
                [self.x_pos, self.y_pos],
                [self.x_pos + self.TILE_WIDTH, self.y_pos],
                [
                    (self.x_pos + (self.TILE_WIDTH // 2)),
                    self.y_pos + ((self.surface_height // 3) * (-1 if self.inverted else 1)),
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
        if self.is_highlighted:
            self.highlight(surface)

    def highlight(self, surface: pygame.surface):
        pygame.draw.polygon(
            surface,
            self.HIGHLIGHT_COLOR,
            [
                [self.x_pos, self.y_pos],
                [self.x_pos + self.TILE_WIDTH, self.y_pos],
                [
                    (self.x_pos + (self.TILE_WIDTH // 2)),
                    self.y_pos + ((self.surface_height // 3) * (-1 if self.inverted else 1)),
                ],
            ],
            width=self.BORDER_WIDTH * 2,
        )
