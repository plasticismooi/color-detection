# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 5-1-2018

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import cv2
import time
import math
import numpy.ma as ma
from time import sleep
import os
import glob
from functools import partial
import gc
import datetime

#project .py files
from detection import detection
from color import color
from wait import wait
from kivy.config import Config

#-----------------------------------Functions----------------------------------- 
def LoadPreSetColors():

    with open('basecolors.txt', 'r') as txtfile:

        for line in txtfile:

             line = line.strip() 

             if line:

                    Name, LeftAngle, RightAngle = line.split(" ")

                    color(Name, int(LeftAngle), int(RightAngle))

#----------------------------------------INTERFACE----------------------------------------

import kivy
import kivy.event

from kivy.uix import *
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.switch import Switch
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty
from kivy import clock
from kivy.clock import Clock
from kivy.uix.widget import Widget

#-----------------------------------init-----------------------------------

LoadPreSetColors()

Config.set('graphics', 'resizable', '0') 
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '600')

#-----------------------------------Screen classes-----------------------------------

class StartScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(StartScreen, self).__init__(*args, **kwargs)

        self.LayoutStartScreenInstance = LayoutStartScreen()
        self.add_widget(self.LayoutStartScreenInstance)



class ResultScreen(Screen):

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)

        self.LayoutResultScreenInstance = LayoutResultScreen()
        self.add_widget(self.LayoutResultScreenInstance)
        
class CalculationScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(CalculationScreen, self).__init__(*args, **kwargs)

    def CalculateResults(self):

        detection.PrepareAllImagesForDetection()

        for image in detection.ListOfAllImages:
            image.StartColorDetection()

        detection.CalcAllPercentages()

        if detection.EnableWriteDataToTXTfile == True:
            detection.WriteDataToTXTfile()

        ColorDetectionInterface.switch_to(ResultScreen())
        
class TakingPicturesScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(TakingPicturesScreen, self).__init__(*args, **kwargs)

        self.TakingPicturesScreenLayoutInstance = TakingPicturesScreenLayout()
        self.add_widget(self.TakingPicturesScreenLayoutInstance)

class SettingsScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(SettingsScreen, self).__init__(*args, **kwargs)
       
        self.LayoutSettingsScreenInstance = LayoutSettingsScreen()
        self.add_widget(self.LayoutSettingsScreenInstance)



#-----------------------------------Layout classes-----------------------------------

class TakingPicturesScreenLayout(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(TakingPicturesScreenLayout, self).__init__(*args, **kwargs)

        self.orientation = 'vertical'
        
        self.StartCalculationButton = Button(text = 'Calculate results', size_hint=(1, 0.9))
        self.StartCalculationButton.bind(on_press = self.StartCalculation)

        self.GoToStartScreenButton = Button(text = 'CANCEL', size_hint=(1, 0.1))
        self.GoToStartScreenButton.bind(on_press = self.GoToStartScreen)

        self.add_widget(self.StartCalculationButton)
        self.add_widget(self.GoToStartScreenButton)

        self.camera = cv2.VideoCapture(1)
        self.PictureNumber = 0

    def StartTakingPictures(self):

        self.RemoveAllImages()
        
        #called on enter via .kv
        Clock.schedule_interval(self.TakePicture, 1)
         
    def TakePicture(self, interval):

        ret, frame = self.camera.read()
        if not ret:

            return
           
        ImageName = 'C:\\Users\\tom_l\\color-detection-data\\images\\image_{}.png'.format(self.PictureNumber)
        cv2.imwrite(ImageName, frame)
        print("{} saved".format(ImageName))
        self.PictureNumber += 1

    def GoToStartScreen(self, instance):

        try:
            Clock.unschedule(self.TakePicture)
            self.PictureNumber = 0
            print('stopped taking pictures')

        except NameError:
            pass

        self.RemoveAllImages()
        ColorDetectionInterface.switch_to(StartScreen())

    def StartCalculation(self, interval):

        try:

            Clock.unschedule(self.TakePicture)
            print('stopped taking pictures')

            self.camera.release()



        except NameError:
            pass

        ColorDetectionInterface.switch_to(CalculationScreen())

    def PathToAllImages(self):
    
        path = 'C:\\Users\\tom_l\\color-detection-data\\images\\*.png'
        DirectoryOfAllImages = glob.glob(path)
    
        return DirectoryOfAllImages

    def RemoveAllImages(self):
    
        DirectoryOfAllImages = self.PathToAllImages()
    
        for BGR_image in DirectoryOfAllImages:
            os.remove(BGR_image)

class LayoutStartScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LayoutStartScreen, self).__init__(**kwargs)

        self.orientation = 'horizontal'

        self.AllColorWidgetsInstance = AllColorWidgets()
        self.ColorCicleAndButtons = StartCircleAndButtons()

        self.add_widget(self.AllColorWidgetsInstance)
        self.add_widget(self.ColorCicleAndButtons)


