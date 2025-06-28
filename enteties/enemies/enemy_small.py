from enteties.enemy_base import Enemy
from config.constants import *
from config.color import *

class EnemySmall(Enemy):
    def __init__(self, screen, track_points):
        Enemy.__init__(self, screen, track_points)
        self.color = RED
        self.radius = ENEMY_RADIUS*0.8
        self.text_color = WHITE
        self.health = 50
        self.speed = ENEMY_SPEED * 2