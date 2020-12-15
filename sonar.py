import time
import struct
import numpy as np
import pyautogui as pag
CHUNK = 1024*2
def find_fish(stream):
    start_time = time.time()
    noFish = True
    soundtrigger = 0
    sound_prev = 120
    stream.start_stream()
    while noFish:
        
        #binary data
        data = stream.read(CHUNK)

        #convert data to integers, make up the array
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

        # create np array
        data_np = np.array(data_int, dtype='b')[::2] + 128
        end_time = time.time()
        fish_time = end_time - start_time

        #if difference is bigger than 50, the fish is hooked
        if abs(data_np[0] - sound_prev) > 50:
            soundtrigger += 1
            

        if soundtrigger == 3:
            time.sleep(1)
            pag.click(button = 'right')
            noFish = False
        elif fish_time > 20:
            noFish = False
            print("time trigger")
            
        sound_prev = data_np[0]
