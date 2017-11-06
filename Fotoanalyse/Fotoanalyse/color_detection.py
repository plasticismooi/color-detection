#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 6-11-2017

import cv2
from Color import Color

#object in this class is a picture
class color_detection:

    AllImages = []
    TotalPixels = 0
    #standard boundary is 155, adjust with SetBoundary() if needed
    boundary = 155

    def __init__(self, image):
        self.image = image
        self.__AddToAllImages()
        
        #detection in RGB or CIELAB?
    def __AddToAllImages(self):
        color_detection.AllImages.append(self)


    def detect(self):
        #actual detection of colors

        height, width, channels = self.image.shape
    
        for loopvariableY in range(height):
            for loopvariableX in range(width):

                self.DetectFlakes(loopvariableY, loopvariableX)
                

    def DetectFlakes(self, loopvariableY, loopvariableX):
        #check if pixel is plastic or not
        bgr_array = self.image[loopvariableY, loopvariableX]
        if(((bgr_array[0]**2) + (bgr_array[1]**2) + (bgr_array[2]**2)) > self.boundary**2):
            #add every detected flake to total pixel count
            self.TotalPixels += 1
            #if pixels is plastic, detect color
            self.DetectColor(loopvariableY, loopvariableX)
               
    def DetectColor(self, loopvariableY, loopvariableX):
        #convert [x,y] values to angles

        #loop all colors
        for CurrentColor in Color.AllColors:
            #check if pixel is a color
            Color.PrintAllColors()

            

    def CalcPercentages(self):

        for CurrentColor in Color.AllColors:
        #loop all Color instances and calculate percantages
            pass

    def PrintTotalPixels(self):
        print(self.TotalPixels, '\n')

    def SetBoundary(self, boundary):
        self.boundary = boundary

    def PrintBoundary(self):
        print('boundary is', self.boundary, '\n')






       