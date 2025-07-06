"""
Tests for the GameManager class.
"""

import pytest
from tower.game.game_manager import GameManager
from tower.config.constants import STARTING_POINTS, STARTING_LIVES

def test_game_manager_initialization():
    """Test if GameManager initializes with correct default values."""
    manager = GameManager()
    assert manager.get_points() == STARTING_POINTS
    assert manager.get_lives() == STARTING_LIVES
    assert manager.get_current_wave() == 1
    assert not manager.is_game_over()
    assert manager.get_enemies_killed() == 0

def test_game_manager_lose_life():
    """Test if losing lives works correctly and game over triggers."""
    manager = GameManager()
    initial_lives = manager.get_lives()
    
    # Lose one life
    manager.lose_life()
    assert manager.get_lives() == initial_lives - 1
    assert not manager.is_game_over()
    
    # Lose remaining lives
    for _ in range(initial_lives - 1):
        manager.lose_life()
    
    assert manager.get_lives() == 0
    assert manager.is_game_over()

def test_game_manager_points():
    """Test if points system works correctly."""
    manager = GameManager()
    initial_points = manager.get_points()
    
    # Add points
    points_to_add = 100
    manager.add_points(points_to_add)
    assert manager.get_points() == initial_points + points_to_add
