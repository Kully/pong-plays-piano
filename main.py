import pygame

import random
import time


pygame.init()

x_res = 880
y_res = 480
title = 'pong-plays-piano'

pygame.display.set_caption(title)
gameDisplay = pygame.display.set_mode((x_res, y_res))
clock = pygame.time.Clock()


def get_random_color():
    r = random.choice(range(100, 256))
    g = random.choice(range(100, 256))
    b = random.choice(range(100, 256))
    return [r, g, b]

def reset_ball():
    ball["x"] = x_res / 2
    ball["y"] = y_res / 2
    ball["y_velocity"] = 0
    ball["x_velocity"] = 8

black = (0, 0, 0)
white = (255, 255, 255)
palette_speed = 10
init_possible_ball_y_velocities = [2,2,3,3]
ball_y_possible_velocities = init_possible_ball_y_velocities

ball_Img = pygame.Surface((16, 16))
pattle1_Img = pygame.Surface((16, 100))
pattle2_Img = pygame.Surface((16, 100))

# color sprites
ball_Img.fill(white)
pattle1_Img.fill(white)
pattle2_Img.fill(white)

ball = {
    "width": ball_Img.get_width(),
    "height": ball_Img.get_height(),
    "x": x_res / 2,
    "y": y_res / 2,
    "x_velocity": 8,
    "max_x_speed": 25,
    "y_velocity": 0,
}
pattle1 = {
    "width": pattle1_Img.get_width(),
    "height": pattle1_Img.get_height(),
    "x": 0,
    "y": y_res / 2 - (pattle1_Img.get_height() / 2),
    "upKey": ord("q"),
    "downKey": ord("a"),
    "upKeyHeld": 0,
    "downKeyHeld": 0,
}
pattle2 = {
    "width": pattle2_Img.get_width(),
    "height": pattle2_Img.get_height(),
    "x": x_res - pattle2_Img.get_width(),
    "y": y_res / 2 - (pattle2_Img.get_height() / 2),
    "upKey": ord("p"),
    "downKey": ord("l"),
    "upKeyHeld": 0,
    "downKeyHeld": 0,
}



pygame.mixer.init()
musicChannel = pygame.mixer.Channel(0)

nul = pygame.mixer.Sound('wav/nul.wav')
E3  = pygame.mixer.Sound('wav/E3.wav')
F3  = pygame.mixer.Sound('wav/F3.wav')
Gb3 = pygame.mixer.Sound('wav/Gb3.wav')
G3  = pygame.mixer.Sound('wav/G3.wav')
Ab3 = pygame.mixer.Sound('wav/Ab3.wav')
A3  = pygame.mixer.Sound('wav/A3.wav')
Bb3 = pygame.mixer.Sound('wav/Bb3.wav')
B3  = pygame.mixer.Sound('wav/B3.wav')
C4  = pygame.mixer.Sound('wav/C4.wav')
Db4 = pygame.mixer.Sound('wav/Db4.wav')
D4  = pygame.mixer.Sound('wav/D4.wav')
Eb4 = pygame.mixer.Sound('wav/Eb4.wav')
E4  = pygame.mixer.Sound('wav/E4.wav')
F4  = pygame.mixer.Sound('wav/F4.wav')
Gb4 = pygame.mixer.Sound('wav/Gb4.wav')
G4  = pygame.mixer.Sound('wav/G4.wav')
Ab4 = pygame.mixer.Sound('wav/Ab4.wav')
A4  = pygame.mixer.Sound('wav/A4.wav')

tetris_part_a = [
    E4,  nul, B3,  C4,  D4,  nul, C4,  B3,
    A3,  nul, A3,  C4,  E4,  nul, D4,  C4,
    B3,  nul, nul, C4,  D4,  nul, E4,  nul,
    C4,  nul, A3,  nul, A3,  nul, nul, nul,
    nul, D4,  nul, F4,  A4,  nul, G4,  F4,
    E4,  nul, nul, C4,  E4,  nul, D4,  C4,
    B3,  B3,  B3,  C4,  D4,  nul, E4,  nul,
    C4,  nul, A3,  nul, A3,  nul, nul, nul,
]

tetris_part_b = [
    E4,  nul, nul, nul, C4,  nul, nul, nul,
    D4,  nul, nul, nul, B3,  nul, nul, nul,
    C4,  nul, nul, nul, A3,  nul, nul, nul,
    Ab3, nul, nul, nul, B3,  nul, nul, nul,

    E4,  nul, nul, nul, C4,  nul, nul, nul,
    D4,  nul, nul, nul, B3,  nul, nul, nul,
    C4,  nul, E4,  nul, A4,  nul, nul, nul,
    Ab4, nul, nul, nul, nul, nul, nul, nul,
]
notes_array = tetris_part_a + tetris_part_b
notes_array = [
    A3, Db4, E4, A4, Ab4, E4, D4, B3,
]

