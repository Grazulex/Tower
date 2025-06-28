from enteties.enemy_base import Enemy
from config.constants import *
from config.color import *

class EnemyBig(Enemy):
    def __init__(self, screen, track_points):
        Enemy.__init__(self, screen, track_points)
        self.color = YELLOW
        self.radius = ENEMY_RADIUS*1.2
        self.health = 200
        self.speed = ENEMY_SPEED * 0.5