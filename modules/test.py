import json
import os
import random
from playsound3 import playsound




# son de bienvenue
def bienvenue():
    try :
        with open("voix.json", "r") as f:
            voix = json.load(f)
    except FileNotFoundError:
        print("Le fichier voix.json est introuvable. Veuillez vérifier le chemin d'accès.")
        return

    




