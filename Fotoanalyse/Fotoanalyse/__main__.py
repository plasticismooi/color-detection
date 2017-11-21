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
from color_detection import color_detection
from Color import Color
from WaitingTime import WaitingTime

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
    
    temp_image = RGB_image/255
    temp_image = temp_image.astype(np.float32)
    LAB_image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2LAB)
    
    return LAB_image

#----------------------------------------Function for writing data to text file---------------------------------------

def WriteDataTotxtFile():
    DataFile = open('/media/pi/9E401DB5401D94DD/Color-detection-data/data.txt', 'w')
    
    DataFile.write('Analysed all pictures in folder /media/pi/9E401DB5401D94DD/Pictures''\n')
    DataFile.write('{} % is white \n{} % is grey \n{} % is black \n\n'.format(color_detection.PercentageWhite, color_detection.PercentageGrey, color_detection.PercentageBlack))
    
    for CurrentColor in Color.AllColors:
        DataFile.write('{} % is {} \n'.format(CurrentColor.Percentage, CurrentColor.name))
        
        
#----------------------------------------initialize class-values----------------------------------------

color_detection.SetNumberOfDecimals(2) #max 14
color_detection.SetBeltColorRadius(0) # 0-443, 0 detects everything, 443 nothing
color_detection.SetLongestGreyRadius(15)

        
#----------------------------------------START PROGRAM----------------------------------------

for NumberOfTakenImages in range(0, 1):
    TakePicture()
    
PreparePictures()
    
Color('1st quadrant', 0, 90)
Color('2nd quadrant', 91, 180)
Color('3rd quadrant', 181, 270)
Color('4th quadrant', 271, 360)


for image in color_detection.ListOfAllImages:
    image.StartColorDetection()
    
color_detection.CalcAllPercentages()
color_detection.PrintAllPercentages()

WriteDataTotxtFile()

print('\n''%s seconds run-time' %(time.time() - start_time))
















    





                
               


