# =================================
# Jeux d'aventure de Gabriel Dupire
# =================================
# Date : 2024-09-04


print("=======================================")
print("DEBUT DU JEU")
print("=======================================")

print("- Tu te reveilles")

nom_du_heros=input("- Comment tu t'appelles ?:")

Jesor=input("- " + nom_du_heros + ", tu sors ? Oui ou Non ?:")
if Jesor.lower()=="oui":
    print("- D'accord " + nom_du_heros + ". Je vois. Tu préfères sortir.")
else:
    print("- Bahhhh " + nom_du_heros + "! TU FAIS QUOI LA ? Tu te casses ?") 

kir=input("- Tu vas dans le Jardin ? oui ou non ?:") 

if kir.lower()=="oui":
    print("- Ok.Tu as obtenu une épèe solide.") 
else:
    print("- OK.")



print("=======================================")
print("FIN DU JEU")
print("=======================================")
