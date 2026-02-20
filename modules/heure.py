import time
from modules.principal.parler import dire


# dire l'heure
def heure():
    heure_actuelle = time.strftime("%H:%M")
    dire(f"Il est {heure_actuelle}")


