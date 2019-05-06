# SOURCE FOR CODE AND KNOWLEDGE
# https://www.101computing.net/getting-started-with-pygame/
# casey & sander you can do next on the website to reach the other parts
import math
import pygame, random
import numpy
#Let's import the Boat Class
from boat2 import Boat
pygame.init()

#colors
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = ( 0, 0, 0)
WATER = (68, 183, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 63)

SCREENWIDTH=1850
SCREENHEIGHT=1100

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sailing Simulation")

#Wind-Text Properties
#Wind
font = pygame.font.Font(None, 52)
text = font.render("Wind Direction", 1, WHITE)
wind = pygame.image.load("images/WindArrow.png")

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

Boat1 = Boat((1700, 500))



# Add the car to the list of objects
all_sprites_list.add(Boat1)

#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()
currentBuoy = 0


def distance():
    distance = round(math.sqrt(((Boat1.pos.x-BuoyPos[currentBuoy])**2)+(Boat1.pos.y-BuoyPos[currentBuoy+1])**2)/200)
    #print(distance)
    return distance

def AngleHeading():
    BoatCartx = Boat1.pos.x
    BoatCarty = -(Boat1.pos.y - SCREENHEIGHT)
    BuoyCartx = BuoyPos[currentBuoy]
    BuoyCarty = -(BuoyPos[currentBuoy+1] - SCREENHEIGHT)
    v = (BuoyCartx - BoatCartx, BuoyCarty - BoatCarty)
    u = (math.sin(math.radians(Boat1.angle)), math.cos(math.radians(Boat1.angle)))
    if numpy.cross(u,v) <= 0:
        if (numpy.dot(u, v)/(numpy.linalg.norm(u))) >= 0:
            Angle2Buoy = round(math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
        else:
            Angle2Buoy = round(math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
    elif numpy.cross(u,v) > 0:
        if (numpy.dot(u, v)/(numpy.linalg.norm(u))) >= 0:
            Angle2Buoy = round(360 - math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
        else:
            Angle2Buoy = round(360 - math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
    return Angle2Buoy

def ClockHeading():
    Angle2Buoy = AngleHeading()    
    if Angle2Buoy >= 345 and Angle2Buoy <= 360 or Angle2Buoy >= 0 and Angle2Buoy < 15:
        clockFace = 12
    elif Angle2Buoy >= 15 and Angle2Buoy < 45:
        clockFace = 1
    elif Angle2Buoy >= 45 and Angle2Buoy < 75:
        clockFace = 2
    elif Angle2Buoy >= 75 and Angle2Buoy < 105:
        clockFace = 3  
    elif Angle2Buoy >= 105 and Angle2Buoy < 135:
        clockFace = 4 
    elif Angle2Buoy >= 135 and Angle2Buoy < 165:
        clockFace = 5
    elif Angle2Buoy >= 165 and Angle2Buoy < 195:
        clockFace = 6
    elif Angle2Buoy >= 195 and Angle2Buoy < 225:
        clockFace = 7
    elif Angle2Buoy >= 225 and Angle2Buoy < 255:
        clockFace = 8
    elif Angle2Buoy >= 255 and Angle2Buoy < 285:
        clockFace = 9
    elif Angle2Buoy >= 285 and Angle2Buoy < 315:
        clockFace = 10
    elif Angle2Buoy >= 315 and Angle2Buoy < 345:
        clockFace = 11
    print(clockFace)
    return clockFace

while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
                if event.key == pygame.K_b:
                    if currentBuoy == 0:
                        currentBuoy += 2
                
                    elif currentBuoy == 2:
                        currentBuoy += 2
                   
                    elif currentBuoy == 4:
                        currentBuoy = 0
                        
                if event.key == pygame.K_d:
                    #distance()
                    ClockHeading()
                    
        #Boat1.distance()
       

        #Game Logic
        all_sprites_list.update()

        #Drawing on Screen
        screen.fill(WATER)

        BuoyPos = [200, 500, 1500, 300, 1500, 800]
                

                    
        #Draw The Buoys
        pygame.draw.circle(screen, RED, [BuoyPos[0],BuoyPos[1]],30, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[2],BuoyPos[3]],30, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[4],BuoyPos[5]],30, 0)
        pygame.draw.circle(screen, GREEN, [BuoyPos[currentBuoy],BuoyPos[currentBuoy+1]],30, 0)
        


        #Wind - Text
        screen.blit(text, (50,50))
        screen.blit(wind, (50,100))

        
        if distance() < 2:
            print('Warning')
        keys = pygame.key.get_pressed()
        Boat1.moveUp(1)
      
        if keys[pygame.K_RIGHT]:
            Boat1.rotate_right()
        if keys[pygame.K_LEFT]:
            Boat1.rotate_left()
        
        #pygame.draw.circle(screen, GREEN, [int(Boat1.pos.x),int(Boat1.pos.y)+40],30, 0)
        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)

        #Refresh Screen
        pygame.display.flip()

        #Number of frames per secong e.g. 60
        clock.tick(60)

pygame.quit()
