import pygame
from pygame import mixer
import random
import math
import mediapipe as mp

#게임 시작
pygame.init()

#화면 세팅
screen = pygame.display.set_mode((800,600))

#제목
pygame.display.set_caption("Space Invaders")

#점수
score_value = 0
font = pygame.font.Font('freesansbold.ttf',45)

textX = 300
textY = 20

game_over = pygame.font.Font('freesansbold.ttf',65)

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
#게임 루프
while True:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Player 움직임과 경계설정
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750
        
    playerX += playerX_change
    
    #탄환 움직임
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480    

    display_font(textX,textY)
    player(playerX,playerY)       
    pygame.display.update()