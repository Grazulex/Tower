import pygame
from config.constants import *
from config.color import *

class Tour:
    def __init__(self, screen, column, row):
        self.screen = screen
        self.column = column
        self.row = row
        self.color = GREEN
        self.text_color = WHITE
        self.health = 1000
        self.damage = 25
        self.attack_speed = 1  # Attacks per second
        self.last_attack_time = pygame.time.get_ticks()  # Initialiser avec le temps actuel
        self.attack_range = TOUR_RANGE
        self.cell_size = CELL_SIZE
        self.font = pygame.font.SysFont(None, 12)

    def draw(self, enemies):
        pygame.draw.rect(self.screen, self.color,
                         (self.cell_size * self.column, self.cell_size * self.row, self.cell_size, self.cell_size))

        text = self.font.render(str(self.damage), True, self.text_color)
        text_rect = text.get_rect(center=(int(self.cell_size * self.column)+(self.cell_size//2), int(self.cell_size * self.row)+(self.cell_size//2)))
        self.screen.blit(text, text_rect)

        #draw range around tour
        center_x = self.cell_size * self.column + self.cell_size // 2
        center_y = self.cell_size * self.row + self.cell_size // 2
        pygame.draw.circle(self.screen, GRAY, (center_x, center_y), self.attack_range, 1)
        if enemies:
            # Trouver tous les ennemis à portée
            enemies_in_range = []
            for enemy in enemies:
                distance = ((enemy.x - center_x) ** 2 + (enemy.y - center_y) ** 2) ** 0.5
                if distance <= self.attack_range:
                    enemies_in_range.append(enemy)
                    # Dessiner une ligne vers l'ennemi à portée
                    pygame.draw.line(self.screen, RED, (center_x, center_y), (enemy.x, enemy.y), 1)
            
            # Si on a des ennemis à portée et que le délai d'attaque est écoulé
            if enemies_in_range:
                current_time = pygame.time.get_ticks()

                attack_delay = (1 / self.attack_speed) * 1000  # Convertir en millisecondes
                time_since_last_attack = current_time - self.last_attack_time
                if time_since_last_attack >= attack_delay:
                    target = min(enemies_in_range, key=lambda e: ((e.x - center_x)**2 + (e.y - center_y)**2))
                    self.attack(target)
                    self.last_attack_time = current_time

    def attack(self, enemy):
        enemy.take_damage(self.damage)