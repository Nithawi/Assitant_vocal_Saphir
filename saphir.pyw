#|----------|
#|          |
#|  Import  |
#|          |
#|----------|


import os

import sounddevice as sd
from modules.heure import heure
from modules.sounds.voix import voix
from modules.principal.parler import dire
from modules.principal.ecouter import ecouter, audio_callback
from modules.recherche import rechercher
from modules.principal.model import SAMPLE_RATE
from modules.meteo import meteo
import modules.principal.state as state
import time
from playsound3 import playsound

#interface 
import threading
import json
import webview





#|---------------------------------------|
#|                                       |
#|  Constantes et variables principales  |
#|                                       |
#|---------------------------------------|



text = ""
debug = True
text_mode = True
commande_par_texte = False


# id de la commande détectée
commande_id = -1

# -- référence à la fenêtre de l'interface graphique
window_ref = None



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
                   "heures", #4
                   "leur", #5
                   "cherche", #6
                   "chercher", #7
                   "recherche", #8
                   "rechercher", #9
                   "météo", #10
                   "meteo", #11
                   "rien", #12
                   "veille" #13
                  ]


#|---------------------------------------|
#|                                       |
#|  Fonctions d'envoi vers l'interface   |
#|  (Python → JavaScript)                |
#|                                       |
#|---------------------------------------|
 
# Ces 3 fonctions appellent du JavaScript dans la fenêtre PyWebView.
# Elles sont appelées depuis ta boucle existante pour mettre à jour l'UI.
 
def ui_status(status):
    """Change l'état visuel affiché : 'idle' | 'active' | 'speaking' | 'off'"""
    if window_ref:
        window_ref.evaluate_js(f"uiSetStatus({json.dumps(status)})")


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
        dire("Désolé, je n'ai pas compris la commande.")
        state.assistant_actif = False

    
    elif commande_id == 0 or commande_id == 1 or commande_id == 2: # stop or bey or step
        voix("Bey")
        window_ref.destroy()
        exit()
    
    elif commande_id == 3 or commande_id == 4 or commande_id == 5: # heure
        heure()

    elif commande_id == 6 or commande_id == 7 or commande_id == 8 or commande_id == 9: # cherche
        rechercher(text)

    elif commande_id == 10 or commande_id == 11: # météo
        meteo()

    elif commande_id == 12 or commande_id == 13: # rien or veille
        dire("Ok, je me met en veille.")
        state.assistant_actif = False





#|---------------|
#|               |
#|   Main loop   |
#|               |
#|---------------|

# Cette fonction contient la boucle principale de l'assistant vocal.
 
def boucle_saphir():
    global text
 
    ui_status("idle")

    try:
        playsound("modules/sounds/start.mp3")
    except Exception as e:
        print(f"Erreur son démarrage: {e}")
 
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype="int16", channels=1, callback=audio_callback):
        try:
            while True:
                if not getattr(state, 'micro', True):
                    time.sleep(0.2)
                    continue

                text = ecouter()
                print("ecoute...")
 
                if "saphir" in text.lower():
                    print(f"Vous avez dit {text}")
                    ui_status("speaking") 
                    voix("Bonjour")
                    
                    if os.path.exists("temp.mp3"):
                        try: os.remove("temp.mp3")
                        except: pass

                    ui_status("active")
                    state.assistant_actif = True
                    try:
                        playsound("modules/sounds/activation.mp3")
                    except Exception as e:
                        print(f"Erreur son activation: {e}")
                    continue
 
                if state.assistant_actif and text:
                    state.assistant_actif = False 
                    detection_commande()

                    ui_status("speaking") 
                    executer_commande()   
                    
                    if os.path.exists("temp.mp3"):
                        try: os.remove("temp.mp3")
                        except: pass
                    
                    if state.assistant_actif:
                        ui_status("active")
                    else:
                        ui_status("idle") 
                        continue
 
        except KeyboardInterrupt:
            print("\nFin du programme")

#|---------------------------------------|
#|                                       |
#|   API exposée au JavaScript           |
#|                                       |
#|---------------------------------------|
 
# Cette classe permet au JavaScript d'appeler des fonctions Python.
# Le bouton "Démarrer" dans l'UI appelle api.demarrer(), etc.
 
class SaphirAPI:
 
    def demarrer(self):
        # Lance la boucle vocale dans un thread séparé
        t = threading.Thread(target=boucle_saphir, daemon=True)
        t.start()
        return {"ok": True}
    
    def arreter(self):
        ui_status("off") 
        if os.path.exists("temp.mp3"):
            try: os.remove("temp.mp3")
            except: pass
        window_ref.destroy()
 
    def get_status(self):
        return {"actif": state.assistant_actif}
    
    def envoyer_texte(self, texte_recu):
        """Fonction appelée par le JavaScript de l'interface"""
        global text, commande_par_texte
        if texte_recu.strip():
            commande_par_texte = True
            state.micro = False
            
            text = texte_recu
            print(f"[Interface] Commande écrite reçue : {text}")
            
            detection_commande()
            
            ui_status("speaking")
            executer_commande()
            
            if os.path.exists("temp.mp3"):
                try: os.remove("temp.mp3")
                except: pass
                
            if state.assistant_actif:
                ui_status("active")
            else:
                ui_status("idle")
            
            state.micro = True
                
        return {"status": "reçu"}
    

#|---------------|
#|               |
#|   Lancement   |
#|               |
#|---------------|
 
api = SaphirAPI()
 
window_ref = webview.create_window(
    title     = "Saphir — Assistant Vocal",
    url       = "index.html",   # ton fichier HTML dans le même dossier
    js_api    = api,
    width     = 450,
    height    = 425,
    resizable = False,
    background_color = "#64003a",
)
 
webview.start(debug=False)