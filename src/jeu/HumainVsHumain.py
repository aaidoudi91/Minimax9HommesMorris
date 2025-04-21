""" L'éxecution de ce fichier lance le jeu en mode humain contre humain. L'IA n'est pas impliquée."""

from src.ia.utils import printTableau, jouerTourHumain, verifierVictoire


def HumainVSHumain():
    """ Lance une partie en mode Humain contre Humain (phase 1 : placement des pions,
    phase 2/3 : déplacement des pions). """

    tableau = ['x'] * 24  # Initialisation du plateau de jeu vide
    print("\033[1mBienvenue dans le Jeu du Neuf Hommes de Morris - Mode \033[94mHumain\033[0m \033[1mcontre "
          "\033[95mHumain\033[0m \033[1m!\033[0;0m\n")

    # Phase 1 : Placement des pions
    print("\033[1mPremière phase : placement des pions.\033[0;0m")  # Phase 1 : Placement des pions
    for i in range(9):
        print(f"\n\033[1mIl vous reste chacun {9 - i} pions à placer.\033[0;0m\n")
        printTableau(tableau)
        jouerTourHumain('1', tableau)
        printTableau(tableau)
        jouerTourHumain('2', tableau)

    # Phase 2 et 3 : Déplacement des pions
    print("\n\033[1mDeuxième phase : déplacement des pions.\033[0;0m\n")  # Phase 2 et 3 : Déplacement des pions
    while True:
        printTableau(tableau)
        jouerTourHumain('1', tableau, phase1=False)
        verifierVictoire(tableau)
        printTableau(tableau)
        jouerTourHumain('2', tableau, phase1=False)
        verifierVictoire(tableau)


if __name__ == "__main__":
    HumainVSHumain()
