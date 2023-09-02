import pygame
import random


class Dice:
    FILL = (242, 238, 203)
    BORDER = (0, 0, 0)
    BLACK = (0, 0, 0)
    DIM = 98
    CIRCLE_DIM = DIM // 8

    SHIFT_UP = DIM // 4
    SHIFT_RIGHT = DIM // 4
    SHIFT_LEFT = DIM - DIM // 4
    SHIFT_DOWN = DIM - DIM // 4
    MIDDLE = DIM // 2

    def __init__(self):
        self._firstRoll = None
        self._secondRoll = None

    def roll(self) -> tuple[int, int]:
        self._firstRoll = random.randint(1, 6)
        self._secondRoll = random.randint(1, 6)
        return (self._firstRoll, self._secondRoll)

    def paint(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.paintDICE(surface, x_pos, y_pos, self._firstRoll)
        self.paintDICE(surface, x_pos + 110, y_pos, self._secondRoll)

    def paintDICE(self, surface: pygame.surface, x_pos: int, y_pos: int, roll: int):
        pygame.draw.rect(surface, self.BORDER, pygame.Rect(x_pos - 2, y_pos - 2, self.DIM + 4, self.DIM + 4))
        pygame.draw.rect(surface, self.FILL, pygame.Rect(x_pos, y_pos, self.DIM, self.DIM))
        self.paint_point(surface, x_pos, y_pos, roll)

    def paint_point(self, surface: pygame.surface, x_pos: int, y_pos: int, roll: int):
        if roll == 1:
            self.paint_one(surface, x_pos, y_pos)
        elif roll == 2:
            self.paint_two(surface, x_pos, y_pos)
        elif roll == 3:
            self.paint_three(surface, x_pos, y_pos)
        elif roll == 4:
            self.paint_four(surface, x_pos, y_pos)
        elif roll == 5:
            self.paint_five(surface, x_pos, y_pos)
        elif roll == 6:
            self.paint_six(surface, x_pos, y_pos)

    def paint_one(self, surface: pygame.surface, x_pos: int, y_pos: int):
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.MIDDLE, y_pos + self.MIDDLE), self.CIRCLE_DIM)

    def paint_two(self, surface: pygame.surface, x_pos: int, y_pos: int):
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.SHIFT_LEFT, y_pos + self.SHIFT_UP), self.CIRCLE_DIM)
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.SHIFT_RIGHT, y_pos + self.SHIFT_DOWN), self.CIRCLE_DIM)

    def paint_three(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.paint_one(surface, x_pos, y_pos)
        self.paint_two(surface, x_pos, y_pos)

    def paint_four(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.paint_two(surface, x_pos, y_pos)
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.SHIFT_RIGHT, y_pos + self.SHIFT_UP), self.CIRCLE_DIM)
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.SHIFT_LEFT, y_pos + self.SHIFT_DOWN), self.CIRCLE_DIM)

    def paint_five(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.paint_one(surface, x_pos, y_pos)
        self.paint_four(surface, x_pos, y_pos)

    def paint_six(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.paint_four(surface, x_pos, y_pos)
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.SHIFT_LEFT, y_pos + self.MIDDLE), self.CIRCLE_DIM)
        pygame.draw.circle(surface, self.BLACK, (x_pos + self.SHIFT_RIGHT, y_pos + self.MIDDLE), self.CIRCLE_DIM)
