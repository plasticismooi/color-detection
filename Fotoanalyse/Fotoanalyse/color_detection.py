#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 6-11-2017

import cv2
from Color import Color
import math

#object in this class is a picture
class color_detection:
    
    AllImages = []
    TotalPixels = 0
    
    boundary = 155

    WhiteBoundary = 70
    BlackBoundary = 20

    WhitePixels = 0
    BlackPixels = 0


    def __init__(self, image, LAB_image):
        self.image = image
        self.LAB_image = LAB_image
        self.__AddToAllImages()

        
        
    def __AddToAllImages(self):
        color_detection.AllImages.append(self)


    def detect(self):
        #actual detection of colors

        height, width, channels = self.image.shape
        #loop each pixel
        for loopvariableY in range(height):
            for loopvariableX in range(width):

                if self.DetectFlakes(loopvariableY, loopvariableX) == True:
                    self.DetectColor(loopvariableY, loopvariableX)
                

    def DetectFlakes(self, loopvariableY, loopvariableX):
        #check if pixel is plastic or not
        bgr_array = self.image[loopvariableY, loopvariableX]
        if(((bgr_array[0]**2) + (bgr_array[1]**2) + (bgr_array[2]**2)) > self.boundary**2):      
            self.TotalPixels += 1
            return True
               

    def DetectColor(self, loopvariableY, loopvariableX):       
        angle = self.ConvertToAngles(loopvariableY, loopvariableX)

        LAB_array = self.LAB_image[loopvariableY, loopvariableX]
        if LAB_array[0] >= color_detection.WhiteBoundary:
            color_detection.WhitePixels += 1
        elif LAB_array[0] <= color_detection.BlackBoundary:
            color_detection.BlackPixels += 1
        else:

            for CurrentColor in Color.AllColors:
                
                if CurrentColor.LeftAngle > angle:
                    if CurrentColor.RightAngle < angle:

                        CurrentColor.PixelCount += 1
                       
        

    def ConvertToAngles(self, loopvariableY, loopvariableX):
        CIELAB_array = self.LAB_image[loopvariableY, loopvariableX]

        a = CIELAB_array[1] 
        b = CIELAB_array[2] 

        QuadrantAngle = self.__ReturnQuadrantAngle(a, b)

        a = abs(a)
        b = abs(b)
        
        AngleRadians =  math.atan(a/b)
        AngleDegrees = math.degrees(AngleRadians)

        angle = AngleDegrees + QuadrantAngle

        return angle


    def __ReturnQuadrantAngle(self, a, b):
        if (b < 0) & (a > 0):
            QuadrantAngle = 0
        elif (b > 0) & (a > 0):
            QuadrantAngle = 90
        elif (b > 0) & (a < 0):
            QuadrantAngle = 180
        else:
            QuadrantAngle = 270
        return QuadrantAngle


    def CalcPercentages(self):

        for CurrentColor in Color.AllColors:
        #loop all Color instances and calculate percantages
            pass

    def PrintTotalPixels(self):
        print('the amount of pixels in', self.TotalPixels, '\n')

    #set and print boundary
    def SetBoundary(self, boundary):
        self.boundary = boundary

    def PrintBoundary(self):
        print('boundary is', self.boundary, '\n')

    #set and print white boundary
    def SetWhiteBoundary(self, WhiteBoundary):
        self.WhiteBoundary = WhiteBoundary

    def PrintWhiteBoundary(self):
        print('white boundary is', self.WhiteBoundary, '\n')

    #set and print black boundary
    def SetBlackBoundary(self):
        self.BlackBoundary = BlackBoundary

    def PrintBlackBoundary(self):
        print('black boundary is', self.BlackBoundary, '\n')






       