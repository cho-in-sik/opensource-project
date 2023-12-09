import pygame
import random
import math

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
bulletimg = pygame.image.load("bullet.png")
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

#게임 루프
while True:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    display_font(textX,textY)
    player(playerX,playerY)       
    pygame.display.update()