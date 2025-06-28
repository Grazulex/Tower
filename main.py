import pygame
import random
from sys import exit
from config.constants import *
from config.color import *
import design.grid as grid_module
import design.track as track_module
from design.enemy_wave import EnemyWave
from ui.game_ui import GameUI
from game.game_manager import GameManager
from enteties.tours.tour_normal import TourNormal
from enteties.tours.tour_power import TourPower
from enteties.tours.tour_slow import TourSlow


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    grid = grid_module.Grid(screen)
    grid_data = grid.get_grid()

    # Initialisation de l'UI et du GameManager
    game_ui = GameUI(screen)
    game_manager = GameManager()

    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()

    # Créer une vague d'ennemis
    enemy_wave = EnemyWave(screen, track_data, num_enemies=random.randint(25,50), spawn_delay=random.randint(500, 2000), game_manager=game_manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # D'abord, vérifier si on clique sur un bouton de tour
                game_ui.handle_click(pos, game_manager.get_points())
                
                # Si on n'a pas cliqué sur un bouton et qu'une tour est sélectionnée,
                # essayer de placer la tour
                if not any(button[0].collidepoint(pos) for button in game_ui.tower_buttons) and game_ui.get_selected_tower() is not None:
                    column = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE
                    print(f"Trying to place tower at: ({row}, {column})")
                    
                    if (row, column) not in track_data and grid_data[row][column] == 0:
                        tower_type = game_ui.get_selected_tower()
                        if game_manager.buy_tower(tower_type.tower_class):
                            grid.add_tower(row, column, tower_type.grid_type)
                            print(f"Adding {tower_type.name.lower()} tower")
                            # Garder la sélection pour pouvoir placer plusieurs tours du même type
                    
                    # Mettre à jour grid_data avec le nouveau type
                    grid_data = grid.get_grid()
        screen.fill(BLACK)
        grid.draw(enemy_wave.get_enemies(), game_manager)
        track.draw()

        # Afficher l'interface utilisateur
        game_ui.draw_points(game_manager.get_points())
        game_ui.draw_lives(game_manager.get_lives())
        game_ui.draw_tower_buttons(game_manager.get_points())
        game_ui.draw_enemy_info(enemy_wave, game_manager)
        
# Si game over, afficher l'écran de fin
        if game_manager.is_game_over():
            game_ui.draw_game_over(game_manager)
            pygame.display.flip()
            pygame.time.wait(3000)  # Attendre 3 secondes
            pygame.quit()
            exit()
        
        # Afficher l'aperçu de la tour sélectionnée
        if game_ui.get_selected_tower() is not None:
            game_ui.draw_preview(pygame.mouse.get_pos())

        # Mettre à jour la vague d'ennemis
        enemy_wave.update()
        
        # Si la vague est terminée, passer à la suivante
        if enemy_wave.is_wave_complete():
            game_manager.set_wave_completed(True)
            pygame.time.wait(2000)  # Petite pause avant la prochaine vague
            
            # Réinitialiser la grille (enlève toutes les tours)
            grid = grid_module.Grid(screen)
            grid_data = grid.get_grid()
            
            # Générer un nouveau chemin aléatoire
            track = track_module.Track(screen)
            track.generate_random_track()
            track_data = track.get_track()
            
            # Passer à la vague suivante
            game_manager.next_wave()
            
            # Créer une nouvelle vague avec le nouveau chemin
            # Augmenter progressivement le nombre d'ennemis et réduire le délai d'apparition
            base_enemies = 25 + (game_manager.get_current_wave() - 1) * 5  # 5 ennemis de plus par vague
            max_enemies = 50 + (game_manager.get_current_wave() - 1) * 5
            base_delay = max(2000 - (game_manager.get_current_wave() - 1) * 100, 500)  # Réduit de 100ms par vague, minimum 500ms
            
            enemy_wave = EnemyWave(
                screen, 
                track_data, 
                num_enemies=random.randint(base_enemies, max_enemies),
                spawn_delay=random.randint(500, base_delay), 
                game_manager=game_manager)

        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    run()

