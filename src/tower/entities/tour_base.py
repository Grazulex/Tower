from typing import List
import pygame
from pygame.surface import Surface
from tower.game.game_manager import GameManager
from tower.entities.enemy_base import EnemyBase
from tower.config.constants import (
    ATTACK_DURATION,
    CELL_SIZE,
    RANGE_CIRCLES_COUNT,
    RANGE_MIN_ALPHA,
    RANGE_MAX_ALPHA,
    RANGE_COLOR_INTENSITY,
    RANGE_GLOW_ALPHA,
)
from tower.config.color import GREEN, WHITE, RED
from dataclasses import dataclass, field


@dataclass()
class TourBase:
    screen: Surface
    column: int
    row: int
    color: tuple = field(default=GREEN, init=False)
    text_color: tuple = field(default=WHITE, init=False)
    health: int = field(default=1000, init=False)
    damage: int = field(default=35, init=False)
    attack_speed: float = field(default=1.0, init=False)
    last_attack_time: int = field(default_factory=lambda: pygame.time.get_ticks(), init=False)
    attack_range: int = field(default=60, init=False)
    cost: int = field(default=100, init=False)
    cell_size: int = field(default=CELL_SIZE, init=False)
    font: pygame.font.Font = field(default_factory=lambda: pygame.font.SysFont(None, 12), init=False)
    is_attacking: bool = field(default=False, init=False)
    attack_animation_duration: int = field(default=ATTACK_DURATION, init=False)
    current_target: EnemyBase = field(default=EnemyBase, init=False)
    """
    Represents a defensive tower in the game.
    
    Attributes:
        screen (pygame.Surface): The game screen where the tower is drawn.
        column (int): The column position of the tower on the grid.
        row (int): The row position of the tower on the grid.
        color (tuple): The color of the tower (RGB format).
        text_color (tuple): The color of the text displaying the tower's damage.
        health (int): The health of the tower.
        damage (int): The damage dealt by the tower to enemies.
        attack_speed (float): The attack speed of the tower (attacks per second).
        last_attack_time (int): The time (in milliseconds) of the last attack.
        attack_range (int): The range within which the tower can attack enemies.
        cost (int): The cost of the tower.
        cell_size (int): The size of a single grid cell.
        font (pygame.font.Font): The font used to display the tower's damage.
        is_attacking (bool): Whether the tower is currently attacking.
        attack_animation_duration (int): The duration of the attack animation (in milliseconds).
        current_target (Enemy): The current enemy being targeted by the tower.
    """

    def play_attack_sound(self) -> None:
        """Plays the tower's attack sound if one is defined and audio is available"""
        try:
            if hasattr(self, "attack_sound"):
                self.attack_sound.play()
        except (pygame.error, AttributeError):
            # Skip playing sound if audio is not available
            pass

    def draw(self, enemies: List[EnemyBase], game_manager: GameManager) -> None:
        """
        Draws the tower on the screen and handles its attack logic.

        Args:
            enemies (list): A list of Enemy objects currently in the game.
            game_manager (GameManager): The game manager handling game state.
        """
        # Base coordinates of the tower
        x = self.cell_size * self.column
        y = self.cell_size * self.row
        size = self.cell_size
        padding = 2  # Space for the glowing border

        # Create a surface for the tower with alpha channel
        tower_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # Fill in with the base color (darker)
        base_color = (
            max(0, self.color[0] - 30),
            max(0, self.color[1] - 30),
            max(0, self.color[2] - 30),
        )
        pygame.draw.rect(tower_surface, base_color, (0, 0, size, size))

        # Add a subtle grid pattern
        grid_color = (
            max(0, self.color[0] - 15),
            max(0, self.color[1] - 15),
            max(0, self.color[2] - 15),
        )
        for i in range(0, size, 4):
            pygame.draw.line(tower_surface, grid_color, (i, 0), (i, size))
            pygame.draw.line(tower_surface, grid_color, (0, i), (size, i))

        # Draw the main square with a glowing border
        inner_rect = pygame.Rect(padding, padding, size - 2 * padding, size - 2 * padding)
        pygame.draw.rect(tower_surface, self.color, inner_rect)

        # Add highlights on the edges
        highlight_color = (
            min(255, self.color[0] + 50),
            min(255, self.color[1] + 50),
            min(255, self.color[2] + 50),
        )
        pygame.draw.line(
            tower_surface,
            highlight_color,
            (padding, padding),
            (size - padding, padding),
            2,
        )
        pygame.draw.line(
            tower_surface,
            highlight_color,
            (padding, padding),
            (padding, size - padding),
            2,
        )

        # Add a darker outer border
        border_color = (
            max(0, self.color[0] - 50),
            max(0, self.color[1] - 50),
            max(0, self.color[2] - 50),
        )
        pygame.draw.rect(tower_surface, border_color, (0, 0, size, size), 1)

        # Add a shine effect in the top left corner
        glow_pos = (padding + 2, padding + 2)
        glow_color = (255, 255, 255, 128)
        glow_size = 3
        pygame.draw.circle(tower_surface, glow_color, glow_pos, glow_size)

        # Draw the tower on the screen
        self.screen.blit(tower_surface, (x, y))

        center_x = self.cell_size * self.column + self.cell_size // 2
        center_y = self.cell_size * self.row + self.cell_size // 2

        # Display shooting range only for the first two waves
        if game_manager and game_manager.get_current_wave() <= 2:
            # Create a surface with alpha channel for the shooting range
            range_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2), pygame.SRCALPHA)

            # Draw multiple concentric circles with varying transparency
            for r in range(self.attack_range, self.attack_range - RANGE_CIRCLES_COUNT, -1):
                # Calculate alpha based on circle position
                progress = (r - (self.attack_range - RANGE_CIRCLES_COUNT)) / RANGE_CIRCLES_COUNT
                alpha = int(RANGE_MIN_ALPHA + (RANGE_MAX_ALPHA - RANGE_MIN_ALPHA) * progress)

                # Use a slightly tinted color based on the tower's color
                range_color = (
                    min(255, self.color[0] + RANGE_COLOR_INTENSITY),
                    min(255, self.color[1] + RANGE_COLOR_INTENSITY),
                    min(255, self.color[2] + RANGE_COLOR_INTENSITY),
                    alpha,
                )
                pygame.draw.circle(
                    range_surface,
                    range_color,
                    (self.attack_range, self.attack_range),
                    r,
                    1,
                )

            # Add a very subtle glow effect
            glow_color = (255, 255, 255, RANGE_GLOW_ALPHA)
            pygame.draw.circle(
                range_surface,
                glow_color,
                (self.attack_range, self.attack_range),
                self.attack_range - 1,
                1,
            )

            # Display the range surface
            self.screen.blit(
                range_surface,
                (center_x - self.attack_range, center_y - self.attack_range),
            )
        if enemies:
            enemies_in_range = []
            for enemy in enemies:
                distance = ((enemy.x - center_x) ** 2 + (enemy.y - center_y) ** 2) ** 0.5
                if distance <= self.attack_range:
                    enemies_in_range.append(enemy)

            if enemies_in_range:
                current_time = pygame.time.get_ticks()

                # Filter valid enemies (alive and visible)
                valid_enemies = [e for e in enemies_in_range if e.visible and e.health > 0]

                if valid_enemies:
                    attack_delay = (1 / self.attack_speed) * 1000
                    time_since_last_attack = current_time - self.last_attack_time
                    if time_since_last_attack >= attack_delay:
                        target = min(valid_enemies, key=lambda e: e.health)
                        # Final check that the target is still valid
                        if target.visible and target.health > 0:
                            self.attack(target)
                            self.last_attack_time = current_time
                            self.play_attack_sound()
                            self.is_attacking = True
                            self.current_target = target

                if self.is_attacking and self.current_target and self.current_target.visible:
                    attack_animation_time = current_time - self.last_attack_time
                    if attack_animation_time <= self.attack_animation_duration:
                        pygame.draw.line(
                            self.screen,
                            RED,
                            (center_x, center_y),
                            (self.current_target.x, self.current_target.y),
                            3,
                        )
                    else:
                        self.is_attacking = False
                        self.current_target = None
                else:
                    self.is_attacking = False
                    self.current_target = None

    def attack(self, enemy: EnemyBase) -> None:
        """
        Attacks the specified enemy, reducing its health.

        Args:
            enemy (Enemy): The enemy to attack.
        """
        enemy.take_damage(self.damage)