class LayoutSettingsScreen(GridLayout):

    def __init__(self, *args, **kwargs):
        super(LayoutSettingsScreen, self).__init__(*args, **kwargs)

        self.rows = 11
        self.cols = 2

        #switches
        self.SaveDetectedPlasticImageSwitchLabel = Label(text = 'Save image with detected plastic for each picture: ')
        self.SaveDetectedPlasticImageSwitch = Switch()
        self.SaveDetectedPlasticImageSwitch.bind(active = self.TurnSaveDetectedPlasticImageOn)

        self.SaveBilateralfilterImageSwitchLabel = Label(text = 'Save image with bilateral filter for each picture: ')
        self.SaveBilateralfilterImageSwitch = Switch()
        self.SaveBilateralfilterImageSwitch.bind(active = self.TurnSaveBilateralfilterImageOn)

        self.WriteDataToTXTfileSwitchLabel = Label(text = 'Write data to .txt file: ')
        self.WriteDatatoTXTfileSwitch = Switch(active = True)
        self.WriteDatatoTXTfileSwitch.bind(active = self.WriteDataToTXTfile)

        #integer textinput
        self.InputBeltValueLabel = Label(text = 'Set the value of the belt in \n"value/brightness" from HSV: ')
        self.InputBeltValue = TextInput(text = '{}'.format(detection.BeltValue), multiline = False, input_filter = 'float')
        self.InputBeltValue.bind(text = self.SetBeltValue)

        self.InputBlackValueLabel = Label(text = 'Set the value of the color black in "\nvalue/brightness" from HSV: ')
        self.InputBlackValue = TextInput(text = '{}'.format(detection.BlackValue), multiline = False, input_filter = 'float')
        self.InputBlackValue.bind(text = self.SetBlackValue)

        self.InputWhiteValueLabel = Label(text = 'Set the value of the color white in \n"value/brightness" from HSV: ')
        self.InputWhiteValue = TextInput(text = '{}'.format(detection.WhiteValue), multiline = False, input_filter = 'float')
        self.InputWhiteValue.bind(text = self.SetWhiteValue)
        
        self.InputMaxSaturationValueLabel = Label(text = 'The maximal saturation of "S" in HSV for a color\nthe to be defined as white/grey/black: ')
        self.InputMaxSaturationValue = TextInput(text = '{}'.format(detection.MaxSaturation), multiline = False, input_filter = 'float')
        self.InputMaxSaturationValue.bind(text = self.SetMaxSaturation)

        self.InputBeltSettingLabel = Label(text = 'Input the speed setting of the belt')
        self.InputBeltSetting = TextInput(text = '{}'.format(wait.BeltSetting), multiline = False, input_filter = 'int')
        self.InputBeltSetting.bind(text = self.SetBeltSpeedSetting)

        self.InputPictureWidthLabel = Label(text = 'Input the width of the pictures in meters')
        self.InputPictureWidth = TextInput(text = '{}'.format(wait.PictureWidth), multiline = False, input_filter = 'float')
        self.InputPictureWidth.bind(text = self.SetPictureWidth)
        
        #buttons
        self.ReturnToStartScreenButton = Button(text = 'To Startscreen')
        self.ReturnToStartScreenButton.bind(on_press = self.GoToStartScreen)

      
        self.add_widget(self.SaveDetectedPlasticImageSwitchLabel)
        self.add_widget(self.SaveDetectedPlasticImageSwitch)

        self.add_widget(self.SaveBilateralfilterImageSwitchLabel)
        self.add_widget(self.SaveBilateralfilterImageSwitch)

        self.add_widget(self.WriteDataToTXTfileSwitchLabel)
        self.add_widget(self.WriteDatatoTXTfileSwitch)

        self.add_widget(self.InputBeltValueLabel)
        self.add_widget(self.InputBeltValue)

        self.add_widget(self.InputBlackValueLabel)
        self.add_widget(self.InputBlackValue)

        self.add_widget(self.InputWhiteValueLabel)
        self.add_widget(self.InputWhiteValue)

        self.add_widget(self.InputMaxSaturationValueLabel)
        self.add_widget(self.InputMaxSaturationValue)

        self.add_widget(self.InputBeltSettingLabel)
        self.add_widget(self.InputBeltSetting)

        self.add_widget(self.InputPictureWidthLabel)
        self.add_widget(self.InputPictureWidth)
       
        self.add_widget(self.ReturnToStartScreenButton)

    def GoToStartScreen(self, instance):

        ColorDetectionInterface.switch_to(StartScreen())

    def WriteDataToTXTfile(self, instance, value):

        if value == False:
            detection.EnableWriteDataToTXTfile = False

        else:
            detection.EnableWriteDataToTXTfile = True

    def SetPictureWidth(self, instance, value):

        wait.PictureWidth = float(value)
        wait.CalculateWaitingTime()

    def SetBeltSpeedSetting(self, instance, value):

        wait.BeltSetting = int(value)
        wait.CalculateWaitingTime()

    def SetMaxSaturation(self, instance, value):
        value = float(value)
        detection.SetMaxSaturation = value
       
    def SetWhiteValue(self, instance, value):
        WhiteValue = float(value) 
        detection.SetWhiteValue(WhiteValue)
        
    def SetBlackValue(self, instance, value):
        value = float(value)
        detection.SetBlackValue(value)
        
    def SetBeltValue(self, instance, value):
        value = float(value)
        detection.SetBeltValue(value)
        
    def TurnSaveBilateralfilterImageOn(self, instance, value):
        if value == True:
            detection.SaveBilateralfilterImage = True
            print('saving all images with bilateral filter')
        else: 
            detection.SaveBilateralfilterImage = False
            print('deactivated saving all images with bilateral filter')
  
    def TurnSaveDetectedPlasticImageOn(self, instance, value):
        if value == True:
            detection.SaveDetectedPlasticImage = True 
            print('saving all images with detected plastic flakes')
        else:
            detection.SaveBilateralfilterImage = False 
            print('deactivated saving all images with detected plastic flakes')

