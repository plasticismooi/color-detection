# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 20-11-2017

import numpy as np
import cv2
#from picamera import PiCamera
from time import sleep
import matplotlib
from matplotlib import pyplot as plt
import math
import numpy.ma as ma

#project .py files
from color_detection import color_detection
from Color import Color
from WaitingTime import WaitingTime


def TakePictures(FotoNumber):
   
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.shutter_speed = 10000
    amera.awb_mode ='auto'
    camera.brightness = 60
    
    #take picture
    RGB_image = camera.capture

    camera.close()
    RGB_image = RGB_image/255
    #convert image to LAB_image
    temp_image = RGB_image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)

    FotoNumber = color_detection(RGB_image, LAB_image)

    sleep(WaitingTime.PictureInterval)
   



#color definitions

Color('1st quadrant', 0, 90)
Color('2nd quadrant', 91, 180)
Color('3rd qudarant', 181, 270)
Color('4th quadrant', 271, 360)

#initialize values


color_detection.SetNumberOfDecimals(2) #max 14
color_detection.SetBeltColorRadius(80) # if 0 all colors are detected, including the conveyerbelt

for image in color_detection.ListOfAllImages:

    image.StartColorDetection()

color_detection.PrintAllPercentages()















    





                
               

