from typing import Optional
import pygame
from pygame.surface import Surface
from enteties.tour_base import TourBase
from config.color import *
from config.constants import (NORMAL_TOWER_RANGE, NORMAL_TOWER_ATTACK_SPEED,
                           NORMAL_TOWER_DAMAGE, NORMAL_TOWER_COST)
from os.path import join
from dataclasses import dataclass, field

@dataclass
class TourNormal(TourBase):
    screen: Optional[Surface]
    column: int
    row: int
    color: tuple = field(default=BLUE, init=False)
    attack_range: int = field(default=NORMAL_TOWER_RANGE, init=False)
    attack_speed: float = field(default=NORMAL_TOWER_ATTACK_SPEED, init=False)
    damage: int = field(default=NORMAL_TOWER_DAMAGE, init=False)
    cost: int = field(default=NORMAL_TOWER_COST, init=False)
    """Tour with balanced stats for general purpose defense"""
    def __post_init__(self):
        super().__init__(self.screen, self.column, self.row)
        # Only load sound if screen is defined (not during type initialization)
        if self.screen is not None:
            self.attack_sound = pygame.mixer.Sound(join('assets', 'sounds', 'crystal_laser_medium.wav'))
