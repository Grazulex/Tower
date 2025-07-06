"""
Tests for the TowerType class.
"""

import pytest
from tower.entities.tours.tower_types import TowerType
from tower.entities.tours.tour_normal import TourNormal
from tower.entities.tours.tour_power import TourPower
from tower.entities.tours.tour_slow import TourSlow


def test_tower_type_values():
    """Test if tower types are correctly mapped to their classes."""
    assert TowerType.NORMAL.tower_class == TourNormal
    assert TowerType.POWER.tower_class == TourPower
    assert TowerType.SLOW.tower_class == TourSlow

def test_tower_type_grid_types():
    """Test if grid types are correctly assigned."""
    assert TowerType.NORMAL.grid_type == 1
    assert TowerType.POWER.grid_type == 2
    assert TowerType.SLOW.grid_type == 3

def test_get_all_towers():
    """Test if get_all_towers returns all tower types."""
    all_towers = TowerType.get_all_towers()
    assert len(all_towers) == 3
    assert TowerType.NORMAL in all_towers
    assert TowerType.POWER in all_towers
    assert TowerType.SLOW in all_towers

def test_tower_costs():
    """Test if tower costs are correctly retrieved."""
    normal_cost = TowerType.NORMAL.get_cost()
    power_cost = TowerType.POWER.get_cost()
    slow_cost = TowerType.SLOW.get_cost()
    
    assert normal_cost > 0
    assert power_cost > normal_cost  # Power tower should be more expensive
    assert slow_cost > 0

def test_tower_colors():
    """Test if tower colors are correctly retrieved."""
    for tower_type in TowerType:
        color = tower_type.get_color()
        assert isinstance(color, tuple)
        assert len(color) == 3  # RGB format
        assert all(0 <= c <= 255 for c in color)  # Valid RGB values
