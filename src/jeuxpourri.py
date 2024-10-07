import os 
import pygame

print("Debut du jeu !")
pygame.init()

# Définir un chat comme un Sprite
class Chat(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "image_chat.png"))
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.top = 100
        self.name = name
        self.jumps = False

    def update(self):
        if self.jumps is True:
            if self.rect.top > 60:
                self.rect.top -= 5
            else:
                self.jumps=False
        else:
            if self.rect.top < 100:
                self.rect.top += 5

    def sauter(self):
        self.jumps = True
        print(f"{self.name} saute !")

    def avancer(self):
        self.rect.left += 4
        print(f"{self.name} avance vers la droite !")

    def reculer(self):
        self.rect.left -= 4
        print(f"{self.name} recule vers la gauche !")


# On met un écran de taille 1000 pixels x 800 pixels et on le remplit de gris
pygame.display.set_caption("Prout Game avec un chat")
ecran=pygame.display.set_mode((1000,800), pygame.SCALED)
ecran.fill((100,100,100))

# Créer un chat
tao=Chat("Tao")
miaulement = pygame.mixer.Sound(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "chat_miaule.wav"))

# On déclare l'ensemble des sprits
allsprites = pygame.sprite.RenderPlain((tao))

running=True
clock=pygame.time.Clock()
while running:
    clock.tick(30)

    # Gestion des évenements
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_UP:
            tao.sauter()
            miaulement.play()

    # Detection des appuis sur les touches
    pressed=pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        tao.avancer()
    if pressed[pygame.K_LEFT]:
        tao.reculer()

    # mise à jour des sprites
    allsprites.update() 

    # affichage
    ecran.fill((100,100,100))
    allsprites.draw(ecran)
    pygame.display.flip()

print("Fin du jeu !")
pygame.quit()