from Codes.Environments.Jump_or_Drop_The_Wall.players.attacker import Attacker
import random
from Codes.Environments.Jump_or_Drop_The_Wall.utils import Wall

from Environments.Jump_or_Drop_The_Wall.players.defenser import Defenser

class Environment_JoD():
    
    def __init__(self, number_of_attackers=1, number_of_defensers=1, size=(20,20)) -> None:
        self.map_size=size
        self.attackers = list()
        self.defensers = list()
        self.number_of_attackers=number_of_attackers
        self.number_of_densers=number_of_defensers
        #We initialize the map by a dictionnary where the elements are either an attacker or a defenser or a wall or nothing
        #TODO(): This way of using the environment doesn't seem to be optimal. 
        self.map = dict()
        self._init_map()
        self._random_init_attackers()
        self._random_init_defensers()

    def _init_map(self):
        for i in range(self.map_size[0]):
            self.map[i] = dict()
            for j in range(self.map_size[1]):
                self.map[i][j]=None


    def _random_init_attackers(self):
        #We intialize the attackers with a random position
        for nb in range(self.number_of_attackers):
            i,j = random.randint(0,self.map_size[0]),random.randint(0,self.map_size[0])
            new_attacker= Attacker(position=(i,j) ,env= self)
            self.attackers.append(new_attacker)
            if(self.map[i][j]==None):
                self.map[i][j] = new_attacker

    def _random_init_defenser(self):
        #We intialiaze the defensers with a random position
        for nb in range(self.number_of_defensers):
            i,j = random.randint(0,self.map_size[0]),random.randint(0,self.map_size[0])
            new_defenser= Defenser(position=(i,j) ,env= self)
            self.attackers.append(new_defenser)
            if(self.map[i][j]==None):
                self.map[i][j] = new_defenser

    def add_wall(self, position):
        # Add a simple wall in the map
        if(self.map[position[0]][position[1]] is None):
            self.map[position[0]][position[1]] = Wall()

    def remove_wall(self,position):
        # Remove the wall at the given position
        if( isinstance(self.map[position[0]][position[1]],Wall )):
            self.map[position[0]][position[1]] = None
        else:
            raise Exception("No wall here")

    def get_map(self):
        return self.map
    
    def is_occupied(self, position):
        if(isinstance(self.map[position[0]][position[1]],(Attacker,Defenser))):
           return True
        else:
            return False
    
    def kill_the_defenser(self, defenser_position):
        self.map[defenser_position[0]][defenser_position[1]]

    def change_position(self, current_position, new_positon):
        if(current_position == new_positon):
            if(self.map[new_positon[0]][])