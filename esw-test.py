import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

from Player import Player
from Enemy import Enemy
from Enemies import Enemies


# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    width = 240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
black_fill = "#000000"
udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"
black_outline = "#000000"
text_fill = "#1FDA11"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
background = Image.open('images/background1.jpg')
background = background.resize((240, 240)) #240 240 크기
enemy_index = [0, 1, 2, 3, 4, 5, 6, 7]  #한줄에 총 8개의 적들 리스트로 설정
stage = 1
new_stage = 0 #새로운 스테이지 마다 랜덤으로 enemy를 생성하기 위해 설정해 놓은 것
life = 3
hit = 0
speed = 15 #player speed
delete_enemy = [] #지워지는 적들 index 리스트에 저장
up_down = 'None'
left_right = 'None'
enemies = Enemies(stage) #Enemies 객체 생성
player = Player(life, speed) #player 객체 생성
button_a = 0
button_b = 0
while True:
    up_down = 'None' #초기화
    left_right = 'None'
    image.paste(background, (0,0)) #백그라운드 이미지 붙이기
    if new_stage == 0: #새로운 스테이지 시 지울 enemies 초기화 후 랜덤으로 뽑기
        delete_enemy = random.sample(enemy_index, 2)
        new_stage = 1 #1일땐 old stage
    

    #방향 버튼 눌렀을때 
    if not button_U.value:  # up pressed
        up_down = 'up'
    if not button_D.value:  # down pressed
        up_down = 'down'
    if not button_L.value:  # left pressed
        left_right = 'left'
    if not button_R.value:  # right pressed
        left_right = 'right'
    if not button_A.value:  # left pressed, fast player speed
        if button_a == 0: #아이템 한번씩만 사용 가능
            for enemy in enemies.enemy_list :  #생성된 적들의 속도 줄이기
                enemy.speed_down()
            print('enemy speed down!')
            button_a += 1
    if not button_B.value:  # left pressed, slow enemy speed
        if button_b == 0: #아이템을 한번씩만 할 수 있음
            player.speed_up()
            print('speed up!')
            button_b += 1

    for i in range(len(enemies.enemy_list)) :  #생성된 랜덤 enemy index
        if i in delete_enemy :              #생성은 되었지만 뽑지 않아 보여지지 않는 것처럼 보임
            continue
        else :
            image.paste(enemies.enemy_list[i].image, (enemies.enemy_list[i].left_top_x, enemies.enemy_list[i].left_top_y))# 이미지 그리는것
    image.paste(player.image, (player.x_position, player.y_position)) #에너미 리스트로 좌표 만들기
    player.move(up_down, left_right) #플레이어 움직임 만듦
    #enemy_list 에서 
    for i in range(len(enemies.enemy_list)) :
        enemies.enemy_list[i].step() #y 좌표 내려가는거 구현, enemies 에서 구현
        if i in delete_enemy :
            continue
        hit = hit or enemies.enemy_list[i].hit_check(player) #플레이어가 맞는지 안맞는지 check 함 hit 가 한번이라도 1의 값을 가지면 유지 돌면서 0으로 초기화되어야함
    
    if hit == 1:       #부딪혔을 때 hit 설정 후 맞은만큼 life 에서 까임 제대로 까였나 print 로 체크
        life -= 1
        print(life) #나오는 결과보고 life 남은거 확인
    if player.life == 0:
        while True:
                draw.rectangle((0, 0, width, height), outline=0, fill=0)

                rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
            
                draw.text((52, 90), "YOU GOT F GRADE", font = fnt2, fill = rcolor)
            
                draw.text((52, 120), "YOU GOT F GRADE", font = fnt2, fill = rcolor)
            
                draw.text((52, 150), "YOU GOT F GRADE", font = fnt2, fill = rcolor)    #game에서 클리어 하지 못할 시 형형색색으로 F학점을 맞았다고 해줌
                disp.image(image)
    if enemies.enemy_list[0].left_top_y >= 240 or hit :            #적들의 리스트가 y좌포 240이면 끝에 닿았다는 소리 || 맞았을때의 상황 설명
        hit = 0 #hit 초기화
        new_stage = 0 #new_stage 를 0으로 해서 새로운 랜덤한 2개 추출
        stage += 1 #다음스테이지로 넘어감
        enemies = Enemies(stage)    #적들을 처음 위치로 설정함 , 객체 생성
        player = Player(life, speed)    #플레이어 객체 맨 처음 위치로 초기화시킴
        if stage > 20: #스테이지 클리어시
            while True:
                draw.rectangle((0, 0, width, height), outline=0, fill=0)

                rcolor = tuple(int (x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
            
                draw.text((65, 90), "Game Clear!!!", font = fnt2, fill = rcolor)
            
                draw.text((65, 120), "Game Clear!!!", font = fnt2, fill = rcolor)
            
                draw.text((65, 150), "Game Clear!!!", font = fnt2, fill = rcolor)    #game clear 시..
                disp.image(image)
    draw.text((10,10), "stage: " + str(stage), font = fnt, fill = (255, 0, 0) ) #맨 위에 total score 띄워줌
    draw.text((160, 10),"life: " + str(life), font = fnt, fill = (255, 0, 0) ) #맨 위에 남은 life 띄워줌
    # Display the Image
    disp.image(image)