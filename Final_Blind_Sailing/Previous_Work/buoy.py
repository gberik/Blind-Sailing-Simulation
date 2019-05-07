import pygame
WHITE = (255, 255, 255)
YELLOW = (255, 255, 63)

class Boat(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)


        picture = pygame.image.load("images/yellow_boat.png")
        boat_image = pygame.transform.scale(picture, (80, 200))
        self.image = boat_image.convert_alpha()
        self.rotated_image = self.image

        # Draw the car (a rectangle!)
        #pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Instead we could load a proper pciture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.rotated_image.get_rect()
