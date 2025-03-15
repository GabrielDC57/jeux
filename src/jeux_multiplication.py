import random, time

# variables génériques
temps_de_reponse = 15
longueur_du_pont = 20

# regle pour avancer
reponse_correcte = 1
pas_du_crocodile = 1

# position
position_joueur = 0
position_crocodile = -int(longueur_du_pont / 2)



def parle(texte):
    """Fonction pour faire parler le jeu"""
    print("\033[1;34m") # Colorie en bleu
    print(texte)        # Affiche la demande
    print("\033[0m")    # Recolorie en couleur normale

def demande(texte):
    """Fonction pour demander un truc au joueur"""
    return input(f"{texte}\n>") # Affiche le texte avec un saut de ligne à la fin (c'est le \n)


def donne_moi_un_calcul():
    """Fonction pour générer deux chiffres aléatoires et obtenir le résultat du X"""
    chiffre_1=random.randrange(0,10,1)
    chiffre_2=random.randrange(0,10,1)
    result=chiffre_1*chiffre_2
    return chiffre_1, chiffre_2, result

def affiche_statistiques():
    """Afficher les infos en temps réel"""
    parle(f"Pont: {longueur_du_pont} | Joueur: {position_joueur} | Crocodile: {position_crocodile}")

print(f"""
============================================================
BONJOUR AVENTURIER DES MATHEMATIQUES
      
Tu dois traverser un pont. Le pont est 
composé de 20 planches.
      
Un crocodile te poursuit à la même vitesse.
Il est en retard de {longueur_du_pont/2} planches
par rapport à toi.

A chaque étape, on te pose une question:

- Si tu réponds juste à une question, tu 
avances d'une planche,
- Si tu réponds faux, tu recules d'une planche
- Si tu réponds en dessous de ({temps_de_reponse}) secondes, 
le crocodile avance d'un pas de plus et risque de te manger

La limite de réponse à chaque question est
de {temps_de_reponse} secondes.
============================================================

""")

dernier_temps = time.time()
while True:
    affiche_statistiques()

    a, b, resultat_attendu = donne_moi_un_calcul()
    resultat_joueur=demande(f"Combien font {a} x {b} ?")
    # gestion du temps
    temps_actuel=time.time()
    temps_ecoule=temps_actuel-dernier_temps
    dernier_temps=temps_actuel
    
    # Dans tous les cas le crocodile avance
    position_crocodile=position_crocodile+pas_du_crocodile
    
    # On vérifie le résultat du joueur
    if int(resultat_joueur)==resultat_attendu:
        print(f"Bravo !!! C'était bien {resultat_attendu}")
        print(f"Tu avances de {reponse_correcte}")
        position_joueur=position_joueur+reponse_correcte
    else:
        print(f"FAUX !!!! C'était {resultat_attendu}")
        print(f"Tu recules de {reponse_correcte}")
        position_joueur=position_joueur-reponse_correcte

    # On verifie le temps de réponse pour savoir si le crocodile doit avancer
    if (temps_ecoule>temps_de_reponse):
        print(f"ATTENTION !!! Tu as répondu en {int(temps_ecoule)} secondes")
        print(f"Le crocodile se RaPPPPRROOOOOOOCHHHE !!! ")
        position_crocodile=position_crocodile+pas_du_crocodile*int(temps_ecoule/temps_de_reponse)
    
    # Fins possibles
    if position_joueur<0:
        parle("""
        ====================================
              TU ES TOMBE DU PONT !!!
                GROS NUL !!!!
        ====================================
        """)
        break

    if position_crocodile>=position_joueur:
        parle("""
        ====================================
              TU AS PERDU !!!
                LE CROCODILE T'A BOUFFE !!!
        ====================================
        """)
        break

    if position_joueur==longueur_du_pont:
        parle("""
        ====================================
            TU AS REUSSI LE PASSAGE DU PONT
                BRAVOOOOOOOO !!!
        ====================================
        """)
        break




