# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 3-1-2018

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import cv2
import time
import math
import numpy.ma as ma
from time import sleep

from functools import partial
import gc

#project .py files
from detection import detection
from color import color
from wait import wait

#----------------------------------------INTERFACE----------------------------------------

import kivy
import kivy.event

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
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SwapTransition
from kivy.properties import ObjectProperty
from kivy import clock
from kivy.clock import Clock
from kivy.uix.widget import Widget


#-----------------------------------Screen classes-----------------------------------

class StartScreen(Screen):

    with open('basecolors.txt', 'r') as txtfile:

        for line in txtfile:

            line = line.strip() 

            if line:

                Name, LeftAngle, RightAngle = line.split(" ")
                color(Name, int(LeftAngle), int(RightAngle))

    def __init__(self, *args, **kwargs):
        super(StartScreen, self).__init__(*args, **kwargs)

        StartScreenLayoutInstance = StartScreenLayout()
        self.add_widget(StartScreenLayoutInstance)

class ResultScreen(Screen):

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)

        self.ResultScreenLayoutInstance = ResultScreenLayout()
        self.add_widget(self.ResultScreenLayoutInstance)
        
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
       
        Layout = SettingsScreenLayout()
        self.add_widget(Layout)

class ColorScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(ColorScreen, self).__init__(*args, **kwargs)

        self.orientation = 'horizontal'

        self.ColorScreenLayoutInstance = ColorScreenLayout()
        self.add_widget(self.ColorScreenLayoutInstance)

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

    def StartTakingPictures(self):
        #called on enter via .kv
        Clock.schedule_interval(self.TakePicture, 1)
         
    def TakePicture(self, interval):

        image = cv2.imread('C:\\Users\\tom_l\\images\\test_image.png')
        print('picture taken')

    def GoToStartScreen(self, instance):

        try:
            Clock.unschedule(self.TakePicture)
            print('stopped taking pictures')

        except NameError:
            pass

        #remove all taken pictures

        ColorDetectionInterface.switch_to(StartScreen())

    def StartCalculation(self, interval):

        try:
            Clock.unschedule(self.TakePicture)
            print('stopped taking pictures')

        except NameError:
            pass

        ColorDetectionInterface.switch_to(CalculationScreen())

class StartScreenLayout(GridLayout):

    def __init__(self, **kwargs):
        super(StartScreenLayout, self).__init__(**kwargs)

        self.rows = 1
        self.cols = 3

        self.StartColorDetectionButton = Button(text = 'Start taking picture')
        self.StartColorDetectionButton.bind(on_press = self.GoToTakingPicuresScreen)

        self.OptionButtonsStartScreen = OptionButtonsStartScreen()
        self.AllCurrentColors = ShowAllSetColors()

        self.add_widget(self.OptionButtonsStartScreen)
        self.add_widget(self.AllCurrentColors)
        self.add_widget(self.StartColorDetectionButton)

    def GoToTakingPicuresScreen(self, instance):
        ColorDetectionInterface.switch_to(TakingPicturesScreen())

