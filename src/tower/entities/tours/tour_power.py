import pygame
from tower.entities.tour_base import TourBase
from tower.config.color import RED
from tower.config.constants import (
    POWER_TOWER_RANGE,
    POWER_TOWER_ATTACK_SPEED,
    POWER_TOWER_DAMAGE,
    POWER_TOWER_COST,
)
from os.path import join
from dataclasses import dataclass, field


@dataclass
class TourPower(TourBase):
    color: tuple = field(default=RED, init=False)
    attack_range: int = field(default=POWER_TOWER_RANGE, init=False)
    attack_speed: float = field(default=POWER_TOWER_ATTACK_SPEED, init=False)
    damage: int = field(default=POWER_TOWER_DAMAGE, init=False)
    cost: int = field(default=POWER_TOWER_COST, init=False)
    """High damage tower with increased attack speed and range"""

    def __post_init__(self):
        super().__init__(self.screen, self.column, self.row)
        # Only load sound if screen is defined (not during type initialization)
        if self.screen is not None:
            try:
                from tower import __file__ as tower_init
                from os.path import dirname
                base_path = dirname(tower_init)
                self.attack_sound = pygame.mixer.Sound(join(base_path, "assets", "sounds", "crystal_laser_short.wav"))
            except (pygame.error, ImportError):
                pass  # Skip sound initialization if audio is not available
