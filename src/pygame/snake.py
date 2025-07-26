import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Obtenir la résolution de l'écran
info_ecran = pygame.display.Info()
LARGEUR_ECRAN = info_ecran.current_w
HAUTEUR_ECRAN = info_ecran.current_h

# Constantes
TAILLE_CASE = 60
FPS = 10
MARGE = 100  # Marge autour de la zone de jeu
LARGEUR_JEU = LARGEUR_ECRAN - 2 * MARGE
HAUTEUR_JEU = HAUTEUR_ECRAN - 2 * MARGE
EPAISSEUR_BORDURE = 5

# Ajuster les dimensions pour qu'elles soient multiples de TAILLE_CASE
LARGEUR_JEU = (LARGEUR_JEU // TAILLE_CASE) * TAILLE_CASE
HAUTEUR_JEU = (HAUTEUR_JEU // TAILLE_CASE) * TAILLE_CASE

# Couleurs
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)
VERT_FONCE = (0, 150, 0)
BLEU = (0, 100, 255)
GRIS_FONCE = (30, 30, 30)

# Couleurs pour le serpent réaliste
VERT_SERPENT_CLAIR = (50, 200, 50)
VERT_SERPENT_FONCE = (30, 120, 30)
VERT_SERPENT_TETE = (40, 180, 40)
JAUNE_OEIL = (255, 255, 0)
NOIR_PUPILLE = (0, 0, 0)

# Couleurs pour la pomme
ROUGE_POMME = (220, 20, 20)
ROUGE_POMME_FONCE = (180, 15, 15)
VERT_FEUILLE = (34, 139, 34)
MARRON_TIGE = (139, 69, 19)

class Snake:
    def __init__(self):
        self.positions = [(MARGE + LARGEUR_JEU//2, MARGE + HAUTEUR_JEU//2)]
        self.direction = (TAILLE_CASE, 0)  # Droite par défaut
        self.grandir = False
        
    def bouger(self):
        tete = self.positions[0]
        nouvelle_tete = (tete[0] + self.direction[0], tete[1] + self.direction[1])
        
        # Vérifier les collisions avec les bords de la zone de jeu
        if (nouvelle_tete[0] < MARGE or nouvelle_tete[0] >= MARGE + LARGEUR_JEU or
            nouvelle_tete[1] < MARGE or nouvelle_tete[1] >= MARGE + HAUTEUR_JEU):
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
            if i == 0:  # Tête du serpent
                self.dessiner_tete(ecran, position)
            else:  # Corps du serpent
                self.dessiner_corps(ecran, position, i)
    
    def dessiner_tete(self, ecran, position):
        # Corps de la tête (cercle principal)
        centre = (position[0] + TAILLE_CASE//2, position[1] + TAILLE_CASE//2)
        rayon = TAILLE_CASE//2 - 3
        pygame.draw.circle(ecran, VERT_SERPENT_TETE, centre, rayon)
        pygame.draw.circle(ecran, VERT_SERPENT_FONCE, centre, rayon, 4)
        
        # Déterminer la direction pour orienter la tête
        if self.direction == (TAILLE_CASE, 0):  # Droite
            # Yeux
            oeil_gauche = (centre[0] + 8, centre[1] - 12)
            oeil_droit = (centre[0] + 8, centre[1] + 12)
        elif self.direction == (-TAILLE_CASE, 0):  # Gauche
            oeil_gauche = (centre[0] - 8, centre[1] - 12)
            oeil_droit = (centre[0] - 8, centre[1] + 12)
        elif self.direction == (0, -TAILLE_CASE):  # Haut
            oeil_gauche = (centre[0] - 12, centre[1] - 8)
            oeil_droit = (centre[0] + 12, centre[1] - 8)
        else:  # Bas
            oeil_gauche = (centre[0] - 12, centre[1] + 8)
            oeil_droit = (centre[0] + 12, centre[1] + 8)
        
        # Dessiner les yeux
        pygame.draw.circle(ecran, JAUNE_OEIL, oeil_gauche, 8)
        pygame.draw.circle(ecran, JAUNE_OEIL, oeil_droit, 8)
        pygame.draw.circle(ecran, NOIR_PUPILLE, oeil_gauche, 4)
        pygame.draw.circle(ecran, NOIR_PUPILLE, oeil_droit, 4)
        
        # Langue fourchue (si direction vers la droite)
        if self.direction == (TAILLE_CASE, 0):
            langue_base = (centre[0] + rayon - 6, centre[1])
            pygame.draw.line(ecran, ROUGE, langue_base, (langue_base[0] + 18, langue_base[1]), 4)
            pygame.draw.line(ecran, ROUGE, (langue_base[0] + 18, langue_base[1]), (langue_base[0] + 24, langue_base[1] - 6), 3)
            pygame.draw.line(ecran, ROUGE, (langue_base[0] + 18, langue_base[1]), (langue_base[0] + 24, langue_base[1] + 6), 3)
    
    def dessiner_corps(self, ecran, position, index):
        # Alterner les couleurs pour créer un motif d'écailles
        if index % 2 == 0:
            couleur_principale = VERT_SERPENT_CLAIR
            couleur_bordure = VERT_SERPENT_FONCE
        else:
            couleur_principale = VERT_SERPENT_FONCE
            couleur_bordure = VERT_SERPENT_CLAIR
        
        # Corps circulaire
        centre = (position[0] + TAILLE_CASE//2, position[1] + TAILLE_CASE//2)
        rayon = TAILLE_CASE//2 - 3
        pygame.draw.circle(ecran, couleur_principale, centre, rayon)
        pygame.draw.circle(ecran, couleur_bordure, centre, rayon, 3)
        
        # Ajouter des détails d'écailles
        if index % 3 == 0:
            for i in range(5):
                for j in range(5):
                    if (i + j) % 2 == 0:
                        point_x = position[0] + 10 + i * 8
                        point_y = position[1] + 10 + j * 8
                        if point_x < position[0] + TAILLE_CASE - 10 and point_y < position[1] + TAILLE_CASE - 10:
                            pygame.draw.circle(ecran, couleur_bordure, (point_x, point_y), 2)

class Nourriture:
    def __init__(self):
        self.position = self.generer_position()
    
    def generer_position(self):
        x = MARGE + random.randint(0, (LARGEUR_JEU - TAILLE_CASE) // TAILLE_CASE) * TAILLE_CASE
        y = MARGE + random.randint(0, (HAUTEUR_JEU - TAILLE_CASE) // TAILLE_CASE) * TAILLE_CASE
        return (x, y)
    
    def dessiner(self, ecran):
        self.dessiner_pomme(ecran, self.position)
    
    def dessiner_pomme(self, ecran, position):
        centre = (position[0] + TAILLE_CASE//2, position[1] + TAILLE_CASE//2)
        
        # Corps de la pomme (cercle principal)
        rayon_pomme = TAILLE_CASE//2 - 6
        pygame.draw.circle(ecran, ROUGE_POMME, centre, rayon_pomme)
        
        # Ombre/relief pour donner du volume
        pygame.draw.circle(ecran, ROUGE_POMME_FONCE, centre, rayon_pomme, 4)
        
        # Reflet sur la pomme
        reflet_pos = (centre[0] - 8, centre[1] - 8)
        pygame.draw.circle(ecran, BLANC, reflet_pos, 8)
        pygame.draw.circle(ecran, ROUGE_POMME, reflet_pos, 8, 2)
        
        # Tige de la pomme
        tige_debut = (centre[0], centre[1] - rayon_pomme)
        tige_fin = (centre[0], centre[1] - rayon_pomme - 12)
        pygame.draw.line(ecran, MARRON_TIGE, tige_debut, tige_fin, 6)
        
        # Feuille
        feuille_base = (centre[0], centre[1] - rayon_pomme - 6)
        feuille_points = [
            feuille_base,
            (feuille_base[0] + 12, feuille_base[1] - 6),
            (feuille_base[0] + 18, feuille_base[1]),
            (feuille_base[0] + 12, feuille_base[1] + 6),
            feuille_base
        ]
        pygame.draw.polygon(ecran, VERT_FEUILLE, feuille_points)
        
        # Petits détails sur la feuille
        pygame.draw.line(ecran, VERT_SERPENT_FONCE, 
                        (feuille_base[0] + 3, feuille_base[1]), 
                        (feuille_base[0] + 15, feuille_base[1] - 3), 3)

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Snake Game")
        self.horloge = pygame.time.Clock()
        self.snake = Snake()
        self.nourriture = Nourriture()
        self.score = 0
        self.police_score = pygame.font.Font(None, 48)
        self.police_instructions = pygame.font.Font(None, 32)
        self.police_titre = pygame.font.Font(None, 64)
        
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
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_F11:
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
        # Remplir l'écran avec un fond gris foncé
        self.ecran.fill(GRIS_FONCE)
        
        # Dessiner la bordure bleue
        zone_jeu = pygame.Rect(MARGE - EPAISSEUR_BORDURE, MARGE - EPAISSEUR_BORDURE, 
                              LARGEUR_JEU + 2 * EPAISSEUR_BORDURE, HAUTEUR_JEU + 2 * EPAISSEUR_BORDURE)
        pygame.draw.rect(self.ecran, BLEU, zone_jeu, EPAISSEUR_BORDURE)
        
        # Remplir la zone de jeu avec du noir
        zone_jeu_interieur = pygame.Rect(MARGE, MARGE, LARGEUR_JEU, HAUTEUR_JEU)
        pygame.draw.rect(self.ecran, NOIR, zone_jeu_interieur)
        
        # Dessiner le serpent et la nourriture
        self.snake.dessiner(self.ecran)
        self.nourriture.dessiner(self.ecran)
        
        # Afficher le score en haut à gauche
        texte_score = self.police_score.render(f"Score: {self.score}", True, BLANC)
        self.ecran.blit(texte_score, (20, 20))
        
        # Afficher le titre en haut au centre
        texte_titre = self.police_titre.render("SNAKE GAME", True, BLEU)
        rect_titre = texte_titre.get_rect(center=(LARGEUR_ECRAN//2, 40))
        self.ecran.blit(texte_titre, rect_titre)
        
        # Afficher les instructions en bas
        instructions = [
            "Utilisez les flèches pour déplacer le serpent",
            "ESC ou F11 pour quitter le jeu"
        ]
        
        for i, instruction in enumerate(instructions):
            texte_instruction = self.police_instructions.render(instruction, True, BLANC)
            rect_instruction = texte_instruction.get_rect(center=(LARGEUR_ECRAN//2, HAUTEUR_ECRAN - 60 + i * 35))
            self.ecran.blit(texte_instruction, rect_instruction)
        
        pygame.display.flip()
    
    def afficher_game_over(self):
        # Overlay semi-transparent sur toute la zone de jeu
        overlay = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU))
        overlay.set_alpha(180)
        overlay.fill(NOIR)
        self.ecran.blit(overlay, (MARGE, MARGE))
        
        # Messages de Game Over
        texte_game_over = self.police_titre.render("GAME OVER!", True, ROUGE)
        texte_score_final = self.police_score.render(f"Score final: {self.score}", True, BLANC)
        texte_rejouer = self.police_instructions.render("Appuyez sur ESPACE pour rejouer", True, BLANC)
        texte_quitter = self.police_instructions.render("ou ESC pour quitter", True, BLANC)
        
        # Centrer les textes dans la zone de jeu
        centre_x = MARGE + LARGEUR_JEU // 2
        centre_y = MARGE + HAUTEUR_JEU // 2
        
        rect_game_over = texte_game_over.get_rect(center=(centre_x, centre_y - 80))
        rect_score = texte_score_final.get_rect(center=(centre_x, centre_y - 20))
        rect_rejouer = texte_rejouer.get_rect(center=(centre_x, centre_y + 40))
        rect_quitter = texte_quitter.get_rect(center=(centre_x, centre_y + 80))
        
        self.ecran.blit(texte_game_over, rect_game_over)
        self.ecran.blit(texte_score_final, rect_score)
        self.ecran.blit(texte_rejouer, rect_rejouer)
        self.ecran.blit(texte_quitter, rect_quitter)
        
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
                        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_F11:
                            en_cours = False
            
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Lancer le jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()