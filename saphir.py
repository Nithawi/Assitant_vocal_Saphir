#|----------|
#|          |
#|  Import  |
#|          |
#|----------|

import sounddevice as sd
from modules.voix import voix
from playsound3 import playsound
from vosk import Model, KaldiRecognizer
import queue
import json
import asyncio
import os
import edge_tts





#|---------------------------------------|
#|                                       |
#|  Constantes et variables principales  |
#|                                       |
#|---------------------------------------|

debug= True

# variables

text = ""
assistant_actif = False
commande_id = -1

# Constants

SAMPLE_RATE = 16000
MODEL_PATH = "vosk-model-small-fr-0.22"  # Path to the Vosk model directory
q = queue.Queue()

# initinalisation model

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)





#|----------------|
#|                |
#|  Dictionnaire  |
#|                |
#|----------------|

#commande dictionnaire
                   
liste_commandes = ["stop", #0
                   "bey", #1
                  ]





#|---------------------|
#|                     |
#|  Fonctions de base  |
#|                     |
#|---------------------|

# parler

def dire(phrase):
    asyncio.run(parler(phrase))

async def parler(phrase):
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

    communicate = edge_tts.Communicate(phrase, voice = "fr-CH-ArianeNeural")
    await communicate.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")

# ecouter 


def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def ecouter():
    global text
    try:
        data = q.get(timeout=2)
    except queue.Empty:
        print("micro desactivé")
        return ""
    
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result)["text"]
        if text:
            print(f"Vous avez dit: {text}")
            return text
    return ""





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

def executer_commande():
    global commande_id, assistant_actif
    if commande_id == 0 or commande_id == 1: # stop or bey
        voix("Bey")
        exit()

    elif commande_id == -1:
        dire("Désolé, je n'ai pas compris la commande, peux-tu répéter ?")
        assistant_actif = True






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

