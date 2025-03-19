""" Ce fichier contient toutes les fonctions utilitaires nécessaires au bon fonctionnement du jeu.
    Composé de 2 parties : """

from copy import deepcopy
import sys


def printTableau(plateau):
    """ Affiche le plateau de jeu avec coordonnées des positions et couleurs pour différencier les joueurs.
        :param plateau : list - Représentant l'état du plateau, contenant "1", "2" (joueurs) ou "x" (position vide). """

    def couleur(joueur):
        """ Retourne la couleur associée au joueur pour l'affichage dans le terminal.
            :param joueur: int - Identifiant du joueur (1 ou 2).
            :return une chaîne de caractères contenant la couleur ANSI et la valeur du joueur. """

        violet = "\033[95m"  # Couleur pour le joueur 2
        bleu = "\033[94m"  # Couleur pour le joueur 1
        reset = "\033[0m"  # Réinitialisation de la couleur
        if joueur == "1":
            return f"{bleu}{joueur}{reset}"
        elif joueur == "2":
            return f"{violet}{joueur}{reset}"
        return joueur  # Si la case est vide, on la retourne telle quelle

    # Les numéros entre parenthèses correspondent aux indices du tableau
    print(couleur(plateau[0]) + "(00)----------------------" + couleur(plateau[1]) +
          "(01)----------------------" + couleur(plateau[2]) + "(02)")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|       " + couleur(plateau[8]) + "(08)--------------" +
          couleur(plateau[9]) + "(09)--------------" + couleur(plateau[10]) + "(10)     |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |        " + couleur(plateau[16]) + "(16)-----" +
          couleur(plateau[17]) + "(17)-----" + couleur(plateau[18]) + "(18)       |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print(couleur(plateau[3]) + "(03)---" + couleur(plateau[11]) + "(11)----" +
          couleur(plateau[19]) + "(19)               " +
          couleur(plateau[20]) + "(20)----" + couleur(plateau[12]) + "(12)---" + couleur(plateau[4]) + "(04)")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |        " + couleur(plateau[21]) + "(21)-----" +
          couleur(plateau[22]) + "(22)-----" + couleur(plateau[23]) + "(23)       |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       " + couleur(plateau[13]) + "(13)--------------" +
          couleur(plateau[14]) + "(14)--------------" + couleur(plateau[15]) + "(15)     |")
    print("|                           |                           |")
    print("|                           |                           |")
    print(couleur(plateau[5]) + "(05)----------------------" + couleur(plateau[6]) +
          "(06)----------------------" + couleur(plateau[7]) + "(07)")
    print("\n")


def positionsAdjacentes(position):
    """ Donne la liste des positions adjacentes à une position donnée sur le plateau.
        :param position: int - L'indice de la position dont on veut connaître les adjacences.
        :return: list - Une liste contenant les indices des positions adjacentes. """

    adjacences = [[1, 3], [0, 2, 9], [1, 4], [0, 5, 11], [2, 7, 12], [3, 6], [5, 7, 14], [4, 6], [9, 11],
                  [1, 8, 10, 17], [9, 12], [3, 8, 13, 19], [4, 10, 15, 20], [11, 14], [6, 13, 15, 22], [12, 14],
                  [17, 19], [9, 16, 18], [17, 20], [11, 16, 21], [12, 18, 23], [19, 22], [21, 23, 14], [20, 22]]
    return adjacences[position]


def estSur2Positions(joueur, plateau, p1, p2):
    """ Vérifie si un joueur possède deux pions sur deux positions données.
        :param joueur: int - Identifiant du joueur (1 ou 2).
        :param plateau: list - Liste représentant l'état du plateau.
        :param p1: int - Première position à vérifier.
        :param p2: int - Deuxième position à vérifier.
        :return: bool - True si le joueur possède un pion sur les deux positions, sinon False. """

    return plateau[p1] == joueur and plateau[p2] == joueur


