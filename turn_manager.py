from player import Player
from dice import Dice
from typing import List
from tile import Tile
from stone import Stone


class TurnManager:
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.available_dices: List[Dice] = []
        self.game_started = False
        self.selected_stone = None
        self.selected_tile = None
        self.current_player = None
        self.possible_moves: List[Tile] = []
        self.highlighted_stones: List[Stone] = []

    def roll_for_turn(self, players: List[Player], dices: List[Dice]) -> Player:
        for dice in dices:
            dice.roll_dice()

        if dices[0].roll > dices[1].roll:
            self.current_player = players[0]
        else:
            self.current_player = players[1]
        self.game_started = True

    def highlight_possible_stones(self, player: Player, tiles: List[Tile]):
        filtered_tiles: List[Tile] = []
        for tile in tiles:
            if tile.currentPlayerOwner == player:
                filtered_tiles.append(tile)

        for tile in filtered_tiles:
            tile.get_last_stone().is_highlighted = True
            self.highlighted_stones.append(tile.get_last_stone())

    def highlight_moves(self, tiles: List[Tile]):
        movable_tiles: List[Tile] = self.get_movable_tiles(tiles)

        for dice in self.available_dices:
            index = self.get_safe_index(tiles.index(self.selected_tile), dice.roll)
            if index is not None:
                if tiles[index] in movable_tiles:
                    self.possible_moves.append(tiles[index])
                    index = None

        for tile in self.possible_moves:
            tile.is_highlighted = True

    def get_safe_index(self, current_index: int, roll: int) -> int:
        next_index = current_index + (roll * (-1 if self.current_player == self.players[1] else 1))
        if next_index >= 24 or next_index < 0:
            return None
        return next_index

    def get_movable_tiles(self, tiles: List[Tile]) -> List[Tile]:
        movable_tiles: List[Tile] = []
        indexes = []

        if self.players[0] == self.current_player:
            indexes = tiles[tiles.index(self.selected_tile) + 1 :]
        else:
            indexes = tiles[0 : tiles.index(self.selected_tile)]

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
