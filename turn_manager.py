from typing import List
from gameboard import Gameboard
from objects.player import Player
from objects.dice import Dice
from objects.tile import Tile
from objects.stone import Stone


class TurnManager:
    def __init__(self, gameboard: Gameboard):
        self.gameboard = gameboard
        self.current_player: Player = None
        self.available_dices: List[Dice] = []
        self.selected_stone: Stone = None
        self.selected_tile: Tile = None
        self.possible_moves: List[Tile] = []
        self.highlighted_stones: List[Stone] = []
        self.center_bar = None
        self._game_started: bool = False

    @property
    def game_started(self):
        return self._game_started

    @game_started.setter
    def game_started(self, value: bool):
        self._game_started = value
        for dice in self.available_dices:
            dice.is_highlighted = not value

    def roll_for_turn(self, dices: List[Dice]):
        for dice in dices:
            dice.roll_dice()

        if dices[0].roll > dices[1].roll:
            self.current_player = self.gameboard.player1
        else:
            self.current_player = self.gameboard.player2
        self.game_started = True

    def new_turn(self, dices: List[Dice]):
        self.available_dices = dices
        for dice in self.available_dices:
            dice.is_faded = False
        self.current_player = (
            self.gameboard.player1 if self.current_player == self.gameboard.player2 else self.gameboard.player2
        )

    def move_stone(self, target_tile: Tile):
        roll = self.calculate_roll(target_tile)

        for dice in self.available_dices:
            if dice.roll == roll:
                self.available_dices.remove(dice)
                dice.is_faded = True
                break

        if len(target_tile.stones) == 1 and target_tile.current_player_owner is not self.current_player:
            stone = target_tile.pop_stone()

            if self.current_player == self.gameboard.player1:
                self.gameboard.player2.bar_tile.add_stone(stone)
            else:
                self.gameboard.player1.bar_tile.add_stone(stone)

            target_tile.add_stone(self.selected_tile.pop_stone())

        else:
            target_tile.add_stone(self.selected_tile.pop_stone())

        self.clear()

    def calculate_roll(self, tile: Tile):
        target_tile = self.gameboard.tiles.index(tile)
        source_tile = self.gameboard.tiles.index(self.selected_tile)

        if target_tile < source_tile:
            return source_tile - target_tile
        else:
            return target_tile - source_tile

    def highlight_possible_stones(self):
        filtered_tiles: List[Tile] = []
        for tile in self.gameboard.tiles:
            if tile.current_player_owner == self.current_player:
                filtered_tiles.append(tile)

        for tile in filtered_tiles:
            if len(tile.stones) != 0:
                last_stone = tile.get_stone()
                last_stone.is_highlighted = True
                if last_stone not in self.highlighted_stones:
                    self.highlighted_stones.append(last_stone)

    def highlight_moves(self):
        movable_tiles: List[Tile] = self.get_movable_tiles()

        for dice in self.available_dices:
            index = self.get_safe_index(self.gameboard.tiles.index(self.selected_tile), dice.roll)
            if index is not None:
                if self.gameboard.tiles[index] in movable_tiles:
                    self.possible_moves.append(self.gameboard.tiles[index])
                    index = None

        for tile in self.possible_moves:
            tile.is_highlighted = True

    def get_safe_index(self, current_index: int, roll: int) -> int:
        next_index = current_index + (roll * (-1 if self.current_player == self.gameboard.player2 else 1))
        if next_index >= 24 or next_index < 0:
            return None
        return next_index

    def get_movable_tiles(self) -> List[Tile]:
        indexes: List[int] = []
        movable_tiles: List[Tile] = []
        if self.gameboard.player1 == self.current_player:
            indexes = self.gameboard.tiles[self.gameboard.tiles.index(self.selected_tile) + 1 :]
        else:
            indexes = self.gameboard.tiles[0 : self.gameboard.tiles.index(self.selected_tile)]

        for tile in indexes:
            if tile not in movable_tiles:
                if len(tile.stones) <= 1:
                    movable_tiles.append(tile)
                elif tile.current_player_owner is self.current_player:
                    movable_tiles.append(tile)

        return movable_tiles

    def unhighlight(self):
        for stone in self.highlighted_stones:
            if self.selected_stone is stone:
                continue
            stone.is_highlighted = False

    def clear(self):
        for tile in self.possible_moves:
            tile.is_highlighted = False
        self.possible_moves = []

        for stone in self.highlighted_stones:
            stone.is_highlighted = False
        self.highlighted_stones = []

        self.selected_stone = None
        self.selected_tile = None
