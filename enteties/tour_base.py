import pygame
from config.constants import *
from config.color import *

class Tour:
    def __init__(self, screen, column, row):
        self.screen = screen
        self.column = column
        self.row = row
        self.color = GREEN
        self.text_color = WHITE
        self.health = 1000
        self.damage = 250
        self.attack_speed = 0.5  # Attacks per second
        self.attack_range = TOUR_RANGE
        self.cell_size = CELL_SIZE
        self.font = pygame.font.SysFont(None, 12)

    def draw(self):
        pygame.draw.rect(self.screen, self.color,
                         (self.cell_size * self.column, self.cell_size * self.row, self.cell_size, self.cell_size))

        text = self.font.render(str(self.damage), True, self.text_color)
        text_rect = text.get_rect(center=(int(self.cell_size * self.column)+(self.cell_size//2), int(self.cell_size * self.row)+(self.cell_size//2)))
        self.screen.blit(text, text_rect)

        #draw range around tour
        center_x = self.cell_size * self.column + self.cell_size // 2
        center_y = self.cell_size * self.row + self.cell_size // 2
        pygame.draw.circle(self.screen, GRAY, (center_x, center_y), self.attack_range, 1)