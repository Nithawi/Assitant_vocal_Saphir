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
import pyautogui

from modules.timer import reglage_minuteur

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
spam = False


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
                   "veille", #13
                   "pause", #14  
                   "play", #15 
                   "volume", #16 
                   "minuteur", #17
                   "timer" #18
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
    # AJOUT ESSENTIEL : On indique à Python qu'on utilise et modifie la variable globale text
    global commande_id, text
    commande_id = -1

    # A. DÉTECTION PRIORITAIRE : Expressions entières (comme "ça va")
    if "comment ça va" in text or "comment ca va" in text or "comment tu va" in text or "ça va" in text or "ca va" in text or "cv" in text or "ça roule" in text or "ca roule" in text:
        commande_id = 19
        return

    # B. DÉTECTION DES COMMANDES SIMPLES (Heure, météo, stop...)
    texte_split = text.split()
    for mot in texte_split:
        if mot in liste_commandes:
            # On ignore les mots clés de recherche qui ont leur propre logique en dessous
            if mot not in ["cherche", "chercher", "recherche", "rechercher"]:
                commande_id = liste_commandes.index(mot)
                if debug:
                    print(f"commande détectée via mot unique: {mot} (id: {commande_id})")
                return

    # C. GESTION DU DÉCOUPAGE DE LA RECHERCHE
    mots_recherche = ["rechercher", "recherche", "chercher", "cherche"]
    for mot in mots_recherche:
        if mot in text:
            # On simule l'ID correspondant à "cherche" (index 6)
            commande_id = 6 
            
            # Découpage magique : supprime tout ce qui est avant le mot clé
            text = text.split(mot, 1)[1].strip()
            
            if debug:
                print(f"commande de recherche détectée via '{mot}' | Requête utile restante : {text}")
            break


#|---------------------------------------|
#|                                       |
#|   Fonction de execution de commande   |
#|                                       |
#|---------------------------------------|


def executer_commande():
    global commande_id

    if commande_id == -1:
        dire("Désolé, je n'ai pas compris la commande.")

    
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
        
    elif commande_id == 14 or commande_id == 15: # pause or play
        pyautogui.press("playpause")
        print("[Média] Pause/Play .")

    elif commande_id == 16: # volume
        if "monte" in text or "augmente" in text or "up" in text:
            for _ in range(9):
                pyautogui.press("volumeup")
            dire("Volume augmenté.")
            print("[Média] Volume augmenté.")
        elif "baisse" in text or "diminue" in text or "down" in text:
            for _ in range(9):
                pyautogui.press("volumedown")
            dire("Volume diminué.")
            print("[Média] Volume diminué.")
        elif "mute" in text or "muet" in text or "silence" in text or "coupe" in text or "coupes" in text or "demute" in text or "démute" in text or "unmute" in text or "remet" in text:
            dire("Volume coupé.")
            pyautogui.press("volumemute")
            print("[Média] Volume coupé.")
        else:
            dire("Désolé, je n'ai pas compris si vous vouliez augmenter ou baisser le volume.")
            print("[Média] Commande de volume non comprise.")

    elif commande_id == 17 or commande_id == 18: # minuteur
        reglage_minuteur(text)

    elif commande_id == 19: # ça va
        voix("humeur")




#|---------------|
#|               |
#|   Main loop   |
#|               |
#|---------------|
 
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
 
                if text: # On vérifie d'abord si Vosk a capté du texte
                    texte_ecoute = text.lower() 

                    # ─── CAS 1 : L'ASSISTANT EST EN VEILLE ───
                    if not state.assistant_actif: 
                        if "saphir" in texte_ecoute: 
                            print(f"Activation par mot-clé ! Phrase complète : {text}")
                            
                            # On passe l'assistant en mode actif
                            state.assistant_actif = True
                            ui_status("active") 

                            # CHRONIQUE : On coupe la phrase pour isoler la commande après "saphir"
                            # Exemple: "saphir donne moi la météo" -> "donne moi la météo"
                            phrase_commande = texte_ecoute.split("saphir", 1)[1].strip()

                            if phrase_commande:
                                # Si l'utilisateur a enchaîné sa commande, on met à jour 'text' et on l'exécute directement !
                                text = phrase_commande
                                detection_commande()
                                ui_status("speaking")
                                executer_commande()
                                
                                # Nettoyage et retour en veille automatique après l'action
                                if os.path.exists("temp.mp3"):
                                    try: 
                                        os.remove("temp.mp3") 
                                    except: 
                                        pass 
                                state.assistant_actif = False
                                ui_status("idle") 
                            else:
                                # Si l'utilisateur a juste dit "Saphir" sans rien ajouter
                                ui_status("speaking")
                                voix("Bonjour")
                                if os.path.exists("temp.mp3"): 
                                    try: 
                                        os.remove("temp.mp3")
                                    except: 
                                        pass
                                ui_status("active")
                                try:
                                    playsound("modules/sounds/activation.mp3") 
                                except Exception as e:
                                    print(f"Erreur son activation: {e}")
                            continue 

                    # ─── CAS 2 : L'ASSISTANT ÉTAIT DÉJÀ ACTIF (il attendait une suite) ───
                    elif state.assistant_actif:
                        state.assistant_actif = False 
                        detection_commande() 
                        ui_status("speaking") 
                        executer_commande() 
                        
                        if os.path.exists("temp.mp3"):
                            try: 
                                os.remove("temp.mp3")
                            except: 
                                pass 
                        
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
            try: 
                os.remove("temp.mp3")
            except: 
                pass
        window_ref.destroy()
 
    def get_status(self):
        return {"actif": state.assistant_actif}
    
    def envoyer_texte(self, texte_recu):
        global text, commande_par_texte, spam
        # Anti-spam
        if spam == True:
            print("Spam détecté : commande déjà en cours de traitement.")
            return {"status": "en cours"}
        if texte_recu.strip():
            spam = True
            commande_par_texte = True
            state.micro = False
                
            text = texte_recu
            print(f"[Interface] Commande écrite reçue : {text}")
                
            detection_commande()
                
            ui_status("speaking")
            executer_commande()
                
            if os.path.exists("temp.mp3"):
                try: 
                    os.remove("temp.mp3")
                except: 
                    pass
                    
            if state.assistant_actif:
                ui_status("active")
            else:
                ui_status("idle")
                
            state.micro = True
            spam = False
        
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