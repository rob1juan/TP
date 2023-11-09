import datetime
import os
import random
import time

import utils
from Historique import Historique
from ai import IA
from gui import GUI
from othello import Othello
from player import Player


def configurer_joueurs():
  type_partie = GUI.type_partie()

  # Si c'est Joueur vs Joueur
  if type_partie == "Joueur vs Joueur":
    couleur_joueur1 = random.choice([Othello.BLANC, Othello.NOIR])
    couleur_joueur2 = Othello.NOIR if couleur_joueur1 == Othello.BLANC else Othello.BLANC
    return Player(couleur_joueur1, "JOUEUR"), Player(couleur_joueur2, "JOUEUR")

  # Si c'est Joueur vs IA
  elif type_partie == "Joueur vs IA":
    couleur_joueur = GUI.choisir_couleur()
    couleur_ia = Othello.NOIR if couleur_joueur == Othello.BLANC else Othello.BLANC
    type_ia = GUI.choisir_type_ia()
    strategie_ia = GUI.choisir_strategie_ia()
    return Player(couleur_joueur, "JOUEUR"), Player(couleur_ia, type_ia,
                                                    strategie_ia)

  # Si c'est IA vs IA
  elif type_partie == "IA vs IA":
    type_ia1 = GUI.choisir_type_ia(1)
    strategie_ia1 = GUI.choisir_strategie_ia()
    type_ia2 = GUI.choisir_type_ia(2)
    strategie_ia2 = GUI.choisir_strategie_ia()
    couleur_ia1 = random.choice([Othello.BLANC, Othello.NOIR])
    couleur_ia2 = Othello.NOIR if couleur_ia1 == Othello.BLANC else Othello.BLANC
    return Player(couleur_ia1, type_ia1,
                  strategie_ia1), Player(couleur_ia2, type_ia2, strategie_ia2)

  else:
    return Player(Othello.BLANC, "JOUEUR"), Player(Othello.NOIR, "JOUEUR")


def jouer_tour(jeu, joueur_actuel, ia):
  utils.clear_console()
  print(
      f"======================\nC'est au tour des {joueur_actuel.Couleur}\n======================\n"
  )

  mouvements = jeu.mouvements_valides(joueur_actuel.Couleur)
  if not mouvements:
    print("Pas de mouvements valides !")
    return joueur_actuel  # Retourner le joueur actuel pour changer le tour

  GUI.afficher_plateau_avec_mouvements(jeu.plateau, mouvements)
  if joueur_actuel.Type == "JOUEUR":
    x, y = GUI.saisir_mouvement()
    while not jeu.effectuer_mouvement(x, y, joueur_actuel.Couleur):
      print("\nMouvement invalide. Veuillez choisir un mouvement valide.\n")
      x, y = GUI.saisir_mouvement()
  else:
    x, y = obtenir_coup_ia(jeu, joueur_actuel, ia)
    jeu.effectuer_mouvement(x, y, joueur_actuel.Couleur)


def obtenir_coup_ia(jeu, joueur_actuel, ia):
  if joueur_actuel.Type == "IA_MINMAX":
    return ia.meilleur_coup(jeu, joueur_actuel.Couleur, 3,
                            joueur_actuel.Strategie)
  elif joueur_actuel.Type == "IA_ALPHABETA":
    return ia.meilleur_coup_alpha_beta(jeu, joueur_actuel.Couleur, 3,
                                       joueur_actuel.Strategie)
  elif joueur_actuel.Type == "IA_NEGAMAX":
    return ia.meilleur_coup_negamax(jeu, joueur_actuel.Couleur, 3,
                                    joueur_actuel.Strategie)
  else:
    return jeu.random_coup(joueur_actuel.Couleur)


def main():
  jeu = Othello()
  ia = IA()

  joueur1, joueur2 = configurer_joueurs()

  # Les blancs commencent
  joueur_actuel = joueur1 if joueur1.Couleur == Othello.BLANC else joueur2

  # Avant la boucle de jeu, définir le nom du fichier pour cette partie
  date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  partie_filename = f"partie_{date_time}.txt"

  while not jeu.est_terminé():
    mouvements = jeu.mouvements_valides(joueur_actuel.Couleur)
    if not mouvements:
      joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2
      continue
    jouer_tour(jeu, joueur_actuel, ia)
    Historique.enregistrer_coup(partie_filename, joueur_actuel)
    joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2

  utils.clear_console()
  #stats
  joueur_gagnant = joueur1 if joueur1.points > joueur2.points else joueur2
  Historique.enregistrer_fin_partie(partie_filename, joueur_gagnant)
  Historique.mise_a_jour_fichier_global(joueur1, joueur2, joueur_gagnant)

  print("Le jeu est terminé !")
  GUI.afficher_plateau(jeu.plateau)
  GUI.afficher_player(joueur1)
  GUI.afficher_player(joueur2)


def main_stats(nb_parties):
  types_ia = ["IA_MINMAX", "IA_ALPHABETA", "IA_NEGAMAX"]
  strategies = ["IA_POSITIONNEL", "IA_ABSOLU", "IA_MOBILITE", "IA_MIXTE"]

  for i in range(nb_parties):
    # Sélection aléatoire du type et de la stratégie pour chaque IA
    type_ia1 = random.choice(types_ia)
    strategie_ia1 = random.choice(strategies)

    type_ia2 = random.choice(types_ia)
    strategie_ia2 = random.choice(strategies)

    couleur_ia1 = random.choice([Othello.BLANC, Othello.NOIR])
    couleur_ia2 = Othello.NOIR if couleur_ia1 == Othello.BLANC else Othello.BLANC

    joueur1 = Player(couleur_ia1, type_ia1, strategie_ia1)
    joueur2 = Player(couleur_ia2, type_ia2, strategie_ia2)

    jeu = Othello()
    ia = IA()

    joueur_actuel = joueur1 if joueur1.Couleur == Othello.BLANC else joueur2

    while not jeu.est_terminé():
      mouvements = jeu.mouvements_valides(joueur_actuel.Couleur)
      if not mouvements:
        joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2
        continue
      x, y = (0, 0)

      if joueur_actuel.Type == "IA_MINMAX":
        x, y = ia.meilleur_coup(jeu, joueur_actuel.Couleur, 3,
                                joueur_actuel.Strategie)
      elif joueur_actuel.Type == "IA_ALPHABETA":
        x, y = ia.meilleur_coup_alpha_beta(jeu, joueur_actuel.Couleur, 3,
                                           joueur_actuel.Strategie)
      elif joueur_actuel.Type == "IA_NEGAMAX":
        x, y = ia.meilleur_coup_negamax(jeu, joueur_actuel.Couleur, 3,
                                        joueur_actuel.Strategie)

      jeu.effectuer_mouvement(x, y, joueur_actuel.Couleur)
      joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2

    b, n = GUI.compter_pions(jeu.plateau)
    jblanc = joueur1 if joueur1.Couleur == Othello.BLANC else joueur2
    jnoir = joueur1 if joueur1.Couleur == Othello.NOIR else joueur2
    joueur_gagnant = jblanc if b > n else jnoir
    Historique.mise_a_jour_fichier_global(joueur1, joueur2, joueur_gagnant)
    print(f"game {i} done")


if __name__ == "__main__":
  main()
  #main_stats(1000)
