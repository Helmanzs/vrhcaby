import pygame
from typing import List
from tile import Tile


class Gameboard:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    BASE_MARGIN = 30
    SURFACE_COLOR = (171, 117, 46)

    def __init__(self):
        self.surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.surface.fill(self.SURFACE_COLOR)
        self.game_over = False
        self.tiles: List[Tile] = []
        self.player1_tile = None
        self.player2_tile = None

    def paint(self):
        for tile in self.tiles:
            tile.paint(self.surface, self.SCREEN_HEIGHT)
        self.player1_tile.paint(self.surface, self.SCREEN_HEIGHT)
        self.player2_tile.paint(self.surface, self.SCREEN_HEIGHT)
