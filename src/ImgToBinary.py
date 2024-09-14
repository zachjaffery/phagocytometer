import numpy as np
import cv2

import tkinter as tk
from tkinter import filedialog
 
import os

# open file picker dialog
def getPath():

    # not sure why this is here, but useful for testing i think
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('TIF files','*.tif')])
    # return filepath of selected file/folder
    return file_path

# Get threshold value for img

    # Applying Otsu's method setting the flag value into cv.THRESH_OTSU.
    # Use a bimodal image as an input.
    # Optimal threshold value is determined automatically.
    


# Make binary image from utso threshold value
def generateBinary(image,useBlur=False, sensitivity=0):
    #t = utsoThreshold()

    # read image as MatLike
    if useBlur:
        image = cv2.GaussianBlur(image,(3,3),(0))


    # check for near black image. If so, thresholding will be pointless, so all black it is (this comes up with neutrophil only images)
    if np.average(image) <= 3:
        otsu_threshold, thresh = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)


    else:

        # calculate otsu value
        otsu_threshold, thresh = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        #adjust to sensitivity, if needed

        adjusted_otsu = otsu_threshold + sensitivity

        # make threshold using otsu value
        retval, thresh = cv2.threshold(image, adjusted_otsu, 255, cv2.THRESH_BINARY)

    return thresh
    
def fileToBinary(yeastImgs, neuImgs):

    yeastBins = []
    neuBins = []
    for i in range(len(yeastImgs)):
        yeastBins.append(generateBinary(yeastImgs[i]))
    for i in range(len(neuImgs)):
        neuBins.append(generateBinary(neuImgs[i]))

    return yeastBins, neuBins


