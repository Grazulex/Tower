import json
import os
import bcrypt
from typing import Dict, Optional


class Player:
    def __init__(self, username: str, password: str, is_password_hashed: bool = False):
        self.username = username
        # Hash le mot de passe s'il ne l'est pas déjà
        if is_password_hashed:
            self.password = password
        else:
            self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.scores = []

    def check_password(self, password: str) -> bool:
        """Vérifie si le mot de passe correspond."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def to_dict(self) -> Dict:
        return {"username": self.username, "password": self.password, "scores": self.scores}

    @classmethod
    def from_dict(cls, data: Dict) -> "Player":
        player = cls(data["username"], data["password"], is_password_hashed=True)
        player.scores = data.get("scores", [])
        return player


class PlayerManager:
    SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "players.json")
    _current_player: Optional[Player] = None

    @classmethod
    def save_players(cls, players: Dict[str, Player]) -> None:
        data = {username: player.to_dict() for username, player in players.items()}
        with open(cls.SAVE_FILE, "w") as f:
            json.dump(data, f)

    @classmethod
    def load_players(cls) -> Dict[str, Player]:
        if not os.path.exists(cls.SAVE_FILE):
            return {}

        with open(cls.SAVE_FILE, "r") as f:
            data = json.load(f)
            return {username: Player.from_dict(player_data) for username, player_data in data.items()}

    @classmethod
    def create_player(cls, username: str, password: str) -> bool:
        players = cls.load_players()
        # Vérifier si le nom d'utilisateur existe déjà (insensible à la casse)
        username_lower = username.lower()
        if any(p.username.lower() == username_lower for p in players.values()):
            return False

        players[username] = Player(username, password)
        cls.save_players(players)
        return True

    @classmethod
    def login_player(cls, username: str, password: str) -> bool:
        players = cls.load_players()
        # Recherche insensible à la casse
        username_lower = username.lower()
        player = next((p for p in players.values() if p.username.lower() == username_lower), None)

        if player and player.check_password(password):
            cls._current_player = player
            return True
        return False

    @classmethod
    def get_current_player(cls) -> Optional[Player]:
        return cls._current_player

    @classmethod
    def save_score(cls, score: int) -> bool:
        if not cls._current_player:
            return False

        # Ne pas ajouter le score s'il est déjà présent
        if score not in cls._current_player.scores:
            cls._current_player.scores.append(score)
            players = cls.load_players()
            players[cls._current_player.username] = cls._current_player
            cls.save_players(players)
        return True

    @classmethod
    def get_high_scores(cls, username: str) -> list:
        players = cls.load_players()
        player = players.get(username)
        if player:
            return sorted(player.scores, reverse=True)
        return []
