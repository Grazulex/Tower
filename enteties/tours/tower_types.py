from enum import Enum
from typing import Type
from .tour_normal import TourNormal
from .tour_power import TourPower
from .tour_slow import TourSlow

class TowerType(Enum):
    NORMAL = (TourNormal, 1)
    POWER = (TourPower, 2)
    SLOW = (TourSlow, 3)

    @property
    def tower_class(self) -> Type:
        return self.value[0]
        
    @property
    def grid_type(self) -> int:
        return self.value[1]

    def get_cost(self) -> int:
        # Crée une instance temporaire pour obtenir le coût
        return self.tower_class(None, 0, 0).cost

    def get_color(self):
        # Crée une instance temporaire pour obtenir la couleur
        return self.tower_class(None, 0, 0).color

    @classmethod
    def get_all_towers(cls):
        return list(cls)