class SettingsScreenLayout(GridLayout):

    def __init__(self, *args, **kwargs):
        super(SettingsScreenLayout, self).__init__(*args, **kwargs)

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
        self.InputNumberOfDecimalLabel = Label(text = 'Set the number of decimals for the calculation: ')
        self.InputNumberOfDecimals = TextInput(text = '2', multiline = False, input_filter = 'int')
        self.InputNumberOfDecimals.bind(text = self.SetNumberOfDecimals)

        self.InputBeltValueLabel = Label(text = 'Set the value of the belt in "value" from HSV: ')
        self.InputBeltValue = TextInput(text = '40', multiline = False, input_filter = 'int')
        self.InputBeltValue.bind(text = self.SetBeltValue)

        self.InputBlackValueLabel = Label(text = 'Set the value of the color black in "value" from HSV: ')
        self.InputBlackValue = TextInput(text = '20', multiline = False, input_filter = 'int')
        self.InputBlackValue.bind(text = self.SetBlackValue)

        self.InputWhiteValueLabel = Label(text = 'Set the value of the color white in "value" from HSV: ')
        self.InputWhiteValue = TextInput(text = '75', multiline = False, input_filter = 'int')
        self.InputWhiteValue.bind(text = self.SetWhiteValue)
        
        self.InputMaxSaturationValueLabel = Label(text = 'The maximal saturation of "S" in HSV for a color the to be \ndefined as white/grey/black: ')
        self.InputMaxSaturationValue = TextInput(text = '25', multiline = False, input_filter = 'int')
        self.InputMaxSaturationValue.bind(text = self.SetMaxSaturation)

        self.InputBeltSpeedSettingLabel = Label(text = 'Input the speed setting of the belt')
        self.InputBeltSpeedSetting = TextInput(text = '0', multiline = False, input_filter = 'int')
        self.InputBeltSpeedSetting.bind(text = self.SetBeltSpeedSetting)

        self.InputPictureWidthLabel = Label(text = 'Input the width of the pictures in meters')
        self.InputPictureWidth = TextInput(text = '0.165', multiline = False, input_filter = 'int')
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

        self.add_widget(self.InputNumberOfDecimalLabel)
        self.add_widget(self.InputNumberOfDecimals)

        self.add_widget(self.InputBeltValueLabel)
        self.add_widget(self.InputBeltValue)

        self.add_widget(self.InputBlackValueLabel)
        self.add_widget(self.InputBlackValue)

        self.add_widget(self.InputWhiteValueLabel)
        self.add_widget(self.InputWhiteValue)

        self.add_widget(self.InputMaxSaturationValueLabel)
        self.add_widget(self.InputMaxSaturationValue)

        self.add_widget(self.InputBeltSpeedSettingLabel)
        self.add_widget(self.InputBeltSpeedSetting)

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

        wait.PictureWidth = value
        wait.CalculateWaitingTime()

    def SetBeltSpeedSetting(self, instance, value):

        wait.BeltSpeed = value
        wait.CalculateWaitingTime()

    def SetMaxSaturation(self, instance, value):
        value = int(value)
        detection.SetMaxSaturation = value
       
    def SetWhiteValue(self, instnace, value):
        value = int(value)
        detection.SetWhiteValue(value)
        
    def SetBlackValue(self, instance, value):
        value = int(value)
        detection.SetBlackValue(value)
        
    def SetBeltValue(self, instance, value):
        value = int(value)
        detection.SetBeltValue(value)

    def SetNumberOfDecimals(self, instance, value):
        
        detection.NumberOfDecimals = value
        
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

class ResultScreenLayout(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ResultScreenLayout, self).__init__(*args, **kwargs)

        self.orientation = 'vertical'

        self.ShowPercentgesInstance = ShowPercentages()

        self.ToStartScreenButton = Button(text = 'To Startscreen', size_hint=(1, 0.1))
        self.ToStartScreenButton.bind(on_press = self.ToStartScreen)

        self.add_widget(self.ShowPercentgesInstance)
        self.add_widget(self.ToStartScreenButton)

    def ToStartScreen(self, instance):

        ColorDetectionInterface.switch_to(StartScreen())

class ColorScreenLayout(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ColorScreenLayout, self).__init__(*args, **kwargs)

        self.orientation = 'vertical'

        self.SettingsColorScreenInstance = SettingsColorScreen()
        self.add_widget(self.SettingsColorScreenInstance)

        for CurrentColor in color.AllColors:

            self.PreSetColorWidgetInstance = PreSetColorWidget(CurrentColor)
            self.add_widget(self.PreSetColorWidgetInstance)

        RemainingSlots =  20 - len(color.AllColors)

        for x in range(0, RemainingSlots):

            self.ColorWidgetInstance = ColorWidget()
            self.add_widget(self.ColorWidgetInstance)

#-----------------------------------Custom Widgets----------------------------------- 

