class Historique:

@staticmethod
def enregistrer_coup(partie_filename, joueur):
    with open(partie_filename, 'a') as file:
        file.write(f"{joueur.Couleur},{joueur.Type},{joueur.Strategie},{joueur.dernier_coup[0]},{joueur.dernier_coup[1]}\n")

@staticmethod
def enregistrer_fin_partie(partie_filename, joueur_gagnant):
    with open(partie_filename, 'a') as file:
        file.write(f"{joueur_gagnant.Couleur},{joueur_gagnant.Type},{joueur_gagnant.Strategie},{joueur_gagnant.points}\n")

@staticmethod
def mise_a_jour_fichier_global(joueur1, joueur2, joueur_gagnant):
    with open("historique_global.txt", 'a') as file:
        file.write(f"{joueur1.Type},{joueur1.Strategie},{joueur1.Couleur},{joueur2.Type},{joueur2.Strategie},{joueur2.Couleur},{joueur_gagnant.Type}_{joueur_gagnant.Strategie}\n")