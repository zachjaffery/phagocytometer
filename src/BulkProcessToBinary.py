from OtsuThreshold import otsuThreshold, getPath, generateBinary

import numpy as np
import cv2

import os
from os import listdir

from src.SplitTiffs import tiffToImages

def bulkToBinary(greenpath, bluepath, dir, useBlur):
    # establish folders containing images
    greenPath = greenpath
    bluePath = bluepath

    # get folder as list
    greens = os.listdir(greenPath)
    blues = os.listdir(bluePath)

    greensSorted = sorted(greens)
    bluesSorted = sorted(blues)

    # make folders for binary images
    greenBin = os.path.join(dir,'tmp/greenBinaries/')
    blueBin = os.path.join(dir,'tmp/blueBinaries/')

    # check to make sure they dont already exists
    isRealGreenBin = os.path.exists(greenBin)
    isRealBlueBin = os.path.exists(blueBin)
    if (isRealBlueBin) == False:
        os.mkdir(blueBin)
    if (isRealGreenBin) == False:
        os.mkdir(greenBin)

    # iterate through green folder and make binaries
    for i in range(len(greensSorted)):

        currFile = greensSorted[i]
        currPath = os.path.join(greenPath,currFile)
        t = otsuThreshold(currPath, useBlur)
        folderOut = greenBin
        index = str(i).zfill(3)
        nameOut = str(index)+"greenBinary"
        
        generateBinary(currPath,
                    t,
                    folderOut,
                    nameOut
                    )

    # iterate through blue folder and make binaries
    for i in range(len(bluesSorted)):

        currFile = bluesSorted[i]
        currPath = os.path.join(bluePath,currFile)
        t = otsuThreshold(currPath, useBlur)
        folderOut = blueBin
        index = str(i).zfill(3)
        nameOut = index+"blueBinary"
        
        generateBinary(currPath,
                    t,
                    folderOut,
                    nameOut
                    )    

    return dir, greenBin, blueBin