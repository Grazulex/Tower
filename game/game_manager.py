from enteties.tours.tour_normal import TourNormal
from enteties.tours.tour_power import TourPower
from enteties.tours.tour_slow import TourSlow

class GameManager:
    def __init__(self):
        self.points = 300  # Points de départ
        self.enemies_killed = 0
        self.current_wave = 1
        self.wave_completed = False  # Flag pour indiquer si la vague actuelle est terminée
        
    def next_wave(self):
        """Passe à la vague suivante"""
        self.current_wave += 1
        self.wave_completed = False
        
    def get_current_wave(self):
        """Retourne le numéro de la vague actuelle"""
        return self.current_wave
        
    def set_wave_completed(self, completed):
        """Définit si la vague actuelle est terminée"""
        self.wave_completed = completed
        
    def is_wave_completed(self):
        """Vérifie si la vague actuelle est terminée"""
        return self.wave_completed
        
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
        
    def enemy_killed(self):
        """Incrémente le compteur d'ennemis tués"""
        self.enemies_killed += 1
        
    def get_enemies_killed(self):
        """Retourne le nombre d'ennemis tués"""
        return self.enemies_killed
