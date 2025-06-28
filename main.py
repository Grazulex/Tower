import pygame
from sys import exit
from config.constants import WINDOW_WIDTH,WINDOW_HEIGHT, TITLE
from design.grid import draw_grid

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

draw_grid(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)