class LayoutResultScreen(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(LayoutResultScreen, self).__init__(*args, **kwargs)

        self.orientation = 'vertical'

        self.ShowPercentgesInstance = ShowPercentages()

        self.ToStartScreenButton = Button(text = 'To Startscreen', size_hint=(1, 0.1))
        self.ToStartScreenButton.bind(on_press = self.ToStartScreen)

        #add open txt file option button 

        self.add_widget(self.ShowPercentgesInstance)
        self.add_widget(self.ToStartScreenButton)

    def ToStartScreen(self, instance):

        ColorDetectionInterface.switch_to(StartScreen())

class StartCircleAndButtons(BoxLayout):

    def __init__(self, **kwargs):
        super(StartCircleAndButtons, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.ColorCircleInstance = ColorCircle()
        self.AllStartScreenButtons = ButtonsStartScreen()

        
        self.add_widget(self.ColorCircleInstance)     
        self.add_widget(self.AllStartScreenButtons)  

#-----------------------------------Custom Widgets----------------------------------- 

class AllColorWidgets(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(AllColorWidgets, self).__init__(*args, **kwargs)

        self.orientation = 'horizontal'

        self.ColorInputInstance = ColorInput()

        self.add_widget(self.ColorInputInstance)

class ButtonsStartScreen(GridLayout):

    def __init__(self, *args, **kwargs):
        super(ButtonsStartScreen, self).__init__(*args, **kwargs)

        self.cols = 1
        self.rows = 2

        self.StartColorDetectionButton = Button(text = 'Start color-detection', )
        self.StartColorDetectionButton.bind(on_press = self.GoToTakingPicuresScreen)

        self.GoToSettingsButton = Button(text = 'to scan-settings', )
        self.GoToSettingsButton.bind(on_press = self.GoToSettingsScreen)

        self.add_widget(self.StartColorDetectionButton)
        self.add_widget(self.GoToSettingsButton)

    def GoToTakingPicuresScreen(self, instance):
        ColorDetectionInterface.switch_to(TakingPicturesScreen())

    def GoToSettingsScreen(self, instance):
        ColorDetectionInterface.switch_to(SettingsScreen())


class ColorInput(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ColorInput, self).__init__(*args, **kwargs)

        self.orientation = 'vertical'

        self.SettingsColorScreenInstance = SettingsColorScreen()
        self.add_widget(self.SettingsColorScreenInstance)

        for CurrentColor in color.AllColors:

            self.PreSetColorWidgetInstance = PreSetColorWidget(CurrentColor)
            self.add_widget(self.PreSetColorWidgetInstance)

        RemainingSlots =  15 - len(color.AllColors)

        for x in range(0, RemainingSlots):

            self.ColorWidgetInstance = ColorWidget()
            self.add_widget(self.ColorWidgetInstance)

class SettingsColorScreen(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(SettingsColorScreen, self).__init__(*args, **kwargs)  
        
        self.CorrectIndicator = True 

        self.orientation = 'horizontal' 

        #labels
        self.NameLabel = Label(text = 'Name')
        self.LeftAngleLabel = Label(text = 'Left')
        self.RightAngleLabel = Label(text = 'Right')


        #buttons
        self.ReturnToConfigScreenButton = Button(text = 'Back')
        self.ReturnToConfigScreenButton.bind(on_press = self.GoToConfigScreen)

        self.ResetColorsButton = Button(text = 'Reset')
        self.ResetColorsButton.bind(on_press = self.ResetColorsToBase)
     
        #adding to widget
        self.add_widget(self.NameLabel)
        self.add_widget(self.LeftAngleLabel)
        self.add_widget(self.RightAngleLabel)
        self.add_widget(self.ResetColorsButton)
        self.add_widget(self.ReturnToConfigScreenButton)

        

    def ResetColorsToBase(self, instance):

        color.AllColors[:] = []
        self.LoadPreSetColors()
        ColorDetectionInterface.switch_to(ColorScreen())

    def GoToConfigScreen(self, instance):

        self.CorrectIndicator = True
        if self.CheckIfColorsAreCorrect() == True:

            ColorDetectionInterface.switch_to(StartScreen())

    def CheckIfColorsAreCorrect(self):

        IndexArray = self.PopulateIndexArray()

        if self.CorrectIndicator == False:

            return

        OverlapArray = self.ReturnOverlapArray(IndexArray) 
        MissingArray = self.ReturnMissingArray(IndexArray)

        if self.CheckForOverlap(OverlapArray) == True:

            self.RaiseOverlapPopup(OverlapArray)
            self.CorrectIndicator = False

        if self.CheckForMissingAngles(MissingArray) == True:

            self.RaiseMissingPopup(MissingArray)
            self.CorrectIndicator = False

        return self.CorrectIndicator

    def PopulateIndexArray(self):

        try:

            IndexArray = np.zeros(360, dtype = np.int8)
        
            for CurrentColor in color.AllColors:

                if CurrentColor.LeftAngle <= CurrentColor.RightAngle:

                    for x in range(CurrentColor.LeftAngle, CurrentColor.RightAngle + 1):

                        IndexArray[x] += 1

                else: 
                    if CurrentColor.LeftAngle >= 360:

                        raise IndexError

                    for x in range(0, CurrentColor.RightAngle + 1):

                        IndexArray[x] += 1

                    for x in range(CurrentColor.LeftAngle, 360):

                        IndexArray[x]  += 1

            return IndexArray

        except IndexError:

            self.CorrectIndicator = False
            self.RaiseIndexErrorPopup()
            return

    def ReturnOverlapArray(self, IndexArray):

        OverlapValue = 2
        OverlapIndexArray = np.nonzero(IndexArray >= OverlapValue)

        if OverlapIndexArray[0].size == 0:

            return False

        else: 

            return OverlapIndexArray

    def ReturnMissingArray(self, IndexArray):

        MissingValue = 0
        MissingIndexArray = np.nonzero(IndexArray == MissingValue)

        if MissingIndexArray[0].size == 0:

            return False

        else: 

            return MissingIndexArray

    def CheckForOverlap(self, OverlapArray):

        if OverlapArray == False:

            return False

        else: 

            return True

    def CheckForMissingAngles(self, MissingArray):

        if MissingArray == False:

            return False

        else: 

            return True

    def RaiseOverlapPopup(self, OverlapArray):
        
        OverlapPopup = Popup(title='OVERLAPPING VALUES! ', content=Label(text='Colors are overlapping on {}\nEnter correct values to start scanning\nPress Esc to leave'.format(OverlapArray[0])), title_color = [1,0,0,1])
        OverlapPopup.open()
        
    def RaiseMissingPopup(self, MissingArray):

        MissingPopup = Popup(title='MISSING VALUES! ', content=Label(text='Value(s) {} are missing \nEnter correct values to start scanning\nPress Esc to leave'.format(MissingArray[0])), title_color = [1,0,0,1])
        MissingPopup.open()   

    def RaiseIndexErrorPopup(self):

        IndexErrorPopup = Popup(title='INPUT ERROR! ', content=Label(text='Values must be in range 0-359 \nEnter correct values to start scanning\nPress Esc to leave'), title_color = [1,0,0,1])
        IndexErrorPopup.open()  

    def LoadPreSetColors(self):

        with open('basecolors.txt', 'r') as txtfile:

            for line in txtfile:

                 line = line.strip() 

                 if line:

                        Name, LeftAngle, RightAngle = line.split(" ")

                        color(Name, int(LeftAngle), int(RightAngle))

class ColorWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ColorWidget, self).__init__(*args, **kwargs)

        self.orientation = 'horizontal'
        self.ColorArray = ['enter name' ,0 ,0 ]

        #button
        self.SaveColorButton = Button(text = 'Save')
        self.SaveColorButton.bind(on_release = self.SaveColor)

        self.RemoveColorButton = Button(text = 'Remove')
        self.RemoveColorButton.bind(on_release = self.RemoveColor)

        self.VisualizeColorButton = Button(text = 'Show')
        self.VisualizeColorButton.bind(on_release = self.VisualizeColor)

        #color labels
        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False,)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int')
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int')

        self.Placeholder = Label(text = '')

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)
 
        #adding to screen
        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)
        self.add_widget(self.SaveColorButton)
        self.add_widget(self.Placeholder)

    def VisualizeColor(self, instance):

        if int(self.ColorArray[1]) > int(self.ColorArray[2]):

            bigcircle.LeftAngle = int(self.ColorArray[1]) - 360
            bigcircle.RightAngle = int(self.ColorArray[2])

        else:

            bigcircle.LeftAngle = int(self.ColorArray[1])
            bigcircle.RightAngle = int(self.ColorArray[2])

        ColorDetectionInterface.switch_to(StartScreen())

    def RemoveColor(self, instance):

        color.AllColors.remove(self.ColorInstance)
        print(self.ColorArray, 'removed')

        self.SetTextInputToWrite()

        
        self.remove_widget(self.RemoveColorButton)
        self.remove_widget(self.VisualizeColorButton)

        self.add_widget(self.SaveColorButton)
        self.add_widget(self.Placeholder)

    def SaveColor(self, instance):

        self.ColorInstance = color(self.ColorArray[0], int(self.ColorArray[1]), int(self.ColorArray[2]))
        print(self.ColorArray, 'saved')

        self.SetTextInputToRead()

        self.remove_widget(self.SaveColorButton)
        self.remove_widget(self.Placeholder)
        
        self.add_widget(self.RemoveColorButton)
        self.add_widget(self.VisualizeColorButton)

    def SaveColorName(self, instance, value):

        ColorName = value
        self.ColorArray[0] = ColorName
        print(self.ColorArray)
        
    def SaveLeftAngle(self, instance, value):

        LeftAngle = value
        self.ColorArray[1] = LeftAngle
        print(self.ColorArray)

    def SaveRightAngle(self, instance, value):

        RightAngle = value
        self.ColorArray[2] = RightAngle 
        print(self.ColorArray)

    def SetTextInputToWrite(self):

        self.remove_widget(self.InputColorName)
        self.remove_widget(self.InputLeftColorValue)
        self.remove_widget(self.InputRightColorValue)

        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = False)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = False)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = False)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)

    def SetTextInputToRead(self):

        self.remove_widget(self.InputColorName)
        self.remove_widget(self.InputLeftColorValue)
        self.remove_widget(self.InputRightColorValue)

        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = True)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = True)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = True)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)

