import pygame
from config.constants import *
from config.color import *

class Tour:
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

    def __init__(self, screen, column, row):
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

    def draw(self, enemies, game_manager):
        """
        Draws the tower on the screen and handles its attack logic.

        Args:
            enemies (list): A list of Enemy objects currently in the game.
            game_manager (GameManager): The game manager handling game state.
        """
        pygame.draw.rect(self.screen, self.color,
                         (self.cell_size * self.column, self.cell_size * self.row, self.cell_size, self.cell_size))

        text = self.font.render(str(self.damage), True, self.text_color)
        text_rect = text.get_rect(center=(int(self.cell_size * self.column)+(self.cell_size//2), int(self.cell_size * self.row)+(self.cell_size//2)))
        self.screen.blit(text, text_rect)

        center_x = self.cell_size * self.column + self.cell_size // 2
        center_y = self.cell_size * self.row + self.cell_size // 2
        pygame.draw.circle(self.screen, GRAY, (center_x, center_y), self.attack_range, 1)
        if enemies:
            enemies_in_range = []
            for enemy in enemies:
                distance = ((enemy.x - center_x) ** 2 + (enemy.y - center_y) ** 2) ** 0.5
                if distance <= self.attack_range:
                    enemies_in_range.append(enemy)

            if enemies_in_range:
                current_time = pygame.time.get_ticks()

                attack_delay = (1 / self.attack_speed) * 1000
                time_since_last_attack = current_time - self.last_attack_time
                if time_since_last_attack >= attack_delay:
                    target = min(enemies_in_range, key=lambda e: e.health)
                    self.attack(target)
                    self.last_attack_time = current_time

                    self.is_attacking = True
                    self.current_target = target

                if self.is_attacking:
                    attack_animation_time = current_time - self.last_attack_time
                    if attack_animation_time <= self.attack_animation_duration:
                        pygame.draw.line(self.screen, RED, (center_x, center_y),
                                       (self.current_target.x, self.current_target.y), 3)
                    else:
                        self.is_attacking = False
                        self.current_target = None

    def attack(self, enemy):
        """
        Attacks the specified enemy, reducing its health.

        Args:
            enemy (Enemy): The enemy to attack.
        """
        enemy.take_damage(self.damage)