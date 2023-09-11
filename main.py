import pygame
from backgammon import Backgammon


successes, failures = pygame.init()
FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)

if __name__ == "__main__":
    game = Backgammon()
    game.run()
