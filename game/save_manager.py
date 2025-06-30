"""
save_manager.py

Ce module gère la sauvegarde et le chargement des données du jeu.
"""
import json
import os

SAVE_FILE = "save_data.json"

def save_high_score(score):
    """
    Sauvegarde le high score dans un fichier.
    
    Args:
        score (int): Le score à sauvegarder
    """
    data = {'high_score': score}
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load_high_score():
    """
    Charge le high score depuis le fichier.
    
    Returns:
        int: Le high score chargé, 0 si aucun fichier n'existe
    """
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
    except (json.JSONDecodeError, IOError):
        pass
    return 0
