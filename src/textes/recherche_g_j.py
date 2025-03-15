# je tape mon texte ici
mon_texte = """
Un jeune enfant, à son bureau, ne joue pas : il a un exercice de conjugaison à faire. Mais il n'arrive toujours pas à le finir.
Parfois, il regarde à la fenêtre. Avec le gel et le givre sur les arbres, le paysage est beau. La place du village est déserte, les gens restent 
chez eux, même les pigeons sont à l'abri.
L'enfant aperçoit alors son père à travers la vitre, les joues rouges. Il a froid, il fait de grands gestes pour se réchauffer. Son fils descend le retrouver
dans le salon.
Le père dit sur la route gelée, le trajet m'a semblé long pour rejoindre la maison ! Puis il s'asseoit et raconte Sur le trottoir en face du gymnase, une femme avec une 
jupe longue est tombée, elle s'est fait mal à la jambe, je l'ai aidéé à se relever. Elle voulait aller jusqu'à la ferme de Gérard, mais elle a changé de projet.
Comme lele boitait, je l'ai accompagnée chez le médecin. Elle n'y était jamais allé. Et il ajoute Mais je suis bien content d'être enfin rentré au chaud !
"""

# J'enlève les sauts de ligne
mon_texte_sans_saut_de_ligne = mon_texte.replace("\n", " ").replace(".", " ").replace(",", " ").replace("!", " ")


# je fais une liste de mot à partir du texte en coupant le texte à tous les espaces trouvés
liste_de_mots = mon_texte_sans_saut_de_ligne.split(" ")

# je prépare listes
mots_avec_g = set()
mots_avec_j = set()

# Je fais un traitement pour chaque mot (boucle sur liste_de_mots)
for mot in liste_de_mots:
    # on cherche les mots avec g
    if "g" in mot:
        mots_avec_g.add(mot)
    if "j" in mot:
        mots_avec_j.add(mot)
    
    
# j'affiche les résultats après la boucle for du dessus
print(f"Les mots avec g:{len(mots_avec_g)}")
print(mots_avec_g)
print(f"Les mots avec h:{len(mots_avec_j)}")
print(mots_avec_j)