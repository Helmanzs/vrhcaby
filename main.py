import pygame
from gameboard import Gameboard
from tile import Tile
from player import Player
from stone import Stone

successes, failures = pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Gameboard = Gameboard()

FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)

Player1 = Player(WHITE)
Player2 = Player(BLACK)

# CREATE TILES
for y in range(2):
    for x in range(13):
        if x == 6:
            continue
        color = (86, 50, 50) if (x % 2 == 0 and y == 1) or (x % 2 == 1 and y == 0) else (231, 207, 180)
        if y == 0:
            tile = Tile(Gameboard.screen_width - (Gameboard.screen_width // 13) * (x + 1), 0, color, False)
            Gameboard.tiles.append(tile)
        else:
            tile = Tile((Gameboard.screen_width // 13) * x, Gameboard.screen_height, color, True)
            Gameboard.tiles.append(tile)

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Gameboard.paint()
    pygame.display.update()
