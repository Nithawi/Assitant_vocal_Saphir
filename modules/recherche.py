import webbrowser as wb
from modules.principal.parler import dire
import modules.principal.state as state

FORMULES_POLITESSE = [
    "s'il te plaît", "s'il te plait", "sil te plait", 
    "merci", "s'il vous plaît", "s'il vous plait",
    "est-ce que tu peux", "peux-tu", "dis-moi", "trouve-moi",
    "est-ce que tu pourrais", "pourrais-tu", "donne-moi", "affiche-moi",
    "stp", "svp","merci d'avance"
]

# rechercher dans google
def rechercher(text):
    # 1. On passe tout en minuscule pour éviter les problèmes de majuscules
    requete = text.lower()
    
    # 2. On retire les mots déclencheurs de recherche
    mots_commande = ["rechercher", "recherche", "chercher", "cherche"]
    for mot in mots_commande:
        if requete.startswith(mot):
            requete = requete.replace(mot, "", 1).strip() # Retire uniquement le premier trouvé au début
            
    # 3. Nettoyage ciblé des formules de politesse
    for formule in FORMULES_POLITESSE:
        # On remplace la formule par un espace vide
        requete = requete.replace(formule, "")
    
    # Petits nettoyages de liaisons orphelines (ex: "cherche 'sur' les chats" ou "cherche 'de' la musique")
    requete = requete.strip()
    if requete.startswith("de ") or requete.startswith("sur ") or requete.startswith("la "):
        # Supprime le petit mot de liaison du début s'il existe
        mots_liaison = ["de ", "sur ", "la ", "les ", "des "]
        for liaison in mots_liaison:
            if requete.startswith(liaison):
                requete = requete.replace(liaison, "", 1).strip()
                break

    # 4. Traitement et envoi vers YouTube ou Google
    if requete:
        # Cas YouTube
        if "youtube" in requete or "ytb" in requete:
            # On nettoie les reliquats liés à la formulation YouTube
            requete = requete.replace("sur youtube", "").replace("youtube", "")
            requete = requete.replace("sur ytb", "").replace("ytb", "")
            requete = requete.strip()
            
            url = f"https://www.youtube.com/results?search_query={requete.replace(' ', '+')}"
            dire(f"Je recherche {requete} sur YouTube")
            wb.open(url)
            
        # Cas Google par défaut
        else:
            url = f"https://www.google.com/search?q={requete.replace(' ', '+')}"
            dire(f"Je recherche {requete} sur Google")
            wb.open(url)
    else:
        dire("Je n'ai pas compris ce que je doit rechercher.")
        state.assistant_actif = True