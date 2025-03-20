"""  L'éxecution de se fichier lance le jeu en mode humain contre IA.
    Note : jouerTourIA() ne se trouve pas dans utils.py pour mieux la différencier avec
    jouerTourIA() de IAVsIA.py, différente. """

from src.ia.minimax import minimax
from src.ia.heuristiques import *


def jouerTourIA(plateau, phase1, heuristic):
    """ Gère le tour de l'IA en utilisant l'algorithme Minimax.
        L'IA réfléchit à son meilleur coup et l'exécute en fonction de la phase du jeu.
        Affiche les actions réalisées par l'IA, notamment les placements, déplacements et suppressions de pions.
        :param plateau: Liste représentant l'état actuel du plateau de jeu.
        :param phase1: Booléen indiquant si l'on est en phase de placement (True) ou de déplacement (False).
        :param heuristic: Fonction heuristique utilisée pour évaluer les coups. """

    print("\n\033[95mL'IA réfléchit...\033[0m")
    evalBoard = minimax(plateau, profondeur=4, maximisant=False, alpha=float('-inf'), beta=float('inf'),
                        etape1=phase1, heuristique=heuristic)  # Appel de Minimax avec une profondeur de recherche de 5

    ancien_plateau = plateau[:]  # Sauvegarde de l'ancien état du plateau
    nouveau_plateau = evalBoard.plateau
    if nouveau_plateau is None:  # Vérification si Minimax a retourné un plateau valide
        print("\033[91mErreur : L'IA n'a pas trouvé de coup valide.\033[0m")
        return

    position_ajoutee = None
    position_retiree = None
    for i in range(len(ancien_plateau)):  # Comparaison entre ancien et nouveau plateau pour identifier les actions
        if ancien_plateau[i] == 'x' and nouveau_plateau[i] == '2':
            position_ajoutee = i  # L'IA a placé un pion ici
        elif ancien_plateau[i] == '2' and nouveau_plateau[i] == 'x':
            position_retiree = i  # L'IA a retiré un pion ici
    plateau[:] = evalBoard.plateau  # Mise à jour du plateau avec le coup de l'IA

    if phase1 and position_ajoutee is not None:  # Affichage des actions de l'IA en fonction de la phase du jeu
        print(f"\033[95mL'IA place un pion en position {position_ajoutee}.\033[0m")
    elif not phase1 and position_ajoutee is not None and position_retiree is not None:
        print(f"\033[95mL'IA déplace un pion de la position {position_retiree} "
              f"vers la position {position_ajoutee}.\033[0m")

    if position_ajoutee is not None and moulinCree(position_ajoutee, plateau):  # Vérification si un moulin a été formé
        print("\033[95mL'IA a formé un moulin !\033[0m")

        piece_retiree = None  # Identification du pion retiré par l'IA après la formation du moulin
        for i in range(len(ancien_plateau)):
            if ancien_plateau[i] == '1' and nouveau_plateau[i] == 'x':
                piece_retiree = i
                break
        if piece_retiree is not None:
            print(f"\033[95mVotre pion en position {piece_retiree} a été retiré.\033[0m")


def HumainVsIA(heuristic):
    """ Lance une partie en mode Humain contre IA (phase 1 : placement des pions - phase 2/3 : déplacement des pions).
        :param heuristic: Fonction heuristique utilisée pour l'IA. """

    tableau = ['x'] * 24  # Initialisation du plateau de jeu vide
    print("Bienvenue dans le Jeu du Moulin - Mode Humain contre IA !\n")

    print("Première phase : placement des pions.")  # Phase 1 : Placement des pions
    for i in range(9):
        print(f"\nIl vous reste chacun {9 - i} pions.\n")
        printTableau(tableau)
        jouerTourHumain('1', tableau)
        jouerTourIA(tableau, phase1=True, heuristic=heuristic)

    print("Deuxième phase : déplacement des pions.")  # Phase 2 et 3 : Déplacement des pions
    while True:
        printTableau(tableau)
        jouerTourHumain('1', tableau, phase1=False)
        verifierVictoire(tableau)  # Vérifie si la partie est terminée
        jouerTourIA(tableau, phase1=False, heuristic=heuristic)
        verifierVictoire(tableau)  # Vérifie à nouveau après le tour de l'IA


if __name__ == "__main__":
    HumainVsIA(heuristiqueExperte)
