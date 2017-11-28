

# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 22-11-2017
#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import os
import datetime
import cv2
from picamera import PiCamera
import time
from time import sleep

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
    camera.awb_mode ='incandescent'
    camera.brightness = 50
    camera.ISO = 800
    
    
    
    camera.start_preview()
    camera.capture('/media/pi/9E401DB5401D94DD/Pictures/{:%Y-%m-%d %H:%M:%S}.png'.format(datetime.datetime.now())) 

    camera.close()
    
    sleep(wait.PictureInterval)
    
    #----------------------------------------Functions for initializing images-----------------------------------

def PrepareAllImagesForDetection():

    DirectoryOfAllImages = PathToAllImages()
    
    for BGR_image in DirectoryOfAllImages:
        BGR_image = cv2.imread(BGR_image)
        detection(BGR_image)
        
def PathToAllImages():
    
    path = '/media/pi/9E401DB5401D94DD/Pictures/*.png'
    DirectoryOfAllImages = glob.glob(path)
    
    return DirectoryOfAllImages

def RemoveAllImages():
    
    DirectoryOfAllImages = PathToAllImages()
    
    for BGR_image in DirectoryOfAllImages:
        os.remove(BGR_image)
   

#----------------------------------------Function for writing data to text file---------------------------------------

def WriteDataTotxtFile():
    DataFile = open('/media/pi/9E401DB5401D94DD/Color-detection-data/data.txt', 'w')
    
    DataFile.write('Analysed all pictures in folder /media/pi/9E401DB5401D94DD/Pictures''\n')
    DataFile.write('{} % is white \n{} % is grey \n{} % is black \n\n'.format(detection.PercentageWhite, detection.PercentageGrey, detection.PercentageBlack))
    
    for CurrentColor in color.AllColors:
        DataFile.write('{} % is {} \n'.format(CurrentColor.Percentage, CurrentColor.name))

#----------------------------------------initialize class-values----------------------------------------
        
AmountOfPicturestToBeTaken = 1

detection.SetNumberOfDecimals(2) #max 14

detection.SetBeltColorRadius(30) # 0-443, 0 detects everything, 443 nothing
detection.SetLongestGreyRadius(15)
detection.SetLowestWhiteValue(70)

wait.SetBeltSetting(1)
wait.SetPictureWidth(0.15)
wait.CalculateWaitingTime()


#----------------------------------------color definitions----------------------------------------

color('red', 340, 15)
color('orange', 16, 40)
color('yellow', 41, 70)
color('green', 71, 140)
color('light blue', 141, 190)
color('dark blue', 191, 270)
color('purple', 271, 339)

#----------------------------------------START PROGRAM----------------------------------------

RemoveAllImages()

for x in range(0, AmountOfPicturestToBeTaken):
    TakePicture()
    
PrepareAllImagesForDetection()

for image in detection.ListOfAllImages:
    image.StartColorDetection()
    
detection.CalcAllPercentages()
detection.PrintAllPercentages()

print('\n''%s seconds run-time' %(time.time() - start_time))

#----------------------------------------END PROGRAM----------------------------------------

























    





                
               


