import pyaudio as pa
import numpy as np
import os 
import time
import struct
import pyautogui as pag

#constants
CHUNK = 1024 * 2
FORMAT = pa.paInt16
CHANNEL = 1
RATE = 44100

#pyaudio class instant
p = pa.PyAudio()

#stream object to get data from microphone
stream = p.open(
    format = FORMAT,
    channels = CHANNEL,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)

print('stream stated')

while True:
    noFish = True
    while noFish:
        #binary data
        data = stream.read(CHUNK)

        #convert data to integers, make up the array
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

        # create np array
        data_np = np.array(data_int, dtype='b')[::2] + 128
        print(data_np[0])
        if data_np[0] > 200:
            pag.click(button = 'right')
            noFish = False

