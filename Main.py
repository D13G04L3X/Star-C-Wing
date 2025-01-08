import pygame
import sys

# Inicializar PyGame
pygame.init()

# Configuración básica de la ventana
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star C-Wing")

# Colores
COLORS = {
    "BLACK": (0, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "CYAN": (0, 255, 255),
    "RED": (255, 0, 0),
    "MAGENTA": (255, 0, 255),
    "BROWN": (165, 42, 42),
    "LGREY": (211, 211, 211),
    "DGREY": (169, 169, 169),
    "LBLUE": (173, 216, 230),
    "LGREEN": (144, 238, 144),
    "LCYAN": (224, 255, 255),
    "LRED": (255, 102, 102),
    "LMAGENTA": (255, 153, 255),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255),
}

