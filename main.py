import pygame
import random


pygame.init()

x_res = 880
y_res = 480
title = 'pong-plays-piano'

pygame.display.set_caption(title)
gameDisplay = pygame.display.set_mode((x_res, y_res))
clock = pygame.time.Clock()

pygame.mixer.init()
music_ch_0 = pygame.mixer.Channel(0)

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
#   ***, ***, ***, ***, ***, ***, ***, ***,
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
tetris_music_array = tetris_part_a + tetris_part_b


PROBABILITY_OF_RANDOM_COLOR = 0.001
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)

P1_DOWN = False
P1_UP = False
P2_DOWN = False
P2_UP = False

pattle_speed = 10
PATTLE_PX_FROM_SIDES = 0

resetKey = pygame.K_SPACE

def flip_sign(number):
    return -1 * number

def get_random_color():
    r = random.choice(range(100, 256))
    g = random.choice(range(100, 256))
    b = random.choice(range(100, 256))
    return [r, g, b]


# load images
ball_Img = pygame.Surface((16, 16))
ball_Img.fill(WHITE)

pattle1_Img = pygame.Surface((16, 100))
pattle1_Img.fill(WHITE)

pattle2_Img = pygame.Surface((16, 100))
pattle2_Img.fill(WHITE)

ball = {
    "width": ball_Img.get_width(),
    "height": ball_Img.get_height(),
    "x": x_res / 2,
    "y": y_res / 2,
    "x_speed": 10,
    "y_speed": 0,
}
pattle1 = {
    "x": PATTLE_PX_FROM_SIDES,
    "y": y_res / 2 - (pattle1_Img.get_height() / 2),
    "moveUpKey": ord("q"),
    "moveDownKey": ord("a"),
    "height": pattle1_Img.get_height(),
    "upKeyHeld": 0,
    "downKeyHeld": 0,
}
pattle2 = {
    "x": x_res - PATTLE_PX_FROM_SIDES - pattle2_Img.get_width(),
    "y": y_res / 2 - (pattle2_Img.get_height() / 2),
    "moveUpKey": ord("p"),
    "moveDownKey": ord("l"),
    "height": pattle2_Img.get_height(),
    "upKeyHeld": 0,
    "downKeyHeld": 0,
}



P1_DOWN = False
P1_UP = False
P2_DOWN = False
P2_UP = False

done = False
music_index = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            # player 1
            if event.key == pattle1["moveDownKey"]:
                P1_DOWN = True
            elif event.key == pattle1["moveUpKey"]:
                P1_UP = True

            # player 2
            if event.key == pattle2["moveDownKey"]:
                P1_DOWN = True
            elif event.key == pattle2["moveUpKey"]:
                P2_UP = True

            # reset spacebar
            if event.key == resetKey:
                ball["x"] = x_res / 2
                ball["y"] = y_res / 2
                ball["x_speed"] = 2
                ball["y_speed"] = 2

        if event.type == pygame.KEYUP:
            # player 1
            if event.key == pattle1["moveDownKey"]:
                P1_DOWN = False
            elif event.key == pattle1["moveUpKey"]:
                P1_UP = False

            # player 2
            if event.key == pattle2["moveDownKey"]:
                P2_DOWN = False
            elif event.key == pattle2["moveUpKey"]:
                P2_UP = False

        if P1_DOWN and not P1_UP:
            P1_CHANGE = pattle_speed
        elif not P1_DOWN and P1_UP:
            P1_CHANGE = -pattle_speed
        elif (not P1_DOWN and not P1_UP) or (P1_DOWN and P1_UP):
            P1_CHANGE = 0

        if P2_DOWN and not P2_UP:
            P2_CHANGE = pattle_speed
        elif not P2_DOWN and P2_UP:
            P2_CHANGE = -pattle_speed
        elif (not P2_DOWN and not P2_UP) or (P2_DOWN and P2_UP):
            P2_CHANGE = 0

    # boundaries
    if ball["y"] <= 0 or (ball["y"] + ball_Img.get_height() >= y_res):
        ball["y_speed"] = flip_sign(ball["y_speed"])

    # ball out of bounds
    if ball["x"] >= x_res + ball_Img.get_width() or ball["x"] <= -ball_Img.get_width():
        ball["x"] = x_res / 2
        ball["y"] = y_res / 2
        ball_x_init_speed = 8
        ball["y_speed"] = 2
        music_index = 0

    # pattle1
    if (P1_UP and pattle1["y"] <= 0) or (P1_DOWN and (pattle1["y"] + pattle1_Img.get_height() >= y_res)):
        P1_CHANGE = 0

    # pattle2
    if (P2_UP and pattle2["y"] <= 0) or (P2_DOWN and (pattle2["y"] + pattle2_Img.get_height() >= y_res)):
        P2_CHANGE = 0

    # ball hits pattle
    ball_hits_pattle2 = (
        ball["x"] + ball_Img.get_width() >= pattle2["x"] and (ball["y"] + ball_Img.get_height() >= pattle2["y"]) and (ball["y"] <= pattle2_Img.get_height() + pattle2["y"])
    )

    ball_hits_pattle1 = (
        ball["x"] <= pattle1["x"] + pattle1_Img.get_width() and (ball["y"] + ball_Img.get_height() >= pattle1["y"]) and (ball["y"] <= pattle1_Img.get_height() + pattle1["y"])
    )

    if ball_hits_pattle1 or ball_hits_pattle2:
        ball["x_speed"] = ball["x_speed"] * -1

        if music_index >= len(tetris_music_array) - 1:
            music_index = 0
        music_ch_0.play(tetris_music_array[music_index])
        music_index += 1

    # move ball and pattles
    ball["y"] += ball["y_speed"]
    ball["x"] += ball["x_speed"]

    pattle1["y"] += P1_CHANGE
    pattle2["y"] += P2_CHANGE

    # randomly color stuff
    if random.random() < PROBABILITY_OF_RANDOM_COLOR:
        random_color = get_random_color()

        ball_Img.fill(random_color)
        pattle1_Img.fill(random_color)
        pattle2_Img.fill(random_color)

    gameDisplay.fill(BLACK)
    gameDisplay.blit(ball_Img, (ball["x"], ball["y"]))
    gameDisplay.blit(pattle1_Img, (pattle1["x"], pattle1["y"]))
    gameDisplay.blit(pattle2_Img, (pattle2["x"], pattle2["y"]))

    pygame.display.update()
    clock.tick(60)
pygame.quit()
