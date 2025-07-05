from typing import List, Tuple
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from config.constants import CELL_SIZE, ENEMY_RADIUS, ENEMY_SPEED, ENEMY_DAMAGED_COLOR
from config.color import RED, BLACK
from effects.particle import Particle
from dataclasses import dataclass, field

@dataclass
class EnemyBase:
    screen: Surface
    track_points: List[Tuple[int, int]]
    game_manager: GameManager
    current_point_index: int = field(default=0, init=False)
    health: int = field(default=100, init=False)
    font: pygame.font.Font = field(default_factory=lambda: pygame.font.SysFont(None, 12), init=False)
    particles: List[Particle] = field(default_factory=list, init=False)
    visible: bool = field(default=True, init=False)
    points_value: int = field(default=25, init=False)
    x: float = field(init=False)
    y: float = field(init=False)
    radius: int = field(default=ENEMY_RADIUS, init=False)
    color: Tuple[int, int, int] = field(default=RED, init=False)
    text_color: Tuple[int, int, int] = field(default=BLACK, init=False)
    speed: float = field(default=ENEMY_SPEED, init=False)
    reached_end: bool = field(default=False, init=False)

    """
    Represents an enemy in the game.

    Attributes:
        screen (pygame.Surface): The game screen where the enemy is drawn.
        track_points (list): The points defining the track for enemy movement.
        game_manager (GameManager): The game manager handling game state (optional).
        current_point_index (int): The index of the current track point the enemy is moving towards.
        health (int): The health of the enemy.
        font (pygame.font.Font): The font used to display the enemy's health.
        particles (list): A list of particles for visual effects when the enemy is removed.
        visible (bool): Whether the enemy is visible on the screen.
        points_value (int): The points awarded for defeating the enemy.
        x (float): The x-coordinate of the enemy's position.
        y (float): The y-coordinate of the enemy's position.
        radius (int): The radius of the enemy's representation.
        color (tuple): The color of the enemy (RGB format).
        text_color (tuple): The color of the text displaying the enemy's health.
        speed (float): The speed of the enemy's movement.
        reached_end (bool): Whether the enemy has reached the end of the track.
    """

    def __post_init__(self):
        """
        Initializes the enemy's position based on the first track point.

        Sets the initial x and y coordinates based on the first track point in the track_points list.
        """
        if not self.track_points:
            raise ValueError("Track points must not be empty.")

        start_row, start_col = self.track_points[0]
        self.x = start_col * CELL_SIZE + CELL_SIZE // 2
        self.y = start_row * CELL_SIZE + CELL_SIZE // 2

    def move(self) -> None:
        """
        Moves the enemy along the track.

        Updates the enemy's position based on its speed and the target track point.
        Marks the enemy as having reached the end if it completes the track.
        """
        if self.reached_end or self.health <= 0:
            return

        target_row, target_col = self.track_points[self.current_point_index]
        target_x = target_col * CELL_SIZE + CELL_SIZE // 2
        target_y = target_row * CELL_SIZE + CELL_SIZE // 2

        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < float(self.speed):
            self.current_point_index += 1
            if self.current_point_index >= len(self.track_points):
                self.reached_end = True
                return
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self) -> None:
        """
        Draws the enemy and its particles on the screen.

        Displays the enemy's health and handles particle effects when the enemy is removed.
        """
        if self.visible:
            # Calculate color based on health
            health_ratio = max(0.0, min(1.0, float(self.health) / 100.0))
            # Transition from base color to red as health decreases
            base_color = self.color
            damaged_color = ENEMY_DAMAGED_COLOR  # Color for damaged enemies
            current_color = (
                int(
                    base_color[0] * health_ratio + damaged_color[0] * (1 - health_ratio)
                ),
                int(
                    base_color[1] * health_ratio + damaged_color[1] * (1 - health_ratio)
                ),
                int(
                    base_color[2] * health_ratio + damaged_color[2] * (1 - health_ratio)
                ),
            )

            # Neon glow effect
            glow_radius = int(self.radius * 1.5)

            # Create multiple circles for glow effect
            for r in range(int(glow_radius), int(self.radius), -1):
                alpha = int(30 * (r / glow_radius))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*current_color, alpha), (r, r), r)
                self.screen.blit(s, (int(self.x - r), int(self.y - r)))

            # Main enemy body with neon effect
            for r in range(int(self.radius), 0, -1):
                alpha = int(255 * (r / self.radius))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*current_color, alpha), (r, r), r)
                self.screen.blit(s, (int(self.x - r), int(self.y - r)))

            # Add glowing border
            border_surface = pygame.Surface(
                (int(self.radius * 2.2), int(self.radius * 2.2)), pygame.SRCALPHA
            )
            pygame.draw.circle(
                border_surface,
                (*current_color, 160),
                (int(self.radius * 1.1), int(self.radius * 1.1)),
                int(self.radius),
                2,
            )
            self.screen.blit(
                border_surface,
                (int(self.x - self.radius * 1.1), int(self.y - self.radius * 1.1)),
            )

        particles_alive = False
        for particle in self.particles[:]:
            particle.update()
            if particle.is_alive():
                particle.draw(self.screen)
                particles_alive = True
            else:
                self.particles.remove(particle)

        if not particles_alive and not self.visible:
            self.x = -100

    def is_active(self) -> bool:
        """
        Checks if the enemy is active.

        Returns:
            bool: True if the enemy has not reached the end and has health remaining, False otherwise.
        """
        return not self.reached_end and self.health > 0

    def take_damage(self, damage: int) -> None:
        """
        Reduces the enemy's health by the specified damage amount.

        Args:
            damage (int): The amount of damage to inflict on the enemy.
        """
        self.health -= damage
        if self.health <= 0:
            self.remove()

    def play_death_sound(self) -> None:
        """Plays the enemy's death sound if one is defined"""
        if hasattr(self, 'death_sound'):
            self.death_sound.play()

    def remove(self) -> None:
        """
        Removes the enemy from the game.

        Triggers particle effects, plays death sound, and updates the game manager with points and enemy kill count.
        """
        self.play_death_sound()

        for i in range(8):
            particle = Particle(self.x, self.y, RED)
            self.particles.append(particle)

        if self.game_manager and self.visible:
            self.game_manager.add_points(self.points_value)
            self.game_manager.enemy_killed()

        self.health = 0
        self.visible = False
