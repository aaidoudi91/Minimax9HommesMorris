""" Implémente précisément l'algorithme Minimax avec élagage alpha-bêta.
    Cette implémentation est générique, modulaire et compatible avec toutes les heuristiques proposées. """

from src.ia.utils import *


class Evaluer:
    """ Classe permettant d'évaluer une configuration du plateau. """
    def __init__(self):
        self.evaluer = 0  # Valeur d'évaluation de la configuration
        self.plateau = []  # Plateau correspondant à cette évaluation


# Variables globales pour les statistiques
brancheElagee = 0  # Nombre d'élagages effectués
etatsAtteints = 0  # Nombre d'états évalués


def minimax(plateau, profondeur, maximisant, alpha, beta, etape1, heuristique):
    """ Algorithme Minimax avec élagage alpha-bêta pour évaluer les meilleures configurations du jeu.
        :param plateau: Liste représentant l'état actuel du plateau.
        :param profondeur: Profondeur maximale de recherche dans l'arbre de jeu.
        :param maximisant: Booléen indiquant si l'on maximise (True) ou minimise (False) la valeur d'évaluation.
        :param alpha: Meilleure valeur trouvée pour le joueur maximisant.
        :param beta: Meilleure valeur trouvée pour le joueur minimisant.
        :param etape1: Booléen indiquant si l'on est à l'étape 1 du jeu.
        :param heuristique: Fonction d'évaluation heuristique utilisée.
        :return: Un objet Evaluer contenant la meilleure configuration du plateau et son score d'évaluation. """

    global brancheElagee, etatsAtteints  # Accès aux variables globales pour les statistiques

    evaluationFinale = Evaluer()
    evaluationFinale.plateau = plateau[:]

    # Condition terminale : profondeur atteinte ou fin de partie
    if profondeur == 0 or (not etape1 and (nombrePion(plateau, '1') < 3 or nombrePion(plateau, '2') < 3)):
        evaluationFinale.evaluer = heuristique(plateau, etape1)
        return evaluationFinale

    etatsAtteints += 1  # Incrémentation du nombre d'états évalués

    if maximisant:  # Tour du joueur '1' (maximisant)
        meilleureValeur = float('-inf')
        mouvementsPossibles = mouvementsPossiblesEtape1(plateau) if etape1 \
            else mouvementsPossiblesEtape2ou3(plateau, '1')

        for config in mouvementsPossibles:
            evalCourante = minimax(config, profondeur - 1, False, alpha, beta, etape1, heuristique)
            if evalCourante.evaluer > meilleureValeur:
                meilleureValeur = evalCourante.evaluer
                evaluationFinale.plateau = config[:]
            alpha = max(alpha, meilleureValeur)

            # Vérification de l'élagage alpha-bêta
            if beta <= alpha:
                brancheElagee += 1  # Incrémentation du compteur d'élagage
                break

        evaluationFinale.evaluer = meilleureValeur if mouvementsPossibles else heuristique(plateau, etape1)

    else:  # Tour du joueur '2' (minimisant, IA)
        meilleureValeur = float('inf')
        mouvementsPossibles = mouvementsPossiblesEtape1(
            plateauInverse(plateau)) if etape1 else mouvementsPossiblesEtape2ou3(plateauInverse(plateau), '1')
        mouvementsPossibles = genereListePlateauInverse(mouvementsPossibles)

        for config in mouvementsPossibles:
            evalCourante = minimax(config, profondeur - 1, True, alpha, beta, etape1, heuristique)
            if evalCourante.evaluer < meilleureValeur:
                meilleureValeur = evalCourante.evaluer
                evaluationFinale.plateau = config[:]
            beta = min(beta, meilleureValeur)

            # Vérification de l'élagage alpha-bêta
            if beta <= alpha:
                brancheElagee += 1  # Incrémentation du compteur d'élagage
                break

        evaluationFinale.evaluer = meilleureValeur if mouvementsPossibles else heuristique(plateau, etape1)

    return evaluationFinale
