# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 28-11-2017

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import cv2
import time
import math
import numpy.ma as ma
from time import sleep


#project .py files
from detection import detection
from color import color
from wait import wait




#----------------------------------------Function for writing data to text file---------------------------------------


def WriteDataTotxtFile():
    DataFile = open('/media/pi/9E401DB5401D94DD/Color-detection-data/data.txt', 'w')
    
    DataFile.write('Analysed all pictures in folder /media/pi/9E401DB5401D94DD/Pictures''\n')
    DataFile.write('{} % is white \n{} % is grey \n{} % is black \n\n'.format(detection.PercentageWhite, detection.PercentageGrey, detection.PercentageBlack))
    
    for CurrentColor in color.AllColors:
        DataFile.write('{} % is {} \n'.format(CurrentColor.Percentage, CurrentColor.name))

#----------------------------------------config settings----------------------------------------


print('Preparing Detection...')

detection.SetAmountOfPicturestToBeTaken(30)
detection.SetNumberOfDecimals(2) #max 14

detection.SaveDetectedPlasticImage(False)
detection.SaveBilateralfilterImage(False)


detection.SetBeltValue(40) # 40 corresponds with light setting 2

detection.SetBlackValue(20)
detection.SetWhiteValue(75)
detection.SetMaxSaturation(25)

wait.SetBeltSetting(0)
wait.SetPictureWidth(0.1675)
wait.CalculateWaitingTime()

#----------------------------------------color definitions----------------------------------------


print('Preparing Colors...')


color('red', 340, 15)
color('orange', 16, 40)
color('yellow', 41, 70)
color('green', 71, 160)
color('light blue', 161, 190)
color('dark blue', 191, 270)
color('purple', 271, 339)


#----------------------------------------read image----------------------------------------



#----------------------------------------Kivy----------------------------------------

import kivy
import kivy.event

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy import clock
from kivy.clock import Clock
from kivy.uix.widget import Widget





class WaitingScreen(Screen):

    pass


class StartScreen(Screen):
        
    def StartTakingPictures(self):
      
        Clock.schedule_interval(self.TakePicture, 1)
         
    def TakePicture(self, interval):

        print('picture taken')

    def StopTakingPictures(self):

        try:
            
            Clock.unschedule(self.TakePicture)
            print('stopped taking pictures')

        except NameError:
            pass


class ResultScreen(Screen):

    pass

class ConfigurationScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(ConfigurationScreen, self).__init__(*args, **kwargs)
        self.drop_down = DropDown()
        

class DropDown(DropDown):

    pass
               
Builder.load_file('interface.kv')

sm = ScreenManager()
Start = StartScreen(name = 'Start')
Configuration = ConfigurationScreen(name = 'Configuration')
sm.add_widget(Start)
sm.add_widget(Configuration)


class ColorApp(App):

    def build(self):
       
        return sm

ColorApp().run()



#----------------------------------------END PROGRAM----------------------------------------

























    





                
               


