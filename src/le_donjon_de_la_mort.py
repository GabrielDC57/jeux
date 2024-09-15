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
    parle(f"Bahhhh {nom_du_heros} ! TU FAIS QUOI LA ? Tu te casses ?") 

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
    parle("Tu et mage.") 
else:
    parle("Tu et mage.") 

# Nouvel étape
ae=demande("_Tu arose les fleur oui ou non") 

if ae.lower()=="oui":
    parle("ok.") 
else:
    parle("Oh zut!!") 






print("=======================================")
print("FIN DU JEU")
print("=======================================")