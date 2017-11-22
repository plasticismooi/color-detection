#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 20-11-2017

import cv2
from color import color
import math
import numpy.ma as ma
import numpy as np
#object in this class is a picture

class detection:
    
    ListOfAllImages = []
    TotalAmountPlasticPixels= 0

    NumberOfDecimals = 2
    
    BeltColorRadius = 155

    LowestWhiteValue = 70
    HighestBlackValue = 20
    LongestGreyRadius = 5

    TotalAmountWhitePixels = 0
    TotalAmountBlackPixels = 0
    TotalAmountGreyPixels = 0
    
    PercentageWhite = 0
    PercentageBlack = 0
    PercentageGrey = 0

    def __init__(self, RGB_image, LAB_image):
        self.RGB_image = RGB_image
        self.LAB_image = LAB_image
        self.__AddToListOfAllImages()

    def __AddToListOfAllImages(self):

        detection.ListOfAllImages.append(self)

    def StartColorDetection(self):

        ArrayWithPlasticPixels = self.__GetArrayWithPlasticPixels()
        
        detection.TotalAmountPlasticPixels = detection.TotalAmountPlasticPixels + len(ArrayWithPlasticPixels)

        for PlasticPixel_LAB in ArrayWithPlasticPixels:

            self.__AddPixelToCorrespondingColor(PlasticPixel_LAB)
        

           

    def __GetArrayWithPlasticPixels(self):
        #True if pixels is the belt, False if pixel is plastic
        BinaryArrayOfDetectedPlastic = self.__ConvertImageToBinaryArray()
        

        height, width, channels = self.LAB_image.shape
        ArrayOfAllDetecedPlasticPixels3D = ma.masked_array((self.LAB_image), mask = BinaryArrayOfDetectedPlastic)
        ArrayOfAllDetecedPlasticPixels3D = np.reshape(ArrayOfAllDetecedPlasticPixels3D, ((height * width), 3))

        #delete [-- -- --] from ArrayWithDetectedPixels3D
        ArrayOfAllDetecedPlasticPixel2D = ma.compress_rows(ArrayOfAllDetecedPlasticPixels3D)
        
        return ArrayOfAllDetecedPlasticPixel2D 

    def __ConvertImageToBinaryArray(self):
        
        #create temporary image copy with sqrt(R^2+B^2+G^2)
        RGB_imageSquared = np.array(self.RGB_image, dtype = 'uint32')**2
        RGB_imagePythagorean = np.sum(RGB_imageSquared, axis = 2)

        #create bitmask with detected pixels as True and the conveyerbelt as False
        BinaryArrayOfDetectedPlastic = RGB_imagePythagorean <= detection.BeltColorRadius**2
        BinaryArrayOfDetectedPlastic = np.repeat(BinaryArrayOfDetectedPlastic[:, :, np.newaxis], 3, axis=2)

        return BinaryArrayOfDetectedPlastic
   
    def __AddPixelToCorrespondingColor(self, PlasticPixel_LAB):   

        if self.__CheckIfPixelIsWhite(PlasticPixel_LAB) == True:
            self.__AddWhitePixelToAmountOfWhitePixels()
        elif self.__CheckIfPixelIsBlack(PlasticPixel_LAB) == True:
            self.__AddBlackPixelToAmountOfBlackPixels()
        elif self.__CheckIfPixelIsGrey(PlasticPixel_LAB) == True:
            self.__AddGreyPixelToAmountOfGreyPixels()
        else:
            self.__AddPixelToCorrectColor(PlasticPixel_LAB)

    def __AddPixelToCorrectColor(self, PlasticPixel_LAB):
        angle = self.__CalculateAngle(PlasticPixel_LAB)

        for CurrentColor in color.AllColors:

            if self.__CheckIfAnglesCrossBAxis(CurrentColor) == True:
                self.__AddPixelToCorrectColorIfAnglesCrossBAxis(CurrentColor, angle)
            else:
                #function __AddPixelToCurrentColor returns true when the pixels matches a color
                 if self.__AddPixelToCurrentColor(CurrentColor, angle) == True:
                     return

    def __CheckIfPixelIsWhite(self, PlasticPixel_LAB):
            
            if PlasticPixel_LAB[0] >= detection.LowestWhiteValue:
                return True
            else:
                return False

    def __CheckIfPixelIsBlack(self, PlasticPixel_LAB):
            
            if PlasticPixel_LAB[0] <= detection.HighestBlackValue:
                return True
            else:
                return False

    def __CheckIfPixelIsGrey(self, PlasticPixel_LAB):

        GreyRadius = self.__CalculateRadius(PlasticPixel_LAB)

        if detection.LongestGreyRadius >= GreyRadius :
            return True
        else: 
            return False

    def __CalculateRadius(self, PlasticPixel_LAB):

        return math.sqrt(PlasticPixel_LAB[1]**2 + PlasticPixel_LAB[2]**2)

    def __AddGreyPixelToAmountOfGreyPixels(self):

        detection.TotalAmountGreyPixels += 1

    def __AddWhitePixelToAmountOfWhitePixels(self):

            detection.TotalAmountWhitePixels += 1

    def __AddBlackPixelToAmountOfBlackPixels(self):

            detection.TotalAmountBlackPixels += 1

    def __AddPixelToCurrentColor(self, CurrentColor, angle):
        if CurrentColor.LeftAngle >= angle:
            if CurrentColor.RightAngle <= angle:
                CurrentColor.AmountOfDetectedPixels += 1
                return True
            else:
                return False

    def __AddPixelToCorrectColorIfAnglesCrossBAxis(self, CurrentColor, angle):

        if (CurrentColor.LeftAngle >= angle) | (CurrentColor.RightAngle <= angle):
            CurrentColor.AmountOfDetectedPixels += 1
            return

    def __CheckIfAnglesCrossBAxis(self, CurrentColor):
        if CurrentColor.LeftAngle < CurrentColor.RightAngle:
            return True
        else:
            return False

    def __CalculateAngle(self, PlasticPixel_LAB):

        a = PlasticPixel_LAB[1] 
        b = PlasticPixel_LAB[2] 
        
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

    def CalcAllPercentages():
        
        if detection.TotalAmountPlasticPixels == 0:
            print('NO PLASTIC DETECTED \n')
            return

        detection.PercentageBlack = round(detection.__CalcBlackPercentage(), detection.NumberOfDecimals) 
        detection.PercentageWhite = round(detection.__CalcWhitePercentage(), detection.NumberOfDecimals)
        detection.PercentageGrey = round(detection.__CalcGreyPercentage(), detection.NumberOfDecimals)


        for CurrentColor in color.AllColors:
            
            CurrentColor.percentage = detection.__CalcPercentages(CurrentColor)
            CurrentColor.Percentage = round(CurrentColor.percentage, detection.NumberOfDecimals)
            
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
    def SetLowestWhiteValue(LowestWhiteValue):

        detection.LowestWhiteValue = LowestWhiteValue

    def PrintLowestWhiteValue():

        print('white boundary is', self.LowestWhiteValue, '\n')

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



        

        






       
