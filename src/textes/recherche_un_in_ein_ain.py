# je tape mon texte ici
mon_texte = """
Ce lundi matin de printemps, Romain va visiter le jardin d'un peintre impressioniste avec sa classe.
Romain et cinq de ses copains, leur sac à main, vont et viennent dans la cour. Chacun guette l'arrivée
du car avec impatience. Soudain le voici ! Les élèves montent et le car démarre enfin. Le trajet dure
vingt minutes. En arrivant, les enfants ont déjà une faim de loup. Romain a du bon pain qu'il voudrait
manger dès maintenant. Mais avant, le maitre propose à la classe de faire un tour dans le jardin. Celui-ci
est très beau. Les tulipes, les jacinthes et les crocus sont en fleurs et le parfum, des narcisses embaument
les chemins. Les enfants ne sont pas déçus d'avoir attendu.
"""

# J'enlève les sauts de ligne
mon_texte_sans_saut_de_ligne = mon_texte.replace("\n", " ").replace(".", " ").replace(",", " ").replace("!", " ")


# je fais une liste de mot à partir du texte en coupant le texte à tous les espaces trouvés
liste_de_mots = mon_texte_sans_saut_de_ligne.split(" ")

# je prépare 3 listes
mots_avec_in_im = []
mots_avec_ain_aim = []
mots_avec_ein = []
mots_avec_un_um = []

# Je fais un traitement pour chaque mot (boucle sur liste_de_mots)
for mot in liste_de_mots:
    # on cherche les mots avec ain mais qui ne sont pas déjà dans in
    if "ain" in mot or "aim" in mot:
        mots_avec_ain_aim.append(mot)

    # on cherche les mots avec in ou im
    if ("in" in mot or "im" in mot) and mot not in mots_avec_ain_aim:
        mots_avec_in_im.append(mot)
    
    # on cherche les mots avec ein
    if "ein" in mot:
        mots_avec_ein.append(mot)

    # on cherche les mots avec v
    if "un" in mot or "um" in mot:
        mots_avec_un_um.append(mot)

# j'affiche les résultats après la boucle for du dessus
print(f"Les mots avec ain/aim:{len(mots_avec_ain_aim)}")
print(mots_avec_ain_aim)
print(f"Les mots avec in/im:{len(mots_avec_in_im)}")
print(mots_avec_in_im)
print(f"Les mots avec ein:{len(mots_avec_ein)}")
print(mots_avec_ein)
print(f"Les mots avec un/um:{len(mots_avec_un_um)}")
print(mots_avec_un_um)