# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 22-11-2017


class wait:

    BeltSpeed = 1
    PictureWidth = 1
    PictureInterval = 1

    def __init__(self):

        pass

    def SetBeltSpeed(self, BeltSetting):

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

    def Calculatewait():

        wait.PictureInterval = wait.BeltSpeed / wait.PictureWidth
        
        

        

    



   


