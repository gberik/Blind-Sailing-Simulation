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
    if num == 0:
        textapp = 'The other boat is'
    elif num == 1:
        textapp = 'The nearest buoy is'
    elif num == 2:
        textapp = 'The boat is moving at'
    elif num == 3:
        textapp = 'The boat is facing'
    elif num == 4:
        textapp = 'The wind direction is'
    elif num == 5:
        textapp = 'Advancing to next buoy'
    return textapp

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

read_text(texty(3),1)

    # Saving the converted audio in a mp3 file named
    # welcome
    # from pydub import AudioSegment
    # sound = AudioSegment.from_mp3("/path/to/file.mp3")
    # sound.export("/output/path/file.wav", format="wav")
