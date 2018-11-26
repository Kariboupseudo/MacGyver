import random
import pygame
from constants import*


class Niveau:
    """Niveau: This class build an object containing a maze in which it's possible to
    select a random position and then validate it in order to place items on a proper position."""

    def __init__(self, level):
        self.lvl = level
        self.structure = self.load_maze()
        self.items = []
        self.random_pos_items()
     
    def random_position(self):
        '''select a random position in the maze where it is possible to move'''
        open_position = []
        num_line = 0
        for line in self.structure:
            num_column = 0
            for case in line:
                if case == "-":
                    open_position.append([num_line, num_column])
                num_column += 1
            num_line += 1
        rando = random.choice(open_position)
        return rando

    def random_pos_items(self):
        """ Random positionning of items in the maze"""
        while not self.items:
            itemlist = ["A", "B", "C"]
            for i in itemlist:
                candidate_pos = self.random_position()
                if self.valid_pos(candidate_pos) is False:
                    self.items = []
                else:
                    self.items.append(Item(i, candidate_pos))
        for i in self.items:
            self.structure[i.poscase_y] = self.structure[i.poscase_y][0:i.poscase_x] \
            + i.display + self.structure[i.poscase_y][i.poscase_x+1:]
    
    def valid_pos(self, candidate_pos):
        """Check if the position of the item is not already taken by a previously created item"""
        if not self.items:
            answer = True
        else:
            answer = True
            for i, item in enumerate(self.items):
                if [candidate_pos[0], candidate_pos[1]] == [item.poscase_x, item.poscase_y]:
                    answer = False
                elif [candidate_pos[0], candidate_pos[1]] == [2, 2]:
                    answer = False
        return answer
    
    def load_maze(self):
        """Loading a maze structure from a txt file"""

        with open(self.lvl + ".txt", "r") as contenu:
            data = contenu.readlines()
        #suppressing invisible characters
        for i in range(len(data)):
            data[i] = data[i].strip()
        return data

    def display_maze(self, window):
        """Displaying a maze structure associating letters with images"""

        #Wall element
        wall = pygame.image.load("images/mur.png").convert()
        #start element
        start = pygame.image.load("images/depart.png").convert()
        #Goal element
        goal = pygame.image.load("images/Gardien.png").convert()
        #Item A
        needle = pygame.image.load("images/needle.png").convert()
        #Item B
        syringe = pygame.image.load("images/syringe.png").convert()
        #Item C
        pipe = pygame.image.load("images/pipe.png").convert()
        #Decoration element
        swiss = pygame.image.load("images/swiss.jpg").convert()
        #Phoenix Foundation Logo
        phoenix = pygame.image.load("images/phoenix.png").convert()

        """double loop to check every character of the txt file"""
        num_line = 0
        for line in self.structure:
            num_column = 0
            for sprite in line:
                pos_x = num_column * taille_sprite
                pos_y = num_line * taille_sprite
                if sprite == "W":
                    window.blit(wall, (pos_x, pos_y))
                if sprite == "D":
                    window.blit(start, (pos_x, pos_y))
                if sprite == "G":
                    window.blit(goal, (pos_x, pos_y)) 
                if sprite == "A":
                    for item in self.items:
                        if item.show is True and item.display == "A":
                            window.blit(needle, (pos_x, pos_y))
                if sprite == "1":
                    for item in self.items:
                        if item.show is True and item.display == "A":
                            window.blit(phoenix, (pos_x, pos_y))
                        if item.show is False and item.display == "A":
                            window.blit(needle, (pos_x, pos_y))
                if sprite == "B":
                    for item in self.items:
                        if item.show is True and item.display == "B":
                            window.blit(syringe, (pos_x, pos_y))
                if sprite == "2":
                    for item in self.items:
                        if item.show is True and item.display == "B":
                            window.blit(phoenix, (pos_x, pos_y))
                        if item.show is False and item.display == "B":
                            window.blit(syringe, (pos_x, pos_y))
                if sprite == "C":
                    for item in self.items:
                        if item.show is True and item.display == "C":
                            window.blit(pipe, (pos_x, pos_y))
                if sprite == "3":
                    for item in self.items:
                        if item.show is True and item.display == "C":
                            window.blit(phoenix, (pos_x, pos_y))
                        if item.show is False and item.display == "C":
                            window.blit(pipe, (pos_x, pos_y))
                if sprite == "0":
                    window.blit(swiss, (pos_x, pos_y))
                num_column += 1
            num_line += 1

