from typing import List
from Codes.Environments.Jump_or_Drop_The_Wall.environment import Environment_JoD
from Codes.Environments.Jump_or_Drop_The_Wall.players.attacker import Attacker
from Codes.Environments.Jump_or_Drop_The_Wall.players.defenser import Defenser
import matplotlib.pyplot as plt
import time
from Codes.Environments.Jump_or_Drop_The_Wall.map import Map_JoD
from Codes.Environments.Jump_or_Drop_The_Wall.utils import Wall

wall_length = 0.5

class Render_JoD:
    def render_env(self, env: Environment_JoD,fig):
        ax = fig.add_subplot(111) 

        ax.axis([-1, 20, -1, 20])
        ax.grid(which = "both")
        map = env.map
        self.render_map(map,ax)
        self.render_defensers(map.defensers,ax)
        self.render_attackers(map.attackers,ax)
        self.render_walls(map.walls,ax)

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1)

    def render_map(self, map: Map_JoD,ax):
        ax.plot(map.map_size[0], map.map_size[1])
        
    def render_defensers(self, defensers: List[Defenser],ax):
        for defenser in defensers:
            ax.scatter(defenser.position[0],defenser.position[1],c=defenser.color)

    def render_attackers(self, attackers: List[Attacker],ax):
        for attacker in attackers:
            ax.scatter(attacker.position[0],attacker.position[1],c=attacker.color)

    def render_walls(self, walls: List[Wall],ax):
        for wall in walls:
            if(not wall.is_broken()):
                wall_x_pos = wall.get_position()[0]
                wall_y_pos = wall.get_position()[1]
                ax.plot([wall_x_pos-wall_length,wall_x_pos+wall_length],[wall_y_pos,wall_y_pos],c='peru',label='wall')
                ax.plot([wall_x_pos,wall_x_pos],[wall_y_pos-wall_length, wall_y_pos+wall_length], c='peru')
