# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 10-11-2017

import numpy as np
import cv2
from picamera import PiCamera
from time import sleep
import matplotlib
from matplotlib import pyplot as plt
import math


#project .py files

from color_detection import color_detection
from Color import Color


def TakePictures(FotoNumber):
   
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.shutter_speed = 10000
    camera.awb_mode ='auto'
    camera.brightness = 60
    
    #take picture
    #image = camera.capture
    image = cv2.imread('/home/pi/Downloads/plastic_6.png')/255
    #convert image to LAB_image
    temp_image = image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)
    
    image = cv2.imread('/home/pi/Downloads/plastic_6.png')

    #camera.close()
    FotoNumber = color_detection(image, LAB_image)
    #Time needed to wait between pictures
    sleep(2.05)

#number of foto's that is going to de taken
FotoNumber = 1
TakePictures(FotoNumber)

color_detection.SetBoundary(120)
color_detection.SetWhiteBoundary(60)

#color definitions

Color('red', 67.5, 112.5)
Color('yellow', 157.7, 202.5)
Color('green', 247.5, 292.5)
Color('blue', 337.5, 22.5)

#loop over all image objects of the class color_detection
for image in color_detection.AllImages:
    image.detect()
    
color_detection.PrintAllPercentages()






    





                
               

