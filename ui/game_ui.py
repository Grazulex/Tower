import pygame
from config.color import *
from config.constants import *
from enteties.tours.tower_types import TowerType

class GameUI:
    """
    Represents the user interface for the game.

    This class handles the rendering of various UI elements such as points, lives,
    game over screen, enemy information, tower previews, and tower selection buttons.

    Attributes:
        screen (pygame.Surface): The game screen where UI elements are drawn.
        font (pygame.font.Font): Font used for rendering main text elements.
        info_font (pygame.font.Font): Font used for rendering smaller informational text.
        button_font (pygame.font.Font): Font used for rendering button text.
        tower_buttons (list): List of tower buttons available for selection.
        button_padding (int): Padding between tower buttons.
        button_size (int): Size of each tower button.
        selected_tower (TowerType): The currently selected tower type.
    """

    def __init__(self, screen):
        """
        Initializes a GameUI instance.

        Args:
            screen (pygame.Surface): The game screen where UI elements are drawn.
        """
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.info_font = pygame.font.SysFont(None, 20)
        self.button_font = pygame.font.SysFont(None, 24)
        self.tower_buttons = []
        self.button_padding = 5
        self.button_size = 30

        all_towers = TowerType.get_all_towers()
        self.selected_tower = min(all_towers, key=lambda t: t.get_cost())

    def draw_points(self, points):
        """
        Draws the player's current points on the screen.

        Args:
            points (int): The player's current points.
        """
        points_text = self.font.render(f"Points: {points}", True, WHITE)
        points_rect = points_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.screen.blit(points_text, points_rect)

    def draw_lives(self, lives):
        """
        Draws the player's remaining lives on the screen.

        Args:
            lives (int): The number of lives remaining.
        """
        lives_text = self.font.render(f"Lives: {lives}", True,
                                    RED if lives < 5 else WHITE)
        lives_rect = lives_text.get_rect(topright=(WINDOW_WIDTH - 10, 50))
        self.screen.blit(lives_text, lives_rect)

    def draw_game_over(self, game_manager):
        """
        Draws the game over screen with relevant statistics.

        Args:
            game_manager (GameManager): The game manager instance providing game statistics.
        """
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)

        wave_text = self.font.render(f"Wave reached: {game_manager.get_current_wave()}", True, WHITE)
        wave_rect = wave_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        self.screen.blit(wave_text, wave_rect)

        kills_text = self.font.render(f"Enemies killed: {game_manager.get_enemies_killed()}", True, WHITE)
        kills_rect = kills_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(kills_text, kills_rect)

    def draw_enemy_info(self, enemy_wave, game_manager):
        """
        Draws information about the current enemy wave.

        Args:
            enemy_wave (EnemyWave): The current enemy wave instance.
            game_manager (GameManager): The game manager instance providing game statistics.
        """
        x_start = BOARD_WIDTH + 10

        y_start = WINDOW_HEIGHT - 120
        wave_text = self.info_font.render(f"Wave {game_manager.get_current_wave()}", True, YELLOW)
        self.screen.blit(wave_text, (x_start, y_start))

        y_start += 30
        total_text = self.info_font.render(f"Total: {enemy_wave.get_total_enemies()}", True, WHITE)
        self.screen.blit(total_text, (x_start, y_start))

        remaining = enemy_wave.get_remaining_enemies()
        remaining_text = self.info_font.render(f"Remaining: {remaining}", True, WHITE)
        self.screen.blit(remaining_text, (x_start, y_start + 20))

        killed_text = self.info_font.render(f"Killed: {game_manager.get_enemies_killed()}", True, WHITE)
        self.screen.blit(killed_text, (x_start, y_start + 40))

        if game_manager.is_wave_completed():
            next_wave_text = self.info_font.render("Next wave...", True, GREEN)
            self.screen.blit(next_wave_text, (x_start, y_start + 60))

    def draw_preview(self, pos):
        """
        Draws a preview of the selected tower at the specified position.

        Args:
            pos (tuple): The position where the preview should be drawn (x, y).
        """
        if self.selected_tower and pos[0] < BOARD_WIDTH:
            cell_x = (pos[0] // CELL_SIZE) * CELL_SIZE
            cell_y = (pos[1] // CELL_SIZE) * CELL_SIZE

            preview_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            color = self.selected_tower.get_color()
            preview_surface.fill((color[0], color[1], color[2], 128))
            self.screen.blit(preview_surface, (cell_x, cell_y))

    def draw_tower_buttons(self, current_points):
        """
        Draws buttons for selecting towers based on the player's current points.

        Args:
            current_points (int): The player's current points.
        """
        self.tower_buttons.clear()

        y_start = 100

        for i, tower_type in enumerate(TowerType.get_all_towers()):
            cost = tower_type.get_cost()
            color = tower_type.get_color()
            can_afford = current_points >= cost

            ui_x = BOARD_WIDTH + 10
            y = y_start + i * (self.button_size + self.button_padding)
            button_rect = pygame.Rect(ui_x, y, self.button_size, self.button_size)

            button_color = color if can_afford else (color[0]//2, color[1]//2, color[2]//2)
            if self.selected_tower == tower_type:
                pygame.draw.rect(self.screen, WHITE, button_rect, 3)
            pygame.draw.rect(self.screen, button_color, button_rect)

            text_color = WHITE if can_afford else (128, 128, 128)
            cost_text = self.button_font.render(str(cost), True, text_color)
            cost_rect = cost_text.get_rect(midleft=(ui_x + self.button_size + 5, y + self.button_size//2))
            self.screen.blit(cost_text, cost_rect)

            click_rect = pygame.Rect(ui_x, y, self.button_size + 50, self.button_size)
            self.tower_buttons.append((click_rect, tower_type, can_afford))

        pygame.draw.line(self.screen, WHITE,
                        (BOARD_WIDTH, 0),
                        (BOARD_WIDTH, WINDOW_HEIGHT),
                        2)

    def handle_click(self, pos, current_points):
        """
        Handles click events for tower selection buttons.

        Args:
            pos (tuple): The position of the click (x, y).
            current_points (int): The player's current points.

        Returns:
            TowerType: The selected tower type, or None if no tower is selected.
        """
        for button_rect, tower_type, can_afford in self.tower_buttons:
            if button_rect.collidepoint(pos):
                if can_afford:
                    if self.selected_tower == tower_type:
                        self.selected_tower = None
                    else:
                        self.selected_tower = tower_type
                return self.selected_tower
        return self.selected_tower

    def get_selected_tower(self):
        """
        Retrieves the currently selected tower type.

        Returns:
            TowerType: The selected tower type, or None if no tower is selected.
        """
        return self.selected_tower
