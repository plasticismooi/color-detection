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
from Color import Color
from color_detection import color_detection


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

#color definitions
yellow = Color(90, 60)
orange = Color(30, 50)
blue = Color(3, 5)

print(yellow.__dict__)
Color.PrintHorizontalAngle
Color.PrintAllColors


#loop over all image object of the class color_detection
for image in color_detection._registery:

    color_detection.SetBoundary(155)
    height, width, channels = image.shape

    for loopvariableY in range(height):
        for loopvariableX in range(width):

            bgr_array = image[loopvariableY, loopvariableX]
            if(((bgr_array[0]**2) + (bgr_array[1]**2) + (bgr_array[2]**2)) > image.boundary**2):

                #image.detect
                pass
