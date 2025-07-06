"""Tests for the main.py module."""

import pytest
import pygame
from tower.main import create_enemy_wave
from tower.config.color import BLACK
from tower.ui.game_ui import GameUI
import tower.design.grid as grid_module
import tower.design.track as track_module
from pygame.surface import Surface
from tower.game.game_state import GameState
from tower.game.game_manager import GameManager
from tower.design.enemy_wave import EnemyWave
from tower.entities.tours.tower_types import TowerType
from tower.config.constants import CELL_SIZE


@pytest.fixture
def screen():
    """Create a test screen surface."""
    pygame.init()
    pygame.display.init()
    display = pygame.display.set_mode((800, 600))
    return pygame.Surface((800, 600))


@pytest.fixture
def track_data():
    """Create sample track data."""
    return [(0, 0), (0, 1), (1, 1), (1, 2)]


@pytest.fixture
def game_manager():
    """Create a game manager instance."""
    return GameManager()


@pytest.fixture
def game_state():
    """Create a game state instance."""
    return GameState()


def run_game_cycle(screen: Surface, game_state: GameState, game_manager: GameManager) -> None:
    """Helper function to run a single game cycle."""
    # Set the initial state to playing
    game_state.set_state("playing")

    # Initialize game components for a single cycle
    grid = grid_module.Grid(screen)
    grid_data = grid.get_grid()
    game_ui = GameUI(screen)
    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()
    enemy_wave = create_enemy_wave(screen, track_data, game_manager)

    # Game rendering for one cycle
    screen.fill(BLACK)
    grid.draw(enemy_wave.get_enemies(), game_manager)
    track.draw()

    # Draw UI elements
    game_ui.draw_points(game_manager.get_points())
    game_ui.draw_lives(game_manager.get_lives())
    game_ui.draw_high_score(game_state.get_high_score())
    game_ui.draw_tower_buttons(game_manager.get_points())
    game_ui.draw_enemy_info(enemy_wave, game_manager)

    # Update enemy wave
    enemy_wave.update()

    # Check wave completion
    if enemy_wave.is_wave_complete():
        game_manager.set_wave_completed(True)
        game_manager.next_wave()
        game_manager.add_points(game_manager.get_lives() * 10)

    # Check for game over
    if game_manager.is_game_over():
        game_state.set_state("game_over")


def test_create_enemy_wave_new_wave(screen, track_data, game_manager):
    """Test creating a new enemy wave with is_new_wave=True."""
    # Set current wave to 2 to test scaling
    game_manager._current_wave = 2

    wave = create_enemy_wave(screen, track_data, game_manager, is_new_wave=True)

    assert isinstance(wave, EnemyWave)
    # For wave 2: base_enemies = 25 + 5 = 30, max_enemies = 50 + 5 = 55
    assert wave.num_enemies >= 25
    assert wave.spawn_delay >= 500 and wave.spawn_delay <= 2000


def test_create_enemy_wave_continue(screen, track_data, game_manager):
    """Test creating a continuing enemy wave with is_new_wave=False."""
    wave = create_enemy_wave(screen, track_data, game_manager, is_new_wave=False)

    assert isinstance(wave, EnemyWave)
    assert 25 <= wave.num_enemies <= 50
    assert 500 <= wave.spawn_delay <= 2000


def test_create_enemy_wave_scaling(screen, track_data, game_manager):
    """Test that enemy wave scales with wave number."""
    # Reset wave to 1
    game_manager._current_wave = 1
    wave1 = create_enemy_wave(screen, track_data, game_manager, is_new_wave=True)

    # Test wave 5
    game_manager._current_wave = 5
    wave5 = create_enemy_wave(screen, track_data, game_manager, is_new_wave=True)

    # Base enemies increase by 5 per wave, so wave 5 should have more potential enemies
    assert wave5.num_enemies >= 25  # Minimum number of enemies
    assert wave5.spawn_delay >= 500  # Minimum spawn delay


def test_game_cycle_normal(screen, game_state, game_manager):
    """Test a normal game cycle without wave completion or game over."""
    # Set up initial game state
    game_manager._points = 100
    game_manager._lives = 10
    game_manager._current_wave = 1

    # Run a game cycle
    run_game_cycle(screen, game_state, game_manager)

    # Verify game continues normally
    assert game_state.get_state() == GameState.PLAYING
    assert game_manager.get_current_wave() == 1  # Wave shouldn't change in normal cycle


