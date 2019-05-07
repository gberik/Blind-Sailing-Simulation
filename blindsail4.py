# SOURCE FOR CODE AND KNOWLEDGE
# https://www.101computing.net/getting-started-with-pygame/

import math
#python3 -m pip install -U pygame --user
import pygame, random
import numpy
import time
from boat3 import Boat
import wave
#pip install pydub
from pydub import AudioSegment
#pip install soundfile
import soundfile
#pip install ffmpy
import ffmpy

#pip install gTTS
from gtts import gTTS

import os
import subprocess

#sudo apt update
#sudo apt install ffmpeg
import ffmpeg



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

#initialize global variables
info_status = 1
currentBuoy = 0
speech_speed = 0.9

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

def get_distance_sentence():
    str_distance = str(distance())
    dist_sentence = "Buoy " + str_distance + " meters away"
    return dist_sentence

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

def get_clock_heading_sentence():
    str_clock_heading = str(ClockHeading())
    heading_sentence = "Buoy at " + str_clock_heading + " o'clock"
    return heading_sentence

def get_cardinal_direction():

    boat_angle = Boat1.angle
    cardinal_direction = "The boat is heading "

    if 337.5 <= boat_angle <= 360 or 0 <= boat_angle < 22.5:
        cardinal_direction += "North"
    elif 22.5 <= boat_angle < 67.5:
        cardinal_direction += "North East"
    elif 67.5 <= boat_angle < 112.5:
        cardinal_direction += "East"
    elif 112.5 <= boat_angle < 157.5:
        cardinal_direction += "South East"
    elif 157.5 <= boat_angle < 202.5:
        cardinal_direction += "South"
    elif 202.5 <= boat_angle < 247.5:
        cardinal_direction += "South West"
    elif 247.5 <= boat_angle < 292.5:
        cardinal_direction += "West"
    elif 292.5 <= boat_angle < 337.5:
        cardinal_direction += "North West"
    return cardinal_direction


def texty(num):
    #assigning what messages the text to speech should say when certain buttons are pressed
    snippet = ''
    if num == 1:
        snippet = get_distance_sentence()
    elif num == 2:
        snippet = get_clock_heading_sentence()
    elif num == 3:
        snippet = 'The wind is blowing East'
    elif num == 4:
        snippet = get_cardinal_direction()
    elif num == 5:
        snippet = 'Advancing to next buoy'
    elif num == 6:
        snippet = "Slow speech mode"
    elif num == 7:
        snippet = "Fast speech mode"
    elif num == 8:
        snippet = "Very fast speech mode"
    return snippet


def read_text(mytext, speed):
    # The text that you want to convert to audio

    #
    # # Language in which you want to convert
    language = 'en'
    #
    # # Passing the text and language to the engine,
    # # here we have marked slow=False. Which tells
    # # the module that the converted audio should
    # # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    #
    # # Saving the converted audio in a mp3 file named
    # # welcome
    myobj.save("welcomey.mp3")

    subprocess.call(['ffmpeg', '-i', 'welcomey.mp3','newwelcomey.wav'])

    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

    spf = wave.open('newwelcomey.wav', 'rb')
    RATE=spf.getframerate()
    signal = spf.readframes(-1)
    print(RATE)

    wf = wave.open('newwelcomey.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*speed)
    wf.writeframes(signal)
    wf.close()

    # Playing the converted file
    os.system("aplay 'newwelcomey.wav'")

    spf = wave.open('newwelcomey.wav', 'rb')
    RATE=spf.getframerate()
    signal = spf.readframes(-1)
    print(RATE)
    wf = wave.open('newwelcomey.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*1/speed)
    wf.writeframes(signal)
    os.remove('newwelcomey.wav')
    wf.close()


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

                #Pressing 5 advances the current buoy
                if event.key == pygame.K_5:
                    if currentBuoy == 0:
                        currentBuoy += 2
                    elif currentBuoy == 2:
                        currentBuoy += 2
                    elif currentBuoy == 4:
                        currentBuoy = 0

                if event.key==pygame.K_1:
                    read_text(texty(1),speech_speed)
                if event.key==pygame.K_2:
                    read_text(texty(2),speech_speed)
                if event.key==pygame.K_3:
                    read_text(texty(3),speech_speed)
                if event.key==pygame.K_4:
                    read_text(texty(4),speech_speed)
                if event.key==pygame.K_5:
                    read_text(texty(5),speech_speed)
                if event.key==pygame.K_6:
                    speech_speed = 0.9
                    read_text(texty(6),speech_speed)
                if event.key==pygame.K_7:
                    speech_speed = 1.2
                    read_text(texty(7),speech_speed)
                if event.key==pygame.K_8:
                    speech_speed = 1.4
                    read_text(texty(8),speech_speed)



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






        #HUD Images & Text to display
        pygame.draw.rect(screen,RED,(1350,925,1850,1100))

        #Display distance to buoy
        distance_to_buoy = get_distance_sentence()
        distance_to_buoy_render = font.render(distance_to_buoy, 1, WHITE)
        screen.blit(distance_to_buoy_render, (1375,950))

        #Display clock heading to buoy
        buoy_clock_pos = get_clock_heading_sentence()
        buoy_clock_pos_render = font.render(buoy_clock_pos, 1, WHITE)
        screen.blit(buoy_clock_pos_render, (1375,1025))

        #Display other images & text on screen
        screen.blit(wind_direction, (50,50))
        screen.blit(wind_arrow, (50,100))
        screen.blit(help_button, (50,1000))

        #You can't sail towards wind warning display
        if Boat1.angle > 245 and Boat1.angle < 295:
            screen.blit(wind_warning, (1100,100))

        #open and close the info menu
        if info_status%2 == 0:
            screen.blit(TTS_info, (0,700))


        #Move the Boat
        keys = pygame.key.get_pressed()
        Boat1.moveUp(1)
        if keys[pygame.K_RIGHT]:
            Boat1.rotate_right()
        if keys[pygame.K_LEFT]:
            Boat1.rotate_left()

        #Refresh Screen
        update_screen()


pygame.quit()
