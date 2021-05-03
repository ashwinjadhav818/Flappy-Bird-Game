import random # ! For Genrating Random Numbers
import sys # ! sys.exit To Exit The Game
import pygame 
from pygame.locals import * # ! Basic PyGame Imports

# ! Global Variables For The Game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

# ! welcomeScreen Function
def welcomeScreen():
    playerx = int(SCREENWIDTH/2.2)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_width())/2.2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

# ! mainGame Function
def mainGaim():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # ? Upper Pipe List
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    # ? Lower Pipe List
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = 8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerAccY
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

    clashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
    if crashTest:
        return

    # ? Score
    playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
    for pipe in upperPipes:
        pipeMidPos = pipe['x'] + GAME_SPRITES['pipes'][0].get_width() / 2
        if pipeMidPos<= playerMidPos < pipeMidPos +4:
            score +=1
            print(f"Your score is {score}")
        GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerMinVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery + playerHeight)

        for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
            upperPipes['x'] += pipeVelX
            lowerPipes['x'] += pipeVelX

        

# ! Genrating Random Pipes
def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/2
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2* offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, # ? Upper Pipe
        {'x': pipeX, 'y': y2} # ? Lower Pipe
    ]

    return pipe

# ! Main Function
if __name__ == "__main__":
        pygame.init() # ? Initilizing PyGame Modules
        FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption("Flappy Bird Game By Ash All-Rounder") # ? Game Caption

        # ? Game Sprites
        GAME_SPRITES['numbers'] = (
            pygame.image.load('gallery/sprites/0.png').convert_alpha(),
            pygame.image.load('gallery/sprites/1.png').convert_alpha(),
            pygame.image.load('gallery/sprites/2.png').convert_alpha(),
            pygame.image.load('gallery/sprites/3.png').convert_alpha(),
            pygame.image.load('gallery/sprites/4.png').convert_alpha(),
            pygame.image.load('gallery/sprites/5.png').convert_alpha(),
            pygame.image.load('gallery/sprites/6.png').convert_alpha(),
            pygame.image.load('gallery/sprites/7.png').convert_alpha(),
            pygame.image.load('gallery/sprites/8.png').convert_alpha(),
            pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        )

        GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
        GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
        GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
        GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
        GAME_SPRITES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
            pygame.image.load(PIPE).convert_alpha()
        )

        # ? Game Sounds
        GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
        GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
        GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
        GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')

        # ? While Loop
        while True:
            welcomeScreen()
            mainGaim()