import random
import sys
import pygame
from pygame.locals import *

#global variable for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_IMAGES = {}
GAME_SOUNDS = {}
PLAYER = 'bird.png'
BACKGROUND = 'background.jpg'
PIPE = 'pipe.png'

def welcomescreen():
    
    
    
    
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_IMAGES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_IMAGES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if user wants to continue game
            
            elif event.type == KEYDOWN and (event.key == K_BACKSPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_IMAGES['background'],(0,0))
                SCREEN.blit(GAME_IMAGES['player'],(playerx,playery))
                SCREEN.blit(GAME_IMAGES['message'],(messagex,messagey))
                SCREEN.blit(GAME_IMAGES['base'],(basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    #creat 2 pipes for game 
    newpipe1 = getRandompipe()
    newpipe2 = getRandompipe()

    #list of upper pipe
    upperpipe = [
        {'x': SCREENWIDTH+200, 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[0]['y']},
    ]

    #pipe of lower pipe
    lowerpipe = [
        {'x': SCREENWIDTH + 200 , 'y': newpipe1[1]['y']} ,
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2) , 'y': newpipe2[1]['y']},
    ]


    pipevelx = -4
    playervely = -9
    playermaxvel = 10
    playerminvel = -8
    playeraccy = 1
    playerflapaccv = -8
    playerflaped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.QUIT()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervely = playerflapaccv
                    playerflaped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = isCollide(playerx, playery, upperpipe, lowerpipe)

        if crashtest:
            return

        #check for score

        playermidpos = playerx + GAME_IMAGES['player'].get_width()/2
        for pipe in upperpipe:
            pipemidpos = pipe['x'] + GAME_IMAGES['pipe'][0].get_width()/2
            if pipemidpos <= playermidpos < pipemidpos + 4:
                score += 1
                print(f"your scorew is {score}")
                GAME_SOUNDS['point'].play()

        if playervely < playermaxvel and not playerflaped:
            playervely+playeraccy

        if playerflaped:
            playerflaped = False
        playerheight = GAME_IMAGES['player'].get_height()
        playery = playery + min(playervely, GROUNDY - playery - playerheight) 
        #move pipe to the left 
        for upperpipe , lowerpipe in zip(upperpipe, lowerpipe):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx 

        #add a new pipe 
        if 0 < upperpipe[0]<5:
            newpipe = getRandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])

        #if the pipe is out of the screen remove it
        if upperpipe[0]< - GAME_IMAGES['PIPE'].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)

        #lets blit our sprits now
        SCREEN.blit(GAME_IMAGES['background'], (0,0))
        SCREEN.blit(GAME_IMAGES['base'], (basex, GROUNDY))
        for upperpipe , lowerpipe in zip(upperpipe, lowerpipe):
            SCREEN.blit(GAME_IMAGES['PIPE'][0], (upperpipe['x'], lowerpipe['y']))
            SCREEN.blit(GAME_IMAGES['PIPE'][1], (lowerpipe['x'], upperpipe['y']))
        SCREEN.blit(GAME_IMAGES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:\
            width += GAME_IMAGES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_IMAGES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_IMAGES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True


    for pipe in lowerpipes:
        if (playery +GAME_IMAGES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) <GAME_IMAGES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False
         


    
def getRandompipe():
    #generate both the pipes position
    pipeheight = GAME_IMAGES['PIPE'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_IMAGES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe= [
        {'x ': pipeX , 'y' : -y1},
        {'x' : pipeX , 'y': y2}]
     
    return


     

if __name__ == "__main__":
    pygame.init() 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('FLAPPY BIRD BY LAZYCODER')
    GAME_IMAGES['numbers'] = (pygame.image.load('0.png').convert_alpha(),
    pygame.image.load('1.png').convert_alpha(),
    pygame.image.load('2.png').convert_alpha(),
    pygame.image.load('3.png').convert_alpha(),
    pygame.image.load('4.png').convert_alpha(),
    pygame.image.load('5.png').convert_alpha(),
    pygame.image.load('6.png').convert_alpha(),
    pygame.image.load('7.png').convert_alpha(),
    pygame.image.load('8.png').convert_alpha(),
    pygame.image.load('9.png').convert_alpha(),
     )
    GAME_IMAGES ['message']= pygame.image.load('message.png').convert_alpha()
    GAME_IMAGES ['base'] = pygame.image.load('base.png').convert_alpha()
    GAME_IMAGES['background'] = pygame.image.load('background.jpg').convert()
    GAME_IMAGES["player"] = pygame.image.load('bird.png').convert_alpha()
    GAME_IMAGES ['PIPE'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    
    pygame.image.load(PIPE).convert_alpha
    )
    
    GAME_SOUNDS['DIE'] = pygame.mixer.Sound('audio\die.wav')
    GAME_SOUNDS['HIT'] = pygame.mixer.Sound('audio\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio\wing.wav')

    while True:
        welcomescreen()
        maingame()
        
        


