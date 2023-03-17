import numpy as np
from PIL import Image

class Enemy:
    def __init__(self, spawn_position):
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 20, spawn_position[1] - 20, spawn_position[0] + 10, spawn_position[1] + 10])
        self.speed = 15
        self.drawmob = Image.open('/home/kau-esw/ESW-Project/asset/mob2.png').resize((30, 30)).transpose(Image.FLIP_TOP_BOTTOM)

    def move(self, spawn_position):
        self.position[1] += self.speed
        self.position[3] += self.speed
        if self.position[3] > 300 or self.position[1] > 300:
            self.position = np.array([spawn_position[0] - 15, spawn_position[1] - 15, spawn_position[0] + 10, spawn_position[1] + 10])


    def hit_check(self, player): #플레이어와 닿았는지 체크
        collision = self.isHit(self.position, player.position)
        return collision

    def isHit(self, ego_position, other_position):
        return ego_position[0] < other_position[0]+20 and ego_position[2] > other_position[2]-20 \
                and ego_position[1] > other_position[1] and ego_position[3] > other_position[3]