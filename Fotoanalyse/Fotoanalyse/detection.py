# OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017

import cv2
from color import color
import math
import numpy.ma as ma
import numpy as np



class detection:
    
    ListOfAllImages = []
    TotalAmountPlasticPixels= 0

    NumberOfDecimals = 2
    WriteDetectedplasticImage = False
    
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

    def __init__(self, BGR_image):

        self.BGR_image = BGR_image

        height, width, channels = self.BGR_image.shape
        BGR_image_float = self.BGR_image/255
        BGR_image_float = BGR_image_float.astype(np.float32)
        self.HSV_Image3D = cv2.cvtColor(BGR_image_float, cv2.COLOR_BGR2HSV)
        
        self.__AddToListOfAllImages()

    def __AddToListOfAllImages(self):

        detection.ListOfAllImages.append(self)

    def StartColorDetection(self):

        ArrayWithDetectedPixels = self.__ReturnArrayWithDetectedPixels(self.HSV_Image3D)
        detection.TotalAmountPlasticPixels = detection.TotalAmountPlasticPixels + len(ArrayWithDetectedPixels)

        for HSV_Pixel in ArrayWithDetectedPixels:
            self.__AddPixelToCorrespondingColor(HSV_Pixel)

    def __ReturnBinaryArrayWithDetectedPixels(self, HSV_Image3D):

        V_Image3D = np.delete(HSV_Image3D, [0,1], axis = 2)
        BinaryArrayWithDetectedPixels = V_Image3D <= detection.BeltValue
        
        if detection.WriteDetectedplasticImage == True:
            self.WriteBinaryImage(BinaryArrayWithDetectedPixels)
        
        BinaryArrayWithDetectedPixels = np.repeat(BinaryArrayWithDetectedPixels [:], 3, axis=1)
        
        return BinaryArrayWithDetectedPixels
    
    def WriteBinaryImage(self, BinaryArrayWithDetectedPixels):
        
        BinaryArrayWithDetectedPixels.dtype = 'uint8'
        BinaryArrayWithDetectedPixels[BinaryArrayWithDetectedPixels > 0] = 255
        cv2.imwrite('/media/pi/9E401DB5401D94DD/test/detectedplastic.png', BinaryArrayWithDetectedPixels)
    
    def __ReturnArrayWithDetectedPixels(self, HSV_Image3D):

        BinaryArrayWithDetectedPixels = self.__ReturnBinaryArrayWithDetectedPixels(HSV_Image3D)
        ArrayOfAllDetecedPlasticPixels = ma.masked_array((self.HSV_Image3D), mask = BinaryArrayWithDetectedPixels)
        
        height, width, channels = HSV_Image3D.shape        
        ArrayOfAllDetecedPlasticPixels = np.reshape(ArrayOfAllDetecedPlasticPixels, ((height * width), 3))
        
        ArrayOfAllDetecedPlasticPixels = ma.compress_rows(ArrayOfAllDetecedPlasticPixels)
        
        return ArrayOfAllDetecedPlasticPixels

    def __AddPixelToCorrespondingColor(self, HSV_Pixel):   

        if self.__CheckIfPixelIsWhite(HSV_Pixel) == True:
            self.__AddWhitePixelToAmountOfWhitePixels()
        elif self.__CheckIfPixelIsBlack(HSV_Pixel) == True:
            self.__AddBlackPixelToAmountOfBlackPixels()
        elif self.__CheckIfPixelIsGrey(HSV_Pixel) == True:
            self.__AddGreyPixelToAmountOfGreyPixels()
        else:
            self.__AddPixelToCorrectColor(HSV_Pixel)

    def __AddPixelToCorrectColor(self, HSV_Pixel):

        for CurrentColor in color.AllColors:

            #if the defined color crosses the 0 value on the circle, detect color as below
            if CurrentColor.LeftAngle > CurrentColor.RightAngle:

                if (CurrentColor.RightAngle > HSV_Pixel[0]) or (CurrentColor.LeftAngle < HSV_Pixel[0]):
                    CurrentColor.AmountOfDetectedPixels += 1
                    return 

            else:
                if CurrentColor.LeftAngle <= HSV_Pixel[0]:
                    if CurrentColor.RightAngle >= HSV_Pixel[0]:
                        CurrentColor.AmountOfDetectedPixels += 1
                        return 
                    
    def __CheckIfPixelIsWhite(self, HSV_Pixel):
      
        if HSV_Pixel[1] <= detection.MaxSaturation:
            
            if HSV_Pixel[2] >= detection.WhiteValue:
                return True
           
            else:
                return False

    def __CheckIfPixelIsBlack(self, HSV_Pixel): 
       
        if HSV_Pixel[2] <= detection.BlackValue:
            return True
        else:   
            return False
            
    def __CheckIfPixelIsGrey(self, HSV_Pixel):
        
        if HSV_Pixel[1] <= detection.MaxSaturation:
            
            if HSV_Pixel[2] >= detection.BlackValue and HSV_Pixel[2] <= detection.WhiteValue:
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

    def SetBeltValue(BeltValue):
        
        detection.BeltValue = BeltValue/100

    def PrintBeltValue():

        print('BeltValue is ', detection.BeltValue, '\n')

    #set and print white pixels
    def SetWhiteValue(WhiteValue):

        detection.WhiteValue = WhiteValue/100

    def PrintWhiteValue():

        print('white boundary is', detection.WhiteValue, '\n')

    #set and print black pixels
    def SetBlackValue(BlackValue):

        detection.BlackValue = BlackValue/100

    def PrintBlackValue():

        print('BlackValue is', self.BlackValue, '\n')

    def PrintTotalTotalAmountBlackPixels(): 
           
        print('total black pixels', detection.TotalAmountBlackPixels, '\n')

    #set and print grey pixels
    def PrintTotalAmountGreyPixels():

        print('TotalAmountGreyPixels is', detection.TotalAmountGreyPixels)
        
    def PrintTotalTotalAmountWhitePixels():   
         
        print('total white pixels', detection.TotalAmountWhitePixels, '\n')

    def SetNumberOfDecimals(NumberOfDecimals):
        
        detection.NumberOfDecimals = NumberOfDecimals
        
    def SetMaxSaturation(MaxSaturation):
        
        detection.MaxSaturation = MaxSaturation/100
        
    def WriteDetectedplasticImage(x):
        
        detection.WriteDetectedplasticImage = x
        


        

        






       
