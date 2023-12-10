class Wall:
    def __init__(self) -> None:
        self.position_x = None
        self.position_y = None
        self.broken = False

    def set_position(self, new_position):
        self.position_x = new_position[0]
        self.position_y = new_position[1]

    def get_position(self):
        return (self.position_x, self.position_y)

    def break_wall(self):
        self.broken = True

    def is_broken(self):
        return self.broken