def prochainMoulin(position, plateau, joueur):
    """ Vérifie si un joueur peut former un moulin à la prochaine action.
        :param position: int - L'indice de la position à vérifier.
        :param plateau: list - Liste représentant l'état du plateau.
        :param joueur: int - Identifiant du joueur (1 ou 2).
        :return: bool - True si un moulin peut être formé à la prochaine action, sinon False. """

    moulin = [(estSur2Positions(joueur, plateau, 1, 2) or estSur2Positions(joueur, plateau, 3, 5)),
              (estSur2Positions(joueur, plateau, 0, 2) or estSur2Positions(joueur, plateau, 9, 17)),
              (estSur2Positions(joueur, plateau, 0, 1) or estSur2Positions(joueur, plateau, 4, 7)),
              (estSur2Positions(joueur, plateau, 0, 5) or estSur2Positions(joueur, plateau, 11, 19)),
              (estSur2Positions(joueur, plateau, 2, 7) or estSur2Positions(joueur, plateau, 12, 20)),
              (estSur2Positions(joueur, plateau, 0, 3) or estSur2Positions(joueur, plateau, 6, 7)),
              (estSur2Positions(joueur, plateau, 5, 7) or estSur2Positions(joueur, plateau, 14, 22)),
              (estSur2Positions(joueur, plateau, 2, 4) or estSur2Positions(joueur, plateau, 5, 6)),
              (estSur2Positions(joueur, plateau, 9, 10) or estSur2Positions(joueur, plateau, 11, 13)),
              (estSur2Positions(joueur, plateau, 8, 10) or estSur2Positions(joueur, plateau, 1, 17)),
              (estSur2Positions(joueur, plateau, 8, 9) or estSur2Positions(joueur, plateau, 12, 15)),
              (estSur2Positions(joueur, plateau, 3, 19) or estSur2Positions(joueur, plateau, 8, 13)),
              (estSur2Positions(joueur, plateau, 20, 4) or estSur2Positions(joueur, plateau, 10, 15)),
              (estSur2Positions(joueur, plateau, 8, 11) or estSur2Positions(joueur, plateau, 14, 15)),
              (estSur2Positions(joueur, plateau, 13, 15) or estSur2Positions(joueur, plateau, 6, 22)),
              (estSur2Positions(joueur, plateau, 13, 14) or estSur2Positions(joueur, plateau, 10, 12)),
              (estSur2Positions(joueur, plateau, 17, 18) or estSur2Positions(joueur, plateau, 19, 21)),
              (estSur2Positions(joueur, plateau, 1, 9) or estSur2Positions(joueur, plateau, 16, 18)),
              (estSur2Positions(joueur, plateau, 16, 17) or estSur2Positions(joueur, plateau, 20, 23)),
              (estSur2Positions(joueur, plateau, 16, 21) or estSur2Positions(joueur, plateau, 3, 11)),
              (estSur2Positions(joueur, plateau, 12, 4) or estSur2Positions(joueur, plateau, 18, 23)),
              (estSur2Positions(joueur, plateau, 16, 19) or estSur2Positions(joueur, plateau, 22, 23)),
              (estSur2Positions(joueur, plateau, 6, 14) or estSur2Positions(joueur, plateau, 21, 23)),
              (estSur2Positions(joueur, plateau, 18, 20) or estSur2Positions(joueur, plateau, 21, 22))]
    return moulin[position]


def moulinCree(position, plateau):
    """ Vérifie si un moulin est formé à la position donnée.
        :param position: int - L'indice de la position sur le plateau.
        :param plateau: list - La liste représentant l'état du plateau.
        :return: bool - True si un moulin est formé, sinon False. """

    p = plateau[position]  # Récupération du joueur sur la position donnée
    if p != 'x':           # Vérifie si la position est occupée par un joueur
        return prochainMoulin(position, plateau, p)  # Vérifie si un moulin est formé
    else:
        return False       # Retourne False si la position est vide


def nombrePossibleMoulins(plateau, joueur):
    """ Calcule le nombre de moulins potentiellement réalisables pour un joueur donné.
        :param plateau: Liste représentant l'état actuel du plateau.
        :param joueur: Le joueur concerné ('1' ou '2').
        :return: Nombre de moulins possibles. """
    nombre = 0
    for i in range(len(plateau)):
        if plateau[i] == "x":  # Vérifie si la position est vide
            if prochainMoulin(i, plateau, joueur):  # Vérifie si un moulin peut être formé
                nombre += 1
    return nombre


def moulinEnFormation(position, plateau, joueur):
    """ Vérifie si un pion est en formation pour un moulin potentiel.
        :param position: Position du pion à vérifier.
        :param plateau: Liste représentant l'état actuel du plateau.
        :param joueur: Le joueur concerné ('1' ou '2').
        :return: True si le pion est en formation pour un moulin, False sinon. """

    listeAdjacences = positionsAdjacentes(position)  # Récupère les positions adjacentes
    for i in listeAdjacences:
        if plateau[i] == joueur and not prochainMoulin(position, plateau, joueur):
            return True  # Vérifie s'il y a un pion du même joueur à côté sans que le moulin soit déjà formé
    return False


