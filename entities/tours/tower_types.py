from enum import Enum
from typing import Type, List, Tuple, Any
from .tour_normal import TourNormal
from .tour_power import TourPower
from .tour_slow import TourSlow

class TowerType(Enum):
    """
    Enum representing different types of towers in the game.

    Each tower type is associated with a specific class and a grid type identifier.

    Attributes:
        NORMAL (tuple): Represents a normal tower with its class and grid type.
        POWER (tuple): Represents a powerful tower with its class and grid type.
        SLOW (tuple): Represents a slow tower with its class and grid type.
    """

    NORMAL = (TourNormal, 1)
    POWER = (TourPower, 2)
    SLOW = (TourSlow, 3)

    @property
    def tower_class(self) -> Type[Any]:
        """
        Returns the class associated with the tower type.

        Returns:
            Type: The class of the tower.
        """
        return self.value[0]

    @property
    def grid_type(self) -> int:
        """
        Returns the grid type identifier for the tower type.

        Returns:
            int: The grid type identifier.
        """
        return self.value[1]

    def get_cost(self) -> int:
        """
        Retrieves the cost of the tower type.

        Returns:
            int: The cost of the tower.
        """
        return self.tower_class(None, 0, 0).cost

    def get_color(self) -> Tuple[int, int, int]:
        """
        Retrieves the color of the tower type.

        Returns:
            tuple: The color of the tower (RGB format).
        """
        return self.tower_class(None, 0, 0).color

    @classmethod
    def get_all_towers(cls) -> List['TowerType']:
        """
        Retrieves all tower types defined in the enum.

        Returns:
            list: A list of all tower types.
        """
        return list(cls)