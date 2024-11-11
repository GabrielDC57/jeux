class Personnage:
    def __init__(self, name, age):
        self.name=name
        self.age=age
        self.fais_dodo=False

    def dire_bonjour(self):
        if self.fais_dodo is True:
            print("... peux pas répondre...il dort")
        else:
            print(f"Bonjour l'ami, je m'appelle {self.name}")

    def dire_son_age(self):
        if self.fais_dodo is True:
            print("... peux pas répondre...il dort")
        else:
            print(f"J'ai {self.age} ans")

    def se_coucher(self):
        if self.fais_dodo is True:
            print(f"Mais t'es con ou quoi ? {self.name} dormait déjà")    
        else:
            print(f"{self.name} va se coucher et il ronfle !!!")
        self.fais_dodo=True

    def se_reveiller(self):
        if self.fais_dodo is False:
            print(f"MAIS {self.name} était déjà réveillé !!!")
        else:
            print(f"{self.name} se reveille !!!")
        self.fais_dodo=False



gabriel=Personnage("Gabriel", 8)
papa=Personnage("Sébastien", 44)
maman=Personnage("Anne-Lise", 43)
raphou=Personnage("Raphaëlle", 6)
elora=Personnage("Elora", 18)

gabriel.dire_bonjour()
gabriel.se_coucher()
gabriel.se_coucher()
gabriel.dire_bonjour()
gabriel.se_reveiller()
gabriel.se_reveiller()
gabriel.dire_bonjour()
gabriel.dire_son_age()
elora.dire_son_age() 