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

# assests directory
DIR_IMG = "./assests/img/"
DIR_SOUND = "./assests/sounds/"

# Icon
icon = pygame.image.load(DIR_IMG + "rocket.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(DIR_IMG + "player.png")
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 5
ENEMY_MOVEMENT_X = 1.3

# enemy fire ball
fireImg = []
fireX = []
fireY = []
fireX_change = []
fireY_change = []
fire_state = []
FIRE_MOVEMENT_X = 0
FIRE_MOVEMENT_Y = 3
number_of_fires = 1  # these will increase as level goes up
time_interval_between_fires = 3  # this will decrease as level goes up
starting_time_for_fire = pygame.time.get_ticks()


# enemy respawning random coordinates
def respawn_coor_x():
    return random.randint(0, 730)


def respawn_coor_y(x):
    return random.randint(0, 20) - x


for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load(DIR_IMG + "monster1.png"))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (50, 50))
    fireImg.append(pygame.image.load(DIR_IMG + "enemy_fire.png"))
    fireImg[i] = pygame.transform.scale(fireImg[i], (24, 24))
    # random enemy coordinates
    x = respawn_coor_x()
    y = respawn_coor_y(i * 50)
    enemyX.append(x)
    enemyY.append(y)
    fireX.append(x)
    fireY.append(y)
    enemyX_change.append(ENEMY_MOVEMENT_X)
    enemyY_change.append(35)
    fireX_change.append(FIRE_MOVEMENT_X)
    fireY_change.append(FIRE_MOVEMENT_Y)
    fire_state.append("ready")

# Bullet
bulletImg = pygame.image.load(DIR_IMG + "bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
# ready state - you cannot see bullet on screen
# fire state - bullet is currently moving
bullet_state = "ready"

# Background image
backgroundImg = pygame.image.load(DIR_IMG + "background.jpg")

# Background sound
mixer.music.load(DIR_SOUND+'background-track.mp3')
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


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def fire_by_enemy(x, y):
    screen.blit(fireImg[0], (x + 14, y + 17))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


def level_up():
    global level
    global number_of_fires
    global time_interval_between_fires
    global ENEMY_MOVEMENT_X
    ENEMY_MOVEMENT_X += 0.2
    time_interval_between_fires -= 1
    number_of_fires += 1
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
                    bullet_sound = mixer.Sound(DIR_SOUND+'shoot.wav')
                    bullet_sound.play()
                    # get the current x coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
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
    if ((pygame.time.get_ticks() - starter_time) / 1000) > 61:
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
            enemyX_change[i] = ENEMY_MOVEMENT_X
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 730:
            enemyX_change[i] = -ENEMY_MOVEMENT_X
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemy_destroy = mixer.Sound(DIR_SOUND+'explosion.wav')
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
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if ((pygame.time.get_ticks() - starting_time_for_fire) / 1000) > time_interval_between_fires:
        starting_time_for_fire = pygame.time.get_ticks()
        for i in range(number_of_fires):
            # which enemy will fire
            which_enemy_fire = random.randint(0, 4)
            if fire_state[which_enemy_fire] is "ready" and enemyY[which_enemy_fire] > 0:
                fireX[which_enemy_fire] = enemyX[which_enemy_fire]
                fireY[which_enemy_fire] = enemyY[which_enemy_fire]
                fire_by_enemy(fireX[which_enemy_fire], fireY[which_enemy_fire])
                fire_state[which_enemy_fire] = "fire"

    for i in range(number_of_enemies):
        if fire_state[i] is "fire" and enemyY[i] > 0:
            fire_by_enemy(fireX[i], fireY[i])
            fireY[i] += fireY_change[i]
            hit_player = isCollision(playerX, playerY, fireX[i], fireY[i])
            if hit_player:
                fireY[i] = 2000
                player_killed = mixer.Sound(DIR_SOUND+"invaderkilled.wav")
                player_killed.play()
                for j in range(number_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break
        if fireY[i] > 800:
            fire_state[i] = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    show_level(levelX, levelY)
    pygame.display.update()
