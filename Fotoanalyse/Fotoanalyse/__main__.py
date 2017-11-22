# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 21-11-2017

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import datetime
import cv2
import time

import math
import numpy.ma as ma
import glob

#project .py files
from detection import detection
from color import color
from wait import wait

start_time = time.time()

#----------------------------------------Test----------------------------------------

test_image = cv2.imread('C:\\Users\\tom_l\\OneDrive\\HHS\\Jaar_3\\stage_2\\test_image.png')

FloatRGB_image = test_image/255
FloatRGB_image = FloatRGB_image.astype(np.float32)
LAB_image = cv2.cvtColor(FloatRGB_image , cv2.COLOR_BGR2LAB)

detection(test_image, LAB_image)


        
        
#----------------------------------------initialize class-values----------------------------------------

detection.SetNumberOfDecimals(2) #max 14
detection.SetBeltColorRadius(40) # 0-443, 0 detects everything, 443 nothing
detection.SetLongestGreyRadius(15)
detection.SetLowestWhiteValue(95)

wait.SetBeltSetting(1)
wait.SetPictureWidth(123451345)
wait.CalculateWaitingTime()
print(wait.PictureInterval)

#----------------------------------------color definitions----------------------------------------
    
color('dark blue', 0, 45)
color('purple', 45, 80)
color('red', 81, 120)
color('orange', 121, 170)
color('yellow', 171, 190)
color('green', 191, 270)
color('light blue', 271, 360)

        
#----------------------------------------START PROGRAM----------------------------------------


for image in detection.ListOfAllImages:
    image.StartColorDetection()
    
detection.CalcAllPercentages()
detection.PrintAllPercentages()



print('\n''%s seconds run-time' %(time.time() - start_time))
















    





                
               


