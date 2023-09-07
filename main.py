import pygame
from gameboard import Gameboard
from objects.player import Player
from turn_manager import TurnManager

successes, failures = pygame.init()
FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
gameboard = Gameboard(Player("WHITE", WHITE), Player("BLACK", BLACK))
turn_manager = TurnManager(gameboard)
turn_manager.center_bar = gameboard.center_bar

mouse_pos = (0, 0)
running = True
while running:
    gameboard.paint()
    turn_manager.center_bar.paint(gameboard.surface)

    if turn_manager.game_started and turn_manager.selected_stone is None and len(turn_manager.highlighted_stones) == 0:
        turn_manager.highlight_possible_stones()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if turn_manager.selected_stone is None:
                for tile in gameboard.tiles:
                    if tile.collider.collidepoint(mouse_pos):
                        if tile.current_player_owner == turn_manager.current_player:
                            turn_manager.selected_stone = tile.get_stone()
                            turn_manager.selected_tile = tile if turn_manager.selected_stone is not None else None
                            turn_manager.unhighlight()
                        else:
                            break

                if turn_manager.selected_stone is not None:
                    turn_manager.highlight_moves()
            else:
                for tile in turn_manager.possible_moves:
                    if tile.collider.collidepoint(mouse_pos):
                        turn_manager.move_stone(tile)
                        break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for tile in turn_manager.possible_moves:
                tile.is_highlighted = False
            turn_manager.possible_moves = []
            turn_manager.clear()

    if len(turn_manager.available_dices) == 0:
        turn_manager.new_turn(gameboard.dices.copy())
        for dice in gameboard.dices:
            dice.roll_dice()

    pygame.display.update()

    while not turn_manager.game_started:
        for dice in gameboard.dices:
            pygame.display.update()
            event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            turn_manager.roll_for_turn(gameboard.dices)
