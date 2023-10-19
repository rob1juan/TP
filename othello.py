# Ce fichier contient l'implémentation de base du jeu comme le plateau, la logique du jeu, les mouvements valides, etc.
import random


class Othello:
  BLANC = 'B'
  NOIR = 'N'
  VIDE = '.'

  DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1),
                (1, 1)]
  
  def __init__(self):
    # Initialisation du plateau de jeu
    self.plateau = [[Othello.VIDE for _ in range(8)] for _ in range(8)]
    # Placement des pions initiaux
    self.plateau[3][3], self.plateau[4][4] = Othello.BLANC, Othello.BLANC
    self.plateau[3][4], self.plateau[4][3] = Othello.NOIR, Othello.NOIR

  def mouvements_valides(self, couleur):
    adversaire = Othello.NOIR if couleur == Othello.BLANC else Othello.BLANC
    valides = []
    for x in range(8):
      for y in range(8):
        if self.plateau[x][y] == Othello.VIDE:
          for dx, dy in Othello.DIRECTIONS:
            if self._est_valide_direction(x, y, dx, dy, couleur, adversaire):
              valides.append((x, y))
              break
    return valides

  def _est_valide_direction(self, x, y, dx, dy, couleur, adversaire):
    x += dx
    y += dy
    if 0 <= x < 8 and 0 <= y < 8 and self.plateau[x][y] == adversaire:
      x += dx
      y += dy
      while 0 <= x < 8 and 0 <= y < 8:
        if self.plateau[x][y] == couleur:
          return True
        if self.plateau[x][y] == Othello.VIDE:
          break
        x += dx
        y += dy
    return False

  def effectuer_mouvement(self, x, y, couleur):
    if (x, y) not in self.mouvements_valides(couleur):
      return False
    adversaire = Othello.NOIR if couleur == Othello.BLANC else Othello.BLANC
    self.plateau[x][y] = couleur
    for dx, dy in Othello.DIRECTIONS:
      if self._est_valide_direction(x, y, dx, dy, couleur, adversaire):
        self._retourner_pions(x, y, dx, dy, couleur)
    return True

  def _retourner_pions(self, x, y, dx, dy, couleur):
    x += dx
    y += dy
    while 0 <= x < 8 and 0 <= y < 8 and self.plateau[x][y] != couleur:
      self.plateau[x][y] = couleur
      x += dx
      y += dy

  def est_terminé(self):
    return not self.mouvements_valides(
        Othello.BLANC) and not self.mouvements_valides(Othello.NOIR)

  def random_coup(self, couleur):
    valides = self.mouvements_valides(couleur)
    return random.choice(valides)
