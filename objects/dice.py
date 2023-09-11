import pygame
import random
from collections import namedtuple


class Dice:
    FILL = (242, 238, 203)
    FADED = (160, 156, 121)
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
        self._roll: int = 1
        self._position: namedtuple = None
        self._is_faded: bool = False
        self._is_highlighted: bool = False
        self._collider: pygame.Rect = None
        self._paint_functions: dict[int, callable] = {
            1: self.__paint_one,
            2: self.__paint_two,
            3: self.__paint_three,
            4: self.__paint_four,
            5: self.__paint_five,
            6: self.__paint_six,
        }

    @property
    def roll(self):
        return self._roll

    @property
    def is_faded(self):
        return self.__is_faded

    @is_faded.setter
    def is_faded(self, value: bool):
        self._is_faded = value

    @property
    def is_highlighted(self):
        return self._is_highlighted

    @is_highlighted.setter
    def is_highlighted(self, value: bool):
        self._is_highlighted = value

    @property
    def collider(self):
        return self._collider

    def roll_dice(self) -> int:
        self._roll = random.randint(1, 6)
        return self._roll

    def paint(self, surface: pygame.surface, position: tuple[int, int]):
        self._position = namedtuple("position", ["x", "y"])(*position)
        self.__paint_dice(surface)

    def __paint_dice(self, surface: pygame.surface):
        self._collider = pygame.draw.rect(
            surface,
            self.BORDER,
            pygame.Rect(self._position.x - 2, self._position.y - 2, self.DIM + 4, self.DIM + 4),
            border_radius=self.BORDER_RADIUS,
            width=self.BORDER_WIDTH,
        )

        fill_color = self.FADED if self._is_faded else self.FILL

        pygame.draw.rect(
            surface,
            fill_color,
            pygame.Rect(self._position.x, self._position.y, self.DIM, self.DIM),
            border_radius=self.BORDER_RADIUS,
        )

        self._paint_functions.get(self._roll)(surface)

        if self._is_highlighted:
            self.__highlight(surface)

    def __paint_one(self, surface: pygame.surface):
        pygame.draw.circle(
            surface, self.BLACK, (self._position.x + self.MIDDLE, self._position.y + self.MIDDLE), self.CIRCLE_DIM
        )

    def __paint_two(self, surface: pygame.surface):
        pygame.draw.circle(
            surface,
            self.BLACK,
            (self._position.x + self.SHIFT_LEFT, self._position.y + self.SHIFT_UP),
            self.CIRCLE_DIM,
        )
        pygame.draw.circle(
            surface,
            self.BLACK,
            (self._position.x + self.SHIFT_RIGHT, self._position.y + self.SHIFT_DOWN),
            self.CIRCLE_DIM,
        )

    def __paint_three(self, surface: pygame.surface):
        self.__paint_one(surface)
        self.__paint_two(surface)

    def __paint_four(self, surface: pygame.surface):
        self.__paint_two(surface)
        pygame.draw.circle(
            surface,
            self.BLACK,
            (self._position.x + self.SHIFT_RIGHT, self._position.y + self.SHIFT_UP),
            self.CIRCLE_DIM,
        )
        pygame.draw.circle(
            surface,
            self.BLACK,
            (self._position.x + self.SHIFT_LEFT, self._position.y + self.SHIFT_DOWN),
            self.CIRCLE_DIM,
        )

    def __paint_five(self, surface: pygame.surface):
        self.__paint_one(surface)
        self.__paint_four(surface)

    def __paint_six(self, surface: pygame.surface):
        self.__paint_four(surface)
        pygame.draw.circle(
            surface, self.BLACK, (self._position.x + self.SHIFT_LEFT, self._position.y + self.MIDDLE), self.CIRCLE_DIM
        )
        pygame.draw.circle(
            surface, self.BLACK, (self._position.x + self.SHIFT_RIGHT, self._position.y + self.MIDDLE), self.CIRCLE_DIM
        )

    def __highlight(self, surface: pygame.surface):
        pygame.draw.rect(
            surface,
            self.HIGHLIGHT_COLOR,
            pygame.Rect(self._position.x - 2, self._position.y - 2, self.DIM + 4, self.DIM + 4),
            border_radius=self.BORDER_RADIUS,
            width=self.BORDER_WIDTH,
        )
