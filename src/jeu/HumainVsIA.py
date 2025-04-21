"""  L'éxecution de ce fichier lance le jeu en mode humain contre IA.
    Note : jouerTourIA() ne se trouve pas dans utils.py pour mieux la différencier avec jouerTourIA() de IAVsIA.py. """


from src.ia.minimax import minimax
from src.ia.heuristiques import *
import sys


def jouerTourIA(plateau, phase1, heuristiqueUtilisee, profondeurUtilisee):
    """ Gère le tour de l'IA en utilisant l'algorithme Minimax.
        L'IA réfléchit à son meilleur coup et l'exécute en fonction de la phase du jeu.
        Affiche les actions réalisées par l'IA, notamment les placements, déplacements et suppressions de pions.
        :param plateau: Liste représentant l'état actuel du plateau de jeu.
        :param phase1: Booléen indiquant si l'on est en phase de placement (True) ou de déplacement (False).
        :param heuristiqueUtilisee: Fonction heuristique utilisée pour évaluer les coups.
        :param profondeurUtilisee: Profondeur maximale de l'arbre de recherche du coup de l'IA. """

    print("\n\033[95mL'IA réfléchit...\033[0m")
    evalPlateau = minimax(plateau, profondeur=profondeurUtilisee, maximisant=False, alpha=float('-inf'), beta=float('inf'),
                          etape1=phase1, heuristique=heuristiqueUtilisee)  # Appel de Minimax avec une profondeur de 4

    ancienPlateau = plateau[:]  # Sauvegarde de l'ancien état du plateau
    nouveauPlateau = evalPlateau.plateau
    if nouveauPlateau is None:  # Vérification si Minimax a retourné un plateau valide
        print("\033[91mErreur : L'IA n'a pas trouvé de coup valide.\033[0m")
        return

    positionAjoutee = None
    positionRetiree = None
    for i in range(len(ancienPlateau)):  # Comparaison entre ancien et nouveau plateau pour identifier les actions
        if ancienPlateau[i] == 'x' and nouveauPlateau[i] == '2':
            positionAjoutee = i  # L'IA a placé un pion ici
        elif ancienPlateau[i] == '2' and nouveauPlateau[i] == 'x':
            positionRetiree = i  # L'IA a retiré un pion ici
    plateau[:] = evalPlateau.plateau  # Mise à jour du plateau avec le coup de l'IA

    if phase1 and positionAjoutee is not None:  # Affichage des actions de l'IA en fonction de la phase du jeu
        print(f"\033[95mL'IA place un pion en position {positionAjoutee}.\033[0m")
    elif not phase1 and positionAjoutee is not None and positionRetiree is not None:
        print(f"\033[95mL'IA déplace un pion de la position {positionRetiree} "
              f"vers la position {positionAjoutee}.\033[0m\n")

    if positionAjoutee is not None and moulinCree(positionAjoutee, plateau):  # Vérification si un moulin a été formé
        print("\033[95mL'IA a formé un moulin !\033[0m")

        piece_retiree = None  # Identification du pion retiré par l'IA après la formation du moulin
        for i in range(len(ancienPlateau)):
            if ancienPlateau[i] == '1' and nouveauPlateau[i] == 'x':
                piece_retiree = i
                break
        if piece_retiree is not None:
            print(f"\033[95mVotre pion en position {piece_retiree} a été retiré.\033[0m")


def HumainVsIA(heuristiqueChoisie, profondeurChoisie):
    """ Lance une partie en mode Humain contre IA (phase 1 : placement des pions - phase 2/3 : déplacement des pions).
        :param heuristiqueChoisie: Fonction heuristique utilisée pour l'IA. """

    tableau = ['x'] * 24  # Initialisation du plateau de jeu vide

    print("\033[1mPremière phase : placement des pions.\033[0;0m")  # Phase 1 : Placement des pions
    for i in range(9):
        print(f"\n\033[1mIl vous reste chacun {9 - i} pions à placer.\033[0;0m\n")
        printTableau(tableau)
        jouerTourHumain('1', tableau)
        jouerTourIA(tableau, phase1=True, heuristiqueUtilisee=heuristiqueChoisie, profondeurUtilisee=profondeurChoisie)

    print("\n\033[1mDeuxième phase : déplacement des pions.\033[0;0m\n")  # Phase 2 et 3 : Déplacement des pions
    while True:
        printTableau(tableau)
        jouerTourHumain('1', tableau, phase1=False)
        verifierVictoire(tableau)  # Vérifie si la partie est terminée
        jouerTourIA(tableau, phase1=False, heuristiqueUtilisee=heuristiqueChoisie, profondeurUtilisee=profondeurChoisie)
        verifierVictoire(tableau)  # Vérifie à nouveau après le tour de l'IA


if __name__ == "__main__":
    if len(sys.argv) != 3:  # Vérification du nombre d'arguments
        print("\033[1mBienvenue dans le Jeu du Neuf Hommes de Morris - Mode \033[94mHumain\033[0m \033[1mcontre "
              "\033[95mIA\033[0m \033[1m!\033[0;0m")
        print(
            f"\033[1mL'IA utilise une heurisitique de niveau 3/3 et une profondeur de recherche de 4\033[0;0m\n")
        HumainVsIA(heuristiqueExperte, 5)
    else:
        # Mapping des niveaux de difficulté (1 -> naive, 2 -> avancée, 3 -> experte)
        niveauxDifficulte = {'1': heuristiqueNaive, '2': heuristiqueAvancee, '3': heuristiqueExperte}
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]

        if arg1 not in niveauxDifficulte:  # Validation de l'argument 1 (doit être compris entre 1 et 3)
            print("\033[91mErreur : Niveau de difficulté (arg1) doit être 1 (naive), 2 (avancée) ou 3 (experte).\033[0m")
            sys.exit(1)

        try:  # Validation de l'argument 2 (doit être un entier positif pour la profondeur)
            profondeurDonnee = int(arg2)
            if profondeurDonnee <= 0:
                raise ValueError
        except ValueError:
            print("\033[91mErreur : La profondeur (arg2) doit être un entier positif.\033[0m")
            sys.exit(1)

        print("\033[1mBienvenue dans le Jeu du Neuf Hommes de Morris - Mode \033[94mHumain\033[0m \033[1mcontre "
              "\033[95mIA\033[0m \033[1m!\033[0;0m")
        print(f"\033[1mL'IA utilise une heurisitique de niveau {arg1}/3 et une profondeur de recherche de {arg2}\033[0;0m\n")
        HumainVsIA(niveauxDifficulte[arg1], profondeurDonnee)  # Lancement avec les arguments fournis
