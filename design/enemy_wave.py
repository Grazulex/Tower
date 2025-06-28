import pygame
import random
from enteties.enemies.enemy_normal import EnemyNormal
from enteties.enemies.enemy_big import EnemyBig
from enteties.enemies.enemy_small import EnemySmall


class EnemyWave:
    def __init__(self, screen, track_points, num_enemies, spawn_delay):
        self.screen = screen
        self.track_points = track_points
        self.num_enemies = num_enemies
        self.spawn_delay = spawn_delay
        
        self.enemies = []
        self.enemies_spawned = 0
        self.last_spawn_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if (self.enemies_spawned < self.num_enemies and
            current_time - self.last_spawn_time >= self.spawn_delay):
            enemy_class = random.choice([EnemyNormal, EnemyBig, EnemySmall])
            enemy = enemy_class(self.screen, self.track_points)
            self.enemies.append(enemy)
            self.enemies_spawned += 1
            self.last_spawn_time = current_time
        
        # Garder une liste des ennemis à retirer
        enemies_to_remove = []
        
        for enemy in self.enemies:
            if enemy.is_active():
                enemy.move()
            # Dessiner tous les ennemis, même ceux qui ne sont plus actifs
            enemy.draw()
            
            # Si l'ennemi n'est plus actif et n'a plus de particules, on le marque pour suppression
            if not enemy.is_active() and not enemy.particles:
                enemies_to_remove.append(enemy)
        
        # Retirer les ennemis qui n'ont plus de particules
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
        
    def is_wave_complete(self):
        return self.enemies_spawned >= self.num_enemies and len(self.enemies) == 0

    def get_enemies(self):
        return self.enemies
