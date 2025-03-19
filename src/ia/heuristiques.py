""" Regroupe différentes fonctions d'évaluation permettant à l'IA d'estimer la qualité d'un état du plateau. """

from src.ia.utils import *

def numPiecesHeuristic(board, isStage1):
    if not isStage1:
        movablePieces = len(mouvementsPossiblesEtape2ou3(board))
        if nombrePion(board, '1') < 3 or movablePieces == 0:
            evaluation = float('inf')
        elif nombrePion(board, '2') < 3:
            evaluation = float('-inf')
        else:
            evaluation = 2 * (nombrePion(board, '1') -
                              nombrePion(board, '2'))
    else:
        evaluation = 1 * (nombrePion(board, '1') - nombrePion(board, '2'))

    return evaluation


def potentialMillsHeuristic(board, isStage1):
    evaluation = 0

    numPossibleMillsPlayer1 = nombrePossibleMoulins(board, "1")

    if not isStage1:
        movablePieces = len(mouvementsPossiblesEtape2ou3(board))

    potentialMillsPlayer2 = nombrePiecesMoulinEnFormation(board, "2")

    if not isStage1:
        if nombrePion(board, '2') <= 2 or movablePieces == 0:
            evaluation = float('inf')
        elif nombrePion(board, '1') <= 2:
            evaluation = float('-inf')
        else:
            if (nombrePion(board, '1') < 4):
                evaluation += 1 * numPossibleMillsPlayer1
                evaluation += 2 * potentialMillsPlayer2
            else:
                evaluation += 2 * numPossibleMillsPlayer1
                evaluation += 1 * potentialMillsPlayer2
    else:
        if nombrePion(board, '1') < 4:
            evaluation += 1 * numPossibleMillsPlayer1
            evaluation += 2 * potentialMillsPlayer2
        else:
            evaluation += 2 * numPossibleMillsPlayer1
            evaluation += 1 * potentialMillsPlayer2

    return evaluation


def advancedHeuristic(plateau, isStage1):
    """
    Une heuristique avancée pour le jeu du moulin.

    Cette heuristique évalue l'état du plateau en tenant compte des facteurs suivants :
    - Nombre de pions sur le plateau.
    - Nombre de moulins formés.
    - Nombre de moulins potentiels (en formation).
    - Nombre de mouvements possibles (mobilité).
    - Blocage des mouvements adverses.
    - Proximité d'une victoire ou d'une défaite.

    Arguments :
    - plateau : Liste représentant l'état actuel du plateau.
    - isStage1 : Booléen indiquant si on est à la phase 1 (placement des pions).

    Retourne :
    - Une valeur numérique représentant l'évaluation de l'état du plateau.
    """
    # Poids pour chaque facteur
    poids_pions = 10
    poids_moulins = 50
    poids_moulins_potentiels = 30
    poids_mobilite = 5
    poids_blocage_adversaire = 30

    # Évaluation initiale
    evaluation = 0

    # 1. Nombre de pions sur le plateau
    pions_joueur1 = nombrePion(plateau, '1')
    pions_joueur2 = nombrePion(plateau, '2')

    if not isStage1:
        # Si un joueur a moins de 3 pions, il perd
        if pions_joueur1 < 3:
            return float('-inf')  # Défaite pour le joueur maximisant
        if pions_joueur2 < 3:
            return float('inf')  # Victoire pour le joueur maximisant

    evaluation += poids_pions * (pions_joueur1 - pions_joueur2)

    # 2. Nombre de moulins formés
    moulins_joueur1 = nombrePossibleMoulins(plateau, '1')
    moulins_joueur2 = nombrePossibleMoulins(plateau, '2')

    evaluation += poids_moulins * (moulins_joueur1 - moulins_joueur2)

    # 3. Nombre de moulins potentiels (en formation)
    moulins_potentiels_joueur1 = nombrePiecesMoulinEnFormation(plateau, '1')
    moulins_potentiels_joueur2 = nombrePiecesMoulinEnFormation(plateau, '2')

    evaluation += poids_moulins_potentiels * (moulins_potentiels_joueur1 - moulins_potentiels_joueur2)

    # 4. Mobilité : Nombre de mouvements possibles
    if not isStage1:
        mouvements_joueur1 = len(mouvementsPossiblesEtape2ou3(plateau, '1'))
        mouvements_joueur2 = len(mouvementsPossiblesEtape2ou3(plateau, '2'))

        evaluation += poids_mobilite * (mouvements_joueur1 - mouvements_joueur2)

        # Vérification des blocages adverses
        if mouvements_joueur2 == 0:
            return float('inf')  # Victoire pour le joueur maximisant
        if mouvements_joueur1 == 0:
            return float('-inf')  # Défaite pour le joueur maximisant

    # 5. Blocage des mouvements adverses
    blocages_adversaire = sum(
        1 for pos in range(len(plateau))
        if plateau[pos] == '2' and all(plateau[adj] != 'x' for adj in positionsAdjacentes(pos))
    )

    evaluation += poids_blocage_adversaire * blocages_adversaire

    return evaluation


