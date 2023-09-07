import pygame
from objects.tile import Tile
from objects.stone import Stone
from objects.player import Player


class Bar(Tile):
    TILE_WIDTH = Stone.STONE_RADIUS * 2 + 10

    def __init__(self, position: tuple[int, int], player: Player, color: pygame.Color, inverted: bool):
        super().__init__(position, color, inverted)
        self._current_player_owner = player

    def add_stone(self, stone: Stone):
        self._stones.append(stone)

    def paint(self, surface: pygame.surface):
        self.__paint_tile(surface)
        self.__paint_stone(surface)

    def __paint_tile(self, surface: pygame.surface):
        pygame.draw.rect(
            surface,
            self._current_player_owner.color,
            pygame.Rect(
                self.position.x,
                0 if self.position.y == 0 else self.position.y - (surface.get_height() // 3),
                self.TILE_WIDTH,
                surface.get_height() // 3,
            ),
            width=self.BORDER_WIDTH,
        )

    def __paint_stone(self, surface: pygame.Surface):
        for stone in self.stones:
            x_pos = self.position.x + 5
            y_pos = self.position.y + (
                (self.stones.index(stone) + 1.2) * (Stone.STONE_RADIUS // 5 * 3) * (-1 if self._inverted else 1)
            )

            stone.paint_stone_in_home(surface, (x_pos, y_pos))
