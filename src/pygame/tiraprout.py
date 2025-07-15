import pygame
import math
import random
import time

# Initialisation de pygame
pygame.init()
try:
    pygame.mixer.init()
except:
    print("Attention: Audio non disponible")

# Constantes
LARGEUR = 1000
HAUTEUR = 700
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)
MARRON = (139, 69, 19)
GRIS = (128, 128, 128)

class Fleche:
    def __init__(self, x, y, angle, vitesse):
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = vitesse
        self.vx = math.cos(angle) * vitesse
        self.vy = math.sin(angle) * vitesse
        self.active = True
        self.gravity = 0.3
        
    def update(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity
            
            # Vérifier si la flèche sort de l'écran
            if self.x < 0 or self.x > LARGEUR or self.y > HAUTEUR:
                self.active = False
    
    def draw(self, screen):
        if self.active:
            # Dessiner la flèche
            angle = math.atan2(self.vy, self.vx)
            longueur = 30
            fin_x = self.x + math.cos(angle) * longueur
            fin_y = self.y + math.sin(angle) * longueur
            pygame.draw.line(screen, MARRON, (self.x, self.y), (fin_x, fin_y), 3)
            
            # Pointe de la flèche
            pygame.draw.circle(screen, ROUGE, (int(self.x), int(self.y)), 5)

class Cible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rayon = 80
        self.nombres = [random.randint(1, 9) for _ in range(6)]
        self.fleches_touchees = []
        
    def draw(self, screen):
        # Dessiner les cercles de la cible
        pygame.draw.circle(screen, BLANC, (self.x, self.y), self.rayon, 5)
        pygame.draw.circle(screen, ROUGE, (self.x, self.y), self.rayon * 0.8, 3)
        pygame.draw.circle(screen, BLANC, (self.x, self.y), self.rayon * 0.6, 3)
        pygame.draw.circle(screen, ROUGE, (self.x, self.y), self.rayon * 0.4, 3)
        pygame.draw.circle(screen, BLANC, (self.x, self.y), self.rayon * 0.2, 3)
        
        # Dessiner les nombres dans les sections
        font = pygame.font.Font(None, 36)
        for i, nombre in enumerate(self.nombres):
            angle = i * math.pi / 3
            text_x = self.x + math.cos(angle) * (self.rayon * 0.7)
            text_y = self.y + math.sin(angle) * (self.rayon * 0.7)
            text = font.render(str(nombre), True, NOIR)
            text_rect = text.get_rect(center=(text_x, text_y))
            screen.blit(text, text_rect)
        
        # Dessiner les flèches qui ont touché
        for fleche_pos in self.fleches_touchees:
            pygame.draw.circle(screen, BLEU, fleche_pos, 8)
    
    def check_collision(self, fleche):
        distance = math.sqrt((fleche.x - self.x)**2 + (fleche.y - self.y)**2)
        if distance <= self.rayon:
            # Déterminer quel nombre a été touché
            angle = math.atan2(fleche.y - self.y, fleche.x - self.x)
            if angle < 0:
                angle += 2 * math.pi
            section = int(angle / (math.pi / 3)) % 6
            self.fleches_touchees.append((int(fleche.x), int(fleche.y)))
            return self.nombres[section]
        return None

class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-10, -5)
        self.couleur = random.choice([ROUGE, BLEU, VERT, JAUNE])
        self.taille = random.randint(3, 8)
        self.vie = 60
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.vie -= 1
        
    def draw(self, screen):
        if self.vie > 0:
            pygame.draw.circle(screen, self.couleur, (int(self.x), int(self.y)), self.taille)

