"""
Tests for the Grid class.
"""

import pytest
import pygame
from tower.design.grid import Grid
from tower.config.constants import CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT


@pytest.fixture
def test_screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))


@pytest.fixture
def test_grid(test_screen):
    """Create a test grid instance."""
    return Grid(test_screen)


def test_grid_initialization(test_grid):
    """Test if grid initializes with correct dimensions."""
    grid_data = test_grid.get_grid()

    expected_rows = BOARD_HEIGHT // CELL_SIZE
    expected_cols = BOARD_WIDTH // CELL_SIZE

    assert len(grid_data) == expected_rows
    assert len(grid_data[0]) == expected_cols
    assert all(cell == 0 for row in grid_data for cell in row)


def test_add_tower(test_grid):
    """Test adding a tower to the grid."""
    row, col = 1, 1
    tower_type = 1  # Normal tower

    test_grid.add_tower(row, col, tower_type)
    grid_data = test_grid.get_grid()

    assert grid_data[row][col] == tower_type
    assert (row, col) in test_grid.towers


def test_remove_tower(test_grid):
    """Test removing a tower from the grid."""
    row, col = 1, 1
    tower_type = 1

    # Add then remove tower
    test_grid.add_tower(row, col, tower_type)
    test_grid.remove_tower(row, col)

    grid_data = test_grid.get_grid()
    assert grid_data[row][col] == 0
    assert (row, col) not in test_grid.towers


def test_multiple_tower_types(test_grid):
    """Test adding different types of towers."""
    # Add different tower types
    positions = [(1, 1), (2, 2), (3, 3)]
    tower_types = [1, 2, 3]  # Normal, Power, Slow

    for (row, col), tower_type in zip(positions, tower_types):
        test_grid.add_tower(row, col, tower_type)

    grid_data = test_grid.get_grid()

    # Verify each tower
    for (row, col), tower_type in zip(positions, tower_types):
        assert grid_data[row][col] == tower_type
        assert (row, col) in test_grid.towers


def test_invalid_tower_type(test_grid):
    """Test adding invalid tower type."""
    row, col = 1, 1
    invalid_tower_type = 99

    test_grid.add_tower(row, col, invalid_tower_type)
    grid_data = test_grid.get_grid()

    assert grid_data[row][col] == 0  # Should not add invalid tower
    assert (row, col) not in test_grid.towers
