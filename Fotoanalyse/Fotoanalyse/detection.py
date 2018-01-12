# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# company: Polytential B.V.
# date : 12-1-2018

import cv2
from color import color
import math
import numpy.ma as ma
import numpy as np
import glob
import os

import datetime
from time import sleep
import time

from wait import wait

class detection:
    
    ListOfAllImages = []
    ImageNumber = 0
    
    NumberOfDecimals = 2
    
    SaveDetectedPlasticImage = True
    SaveBilateralfilterImage = None
    EnableWriteDataToTXTfile = True
    
    BeltValue = 0.4

    WhiteValue = 0.75
    BlackValue = 0.2
    MaxSaturation = 0.25
    
    TotalAmountPlasticPixels= 0

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
        self.HSV_Image = cv2.cvtColor(BGR_image_float, cv2.COLOR_BGR2HSV)
        
        self.ImageNumber = detection.ImageNumber
        detection.ImageNumber += 1
        
        self.__AddToListOfAllImages()

    def __AddToListOfAllImages(self):

        detection.ListOfAllImages.append(self)
        
#----------------------------------------Functions for initializing images-----------------------------------


    def PrepareAllImagesForDetection():

        DirectoryOfAllImages = detection.__PathToAllImages()
    
        for BGR_image in DirectoryOfAllImages:
        
            BGR_image = cv2.imread(BGR_image)
            BGRImage = cv2.bilateralFilter(BGR_image, 9, 200 ,75)

            detection(BGR_image)

            if detection.SaveBilateralfilterImage == True:
                cv2.imwrite('C:\\Users\\tom_l\\color-detection-data\\testresults\\bilateralfilter_{}.png'.format(detection.ImageNumber), BGR_image)

    def __PathToAllImages():
    
        path = 'C:\\Users\\tom_l\\color-detection-data\\images\\*.png'
        DirectoryOfAllImages = glob.glob(path)

        return DirectoryOfAllImages

    def RemoveAllImages():
    
        DirectoryOfAllImages = detection.__PathToAllImages()
    
        for BGR_image in DirectoryOfAllImages:
            os.remove(BGR_image)

#----------------------------------------Start Detection---------------------------------------

    def StartColorDetection(self):

        ArrayWithDetectedPixels = self.__ReturnArrayWithDetectedPixels(self.HSV_Image)
        detection.TotalAmountPlasticPixels = detection.TotalAmountPlasticPixels + len(ArrayWithDetectedPixels)

        for HSV_Pixel in ArrayWithDetectedPixels:
            self.__AddPixelToCorrespondingColor(HSV_Pixel)

        

#----------------------------------------Detect plastic----------------------------------------

    def __ReturnBinaryArrayOfDetectedPixels(self, HSV_Image):

        V_Image = np.delete(HSV_Image, [0,1], axis = 2)
        BinaryArrayOfDetectedPixels = V_Image <= detection.BeltValue
        
        if detection.SaveDetectedPlasticImage == True:
            self.SaveBinaryImage(BinaryArrayOfDetectedPixels)
        
        BinaryArrayOfDetectedPixels = np.repeat(BinaryArrayOfDetectedPixels [:], 3, axis=1)
        
        return BinaryArrayOfDetectedPixels
    
    def __ReturnArrayWithDetectedPixels(self, HSV_Image):

        BinaryArrayOfDetectedPixels = self.__ReturnBinaryArrayOfDetectedPixels(HSV_Image)
        ArrayOfAllDetecedPlasticPixels = ma.masked_array((self.HSV_Image), mask = BinaryArrayOfDetectedPixels)
        
        height, width, channels = HSV_Image.shape        
        ArrayOfAllDetecedPlasticPixels = np.reshape(ArrayOfAllDetecedPlasticPixels, ((height * width), 3))
        ArrayOfAllDetecedPlasticPixels = ma.compress_rows(ArrayOfAllDetecedPlasticPixels)

        return ArrayOfAllDetecedPlasticPixels

