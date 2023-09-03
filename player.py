import pygame


class Player:
    def __init__(self, name: str, color: pygame.Color):
        self.name = name
        self.color = color
        self.home_tile = None
        self.bar_tile = None
