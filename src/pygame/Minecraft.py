import pygame
import sys
import math
import random
from typing import Tuple, List

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 1200
HAUTEUR = 800
FPS = 60
TAILLE_BLOC = 1.0

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (34, 139, 34)
MARRON = (139, 69, 19)
GRIS = (128, 128, 128)
BLEU = (30, 144, 255)
VERT_FONCE = (0, 100, 0)
BOIS = (101, 67, 33)
CIEL = (135, 206, 235)

# Types de blocs et objets
VIDE = 0
HERBE = 1
TERRE = 2
PIERRE = 3
BOIS_TYPE = 4
FEUILLES = 5
PLANCHES = 6
BATON = 7
PIOCHE_BOIS = 8
PIOCHE_PIERRE = 9
EPEE_BOIS = 10
ETABLI = 11

# Couleurs des blocs
COULEURS_BLOCS = {
    VIDE: None,
    HERBE: VERT,
    TERRE: MARRON,
    PIERRE: GRIS,
    BOIS_TYPE: BOIS,
    FEUILLES: VERT_FONCE,
    PLANCHES: (160, 82, 45),
    BATON: (139, 69, 19),
    PIOCHE_BOIS: (160, 82, 45),
    PIOCHE_PIERRE: GRIS,
    EPEE_BOIS: (160, 82, 45),
    ETABLI: (139, 69, 19)
}

# Recettes de craft
RECETTES = {
    PLANCHES: {
        "ingredients": {BOIS_TYPE: 1},
        "quantite": 4,
        "nom": "Planches"
    },
    BATON: {
        "ingredients": {PLANCHES: 2},
        "quantite": 4,
        "nom": "Bâtons"
    },
    ETABLI: {
        "ingredients": {PLANCHES: 4},
        "quantite": 1,
        "nom": "Établi"
    },
    PIOCHE_BOIS: {
        "ingredients": {PLANCHES: 3, BATON: 2},
        "quantite": 1,
        "nom": "Pioche en bois",
        "etabli_requis": True
    },
    PIOCHE_PIERRE: {
        "ingredients": {PIERRE: 3, BATON: 2},
        "quantite": 1,
        "nom": "Pioche en pierre",
        "etabli_requis": True
    },
    EPEE_BOIS: {
        "ingredients": {PLANCHES: 2, BATON: 1},
        "quantite": 1,
        "nom": "Épée en bois",
        "etabli_requis": True
    }
}

