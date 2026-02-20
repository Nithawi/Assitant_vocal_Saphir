
from playsound3 import playsound
import json
import random


# son de bienvenue
def voix(Category):
    try :
        with open("voix.json", "r") as f:
            voix = json.load(f)
    except FileNotFoundError:
        print("Le fichier voix.json est introuvable. Veuillez vérifier le chemin d'accès.")
        return
    try :
        if Category in voix:
            sound = random.choice(voix[Category])
            playsound(sound["file"])
        else:
            print(f"Aucun son de {Category} trouvé dans le fichier voix.json.")
    except KeyError:
        print(f"Catégorie {Category} non trouvée dans le fichier voix.json.")


        