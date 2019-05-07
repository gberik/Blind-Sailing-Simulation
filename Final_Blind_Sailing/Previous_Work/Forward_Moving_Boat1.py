import math


#update the moveup in boat1.py to make the boat go in the desired direction
# is the movement feels wrong, change sin to cos and cos to sin
def moveUp(self, pixels):
    self.rect.y -= math.cos(math.radians(self.angle))*pixels
    self.rect.x += math.sin(math.radians(self.angle))*pixels
