import pygame
from config.color import *
from config.constants import *

class GameUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)  # Police plus grande pour le score
        
    def draw_points(self, points):
        """Affiche le nombre de points du joueur"""
        points_text = self.font.render(f"Points: {points}", True, WHITE)
        points_rect = points_text.get_rect(topleft=(10, 10))  # Position en haut à gauche
        self.screen.blit(points_text, points_rect)
        
    def draw_tower_costs(self):
        """Affiche le coût des différentes tours"""
        font_small = pygame.font.SysFont(None, 24)
        costs = [
            ("Normal Tower: 100", BLUE),
            ("Power Tower: 150", RED),
            ("Slow Tower: 175", YELLOW)
        ]
        
        for i, (text, color) in enumerate(costs):
            cost_text = font_small.render(text, True, color)
            cost_rect = cost_text.get_rect(topleft=(10, 50 + i * 25))
            self.screen.blit(cost_text, cost_rect)
