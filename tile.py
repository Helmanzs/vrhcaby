import pygame
from stone import Stone


class Tile:
    def __init__(self, xPos: int, yPos: int, color: pygame.Color, inverted: bool = False):
        self.color = color
        self.xPos = xPos
        self.yPos = yPos
        self.inverted = inverted
        self.stones = []

    def add_stone(self, stone: Stone):
        self.stones.append(stone)

    def paint(self, screen: pygame.surface, height: int):
        pygame.draw.polygon(
            screen,
            self.color,
            [
                [self.xPos, self.yPos],
                [self.xPos + 98, self.yPos],
                [(self.xPos + (98 // 2)), self.yPos + ((height // 3) * (-1 if self.inverted else 1))],
            ],
        )
        for stone in self.stones:
            stone.paint(
                screen,
                (self.xPos + (98 // 2)),
                self.yPos + ((self.stones.index(stone) + 0.6) * (2.1 * stone.radius)) * (-1 if self.inverted else 1),
            )
