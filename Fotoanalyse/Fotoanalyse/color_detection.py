#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 17-11-2017

import cv2
from Color import Color
import math
import numpy.ma as ma
import numpy as np
#object in this class is a picture

class color_detection:
    
    ListOfAllImages = []
    TotalPlasticPixels = 0

    NumberOfDecimals = 2
    
    BeltColorRadius = 155

    LowestWhiteValue = 70
    HighestBlackValue = 20
    LongestGreyRadius = 5

    TotalAmountWhitePixels = 0
    TotalAmountBlackPixels = 0
    TotalAmountGreyPixels = 0
   

    def __init__(self, RGB_image, LAB_image):
        self.image = RGB_image
        self.LAB_image = LAB_image
        self.__AddToListOfAllImages()

    def __AddToListOfAllImages(self):

        color_detection.ListOfAllImages.append(self)

    def StartColorDetection(self):

        ArrayWithPlasticPixels = self.__GetArrayWithPlasticPixels()
        color_detection.TotalPlasticPixels = len(ArrayWithPlasticPixels)

        for PixelData in ArrayWithPlasticPixels:

            self.__AddPixelToCorrespondingColor(PixelData)
           

    def __GetArrayWithPlasticPixels(self):

        BinaryImage = self.__GetArrayWithDetectedPixels()
        

        height, width, channels = self.LAB_image.shape
        masked_image = ma.masked_array((self.LAB_image), mask = BinaryImage)
        ArrayWithDetectedPixels = np.reshape(masked_image, ((height * width), 3))

        #delete [-- -- --] from ArrayWithDetectedPixels
        ArrayWithDetectedPixels = ma.compress_rows(ArrayWithDetectedPixels)
        
        return ArrayWithDetectedPixels

    def __GetArrayWithDetectedPixels(self):
        
        #create temporary image copy with sqrt(R^2+B^2+G^2)
        temp_image = np.array(self.image, dtype = 'uint32')**2
        temp_image = np.sum(temp_image, axis = 2)

        #create bitmask with detected pixels as True and the conveyerbelt as False
        BinaryImageMap = temp_image <= color_detection.BeltColorRadius**2
        BinaryImageMap = np.repeat(BinaryImageMap[:, :, np.newaxis], 3, axis=2)

        return BinaryImageMap
   
    def __AddPixelToCorrespondingColor(self, PixelData):   

        if self.__CheckIfPixelIsWhite(PixelData) == True:
            self.__AddWhitePixelToAmountOfWhitePixels()
        elif self.__CheckIfPixelIsBlack(PixelData) == True:
            self.__AddBlackPixelToAmountOfBlackPixels()
        elif self.__CheckIfPixelIsGrey(PixelData) == True:
            self.__AddGreyPixelToAmountOfGreyPixels()
        else:
            self.__AddPixelToCorrectColor(PixelData)

    def __AddPixelToCorrectColor(self, PixelData):
            angle = self.__CalculateAngle(PixelData)

            self.__AddPixelToCorrectColorUsingAngle(angle)

    def __CheckIfPixelIsWhite(self, PixelData):
            
            if PixelData[0] >= color_detection.LowestWhiteValue:
                return True
            else:
                return False

    def __CheckIfPixelIsBlack(self, PixelData):
            
            if PixelData[0] <= color_detection.HighestBlackValue:
                return True
            else:
                return False

    def __CheckIfPixelIsGrey(self, PixelData):

        GreyRadius = self.__CalculateRadius(PixelData)

        if color_detection.LongestGreyRadius >= GreyRadius :
            return True
        else: 
            return False

    def __CalculateRadius(self, PixelData):

        return math.sqrt(PixelData[1]**2 + PixelData[2]**2)

    def __AddGreyPixelToAmountOfGreyPixels(self):

        color_detection.TotalAmountGreyPixels += 1

    def __AddWhitePixelToAmountOfWhitePixels(self):

            color_detection.TotalAmountWhitePixels += 1

    def __AddBlackPixelToAmountOfBlackPixels(self):

            color_detection.TotalAmountBlackPixels += 1

    def __AddPixelToCorrectColorUsingAngle(self, angle):

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
                CurrentColor.AmountOfDetectedPixels += 1
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

    def __CalculateAngle(self, PixelData):

        a = PixelData[1] 
        b = PixelData[2] 
        
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

        print(round(color_detection.__CalcBlackPercentage(), color_detection.NumberOfDecimals), '% is black')
        print(round(color_detection.__CalcWhitePercentage(), color_detection.NumberOfDecimals),'% is white')
        print(round(color_detection.__CalcGreyPercentage(), color_detection.NumberOfDecimals), '% is grey ','\n')

        for CurrentColor in Color.AllColors:
            
            percentage = color_detection.__CalcPercentages(CurrentColor)
            print(round(percentage, color_detection.NumberOfDecimals), '% is', CurrentColor.name)

    def __CalcWhitePercentage():

        return ((color_detection.TotalAmountWhitePixels / color_detection.TotalPlasticPixels) * 100)

    def __CalcBlackPercentage():

        return ((color_detection.TotalAmountBlackPixels / color_detection.TotalPlasticPixels) * 100)

    def __CalcGreyPercentage():

        return ((color_detection.TotalAmountGreyPixels / color_detection.TotalPlasticPixels) * 100)
        
    def __CalcPercentages(CurrentColor):

        return ((CurrentColor.AmountOfDetectedPixels / color_detection.TotalPlasticPixels) * 100)

    def PrintTotalPlasticPixels():

        print('the amount of pixels is', color_detection.TotalPlasticPixels, '\n')

    def SetBeltColorRadius(BeltColorRadius):
        # 0 means ignore the belt and detect everything
        color_detection.BeltColorRadius = BeltColorRadius

    def PrintBeltColorRadius():

        print('BeltColorRadius is ', color_detection.BeltColorRadius, '\n')

    #set and print white pixels
    def SetLowestWhiteValue(LowestWhiteValue):

        color_detection.LowestWhiteValue = LowestWhiteValue

    def PrintLowestWhiteValue():

        print('white boundary is', self.LowestWhiteValue, '\n')

    def PrintTotalTotalAmountWhitePixels():   
         
        print('total white pixels', color_detection.TotalAmountWhitePixels, '\n')

    #set and print black pixels
    def SetHighestBlackValue(HighestBlackValue):

        color_detection.HighestBlackValue = HighestBlackValue

    def PrintHighestBlackValue():

        print('black boundary is', self.HighestBlackValue, '\n')

    def PrintTotalTotalAmountBlackPixels(): 
           
        print('total black pixels', color_detection.TotalAmountBlackPixels, '\n')

    #set and print grey pixels
    def PrintTotalAmountGreyPixels():

        print('TotalAmountGreyPixels is', color_detection.TotalAmountGreyPixels) 

    def SetLongestGreyRadius(LongestGreyRadius):

        color_detection.LongestGreyRadius = LongestGreyRadius

    def SetNumberOfDecimals(NumberOfDecimals):
        color_detection.NumberOfDecimals = NumberOfDecimals



        

        






       
