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
        self.damage = 50
        self.attack_speed = 1.0  # Attacks per second
        #self.attack_range = TOUR_RANGE
        self.cell_size = CELL_SIZE

    def draw(self):
        pygame.draw.rect(self.screen, self.color,
                         (self.cell_size * self.column, self.cell_size * self.row, self.cell_size, self.cell_size))