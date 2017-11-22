# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 21-11-2017

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import datetime
import cv2
from picamera import PiCamera
import time

import math
import numpy.ma as ma
import glob

#project .py files
from detection import detection
from color import color
from wait import wait

start_time = time.time()

#----------------------------------------Functions for initializing camera and taking pictures-----------------------------------

def TakePicture():
       
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.shutter_speed = 10000
    camera.awb_mode ='auto'
    camera.brightness = 50
    
    camera.start_preview()
    camera.capture('/media/pi/9E401DB5401D94DD/Pictures/{:%Y-%m-%d %H:%M:%S}.png'.format(datetime.datetime.now())) 

    camera.close()
    
def PreparePictures():
    
    ImageFiles = ReadPictures()
    
    for RGB_image in ImageFiles:
        RGB_image = cv2.imread(RGB_image)
        LAB_image = ConvertRGBtoLAB(RGB_image)
        
        CreateImageObject(RGB_image, LAB_image)
    
def ReadPictures():
    
    path = '/media/pi/9E401DB5401D94DD/Pictures/*.png'
    files = glob.glob(path)
    
    return files

def CreateImageObject(RGB_image, LAB_image):
   
    color_detection(RGB_image, LAB_image)

def ConvertRGBtoLAB(RGB_image):
    
    FloatRGB_image = RGB_image/255
    FloatRGB_image = FloatRGB_image.astype(np.float32)
    LAB_image = cv2.cvtColor(FloatRGB_image , cv2.COLOR_BGR2LAB)
    
    return LAB_image

#----------------------------------------Function for writing data to text file---------------------------------------

def WriteDataTotxtFile():
    DataFile = open('/media/pi/9E401DB5401D94DD/Color-detection-data/data.txt', 'w')
    
    DataFile.write('Analysed all pictures in folder /media/pi/9E401DB5401D94DD/Pictures''\n')
    DataFile.write('{} % is white \n{} % is grey \n{} % is black \n\n'.format(color_detection.PercentageWhite, color_detection.PercentageGrey, color_detection.PercentageBlack))
    
    for CurrentColor in Color.AllColors:
        DataFile.write('{} % is {} \n'.format(CurrentColor.Percentage, CurrentColor.name))
        
        
#----------------------------------------initialize class-values----------------------------------------

detection.SetNumberOfDecimals(2) #max 14
detection.SetBeltColorRadius(0) # 0-443, 0 detects everything, 443 nothing
detection.SetLongestGreyRadius(15)

#----------------------------------------Color definitions----------------------------------------
    
color('dark blue', 0, 45)
color('purple', 45, 80)
color('red', 81, 120)
color('orange', 121, 170)
color('yellow', 171, 190)
color('green', 191, 270)
color('light blue', 271, 360)
        
#----------------------------------------START PROGRAM----------------------------------------

for NumberOfTakenImages in range(0, 1):
    TakePicture()
    
PreparePictures()

for image in detection.ListOfAllImages:
    image.StartColorDetection()
    
color_detection.CalcAllPercentages()
color_detection.PrintAllPercentages()

WriteDataTotxtFile()

print('\n''%s seconds run-time' %(time.time() - start_time))
















    





                
               