class PreSetColorWidget(BoxLayout):

    def __init__(self, CurrentColor, **kwargs):
        super(PreSetColorWidget, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.CurrentColor = CurrentColor
        self.ColorArray = [CurrentColor.name, CurrentColor.LeftAngle, CurrentColor.RightAngle]

        #button
        self.SaveColorButton = Button(text = 'Save')
        self.SaveColorButton.bind(on_release = self.SaveColor)

        self.RemovePreSetColorButton = Button(text = 'Remove')
        self.RemovePreSetColorButton.bind(on_press = self.RemovePreSetColor)

        self.RemoveColorButton = Button(text = 'Remove')
        self.RemoveColorButton.bind(on_release = self.RemoveColor)

        self.VisualizeColorButton = Button(text = 'Show')
        self.VisualizeColorButton.bind(on_release = self.VisualizeColor)

        #color labels
        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = True)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = True)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = True)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        #adding to screen
        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)
        self.add_widget(self.RemovePreSetColorButton)
        self.add_widget(self.VisualizeColorButton)

    def VisualizeColor(self, instance):

        if int(self.ColorArray[1]) > int(self.ColorArray[2]):

            bigcircle.LeftAngle = int(self.ColorArray[1]) - 360
            bigcircle.RightAngle = int(self.ColorArray[2])

        else:

            bigcircle.LeftAngle = int(self.ColorArray[1])
            bigcircle.RightAngle = int(self.ColorArray[2])

        ColorDetectionInterface.switch_to(StartScreen())

    def RemovePreSetColor(self, instance):

        color.AllColors.remove(self.CurrentColor)
        print(self.ColorArray, 'removed')

        self.remove_widget(self.VisualizeColorButton)
        self.SetTextInputToWrite()
        self.remove_widget(self.RemovePreSetColorButton)
        self.add_widget(self.SaveColorButton)
  
    def RemoveColor(self, instance):

        color.AllColors.remove(self.ColorInstance)
        print(self.ColorArray, 'removed')

        self.remove_widget(self.VisualizeColorButton)
        self.SetTextInputToWrite()
        self.remove_widget(self.RemoveColorButton)
        self.add_widget(self.SaveColorButton)

    def SaveColor(self, instance):

        self.ColorInstance = color(self.ColorArray[0], int(self.ColorArray[1]), int(self.ColorArray[2]))
        print(self.ColorArray, 'saved')

        self.remove_widget(self.SaveColorButton)
        self.SetTextInputToRead()
        self.add_widget(self.RemoveColorButton)
        self.add_widget(self.VisualizeColorButton)

    def SaveColorName(self, instance, value):

        ColorName = value
        self.ColorArray[0] = ColorName
        print(self.ColorArray)
        
    def SaveLeftAngle(self, instance, value):

        LeftAngle = value
        self.ColorArray[1] = LeftAngle
        print(self.ColorArray)

    def SaveRightAngle(self, instance, value):

        RightAngle = value
        self.ColorArray[2] = RightAngle 
        print(self.ColorArray)

    def SetTextInputToWrite(self):

        self.remove_widget(self.InputColorName)
        self.remove_widget(self.InputLeftColorValue)
        self.remove_widget(self.InputRightColorValue)

        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = False)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = False)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = False)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)


    def SetTextInputToRead(self):

        self.remove_widget(self.InputColorName)
        self.remove_widget(self.InputLeftColorValue)
        self.remove_widget(self.InputRightColorValue)

        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = True)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = True)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = True)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)

