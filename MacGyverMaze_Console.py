import os
import random

class Laby:
    
    def __init__(self):
        self.id_perso = "M"
        self.lvl = self.charge_labyrinthe(input('Saisir nom du fichier contenant le labyrinthe:'))
        self.macgyver = Character([1, 1])
        self.lvl[self.macgyver.pos_y] = self.lvl[self.macgyver.pos_y][0:self.macgyver.pos_x] +\
                self.id_perso + self.lvl[self.macgyver.pos_y][self.macgyver.pos_x+1:]
        self.items = []
        self.print_pos_m()
        self.random_pos_items()

    def print_pos_m(self):#Function aimed at debugging program's behaviour
        print(self.macgyver.pos_x, self.macgyver.pos_y)
        print("Objets collectés : " + str(self.macgyver.ens2))
        for item in self.items:
            print(item.display, item.pos_x, item.pos_y)

    def random_pos_items(self):
        """ Random position of items """
        while not self.items:
            itemlist = ["A","B","C"]
            for item in itemlist:
                CandidatePos = self.random_position()
                if self.valid_pos(CandidatePos) is False:
                    self.items = []
                else:
                    self.items.append(Item(item, CandidatePos))
        for item in self.items:
            self.lvl[item.pos_y] = self.lvl[item.pos_y][0:item.pos_x] + item.display + self.lvl[item.pos_y][item.pos_x+1:]

    def charge_labyrinthe(self, lvl):
        """
        load the maze from a txt file 
        """
        try:
            with open(lvl + ".txt","r") as contenu:
                data = contenu.readlines()
            #suppression caractères invisibles
            for i in range(len(data)):
                data[i] = data[i].strip()
            return(data)
        except FileNotFoundError:
            print("Couldn't open map file \"" + lvl + "\"")
            exit()
            
    """Check if the position of the item is not already taken by a previously created item"""
    def valid_pos(self, CandidatePos):
        if not self.items:
            return True
        else:
            reponse = True
            for i, item in enumerate(self.items):
                if [CandidatePos[0], CandidatePos[1]] == [item.pos_x, item.pos_y]:
                    reponse = False
                elif [CandidatePos[0], CandidatePos[1]] == [self.macgyver.pos_x,self.macgyver.pos_y]:
                    reponse = False
            return reponse
                
    def affiche_labyrinthe(self):
        for ligne in self.lvl:
            print(ligne)

    def verification_deplacement(self, pos_col, pos_ligne):
        '''check if move is located inside the maze and
        positionned on a valid place
        '''
        #maze size
        n_cols = len(self.lvl[0])
        n_lignes = len(self.lvl)
        self.collect_items()
        if pos_ligne < 0 or pos_col < 0 or pos_ligne > n_lignes - 1 or pos_col > n_cols -1:
            return None
        elif self.lvl[pos_ligne][pos_col] == "G":
            return [-1,-1] #outside maze position means victory
        elif self.lvl[pos_ligne][pos_col] not in ["-", "A", "B", "C"]:
            return None
        else:
            return [pos_col, pos_ligne]

    def random_position(self):
        OpenPosition = []
        num_line = 0
        for line in self.lvl:
            num_column = 0
            for case in line:
                if case == "-":
                    OpenPosition.append([num_line, num_column])
                num_column += 1
            num_line += 1
        #print("Openposition " + str(OpenPosition))
        rando = random.choice(OpenPosition)
        #print(rando)
        return rando


    def collect_items(self):
        """Collect items found"""
        for item in self.items:
            if (item.pos_x == self.macgyver.pos_x and
                item.pos_y == self.macgyver.pos_y and
                    item.show is True):
                item.show = False
                self.macgyver.ens2.add(item.display)

    def jeu(self):
        """
        Display maze after the player's move
           
        """
        while True :
            self.choix_joueur()
            self.affiche_labyrinthe()
            #self.print_pos_m()#Uncomment this to debug 
            #Si en dehors du labyrinthe
            if [self.macgyver.pos_x, self.macgyver.pos_y] == [-1,-1] and len(self.macgyver.ens2) == len(self.macgyver.ens1):
                print("Vous avez gagné !")
            elif [self.macgyver.pos_x, self.macgyver.pos_y] == [-1,-1] and len(self.macgyver.ens2) != len(self.macgyver.ens1):
                print("Vous êtes mort !")

    def choix_joueur(self):
        """ Player's input for move is validated.
            If so player's position is modified,
            it's possible to quit game and a message
            is displayed if the move can't happen.
        """
        choix = input("Votre déplacement (Haut/Bas/Droite/Gauche/Quitter) ?")
        if choix == "H" or choix == "Haut":
            dep = self.verification_deplacement(self.macgyver.pos_x, self.macgyver.pos_y -1)
        elif choix == "B" or choix == "Bas":
            dep = self.verification_deplacement(self.macgyver.pos_x, self.macgyver.pos_y +1)
        elif choix == "G" or choix == "Gauche":
            dep = self.verification_deplacement(self.macgyver.pos_x-1, self.macgyver.pos_y)
        elif choix == "D" or choix == "Droite":
            dep = self.verification_deplacement(self.macgyver.pos_x+1, self.macgyver.pos_y)
        elif choix == "Q" or choix == "Quitter":
            os._exit(1)
        else:
            dep = None

        if dep == None:
            print("Déplacement impossible")
        else:
            self.macgyver.former_pos_x = self.macgyver.pos_x
            self.macgyver.former_pos_y = self.macgyver.pos_y
            self.macgyver.pos_x = dep[0] #modification de position du personnage
            self.macgyver.pos_y = dep[1]
            self.lvl[self.macgyver.former_pos_y] = self.lvl[self.macgyver.former_pos_y][0:self.macgyver.former_pos_x] +\
                "-" + self.lvl[self.macgyver.former_pos_y][self.macgyver.former_pos_x+1:]
            self.lvl[self.macgyver.pos_y] = self.lvl[self.macgyver.pos_y][0:self.macgyver.pos_x] +\
                self.id_perso + self.lvl[self.macgyver.pos_y][self.macgyver.pos_x+1:]



class Item:
    """Describes an item"""
    def __init__(self, display, position):
        self.display = display
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.show = True

class Character(Item):
    """Describes the main character"""
    def __init__(self,pos_perso):
        self.former_pos_x = -1
        self.former_pos_y = -1
        self.pos_x = pos_perso[0]
        self.pos_y = pos_perso[1]
        self.ens1 = {"A","B","C"}
        self.ens2 = set()


if __name__=="__main__":
    lab = Laby()
    while True:
        lab.affiche_labyrinthe()
        lab.jeu()

    
