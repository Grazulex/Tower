import pygame
import random
from config.constants import *

class Particle:
    """
    Represents a particle used for visual effects in the game.

    Attributes:
        x (float): The x-coordinate of the particle.
        y (float): The y-coordinate of the particle.
        color (tuple): The color of the particle (RGB format).
        radius (int): The radius of the particle.
        lifetime (int): The remaining lifetime of the particle.
        dx (float): The horizontal velocity of the particle.
        dy (float): The vertical velocity of the particle.
        alpha (int): The opacity of the particle (0-255).
    """

    def __init__(self, x, y, color):
        """
        Initializes a Particle instance.

        Args:
            x (float): The initial x-coordinate of the particle.
            y (float): The initial y-coordinate of the particle.
            color (tuple): The color of the particle (RGB format).
        """
        self.x = x
        self.y = y
        # Créer une variation de couleur plus douce
        color_variation = random.randint(-PARTICLE_COLOR_VARIATION, PARTICLE_COLOR_VARIATION)
        self.color = (
            max(0, min(255, color[0] + color_variation)),
            max(0, min(255, color[1] + color_variation)),
            max(0, min(255, color[2] + color_variation))
        )
        self.radius = random.randint(PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX)
        self.lifetime = random.randint(PARTICLE_LIFETIME_MIN, PARTICLE_LIFETIME_MAX)
        self.dx = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.dy = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.alpha = 255  # Opacity of the particle

    def update(self):
        """
        Updates the particle's position, lifetime, and opacity.

        The particle moves based on its velocity and its lifetime decreases.
        The opacity is adjusted proportionally to the remaining lifetime.
        """
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.alpha = int((self.lifetime / 30) * 255)

    def draw(self, screen):
        """
        Draws the particle on the screen.

        Args:
            screen (pygame.Surface): The surface where the particle is drawn.
        """
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        """
        Checks if the particle is still alive.

        Returns:
            bool: True if the particle's lifetime is greater than 0, False otherwise.
        """
        return self.lifetime > 0