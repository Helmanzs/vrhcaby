import sys
import pygame
from gameboard import Gameboard
from turn_manager import TurnManager
from objects.player import Player
from tkinter.messagebox import askyesno


class Backgammon:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        self.gameboard = Gameboard(Player("WHITE", self.WHITE), Player("BLACK", self.BLACK))
        self.turn_manager = TurnManager(self.gameboard)
        self.turn_manager._center_bar = self.gameboard.center_bar
        self.game_running = True

    def reset(self):
        self.gameboard = Gameboard(Player("WHITE", self.WHITE), Player("BLACK", self.BLACK))
        self.turn_manager = TurnManager(self.gameboard)
        self.turn_manager._center_bar = self.gameboard.center_bar
        self.game_running = True

    def check_for_winner(self):
        player_won = self.turn_manager.check_for_win()
        if player_won is not None:
            answer = askyesno(title="Confirmation", message=f"{player_won.name} won! \nDo you want to play again?")
            if answer:
                self.reset()
            else:
                pygame.quit()
                sys.exit()

    def run(self):
        mouse_pos = (0, 0)
        while self.game_running:
            self.gameboard.paint()
            self.turn_manager._center_bar.paint(self.gameboard.surface)

            if self.turn_manager.game_started:
                if self.turn_manager.selected_stone is None:
                    if len(self.turn_manager.highlighted_stones) == 0:
                        self.turn_manager.highlight_possible_stones()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.turn_manager.selected_stone is None:
                        if self.gameboard.center_bar.stone is None:
                            for tile in self.gameboard.tiles:
                                if tile.collider.collidepoint(mouse_pos):
                                    if tile.current_player_owner == self.turn_manager.current_player:
                                        if tile not in self.turn_manager.no_longer_possible_tiles:
                                            self.turn_manager.selected_stone = tile.get_stone()
                                            self.turn_manager.selected_tile = tile
                                            self.turn_manager.unhighlight()

                        else:
                            if self.gameboard.center_bar.collider is not None:
                                if self.gameboard.center_bar.collider.collidepoint(mouse_pos):
                                    if tile not in self.turn_manager.no_longer_possible_tiles:
                                        self.turn_manager.selected_stone = self.gameboard.center_bar.stone
                                        self.turn_manager.selected_tile = self.gameboard.center_bar
                                        self.turn_manager.unhighlight()

                        if self.turn_manager.selected_stone is not None:
                            self.turn_manager.highlight_moves()

                    else:
                        for tile in self.turn_manager.possible_moves:
                            if tile.collider.collidepoint(mouse_pos):
                                self.turn_manager.move_stone(tile)
                                break

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if self.turn_manager.selected_tile is not None:
                        if not self.turn_manager.possible_moves:
                            self.turn_manager.no_longer_possible_tiles.append(self.turn_manager.selected_tile)

                    self.turn_manager.clear()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    mouse_pos = pygame.mouse.get_pos()
                    for dice in self.gameboard.dices:
                        if dice.collider.collidepoint(mouse_pos):
                            dice.roll_dice()

            if len(self.turn_manager.available_dices) == 0:
                self.turn_manager.new_turn(self.gameboard.dices.copy())

            self.check_for_winner()

            pygame.display.update()

            if not self.turn_manager.game_started:
                for dice in self.gameboard.dices:
                    self.gameboard.paint()
                    pygame.display.update()
                    event = pygame.event.wait()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.turn_manager.roll_for_turn(self.gameboard.dices)
