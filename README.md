# MASTERMIND by Elina

## Description

Ce projet est un jeu de logique appelé **Mastermind**. Le joueur doit deviner une combinaison secrete de 4 nombres entre 0 et 5. Après chaque proposition, le jeu donne des indices pour aider a trouver la bonne combinaison.



## Comment sa marche ?

1. L'ordinateur genere une combinaison secrete aleatoire (4 nombres de 0 a 5)
2. Le joueur doit deviner cette combinaison
3. Après chaque tentative, le jeu affiche :
   - **Bien place** : le nombre est correct ET a la bonne position
   - **Mal place** : le nombre est correct MAIS a la mauvaise position
4. Le joueur a maximum **10 tentatives** pour trouver

### Exemple

```
Combinaison secrete : [1, 3, 4, 2]
Ma proposition :      [1, 2, 3, 4]

Resultat :
- Bien place : 1
- Mal place : 2
```

---

## Gameplay

1. **Clique sur les 6 couleurs** affichees en bas
2. **Remplis les 4 positions** (de gauche a droite)
3. **Clique sur VALIDATE** pour proposer ta combinaison
4. **Lis les indices** et recommence

### Controles

- **Souris** : cliquer sur les couleurs
- **Clavier (0-5)** : selectionner directement
- **Fleches** : changer de position
- **Backspace** : effacer une selection

---

## Structure du code

### main.py - `MastermindGame`

- `generate_secret()` : cree la combinaison secrete aleatoire
- `check_guess()` : verifie si la proposition est valide
- `calculate_clues()` : compare la proposition avec le secret
- `play_turn()` : execute un tour du jeu
- `restart_game()` : recommence une nouvelle partie

### interface.py - `GameInterface`

- Affiche le jeu avec pygame
- Gere les clics de souris et l'historique
- Affiche les indices et les messages

---

## Concepts utilises

### Listes
```python
secret_combination = [1, 3, 4, 2]
```

### Boucles
```python
for position in range(4):
    # faire quelque chose
```

### Conditions
```python
if len(guess) != 4:
    return False
```

### Dictionnaires
```python
result = {'correct_position': 2, 'wrong_position': 1}
```

### Classes
```python
class MastermindGame:
    def play_turn(self, guess):
        # logique du jeu
```



## Auteur

Cree par **Elina** - Projet d'apprentissage Python 