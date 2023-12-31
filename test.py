import pygame
from pygame import mixer
import random
import math
import cv2
import mediapipe as mp
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime


#게임 시작 
pygame.init()

#화면 세팅
screen = pygame.display.set_mode((800,600))

#제목
pygame.display.set_caption("Play")

#그리기 도구 지원해주는 서브 패키지
mp_drawing = mp.solutions.drawing_utils

#손 감지 모듈
mp_hands = mp.solutions.hands




# 캠 키기
cap = cv2.VideoCapture(0)

#점수
score_value = 0
font = pygame.font.Font('freesansbold.ttf',45)

textX = 50
textY = 60

game_over = pygame.font.Font('freesansbold.ttf',65)


#프레임
clock = pygame.time.Clock()

#highScore.txt 파일 생성
def create_highscore_file():
    with open("highScore.txt", "w") as file:
        file.write("0")

#점수 표시
def display_font(x,y):
    score = font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#폰트 로드
def loadfont(fontsize=50):
	ttf = 'NotoSansKR-VariableFont_wght.ttf'
	return ImageFont.truetype(font=ttf, size=fontsize)

titlefontObj = loadfont(fontsize=60)



#최고점수 업데이트
def update_highscore(score):
    try:
        with open("highScore.txt", "r") as file:
            current_highscore = int(file.read())
    except FileNotFoundError:   #예외처리1
        create_highscore_file()
        current_highscore = 0

    if score > current_highscore:
        with open("highScore.txt", "w") as file:
            cv2.imwrite("record breaker.jpg", image)  #openCV imwrite메서드로 최고기록 갱신 시의 프레임 저장 후 jpg파일 생성
            target_img = Image.open("record breaker.jpg")   #target_img 지정

            #프레임 위에 그릴 Text지정 (datetime 모듈 활용)
            title_text ="최고 기록 " \
                        + str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))\
                        + " 에 갱신"


            out_img = ImageDraw.Draw(target_img)
            out_img.text(xy=(15,15), text=title_text, fill=(237, 230, 211), font=titlefontObj)  #저장된 프레임에 최고기록 갱신 시간을 text로 그리기"

            target_img.save("please.jpg")
            
            file.write(str(score))

#게임오버 표시
def display_gameover():
    over = game_over.render("Game Over",True,(255,255,255))
    screen.blit(over,(250,280))


#최고점수 표시
def display_highscore():
    try:
        with open("highScore.txt", "r") as file:
            highscore = int(file.read())  # highScore.txt 파일에서 점수 읽기
    except FileNotFoundError:
        pass
    else:
        # 폰트 및 색상 설정
        score_font = pygame.font.Font('freesansbold.ttf', 45)
        score_color = (255, 255, 255)

        # 화면에 표시될 텍스트 렌더링
        highscore_text = score_font.render("HighScore: " + str(highscore), True, score_color)
        
        # 화면에 텍스트 표시
        screen.blit(highscore_text, (50, 10))

#게임 재시작
def restart_game():
    global playerX, playerY, playerX_change, bullet_state, bulletY, score_value
    playerX = 350
    playerY = 500
    playerX_change = 0
    bullet_state = "ready"
    bulletY = 480
    score_value = 0
    
    for i in range(0, 6):
        enemyX[i] = random.randint(0, 755)
        enemyY[i] = random.randint(50, 200)


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
    enemyX_change.append(6)
    enemyY_change.append(45)

def enemy(x,y,i):
    screen.blit(enemyimgT[i],(x,y))
    

#Bullet


bulletimg = pygame.image.load("bullet.png")
bulletimg = pygame.transform.scale(bulletimg, (25, 25))



bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

#pillsalgi
pillsalimg = pygame.image.load("newpillsalgi.png")
pillsalimg = pygame.transform.scale(pillsalimg, (100, 200))

# 필살기 상태 초기화
pillsalgi_state = "ready"
pillsalgiX = 0
pillsalgiY = 0
pillsalgiY_change = 20



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
    


