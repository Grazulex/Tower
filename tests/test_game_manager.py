"""
Tests for the GameManager class.
"""

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


def test_game_manager_wave_handling():
    """Test wave completion and progression logic."""
    manager = GameManager()
    initial_wave = manager.get_current_wave()

    # Test wave completion
    assert not manager.is_wave_completed()
    manager.set_wave_completed(True)
    assert manager.is_wave_completed()

    # Test wave progression
    manager.next_wave()
    assert manager.get_current_wave() == initial_wave + 1
    assert not manager.is_wave_completed()


def test_game_manager_enemy_kills():
    """Test enemy kill tracking."""
    manager = GameManager()
    initial_kills = manager.get_enemies_killed()

    # Track a kill
    manager.enemy_killed()
    assert manager.get_enemies_killed() == initial_kills + 1


def test_game_manager_tower_purchase():
    """Test tower purchasing system."""

    class MockTower:
        def __init__(self, cost):
            self.cost = cost

    manager = GameManager()
    initial_points = manager.get_points()

    # Create mock towers
    cheap_tower = lambda *args: MockTower(cost=50)
    expensive_tower = lambda *args: MockTower(cost=initial_points + 100)

    # Test affordable tower
    assert manager.can_afford_tower(cheap_tower)
    success = manager.buy_tower(cheap_tower)
    assert success
    assert manager.get_points() == initial_points - 50

    # Test unaffordable tower
    assert not manager.can_afford_tower(expensive_tower)
    success = manager.buy_tower(expensive_tower)
    assert not success
    assert manager.get_points() == initial_points - 50  # Points shouldn't change
