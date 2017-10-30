# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 13-10-2017

import numpy as np
import cv2

from time import sleep
import matplotlib
from matplotlib import pyplot as plt
import math
    
def object_detection(b):


    print('start object detection')
    #inlezen fotos
    image = cv2.imread('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\plastic_4.png')
    #image = image[55:768, 0:1024]
    #cv2.imwrite('/media/pi/9E401DB5401D94DD/image.png',image)
    
    height, width, channels = image.shape
    for m in range(height):
        for n in range(width):
            BGR_array = image[m,n]
            if (((BGR_array[0]**2) + (BGR_array[1]**2) + (BGR_array[2]**2)) < 160**2):
                image[m, n] = [0,0,0]
                
    LAB_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    cv2.imwrite('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\plastic_4_masked.png',image)
    print('done with background detection')
    print('preparing color detection')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    (_, contours, _) = cv2.findContours(gray_image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    
    #c contour nummer
    for c in range (len(contours)):
        print('new flake')
        #temp_1 is het aantal pixels van de contour
        lengtecontour, temp_2, temp_3 = contours[c].shape

        if (lengtecontour > 30):
            contourYvalue = np.zeros(lengtecontour)
            contourXvalue = np.zeros(lengtecontour)
            for d in range (lengtecontour):
                #schrijf alle x en y waardes van contour c naar contour(x,y)values
                contourYvalue[d] = contours[c][d][0][1]
                contourXvalue[d] = contours[c][d][0][0]

            print(c)
            print(contourXvalue)
            print(contourYvalue)

            
            #i is tijdelijke waarde voor y
            for i in range (np.argmax(contourYvalue) + 1):
                #gebruikte tijdelijke variabele resetten
                grensen_array = []
                rechtergrens = 0
                linkergrens = 0
                huidigeYwaarde = 0
                indexHuidigeYwaarde = 0
                print('new row')
               
                
                huidigeYwaarde = contourYvalue[i]
                indexHuidigeYwaarde = i

                #alle grenswaarden in grensen_array zetten            
                for j in range(0 , lengtecontour):
                    if (int(huidigeYwaarde) == contourYvalue[j]):
                        grensen_array.append(contourXvalue[j]) 
                
                lengte_grensen_array = len(grensen_array)
                grensen_array.sort()
                if (lengte_grensen_array >= 1): 
                    linkersgrens = grensen_array[0]
                #als er geen of 1 x-waardes zijn gevonden, wordt deze toegekend aan de rechtergrens
                if (lengte_grensen_array == 1 ):
                    rechtergrens = linkergrens

                    for x in range(int(linkergrens), (int(rechtergrens) + 1)):
                        image[int(huidigeYwaarde), x] = (0, 0, 255)

                elif (lengte_grensen_array == 2 ):
                    linkergrens = grensen_array[0]
                    rechtergrens = grensen_array[1]

                    for x in range(int(linkergrens), (int(rechtergrens) + 1)):
                        image[int(huidigeYwaarde), x] = (0, 0, 255)

                #wanneer er meer dan 2 waardes in rechtergrens_array zitten wordt de onderstaande code uitgevoerd
                else:
                    #controleer of rechtergrens array even is
                    if ((lengte_grensen_array%2) != 0):
                        #wanneer er 1 x-waarde deze nergeren, is een paar regels hierboven al behandeld
                        if(lengte_grensen_array == 1):
                            pass
                        # lengte_rechtergrens_array is hier 3,5,7,9 enz
                        else:
                            e = 0
                            f = 1
                            while(e < lengte_grensen_array):
                                for x in range(int(grensen_array[e]), (int(grensen_array[f]) + 1)):
                                    image[int(huidigeYwaarde), x] = (0, 0, 255)
                                e = e + 2
                                f = f + 2

                    #array is even


        cv2.imwrite('C:\\Users\\tom_l\\Desktop\\School\\HHS\\Jaar_3\\Stage_1\\fotos\\plastic_4_test.png',image)
  
    print('start color detection''\n')
    
    zwart = 0
    kleur = 0
    wit = 0
    pixels_totaal = 0
    
    for (y) in range(height):
        for(x) in range(width):
            
            
                    #assenstelsel aanpassen naar 0-100
                    LAB_array[0] = (LAB_array[0] * 0.392)

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

#foto's doorlopen die gemaakt zijn in setup_camera functie
for b in range(a):
    object_detection(b)