# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 20-11-2017

import numpy as np
import datetime
import cv2
from picamera import PiCamera
from time import sleep
import math
import numpy.ma as ma
import glob

#project .py files
from color_detection import color_detection
from Color import Color
from WaitingTime import WaitingTime


def TakePicture():
   
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.shutter_speed = 10000
    camera.awb_mode ='auto'
    camera.brightness = 60
    
    camera.start_preview()
    camera.capture('/media/pi/9E401DB5401D94DD/Pictures/{:%Y-%m-%d %H:%M:%S}.png'.format(datetime.datetime.now())) 

    camera.close()
    
def PrepareImages():
    path = '/media/pi/9E401DB5401D94DD/Pictures/*.png'
    files = glob.glob(path)
    for RGB_image in files:
        RGB_image = cv2.imread(RGB_image)
        AddImageToObject(RGB_image)
        
def AddImageToObject(RGB_image):
    LAB_image = ConvertRGBtoLAB(RGB_image)
        
    color_detection(RGB_image, LAB_image)


def ConvertRGBtoLAB(RGB_image):
    
    temp_image = RGB_image/255
    temp_image = temp_image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)
    
    return LAB_image
    

for NumberOfTakenImages in range(0, 1):
    TakePicture()
    
PrepareImages()

    

    
Color('1st quadrant', 0, 90)
Color('2nd quadrant', 91, 180)
Color('3rd qudarant', 181, 270)
Color('4th quadrant', 271, 360)

#initialize values


color_detection.SetNumberOfDecimals(2) #max 14
color_detection.SetBeltColorRadius(0) # if 0 all colors are detected, including the conveyerbelt

for image in color_detection.ListOfAllImages:
    image.StartColorDetection()

color_detection.PrintAllPercentages()
















    





                
               