done = False
music_index = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_ball()
                music_index = 0
                ball_y_possible_velocities = init_possible_ball_y_velocities

            # pattle1
            if event.key == pattle1["downKey"]:
                pattle1["downKeyHeld"] = 1
            if event.key == pattle1["upKey"]:
                pattle1["upKeyHeld"] = 1
            # pattle2
            if event.key == pattle2["downKey"]:
                pattle2["downKeyHeld"] = 1
            elif event.key == pattle2["upKey"]:
                pattle2["upKeyHeld"] = 1

        if event.type == pygame.KEYUP:
            # pattle1
            if event.key == pattle1["downKey"]:
                pattle1["downKeyHeld"] = 0
            elif event.key == pattle1["upKey"]:
                pattle1["upKeyHeld"] = 0
            # pattle2
            if event.key == pattle2["downKey"]:
                pattle2["downKeyHeld"] = 0
            elif event.key == pattle2["upKey"]:
                pattle2["upKeyHeld"] = 0

    # ball hits top or bottom wall
    if ball["y"] <= 0 or (ball["y"] + ball_Img.get_height() >= y_res):
        ball["y_velocity"] = -1 * ball["y_velocity"]

    # ball enters a player's goal
    if (ball["x"] >= x_res + ball["width"]) or (ball["x"] <= -ball["width"]):
        reset_ball()
        music_index = 0
        ball_y_possible_velocities = init_possible_ball_y_velocities

    ball_hits_pattle1 = (
        ball["x"] <= pattle1["x"] + pattle1["width"] and
        (ball["y"] + ball["height"] >= pattle1["y"]) and
        (ball["y"] <= pattle1["height"] + pattle1["y"])
    )
    ball_hits_pattle2 = (
        ball["x"] + ball["width"] >= pattle2["x"] and
        (ball["y"] + ball["height"] >= pattle2["y"]) and
        (ball["y"] <= pattle2["height"] + pattle2["y"])
    )

    if ball_hits_pattle1 or ball_hits_pattle2:
        if music_index == 0:
            # random color
            ball_Img.fill(get_random_color())
            pattle1_Img.fill(get_random_color())
            pattle2_Img.fill(get_random_color())

            # add a different angle for ball to fly in after hit
            max_velocity = max(ball_y_possible_velocities)
            ball_y_possible_velocities.append(max_velocity + 1)

            # increment x velocity of ball
            if abs(ball["x_velocity"]) < ball["max_x_speed"]:
                if ball["x_velocity"] < 0:
                    ball["x_velocity"] -= 1
                else:
                    ball["x_velocity"] += 1

        # update ball velocity
        ball["x_velocity"] = -1 * ball["x_velocity"]
        ball["y_velocity"] = random.choice(ball_y_possible_velocities)

        musicChannel.play(notes_array[music_index])
        music_index += 1

        # play next note in song        
        if music_index >= len(notes_array):
            music_index = 0

    pattle1_y_direction = (pattle1["downKeyHeld"] - pattle1["upKeyHeld"])
    pattle2_y_direction = (pattle2["downKeyHeld"] - pattle2["upKeyHeld"])

    # move ball and pattles
    ball["y"] += ball["y_velocity"]
    ball["x"] += ball["x_velocity"]

    pattle1["y"] += pattle1_y_direction * palette_speed
    pattle2["y"] += pattle2_y_direction * palette_speed

    # pattle1 boundaries
    if (pattle1["y"] < 0):
        pattle1["y"] = 0
    if (pattle1["y"] + pattle1["height"] > y_res):
        pattle1["y"] = y_res - pattle1["height"] - 4

    # pattle2 boundaries
    if (pattle2["y"] < 0):
        pattle2["y"] = 0
    if (pattle2["y"] + pattle2["height"] > y_res):
        pattle2["y"] = y_res - pattle2["height"] - 4

    # draw to screen
    gameDisplay.fill(black)
    gameDisplay.blit(ball_Img, (ball["x"], ball["y"]))
    gameDisplay.blit(pattle1_Img, (pattle1["x"], pattle1["y"]))
    gameDisplay.blit(pattle2_Img, (pattle2["x"], pattle2["y"]))

    pygame.display.update()
    clock.tick(60)
pygame.quit()
