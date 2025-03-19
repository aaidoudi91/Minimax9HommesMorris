""" L'éxecution de se fichier lance le jeu en mode humain contre humain. L'IA n'est pas impliquée."""

from src.ia.utils import *


def HumainVSHumain():
    """ Lance une partie en mode Humain contre Humain (phase 1 : placement des pions
        - phase 2/3 : déplacement des pions). """

    tableau = ['x'] * 24  # Initialisation du plateau de jeu vide
    print("Bienvenue dans le Jeu du Moulin - Mode Humain contre IA !\n")

    # Phase 1 : Placement des pions
    print("Première phase : placement des pions.")
    for i in range(9):
        print(f"\nIl vous reste chacun {9-i} pions.\n")
        printTableau(tableau)
        jouerTourHumain('1', tableau)
        printTableau(tableau)
        jouerTourHumain('2', tableau)

    # Phase 2 et 3 : Déplacement des pions
    print("Deuxième phase : déplacement des pions.")
    while True:
        printTableau(tableau)
        jouerTourHumain('1', tableau, phase1=False)
        verifierVictoire(tableau)
        printTableau(tableau)
        jouerTourHumain('2', tableau, phase1=False)
        verifierVictoire(tableau)


if __name__ == "__main__":
    HumainVSHumain()
