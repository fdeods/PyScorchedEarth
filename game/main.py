import pygame
import time

#set up global variables
white = (255, 255, 255)
black = (0, 0, 0)
display_width = 800
display_height = 600
FPS = 1
gameExit = False

#init game and pygame variables
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
font = pygame.font.SysFont(None, 25)
pygame.display.set_caption('ScorchedEarth')

def text_object(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(text, color):
    textSurf, textRect = text_object(text, color)
    textRect.center = (display_width / 2), (display_height / 2)
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    gameExit = False
    gameOver = False
    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("R - retry, Q-quit", black)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, [300,400,10,100])
        pygame.display.update()
        clock.tick(FPS)

gameLoop()

message_to_screen("Bye", black)
pygame.display.update()
time.sleep(2)
pygame.quit()