# OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 24-11-2017

import cv2
from color import color
import math
import numpy.ma as ma
import numpy as np
import colorsys
#object in this class is a picture

class detection:
    
    ListOfAllImages = []
    TotalAmountPlasticPixels= 0

    NumberOfDecimals = 2
    
    BeltValue = 8

    WhiteValue = 80
    BlackValue = 10
    MaxSaturation = 15

    TotalAmountWhitePixels = 0
    TotalAmountBlackPixels = 0
    TotalAmountGreyPixels = 0
    
    PercentageWhite = 0
    PercentageBlack = 0
    PercentageGrey = 0

    def __init__(self, RGB_image):

        self.RGB_image = RGB_image
        self.__AddToListOfAllImages()

    def __AddToListOfAllImages(self):

        detection.ListOfAllImages.append(self)

    def StartColorDetection(self):
        
        height, width, channels = self.RGB_image.shape

        for x in range(height):
            for y in range(width):

                HSV_pixel = np.array([0,0,0])
                RGB_pixel = self.RGB_image[x,y]/255
                temporary_hsv_pixel = colorsys.rgb_to_hsv(RGB_pixel[0], RGB_pixel[1], RGB_pixel[2])

           
                HSV_pixel[0] = temporary_hsv_pixel[0] * 360
                HSV_pixel[1] = temporary_hsv_pixel[1] * 100
                HSV_pixel[2] = temporary_hsv_pixel[2] * 100

                if self.CheckIfPixelsIsPlastic(HSV_pixel) == True:

                    self.__AddPixelToCorrespondingColor(HSV_pixel)
                    detection.TotalAmountPlasticPixels +=1

    def CheckIfPixelsIsPlastic(self, HSV_pixel):

        if HSV_pixel[2] >= detection.BeltValue:
            return True
        else:
            return False

    def __AddPixelToCorrespondingColor(self, HSV_pixel):   

        if self.__CheckIfPixelIsWhite(HSV_pixel) == True:
            self.__AddWhitePixelToAmountOfWhitePixels()
        elif self.__CheckIfPixelIsBlack(HSV_pixel) == True:
            self.__AddBlackPixelToAmountOfBlackPixels()
        elif self.__CheckIfPixelIsGrey(HSV_pixel) == True:
            self.__AddGreyPixelToAmountOfGreyPixels()
        else:
            self.__AddPixelToCorrectColor(HSV_pixel)

    def __AddPixelToCorrectColor(self, HSV_pixel):

        for CurrentColor in color.AllColors:

            #if the defined color crosses the 0 value on the circle, detect color as below
            if CurrentColor.LeftAngle < CurrentColor.RightAngle:

                if (CurrentColor.LeftAngle >= HSV_pixel[0]) | (CurrentColor.RightAngle <= HSV_pixel[0]):
                    CurrentColor.AmountOfDetectedPixels += 1
                    return

            else:
                if CurrentColor.LeftAngle >= HSV_pixel[0]:
                    if CurrentColor.RightAngle <= HSV_pixel[0]:
                        CurrentColor.AmountOfDetectedPixels += 1
                        return True
                    else:
                        return False


    def __CheckIfPixelIsWhite(self, HSV_pixel):

        if HSV_pixel[1] <= detection.MaxSaturation:
            
            if HSV_pixel[2] >= detection.WhiteValue:
                return True
           
            else:
                return False

    def __CheckIfPixelIsBlack(self, HSV_pixel):

        if HSV_pixel[2] <= detection.BlackValue:
            return True
        else:   
            return False
            
    def __CheckIfPixelIsGrey(self, HSV_pixel):

        if HSV_pixel[1] <= detection.MaxSaturation:

            if HSV_pixel[2] >= detection.BlackValue & HSV_pixel[2] <= detection.WhiteValue:
                return True
            else:
                return False

    def __AddGreyPixelToAmountOfGreyPixels(self):

        detection.TotalAmountGreyPixels += 1

    def __AddWhitePixelToAmountOfWhitePixels(self):

            detection.TotalAmountWhitePixels += 1

    def __AddBlackPixelToAmountOfBlackPixels(self):

            detection.TotalAmountBlackPixels += 1

    def CalcAllPercentages():
        
        try:

            detection.PercentageBlack = round(detection.__CalcBlackPercentage(), detection.NumberOfDecimals) 
            detection.PercentageWhite = round(detection.__CalcWhitePercentage(), detection.NumberOfDecimals)
            detection.PercentageGrey = round(detection.__CalcGreyPercentage(), detection.NumberOfDecimals)


            for CurrentColor in color.AllColors:
            
                CurrentColor.percentage = detection.__CalcPercentages(CurrentColor)
                CurrentColor.Percentage = round(CurrentColor.percentage, detection.NumberOfDecimals)

        except ZeroDivisionError:
            print('NO PLASTIC DETECTED')
            
    def PrintAllPercentages():
        print(detection.PercentageWhite, '% is white')
        print(detection.PercentageBlack, '% is black')
        print(detection.PercentageGrey, '% is grey''\n')
        
        for CurrentColor in color.AllColors:
            print(CurrentColor.Percentage, '% is ', CurrentColor.name)
        

    def __CalcWhitePercentage():

        return ((detection.TotalAmountWhitePixels / detection.TotalAmountPlasticPixels) * 100)

    def __CalcBlackPercentage():

        return ((detection.TotalAmountBlackPixels / detection.TotalAmountPlasticPixels) * 100)

    def __CalcGreyPercentage():

        return ((detection.TotalAmountGreyPixels / detection.TotalAmountPlasticPixels) * 100)
        
    def __CalcPercentages(CurrentColor):

        return ((CurrentColor.AmountOfDetectedPixels / detection.TotalAmountPlasticPixels) * 100)

    def PrintTotalAmountPlasticPixels():

        print('the amount of pixels is', detection.TotalAmountPlasticPixels, '\n')

    def SetBeltColorRadius(BeltColorRadius):
        # 0 means ignore the belt and detect everything
        detection.BeltColorRadius = BeltColorRadius

    def PrintBeltColorRadius():

        print('BeltColorRadius is ', detection.BeltColorRadius, '\n')

    #set and print white pixels
    def SetValue(Value):

        detection.Value = Value

    def PrintValue():

        print('white boundary is', self.Value, '\n')

    def PrintTotalTotalAmountWhitePixels():   
         
        print('total white pixels', detection.TotalAmountWhitePixels, '\n')

    #set and print black pixels
    def SetHighestBlackValue(HighestBlackValue):

        detection.HighestBlackValue = HighestBlackValue

    def PrintHighestBlackValue():

        print('black boundary is', self.HighestBlackValue, '\n')

    def PrintTotalTotalAmountBlackPixels(): 
           
        print('total black pixels', detection.TotalAmountBlackPixels, '\n')

    #set and print grey pixels
    def PrintTotalAmountGreyPixels():

        print('TotalAmountGreyPixels is', detection.TotalAmountGreyPixels) 

    def SetLongestGreyRadius(LongestGreyRadius):

        detection.LongestGreyRadius = LongestGreyRadius

    def SetNumberOfDecimals(NumberOfDecimals):
        detection.NumberOfDecimals = NumberOfDecimals



        

        






       
