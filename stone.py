import pygame
from player import Player


class Stone:
    radius = 25

    def __init__(self, player: Player):
        self.player = player
        self.color = player.color

    def paint(self, screen: pygame.surface, xPos: int, yPos: int):
        pygame.draw.circle(screen, self.color, (xPos, yPos), self.radius)
