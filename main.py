import pygame
import random
from sys import exit
from config.constants import *
from config.color import *
import design.grid as grid_module
import design.track as track_module
from design.enemy_wave import EnemyWave


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    grid = grid_module.Grid(screen)
    grid_data = grid.get_grid()

    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()

    # Créer une vague de 5 ennemis avec 1 seconde (1000ms) entre chaque spawn
    enemy_wave = EnemyWave(screen, track_data, num_enemies=random.randint(15,25), spawn_delay=random.randint(500, 2000))

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
                        grid.add_tower(row, column, 1)
                        print("Adding normal tower")
                    elif current_type == 1:
                        grid.remove_tower(row, column)
                        grid.add_tower(row, column, 2)
                        print("Upgrading to power tower")
                    elif current_type == 2:
                        grid.remove_tower(row, column)
                        grid.add_tower(row, column, 3)
                        print("Upgrading to slow tower")
                    elif current_type == 3:
                        grid.remove_tower(row, column)
                        print("Removing tower")
                    
                    # Mettre à jour grid_data avec le nouveau type
                    grid_data = grid.get_grid()
        screen.fill(BLACK)
        grid.draw(enemy_wave.get_enemies())
        track.draw()

        # Mettre à jour la vague d'ennemis
        enemy_wave.update()

        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    run()

