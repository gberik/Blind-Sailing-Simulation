#Code Used From:
#https://www.101computing.net/creating-sprites-using-pygame/

import pygame
from pygame.math import Vector2
import math


WHITE = (255, 255, 255)
YELLOW = (255, 255, 63)


class Boat(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, pos):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent

        self.image = pygame.Surface((80,202), pygame.SRCALPHA)
        # self.image.fill(WHITE)
        # self.image.set_colorkey(WHITE)

        picture = pygame.image.load("images/yellow_boat.png")
        boat_image = pygame.transform.scale(picture, (80, 200))
        self.image = boat_image
        self.rotated_image = self.image

        self.rect = self.image.get_rect(center=(pos))
        self.pos = Vector2(pos)
        self.offset = Vector2(0, 0)
        self.angle = 270
        self.rotate()

        #pygame.draw.rect(picture, WHITE, 0, width = 0)


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

    def moveUp(self, pixels):
        #Don't move if pointed upwind
         if self.angle > 245 and self.angle < 295:
            self.pos.y = self.pos.y
            self.pos.x = self.pos.x 
            self.rect.y = self.rect.y
            self.rect.x = self.rect.x
            self.rect = self.image.get_rect(center=self.pos)
         else:
            self.pos.y -= math.cos(math.radians(self.angle))*pixels
            self.pos.x += math.sin(math.radians(self.angle))*pixels
            self.rect.y -= math.cos(math.radians(self.angle))*pixels
            self.rect.x += math.sin(math.radians(self.angle))*pixels
            self.rect = self.image.get_rect(center=self.pos)
         if self.pos.x < 0 or self.pos.x > 1850:
            self.pos.x = 1700
            self.pos.y = 500
            self.angle = 270
            self.rotate()

         if self.pos.y < 0 or self.pos.y > 1100:
            self.pos.x = 1700
            self.pos.y = 500
            self.angle = 270
            self.rotate()

    
   
        