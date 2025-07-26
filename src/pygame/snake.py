import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
TAILLE_CASE = 20
FPS = 10

# Couleurs
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)
VERT_FONCE = (0, 150, 0)

class Snake:
    def __init__(self):
        self.positions = [(LARGEUR//2, HAUTEUR//2)]
        self.direction = (TAILLE_CASE, 0)  # Droite par défaut
        self.grandir = False
        
    def bouger(self):
        tete = self.positions[0]
        nouvelle_tete = (tete[0] + self.direction[0], tete[1] + self.direction[1])
        
        # Vérifier les collisions avec les bords
        if (nouvelle_tete[0] < 0 or nouvelle_tete[0] >= LARGEUR or
            nouvelle_tete[1] < 0 or nouvelle_tete[1] >= HAUTEUR):
            return False
            
        # Vérifier les collisions avec soi-même
        if nouvelle_tete in self.positions:
            return False
            
        self.positions.insert(0, nouvelle_tete)
        
        if not self.grandir:
            self.positions.pop()
        else:
            self.grandir = False
            
        return True
    
    def changer_direction(self, nouvelle_direction):
        # Empêcher le serpent de revenir sur lui-même
        if (nouvelle_direction[0] * -1, nouvelle_direction[1] * -1) != self.direction:
            self.direction = nouvelle_direction
    
    def manger(self):
        self.grandir = True
    
    def dessiner(self, ecran):
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(position[0], position[1], TAILLE_CASE, TAILLE_CASE)
            if i == 0:  # Tête du serpent
                pygame.draw.rect(ecran, VERT_FONCE, rect)
            else:  # Corps du serpent
                pygame.draw.rect(ecran, VERT, rect)
            pygame.draw.rect(ecran, BLANC, rect, 1)

class Nourriture:
    def __init__(self):
        self.position = self.generer_position()
    
    def generer_position(self):
        x = random.randint(0, (LARGEUR - TAILLE_CASE) // TAILLE_CASE) * TAILLE_CASE
        y = random.randint(0, (HAUTEUR - TAILLE_CASE) // TAILLE_CASE) * TAILLE_CASE
        return (x, y)
    
    def dessiner(self, ecran):
        rect = pygame.Rect(self.position[0], self.position[1], TAILLE_CASE, TAILLE_CASE)
        pygame.draw.rect(ecran, ROUGE, rect)

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Snake Game")
        self.horloge = pygame.time.Clock()
        self.snake = Snake()
        self.nourriture = Nourriture()
        self.score = 0
        self.police = pygame.font.Font(None, 36)
        
    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.changer_direction((0, -TAILLE_CASE))
                elif event.key == pygame.K_DOWN:
                    self.snake.changer_direction((0, TAILLE_CASE))
                elif event.key == pygame.K_LEFT:
                    self.snake.changer_direction((-TAILLE_CASE, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.changer_direction((TAILLE_CASE, 0))
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def verifier_collision_nourriture(self):
        if self.snake.positions[0] == self.nourriture.position:
            self.snake.manger()
            self.score += 10
            # Générer nouvelle nourriture en évitant le corps du serpent
            while True:
                self.nourriture.position = self.nourriture.generer_position()
                if self.nourriture.position not in self.snake.positions:
                    break
    
    def dessiner(self):
        self.ecran.fill(NOIR)
        self.snake.dessiner(self.ecran)
        self.nourriture.dessiner(self.ecran)
        
        # Afficher le score
        texte_score = self.police.render(f"Score: {self.score}", True, BLANC)
        self.ecran.blit(texte_score, (10, 10))
        
        # Afficher les instructions
        texte_instructions = pygame.font.Font(None, 24).render("Utilisez les flèches pour bouger, ESC pour quitter", True, BLANC)
        self.ecran.blit(texte_instructions, (10, HAUTEUR - 30))
        
        pygame.display.flip()
    
    def afficher_game_over(self):
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(128)
        overlay.fill(NOIR)
        self.ecran.blit(overlay, (0, 0))
        
        texte_game_over = self.police.render("GAME OVER!", True, ROUGE)
        texte_score_final = self.police.render(f"Score final: {self.score}", True, BLANC)
        texte_rejouer = pygame.font.Font(None, 24).render("Appuyez sur ESPACE pour rejouer ou ESC pour quitter", True, BLANC)
        
        # Centrer les textes
        rect_game_over = texte_game_over.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50))
        rect_score = texte_score_final.get_rect(center=(LARGEUR//2, HAUTEUR//2))
        rect_rejouer = texte_rejouer.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))
        
        self.ecran.blit(texte_game_over, rect_game_over)
        self.ecran.blit(texte_score_final, rect_score)
        self.ecran.blit(texte_rejouer, rect_rejouer)
        
        pygame.display.flip()
    
    def reinitialiser(self):
        self.snake = Snake()
        self.nourriture = Nourriture()
        self.score = 0
    
    def executer(self):
        en_cours = True
        jeu_termine = False
        
        while en_cours:
            if not jeu_termine:
                en_cours = self.gerer_evenements()
                
                if en_cours:
                    # Déplacer le serpent
                    if not self.snake.bouger():
                        jeu_termine = True
                    
                    # Vérifier si le serpent mange la nourriture
                    self.verifier_collision_nourriture()
                    
                    self.dessiner()
            else:
                # Game Over
                self.afficher_game_over()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_cours = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.reinitialiser()
                            jeu_termine = False
                        elif event.key == pygame.K_ESCAPE:
                            en_cours = False
            
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Lancer le jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()