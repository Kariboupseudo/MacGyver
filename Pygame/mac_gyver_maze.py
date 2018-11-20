"""
Game "Help MacGyver to escape !"
It's a game where you need to move MacGyver in a maze in order to get out of it.
MacGyver needs to collect 3 items to be able to beat the guardian.
Script Python
Files : mac_gyver_maze.py, classes.py, constants.py, maze.txt + 13 images
"""
import pygame
from pygame.locals import* #import pygame constants
from constants import*
from classes import*

pygame.init()

#opening a pygame window
window = pygame.display.set_mode((side_window, side_window))

"""Loading home screen image"""
home = pygame.image.load("accueil.png").convert()
"""Loading background"""
background = pygame.image.load("background.jpg").convert()

"""Main loop"""
Main = 1
while Main:

    window.blit(home, (0, 0))#displaying home screen
    pygame.display.flip() #window refreshing
    Menu = 1
    Gaming = 0
    Ending = 0
    """Home screen loop"""
    while Menu:

        start = 0 #variable to start the game
        pygame.time.Clock().tick(30)#speed limitation of the loop at 30fps
        for event in pygame.event.get(): #capture events
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                Main = 0
                Menu = 0
                Gaming = 0 #Program is shut off
            if event.type == KEYDOWN and event.key == K_RETURN:
                Menu = 0 #Home screen is shut off
                start = "maze"
                Gaming = 1

        if start != 0:
            #maze generation from a txt file
            level = Niveau(start)
            level.load_maze()
            level.display_maze(window)

            #Main character creation
            hero = Perso(level, level.items)

        while Gaming:
            """The game is played by moving the main character in a maze.
            Main character is controlled with arrow keys.
            """

            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    Main = 0
                    Menu = 0
                    Gaming = 0
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        hero.move('right')
                    elif event.key == K_LEFT:
                        hero.move('left')
                    elif event.key == K_UP:
                        hero.move('up')
                    elif event.key == K_DOWN:
                        hero.move('down')

            #Displaying new positions of the main character
            window.blit(background, (0, 0))
            level.display_maze(window)
            window.blit(hero.MG_Display, (hero.pospix_x, hero.pospix_y))
            pygame.display.flip()

            #End of game -> displaying a contextual screen
            if hero.conclusion is None:
                Main = 0
                Gaming = 1
                Menu = 0
                Ending = 0

            if hero.conclusion is not None:
                Main = 0
                Gaming = 0
                Menu = 0
                Ending = 1

            while Ending:
                if hero.conclusion:
                    window.blit(hero.end(), (30, 30))
                    pygame.display.flip()
                elif not hero.conclusion:
                    window.blit(hero.end(), (30, 30))
                    pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        Main = 0
                        Menu = 0
                        Gaming = 0
                        Ending = 0
                    elif event.type == KEYDOWN and event.key == K_RETURN:
                        """Game over screen"""
                        thanks = pygame.image.load("thanks.jpg").convert()
                        Ending = 0
                        window.blit(thanks, (30, 30))
                        pygame.display.flip()
                        