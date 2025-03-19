# Minimax & Élagage Alpha-Bêta pour le jeu du Neuf Hommes de Morris

Ce projet propose une implémentation complète du célèbre jeu de plateau Neuf Hommes de Morris (également appelé "Jeu du Moulin"), intégrant une intelligence artificielle capable de jouer contre un humain ou contre elle-même.

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
│   ├── heuristiques.py       # Différentes heuristiques plus ou moins avancées
│
```

## Prérequis
Aucun téléchargement supplémentaire n'est nécessaire.

## Exécution

3 Modes de jeu sont disponibles :
- Deux humains s'affrontent, dans le fichier  *HumainVsHumain.py*
- Un humain affronte une IA, dans le fichier *HumainVsIA.py*
- Deux IA s'affrontent, dans le fichier *IAVsIA.py*

En fonction, il l'éxecution se fait depuis le repertoire src via la commande (par exemple pour HumainVsIA)
```
python3 jeu/HumainVsIA.py
```

## Auteur & Crédits
Projet réalisé dans le cadre pédagogique de l'UE d'Intelligence Artificielle

Auteur : Aidoudi Aaron
