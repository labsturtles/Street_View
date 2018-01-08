# coding: utf-8
#alu.21406@usj.es

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

import serial
from time import sleep

import process_view as pv

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

#from grabscreen import grab_screen
import cv2

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util
#from protos import string_int_label_map_pb2
#from object_detection.utils import label_map_util
from utils import visualization_utils as vis_util


# # Model preparation 
# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

print('DOWNLOAD')
# ## Download Model
#opener = urllib.request.URLopener()
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#tar_file = tarfile.open(MODEL_FILE)
#for file in tar_file.getmembers():
#  file_name = os.path.basename(file.name)
#  if 'frozen_inference_graph.pb' in file_name:
#    tar_file.extract(file, os.getcwd())




# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
#PATH_TO_LABELS = os.path.join('data','graph.pbtxt')


NUM_CLASSES = 90

print('READ FILE')
# ## Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

print('LOAD LABEL')
# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map,max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

print('HELP CODE')
# ## Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

print('SIZE')
# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


#---------------------------------------------------------------------------------------------------------#
#inicia la captura de imagen con OPENCV 
print('OPENCV')
with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:

    print ("Configuring video capture EasyCAP (V4L2) ...")
    os.system("v4l2-ctl -d /dev/video1 -i 0 -s 5 --set-fmt-video=width=640,height=480")

#    os.system("v4l2-ctl -d /dev/video1 -i 0 -s 5 --set-fmt-video=width=720,height=576")
# -d : device (in my case /dev/video0),
# -i : input. for my Easycap (0 = CVBS0; 1 = CVBS1; 2 = CVBS2; 3 = CVBS3; 4 = CVBS4; 5 = S-VIDEO)
# -s : norm (0 = PAL_BGHIN; 1 = NTSC_N_443; 2 = PAL_Nc; 3 = NTSC_N; 4 = SECAM; 5 = NTSC_M; 6 = NTSC_M_JP; 7 = PAL_60; 8 = NTSC_443; 9 = PAL_M;)

#   screen = cv2.resize(grab_screen(region=(0,40,1280,745)), (WIDTH,HEIGHT))
#   screen = cv2.resize(grab_screen(region=(0,40,1280,745)), (800,450))

    cap =  cv2.VideoCapture(1)
    #LOW: 240x320  MEDIUM: 320x480  HIGH 480x640
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    
#    cap =  cv2.VideoCapture('/home/jetson/Descargas/Pedestrians.mp4')
#    cap =  cv2.VideoCapture('/home/jetson/Descargas/VID_20171107_172836.3gp')

    fps = cap.get(cv2.CAP_PROP_FPS)
    if (str(fps)=='nan'):
       fps=30 
    witch = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print ("Frame default resolution: " + str(fps) + " -  " + str(witch) + " - " + str(height))

#---------------------------------------------------------------------------------------------------------#
    #Se define el area de deteccion
    pv.resolucionImagen(witch,height)
    pv.creaAreaDetect((witch/2)-200, (witch/2)+200, (height/2)-200, (height/2)+200)

#---------------------------------------------------------------------------------------------------------#  
    #Se inicia la comunicacion del puerto Serie  
  
    # Q  W  E
    # A  S  D
    # Z  X  C
    ctrlPad="@"
    timewait=0
    
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # open serial port       
    except:
        portOpen=False
        pass
    else:
        print(ser.name)         # check which port was really used
        portOpen=True
   

#---------------------------------------------------------------------------------------------------------#
    #Bucle de trabajo
    fg = fps
    #while(True):
    while(cap.isOpened()):
            if (portOpen==True):
               ser.write(ctrlPad[0].encode())
            ret, image_np = cap.read()
            if fg>0: #fps/24:
                fg = 0

                if (timewait==0):
                    ctrlPad="W"
                else:
                    timewait-=1


                #ret, image_np = cap.read()
                

		# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
		
                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
		      
                # Each score represent how level of confidence for each of the objects.
		# Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
		
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})


#### inicio TOMA DE DECISIONES ####

                print(pv.procesaElemento(
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                image_np )   
                ) 
       
#### fin TOMA DE DECISIONES ####             

	       # Visualization of the results of a detection.
               # vis_util.visualize_boxes_and_labels_on_image_array(
               # image_np,
               # np.squeeze(boxes),
               # np.squeeze(classes).astype(np.int32),
               # np.squeeze(scores),
               # category_index,
               # use_normalized_coordinates=True,
               # line_thickness=8)


               #      print(image_np.shape[1])
               #      r = (1180.0 / image_np.shape[1])
               #      dim = (1300, int(image_np.shape[0] * r))
               #      resized = cv2.resize(image_np, dim, interpolation=cv2.INTER_AREA)
               #      cv2.imshow('resized', resized)
               #     cv2.waitKey(0)

                cv2.imshow('window',image_np)
            else:
                fg += 1
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

cap.release() #release video file
cv2.destroyAllWindows()
