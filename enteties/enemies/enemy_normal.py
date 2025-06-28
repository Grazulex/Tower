from enteties.enemy_base import Enemy
from config.color import *

class EnemyNormal(Enemy):
    def __init__(self, screen, track_points):
        Enemy.__init__(self, screen, track_points)
        self.color = BLUE
        self.text_color = WHITE