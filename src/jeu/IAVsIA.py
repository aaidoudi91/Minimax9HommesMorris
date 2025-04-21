"""  L'éxecution de ce fichier lance un tournoi entre deux IA ou bien une partie en mode IA contre IA.
    Quelques fonctions sont définies spécifiquement pour ce mode de jeu, ce sont :

        - detecterCycle : si les IA ne trouvent pas de solutions et se bloquent mutuellement, il est préférable
        d'arrêter et de déclarer le match comme une égalité.
        - verifierVictoireAvecRetour : différente de la fonction verifierVictoire utilisée dans les autres modes de jeu
        et arrêtant le programme, celle-ci renvoie un booléen de sorte à pouvoir continuer d'autres parties.
        - jouerTourIA : différente de la fonction de même nom utilisée dans le mode HumainVsIA, celle-ci prend en
        compte le joueur et la profondeur (différente selon l'heuristique).
        - tournoiIA : lance un tournoi entre deux IA (50 parties). Les résultats sont affichés à la fin de
        l'exécution. """

from src.ia.minimax import *
from src.ia.heuristiques import *


def detecterCycle(etatsPrecedents, plateau, compteurCycles):
    """ Détecte les cycles dans les états du plateau et compte leur occurrence.
    Si le nombre de cycles dépasse 5, arrête la partie et déclare qu'il n'y a aucun vainqueur.
        :param etatsPrecedents: Ensemble des états précédents du plateau.
        :param plateau: Liste représentant l'état actuel du plateau.
        :param compteurCycles: Entier représentant le nombre de cycles détectés.
        :return: Booléen indiquant si un cycle est détecté, et le compteur mis à jour. """

    plateauHash = tuple(plateau)  # Tuple pour rendre le plateau hachable
    if plateauHash in etatsPrecedents:
        compteurCycles += 1
        if compteurCycles > 5:
            print("\033[91mLa partie est arrêtée en raison de cycles répétés. Aucun vainqueur.\033[0m")
            return True, compteurCycles  # Arrête la partie
    else:
        etatsPrecedents.add(plateauHash)
    return False, compteurCycles


def verifierVictoireAvecRetour(plateau):
    """ Vérifie si un joueur a gagné (si son adversaire a moins de 3 pions OU si son adversaire ne peut plus faire de
    mouvement légal). Retourne l'identifiant du gagnant ou None si aucun joueur n'a gagné (ce qui n'est pas le cas
    avec verifierVictoire du fichier utils.py).
        :param plateau: Liste représentant l'état du plateau.
        :return: '1' si le joueur 1 gagne, '2' si le joueur 2 gagne ou None sinon. """

    if nombrePion(plateau, '1') < 3 or len(mouvementsPossiblesEtape2ou3(plateau, '1')) == 0:
        return '2'  # Joueur 2 gagne

    elif nombrePion(plateau, '2') < 3 or len(mouvementsPossiblesEtape2ou3(plateau, '2')) == 0:
        return '1'  # Joueur 1 gagne

    return None


def jouerTourIA(plateau, joueur, phase1, heuristiqueUtilisee, profondeurUtilisee):
    """ Gère le tour d'une IA en utilisant l'algorithme Minimax. Différent de la fonction définie dans HumainVsIA.py.
    L'IA réfléchit à son meilleur coup et l'exécute en fonction de la phase du jeu.
    Affiche les actions réalisées par l'IA, notamment les placements, déplacements et suppressions de pions.
        :param plateau: Liste représentant l'état actuel du plateau de jeu.
        :param joueur: 1 ou 2 en fonction de l'ordre des joueurs.
        :param phase1: Booléen indiquant si l'on est en phase de placement (True) ou de déplacement (False).
        :param heuristiqueUtilisee: Fonction heuristique utilisée pour évaluer les coups.
        :param profondeurUtilisee: Profondeur maximale de l'arbre de recherche du coup de l'IA. """

    evalPlateau = minimax(plateau, profondeur=profondeurUtilisee, maximisant=(joueur == '2'), alpha=float('-inf'),
                          beta=float('inf'), etape1=phase1, heuristique=heuristiqueUtilisee)

    # Identifier les changements effectués par l'IA
    ancienPlateau = plateau[:]
    nouveauPlateau = evalPlateau.plateau

    # Trouver la position où l'IA a placé ou déplacé un pion
    positionAjoutee = None
    positionRetiree = None

    for i in range(len(ancienPlateau)):
        if ancienPlateau[i] == 'x' and nouveauPlateau[i] == joueur:
            positionAjoutee = i
        elif ancienPlateau[i] == joueur and nouveauPlateau[i] == 'x':
            positionRetiree = i

    # Mettre à jour le plateau avec le meilleur coup trouvé par l'IA
    plateau[:] = evalPlateau.plateau

    # Afficher les actions de l'IA
    couleur = "\033[94m" if joueur == '1' else "\033[95m"
    print(f"\n{couleur}Tour de l'IA {joueur}\033[0m")

    if phase1 and positionAjoutee is not None:
        print(f"{couleur}L'IA {joueur} a placé un pion en position {positionAjoutee}.\033[0m")

    elif not phase1 and positionAjoutee is not None and positionRetiree is not None:
        print(f"{couleur}L'IA {joueur} a déplacé un pion de la position {positionRetiree} "
            f"à la position {positionAjoutee}.\033[0m")

    if positionAjoutee is not None and moulinCree(positionAjoutee, plateau):
        print(f"{couleur}L'IA {joueur} a formé un moulin !\033[0m")

        # Trouver et afficher la pièce retirée par l'IA
        piece_retiree = None
        for i in range(len(ancienPlateau)):
            if ancienPlateau[i] != joueur and ancienPlateau[i] != 'x' and nouveauPlateau[i] == 'x':
                piece_retiree = i
                break

        if piece_retiree is not None:
            print(f"{couleur}L'IA {joueur} a retiré un pion adverse en position {piece_retiree}.\033[0m")


