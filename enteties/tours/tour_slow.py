from enteties.tour_base import Tour
from config.color import *

class TourSlow(Tour):
    def __init__(self, screen, column, row):
        Tour.__init__(self, screen, column, row)
        self.color = YELLOW
        self.attack_range = 90  # Grande portée
        self.attack_speed = 0.5  # Attaque lente
        self.damage = 75  # Dégâts élevés
        self.cost = 175  # La plus chère car très puissante
