"""
References : 
https://coneural.org/florian/papers/05_cart_pole.pdf
https://ieeexplore.ieee.org/document/6313077

"""


import random
import math
from matplotlib import pyplot as plt


class CartPole:
    def __init__(self):
        self.cpt = 0
        self.Terminated = False
        self.position = random.uniform(-0.05, -0.05)	
        self.velocity = random.uniform(-0.05, -0.05)	
        self.pole_angle = random.uniform(-0.05, -0.05)	
        self.pole_angular_velocity = random.uniform(-0.05, -0.05)	

        self.gravity = 9.8
        self.mass_cart = 1.0
        self.mass_pole = 0.1
        self.total_mass = (self.mass_pole + self.mass_cart)
        self.length = 0.5
        self.pole_mass_length = (self.mass_pole * self.length)
        self.force_mag = 10.0
        self.tau = 0.02

    def bound(self):
        if self.position < -4.8:
            self.position = -4.8
        elif self.position > 4.8:
            self.position = 4.8

        if self.pole_angle < -(12 * 4 * math.pi / 360): # -0.418:
            self.pole_angle = -(12 * 4 * math.pi / 360)
        elif self.pole_angle > 12 * 4 * math.pi / 360:
            self.pole_angle = 12 * 4 * math.pi / 360
        


    def get_state(self):
        return [self.position, self.velocity, self.pole_angle, self.pole_angular_velocity]


    def action(self , action):
        if(action==0 or action==1):
            self.cpt += 1
            force = self.force_mag if action==1 else -self.force_mag
            costheta = math.cos(self.pole_angle)
            sintheta = math.sin(self.pole_angle)

            temp = (force + self.pole_mass_length * (self.pole_angular_velocity)**2 * sintheta) / self.total_mass

            thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.mass_pole * costheta**2 / self.total_mass))

            xacc = temp - self.pole_mass_length * thetaacc * costheta / self.total_mass


            # Semi implicit Euler
            self.velocity += self.tau*xacc
            self.position += self.tau*self.velocity
            self.pole_angular_velocity += self.tau*thetaacc
            self.pole_angle += self.tau*self.pole_angular_velocity


            self.bound()
            if(self.final_state()):
                self.Terminated = True
            return 1
        else:
            raise Exception("Error: Action not valid")
            print("Error: Action not valid")

    def final_state(self):
        return (    self.pole_angle >= (12 * 2 * math.pi / 360) or
                    self.pole_angle <= -(12 * 2 * math.pi / 360) or
                    self.position >= 2.4 or
                    self.position <= -2.4 )

    def reset(self):
        self.Terminated = False
        self.cpt = 0
        self.position = random.uniform(-0.05, -0.05)
        self.velocity = random.uniform(-0.05, -0.05)
        self.pole_angle = random.uniform(-0.05, -0.05)
        self.pole_angular_velocity = random.uniform(-0.05, -0.05)