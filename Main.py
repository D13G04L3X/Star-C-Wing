import pygame
import random
import pygame
pygame.init()  # Inicializa todos los módulos de pygame
pygame.mixer.init()  # Inicializa el módulo de sonido
import json

# Inicializar PyGame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1280, 650
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
ENEMY_SPEED = 10
ASTEROID_SPEED = 6
BULLET_SPEED = 20

# Cargar imágenes de fondo
menu_bg = pygame.image.load("menu_background.png")
game_bg = pygame.image.load("game_background.png")

def draw_text(text, font_size, x, y, color):
    font = pygame.font.SysFont("Arial", font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def save_game(player_name, score):
    save_data = {"player_name": player_name, "score": score}
    with open(f"{player_name}_save.json", "w") as save_file:
        json.dump(save_data, save_file)

def load_game(player_name):
    try:
        with open(f"{player_name}_save.json", "r") as save_file:
            save_data = json.load(save_file)
            return save_data["score"]
    except FileNotFoundError:
        return 0

# Clase para los enemigos
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('enemy.png')  # Imagen del enemigo
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def shoot(self, bullets):
        if random.randint(1, 100) < 2:  # Probabilidad baja de disparo
            bullets.append(Bullet(self.x, self.y + self.height // 2))

    def move(self):
        self.x -= ENEMY_SPEED
        if self.x < 0:
            self.reset_position()

    def reset_position(self):
        self.x = WIDTH
        self.y = random.randint(50, HEIGHT - 50)

    def check_collision(self, rect):
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return enemy_rect.colliderect(rect)

# Clase para los asteroides
class Asteroid:
    def __init__(self, x, y):
        self.image = pygame.image.load('asteroid.png')  # Imagen del asteroide
        self.x = x
        self.y = y
        self.size = random.randint(30, 50)  # Tamaño variable
        self.speed = random.randint(2, 6)  # Velocidad variable

    def draw(self):
        scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        screen.blit(scaled_image, (self.x, self.y))

    def move(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(50, HEIGHT - 50)

    def check_collision(self, rect):
        asteroid_rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        return asteroid_rect.colliderect(rect)
    
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

    def check_collision(self, rect):
        bullet_rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        return bullet_rect.colliderect(rect)
    
# Clase para la nave del jugador
class Ship:
    def __init__(self):
        self.image = pygame.image.load('ship.png')  # Agrega un sprite personalizado.
        self.x = 100
        self.y = HEIGHT // 2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = 100

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        # Dibujar barra de salud
        pygame.draw.rect(screen, RED, (10, 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (10, 10, self.health, 10))

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= 5
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += 5

# Función para manejar el disparo
def shoot_bullet(bullets, player, sound):
    bullets.append(Bullet(player.x + player.width, player.y + player.height // 2))
    sound.play()

# Función para el menú inicial
def main_menu():
    running = True
    while running:
        screen.blit(menu_bg, (0, 0))  # Imagen de fondo del menú
        draw_text("Star C-Wing", 50, WIDTH // 2 - 100, 50, WHITE)
        draw_text("1. Iniciar juego nuevo", 30, WIDTH // 2 - 150, 200, WHITE)
        draw_text("2. Cargar partida", 30, WIDTH // 2 - 150, 250, WHITE)
        draw_text("3. Ver mejores scores", 30, WIDTH // 2 - 150, 300, WHITE)
        draw_text("4. Salir", 30, WIDTH // 2 - 150, 350, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_name = input("Ingrese su nombre: ")
                    return player_name, 0  # Nuevo juego
                elif event.key == pygame.K_2:
                    player_name = input("Ingrese su nombre: ")
                    return player_name, load_game(player_name)  # Cargar juego
                elif event.key == pygame.K_4:
                    pygame.quit()
                    exit()

# Función principal del juego
def main():
    clock = pygame.time.Clock()
    running = True

    # Variables del juego
    enemies = [Enemy(WIDTH, random.randint(50, HEIGHT - 50)) for _ in range(5)]
    asteroids = [Asteroid(WIDTH, random.randint(50, HEIGHT - 50)) for _ in range(5)]
    bullets = []
    player = Ship()
    score = 0

    # Cargar sonido
    shoot_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound('shoot.wav')))

    while running:
        screen.blit(game_bg, (0, 0))  # Imagen de fondo del menú screen.fill(BLACK)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet(bullets, player, shoot_sound)

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Movimiento y lógica de los enemigos y asteroides
        for enemy in enemies[:]:
            enemy.move()
            if enemy.check_collision(pygame.Rect(player.x, player.y, player.width, player.height)):
                player.health -= 20
                enemy.reset_position()

            for bullet in bullets[:]:
                if bullet.check_collision(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(Enemy(WIDTH, random.randint(50, HEIGHT - 50)))
                    score += 10

        for asteroid in asteroids:
            asteroid.move()
            if asteroid.check_collision(pygame.Rect(player.x, player.y, player.width, player.height)):
                player.health -= 10
                asteroid.x = WIDTH

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

        # Dibujar el puntaje
        draw_text(f"Score: {score}", 20, WIDTH - 150, 10, WHITE)

        # Verificar si el jugador pierde
        if player.health <= 0:
            draw_text("GAME OVER", 50, WIDTH // 2 - 150, HEIGHT // 2 - 25, RED)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
    main()
