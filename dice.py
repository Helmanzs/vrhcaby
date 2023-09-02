import pygame
import random


class Dice:
    FILL = (242, 238, 203)
    BORDER = (0, 0, 0)
    BLACK = (0, 0, 0)
    HIGHLIGHT_COLOR = (255, 0, 0)
    DIM = 98
    CIRCLE_DIM = DIM // 8

    BORDER_WIDTH = 3
    BORDER_RADIUS = 10

    SHIFT_UP = DIM // 4
    SHIFT_RIGHT = DIM // 4
    SHIFT_LEFT = DIM - DIM // 4
    SHIFT_DOWN = DIM - DIM // 4
    MIDDLE = DIM // 2

    def __init__(self):
        self.roll = 1
        self.x_pos = 0
        self.y_pos = 0

    def roll_dice(self):
        self.roll = random.randint(1, 6)

    def paint(self, surface: pygame.surface, x_pos: int, y_pos: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.paintDICE(surface, self.roll)

    def paintDICE(self, surface: pygame.surface, roll: int):
        pygame.draw.rect(
            surface,
            self.BORDER,
            pygame.Rect(self.x_pos - 2, self.y_pos - 2, self.DIM + 4, self.DIM + 4),
            border_radius=self.BORDER_RADIUS,
            width=self.BORDER_WIDTH,
        )
        pygame.draw.rect(
            surface,
            self.FILL,
            pygame.Rect(self.x_pos, self.y_pos, self.DIM, self.DIM),
            border_radius=self.BORDER_RADIUS,
        )
        self.paint_point(surface, roll)

    def paint_point(self, surface: pygame.surface, roll: int):
        if roll == 1:
            self.paint_one(surface)
        elif roll == 2:
            self.paint_two(surface)
        elif roll == 3:
            self.paint_three(surface)
        elif roll == 4:
            self.paint_four(surface)
        elif roll == 5:
            self.paint_five(surface)
        elif roll == 6:
            self.paint_six(surface)

    def paint_one(
        self,
        surface: pygame.surface,
    ):
        pygame.draw.circle(surface, self.BLACK, (self.x_pos + self.MIDDLE, self.y_pos + self.MIDDLE), self.CIRCLE_DIM)

    def paint_two(self, surface: pygame.surface):
        pygame.draw.circle(
            surface, self.BLACK, (self.x_pos + self.SHIFT_LEFT, self.y_pos + self.SHIFT_UP), self.CIRCLE_DIM
        )
        pygame.draw.circle(
            surface, self.BLACK, (self.x_pos + self.SHIFT_RIGHT, self.y_pos + self.SHIFT_DOWN), self.CIRCLE_DIM
        )

    def paint_three(self, surface: pygame.surface):
        self.paint_one(surface)
        self.paint_two(surface)

    def paint_four(self, surface: pygame.surface):
        self.paint_two(surface)
        pygame.draw.circle(
            surface, self.BLACK, (self.x_pos + self.SHIFT_RIGHT, self.y_pos + self.SHIFT_UP), self.CIRCLE_DIM
        )
        pygame.draw.circle(
            surface, self.BLACK, (self.x_pos + self.SHIFT_LEFT, self.y_pos + self.SHIFT_DOWN), self.CIRCLE_DIM
        )

    def paint_five(self, surface: pygame.surface):
        self.paint_one(surface)
        self.paint_four(surface)

    def paint_six(self, surface: pygame.surface):
        self.paint_four(surface)
        pygame.draw.circle(
            surface, self.BLACK, (self.x_pos + self.SHIFT_LEFT, self.y_pos + self.MIDDLE), self.CIRCLE_DIM
        )
        pygame.draw.circle(
            surface, self.BLACK, (self.x_pos + self.SHIFT_RIGHT, self.y_pos + self.MIDDLE), self.CIRCLE_DIM
        )

    def highlight(self, surface: pygame.surface):
        pygame.draw.rect(
            surface,
            self.HIGHLIGHT_COLOR,
            pygame.Rect(self.x_pos - 2, self.y_pos - 2, self.DIM + 4, self.DIM + 4),
            border_radius=self.BORDER_RADIUS,
            width=self.BORDER_WIDTH,
        )
