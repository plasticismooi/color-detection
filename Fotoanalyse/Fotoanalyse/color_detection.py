#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 6-11-2017

import cv2
from Color import Color
import math

#object in this class is a picture
class color_detection:
    
    ListOfAllImages = []
    TotalPlasticPixelsOfAllImages = 0
    
    BeltColorRadius = 155

    LowestWhiteValue = 70
    HighestBlackValue = 20

    TotalAmountWhitePixels = 0
    TotalAmountBlackPixels = 0


    def __init__(self, image, LAB_image):
        self.image = image
        self.LAB_image = LAB_image
        self.__AddToListOfAllImages()

    def __AddToListOfAllImages(self):

        color_detection.ListOfAllImages.append(self)

    def StartColorDetection(self):
   
        height, width, channels = self.image.shape
        #Looping must become its own function
        for loopvariableY in range(height):
            for loopvariableX in range(width):
       
                if self.__CheckIfPixelIsPlastic(loopvariableY, loopvariableX) == True:
                    color_detection.TotalPlasticPixelsOfAllImages += 1
                    #raise AmountOfDetectedPixel by 1 if colors match
                    self.__AddPixelToCorrespondingColor(loopvariableY, loopvariableX) 
                
    def __CheckIfPixelIsPlastic(self, loopvariableY, loopvariableX):
        #check if pixel is plastic or not
        BGR_array = self.image[loopvariableY, loopvariableX]
        if(((BGR_array[0]**2) + (BGR_array[1]**2) + (BGR_array[2]**2)) > self.BeltColorRadius**2):      
            return True
        else: 
            return False
              
    def __AddPixelToCorrectPixelCount(self, loopvariableY, loopvariableX):   

        if self.__CheckIfPixelIsWhite(loopvariableY, loopvariableX) == True:
            self.__AddWhitePixelToWhitePixelCount()
        elif self.__CheckIfPixelIsBlack(loopvariableY, loopvariableX) == True:
            self.__AddBlackPixelToBlackPixelCount()
        else:
            self.__AddPixelToCorrectColor(loopvariableY, loopvariableX)

    def __AddPixelToCorrectColor(self, loopvariableY, loopvariableX):
            angle = self.__CalculateAngleFromLoopvariable(loopvariableY, loopvariableX)

            if self.__CheckIfCalculatedAngleSucceeded(angle) == True:
                self.__AddPixelToCorrectPixelCountUsingAngle(angle)

    def __CheckIfCalculatedAngleSucceeded(self, angle):
            if (angle == None):
                return False
            else:
                return True

    def __CheckIfPixelIsWhite(self, loopvariableY, loopvariableX):
            LAB_array = self.LAB_image[loopvariableY, loopvariableX]
            if LAB_array[0] >= color_detection.LowestWhiteValue:
                return True
            else:
                return False

    def __CheckIfPixelIsBlack(self, loopvariableY, loopvariableX):
            LAB_array = self.LAB_image[loopvariableY, loopvariableX]
            if LAB_array[0] <= color_detection.HighestBlackValue:
                return True
            else:
                return False

    def __AddWhitePixelToWhitePixelCount(self):

            color_detection.TotalAmountWhitePixels += 1

    def __AddBlackPixelToBlackPixelCount(self):

            color_detection.TotalAmountBlackPixels += 1

    def __AddPixelToCorrectPixelCountUsingAngle(self, angle):

        for CurrentColor in Color.AllColors:

            if self.__CheckIfAnglesCrossBAxis(CurrentColor) == True:
                self.__AddPixelToCorrectColorIfAnglesCrossBAxis(CurrentColor, angle)
            else:
                #function __AddPixelToCurrentColor returns true when the pixels matches a color
                 if self.__AddPixelToCurrentColor(CurrentColor, angle) == True:
                     return

    def __AddPixelToCurrentColor(self, CurrentColor, angle):
        if CurrentColor.LeftAngle >= angle:
            if CurrentColor.RightAngle <= angle:
                CurrentColor.PixelCount += 1
                return True
            else:
                return False

    def __AddPixelToCorrectColorIfAnglesCrossBAxis(self, CurrentColor, angle):

        if (CurrentColor.LeftAngle >= angle) | (CurrentColor.RightAngle <= angle):
            CurrentColor.PixelCount += 1
            return

    def __CheckIfAnglesCrossBAxis(self, CurrentColor):
        if CurrentColor.LeftAngle < CurrentColor.RightAngle:
            return True
        else:
            return False

    def __CalculateAngleFromLoopvariable(self, loopvariableY, loopvariableX):
        CIELAB_array = self.LAB_image[loopvariableY, loopvariableX]

        a = CIELAB_array[1] 
        b = CIELAB_array[2] 

        a = round(a, None)
        b = round(b, None)
        
        if b == 0.0:
            return self.__ReturnAngleIfBIsNull(a)

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

    def __ReturnAngleIfBIsNull(self, a):
        if a > 0:
            angle = 180
            return angle
        else:
            angle = 0 
            return angle

    def PrintAllPercentages():

        print(color_detection.__CalcBlackPercentage(), '% is black')
        print(color_detection.__CalcWhitePercentage(), '% is white')

        print()

        for CurrentColor in Color.AllColors:
            
            percentage = color_detection.__CalcPercentages(CurrentColor)
            print(percentage, '% is', CurrentColor.name)

    def __CalcWhitePercentage():

        return ((color_detection.TotalAmountWhitePixels / color_detection.TotalPlasticPixelsOfAllImages) * 100)

    def __CalcBlackPercentage():

        return ((color_detection.TotalAmountBlackPixels / color_detection.TotalPlasticPixelsOfAllImages) * 100)
        
    def __CalcPercentages(CurrentColor):

        return ((CurrentColor.PixelCount / color_detection.TotalPlasticPixelsOfAllImages) * 100)

    def PrintTotalPlasticPixelsOfAllImages():

        print('the amount of pixels is', color_detection.TotalPlasticPixelsOfAllImages, '\n')

    def SetBeltColorRadius(BeltColorRadius):

        color_detection.BeltColorRadius = BeltColorRadius

    def PrintBoundary(self):

        print('boundary is', self.boundary, '\n')

    #set and print white boundary
    def SetLowestWhiteValue(LowestWhiteValue):

        color_detection.LowestWhiteValue = LowestWhiteValue

    def PrintLowestWhiteValue(self):

        print('white boundary is', self.LowestWhiteValue, '\n')

    def PrintTotalTotalAmountWhitePixels():   
         
        print('total white pixels', color_detection.TotalAmountWhitePixels, '\n')

    #set and print black boundary
    def SetHighestBlackValue(HighestBlackValue):

        color_detection.HighestBlackValue = HighestBlackValue

    def PrintHighestBlackValue(self):

        print('black boundary is', self.HighestBlackValue, '\n')

    def PrintTotalTotalAmountBlackPixels(self): 
           
        print('total black pixels', color_detection.TotalAmountBlackPixels, '\n')
        

        






       
