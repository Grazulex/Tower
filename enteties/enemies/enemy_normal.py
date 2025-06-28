from enteties.enemy_base import Enemy
from config.color import *

class EnemyNormal(Enemy):
    def __init__(self, screen, track_points, game_manager=None):
        Enemy.__init__(self, screen, track_points, game_manager)
        self.color = BLUE
        self.text_color = WHITE
        self.health = 150  # Augmentée pour la difficulté
        self.points_value = 25  # Points standard
