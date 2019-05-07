import pygame
from pygame.math import Vector2
import math

#colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 63)

#Create Boat class as a sprite
class Boat(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((80,202), pygame.SRCALPHA)

        #Set and scale the sprite image
        picture = pygame.image.load("images/yellow_boat.png")
        boat_image = pygame.transform.scale(picture, (80, 200))
        self.image = boat_image
        self.rotated_image = self.image

        #Define properties of the Boat sprite
        self.rect = self.image.get_rect(center=(pos))
        self.pos = Vector2(pos)
        self.offset = Vector2(0, 0)
        self.angle = 270
        self.rotate()


    #rotate the sprite and equalize pos, image and rect
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.rotated_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)

    def rotate_right(self):
        #Keep angle between 0 and 360
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        #Rotate Right
        self.angle += 1
        self.rotate()

    def rotate_left(self):
        #Keep angle between 0 and 360
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        #Rotate Left
        self.angle -= 1
        self.rotate()

    #respawn the boat
    def reset_boat(self):
        self.pos.x = 1700
        self.pos.y = 500
        self.angle = 270
        self.rotate()

    #Go forward
    def moveUp(self, pixels):
        #Don't move if pointed towards wind
         if self.angle > 245 and self.angle < 295:
            self.pos.y = self.pos.y
            self.pos.x = self.pos.x
            self.rect.y = self.rect.y
            self.rect.x = self.rect.x
            self.rect = self.image.get_rect(center=self.pos)
        #Move otherwise
         else:
            self.pos.y -= math.cos(math.radians(self.angle))*pixels
            self.pos.x += math.sin(math.radians(self.angle))*pixels
            self.rect.y -= math.cos(math.radians(self.angle))*pixels
            self.rect.x += math.sin(math.radians(self.angle))*pixels
            self.rect = self.image.get_rect(center=self.pos)
