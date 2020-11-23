# Made by Pranshu Aggarwal

# Welcome to Breakout Sixth sense version or The Future: Sixth sense technology
# Forget keysboard. Here you have to control your board with your hands
# Enjoy the game


import cv2 as cv
import numpy as np
import pygame
import random
from pygame import mixer


pygame.init()

dis = pygame.display.set_mode((400, 500))

img = pygame.image.load('Rules.png')


red = [255,0,0]
light_blue = [0,0,128]

green = [0,255,0]

pygame.draw.rect(dis, red, [100,10,200,50])

dis.blit(img, (10,100))



font = pygame.font.Font('freesansbold.ttf', 40)


text = font.render('Start', True, green, red)



textRect = text.get_rect()  
textRect.center = (190, 35)



dis.blit(text, textRect)


pygame.display.update()

# initialization for breakout


blue = [0,0,255]

white = [255,255,255]

color1 = [255,0,0]
color2 = [255,0,0]
color3 = [255,0,0]
color4 = [255,0,0]
color5 = [255,0,0]
color6 = [255,0,0]
color7 = [255,0,0]


font = pygame.font.Font('freesansbold.ttf', 15)
font2 = pygame.font.Font('freesansbold.ttf', 90) 
text = font.render('Welcome! Press R to restart', True, green, light_blue)

textRect = text.get_rect()  
textRect.center = (110, 13)

text2 = font2.render('You Won', True, green, light_blue)
textrect = text2.get_rect()
textrect.center = (200, 200)

x_slider = 300

length_of_slider = 100


x_ball_old = 0
y_ball_old = 0

x_list = []

for i in range(10, 390, 10):
    x_list.append(i)


x_ball = random.choice(x_list)

vel = 20


# initialization ends



cam = cv.VideoCapture(0)

lower_value = np.array([20,100,100])
upper_value = np.array([40,255,255])

run = True

