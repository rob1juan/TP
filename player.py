# Classe de base pour les joueurs et des sous-classes pour les joueurs humains et ordinateurs.
class Player:
  Color = ""
  Type = ""
  Strategie = ""

  TYPES = ["JOUEUR", "IA_MINMAX", "IA_ALPHABETA", "IA_NEGAMAX", "IA_RANDOM"]

  def __init__(self, color, type, strategie="IA_POSITIONNEL"):
    self.Couleur = color
    self.Type = type
    self.Strategie = strategie
