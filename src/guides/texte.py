mon_texte = """
Ce matin, Barnabé va rendre visite à sa tante : il doit lui apporter une revue. Il fait presque chaud;
on voit aue la date du printemps approche ! Il décide de passer par le parc, ce sera plus agréable 
que le boulevard avec les voitures partout. Cependant, au parc, ce n'est pas tout calme, il y a beaucoup
de monde. Barnabé se demande qui fait le plus de bruit : les filles qui font de la balançoire ou du 
toboggan ? Ceux qui pataugent avec des bottes dans la boue ? Le garçon qui frappe dans un ballon puis 
court pour l'attraper ? Ou bien encore les bébés qui crient ou pleurent ?
Sur la butte, il aperçoit même des garçons qui jouent à se battre, ils s'attaquent avec des épées en bois
... Pourquoi aije choisi ce chemin ? se demande-t-il. Alors, Barnabé quitte le parc et retourne sur le
boulevard.
"""

mon_texte_sans_saut_ligne = mon_texte.replace("\n"," ")
print("Mon texte:")
print(mon_texte_sans_saut_ligne)

liste_mot_avec_p = []
liste_mot_avec_b = []
for mot in mon_texte_sans_saut_ligne.split(" "):
    if "p" in mot:
        liste_mot_avec_p.append(mot)
    if "b" in mot:
        liste_mot_avec_b.append(mot)

print("\nLes mots avec b:")
print(liste_mot_avec_b)

print("\nLes mots avec p:")
print(liste_mot_avec_p)

for mot in liste_mot_avec_p:
    if "pp" in mot:
        print(f"J'ai trouvé un mot avec un double p : {mot}")