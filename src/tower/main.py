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
from tower.config.constants import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    CELL_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TITLE,
)
from tower.config.color import WHITE, BLACK
import tower.design.grid as grid_module
import tower.design.track as track_module
from tower.design.enemy_wave import EnemyWave
from tower.ui.game_ui import GameUI
from tower.game.game_manager import GameManager
from tower.game.game_state import GameState
from tower.ui.menu_manager import MenuManager
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


def initialize_game(
    screen: Surface,
) -> tuple[GameState, MenuManager, GameManager, grid_module.Grid, track_module.Track, EnemyWave]:
    """Initialize game components.

    Args:
        screen: The game screen surface

    Returns:
        tuple containing initialized game components:
        - game_state: The game state instance
        - game_ui: The game UI instance
        - game_manager: The game manager instance
        - grid: The game grid instance
        - track: The game track instance
        - enemy_wave: The initial enemy wave
    """
    game_state = GameState()
    menu_manager = MenuManager(screen)
    game_manager = GameManager()

    grid = grid_module.Grid(screen)
    track = track_module.Track(screen)
    track.generate_random_track()
    track_data = track.get_track()

    enemy_wave = create_enemy_wave(screen, track_data, game_manager)

    return game_state, menu_manager, game_manager, grid, track, enemy_wave


def handle_tower_placement(
    pos: tuple[int, int],
    game_ui: GameUI,
    game_manager: GameManager,
    grid: grid_module.Grid,
    track_data: list[tuple[int, int]],
) -> None:
    """Handle tower placement logic.

    Args:
        pos: Mouse position (x, y)
        game_ui: The game UI instance
        game_manager: The game manager instance
        grid: The game grid instance
        track_data: List of track points
    """
    if (
        not any(button[0].collidepoint(pos) for button in game_ui.tower_buttons)
        and game_ui.get_selected_tower() is not None
    ):
        column = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE

        if 0 <= row < GRID_HEIGHT and 0 <= column < GRID_WIDTH:
            if (row, column) not in track_data and grid.get_grid()[row][column] == 0:
                tower_type = game_ui.get_selected_tower()
                if game_manager.buy_tower(tower_type.tower_class):
                    grid.add_tower(row, column, tower_type.grid_type)


def handle_wave_completion(
    screen: Surface,
    game_manager: GameManager,
    grid: grid_module.Grid,
    track: track_module.Track,
    wave_complete_sound: pygame.mixer.Sound,
) -> tuple[EnemyWave, grid_module.Grid, track_module.Track, list[tuple[int, int]]]:
    """
    Handle wave completion logic.

    Args:
        screen: The game screen surface
        game_manager: The game manager instance
        grid: The game grid instance
        track: The game track instance
        wave_complete_sound: The wave completion sound effect

    Returns:
        tuple containing:
        - new enemy wave
        - new grid
        - new track
        - new track data
    """
    game_manager.set_wave_completed(True)
    wave_complete_sound.play()
    pygame.time.wait(3000)

    # Créer une nouvelle grille vide et un nouveau chemin
    new_grid = grid_module.Grid(screen)
    new_track = track_module.Track(screen)
    new_track.generate_random_track()
    new_track_data = new_track.get_track()

    game_manager.next_wave()
    game_manager.add_points(game_manager.get_lives() * 10)

    enemy_wave = create_enemy_wave(screen, new_track_data, game_manager, is_new_wave=True)
    return enemy_wave, new_grid, new_track, new_track_data


def render_menu_screen(screen: Surface, menu_manager: MenuManager) -> None:
    """Render the menu screen.

    Args:
        screen: The game screen surface
        menu_manager: The menu manager instance
    """
    menu_manager.draw()
    pygame.display.flip()


def render_game_screen(
    screen: Surface,
    game_state: GameState,
    game_manager: GameManager,
    menu_manager: MenuManager,
    grid: grid_module.Grid,
    track: track_module.Track,
    enemy_wave: EnemyWave,
) -> None:
    """Render the main game screen.

    Args:
        screen: The game screen surface
        game_state: The game state instance
        game_manager: The game manager instance
        game_ui: The game UI instance
        grid: The game grid instance
        track: The game track instance
        enemy_wave: The current enemy wave
    """
    screen.fill(BLACK)
    grid.draw(enemy_wave.get_enemies(), game_manager)
    track.draw()

    game_ui = menu_manager.get_game_ui()
    game_ui.draw_points(game_manager.get_points())
    game_ui.draw_lives(game_manager.get_lives())
    game_ui.draw_high_score(game_state.get_high_score())
    game_ui.draw_tower_buttons(game_manager.get_points())
    game_ui.draw_enemy_info(enemy_wave, game_manager)

    if game_ui.get_selected_tower() is not None:
        game_ui.draw_preview(pygame.mouse.get_pos())


def run() -> None:
    """Initialize and run the main game loop."""
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Load sounds
    from tower import __file__ as tower_init
    from os.path import dirname

    base_path = dirname(tower_init)
    wave_complete_sound = pygame.mixer.Sound(join(base_path, "assets", "musics", "win_zen_crystal_melody.wav"))
    menu_music = pygame.mixer.Sound(join(base_path, "assets", "musics", "zen_menu_loop.wav"))
    game_over_music = pygame.mixer.Sound(join(base_path, "assets", "musics", "zen_death_melody.wav"))

    menu_channel = pygame.mixer.Channel(0)
    menu_channel.play(menu_music, loops=-1)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Initialize game components
    game_state, menu_manager, game_manager, grid, track, enemy_wave = initialize_game(screen)
    track_data = track.get_track()

    # Game loop
    while True:
        if game_state.get_state() == GameState.MENU:
            render_menu_screen(screen, menu_manager)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif menu_manager.handle_event(event):
                    menu_channel.stop()
                    game_state.set_state("playing")

        elif game_state.get_state() == GameState.PLAYING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    game_ui = menu_manager.get_game_ui()
                    game_ui.handle_click(pos)
                    handle_tower_placement(pos, game_ui, game_manager, grid, track_data)

            render_game_screen(screen, game_state, game_manager, menu_manager, grid, track, enemy_wave)
            enemy_wave.update()

            if game_manager.is_game_over():
                if game_state.update_high_score(game_manager.get_points()):
                    print("New high score!")
                game_state.set_state("game_over")
                game_over_music.play()

            elif enemy_wave.is_wave_complete():
                enemy_wave, grid, track, track_data = handle_wave_completion(
                    screen, game_manager, grid, track, wave_complete_sound
                )

        elif game_state.get_state() == GameState.GAME_OVER:
            screen.fill(BLACK)
            menu_manager.get_game_ui().draw_game_over(game_manager)

            font = pygame.font.Font(None, 36)
            text = font.render("Press Enter to return to the menu", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            screen.blit(text, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_over_music.stop()
                    menu_channel.stop()
                    # Réinitialiser complètement le jeu
                    game_state, menu_manager, game_manager, grid, track, enemy_wave = initialize_game(screen)
                    track_data = track.get_track()
                    menu_channel.play(menu_music, loops=-1)

        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    run()
