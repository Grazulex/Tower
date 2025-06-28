from enteties.tour_base import Tour
from config.color import *

class TourSlow(Tour):
    def __init__(self, screen, column, row):
        Tour.__init__(self, screen, column, row)
        self.color = YELLOW
        self.attack_range = 80
        self.attack_speed = 0.25
        self.damage = 500