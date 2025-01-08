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

# Clase Ship para manejar la nave
class Ship:
    def __init__(self, x, y, stocks, lives):
        self.x = x
        self.y = y
        self.stocks = stocks
        self.lives = lives

    def draw(self):
        pygame.draw.polygon(WINDOW, COLORS["LGREEN"], [(self.x, self.y), (self.x + 20, self.y + 10), (self.x, self.y + 20)])

    def draw_info(self, score, top_score):
        font = pygame.font.SysFont("Arial", 20)
        # Dibujar vidas
        lives_text = font.render(f"Naves: {self.lives}", True, COLORS["WHITE"])
        WINDOW.blit(lives_text, (55, 10))
        # Dibujar puntaje
        score_text = font.render(f"Puntaje: {score}", True, COLORS["WHITE"])
        WINDOW.blit(score_text, (4, 10))
        # Dibujar escudo
        shield_text = font.render(f"Escudo: {'*' * self.stocks}", True, COLORS["LRED"])
        WINDOW.blit(shield_text, (70, 10))
        # Dibujar puntaje más alto
        top_score_text = font.render(f"Top: {max(score, top_score)}", True, COLORS["LGREY"])
        WINDOW.blit(top_score_text, (200, 10))

    def clear(self):
        pygame.draw.rect(WINDOW, COLORS["BLACK"], (self.x - 5, self.y - 5, 30, 30))

    def update_lives(self, score_point):
        if score_point >= 7000:
            self.lives += 1
            return 0  # Reset score point
        if self.stocks <= 0:
            self.clear()
            self.lives -= 1
            # Dibujar explosión
            pygame.draw.circle(WINDOW, COLORS["YELLOW"], (self.x, self.y), 20)
            pygame.display.update()
            pygame.time.delay(500)
        return score_point

# Función para pintar los bordes del escenario
def draw_stage_border():
    pygame.draw.rect(WINDOW, COLORS["YELLOW"], (40, 10, WIDTH - 80, HEIGHT - 20), 2)
    font = pygame.font.SysFont("Arial", 30)
    title = font.render("STAR C-WING", True, COLORS["YELLOW"])
    WINDOW.blit(title, (WIDTH // 2 - title.get_width() // 2, 5))

# Ocultar/Mostrar cursor (PyGame lo maneja por defecto)
def set_cursor_visibility(visible):
    pygame.mouse.set_visible(visible)

# Bucle principal del juego
def main():
    clock = pygame.time.Clock()
    running = True
    ship = Ship(400, 300, 5, 3)
    score = 0
    top_score = 10000
    score_point = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar todo
        WINDOW.fill(COLORS["BLACK"])
        draw_stage_border()
        ship.draw()
        ship.draw_info(score, top_score)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