class Perso:
    """Perso : builds a character with positionning values both in cases and in pixels.
    This class needs the level structure and the item list to verify each character's move."""
    def __init__(self, level, items):
        self.poscase_x = 2
        self.poscase_y = 2
        self.pospix_x = self.poscase_x * taille_sprite
        self.pospix_y = self.poscase_y * taille_sprite
        self.MG_Display = pygame.image.load("images/MacGyver.png").convert()
        self.level = level
        self.items = items
        self.ens1 = {"A", "B", "C"}
        self.ens2 = set()
        self.conclusion = None

    def move(self, way):
        """Take a move instruction and execute the move with 
        verification of his consequence on the game"""
        if way == "right":
            if self.poscase_x < (nb_sprite_cote - 2):
                #Checking if landing position is already occupied by an item
                for i in self.items:
                    if self.level.structure[self.poscase_y][self.poscase_x+1] \
                    == i.display and i.show is True:
                        i.show = False 
                        self.ens2.add(i.display) #Item is added in Character's inventory
                        self.poscase_x += 1
                        #Calculation of the character's new position in pixels
                        self.pospix_x = self.poscase_x * taille_sprite
                #Checking if landing position is the guardian/exit position 
                if self.level.structure[self.poscase_y][self.poscase_x+1] == 'G':
                    self.end() #Checking if character's has 3 items in his inventory                     
                #Checking if landing position is a wall
                if self.level.structure[self.poscase_y][self.poscase_x+1] != 'W':
                    self.poscase_x += 1
                    self.pospix_x = self.poscase_x * taille_sprite                  

                                  
        if way == "left":
            if self.poscase_x > 0:
                for i in self.items:
                    if self.level.structure[self.poscase_y][self.poscase_x-1] == i.display and i.show is True:
                        i.show = False
                        self.ens2.add(i.display)
                        self.poscase_x -= 1
                        self.pospix_x = self.poscase_x * taille_sprite
                if self.level.structure[self.poscase_y][self.poscase_x-1] == 'G':
                    self.end()
                if self.level.structure[self.poscase_y][self.poscase_x-1] != 'W':
                    self.poscase_x -= 1
                    self.pospix_x = self.poscase_x * taille_sprite
         
        if way == "up":
            if self.poscase_y > 0:
                for i in self.items:
                    if self.level.structure[self.poscase_y-1][self.poscase_x] == i.display and i.show is True:
                        i.show = False
                        self.ens2.add(i.display)
                        self.poscase_y -= 1
                        self.pospix_y = self.poscase_y * taille_sprite
                if self.level.structure[self.poscase_y-1][self.poscase_x] == 'G':
                    self.end()
                if self.level.structure[self.poscase_y-1][self.poscase_x] != 'W':
                    self.poscase_y -= 1
                    self.pospix_y = self.poscase_y * taille_sprite
 
            
        if way == "down":
            if self.poscase_y < (nb_sprite_cote - 2):
                for i in self.items:
                    if self.level.structure[self.poscase_y+1][self.poscase_x] ==\
                    i.display and i.show is True:
                        i.show = False
                        self.ens2.add(i.display)
                        self.poscase_y += 1
                        self.pospix_y = self.poscase_y * taille_sprite
                if self.level.structure[self.poscase_y+1][self.poscase_x] == 'G':
                    self.end()       
                if self.level.structure[self.poscase_y+1][self.poscase_x] != 'W':
                    self.poscase_y += 1
                    self.pospix_y = self.poscase_y * taille_sprite

    def end(self):
        '''checking if the victory conditions are met by the character 
        and return of a contextual image'''
    
        """victory screen"""
        victory = pygame.image.load("images/victory.jpg").convert()
        """lose screen"""
        lose = pygame.image.load("images/lose.jpg").convert()
        if len(self.ens2) == len(self.ens1):
            self.conclusion = True
            temp = victory
        else:
            self.conclusion = False
            temp = lose
        return temp

class Item:
    '''build an item object with positionning values both in cases and pixels
        a display status and a show status with boolean value to switch
        if the item has been collected.'''
    def __init__(self, display, position):
        self.poscase_x = position[0]
        self.poscase_y = position[1]
        self.pospix_x = self.poscase_x * taille_sprite
        self.pospix_y = self.poscase_y * taille_sprite
        self.display = display
        self.show = True
