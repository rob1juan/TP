import os
import time
from othello import Othello
from gui import GUI


def clear_console():
  # Effacer la console
  os.system('cls' if os.name == 'nt' else 'clear')


def main():
  jeu = Othello()
  tour = Othello.BLANC  # Les blancs commencent

  type_partie = GUI.type_partie()

  if type_partie != "Joueur vs Joueur":
    print("Mode non supporté pour le moment.")
    return

  while not jeu.est_terminé():
    clear_console()

    print(
        f"======================\nC'est au tour des {tour}\n======================\n"
    )

    mouvements = jeu.mouvements_valides(tour)
    if not mouvements:
      print("Pas de mouvements valides !")
      # Changer de tour
      tour = Othello.NOIR if tour == Othello.BLANC else Othello.BLANC
      continue

    # Affiche le plateau avec les mouvements possibles
    GUI.afficher_plateau_avec_mouvements(jeu.plateau, mouvements)

    # Demander à l'utilisateur de choisir un mouvement
    x, y = GUI.saisir_mouvement()
    while not jeu.effectuer_mouvement(x, y, tour):
      print("\nMouvement invalide. Veuillez choisir un mouvement valide.\n")
      x, y = GUI.saisir_mouvement()

    # Affichage du plateau actuel sans les mouvements possibles
    clear_console()
    GUI.afficher_plateau(jeu.plateau)
    time.sleep(1)

    # Changer de tour
    tour = Othello.NOIR if tour == Othello.BLANC else Othello.BLANC

  clear_console()
  print("Le jeu est terminé !")
  GUI.afficher_plateau(jeu.plateau)


if __name__ == "__main__":
  main()
