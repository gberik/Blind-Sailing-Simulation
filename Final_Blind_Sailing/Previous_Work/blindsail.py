# SOURCE FOR CODE AND KNOWLEDGE
# https://www.101computing.net/getting-started-with-pygame/
# casey & sander you can do next on the website to reach the other parts

import pygame, random
#Let's import the Boat Class
from boat import Boat
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
SCREENHEIGHT=1025

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sailing Simulation")

#Wind-Text Properties
#Wind
font = pygame.font.Font(None, 52)
text = font.render("Wind", 1, WHITE)
wind = pygame.image.load("images/WindArrow.png")
wind = pygame.transform.scale(wind, (200, 120))

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

Boat1 = Boat(BLUE, 20, 30)
Boat1.rect.x = 200
Boat1.rect.y = 300

# Add the car to the list of objects
all_sprites_list.add(Boat1)

#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()

while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Boat1.moveLeft(1)
        if keys[pygame.K_RIGHT]:
            Boat1.moveRight(1)
        if keys[pygame.K_UP]:
            Boat1.moveUp(1)
        if keys[pygame.K_DOWN]:
            Boat1.moveDown(1)
        if keys[pygame.K_COMMA]:
            #Boat1.rot_center(5)
            print(type(Boat1.rot_center(5)))
        #Game Logic
        all_sprites_list.update()

        #Drawing on Screen
        screen.fill(WATER)

        #Draw The Buoys
        pygame.draw.circle(screen, RED, [1600,312],15, 0)
        pygame.draw.circle(screen, RED, [330,512],15, 0)
        pygame.draw.circle(screen, RED, [1600,712],15, 0)

        #Wind - Text
        screen.blit(text, (65,455))
        screen.blit(wind, (10,452))



        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)

        #Refresh Screen
        pygame.display.flip()

        #Number of frames per secong e.g. 60
        clock.tick(60)

pygame.quit()
