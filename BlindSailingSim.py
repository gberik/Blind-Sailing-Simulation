import pygame as pg, sys
from pygame.locals import *
import enum
import math

# Define some colors
CAMOGREEN = (108, 137, 13)
RICHGREEN = (50, 137, 13)
LUSHGREEN = (0, 158, 26)
CAMOBROWN = (85, 86, 5)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COOKEDSALMON = (168, 25, 65)
GINGER = (224, 72, 6)
ORANGE = (247, 160, 0)
DRIEDBLOOD = (147, 0, 0)
PLUM = (114, 4, 59)
VELVET = (71, 4, 114)
BLU = (68, 183, 255)
TURQOUISE = (1, 158, 134)
GREY = (170, 174, 181)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Potential Tank Color Schemes

###HOT###
#ORNG, CKSLMN, PLUM
#GING, PLUM, ORANG
#ORNG, GING, DRYBLD

###COLD###
#TURQ, BLU, VEL
#LUSH, VEL, BLU
#CAMOB, RICH, CAMOG


WALL = 0
PATH = 1

colors = {WALL : BLU,
          PATH : BLU}

map = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL],
    [WALL, PATH, WALL, PATH, WALL, WALL, PATH, WALL, PATH, PATH, PATH, WALL, PATH, WALL, WALL, PATH, WALL, PATH, WALL],
    [WALL, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, WALL],
    [WALL, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, WALL],
    [WALL, PATH, PATH, PATH, PATH, WALL, WALL, PATH, PATH, WALL, PATH, PATH, WALL, WALL, PATH, PATH, PATH, PATH, WALL],
    [WALL, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, WALL],
    [WALL, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, WALL],
    [WALL, PATH, WALL, PATH, WALL, WALL, PATH, WALL, PATH, PATH, PATH, WALL, PATH, WALL, WALL, PATH, WALL, PATH, WALL],
    [WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]
    ]

TILESIZE = 100

MAPWIDTH = 19
MAPHEIGHT = 11


pg.init()

# Set the width and height of the screen (width,height)
DISPLAYSURF = pg.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

wall_list = []
for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            if colors[map[row][column]] == BLACK:
                wall_list.append(pg.draw.rect(DISPLAYSURF, colors[map[row][column]], (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE)))

