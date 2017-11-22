# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 20-11-2017


class Color:
    AllColors = []
    
    def __init__(self, name, RightAngle, LeftAngle):
        self.name = name
        self.LeftAngle = LeftAngle
        self.RightAngle = RightAngle
        self.AmountOfDetectedPixels = 0
        self.Percentage = 0
        self.__AddColorToAllColors()

    #private
    def __AddColorToAllColors(self): 
        Color.AllColors.append(self)

    def PrintAllColors():
        print(Color.AllColors)

    def PrintAmountOfDetectedPixels(self):
        print('The amount of detected pixels is', self.AmountOfDetectedPixels)
        
    def PrintPercentage(self):
        print(self.Percentage, '% is ', self.name)

    def PrintLeftAngle(self):
        print('LeftAngle is :', self.LeftAngle)

    def PrintRightAngle(self):
        print('RightAngle is : ', self.RightAngle)




















    

        



