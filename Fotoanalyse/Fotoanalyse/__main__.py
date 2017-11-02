# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 1-11-2017

import numpy as np
import cv2
#from picamera import PiCamera
from time import sleep
import matplotlib
from matplotlib import pyplot as plt
import math
#project .py files
from AddColor import AddColor
from color_detection import color_detection


def setup_camera(FotoNumber):
    
    #instellen picamera
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    #shutterspeed hoog, dit voorkomt bewogen plastic op de loopband
    camera.shutter_speed = 10000
    
    #beste instelling voor belichting op loopband
    camera.awb_mode ='auto'
    camera.brightness = 60
    #foto nemen
    camera.capture('/media/pi/9E401DB5401D94DD/RGB/image_%i.png'%FotoNumber)
    camera.close()
    #2.05 is de totale tijd die de lopendeband nodig heeft om nieuw plastic onder de camera te leggen
    sleep(2.05)
    

image1 = cv2.imread('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\plastic_4.png')
image2 = cv2.imread('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\plastic_6.png')

height, width, channels = image1.shape

#set images as objects
image_1 = color_detection(image1)
image_2 = color_detection(image2)

#color definitions
yellow = AddColor(90, 60)
orange = AddColor(30, 50)

#loop over all image object of the class color_detection
for image in color_detection._registery:

    for loopvariableY in range(height):
        for loopvariableX in range(width):

            bgr_array = image1[loopvariableY, loopvariableX]
            if(((bgr_array[0]**2) + (bgr_array[1]**2) + (bgr_array[2]**2)) > image_1.boundary**2):

                image.detect(loopvariableY, loopvariableX, yellow)
                image.detect(loopvariableY, loopvariableX, orange)