def mainloop(run, x_slider, x_ball, y_ball, x_ball_old, y_ball_old, length_of_slider, delayer):
    while run:
        pygame.time.delay(40)
        global vel
        ret,frame = cam.read()
        frame = cv.flip(frame,1)
    
        w = frame.shape[1]
        h = frame.shape[0]
        
        image_smooth = cv.GaussianBlur(frame,(7,7),0)

        mask = np.zeros_like(frame)

        mask[50:350,30:350] = [255,255,255]

        image_roi = cv.bitwise_and(image_smooth,mask)
        cv.rectangle(frame,(50,150),(350,450),(0,0,255),2)
        cv.line(frame,(150,150),(150,450),(0,0,255),1)
        cv.line(frame,(250,150),(250,450),(0,0,255),1)
        cv.line(frame,(50,150),(350,150),(0,0,255),1)
        cv.line(frame,(50,450),(350,450),(0,0,255),1)


        image_hsv = cv.cvtColor(image_roi,cv.COLOR_BGR2HSV)
        image_threshold = cv.inRange(image_hsv,lower_value,upper_value)
    
        contours, hierachy = cv.findContours(image_threshold,\
                                             cv.RETR_TREE,\
                                             cv.CHAIN_APPROX_NONE)


        if(len(contours)!=0):
           areas = [cv.contourArea(c) for c in contours]
           max_index = np.argmax(areas)
           cnt = contours[max_index]

           M = cv.moments(cnt)
           if(M['m00']!=0):
               cx = int(M['m10']/M['m00'])
               cy = int(M['m01']/M['m00'])
               cv.circle(frame,(cx,cy),4,(0,0,255),-1)
            
   
               if cy in range(150,450):
                   if cx<150 and x_slider > 5:
                       x_slider-=vel
                   elif cx>250 and x_slider+length_of_slider < 400:
                       x_slider+=vel
               

           cv.imshow('Frame',frame)
                
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        # motion of the slider
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            mainloop(True, 200, x_ball, 80, 0, 0, 100, 0)

        # motion of ball vertically
    
        # hitting the striker
        if y_ball == 450 and x_ball>= x_slider and x_ball < x_slider + length_of_slider:
            y_ball_old = y_ball
            y_ball-=10
        # in between, going up
        elif y_ball<450  and y_ball > 50 and y_ball_old > y_ball:
            y_ball_old = y_ball
            y_ball-=10
        # in between, going down
        elif y_ball < 450  and y_ball > 50 and y_ball_old < y_ball:
            y_ball_old = y_ball
            y_ball+=10
            if x_ball_old < x_ball:
                x_ball+=10
            else:
                x_ball-=10
        # htting the bricks
        elif y_ball <= 50:
            y_ball_old = y_ball
            y_ball +=10
        # going below the striker
        elif y_ball_old < y_ball and y_ball >= 450:
            y_ball_old = y_ball
            y_ball+=10
        
        # motion of the ball horizontally

        # hitting the left wall 
        if x_ball - 10 < 5:
            x_ball_old = x_ball
            x_ball+=10
        # hitting the right wall
        elif x_ball + 10 > 395:
            x_ball_old = x_ball
            x_ball -= 10
        # hitting the striker while going right
        elif x_ball>= x_slider and x_ball < x_slider + length_of_slider and x_ball_old < x_ball:
            x_ball_old = x_ball
            x_ball +=10
        # hitting the striker while going left
        elif x_ball>= x_slider and x_ball < x_slider + length_of_slider and x_ball_old > x_ball:
            x_ball_old = x_ball
            x_ball -=10
        # going left in between
        elif x_ball_old > x_ball:
            x_ball_old = x_ball
            x_ball -=10
        # going right in between
        elif x_ball_old < x_ball:
            x_ball_old = x_ball
            x_ball+=10      

        global color1
        global color2
        global color3
        global color4
        global color5
        global color6
        global color7

        
        # removing the bricks if hit
    
        if y_ball - 10 == 40 and x_ball >= 5 and x_ball <= 55 and color1 != [0,0,0]:
            color1 = [0,0,0]
        elif y_ball - 10 == 40 and x_ball >= 60 and x_ball <= 110 and color2 != [0,0,0]:
            color2 = [0,0,0]
        elif y_ball - 10 == 40 and x_ball >= 115 and x_ball <= 165 and color3 != [0,0,0]:
            color3 = [0,0,0]
        elif y_ball - 10 == 40 and x_ball >= 170 and x_ball <= 220 and color4 != [0,0,0]:
            color4 = [0,0,0]
        elif y_ball - 10 == 40 and x_ball >= 225 and x_ball <= 275 and color5 != [0,0,0]:
            color5 = [0,0,0]
        elif y_ball - 10 == 40 and x_ball >= 280 and x_ball <= 330 and color6 != [0,0,0]:
            color6 = [0,0,0]
        elif y_ball - 10 == 40 and x_ball >= 335 and x_ball <= 395 and color7 != [0,0,0]:
            color7 = [0,0,0]
       
        # ending the game
        if y_ball > 470:
            run = False    
    
        dis.fill([0,0,0])

        if color1 == [0,0,0] and color2 == [0,0,0] and color3 == [0,0,0] and color4 == [0,0,0] and color5 == [0,0,0] and color6 == [0,0,0] and color7 == [0,0,0]:
            dis.fill([0,0,0])
            dis.blit(text2, textrect)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
    
        #ball
        pygame.draw.circle(dis, white, (x_ball,y_ball), 10, 0)
    
        # slider
        pygame.draw.rect(dis, green, [x_slider,460,length_of_slider,15])

        # red bricks
        pygame.draw.rect(dis, color1, [5,30,50,15])
        pygame.draw.rect(dis, color2, [60,30,50,15])
        pygame.draw.rect(dis, color3, [115,30,50,15])
        pygame.draw.rect(dis, color4, [170,30,50,15])
        pygame.draw.rect(dis, color5, [225,30,50,15])
        pygame.draw.rect(dis, color6, [280,30,50,15])
        pygame.draw.rect(dis, color7, [335,30,60,15])

        # text
        dis.blit(text, textRect)
    
        pygame.display.update()

        if delayer == 0:
            pygame.time.delay(2000)
            delayer+=1


    cam.release()
    pygame.quit()


maingame = True

while maingame:
    x, y = pygame.mouse.get_pos()
    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= 300 and x >= 110 and y <= 60 and y >= 10:
                dis.fill([255,255,255])
                pygame.display.update()
                mainloop(True, 200, x_ball, 80, 0, 0, 100, 0)
