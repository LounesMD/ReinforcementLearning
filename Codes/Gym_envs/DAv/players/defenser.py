class Defenser:
    def __init__(self, position, map, id="defenser", actions=[0, 1, 2, 3, 4]) -> None:
        self.id = id
        self.position = position
        # Actions: 0: letf; 1: up; 2: right; 3: down; 4: drop a wall
        self.actions = actions
        self.map = map
        self.drop = False
        self.alive = True
        self.color = "green"

    def get_id(self):
        return self.id

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position

    def get_actions(self):
        return self.actions

    def get_map(self):
        return self.map

    def step(self, action):
        assert self.is_alive()
        reward = 1
        current_position = self.position

        # We move the defenser
        if action == 0:
            new_position = (self.position[0] - 1, self.position[1])
        elif action == 1:
            new_position = (self.position[0], self.position[1] + 1)
        elif action == 2:
            new_position = (self.position[0] + 1, self.position[1])
        elif action == 3:
            new_position = (self.position[0], self.position[1] - 1)
        elif action == 4:
            self.drop = True
            new_position = current_position

        if self.map.is_accessible(new_position) and action != 4:
            if self.drop:
                self.map.change_position(current_position, new_position)
                self.add_a_wall(current_position)
                self.drop = False
            else:
                self.map.change_position(current_position, new_position)

        return reward

    def add_a_wall(self, wall_position):
        self.map.add_wall(wall_position)

    def kill(self):
        self.alive = False
        self.color = "blue"

    def is_alive(self):
        return self.alive
