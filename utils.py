# Pour tout code auxiliaire ou fonctions utiles, comme la mémorisation des états de jeu, la gestion des temps, etc.
import os


@staticmethod
def clear_console():
  # Effacer la console
  os.system('cls' if os.name == 'nt' else 'clear')