class JeuArcherieMath:
    def __init__(self):
        try:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
            pygame.display.set_caption("Jeu d'Archerie Mathématique")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 48)
            self.petit_font = pygame.font.Font(None, 36)
            
            self.reset_game()
            print("Jeu initialisé avec succès!")
        except Exception as e:
            print(f"Erreur lors de l'initialisation: {e}")
            raise
        
    def reset_game(self):
        try:
            self.fleches = []
            self.cible = Cible(LARGEUR - 150, HAUTEUR // 2)
            self.nombres_touches = []
            self.phase = "tir"  # "tir", "question", "resultat"
            self.question = ""
            self.reponse_correcte = 0
            self.reponse_joueur = ""
            self.temps_question = 0
            self.confettis = []
            self.message = ""
            self.temps_message = 0
            self.arc_x = 100
            self.arc_y = HAUTEUR // 2
            self.angle_arc = 0
            self.puissance = 0
            self.charger_puissance = False
            print("Jeu réinitialisé")
        except Exception as e:
            print(f"Erreur lors de la réinitialisation: {e}")
            raise
        
    def jouer_son_prout(self):
        # Simulation du son de prout - version simplifiée
        print("PROUT! 💨")
    
    def generer_question(self):
        if len(self.nombres_touches) >= 2:
            operation = random.choice(["+", "*"])
            num1, num2 = self.nombres_touches[:2]
            
            if operation == "+":
                self.question = f"{num1} + {num2} = ?"
                self.reponse_correcte = num1 + num2
            else:
                self.question = f"{num1} × {num2} = ?"
                self.reponse_correcte = num1 * num2
                
            self.phase = "question"
            self.temps_question = time.time()
            self.reponse_joueur = ""
    
    def creer_confettis(self):
        for _ in range(30):
            self.confettis.append(Confetti(LARGEUR//2, HAUTEUR//2))
    
    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.phase == "question":
                    if event.key == pygame.K_BACKSPACE:
                        self.reponse_joueur = self.reponse_joueur[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.verifier_reponse()
                    elif event.unicode.isdigit() or event.unicode == '-':
                        self.reponse_joueur += event.unicode
                elif self.phase == "resultat":
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        
            if event.type == pygame.MOUSEBUTTONDOWN and self.phase == "tir":
                if event.button == 1:  # Clic gauche
                    self.charger_puissance = True
                    
            if event.type == pygame.MOUSEBUTTONUP and self.phase == "tir":
                if event.button == 1 and self.charger_puissance:
                    self.tirer_fleche()
                    self.charger_puissance = False
                    self.puissance = 0
        
        return True  # Continue le jeu si pas de QUIT
    
    def tirer_fleche(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle_arc = math.atan2(mouse_y - self.arc_y, mouse_x - self.arc_x)
        vitesse = min(self.puissance * 0.3, 15)
        fleche = Fleche(self.arc_x, self.arc_y, self.angle_arc, vitesse)
        self.fleches.append(fleche)
    
    def verifier_reponse(self):
        try:
            reponse = int(self.reponse_joueur)
            if reponse == self.reponse_correcte:
                self.message = "Bravo ! Bonne réponse !"
                self.creer_confettis()
            else:
                self.message = "Mauvaise réponse ! PROUT !"
                self.jouer_son_prout()
        except ValueError:
            self.message = "Réponse invalide ! PROUT !"
            self.jouer_son_prout()
            
        self.phase = "resultat"
        self.temps_message = time.time()
    
    def update(self):
        # Mettre à jour les flèches
        for fleche in self.fleches[:]:
            fleche.update()
            if not fleche.active:
                self.fleches.remove(fleche)
                continue
                
            # Vérifier collision avec la cible
            nombre_touche = self.cible.check_collision(fleche)
            if nombre_touche is not None:
                self.nombres_touches.append(nombre_touche)
                fleche.active = False
                
                # Générer question si on a au moins 2 nombres
                if len(self.nombres_touches) >= 2:
                    self.generer_question()
        
        # Gérer la puissance de l'arc
        if self.charger_puissance and self.phase == "tir":
            self.puissance = min(self.puissance + 2, 100)
        
        # Vérifier le temps limite pour les questions
        if self.phase == "question":
            temps_ecoule = time.time() - self.temps_question
            if temps_ecoule > 30:  # 30 secondes
                self.message = "Temps écoulé ! PROUT !"
                self.jouer_son_prout()
                self.phase = "resultat"
                self.temps_message = time.time()
        
        # Mettre à jour les confettis
        for confetti in self.confettis[:]:
            confetti.update()
            if confetti.vie <= 0:
                self.confettis.remove(confetti)
    
    def draw(self):
        self.screen.fill((135, 206, 235))  # Bleu ciel
        
        # Dessiner l'arc
        pygame.draw.circle(self.screen, MARRON, (self.arc_x, self.arc_y), 15)
        
        # Dessiner la ligne de visée
        if self.phase == "tir":
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, GRIS, (self.arc_x, self.arc_y), (mouse_x, mouse_y), 2)
            
            # Barre de puissance
            if self.charger_puissance:
                barre_width = 200
                barre_height = 20
                barre_x = self.arc_x - barre_width // 2
                barre_y = self.arc_y - 50
                
                pygame.draw.rect(self.screen, BLANC, (barre_x, barre_y, barre_width, barre_height))
                pygame.draw.rect(self.screen, ROUGE, (barre_x, barre_y, (self.puissance / 100) * barre_width, barre_height))
                pygame.draw.rect(self.screen, NOIR, (barre_x, barre_y, barre_width, barre_height), 2)
        
        # Dessiner la cible
        self.cible.draw(self.screen)
        
        # Dessiner les flèches
        for fleche in self.fleches:
            fleche.draw(self.screen)
        
        # Dessiner les confettis
        for confetti in self.confettis:
            confetti.draw(self.screen)
        
        # Interface utilisateur
        if self.phase == "tir":
            text = self.font.render("Cliquez et maintenez pour viser et tirer!", True, NOIR)
            self.screen.blit(text, (20, 20))
            
            if self.nombres_touches:
                nombres_text = f"Nombres touchés: {', '.join(map(str, self.nombres_touches))}"
                text = self.petit_font.render(nombres_text, True, NOIR)
                self.screen.blit(text, (20, 60))
                
        elif self.phase == "question":
            # Dessiner la question
            question_text = self.font.render(self.question, True, NOIR)
            question_rect = question_text.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50))
            self.screen.blit(question_text, question_rect)
            
            # Dessiner la réponse en cours
            reponse_text = self.font.render(f"Réponse: {self.reponse_joueur}", True, BLEU)
            reponse_rect = reponse_text.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            self.screen.blit(reponse_text, reponse_rect)
            
            # Temps restant
            temps_restant = max(0, 30 - int(time.time() - self.temps_question))
            temps_text = self.font.render(f"Temps: {temps_restant}s", True, ROUGE)
            temps_rect = temps_text.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))
            self.screen.blit(temps_text, temps_rect)
            
        elif self.phase == "resultat":
            # Dessiner le message de résultat
            message_text = self.font.render(self.message, True, NOIR)
            message_rect = message_text.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            self.screen.blit(message_text, message_rect)
            
            # Instructions pour continuer
            continue_text = self.petit_font.render("Appuyez sur ESPACE pour rejouer", True, NOIR)
            continue_rect = continue_text.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))
            self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
    
    def run(self):
        print("Démarrage du jeu...")
        running = True
        try:
            while running:
                running = self.gerer_evenements()
                if running:
                    self.update()
                    self.draw()
                    self.clock.tick(FPS)
        except Exception as e:
            print(f"Erreur pendant le jeu: {e}")
            raise
        finally:
            pygame.quit()
            print("Jeu fermé")

if __name__ == "__main__":
    try:
        jeu = JeuArcherieMath()
        jeu.run()
    except Exception as e:
        print(f"Erreur: {e}")
        input("Appuyez sur Entrée pour fermer...")