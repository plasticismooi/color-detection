# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 2-11-2017

import numpy as np
import cv2
#from picamera import PiCamera
from time import sleep
import matplotlib
from matplotlib import pyplot as plt
import math


#project .py files

from color_detection import color_detection
from Color import Color


def TakePictures(FotoNumber):
   
    #camera = PiCamera()
    #camera.resolution = (1024, 768)
    
    #camera.shutter_speed = 10000
    #camera.awb_mode ='auto'
    #camera.brightness = 60
    
    #take picture
    #image = camera.capture
    image = cv2.imread('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\download.png')/255
    #convert image to LAB_image
    temp_image = image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)

    image = cv2.imread('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\download.png')


    FotoNumber = color_detection(image, LAB_image)
    #camera.close()

    #Time needed to wait between pictures
    sleep(2.05)

#number of foto's that is going to de taken
FotoNumber = 1
TakePictures(FotoNumber)


#color definitions

test1 = Color(1, 90)
test2 = Color(91, 180)
test3 = Color(181, 270)
test4 = Color(271, 360)

#loop over all image objects of the class color_detection
for image in color_detection.AllImages:
    image.detect()

Color.PrintPixelCount(test1)
Color.PrintPixelCount(test1)
Color.PrintPixelCount(test3)
Color.PrintPixelCount(test4)




    





                
               
