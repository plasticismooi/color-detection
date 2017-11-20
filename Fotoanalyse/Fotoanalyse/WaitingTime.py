class WaitingTime:

    BeltSpeed = 1
    PictureWidth = 1
    PictureInterval = 1

    def __init__(self):

        pass

    def SetBeltSpeed(self, BeltSetting):

        if BeltSetting == 0:
            WaitingTime.BeltSpeed = 0.53
        elif BeltSetting == 1:
            WaitingTime.BeltSpeed = 0.065
        elif BeltSetting == 2:
            WaitingTime.BeltSpeed = 0.078
        elif BeltSetting == 3:
            WaitingTime.BeltSpeed = 0.091
        elif BeltSetting == 4:
            WaitingTime.BeltSpeed = 0.104
        elif BeltSetting == 5:
            WaitingTime.BeltSpeed = 0.120
        elif BeltSetting == 6:
            WaitingTime.BeltSpeed = 0.135
        elif BeltSetting == 7:
            WaitingTime.BeltSpeed = 0
        elif BeltSetting == 8:
            WaitingTime.BeltSpeed = 0
        elif BeltSetting == 9:
            WaitingTime.BeltSpeed = 0
        else:
            WaitingTime.BeltSpeed = 0

    def PrintBeltSpeed():

        print(WaitingTime.BeltSpeed)

    def SetPictureWidth(PictureWidth):

        WaitingTime.PictureWidth = PictureWidth 

    def CalculateWaitingTime():

        PictureInterval = WaitingTime.BeltSpeed / WaitingTime.PictureInterval
        return PictureInterval
        

        

    



   


