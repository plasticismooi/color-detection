# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 10-11-2017

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
    #amera.awb_mode ='auto'
    #camera.brightness = 60
    
    #take picture
    #image = camera.capture
    image = cv2.imread('C://Users//tom_l//OneDrive//HHS//Jaar_3//stage 2//test_image.png')/255
    #convert image to LAB_image
    temp_image = image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)
    
    image = cv2.imread('C://Users//tom_l//OneDrive//HHS//Jaar_3//stage 2//test_image.png')

    #camera.close()
    FotoNumber = color_detection(image, LAB_image)
    #Time needed to wait between pictures
    sleep(2.05)

#number of foto's that is going to de taken
FotoNumber = 1
TakePictures(FotoNumber)



#color definitions

Color('1st quadrant', 0, 90)
Color('2nd quadrant', 91, 180)
Color('3rd qudarant', 181, 270)
Color('4th quadrant', 271, 360)

#initialize values

color_detection.SetNumberOfDecimals(1) #max 14
color_detection.SetBeltColorRadius(70) # if 0 all colors are detected, including the conveyerbelt

color_detection.SetLowestWhiteValue(85)
color_detection.SetHighestBlackValue(20)
color_detection.SetLongestGreyRadius(10)


#loop over all image objects of the class color_detection
for image in color_detection.ListOfAllImages:
    image.StartColorDetection()

color_detection.PrintTotalPlasticPixelsOfAllImages()

color_detection.PrintAllPercentages()






    





                
               

