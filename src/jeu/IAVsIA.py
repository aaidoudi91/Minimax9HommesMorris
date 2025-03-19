from src.ia.minimax import *
from src.ia.heuristiques import *


def jouerTourIA(plateau, joueur, phase1, heuristic):
    """
    Gère le tour d'une IA.
    Utilise l'algorithme Minimax pour déterminer le meilleur coup.
    Affiche les actions effectuées par l'IA.
    """
    evalBoard = minimax(plateau, profondeur=5, maximisant=(joueur == '2'), alpha=float('-inf'), beta=float('inf'),
                        etape1=phase1, heuristique=heuristic)

    # Identifier les changements effectués par l'IA
    ancien_plateau = plateau[:]
    nouveau_plateau = evalBoard.plateau

    # Trouver la position où l'IA a placé ou déplacé un pion
    position_ajoutee = None
    position_retiree = None

    for i in range(len(ancien_plateau)):
        if ancien_plateau[i] == 'x' and nouveau_plateau[i] == joueur:
            position_ajoutee = i
        elif ancien_plateau[i] == joueur and nouveau_plateau[i] == 'x':
            position_retiree = i

    # Mettre à jour le plateau avec le meilleur coup trouvé par l'IA
    plateau[:] = evalBoard.plateau

    # Afficher les actions de l'IA
    couleur = "\033[94m" if joueur == '1' else "\033[95m"
    print(f"\n{couleur}--- Tour de l'IA {joueur} ---\033[0m")

    if phase1 and position_ajoutee is not None:
        print(f"{couleur}L'IA {joueur} a placé un pion en position {position_ajoutee}.\033[0m")

    elif not phase1 and position_ajoutee is not None and position_retiree is not None:
        print(
            f"{couleur}L'IA {joueur} a déplacé un pion de la position {position_retiree} à la position {position_ajoutee}.\033[0m")

    if position_ajoutee is not None and moulinCree(position_ajoutee, plateau):
        print(f"{couleur}L'IA {joueur} a formé un moulin !\033[0m")

        # Trouver et afficher la pièce retirée par l'IA
        piece_retirée = None
        for i in range(len(ancien_plateau)):
            if ancien_plateau[i] != joueur and ancien_plateau[i] != 'x' and nouveau_plateau[i] == 'x':
                piece_retirée = i
                break

        if piece_retirée is not None:
            print(f"{couleur}L'IA {joueur} a retiré un pion adverse en position {piece_retirée}.\033[0m")


def verifierVictoire(plateau):
    """
    Vérifie si un joueur a gagné (si l'adversaire a moins de 3 pions ou ne peut plus bouger).
    """
    if nombrePion(plateau, '1') < 3 or len(mouvementsPossiblesEtape2ou3(plateau, '1')) == 0:
        print("\033[95m\n--- L'IA 2 a gagné ! ---\033[0m")
        exit()
    elif nombrePion(plateau, '2') < 3 or len(mouvementsPossiblesEtape2ou3(plateau, '2')) == 0:
        print("\033[94m\n--- L'IA 1 a gagné ! ---\033[0m")
        exit()


def AIVsAI(heuristic1, heuristic2):
    """Lance une partie en mode IA contre IA."""
    tableau = ['x'] * 24
    print("Bienvenue dans le Jeu du Moulin - Mode IA contre IA !\n")

    # Phase 1 : Placement des pions
    for _ in range(9):
        printTableau(tableau)
        jouerTourIA(tableau, joueur='1', phase1=True, heuristic=heuristic1)
        jouerTourIA(tableau, joueur='2', phase1=True, heuristic=heuristic2)

    # Phase 2 et 3 : Déplacement des pions
    while True:
        printTableau(tableau)
        jouerTourIA(tableau, joueur='1', phase1=False, heuristic=heuristic1)
        verifierVictoire(tableau)
        jouerTourIA(tableau, joueur='2', phase1=False, heuristic=heuristic2)
        verifierVictoire(tableau)


if __name__ == "__main__":
    print("Bienvenue sur le Jeu du Moulin - Mode IA contre IA !\n")

    # Lancement avec deux heuristiques différentes pour les deux IA (modifiable)
    AIVsAI(potentialMillsHeuristic, advancedKartikHeuristic)
