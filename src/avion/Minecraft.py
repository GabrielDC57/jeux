import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
TAILLE_BLOC = 30
COLONNES = 10
LIGNES = 20
LARGEUR_GRILLE = COLONNES * TAILLE_BLOC
HAUTEUR_GRILLE = LIGNES * TAILLE_BLOC
OFFSET_X = (LARGEUR - LARGEUR_GRILLE) // 2
OFFSET_Y = 50

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
ORANGE = (255, 165, 0)
VIOLET = (128, 0, 128)
CYAN = (0, 255, 255)
GRIS = (128, 128, 128)
GRIS_FONCE = (64, 64, 64)

# Formes des pièces Tetris
PIECES = [
    # I - Ligne
    [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    # O - Carré
    [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    # T - T
    [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    # S - S
    [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.#...',
         '.##..',
         '..#..',
         '.....']
    ],
    # Z - Z
    [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '..#..',
         '.##..',
         '.#...',
         '.....']
    ],
    # J - J
    [
        ['.....',
         '.#...',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.##..',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '..#..',
         '.....']
    ],
    # L - L
    [
        ['.....',
         '..#..',
         '..#..',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '#....',
         '.....'],
        ['.....',
         '##...',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ]
]

COULEURS_PIECES = [CYAN, JAUNE, VIOLET, VERT, ROUGE, BLEU, ORANGE]

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(PIECES) - 1)
        self.rotation = 0
        self.couleur = COULEURS_PIECES[self.type]
    
    def forme(self):
        return PIECES[self.type][self.rotation]
    
    def tourner(self):
        self.rotation = (self.rotation + 1) % len(PIECES[self.type])

class Tetris:
    def __init__(self):
        self.grille = [[0 for _ in range(COLONNES)] for _ in range(LIGNES)]
        self.piece_actuelle = self.nouvelle_piece()
        self.piece_suivante = self.nouvelle_piece()
        self.score = 0
        self.niveau = 1
        self.lignes_completees = 0
        self.temps_chute = 500
        self.temps_derniere_chute = 0
        self.jeu_termine = False
        
    def nouvelle_piece(self):
        return Piece(COLONNES // 2 - 2, 0)
    
    def piece_valide(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = piece.rotation
        
        forme = PIECES[piece.type][rotation]
        for i, ligne in enumerate(forme):
            for j, cell in enumerate(ligne):
                if cell == '#':
                    nx = piece.x + j + dx
                    ny = piece.y + i + dy
                    
                    if (nx < 0 or nx >= COLONNES or 
                        ny >= LIGNES or 
                        (ny >= 0 and self.grille[ny][nx])):
                        return False
        return True
    
    def placer_piece(self, piece):
        forme = piece.forme()
        for i, ligne in enumerate(forme):
            for j, cell in enumerate(ligne):
                if cell == '#':
                    self.grille[piece.y + i][piece.x + j] = piece.couleur
        
        # Vérifier les lignes complètes
        lignes_a_supprimer = []
        for i in range(LIGNES):
            if all(self.grille[i]):
                lignes_a_supprimer.append(i)
        
        # Supprimer les lignes complètes
        for ligne in lignes_a_supprimer:
            del self.grille[ligne]
            self.grille.insert(0, [0 for _ in range(COLONNES)])
        
        # Mettre à jour le score
        if lignes_a_supprimer:
            self.lignes_completees += len(lignes_a_supprimer)
            self.score += len(lignes_a_supprimer) * 100 * self.niveau
            self.niveau = self.lignes_completees // 10 + 1
            self.temps_chute = max(50, 500 - (self.niveau - 1) * 50)
        
        # Nouvelle pièce
        self.piece_actuelle = self.piece_suivante
        self.piece_suivante = self.nouvelle_piece()
        
        # Vérifier si le jeu est terminé
        if not self.piece_valide(self.piece_actuelle):
            self.jeu_termine = True
    
    def deplacer_piece(self, dx, dy):
        if self.piece_valide(self.piece_actuelle, dx, dy):
            self.piece_actuelle.x += dx
            self.piece_actuelle.y += dy
            return True
        return False
    
    def tourner_piece(self):
        nouvelle_rotation = (self.piece_actuelle.rotation + 1) % len(PIECES[self.piece_actuelle.type])
        if self.piece_valide(self.piece_actuelle, rotation=nouvelle_rotation):
            self.piece_actuelle.rotation = nouvelle_rotation
    
    def chute_piece(self):
        if not self.deplacer_piece(0, 1):
            self.placer_piece(self.piece_actuelle)
    
    def chute_rapide(self):
        while self.deplacer_piece(0, 1):
            self.score += 1
        self.placer_piece(self.piece_actuelle)
    
    def mettre_a_jour(self, dt):
        if self.jeu_termine:
            return
        
        self.temps_derniere_chute += dt
        if self.temps_derniere_chute >= self.temps_chute:
            self.chute_piece()
            self.temps_derniere_chute = 0

def dessiner_bloc(surface, x, y, couleur):
    rect = pygame.Rect(x, y, TAILLE_BLOC, TAILLE_BLOC)
    pygame.draw.rect(surface, couleur, rect)
    pygame.draw.rect(surface, BLANC, rect, 2)

def dessiner_grille(surface, tetris):
    # Dessiner la grille de fond
    for i in range(LIGNES):
        for j in range(COLONNES):
            x = OFFSET_X + j * TAILLE_BLOC
            y = OFFSET_Y + i * TAILLE_BLOC
            
            if tetris.grille[i][j]:
                dessiner_bloc(surface, x, y, tetris.grille[i][j])
            else:
                pygame.draw.rect(surface, GRIS_FONCE, 
                               (x, y, TAILLE_BLOC, TAILLE_BLOC), 1)

def dessiner_piece(surface, piece):
    forme = piece.forme()
    for i, ligne in enumerate(forme):
        for j, cell in enumerate(ligne):
            if cell == '#':
                x = OFFSET_X + (piece.x + j) * TAILLE_BLOC
                y = OFFSET_Y + (piece.y + i) * TAILLE_BLOC
                dessiner_bloc(surface, x, y, piece.couleur)

def dessiner_piece_suivante(surface, piece):
    forme = piece.forme()
    start_x = LARGEUR - 150
    start_y = 100
    
    for i, ligne in enumerate(forme):
        for j, cell in enumerate(ligne):
            if cell == '#':
                x = start_x + j * 20
                y = start_y + i * 20
                pygame.draw.rect(surface, piece.couleur, (x, y, 20, 20))
                pygame.draw.rect(surface, BLANC, (x, y, 20, 20), 1)

def dessiner_interface(surface, tetris, font):
    # Score
    score_text = font.render(f"Score: {tetris.score}", True, BLANC)
    surface.blit(score_text, (10, 10))
    
    # Niveau
    niveau_text = font.render(f"Niveau: {tetris.niveau}", True, BLANC)
    surface.blit(niveau_text, (10, 50))
    
    # Lignes
    lignes_text = font.render(f"Lignes: {tetris.lignes_completees}", True, BLANC)
    surface.blit(lignes_text, (10, 90))
    
    # Pièce suivante
    suivante_text = font.render("Suivante:", True, BLANC)
    surface.blit(suivante_text, (LARGEUR - 150, 70))
    dessiner_piece_suivante(surface, tetris.piece_suivante)
    
    # Contrôles
    controls = [
        "Contrôles:",
        "← → : Déplacer",
        "↓ : Chute rapide",
        "↑ : Tourner",
        "Espace : Chute",
        "R : Recommencer"
    ]
    
    for i, control in enumerate(controls):
        text = font.render(control, True, BLANC)
        surface.blit(text, (LARGEUR - 150, 200 + i * 25))

def main():
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    tetris = Tetris()
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if tetris.jeu_termine:
                    if event.key == pygame.K_r:
                        tetris = Tetris()
                else:
                    if event.key == pygame.K_LEFT:
                        tetris.deplacer_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        tetris.deplacer_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        tetris.deplacer_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        tetris.tourner_piece()
                    elif event.key == pygame.K_SPACE:
                        tetris.chute_rapide()
        
        tetris.mettre_a_jour(dt)
        
        # Dessiner
        screen.fill(NOIR)
        
        if not tetris.jeu_termine:
            dessiner_grille(screen, tetris)
            dessiner_piece(screen, tetris.piece_actuelle)
        else:
            dessiner_grille(screen, tetris)
            game_over_text = font.render("GAME OVER", True, ROUGE)
            restart_text = font.render("Appuyez sur R pour recommencer", True, BLANC)
            screen.blit(game_over_text, (LARGEUR // 2 - 60, HAUTEUR // 2 - 20))
            screen.blit(restart_text, (LARGEUR // 2 - 120, HAUTEUR // 2 + 20))
        
        dessiner_interface(screen, tetris, font)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()