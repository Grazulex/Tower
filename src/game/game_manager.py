from typing import Type, Any
from config.constants import STARTING_POINTS, STARTING_LIVES


class GameManager:
    """
    Manages the state and progression of the game.

    This class handles various aspects of the game, such as player points,
    waves, lives, and interactions with towers and enemies.

    Attributes:
        points (int): The player's current points.
        enemies_killed (int): The total number of enemies killed by the player.
        current_wave (int): The current wave number.
        wave_completed (bool): Indicates whether the current wave is completed.
        lives (int): The number of lives remaining for the player.
        game_over (bool): Indicates whether the game is over.
    """

    def __init__(self):
        """
        Initializes a GameManager instance with default values.
        """
        self.points = STARTING_POINTS
        self.enemies_killed = 0
        self.current_wave = 1
        self.wave_completed = False
        self.lives = STARTING_LIVES
        self.game_over = False

    def lose_life(self) -> None:
        """
        Decreases the player's lives by one. Ends the game if lives reach zero.
        """
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def get_lives(self) -> int:
        """
        Retrieves the number of lives remaining.

        Returns:
            int: The number of lives.
        """
        return self.lives

    def is_game_over(self) -> bool:
        """
        Checks if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.game_over

    def next_wave(self) -> None:
        """
        Advances to the next wave and resets the wave completion status.
        Points are intentionally carried over between waves.
        """
        self.current_wave += 1
        self.wave_completed = False
        # Points are intentionally preserved

    def get_current_wave(self) -> int:
        """
        Retrieves the current wave number.

        Returns:
            int: The current wave number.
        """
        return self.current_wave

    def set_wave_completed(self, completed: bool) -> None:
        self.wave_completed = completed

    def reset_game(self) -> None:
        """Reset the game state for a new game.
        This function is called only when a new game is started,
        not when transitioning between waves.
        """
        self.points = STARTING_POINTS  # Points are reset only for a new game
        self.lives = STARTING_LIVES
        self.current_wave = 1
        self.enemies_killed = 0
        self.wave_completed = False
        self.game_over = False

    def is_wave_completed(self) -> bool:
        """
        Checks if the current wave is completed.

        Returns:
            bool: True if the wave is completed, False otherwise.
        """
        return self.wave_completed

    def add_points(self, amount: int) -> None:
        """
        Adds points to the player's total.

        Args:
            amount (int): The number of points to add.
        """
        self.points += amount

    def can_afford_tower(self, tower_class: Type[Any]) -> bool:
        """
        Checks if the player can afford a tower of the specified class.

        Args:
            tower_class (Type): The class of the tower to check.

        Returns:
            bool: True if the player can afford the tower, False otherwise.
        """
        dummy_tower = tower_class(None, 0, 0)
        return self.points >= dummy_tower.cost

    def buy_tower(self, tower_class: Type[Any]) -> bool:
        """
        Attempts to purchase a tower of the specified class.

        Args:
            tower_class (Type): The class of the tower to purchase.

        Returns:
            bool: True if the tower was successfully purchased, False otherwise.
        """
        if self.can_afford_tower(tower_class):
            dummy_tower = tower_class(None, 0, 0)
            self.points -= dummy_tower.cost
            return True
        return False

    def get_points(self) -> int:
        """
        Retrieves the player's current points.

        Returns:
            int: The player's points.
        """
        return self.points

    def enemy_killed(self) -> None:
        """
        Increments the count of enemies killed by the player.
        """
        self.enemies_killed += 1

    def get_enemies_killed(self) -> int:
        """
        Retrieves the total number of enemies killed.

        Returns:
            int: The number of enemies killed.
        """
        return self.enemies_killed
