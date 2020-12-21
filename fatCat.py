import tkinter as tk 
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
import threading



import getBob 
import sonar

def loop(id,stop_fish):
    while stop_fish():
        #need to wait because blizzard is shit
        time.sleep(1)
        #cast fish
        pag.press('e')
        time.sleep(3)

        #move coursor to bobber
        getBob.get_bob(detect_fn)
        sonar.find_fish(stream)
        

#fishing thread
stop = False
fish_thread = threading.Thread(target=loop,args=(1,lambda: stop
))
def fish():
    global fish_thread
    global stop 
    stop = True
    label_info['text']="Fishing"
    fish_thread.start()

def rest():
    global fish_thread
    global stop
    stop = False
    print("resting")
    label_info['text']="Resting"
    fish_thread.join()




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
print('Loading model ...')
start_time = time.time()
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))






#building main UI
window = tk.Tk()
window.title("Fat Cat")
window.columnconfigure(0,weight=1,minsize=225)
window.rowconfigure(0,weight=1,minsize=75)
window.rowconfigure(1,weight=1,minsize=75)
window.rowconfigure(2,weight=1,minsize=75)

frame_title = tk.Frame(master=window)
frame_info = tk.Frame(master=window)
frame_selection = tk.Frame(master=window)

frame_title.grid(row=0,column=0)
frame_info.grid(row=1,column=0)
frame_selection.grid(row=2,column=0)

label_title = tk.Label(master= frame_title, text="Fat Cat Needs Fishes")
label_title.pack()

label_info = tk.Label(master=frame_info, text="status_text")
label_info.pack()

button_fish = tk.Button(master= frame_selection,text="Fish~",command=fish)
button_fish.grid(row=0,column=0)

button_rest = tk.Button(master=frame_selection,text="Rest",command=rest)
button_rest.grid(row=0,column=1)





# window.after(1000,loop)
window.mainloop()
