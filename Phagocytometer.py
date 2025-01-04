import os
from os import listdir, mkdir, rmdir
import tkinter as tk
from tkinter import messagebox
import customtkinter
from customtkinter import *
from CTkColorPicker import *
import time
import cv2


from src.ImgToBinary import getPath
from src.CountNeutrophils import countNeus
from src.ChannelsToPhagocytosis import splitAndCountPhago
from src.ChannelsToTouching import splitAndCountInt
from src.BatchOpen import batchOpen 
from src.stats import makeStats
from src.phagoColorFunc import colorTif
from src.processnd2 import nd2ToArray, arrayToImg
from src.ImgToBinary import fileToBinary
from src.SplitTiffs import tifChannelNames, tifToArrays
from src.Constants import bgr_default, hex_default

class TopLevelColors(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
                """Centers the window to the main display/monitor"""
                screen_width = Screen.winfo_screenwidth()
                screen_height = Screen.winfo_screenheight()
                x = int(((screen_width/2) - (width/2)) * scale_factor)
                y = int(((screen_height/2) - (height/1.5)) * scale_factor)
                return f"{width}x{height}+{x}+{y}"
        
        self.title("Customize Colors")

        self.geometry(CenterWindowToDisplay(self, 350, 250, self._get_window_scaling())) 

        global hex_array
        hex_array = hex_default
        bgHex = hex_array[0]
        neuHex = hex_array[1]
        yeastHex = hex_array[2]
        phagoHex = hex_array[3]

        self.bgColorText = customtkinter.CTkLabel(self,text="Background Color: ")
        self.bgColorText.grid(row=1,column=1,padx=10,pady=10)

        self.bgColor = customtkinter.CTkButton(self,text="",command=self.askBgColor)
        self.bgColor.grid(row=1,column=2,padx=10,pady=10)
        self.bgColor.configure(fg_color=bgHex)

        self.neuColorText = customtkinter.CTkLabel(self,text="Neutrophil Color: ")
        self.neuColorText.grid(row=2,column=1,padx=10,pady=10)

        self.neuColor = customtkinter.CTkButton(self,text="",command=self.askNeuColor)
        self.neuColor.grid(row=2,column=2,padx=10,pady=10)
        self.neuColor.configure(fg_color=neuHex)

        self.yeastColorText = customtkinter.CTkLabel(self,text="Yeast Color: ")
        self.yeastColorText.grid(row=3,column=1,padx=10,pady=10)

        self.yeastColor = customtkinter.CTkButton(self,text="",command=self.askYeastColor)
        self.yeastColor.grid(row=3,column=2,padx=10,pady=10)
        self.yeastColor.configure(fg_color=yeastHex)

        self.phagoColorText = customtkinter.CTkLabel(self,text="Interaction Color: ")
        self.phagoColorText.grid(row=4,column=1,padx=10,pady=10)

        self.phagoColor = customtkinter.CTkButton(self,text="",command=self.askPhagoColor)
        self.phagoColor.grid(row=4,column=2,padx=10,pady=10)
        self.phagoColor.configure(fg_color=phagoHex)

        self.closeButton = customtkinter.CTkButton(self,text="Close",command=lambda: TopLevelColors.withdraw(self))
        self.closeButton.grid(row=5,column=1,padx=10,pady=10)

    def askBgColor(self):
        pickBgColor = AskColor() # open the color picker
        color = pickBgColor.get() # get the color string
        self.bgColor.configure(fg_color=color)
        hex_array[0] = color
        TopLevelColors().focus
    def askNeuColor(self):
        pickNeuColor = AskColor() # open the color picker
        color = pickNeuColor.get() # get the color string
        self.neuColor.configure(fg_color=color)
        hex_array[1] = color
        TopLevelColors().focus
    def askYeastColor(self):
        pickYeastColor = AskColor() # open the color picker
        color = pickYeastColor.get() # get the color string
        self.yeastColor.configure(fg_color=color)
        hex_array[2] = color
        TopLevelColors().focus
    def askPhagoColor(self):
        pickPhagoColor = AskColor() # open the color picker
        color = pickPhagoColor.get() # get the color string
        self.phagoColor.configure(fg_color=color)
        hex_array[3] = color
        TopLevelColors().focus
    
class TopLevelChannels(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
                """Centers the window to the main display/monitor"""
                screen_width = Screen.winfo_screenwidth()
                screen_height = Screen.winfo_screenheight()
                x = int(((screen_width/2) - (width/2)) * scale_factor)
                y = int(((screen_height/2) - (height/1.5)) * scale_factor)
                return f"{width}x{height}+{x}+{y}"
        
        self.title("Select Channels")

        self.geometry(CenterWindowToDisplay(self, 400, 300, self._get_window_scaling())) 

        global channelnames
        channelnames = channelNames

        self.text = customtkinter.CTkTextbox(self,fg_color='transparent',wrap='word',width=250,height=75)
        self.text.grid(row=1,column=1,columnspan=3,sticky='ew')
        self.text.insert("0.0", "Please select the channels that correspond to the yeast and the phagocytes")
        self.text.configure(state='disabled')

        self.channel1text = customtkinter.CTkLabel(self,text='Yeast Channel:')
        self.channel1text.grid(row=2,column=1,padx=10,pady=10)

        self.channel1option = customtkinter.CTkOptionMenu(self,values=channelnames)
        self.channel1option.grid(row=2,column=2,padx=10,pady=10,sticky='n')

        self.channel2text = customtkinter.CTkLabel(self,text='Phagocyte Channel:')
        self.channel2text.grid(row=3,column=1,padx=10,pady=10)

        self.channel2option = customtkinter.CTkOptionMenu(self,values=channelnames)
        self.channel2option.grid(row=3,column=2,padx=10,pady=10,sticky='n')


        global waitVar
        waitVar = customtkinter.IntVar()
        self.channelGo = customtkinter.CTkButton(self,text='Continue',command=lambda: self.continueProcess(),width=100)
        self.channelGo.grid(row=4,column=2,padx=10,pady=10)
        self.channelGo.wait_variable(waitVar)
        

    def continueProcess(self):
        global yeastChannel
        global NeuChannel

        yeastChannel = self.channel1option.get()
        NeuChannel = self.channel2option.get()


        self.after(2000,waitVar.set,1)
        
        try:
            TopLevelChannels.quit(self)
            TopLevelChannels.withdraw(self)
        except Exception as e:
            print(str(e))
            
class TabView(customtkinter.CTkTabview):
    def __init__(self,master):
        super().__init__(master)

        
        # create tabs
        mainTab = self.add('Process Single TIFF')
        batchTab = self.add('Batch Process')
        nd2Tab = self.add('Process .nd2 File')
        colorTab = self.add('Auto-Color File')

        # declare channel window
        
        self.toplevel_channels = None
        self.toplevel_colors = None

        """         MAIN TAB CODE          """
         # buffer frames
        self.emptyTop = customtkinter.CTkFrame(mainTab,fg_color="transparent", height=10)
        self.emptyTop.grid(row=0, column=3)

        self.empty00 = customtkinter.CTkFrame(mainTab, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=1,column=0,padx=5,pady=5)

        # select file label
        self.openLabel = customtkinter.CTkLabel(mainTab,height=5,text="Select a TIF file to count:", anchor="e")
        self.openLabel.grid(row=1,column=1,padx=5,pady=5, sticky="ew")

        # select file box
        self.openText = customtkinter.CTkTextbox(mainTab, height=5, width=100, text_color="#6B6B6B")
        self.openText.insert("0.0","Filename will appear here")
        self.openText.grid(row=1,column=2, padx=5,pady=5,sticky='ew')
        self.openText.configure(state="disabled")
        

        # select file button
        self.openButton = customtkinter.CTkButton(mainTab, command=self.getOpenPath, text="Select File",text_color='white')
        self.openButton.grid(row=1,column=3, padx=5, pady=5,sticky='ew')

        # buffer frame
        self.empty01 = customtkinter.CTkFrame(mainTab, fg_color="transparent", height=5, width=15)
        self.empty01.grid(row=1,column=4,padx=5,pady=5)

        

        # buffer frame
        self.empty10 = customtkinter.CTkFrame(mainTab, fg_color="transparent", height=5, width=15)
        self.empty10.grid(row=2,column=0,padx=5,pady=5)

        # name output file label
        self.outputLabel = customtkinter.CTkLabel(mainTab,height=5,text="Set filename for the output CSV (Optional):", wraplength=150,justify="left", anchor="e")
        self.outputLabel.grid(row=2,column=1,padx=5,pady=5, sticky="ew")

        # output file text box
        self.outputText = customtkinter.CTkTextbox(mainTab, height=5, width=100, text_color="#BABABA")
        self.outputText.insert("0.0","example.csv")
        self.outputText.grid(row=2,column=2,columnspan=1, padx=5,pady=5,sticky='ew')

        # buffer frames
        spacerWidth = self.openButton.cget("width")
        self.empty11 = customtkinter.CTkFrame(mainTab, fg_color="transparent", height=5, width=spacerWidth)
        self.empty11.grid(row=2,column=3,padx=5,pady=5, sticky='ew')

        self.empty12 = customtkinter.CTkFrame(mainTab, fg_color="transparent", height=5, width=15)
        self.empty12.grid(row=2,column=4,padx=5,pady=5)
        
        
        # SENSITIVITY SLIDER, MAYBE TAKE OUT
        """
        self.sensFrame = customtkinter.CTkFrame(mainTab, fg_color="transparent")
        self.sensFrame.grid(row=3, column=2, sticky='ew')

        self.sensSlider = customtkinter.CTkSlider(self.sensFrame, from_=-10, to=10, number_of_steps=20, command=self.sliderUpdate)
        self.sensSlider.grid(row=0, column=0, in_=self.sensFrame)

        self.sensVal = customtkinter.CTkLabel(self.sensFrame, text="0")
        self.sensVal.grid(row=0,column=2, in_=self.sensFrame)
        

        self.sensText = customtkinter.CTkLabel(self.sensFrame, text="Sensitivity")
        self.sensText.grid(row=0,column=3, in_=self.sensFrame)
        """

        # experimentally decided scale value, subject to change
        self.useZ = IntVar(value=1)
        self.zCheck = customtkinter.CTkCheckBox(mainTab,text="Use Z-adjustment? (recommended)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1,variable=self.useZ)
        self.zCheck.grid(row=4,column=2,sticky="w")
        
        # gaussian blur option
        self.blurCheck = customtkinter.CTkCheckBox(mainTab,text="Use Gaussian blur for thresholding? (Helpful for noisy images)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.blurCheck.grid(row=5,column=2, sticky="w")

        # option to save binary images
        self.saveCheck = customtkinter.CTkCheckBox(mainTab,text="Save binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.saveCheck.grid(row=6,column=2, sticky="w")
        
        # button to count the file
        self.countButton = customtkinter.CTkButton(mainTab,command=self.runCount,text="Count File",text_color='white')
        self.countButton.grid(row=7,column=3, sticky='ew')



        """         BATCH TAB CODE           """

        # spacer frame
        self.emptyTop = customtkinter.CTkFrame(batchTab,fg_color="transparent", height=10)
        self.emptyTop.grid(row=0, column=3)

        # spacer frame
        self.empty00 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=1,column=0,padx=5,pady=5)

        # select file label
        self.openLabel = customtkinter.CTkLabel(batchTab,height=5,text="Select multiple TIF files to count:", anchor="e")
        self.openLabel.grid(row=1,column=1,padx=5,pady=5, sticky="ew")

        # # select file box
        # self.openText = customtkinter.CTkTextbox(batchTab, height=5, width=100, text_color="#BABABA")
        # self.openText.insert("0.0","Choose a file path")
        # self.openText.grid(row=1,column=2, padx=5,pady=5,sticky='ew')
        # self.openText.configure(state="disabled")

        # select file button
        self.openButton = customtkinter.CTkButton(batchTab, command=self.getBatchOpen, text="Select Files",text_color='white')
        self.openButton.grid(row=1,column=2, padx=5, pady=5,sticky='ew')

        # buffer frame
        self.empty01 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty01.grid(row=1,column=3,padx=5,pady=5)

        

        # buffer frame
        self.empty10 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty10.grid(row=2,column=0,padx=5,pady=5)


        # buffer frames
        spacerWidth = self.openButton.cget("width")
        self.empty11 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=spacerWidth)
        self.empty11.grid(row=2,column=3,padx=5,pady=5, sticky='ew')

        # spacer frame
        self.empty12 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty12.grid(row=2,column=4,padx=5,pady=5)

        # spacer frame
        self.empty01 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=15, width=5)
        self.empty01.grid(row=3,column=1,padx=5,pady=5, sticky='e')

        # 'n' files selected textbox
        self.selectedtext = customtkinter.CTkTextbox(batchTab, bg_color="transparent", fg_color="transparent",state='disabled', height=15)
        self.selectedtext.grid(row=3, column=2, padx=5,pady=5, sticky='')
        
        # spacer frame
        self.empty01 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty01.grid(row=4,column=2,padx=5,pady=5, sticky='w')

        # experimentally decided scale value, subject to change
        # to change this value, see 'declarations.py'
        self.useZ = IntVar(value=1)
        self.zBatchCheck = customtkinter.CTkCheckBox(batchTab,text="Use Z-adjustment? (recommended)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1,variable=self.useZ)
        self.zBatchCheck.grid(row=5,column=2,sticky="w")
        
        # gaussian blur option
        self.blurBatchCheck = customtkinter.CTkCheckBox(batchTab,text="Use Gaussian blur for thresholding? (Helpful for noisy images)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.blurBatchCheck.grid(row=6,column=2, sticky="w")

        # option to save binary images
        self.saveBatchCheck = customtkinter.CTkCheckBox(batchTab,text="Save binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.saveBatchCheck.grid(row=7,column=2, sticky="w")
        
        # button to count the file
        self.countButton = customtkinter.CTkButton(batchTab,command=self.tryProcess,text="Count Files",text_color='white')
        self.countButton.grid(row=8,column=3)

        
        """         COLOR TAB CODE          """

        # spacer frame
        self.empty00 = customtkinter.CTkFrame(colorTab, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=1,column=0,padx=5,pady=5)

        
        self.label = customtkinter.CTkLabel(colorTab,text='Select a TIFF file to color:', wraplength=350)
        self.label.grid(row=1, column=1, sticky='w')

        # select file box
        self.openColorText = customtkinter.CTkTextbox(colorTab, height=5, width=100, text_color="#6B6B6B")
        self.openColorText.insert("0.0","Filename will appear here")
        self.openColorText.grid(row=1,column=2, padx=5,pady=5,sticky='ew')
        self.openColorText.configure(state="disabled")


        self.colorButton = customtkinter.CTkButton(colorTab, text="Select File",command=self.getColorOpen)
        self.colorButton.grid(row=1, column=3, sticky='ew')

        
        self.blurColorCheck = customtkinter.CTkCheckBox(colorTab,text="Use Gaussian blur for thresholding? (Helpful for noisy images)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.blurColorCheck.grid(row=2, column=2, sticky='ew')

        self.saveColorCheck = customtkinter.CTkCheckBox(colorTab,text="Save binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.saveColorCheck.grid(row=3, column=2, sticky='ew')


        self.label = customtkinter.CTkLabel(colorTab,text='File format:', wraplength=350)
        self.label.grid(row=4, column=1, sticky='w')

        # file format for output selector
        self.formatVal = customtkinter.StringVar(value="JPG Sequence")
        self.exportFormat = customtkinter.CTkOptionMenu(colorTab,values=['JPG Sequence','MP4'], variable=self.formatVal, fg_color='white',text_color='black')
        self.exportFormat.grid(row=4, column=2, sticky='ew')

        self.customizeColor = customtkinter.CTkButton(colorTab, text="Customize Colors", command=self.openColorWindow)
        self.customizeColor.grid(row=5,column=1,padx=5,pady=5)

        self.runColor = customtkinter.CTkButton(colorTab, text="Process File", command=self.tryColor)
        self.runColor.grid(row=5, column=3, sticky='ew',padx=5,pady=5)
        
        self.empty00 = customtkinter.CTkFrame(colorTab, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=5,column=4,padx=5,pady=5)

        """         ND2 CODE            """

        self.emptyTop = customtkinter.CTkFrame(nd2Tab,fg_color="transparent", height=10)
        self.emptyTop.grid(row=0, column=3)

        self.empty00 = customtkinter.CTkFrame(nd2Tab, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=1,column=0,padx=5,pady=5)

        # select file label
        self.opennd2Label = customtkinter.CTkLabel(nd2Tab,height=5,text="Select an ND2 file to count:", anchor="e")
        self.opennd2Label.grid(row=1,column=1,padx=5,pady=5, sticky="ew")

        # select file box
        self.opennd2Text = customtkinter.CTkTextbox(nd2Tab, height=5, width=100, text_color="#6B6B6B")
        self.opennd2Text.insert("0.0","Filename will appear here")
        self.opennd2Text.grid(row=1,column=2, padx=5,pady=5,sticky='ew')
        self.opennd2Text.configure(state="disabled")
        

        # select file button
        self.opennd2Button = customtkinter.CTkButton(nd2Tab, command=self.getOpenPath, text="Select File",text_color='white')
        self.opennd2Button.grid(row=1,column=3, padx=5, pady=5,sticky='ew')

        # buffer frame
        self.empty01 = customtkinter.CTkFrame(nd2Tab, fg_color="transparent", height=5, width=15)
        self.empty01.grid(row=1,column=4,padx=5,pady=5)

        

        # buffer frame
        self.empty10 = customtkinter.CTkFrame(nd2Tab, fg_color="transparent", height=5, width=15)
        self.empty10.grid(row=2,column=0,padx=5,pady=5)

        # name output file label
        self.outputnd2Label = customtkinter.CTkLabel(nd2Tab,height=5,text="Set filename for the output CSV (Optional):", wraplength=150,justify="left", anchor="e")
        self.outputnd2Label.grid(row=2,column=1,padx=5,pady=5, sticky="ew")

        # output file text box
        self.outputnd2Text = customtkinter.CTkTextbox(nd2Tab, height=5, width=100, text_color="#BABABA")
        self.outputnd2Text.insert("0.0","example.csv")
        self.outputnd2Text.grid(row=2,column=2,columnspan=1, padx=5,pady=5,sticky='ew')

        # buffer frames
        spacerWidth = self.opennd2Button.cget("width")
        self.empty11 = customtkinter.CTkFrame(nd2Tab, fg_color="transparent", height=5, width=spacerWidth)
        self.empty11.grid(row=2,column=3,padx=5,pady=5, sticky='ew')

        self.empty12 = customtkinter.CTkFrame(nd2Tab, fg_color="transparent", height=5, width=15)
        self.empty12.grid(row=2,column=4,padx=5,pady=5)
        

        # experimentally decided scale value, subject to change
        self.useND2Z = IntVar(value=1)
        self.zND2Check = customtkinter.CTkCheckBox(nd2Tab,text="Use Z-adjustment? (recommended)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1,variable=self.useND2Z)
        self.zND2Check.grid(row=4,column=2,sticky="w")
        
        # gaussian blur option
        self.blurND2Check = customtkinter.CTkCheckBox(nd2Tab,text="Use Gaussian blur for thresholding? (Helpful for noisy images)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.blurND2Check.grid(row=5,column=2, sticky="w")

        # option to save binary images
        self.saveND2Check = customtkinter.CTkCheckBox(nd2Tab,text="Save binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.saveND2Check.grid(row=6,column=2, sticky="w")
        
        # button to count the file
        self.countND2Button = customtkinter.CTkButton(nd2Tab,command=self.processND2,text="Count File",text_color='white')
        self.countND2Button.grid(row=7,column=3, sticky='ew')


    def openColorWindow(self):
        if self.toplevel_colors is None or not self.toplevel_colors.winfo_exists():
            self.toplevel_colors = TopLevelColors()  # create window if its None or destroyed
            self.toplevel_colors.focus()
        else:
            self.toplevel_colors.focus()  # if window exists focus it



    def processND2(self):
        global goCheck
        
        masterList, channelNames = nd2ToArray(file_path)
        global channelnames
        channelnames = channelNames
        self.getChannelIdentity()

        arrayToImg(masterList, yeastChannel, NeuChannel)

    def destroyChannelWindow(self):
        self.toplevel_channels.quit()
        
    def getChannelIdentity(self):

        if self.toplevel_channels is None or not self.toplevel_channels.winfo_exists():
            self.toplevel_channels = TopLevelChannels()  # create window if its None or destroyed
            self.toplevel_channels.focus()
        else:
            self.toplevel_channels.focus()  # if window exists focus it


    def fullCount(self, tifPath, CSVname, runType, useBlur=False, useZ=True):

        # function to run all processing/counting functions in sequence
        desktop = os.path.expanduser("~/Desktop")
        outputFolder = os.path.join(desktop,'Phagocytometer Files')
        if not os.path.exists(outputFolder):
            print('creating output folder...')
            os.mkdir(outputFolder)
        global csvpath

        # for sensitivity slider, maybe coming back later. 
        # sensActive = False
        
        # if sensActive:
        #     sens = self.sensSlider.get()
        # else:
        #     sens = 0

  
        # split tiff into separate images
        global channelNames
        print('getting channel information...')
        channelNames = tifChannelNames(tifPath)

        
        self.getChannelIdentity()
       
        print('converting to images...')
        yeastImgs, neuImgs = tifToArrays(tifPath, yeastChannel, NeuChannel, channelNames)
        print('thresholding...')
        yeastBins, neuBins = fileToBinary(yeastImgs, neuImgs)
        print("counting...")
        # count the neutrophil folder
        csvpath = countNeus(neuBins, outputFolder, CSVname)
        
        """ # soon will be able to differentiate between phagocytosis and all interactions (hopefully!)
        if self.countPhagoCheck.get():
            splitAndCountPhago(greenBin1, blueBin1, dir2, csvpath, useZ)
        if self.countInteractCheck.get():
            splitAndCountInt(greenBin1, blueBin1, dir2, csvpath, useZ)
        
            for now, use interaction algo:
        """
        print("count yeast-neutrophil interactions...")
        multBins = splitAndCountInt(yeastBins, neuBins, csvpath, True, outputFolder)

        # basic percentage average calculations to add to CSV
        print("calculating statistics...")
        makeStats(csvpath)

        # delete temporary images, if computer perms allow
        if runType == 'Single':
            isSave = self.saveCheck.get()       
            if isSave:
                try:
                    print("saving images...")
                    self.saveToImg(yeastBins,neuBins,multBins,outputFolder)
                except PermissionError:
                    self.permissionError()
            isBatchSave = self.saveBatchCheck.get()
        elif runType == 'Batch':
            isBatchSave = self.saveBatchCheck.get()
            if isBatchSave:
                try:
                    print("saving images...")
                    currFolder = os.path.join(outputFolder,currTiff)
                    os.mkdir(currFolder)
                    self.saveToImg(yeastBins,neuBins,multBins,currFolder)
                except PermissionError:
                    self.permissionError()
    def permissionError(self): 
        messagebox.showerror(message="Permission to delete files was denied. To manually delete, navigate to the Phagocytometer Files folder and delete 'Images' folder.", type='ok', icon='warning')

    def saveToImg(self, yeastArray, neuArray, multArray, dir):

        imgFolder = os.path.join(dir,'Images')
        if not os.path.exists(imgFolder):
            os.mkdir(imgFolder)
        yeastFolder = os.path.join(imgFolder,'Yeast')
        if not os.path.exists(yeastFolder):
            os.mkdir(yeastFolder)
        neuFolder = os.path.join(imgFolder,'Neutrophils')
        if not os.path.exists(neuFolder):
            os.mkdir(neuFolder)
        multFolder = os.path.join(imgFolder,'Interactions')
        if not os.path.exists(multFolder):
            os.mkdir(multFolder)



        for i in range(len(yeastFolder)):

            filename = os.path.join(
                yeastFolder,
                ('yeast_binary'+(str(i+1)).zfill(3)+'.jpg')
            )
            cv2.imwrite(filename,yeastArray[i])

        for j in range(len(neuFolder)):

            filename = os.path.join(
                neuFolder,
                ('neutrophil_binary'+(str(j+1)).zfill(3)+'.jpg')
            )
            cv2.imwrite(filename,neuArray[j])

        for k in range(len(multFolder)):

            filename = os.path.join(
                multFolder,
                ('interaction_binary'+(str(k+1)).zfill(3)+'.jpg')
            )
            cv2.imwrite(filename,multArray[k])

    def getOpenPath(self):
        # popup to select single file

        global file_path
        file_path = getPath()

        # set filename texbox to selected file
        if file_path != "":

            self.openText.configure(state="normal")
            self.openText.delete("0.0", "end")
            self.openText.insert("0.0",file_path)
            self.openText.configure(state="disabled")


    def sliderUpdate(self, inp):
        # update UI when sens changes

        if inp > 0:
            strOut = "+"+str(int(inp))
            self.sensVal.configure(text=strOut)
        else:
            self.sensVal.configure(text=str(int(inp)))

    

    def runCount(self):
        # initiates processing sequence and collects necessary variables
        time1 = time.perf_counter()
        blurState = self.blurCheck.get()
        useZ = self.zCheck.get()
        CSVname = self.outputText.get("0.0",END)
        try:
            self.fullCount(file_path, CSVname, 'Single', blurState, useZ)
            time2 = time.perf_counter()
            duration = round(time2-time1,2)
            print('Runtime: '+str(duration)+' seconds')
            self.countComplete()
        except NameError:
            self.FileError()
        except Exception as e:
            print(str(e))

    def countComplete(self):

        messagebox.showinfo(message="File counted.", type="ok")


    def getBatchOpen(self):
        # popup to get multiple files

        global files
        files = batchOpen()
        global numFiles
        numFiles = len(files)

        self.selectedtext.configure(state="normal")
        self.selectedtext.delete("0.0",END)
        str1 = "You have selected "+str(numFiles)+" file(s)."
        self.selectedtext.insert("0.0",str1)
        self.selectedtext.configure(state="disabled")

    def tryProcess(self):
        # initiates batch processings
        
        try:
            self.batchProcessFiles(files)
        except NameError:
            self.FileError()

    def batchProcessFiles(self, files):
        # runs full counting sequence for multiple files
        time1 = time.perf_counter()
        global csvpath
        global currTiff
        for tif in range(numFiles):
            print('starting batch '+str(tif)+'...')
            currImage = files[tif]
            currName = os.path.splitext(os.path.basename(currImage))[0]
            # currName = "batch_"+str(tif)+".csv"
            currTiff = 'batch'+str(tif)
            self.fullCount(currImage, currName, 'Batch')
        time2 = time.perf_counter()
        duration = round(time2-time1,2)
        print('Runtime: '+str(duration)+' seconds')
        self.batchComplete()


    def batchComplete(self):
        alert = str(numFiles)+" files counted."
        messagebox.showinfo(message=alert, type="ok")

    def colorComplete(self):
        alert = 'Files colored.'
        messagebox.showinfo(message=alert, type="ok")

    def getColorOpen(self):
        global color_file_path
        color_file_path = getPath()

        if color_file_path != "":

            self.openColorText.configure(state="normal")
            self.openColorText.delete("0.0", "end")
            self.openColorText.insert("0.0",color_file_path)
            self.openColorText.configure(state="disabled")

    def tryColor(self):
        try:
            time1 = time.perf_counter()
            self.colorFile(color_file_path)
            time2 = time.perf_counter()
            duration = round(time2-time1,2)
            print('Runtime: '+str(duration)+' seconds')
            self.colorComplete()
        except NameError as e:
            self.FileError()
            print(str(e))

    def colorFile(self, inputtiff):
        desktop = os.path.expanduser("~/Desktop")
        outputFolder = os.path.join(desktop,'Phagocytometer Files')
        blur = self.blurColorCheck.get()
        global channelNames
        hex_array = hex_default
        print('getting channel information...')
        channelNames = tifChannelNames(inputtiff)
        
        self.getChannelIdentity()

        print("converting to images...")
        yeastImgs, neuImgs = tifToArrays(inputtiff, yeastChannel, NeuChannel, channelNames)
        print("thresholding...")
        yeastBins, neuBins = fileToBinary(yeastImgs, neuImgs)
        exportFormat = self.exportFormat.get()
        print("coloring images...")
        multBins = colorTif(yeastBins, neuBins, outputFolder, exportFormat, hex_array)
        isColorSave = self.saveColorCheck.get()
        if isColorSave:
            self.saveToImg(yeastBins,neuBins,multBins,outputFolder)


    def FileError(self):
        # if file not found
        messagebox.showerror(message="Please select a file.", type='ok', icon='warning')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # center and title window
        def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
                """Centers the window to the main display/monitor"""
                screen_width = Screen.winfo_screenwidth()
                screen_height = Screen.winfo_screenheight()
                x = int(((screen_width/2) - (width/2)) * scale_factor)
                y = int(((screen_height/2) - (height/1.5)) * scale_factor)
                return f"{width}x{height}+{x}+{y}"
        
        self.title("Phagocytometer")

        self.geometry(CenterWindowToDisplay(self, 900, 450, self._get_window_scaling())) 

        # create and use tabbed window
        self.tab_view = TabView(self)
        self.tab_view.pack(padx=20,pady=20, anchor='center') 
        icon = tk.PhotoImage(file = 'assets/phagocytometer_icon.png')
        self.iconphoto(False, icon)

if __name__ == '__main__':
    app = App()
    app.mainloop()
 