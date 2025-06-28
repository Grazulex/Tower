import pygame
from .enemies import Enemy

class EnemyWave:
    def __init__(self, screen, track_points, num_enemies, spawn_delay):
        self.screen = screen
        self.track_points = track_points
        self.num_enemies = num_enemies  # Nombre total d'ennemis à spawner
        self.spawn_delay = spawn_delay  # Délai en millisecondes entre chaque spawn
        
        self.enemies = []  # Liste des ennemis actifs
        self.enemies_spawned = 0  # Nombre d'ennemis déjà spawned
        self.last_spawn_time = 0  # Temps du dernier spawn
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Spawn un nouvel ennemi si c'est le moment
        if (self.enemies_spawned < self.num_enemies and 
            current_time - self.last_spawn_time >= self.spawn_delay):
            self.enemies.append(Enemy(self.screen, self.track_points))
            self.enemies_spawned += 1
            self.last_spawn_time = current_time
        
        # Mettre à jour tous les ennemis actifs
        active_enemies = []
        for enemy in self.enemies:
            if enemy.is_active():
                enemy.move()
                enemy.draw()
                active_enemies.append(enemy)
        
        # Garder seulement les ennemis actifs
        self.enemies = active_enemies
        
    def is_wave_complete(self):
        # La vague est terminée quand tous les ennemis ont été spawned
        # et qu'il n'y a plus d'ennemis actifs
        return self.enemies_spawned >= self.num_enemies and len(self.enemies) == 0
