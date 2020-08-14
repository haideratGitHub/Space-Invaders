import pygame
import random

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
enemyImg = pygame.image.load("monster.png")
enemyImg = pygame.transform.scale(enemyImg, (60, 60))
# random enemy coordinates
enemyX = random.randint(0, 740)
enemyY = random.randint(50, 200)
enemyX_change = 1
enemyY_change = 30

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


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


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

    # enemy movement
    enemyX += enemyX_change

    # enemy boundary checks
    if enemyX <= 0:
        enemyX_change = 1
        enemyY += enemyY_change
    if enemyX > 730:
        enemyX_change = -1
        enemyY += enemyY_change

    # check if previous bullet is out of screen/hit
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # bullet movement
    if bullet_state is "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
