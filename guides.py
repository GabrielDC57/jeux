age = input("Quel est ton age ?")
annee_courante = input("Et on est en quelle année ?")
nom_du_heros = input("Quel est ton prénom ?")

annee_de_naissance = int(annee_courante) - int(age) # int c'est pour transformer un mot en chiffre.

print(f"Je m'appelle {nom_du_heros}.")
print(f"Je suis en né {annee_de_naissance} et j'ai {age} ans.")
if annee_de_naissance < 2016:
    print(f"Oula lala {nom_du_heros} ! Tu es vachement vieux ! Reste au lit papy")
else:
    print("A l'aventure !")

