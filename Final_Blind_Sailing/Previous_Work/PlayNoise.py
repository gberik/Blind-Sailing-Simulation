
import os
# must pip install sox
# type sudo apt install sox into cmd
duration = .2  # seconds
freq = 550  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