class OptionButtonsStartScreen(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(OptionButtonsStartScreen, self).__init__(*args, **kwargs) 
        
        self.orientation = 'vertical' 

        self.GoToColorScreenButton = Button(text = 'To color definitions')
        self.GoToColorScreenButton.bind(on_press = self.GoToColorScreen)

        self.OptionButtonsStartScreen = Button(text = 'To settings')
        self.OptionButtonsStartScreen.bind(on_press = self.GoToSettingsScreen)

        self.add_widget(self.OptionButtonsStartScreen)
        self.add_widget(self.GoToColorScreenButton)

    def GoToColorScreen(self, instance):

        ColorDetectionInterface.switch_to(ColorScreen())

    def GoToSettingsScreen(self, instance):

        ColorDetectionInterface.switch_to(SettingsScreen())

class ShowAllSetColors(GridLayout):

    def __init__(self, *args, **kwargs):
        super(ShowAllSetColors, self).__init__(*args, **kwargs)  

        self.cols = 1
        self.rows = 1

        if not color.AllColors:
            self.add_widget(Label(text = 'no colors set'))

        else:
             for CurrentColor in color.AllColors:

                self.CurrentLabel = Label(text = '{} {} {}'.format(CurrentColor.name, CurrentColor.LeftAngle, CurrentColor.RightAngle))
                self.rows += 1
                self.add_widget(self.CurrentLabel)

class SettingsColorScreen(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(SettingsColorScreen, self).__init__(*args, **kwargs)  
        
        self.CorrectIndicator = True 

        self.orientation = 'horizontal' 

        #labels
        self.LeftAngleLabel = Label(text = 'Insert left angle below')
        self.RightAngleLabel = Label(text = 'Insert right angle below')

        #buttons
        self.ReturnToConfigScreenButton = Button(text = 'To StartScreen')
        self.ReturnToConfigScreenButton.bind(on_press = self.GoToConfigScreen)

        self.NameLabel = Label(text = 'Insert color name below')
     
        #adding to widget
        self.add_widget(self.NameLabel)
        self.add_widget(self.LeftAngleLabel)
        self.add_widget(self.RightAngleLabel)
        self.add_widget(self.ReturnToConfigScreenButton)
        
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
        
        OverlapPopup = Popup(title='Overlap!', content=Label(text='There is overlap on {}'.format(OverlapArray)), size_hint=(None, None), size=(400, 400))
        OverlapPopup.open()
        
    def RaiseMissingPopup(self, MissingArray):

        MissingPopup = Popup(title='Missing values!', content=Label(text='Value(s) {} are missing'.format(MissingArray)), size_hint=(None, None), size=(400, 400))
        MissingPopup.open()   

    def RaiseIndexErrorPopup(self):

        print('indexerror popup called')  
        
        IndexErrorPopup = Popup(title='IndexError!', content=Label(text='values must be in range 0-359'), size_hint=(None, None), size=(400, 400))
        IndexErrorPopup.open()  

class ColorWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ColorWidget, self).__init__(*args, **kwargs)

        self.orientation = 'horizontal'
        self.ColorArray = ['enter name' ,0 ,0 ]

        #button
        self.SaveColorButton = Button(text = 'Save color')
        self.SaveColorButton.bind(on_release = self.SaveColor)

        self.RemoveColorButton = Button(text = 'Remove color')
        self.RemoveColorButton.bind(on_release = self.RemoveColor)

        #color labels
        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False,)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int')
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int')

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        #adding to screen
        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)
        self.add_widget(self.SaveColorButton)
 
    def RemoveColor(self, instance):

        color.AllColors.remove(self.ColorInstance)
        print(self.ColorArray, 'removed')

        self.remove_widget(self.RemoveColorButton)
        self.add_widget(self.SaveColorButton)

    def SaveColor(self, instance):

        self.ColorInstance = color(self.ColorArray[0], int(self.ColorArray[1]), int(self.ColorArray[2]))
        print(self.ColorArray, 'saved')

        self.remove_widget(self.SaveColorButton)
        self.add_widget(self.RemoveColorButton)
        self.SetInputToReadOnly()

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

    def SetInputToReadOnly(self):

        self.InputColorName = TextInput(readonly = True)
        self.InputLeftColorValue = TextInput(readonly = True)
        self.InputRightColorValue = TextInput(readonly = True)

