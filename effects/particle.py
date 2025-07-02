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
        Draws the particle on the screen with a neon effect.

        Args:
            screen (pygame.Surface): The surface where the particle is drawn.
        """
        if self.lifetime > 0:
            # S'assurer que l'alpha est dans la plage valide (0-255)
            self.alpha = max(0, min(255, int(self.alpha)))
            
            # Dessiner le corps principal de la particule
            particle_color = (max(0, min(255, int(self.color[0]))),
                            max(0, min(255, int(self.color[1]))),
                            max(0, min(255, int(self.color[2]))),
                            self.alpha)
            
            # Créer une surface pour la particule
            size = max(1, int(self.radius * 2))
            particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Dessiner la particule
            pygame.draw.circle(particle_surface,
                             particle_color,
                             (size // 2, size // 2),
                             max(1, int(self.radius)))
            
            # Ajouter un point brillant au centre
            highlight_radius = max(1, int(self.radius * 0.5))
            highlight_color = (255, 255, 255, self.alpha // 2)
            pygame.draw.circle(particle_surface,
                             highlight_color,
                             (size // 2, size // 2),
                             highlight_radius)
            
            # Dessiner la particule sur l'écran
            screen.blit(particle_surface,
                       (int(self.x - size // 2),
                        int(self.y - size // 2)))

    def is_alive(self):
        """
        Checks if the particle is still alive.

        Returns:
            bool: True if the particle's lifetime is greater than 0, False otherwise.
        """
        return self.lifetime > 0