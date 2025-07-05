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
from typing import List, Tuple
from config.constants import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    CELL_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TITLE,
)
from config.color import WHITE, BLACK
import design.grid as grid_module
import design.track as track_module
from design.enemy_wave import EnemyWave
from ui.game_ui import GameUI
from game.game_manager import GameManager
from game.game_state import GameState
from os.path import join
from pygame.surface import Surface

# Calculate grid dimensions
GRID_WIDTH = BOARD_WIDTH // CELL_SIZE
GRID_HEIGHT = BOARD_HEIGHT // CELL_SIZE


def create_enemy_wave(
    screen: Surface,
    track_data: List[Tuple[int, int]],
    game_manager: GameManager,
    is_new_wave: bool = False,
) -> EnemyWave:
    """
    Creates a new enemy wave with appropriate parameters based on the game state.

    Args:
        screen: The game screen surface
        track_data: The current track data
        game_manager: The game manager instance
        is_new_wave: Boolean indicating if this is a new wave (affects enemy count)

    Returns:
        A new EnemyWave instance
    """
    if is_new_wave:
        base_enemies = 25 + (game_manager.get_current_wave() - 1) * 5
        max_enemies = 50 + (game_manager.get_current_wave() - 1) * 5
        base_delay = max(2000 - (game_manager.get_current_wave() - 1) * 100, 500)
        num_enemies = random.randint(base_enemies, max_enemies)
        spawn_delay = random.randint(500, base_delay)
    else:
        num_enemies = random.randint(25, 50)
        spawn_delay = random.randint(500, 2000)

    return EnemyWave(
        screen,
        track_data,
        num_enemies=num_enemies,
        spawn_delay=spawn_delay,
        game_manager=game_manager,
    )


def run() -> None:
    """
    Initializes and runs the main game loop.

    Sets up the game window, initializes game components, and handles user input,
    game logic, and rendering.

    The game loop continues until the user quits or the game ends.
    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )  # Create the game window

    # Load sounds
    wave_complete_sound = pygame.mixer.Sound(
        join("assets", "musics", "win_zen_crystal_melody.wav")
    )
    menu_music = pygame.mixer.Sound(join("assets", "musics", "zen_menu_loop.wav"))
    game_over_music = pygame.mixer.Sound(
        join("assets", "musics", "zen_death_melody.wav")
    )

    menu_channel = pygame.mixer.Channel(0)
    menu_channel.play(menu_music, loops=-1)
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

    enemy_wave = create_enemy_wave(screen, track_data, game_manager)

    # Welcome screen loop
    while game_state.get_state() == GameState.MENU:
        screen.fill(BLACK)

        # Display welcome message
        font = pygame.font.Font(None, 74)
        text = font.render("Welcome to the game!", True, WHITE)
        screen.blit(
            text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 3)
        )

        play_text = font.render("Press Enter to start", True, WHITE)
        screen.blit(
            play_text,
            (WINDOW_WIDTH // 2 - play_text.get_width() // 2, WINDOW_HEIGHT // 2),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state.set_state("playing")
                # Stop menu music
                menu_channel.stop()
                # Reset the GameManager
                game_manager.reset_game()
                grid = grid_module.Grid(screen)
                grid_data = grid.get_grid()
                track = track_module.Track(screen)
                track.generate_random_track()
                track_data = track.get_track()
                enemy_wave = create_enemy_wave(screen, track_data, game_manager)

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
                game_ui.handle_click(pos)

                # Handle tower placement
                if (
                    not any(
                        button[0].collidepoint(pos) for button in game_ui.tower_buttons
                    )
                    and game_ui.get_selected_tower() is not None
                ):
                    column = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE

                    if 0 <= row < GRID_HEIGHT and 0 <= column < GRID_WIDTH:
                        # Check if the cell is valid for tower placement
                        if (row, column) not in track_data and grid_data[row][
                            column
                        ] == 0:
                            tower_type = game_ui.get_selected_tower()
                            if game_manager.buy_tower(
                                tower_type.tower_class
                            ):  # Check if the player can afford the tower
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
                print("New high score!")
            game_state.set_state("game_over")
            # Play game over music
            game_over_music.play()

            # Game over screen loop
            while game_state.get_state() == GameState.GAME_OVER:
                screen.fill(BLACK)
                game_ui.draw_game_over(game_manager)

                # Add instruction text
                font = pygame.font.Font(None, 36)
                text = font.render("Press Enter to return to the menu", True, WHITE)
                text_rect = text.get_rect(
                    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
                )
                screen.blit(text, text_rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Stop all music
                            game_over_music.stop()
                            menu_channel.stop()
                            game_state.set_state("playing")
                            game_manager.reset_game()
                            # Reset game components
                            grid = grid_module.Grid(screen)
                            grid_data = grid.get_grid()
                            track = track_module.Track(screen)
                            track.generate_random_track()
                            track_data = track.get_track()
                            enemy_wave = create_enemy_wave(
                                screen, track_data, game_manager
                            )

        # Draw tower preview if a tower is selected
        if game_ui.get_selected_tower() is not None:
            game_ui.draw_preview(pygame.mouse.get_pos())

        # Update enemy wave
        enemy_wave.update()

        # Handle wave completion
        if enemy_wave.is_wave_complete():
            game_manager.set_wave_completed(True)
            # Play wave complete sound
            wave_complete_sound.play()
            pygame.time.wait(3000)  # Wait longer for the music to play

            # Reset grid and track for the next wave
            grid = grid_module.Grid(screen)
            grid_data = grid.get_grid()

            track = track_module.Track(screen)
            track.generate_random_track()
            track_data = track.get_track()

            game_manager.next_wave()  # Progress to the next wave
            game_manager.add_points(
                game_manager.get_lives() * 10
            )  # Add points for completing the wave

            # Create new enemy wave for the next level
            enemy_wave = create_enemy_wave(
                screen, track_data, game_manager, is_new_wave=True
            )

        clock.tick(60)  # Limit the frame rate to 60 FPS
        pygame.display.flip()  # Update the display


if __name__ == "__main__":
    run()
