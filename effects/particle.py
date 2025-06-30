import pygame
import random

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
        self.color = color
        self.radius = random.randint(2, 3)
        self.lifetime = 30
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)
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