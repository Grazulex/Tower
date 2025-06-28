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
        self.towers = {}  # Dictionnaire pour stocker les instances de tours avec (row, column) comme clé
        
        for row in range(0, (BOARD_HEIGHT//self.cell_size)):
            self.grid.append([])
            for column in range(0, (BOARD_WIDTH//self.cell_size)):
                self.grid[-1].append(0)


    def add_tower(self, row, column, tower_type):
        # Créer la nouvelle tour
        if tower_type == 1:
            tower = TourNormal(self.screen, column, row)
        elif tower_type == 2:
            tower = TourPower(self.screen, column, row)
        elif tower_type == 3:
            tower = TourSlow(self.screen, column, row)
        else:
            return
        
        # Stocker la tour dans notre dictionnaire
        self.towers[(row, column)] = tower
        self.grid[row][column] = tower_type

    def remove_tower(self, row, column):
        if (row, column) in self.towers:
            del self.towers[(row, column)]
            self.grid[row][column] = 0

    def draw(self, enemies, game_manager):
        # Dessiner la grille de base
        for row in range(0, (BOARD_HEIGHT//self.cell_size)):
            for column in range(0, (BOARD_WIDTH//self.cell_size)):
                if self.grid[row][column] == 0:
                    pygame.draw.rect(self.screen, DARK_GRAY, (self.cell_size*column, self.cell_size*row, self.cell_size, self.cell_size),1)
        
        # Dessiner toutes les tours existantes
        for tower in self.towers.values():
            tower.draw(enemies, game_manager)


    def get_grid(self):
        return self.grid
