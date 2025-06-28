from enteties.tour_base import Tour
from config.color import *

class TourNormal(Tour):
    def __init__(self, screen, column, row):
        Tour.__init__(self, screen, column, row)
        self.color = BLUE