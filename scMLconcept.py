#need labels.pbtxt, models
#load model 
#cast fish 
#screencap
#find points
#go to points
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pathlib
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
import pyautogui as pag
import pyaudio as pa
import struct



import getBob 
import sonar


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


#prep work
PATH_TO_SAVED_MODEL = "mlComponent/saved_model"



#load the saved model
print('Loading model ...', end='')
start_time = time.time()
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))


while True:

    #need to wait because blizzard is shit
    time.sleep(1)
    #cast fish
    pag.press('e')
    time.sleep(3)

    #move coursor to bobber
    getBob.get_bob(detect_fn)
    sonar.find_fish(stream)
   

        

   
    
    