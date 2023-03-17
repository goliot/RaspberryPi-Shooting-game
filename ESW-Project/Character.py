import numpy as np
from PIL import Image


class Character:
    def __init__(self, width, height):
        self.state = None
        self.speed = 10
        width = 120
        height = 223
        self.position = np.array([width - 10, height - 10, width + 10, height + 10])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.drawplayer = Image.open('/home/kau-esw/ESW-Project/asset/player.png').resize((30, 30))


    def move(self, command = None):
        if command['left_pressed']:
            self.position[0] -= self.speed
            self.position[2] -= self.speed
                
        elif command['right_pressed']:
            self.position[0] += self.speed
            self.position[2] += self.speed
        
        if self.position[0] < 10 or self.position[2] < 10: #벽 뚫지 못하게 방지
            self.position[0] += self.speed * 2
            self.position[2] += self.speed * 2
        elif self.position[0] > 230 or self.position[2] > 230:
            self.position[0] -= self.speed * 2
            self.position[2] -= self.speed * 2
        #캐릭터가 양쪽 벽에 닿으면 튕기게

        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 