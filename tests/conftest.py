"""
Configuration file for pytest.
Contains fixtures that can be used across multiple test files.
"""

import os
import pytest
import pygame
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def initialize_pygame():
    """Initialize pygame for all tests."""
    # Configure Pygame to use a dummy video driver
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    pygame.display.set_mode((800, 600))
    try:
        pygame.mixer.init()
    except pygame.error:
        # Skip mixer initialization if no audio device is available
        print("Warning: Audio device not available, running without sound")
    yield
    pygame.quit()


@pytest.fixture
def mock_sound():
    """Create a mock sound object for testing."""
    mock = MagicMock()
    mock.play = MagicMock()
    return mock
