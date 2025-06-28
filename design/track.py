import pygame
from config.color import *
from config.constants import *

class Track:
    def __init__(self, screen):
        self.screen = screen
        self.line_width = TRACK_WIDTH
        self.track_color = YELLOW
        self.track = []

    def generate_random_track(self):
        import random
        row = (BOARD_HEIGHT // CELL_SIZE) // 2
        col = 0
        self.track = [(row, col)]
        visited = set(self.track)
        while col < (BOARD_WIDTH // CELL_SIZE) - 1:
            moves = []
            if row > 0 and (row - 1, col) not in visited:
                moves.append((-1, 0))  # haut
            if row < (BOARD_HEIGHT // CELL_SIZE) - 1 and (row + 1, col) not in visited:
                moves.append((1, 0))   # bas
            if (row, col + 1) not in visited:
                moves.append((0, 1))   # droite
            if not moves:
                break
            move = random.choice(moves)
            row += move[0]
            col += move[1]
            self.track.append((row, col))
            visited.add((row, col))


    def draw(self):
        if len(self.track) > 1:
            points = [(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2) for row, col in self.track]
            pygame.draw.lines(self.screen, self.track_color, False, points, self.line_width)


    def get_track(self):
        return self.track