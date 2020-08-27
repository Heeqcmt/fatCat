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
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
import pyautogui as pag


#prep work
PATH_TO_SAVED_MODEL = "c:/Users/BerMau/Documents/Tensorflow/workplace/bobber/exported-models/my_model/saved_model"
PATH_TO_LABELS = "c:/Users/BerMau/Documents/Tensorflow/workplace/bobber/annotations/label_map.pbtxt"
PATH_TO_IMAGE = "c:/Users/BerMau/Desktop/image1.jpg"
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
#saved image in images/finaltest
def get_image():
    image_paths = pathlib.Path(PATH_TO_IMAGE)
    return image_paths
IMAGE_PATH = get_image()
#putting everything together
def load_image_into_numpy_array(path):
    return np.array(Image.open(path))




#load the saved model
print('Loading model ...', end='')
start_time = time.time()
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))
#load label map for plotting
category_index = label_map_util.create_categories_from_labelmap(PATH_TO_LABELS, use_display_name=True)


while True:
    #cast fish
    pag.press('e')
    time.sleep(2)
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
    image_np_with_detections = image_np.copy()
#draw the box on to the image
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.30,
        agnostic_mode=False)

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

    plt.figure()
    plt.imshow(image_np_with_detections)
    print('Done')
    plt.savefig("afterlabel.jpg")

    time.sleep(10)

    