from player import Player
from dice import Dice
from typing import List
from turn import Turn
from tile import Tile
from stone import Stone


class TurnManager:
    def __init__(self):
        self.game_started = False
        self.current_player = None
        self.possible_turns: List[Turn]
        self.turn_history: List[Turn]
        self.turn = None

    def roll_for_turn(self, players: List[Player], dices: List[Dice]) -> Player:
        for dice in dices:
            dice.roll_dice()

        if dices[0].roll > dices[1].roll:
            self.current_player = players[0]
        else:
            self.current_player = players[1]
        self.game_started = True
        self.turn = Turn()

    def highlight_possible_stones(self, player: Player, tiles: List[Tile]):
        filtered_tiles: List[Tile] = []
        for tile in tiles:
            if tile.currentPlayerOwner == player:
                filtered_tiles.append(tile)
        stones: List[Stone] = []
        for tile in filtered_tiles:
            stones.append(tile.get_last_stone())
        for stone in stones:
            stone.is_highlighted = True
