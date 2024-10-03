# =================================
# Jeux d'aventure de Gabriel Dupire
# =================================
# Date : 2024-09-04


def parle(texte):
    """Fonction pour faire parler le jeu"""
    print("\033[1;34m") # Colorie en bleu
    print(f"{texte}")   # Affiche la demande
    print("\033[0m")    # Recolorie en couleur normale

def demande(texte):
    """Fonction pour demander un truc au joueur"""
    return input(f"{texte}\n>") # Affiche le texte avec un saut de ligne à la fin (c'est le \n)


print("=======================================")
print("DEBUT DU JEU")
print("=======================================")

parle("Tu te reveilles !")

nom_du_heros=demande("Comment tu t'appelles ?")

# Nouvel étape
Jesor=demande(f"{nom_du_heros}, tu sors ? Oui ou Non ?")

if Jesor.lower()=="oui":
    parle(f"D'accord {nom_du_heros}. Je vois. Tu préfères sortir.")
else:
    parle(f"Bahhhh {nom_du_heros}  TU FAIS QUOI ?") 

# Nouvel étape
kir=demande("Tu vas dans le Jardin ? oui ou non ?") 

      
if kir.lower()=="oui":
    parle("Ok.Tu as obtenu une épèe solide.") 
else:
    parle("Ok.") 

# Nouvel étape
pou=demande("Tu explore oui ou non")

if pou.lower()=="oui":
    parle("Tu vois un lit, un cofre et ta valise")
else:
    parle("Ok.Ok")

# Nouvel étape
era=demande("Tu vas à la cave oui ou non") 

if era.lower()=="oui":
    parle(f"{nom_du_heros} tu t'appelle bien {nom_du_heros}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") 
else:
    parle(f"{nom_du_heros}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") 
    

# Nouvel étape
ae=demande("_Tu arose les fleur oui ou non") 

if ae.lower()=="oui":
    parle(f"ok{nom_du_heros}.") 
else:
    parle("Oh zut!!") 

ouf=demande("Où veux tu aller ? Gauche, Droite, Avant, Arrière")
if ouf.lower()=="gauche":
    print("Gauche")
elif ouf.lower()=="droite":
    print("Droite")
elif ouf.lower()=="arrière":
    print("arrier")
else:
    print("Boom le mur")
ouvrire=demande("Tu inspectes les objets oui ou non") 
if ouvrire.lower()=="oui":
    parle("Le coffre est bleu,grand et solide,le lit est vert et mesure cinq m et ta valise est orange et mesure cinquante cm") 
else:
    parle("Tu est sur?") 

parle(f"Tu part pour le dongeon de la mort!") 
parle("Tu vois un dongeon très grand il a l' air dangereus.")  
parle(f"Fais dodo {nom_du_heros}!") 
parle(f"{nom_du_heros} tu dois acheter un livre,des patates,du coca,de l'eau ...")





print("=======================================")
print("FIN DU JEU")
print("=======================================")
