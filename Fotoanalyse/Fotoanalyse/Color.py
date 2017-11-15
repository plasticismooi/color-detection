class Color:
    AllColors = []
    
    def __init__(self, name, RightAngle, LeftAngle):
        self.name = name
        self.LeftAngle = LeftAngle
        self.RightAngle = RightAngle
        self.PixelCount = 0
        self.__AddColorToAllColors()

    #private
    def __AddColorToAllColors(self): 
        Color.AllColors.append(self)

    def PrintAllColors():
        print(Color.AllColors)

    def PrintPixelCount(self):
        print('total PixelCount is', self.PixelCount)

    def PrintLeftAngle(self):
        print('LeftAngle is :', self.LeftAngle)

    def PrintRightAngle(self):
        print('RightAngle is : ', self.RightAngle)




















    

        



