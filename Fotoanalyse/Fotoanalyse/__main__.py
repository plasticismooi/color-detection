# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import cv2
import time
import math
import numpy.ma as ma

#project .py files
from detection import detection
from color import color
from wait import wait


#----------------------------------------Function for writing data to text file---------------------------------------


def WriteDataTotxtFile():
    DataFile = open('/media/pi/9E401DB5401D94DD/Color-detection-data/data.txt', 'w')
    
    DataFile.write('Analysed all pictures in folder /media/pi/9E401DB5401D94DD/Pictures''\n')
    DataFile.write('{} % is white \n{} % is grey \n{} % is black \n\n'.format(detection.PercentageWhite, detection.PercentageGrey, detection.PercentageBlack))
    
    for CurrentColor in color.AllColors:
        DataFile.write('{} % is {} \n'.format(CurrentColor.Percentage, CurrentColor.name))

#----------------------------------------initialize class-values----------------------------------------


print('Preparing Detection...')

detection.SetAmountOfPicturestToBeTaken(30)
detection.SetNumberOfDecimals(2) #max 14

detection.SaveDetectedPlasticImage(True)
detection.SaveBilateralfilterImage(True)


detection.SetBeltValue(40) # 40 corresponds with light setting 2

detection.SetBlackValue(20)
detection.SetWhiteValue(75)
detection.SetMaxSaturation(25)

wait.SetBeltSetting(0)
wait.SetPictureWidth(0.1675)
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


detection.RemoveAllImages()
print('Started Taking Pictures...')
for x in range(0, detection.AmountOfPicturestToBeTaken):
    detection.TakePicture()
    
print('done Taking Pictures...')
print('start detecing colors')

detection.PrepareAllImagesForDetection()

for image in detection.ListOfAllImages:
    image.StartColorDetection()
    
print('\n''%s seconds run-time' %round((time.time() - start_time), detection.NumberOfDecimals))
print('Done Detecting''\n')
    
detection.CalcAllPercentages()
detection.PrintAllPercentages()



#----------------------------------------END PROGRAM----------------------------------------

























    





                
               


