class Attacker:
    def __init__(self, position, map, id="attacker", actions=[0, 1, 2, 3]) -> None:
        self.id = id
        self.position = position
        # Actions: 0: letf; 1: up; 2: right; 3: down
        self.actions = actions
        self.map = map
        self.color = "red"

    def step(self, action):
        current_position = self.position
        new_position = self.position

        # We move the attacker
        if action == 0:
            new_position = (self.position[0] - 1, self.position[1])
        elif action == 1:
            new_position = (self.position[0], self.position[1] + 1)
        elif action == 2:
            new_position = (self.position[0] + 1, self.position[1])
        elif action == 3:
            new_position = (self.position[0], self.position[1] - 1)

        if not self.map.is_within_limits(new_position):
            new_position = self.position

        if self.map.is_blocked(new_position):
            new_position = self.break_the_wall(new_position, current_position)

        if self.map.is_occupied_by_defenser(new_position): #If there is a defenser, we kill the it and we take its position.
            self.map.get_cell(new_position).kill()
            self.map.assign_element(new_position,None)
            new_position = current_position

        self.position = new_position
        self.map.change_position(current_position, new_position)

    def break_the_wall(self, wall_position, current_position):
        self.map.remove_wall(wall_position)
        return current_position
