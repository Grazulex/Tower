import pygame
from config.color import *
from config.constants import *
from enteties.tours.tower_types import TowerType

class GameUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)  # Police plus grande pour le score
        self.info_font = pygame.font.SysFont(None, 20)  # Police plus petite pour les infos
        self.button_font = pygame.font.SysFont(None, 24)
        self.tower_buttons = []  # Liste de tuples (rect, tower_type, can_afford)
        self.button_padding = 5
        self.button_size = 30  # Taille du carré de couleur
        
        # Sélectionner par défaut la tour la moins chère
        all_towers = TowerType.get_all_towers()
        self.selected_tower = min(all_towers, key=lambda t: t.get_cost())
        
    def draw_points(self, points):
        """Affiche le nombre de points du joueur"""
        points_text = self.font.render(f"Points: {points}", True, WHITE)
        points_rect = points_text.get_rect(topleft=(BOARD_WIDTH + 10, 10))  # Position dans la zone UI
        self.screen.blit(points_text, points_rect)
        
    def draw_enemy_info(self, enemy_wave, game_manager):
        """Affiche les informations sur les ennemis et la vague"""
        x_start = BOARD_WIDTH + 10
        
        # Affichage du numéro de la vague (en haut des informations)
        y_start = WINDOW_HEIGHT - 120
        wave_text = self.info_font.render(f"Vague {game_manager.get_current_wave()}", True, YELLOW)
        self.screen.blit(wave_text, (x_start, y_start))
        
        # Informations sur les ennemis
        y_start += 30
        # Nombre total d'ennemis dans la vague
        total_text = self.info_font.render(f"Total: {enemy_wave.get_total_enemies()}", True, WHITE)
        self.screen.blit(total_text, (x_start, y_start))
        
        # Nombre d'ennemis restants
        remaining = enemy_wave.get_remaining_enemies()
        remaining_text = self.info_font.render(f"Restants: {remaining}", True, WHITE)
        self.screen.blit(remaining_text, (x_start, y_start + 20))
        
        # Nombre d'ennemis tués
        killed_text = self.info_font.render(f"Tués: {game_manager.get_enemies_killed()}", True, WHITE)
        self.screen.blit(killed_text, (x_start, y_start + 40))
        
        # Si la vague est terminée, afficher un message
        if game_manager.is_wave_completed():
            next_wave_text = self.info_font.render("Prochaine vague...", True, GREEN)
            self.screen.blit(next_wave_text, (x_start, y_start + 60))
        
    def draw_preview(self, pos):
        """Affiche un aperçu de la tour sélectionnée sous le curseur"""
        if self.selected_tower and pos[0] < BOARD_WIDTH:  # Seulement si le curseur est dans la zone de jeu
            # Calculer la position de la cellule
            cell_x = (pos[0] // CELL_SIZE) * CELL_SIZE
            cell_y = (pos[1] // CELL_SIZE) * CELL_SIZE
            
            # Dessiner un carré semi-transparent
            preview_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            color = self.selected_tower.get_color()
            preview_surface.fill((color[0], color[1], color[2], 128))  # Alpha = 128 pour semi-transparent
            self.screen.blit(preview_surface, (cell_x, cell_y))
    
    def draw_tower_buttons(self, current_points):
        """Affiche les boutons de sélection des tours"""
        self.tower_buttons.clear()
        
        for i, tower_type in enumerate(TowerType.get_all_towers()):
            cost = tower_type.get_cost()
            color = tower_type.get_color()
            can_afford = current_points >= cost
            
            # Calculer la position du bouton
            ui_x = BOARD_WIDTH + 10
            y = 50 + i * (self.button_size + self.button_padding)
            button_rect = pygame.Rect(ui_x, y, self.button_size, self.button_size)
            
            # Dessiner le carré de couleur
            button_color = color if can_afford else (color[0]//2, color[1]//2, color[2]//2)
            if self.selected_tower == tower_type:
                # Ajouter une bordure pour la tour sélectionnée
                pygame.draw.rect(self.screen, WHITE, button_rect, 3)
            pygame.draw.rect(self.screen, button_color, button_rect)
            
            # Ajouter le coût à droite du carré
            text_color = WHITE if can_afford else (128, 128, 128)
            cost_text = self.button_font.render(str(cost), True, text_color)
            cost_rect = cost_text.get_rect(midleft=(ui_x + self.button_size + 5, y + self.button_size//2))
            self.screen.blit(cost_text, cost_rect)
            
            # Stocker le rectangle et le type de tour pour la détection des clics
            click_rect = pygame.Rect(ui_x, y, self.button_size + 50, self.button_size)  # Zone cliquable élargie
            self.tower_buttons.append((click_rect, tower_type, can_afford))
            
        # Dessiner une ligne verticale pour séparer le jeu de l'UI
        pygame.draw.line(self.screen, WHITE, 
                        (BOARD_WIDTH, 0),
                        (BOARD_WIDTH, WINDOW_HEIGHT),
                        2)
    
    def handle_click(self, pos, current_points):
        """Gère les clics sur les boutons de tours"""
        for button_rect, tower_type, can_afford in self.tower_buttons:
            if button_rect.collidepoint(pos):
                if can_afford:
                    # Si on clique sur la tour déjà sélectionnée, on la désélectionne
                    if self.selected_tower == tower_type:
                        self.selected_tower = None
                    else:
                        self.selected_tower = tower_type
                return self.selected_tower
        return self.selected_tower
    
    def get_selected_tower(self):
        """Retourne le type de tour actuellement sélectionné"""
        return self.selected_tower
