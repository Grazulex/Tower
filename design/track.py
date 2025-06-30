import pygame
from config.color import *
from config.constants import *

class Track:
    """
    Represents the track for enemy movement in the game.

    Attributes:
        screen (pygame.Surface): The game screen where the track is drawn.
        line_width (int): The width of the track lines.
        track_color (tuple): The color of the track lines.
        track (list): A list of tuples representing the track points (row, column).
    """

    def __init__(self, screen):
        """
        Initializes the Track instance.

        Args:
            screen (pygame.Surface): The game screen where the track is drawn.
        """
        self.screen = screen
        self.line_width = TRACK_WIDTH
        self.track_color = YELLOW
        self.track = []

    def generate_random_track(self):
        """
        Generates a random track for enemy movement.

        The track starts at the middle of the first column and progresses
        randomly to the right while avoiding revisiting cells.

        Uses:
            random: To randomly select the next move.

        The track is stored as a list of tuples representing grid positions.
        """
        import random
        row = (BOARD_HEIGHT // CELL_SIZE) // 2
        col = 0
        self.track = [(row, col)]
        visited = set(self.track)
        while col < (BOARD_WIDTH // CELL_SIZE) - 1:
            moves = []
            if row > 0 and (row - 1, col) not in visited:
                moves.append((-1, 0))  # Move up
            if row < (BOARD_HEIGHT // CELL_SIZE) - 1 and (row + 1, col) not in visited:
                moves.append((1, 0))   # Move down
            if (row, col + 1) not in visited:
                moves.append((0, 1))   # Move right
            if not moves:
                break
            move = random.choice(moves)
            row += move[0]
            col += move[1]
            self.track.append((row, col))
            visited.add((row, col))

    def draw(self):
        """
        Draws the track on the game screen.

        The track is drawn as a series of connected lines between the track points.
        """
        if len(self.track) > 1:
            points = [(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2) for row, col in self.track]
            pygame.draw.lines(self.screen, self.track_color, False, points, self.line_width)

    def get_track(self):
        """
        Gets the current track.

        Returns:
            list: A list of tuples representing the track points (row, column).
        """
        return self.track