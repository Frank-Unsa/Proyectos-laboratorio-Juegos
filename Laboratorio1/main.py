import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_speed = []  # Lista para controlar la velocidad de los enemigos
enemyY_change = 40
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_speed.append(0.5)  # Establece la velocidad inicial aquí

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Start Menu
start_font = pygame.font.Font('freesansbold.ttf', 64)
menuX = 200
menuY = 250
menu_spacing = 60
menu_selected = 1  # Nivel de dificultad seleccionado (1, 2 o 3)


def show_start_menu():
    screen.fill((0, 0, 0))
    # Dibuja el titulo "Space Invaders"
    title_text = start_font.render("Space Invaders", True, (255, 255, 255))
    screen.blit(title_text, (200, 100))

    # Dibuja el menu de opciones
    option1_text = font.render("1. Nivel Fácil", True, (255, 255, 255))
    option2_text = font.render("2. Nivel Intermedio", True, (255, 255, 255))
    option3_text = font.render("3. Nivel Difícil", True, (255, 255, 255))
    screen.blit(option1_text, (menuX, menuY))
    screen.blit(option2_text, (menuX, menuY + menu_spacing))
    screen.blit(option3_text, (menuX, menuY + 2 * menu_spacing))

    # Indicar la opción seleccionada
    indicator_text = font.render(">", True, (255, 255, 255))
    screen.blit(indicator_text, (menuX - 30, menuY + (menu_selected - 1) * menu_spacing))

    pygame.display.update()


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Dibuja el texto y las opciones de "Game Over" en la pantalla
        game_over_text()
        restart_text = font.render("Reiniciar (R)", True, (255, 255, 255))
        exit_text = font.render("Salir (S)", True, (255, 255, 255))
        screen.blit(restart_text, (300, 350))
        screen.blit(exit_text, (300, 400))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Restart the game
            return
        elif keys[pygame.K_s]:
            pygame.quit()
            quit()
        pygame.time.Clock().tick(30)


# Función para configurar la velocidad de los enemigos según el nivel seleccionado
def set_enemy_speed(level):
    if level == 1:
        return 0.5
    elif level == 2:
        return 1.0
    elif level == 3:
        return 1.5


# Game Loop
start_menu = True
running = False
while start_menu:
    show_start_menu()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                menu_selected = min(menu_selected + 1, 3)
            elif event.key == pygame.K_UP:
                menu_selected = max(menu_selected - 1, 1)
            elif event.key == pygame.K_RETURN:
                start_menu = False
                running = True

# Configurar la velocidad de los enemigos según el nivel seleccionado
enemy_speed = set_enemy_speed(menu_selected)

# Game Loop
while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Si se presiona una tecla, verifique si es derecha o izquierda
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Obtener la coordenada x actual de la nave espacial.
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Comprobando los límites de la nave espacial para que no se salga de los límites
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_menu()
            # Restaura los valores iniciales
            playerX = 370
            playerY = 480
            score_value = 0
            for i in range(num_of_enemies):
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                enemyX_speed[i] = set_enemy_speed(menu_selected) # Usa la velocidad del nivel seleccionado.
        enemyX[i] += enemyX_speed[i] # Actualiza la posición horizontal del enemigo.
        if enemyX[i] <= 0:
            enemyX_speed[i] = set_enemy_speed(menu_selected)  # Ajusta la velocidad del enemigo aquí
            enemyY[i] += enemyY_change
        elif enemyX[i] >= 736:
            enemyX_speed[i] = -set_enemy_speed(menu_selected)  # Ajusta la velocidad del enemigo aquí
            enemyY[i] += enemyY_change
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
quit()