def advancedKartikHeuristic(plateau, isStage1):
    """
    Heuristique avancée basée sur les recommandations de Kartik Kukreja.

    Cette fonction évalue l'état du plateau en tenant compte des caractéristiques suivantes :
    - Moulins fermés récemment (Closed Morris).
    - Nombre total de moulins (Number of Morrises).
    - Nombre de pièces adverses bloquées (Blocked opponent pieces).
    - Nombre total de pièces (Number of pieces).
    - Configurations à 2 pièces (Two-piece configurations).
    - Configurations à 3 pièces (Three-piece configurations).
    - Double moulins (Double Morris).
    - Configuration gagnante ou perdante (Winning configuration).

    Arguments :
    - plateau : Liste représentant l'état actuel du plateau.
    - isStage1 : Booléen indiquant si on est à la phase 1 (placement des pions).

    Retourne :
    - Une valeur numérique représentant l'évaluation de l'état du plateau.
    """
    # Poids pour chaque caractéristique
    poids_closed_morris = 18 if isStage1 else 14
    poids_morrises = 26 if isStage1 else 43
    poids_blocked_pieces = 1 if isStage1 else 10
    poids_pieces = 9 if isStage1 else 11
    poids_two_piece_configs = 10 if isStage1 else 8
    poids_three_piece_configs = 7 if isStage1 else 1086
    poids_double_morris = 0 if isStage1 else 8
    poids_winning_config = 0 if isStage1 else 1190

    # Initialisation de l'évaluation
    evaluation = 0

    # Calcul des caractéristiques pour le joueur maximisant ('1') et le joueur minimisant ('2')

    # Fermeture récente d'un moulin
    closed_morris_player = any(moulinCree(i, plateau) for i in range(len(plateau)) if plateau[i] == '1')
    closed_morris_opponent = any(moulinCree(i, plateau) for i in range(len(plateau)) if plateau[i] == '2')

    evaluation += poids_closed_morris * (int(closed_morris_player) - int(closed_morris_opponent))

    # Nombre total de moulins
    num_morrises_player = nombrePossibleMoulins(plateau, '1')
    num_morrises_opponent = nombrePossibleMoulins(plateau, '2')

    evaluation += poids_morrises * (num_morrises_player - num_morrises_opponent)

    # Nombre de pièces bloquées
    blocked_pieces_player = sum(
        all(plateau[adj] != 'x' for adj in positionsAdjacentes(i)) for i in range(len(plateau)) if plateau[i] == '2'
    )

    blocked_pieces_opponent = sum(
        all(plateau[adj] != 'x' for adj in positionsAdjacentes(i)) for i in range(len(plateau)) if plateau[i] == '1'
    )

    evaluation += poids_blocked_pieces * (blocked_pieces_opponent - blocked_pieces_player)

    # Nombre total de pièces
    num_pieces_player = nombrePion(plateau, '1')
    num_pieces_opponent = nombrePion(plateau, '2')

    evaluation += poids_pieces * (num_pieces_player - num_pieces_opponent)

    # Configurations à 2 pièces
    two_piece_configs_player = nombrePiecesMoulinEnFormation(plateau, '1')
    two_piece_configs_opponent = nombrePiecesMoulinEnFormation(plateau, '2')

    evaluation += poids_two_piece_configs * (two_piece_configs_player - two_piece_configs_opponent)

    # Configurations à 3 pièces
    three_piece_configs_player = sum(
        prochainMoulin(i, plateau, '1') for i in range(len(plateau)) if plateau[i] == 'x'
    )

    three_piece_configs_opponent = sum(
        prochainMoulin(i, plateau, '2') for i in range(len(plateau)) if plateau[i] == 'x'
    )

    evaluation += poids_three_piece_configs * (three_piece_configs_player - three_piece_configs_opponent)

    # Double moulins
    double_morris_player = sum(
        moulinCree(i, plateau) and prochainMoulin(i, plateau, '1') for i in range(len(plateau))
        if plateau[i] == '1'
    )

    double_morris_opponent = sum(
        moulinCree(i, plateau) and prochainMoulin(i, plateau, '2') for i in range(len(plateau))
        if plateau[i] == '2'
    )

    evaluation += poids_double_morris * (double_morris_player - double_morris_opponent)

    # Configuration gagnante ou perdante
    win_config_player = int(num_pieces_opponent < 3 or blocked_pieces_opponent == num_pieces_opponent)

    lose_config_player = int(num_pieces_player < 3 or blocked_pieces_player == num_pieces_player)

    evaluation += poids_winning_config * (win_config_player - lose_config_player)

    return evaluation
