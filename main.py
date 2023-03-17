from PIL import ImageDraw, ImageFont, Image
import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from Enemy import Enemy
from Bullet import Bullet
from Character import Character
from Joystick import Joystick


def main():
    rand = random.randint(20, 50)

    mob_path = '/home/kau-esw/ESW-Project/asset/mob2.png'
    player_path = '/home/kau-esw/ESW-Project/asset/player.png'
    background_path = '/home/kau-esw/ESW-Project/asset/esw_background.png'
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

    joystick = Joystick()

    image = Image.new("RGB", (joystick.width, joystick.height))
    draw = ImageDraw.Draw(image)

    backgroundImage = Image.open(background_path).resize((240, 240))
    playerImage = Image.open(player_path).resize((40, 40))
    mobImage = Image.open(mob_path).resize((40, 40)).transpose(Image.FLIP_TOP_BOTTOM)

    joystick.disp.image(image)

    score = 0
    life = 5
    bomb = 2

    # mobObject = Enemy.drawmob
    player = Character(joystick.width, joystick.height)
    positionXIndex = [rand, rand+40, rand+80, rand+120]

    enemy_1 = Enemy((positionXIndex[0], -20))
    enemy_2 = Enemy((positionXIndex[1], -20))
    enemy_3 = Enemy((positionXIndex[2], -20))
    enemy_4 = Enemy((positionXIndex[3], -20))

    enemys_list = [enemy_1, enemy_2, enemy_3, enemy_4]
    # enemys_list = [enemy_1]

    bullets = []

    while True:
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

        player.move(command)

    
        # draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 255))
        image.paste(backgroundImage, (0,0))
        # draw.ellipse(tuple(player.position), outline = player.outline, fill = (0, 255, 0))
        image.paste(player.drawplayer, (player.position[0], player.position[1]))
    
        for enemy in enemys_list:
            # randomIndex = random.sample(positionXIndex, 4)
            rposition = random.randint(50, 200)

            image.paste(enemy.drawmob, (enemy.position[0], enemy.position[1]))
            enemy.move((rposition, -20))
            
            if not joystick.button_A.value:
                if bomb > 0:
                    for enemy in enemys_list:
                        enemys_list.remove(enemy)
                        enemys_list.append(Enemy((rposition, -20)))
                        score += 1
                    bomb -= 1
                    continue

            if enemy.position[1] > 200:
                if not enemy.hit_check(player) :
                    # print(enemy.position)
                    # print(player.position)
                    # print(enemy.hit_check(player))
                    enemys_list.remove(enemy)
                    enemys_list.append(Enemy((rposition, -20)))
                    score += 1
            # elif enemy.position[0] < player.position[0]+10 and enemy.position[0] > player.position[0]-10 and enemy.position[1] > player.position - 10 and enemy.position[1] < player.position[1] + 10:
                elif enemy.hit_check(player) :
                    # print(enemy.position)
                    # print(player.position)
                    # print(enemy.hit_check(player))
                    enemys_list.remove(enemy)
                    enemys_list.append(Enemy((rposition, -20)))
                    life -= 1

                elif enemy.state == 'die' :
                    enemys_list.remove(enemy)
                    enemys_list.append(Enemy((rposition, -20)))
                    score += 1
                    enemy.state = 'alive'


        if life <= 0 : #패배
            while True:
                draw.rectangle((0, 0, joystick.width, joystick.height), outline=0, fill=0)
                rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))                       
                draw.text((52, 90), "YOU LOSE...", font = fnt, fill = rcolor)
                joystick.disp.image(image)
        if score >= 100 :#승리
            while True:
                draw.rectangle((0, 0, joystick.width, joystick.height), outline=0, fill=0)
                rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))                       
                draw.text((52, 90), "YOU WIN!", font = fnt, fill = rcolor)
                joystick.disp.image(image)

                
        for bullet in bullets:
            if bullet.state != 'hit':
                draw.rectangle(tuple(bullet.position), outline = bullet.outline, fill = (0, 0, 255))

        rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))

        draw.text((110, 10), "Score: " + str(score), font = fnt, fill = rcolor)
        draw.text((20, 10), "Life: " + str(life), font = fnt, fill = rcolor)
        draw.text((20, 200), "Bomb: " + str(bomb), font = fnt, fill =rcolor)
        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(image)        

if __name__ == '__main__':
    main()