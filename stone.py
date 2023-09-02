import pygame
from player import Player


class Stone:
    STONE_RADIUS = 25

    def __init__(self, player: Player):
        self.player = player
        self.color = player.color

    def paint(self, surface: pygame.surface, x_pos: int, y_pos: int):
        pygame.draw.circle(surface, self.color, (x_pos, y_pos), self.STONE_RADIUS)

    def paint_home(self, surface: pygame.surface, x_pos: int, y_pos: int):
        pygame.draw.rect(surface, self.color, pygame.Rect(x_pos, y_pos, self.STONE_RADIUS * 2, self.STONE_RADIUS // 2))
