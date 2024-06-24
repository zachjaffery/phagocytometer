import numpy as np
import cv2
import os
import pandas as pd


from src.CountCells import countCellsInImage

def splitAndCountPhago(greenbin, bluebin, csvname):

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
        for i in range(len(greenBinSorted)):

            # read current neutrophil binary
            neuFile = greenBinSorted[i]

            neuFilename = neuDirectory+neuFile
            neuImg = cv2.imread(neuFilename,0)

            # read current yeast binary
            yeastFile = blueBinSorted[i]

            yeastFilename = yeastDirectory+yeastFile
            yeastImg = cv2.imread(yeastFilename,0)

            # multiply to get phagocytosis
            mult = cv2.multiply(neuImg,yeastImg)
            count = countCellsInImage(mult)

            phagoCount.append(count)
    else: 
        raise Exception("Neutrophil and Yeast folders are different lengths")

   
    CSVfilename = csvname

    df = pd.read_csv(CSVfilename)
    df['Phagocytosis'] = phagoCount
    df.to_csv(CSVfilename,index=False)




