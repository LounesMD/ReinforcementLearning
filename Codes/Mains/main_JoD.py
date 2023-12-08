import time
from Codes.Environments.Jump_or_Drop_The_Wall.environment import Environment_JoD
from Codes.Environments.Jump_or_Drop_The_Wall.render import Render_JoD
from Codes.Environments.Jump_or_Drop_The_Wall.politics.defenser_politic_random import defenser_politic_random
from Codes.Environments.Jump_or_Drop_The_Wall.politics.attacker_politic_random import attacker_politic_random
import matplotlib.pyplot as plt


def main():
    render = Render_JoD()
    env = Environment_JoD()
    plt.ion()
    fig = plt.figure() 

    render.render_env(env,fig)

    def_politic = defenser_politic_random()
    att_politic = attacker_politic_random()

    are_alive = True
    while(are_alive):
        defensers = env.get_defensers()
        attackers = env.get_attackers()
        for defenser in defensers:
            if(defenser.is_alive()):
                defenser.step( def_politic.get_action(env.get_map(),defenser) )
        
        for attacker in attackers:
            attacker.step( att_politic.get_action(env.get_map(),attacker) )

        render.render_env(env,fig)

        are_alive = [defenser.is_alive() for defenser in env.get_defensers()] 
        
if __name__ == "__main__":
    main()
