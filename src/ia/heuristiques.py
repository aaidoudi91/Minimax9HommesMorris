""" Regroupe différentes fonctions d'évaluation permettant à l'IA d'estimer la qualité d'un état du plateau. """

from src.ia.utils import *


def heuristiqueNaive(plateau, phase1):
    """ Évalue le plateau de jeu en fonction des moulins potentiels.
        :param plateau: Liste représentant l'état actuel du plateau de jeu.
        :param phase1: Booléen indiquant si le jeu est en phase 1 (placement des pions) ou non.
        :return: Un score numérique évaluant l'état du plateau en faveur d'un joueur ou de l'autre. """

    evaluation = 0
    # Nombre de moulins potentiels pour le joueur 1
    nombrePossibleMoulinsJoueur1 = nombrePossibleMoulins(plateau, "1")
    # Nombre de pièces du joueur 2 proches de former un moulin
    nombrePossibleMoulinsJoueur2 = nombrePiecesMoulinEnFormation(plateau, "2")

    if not phase1:  # Si nous ne sommes pas en phase 1, on détermine le nombre de pièces mobiles
        piecesMobiles = len(mouvementsPossiblesEtape2ou3(plateau))

        if nombrePion(plateau, '2') <= 2 or piecesMobiles == 0:  # Vérification des conditions de :
            return float('inf')                                         # Victoire du joueur 1
        elif nombrePion(plateau, '1') <= 2:
            return float('-inf')                                        # Victoire du joueur 2

    if nombrePion(plateau, '1') < 4:             # Évaluation basée sur les moulins possibles
        evaluation += 1 * nombrePossibleMoulinsJoueur1  # Moins de poids pour le joueur 1
        evaluation += 2 * nombrePossibleMoulinsJoueur2  # Plus de poids pour le joueur 2
    else:
        evaluation += 2 * nombrePossibleMoulinsJoueur1  # Plus de poids pour le joueur 1
        evaluation += 1 * nombrePossibleMoulinsJoueur2  # Moins de poids pour le joueur 2

    return evaluation


def heuristiqueAvancee(plateau, phase1):
    """ Une heuristique avancée évaluant l'état du plateau en tenant compte des facteurs suivants :
        - Nombre de pions sur le plateau.
        - Nombre de moulins formés.
        - Nombre de moulins potentiels (en formation).
        - Nombre de mouvements possibles (mobilité).
        - Blocage des mouvements adverses.
        - Proximité d'une victoire ou d'une défaite.
        :param plateau : Liste représentant l'état actuel du plateau.
        :param phase1 : Booléen indiquant si on est à la phase 1 (placement des pions).
        :return: Une valeur numérique représentant l'évaluation de l'état du plateau. """

    # Poids pour chaque facteur dans l'évaluation du plateau
    poidsPions = 10
    poidsMoulins = 50
    poidsMoulinsPotentiels = 30
    poidsMouvementsPossibles = 5
    poidsMouvementsBloques = 30

    # Initialisation de l'évaluation
    evaluation = 0

    # 1. Nombre de pions sur le plateau
    pionsJoueur1 = nombrePion(plateau, '1')
    pionsJoueur2 = nombrePion(plateau, '2')

    if not phase1:
        # Vérifier si un joueur a perdu (moins de 3 pions)
        if pionsJoueur1 < 3:
            return float('-inf')  # Défaite pour le joueur maximisant
        if pionsJoueur2 < 3:
            return float('inf')  # Victoire pour le joueur maximisant

    # Contribution du nombre de pions à l'évaluation
    evaluation += poidsPions * (pionsJoueur1 - pionsJoueur2)

    # 2. Nombre de moulins formés
    moulinsJoueur1 = nombrePossibleMoulins(plateau, '1')
    moulinsJoueur2 = nombrePossibleMoulins(plateau, '2')

    evaluation += poidsMoulins * (moulinsJoueur1 - moulinsJoueur2)

    # 3. Nombre de moulins potentiels (en formation)
    moulinsPotentielsJoueur1 = nombrePiecesMoulinEnFormation(plateau, '1')
    moulinsPotentielsJoueur2 = nombrePiecesMoulinEnFormation(plateau, '2')

    evaluation += poidsMoulinsPotentiels * (moulinsPotentielsJoueur1 - moulinsPotentielsJoueur2)

    # 4. Mobilité : Nombre de mouvements possibles (uniquement après la phase 1)
    if not phase1:
        mouvementsJoueur1 = len(mouvementsPossiblesEtape2ou3(plateau, '1'))
        mouvementsJoueur2 = len(mouvementsPossiblesEtape2ou3(plateau, '2'))

        evaluation += poidsMouvementsPossibles * (mouvementsJoueur1 - mouvementsJoueur2)

        # Vérifier si un joueur est totalement bloqué (perd automatiquement)
        if mouvementsJoueur2 == 0:
            return float('inf')  # Victoire pour le joueur maximisant
        if mouvementsJoueur1 == 0:
            return float('-inf')  # Défaite pour le joueur maximisant

    # 5. Blocage des mouvements adverses
    # Comptabiliser les pions de l'adversaire bloqués (sans mouvements disponibles)
    blocagesAdversaire = sum(1 for pos in range(len(plateau))
                             if plateau[pos] == '2' and all(plateau[adj] != 'x' for adj in positionsAdjacentes(pos)))

    evaluation += poidsMouvementsBloques * blocagesAdversaire

    return evaluation


