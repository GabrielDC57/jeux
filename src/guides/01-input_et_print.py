# Mettre le résultat d'une question dans une variable (emplacement mémoire  sauvegarde)
age = input("Quel est ton age ?")
annee_courante = input("Et on est en quelle année ?")
nom_du_heros = input("Quel est ton prénom ?")

# Faire des calculs, ici une soustraction entre annee courant et l'age
# on est obligé de mettre int() autour, car c'était des textes...et il faut les convertir en entier(chiffre pas à virgule)
annee_de_naissance = int(annee_courante) - int(age) # int c'est pour transformer un mot en chiffre.

# Afficher les résultats
print(f"Je m'appelle {nom_du_heros}.")
print(f"Je suis en né {annee_de_naissance} et j'ai {age} ans.")

# Faire une condition si plus petit que 2016
if annee_de_naissance < 2016:
    print(f"Oula lala {nom_du_heros} ! Tu es vachement vieux ! Reste au lit papy")
else:
    print("A l'aventure !")

