import pygame   # Biblioteca para manejar gráficos, eventos, sonidos y lógica de juegos.
import sys      # Permite cerrar el programa limpiamente.
import random   # Genera valores aleatorios, en este caso, para la posición de la comida.

# Inicializar Pygame
pygame.init() # Inicia todos los modulos de Pygame para su uso

# Configuración de la ventana
WIDTH, HEIGHT = 600, 400        # Definen el tamaño de la ventana.
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # pygame.display.set_mode: Crea la ventana del juego
pygame.display.set_caption("Snake Game")       # Define el título de la ventana

# Colores, Cada color se define como una tupla de valores RGB.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configuración del reloj, Controla la velocidad del juego limitando los cuadros por segundo.
clock = pygame.time.Clock()

# Variables del Snake
snake_pos = [100, 50]       # Posición inicial de la cabeza de la serpiente
snake_body = [[100, 50], [90, 50], [80, 50]]    # Lista de bloques que representan el cuerpo del Snake
direction = 'RIGHT'     # Dirección actual del movimiento
change_to = direction   # Dirección próxima del movimiento.

# Variables de la comida
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]      # Posición inicial de la comida, generada aleatoriamente.
food_spawn = True       # Indica si la comida está disponible o debe generarse de nuevo.

# Puntuación, contador de puntos
score = 0

# Fuente para mostrar puntuación en pantalla
font = pygame.font.SysFont('consolas', 20)

# Función para mostrar la puntuación
def show_score():
    score_surface = font.render(f'Score: {score}', True, WHITE)     # font.render Crea un texto con la puntuación.
    score_rect = score_surface.get_rect()
    score_rect.midtop = (WIDTH // 2, 10)
    screen.blit(score_surface, score_rect)      # blit Dibuja el texto en la pantalla

# Bucle principal
while True:
    # Manejar eventos
    for event in pygame.event.get():        # Captura eventos, como cerrar la ventana o pulsar teclas.
        if event.type == pygame.QUIT:       # Sale del programa
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    # Detecta si se presiona una tecla
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Cambiar la dirección
    direction = change_to

    # Actualizar la posición del Snake según la dirección elegida.
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Crecer el Snake si come la comida
    snake_body.insert(0, list(snake_pos))       # Añade un nuevo bloque a la cabeza
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()           # Elimina el último bloque para mantener el tamaño

    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]  # random.randrange(1, (WIDTH // 10)) genera un número aleatorio entre 1 y (WIDTH // 10) - 1. WIDTH // 10 divide el ancho total de la pantalla por 10, lo que sugiere que el juego tiene una cuadrícula de 10 píxeles por celda. Al multiplicar el valor aleatorio por 10 (* 10), se obtiene una posición en la cuadrícula de píxeles del juego, asegurando que la comida aparezca en una posición múltiplo de 10.
    food_spawn = True

    # Dibujar en pantalla
    screen.fill(BLACK)      # Limpia la pantalla.
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))   # Dibuja la serpiente y la comida.
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Mostrar puntuación, Llama a la función para mostrar la puntuación.
    show_score()

    # Terminar el juego si el Snake choca, detectar colisiones
    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
        pygame.quit()
        sys.exit()
    for block in snake_body[1:]:
        if snake_pos == block:
            pygame.quit()
            sys.exit()

    # Actualizar la pantalla
    pygame.display.flip()       #  Actualiza la pantalla para mostrar los cambios.
    clock.tick(25)              # Establece la velocidad del juego (15 FPS).
