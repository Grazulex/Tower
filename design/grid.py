import pygame
from config.color import *
from config.constants import *
from enteties.tour_base import Tour

class Grid:

    def __init__(self, screen):
        self.screen = screen
        self.cell_size = CELL_SIZE
        self.grid_color = WHITE
        self.grid = []
        for row in range(0, (BOARD_HEIGHT//self.cell_size)):
            self.grid.append([])
            for column in range(0, (BOARD_WIDTH//self.cell_size)):
                self.grid[-1].append(0)


    def draw(self):
        for row in range(0, (BOARD_HEIGHT//self.cell_size)):
            for column in range(0, (BOARD_WIDTH//self.cell_size)):
                if self.grid[row][column] == 0:
                    pygame.draw.rect(self.screen, DARK_GRAY, (self.cell_size*column, self.cell_size*row, self.cell_size, self.cell_size),1)
                else:
                    tour = Tour(self.screen, column, row)
                    tour.draw()

    def get_grid(self):
        return self.grid
