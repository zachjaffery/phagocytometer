import numpy as np
import pandas as pd
import cv2
import os
from os import listdir, mkdir, rmdir
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import *
import datetime
from datetime import datetime
import shutil


from OtsuThreshold import getPath, otsuThreshold, generateBinary
from src.SplitTiffs import tiffToImages
from src.CountCells import countCellsInImage
from src.BulkProcessToImg import bulkToImg
from src.BulkProcessToBinary import bulkToBinary
from src.CountNeutrophils import countNeus
from src.ChannelsToPhagocytosis import splitAndCountPhago
from src.BatchOpen import batchOpen



class ToplevelBatch(customtkinter.CTkToplevel):
    def __init__(batch, empty):
        
        super().__init__()
        
        def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
            """Centers the window to the main display/monitor"""
            screen_width = Screen.winfo_screenwidth()
            screen_height = Screen.winfo_screenheight()
            x = int(((screen_width/2) - (width/2)) * scale_factor)
            y = int(((screen_height/2) - (height/1.5)) * scale_factor)
            return f"{width}x{height}+{x}+{y}"
        
        batch.title("Batch Process")

        batch.geometry(CenterWindowToDisplay(batch, 400, 300, batch._get_window_scaling())) 

        batch.label = customtkinter.CTkLabel(batch,text='Select multiple TIF files then click "Process Files." Files will be name batch_1, batch_2, etc.', wraplength=350)
        batch.label.pack(anchor=CENTER, padx=10, pady=10)

        batch.batchButton = customtkinter.CTkButton(batch, text="Select Files",command=batch.getBatchOpen)
        batch.batchButton.pack(padx=10, pady=10)

        batch.selectedtext = customtkinter.CTkTextbox(batch, bg_color="transparent", fg_color="transparent",state='disabled', height=15)
        batch.selectedtext.pack(anchor=CENTER, padx=10, pady=10)
        

        batch.runBatch = customtkinter.CTkButton(batch, text="Process Files", command=batch.tryProcess)
        batch.runBatch.pack(padx=10, pady=10)
        
        

    def getBatchOpen(batch):
        global files
        files = batchOpen()
        global numFiles
        numFiles = len(files)

        batch.selectedtext.configure(state="normal")
        batch.selectedtext.delete("0.0",END)
        str1 = "You have selected "+str(numFiles)+" file(s)."
        batch.selectedtext.insert("0.0",str1)
        batch.selectedtext.configure(state="disabled")

    def tryProcess(batch):
        try:
            batch.batchProcessFiles(files)
        except NameError:
            batch.FileError()

    def batchProcessFiles(batch, files):

        global csvpath
        
        for tif in range(numFiles):
            
            currImage = files[tif]
            currName = "batch_"+str(tif)+".csv"
            #add progress bar
            dir1, greenPath1, bluePath1, tmpfolder = bulkToImg(currImage)
            dir2, greenBin1, blueBin1 = bulkToBinary(greenPath1, bluePath1, dir1, False)
            csvpath = countNeus(greenBin1, blueBin1, dir2, currName)
            splitAndCountPhago(greenBin1, blueBin1, csvpath)
            shutil.rmtree(tmpfolder)
        batch.batchComplete()



    def FileError(batch):
        messagebox.showerror(message="Please select a file.", type='ok', icon='warning')

    def batchComplete(batch):
        alert = numFiles+"files counted."
        messagebox.showinfo(message=alert, type="ok")

