"""
main.py

This script initializes and runs a tower defense game using the Pygame library.
It handles game setup, user interactions, game logic, and rendering.

Modules:
- pygame: Used for game rendering and event handling.
- random: Used for generating random values for enemy waves and track generation.
- sys: Used for exiting the program.
- config.constants: Contains game constants like window dimensions and title.
- config.color: Contains color definitions used in the game.
- design.grid: Manages the game grid where towers are placed.
- design.track: Manages the track for enemy movement.
- design.enemy_wave: Handles enemy wave generation and updates.
- ui.game_ui: Manages the user interface elements.
- game.game_manager: Handles game state, points, lives, and wave progression.

Functions:
- run(): Initializes the game, handles the main game loop, and manages game logic.
"""

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
from game.game_state import GameState

def run():
    """
    Initializes and runs the main game loop.

    Sets up the game window, initializes game components, and handles user input,
    game logic, and rendering.

    The game loop continues until the user quits or the game ends.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Create the game window
    pygame.display.set_caption(TITLE)  # Set the window title
    clock = pygame.time.Clock()  # Initialize the game clock

    # Initialize game state
    game_state = GameState()

    # Initialize game components
    grid = grid_module.Grid(screen)
    grid_data = grid.get_grid()

    game_ui = GameUI(screen)
    game_manager = GameManager()

    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()

    enemy_wave = EnemyWave(
        screen,
        track_data,
        num_enemies=random.randint(25, 50),
        spawn_delay=random.randint(500, 2000),
        game_manager=game_manager
    )

    # Welcome screen loop
    while game_state.get_state() == GameState.MENU:
        screen.fill(BLACK)

        # Display welcome message
        font = pygame.font.Font(None, 74)
        text = font.render('Bienvenue au jeu!', True, WHITE)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 3))

        play_text = font.render('Appuyez sur Entrée pour commencer', True, WHITE)
        screen.blit(play_text, (WINDOW_WIDTH // 2 - play_text.get_width() // 2, WINDOW_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state.set_state(GameState.PLAYING)
                # Créer un nouveau GameManager pour une nouvelle partie
                game_manager = GameManager()

    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit event
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
                pos = pygame.mouse.get_pos()

                # Handle UI button clicks
                game_ui.handle_click(pos, game_manager.get_points())

                # Handle tower placement
                if not any(button[0].collidepoint(pos) for button in game_ui.tower_buttons) and game_ui.get_selected_tower() is not None:
                    column = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE

                    # Check if the cell is valid for tower placement
                    if (row, column) not in track_data and grid_data[row][column] == 0:
                        tower_type = game_ui.get_selected_tower()
                        if game_manager.buy_tower(tower_type.tower_class):  # Check if the player can afford the tower
                            grid.add_tower(row, column, tower_type.grid_type)
                    grid_data = grid.get_grid()

        # Game rendering
        screen.fill(BLACK)  # Clear the screen
        grid.draw(enemy_wave.get_enemies(), game_manager)  # Draw the grid and towers
        track.draw()  # Draw the track

        # Draw UI elements
        game_ui.draw_points(game_manager.get_points())
        game_ui.draw_lives(game_manager.get_lives())
        game_ui.draw_high_score(game_state.get_high_score())
        game_ui.draw_tower_buttons(game_manager.get_points())
        game_ui.draw_enemy_info(enemy_wave, game_manager)

        # Check for game over
        if game_manager.is_game_over():
            # Update high score
            if game_state.update_high_score(game_manager.get_points()):
                print('New high score!')
            game_state.set_state(GameState.GAME_OVER)

            # Game over screen loop
            while game_state.get_state() == GameState.GAME_OVER:
                screen.fill(BLACK)
                game_ui.draw_game_over(game_manager)
                
                # Add instruction text
                font = pygame.font.Font(None, 36)
                text = font.render('Appuyez sur Entrée pour retourner au menu', True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
                screen.blit(text, text_rect)
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game_state.set_state(GameState.MENU)
                            # Créer un nouveau GameManager pour une nouvelle partie
                            game_manager = GameManager()
                            # Reset game components
                            grid = grid_module.Grid(screen)
                            grid_data = grid.get_grid()
                            track = track_module.Track(screen)
                            track.generate_random_track()
                            track_data = track.get_track()
                            enemy_wave = EnemyWave(
                                screen,
                                track_data,
                                num_enemies=random.randint(25, 50),
                                spawn_delay=random.randint(500, 2000),
                                game_manager=game_manager
                            )

        # Draw tower preview if a tower is selected
        if game_ui.get_selected_tower() is not None:
            game_ui.draw_preview(pygame.mouse.get_pos())

        # Update enemy wave
        enemy_wave.update()

        # Handle wave completion
        if enemy_wave.is_wave_complete():
            game_manager.set_wave_completed(True)
            pygame.time.wait(2000)

            # Reset grid and track for the next wave
            grid = grid_module.Grid(screen)
            grid_data = grid.get_grid()

            track = track_module.Track(screen)
            track.generate_random_track()
            track_data = track.get_track()

            game_manager.next_wave()  # Progress to the next wave

            # Generate new enemy wave parameters
            base_enemies = 25 + (game_manager.get_current_wave() - 1) * 5
            max_enemies = 50 + (game_manager.get_current_wave() - 1) * 5
            base_delay = max(2000 - (game_manager.get_current_wave() - 1) * 100, 500)

            enemy_wave = EnemyWave(
                screen,
                track_data,
                num_enemies=random.randint(base_enemies, max_enemies),
                spawn_delay=random.randint(500, base_delay),
                game_manager=game_manager
            )

        clock.tick(60)  # Limit the frame rate to 60 FPS
        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    run()