#Label window
pg.display.set_caption("Tank Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pg.time.Clock()


class Tank():
    #Random color for surface fill
    BOO = (8,0,0)

    def __init__(self, color1, color2, color3, x, y, up, down, right, left, clockwise, counterclockwise):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.size = 40
        self.start_x = x
        self.start_y = y
        self.x = self.start_x
        self.y = self.start_y
        self.turret_theta = 0
        self.surf = pg.Surface((60,60))
        self.score = 0

        # Rectangle marking tank boundry
        self.rect = pg.Rect(self.x-20, self.y - 20, self.size, self.size)

        #controls
        self.up =  up
        self.down = down
        self.right = right
        self.left = left
        self.clockwise = clockwise
        self.counterclockwise = counterclockwise

        #Collision detection rectangles
        self.left_collider = pg.Rect(self.x-23, self.y-20, 4, 40)
        self.right_collider = pg.Rect(self.x+20, self.y-20, 4, 40)
        self.top_collider = pg.Rect(self.x-20, self.y-23, 40, 4)
        self.bottom_collider = pg.Rect(self.x-20, self.y+20, 40, 4)


        self.surf.fill(Tank.BOO)
        # Makes fill color transparent
        self.surf.set_colorkey(Tank.BOO)


    def draw_tank(self, DISPLAYSURF):
        #Tank body
        pg.draw.rect(DISPLAYSURF, self.color1,(self.x-20, self.y - 20, self.size, self.size), 0 )
        #Turrent body
        pg.draw.circle(DISPLAYSURF, self.color2, [self.x, self.y], 18, 0)
        #Turret
        pg.draw.rect(self.surf, self.color3, [32,25, 28, 10], 0)


    def rotate(self, surface, rect, angle):
        # Rotate about the center
        new_image = pg.transform.rotate(surface, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect


    def turret_motion(self):
        #get centerd rectangle
        rect = self.surf.get_rect(center = (self.x,self.y))
        #return turret location
        image, rect = self.rotate(self.surf, rect, self.turret_theta)
        #copy turret to screen
        DISPLAYSURF.blit(image, rect)


    def motion(self, tank, wall_list, other_tank):

            # User pushes down on a key
            if pg.key.get_pressed()[self.right] and (CollisionStatus.RIGHT not in collision_detection(tank, wall_list, other_tank)):
                self.x += 3
            if pg.key.get_pressed()[self.left] and (CollisionStatus.LEFT not in collision_detection(tank, wall_list, other_tank)):
                self.x += -3

            if pg.key.get_pressed()[self.up] and (CollisionStatus.TOP not in collision_detection(tank, wall_list, other_tank)):
                self.y += -3
            if pg.key.get_pressed()[self.down] and (CollisionStatus.BOTTOM not in collision_detection(tank, wall_list, other_tank)):
                self.y += 3

            if pg.key.get_pressed()[self.clockwise]:
                self.turret_theta += -5
            if pg.key.get_pressed()[self.counterclockwise]:
                self.turret_theta += 5


    def update_state(self):
        self.rect = pg.Rect(self.x-20, self.y - 20, self.size, self.size)
        self.left_collider = pg.Rect(self.x-23, self.y-20, 4, 40)
        self.right_collider = pg.Rect(self.x+20, self.y-20, 4, 40)
        self.top_collider = pg.Rect(self.x-20, self.y-23, 40, 4)
        self.bottom_collider = pg.Rect(self.x-20, self.y+20, 40, 4)


    def create_tank(self, DISPLAYSURF, wall_list, other_tank):
        self.draw_tank(DISPLAYSURF)
        self.motion(self, wall_list, other_tank)
        self.turret_motion()
        self.update_state()

class Bullet():

    def __init__(self, tank, other_tank):
        self.tank = tank
        self.marker = True

    def bullet_start(self):
        self.x = self.tank.x
        self.y = self.tank.y
        self.direction = self.tank.turret_theta

    def draw_bullet(self):
        pg.draw.rect(DISPLAYSURF, RED, (self.x, self.y, 4, 4), 0)


    def bullet_motion(self):
        self.y += (-5*math.sin(math.radians(self.direction)))
        self.x += (5*math.cos(math.radians(self.direction)))
        self.rect = pg.Rect(self.x, self.y, 4, 4)


    def create_bullet(self):
        if self.marker == True:
            self.bullet_start()
            self.marker = False
        self.draw_bullet()
        self.bullet_motion()

class CollisionStatus(enum.Enum):

    LEFT = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5


def collision_detection(tank, wall_list, other_tank):
    collisions = []
    if tank.left_collider.collidelist(wall_list+other_tank) != -1:
        collisions.append(CollisionStatus.LEFT)
    if tank.right_collider.collidelist(wall_list+other_tank) != -1:
        collisions.append(CollisionStatus.RIGHT)
    if tank.top_collider.collidelist(wall_list+other_tank) != -1:
        collisions.append(CollisionStatus.TOP)
    if tank.bottom_collider.collidelist(wall_list+other_tank) != -1:
        collisions.append(CollisionStatus.BOTTOM)
    return collisions



def fire(shooter, shooter_list, target, key):

    if event.type == pg.KEYDOWN:
        if event.key == key and len(shooter_list) < 15:
            bullet = Bullet(shooter, target)
            bullet.x = shooter.x
            bullet.y = shooter.y
            shooter_list.append(bullet)

    for bullet in shooter_list:
        bullet.create_bullet()

        if bullet.rect.collidelist(wall_list) != -1:
            shooter_list.remove(bullet)
        if bullet.rect.colliderect(target.rect):
            bullet.tank.score +=1
            target.x = target.start_x
            target.y = target.start_y
            shooter_list.remove(bullet)


hot_tank = Tank(ORANGE, GINGER, DRIEDBLOOD, 1650, 950, pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT, pg.K_COMMA, pg.K_m)
cold_tank = Tank(LUSHGREEN,VELVET, BLU, 250, 150, pg.K_r, pg.K_f, pg.K_g, pg.K_d, pg.K_1, pg.K_2)
hot_bullet_list = []
cold_bullet_list = []

pg.font.init()
myfont = pg.font.SysFont('chilanka', 30)
hot_score = myfont.render('Hot Tank Score: ' + str(hot_tank.score), False, RED)
cold_score = myfont.render('Cold Tank Score: '+ str(hot_tank.score), False, BLUE)
#print(pg.font.get_fonts())  This is a list of fonts we can use including chilanka


# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True


    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            pg.draw.rect(DISPLAYSURF, colors[map[row][column]], (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))



    cold_tank.create_tank(DISPLAYSURF,wall_list, [hot_tank.rect])
    hot_tank.create_tank(DISPLAYSURF, wall_list, [cold_tank.rect])


    fire(hot_tank, hot_bullet_list, cold_tank, pg.K_PERIOD)
    fire(cold_tank, cold_bullet_list, hot_tank, pg.K_3)

    hot_score = myfont.render('Hot Tank Score: '+ str(hot_tank.score), False, RED)
    cold_score = myfont.render('Cold Tank Score: '+ str(cold_tank.score), False, BLUE)

    DISPLAYSURF.blit(hot_score,(1350,60))
    DISPLAYSURF.blit(cold_score,(300,60))

    # Go ahead and update the screen with what we've drawn.
    pg.display.flip()

    # Used to manage how fast the screen updates
    clock = pg.time.Clock()
    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pg.quit()