def heuristiqueExperte(plateau, phase1):
    """ Heuristique avancée basée sur les recommandations de Kartik Kukreja, évaluant l'état du plateau en tenant
        compte des caractéristiques suivantes :
        - Moulins fermés récemment.
        - Nombre total de moulins.
        - Nombre de pièces adverses bloquées.
        - Nombre total de pièces.
        - Configurations à 2 pièces.
        - Configurations à 3 pièces.
        - Double moulins.
        - Configuration gagnante ou perdante (Winning configuration).
        :param plateau : Liste représentant l'état actuel du plateau.
        :param phase1 : Booléen indiquant si on est à la phase 1 (placement des pions).
        :return: Une valeur numérique représentant l'évaluation de l'état du plateau. """

    # Poids des caractéristiques en fonction de la phase de jeu
    poidsMoulinsFermes = 18 if phase1 else 14
    poidsMoulins = 26 if phase1 else 43
    poidsPionsBloques = 1 if phase1 else 10
    poidsPions = 9 if phase1 else 11
    poidsConfig2Pions = 10 if phase1 else 8
    poidsConfig3Pions = 7 if phase1 else 1086
    poidsDoubleMoulins = 0 if phase1 else 8
    poidsConfigGagnante = 0 if phase1 else 1190

    evaluation = 0  # Initialisation de l'évaluation

    # Détection des moulins fermés récemment
    moulinFermeJoueur = any(moulinCree(i, plateau) for i in range(len(plateau)) if plateau[i] == '1')
    moulinFermeAdversaire = any(moulinCree(i, plateau) for i in range(len(plateau)) if plateau[i] == '2')
    evaluation += poidsMoulinsFermes * (int(moulinFermeJoueur) - int(moulinFermeAdversaire))

    # Nombre total de moulins
    nbMoulinsJoueur = nombrePossibleMoulins(plateau, '1')
    nbMoulinsAdversaire = nombrePossibleMoulins(plateau, '2')
    evaluation += poidsMoulins * (nbMoulinsJoueur - nbMoulinsAdversaire)

    # Nombre de pions bloqués
    pionsBloquesJoueur = sum(all(plateau[adj] != 'x' for adj in positionsAdjacentes(i)) for i in range(len(plateau))
                             if plateau[i] == '2')
    pionsBloquesAdversaire = sum(all(plateau[adj] != 'x' for adj in positionsAdjacentes(i)) for i in range(len(plateau))
                                 if plateau[i] == '1')
    evaluation += poidsPionsBloques * (pionsBloquesAdversaire - pionsBloquesJoueur)

    # Nombre total de pions
    nbPionsJoueur = nombrePion(plateau, '1')
    nbPionsAdversaire = nombrePion(plateau, '2')
    evaluation += poidsPions * (nbPionsJoueur - nbPionsAdversaire)

    # Configurations avec 2 pions en formation
    config2PionsJoueur = nombrePiecesMoulinEnFormation(plateau, '1')
    config2PionsAdversaire = nombrePiecesMoulinEnFormation(plateau, '2')
    evaluation += poidsConfig2Pions * (config2PionsJoueur - config2PionsAdversaire)

    # Configurations avec 3 pions en formation
    config3PionsJoueur = sum(prochainMoulin(i, plateau, '1') for i in range(len(plateau)) if plateau[i] == 'x')
    config3PionsAdversaire = sum(prochainMoulin(i, plateau, '2') for i in range(len(plateau)) if plateau[i] == 'x')
    evaluation += poidsConfig3Pions * (config3PionsJoueur - config3PionsAdversaire)

    # Double moulins
    doubleMoulinJoueur = sum(moulinCree(i, plateau) and prochainMoulin(i, plateau, '1')
                             for i in range(len(plateau)) if plateau[i] == '1')
    doubleMoulinAdversaire = sum(moulinCree(i, plateau) and prochainMoulin(i, plateau, '2')
                                 for i in range(len(plateau)) if plateau[i] == '2')
    evaluation += poidsDoubleMoulins * (doubleMoulinJoueur - doubleMoulinAdversaire)

    # Configuration gagnante ou perdante
    victoireJoueur = int(nbPionsAdversaire < 3 or pionsBloquesAdversaire == nbPionsAdversaire)
    defaiteJoueur = int(nbPionsJoueur < 3 or pionsBloquesJoueur == nbPionsJoueur)
    evaluation += poidsConfigGagnante * (victoireJoueur - defaiteJoueur)

    return evaluation
