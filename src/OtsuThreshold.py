import numpy as np
import cv2

import tkinter as tk
from tkinter import filedialog
 
import os

# open file picker dialog
def getPath():
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
def generateBinary(img_name,output_folder,output_name, useBlur, sensitivity):
    #t = utsoThreshold()

    # read image as MatLike
    image = cv2.imread(img_name, 0)
    if useBlur:
        image = cv2.GaussianBlur(image,(3,3),(0))


    
    if np.average(image) <= 3:
        otsu_threshold, thresh = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)


    else:

        # calculate otsu value
        otsu_threshold, thresh = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        #adjust to sensitivity

        adjusted_otsu = otsu_threshold + sensitivity

        # make threshold using otsu value
        retval, thresh = cv2.threshold(image, adjusted_otsu, 255, cv2.THRESH_BINARY)

        

    # make file name
    ext = ".jpg"
    filename = output_name+ext

    #print(filename)
    # make filepath from name

    out_filepath = os.path.join(output_folder, filename)
    #print(out_filepath)

    # write the output image
    cv2.imwrite(out_filepath, thresh)
    


    


