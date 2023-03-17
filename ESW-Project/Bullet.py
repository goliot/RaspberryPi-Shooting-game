import numpy as np

class Bullet:
    def __init__(self, position, command):
        self.appearance = 'rectangle'
        self.speed = 10
        self.damage = 10
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.state = None
        self.outline = "#0000FF"


    def bomb(self, enemy):
        ememy.state = 'die'
        

    def move(self):
        self.position[1] -= self.speed
        self.position[3] -= self.speed

    def collision_check(self, enemys): #총알, 적 충돌 체크
        for enemy in enemys:
            collision = self.overlap(self.position, enemy.position)
            
            if collision:
                enemy.state = 'die'
                self.state = 'hit'

    def overlap(self, ego_position, other_position):
        return ego_position[0] > other_position[0] and ego_position[1] > other_position[1] \
                 and ego_position[2] < other_position[2] and ego_position[3] < other_position[3]
            