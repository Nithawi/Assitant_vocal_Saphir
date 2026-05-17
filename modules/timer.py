import time
import threading
from playsound3 import playsound
from modules.principal.parler import dire
import modules.principal.state as state

def timer(duree_secondes):

    time.sleep(duree_secondes)
    
    
    try:
        playsound("modules/sounds/timer.mp3") 
    except:
        pass
    dire("Le minuteur est terminé !")

def reglage_minuteur(phrase):
    chiffres_en_lettres = {
        "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4,
        "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9,
        "dix": 10, "quinze": 15, "vingt": 20, "trente": 30,
        "quarante": 40, "cinquante": 50, "soixante": 60
    }

    phrases = phrase.lower().replace("-", " ").split()
    mots = phrase.split()

    index_debut = 0
    for mot_cle in ["minuteur", "timer"]:
        if mot_cle in mots:
            index_debut = mots.index(mot_cle) + 1
            break
    
    mots = mots[index_debut:]
    temps = 0
    unite = "minutes"

    for i, mot in enumerate(mots):
        if mot == "et":
            continue

        if mot in chiffres_en_lettres:
            valeur = chiffres_en_lettres[mot]
            if temps in [20, 30, 40, 50, 60] and valeur < 10:
                temps += valeur
            else:
                temps = valeur
            
        elif mot.isdigit():
            temps = int(mot)
            break

    if any(s in phrases for s in ["seconde", "secondes", "sec", "s"]):
        unite = "secondes"
    elif any(m in phrases for m in ["minute", "minutes", "min", "m"]):
        unite = "minutes"
            
    if temps == 0:
        dire("Je n'ai pas compris la durée du minuteur.")
        return

    duree = temps if unite == "secondes" else temps * 60
    
    dire(f"Ok, je règle un minuteur de {temps} {unite}.")
    
    # Lancement en arrière-plan (Thread) pour ne pas figer Saphir
    thread_timer = threading.Thread(target=timer, args=(duree,), daemon=True)
    thread_timer.start()