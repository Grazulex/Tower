"""
Tests for the EnemyWave class.
"""

import pytest
import pygame
from tower.design.enemy_wave import EnemyWave
from tower.game.game_manager import GameManager

@pytest.fixture
def test_screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))

@pytest.fixture
def test_track():
    """Create a simple test track."""
    return [(0, 0), (0, 1), (1, 1), (1, 2)]

@pytest.fixture
def test_wave(test_screen, test_track):
    """Create a test enemy wave instance."""
    return EnemyWave(
        test_screen,
        test_track,
        num_enemies=5,
        spawn_delay=100,
        game_manager=GameManager()
    )

def test_wave_initialization(test_wave):
    """Test if wave initializes with correct values."""
    assert test_wave.num_enemies == 5
    assert test_wave.spawn_delay == 100
    assert test_wave.enemies_spawned == 0
    assert len(test_wave.enemies) == 0
    assert not test_wave.is_wave_complete()

def test_wave_spawning(test_wave):
    """Test if enemies spawn correctly."""
    # Set initial spawn time to allow immediate spawning
    test_wave.last_spawn_time = pygame.time.get_ticks() - test_wave.spawn_delay - 1
    
    # Update to trigger spawning
    test_wave.update()
    
    assert test_wave.enemies_spawned == 1
    assert len(test_wave.enemies) == 1
    # We have 5 total enemies, spawned 1, so 4 remain
    remaining = test_wave.num_enemies - test_wave.enemies_spawned
    assert remaining == 4

def test_wave_completion(test_wave):
    """Test wave completion logic."""
    # Spawn all enemies
    for _ in range(test_wave.num_enemies):
        # Set spawn time to allow immediate spawning
        test_wave.last_spawn_time = pygame.time.get_ticks() - test_wave.spawn_delay - 1
        test_wave.update()
    
    assert test_wave.enemies_spawned == test_wave.num_enemies
    
    # Remove all enemies (simulating them reaching the end or dying)
    test_wave.enemies.clear()
    
    assert test_wave.is_wave_complete()

def test_enemy_removal(test_wave):
    """Test if enemies are properly removed when they reach the end."""
    # Set spawn time to allow immediate spawning
    test_wave.last_spawn_time = pygame.time.get_ticks() - test_wave.spawn_delay - 1
    test_wave.update()  # Spawn one enemy
    
    assert len(test_wave.enemies) == 1  # Verify enemy was spawned
    enemy = test_wave.enemies[0]
    
    # Simulate enemy reaching the end
    enemy.reached_end = True
    enemy.visible = False
    enemy.particles = []  # Ensure no particles are active
    
    # Update to trigger enemy removal
    test_wave.update()
    
    assert len(test_wave.enemies) == 0

def test_get_total_enemies(test_wave):
    """Test if total enemies count is correct."""
    assert test_wave.get_total_enemies() == 5
