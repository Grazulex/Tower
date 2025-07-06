"""
Tests for the Track class.
"""

import pytest
import pygame
from tower.design.track import Track
from tower.config.constants import CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT


@pytest.fixture
def test_screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))


@pytest.fixture
def test_track(test_screen):
    """Create a test track instance."""
    return Track(test_screen)


def test_track_initialization(test_track):
    """Test if track initializes correctly."""
    assert len(test_track.track) == 0
    assert test_track.line_width > 0


def test_track_generation(test_track):
    """Test if track generates correctly."""
    test_track.generate_random_track()
    track_points = test_track.get_track()

    assert len(track_points) > 0

    # Check if track points are within bounds
    for row, col in track_points:
        assert 0 <= row < BOARD_HEIGHT // CELL_SIZE
        assert 0 <= col < BOARD_WIDTH // CELL_SIZE


def test_track_connectivity(test_track):
    """Test if track points are connected."""
    test_track.generate_random_track()
    track_points = test_track.get_track()

    # Check if consecutive points are adjacent
    for i in range(len(track_points) - 1):
        current = track_points[i]
        next_point = track_points[i + 1]

        # Points should differ by at most 1 in either row or column
        row_diff = abs(current[0] - next_point[0])
        col_diff = abs(current[1] - next_point[1])

        assert (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)


def test_track_progress(test_track):
    """Test if track progresses towards the right."""
    test_track.generate_random_track()
    track_points = test_track.get_track()

    start_col = track_points[0][1]
    end_col = track_points[-1][1]

    assert end_col > start_col  # Track should progress to the right


def test_track_drawing(test_track):
    """Test if track can be drawn."""
    test_track.generate_random_track()
    test_track.draw()  # Should not raise any exceptions

    # Get track data
    track_points = test_track.get_track()
    assert len(track_points) > 0