# Noms des objets
NOMS_OBJETS = {
    HERBE: "Herbe",
    TERRE: "Terre", 
    PIERRE: "Pierre",
    BOIS_TYPE: "Bois",
    FEUILLES: "Feuilles",
    PLANCHES: "Planches",
    BATON: "Bâton",
    PIOCHE_BOIS: "Pioche bois",
    PIOCHE_PIERRE: "Pioche pierre",
    EPEE_BOIS: "Épée bois",
    ETABLI: "Établi"
}
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def longueur(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalise(self):
        l = self.longueur()
        if l > 0:
            return Vector3(self.x/l, self.y/l, self.z/l)
        return Vector3()

class Camera:
    def __init__(self, position=None, rotation=None):
        self.position = position or Vector3(0, 5, 0)
        self.rotation = rotation or Vector3(0, 0, 0)  # pitch, yaw, roll
        self.fov = 70
        self.distance_vue = 50
        
    def projet_point(self, point):
        # Transformation par rapport à la caméra
        dx = point.x - self.position.x
        dy = point.y - self.position.y
        dz = point.z - self.position.z
        
        # Rotation autour de Y (yaw)
        cos_yaw = math.cos(math.radians(self.rotation.y))
        sin_yaw = math.sin(math.radians(self.rotation.y))
        
        x_rot = dx * cos_yaw + dz * sin_yaw
        z_rot = -dx * sin_yaw + dz * cos_yaw
        
        # Rotation autour de X (pitch)
        cos_pitch = math.cos(math.radians(self.rotation.x))
        sin_pitch = math.sin(math.radians(self.rotation.x))
        
        y_rot = dy * cos_pitch - z_rot * sin_pitch
        z_final = dy * sin_pitch + z_rot * cos_pitch
        
        # Projection perspective
        if z_final <= 0.1:
            return None
            
        facteur = (LARGEUR / 2) / math.tan(math.radians(self.fov / 2))
        
        x_ecran = LARGEUR / 2 + (x_rot * facteur) / z_final
        y_ecran = HAUTEUR / 2 - (y_rot * facteur) / z_final
        
        return (int(x_ecran), int(y_ecran), z_final)

class Joueur:
    def __init__(self, x, y, z):
        self.position = Vector3(x, y, z)
        self.vitesse = Vector3()
        self.camera = Camera(Vector3(x, y + 1.7, z))
        self.vitesse_deplacement = 0.1
        self.vitesse_saut = 0.3
        self.sur_sol = False
        self.sensibilite_souris = 0.2
        self.inventaire = {HERBE: 64, TERRE: 64, PIERRE: 64, BOIS_TYPE: 64, FEUILLES: 64, PLANCHES: 0, BATON: 0, PIOCHE_BOIS: 0, PIOCHE_PIERRE: 0, EPEE_BOIS: 0, ETABLI: 0}
        self.bloc_selectionne = HERBE
        self.outils_equipe = None
        self.etabli_proche = False
        
    def update(self, monde):
        # Appliquer la gravité
        self.vitesse.y -= 0.02
        
        # Mouvement
        nouvelle_pos = self.position + self.vitesse
        
        # Vérifier collisions Y
        if not self.collision_y(nouvelle_pos, monde):
            self.position.y = nouvelle_pos.y
            self.sur_sol = False
        else:
            if self.vitesse.y < 0:
                self.sur_sol = True
            self.vitesse.y = 0
            
        # Vérifier collisions X
        test_x = Vector3(nouvelle_pos.x, self.position.y, self.position.z)
        if not self.collision_generale(test_x, monde):
            self.position.x = nouvelle_pos.x
        else:
            self.vitesse.x = 0
            
        # Vérifier collisions Z
        test_z = Vector3(self.position.x, self.position.y, nouvelle_pos.z)
        if not self.collision_generale(test_z, monde):
            self.position.z = nouvelle_pos.z
        else:
            self.vitesse.z = 0
            
        # Mettre à jour la caméra
        self.camera.position = Vector3(self.position.x, self.position.y + 1.7, self.position.z)
        
        # Vérifier si proche d'un établi
        self.etabli_proche = self.verifier_etabli_proche(monde)
        
        # Friction
        self.vitesse.x *= 0.8
        self.vitesse.z *= 0.8
        
    def verifier_etabli_proche(self, monde):
        # Vérifier les blocs autour du joueur pour un établi
        for dx in range(-2, 3):
            for dy in range(-1, 3):
                for dz in range(-2, 3):
                    x = int(self.position.x + dx)
                    y = int(self.position.y + dy)
                    z = int(self.position.z + dz)
                    if monde.get_bloc(x, y, z) == ETABLI:
                        return True
        return False
        
    def peut_crafter(self, objet):
        if objet not in RECETTES:
            return False
            
        recette = RECETTES[objet]
        
        # Vérifier si établi requis
        if recette.get("etabli_requis", False) and not self.etabli_proche:
            return False
            
        # Vérifier les ingrédients
        for ingredient, quantite_requise in recette["ingredients"].items():
            if self.inventaire.get(ingredient, 0) < quantite_requise:
                return False
        return True
        
    def crafter(self, objet):
        if not self.peut_crafter(objet):
            return False
            
        recette = RECETTES[objet]
        
        # Retirer les ingrédients
        for ingredient, quantite_requise in recette["ingredients"].items():
            self.inventaire[ingredient] -= quantite_requise
            
        # Ajouter l'objet crafté
        if objet not in self.inventaire:
            self.inventaire[objet] = 0
        self.inventaire[objet] += recette["quantite"]
        
        return True
        
    def collision_y(self, pos, monde):
        # Vérifier collision verticale
        coins = [
            (pos.x - 0.3, pos.y, pos.z - 0.3),
            (pos.x + 0.3, pos.y, pos.z - 0.3),
            (pos.x - 0.3, pos.y, pos.z + 0.3),
            (pos.x + 0.3, pos.y, pos.z + 0.3),
            (pos.x - 0.3, pos.y + 1.8, pos.z - 0.3),
            (pos.x + 0.3, pos.y + 1.8, pos.z - 0.3),
            (pos.x - 0.3, pos.y + 1.8, pos.z + 0.3),
            (pos.x + 0.3, pos.y + 1.8, pos.z + 0.3),
        ]
        
        for x, y, z in coins:
            if monde.get_bloc(int(x), int(y), int(z)) != VIDE:
                return True
        return False
        
    def collision_generale(self, pos, monde):
        # Vérifier collision générale
        coins = [
            (pos.x - 0.3, pos.y, pos.z - 0.3),
            (pos.x + 0.3, pos.y, pos.z - 0.3),
            (pos.x - 0.3, pos.y, pos.z + 0.3),
            (pos.x + 0.3, pos.y, pos.z + 0.3),
            (pos.x - 0.3, pos.y + 1.8, pos.z - 0.3),
            (pos.x + 0.3, pos.y + 1.8, pos.z - 0.3),
            (pos.x - 0.3, pos.y + 1.8, pos.z + 0.3),
            (pos.x + 0.3, pos.y + 1.8, pos.z + 0.3),
        ]
        
        for x, y, z in coins:
            if monde.get_bloc(int(x), int(y), int(z)) != VIDE:
                return True
        return False
        
    def bouger(self, direction):
        # Calculer direction basée sur la rotation de la caméra
        yaw = math.radians(self.camera.rotation.y)
        
        if direction == "avant":
            self.vitesse.x += math.sin(yaw) * self.vitesse_deplacement
            self.vitesse.z += math.cos(yaw) * self.vitesse_deplacement
        elif direction == "arriere":
            self.vitesse.x -= math.sin(yaw) * self.vitesse_deplacement
            self.vitesse.z -= math.cos(yaw) * self.vitesse_deplacement
        elif direction == "gauche":
            self.vitesse.x += math.cos(yaw) * self.vitesse_deplacement
            self.vitesse.z -= math.sin(yaw) * self.vitesse_deplacement
        elif direction == "droite":
            self.vitesse.x -= math.cos(yaw) * self.vitesse_deplacement
            self.vitesse.z += math.sin(yaw) * self.vitesse_deplacement
            
    def sauter(self):
        if self.sur_sol:
            self.vitesse.y = self.vitesse_saut
            self.sur_sol = False
            
    def regarder(self, dx, dy):
        self.camera.rotation.y += dx * self.sensibilite_souris
        self.camera.rotation.x += dy * self.sensibilite_souris
        
        # Limiter la rotation verticale
        self.camera.rotation.x = max(-90, min(90, self.camera.rotation.x))

class Bloc:
    def __init__(self, x, y, z, type_bloc):
        self.x = x
        self.y = y
        self.z = z
        self.type = type_bloc
        
    def get_faces(self, monde):
        faces = []
        
        # Vérifier chaque face et l'ajouter si elle est visible
        directions = [
            (0, 1, 0),   # Dessus
            (0, -1, 0),  # Dessous
            (1, 0, 0),   # Droite
            (-1, 0, 0),  # Gauche
            (0, 0, 1),   # Devant
            (0, 0, -1)   # Derrière
        ]
        
        for i, (dx, dy, dz) in enumerate(directions):
            voisin_x = self.x + dx
            voisin_y = self.y + dy
            voisin_z = self.z + dz
            
            if monde.get_bloc(voisin_x, voisin_y, voisin_z) == VIDE:
                faces.append(self.get_face(i))
                
        return faces
        
    def get_face(self, direction):
        x, y, z = self.x, self.y, self.z
        
        if direction == 0:  # Dessus
            return [
                Vector3(x, y+1, z), Vector3(x+1, y+1, z),
                Vector3(x+1, y+1, z+1), Vector3(x, y+1, z+1)
            ]
        elif direction == 1:  # Dessous
            return [
                Vector3(x, y, z+1), Vector3(x+1, y, z+1),
                Vector3(x+1, y, z), Vector3(x, y, z)
            ]
        elif direction == 2:  # Droite
            return [
                Vector3(x+1, y, z), Vector3(x+1, y, z+1),
                Vector3(x+1, y+1, z+1), Vector3(x+1, y+1, z)
            ]
        elif direction == 3:  # Gauche
            return [
                Vector3(x, y, z+1), Vector3(x, y, z),
                Vector3(x, y+1, z), Vector3(x, y+1, z+1)
            ]
        elif direction == 4:  # Devant
            return [
                Vector3(x, y, z+1), Vector3(x+1, y, z+1),
                Vector3(x+1, y+1, z+1), Vector3(x, y+1, z+1)
            ]
        else:  # Derrière
            return [
                Vector3(x+1, y, z), Vector3(x, y, z),
                Vector3(x, y+1, z), Vector3(x+1, y+1, z)
            ]

class Monde:
    def __init__(self, largeur, hauteur, profondeur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.profondeur = profondeur
        self.grille = [[[VIDE for _ in range(profondeur)] for _ in range(hauteur)] for _ in range(largeur)]
        self.generer_monde()
        
    def generer_monde(self):
        # Générer un terrain 3D
        for x in range(self.largeur):
            for z in range(self.profondeur):
                # Hauteur du sol avec du bruit
                hauteur_sol = 5 + int(3 * math.sin(x * 0.1) * math.cos(z * 0.1))
                hauteur_sol = max(1, min(self.hauteur - 1, hauteur_sol))
                
                # Placer les blocs
                for y in range(hauteur_sol + 1):
                    if y == hauteur_sol:
                        self.grille[x][y][z] = HERBE
                    elif y >= hauteur_sol - 2:
                        self.grille[x][y][z] = TERRE
                    else:
                        self.grille[x][y][z] = PIERRE
                        
                # Ajouter des arbres
                if random.randint(1, 20) == 1 and hauteur_sol < self.hauteur - 5:
                    self.creer_arbre(x, hauteur_sol + 1, z)
                    
    def creer_arbre(self, x, y, z):
        # Tronc
        for i in range(4):
            if y + i < self.hauteur:
                self.grille[x][y + i][z] = BOIS_TYPE
                
        # Feuilles
        for dx in range(-2, 3):
            for dy in range(2, 5):
                for dz in range(-2, 3):
                    if (0 <= x + dx < self.largeur and 
                        0 <= y + dy < self.hauteur and 
                        0 <= z + dz < self.profondeur):
                        if abs(dx) + abs(dz) <= 2 and self.grille[x + dx][y + dy][z + dz] == VIDE:
                            self.grille[x + dx][y + dy][z + dz] = FEUILLES
                            
    def get_bloc(self, x, y, z):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur and 0 <= z < self.profondeur:
            return self.grille[x][y][z]
        return VIDE
        
    def set_bloc(self, x, y, z, type_bloc):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur and 0 <= z < self.profondeur:
            self.grille[x][y][z] = type_bloc
            
    def get_blocs_visibles(self, camera):
        blocs = []
        # Optimisation: ne rendre que les blocs proches de la caméra
        rayon = 15
        cx, cy, cz = int(camera.position.x), int(camera.position.y), int(camera.position.z)
        
        for x in range(max(0, cx - rayon), min(self.largeur, cx + rayon)):
            for y in range(max(0, cy - rayon), min(self.hauteur, cy + rayon)):
                for z in range(max(0, cz - rayon), min(self.profondeur, cz + rayon)):
                    if self.grille[x][y][z] != VIDE:
                        blocs.append(Bloc(x, y, z, self.grille[x][y][z]))
        return blocs

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Minecraft 3D - Steve")
        self.horloge = pygame.time.Clock()
        
        # Capturer la souris
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        # Créer le monde et le joueur
        self.monde = Monde(50, 20, 50)
        self.joueur = Joueur(25, 10, 25)
        
        # Interface
        self.police = pygame.font.Font(None, 24)
        self.police_petite = pygame.font.Font(None, 18)
        self.afficher_debug = True
        self.interface_craft = False
        self.scroll_craft = 0
        
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
                
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return False
                elif evenement.key == pygame.K_SPACE:
                    self.joueur.sauter()
                elif evenement.key >= pygame.K_1 and evenement.key <= pygame.K_9:
                    # Sélectionner dans l'inventaire
                    objets_avec_quantite = [(obj, qte) for obj, qte in self.joueur.inventaire.items() if qte > 0]
                    index = evenement.key - pygame.K_1
                    if index < len(objets_avec_quantite):
                        self.joueur.bloc_selectionne = objets_avec_quantite[index][0]
                elif evenement.key == pygame.K_F3:
                    self.afficher_debug = not self.afficher_debug
                elif evenement.key == pygame.K_c:
                    self.interface_craft = not self.interface_craft
                elif evenement.key == pygame.K_e:
                    # Équiper/déséquiper un outil
                    if self.joueur.bloc_selectionne in [PIOCHE_BOIS, PIOCHE_PIERRE, EPEE_BOIS]:
                        if self.joueur.outils_equipe == self.joueur.bloc_selectionne:
                            self.joueur.outils_equipe = None
                        else:
                            self.joueur.outils_equipe = self.joueur.bloc_selectionne
                    
            if evenement.type == pygame.MOUSEMOTION:
                dx, dy = evenement.rel
                self.joueur.regarder(dx, dy)
                
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if self.interface_craft:
                    self.gerer_clic_craft(evenement.pos, evenement.button)
                else:
                    self.gerer_clic_souris(evenement.button)
                    
            if evenement.type == pygame.MOUSEWHEEL:
                if self.interface_craft:
                    self.scroll_craft = max(0, self.scroll_craft - evenement.y * 2)
                
        return True
        
    def gerer_clic_souris(self, bouton):
        # Raycast pour trouver le bloc visé
        bloc_vise = self.raycast()
        if bloc_vise:
            x, y, z = bloc_vise
            if bouton == 1:  # Clic gauche - détruire
                type_bloc = self.monde.get_bloc(x, y, z)
                if type_bloc != VIDE:
                    self.monde.set_bloc(x, y, z, VIDE)
                    if type_bloc in self.joueur.inventaire:
                        self.joueur.inventaire[type_bloc] += 1
            elif bouton == 3:  # Clic droit - placer
                # Trouver une position adjacente libre
                directions = [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)]
                for dx, dy, dz in directions:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if (self.monde.get_bloc(nx, ny, nz) == VIDE and 
                        self.joueur.inventaire.get(self.joueur.bloc_selectionne, 0) > 0):
                        self.monde.set_bloc(nx, ny, nz, self.joueur.bloc_selectionne)
                        self.joueur.inventaire[self.joueur.bloc_selectionne] -= 1
                        break
                        
    def gerer_clic_craft(self, pos_souris, bouton):
        if bouton != 1:  # Seulement clic gauche
            return
            
        x_souris, y_souris = pos_souris
        
        # Zone de craft
        craft_x = LARGEUR - 300
        craft_y = 100
        
        # Vérifier clic sur les recettes
        y_offset = craft_y - self.scroll_craft
        
        for objet, recette in RECETTES.items():
            rect_recette = pygame.Rect(craft_x, y_offset, 280, 60)
            
            if rect_recette.collidepoint(x_souris, y_souris):
                if self.joueur.peut_crafter(objet):
                    self.joueur.crafter(objet)
                break
                
            y_offset += 70
                        
    def raycast(self):
        # Raycast simple pour trouver le bloc visé
        pos = Vector3(self.joueur.camera.position.x, self.joueur.camera.position.y, self.joueur.camera.position.z)
        
        # Direction du regard
        yaw = math.radians(self.joueur.camera.rotation.y)
        pitch = math.radians(self.joueur.camera.rotation.x)
        
        dx = math.sin(yaw) * math.cos(pitch)
        dy = -math.sin(pitch)
        dz = math.cos(yaw) * math.cos(pitch)
        
        direction = Vector3(dx, dy, dz)
        
        # Marcher le long du rayon
        for i in range(int(5 / 0.1)):  # 5 blocs de portée
            test_pos = pos + direction * (i * 0.1)
            x, y, z = int(test_pos.x), int(test_pos.y), int(test_pos.z)
            if self.monde.get_bloc(x, y, z) != VIDE:
                return (x, y, z)
        return None
        
    def update(self):
        # Gestion des touches
        touches = pygame.key.get_pressed()
        if touches[pygame.K_w]:
            self.joueur.bouger("avant")
        if touches[pygame.K_s]:
            self.joueur.bouger("arriere")
        if touches[pygame.K_a]:
            self.joueur.bouger("gauche")
        if touches[pygame.K_d]:
            self.joueur.bouger("droite")
            
        # Mettre à jour le joueur
        self.joueur.update(self.monde)
        
    def dessiner_face(self, points, couleur, camera):
        # Projeter tous les points
        points_projetes = []
        for point in points:
            proj = camera.projet_point(point)
            if proj is None:
                return
            points_projetes.append(proj)
            
        # Vérifier si tous les points sont dans l'écran
        if all(0 <= p[0] <= LARGEUR and 0 <= p[1] <= HAUTEUR for p in points_projetes):
            # Calculer la distance moyenne pour le tri Z
            distance_moy = sum(p[2] for p in points_projetes) / len(points_projetes)
            
            # Convertir en points 2D
            points_2d = [(p[0], p[1]) for p in points_projetes]
            
            return (points_2d, couleur, distance_moy)
        return None
        
    def dessiner(self):
        self.ecran.fill(CIEL)
        
        # Obtenir tous les blocs visibles
        blocs_visibles = self.monde.get_blocs_visibles(self.joueur.camera)
        
        # Collecter toutes les faces à dessiner
        faces_a_dessiner = []
        
        for bloc in blocs_visibles:
            couleur = COULEURS_BLOCS[bloc.type]
            faces = bloc.get_faces(self.monde)
            
            for face in faces:
                resultat = self.dessiner_face(face, couleur, self.joueur.camera)
                if resultat:
                    faces_a_dessiner.append(resultat)
                    
        # Trier par distance (plus loin en premier)
        faces_a_dessiner.sort(key=lambda x: x[2], reverse=True)
        
        # Dessiner les faces
        for points_2d, couleur, _ in faces_a_dessiner:
            try:
                pygame.draw.polygon(self.ecran, couleur, points_2d)
                pygame.draw.polygon(self.ecran, NOIR, points_2d, 1)
            except:
                pass  # Ignorer les erreurs de dessin
                
        # Crosshair
        centre_x, centre_y = LARGEUR // 2, HAUTEUR // 2
        pygame.draw.line(self.ecran, BLANC, (centre_x - 10, centre_y), (centre_x + 10, centre_y), 2)
        pygame.draw.line(self.ecran, BLANC, (centre_x, centre_y - 10), (centre_x, centre_y + 10), 2)
        
        # Interface
        self.dessiner_interface()
        
        # Interface de craft
        if self.interface_craft:
            self.dessiner_interface_craft()
        
        pygame.display.flip()
        
    def dessiner_interface(self):
        # Inventaire (objets avec quantité > 0)
        objets_avec_quantite = [(obj, qte) for obj, qte in self.joueur.inventaire.items() if qte > 0]
        
        for i, (type_obj, quantite) in enumerate(objets_avec_quantite[:9]):  # Max 9 slots
            couleur = COULEURS_BLOCS[type_obj]
            rect = pygame.Rect(10 + i * 60, 10, 50, 50)
            pygame.draw.rect(self.ecran, couleur, rect)
            pygame.draw.rect(self.ecran, NOIR, rect, 2)
            
            if type_obj == self.joueur.bloc_selectionne:
                pygame.draw.rect(self.ecran, BLANC, rect, 4)
                
            # Afficher si c'est un outil équipé
            if type_obj == self.joueur.outils_equipe:
                pygame.draw.rect(self.ecran, (255, 255, 0), rect, 3)
            
            # Quantité
            texte = self.police_petite.render(str(quantite), True, BLANC)
            self.ecran.blit(texte, (rect.x + 35, rect.y + 35))
            
            # Nom de l'objet si sélectionné
            if type_obj == self.joueur.bloc_selectionne:
                nom = NOMS_OBJETS.get(type_obj, f"Objet {type_obj}")
                texte_nom = self.police.render(nom, True, BLANC)
                self.ecran.blit(texte_nom, (rect.x, rect.y - 25))
                
        # Indicateur d'établi proche
        if self.joueur.etabli_proche:
            texte_etabli = self.police.render("Établi à proximité - Appuyez sur C pour crafter", True, (0, 255, 0))
            self.ecran.blit(texte_etabli, (10, 80))
        else:
            texte_craft = self.police.render("Appuyez sur C pour crafter (sans établi)", True, BLANC)
            self.ecran.blit(texte_craft, (10, 80))
                
        # Debug info
        if self.afficher_debug:
            pos = self.joueur.position
            rot = self.joueur.camera.rotation
            debug_texts = [
                f"Position: {pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f}",
                f"Rotation: {rot.x:.1f}, {rot.y:.1f}",
                f"Sur sol: {self.joueur.sur_sol}",
                "",
                "Contrôles:",
                "WASD: Bouger",
                "Souris: Regarder",
                "Espace: Sauter",
                "Clic G: Détruire",
                "Clic D: Placer",
                "1-9: Sélectionner",
                "E: Équiper outil",
                "C: Interface craft",
                "F3: Debug",
                "ESC: Quitter"
            ]
            
            for i, text in enumerate(debug_texts):
                if text:
                    surface = self.police.render(text, True, BLANC)
                    self.ecran.blit(surface, (LARGEUR - 250, 10 + i * 20))
                    
    def dessiner_interface_craft(self):
        # Fond semi-transparent
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(128)
        overlay.fill(NOIR)
        self.ecran.blit(overlay, (0, 0))
        
        # Panneau de craft
        craft_rect = pygame.Rect(LARGEUR - 350, 50, 340, HAUTEUR - 100)
        pygame.draw.rect(self.ecran, (50, 50, 50), craft_rect)
        pygame.draw.rect(self.ecran, BLANC, craft_rect, 2)
        
        # Titre
        titre = self.police.render("Interface de Craft", True, BLANC)
        self.ecran.blit(titre, (craft_rect.x + 10, craft_rect.y + 10))
        
        # Instructions
        instructions = [
            "Clic gauche: Crafter",
            "Molette: Défiler",
            "C: Fermer"
        ]
        
        for i, instruction in enumerate(instructions):
            texte = self.police_petite.render(instruction, True, BLANC)
            self.ecran.blit(texte, (craft_rect.x + 10, craft_rect.y + 40 + i * 15))
            
        # Liste des recettes
        y_offset = craft_rect.y + 100 - self.scroll_craft
        
        for objet, recette in RECETTES.items():
            if y_offset > craft_rect.y + craft_rect.height:
                break
            if y_offset + 60 < craft_rect.y + 100:
                y_offset += 70
                continue
                
            # Rectangle de la recette
            rect_recette = pygame.Rect(craft_rect.x + 10, y_offset, 320, 60)
            
            # Couleur selon disponibilité
            peut_crafter = self.joueur.peut_crafter(objet)
            couleur_fond = (0, 100, 0) if peut_crafter else (100, 0, 0)
            
            pygame.draw.rect(self.ecran, couleur_fond, rect_recette)
            pygame.draw.rect(self.ecran, BLANC, rect_recette, 1)
            
            # Icône de l'objet
            couleur_objet = COULEURS_BLOCS[objet]
            icone_rect = pygame.Rect(rect_recette.x + 5, rect_recette.y + 5, 30, 30)
            pygame.draw.rect(self.ecran, couleur_objet, icone_rect)
            pygame.draw.rect(self.ecran, NOIR, icone_rect, 1)
            
            # Nom et quantité
            nom = recette["nom"]
            quantite = recette["quantite"]
            texte_nom = self.police.render(f"{nom} x{quantite}", True, BLANC)
            self.ecran.blit(texte_nom, (rect_recette.x + 45, rect_recette.y + 5))
            
            # Ingrédients requis
            ingredients_text = []
            for ingredient, qte_requise in recette["ingredients"].items():
                nom_ingredient = NOMS_OBJETS.get(ingredient, f"Objet {ingredient}")
                qte_disponible = self.joueur.inventaire.get(ingredient, 0)
                couleur_ingredient = BLANC if qte_disponible >= qte_requise else (255, 100, 100)
                ingredients_text.append((f"{nom_ingredient}: {qte_disponible}/{qte_requise}", couleur_ingredient))
                
            for i, (texte, couleur) in enumerate(ingredients_text):
                surface_ingredient = self.police_petite.render(texte, True, couleur)
                self.ecran.blit(surface_ingredient, (rect_recette.x + 45, rect_recette.y + 25 + i * 12))
                
            # Indicateur établi requis
            if recette.get("etabli_requis", False):
                etabli_text = "Établi requis"
                couleur_etabli = BLANC if self.joueur.etabli_proche else (255, 100, 100)
                surface_etabli = self.police_petite.render(etabli_text, True, couleur_etabli)
                self.ecran.blit(surface_etabli, (rect_recette.x + 200, rect_recette.y + 5))
                
            y_offset += 70
        
    def executer(self):
        en_cours = True
        while en_cours:
            en_cours = self.gerer_evenements()
            self.update()
            self.dessiner()
            self.horloge.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()