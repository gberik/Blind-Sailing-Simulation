#Code Used From:
#https://www.101computing.net/creating-sprites-using-pygame/

import pygame
from pygame.math import Vector2

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
        self.angle = 0


    def rotate(self):
        self.image = pygame.transform.rotozoom(self.rotated_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)

    def rotate_right(self):
        self.angle += 1
        self.rotate()

    def rotate_left(self):
        self.angle -= 1
        self.rotate()

    def moveRight(self, pixels):
        self.rect.x += pixels
        self.pos.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        self.pos.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels
        self.pos.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels
        self.pos.y += pixels