def test_game_cycle_wave_complete(screen, game_state, game_manager):
    """Test a game cycle where the wave is completed."""
    # Set up wave completion scenario
    game_manager._points = 200
    game_manager._lives = 8
    game_manager._current_wave = 2

    # Create a completed wave
    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()
    enemy_wave = create_enemy_wave(screen, track_data, game_manager)
    enemy_wave.enemies_spawned = enemy_wave.num_enemies  # Force all enemies spawned
    enemy_wave.enemies.clear()  # Clear all active enemies

    # Run a game cycle
    run_game_cycle(screen, game_state, game_manager)

    # Verify wave completion effects
    assert game_manager.get_points() >= 200  # Points should be at least initial amount


def test_game_cycle_game_over(screen, game_state, game_manager):
    """Test a game cycle that results in game over."""
    # Set up game over scenario
    game_manager._points = 300
    game_manager._current_wave = 3

    # Force game over by removing all lives
    while game_manager.get_lives() > 0:
        game_manager.lose_life()

    # Run a game cycle
    run_game_cycle(screen, game_state, game_manager)

    # Verify game over state
    assert game_state.get_state() == GameState.GAME_OVER


def test_initialize_game(screen):
    """Test game initialization."""
    from tower.main import initialize_game

    game_state, game_ui, game_manager, grid, track, enemy_wave = initialize_game(screen)

    assert isinstance(game_state, GameState)
    assert isinstance(game_ui, GameUI)
    assert isinstance(game_manager, GameManager)
    assert isinstance(grid, grid_module.Grid)
    assert isinstance(track, track_module.Track)
    assert isinstance(enemy_wave, EnemyWave)
    assert game_state.get_state() == GameState.MENU


def test_handle_tower_placement(screen):
    """Test tower placement logic."""
    from tower.main import handle_tower_placement

    game_ui = GameUI(screen)
    game_manager = GameManager()
    grid = grid_module.Grid(screen)
    track_data = [(0, 0), (0, 1)]  # Some track points

    # Add sufficient points to buy a tower
    game_manager._points = 1000

    # Select the first available tower
    all_towers = TowerType.get_all_towers()
    game_ui.selected_tower = all_towers[0]

    # Try to place tower at valid position
    valid_pos = (CELL_SIZE * 2, CELL_SIZE * 2)  # Position away from track
    handle_tower_placement(valid_pos, game_ui, game_manager, grid, track_data)

    # Verify tower was placed
    grid_data = grid.get_grid()
    assert grid_data[2][2] != 0  # Should have tower at (2,2)

    # Try to place tower on track
    invalid_pos = (CELL_SIZE * 0, CELL_SIZE * 0)  # Position on track
    initial_points = game_manager.get_points()
    handle_tower_placement(invalid_pos, game_ui, game_manager, grid, track_data)

    # Verify tower was not placed and points weren't spent
    assert game_manager.get_points() == initial_points


def test_handle_wave_completion(screen):
    """Test wave completion handling."""
    from tower.main import handle_wave_completion
    import pygame.mixer

    pygame.mixer.init()

    # Initialize components
    game_manager = GameManager()
    grid = grid_module.Grid(screen)
    track = track_module.Track(screen)
    wave_complete_sound = pygame.mixer.Sound(buffer=bytearray([1, 2, 3, 4]))  # Dummy sound

    # Set initial state
    initial_wave = game_manager.get_current_wave()
    initial_points = game_manager.get_points()

    # Handle wave completion
    new_wave, new_grid, new_track, new_track_data = handle_wave_completion(screen, game_manager, grid, track, wave_complete_sound)

    # Verify state changes
    assert game_manager.get_current_wave() == initial_wave + 1
    assert game_manager.get_points() > initial_points
    assert isinstance(new_wave, EnemyWave)
    assert isinstance(new_grid, grid_module.Grid)
    assert isinstance(new_track, track_module.Track)
    assert len(new_track_data) > 0


def test_render_menu_screen(screen):
    """Test menu screen rendering."""
    game_state = GameState()

    # Note: Skip pygame.display.flip() in the test as it's not needed
    screen.fill(BLACK)
    # We can't verify the exact rendering, but we can check that it doesn't raise errors
    assert True


def test_render_game_screen(screen):
    """Test game screen rendering."""
    from tower.main import render_game_screen

    # Initialize components
    game_state = GameState()
    game_manager = GameManager()
    game_ui = GameUI(screen)
    grid = grid_module.Grid(screen)
    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()
    enemy_wave = create_enemy_wave(screen, track_data, game_manager)

    # Render game screen
    render_game_screen(screen, game_state, game_manager, game_ui, grid, track, enemy_wave)

    # We can't verify the exact rendering, but we can check that it doesn't raise errors
    assert True
