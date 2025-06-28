import pygame
import random
from config.constants import *
from config.color import *


class Enemy:
    def __init__(self, screen, track_points):
        self.screen = screen
        self.track_points = track_points  # Liste des points du track
        self.current_point_index = 0  # Index du point actuel sur le track
        
        # Position initiale (premier point du track)
        start_row, start_col = track_points[0]
        self.x = start_col * CELL_SIZE + CELL_SIZE // 2
        self.y = start_row * CELL_SIZE + CELL_SIZE // 2
        
        # Caractéristiques de l'ennemi
        self.radius = ENEMY_RADIUS
        self.color = RED
        self.speed = random.randint(1, ENEMY_SPEED)
        
        # Pour savoir si l'ennemi a atteint la fin du track
        self.reached_end = False

    def move(self):
        if self.reached_end:
            return

        # Point cible actuel
        target_row, target_col = self.track_points[self.current_point_index]
        target_x = target_col * CELL_SIZE + CELL_SIZE // 2
        target_y = target_row * CELL_SIZE + CELL_SIZE // 2

        # Calculer la direction vers le point cible
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Si on est assez proche du point cible, passer au point suivant
        if distance < self.speed:
            self.current_point_index += 1
            if self.current_point_index >= len(self.track_points):
                self.reached_end = True
                return
        else:
            # Normaliser le vecteur de direction et appliquer la vitesse
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_active(self):
        return not self.reached_end