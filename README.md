# Minimax & Élagage Alpha-Bêta pour le jeu du Neuf Hommes de Morris

Ce projet propose une implémentation complète du célèbre jeu de plateau Neuf Hommes de Morris (également appelé Jeu du Moulin), intégrant une intelligence artificielle capable de jouer contre un humain ou contre elle-même.

L'IA repose sur l'algorithme Minimax avec optimisation par élagage alpha-bêta, permettant une prise de décision efficace et intelligente.

Le jeu se fait via la console, avec un affichage clair et coloré.

## Architecture du Projet
```
src/
│
├── jeu/                      # Contenant différents modes de jeu éxécutables
│   ├── HumainVsHumain.py     # Deux humains s'affrontent
│   ├── HumainVsIA.py         # Un humain affronte une IA
│   ├── IAVsIA.py             # Deux IA s'affrontent
│
├── ia/                       # Contenant les fonctions, algorithmes et classes nécessaires au jeu et à l'IA
│   ├── utils.py              # Toutes les fonctions de bases pour le jeu et l'IA
│   ├── minimax.py            # L'implémentation de l'algorithme Minimax avec élagage Alpha Beta
│   ├── heuristiques.py       # Différentes heuristiques : naïve, avancée, et experte
│
├── __init__.py               # Permet de marquer le répertoire comme un package Python.
│
```

## Prérequis
- Python 3.7 ou supérieur est requis.
- Aucun téléchargement supplémentaire n'est nécessaire. Les seules bibliothèques utilisées, copy et sys, font partie de 
la bibliothèque standard de Python.



## Exécution

3 Modes de jeu sont disponibles :

- **Deux humains s'affrontent**, via le fichier *HumainVsHumain.py*. L'exécution se fait 
depuis le répertoire du projet tel que : 
```
python3 -m src.jeu.HumainVsHumain
```
- **Un humain affronte une IA**, via le fichier *HumainVsIA.py*. L'exécution se fait via la commande suivante, avec les 
arguments **optionnels** *niveauIA* (un entier compris entre 1 et 3, 3 étant l'heuristique la plus avancée) et 
*profondeur* (un entier indiquant la profondeur de recherche de l'algorithme minimax).\
Sans ces arguments, la partie se lance avec une heuristique de niveau 3/3 et une profondeur de 4.
```
python3 -m src.jeu.HumainVsIA <niveauIA> <profondeur>
```

- **Deux IA s'affrontent**, via le fichier *IAVsIA.py* et la commande :
```
python3 -m src.jeu.IAVsIA
```

*Dans les commandes ci-dessus, -m permet d'exécuter les fichiers tels qu'un module, ce qui permet à Python de traiter src comme un package 
principal et gèrer correctement les imports relatifs.*


## Auteur & Crédits
Projet réalisé dans le cadre pédagogique de l'UE d'Intelligence Artificielle

Auteur : Aidoudi Aaron
