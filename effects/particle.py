import pygame
import random
from config.color import *

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 3)  # particules plus petites
        self.lifetime = 30  # durée de vie plus courte
        self.dx = random.uniform(-2, 2)  # vitesse plus modérée
        self.dy = random.uniform(-2, 2)  # vitesse plus modérée
        self.alpha = 255  # opacité

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.alpha = int((self.lifetime / 30) * 255)  # diminue progressivement l'opacité
        
    def draw(self, screen):
        if self.lifetime > 0:
            # Dessinons directement sur l'écran pour tester
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        return self.lifetime > 0
