import pygame
from config.color import *
from config.constants import *
from enteties.tours.tour_normal import TourNormal
from enteties.tours.tour_power import TourPower
from enteties.tours.tour_slow import TourSlow



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


    def draw(self, enemies):
        for row in range(0, (BOARD_HEIGHT//self.cell_size)):
            for column in range(0, (BOARD_WIDTH//self.cell_size)):
                if self.grid[row][column] == 0:
                    pygame.draw.rect(self.screen, DARK_GRAY, (self.cell_size*column, self.cell_size*row, self.cell_size, self.cell_size),1)
                elif self.grid[row][column]==1:
                        tour = TourNormal(self.screen, column, row)
                        tour.draw(enemies)
                elif self.grid[row][column]==2:
                        tour = TourPower(self.screen, column, row)
                        tour.draw(enemies)
                elif self.grid[row][column]==3:
                        tour = TourSlow(self.screen, column, row)
                        tour.draw(enemies)


    def get_grid(self):
        return self.grid
