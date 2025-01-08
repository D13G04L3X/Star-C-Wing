import pygame
import random
import pygame
pygame.init()  # Inicializa todos los módulos de pygame
pygame.mixer.init()  # Inicializa el módulo de sonido

# Inicializar PyGame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star C-Wing")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LCYAN = (0, 255, 255)
LRED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Velocidades iniciales
ENEMY_SPEED = 5
ASTEROID_SPEED = 3
BULLET_SPEED = 10

def draw_text(text, font_size, x, y, color):
    font = pygame.font.SysFont("Arial", font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Clase para los enemigos
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20

    def draw(self):
        pygame.draw.polygon(screen, LCYAN, [(self.x, self.y), (self.x + self.width, self.y + self.height // 2), (self.x, self.y + self.height)])

    def move(self):
        self.x -= ENEMY_SPEED
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(50, HEIGHT - 50)

    def check_collision(self, ship):
        ship_rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if ship_rect.colliderect(enemy_rect):
            ship.reduce_shield()
            self.reset_position()

    def reset_position(self):
        self.x = WIDTH
        self.y = random.randint(50, HEIGHT - 50)

# Clase para los asteroides
class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

    def move(self):
        self.x -= ASTEROID_SPEED
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(50, HEIGHT - 50)

# Clase para las balas
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)

    def move(self):
        self.x += BULLET_SPEED

    def is_off_screen(self):
        return self.x > WIDTH
    
# Clase Ship para manejar la nave
def main():
    clock = pygame.time.Clock()
    running = True

    # Crear instancias de enemigos, asteroides y balas
    enemies = [Enemy(WIDTH, random.randint(50, HEIGHT - 50)) for _ in range(5)]
    asteroids = [Asteroid(WIDTH, random.randint(50, HEIGHT - 50)) for _ in range(5)]
    bullets = []

    # Nave del jugador
    class Ship:
        def __init__(self):
            self.x = 100
            self.y = HEIGHT // 2
            self.width = 40
            self.height = 20
            self.shield = 3

        def draw(self):
            pygame.draw.rect(screen, LRED, (self.x, self.y, self.width, self.height))

        def move(self, keys):
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= 5
            if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
                self.y += 5

        def reduce_shield(self):
            self.shield -= 1

    player = Ship()

    while running:
        screen.fill(BLACK)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x + player.width, player.y + player.height // 2))

        # Movimiento de los objetos
        keys = pygame.key.get_pressed()
        player.move(keys)

        for enemy in enemies:
            enemy.move()
            enemy.check_collision(player)

        for asteroid in asteroids:
            asteroid.move()

        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullets.remove(bullet)

        # Dibujar los objetos
        player.draw()

        for enemy in enemies:
            enemy.draw()

        for asteroid in asteroids:
            asteroid.draw()

        for bullet in bullets:
            bullet.draw()

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

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
