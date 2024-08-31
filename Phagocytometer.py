import os
from os import listdir, mkdir, rmdir
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import *
import datetime
from datetime import datetime
import shutil


from src.OtsuThreshold import getPath
from src.BulkProcessToImg import bulkToImg
from src.BulkProcessToBinary import bulkToBinary
from src.CountNeutrophils import countNeus
from src.ChannelsToPhagocytosis import splitAndCountPhago
from src.ChannelsToTouching import splitAndCountInt
from src.BatchOpen import batchOpen 
from src.stats import makeStats
from src.phagoColorFunc import colorTif



class TabView(customtkinter.CTkTabview):
    def __init__(self,master):
        super().__init__(master)

        
        # create tabs
        mainTab = self.add('Process Single File')
        batchTab = self.add('Batch Process')
        colorTab = self.add('Auto-Color File')

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
        self.delCheck = customtkinter.CTkCheckBox(mainTab,text="Delete binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.delCheck.grid(row=6,column=2, sticky="w")
        
        # button to count the file
        self.countButton = customtkinter.CTkButton(mainTab,command=self.runCount,text="Count File",text_color='white')
        self.countButton.grid(row=7,column=3, sticky='ew')



        """         BATCH TAB CODE           """

        self.emptyTop = customtkinter.CTkFrame(batchTab,fg_color="transparent", height=10)
        self.emptyTop.grid(row=0, column=3)

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

        self.empty12 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty12.grid(row=2,column=4,padx=5,pady=5)

        self.empty01 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=15, width=5)
        self.empty01.grid(row=3,column=1,padx=5,pady=5, sticky='e')

        self.selectedtext = customtkinter.CTkTextbox(batchTab, bg_color="transparent", fg_color="transparent",state='disabled', height=15)
        self.selectedtext.grid(row=3, column=2, padx=5,pady=5, sticky='')

        self.empty01 = customtkinter.CTkFrame(batchTab, fg_color="transparent", height=5, width=15)
        self.empty01.grid(row=4,column=2,padx=5,pady=5, sticky='w')

        # experimentally decided scale value, subject to change
        self.useZ = IntVar(value=1)
        self.zBatchCheck = customtkinter.CTkCheckBox(batchTab,text="Use Z-adjustment? (recommended)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1,variable=self.useZ)
        self.zBatchCheck.grid(row=5,column=2,sticky="w")
        
        # gaussian blur option
        self.blurBatchCheck = customtkinter.CTkCheckBox(batchTab,text="Use Gaussian blur for thresholding? (Helpful for noisy images)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.blurBatchCheck.grid(row=6,column=2, sticky="w")

        # option to save binary images
        self.delBatchCheck = customtkinter.CTkCheckBox(batchTab,text="Delete binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.delBatchCheck.grid(row=7,column=2, sticky="w")
        
        # button to count the file
        self.countButton = customtkinter.CTkButton(batchTab,command=self.batchProcessFiles,text="Count Files",text_color='white')
        self.countButton.grid(row=8,column=3)

        
        """         COLOR TAB CODE          """
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

        self.delColorCheck = customtkinter.CTkCheckBox(colorTab,text="Delete binary images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.delColorCheck.grid(row=3, column=2, sticky='ew')


        self.label = customtkinter.CTkLabel(colorTab,text='File format:', wraplength=350)
        self.label.grid(row=4, column=1, sticky='w')

        self.formatVal = customtkinter.StringVar(value="JPG Sequence")
        self.exportFormat = customtkinter.CTkOptionMenu(colorTab,values=['JPG Sequence','MP4'], variable=self.formatVal, fg_color='white',text_color='black')
        self.exportFormat.grid(row=4, column=2, sticky='ew')


        self.runColor = customtkinter.CTkButton(colorTab, text="Process File", command=self.tryColor)
        self.runColor.grid(row=4, column=3, sticky='ew')
        
        self.empty00 = customtkinter.CTkFrame(colorTab, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=5,column=4,padx=5,pady=5)

    def fullCount(self, tifPath, CSVname, useBlur, useZ):
        global csvpath

        sensActive = False
        
        if sensActive:
            sens = self.sensSlider.get()
        else:
            sens = 0


        
        dir1, greenPath1, bluePath1, tmpfolder = bulkToImg(tifPath)
        dir2, greenBin1, blueBin1 = bulkToBinary(greenPath1, bluePath1, dir1, useBlur, sens)
        csvpath = countNeus(greenBin1, blueBin1, dir2, CSVname)
        
        if self.countPhagoCheck.get():
            splitAndCountPhago(greenBin1, blueBin1, dir2, csvpath, useZ)
        if self.countInteractCheck.get():
            splitAndCountInt(greenBin1, blueBin1, dir2, csvpath, useZ)
        
        makeStats(csvpath)
        isDelete = self.delCheck.get()
        if isDelete:
            shutil.rmtree(tmpfolder)

    def getOpenPath(self):
        global file_path
        file_path = getPath()

        if file_path != "":

            self.openColorText.configure(state="normal")
            self.openColorText.delete("0.0", "end")
            self.openColorText.insert("0.0",file_path)
            self.openColorText.configure(state="disabled")

    def sliderUpdate(self, inp):
        
        
        if inp > 0:
            strOut = "+"+str(int(inp))
            self.sensVal.configure(text=strOut)
        else:
            self.sensVal.configure(text=str(int(inp)))

    def noFileError(self):
        messagebox.showerror(message="Please select a file.", type='ok', icon='warning')
    

    def runCount(self):
        blurState = self.blurCheck.get()
        useZ = self.zCheck.get()
        CSVname = self.outputText.get("0.0",END)
        try:
            self.fullCount(file_path, CSVname, blurState,useZ)
            self.countComplete()
        except NameError:
            self.noFileError()

    def countComplete(self):
        messagebox.showinfo(message="File counted.", type="ok")

    def getBatchOpen(self):
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
        try:
            self.batchProcessFiles(files)
        except NameError:
            self.FileError()

    def batchProcessFiles(self, files):

        global csvpath
        
        for tif in range(numFiles):
            
            currImage = files[tif]
            currName = os.path.splitext(os.path.basename(currImage))[0]
            # currName = "batch_"+str(tif)+".csv"
            #add progress bar
            dir1, greenPath1, bluePath1, tmpfolder = bulkToImg(currImage)
            # dir2, greenBin1, blueBin1 = bulkToBinary(greenPath1, bluePath1, dir1, False, sensitivity=0)

            if self.blurBatchCheck.get():
                blur = True
            dir2, greenBin1, blueBin1 = bulkToBinary(greenPath1, bluePath1, dir1, blur)
            csvpath = countNeus(greenBin1, blueBin1, dir2, currName)
            useZ = self.zBatchCheck.get()
            splitAndCountPhago(greenBin1, blueBin1, csvpath, useZ)
            makeStats(csvpath)
            isBatchDelete = self.delBatchCheck.get()
            if isBatchDelete:
                shutil.rmtree(tmpfolder)
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
            self.colorFile(color_file_path)
            self.colorComplete()
        except NameError:
            self.FileError()

    def colorFile(self, inputtiff):
        
        blur = self.blurColorCheck.get()
        dir, greenPath, bluePath, tmpfolder = bulkToImg(inputtiff)
        dir, greenBin, blueBin = bulkToBinary(greenPath, bluePath, dir,blur)
        exportFormat = self.exportFormat.get()
        
        colorTif(greenBin, blueBin, dir, exportFormat)


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
 