import pygame
import random
import time
import sys

# Initialisation de pygame
pygame.init()

# Constantes
LARGEUR = 1000
HAUTEUR = 600
FPS = 60
COULEUR_FOND = (135, 206, 235)  # Bleu ciel
COULEUR_PONT = (139, 69, 19)   # Marron
COULEUR_PLANCHE = (160, 82, 45) # Marron clair
COULEUR_EAU = (0, 100, 200)    # Bleu foncé
COULEUR_JOUEUR = (255, 255, 0)  # Jaune
COULEUR_CROCODILE = (0, 100, 0) # Vert foncé
COULEUR_TEXTE = (0, 0, 0)       # Noir
COULEUR_ROUGE = (255, 0, 0)     # Rouge

# Initialisation de l'écran
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Poursuite Mathématique sur le Pont")
horloge = pygame.time.Clock()
police = pygame.font.Font(None, 36)
grande_police = pygame.font.Font(None, 48)

class JeuPont:
    def __init__(self):
        self.position_joueur = 0
        self.position_crocodile = -5
        self.question_actuelle = 1
        self.score = 0
        self.temps_debut_question = 0
        self.question = ""
        self.reponse_correcte = 0
        self.reponse_joueur = ""
        self.message = ""
        self.jeu_termine = False
        self.victoire = False
        self.generer_nouvelle_question()
    
    def generer_nouvelle_question(self):
        """Génère une nouvelle question de multiplication"""
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        self.question = f"{a} × {b} = ?"
        self.reponse_correcte = a * b
        self.reponse_joueur = ""
        self.temps_debut_question = time.time()
        self.message = ""
    
    def verifier_reponse(self):
        """Vérifie la réponse du joueur et met à jour les positions"""
        try:
            reponse = int(self.reponse_joueur)
            temps_reponse = time.time() - self.temps_debut_question
            
            if reponse == self.reponse_correcte:
                # Bonne réponse
                self.position_joueur += 1
                self.position_crocodile += 1
                self.score += 1
                
                if temps_reponse < 3:
                    # Bonus pour rapidité
                    self.position_joueur += 1
                    self.message = f"Correct et rapide ! ({temps_reponse:.1f}s)"
                else:
                    self.message = f"Correct ! ({temps_reponse:.1f}s)"
            else:
                # Mauvaise réponse
                self.position_crocodile += 1
                self.message = f"Faux ! {self.reponse_correcte} était la bonne réponse"
            
            if temps_reponse > 8:
                # Pénalité pour lenteur
                self.position_crocodile += 1
                self.message += " - Trop lent !"
            
        except ValueError:
            # Réponse non numérique
            self.position_crocodile += 1
            self.message = "Réponse invalide !"
        
        # Vérifier les conditions de fin
        if self.position_joueur >= 25:
            self.jeu_termine = True
            self.victoire = True
        elif self.position_crocodile >= self.position_joueur:
            self.jeu_termine = True
            self.victoire = False
        elif self.question_actuelle >= 25:
            if self.position_joueur > self.position_crocodile:
                self.jeu_termine = True
                self.victoire = True
            else:
                self.jeu_termine = True
                self.victoire = False
    
    def dessiner_pont(self):
        """Dessine le pont avec les planches"""
        # Eau
        pygame.draw.rect(ecran, COULEUR_EAU, (0, 400, LARGEUR, 200))
        
        # Pont principal
        largeur_planche = (LARGEUR - 100) // 25
        y_pont = 350
        
        for i in range(25):
            x = 50 + i * largeur_planche
            # Planche
            pygame.draw.rect(ecran, COULEUR_PLANCHE, (x, y_pont, largeur_planche - 2, 50))
            # Bordure
            pygame.draw.rect(ecran, COULEUR_PONT, (x, y_pont, largeur_planche - 2, 50), 2)
            
            # Numéro de planche
            numero = police.render(str(i + 1), True, COULEUR_TEXTE)
            ecran.blit(numero, (x + largeur_planche // 2 - 10, y_pont + 55))
    
    def dessiner_personnages(self):
        """Dessine le joueur et le crocodile"""
        largeur_planche = (LARGEUR - 100) // 25
        y_personnages = 320
        
        # Position du joueur
        if self.position_joueur >= 0:
            x_joueur = 50 + self.position_joueur * largeur_planche + largeur_planche // 2
            # Bonhomme (cercle + corps)
            pygame.draw.circle(ecran, COULEUR_JOUEUR, (x_joueur, y_personnages - 10), 15)
            pygame.draw.rect(ecran, COULEUR_JOUEUR, (x_joueur - 8, y_personnages, 16, 30))
        
        # Position du crocodile
        if self.position_crocodile >= 0:
            x_crocodile = 50 + self.position_crocodile * largeur_planche + largeur_planche // 2
            # Crocodile (ellipse + yeux)
            pygame.draw.ellipse(ecran, COULEUR_CROCODILE, (x_crocodile - 20, y_personnages - 5, 40, 20))
            pygame.draw.circle(ecran, COULEUR_ROUGE, (x_crocodile - 10, y_personnages - 3), 3)
            pygame.draw.circle(ecran, COULEUR_ROUGE, (x_crocodile + 10, y_personnages - 3), 3)
    
    def dessiner_interface(self):
        """Dessine l'interface utilisateur"""
        # Fond pour l'interface
        pygame.draw.rect(ecran, (255, 255, 255), (0, 0, LARGEUR, 150))
        pygame.draw.rect(ecran, COULEUR_TEXTE, (0, 0, LARGEUR, 150), 3)
        
        # Question actuelle
        texte_question = grande_police.render(f"Question {self.question_actuelle}/25", True, COULEUR_TEXTE)
        ecran.blit(texte_question, (20, 20))
        
        # Score
        texte_score = police.render(f"Score: {self.score}/25", True, COULEUR_TEXTE)
        ecran.blit(texte_score, (LARGEUR - 150, 20))
        
        # Question mathématique
        texte_math = grande_police.render(self.question, True, COULEUR_TEXTE)
        ecran.blit(texte_math, (20, 60))
        
        # Réponse du joueur
        texte_reponse = police.render(f"Votre réponse: {self.reponse_joueur}", True, COULEUR_TEXTE)
        ecran.blit(texte_reponse, (20, 100))
        
        # Message de feedback
        if self.message:
            couleur_msg = COULEUR_ROUGE if "Faux" in self.message or "invalide" in self.message else (0, 150, 0)
            texte_msg = police.render(self.message, True, couleur_msg)
            ecran.blit(texte_msg, (300, 100))
        
        # Temps écoulé
        temps_ecoule = time.time() - self.temps_debut_question
        couleur_temps = COULEUR_ROUGE if temps_ecoule > 10 else COULEUR_TEXTE
        texte_temps = police.render(f"Temps: {temps_ecoule:.1f}s", True, couleur_temps)
        ecran.blit(texte_temps, (LARGEUR - 150, 60))
        
        # Positions
        texte_pos = police.render(f"Vous: planche {max(1, self.position_joueur + 1)}", True, COULEUR_TEXTE)
        ecran.blit(texte_pos, (400, 20))
        
        if self.position_crocodile >= 0:
            texte_croco = police.render(f"Crocodile: planche {self.position_crocodile + 1}", True, COULEUR_CROCODILE)
            ecran.blit(texte_croco, (400, 45))
        else:
            texte_croco = police.render(f"Crocodile: {abs(self.position_crocodile)} planches derrière", True, COULEUR_CROCODILE)
            ecran.blit(texte_croco, (400, 45))
    
    def dessiner_fin_jeu(self):
        """Dessine l'écran de fin de jeu"""
        # Fond semi-transparent
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        ecran.blit(overlay, (0, 0))
        
        # Message de fin
        if self.victoire:
            message = "VICTOIRE !"
            sous_message = "Vous avez échappé au crocodile !"
            couleur = (0, 255, 0)
        else:
            message = "DÉFAITE !"
            sous_message = "Le crocodile vous a attrapé !"
            couleur = COULEUR_ROUGE
        
        texte_fin = grande_police.render(message, True, couleur)
        rect_fin = texte_fin.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 50))
        ecran.blit(texte_fin, rect_fin)
        
        texte_sous = police.render(sous_message, True, (255, 255, 255))
        rect_sous = texte_sous.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        ecran.blit(texte_sous, rect_sous)
        
        texte_score_final = police.render(f"Score final: {self.score}/25", True, (255, 255, 255))
        rect_score = texte_score_final.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 30))
        ecran.blit(texte_score_final, rect_score)
        
        texte_rejouer = police.render("Appuyez sur R pour rejouer ou Q pour quitter", True, (255, 255, 255))
        rect_rejouer = texte_rejouer.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 80))
        ecran.blit(texte_rejouer, rect_rejouer)

def main():
    jeu = JeuPont()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not jeu.jeu_termine:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if jeu.reponse_joueur:
                            jeu.verifier_reponse()
                            if not jeu.jeu_termine:
                                jeu.question_actuelle += 1
                                if jeu.question_actuelle <= 25:
                                    jeu.generer_nouvelle_question()
                    elif event.key == pygame.K_BACKSPACE:
                        jeu.reponse_joueur = jeu.reponse_joueur[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == '-':
                            jeu.reponse_joueur += event.unicode
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        jeu = JeuPont()  # Nouveau jeu
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
        
        # Dessin
        ecran.fill(COULEUR_FOND)
        
        if not jeu.jeu_termine:
            jeu.dessiner_interface()
            jeu.dessiner_pont()
            jeu.dessiner_personnages()
        else:
            jeu.dessiner_pont()
            jeu.dessiner_personnages()
            jeu.dessiner_fin_jeu()
        
        pygame.display.flip()
        horloge.tick(FPS)

if __name__ == "__main__":
    main()