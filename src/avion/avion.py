import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
ROSE = (255, 105, 180)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

class Avion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 30
        self.vitesse = 5
        self.vie = 5
        self.temps_dernier_tir = 0
        self.cadence = 200  # millisecondes
        
    def deplacer(self, touches):
        if touches[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vitesse
        if touches[pygame.K_RIGHT] and self.x < LARGEUR - self.largeur:
            self.x += self.vitesse
        if touches[pygame.K_UP] and self.y > 0:
            self.y -= self.vitesse
        if touches[pygame.K_DOWN] and self.y < HAUTEUR - self.hauteur:
            self.y += self.vitesse
    
    def tirer(self):
        maintenant = pygame.time.get_ticks()
        if maintenant - self.temps_dernier_tir > self.cadence:
            self.temps_dernier_tir = maintenant
            return Projectile(self.x + self.largeur // 2, self.y)
        return None
    
    def dessiner(self, ecran):
        # Corps de l'avion
        pygame.draw.polygon(ecran, BLEU, [
            (self.x + self.largeur // 2, self.y),
            (self.x, self.y + self.hauteur),
            (self.x + self.largeur // 4, self.y + self.hauteur - 5),
            (self.x + 3 * self.largeur // 4, self.y + self.hauteur - 5),
            (self.x + self.largeur, self.y + self.hauteur)
        ])
        
        # Ailes
        pygame.draw.polygon(ecran, BLEU, [
            (self.x + self.largeur // 4, self.y + self.hauteur // 2),
            (self.x - 5, self.y + self.hauteur // 2 + 10),
            (self.x + self.largeur // 4, self.y + self.hauteur // 2 + 15)
        ])
        
        pygame.draw.polygon(ecran, BLEU, [
            (self.x + 3 * self.largeur // 4, self.y + self.hauteur // 2),
            (self.x + self.largeur + 5, self.y + self.hauteur // 2 + 10),
            (self.x + 3 * self.largeur // 4, self.y + self.hauteur // 2 + 15)
        ])
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 3
        self.hauteur = 8
        self.vitesse = 8
        
    def deplacer(self):
        self.y -= self.vitesse
        
    def dessiner(self, ecran):
        pygame.draw.rect(ecran, JAUNE, (self.x, self.y, self.largeur, self.hauteur))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

class Fantome:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 30
        self.hauteur = 30
        self.vitesse = random.uniform(1, 3)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.couleur = random.choice([ROSE, ROUGE, ORANGE, CYAN])
        self.temps_changement = 0
        
    def deplacer(self):
        # Changement de direction aléatoire
        maintenant = pygame.time.get_ticks()
        if maintenant - self.temps_changement > 2000:  # Change de direction toutes les 2 secondes
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.temps_changement = maintenant
        
        self.x += self.direction_x * self.vitesse
        self.y += self.direction_y * self.vitesse
        
        # Rebond sur les bords
        if self.x <= 0 or self.x >= LARGEUR - self.largeur:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= HAUTEUR - self.hauteur:
            self.direction_y *= -1
            
        # Garder dans les limites
        self.x = max(0, min(LARGEUR - self.largeur, self.x))
        self.y = max(0, min(HAUTEUR - self.hauteur, self.y))
    
    def dessiner(self, ecran):
        # Corps du fantôme (demi-cercle)
        pygame.draw.circle(ecran, self.couleur, 
                         (int(self.x + self.largeur // 2), int(self.y + self.hauteur // 2)), 
                         self.largeur // 2)
        
        # Base ondulée du fantôme
        points = []
        for i in range(6):
            x = self.x + i * (self.largeur // 5)
            y = self.y + self.hauteur - 5 if i % 2 == 0 else self.y + self.hauteur
            points.append((x, y))
        points.append((self.x + self.largeur, self.y + self.hauteur // 2))
        points.append((self.x, self.y + self.hauteur // 2))
        
        pygame.draw.polygon(ecran, self.couleur, points)
        
        # Yeux
        pygame.draw.circle(ecran, BLANC, 
                         (int(self.x + self.largeur // 3), int(self.y + self.hauteur // 3)), 4)
        pygame.draw.circle(ecran, BLANC, 
                         (int(self.x + 2 * self.largeur // 3), int(self.y + self.hauteur // 3)), 4)
        
        # Pupilles
        pygame.draw.circle(ecran, NOIR, 
                         (int(self.x + self.largeur // 3), int(self.y + self.hauteur // 3)), 2)
        pygame.draw.circle(ecran, NOIR, 
                         (int(self.x + 2 * self.largeur // 3), int(self.y + self.hauteur // 3)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 35
        self.hauteur = 35
        self.vitesse = 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.couleur = JAUNE
        self.temps_changement = 0
        self.angle_bouche = 0
        self.temps_bouche = 0
        self.points = 50  # Plus de points qu'un fantôme
        
    def deplacer(self):
        # Changement de direction aléatoire
        maintenant = pygame.time.get_ticks()
        if maintenant - self.temps_changement > 2500:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.temps_changement = maintenant
        
        self.x += self.direction_x * self.vitesse
        self.y += self.direction_y * self.vitesse
        
        # Rebond sur les bords
        if self.x <= 0 or self.x >= LARGEUR - self.largeur:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= HAUTEUR - self.hauteur:
            self.direction_y *= -1
            
        # Garder dans les limites
        self.x = max(0, min(LARGEUR - self.largeur, self.x))
        self.y = max(0, min(HAUTEUR - self.hauteur, self.y))
        
        # Animation de la bouche
        if maintenant - self.temps_bouche > 200:
            self.angle_bouche = (self.angle_bouche + 30) % 90
            self.temps_bouche = maintenant
    
    def dessiner(self, ecran):
        centre_x = int(self.x + self.largeur // 2)
        centre_y = int(self.y + self.hauteur // 2)
        rayon = self.largeur // 2
        
        # Déterminer la direction de la bouche
        if self.direction_x > 0:  # Droite
            angle_start = self.angle_bouche
            angle_end = 360 - self.angle_bouche
        elif self.direction_x < 0:  # Gauche
            angle_start = 180 - self.angle_bouche
            angle_end = 180 + self.angle_bouche
        elif self.direction_y > 0:  # Bas
            angle_start = 90 - self.angle_bouche
            angle_end = 90 + self.angle_bouche
        else:  # Haut
            angle_start = 270 - self.angle_bouche
            angle_end = 270 + self.angle_bouche
        
        # Dessiner le cercle de Pac-Man avec la bouche
        if self.angle_bouche > 0:
            # Calculer les points pour le secteur (bouche ouverte)
            points = [(centre_x, centre_y)]
            for angle in range(int(angle_end), int(angle_start + 360) if angle_start > angle_end else int(angle_start), -5):
                rad = math.radians(angle)
                x = centre_x + rayon * math.cos(rad)
                y = centre_y + rayon * math.sin(rad)
                points.append((x, y))
            points.append((centre_x, centre_y))
            
            if len(points) > 2:
                pygame.draw.polygon(ecran, self.couleur, points)
        else:
            # Cercle complet (bouche fermée)
            pygame.draw.circle(ecran, self.couleur, (centre_x, centre_y), rayon)
        
        # Contour
        pygame.draw.circle(ecran, NOIR, (centre_x, centre_y), rayon, 2)
        
        # Œil
        oeil_x = centre_x - 5 if self.direction_x >= 0 else centre_x + 5
        oeil_y = centre_y - 8
        pygame.draw.circle(ecran, NOIR, (oeil_x, oeil_y), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 30
        self.hauteur = 30
        self.vitesse = random.uniform(1, 3)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.couleur = random.choice([ROSE, ROUGE, ORANGE, CYAN])
        self.temps_changement = 0
        
    def deplacer(self):
        # Changement de direction aléatoire
        maintenant = pygame.time.get_ticks()
        if maintenant - self.temps_changement > 2000:  # Change de direction toutes les 2 secondes
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.temps_changement = maintenant
        
        self.x += self.direction_x * self.vitesse
        self.y += self.direction_y * self.vitesse
        
        # Rebond sur les bords
        if self.x <= 0 or self.x >= LARGEUR - self.largeur:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= HAUTEUR - self.hauteur:
            self.direction_y *= -1
            
        # Garder dans les limites
        self.x = max(0, min(LARGEUR - self.largeur, self.x))
        self.y = max(0, min(HAUTEUR - self.hauteur, self.y))
    
    def dessiner(self, ecran):
        # Corps du fantôme (demi-cercle)
        pygame.draw.circle(ecran, self.couleur, 
                         (int(self.x + self.largeur // 2), int(self.y + self.hauteur // 2)), 
                         self.largeur // 2)
        
        # Base ondulée du fantôme
        points = []
        for i in range(6):
            x = self.x + i * (self.largeur // 5)
            y = self.y + self.hauteur - 5 if i % 2 == 0 else self.y + self.hauteur
            points.append((x, y))
        points.append((self.x + self.largeur, self.y + self.hauteur // 2))
        points.append((self.x, self.y + self.hauteur // 2))
        
        pygame.draw.polygon(ecran, self.couleur, points)
        
        # Yeux
        pygame.draw.circle(ecran, BLANC, 
                         (int(self.x + self.largeur // 3), int(self.y + self.hauteur // 3)), 4)
        pygame.draw.circle(ecran, BLANC, 
                         (int(self.x + 2 * self.largeur // 3), int(self.y + self.hauteur // 3)), 4)
        
        # Pupilles
        pygame.draw.circle(ecran, NOIR, 
                         (int(self.x + self.largeur // 3), int(self.y + self.hauteur // 3)), 2)
        pygame.draw.circle(ecran, NOIR, 
                         (int(self.x + 2 * self.largeur // 3), int(self.y + self.hauteur // 3)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Avion vs Fantômes Pac-Man")
        self.horloge = pygame.time.Clock()
        
        self.avion = Avion(LARGEUR // 2, HAUTEUR - 100)
        self.projectiles = []
        self.fantomes = []
        self.pacmans = []
        self.score = 0
        self.niveau = 1
        self.temps_dernier_spawn = 0
        self.spawn_interval = 2000  # millisecondes
        
        # Police pour le texte
        self.police = pygame.font.Font(None, 36)
        
        # Générer les premiers fantômes
        for _ in range(3):
            self.spawn_fantome()
        
        # Générer le premier Pac-Man
        self.spawn_pacman()
    
    def spawn_fantome(self):
        x = random.randint(0, LARGEUR - 30)
        y = random.randint(0, HAUTEUR // 2)
        self.fantomes.append(Fantome(x, y))
    
    def spawn_pacman(self):
        x = random.randint(0, LARGEUR - 35)
        y = random.randint(0, HAUTEUR // 2)
        self.pacmans.append(Pacman(x, y))
    
    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = self.avion.tirer()
                    if projectile:
                        self.projectiles.append(projectile)
        return True
    
    def mettre_a_jour(self):
        touches = pygame.key.get_pressed()
        self.avion.deplacer(touches)
        
        # Tir automatique avec la barre d'espace
        if touches[pygame.K_SPACE]:
            projectile = self.avion.tirer()
            if projectile:
                self.projectiles.append(projectile)
        
        # Déplacer les projectiles
        for projectile in self.projectiles[:]:
            projectile.deplacer()
            if projectile.y < 0:
                self.projectiles.remove(projectile)
        
        # Déplacer les fantômes
        for fantome in self.fantomes:
            fantome.deplacer()
        
        # Déplacer les Pac-Man
        for pacman in self.pacmans:
            pacman.deplacer()
        
        # Vérifier les collisions projectile-fantôme
        for projectile in self.projectiles[:]:
            for fantome in self.fantomes[:]:
                if projectile.get_rect().colliderect(fantome.get_rect()):
                    self.projectiles.remove(projectile)
                    self.fantomes.remove(fantome)
                    self.score += 10
                    break
        
        # Vérifier les collisions projectile-pacman
        for projectile in self.projectiles[:]:
            for pacman in self.pacmans[:]:
                if projectile.get_rect().colliderect(pacman.get_rect()):
                    self.projectiles.remove(projectile)
                    self.pacmans.remove(pacman)
                    self.score += 50  # 50 points pour un Pac-Man
                    break
        
        # Vérifier les collisions avion-fantôme
        for fantome in self.fantomes[:]:
            if self.avion.get_rect().colliderect(fantome.get_rect()):
                self.fantomes.remove(fantome)
                self.avion.vie -= 1
                if self.avion.vie <= 0:
                    return False
        
        # Vérifier les collisions avion-pacman
        for pacman in self.pacmans[:]:
            if self.avion.get_rect().colliderect(pacman.get_rect()):
                self.pacmans.remove(pacman)
                self.avion.vie -= 1
                if self.avion.vie <= 0:
                    return False
        
        # Spawn de nouveaux fantômes
        maintenant = pygame.time.get_ticks()
        if maintenant - self.temps_dernier_spawn > self.spawn_interval:
            self.spawn_fantome()
            self.temps_dernier_spawn = maintenant
            
            # Augmenter la difficulté et ajouter un Pac-Man à chaque niveau
            if self.score > 0 and self.score % 100 == 0:
                nouveau_niveau = self.score // 100 + 1
                if nouveau_niveau > self.niveau:
                    self.niveau = nouveau_niveau
                    self.spawn_pacman()  # Nouveau Pac-Man à chaque niveau
                    self.spawn_interval = max(1000, self.spawn_interval - 100)
        
        return True
    
    def dessiner(self):
        self.ecran.fill(NOIR)
        
        # Dessiner les objets
        self.avion.dessiner(self.ecran)
        
        for projectile in self.projectiles:
            projectile.dessiner(self.ecran)
        
        for fantome in self.fantomes:
            fantome.dessiner(self.ecran)
        
        for pacman in self.pacmans:
            pacman.dessiner(self.ecran)
        
        # Afficher le score et les vies
        texte_score = self.police.render(f"Score: {self.score}", True, BLANC)
        texte_vie = self.police.render(f"Vies: {self.avion.vie}", True, BLANC)
        texte_niveau = self.police.render(f"Niveau: {self.niveau}", True, BLANC)
        
        self.ecran.blit(texte_score, (10, 10))
        self.ecran.blit(texte_vie, (10, 50))
        self.ecran.blit(texte_niveau, (10, 90))
        
        # Instructions
        instructions = self.police.render("Flèches: Déplacer | Espace: Tirer", True, BLANC)
        self.ecran.blit(instructions, (LARGEUR - 350, HAUTEUR - 30))
        
        pygame.display.flip()
    
    def game_over(self):
        self.ecran.fill(NOIR)
        
        texte_game_over = pygame.font.Font(None, 72).render("GAME OVER", True, ROUGE)
        texte_score_final = self.police.render(f"Score Final: {self.score}", True, BLANC)
        texte_restart = self.police.render("Appuyez sur R pour recommencer ou Q pour quitter", True, BLANC)
        
        self.ecran.blit(texte_game_over, (LARGEUR // 2 - 150, HAUTEUR // 2 - 100))
        self.ecran.blit(texte_score_final, (LARGEUR // 2 - 80, HAUTEUR // 2 - 20))
        self.ecran.blit(texte_restart, (LARGEUR // 2 - 200, HAUTEUR // 2 + 50))
        
        pygame.display.flip()
        
        # Attendre la réponse du joueur
        en_attente = True
        while en_attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True  # Recommencer
                    elif event.key == pygame.K_q:
                        return False  # Quitter
        
        return False
    
    def executer(self):
        en_cours = True
        
        while en_cours:
            if not self.gerer_evenements():
                break
            
            if not self.mettre_a_jour():
                # Game over
                if self.game_over():
                    # Recommencer le jeu
                    self.__init__()
                    continue
                else:
                    break
            
            self.dessiner()
            self.horloge.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer( )