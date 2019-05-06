import wave
from pydub import AudioSegment
import soundfile
import ffmpy


# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os
import subprocess
import ffmpeg

def texty(num):
    #assigning what messages the text to speech should say when certain buttons are pressed
    snippet = ''
    if num == 1:
        distance = str(distance())
        textapp = 'boat lengths away from the nearest buoy'
        snippet = snippet + distance
        snippet = snippet + textapp
    elif num == 2:
        Angle2Buoy = str(AngleHeading())
        textapp = 'The boat is facing'
        snippet = snippet + Angle2Boat + 'degrees'
        snippet = textapp + snippet
    elif num == 3:
        clockFace = str(ClockHeading())
        textapp = 'The buoy is at'
        snippet = snippet + clockFace + "o'Clock"
        snippet = textapp + snippet

    elif num == 4:
        textapp = 'The wind is blowing East'
        snippet = textapp + snippet
    elif num == 5:
        currentBuoy = str(currentBuoy)
        textapp = 'Advancing to buoy'
        snippet = snippet + currentBuoy
        snippet = textapp + snippet
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

    subprocess.call(['ffmpeg', '-i', '/home/cmay/welcomey.mp3','/home/cmay/newwelcomey.wav'])
    #
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
    os.system("aplay /home/cmay/newwelcomey.wav")

    spf = wave.open('newwelcomey.wav', 'rb')
    RATE=spf.getframerate()
    signal = spf.readframes(-1)
    print(RATE)
    wf = wave.open('newwelcomey.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*1/speed)
    wf.writeframes(signal)
    os.remove("newwelcomey.wav")
    wf.close()

read_text(texty(1),1)

    # Saving the converted audio in a mp3 file named
    # welcome
    # from pydub import AudioSegment
    # sound = AudioSegment.from_mp3("/path/to/file.mp3")
    # sound.export("/output/path/file.wav", format="wav")
