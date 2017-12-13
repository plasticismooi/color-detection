# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017


class color:
    AllColors = []
    
    def __init__(self, name, LeftAngle, RightAngle):
        self.name = name
        self.LeftAngle = LeftAngle
        self.RightAngle = RightAngle
        self.AmountOfDetectedPixels = 0
        self.Percentage = 0
        self.__AddColorToAllColors()

    def __AddColorToAllColors(self): 
        color.AllColors.append(self)

    def PrintAllColors():
        print(color.AllColors)

    def PrintAmountOfDetectedPixels(self):
        print('The amount of detected pixels is', self.AmountOfDetectedPixels)
        
    def PrintPercentage(self):
        print(self.Percentage, '% is ', self.name)

    def PrintLeftAngle(self):
        print('LeftAngle is :', self.LeftAngle)

    def PrintRightAngle(self):
        print('RightAngle is : ', self.RightAngle)


        # functions called by colorscreen class
    def SetLeftAngle(self, instance, value):

        self.LeftAngle = value
        print('the left angle of {} is set to {}'.format(self.name, value))

    def SetrightAngle(self, instance, value):

        self.RightAngle = value
        print('the rigth angle of {} is set to {}'.format(self.name, value))

    def RemoveColor(self, instance):
        
        print('color {} removed'.format(self.name))
        del self
           





















    

        



