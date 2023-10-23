# Pour tout ce qui concerne l'interface graphique.
from othello import Othello


class GUI:

  @staticmethod
  def choisir_couleur():
    while True:
      choix = input(
          "Voulez-vous jouer avec les blancs (B) ou les noirs (N)? ").upper()
      if choix in ['B', 'N']:
        return choix
      print("Choix invalide. Veuillez choisir B ou N.")

  @staticmethod
  def type_partie():
    options = {"1": "Joueur vs Joueur", "2": "Joueur vs IA", "3": "IA vs IA"}
    while True:
      print("Choisissez le type de partie :")
      for key, value in options.items():
        print(f"{key}. {value}")
      choix = input()
      if choix in options:
        return options[choix]
      print("Choix invalide. Veuillez choisir une option valide.")

  @staticmethod
  def choisir_type_ia(num_ia=None):
    options = {
        "1": ("MinMax", "IA_MINMAX"),
        "2": ("AlphaBeta", "IA_ALPHABETA"),
        "3": ("NegaMax", "IA_NEGAMAX"),
        "4": ("Random", "IA_RANDOM")
    }
    if num_ia is not None:
      print(f"Veuillez choisir le type d'IA {num_ia} :")

    for key, value in options.items():
      print(f"{key}. {value[0]}")
    while True:
      choix = input("Entrez le numéro correspondant à votre choix : ")
      if choix in options:
        return options[choix][1]
      print("Choix invalide. Veuillez choisir une option valide.")

  @staticmethod
  def choisir_strategie_ia():
    options = {
        "1": ("Positionnel", "IA_POSITIONNEL"),
        "2": ("Absolu", "IA_ABSOLU"),
        "3": ("Mobilité", "IA_MOBILITE"),
        "4": ("Mixte", "IA_MIXTE")
    }
    print("Veuillez choisir la stratégie de l'IA :")
    for key, value in options.items():
      print(f"{key}. {value[0]}")
    while True:
      choix = input("Entrez le numéro correspondant à votre choix : ")
      if choix in options:
        return options[choix][1]
      print("Choix invalide. Veuillez choisir une option valide.")

  @staticmethod
  def saisir_mouvement():
    while True:
      try:
        y, x = map(int,
                   input("Entrez votre mouvement (format: x y): ").split())
        if 0 <= x < 8 and 0 <= y < 8:
          return x, y
      except ValueError:
        pass
      print(
          "Mouvement invalide. Veuillez entrer des coordonnées valides (entre 0 et 7)."
      )

  @staticmethod
  def compter_pions(plateau):
    blancs = sum(ligne.count(Othello.BLANC) for ligne in plateau)
    noirs = sum(ligne.count(Othello.NOIR) for ligne in plateau)
    return blancs, noirs

  @staticmethod
  def afficher_plateau(plateau):
    # Affichage des coordonnées horizontales
    print("  " + " ".join(str(i) for i in range(8)))

    for index, ligne in enumerate(plateau):
      # Affichage de la coordonnée verticale
      print(str(index) + " " + ' '.join(ligne))
    print()
    # Compter les pions et afficher les scores
    blancs, noirs = GUI.compter_pions(plateau)
    print(f"Blancs (B): {blancs} | Noirs (N): {noirs}\n")

  @staticmethod
  def afficher_plateau_avec_mouvements(plateau, mouvements):
    plateau_avec_mouvements = [ligne.copy() for ligne in plateau]
    for x, y in mouvements:
      plateau_avec_mouvements[x][y] = '?'
    GUI.afficher_plateau(plateau_avec_mouvements)

  @staticmethod
  def afficher_player(player):
    print(f"Joueur {player.Couleur}: {player.Type} {player.Strategie}\n")
