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
    enemy_wave = EnemyWave(screen, track_data, num_enemies=random.randint(15,25), spawn_delay=random.randint(500, 2000), game_manager=game_manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                print(f"Clicked on cell: ({row}, {column})")
                if (row, column) not in track_data:
                    current_type = grid_data[row][column]
                    print(f"Current tower type: {current_type}")
                    
                    if current_type == 0:
                        if game_manager.buy_tower(TourNormal):
                            grid.add_tower(row, column, 1)
                            print("Adding normal tower")
                    elif current_type == 1:
                        if game_manager.buy_tower(TourPower):
                            grid.remove_tower(row, column)
                            grid.add_tower(row, column, 2)
                            print("Upgrading to power tower")
                    elif current_type == 2:
                        if game_manager.buy_tower(TourSlow):
                            grid.remove_tower(row, column)
                            grid.add_tower(row, column, 3)
                            print("Upgrading to slow tower")
                    elif current_type == 3:
                        grid.remove_tower(row, column)
                        print("Removing tower")
                    
                    # Mettre à jour grid_data avec le nouveau type
                    grid_data = grid.get_grid()
        screen.fill(BLACK)
        grid.draw(enemy_wave.get_enemies(), game_manager)
        track.draw()

        # Afficher l'interface utilisateur
        game_ui.draw_points(game_manager.get_points())
        game_ui.draw_tower_costs()

        # Mettre à jour la vague d'ennemis
        enemy_wave.update()

        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    run()