def nombrePiecesMoulinEnFormation(plateau, joueur):
    """ Compte le nombre de pièces pouvant potentiellement former un moulin.
        :param plateau: Liste représentant l'état actuel du plateau.
        :param joueur: Le joueur concerné ('1' ou '2').
        :return: Nombre de pièces pouvant former un moulin. """

    nombre = 0
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            adjacent_list = positionsAdjacentes(i)  # Récupère les positions adjacentes
            for pos in adjacent_list:
                if joueur == "1":
                    if plateau[pos] == "2":  # Vérifie si un adversaire bloque la formation d'un moulin
                        plateau[i] = "2"
                        if moulinCree(i, plateau):  # Vérifie si un moulin est créé après modification
                            nombre += 1
                        plateau[i] = joueur  # Réinitialise la position après vérification
                else:
                    if plateau[pos] == "1" and moulinEnFormation(pos, plateau, "1"):
                        nombre += 1
    return nombre


def nombrePion(plateau, joueur):
    """ Compte le nombre de pions d'un joueur sur le plateau.
        :param plateau: list - La liste représentant l'état du plateau.
        :param joueur: str - Identifiant du joueur ('1' ou '2').
        :return: int - Nombre de pions du joueur sur le plateau.
        """
    return plateau.count(joueur)


def retirerPiece(copiePlateau, listePlateau, joueur1):
    """ Supprime une pièce adverse du plateau si elle ne fait pas partie d'un moulin.
        :param copiePlateau: list - Copie de l'état actuel du plateau.
        :param listePlateau: list - Liste des configurations possibles après suppression d'un pion.
        :param joueur1: str - Identifiant du joueur actuel ('1' ou '2').
        :return: list - Liste mise à jour des configurations possibles du plateau. """

    joueur2 = '2' if joueur1 == '1' else '1'        # Déterminer l'adversaire
    for i in range(len(copiePlateau)):              # Parcours de toutes les positions du plateau
        if copiePlateau[i] == joueur2:              # Vérifie si la position appartient à l'adversaire
            if not moulinCree(i, copiePlateau):     # Vérifie que le pion ne fait pas partie d'un moulin
                new_board = deepcopy(copiePlateau)  # Copie du plateau actuel
                new_board[i] = 'x'                  # Suppression du pion en remplaçant par 'x'
                listePlateau.append(new_board)      # Ajoute la nouvelle configuration à la liste

    return listePlateau  # Retourne la liste mise à jour des configurations possibles


def mouvementsPossiblesEtape1(plateau):
    """ Génère tous les mouvements possibles pour la phase 1 du jeu (placement des pions sur les cases vides).
        :param plateau: Liste représentant l'état actuel du plateau.
        :return: Liste des états possibles du plateau après un mouvement. """

    listePlateau = []
    for i in range(len(plateau)):
        if plateau[i] == 'x':                 # Vérifie si la position est vide
            copiePlateau = deepcopy(plateau)  # Copie du plateau actuel
            copiePlateau[i] = '1'             # Placement d'un pion du joueur 1

            if moulinCree(i, copiePlateau):   # Vérifie si un moulin est formé
                listePlateau = retirerPiece(copiePlateau, listePlateau, '1')
            else:
                listePlateau.append(copiePlateau)

    return listePlateau


def mouvementsPossiblesEtape2(plateau, joueur):
    """ Génère tous les mouvements possibles pour la phase 2 (déplacement des pions vers des positions adjacentes).
        :param plateau: Liste représentant l'état actuel du plateau.
        :param joueur: Caractère représentant le joueur ('1' ou '2').
        :return: Liste des états possibles du plateau après un mouvement. """

    listePlateau = []
    for i in range(len(plateau)):
        if plateau[i] == joueur:                            # Vérifie si la position contient un pion du joueur
            listePlacesAdjacentes = positionsAdjacentes(i)  # Obtient les cases adjacentes

            for pos in listePlacesAdjacentes:
                if plateau[pos] == 'x':                     # Vérifie si la case adjacente est libre
                    copiePlateau = deepcopy(plateau)
                    copiePlateau[i] = 'x'                   # Vide la position actuelle
                    copiePlateau[pos] = joueur              # Déplace le pion vers la nouvelle position

                    if moulinCree(pos, copiePlateau):       # Vérifie si un moulin est formé après le déplacement
                        listePlateau = retirerPiece(copiePlateau, listePlateau, joueur)
                    else:
                        listePlateau.append(copiePlateau)
    if not listePlateau:  # Vérification pour éviter de retourner une liste vide
        print("\033[91mAucun mouvement valide généré pour le joueur.\033[0m")
    return listePlateau


