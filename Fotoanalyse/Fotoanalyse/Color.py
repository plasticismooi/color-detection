class Color:
    AllColors = []
    

    def __init__(self, HorizontalAngle, VerticalAngle):
        self.HorizontalAngle = HorizontalAngle
        self.VerticalAngle = VerticalAngle
        self.__AddColorToAllColors()

        

    #private
    def __AddColorToAllColors(self): 
        Color.AllColors.append(self)

    def PrintAllColors(self):
        print(Color.AllColors)

    def PrintHorizontalAngle(self):
        print('HorizontalAngle is :', self.HorizontalAngle)

    def PrintVerticalAngle(self):
        print('VerticalAngle is : ', self.VerticalAngle)



















    

        



