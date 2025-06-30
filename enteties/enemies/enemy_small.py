from enteties.enemy_base import Enemy
from config.constants import *
from config.color import *

class EnemySmall(Enemy):
    def __init__(self, screen, track_points, game_manager=None):
        Enemy.__init__(self, screen, track_points, game_manager)
        self.color = GREEN
        self.radius = ENEMY_RADIUS*0.8
        self.text_color = WHITE
        self.health = 75  # Augmentée
        self.speed = ENEMY_SPEED * 2.5  # Plus rapide
        self.points_value = 35  # Plus de points car difficile à toucher
