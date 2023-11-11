class Defenser:
    def __init__(self, position, env, id="defenser", actions=[0, 1, 2, 3, 4]) -> None:
        self.id = id
        self.position = position
        # Actions: 0: letf; 1: up; 2: right; 3: down; 4: drop a wall
        self.actions = actions
        self.env = env
        self.drop = False
        self.alive = True
        self.color = "green"

    def step(self, action):
        current_position = self.position
        new_position = self.position

        # We move the defenser
        if action == 0:
            new_position = (self.position[0] - 1, self.position[1])
        elif action == 1:
            new_position = (self.position[0], self.position[1] + 1)
        elif action == 2:
            new_position = (self.position[0] + 1, self.position[1])
        elif action == 3:
            new_position = (self.position[0], self.position[1] - 1)

        if not self.env.wall(new_position) and action != 4:
            if self.drop:
                self.add_a_wall(current_position)
                self.drop = False

        elif action == 4:
            self.drop = True

        self.position = new_position
        self.env.change_position(current_position, new_position)

    def add_a_wall(self, wall_position):
        self.env.add_wall(wall_position)

    def kill(self):
        self.alive = False
