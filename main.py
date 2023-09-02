import pygame
from gameboard import Gameboard
from tile import Tile
from player import Player
from stone import Stone
from dice import Dice
from home_tile import Home_Tile
from bar import Bar

successes, failures = pygame.init()
FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Gameboard = Gameboard()

Dice = Dice()

Player1 = Player(WHITE)
Player2 = Player(BLACK)

# CREATE TILES
for y in range(2):
    for x in range(13):
        if x == 6:
            continue
        color = (86, 50, 50) if (x % 2 == 0 and y == 1) or (x % 2 == 1 and y == 0) else (231, 207, 180)
        if y == 0:
            tile = Tile(Gameboard.SCREEN_WIDTH - (Gameboard.SCREEN_WIDTH // 14) * (x + 2), 0, color, False)
            Gameboard.tiles.append(tile)
        else:
            tile = Tile((Gameboard.SCREEN_WIDTH // 14) * x, Gameboard.SCREEN_HEIGHT, color, True)
            Gameboard.tiles.append(tile)

Gameboard.player1_tile = Home_Tile(
    Gameboard.SCREEN_WIDTH - (Gameboard.SCREEN_WIDTH // 17), 0, Player1.color, Player1, False
)

Gameboard.player2_tile = Home_Tile(
    Gameboard.SCREEN_WIDTH - (Gameboard.SCREEN_WIDTH // 17), Gameboard.SCREEN_HEIGHT, BLACK, Player2.color, True
)

Gameboard.player1_bar = Bar(Gameboard.SCREEN_WIDTH // 2 - Bar.TILE_WIDTH * 1.25 + 2, 0, Player1.color, Player1, False)
Gameboard.player2_bar = Bar(
    Gameboard.SCREEN_WIDTH // 2 - Bar.TILE_WIDTH * 1.25 + 2, Gameboard.SCREEN_HEIGHT, Player2.color, Player2, True
)

# CREATE STONES
positions = [
    (11, Player1, 5),
    (12, Player2, 5),
    (18, Player1, 5),
    (5, Player2, 5),
    (16, Player1, 3),
    (7, Player2, 3),
    (0, Player1, 2),
    (23, Player2, 2),
]
for pos, player, count in positions:
    for i in range(count):
        Gameboard.tiles[pos].add_stone(Stone(player))

running = True
while running:
    Gameboard.paint()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Dice.roll()
            Dice.paint(
                Gameboard.surface,
                Gameboard.SCREEN_WIDTH - Gameboard.SCREEN_WIDTH // 6,
                Gameboard.SCREEN_HEIGHT // 2.5,
            )

    pygame.display.update()
