# TP2 IA UQAC - CSP SUDOKU

> Pour l'exécution du programme, **aucune librairie n'est nécessaire**. 

## Prérequis

- Python (3.9 idéalement)

## Execution

Deux façons d'exécuter le programme :

### Générer une grille aléatoire 9x9 :

```bash
python3 Main.py random *difficulty*
```
Avec *difficulty* un entier entre 1 et 9.

### Lire un fichier de sudoku :

```bash
python3 Main.py read *filename*
```
 
#### Syntaxe du fichier de sudoku

```
*lines*x*columns*
X X X X ...
X X X X ...
...
```
  
 - *lines* et *columns* donne la taille d'un "sous carré" du Sudoku. Par exemple pour une grille de taille 9x9, il faut entrer les valeurs 3x3. 
 - 1 <= *lines* x *columns* <= 16. 16 est la taille maximum d'une grille de sudoku.
 - Les X représentent les cases de la grille. Ils peuvent prendre une valeur de 1 à 9 et de A à G. A et G sont les nombres de 10 à 16. 0 représente une case vide.
 - Exemple :
 
  2x3
  0 0 3 1 0 0
  0 6 0 0 0 0
  0 4 2 3 1 0
  5 0 0 0 0 0
  0 0 0 0 2 0
  0 0 0 0 6 0

Représente cette grille :

============================
||   |   | 3 || 1 |   |   ||
----------------------------
||   | 6 |   ||   |   |   ||
============================
||   | 4 | 2 || 3 | 1 |   ||
----------------------------
|| 5 |   |   ||   |   |   ||
============================
||   |   |   ||   | 2 |   ||
----------------------------
||   |   |   ||   | 6 |   ||
============================
 
