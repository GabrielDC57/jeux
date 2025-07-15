import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
TAILLE_CASE = 20
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
VERT_FONCE = (34, 139, 34)

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Pac-Man aux Courgettes")

# Labyrinthe simplifié (1 = mur, 0 = chemin, 2 = pastille)
labyrinthe = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,1,1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1,1,1,1,1,2,1,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,1,1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1,1,1,1,1,2,1,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0=droite, 1=bas, 2=gauche, 3=haut
        self.bouche_ouverte = True
        self.compteur_animation = 0
        
    def deplacer(self, dx, dy):
        nouvelle_x = self.x + dx
        nouvelle_y = self.y + dy
        
        # Vérifier les limites et les murs
        if (0 <= nouvelle_x < len(labyrinthe[0]) and 
            0 <= nouvelle_y < len(labyrinthe) and 
            labyrinthe[nouvelle_y][nouvelle_x] != 1):
            self.x = nouvelle_x
            self.y = nouvelle_y
            
            # Manger la pastille
            if labyrinthe[self.y][self.x] == 2:
                labyrinthe[self.y][self.x] = 0
                return True
        return False
    
    def dessiner(self, ecran):
        # Animation de la bouche
        self.compteur_animation += 1
        if self.compteur_animation > 10:
            self.bouche_ouverte = not self.bouche_ouverte
            self.compteur_animation = 0
        
        centre_x = self.x * TAILLE_CASE + TAILLE_CASE // 2
        centre_y = self.y * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 2 - 2
        
        if self.bouche_ouverte:
            # Dessiner Pac-Man avec la bouche ouverte
            angle_debut = self.direction * 90 + 30
            angle_fin = self.direction * 90 - 30
            
            # Dessiner un cercle avec une portion manquante pour la bouche
            pygame.draw.circle(ecran, JAUNE, (centre_x, centre_y), rayon)
            
            # Dessiner la bouche (triangle noir)
            if self.direction == 0:  # droite
                points = [(centre_x, centre_y), (centre_x + rayon, centre_y - rayon//2), (centre_x + rayon, centre_y + rayon//2)]
            elif self.direction == 1:  # bas
                points = [(centre_x, centre_y), (centre_x - rayon//2, centre_y + rayon), (centre_x + rayon//2, centre_y + rayon)]
            elif self.direction == 2:  # gauche
                points = [(centre_x, centre_y), (centre_x - rayon, centre_y - rayon//2), (centre_x - rayon, centre_y + rayon//2)]
            else:  # haut
                points = [(centre_x, centre_y), (centre_x - rayon//2, centre_y - rayon), (centre_x + rayon//2, centre_y - rayon)]
            
            pygame.draw.polygon(ecran, NOIR, points)
        else:
            # Dessiner Pac-Man avec la bouche fermée
            pygame.draw.circle(ecran, JAUNE, (centre_x, centre_y), rayon)
        
        # Dessiner l'œil
        oeil_x = centre_x + (rayon//3) * (1 if self.direction != 2 else -1)
        oeil_y = centre_y - rayon//3
        pygame.draw.circle(ecran, NOIR, (oeil_x, oeil_y), 2)

class Courgette:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.direction = random.randint(0, 3)
        self.compteur_mouvement = 0
        
    def deplacer(self):
        self.compteur_mouvement += 1
        if self.compteur_mouvement < 20:  # Bouger plus lentement que Pac-Man
            return
        
        self.compteur_mouvement = 0
        
        # Changement de direction aléatoire
        if random.randint(0, 10) == 0:
            self.direction = random.randint(0, 3)
        
        dx, dy = 0, 0
        if self.direction == 0:  # droite
            dx = 1
        elif self.direction == 1:  # bas
            dy = 1
        elif self.direction == 2:  # gauche
            dx = -1
        elif self.direction == 3:  # haut
            dy = -1
        
        nouvelle_x = self.x + dx
        nouvelle_y = self.y + dy
        
        # Vérifier les limites et les murs
        if (0 <= nouvelle_x < len(labyrinthe[0]) and 
            0 <= nouvelle_y < len(labyrinthe) and 
            labyrinthe[nouvelle_y][nouvelle_x] != 1):
            self.x = nouvelle_x
            self.y = nouvelle_y
        else:
            # Changer de direction si on touche un mur
            self.direction = random.randint(0, 3)
    
    def dessiner(self, ecran):
        centre_x = self.x * TAILLE_CASE + TAILLE_CASE // 2
        centre_y = self.y * TAILLE_CASE + TAILLE_CASE // 2
        
        # Dessiner la courgette (forme allongée)
        largeur = TAILLE_CASE - 4
        hauteur = TAILLE_CASE // 2
        
        rect = pygame.Rect(centre_x - largeur//2, centre_y - hauteur//2, largeur, hauteur)
        pygame.draw.ellipse(ecran, VERT_FONCE, rect)
        
        # Dessiner des rayures pour faire plus "courgette"
        for i in range(3):
            x_rayure = centre_x - largeur//2 + i * largeur//4
            pygame.draw.line(ecran, VERT, (x_rayure, centre_y - hauteur//2), (x_rayure, centre_y + hauteur//2), 2)
        
        # Dessiner des yeux simples
        pygame.draw.circle(ecran, BLANC, (centre_x - 4, centre_y - 2), 3)
        pygame.draw.circle(ecran, BLANC, (centre_x + 4, centre_y - 2), 3)
        pygame.draw.circle(ecran, NOIR, (centre_x - 4, centre_y - 2), 2)
        pygame.draw.circle(ecran, NOIR, (centre_x + 4, centre_y - 2), 2)

def dessiner_labyrinthe(ecran):
    for y in range(len(labyrinthe)):
        for x in range(len(labyrinthe[y])):
            rect = pygame.Rect(x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            
            if labyrinthe[y][x] == 1:  # Mur
                pygame.draw.rect(ecran, BLEU, rect)
            elif labyrinthe[y][x] == 2:  # Pastille
                centre_x = x * TAILLE_CASE + TAILLE_CASE // 2
                centre_y = y * TAILLE_CASE + TAILLE_CASE // 2
                pygame.draw.circle(ecran, BLANC, (centre_x, centre_y), 2)

def compter_pastilles():
    count = 0
    for ligne in labyrinthe:
        count += ligne.count(2)
    return count

def main():
    horloge = pygame.time.Clock()
    
    # Initialiser Pac-Man
    pacman = PacMan(1, 1)
    
    # Initialiser les courgettes
    courgettes = [
        Courgette(19, 10, VERT_FONCE),
        Courgette(20, 10, VERT_FONCE),
        Courgette(18, 12, VERT_FONCE),
        Courgette(21, 12, VERT_FONCE)
    ]
    
    score = 0
    font = pygame.font.Font(None, 36)
    
    en_cours = True
    
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.direction = 0
                    if pacman.deplacer(1, 0):
                        score += 10
                elif event.key == pygame.K_DOWN:
                    pacman.direction = 1
                    if pacman.deplacer(0, 1):
                        score += 10
                elif event.key == pygame.K_LEFT:
                    pacman.direction = 2
                    if pacman.deplacer(-1, 0):
                        score += 10
                elif event.key == pygame.K_UP:
                    pacman.direction = 3
                    if pacman.deplacer(0, -1):
                        score += 10
        
        # Déplacer les courgettes
        for courgette in courgettes:
            courgette.deplacer()
        
        # Vérifier les collisions avec les courgettes
        for courgette in courgettes:
            if pacman.x == courgette.x and pacman.y == courgette.y:
                print("Game Over! Les courgettes vous ont attrapé!")
                en_cours = False
        
        # Vérifier si toutes les pastilles sont mangées
        if compter_pastilles() == 0:
            print("Félicitations! Vous avez gagné!")
            en_cours = False
        
        # Dessiner tout
        ecran.fill(NOIR)
        dessiner_labyrinthe(ecran)
        pacman.dessiner(ecran)
        
        for courgette in courgettes:
            courgette.dessiner(ecran)
        
        # Afficher le score
        texte_score = font.render(f"Score: {score}", True, BLANC)
        ecran.blit(texte_score, (10, 10))
        
        pygame.display.flip()
        horloge.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()