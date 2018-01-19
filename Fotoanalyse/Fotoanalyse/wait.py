# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# company: Polytential B.V.
# date : 19-1-2018

class wait:

    BeltSetting = 3
    BeltSpeed = 0.09
    PictureWidth = 0.13
    PictureInterval = 1

    def __init__(self):

        pass

    def SetBeltSetting(BeltSetting):

        BeltSetting = int(BeltSetting)

        BeltSpeedDict = {0: 0.053, 1: 0.065, 2: 0.078, 3: 0.09, 4: 0.104, 5: 0.120, 6: 0.135}

        wait.BeltSpeed = BeltSpeedDict.get(BeltSetting)

    def PrintBeltSpeed():

        print(wait.BeltSpeed)

    def SetPictureWidth(PictureWidth):

        wait.PictureWidth = PictureWidth 

    def CalculateWaitingTime():

        try:
            wait.PictureInterval =   wait.PictureWidth / wait.BeltSpeed
            print(wait.PictureInterval)

        except TypeError:

            pass
        
        

        

    



   


