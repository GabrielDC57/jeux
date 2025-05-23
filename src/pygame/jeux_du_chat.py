import pygame
from chat import Chat

# La couleur gris c'est Rouge=100 Vert=100 Bleu=100
ROUGE=(100,0,0)
VERT=(0,100,0)
BLEU=(0,0,100)
GRIS=(100,100,100)

print("Debut du jeu !")
pygame.init()

# On met un écran de taille 1000 pixels x 800 pixels et on le remplit de gris
pygame.display.set_caption("Jeux avec un chat")
ecran=pygame.display.set_mode((1000,800), pygame.SCALED)
ecran.fill(GRIS)

# Créer un chat de classe Chat qu'on appelle Tao et qu'on place à 50-50 du bord haut et gauche
tao=Chat("Tao", (50,50))

# On déclare l'ensemble des sprits
allsprites = pygame.sprite.RenderPlain((tao))

# Boucle infinie (le mot clef while)
running=True
clock=pygame.time.Clock()
while running:
    clock.tick(30)

    # Gestion des évenements
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            tao.miauler()

    # Detection des appuis sur les touches
    pressed=pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        tao.avancer()
    if pressed[pygame.K_LEFT]:
        tao.reculer()
    if pressed[pygame.K_UP]:
        tao.monter()
    if pressed[pygame.K_DOWN]:
        tao.descendre()

    # mise à jour des sprites
    allsprites.update() 

    # affichage
    ecran.fill(GRIS)
    allsprites.draw(ecran)
    pygame.display.flip()

pygame.quit()