from enteties.tour_base import Tour
from config.color import *

class TourPower(Tour):
    def __init__(self, screen, column, row):
        Tour.__init__(self, screen, column, row)
        self.color = RED
        self.attack_range = 45  # Portée moyenne
        self.attack_speed = 2.0  # Attaque très rapide
        self.damage = 15  # Dégâts faibles mais fréquents
        self.cost = 150  # Plus chère car efficace contre les rapides
