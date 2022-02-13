import pygame
import random
import math
import sys
from pygame import mixer

pygame.init()  # required for pygame to run

dis_width = 1000
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))  # width*height, rmb to add extra pair of paranthesis

background = pygame.image.load("sky.jpg")

# sound stuff
gunshot_sound = mixer.Sound("gun-gunshot-01.wav")  # capital Sound for short sounds
explosion_sound = mixer.Sound("explosion.wav")

# mixer.music.load("bassbg.wav")  #for long sounds like background music
# mixer.music.play(-1)  #to infinitely loop the backg music

pygame.display.set_caption("Arial combat")  # title of window
icon = pygame.image.load("fighter_icon.png")  # title icon
pygame.display.set_icon(icon)  # set as icon

player_icon = pygame.image.load("player_icon.png")
player_x_pos = 465
player_y_pos = 500
player_x_pos_change = 0
player_y_pos_change = 0

enemy_icon = pygame.image.load("enemy.png")
enemy_x_pos = random.randint(0, 1000 - 32)
enemy_y_pos = 50
enemy_x_pos_change = random.choice([-0.2, 0.2])
enemy_y_pos_change = 0.1
enemy_right = 0.2
enemy_left = -0.2

missle_icon = pygame.image.load("missle.png")
missle_x_pos = enemy_x_pos
missle_y_pos = enemy_y_pos + 64
missle_y_pos_change = 1

bullet_icon = pygame.image.load("bullet.png")
bullet_x_pos = player_x_pos
bullet_y_pos = player_y_pos
bullet_y_pos_change = 0
bullet_state = "ready"  # or fire

score = 0
health = 3
downed_planes = 0
missed_shots = 0

font = pygame.font.Font("freesansbold.ttf", 32)
text_x_pos = 10
text_y_pos = 10

print('''
Hello, welcome to JS's first pygame game

You score 1 point for every plane you shoot down but lose 1 point for every shot you miss
You have a total of 3 health

WASD or arrow keys to control the plane
Space to shoot

Good luck!
''')


def show_score(x, y):
    score_val = font.render(f"Score: {score}", True, (0, 0, 0))
    dis.blit(score_val, (x, y))


def player(x, y):
    dis.blit(player_icon, (x, y))  # drawing the player icon on the blit(grid)


def enemy(x, y):
    dis.blit(enemy_icon, (x, y))


