# SOURCE FOR CODE AND KNOWLEDGE
# https://www.101computing.net/getting-started-with-pygame/
# casey & sander you can do next on the website to reach the other parts
import math
import pygame, random
import numpy
import time
from boat3 import Boat
pygame.init()

#Colors
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = ( 0, 0, 0)
WATER = (68, 183, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 63)

#Screen Properties
SCREENWIDTH=1850
SCREENHEIGHT=1100
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sailing Simulation")

#Make a sprites list and add Boat1
all_sprites_list = pygame.sprite.Group()
Boat1 = Boat((1700, 500))
all_sprites_list.add(Boat1)

#Initialize HUD: Text - Image on Screen
font = pygame.font.Font(None, 52)
wind_direction = font.render("Wind Direction", 1, WHITE)
TTS_info = pygame.image.load("images/KeypressLegend.png")
wind_arrow = pygame.image.load("images/WindArrow.png")
help_button = font.render("Press H for Instructions", 1, WHITE)
wind_warning = font.render("You can't sail directly into the wind", 1, WHITE)
buoy_warning = font.render("Don't hit the buoys!", 1, WHITE)
off_screen_warning = font.render("Don't go off screen", 1, WHITE)
info_status = 1
currentBuoy = 0

#Let's put a better comment - Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()

#Refreshes Screen
def update_screen():
    all_sprites_list.draw(screen)
    pygame.display.flip()
    #Set the frames per second to desired number
    clock.tick(60)

#Define functions that restart the boat with the correct warnings
def restart_boat_with_delay_hitted_buoy():
    screen.blit(buoy_warning, (1100,100))
    Boat1.reset_boat()
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()
    time.sleep(1)

def restart_boat_with_delay_went_off_screen():
    screen.blit(off_screen_warning, (1100,100))
    Boat1.reset_boat()
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()
    time.sleep(1)

#Distance to current buoy
def distance():
    #200 pixels representsent a 4.2 meter boat
    pixels_to_meters_rate = .021
    distance = round(math.sqrt(((Boat1.pos.x-BuoyPos[currentBuoy])**2)+(Boat1.pos.y-BuoyPos[currentBuoy+1])**2)*pixels_to_meters_rate)
    return distance

#Angle to current buoy
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

#Angle in terms of clock heading to current buoy
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
    #print(clockFace)
    return clockFace

#Main Loop
while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False

            #Pressing the x Key will quit the game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x:
                     carryOn=False

                #Pressing h open/close the info menu
                if event.key==pygame.K_h:
                    info_status += 1

                #Pressing b advances the current buoy
                if event.key == pygame.K_b:
                    if currentBuoy == 0:
                        currentBuoy += 2

                    elif currentBuoy == 2:
                        currentBuoy += 2

                    elif currentBuoy == 4:
                        currentBuoy = 0

                #BETTER COMMENT HERE
                if event.key == pygame.K_d:
                    print(distance)
                    ClockHeading()

        #Update Sprites
        all_sprites_list.update()
        screen.fill(WATER)

        #Draw The Buoys
        BuoyPos = [200, 500, 1500, 300, 1500, 800]
        radius = 30
        pygame.draw.circle(screen, RED, [BuoyPos[0],BuoyPos[1]],radius, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[2],BuoyPos[3]],radius, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[4],BuoyPos[5]],radius, 0)
        #Make Current Buoy Green
        pygame.draw.circle(screen, GREEN, [BuoyPos[currentBuoy],BuoyPos[currentBuoy+1]],30, 0)

        #HUD Images & Text
        pygame.draw.rect(screen,RED,(1350,925,1850,1100))

        str_distance = str(distance())
        distance_to_buoy = font.render("Distance to Buoy: " + str_distance + " meters", 1, WHITE)
        screen.blit(distance_to_buoy, (1375,950))

        str_clockFace = str(ClockHeading())
        buoy_clock_pos = font.render("Buoy Direction: " + str_clockFace + " o'clock", 1, WHITE)
        screen.blit(buoy_clock_pos, (1375,1025))


        screen.blit(wind_direction, (50,50))
        screen.blit(wind_arrow, (50,100))
        screen.blit(help_button, (50,1000))
        if Boat1.angle > 245 and Boat1.angle < 295:
            screen.blit(wind_warning, (1100,100))
        if info_status%2 == 0:
            screen.blit(TTS_info, (0,700))


        #Collision Detection with Buoys
        if (BuoyPos[0]-radius*1.5 < Boat1.pos.x < BuoyPos[0]+radius*1.5) and (BuoyPos[1]-radius*1.5 < Boat1.pos.y < BuoyPos[1]+radius*1.5):
            restart_boat_with_delay_hitted_buoy()

        elif (BuoyPos[2]-radius*1.5 < Boat1.pos.x < BuoyPos[2]+radius*1.5) and (BuoyPos[3]-radius*1.5 < Boat1.pos.y < BuoyPos[3]+radius*1.5):
            restart_boat_with_delay_hitted_buoy()

        elif (BuoyPos[4]-radius*1.5 < Boat1.pos.x < BuoyPos[4]+radius*1.5) and (BuoyPos[5]-radius*1.5 < Boat1.pos.y < BuoyPos[5]+radius*1.5):
            restart_boat_with_delay_hitted_buoy()

        #Stay in Screen
        if Boat1.pos.x < 0 or Boat1.pos.x > 1850:
           restart_boat_with_delay_went_off_screen()

        if Boat1.pos.y < 0 or Boat1.pos.y > 1100:
           restart_boat_with_delay_went_off_screen()


        #Replace the sound here
        #if distance < 2:
            #print('Warning')

        #Move the Boat
        keys = pygame.key.get_pressed()
        Boat1.moveUp(1)
        if keys[pygame.K_RIGHT]:
            Boat1.rotate_right()
        if keys[pygame.K_LEFT]:
            Boat1.rotate_left()

        #Refresh Screen
        distance()
        ClockHeading()
        update_screen()


pygame.quit()
