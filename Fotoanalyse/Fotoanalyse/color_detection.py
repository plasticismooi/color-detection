#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 1-11-2017

import cv2

class color_detection:

    TotalPixels = 0
    #standard boundary is 155, adjust with SetBoundary() if needed
    boundary = 155
    zwart = 0
    wit = 0
    kleur = 0 

    def __init__(self, image):
        self.image = image
        
        #detection in RGB or CIELAB?

    def Detect(self):

        height, width, channels = self.image.shape
        LAB_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)

        for LoopVariableY in range(height):
            for LoopVariableX in range(width):

                BGR_array = self.image[LoopVariableY,LoopVariableX]
                if (((BGR_array[0]**2) + (BGR_array[1]**2) + (BGR_array[2]**2)) > self.boundary**2):
          
                    LAB_array = LAB_image[LoopVariableY,LoopVariableX]

                    #assenstelsel aanpassen naar 0-100
                    LAB_array[0] = (LAB_array[0] * 0.392)

                    if ( LAB_array[0] < 21):
                        self.zwart += 1
                    elif ((LAB_array[0] > 20) & (LAB_array[0] < 70)):
                        self.kleur += 1
                    elif ( LAB_array[0] >= 70 ):
                        self.wit += 1
        
        TotalPixels = self.wit + self.kleur + self.zwart
        self.TotalPixels = TotalPixels

    def CombineAllImages(self, ):
        #loop all instances and add wit, zwart, kleur accordingly



    def PrintTotalPixels(self):
        print(self.TotalPixels, '\n')

    def SetBoundary(self, boundary):
        self.boundary = boundary

    def PrintBoundary(self):
        print('boundary is', self.boundary, '\n')
       
        
    def PrintPercentages(self):
        if (self.TotalPixels != 0): 

            proc_zwart = (self.zwart / self.TotalPixels) * 100
            proc_kleur = (self.kleur / self.TotalPixels) * 100
            proc_wit = (self.wit / self.TotalPixels) * 100 
            #print data
            
            print(proc_wit)
            print('procent is wit''\n')
            print(proc_kleur)
            print('procent is kleur''\n')
            print(proc_zwart)
            print('procent is zwart''\n')
        else:
            print('er liggen geen plastic flakes op de foto')


        









        


