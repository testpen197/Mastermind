import pygame

class GameInterface:
   
    
    def __init__(self, game):
        # Initialiser pygame
        pygame.init()
        
        # Garder une reference au jeu
        self.game = game
        
        # Dimensions de la fenetre
        self.window_width = 700
        self.window_height = 800
        
        # Creer la fenetre
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("MASTERMIND - Guess the combination")
        
        # Horloge pour la vitesse du jeu
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Couleurs (RGB)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (150, 150, 150)
        self.light_gray = (200, 200, 200)
        self.blue = (50, 100, 200)
        self.dark_blue = (30, 60, 120)
        self.green = (100, 200, 100)
        self.red = (200, 100, 100)
        
        # Les couleurs du jeu (6 couleurs)
        self.color_boxes = [
            (255, 0, 0),      # 0 - Rouge
            (255, 165, 0),    # 1 - Orange
            (255, 255, 0),    # 2 - Jaune
            (0, 200, 0),      # 3 - Vert
            (0, 0, 255),      # 4 - Bleu
            (150, 0, 150)     # 5 - Violet
        ]
        
        # Police d'ecriture
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Charger l'image personnalisee
        try:
            self.image = pygame.image.load("images/image.png")
            # Redimensionner l'image (largeur, hauteur)
            self.image = pygame.transform.scale(self.image, (100, 100))
        except:
            self.image = None
        
        # Selection du joueur
        self.player_selection = [None, None, None, None]
        self.current_position = 0
        
        # Messages
        self.current_message = ""
        self.final_message = ""
    
    def draw_title(self):
       
        title_text = self.font_large.render("MASTERMIND by Elina", True, self.blue)
        self.screen.blit(title_text, (80, 20))
        
        instruction_text = self.font_small.render("Guess the combination: 4 numbers (0-5)", True, self.gray)
        self.screen.blit(instruction_text, (100, 70))
        
        # Afficher l'image personnalisee
        if self.image:
            self.screen.blit(self.image, (550, 20))
    
    def draw_attempt_counter(self):
       
        counter_text = f"Attempt: {self.game.attempt_count}/{self.game.max_attempts}"
        text_surface = self.font_medium.render(counter_text, True, self.blue)
        self.screen.blit(text_surface, (200, 110))
    
    def draw_player_selection(self):
        
        y_position = 170
        
        title_text = self.font_small.render("Your combination:", True, self.blue)
        self.screen.blit(title_text, (50, y_position))
        
        # Pour chaque position (0, 1, 2, 3)
        for position in range(4):
            x_position = 150 + (position * 100)
            box_size = 60
            
            # Determiner la couleur de la bordure
            border_color = self.blue if position == self.current_position else self.gray
            
            # Dessiner la case
            pygame.draw.rect(self.screen, self.dark_blue, (x_position, y_position + 40, box_size, box_size))
            pygame.draw.rect(self.screen, border_color, (x_position, y_position + 40, box_size, box_size), 3)
            
            # Si une couleur est selectionnee
            if self.player_selection[position] is not None:
                color_index = self.player_selection[position]
                color = self.color_boxes[color_index]
                
                # Petit carre de couleur au centre
                pygame.draw.rect(self.screen, color, (x_position + 10, y_position + 50, 40, 40))
                pygame.draw.rect(self.screen, self.white, (x_position + 10, y_position + 50, 40, 40), 2)
            else:
                # Afficher le point d'interrogation
                question_text = self.font_medium.render("?", True, self.gray)
                self.screen.blit(question_text, (x_position + 20, y_position + 45))
    
    def draw_color_buttons(self):
        
        y_position = 330
        
        instruction_text = self.font_small.render("Click a color (0-5):", True, self.blue)
        self.screen.blit(instruction_text, (50, y_position))
        
        # Pour chaque couleur (0 a 5)
        for color_index in range(6):
            x_position = 100 + (color_index * 90)
            box_size = 50
            
            # Couleur du bouton
            color = self.color_boxes[color_index]
            
            # Dessiner le bouton
            pygame.draw.rect(self.screen, color, (x_position, y_position + 40, box_size, box_size))
            pygame.draw.rect(self.screen, self.white, (x_position, y_position + 40, box_size, box_size), 2)
            
            # Afficher le numero
            number_text = self.font_small.render(str(color_index), True, self.white)
            self.screen.blit(number_text, (x_position + 18, y_position + 50))
    
    def draw_history(self):
       
        y_position = 450
        
        history_title = self.font_small.render("History:", True, self.blue)
        self.screen.blit(history_title, (50, y_position))
        
        # Pour chaque tentative dans l'historique
        for entry in self.game.history[-3:]:
            y_position = y_position + 30
            
            # Extraire les informations
            attempt_num = entry['attempt']
            guess = entry['guess']
            correct = entry['correct']
            wrong = entry['wrong']
            
            # Convertir la proposition en texte
            guess_text = ' '.join(str(x) for x in guess)
            
            # Afficher la ligne
            line_text = f"{attempt_num}. [{guess_text}] -> Good: {correct}, Wrong: {wrong}"
            text_surface = self.font_small.render(line_text, True, self.white)
            self.screen.blit(text_surface, (60, y_position))
    
    def draw_message(self):
        
        message = self.final_message if self.final_message else self.current_message
        
        if not message:
            return
        
        # Determiner la couleur du message
        if "VICTOIRE" in message:
            message_color = self.green
        elif "DEFAITE" in message:
            message_color = self.red
        else:
            message_color = self.white
        
        # Afficher le message
        text_surface = self.font_small.render(message, True, message_color)
        self.screen.blit(text_surface, (50, 680))
    
    def draw_validate_button(self):
        
        button_x = 200
        button_y = 620
        button_width = 300
        button_height = 40
        
        # Verifier si tous les nombres sont selectionnes
        all_selected = all(x is not None for x in self.player_selection)
        
        # Couleur du bouton
        if all_selected:
            button_color = self.green
        else:
            button_color = self.gray
        
        # Dessiner le bouton
        pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, self.white, (button_x, button_y, button_width, button_height), 2)
        
        # Texte du bouton
        button_text = self.font_medium.render("VALIDATE", True, self.white)
        self.screen.blit(button_text, (300, 625))
        
        # Retourner le rectangle du bouton pour les clics
        return pygame.Rect(button_x, button_y, button_width, button_height)
    
    def draw_restart_button(self):
        
        if not self.game.game_over:
            return None
        
        button_x = 200
        button_y = 740
        button_width = 300
        button_height = 40
        
        # Dessiner le bouton
        pygame.draw.rect(self.screen, self.blue, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, self.white, (button_x, button_y, button_width, button_height), 2)
        
        # Texte du bouton
        button_text = self.font_medium.render("PLAY AGAIN", True, self.white)
        self.screen.blit(button_text, (265, 745))
        
        # Retourner le rectangle du bouton pour les clics
        return pygame.Rect(button_x, button_y, button_width, button_height)
    
    def handle_mouse_click(self, mouse_pos, validate_button, restart_button):
       
        # Verifier les clics sur les boutons de couleurs
        for color_index in range(6):
            x_position = 100 + (color_index * 90)
            button_rect = pygame.Rect(x_position, 370, 50, 50)
            
            if button_rect.collidepoint(mouse_pos):
                # Selectionner cette couleur a la position actuelle
                self.player_selection[self.current_position] = color_index
                
                # Passer a la position suivante
                if self.current_position < 3:
                    self.current_position = self.current_position + 1
        
        # Verifier le clic sur le bouton Valider
        if validate_button.collidepoint(mouse_pos):
            all_selected = all(x is not None for x in self.player_selection)
            
            if all_selected:
                # Jouer le tour
                result = self.game.play_turn(self.player_selection)
                
                if result['valid']:
                    self.current_message = result['message']
                    
                    if result['finished']:
                        self.final_message = result['message']
                    
                    # Reinitialiser la selection
                    self.player_selection = [None, None, None, None]
                    self.current_position = 0
        
        # Verifier le clic sur le bouton Recommencer
        if restart_button and restart_button.collidepoint(mouse_pos):
            self.game.restart_game()
            self.player_selection = [None, None, None, None]
            self.current_position = 0
            self.current_message = ""
            self.final_message = ""
    
    def run(self):
        
        running = True
        
        while running:
            # Gerer les evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    validate_button = pygame.Rect(200, 620, 300, 40)
                    restart_button_rect = None
                    
                    if self.game.game_over:
                        restart_button_rect = pygame.Rect(200, 740, 300, 40)
                    
                    self.handle_mouse_click(event.pos, validate_button, restart_button_rect)
            
            # Remplir l'ecran de noir
            self.screen.fill(self.black)
            
            # Dessiner tous les elements
            self.draw_title()
            self.draw_attempt_counter()
            self.draw_player_selection()
            self.draw_color_buttons()
            self.draw_history()
            self.draw_message()
            validate_button = self.draw_validate_button()
            self.draw_restart_button()
            
            # Mettre a jour l'affichage
            pygame.display.flip()
            
            # Limiter a 60 images par seconde
            self.clock.tick(self.fps)
        
        # Quitter pygame
        pygame.quit()