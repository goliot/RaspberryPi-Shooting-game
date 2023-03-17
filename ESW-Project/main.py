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

    player_path = '/home/kau-esw/ESW-Project/asset/player.png'
    background_path = '/home/kau-esw/ESW-Project/asset/esw_background.png'
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

    joystick = Joystick()

    image = Image.new("RGB", (joystick.width, joystick.height))
    draw = ImageDraw.Draw(image)

    backgroundImage = Image.open(background_path).resize((240, 240))
    playerImage = Image.open(player_path).resize((40, 40))

    joystick.disp.image(image)

    score = 0
    life = 5
    ammo = 50

    player = Character(joystick.width, joystick.height)
    positionXIndex = [rand, rand+40, rand+80, rand+120]

    enemy_1 = Enemy((positionXIndex[0], -20))
    enemy_2 = Enemy((positionXIndex[1], -20))
    enemy_3 = Enemy((positionXIndex[2], -20))
    enemy_4 = Enemy((positionXIndex[3], -20))

    enemys_list = [enemy_1, enemy_2, enemy_3, enemy_4]

    bullets = []

    while True:
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        
        if not joystick.button_U.value: #위
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value: #아래
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value: #왼쪽
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value: #오른쪽
            command['right_pressed'] = True
            command['move'] = True

        player.move(command)

        image.paste(backgroundImage, (0,0))
        image.paste(player.drawplayer, (player.position[0], player.position[1]))
    
        if not joystick.button_A.value: #A버튼
            if ammo > 0:
                bullet = Bullet(player.center, command) 
                bullets.append(bullet)
                ammo -= 1
        
        for bullet in bullets:
            bullet.collision_check(enemys_list)
            bullet.move()

    
        for enemy in enemys_list:
            rposition = random.randint(20, 220)

            image.paste(enemy.drawmob, (enemy.position[0], enemy.position[1]))
            enemy.move((rposition, -20))
            if enemy.state == 'die':
                enemys_list.remove(enemy)
                enemys_list.append(Enemy((rposition, -20)))
                score += 1
                enemy.state = 'alive'
                continue
                
            if enemy.position[1] > 210 and enemy.state != 'die': #바닥쪽에 가고 나서, 총알도 안맞았으면
                if not enemy.hit_check(player) : #플레이어에 안맞았을 때
                    enemys_list.remove(enemy)
                    enemys_list.append(Enemy((rposition, -20)))
                    score += 1
                    continue
                elif enemy.hit_check(player) : #플레이어에 맞았을 때
                    enemys_list.remove(enemy)
                    enemys_list.append(Enemy((rposition, -20)))
                    life -= 1
                    continue

        for bullet in bullets:
            if bullet.state != 'hit':
                draw.rectangle(tuple(bullet.position), outline = bullet.outline, fill = (0, 0, 255))


        if life <= 0 : #패배시 you lose 텍스트
            while True:
                draw.rectangle((0, 0, joystick.width, joystick.height), outline=0, fill=0)
                rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))                       
                draw.text((52, 90), "YOU LOSE...", font = fnt, fill = rcolor)
                joystick.disp.image(image)
        if score >= 100 :#승리시 you win 텍스트
            while True:
                draw.rectangle((0, 0, joystick.width, joystick.height), outline=0, fill=0)
                rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))                       
                draw.text((52, 90), "YOU WIN!", font = fnt, fill = rcolor)
                joystick.disp.image(image)

                
        for bullet in bullets:
            if bullet.state != 'hit':
                draw.rectangle(tuple(bullet.position), outline = bullet.outline, fill = (0, 0, 255))

        rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
        draw.text((110, 10), "Score: " + str(score), font = fnt, fill = rcolor) #현재 점수
        draw.text((20, 10), "Life: " + str(life), font = fnt, fill = rcolor) #현재 목숨
        draw.text((20, 200), "Bullet: " + str(ammo), font = fnt, fill =rcolor) #현재 폭탄 개수
        joystick.disp.image(image)        

if __name__ == '__main__':
    main()