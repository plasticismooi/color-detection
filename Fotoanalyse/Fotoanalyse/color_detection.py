#OOP approach for color detection
# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 3-11-2017

import cv2
from Color import Color

#object in this class is a picture
class color_detection:

    
    TotalPixels = 0
    #standard boundary is 155, adjust with SetBoundary() if needed
    boundary = 155

    def __init__(self, image):
        self.image = image
        
        #detection in RGB or CIELAB?

    def detect(self, loopvariableY, loopvariableX, color):
        #actual detection of colors
        self.loopvariableY = loopvariableY
        self.loopvariableX = loopvariableX

        #use angels to calculate coordinates

        #check y,x for calcutated coordinates

    def PrintTotalPixels(self):
        print(self.TotalPixels, '\n')

    def SetBoundary(self, boundary):
        self.boundary = boundary

    def PrintBoundary(self):
        print('boundary is', self.boundary, '\n')




       