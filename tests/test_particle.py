"""
Tests for the Particle class.
"""

import pytest
import pygame
from tower.effects.particle import Particle
from tower.config.constants import (
    PARTICLE_SIZE_MIN,
    PARTICLE_SIZE_MAX,
    PARTICLE_LIFETIME_MIN,
    PARTICLE_LIFETIME_MAX,
    PARTICLE_SPEED,
)


@pytest.fixture
def test_screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))


@pytest.fixture
def test_particle():
    """Create a test particle instance."""
    return Particle(100, 100, (255, 0, 0))  # Red particle at (100, 100)


def test_particle_initialization(test_particle):
    """Test if particle initializes with correct values."""
    assert test_particle.x == 100
    assert test_particle.y == 100
    assert all(0 <= c <= 255 for c in test_particle.color)
    assert PARTICLE_SIZE_MIN <= test_particle.radius <= PARTICLE_SIZE_MAX
    assert PARTICLE_LIFETIME_MIN <= test_particle.lifetime <= PARTICLE_LIFETIME_MAX
    assert -PARTICLE_SPEED <= test_particle.dx <= PARTICLE_SPEED
    assert -PARTICLE_SPEED <= test_particle.dy <= PARTICLE_SPEED
    assert test_particle.alpha == 255


def test_particle_update(test_particle):
    """Test if particle updates correctly."""
    initial_x = test_particle.x
    initial_y = test_particle.y
    initial_lifetime = test_particle.lifetime

    test_particle.update()

    # Position should change based on velocity
    assert test_particle.x == initial_x + test_particle.dx
    assert test_particle.y == initial_y + test_particle.dy
    assert test_particle.lifetime == initial_lifetime - 1

    # Alpha should be proportional to remaining lifetime
    expected_alpha = int((test_particle.lifetime / 30) * 255)
    assert test_particle.alpha == expected_alpha


def test_particle_is_alive(test_particle):
    """Test particle lifetime logic."""
    assert test_particle.is_alive()

    # Force particle to end of life
    test_particle.lifetime = 0
    assert not test_particle.is_alive()


def test_particle_draw(test_particle, test_screen):
    """Test if particle can be drawn without errors."""
    # Initial alpha should be 255
    assert test_particle.alpha == 255

    # Draw should work without errors
    test_particle.draw(test_screen)

    # Force a lifetime decrease to ensure alpha change
    test_particle.lifetime = 15  # Half of default lifetime

    # Update and draw again
    test_particle.update()
    test_particle.draw(test_screen)

    # Alpha should be proportional to remaining lifetime
    expected_alpha = int((test_particle.lifetime / 30) * 255)
    assert test_particle.alpha == expected_alpha
    assert test_particle.alpha < 255
