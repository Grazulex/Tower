"""
Tests for the GameUI class.
"""

import pytest
import pygame
from tower.ui.game_ui import GameUI
from tower.game.game_manager import GameManager
from tower.design.enemy_wave import EnemyWave


@pytest.fixture
def screen():
    """Create a test screen surface."""
    pygame.init()
    return pygame.Surface((800, 600))


@pytest.fixture
def game_ui(screen):
    """Create a GameUI instance."""
    return GameUI(screen)


@pytest.fixture
def game_manager():
    """Create a GameManager instance."""
    return GameManager()


@pytest.fixture
def enemy_wave(screen):
    """Create an EnemyWave instance."""
    track_data = [(0, 0), (1, 1)]  # Simple track
    return EnemyWave(screen, track_data, num_enemies=10, spawn_delay=100, game_manager=GameManager())


def test_game_ui_initialization(game_ui):
    """Test GameUI initialization."""
    assert game_ui.screen is not None
    assert game_ui.font is not None
    assert game_ui.info_font is not None
    assert game_ui.button_font is not None
    assert isinstance(game_ui.tower_buttons, list)
    assert game_ui.button_padding == 5
    assert game_ui.button_size == 30
    assert game_ui.selected_tower is not None


def test_draw_points(game_ui):
    """Test points drawing."""
    points = 100
    game_ui.draw_points(points)
    # Verify that text was rendered (can't check actual pixels due to Pygame's rendering)
    assert True  # If we got here without errors, the drawing worked


def test_draw_lives(game_ui):
    """Test lives drawing with different colors."""
    # Test low lives (red color)
    game_ui.draw_lives(3)
    # Test normal lives (white color)
    game_ui.draw_lives(10)
    assert True  # If we got here without errors, the drawing worked


def test_draw_game_over(game_ui, game_manager):
    """Test game over screen drawing."""
    game_manager._points = 500
    game_manager._current_wave = 3
    game_manager._enemies_killed = 25
    game_ui.draw_game_over(game_manager)
    assert True  # If we got here without errors, the drawing worked


def test_draw_enemy_info(game_ui, enemy_wave, game_manager):
    """Test enemy info drawing."""
    game_manager._current_wave = 2
    game_manager._enemies_killed = 5
    game_ui.draw_enemy_info(enemy_wave, game_manager)

    # Test with wave completed
    game_manager._wave_completed = True
    game_ui.draw_enemy_info(enemy_wave, game_manager)
    assert True  # If we got here without errors, the drawing worked


def test_draw_high_score(game_ui):
    """Test high score drawing."""
    game_ui.draw_high_score(1000)
    assert True  # If we got here without errors, the drawing worked


def test_draw_tower_buttons(game_ui):
    """Test tower buttons drawing."""
    # Test with enough points to afford all towers
    game_ui.draw_tower_buttons(1000)
    assert len(game_ui.tower_buttons) > 0

    # Test with no points (should show grayed out buttons)
    game_ui.draw_tower_buttons(0)
    assert len(game_ui.tower_buttons) > 0


def test_handle_click(game_ui):
    """Test tower button click handling."""
    # Draw buttons first to populate tower_buttons list
    game_ui.draw_tower_buttons(1000)

    # Test clicking on a tower button
    first_button = game_ui.tower_buttons[0]
    click_pos = (first_button[0].x + 5, first_button[0].y + 5)  # Click in the middle of the first button
    game_ui.selected_tower = None  # Clear initial selection
    result = game_ui.handle_click(click_pos)
    assert result is not None

    # Test clicking the same button again (should deselect)
    result = game_ui.handle_click(click_pos)
    assert result is None

    # Test clicking outside buttons
    result = game_ui.handle_click((0, 0))
    assert result == game_ui.selected_tower  # Should return current selection unchanged


def test_get_selected_tower(game_ui):
    """Test getting selected tower."""
    initial_tower = game_ui.get_selected_tower()
    assert initial_tower is not None

    # Clear selection
    game_ui.selected_tower = None
    assert game_ui.get_selected_tower() is None


def test_draw_preview(game_ui):
    """Test tower preview drawing."""
    # Test preview in valid position
    game_ui.draw_preview((100, 100))

    # Test preview outside board
    game_ui.draw_preview((1000, 1000))
    assert True  # If we got here without errors, the drawing worked
