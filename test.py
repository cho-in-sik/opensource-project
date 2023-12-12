import pygame
from pygame import mixer
import random
import math

import cv2
import mediapipe as mp

#게임 시작 
pygame.init()

#화면 세팅
screen = pygame.display.set_mode((800,600))

#제목
pygame.display.set_caption("Space Invaders")

#그리기 도구 지원해주는 서브 패키지
mp_drawing = mp.solutions.drawing_utils

#손 감지 모듈
mp_hands = mp.solutions.hands

# 캠 키기
cap = cv2.VideoCapture(0)

#점수
score_value = 0
font = pygame.font.Font('freesansbold.ttf',45)

textX = 300
textY = 20

game_over = pygame.font.Font('freesansbold.ttf',65)

#프레임
clock = pygame.time.Clock()

#점수 표시
def display_font(x,y):
    score = font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))


#게임오버 표시
def display_gameover():
    over = game_over.render("Game Over",True,(255,255,255))
    screen.blit(over,(250,280))
    

#배경
background = pygame.image.load("background.png")

#bgm
mixer.music.load("bgm.mp3")
mixer.music.play(-1)

#Plyaer
playerimg = pygame.image.load("space-invaders.png")
playerimg = pygame.transform.scale(playerimg, (45, 45))

playerX = 350
playerY = 500
playerX_change = 0

def player(x,y):
    screen.blit(playerimg,(x,y))

#Enemy
enemyimg = []
enemyimgT =  []    
enemyX  = []
enemyY  = []
enemyX_change  = []
enemyY_change  = []


#몹생성
for i in range(0,6):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyimgT.append(pygame.transform.scale(enemyimg[i], (45, 45)))
    enemyX.append(random.randint(0,755))
    enemyY.append(random.randint(50,200))
    enemyX_change.append(4)
    enemyY_change.append(45)

def enemy(x,y,i):
    screen.blit(enemyimgT[i],(x,y))
    

#Bullet
bulletimg = pygame.image.load("new_bullet.png")
bulletimg = pygame.transform.scale(bulletimg, (35, 35))

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg,(x+5,y+16))
    mixer.music.load("fire.ogg")
    mixer.music.play()


def Collusion(aX,aY,bX,bY):
    distance = math.sqrt(math.pow((aX-bX),2)+math.pow((aY-bY),2))
    if distance <= 25:
        return True
    else:
        return False

# 적의 움직임을 제어하기 위한 타이머나 프레임 기반 변수
enemy_move_timer = pygame.time.get_ticks() 
with mp_hands.Hands(max_num_hands = 1, min_detection_confidence =0.5,
                    min_tracking_confidence = 0.5) as hands:
    while cap.isOpened():

        clock.tick(60)

        # 캠 읽기 성공여부 success와 읽은 이미지를 image에 저장
        success, image = cap.read()

        # 캠 읽기 실패시 continue
        if not success:
            continue

        # 이미지 값 좌우반전 ( 캠 켰을때 반전된 이미지 보완 )
        # 이미지 값 순서를 BGR -> RGB로 변환
        # 이미지 순서가 RGB여야 Mediapipe 사용가능
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # Image에서 손을 추적하고 결과를 result에 저장
        result = hands.process(image)

        # 이미지 값 순서를 RGB에서 BGR로 다시 바꿈
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #캠 화면에 띄울 텍스트 정의 ( 기본 값 )
        gesture_text = 'Cant found hand'

        # 결과 result가 제대로 추적이 되었을때 
        if result.multi_hand_landmarks:

            # 첫 번째로 추적된 손을 hand_landmarks에 할당
            hand_landmarks = result.multi_hand_landmarks[0]

            # 검지 ~ 소지 까지의 다 펴져있는지에 대한 bool 변수들 선언
            finger_1 = False
            finger_2 = False
            finger_3 = False
            finger_4 = False
            finger_5 = False

            #4번 마디가 2번 마디 보다 y값이 작으면 finger_1를 참
            if(hand_landmarks.landmark[4].y < hand_landmarks.landmark[2].y):
                finger_1 = True

            #8번 마디가 6번 마디 보다 y값이 작으면 finger_2를 참
            if(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y):
                finger_2 = True
                
            #12번 마디가 10번 마디 보다 y값이 작으면 finger_3를 참
            if(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y):
                finger_3 = True
                
            #16번 마디가 14번 마디 보다 y값이 작으면 finger_4를 참
            if(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y):
                finger_4 = True
                
            #20번 마디가 18번 마디 보다 y값이 작으면 finger_5를 참
            if(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y):
                finger_5 = True

            # 검지, 중지, 약지 펴져있으면 STOP
            if(finger_2 and finger_3 and finger_4):
                gesture_text = 'stop'
                playerX_change = 0
            
            # 약지 -> 오른쪽
            elif(finger_5):
                gesture_text = '-->'
                playerX_change = 10

            # 검지 -> 왼쪽
            elif(finger_2):
                gesture_text = '<--'
                playerX_change = -10

            # 주먹쥐면 "발사"
            elif( (not finger_2) and (not finger_3) and (not finger_4)
                and (not finger_5)):
                gesture_text = '발사'
                if bullet_state is "ready":
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)

           
            
            # 캠 화면에 손가락을 그림
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
        # 캠화면에 텍스트를 작성
        cv2.putText( image, text=' {}'.format(gesture_text)
                     , org=(10,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                 fontScale=1,color=(0,0,255), thickness=2)   
            
        #캠 화면 ( 이미지 )을 화면에 띄움
        cv2.imshow('image', image)

        
        screen.fill((0,0,0))
        screen.blit(background,(0,0))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -10
                
                if event.key == pygame.K_RIGHT:
                    playerX_change = 10
                
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)

                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                    
        #적움직임
        current_time = pygame.time.get_ticks()
        if current_time - enemy_move_timer > 2000:  # 1000밀리초(1초)마다 적을 움직이도록 설정 (필요에 따라 조절)
            enemy_move_timer = current_time  # 타이머 초기화

            for i in range(0, 3):
                enemyY[i] += enemyY_change[i]

                

        #Player 이동
        if playerX <= 0:
            playerX = 0
        elif playerX >= 750:
            playerX = 750
            
        playerX += playerX_change
        
        #Bullet 이동
        if bullet_state is "fire":
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change
        
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = 480
        
        #Enemy 이동
        
        for i in range(0,6):
            if enemyY[i]>=480:
                for j in range(0,3):
                    enemyY[j]= 2000
                display_gameover()
                break
                
            enemyX[i] += enemyX_change[i] 
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 750:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[0]
            
            colide = Collusion(enemyX[i],enemyY[i],bulletX,bulletY)
            
            enemy(enemyX[i],enemyY[i],i)
        
            if colide:
                bullet_state = "ready"
                bulletY = 480
                enemyX[i] = random.randint(0,755)
                enemyY[i]= random.randint(50,200)
                score_value +=1
                mixer.music.load("explosion.ogg")
                mixer.music.play()

        display_font(textX,textY)
        player(playerX,playerY)       
        pygame.display.update()

   
    