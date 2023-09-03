import pygame
from bar import Bar
from player import Player


class Center_Bar(Bar):
    def __init__(self, x_pos: int, y_pos: int, color: pygame.Color, player: Player, inverted: bool):
        super().__init__(x_pos, y_pos, color, player, inverted)

    def paint(self, surface: pygame.surface):
        if len(self.stones) != 0:
            self.collider = pygame.draw.rect(
                surface,
                self.currentPlayerOwner.color,
                pygame.Rect(self.x_pos - 38, self.y_pos - 38, 75, 75),
                width=self.BORDER_WIDTH,
            )
            self.stones[0].paint(surface, self.x_pos, self.y_pos)

            if self.stones[0].is_highlighted:
                self.stones[0].highlight(surface)