class ShowPercentages(BoxLayout):

    def __init__(self, **kwargs):
        super(ShowPercentages, self).__init__(**kwargs)
        
        self.orientation = 'vertical'

        self.LabelBlack = Label(text = '{}% is black'.format(detection.PercentageBlack))
        self.LabelGrey = Label(text = '{}% is grey'.format(detection.PercentageGrey))
        self.LabelWhite = Label(text = '{}% is white'.format(detection.PercentageWhite))

        self.add_widget(self.LabelBlack)
        self.add_widget(self.LabelGrey)
        self.add_widget(self.LabelWhite)

        for CurrentColor in color.AllColors:

            self.CurrentColorLabel = Label(text = '{}% is {}'.format(CurrentColor.Percentage, CurrentColor.name))
            self.add_widget(self.CurrentColorLabel)

class ColorCircle(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ColorCircle, self).__init__(*args, **kwargs)

        self.rows = 2
        self.cols = 1

        self.small = smallcircle()
        self.big = bigcircle()

        self.add_widget(self.big)
        self.add_widget(self.small)

#-----------------------------------Class Sub-Widgets----------------------------------- 

class smallcircle(GridLayout):

    def __init__(self, *args, **kwargs):
        super(smallcircle, self).__init__(*args, **kwargs)

        self.rows = 1
        self.cols = 1

