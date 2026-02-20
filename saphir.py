#|----------|
#|          |
#|  Import  |
#|          |
#|----------|


import sounddevice as sd
from modules.heure import heure
from modules.sounds.voix import voix
from modules.principal.parler import dire
from modules.principal.ecouter import ecouter, audio_callback
import os





#|---------------------------------------|
#|                                       |
#|  Constantes et variables principales  |
#|                                       |
#|---------------------------------------|


SAMPLE_RATE = 16000
MODEL_PATH = "vosk-model-small-fr-0.22"  # Path to the Vosk model directory
text = ""
assistant_actif = False
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
                   "heure" #3
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
    global commande_id, assistant_actif

    if commande_id == -1:
        dire("Désolé, je n'ai pas compris la commande, peux-tu répéter ?")
        assistant_actif = True
    
    elif commande_id == 0 or commande_id == 1 or commande_id == 2: # stop or bey or step
        voix("Bey")
        exit()
    
    elif commande_id == 3: # heure
        heure()





#|---------------|
#|               |
#|   Main loop   |
#|               |
#|---------------|


with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype="int16", channels=1, callback=audio_callback):

    try:
        while True:
            text=ecouter()
            print("ecoute...")
            if "saphir" in text.lower():
                print(f"Vous avez dit {text}")
                voix("Bonjour")
                assistant_actif = True
                continue

            if assistant_actif and text:
                assistant_actif = False
                detection_commande()
                executer_commande()
        
    except KeyboardInterrupt:
        print("\nFin du programme")