def mouvementsPossiblesEtape3(plateau, joueur):
    """ Génère tous les mouvements possibles pour la phase 3 (déplacement des pions vers toutes positions libres)
        :param plateau: Liste représentant l'état actuel du plateau.
        :param joueur: Caractère représentant le joueur ('1' ou '2').
        :return: Liste des états possibles du plateau après un mouvement. """
    listePlateau = []
    for i in range(len(plateau)):
        if plateau[i] == joueur:                     # Vérifie si la position contient un pion du joueur
            for j in range(len(plateau)):
                if plateau[j] == 'x':                # Vérifie si la case cible est libre
                    copiePlateau = deepcopy(plateau)
                    copiePlateau[i] = 'x'            # Vide la position actuelle
                    copiePlateau[j] = joueur         # Déplace le pion vers la nouvelle position

                    if moulinCree(j, copiePlateau):  # Vérifie si un moulin est formé après le déplacement
                        listePlateau = retirerPiece(copiePlateau, listePlateau, joueur)
                    else:
                        listePlateau.append(copiePlateau)

    if not listePlateau:  # Vérification pour éviter de retourner une liste vide
        print("\033[91mAucun mouvement valide généré pour le joueur.\033[0m")
    return listePlateau


def mouvementsPossiblesEtape2ou3(plateau, joueur='1'):
    """ Génère tous les mouvements possibles selon la phase du jeu (phase 2 ou phase 3).
        :param plateau: Liste représentant l'état actuel du plateau.
        :param joueur: Caractère représentant le joueur ('1' ou '2').
        :return: Liste des états possibles du plateau après un mouvement. """

    if nombrePion(plateau, joueur) == 3:  # Si le joueur a seulement trois pions, il passe à la phase 3 (voler)
        return mouvementsPossiblesEtape3(plateau, joueur)
    else:                                 # Sinon, il reste en phase 2 (déplacement adjacents)
        return mouvementsPossiblesEtape2(plateau, joueur)


def plateauInverse(plateau):
    """ Inverse le plateau de jeu en échangeant les pions des joueurs.
        :param plateau: Liste représentant l'état actuel du plateau.
        :return: Liste représentant le plateau inversé. """

    plateauInv = []
    for i in plateau:
        if i == "1":
            plateauInv.append("2")  # Remplace les pions du joueur 1 par ceux du joueur 2
        elif i == "2":
            plateauInv.append("1")  # Remplace les pions du joueur 2 par ceux du joueur 1
        else:
            plateauInv.append("x")  # Conserve les positions vides
    return plateauInv


def genereListePlateauInverse(listePositions):
    """ Génère une liste de plateaux inversés à partir d'une liste de positions.
        :param listePositions: Liste de plateaux représentant différentes configurations de jeu.
        :return: Liste de plateaux inversés. """

    resultat = []
    for i in listePositions:
        resultat.append(plateauInverse(i))  # Applique l'inversion à chaque plateau de la liste
    return resultat


""" ================================ Fonctions liées aux interactions utilisateur ================================ 
    C'est la demande d'une position pour un pion, jouer le tour, ou encore verifier la victoire. """


def demanderPosition(message):
    """ Demande une position valide à l'utilisateur et la retourne.
        :param message: Message affiché pour demander une position.
        :return: Un entier correspondant à une position valide sur le plateau. """

    while True:
        try:
            pos = int(input(message))  # Demande une position et la convertit en entier
            if 0 <= pos < 24:          # Vérifie que la position est valide (entre 0 et 23)
                return pos
            else:
                print("\033[91mPosition invalide. Réessayez.\033[0m")  # Message d'erreur si hors limites
        except ValueError:
            print("\033[91mEntrée invalide. Réessayez.\033[0m")        # Message d'erreur si pas un nombre


def retirerPionAdverse(plateau, joueurAdverse):
    """ Permet au joueur actuel de retirer un pion adverse après avoir formé un moulin.
        :param plateau: Liste représentant l'état du plateau.
        :param joueurAdverse: Caractère représentant le joueur adverse ('1' ou '2'). """

    while True:
        pos = demanderPosition(f"\033[94mRetirez une pièce du joueur {joueurAdverse} :\033[0m ")
        # Vérifie que la position contient bien un pion adverse et qu'il n'est pas protégé par un moulin,
        # sauf si l'adversaire n'a que 3 pions restants (dans ce cas, on peut enlever n'importe quel pion).
        if plateau[pos] == joueurAdverse and (not moulinCree(pos, plateau) or nombrePion(plateau, joueurAdverse) == 3):
            plateau[pos] = 'x'  # Remplace le pion retiré par une case vide ('x')
            break
        else:
            print("\033[91mPosition invalide. Réessayez.\033[0m")  # Message d'erreur si la position est incorrecte


