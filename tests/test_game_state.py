"""
Tests for the GameState class.
"""

from tower.game.game_state import GameState


def test_game_state_initialization():
    """Test if GameState initializes with correct default values."""
    state = GameState()
    assert state.get_state() == GameState.MENU
    # Note: high score may have a previous value from save file


def test_game_state_transitions():
    """Test if state transitions work correctly."""
    state = GameState()

    # Test transition to playing
    state.set_state(GameState.PLAYING)
    assert state.get_state() == GameState.PLAYING

    # Test transition to game over
    state.set_state(GameState.GAME_OVER)
    assert state.get_state() == GameState.GAME_OVER

    # Test transition back to menu
    state.set_state(GameState.MENU)
    assert state.get_state() == GameState.MENU


def test_high_score_update():
    """Test if high score updates work correctly."""
    state = GameState()
    initial_high_score = state.get_high_score()

    # Test with lower score
    lower_score = initial_high_score - 1 if initial_high_score > 0 else 0
    was_updated = state.update_high_score(lower_score)
    assert not was_updated
    assert state.get_high_score() == initial_high_score

    # Test with higher score
    higher_score = initial_high_score + 100
    was_updated = state.update_high_score(higher_score)
    assert was_updated
    assert state.get_high_score() == higher_score
