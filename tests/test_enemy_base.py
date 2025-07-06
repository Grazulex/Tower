"""
Tests for the EnemyBase class.
"""

import pytest
import pygame
from tower.entities.enemy_base import EnemyBase
from tower.game.game_manager import GameManager
from tower.config.constants import CELL_SIZE


@pytest.fixture
def test_screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))


@pytest.fixture
def test_track():
    """Create a simple test track."""
    return [(0, 0), (0, 1), (1, 1), (1, 2)]


@pytest.fixture
def enemy_base(test_screen, test_track):
    """Create a base enemy instance."""
    return EnemyBase(test_screen, test_track, GameManager())


def test_enemy_initialization(enemy_base, test_track):
    """Test if enemy initializes with correct values."""
    assert enemy_base.health == 100  # Default health
    assert enemy_base.visible == True
    assert enemy_base.current_point_index == 0
    assert enemy_base.reached_end == False

    # Test initial position (should be at center of first track cell)
    expected_x = test_track[0][1] * CELL_SIZE + CELL_SIZE // 2
    expected_y = test_track[0][0] * CELL_SIZE + CELL_SIZE // 2
    assert enemy_base.x == expected_x
    assert enemy_base.y == expected_y


def test_enemy_take_damage(enemy_base):
    """Test if taking damage works correctly."""
    initial_health = enemy_base.health
    damage = 30

    enemy_base.take_damage(damage)
    assert enemy_base.health == initial_health - damage
    assert enemy_base.visible == True  # Enemy should still be visible

    # Test fatal damage
    enemy_base.take_damage(enemy_base.health)
    assert enemy_base.health <= 0
    assert enemy_base.visible == False  # Enemy should be invisible after death


def test_enemy_is_active(enemy_base):
    """Test if enemy active state is correct under different conditions."""
    assert enemy_base.is_active() == True  # Should be active when healthy

    # Test after taking fatal damage
    enemy_base.take_damage(enemy_base.health)
    assert enemy_base.is_active() == False  # Should be inactive when dead
