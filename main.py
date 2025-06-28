import pygame
from sys import exit
from config.constants import *
from config.color import *
import design.grid as grid_module
import design.track as track_module


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos= pygame.mouse.get_pos()
                print(pos)
                column = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                print(f"Clicked on cell: ({row}, {column})")
                grid_data[row][column] = 1

        screen.fill(BLACK)
        grid.draw()
        track.draw()

        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    run()

