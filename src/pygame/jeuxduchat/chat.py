import os 
import pygame

class Chat(pygame.sprite.Sprite):
    """Cette classe détaille un chat"""

    def __init__(self, name, coordonnee):
        """cette fonction permet d'initaliser un chat"""
        pygame.sprite.Sprite.__init__(self)
        # aller chercher l'image dans le bon repertoire (pas facile,j'avoue)
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"image_chat.png"))
        # aller chercher un miaulement
        self.miaulement = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.realpath(__file__)),"chat_miaule.wav"))
        # convertir l'image
        self.image = self.image.convert()
        # recupérer son rectangle
        self.rect = self.image.get_rect()
        # le mettre à 100 pixels du haut de la fenetre
        self.rect.left,self.rect.top=coordonnee
        # Le nom du chat
        self.name = name

    def update(self):
        """Mise à jour du sprite"""
        pass

    def avancer(self):
        """Avancer le chat de 4 pixels"""
        self.rect.left += 4
        print(f"{self.name} avance vers la droite !")

    def reculer(self):
        """Reculer le chat de 4 pixels"""
        self.rect.left -= 4
        print(f"{self.name} recule vers la gauche !")

    def descendre(self):
        """Descendre le chat de 4 pixels"""
        self.rect.top += 4
        print(f"{self.name} descend !")

    def monter(self):
        """Monter le chat de 4 pixels"""
        self.rect.top -= 4
        print(f"{self.name} monte !")

    def miauler(self):
        """Faire miauler le chat"""
        self.miaulement.play()


