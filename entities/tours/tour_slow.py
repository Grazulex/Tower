from typing import Optional
import pygame
from pygame.surface import Surface
from entities.tour_base import TourBase
from config.color import *
from config.constants import (SLOW_TOWER_RANGE, SLOW_TOWER_ATTACK_SPEED,
                           SLOW_TOWER_DAMAGE, SLOW_TOWER_COST)
from os.path import join
from dataclasses import dataclass, field

@dataclass
class TourSlow(TourBase):
    screen: Optional[Surface]
    column: int
    row: int
    color: tuple = field(default=YELLOW, init=False)
    attack_range: int = field(default=SLOW_TOWER_RANGE, init=False)
    attack_speed: float = field(default=SLOW_TOWER_ATTACK_SPEED, init=False)
    damage: int = field(default=SLOW_TOWER_DAMAGE, init=False)
    cost: int = field(default=SLOW_TOWER_COST, init=False)
    """Support tower that slows enemies with reduced attack speed"""

    def __post_init__(self):
        super().__init__(self.screen, self.column, self.row)
        # Only load sound if screen is defined (not during type initialization)
        if self.screen is not None:
            self.attack_sound = pygame.mixer.Sound(join('assets', 'sounds', 'crystal_laser_long.wav'))
