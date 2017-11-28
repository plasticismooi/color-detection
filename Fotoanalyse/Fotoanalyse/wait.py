# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017

class wait:

    BeltSpeed = None
    PictureWidth = None
    PictureInterval = None

    def __init__(self):

        pass

    def SetBeltSetting(BeltSetting):

        if BeltSetting == 0:
            wait.BeltSpeed = 0.53
        elif BeltSetting == 1:
            wait.BeltSpeed = 0.065
        elif BeltSetting == 2:
            wait.BeltSpeed = 0.078
        elif BeltSetting == 3:
            wait.BeltSpeed = 0.091
        elif BeltSetting == 4:
            wait.BeltSpeed = 0.104
        elif BeltSetting == 5:
            wait.BeltSpeed = 0.120
        elif BeltSetting == 6:
            wait.BeltSpeed = 0.135
        elif BeltSetting == 7:
            wait.BeltSpeed = 0
        elif BeltSetting == 8:
            wait.BeltSpeed = 0
        elif BeltSetting == 9:
            wait.BeltSpeed = 0
        else:
            wait.BeltSpeed = 0

    def PrintBeltSpeed():

        print(wait.BeltSpeed)

    def SetPictureWidth(PictureWidth):

        wait.PictureWidth = PictureWidth 

    def CalculateWaitingTime():

        try:
            wait.PictureInterval =   wait.PictureWidth / wait.BeltSpeed

        except TypeError:

            print ('WARNING')
            print ('set value for picture width and or belt setting')
        
        

        

    



   


