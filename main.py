import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# creating the game window
screen = pygame.display.set_mode((800, 600))

# Title
pygame.display.set_caption("Space Invaders")

# Icon
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
Enemies = ["monster.png", "monster1.png", "monster2.png", "monster3.png", "monster4.png"]
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 5


def respawn_coor_x():
    return random.randint(0, 730)


def respawn_coor_y(x):
    return random.randint(0, 20) - x


for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("monster1.png"))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (50, 50))
    # random enemy coordinates
    enemyX.append(respawn_coor_x())
    enemyY.append(respawn_coor_y(i * 50))
    enemyX_change.append(1.3)
    enemyY_change.append(35)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
# ready state - you cannot see bullet on screen
# fire state - bullet is currently moving
bullet_state = "ready"

# Background image
backgroundImg = pygame.image.load("background.jpg")

# Background sound
mixer.music.load('background-track.mp3')
mixer.music.play(-1)

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10

# starting level
level = 1
levelX = 700
levelY = 10
# starting time
starter_time = pygame.time.get_ticks()


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_level(x, y):
    lvl = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(lvl, (x, y))


def game_over_text():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


def level_up():
    global level
    level += 1
    show_level(levelX, levelY)


# Game loop
running = True
while running:
    # background color
    # screen.fill((0, 0, 128))

    # background image
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if key is pressed
        if event.type == pygame.KEYDOWN:
            # check if its right key or left key
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    # get the current x coordinate of spaceship
                    bulletX = playerX
                    fire(bulletX, bulletY)
        # check if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    # Boundaries
    if playerX <= 0:
        playerX = 0
    if playerX > 736:
        playerX = 736

    # check if one track completed then increase level
    if ((pygame.time.get_ticks() - starter_time)/1000) > 5:
        level_up()
        starter_time = pygame.time.get_ticks()
    for i in range(number_of_enemies):
        # enemy movement
        enemyX[i] += enemyX_change[i]
        # check if enemy and player collided
        col = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if col:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        if enemyY[i] > 480:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # enemy boundary checks
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 730:
            enemyX_change[i] = -1.3
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemy_destroy = mixer.Sound('explosion.wav')
            enemy_destroy.play()
            enemyX[i] = respawn_coor_x()
            enemyY[i] = respawn_coor_y(i * 50)
        enemy(enemyX[i], enemyY[i], i)

    # check if previous bullet is out of screen/hit
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # bullet movement
    if bullet_state is "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_level(levelX,levelY)
    pygame.display.update()
