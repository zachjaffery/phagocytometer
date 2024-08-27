import numpy as np
import cv2
import os
import pandas as pd


from src.CountCells import countCellsInImage
from src.declarations import z_factor

def splitAndCountPhago(greenbin, bluebin, binDir, csvname, useZ, saveMult=True):

    greenBin = greenbin
    blueBin = bluebin

    greenBinSorted = sorted(os.listdir(greenBin))
    blueBinSorted = sorted(os.listdir(blueBin))

    if len(greenBinSorted) == len(blueBinSorted):

        # establish folders
        neuDirectory = greenBin
        yeastDirectory = blueBin

        #create data lists
        phagoCount = []
        fold = os.path.join(binDir,'/mult/')
        if os.path.exists(fold) is False:
            os.mkdir(fold)
        for i in range(len(greenBinSorted)):

            # read current neutrophil binary
            neuFile = greenBinSorted[i]

            neuFilename = neuDirectory+neuFile
            neuImg = cv2.imread(neuFilename,0)

            # read current yeast binary
            yeastFile = blueBinSorted[i]

            yeastFilename = yeastDirectory+yeastFile
            yeastImg = cv2.imread(yeastFilename,0)
            filename = (str(i)+".jpg")
            
            path = os.path.join(fold,filename)
            # multiply to get phagocytosis

            kernel = np.ones((5,5),np.uint8)

            #subtract
            differenceMap = cv2.subtract(neuImg,yeastImg)


            cv2.namedWindow('window')
            cv2.imshow('window',differenceMap)
            cv2.waitKey(0)
    else: 
        raise Exception("Neutrophil and Yeast folders are different lengths")

   
    CSVfilename = csvname

    df = pd.read_csv(CSVfilename)
    df['Phagocytosis'] = phagoCount
    df.to_csv(CSVfilename,index=False)



