from player import Player
from dice import Dice
from typing import List
from tile import Tile
from stone import Stone


class TurnManager:
    def __init__(self, players: List[Player], tiles: List[Tile]):
        self.players: List[Player] = players
        self.available_dices: List[Dice] = []
        self.game_started = False
        self.selected_stone = None
        self.selected_tile = None
        self.current_player = None
        self.possible_moves: List[Tile] = []
        self.highlighted_stones: List[Stone] = []
        self.tiles: List[Tile] = tiles

    def roll_for_turn(self, players: List[Player], dices: List[Dice]) -> Player:
        for dice in dices:
            dice.roll_dice()

        if dices[0].roll > dices[1].roll:
            self.current_player = players[0]
        else:
            self.current_player = players[1]
        self.game_started = True

    def new_turn(self, dices: List[Dice]):
        self.available_dices = dices
        for dice in self.available_dices:
            dice.is_faded = False
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def move_stone(self, target_tile: Tile):
        roll = self.calculate_roll(target_tile)

        for dice in self.available_dices:
            if dice.roll == roll:
                self.available_dices.remove(dice)
                dice.is_faded = True
                break

        target_tile.add_stone(self.selected_tile.stones.pop())
        self.clear()

    def calculate_roll(self, tile: Tile):
        target_tile = self.tiles.index(tile)
        source_tile = self.tiles.index(self.selected_tile)

        if target_tile < source_tile:
            return source_tile - target_tile
        else:
            return target_tile - source_tile

    def highlight_possible_stones(self, player: Player):
        filtered_tiles: List[Tile] = []
        for tile in self.tiles:
            if tile.currentPlayerOwner == player:
                filtered_tiles.append(tile)

        for tile in filtered_tiles:
            if len(tile.stones) != 0:
                last_stone = tile.get_last_stone()
                last_stone.is_highlighted = True
                if last_stone not in self.highlighted_stones:
                    self.highlighted_stones.append(last_stone)

    def highlight_moves(self):
        movable_tiles: List[Tile] = self.get_movable_tiles()

        for dice in self.available_dices:
            index = self.get_safe_index(self.tiles.index(self.selected_tile), dice.roll)
            if index is not None:
                if self.tiles[index] in movable_tiles:
                    self.possible_moves.append(self.tiles[index])
                    index = None

        for tile in self.possible_moves:
            tile.is_highlighted = True

    def get_safe_index(self, current_index: int, roll: int) -> int:
        next_index = current_index + (roll * (-1 if self.current_player == self.players[1] else 1))
        if next_index >= 24 or next_index < 0:
            return None
        return next_index

    def get_movable_tiles(self) -> List[Tile]:
        movable_tiles: List[Tile] = []
        indexes = []

        if self.players[0] == self.current_player:
            indexes = self.tiles[self.tiles.index(self.selected_tile) + 1 :]
        else:
            indexes = self.tiles[0 : self.tiles.index(self.selected_tile)]

        for tile in indexes:
            if tile not in movable_tiles:
                if len(tile.stones) <= 1:
                    movable_tiles.append(tile)
                elif tile.currentPlayerOwner is self.current_player:
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
