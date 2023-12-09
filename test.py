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
    