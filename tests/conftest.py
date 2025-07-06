"""
Configuration file for pytest.
Contains fixtures that can be used across multiple test files.
"""

import pytest
import pygame

@pytest.fixture(autouse=True)
def initialize_pygame():
    """Initialize pygame for all tests."""
    pygame.init()
    pygame.mixer.init()
    yield
    pygame.quit()
