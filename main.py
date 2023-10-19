import os
import random
import time

from ai import IA
from gui import GUI
from othello import Othello
from player import Player


def clear_console():
  # Effacer la console
  os.system('cls' if os.name == 'nt' else 'clear')


def main():
  jeu = Othello()
  ia = IA()

  # Configuration des joueurs
  type_partie = GUI.type_partie()

  # Si c'est Joueur vs Joueur
  if type_partie == "Joueur vs Joueur":
    couleur_joueur1 = random.choice([Othello.BLANC, Othello.NOIR])
    couleur_joueur2 = Othello.NOIR if couleur_joueur1 == Othello.BLANC else Othello.BLANC
    joueur1 = Player(couleur_joueur1, "JOUEUR")
    joueur2 = Player(couleur_joueur2, "JOUEUR")

  # Si c'est Joueur vs IA
  elif type_partie == "Joueur vs IA":
    couleur_joueur = GUI.choisir_couleur()
    couleur_ia = Othello.NOIR if couleur_joueur == Othello.BLANC else Othello.BLANC
    type_ia = GUI.choisir_type_ia()
    joueur1 = Player(couleur_joueur, "JOUEUR")
    joueur2 = Player(couleur_ia, type_ia)

  # Si c'est IA vs IA
  elif type_partie == "IA vs IA":
    type_ia1 = GUI.choisir_type_ia(1)
    type_ia2 = GUI.choisir_type_ia(2)
    couleur_ia1 = random.choice([Othello.BLANC, Othello.NOIR])
    couleur_ia2 = Othello.NOIR if couleur_ia1 == Othello.BLANC else Othello.BLANC
    joueur1 = Player(couleur_ia1, type_ia1)
    joueur2 = Player(couleur_ia2, type_ia2)
  else:
    joueur1 = Player(Othello.BLANC, "JOUEUR")
    joueur2 = Player(Othello.NOIR, "JOUEUR")

  # Les blancs commencent
  joueur_actuel = joueur1 if joueur1.Couleur == Othello.BLANC else joueur2

  while not jeu.est_terminé():
    clear_console()
    print(
        f"======================\nC'est au tour des {joueur_actuel.Couleur}\n======================\n"
    )

    mouvements = jeu.mouvements_valides(joueur_actuel.Couleur)
    if not mouvements:
      print("Pas de mouvements valides !")
      joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2
      continue

    GUI.afficher_plateau_avec_mouvements(jeu.plateau, mouvements)
    x, y = 0, 0
    if joueur_actuel.Type == "JOUEUR":
      x, y = GUI.saisir_mouvement()
      while not jeu.effectuer_mouvement(x, y, joueur_actuel.Couleur):
        print("\nMouvement invalide. Veuillez choisir un mouvement valide.\n")
        x, y = GUI.saisir_mouvement()
    else:
      if joueur_actuel.Type == "IA_MINMAX":
        x, y = ia.meilleur_coup(jeu, joueur_actuel.Couleur, 3)
      elif joueur_actuel.Type == "IA_ALPHABETA":
        x, y = ia.meilleur_coup_alpha_beta(jeu, joueur_actuel.Couleur, 3)
      elif joueur_actuel.Type == "IA_NEGAMAX":
        x, y = ia.meilleur_coup_negamax(jeu, joueur_actuel.Couleur, 3)
      elif joueur_actuel.Type == "IA_RANDOM":
        x, y = jeu.random_coup(joueur_actuel.Couleur)
    jeu.effectuer_mouvement(x, y, joueur_actuel.Couleur)

    # Affichage du plateau actuel sans les mouvements possibles
    clear_console()
    GUI.afficher_plateau(jeu.plateau)
    time.sleep(1)

    # Changer de joueur
    joueur_actuel = joueur1 if joueur_actuel == joueur2 else joueur2

  clear_console()
  print("Le jeu est terminé !")
  GUI.afficher_plateau(jeu.plateau)


if __name__ == "__main__":
  main()
