# Contient les fonctions d'évaluations de l'IA
import random
from copy import deepcopy

from othello import Othello


class IA:

  # Matrices de valeurs tactiques
  tab_eval_1 = [[500, -150, 30, 10, 10, 30, -150, 500],
                [-150, -250, 0, 0, 0, 0, -250, -150],
                [30, 0, 1, 2, 2, 1, 0, 30], [10, 0, 2, 16, 16, 2, 0, 10],
                [10, 0, 2, 16, 16, 2, 0, 10], [30, 0, 1, 2, 2, 1, 0, 30],
                [-150, -250, 0, 0, 0, 0, -250, -150],
                [500, -150, 30, 10, 10, 30, -150, 500]]

  tab_eval_2 = [[100, -20, 10, 5, 5, 10, -20, 100],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [10, -2, -1, -1, -1, -1, -2, 10],
                [5, -2, -1, -1, -1, -1, -2, 5], [5, -2, -1, -1, -1, -1, -2, 5],
                [10, -2, -1, -1, -1, -1, -2, 10],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [100, -20, 10, 5, 5, 10, -20, 100]]

  # ici qu'on fera varier les statégie de recherche
  def evaluer_plateau(self, othello: Othello, couleur, strategie):
    if strategie == "IA_POSITIONNEL":
      return self._evaluation_positionnel(othello, IA.tab_eval_1, couleur)
    elif strategie == "IA_ABSOLU":
      return self._evaluation_absolue(othello, couleur)
    elif strategie == "IA_MOBILITE":
      return self._evaluation_mobilite(othello, couleur)
    elif strategie == "IA_MIXTE":
      return self._evaluation_mixte(othello, couleur)
    else:
      raise ValueError(f"Stratégie {strategie} non reconnue.")

  def _evaluation_positionnel(self, othello: Othello, matrice, couleur):
    plateau = othello.plateau
    valeur = 0
    for i in range(8):
      for j in range(8):
        if plateau[i][j] == couleur:
          valeur += matrice[i][j]
        elif plateau[i][j] != Othello.VIDE:
          valeur -= matrice[i][j]
    return valeur

  def _evaluation_absolue(self, othello: Othello, couleur):
    plateau = othello.plateau
    adversaire = Othello.NOIR if couleur == Othello.BLANC else Othello.BLANC
    score_joueur = sum(ligne.count(couleur) for ligne in plateau)
    score_adversaire = sum(ligne.count(adversaire) for ligne in plateau)
    return score_joueur - score_adversaire

  def _evaluation_mobilite(self, othello: Othello, couleur):
    plateau = othello.plateau
    adversaire = Othello.NOIR if couleur == Othello.BLANC else Othello.BLANC
    mouvements_joueur = len(Othello().mouvements_valides(couleur))
    mouvements_adversaire = len(Othello().mouvements_valides(adversaire))
    score = mouvements_joueur - mouvements_adversaire

    # Donner une prime pour la prise des coins
    coins = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for x, y in coins:
      if plateau[x][y] == couleur:
        score += 25
      elif plateau[x][y] == adversaire:
        score -= 25
    return score

  def _evaluation_mixte(self, othello: Othello, couleur):
    nombre_pions = sum([
        ligne.count(Othello.BLANC) for ligne in othello.plateau
    ]) + sum([ligne.count(Othello.NOIR) for ligne in othello.plateau])

    # Début de partie
    if nombre_pions < 26:  # 20 à 25 premiers coups
      return self._evaluation_positionnel(othello, IA.tab_eval_1, couleur)
    # Milieu de partie
    elif nombre_pions < 52:  # Juste un nombre arbitraire pour délimiter le milieu de la partie
      return self._evaluation_mobilite(othello, couleur)
    # Fin de partie
    else:  # 10 à 16 derniers coups
      return self._evaluation_absolue(othello, couleur)

  # ALGORITHME MIN MAX
  def minmax(self, othello: Othello, couleur, strategie, profondeur,
             est_maximisant):
    plateau = othello.plateau
    # Si la profondeur est 0 ou le jeu est terminé, retournez la valeur du plateau
    if profondeur == 0 or othello.est_terminé():
      return self.evaluer_plateau(
          othello, couleur,
          strategie)  # Ici, j'utilise tab_eval_1 comme exemple

    mouvements_valides = othello.mouvements_valides(couleur)
    if est_maximisant:
      max_eval = float('-inf')
      for x, y in mouvements_valides:
        nouvelle_instance_othello = deepcopy(othello)
        nouvelle_instance_othello.effectuer_mouvement(x, y, couleur)
        eval_coup = self.minmax(nouvelle_instance_othello, couleur, strategie,
                                profondeur - 1, False)
        max_eval = max(max_eval, eval_coup)
      return max_eval
    else:
      min_eval = float('inf')
      for x, y in mouvements_valides:
        nouvelle_instance_othello = deepcopy(othello)
        nouvelle_instance_othello.effectuer_mouvement(x, y, couleur)
        eval_coup = self.minmax(nouvelle_instance_othello, couleur, strategie,
                                profondeur - 1, True)
        min_eval = min(min_eval, eval_coup)
      return min_eval

  def meilleur_coup(self, othello: Othello, couleur, profondeur, strategie):
    best_value = float('-inf') if couleur == "B" else float('inf')
    best_move = None

    mouvements_valides = othello.mouvements_valides(couleur)
    for x, y in mouvements_valides:
      nouvelle_instance_othello = deepcopy(othello)
      nouvelle_instance_othello.effectuer_mouvement(x, y, couleur)
      if couleur == "B":
        eval_coup = self.minmax(nouvelle_instance_othello, "N", strategie,
                                profondeur - 1, False)
        if eval_coup > best_value:
          best_value = eval_coup
          best_move = (x, y)
      else:
        eval_coup = self.minmax(nouvelle_instance_othello, "B", strategie,
                                profondeur - 1, True)
        if eval_coup < best_value:
          best_value = eval_coup
          best_move = (x, y)

    if (best_move is None):
      return random.choice(mouvements_valides)
    return best_move

  # ALGORITHME ALPHA - BETA
  def alphabeta(self, othello: Othello, couleur, strategie, profondeur, alpha,
                beta, est_maximisant):
    plateau = othello.plateau
    # Si la profondeur est 0 ou le jeu est terminé, retournez la valeur du plateau
    if profondeur == 0 or othello.est_terminé():
      return self.evaluer_plateau(othello, couleur, strategie)

    mouvements_valides = othello.mouvements_valides(couleur)

    if est_maximisant:
      max_eval = float('-inf')
      for x, y in mouvements_valides:
        nouvelle_instance_othello = deepcopy(othello)
        nouvelle_instance_othello.effectuer_mouvement(x, y, couleur)
        eval_coup = self.alphabeta(nouvelle_instance_othello, couleur,
                                   strategie, profondeur - 1, alpha, beta,
                                   False)
        max_eval = max(max_eval, eval_coup)
        alpha = max(alpha, eval_coup)
        if beta <= alpha:
          break
      return max_eval
    else:
      min_eval = float('inf')
      for x, y in mouvements_valides:
        nouvelle_instance_othello = deepcopy(othello)
        nouvelle_instance_othello.effectuer_mouvement(x, y, couleur)
        eval_coup = self.alphabeta(nouvelle_instance_othello, couleur,
                                   strategie, profondeur - 1, alpha, beta,
                                   True)
        min_eval = min(min_eval, eval_coup)
        beta = min(beta, eval_coup)
        if beta <= alpha:
          break
      return min_eval

  def meilleur_coup_alpha_beta(self, othello: Othello, couleur, profondeur,
                               strategie):
    best_value = float('-inf') if couleur == "B" else float('inf')
    best_move = None

    alpha = float('-inf')
    beta = float('inf')

    mouvements_valides = othello.mouvements_valides(couleur)
    for x, y in mouvements_valides:
      nouvelle_instance_othello = deepcopy(othello)
      nouvelle_instance_othello.effectuer_mouvement(x, y, couleur)
      if couleur == "B":
        eval_coup = self.alphabeta(nouvelle_instance_othello, "N", strategie,
                                   profondeur - 1, alpha, beta, False)
        if eval_coup > best_value:
          best_value = eval_coup
          best_move = (x, y)
        alpha = max(alpha, best_value)
      else:
        eval_coup = self.alphabeta(nouvelle_instance_othello, "B", strategie,
                                   profondeur - 1, alpha, beta, True)
        if eval_coup < best_value:
          best_value = eval_coup
          best_move = (x, y)
        beta = min(beta, best_value)
    if (best_move is None):
      return random.choice(mouvements_valides)
    return best_move

  # ALGORITHME NEGAMAX
  def negamax(self, jeu, profondeur, couleur, strategie):
    if profondeur == 0 or jeu.est_terminé():
      return self.evaluer_plateau(jeu, couleur, strategie)

    adversaire = Othello.NOIR if couleur == Othello.BLANC else Othello.BLANC
    max_eval = float('-inf')

    for move in jeu.mouvements_valides(couleur):
      x, y = move
      jeu_copie = deepcopy(jeu)
      jeu_copie.effectuer_mouvement(x, y, couleur)
      eval_coup = -self.negamax(jeu_copie, profondeur - 1, adversaire,
                                strategie)
      max_eval = max(max_eval, eval_coup)

    return max_eval

  def meilleur_coup_negamax(self, jeu, couleur, profondeur, strategie):
    best_value = float('-inf')
    best_move = None

    for move in jeu.mouvements_valides(couleur):
      x, y = move
      jeu_copie = deepcopy(jeu)
      jeu_copie.effectuer_mouvement(x, y, couleur)
      eval_coup = -self.negamax(jeu_copie, profondeur - 1, couleur, strategie)
      if eval_coup > best_value:
        best_value = eval_coup
        best_move = (x, y)
    if (best_move is None):
      return random.choice(mouvements_valides)
    return best_move
