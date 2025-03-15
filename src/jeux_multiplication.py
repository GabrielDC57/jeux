import random, time

# variables génériques
temps_de_reponse = 12
temps_de_reponse_rapide = 4
longueur_du_pont = 20

# regle pour avancer
reponse_correcte = 1
pas_du_crocodile = 1

# position
position_joueur=0
position_crocodile=-int(longueur_du_pont / 2)

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

def demande(texte):
    """Fonction pour demander un truc au joueur"""
    return input(f"{texte}\n>") # Affiche le texte avec un saut de ligne à la fin (c'est le \n)

def donne_moi_un_calcul():
    """Fonction pour générer deux chiffres aléatoires et obtenir le résultat du X"""
    #chiffre_1=random.randrange(0,10,1)
    chiffre_1=random.choice([7,3,8,4])
    chiffre_2=random.randrange(0,10,1)
    result=chiffre_1*chiffre_2
    return chiffre_1, chiffre_2, result

def affiche_statistiques():
    """Afficher les infos en temps réel"""
    parle(f"Pont: {longueur_du_pont} | Joueur: {position_joueur} | Crocodile: {position_crocodile}")

print(f"""
==================================================================
BONJOUR AVENTURIER DES MATHEMATIQUES
      
Tu dois traverser un pont. Le pont est composé de 20 planches.
      
Un crocodile te poursuit à la même vitesse.
Il est en retard de {longueur_du_pont/2} planches
par rapport à toi.

A chaque étape, on te pose une question :

- Si tu réponds juste à une question, tu avances d'une planche,
- Si tu réponds faux, tu recules d'une planche,

MAIS le temps compte aussi : 

- Si tu réponds en dessous de ({temps_de_reponse}) secondes, 
le crocodile avance d'un pas de plus et risque de te manger
- Si tu réponds juste et en dessous de {temps_de_reponse_rapide} secondes, 
alors t'avance encore d'une planche

La limite de réponse à chaque question est
de {temps_de_reponse} secondes.
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
        print(f"Bravo !!! C'était bien {resultat_attendu}")
        print(f"Tu avances de {reponse_correcte}")
        position_joueur=position_joueur+reponse_correcte
        nb_de_question_juste+=1
    else:
        print(f"FAUX !!!! C'était {resultat_attendu}")
        print(f"Tu recules de {reponse_correcte}")
        position_joueur=position_joueur-reponse_correcte
        nb_de_question_fausse+=1

    # On verifie le temps de réponse
    if (temps_ecoule<=temps_de_reponse_rapide):
        print(f"WAOUHHHH, {int(temps_ecoule)} secondes !!! T'es rapide !")
        print(f"Tu avances ENCORE de {reponse_correcte}")
        position_joueur=position_joueur+reponse_correcte
        nb_de_question_rapide+=1

    if (temps_ecoule>temps_de_reponse):
        print(f"ATTENTION !!! Tu as répondu en {int(temps_ecoule)} secondes")
        print(f"Le crocodile se RaPPPPRROOOOOOOCHHHE !!! ")
        position_crocodile=position_crocodile+pas_du_crocodile*int(temps_ecoule/temps_de_reponse)
        nb_de_question_lente+=1

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
        =============================================
              TU AS PERDU !!!
                LE CROCODILE T'A BOUFFE GROS NUL !!!
        =============================================
        """)
        break

    if position_joueur==longueur_du_pont:
        parle("""
        ====================================
            TU AS REUSSI LE PASSAGE DU PONT
                BRAVOOOOOOOO LE NUL !!!
        ====================================
        """)
        break

temps_total=time.time()-premier_temps

print()
print(f"======================================================================================")
print(f"Résumé du jeu")
print(f"======================================================================================")
print(f"Vous avez traversé {position_joueur} planches sur les {longueur_du_pont} du pont")
print(f"Vous avez répondu juste à {nb_de_question_juste} questions")
print(f"Vous avez répondu faux à {nb_de_question_fausse} questions")
print(f"Vous avez mis {temps_total:.2f} secondes pour {nb_de_question} questions")
print(f"Vous avez mis environ {(temps_total/nb_de_question):.2f} secondes par question")
print(f"Vous avez distancé le crocodile sur {nb_de_question_rapide} questions")
print(f"Vous avez été rattrapé par le crocodile sur {nb_de_question_lente} questions")
print(f"Vous avez mis {temps_mini:.2f} secondes sur la question {temps_mini_question}")
print(f"Vous avez mis {temps_maxi:.2f} secondes sur la question {temps_maxi_question}")
print(f"======================================================================================")

