#|----------|
#|          |
#|  Import  |
#|          |
#|----------|


import sounddevice as sd
import requests
from modules.heure import heure
from modules.sounds.voix import voix
from modules.principal.parler import dire
from modules.principal.ecouter import ecouter, audio_callback
from modules.recherche import rechercher
from modules.principal.model import SAMPLE_RATE
import modules.principal.state as state





#|---------------------------------------|
#|                                       |
#|  Constantes et variables principales  |
#|                                       |
#|---------------------------------------|



text = ""
debug = True


# id de la commande détectée
commande_id = -1





#|----------------|
#|                |
#|  Dictionnaire  |
#|                |
#|----------------|

#commande dictionnaire
                   
liste_commandes = ["stop", #0
                   "bey", #1
                   "step", #2
                   "heure", #3
                   "cherche", #4
                   "chercher", #5
                   "recherche", #6
                   "rechercher", #7
                   "augmente", #8
                   "baisse", #9
                   "météo", #10
                  ]





#|---------------------------------------|
#|                                       |
#|   Fonction de detection de commande   |
#|                                       |
#|---------------------------------------|


def detection_commande():
        global commande_id
        commande_id = -1

        #diviser la phrase en mots et vérifier si l'un d'eux correspond à une commande
        texte_split = text.lower().split()
        for mot in texte_split:
            if mot in liste_commandes:
                commande_id = liste_commandes.index(mot)
            if debug:
                    print(f"commande détectée: {mot} (id: {commande_id})")





#|---------------------------------------|
#|                                       |
#|   Fonction de execution de commande   |
#|                                       |
#|---------------------------------------|


def executer_commande():
    global commande_id

    if commande_id == -1:
        dire("Désolé, je n'ai pas compris la commande, peux-tu répéter ?")
        state.assistant_actif = True
    
    elif commande_id == 0 or commande_id == 1 or commande_id == 2: # stop or bey or step
        voix("Bey")
        exit()
    
    elif commande_id == 3: # heure
        heure()

    elif commande_id == 4 or commande_id == 5 or commande_id == 6 or commande_id == 7: # cherche
        rechercher(text)

        





#|---------------|
#|               |
#|   Main loop   |
#|               |
#|---------------|


with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype="int16", channels=1, callback=audio_callback):

    try:
        while True:
            text = ecouter()
            print("ecoute...")
            if "saphir" in text.lower():
                print(f"Vous avez dit {text}")
                voix("Bonjour")
                state.assistant_actif = True
                continue

            if state.assistant_actif and text:
                state.assistant_actif = False
                detection_commande()
                executer_commande()
        
    except KeyboardInterrupt:
        print("\nFin du programme")

