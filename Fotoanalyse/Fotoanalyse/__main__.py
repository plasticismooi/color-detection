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
    image = camera.capture

    camera.close()
    FotoNumber = color_detection(image, LAB_image)
    #Time needed to wait between pictures
    sleep()

    image = cv2.imread('C://Users//tom_l//OneDrive//HHS//Jaar_3//stage 2//test_image.png')/255
    #convert image to LAB_image
    temp_image = image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)

    


x = WaitingTime.CalculateWaitingTime()
print (x)
    

RGB_image = cv2.imread('C://Users//tom_l//OneDrive//HHS//Jaar_3//stage 2//test_image.png')/255
#convert image to LAB_image
temp_image = RGB_image.astype(np.float32)
LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)

RGB_image = cv2.imread('C://Users//tom_l//OneDrive//HHS//Jaar_3//stage 2//test_image.png')

test_image = color_detection(RGB_image, LAB_image)
#color definitions

Color('1st quadrant', 0, 90)
Color('2nd quadrant', 91, 180)
Color('3rd qudarant', 181, 270)
Color('4th quadrant', 271, 360)

#initialize values


color_detection.SetNumberOfDecimals(2) #max 14
color_detection.SetBeltColorRadius(80) # if 0 all colors are detected, including the conveyerbelt

test_image.StartColorDetection()

color_detection.PrintAllPercentages()









##loop over all image objects of the class color_detection
#for image in color_detection.ListOfAllImages:
#    image.StartColorDetection()

#color_detection.PrintTotalPlasticPixelsOfAllImages()

#color_detection.PrintAllPercentages()






    





                
               

