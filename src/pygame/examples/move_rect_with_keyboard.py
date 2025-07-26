import pygame

pygame.init()

LARGEUR=800
HAUTEUR=600

ecran=pygame.display.set_mode((LARGEUR, HAUTEUR))

carree=pygame.Rect(0,0,50,50)

running=True
clock=pygame.time.Clock()
while running:
    # nombre d'images par secondes
    clock.tick(60)

    # Lire les évenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            carree.left=LARGEUR/2-carree.width/2
            carree.top=HAUTEUR/2-carree.height/2
    
    # Autre évenements
    pressedKeys=pygame.key.get_pressed()

    # .. déplacement
    if pressedKeys[pygame.K_RIGHT]:
        carree.move_ip(2,0)
    if pressedKeys[pygame.K_LEFT]:
        carree.move_ip(-2,0)
    if pressedKeys[pygame.K_UP]:
        carree.move_ip(0,-2)
    if pressedKeys[pygame.K_DOWN]:
        carree.move_ip(0,2)

    # .. taille
    if pressedKeys[pygame.K_a]:
        carree.scale_by_ip(1.1,1.1)
    if pressedKeys[pygame.K_q]:
        carree.scale_by_ip(0.9,0.9)

    # dessine les objets
    ecran.fill(pygame.Color(20,20,20))
    pygame.draw.rect(ecran, pygame.Color(0,0,255), carree)
    pygame.display.update()


pygame.quit()