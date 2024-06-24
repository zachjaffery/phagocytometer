from src.UtsoThreshold import utsoThreshold, getPath, generateBinary

import numpy as np
import cv2

 
import os
from os import listdir

from src.SplitTiffs import tiffToImages


# CODE TO UTILIZE SPLIT FUNCTION
# MAKES FOLDERS IF THEY DONT ALREADY EXIST
# write images to separate green and blue folders
# green = neutrophil
# blue = yeast


# THIS IS PROBABLY ONLY NEEDED FOR TESTING, CAN BE OPTIMIZED
def bulkToImg(filepath):


    desktop = os.path.expanduser("~/Desktop")
    dir = os.path.join(desktop,"Phagocytometer/")

    isExistsDir = os.path.exists(dir)
    if isExistsDir == False:
        os.mkdir(dir)

    
    tmpfolder = os.path.join(dir,'tmp/')
    isExistsTmp = os.path.exists(tmpfolder)
    if isExistsTmp == False:
        os.mkdir(tmpfolder)
    
    greenPath = os.path.join(dir,'tmp/GreenRaw/')
    bluePath = os.path.join(dir,'tmp/BlueRaw')

    # greenPath = "/Users/zachjaffery/Desktop/Counting Neu/Greens/"
    # bluePath = "/Users/zachjaffery/Desktop/Counting Neu/Blues/"
    isRealGreen = os.path.exists(greenPath)
    isRealBlue = os.path.exists(bluePath)
    if (isRealBlue) == False:
        os.mkdir(bluePath)
    if (isRealGreen) == False:
        os.mkdir(greenPath)

    tiffFile = filepath

    tiffToImages(tiffFile,greenPath,bluePath)
    return dir, greenPath, bluePath, tmpfolder

