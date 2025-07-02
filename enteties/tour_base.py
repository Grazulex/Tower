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

    def play_attack_sound(self):
        """
        Méthode à surcharger dans les classes filles pour jouer le son d'attaque spécifique.
        """
        pass

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
        # Créer un dégradé du haut vers le bas
        for i in range(self.cell_size):
            progress = i / self.cell_size
            # Assombrir légèrement la couleur pour le bas de la tour
            gradient_color = (
                max(0, self.color[0] - int(TOWER_GRADIENT_INTENSITY * progress)),
                max(0, self.color[1] - int(TOWER_GRADIENT_INTENSITY * progress)),
                max(0, self.color[2] - int(TOWER_GRADIENT_INTENSITY * progress))
            )
            pygame.draw.line(
                self.screen,
                gradient_color,
                (self.cell_size * self.column, self.cell_size * self.row + i),
                (self.cell_size * (self.column + 1), self.cell_size * self.row + i)
            )

        #text = self.font.render(str(self.damage), True, self.text_color)
        #text_rect = text.get_rect(center=(int(self.cell_size * self.column)+(self.cell_size//2), int(self.cell_size * self.row)+(self.cell_size//2)))
        #self.screen.blit(text, text_rect)

        center_x = self.cell_size * self.column + self.cell_size // 2
        center_y = self.cell_size * self.row + self.cell_size // 2
        
        # Créer une surface avec canal alpha pour le périmètre de tir
        range_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2), pygame.SRCALPHA)
        
        # Dessiner plusieurs cercles concentriques avec différentes transparences
        for r in range(self.attack_range, self.attack_range - RANGE_CIRCLES_COUNT, -1):
            # Calculer l'alpha en fonction de la position du cercle
            progress = (r - (self.attack_range - RANGE_CIRCLES_COUNT)) / RANGE_CIRCLES_COUNT
            alpha = int(RANGE_MIN_ALPHA + (RANGE_MAX_ALPHA - RANGE_MIN_ALPHA) * progress)
            
            # Utiliser une couleur légèrement teintée selon la couleur de la tour
            range_color = (
                min(255, self.color[0] + RANGE_COLOR_INTENSITY),
                min(255, self.color[1] + RANGE_COLOR_INTENSITY),
                min(255, self.color[2] + RANGE_COLOR_INTENSITY),
                alpha
            )
            pygame.draw.circle(range_surface, range_color, (self.attack_range, self.attack_range), r, 1)
        
        # Ajouter un effet de brillance très subtil
        glow_color = (255, 255, 255, RANGE_GLOW_ALPHA)
        pygame.draw.circle(range_surface, glow_color, (self.attack_range, self.attack_range), self.attack_range - 1, 1)
        
        # Afficher la surface du périmètre
        self.screen.blit(range_surface, (center_x - self.attack_range, center_y - self.attack_range))
        if enemies:
            enemies_in_range = []
            for enemy in enemies:
                distance = ((enemy.x - center_x) ** 2 + (enemy.y - center_y) ** 2) ** 0.5
                if distance <= self.attack_range:
                    enemies_in_range.append(enemy)

            if enemies_in_range:
                current_time = pygame.time.get_ticks()

                # Filtrer les ennemis valides (vivants et visibles)
                valid_enemies = [e for e in enemies_in_range if e.visible and e.health > 0]
                
                if valid_enemies:
                    attack_delay = (1 / self.attack_speed) * 1000
                    time_since_last_attack = current_time - self.last_attack_time
                    if time_since_last_attack >= attack_delay:
                        target = min(valid_enemies, key=lambda e: e.health)
                        # Vérifier une dernière fois que la cible est toujours valide
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

    def attack(self, enemy):
        """
        Attacks the specified enemy, reducing its health.

        Args:
            enemy (Enemy): The enemy to attack.
        """
        enemy.take_damage(self.damage)