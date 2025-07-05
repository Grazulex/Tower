from typing import List, Tuple
import pygame
import random
from pygame.surface import Surface
from game.game_manager import GameManager
from entities.enemy_base import EnemyBase
from entities.enemies.enemy_normal import EnemyNormal
from entities.enemies.enemy_big import EnemyBig
from entities.enemies.enemy_small import EnemySmall
from entities.enemies.enemy_slow import EnemySlow


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

    def __init__(
        self,
        screen: Surface,
        track_points: List[Tuple[int, int]],
        num_enemies: int,
        spawn_delay: int,
        game_manager: GameManager,
    ):
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

    def update(self) -> None:
        """
        Updates the state of the enemy wave.

        Handles enemy spawning, movement, drawing, and removal of inactive enemies.
        Also updates the game manager when an enemy reaches the end of the track.
        """
        current_time = pygame.time.get_ticks()

        if (
            self.enemies_spawned < self.num_enemies
            and current_time - self.last_spawn_time >= self.spawn_delay
        ):
            enemy_class = random.choice([EnemyNormal, EnemyBig, EnemySmall, EnemySlow])
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

    def is_wave_complete(self) -> bool:
        """
        Checks if the wave is complete.

        Returns:
            bool: True if all enemies have been spawned and removed, False otherwise.
        """
        return self.enemies_spawned >= self.num_enemies and len(self.enemies) == 0

    def get_enemies(self) -> List[EnemyBase]:
        """
        Gets the list of active enemies.

        Returns:
            list: The list of active enemies in the wave.
        """
        return self.enemies

    def get_total_enemies(self) -> int:
        """
        Gets the total number of enemies in the wave.

        Returns:
            int: The total number of enemies in the wave.
        """
        return self.num_enemies

    def get_remaining_enemies(self) -> int:
        """
        Gets the number of remaining enemies in the wave.

        Returns:
            int: The number of enemies yet to be spawned plus the number of active enemies.
        """
        return self.num_enemies - self.enemies_spawned + len(self.enemies)
