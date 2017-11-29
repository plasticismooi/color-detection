# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017

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



#----------------------------------------Functions for initializing camera and taking pictures-----------------------------------


def TakePicture():
       
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.shutter_speed = 10000
    camera.awb_mode ='fluorescent'
    camera.brightness = 50 
    
    camera.start_preview()
    camera.capture('/media/pi/9E401DB5401D94DD/Pictures/{:%Y-%m-%d %H:%M:%S}.png'.format(datetime.datetime.now()))
    camera.close()
    
    sleep(wait.PictureInterval)
    
    #----------------------------------------Functions for initializing images-----------------------------------


def PrepareAllImagesForDetection():

    DirectoryOfAllImages = PathToAllImages()
    
    for BGR_image in DirectoryOfAllImages:
        
        BGR_image = cv2.imread(BGR_image)
        BlurredBGRImage = cv2.bilateralFilter(BGR_image, 9, 200 ,75)

        if SaveBilateralfilterImage == True:
            cv2.imwrite('/media/pi/9E401DB5401D94DD/test/bilateral.png', BlurredBGRImage)

        detection(BlurredBGRImage)
        
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


print('Preparing Detection...')

AmountOfPicturestToBeTaken = 1
SaveBilateralfilterImage = True


detection.SetNumberOfDecimals(2) #max 14
detection.SaveDetectedPlasticImage(True)

detection.SetBeltValue(40) # 40 corresponds with light setting 2

detection.SetBlackValue(20)
detection.SetWhiteValue(75)
detection.SetMaxSaturation(25)

wait.SetBeltSetting(1)
wait.SetPictureWidth(0.165)
wait.CalculateWaitingTime()

#----------------------------------------color definitions----------------------------------------


print('Preparing Colors...')

color('red', 340, 15)
color('orange', 16, 40)
color('yellow', 41, 70)
color('green', 71, 160)
color('light blue', 161, 190)
color('dark blue', 191, 270)
color('purple', 271, 339)

#----------------------------------------START PROGRAM----------------------------------------


start_time = time.time()
print('Started Detecting...')
RemoveAllImages()

for x in range(0, AmountOfPicturestToBeTaken):
    TakePicture()
    
PrepareAllImagesForDetection()

for image in detection.ListOfAllImages:
    image.StartColorDetection()

print('Done Detecting')
    
detection.CalcAllPercentages()
detection.PrintAllPercentages()

print('\n''%s seconds run-time' %(time.time() - start_time))

#----------------------------------------END PROGRAM----------------------------------------

























    





                
               


