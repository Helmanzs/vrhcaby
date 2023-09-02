import pygame
from typing import List
from tile import Tile


class Gameboard:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    SURFACE_COLOR = (133, 94, 66)
    BAR_COLOR = (34, 24, 18)

    def __init__(self):
        self.surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.surface.fill(self.SURFACE_COLOR)
        self.game_over = False
        self.tiles: List[Tile] = []
        self.player1_tile = None
        self.player2_tile = None
        self.player1_bar = None
        self.player2_bar = None

    def paint(self):
        for tile in self.tiles:
            tile.paint(self.surface, self.SCREEN_HEIGHT)

        self.paint_bar(self.SCREEN_WIDTH // 2 - Tile.TILE_WIDTH - 3, 0)
        self.paint_bar(self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 14), 0)

        self.player1_bar.paint(self.surface, self.SCREEN_HEIGHT)
        self.player2_bar.paint(self.surface, self.SCREEN_HEIGHT)

        self.player1_tile.paint(self.surface, self.SCREEN_HEIGHT)
        self.player2_tile.paint(self.surface, self.SCREEN_HEIGHT)

    def paint_bar(self, x_pos: int, y_pos: int):
        pygame.draw.rect(
            self.surface,
            self.BAR_COLOR,
            pygame.Rect(x_pos, y_pos, Tile.TILE_WIDTH + 6, self.SCREEN_HEIGHT),
        )
