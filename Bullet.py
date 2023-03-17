import numpy as np

class Bullet:
    def __init__(self, position, command):
        self.appearance = 'rectangle'
        self.speed = 10
        self.damage = 10
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.direction = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        self.state = None
        self.outline = "#0000FF"


    def bomb(self, enemy):
        ememy.state = 'die'
        

    def move(self):
        self.position[1] -= self.speed
        self.position[3] -= self.speed
            