from typing import List
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from entities.enemy_base import EnemyBase
from config.color import *
from config.constants import *
from entities.tours.tour_normal import TourNormal
from entities.tours.tour_power import TourPower
from entities.tours.tour_slow import TourSlow

class Grid:
    """
    Represents the game grid where towers are placed.

    Attributes:
        screen (pygame.Surface): The game screen where the grid is drawn.
        cell_size (int): The size of each cell in the grid.
        grid_color (tuple): The color of the grid lines.
        grid (list): A 2D list representing the grid cells.
        towers (dict): A dictionary mapping grid positions to tower instances.
    """

    def __init__(self, screen: Surface):
        """
        Initializes the Grid instance.

        Args:
            screen (pygame.Surface): The game screen where the grid is drawn.
        """
        self.screen = screen
        self.cell_size = CELL_SIZE
        self.grid_color = WHITE
        self.grid = []
        self.towers = {}

        # Create the grid as a 2D list
        for row in range(0, (BOARD_HEIGHT // self.cell_size)):
            self.grid.append([])
            for column in range(0, (BOARD_WIDTH // self.cell_size)):
                self.grid[-1].append(0)

    def add_tower(self, row: int, column: int, tower_type: int) -> None:
        """
        Adds a tower to the grid.

        Args:
            row (int): The row index of the grid cell.
            column (int): The column index of the grid cell.
            tower_type (int): The type of tower to add (1 for normal, 2 for power, 3 for slow).
        """
        if tower_type == 1:
            tower = TourNormal(self.screen, column, row)
        elif tower_type == 2:
            tower = TourPower(self.screen, column, row)
        elif tower_type == 3:
            tower = TourSlow(self.screen, column, row)
        else:
            return

        self.towers[(row, column)] = tower
        self.grid[row][column] = tower_type

    def remove_tower(self, row: int, column: int) -> None:
        """
        Removes a tower from the grid.

        Args:
            row (int): The row index of the grid cell.
            column (int): The column index of the grid cell.
        """
        if (row, column) in self.towers:
            del self.towers[(row, column)]
            self.grid[row][column] = 0

    def draw(self, enemies: List[EnemyBase], game_manager: GameManager) -> None:
        """
        Draws the grid and towers on the screen.

        Args:
            enemies (list): The list of active enemies in the game.
            game_manager (GameManager): The game manager handling game state.
        """
        # Draw the grid cells
        for row in range(0, (BOARD_HEIGHT // self.cell_size)):
            for column in range(0, (BOARD_WIDTH // self.cell_size)):
                if self.grid[row][column] == 0:
                    pygame.draw.rect(
                        self.screen, DARK_GRAY,
                        (self.cell_size * column, self.cell_size * row, self.cell_size, self.cell_size), 1
                    )

        # Draw the towers
        for tower in self.towers.values():
            tower.draw(enemies, game_manager)

    def get_grid(self) -> List[List[int]]:
        """
        Gets the current state of the grid.

        Returns:
            list: A 2D list representing the grid cells.
        """
        return self.grid