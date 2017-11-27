# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 22-11-2017
#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import os
import datetime
import cv2
import time
from time import sleep

import math
import numpy.ma as ma
import glob

#project .py files
from detection import detection
from color import color
from wait import wait

#----------------------------------------color definitions----------------------------------------

color('red', 340, 15)
color('orange', 16, 40)
color('yellow', 41, 70)
color('green', 71, 140)
color('light blue', 141, 190)
color('dark blue', 191, 270)
color('purple', 271, 339)

#--------------------------------START TEST--------------------------------

BGR_image = cv2.imread('C:\\Users\\tom_l\\OneDrive\\HHS\\Jaar_3\\stage_2\\test_image.png')

B, G, R = cv2.split(BGR_image)      
RGB_image = cv2.merge([R, G, B])     

detection(RGB_image)
detection.SetNumberOfDecimals(3)

for image in detection.ListOfAllImages:
    image.StartColorDetection()

detection.CalcAllPercentages()
detection.PrintAllPercentages()

#--------------------------------END TEST--------------------------------























    





                
               


