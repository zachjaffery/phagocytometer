# OBSOLETE?


"""


from OtsuThreshold import getPath, generateBinary

import numpy as np
import cv2

 
import os
from os import listdir

from src.SplitTiffs import tiffToImages

#write images to separate green and blue folders
#green = neutrophil
#blue = yeast
greenPath = "/Users/zachjaffery/Desktop/Counting Neu/Greens/"
bluePath = "/Users/zachjaffery/Desktop/Counting Neu/Blues/"
isRealGreen = os.path.exists(greenPath)
isRealBlue = os.path.exists(bluePath)
if (isRealBlue) == False:
    os.mkdir(bluePath)
if (isRealGreen) == False:
    os.mkdir(greenPath)

tiffFile = "/Users/zachjaffery/Desktop/test.tif"

tiffToImages(tiffFile,greenPath,bluePath)


#write binaries to separate folders

greenBinaryPath = "/Users/zachjaffery/Desktop/Counting Neu/Green Binaries/"
blueBinaryPath = "/Users/zachjaffery/Desktop/Counting Neu/Blues Binaries/"
isRealGreenBin = os.path.exists(greenBinaryPath)
isRealBlueBin = os.path.exists(blueBinaryPath)
if (isRealBlueBin) == False:
    os.mkdir(blueBinaryPath)
if (isRealGreenBin) == False:
    os.mkdir(greenBinaryPath)

folder_dir = os.listdir(greenPath)


for i in range(len(folder_dir)):
    currImage = str(folder_dir[i])
    currPath = os.path.join(str(greenPath),currImage)
    t = otsuThreshold(currPath)
    outname = os.path.join("greenBinary",str(i))
    generateBinary(currPath,t,greenBinaryPath,outname)



"""