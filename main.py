import pygame

width = 300
height = 200
screen = pygame.display.set_mode((width, height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
