def affichage(text):
    """C'est une fonction d'affichage pour mettre le texte entre deux lignes"""
    print("-------------MON TEXTE A MOI ------------")
    print(text)
    print("-------------FIN DU TEXTE ------------")
    print()

affichage("Gabriel fait ses devoirs")
affichage("Gabriel fait un prout")
affichage("Gabriel fait un pied de nez")


def dit_x_fois_le_texte(text, nb_de_fois):
    for n in range(nb_de_fois):
        print(f"J'ai fait {n+1} fois {text}")

dit_x_fois_le_texte("Prout", 100)
dit_x_fois_le_texte("Je te kiffe",20)