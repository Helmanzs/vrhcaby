import pygame
from player import Player


class Stone:
    STONE_RADIUS = 25
    HIGHLIGHT_COLOR = (255, 0, 0)
    BORDER_WIDTH = 4

    def __init__(self, player: Player):
        self.player = player
        self.color = player.color
        self.x_pos = 0
        self.y_pos = 0
        self.is_highlighted = False

    def paint(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        pygame.draw.circle(surface, self.color, (self.x_pos, self.y_pos), self.STONE_RADIUS)
        if self.is_highlighted:
            self.highlight(surface)

    def paint_home(self, surface: pygame.surface, x_pos: int, y_pos: int):
        pygame.draw.rect(surface, self.color, pygame.Rect(x_pos, y_pos, self.STONE_RADIUS * 2, self.STONE_RADIUS // 2))

    def highlight(self, surface: pygame.surface):
        pygame.draw.circle(
            surface,
            self.HIGHLIGHT_COLOR,
            (self.x_pos, self.y_pos),
            self.STONE_RADIUS + self.BORDER_WIDTH,
            width=self.BORDER_WIDTH,
        )
