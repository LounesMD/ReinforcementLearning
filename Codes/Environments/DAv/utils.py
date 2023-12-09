class Wall:
    def __init__(self) -> None:
        self.position_x = None
        self.position_y = None
        self.broken = False

    def set_position(self,x_pos, y_pos):
        self.position_x = x_pos
        self.position_y = y_pos

    def get_position(self):
        return (self.position_x,self.position_y)

    def break_wall(self):
        self.broken = True

    def is_broken(self):
        return self.broken