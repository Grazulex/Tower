import pygame
import random
from enteties.enemies.enemy_normal import EnemyNormal
from enteties.enemies.enemy_big import EnemyBig
from enteties.enemies.enemy_small import EnemySmall

class EnemyWave:
    """
    Represents a wave of enemies in the game.

    Attributes:
        screen (pygame.Surface): The game screen where enemies are drawn.
        track_points (list): The points defining the track for enemy movement.
        num_enemies (int): The total number of enemies in the wave.
        spawn_delay (int): The delay (in milliseconds) between enemy spawns.
        game_manager (GameManager): The game manager handling game state.
        enemies (list): The list of active enemies in the wave.
        enemies_spawned (int): The number of enemies spawned so far.
        last_spawn_time (int): The time (in milliseconds) when the last enemy was spawned.
    """

    def __init__(self, screen, track_points, num_enemies, spawn_delay, game_manager):
        """
        Initializes the EnemyWave instance.

        Args:
            screen (pygame.Surface): The game screen where enemies are drawn.
            track_points (list): The points defining the track for enemy movement.
            num_enemies (int): The total number of enemies in the wave.
            spawn_delay (int): The delay (in milliseconds) between enemy spawns.
            game_manager (GameManager): The game manager handling game state.
        """
        self.screen = screen
        self.track_points = track_points
        self.num_enemies = num_enemies
        self.spawn_delay = spawn_delay
        self.game_manager = game_manager

        self.enemies = []
        self.enemies_spawned = 0
        self.last_spawn_time = 0

    def update(self):
        """
        Updates the state of the enemy wave.

        Handles enemy spawning, movement, drawing, and removal of inactive enemies.
        Also updates the game manager when an enemy reaches the end of the track.
        """
        current_time = pygame.time.get_ticks()

        if (self.enemies_spawned < self.num_enemies and
            current_time - self.last_spawn_time >= self.spawn_delay):
            enemy_class = random.choice([EnemyNormal, EnemyBig, EnemySmall])
            enemy = enemy_class(self.screen, self.track_points, self.game_manager)
            self.enemies.append(enemy)
            self.enemies_spawned += 1
            self.last_spawn_time = current_time

        enemies_to_remove = []

        for enemy in self.enemies:
            if enemy.is_active():
                enemy.move()
            enemy.draw()

            if not enemy.is_active():
                if enemy.reached_end:
                    self.game_manager.lose_life()
                if not enemy.particles:
                    enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

    def is_wave_complete(self):
        """
        Checks if the wave is complete.

        Returns:
            bool: True if all enemies have been spawned and removed, False otherwise.
        """
        return self.enemies_spawned >= self.num_enemies and len(self.enemies) == 0

    def get_enemies(self):
        """
        Gets the list of active enemies.

        Returns:
            list: The list of active enemies in the wave.
        """
        return self.enemies

    def get_total_enemies(self):
        """
        Gets the total number of enemies in the wave.

        Returns:
            int: The total number of enemies in the wave.
        """
        return self.num_enemies

    def get_remaining_enemies(self):
        """
        Gets the number of remaining enemies in the wave.

        Returns:
            int: The number of enemies yet to be spawned plus the number of active enemies.
        """
        return self.num_enemies - self.enemies_spawned + len(self.enemies)