import pygame
from config.constants import *
from config.color import *


class Enemy:
    def __init__(self, screen, track_points):
        self.screen = screen
        self.track_points = track_points
        self.current_point_index = 0
        self.health = 100
        self.font = pygame.font.SysFont(None, 12)
        
        start_row, start_col = track_points[0]
        self.x = start_col * CELL_SIZE + CELL_SIZE // 2
        self.y = start_row * CELL_SIZE + CELL_SIZE // 2
        
        self.radius = ENEMY_RADIUS
        self.color = RED
        self.text_color = BLACK
        self.speed = ENEMY_SPEED
        
        self.reached_end = False

    def move(self):
        if self.reached_end:
            return

        target_row, target_col = self.track_points[self.current_point_index]
        target_x = target_col * CELL_SIZE + CELL_SIZE // 2
        target_y = target_row * CELL_SIZE + CELL_SIZE // 2

        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.speed:
            self.current_point_index += 1
            if self.current_point_index >= len(self.track_points):
                self.reached_end = True
                return
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)
        text = self.font.render(str(self.health), True, self.text_color)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        self.screen.blit(text, text_rect)

    def is_active(self):
        return not self.reached_end