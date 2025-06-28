from enteties.tours.tour_normal import TourNormal
from enteties.tours.tour_power import TourPower
from enteties.tours.tour_slow import TourSlow

class GameManager:
    def __init__(self):
        self.points = 300  # Points de départ
        
    def add_points(self, amount):
        """Ajoute des points au joueur"""
        self.points += amount
        print(f"Points gagnés: {amount}. Total: {self.points}")
        
    def can_afford_tower(self, tower_class):
        """Vérifie si le joueur peut acheter une tour"""
        dummy_tower = tower_class(None, 0, 0)  # Création temporaire pour accéder au coût
        return self.points >= dummy_tower.cost
        
    def buy_tower(self, tower_class):
        """Tente d'acheter une tour. Retourne True si l'achat est réussi"""
        if self.can_afford_tower(tower_class):
            dummy_tower = tower_class(None, 0, 0)
            self.points -= dummy_tower.cost
            print(f"Tour achetée! Points restants: {self.points}")
            return True
        print(f"Pas assez de points! Points disponibles: {self.points}")
        return False
        
    def get_points(self):
        """Retourne le nombre de points actuel"""
        return self.points
