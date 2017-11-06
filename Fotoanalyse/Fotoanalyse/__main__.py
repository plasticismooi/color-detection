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
   
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.shutter_speed = 10000
    camera.awb_mode ='auto'
    camera.brightness = 60

    #take picture
    image = camera.capture
    #makes object of each taken foto
    FotoNumber = color_detection(image)
    camera.close()

    #Time needed to wait between pictures
    sleep(2.05)

#number of foto's that is going to de taken
#FotoNumber = 1
#TakePictures(FotoNumber)


image = cv2.imread('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\plastic_4.png')
image1 = color_detection(image)
#color definitions
yellow = Color(90, 60)
orange = Color(30, 50)
blue = Color(3, 5)


Color.PrintHorizontalAngle(yellow)

#loop over all image objects of the class color_detection
for image in color_detection.AllImages:
    image.detect()

    





                
               
