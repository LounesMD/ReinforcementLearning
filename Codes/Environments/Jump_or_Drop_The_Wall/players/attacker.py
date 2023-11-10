class Attacker():

    def __init__(self, position, env, id="attacker", actions=[0,1,2,3]) -> None:
        self.id=id
        self.position= position
        #Actions: 0: letf; 1: up; 2: right; 3: down
        self.actions= actions
        self.env = env
        self.color = "red"

    def step(self,action):
        current_position = self.position
        new_position = self.position

        # We move the attacker 
        if action==0:
            new_position = (self.position[0]-1, self.position[1])
        elif action==1:
            new_position = (self.position[0], self.position[1]+1)
        elif action==2:
            new_position = (self.position[0]+1, self.position[1])
        elif action==3:
            new_position = (self.position[0], self.position[1]-1)

        if not self.env.is_accessible(new_position):
            new_position = self.position

        if self.env.wall(new_position):
            new_position = self.break_the_wall(new_position,current_position)

        if self.env.is_occupied(new_position):
            self.env.kill_the_defenser(new_position)
            new_position = current_position

        
        self.position= new_position
        self.env.change_position(current_position, new_position)
        
    def break_the_wall(self,action, wall_position, current_position):
        self.env.remove_wall(wall_position)
        return current_position