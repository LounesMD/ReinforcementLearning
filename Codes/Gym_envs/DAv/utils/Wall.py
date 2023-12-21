class Wall:
    def __init__(self) -> None:
        self.position = None
        self.broken = False

    def set_position(self, new_position):
        self.position = new_position

    def get_position(self):
        return self.position

    def break_wall(self):
        self.broken = True

    def is_broken(self):
        return self.broken