def tournoiIA(heuristiqueChoisie1, heuristiqueChoisie2, nb_parties=50):
    """ Organise un tournoi entre deux IA.
        :param heuristiqueChoisie1: Heuristique utilisée par l'IA 1.
        :param heuristiqueChoisie2: Heuristique utilisée par l'IA 2.
        :param nb_parties: Nombre total de parties à jouer (par défaut 50).
        :return: Résultats du tournoi sous forme d'un dictionnaire. """

    resultats = {'IA1': 0, 'IA2': 0, 'Egalite': 0}  # Initialisation des résultats

    for partie in range(nb_parties):
        tableau = ['x'] * 24     # Plateau initial
        etatsPrecedents = set()  # Ensemble pour détecter les cycles
        compteurCycles = 0       # Compteur pour suivre les cycles

        print(f"\n--- Partie {partie + 1} ---\n")

        # Phase 1 : Placement des pions
        for _ in range(9):
            jouerTourIA(tableau, joueur='1', phase1=True, heuristiqueUtilisee=heuristiqueChoisie1, profondeurUtilisee=4)
            jouerTourIA(tableau, joueur='2', phase1=True, heuristiqueUtilisee=heuristiqueChoisie2, profondeurUtilisee=6)

        # Phase 2 et 3 : Déplacement des pions
        while True:
            jouerTourIA(tableau, joueur='1', phase1=False, heuristiqueUtilisee=heuristiqueChoisie1, profondeurUtilisee=4)
            cycleDetecte, compteurCycles = detecterCycle(etatsPrecedents, tableau, compteurCycles)
            if cycleDetecte:
                print("\033[91mÉgalité détectée en raison de cycles répétitifs.\033[0m")
                resultats['Egalite'] += 1
                break
            gagnant = verifierVictoireAvecRetour(tableau)
            if gagnant:
                resultats['IA1' if gagnant == '1' else 'IA2'] += 1
                break

            jouerTourIA(tableau, joueur='2', phase1=False, heuristiqueUtilisee=heuristiqueChoisie2, profondeurUtilisee=6)
            cycleDetecte, compteurCycles = detecterCycle(etatsPrecedents, tableau, compteurCycles)
            if cycleDetecte:
                print("\033[91mÉgalité détectée en raison de cycles répétitifs.\033[0m")
                resultats['Egalite'] += 1
                break
            gagnant = verifierVictoireAvecRetour(tableau)
            if gagnant:
                resultats['IA1' if gagnant == '1' else 'IA2'] += 1
                break

    # Affichage des résultats du tournoi
    print("\n--- Résultats du tournoi ---")
    print(f"IA 1 : {resultats['IA1']} victoires")
    print(f"IA 2 : {resultats['IA2']} victoires")
    print(f"Égalités : {resultats['Egalite']}")

    return resultats


def AIVsAI(heuristiqueChoisie1, heuristiqueChoisie2):
    """Lance une partie en mode IA contre IA."""

    tableau = ['x'] * 24
    print("\033[1mBienvenue dans le Jeu du Neuf Hommes de Morris - Mode \033[94mIA\033[0m \033[1mcontre "
          "\033[95mIA\033[0m \033[1m!\033[0;0m\n")

    # Phase 1 : Placement des pions
    for _ in range(9):
        printTableau(tableau)
        jouerTourIA(tableau, joueur='1', phase1=True, heuristiqueUtilisee=heuristiqueChoisie1, profondeurUtilisee=5)
        jouerTourIA(tableau, joueur='2', phase1=True, heuristiqueUtilisee=heuristiqueChoisie2, profondeurUtilisee=3)

    etatsPrecedents = set()  # Ensemble pour stocker les états précédents du plateau
    compteurCycles = 0  # Compteur pour suivre le nombre de cycles détectés

    # Phase 2 et 3 : Déplacement des pions
    while True:
        printTableau(tableau)
        jouerTourIA(tableau, joueur='1', phase1=False, heuristiqueUtilisee=heuristiqueChoisie1, profondeurUtilisee=7)
        cycleDetecte, compteurCycles = detecterCycle(etatsPrecedents, tableau, compteurCycles)
        if cycleDetecte:
            return
        verifierVictoire(tableau)
        cycleDetecte, compteurCycles = detecterCycle(etatsPrecedents, tableau, compteurCycles)
        if cycleDetecte:
            return
        jouerTourIA(tableau, joueur='2', phase1=False, heuristiqueUtilisee=heuristiqueChoisie2, profondeurUtilisee=5)
        verifierVictoire(tableau)


if __name__ == "__main__":
    AIVsAI(heuristiqueAvancee, heuristiqueExperte)
    #tournoiIA(heuristiqueExperte, heuristiqueAvancee)
