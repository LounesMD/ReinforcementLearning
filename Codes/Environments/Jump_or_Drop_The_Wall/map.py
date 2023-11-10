class Map():
    
    def __init__(self, position_x, position_y) -> None:
        self.position_x = position_x
        self.position_y = position_y


    def get_position(self):
        return (self.position_x, self.position_y)
        
        