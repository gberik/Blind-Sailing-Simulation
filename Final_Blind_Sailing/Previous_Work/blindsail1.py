# SOURCE FOR CODE AND KNOWLEDGE
# https://www.101computing.net/getting-started-with-pygame/
# casey & sander you can do next on the website to reach the other parts

import pygame, random
from boat1 import Boat

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
SCREENWIDTH=2000
SCREENHEIGHT=1200
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sailing Simulation")

#Make a sprites list and add Boat1
all_sprites_list = pygame.sprite.Group()
Boat1 = Boat((700, 400))
all_sprites_list.add(Boat1)

#HUD - Text on Screen
font = pygame.font.Font(None, 52)
wind_direction = font.render("Wind Direction", 1, WHITE)
TTS_info = pygame.image.load("images/KeypressLegend.png")
wind_arrow = pygame.image.load("images/WindArrow.png")
help_button = font.render("Press H for Instructions", 1, WHITE)
info_status = 1

#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()
currentBuoy = 0

#Main Loop
while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                    carryOn=False
                elif event.key==pygame.K_h:
                    info_status += 1

        #Boat1.distance()
        keys = pygame.key.get_pressed()
        #keys2 = pygame.KEYUP()
        if keys[pygame.K_LEFT]:
            Boat1.moveLeft(1)
        if keys[pygame.K_RIGHT]:
            Boat1.moveRight(1)
        if keys[pygame.K_UP]:
            Boat1.moveUp(1)
        if keys[pygame.K_DOWN]:
            Boat1.moveDown(1)
        if keys[pygame.K_COMMA]:
            Boat1.rotate_right()
        if keys[pygame.K_l]:
            keys[pygame.K_l] == False
            Boat1.rotate_left()

        #Game Logic
        all_sprites_list.update()

        #Drawing on Screen
        screen.fill(WATER)

        BuoyPos = [1000, 300, 666, 900, 1333, 900]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                if currentBuoy<4:
                    currentBuoy += 2
                else:
                    currentBuoy  = 0

                print(currentBuoy)

        #Draw The Buoys
        pygame.draw.circle(screen, RED, [BuoyPos[0],BuoyPos[1]],30, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[2],BuoyPos[3]],30, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[4],BuoyPos[5]],30, 0)

        #Print HUD
        pygame.draw.rect(screen,RED,(1600,1050,2000,1200))
        angle = str(Boat1.angle)
        boat_angle = font.render("Boat angle: " + angle, 1, WHITE)
        screen.blit(wind_direction, (50,50))
        screen.blit(wind_arrow, (50,100))
        screen.blit(boat_angle, (1650,1100))
        screen.blit(help_button, (50,1100))

        if info_status%2 == 0:
            screen.blit(TTS_info, (0,800))







        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)

        #Refresh Screen
        pygame.display.flip()

        #Number of frames per secong e.g. 60
        clock.tick(60)

pygame.quit()
