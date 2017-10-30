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

def setup_camera(FotoNumber):
    
    #instellen picamera
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    #shutterspeed hoog, dit voorkomt bewogen plastic op de loopband
    camera.shutter_speed = 10000
    
    #beste instelling voor belichting op loopband
    camera.awb_mode ='auto'
    camera.brightness = 60
    camera.exposure_mode = 'auto'
    camera.raw_format = 'rgb'
   
    camera.start_preview()
    
    #foto nemen
    camera.capture('/media/pi/9E401DB5401D94DD/RGB/image_%i.png'%FotoNumber)
    camera.close()
    #2.05 is de totale tijd die de lopendeband nodig heeft om nieuw plastic onder de camera te leggen
    sleep(2.05)
    


def object_detection(FotoNumber):
    print('start background detection')
    #inlezen fotos
    image = cv2.imread('/media/pi/9E401DB5401D94DD/RGB/image_%i.png'%FotoNumber)
    #deel van de foto is niet op van lopende band, deze moet weggeknipt worden
    image = image[55:768, 0:1024]
    
    height, width, channels = image.shape

    for LoopVariableY in range(height):
        for LoopVariableX in range(width):

            BGR_array = image[LoopVariableY,LoopVariableY]
            if (((BGR_array[0]**2) + (BGR_array[1]**2) + (BGR_array[2]**2)) < 155**2):
                image[LoopVariableY, LoopVariableX] = [0,0,0]
                
    LAB_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    print('Background detected''\n')
    print('start color detection')
    
    zwart = 0
    kleur = 0
    wit = 0
    pixels_totaal = 0
    
    for (LoopVariableY) in range(height):
        for(LoopVariableX) in range(width):
            
            if (contour_image[LoopVariableY,LoopVariableY] != 0,0,0):
    
                LAB_array = LAB_image[y,x]

                #assenstelsel aanpassen naar 0-100
                LAB_array[0] = (LAB_array[0] * 0.392)
                if (LAB_array[0] == 0):
                    pass
                elif ((LAB_array[0] > 0) & (LAB_array[0] < 21)):
                    zwart = zwart + 1
                elif ((LAB_array[0] > 20) & (LAB_array[0] < 70)):
                   kleur = kleur + 1
                elif ( LAB_array[0] >= 70 ):
                    wit = wit + 1
                    
    pixels_totaal = wit + zwart + kleur
     #wanneer het voorkomt dat er geen plastic op de band ligt, zijn er geen pixels, dus zal er door nul gedeeld worden, dit moet voorkomen worden
               
    if (pixels_totaal != 0): 
        proc_zwart = (zwart / pixels_totaal) * 100
        proc_kleur = (kleur / pixels_totaal) * 100
        proc_wit = (wit / pixels_totaal) * 100 
        
        print('foto %i'%FotoNumber )
        print(proc_wit)
        print('procent is wit''\n')
        print(proc_kleur)
        print('procent is kleur''\n')
        print(proc_zwart)
        print('procent is zwart''\n')
    else:
        print('er ligt geen plastic op de band bij foto %i'%FotoNumber)

                               
FotoNumber = 1

for b in range(FotoNumber):
    setup_camera(FotoNumber)
    
#foto's doorlopen die gemaakt zijn in setup_camera functie
for b in range(FotoNumber):
    object_detection(FotoNumber)