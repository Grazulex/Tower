import pygame
from config.color import WHITE
from config.constants import BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE

def draw_grid(screen):
    for x in range(0, BOARD_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, BOARD_HEIGHT))
    for y in range(0, BOARD_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (BOARD_WIDTH, y))
