from typing import List
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from enteties.enemy_base import EnemyBase
from config.constants import *
from config.color import *

class TourBase:
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

    def play_attack_sound(self):
        """
        Method to be overridden in child classes to play specific attack sound.
        """
        pass

    def __init__(self, screen: Surface, column: int, row: int):
        """
        Initializes a Tour instance.

        Args:
            screen (pygame.Surface): The game screen where the tower is drawn.
            column (int): The column position of the tower on the grid.
            row (int): The row position of the tower on the grid.
        """
        self.screen = screen
        self.column = column
        self.row = row
        self.color = GREEN
        self.text_color = WHITE
        self.health = 1000
        self.damage = 35
        self.attack_speed = 1.0
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_range = 60
        self.cost = 100
        self.cell_size = CELL_SIZE
        self.font = pygame.font.SysFont(None, 12)

        self.is_attacking = False
        self.attack_animation_duration = ATTACK_DURATION
        self.current_target = None

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
        base_color = (max(0, self.color[0] - 30),
                     max(0, self.color[1] - 30),
                     max(0, self.color[2] - 30))
        pygame.draw.rect(tower_surface, base_color, (0, 0, size, size))

        # Add a subtle grid pattern
        grid_color = (max(0, self.color[0] - 15),
                     max(0, self.color[1] - 15),
                     max(0, self.color[2] - 15))
        for i in range(0, size, 4):
            pygame.draw.line(tower_surface, grid_color, (i, 0), (i, size))
            pygame.draw.line(tower_surface, grid_color, (0, i), (size, i))

        # Draw the main square with a glowing border
        inner_rect = pygame.Rect(padding, padding, size - 2*padding, size - 2*padding)
        pygame.draw.rect(tower_surface, self.color, inner_rect)

        # Add highlights on the edges
        highlight_color = (min(255, self.color[0] + 50),
                         min(255, self.color[1] + 50),
                         min(255, self.color[2] + 50))
        pygame.draw.line(tower_surface, highlight_color, (padding, padding), (size-padding, padding), 2)
        pygame.draw.line(tower_surface, highlight_color, (padding, padding), (padding, size-padding), 2)

        # Add a darker outer border
        border_color = (max(0, self.color[0] - 50),
                       max(0, self.color[1] - 50),
                       max(0, self.color[2] - 50))
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
                    alpha
                )
                pygame.draw.circle(range_surface, range_color, (self.attack_range, self.attack_range), r, 1)
            
            # Add a very subtle glow effect
            glow_color = (255, 255, 255, RANGE_GLOW_ALPHA)
            pygame.draw.circle(range_surface, glow_color, (self.attack_range, self.attack_range), self.attack_range - 1, 1)
            
            # Display the range surface
            self.screen.blit(range_surface, (center_x - self.attack_range, center_y - self.attack_range))
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
                        pygame.draw.line(self.screen, RED, (center_x, center_y),
                                       (self.current_target.x, self.current_target.y), 3)
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