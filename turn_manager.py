from typing import List
from gameboard import Gameboard
from objects.player import Player
from objects.dice import Dice
from objects.tile import Tile
from objects.stone import Stone


class TurnManager:
    def __init__(self, gameboard: Gameboard):
        self.gameboard: Gameboard = gameboard
        self.current_player: Player = None
        self.available_dices: List[Dice] = []
        self.selected_stone: Stone = None
        self.selected_tile: Tile = None
        self.possible_moves: List[Tile] = []
        self.highlighted_stones: List[Stone] = []
        self.no_longer_possible_tiles: List[Tile] = []
        self._game_started: bool = False
        self.home_available: bool = False
        self.sloppy_search: bool = False

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
        self.no_longer_possible_tiles = []

        self.available_dices = dices
        for dice in self.available_dices:
            dice.is_faded = False
        self.current_player = (
            self.gameboard.player1 if self.current_player == self.gameboard.player2 else self.gameboard.player2
        )

        if len(self.current_player.bar_tile.stones) != 0:
            self.gameboard.center_bar.stone = self.current_player.bar_tile.pop_stone()

        self.check_for_home_eligibility()

    def check_for_home_eligibility(self):
        tiles: List[Tile] = []
        if self.current_player == self.gameboard.player1:
            tiles = self.gameboard.tiles[18:24]
            tiles.append(self.gameboard.player1.home_tile)
        else:
            tiles = self.gameboard.tiles[0:6]
            tiles.append(self.gameboard.player2.home_tile)

        stone_count = 0
        for tile in tiles:
            stone_count += len(tile.stones)

        if stone_count == 15:
            self.home_available = True

    def move_stone(self, target_tile: Tile):
        if target_tile == self.current_player.home_tile:
            self.remove_dice(self.calculate_home_roll())
        else:
            self.remove_dice(self.calculate_roll(target_tile))

        if len(target_tile.stones) == 1 and target_tile.current_player_owner is not self.current_player:
            stone = target_tile.pop_stone()

            if self.current_player == self.gameboard.player1:
                self.gameboard.player2.bar_tile.add_stone(stone)
            else:
                self.gameboard.player1.bar_tile.add_stone(stone)

        if self.gameboard.center_bar.stone is not None:
            target_tile.add_stone(self.gameboard.center_bar.pop_stone())
        else:
            target_tile.add_stone(self.selected_tile.pop_stone())

        self.clear()

    def remove_dice(self, roll: int):
        removed = False
        for dice in self.available_dices:
            if dice.roll == roll:
                self.available_dices.remove(dice)
                dice.is_faded = True
                removed = True
                break

        if removed is False:
            if self.sloppy_search:
                bigger_roll = 0
                for dice in self.available_dices:
                    if dice.roll > bigger_roll:
                        bigger_roll = dice.roll
                self.remove_dice(bigger_roll)

    def calculate_roll(self, tile: Tile):
        target_tile = self.gameboard.tiles.index(tile)

        if self.gameboard.center_bar.stone is not None:
            source_tile = -1 if self.current_player == self.gameboard.player1 else 24
        else:
            source_tile = self.gameboard.tiles.index(self.selected_tile)

        if target_tile < source_tile:
            return source_tile - target_tile
        else:
            return target_tile - source_tile

    def calculate_home_roll(self):
        target_tile = 24 if self.current_player == self.gameboard.player1 else -1
        source_tile = self.gameboard.tiles.index(self.selected_tile)

        if target_tile < source_tile:
            return source_tile - target_tile
        else:
            return target_tile - source_tile

    def highlight_possible_stones(self):
        if self.gameboard.center_bar.stone is not None:
            self.gameboard.center_bar.stone.is_highlighted = True
            self.highlighted_stones.append(self.gameboard.center_bar.stone)
            return

        filtered_tiles: List[Tile] = []
        for tile in self.gameboard.tiles:
            if tile.current_player_owner == self.current_player:
                filtered_tiles.append(tile)

        for tile in filtered_tiles:
            if tile not in self.no_longer_possible_tiles:
                if len(tile.stones) != 0:
                    last_stone = tile.get_stone()
                    last_stone.is_highlighted = True
                    if last_stone not in self.highlighted_stones:
                        self.highlighted_stones.append(last_stone)

        if not self.highlighted_stones:
            self.new_turn(self.gameboard.dices.copy())
            for dice in self.gameboard.dices:
                dice.roll_dice()

    def highlight_moves(self):
        movable_tiles: List[Tile] = self.get_movable_tiles()

        for dice in self.available_dices:
            index = None
            if self.gameboard.center_bar.stone is not None:
                if self.current_player == self.gameboard.player1:
                    index = self.get_safe_index(-1, dice.roll)
                else:
                    index = self.get_safe_index(24, dice.roll)
            else:
                index = self.get_safe_index(self.gameboard.tiles.index(self.selected_tile), dice.roll)

            if index is not None:
                self.check_for_home_eligibility()
                if (index == -1 or index == 24) and self.home_available:
                    self.home_moves()
                    continue

                if index > -1 and index < 24:
                    if self.gameboard.tiles[index] in movable_tiles:
                        self.possible_moves.append(self.gameboard.tiles[index])

        for tile in self.possible_moves:
            tile.is_highlighted = True

    def home_moves(self):
        home_tile = self.current_player.home_tile
        home_tile.is_highlighted = True
        self.possible_moves.append(home_tile)

    def get_safe_index(self, current_index: int, roll: int) -> int:
        next_index = current_index + (roll * (-1 if self.current_player == self.gameboard.player2 else 1))
        if next_index > 24 or next_index < -1:
            return None
        return next_index

    def get_movable_tiles(self) -> List[Tile]:
        movable_tiles: List[Tile] = []
        indexes: List[Tile] = []

        if self.gameboard.center_bar.stone is not None:
            indexes = self.gameboard.tiles
        else:
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

    def check_for_win(self) -> Player:
        if len(self.gameboard.player1.home_tile.stones) == 1:
            return self.gameboard.player1

        if len(self.gameboard.player2.home_tile.stones) == 1:
            return self.gameboard.player2

        return None

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
        self.home_available = False
        self.sloppy_search = False
