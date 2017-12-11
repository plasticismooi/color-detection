# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017

class wait:

    BeltSpeed = None
    PictureWidth = None
    PictureInterval = 1

    def __init__(self):

        pass

    def SetBeltSetting(BeltSetting):


        BeltspeedDict = {0: 0.054, 1: 0.065, 2: 0.078, 3: 0.091, 4: 0.104, 5: 0.120, 6: 0.135}

        BeltspeedDict['BeltSpeed'] = wait.BeltSpeed


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
        
        

        

    



   


