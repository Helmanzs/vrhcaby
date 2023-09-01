import pygame


class Gameboard:
    screen_width = 1280
    screen_height = 720
    base_margin = 30
    box_color = (171, 117, 46)
    surface_color = (247, 236, 200)

    def __init__(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(self.box_color)
        self.game_over = False
        self.tiles = []

    def paint(self):
        for tile in self.tiles:
            tile.paint(self.screen, self.screen_height)
