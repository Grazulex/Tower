from enteties.enemy_base import Enemy
from config.constants import *
from config.color import *

class EnemyBig(Enemy):
    def __init__(self, screen, track_points, game_manager=None):
        Enemy.__init__(self, screen, track_points, game_manager)
        self.color = YELLOW
        self.radius = ENEMY_RADIUS*1.2
        self.health = 300  # Plus résistant
        self.speed = ENEMY_SPEED * 0.4  # Plus lent
        self.points_value = 50  # Plus de points car plus résistant
