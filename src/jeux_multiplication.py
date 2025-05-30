import random, time

# variables génériques
temps_de_reponse=10
temps_de_reponse_rapide=5
longueur_du_pont=23

# regle pour avancer
reponse_correcte=1
pas_du_crocodile=1

# position
position_joueur=0
position_crocodile=-int(longueur_du_pont/2)

# statistiques
nb_de_question=0
nb_de_question_juste=0
nb_de_question_rapide=0
nb_de_question_lente=0
nb_de_question_fausse=0
temps_mini=60
temps_mini_question=""
temps_maxi=0
temps_maxi_question=""

# Fonctions
def parle(texte):
    """Fonction pour faire parler le jeu"""
    print("\033[1;34m") # Colorie en bleu
    print(texte)        # Affiche la demande
    print("\033[0m")    # Recolorie en couleur normale

def parle_vert(texte):
    """Fonction pour faire parler le jeu"""
    print(f"\033[1;32m{texte}\033[0m")

def parle_rouge(texte):
    """Fonction pour faire parler le jeu"""
    print(f"\033[1;31m{texte}\033[0m")

def demande(texte):
    """Fonction pour demander un truc au joueur"""
    return input(f"{texte}\n>") # Affiche le texte avec un saut de ligne à la fin (c'est le \n)

def donne_moi_un_calcul():
    """Fonction pour générer deux chiffres aléatoires et obtenir le résultat du X"""
    #chiffre_1=random.randrange(0,10,1)
    chiffre_1=random.choice([3,4,7,8,9])
    #chiffre_1=12
    chiffre_2=random.randrange(0,11,1)
    result=chiffre_1*chiffre_2
    return chiffre_1, chiffre_2, result

def affiche_statistiques():
    """Afficher les infos en temps réel"""
    parle(f"Pont: {longueur_du_pont} | Joueur: {position_joueur} | Crocodile: {position_crocodile}")

parle(f"""
==================================================================
BONJOUR AVENTURIER DES MATHEMATIQUES,
      
Tu dois traverser un pont de tous les dangers. 
Ce pont est composé de {longueur_du_pont} planches.
      
Un crocodile te poursuit à la même vitesse.
Il est en retard de {-position_crocodile} planches par rapport à toi.

A chaque étape, on te posera une question :

- Si tu réponds juste à une question, tu avances d'une planche,
- Si tu réponds faux, tu recules d'une planche.

La limite de réponse à chaque question est de {temps_de_reponse} secondes :

- Si tu réponds au dessus de {temps_de_reponse} secondes, 
le crocodile avance d'un pas de plus et risque de te manger,
- Si tu réponds juste et en dessous de {temps_de_reponse_rapide} secondes, 
alors t'avance encore d'une planche.

BONNE CHANCE, AVENTURIER DES MATHEMATIQUES !!!
==================================================================
""")

input("Appuie sur ENTREE dès que est prêt !")

# on initialise le temps pour le calcul des temps de réponse
premier_temps=time.time()
dernier_temps=premier_temps

while True:
    # Rappel de la position du joueur
    affiche_statistiques()

    # Poser la question
    nb_de_question+=1
    a, b, resultat_attendu = donne_moi_un_calcul()
    resultat_joueur=demande(f"Combien font {a} x {b} ?")

    # gestion du temps
    temps_actuel=time.time()
    temps_ecoule=temps_actuel-dernier_temps
    dernier_temps=temps_actuel
    if temps_ecoule<temps_mini:
        temps_mini=temps_ecoule
        temps_mini_question=f"{a} x {b}"
    if temps_ecoule>temps_maxi:
        temps_maxi=temps_ecoule
        temps_maxi_question=f"{a} x {b}"
    
    # Dans tous les cas le crocodile avance
    position_crocodile=position_crocodile+pas_du_crocodile
    
    # On vérifie le résultat du joueur
    if int(resultat_joueur)==resultat_attendu:
        parle_vert(f"Bravo !!! C'était bien {resultat_attendu}")
        parle_vert(f"Tu avances de {reponse_correcte}")
        position_joueur=position_joueur+reponse_correcte
        nb_de_question_juste+=1

        # On verifie le temps de réponse
        if (temps_ecoule<=temps_de_reponse_rapide):
            parle_vert(f"WAOUHHHH, {int(temps_ecoule)} secondes !!! T'es rapide !")
            parle_vert(f"Tu avances ENCORE de {reponse_correcte}")
            position_joueur=position_joueur+reponse_correcte
            nb_de_question_rapide+=1
    else:
        parle_rouge(f"FAUX !!!! C'était {resultat_attendu}")
        parle_rouge(f"Tu recules de {reponse_correcte}")
        position_joueur=position_joueur-reponse_correcte
        nb_de_question_fausse+=1

    if (temps_ecoule>temps_de_reponse):
        parle_rouge(f"ATTENTION !!! Tu as répondu en {int(temps_ecoule)} secondes")
        parle_rouge(f"Le crocodile se RaPPPPRROOOOOOOCHHHE !!! ")
        position_crocodile=position_crocodile+pas_du_crocodile*int(temps_ecoule/temps_de_reponse)
        nb_de_question_lente+=1

    # Fins possibles
    if position_joueur<0:
        parle("""
        ====================================
              TU ES TOMBE DU PONT !!!
        ====================================
        """)
        break

    if position_crocodile>=position_joueur:
        parle("""
        =============================================
              TU AS PERDU !!!
                LE CROCODILE T'A BOUFFE !!!
        =============================================
        """)
        break

    if position_joueur>=longueur_du_pont:
        parle("""
        ====================================
            TU AS REUSSI LE PASSAGE DU PONT
                BRAVOOOOOOOO !!!
        ====================================
        """)
        break

temps_total=time.time()-premier_temps

print(f"""
============================================================
Résumé du jeu
============================================================
Vous avez traversé {position_joueur} planches sur les {longueur_du_pont} du pont
Vous avez répondu juste à {nb_de_question_juste} questions
Vous avez répondu faux à {nb_de_question_fausse} questions
Vous avez mis {temps_total:.2f} secondes pour {nb_de_question} questions
Vous avez mis environ {(temps_total/nb_de_question):.2f} secondes par question
Vous avez distancé le crocodile sur {nb_de_question_rapide} questions
Vous avez été rattrapé par le crocodile sur {nb_de_question_lente} questions
Vous avez mis {temps_mini:.2f} secondes sur la question {temps_mini_question}
Vous avez mis {temps_maxi:.2f} secondes sur la question {temps_maxi_question}
============================================================
""")