class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")
    

    

    def __init__(self):

        super().__init__()

        def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
            """Centers the window to the main display/monitor"""
            screen_width = Screen.winfo_screenwidth()
            screen_height = Screen.winfo_screenheight()
            x = int(((screen_width/2) - (width/2)) * scale_factor)
            y = int(((screen_height/2) - (height/1.5)) * scale_factor)
            return f"{width}x{height}+{x}+{y}"
        
        self.title("Phagocytometer")

        self.geometry(CenterWindowToDisplay(self, 800, 400, self._get_window_scaling()))  



        # open button/filepath

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)

        



        self.emptyTop = customtkinter.CTkFrame(self,fg_color="transparent", height=10)
        self.emptyTop.grid(row=0, column=3)

        self.empty00 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=15)
        self.empty00.grid(row=1,column=0,padx=5,pady=5)

        self.openLabel = customtkinter.CTkLabel(self,height=5,text="Select a TIF file to count:", anchor="e")
        self.openLabel.grid(row=1,column=1,padx=5,pady=5, sticky="ew")

        self.openText = customtkinter.CTkTextbox(self, height=5, width=100, text_color="#BABABA")
        self.openText.insert("0.0","Choose a file path")
        self.openText.grid(row=1,column=2, padx=5,pady=5,sticky='ew')
        self.openText.configure(state="disabled")

        self.openButton = customtkinter.CTkButton(self, command=self.getOpenPath, text="Select File")
        self.openButton.grid(row=1,column=3, padx=5, pady=5,sticky='ew')

        self.empty01 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=15)
        self.empty01.grid(row=1,column=4,padx=5,pady=5)

        # output directory


        self.empty10 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=15)
        self.empty10.grid(row=2,column=0,padx=5,pady=5)

        self.outputLabel = customtkinter.CTkLabel(self,height=5,text="Set filename for the output CSV (Optional):", wraplength=150,justify="left", anchor="e")
        self.outputLabel.grid(row=2,column=1,padx=5,pady=5, sticky="ew")

        self.outputText = customtkinter.CTkTextbox(self, height=5, width=100, text_color="#6b6b6b")
        self.outputText.insert("0.0","example.csv")
        self.outputText.grid(row=2,column=2,columnspan=1, padx=5,pady=5,sticky='ew')

        spacerWidth = self.openButton.cget("width")
        print(spacerWidth)
        self.empty11 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=spacerWidth)
        self.empty11.grid(row=2,column=3,padx=5,pady=5, sticky='ew')


        self.empty12 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=15)
        self.empty12.grid(row=2,column=4,padx=5,pady=5)

        self.blurCheck = customtkinter.CTkCheckBox(self,text="Use Gaussian blur for thresholding? (Helpful for noisy images)",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.blurCheck.grid(row=3,column=2, sticky="w")

        self.delCheck = customtkinter.CTkCheckBox(self,text="Delete images after counting?",checkbox_width=15,checkbox_height=15,border_width=1,corner_radius=1)
        self.delCheck.grid(row=4,column=2, sticky="w")
        
        self.countButton = customtkinter.CTkButton(self,command=self.runCount,text="Count File")
        self.countButton.grid(row=5,column=3)

        self.empty50 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=15)
        self.empty50.grid(row=6,column=4,padx=5,pady=5, sticky='ns')
        self.empty50 = customtkinter.CTkFrame(self, fg_color="transparent", height=5, width=15)
        self.empty50.grid(row=7,column=4,padx=5,pady=5, sticky='ns')

        self.batchButton = customtkinter.CTkButton(self, text="Batch Count", command=self.openBatchWindow)
        self.batchButton.grid(row=8,column=1, padx=5,pady=5, sticky="w")

    def fullCount(self, tifPath, CSVname, useBlur):
        global csvpath
        baseDir = os.getcwd() 


        #add progress bar
        dir1, greenPath1, bluePath1, tmpfolder = bulkToImg(tifPath)
        dir2, greenBin1, blueBin1 = bulkToBinary(greenPath1, bluePath1, dir1, useBlur)
        csvpath = countNeus(greenBin1, blueBin1, dir2, CSVname)
        splitAndCountPhago(greenBin1, blueBin1, csvpath)
        isDelete = self.delCheck.get()
        if isDelete:
            shutil.rmtree(tmpfolder)

    def getOpenPath(self):
        global file_path
        file_path = getPath()

        if file_path != "":

            self.openText.configure(state="normal")
            self.openText.delete("0.0", "end")
            self.openText.insert("0.0",file_path)
            self.openText.configure(state="disabled")

    
    def noFileError(self):
        messagebox.showerror(message="Please select a file.", type='ok', icon='warning')
    
    def openBatchWindow(self):
        ToplevelBatch(self)





    def runCount(self):
        blurState = self.blurCheck.get()

        CSVname = self.outputText.get("0.0",END)
        try:
            self.fullCount(file_path, CSVname, blurState)
            self.countComplete()
        except NameError:
            self.noFileError()

    def countComplete(self):
        messagebox.showinfo(message="File counted.", type="ok")

if __name__ == '__main__':
    app = App()
    app.mainloop()
