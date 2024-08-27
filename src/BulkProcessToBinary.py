from src.OtsuThreshold import generateBinary

import os
from os import listdir



def bulkToBinary(greenpath, bluepath, dir, useBlur=False, sensitivity=0):
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
        folderOut = greenBin
        index = str(i).zfill(3)
        nameOut = str(index)+"greenBinary"
        
        generateBinary(currPath,
                    folderOut,
                    nameOut, useBlur, sensitivity
                    )
        
        # OTHER SEGMENTING ALGO
        # watershedSegment(currPath,
        #             folderOut,
        #             nameOut)

    # iterate through blue folder and make binaries
    for i in range(len(bluesSorted)):

        currFile = bluesSorted[i]
        currPath = os.path.join(bluePath,currFile)
        folderOut = blueBin
        index = str(i).zfill(3)
        nameOut = index+"blueBinary"
        
        generateBinary(currPath,
                    folderOut,
                    nameOut, useBlur, sensitivity
                    )    
        
        # OTHER SEGMENTING ALGO
        # watershedSegment(currPath,
        #             folderOut,
        #             nameOut)

    return dir, greenBin, blueBin