#----------------------------------------Add pixel to correct color----------------------------------------
        

    def __AddPixelToCorrespondingColor(self, HSV_Pixel):   

        if self.__CheckIfPixelIsColor(HSV_Pixel) == False:

            if self.__CheckIfPixelIsWhite(HSV_Pixel) == True:
                self.__AddWhitePixelToAmountOfWhitePixels()
            elif self.__CheckIfPixelIsGrey(HSV_Pixel) == True:
                self.__AddGreyPixelToAmountOfGreyPixels()
            else: 
                self.__AddBlackPixelToAmountOfBlackPixels()
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

    def __CheckIfPixelIsColor(self, HSV_Pixel):

        if detection.MaxSaturation <= HSV_Pixel[1]:
            return True
        else:
            return False
                    
    def __CheckIfPixelIsWhite(self, HSV_Pixel):
     
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

#----------------------------------------Calculate Percentages----------------------------------------


    def CalcAllPercentages():
        
        try:

            detection.PercentageBlack = round(detection.__CalcBlackPercentage(), detection.NumberOfDecimals) 
            detection.PercentageWhite = round(detection.__CalcWhitePercentage(), detection.NumberOfDecimals)
            detection.PercentageGrey = round(detection.__CalcGreyPercentage(), detection.NumberOfDecimals)


            for CurrentColor in color.AllColors:
            
                CurrentColor.percentage = detection.__CalcPercentages(CurrentColor)
                CurrentColor.Percentage = round(CurrentColor.percentage, detection.NumberOfDecimals)

        except ZeroDivisionError:
            
            pass

        return True
            
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

#----------------------------------------SETTERS----------------------------------------
 
    def SetBeltValue(BeltValue):
        
        detection.BeltValue = BeltValue 

    def SetWhiteValue(WhiteValue):

        detection.WhiteValue = WhiteValue 

    def SetBlackValue(BlackValue):

        detection.BlackValue = BlackValue 
        
    def SetMaxSaturation(MaxSaturation):
        
        detection.MaxSaturation = MaxSaturation 

#----------------------------------------GETTERS----------------------------------------
        
    def GetAmountOfPicturesToBeTaken():
        
        return detection.AmountOfPicturestToBeTaken 

    def GetBeltValue():
        
        return detection.BeltValue 

    def GetWhiteValue():

        return detection.WhiteValue

    def GetBlackValue():

        return detection.BlackValue 

    def GetNumberOfDecimals():
        
        return detection.NumberOfDecimals 
        
    def GetMaxSaturation():
        
        return detection.MaxSaturation 

#----------------------------------------Print----------------------------------------


    def PrintTotalAmountPlasticPixels():

        print('the amount of detected pixels is', detection.TotalAmountPlasticPixels, '\n')

    def PrintBeltValue():

        print('BeltValue is ', detection.BeltValue, '\n')

    def PrintWhiteValue():

        print('WhiteValue is', detection.WhiteValue, '\n')

    def PrintBlackValue():

        print('BlackValue is', self.BlackValue, '\n')

    def PrintTotalTotalAmountBlackPixels(): 
           
        print('number of black pixels is ', detection.TotalAmountBlackPixels, '\n')

    def PrintTotalAmountGreyPixels():

        print('number of grey pixels is', detection.TotalAmountGreyPixels)
        
    def PrintTotalAmountWhitePixels():   
         
        print('number of white pixels is', detection.TotalAmountWhitePixels, '\n')

#----------------------------------------additional functions----------------------------------------
        

    def SaveBinaryImage(self, BinaryArrayOfDetectedPixels):
        
        BinaryArrayOfDetectedPixels.dtype = 'uint8'
        BinaryArrayOfDetectedPixels[BinaryArrayOfDetectedPixels > 0] = 255
        cv2.imwrite('C:\\Users\\tom_l\\color-detection-data\\testresults\\binaryimage_{}.png'.format(self.ImageNumber), BinaryArrayOfDetectedPixels)
        

    def WriteDataToTXTfile():

        DataFile = open('C:\\Users\\tom_l\\color-detection-data\\testresults\\data.txt', 'w')
    
        DataFile.write('Analysed all pictures in folder\n')
        DataFile.write('{} % is white \n{} % is grey \n{} % is black \n\n'.format(detection.PercentageWhite, detection.PercentageGrey, detection.PercentageBlack))
    
        for CurrentColor in color.AllColors:
             DataFile.write('{} % is {} \n'.format(CurrentColor.Percentage, CurrentColor.name))