class bigcircle(GridLayout):

    LeftAngle = 0
    RightAngle = 0

    def __init__(self, *args, **kwargs):
        super(bigcircle, self).__init__(*args, **kwargs)

        self.rows = 1
        self.cols = 1


#-----------------------------------Screenmanager-----------------------------------             
          
Builder.load_file('interface.kv')

ColorDetectionInterface = ScreenManager(transition = SwapTransition())

StartScreenInstance = StartScreen(name = 'Start')
SettingsScreenInstance = SettingsScreen(name = 'Configuration')
TakingPicturesScreenInstance = TakingPicturesScreen(name = 'TakingPicturesScreen')
ResultsScreenInstance = ResultScreen(name = 'Results')
CalculatingScreenInstance = CalculationScreen(name = 'Calculating')


ColorDetectionInterface.add_widget(StartScreenInstance)
ColorDetectionInterface.add_widget(SettingsScreenInstance)
ColorDetectionInterface.add_widget(TakingPicturesScreenInstance)
ColorDetectionInterface.add_widget(CalculatingScreenInstance)
ColorDetectionInterface.add_widget(ResultsScreenInstance)


class ColorDetectionApp(App):

    def build(self):
       
        return ColorDetectionInterface

ColorDetectionApp().run()

#----------------------------------------END PROGRAM----------------------------------------


