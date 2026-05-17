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
    chiffres = {
        "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4,
        "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9,
        "dix": 10, "onze": 11, "douze": 12, "treize": 13, "quatorze": 14, "quinze": 15, "dix-sept": 17,"dix-huit": 18, "dix-neuf": 19, "vingt": 20, "trente": 30,
        "quarante": 40, "cinquante": 50, "soixante": 60
    }

    phrases = phrase.lower().replace("-", " ").split()
    text = phrase.split()

    index_debut = 0
    for mot_cle in ["minuteur", "timer"]:
        if mot_cle in text:
            index_debut = text.index(mot_cle) + 1
            break
    
    mots = text[index_debut:]
    minutes = 0
    secondes = 0
    heures = 0

    for i, mot in enumerate(mots):

        # LES HEURES
        if "heure" in mot or "heures" in mot or "h" in mot:
            if i - 1 >= 0:
                avant = mots[i - 1]
                dizaine = 0
                if i - 3 >= 0 and mots[i - 3] in chiffres:
                    dizaine = chiffres[mots[i - 3]] * 10

                if avant in chiffres:
                    heures += (dizaine + chiffres[avant])
                elif avant.isdigit():
                    heures += int(avant)

        # LES MINUTES
        if "minute" in mot or "minutes" in mot or "min" in mot or "mins" in mot or mot == "m" or mot == "mn" or mot == "mns":
            if i - 1 >= 0:
                avant = mots[i - 1]
                dizaine = 0
                if i - 3 >= 0 and mots[i - 3] in chiffres:
                    dizaine = chiffres[mots[i - 3]]

                if avant in chiffres:
                    minutes = dizaine + chiffres[avant]
                elif avant.isdigit():
                    minutes = int(avant)

        # LES SECONDES
        elif "seconde" in mot or "secondes" in mot or "sec" in mot or "secs" in mot or mot == "s":
            if i - 1 >= 0:
                avant = mots[i - 1]
                dizaine = 0
                if i - 3 >= 0 and mots[i - 3] in chiffres:
                    dizaine = chiffres[mots[i - 3]] 

                if avant in chiffres:
                    secondes = dizaine + chiffres[avant] 
                elif avant.isdigit():
                    secondes = int(avant)

    # calcul de la durée totale en secondes
    duree_totale = (heures * 3600) + (minutes * 60) + secondes

    if duree_totale == 0:
        dire("Je n'ai pas compris la durée du minuteur.")
        return
    
    elif heures > 0 and minutes == 0 and secondes == 0:
        dire(f"Ok, je règle un minuteur de {heures} heure.")

    elif heures > 0 and minutes > 0 and secondes == 0:
        dire(f"Ok, je règle un minuteur de {heures} heure et {minutes} minute.")
    
    elif heures > 0 and minutes > 0 and secondes > 0:
        dire(f"Ok, je règle un minuteur de {heures} heure, {minutes} minute et {secondes} seconde.")
    
    elif heures > 0 and minutes == 0 and secondes > 0:
        dire(f"Ok, je règle un minuteur de {heures} heure et {secondes} seconde.")

    elif minutes > 0 and secondes > 0 and heures == 0:
        dire(f"Ok, je règle un minuteur de {minutes} minute et {secondes} seconde.")
    
    elif minutes > 0 and secondes == 0 and heures == 0:
        dire(f"Ok, je règle un minuteur de {minutes} minute.")
    
    else:
        dire(f"Ok, je règle un minuteur de {secondes} seconde.")


    # On lance le compte à rebours en tâche de fond
    thread_timer = threading.Thread(target=timer, args=(duree_totale,), daemon=True)
    thread_timer.start()