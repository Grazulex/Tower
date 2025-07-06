"""
Tests for the TourBase class.
"""

import pytest
import pygame
from tower.entities.tour_base import TourBase
from tower.entities.enemy_base import EnemyBase
from tower.game.game_manager import GameManager
from tower.config.constants import CELL_SIZE

@pytest.fixture
def test_screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))

@pytest.fixture
def test_tower(test_screen):
    """Create a test tower instance."""
    return TourBase(test_screen, 1, 1)

@pytest.fixture
def test_enemy(test_screen):
    """Create a test enemy instance."""
    track = [(0, 0), (1, 1)]  # Simple diagonal track
    return EnemyBase(test_screen, track, GameManager())

def test_tower_initialization(test_tower):
    """Test if tower initializes with correct values."""
    assert test_tower.health == 1000  # Default health
    assert test_tower.damage == 35  # Default damage
    assert test_tower.column == 1
    assert test_tower.row == 1
    assert test_tower.cell_size == CELL_SIZE
    assert not test_tower.is_attacking

def test_tower_position(test_tower):
    """Test if tower position is correctly calculated."""
    expected_x = test_tower.column * CELL_SIZE
    expected_y = test_tower.row * CELL_SIZE
    
    # Draw tower to test position calculation
    test_tower.draw([], None)
    
    assert test_tower.cell_size * test_tower.column == expected_x
    assert test_tower.cell_size * test_tower.row == expected_y

def test_tower_attack(test_tower, test_enemy):
    """Test if tower can attack enemies."""
    initial_enemy_health = test_enemy.health
    test_tower.attack(test_enemy)
    assert test_enemy.health == initial_enemy_health - test_tower.damage

def test_tower_attack_range(test_tower, test_enemy):
    """Test if tower correctly identifies enemies in range."""
    # Position enemy at tower's position (should be in range)
    test_enemy.x = test_tower.column * CELL_SIZE
    test_enemy.y = test_tower.row * CELL_SIZE
    test_enemy.visible = True
    test_enemy.health = 100
    
    # Set last attack time to allow immediate attack
    current_time = pygame.time.get_ticks()
    test_tower.last_attack_time = current_time - (1 / test_tower.attack_speed) * 2000
    
    enemies = [test_enemy]
    game_manager = GameManager()
    test_tower.draw(enemies, game_manager)
    
    # Enemy should be in range and tower should be attacking
    assert test_tower.is_attacking

def test_tower_attack_animation(test_tower, test_enemy):
    """Test tower attack animation."""
    # Position enemy at tower's position
    test_enemy.x = test_tower.column * CELL_SIZE
    test_enemy.y = test_tower.row * CELL_SIZE
    test_enemy.visible = True
    test_enemy.health = 100
    
    # Initial state
    assert not test_tower.is_attacking
    test_tower.current_target = None  # Set current target to None explicitly
    
    # Set last attack time to allow immediate attack
    current_time = pygame.time.get_ticks()
    test_tower.last_attack_time = current_time - (1 / test_tower.attack_speed) * 2000
    
    # Draw tower with enemy in range
    test_tower.draw([test_enemy], GameManager())
    
    # Check attack state
    assert test_tower.is_attacking
    assert test_tower.current_target == test_enemy
