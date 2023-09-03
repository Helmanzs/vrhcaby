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

players: List[Player] = [Player("WHITE", WHITE), Player("BLACK", BLACK)]
turn_manager = TurnManager(players)
dices: List[Dice] = [Dice(), Dice()]

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
]
for pos, player, count in positions:
    for i in range(count):
        gameboard.tiles[pos].add_stone(Stone(player))

mouse_pos = None
running = True
while running:
    gameboard.paint()

    if turn_manager.game_started and turn_manager.selected_stone is None:
        turn_manager.highlight_possible_stones(turn_manager.current_player, gameboard.tiles)

        for tile in turn_manager.possible_moves:
            tile.is_highlighted = False
        turn_manager.possible_moves = []

    for dice in dices:
        dice.paint(
            gameboard.surface,
            gameboard.SCREEN_WIDTH - gameboard.SCREEN_WIDTH // 3 + (105 * dices.index(dice)),
            gameboard.SCREEN_HEIGHT // 2.4,
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if turn_manager.selected_stone is None:
                for tile in gameboard.tiles:
                    if tile.collider.collidepoint(mouse_pos):
                        if tile.currentPlayerOwner == turn_manager.current_player:
                            turn_manager.selected_stone = tile.get_last_stone()
                            turn_manager.selected_tile = tile if turn_manager.selected_stone is not None else None
                            turn_manager.unhighlight()

                if turn_manager.selected_stone is not None:
                    turn_manager.highlight_moves(dices, gameboard.tiles)
            else:
                for tile in turn_manager.possible_moves:
                    if tile.collider.collidepoint(mouse_pos):
                        tile.add_stone(turn_manager.selected_tile.stones.pop())
                        turn_manager.selected_stone = None
                        turn_manager.selected_tile = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            turn_manager.selected_stone = None
            turn_manager.selected_tile = None

    pygame.display.update()

    while not turn_manager.game_started:
        for dice in dices:
            dice.highlight(gameboard.surface)
            pygame.display.update()
            event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            turn_manager.roll_for_turn(players, dices)