class PreSetColorWidget(BoxLayout):

    def __init__(self, CurrentColor, **kwargs):
        super(PreSetColorWidget, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.CurrentColor = CurrentColor
        self.ColorArray = [CurrentColor.name, CurrentColor.LeftAngle, CurrentColor.RightAngle]

        #button
        self.SaveColorButton = Button(text = 'Save color')
        self.SaveColorButton.bind(on_release = self.SaveColor)

        self.RemovePreSetColorButton = Button(text = 'Remove color')
        self.RemovePreSetColorButton.bind(on_press = self.RemovePreSetColor)

        self.RemoveColorButton = Button(text = 'Remove color')
        self.RemoveColorButton.bind(on_release = self.RemoveColor)

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

    def RemovePreSetColor(self, instance):

        color.AllColors.remove(self.CurrentColor)
        print(self.ColorArray, 'removed')

        self.remove_widget(self.RemovePreSetColorButton)
        self.add_widget(self.SaveColorButton)
        self.SetTextInputToWrite()

    def RemoveColor(self, instance):

        color.AllColors.remove(self.ColorInstance)
        print(self.ColorArray, 'removed')

        self.remove_widget(self.RemoveColorButton)
        self.add_widget(self.SaveColorButton)
        self.SetTextInputToWrite()
    
    def SaveColor(self, instance):

        self.ColorInstance = color(self.ColorArray[0], int(self.ColorArray[1]), int(self.ColorArray[2]))
        print(self.ColorArray, 'saved')

        self.SetTextInputToRead()

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

        self.clear_widgets()

        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = False)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = False)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = False)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)
        self.add_widget(self.SaveColorButton)

    def SetTextInputToRead(self):

        self.clear_widgets()

        self.InputColorName = TextInput(text = '{}'.format(self.ColorArray[0]), multiline = False, readonly = True)
        self.InputLeftColorValue = TextInput(text = '{}'.format(self.ColorArray[1]), multiline = False, input_filter = 'int', readonly = True)
        self.InputRightColorValue = TextInput(text = '{}'.format(self.ColorArray[2]), multiline = False, input_filter = 'int', readonly = True)

        self.InputColorName.bind(text = self.SaveColorName)
        self.InputLeftColorValue.bind(text = self.SaveLeftAngle)
        self.InputRightColorValue.bind(text = self.SaveRightAngle)

        self.add_widget(self.InputColorName)
        self.add_widget(self.InputLeftColorValue)
        self.add_widget(self.InputRightColorValue)
        self.add_widget(self.RemoveColorButton)

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
            self.CurrentLabel = Label(text = '{}% is {}'.format(CurrentColor.Percentage, CurrentColor.name))
            self.add_widget(self.CurrentLabel)
   

#-----------------------------------Screenmanager-----------------------------------             
          
Builder.load_file('interface.kv')

ColorDetectionInterface = ScreenManager(transition = SwapTransition())

Start = StartScreen(name = 'Start')
Configuration = SettingsScreen(name = 'Configuration')
TakingPictures = TakingPicturesScreen(name = 'TakingPicturesScreen')
Results = ResultScreen(name = 'Results')
Calculating = CalculationScreen(name = 'Calculating')
Color = ColorScreen(name = 'Color')

ColorDetectionInterface.add_widget(Start)
ColorDetectionInterface.add_widget(Configuration)
ColorDetectionInterface.add_widget(TakingPictures)
ColorDetectionInterface.add_widget(Calculating)
ColorDetectionInterface.add_widget(Results)
ColorDetectionInterface.add_widget(Color)

class ColorApp(App):

    def build(self):
       
        return ColorDetectionInterface

ColorApp().run()

#----------------------------------------END PROGRAM----------------------------------------

























    





                
               