def jouerTourHumain(joueur, plateau, phase1=True):
    """ Gère le tour du joueur humain (phase 1 : placement des pions - phase 2/3 : déplacement des pions.)
        :param joueur: Caractère représentant le joueur ('1' ou '2').
        :param plateau: Liste représentant l'état du plateau.
        :param phase1: Booléen indiquant si le jeu est en phase 1 (True) ou en phase 2/3 (False). """

    couleur = "\033[94m" if joueur == '1' else "\033[95m"  # Définition de la couleur selon le joueur
    adversaire = '2' if joueur == '1' else '1'  # Identification de l'adversaire

    if phase1:  # phase 1 : placement des pions
        print(f"{couleur}Joueur {joueur} : Placez une pièce sur le plateau.\033[0m")
        while True:
            pos = demanderPosition(f"{couleur}Entrez une position : \033[0m")
            if plateau[pos] == 'x':           # Vérifie que la case est libre
                plateau[pos] = joueur         # Place le pion du joueur à cette position
                if moulinCree(pos, plateau):  # Vérifie si un moulin a été formé
                    print(f"{couleur}Vous avez formé un moulin !\033[0m")
                    retirerPionAdverse(plateau, adversaire)  # Permet au joueur de retirer un pion adverse
                break
            else:
                print("\033[91mPosition occupée. Réessayez.\033[0m")  # Message d'erreur si la case est occupée

    else:  # phase 2/3 : déplacement des pions
        print(f"{couleur}Joueur {joueur} : Déplacez une pièce.\033[0m")
        # Si le joueur n'a plus que 3 pions, il peut "voler" sur n'importe quelle case libre
        if nombrePion(plateau, joueur) == 3:
            print(f"{couleur}Vous avez seulement 3 pions. Vous pouvez voler vers n'importe quelle position !\033[0m")

        while True:
            pos1 = demanderPosition(f"{couleur}Choisissez une pièce à déplacer : \033[0m")
            if plateau[pos1] == joueur:  # Vérifie que la case contient un pion du joueur

                # Détermine les mouvements autorisés :
                # - Soit les cases adjacentes si plus de 3 pions.
                # - Soit toutes les cases vides si le joueur n'a plus que 3 pions (règle du vol).
                positionsPossibles = positionsAdjacentes(pos1) if nombrePion(plateau, joueur) > 3 else range(24)
                pos2 = demanderPosition(f"{couleur}Choisissez une nouvelle position : \033[0m")
                if pos2 in positionsPossibles and plateau[pos2] == 'x':  # Vérifie si le déplacement est valide
                    plateau[pos1] = 'x'     # Vide l'ancienne position
                    plateau[pos2] = joueur  # Place le pion à la nouvelle position

                    if moulinCree(pos2, plateau):  # Vérifie si un moulin a été formé après le déplacement
                        print(f"{couleur}Vous avez formé un moulin !\033[0m")
                        retirerPionAdverse(plateau, adversaire)  # Permet de retirer un pion adverse
                    break
                else:
                    print("\033[91mDéplacement invalide. Réessayez.\033[0m")  # Message d'erreur si mouvement interdit
            else:
                print("\033[91mCe n'est pas votre pièce. Réessayez.\033[0m")  # Message d'erreur si pas son pion


def verifierVictoire(plateau):
    """ Vérifie si un joueur a gagné (si son adversaire a moins de 3 pions OU si son adversaire ne peut plus faire de
        mouvement légal).
        :param plateau: Liste représentant l'état du plateau. """

    # Vérifie si le joueur 1 a perdu (moins de 3 pions ou aucun déplacement possible)
    if nombrePion(plateau, '1') < 3 or len(mouvementsPossiblesEtape2ou3(plateau, '1')) == 0:
        print("\033[95m\n--- Joueur 2 a gagné ! ---\033[0m")
        sys.exit()  # Termine le programme immédiatement

    # Vérifie si le joueur 2 a perdu
    elif nombrePion(plateau, '2') < 3 or len(mouvementsPossiblesEtape2ou3(plateau, '2')) == 0:
        print("\033[94m\n--- Joueur 1 a gagné ! ---\033[0m")
        sys.exit()