def missle(x, y):
    dis.blit(missle_icon, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    dis.blit(bullet_icon, (x + 24, y - 10))


def is_enemy_collision(enemy_x_pos, enemy_y_pos, bullet_x_pos, bullet_y_pos):
    distance = math.sqrt((enemy_x_pos - bullet_x_pos) ** 2 + (enemy_y_pos - bullet_y_pos) ** 2)
    if distance < 45:
        return True


def is_player_collision(player_x_pos, player_y_pos, missle_x_pos, missle_y_pos):
    distance = math.sqrt((player_x_pos - missle_x_pos) ** 2 + (player_y_pos - missle_y_pos) ** 2)
    if distance < 45:
        return True


def is_player_enemy_collision(player_x_pos, player_y_pos, enemy_x_pos, enemy_y_pos):
    distance = math.sqrt((player_x_pos - enemy_x_pos) ** 2 + (player_y_pos - enemy_y_pos) ** 2)
    if distance < 45:
        return True


# game loop
running = True  # game running
while health != 0 and running:

    dis.fill((50, 50, 100))  # fill colour of the screen
    dis.blit(background, (0, 0))
    if bullet_state == "ready":
        bullet_x_pos = player_x_pos
        bullet_y_pos = player_y_pos
    for event in pygame.event.get():  # get all events in pygame
        if event.type == pygame.QUIT:  # if close button is pressed
            running = False
        if event.type == pygame.KEYDOWN:  # if any key is pressed down on computer
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # if the key is left arrow or A
                # print("Left input has been sent.")
                player_x_pos_change = -0.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # if the key is right arrow or D
                # print("Right input has been sent.")
                player_x_pos_change = 0.5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                # print("Up input has been sent")
                player_y_pos_change = -0.5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # print("Down input has been sent")
                player_y_pos_change = 0.25
            if event.key == pygame.K_SPACE:
                fire_bullet(bullet_x_pos, bullet_y_pos)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # if the left/right input is removed
                # print("Sideways(left/right) input has been stopped")
                player_x_pos_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # print("Up/down input has been stopped")
                player_y_pos_change = 0
    player_x_pos += player_x_pos_change
    if player_x_pos > 1000 - 64:
        # print("Relocating plane..")
        player_x_pos = 1000 - 64  # 1000 is the limit and 64 is the pixel size of the player icon
    elif player_x_pos < 0:
        # print("Relocating plane..")
        player_x_pos = 0
    player_y_pos += player_y_pos_change
    if player_y_pos > 600 - 64:
        # print("Relocating plane..")
        player_y_pos = 600 - 64
    elif player_y_pos < 300:
        # print("Relocating plane..")
        player_y_pos = 300

    enemy_x_pos += enemy_x_pos_change
    enemy_y_pos += enemy_y_pos_change
    if enemy_x_pos > 1000 - 64:
        # print("changing enemy movement direction..")
        enemy_x_pos_change = enemy_left
    elif enemy_x_pos < 0:
        # print("changing enemy movement direction..")
        enemy_x_pos_change = enemy_right
    if enemy_y_pos > 350:
        enemy_y_pos_change = -(enemy_y_pos_change)
    elif enemy_y_pos < 0:
        enemy_y_pos_change = -(enemy_y_pos_change)

    missle_y_pos += missle_y_pos_change

    player(player_x_pos, player_y_pos)
    enemy(enemy_x_pos, enemy_y_pos)
    missle(missle_x_pos, missle_y_pos)

    if bullet_state == "fire":
        fire_bullet(bullet_x_pos, bullet_y_pos)
        gunshot_sound.play()  # play sound for gunshot
        bullet_y_pos_change = -1
        bullet_y_pos += bullet_y_pos_change
        if bullet_y_pos < 0:
            bullet_y_pos = player_y_pos
            bullet_x_pos = player_x_pos
            bullet_y_pos_change = 0
            bullet_state = "ready"
            score -= 1
            missed_shots += 1

    if missle_y_pos > 600:
        missle_x_pos = enemy_x_pos + 23
        missle_y_pos = enemy_y_pos + 50

    # collision
    enemy_collision = is_enemy_collision(enemy_x_pos, enemy_y_pos, bullet_x_pos, bullet_y_pos)
    if enemy_collision == True:
        # print("you shot down an enemy!")
        explosion_sound.play()  # play explosion sound // probably not working because gunshot sound is too long?
        score += 1
        bullet_y_pos = player_y_pos
        bullet_state = "ready"
        enemy_x_pos = random.randint(0, 1000 - 32)
        enemy_y_pos = 50
        enemy_x_pos_change += 0.1
        enemy_right += 0.1
        enemy_left -= 0.1
        downed_planes += 1

    player_collision = is_player_collision(player_x_pos, player_y_pos, missle_x_pos, missle_y_pos)
    if player_collision == True:
        # print("you got shot!")
        health -= 1
        missle_y_pos = enemy_y_pos
        missle_x_pos = enemy_x_pos
        player_x_pos = 465
        player_y_pos = 500

    player_enemy_collision = is_player_enemy_collision(player_x_pos, player_y_pos, enemy_x_pos, enemy_y_pos)
    if player_enemy_collision == True:
        # print("planes collided!")
        health -= 1
        player_x_pos = 465
        player_y_pos = 500
        enemy_x_pos = random.randint(0, 1000 - 32)
        enemy_y_pos = 50
        downed_planes += 1

    show_score(text_x_pos, text_y_pos)
    pygame.display.update()  # update because player will be moving around, gotta update display
print(f'''
You scored {score} points,
shooting down {downed_planes} planes and,
missing {missed_shots} shots

Thanks for playing!
''')

player_x_pos = 10000
player_y_pos = 10000
enemy_x_pos = 10000
enemy_y_pos = 10000
