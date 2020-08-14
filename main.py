import pygame

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

# Background image
backgroundImg = pygame.image.load("background.jpg")


def player(x,y):
    screen.blit(playerImg, (x, y))


# Game loop
running = True
while running:
    # background color
    screen.fill((0, 0, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if key is pressed
        if event.type == pygame.KEYDOWN:
            # check if its right key or left key
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
        # check if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Boundaries
    if playerX <= 0:
        playerX = 0
    if playerX > 736:
        playerX = 736

    player(playerX, playerY)
    pygame.display.update()
