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

#image_1 instellen als object
image_1 = color_detection(image1)
image_1.Detect()
image_1.PrintTotalPixels()
image_1.PrintBoundary()
image_1.PrintPercentages()

image_2 = color_detection(image2)
image_2.SetBoundary(154)
image_2.Detect()
image_2.PrintTotalPixels()
image_2.PrintBoundary()
image_2.PrintPercentages()









    

