import pygame
from gameboard import gameboard
from player import Player
from stone import Stone
from dice import Dice
from home_tile import Home_Tile
from bar import Bar
from typing import List
from turn_manager import TurnManager

successes, failures = pygame.init()
FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
gameboard = gameboard()

turn_manager = TurnManager()
dices: List[Dice] = [Dice(), Dice()]
players: List[Player] = [Player("WHITE", WHITE), Player("BLACK", BLACK)]

gameboard.player1_tile = Home_Tile(
    gameboard.SCREEN_WIDTH - (gameboard.SCREEN_WIDTH // 17),
    gameboard.SCREEN_HEIGHT,
    players[0].color,
    players[0],
    True,
)
gameboard.player2_tile = Home_Tile(
    gameboard.SCREEN_WIDTH - (gameboard.SCREEN_WIDTH // 17), 0, players[1].color, players[1], False
)


gameboard.player1_bar = Bar(
    gameboard.SCREEN_WIDTH // 2 - Bar.TILE_WIDTH * 1.25 + 2, 0, players[0].color, players[0], False
)
gameboard.player2_bar = Bar(
    gameboard.SCREEN_WIDTH // 2 - Bar.TILE_WIDTH * 1.25 + 2,
    gameboard.SCREEN_HEIGHT,
    players[1].color,
    players[1],
    True,
)

# CREATE STONES
positions = [
    (11, players[0], 5),
    (12, players[1], 5),
    (18, players[0], 5),
    (5, players[1], 5),
    (16, players[0], 3),
    (7, players[1], 3),
    (0, players[0], 2),
    (23, players[1], 2),
    (22, players[1], 2),
]
for pos, player, count in positions:
    for i in range(count):
        gameboard.tiles[pos].add_stone(Stone(player))


running = True
while running:
    gameboard.paint()

    for dice in dices:
        dice.paint(
            gameboard.surface,
            gameboard.SCREEN_WIDTH - gameboard.SCREEN_WIDTH // 3 + (105 * dices.index(dice)),
            gameboard.SCREEN_HEIGHT // 2.4,
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            turn_manager.highlight_possible_stones(turn_manager.current_player, gameboard.tiles)

    pygame.display.update()

    while not turn_manager.game_started:
        for dice in dices:
            dice.highlight(gameboard.surface)
            pygame.display.update()
            event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            turn_manager.roll_for_turn(players, dices)