with mp_hands.Hands(max_num_hands = 1, min_detection_confidence =0.5,
                    min_tracking_confidence = 0.5) as hands:
    while cap.isOpened():

        #img counter
        img_counter = 0

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

        # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
        image.flags.writeable = False

        # Image에서 손을 추적하고 결과를 result에 저장
        result = hands.process(image)

        # 이미지 값 순서를 RGB에서 BGR로 다시 바꿈
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        
        

        #캠 화면에 띄울 텍스트 정의 ( 기본 값 )
        gesture_text = ''

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




            

            #전부 펴져있으면 리스타트
            if( finger_1 and finger_2 and finger_3 and finger_4 and finger_5):
                gesture_text = 'Restart'
                restart_game()
                
            # 검지, 중지, 약지 펴져있으면 STOP
            elif(finger_2 and finger_3 and finger_4):
                gesture_text = 'stop'
                playerX_change = 0
                

            elif finger_4 and pillsalgi_state =="ready":
                gesture_text = "pillsalgi"
                pillsalgi_state = "fire"
                pillsalgiX = playerX
                pillsalgiY = playerY
             # 검지 -> 왼쪽
            elif(finger_2):
                gesture_text = '<--'
                playerX_change = -15
            # 약지 -> 오른쪽
            elif(finger_5):
                gesture_text = '-->'
                playerX_change = 15
                

        
            # 주먹쥐면 "fire"
            elif( (not finger_2) and (not finger_3) and (not finger_4)
                and (not finger_5)):
                gesture_text = 'fire'

                gesture_text = 'shooting'
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
                #q 누르면 종료
                if event.key ==pygame.K_q:
                    pygame.display.quit()
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
        # 스코어가 3 이상이면 총알 이미지를 바꿈
        if score_value >= 3:
            # 새로운 총알 이미지 로드
            bulletimg = pygame.image.load("new_bullet.png")
            bulletimg = pygame.transform.scale(bulletimg, (35, 35))
        #초기화했을때 기본총알로 재변경
        if score_value == 0:
            bulletimg = pygame.image.load("bullet.png")
            bulletimg = pygame.transform.scale(bulletimg, (25, 25))

       
        # 필살기 이동
        if pillsalgi_state is "fire":
            screen.blit(pillsalimg, (pillsalgiX, pillsalgiY))
            pillsalgiY -= pillsalgiY_change

            # 필살기가 화면을 벗어나면 상태를 "ready"로 설정
            if pillsalgiY < 0:
                pillsalgi_state = "ready"
                pillsalgiY = 0
        
      
        #Enemy 이동
        for i in range(0,6):
            if enemyY[i]>=480:
                for j in range(0,6):
                    enemyY[j]= 2000
                display_gameover()
               
                break
                
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 6
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 750:
                enemyX_change[i] = -6
                enemyY[i] += enemyY_change[0]
            
            colide = Collusion(enemyX[i],enemyY[i],bulletX,bulletY)
            display_highscore()
            
        
            enemy(enemyX[i],enemyY[i],i)
        
            if colide:
                bullet_state = "ready"
                bulletY = 480
                enemyX[i] = random.randint(0,755)
                enemyY[i]= random.randint(50,200)
                score_value +=1
                mixer.music.load("explosion.ogg")
                mixer.music.play()
            
        # 필살기와 몬스터의 충돌 검사
        for i in range(0, 6):
            colide_pillsalgi = Collusion(enemyX[i], enemyY[i], pillsalgiX, pillsalgiY)

            if colide_pillsalgi:
                pillsalgi_state = "ready"
                pillsalgiY = 0
                enemyX[i] = random.randint(0, 755)
                enemyY[i] = random.randint(50, 200)
                score_value += 1
                mixer.music.load("explosion.ogg")
                mixer.music.play()

        update_highscore(score_value)

     
        display_font(textX,textY)
        player(playerX,playerY)       
        pygame.display.update()

    

   
    