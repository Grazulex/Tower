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
        
        active_enemies = []
        for enemy in self.enemies:
            if enemy.is_active():
                enemy.move()
                enemy.draw()
                active_enemies.append(enemy)
        
        self.enemies = active_enemies
        
    def is_wave_complete(self):
        return self.enemies_spawned >= self.num_enemies and len(self.enemies) == 0
