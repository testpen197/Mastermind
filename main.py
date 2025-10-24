import random
from interface import GameInterface

class MastermindGame:
    
    def __init__(self):
        # Les 6 couleurs disponibles (representees par des nombres)
        self.colors = [1, 2, 3, 4, 5, 6]
        
        # La combinaison secrete que le joueur doit deviner
        self.secret_combination = self.generate_secret()
        
        # Nombre de tentatives du joueur
        self.attempt_count = 0
        
        # Nombre maximum de tentatives autorisees
        self.max_attempts = 10
        
        # Liste pour garder l'historique de toutes les tentatives
        self.history = []
        
        # Boolean pour savoir si la partie est terminee
        self.game_over = False
        
        # Boolean pour savoir si le joueur a gagne
        self.player_won = False
    
    def generate_secret(self):
        
        secret = []
        for i in range(4):
            random_color = random.randint(0, 5)
            secret.append(random_color)
        return secret
    
    def check_guess(self, guess):
       
        # Verifier si la proposition a exactement 4 elements
        if len(guess) != 4:
            return False, "La combinaison doit avoir exactement 4 nombres"
        
        # Verifier si tous les elements sont entre 0 et 5
        for number in guess:
            if number < 0 or number > 5:
                return False, "Les nombres doivent etre entre 0 et 5"
        
        return True, ""
    
    def calculate_clues(self, guess):
       
        # Copier les listes pour ne pas les modifier
        secret_copy = self.secret_combination.copy()
        guess_copy = guess.copy()
        
        correct_position = 0
        wrong_position = 0
        
        # ETAPE 1: Compter les nombres bien places
        # Parcourir chaque position (0, 1, 2, 3)
        for position in range(4):
            if guess_copy[position] == secret_copy[position]:
                # Le nombre est au bon endroit
                correct_position = correct_position + 1
                # Marquer comme traite avec -1
                secret_copy[position] = -1
                guess_copy[position] = -1
        
        # ETAPE 2: Compter les nombres mal places
        # Parcourir chaque position de la proposition
        for position in range(4):
            # Si ce nombre n'a pas deja ete compte
            if guess_copy[position] != -1:
                # Verifier si ce nombre existe ailleurs dans le secret
                if guess_copy[position] in secret_copy:
                    wrong_position = wrong_position + 1
                    # Retirer ce nombre pour eviter double comptage
                    index = secret_copy.index(guess_copy[position])
                    secret_copy[index] = -1
        
        return {
            'correct_position': correct_position,
            'wrong_position': wrong_position
        }
    
    def play_turn(self, guess):
       
        # Valider la proposition
        is_valid, error_message = self.check_guess(guess)
        
        if not is_valid:
            return {'valid': False, 'message': error_message}
        
        # Incrementer le compteur de tentatives
        self.attempt_count = self.attempt_count + 1
        
        # Calculer les indices
        clues = self.calculate_clues(guess)
        
        # Ajouter a l'historique
        self.history.append({
            'attempt': self.attempt_count,
            'guess': guess,
            'correct': clues['correct_position'],
            'wrong': clues['wrong_position']
        })
        
        # Verifier la victoire
        if clues['correct_position'] == 4:
            self.game_over = True
            self.player_won = True
            message = f"VICTOIRE! Vous avez trouve en {self.attempt_count} tentatives!"
            return {
                'valid': True,
                'correct': clues['correct_position'],
                'wrong': clues['wrong_position'],
                'message': message,
                'finished': True,
                'won': True
            }
        
        # Verifier la defaite
        if self.attempt_count >= self.max_attempts:
            self.game_over = True
            self.player_won = False
            secret_str = ' '.join(str(x) for x in self.secret_combination)
            message = f"DEFAITE! La combinaison etait: {secret_str}"
            return {
                'valid': True,
                'correct': clues['correct_position'],
                'wrong': clues['wrong_position'],
                'message': message,
                'finished': True,
                'won': False
            }
        
        # Le jeu continue
        message = f"Bien places: {clues['correct_position']} | Mal places: {clues['wrong_position']}"
        return {
            'valid': True,
            'correct': clues['correct_position'],
            'wrong': clues['wrong_position'],
            'message': message,
            'finished': False
        }
    
    def restart_game(self):
        """
        Reinitialise le jeu pour une nouvelle partie.
        """
        self.secret_combination = self.generate_secret()
        self.attempt_count = 0
        self.history = []
        self.game_over = False
        self.player_won = False


if __name__ == "__main__":
    # Creer une instance du jeu
    game = MastermindGame()
    
    # Creer l'interface et lancer le jeu
    interface = GameInterface(game)
    interface.run()