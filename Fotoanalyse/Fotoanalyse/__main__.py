# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 13-10-2017

import numpy as np
import cv2
from picamera import PiCamera
from time import sleep
import matplotlib
from matplotlib import pyplot as plt
import math

def setup_camera(b):
    
    # instellen picamera
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    #shutterspeed hoog, dit voorkomt bewogen plastic op de loopband
    camera.shutter_speed = 10000
    
    # beste instelling voor belichting op loopband
    camera.awb_mode ='auto'
    camera.brightness = 60
    camera.exposure_mode = 'auto'
    camera.raw_format = 'rgb'
   
    camera.start_preview()
    
    # foto nemen
    camera.capture('/media/pi/9E401DB5401D94DD/RGB/image_%i.png'%b)
    camera.close()
 
    sleep(2.05)
    
def object_detection(b):
    print('start object detection')
    #inlezen fotos
    image = cv2.imread('/media/pi/9E401DB5401D94DD/RGB/image_%i.png'%b)
    image = image[55:768, 0:1024]
    cv2.imwrite('/media/pi/9E401DB5401D94DD/image.png',image)
    
    height, width, channels = image.shape
    for y in range(height):
        for x in range(width):
            BGR_array = image[y,x]
            if (((BGR_array[0]**2) + (BGR_array[1]**2) + (BGR_array[2]**2)) < 155**2):
                image[m, n] = [0,0,0]
                
    LAB_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    print('done with background detection')
    print('preparing color detection')
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    print('start color detection''\n')
    
    zwart = 0
    kleur = 0
    wit = 0
    pixels_totaal = 0
    
    for (y) in range(height):
        for(x) in range(width):
            
            if (contour_image[y,x] != 0,0,0):
    
                LAB_array = LAB_image[y,x]

                #assenstelsel aanpassen naar 0-100
                LAB_array[0] = (LAB_array[0] * 0.392)
                if (LAB_array[0] == 0):
                    pass
                if ((LAB_array[0] > 0) & (LAB_array[0] < 21)):
                    zwart = zwart + 1
                if ((LAB_array[0] > 20) & (LAB_array[0] < 70)):
                   kleur = kleur + 1
                if ( LAB_array[0] >= 70 ):
                    wit = wit + 1
                    
    pixels_totaal = wit + zwart + kleur
            
    if (pixels_totaal != 0):  #wanneer het voorkomt dat er geen plastic op de band ligt, zijn er geen pixels, dus zal er door nul gedeeld worden, dit moet voorkomen worden
        proc_wit = (wit / pixels_totaal) * 100
        proc_zwart = (zwart / pixels_totaal) * 100
        proc_kleur = (kleur / pixels_totaal) * 100
        
        print('foto %i'%b )
        print(proc_wit)
        print('procent is wit''\n')
        print(proc_kleur)
        print('procent is kleur''\n')
        print(proc_zwart)
        print('procent is zwart''\n')
    else:
        print('er ligt geen plastic op de band bij foto %i'%b)
                                
a = 1

for b in range(a):
    setup_camera(b)
    
#foto's doorlopen die gemaakt zijn in setup_camera functie
for b in range(a):
    object_detection(b)