import webbrowser as wb
from modules.principal.parler import dire
import modules.principal.state as state

# rechercher dans google
def rechercher(text):
        mots = text.lower().split()
        # Retire le mot 'cherche' ou 'recherche' pour garder la requête
        requete = " ".join([mot for mot in mots if mot not in ["cherche", "recherche", "chercher"]])

        if requete:
            if "youtube" in requete:
                requete = requete.replace("sur youtube","").replace("youtube","")
                url = f"https://www.youtube.com/results?search_query={requete.replace(' ', '+')}"
                dire(f"Je recherche {requete} sur YouTube")
                wb.open(url)
            else:
                url = f"https://www.google.com/search?q={requete.replace(' ', '+')}"
                dire(f"Je recherche {requete} sur Google")
                wb.open(url)
        else:
            dire("Je n'ai pas compris ce que je dois rechercher.")
            state.assistant_actif = True
