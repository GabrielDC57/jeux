# je tape mon texte ici
mon_texte = """
Une femme part au marché avec son fils. Une fois arrivés sur place, ils font le tour des étales.
Les fruits et les légumes sont très beaux. La mère se laisse d'abord tenter par des fraises et des
framboises. A l'étale du boucher, elle achète du foie. ELle a aussi très envie de fleurs. Mais les prix sont élevés.
Elle demande à la marchande de faire un effort pour les baisser. La commerçante refuse. Elle affirme qu'elle les vendra
facilement, même à ce prix ! La jeune femme déçue, repart avec son fils, ils se dirigent alors vers un marchand de vetements
car il faut un survetement neuf pour le garcon. Enfin, sur le chemin du retour, ils s'arrêtent un moment pour écouter un 
saxophoniste qui joue à côté de la pharmacie. La mère fournit quelques pièces à son enfants pour qu'il les dépose dans un petit coffret
en fer placé devant le musicien.
"""

# J'enlève les sauts de ligne
mon_texte_sans_saut_de_ligne = mon_texte.replace("\n", " ").replace(".", " ").replace(",", " ").replace("!", " ")


# je fais une liste de mot à partir du texte en coupant le texte à tous les espaces trouvés
liste_de_mots = mon_texte_sans_saut_de_ligne.split(" ")

# je prépare 3 listes
mots_avec_f = []
mots_avec_ff = []
mots_avec_ph = []
mots_avec_v = []

# Je fais un traitement pour chaque mot (boucle sur liste_de_mots)
for mot in liste_de_mots:
    # on cherche les mots avec ff
    if "ff" in mot:
        mots_avec_ff.append(mot)
    # on cherche les mots avec f mais qui ne sont pas déjà dans ff
    if "f" in mot and mot not in mots_avec_ff and mot not in mots_avec_f:
        mots_avec_f.append(mot)
    # on cherche les mots avec ph
    if "ph" in mot:
        mots_avec_ph.append(mot)
    # on cherche les mots avec v
    if "v" in mot and mot not in mots_avec_v:
        mots_avec_v.append(mot)

# j'affiche les résultats après la boucle for du dessus
print(f"Les mots avec ff:{len(mots_avec_ff)}")
print(mots_avec_ff)
print(f"Les mots avec f:{len(mots_avec_f)}")
print(mots_avec_f)
print(f"Les mots avec ph:{len(mots_avec_ph)}")
print(mots_avec_ph)
print(f"Les mots avec v:{len(mots_avec_v)}")
print(mots_avec_v)