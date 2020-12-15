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
PATH_TO_IMAGE = "./image1.jpg"

#saved image in images/finaltest
def get_image():
    image_paths = pathlib.Path(PATH_TO_IMAGE)
    return image_paths

IMAGE_PATH = get_image()

#putting everything together
def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

def get_bob(detect_fn):
    #capture image
    pag.screenshot(PATH_TO_IMAGE)

    #find points
    print('Running inference for {}...'.format(IMAGE_PATH), end='')
    #load the image into numpy
    image_np = load_image_into_numpy_array(IMAGE_PATH)
    #load the image into the tensor
    input_tensor = tf.convert_to_tensor(image_np)
    #add if there are batch of images
    input_tensor = input_tensor[tf.newaxis, ...]
    #run detection on the image
    detections = detect_fn(input_tensor)
    #pop the total number of detections 
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}

    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    


    #extract the mid point of the box
    xmax = detections['detection_boxes'][0][3]
    xmin = detections['detection_boxes'][0][1]
    ymax = detections['detection_boxes'][0][0]
    ymin = detections['detection_boxes'][0][2]
    xmid = (((xmax - xmin)/2) + xmin) * 1920
    ymid = (((ymax - ymin)/2) + ymin) * 1080
    print('xmid {}'.format(xmid))
    print('ymid {}'.format(ymid))

    #move mouse
    pag.moveTo(xmid,ymid)
