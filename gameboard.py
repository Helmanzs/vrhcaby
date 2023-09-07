import pygame
from typing import List
from objects.tile import Tile
from objects.dice import Dice
from objects.player import Player
from objects.bar import Bar
from objects.stone import Stone
from objects.center_bar import Center_Bar


class Gameboard:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    SURFACE_COLOR = (133, 94, 66)
    BAR_COLOR = (34, 24, 18)
    LIGHT_TILE_COLOR = (231, 207, 180)
    DARK_TILE_COLOR = (86, 50, 50)

    def __init__(self, player1: Player, player2: Player):
        self.surface: pygame.Surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.surface.fill(self.SURFACE_COLOR)
        self.game_over = False
        self.tiles: List[Tile] = []
        self.dices: List[Dice] = [Dice(), Dice()]
        self.center_bar: Bar = None
        self.player1: Player = player1
        self.player2: Player = player2
        self.create_tiles()
        self.create_stones()

    def create_tiles(self):
        for y in range(2):
            for x in range(13):
                if x == 6:
                    continue

                color = (
                    self.DARK_TILE_COLOR
                    if (x % 2 == 0 and y == 1) or (x % 2 == 1 and y == 0)
                    else self.LIGHT_TILE_COLOR
                )

                if y == 0:
                    self.tiles.append(Tile((self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 14) * (x + 2), 0), color, False))
                else:
                    self.tiles.append(Tile(((self.SCREEN_WIDTH // 14) * x, self.SCREEN_HEIGHT), color, True))

        self.center_bar = Center_Bar((self.SCREEN_WIDTH // 2 - 40, self.SCREEN_HEIGHT // 2))

        self.player1.home_tile = Bar(
            (self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 17), self.SCREEN_HEIGHT),
            self.player1,
            self.player1.color,
            True,
        )
        self.player2.home_tile = Bar(
            (self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 17), 0),
            self.player2,
            self.player2.color,
            False,
        )

        self.player1.bar_tile = Bar(
            (self.SCREEN_WIDTH // 2 - Bar.TILE_WIDTH * 1.25 + 2, 0),
            self.player1,
            self.player1.color,
            False,
        )
        self.player2.bar_tile = Bar(
            (self.SCREEN_WIDTH // 2 - Bar.TILE_WIDTH * 1.25 + 2, self.SCREEN_HEIGHT),
            self.player2,
            self.player2.color,
            True,
        )

    def create_stones(self):
        positions = [
            (11, self.player1, 5),
            (12, self.player2, 5),
            (18, self.player1, 5),
            (5, self.player2, 5),
            (16, self.player1, 3),
            (7, self.player2, 3),
            (0, self.player1, 2),
            (23, self.player2, 2),
        ]
        for pos, player, count in positions:
            for i in range(count):
                self.tiles[pos].add_stone(Stone(player))

    def paint(self):
        self.surface.fill(self.SURFACE_COLOR)

        for tile in self.tiles:
            tile.paint(self.surface)

        for dice in self.dices:
            dice.paint(
                self.surface,
                (
                    self.SCREEN_WIDTH - self.SCREEN_WIDTH // 3 + (105 * self.dices.index(dice)),
                    self.SCREEN_HEIGHT // 2.4,
                ),
            )

        self.paint_bar(self.SCREEN_WIDTH // 2 - Tile.TILE_WIDTH - 3, 0)
        self.paint_bar(self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 14), 0)

        self.player1.bar_tile.paint(self.surface)
        self.player2.bar_tile.paint(self.surface)

        self.player1.home_tile.paint(self.surface)
        self.player2.home_tile.paint(self.surface)

    def paint_bar(self, x_pos: int, y_pos: int):
        pygame.draw.rect(
            self.surface,
            self.BAR_COLOR,
            pygame.Rect(x_pos, y_pos, Tile.TILE_WIDTH + 6, self.SCREEN_HEIGHT),
        )
