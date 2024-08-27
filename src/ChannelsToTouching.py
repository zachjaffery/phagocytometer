import numpy as np
import cv2
import os
import pandas as pd


from src.CountCells import countCellsInImage
from src.declarations import z_factor

def splitAndCountInt(greenbin, bluebin, csvname, useZ,  binDir, saveMult=True):

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

            mult = cv2.multiply(neuImg,yeastImg)
            mult = cv2.morphologyEx(mult,cv2.MORPH_CLOSE,kernel)
            mult = cv2.dilate(mult,kernel, iterations=1)


            count = countCellsInImage(mult)
            if saveMult:
                cv2.imwrite(path,mult)
            #Z-FACTOR ADJUSTMENT
            if useZ:
                count = count*z_factor
            phagoCount.append(count)
    else: 
        raise Exception("Neutrophil and Yeast folders are different lengths")

   
    CSVfilename = csvname

    df = pd.read_csv(CSVfilename)
    df['Neutrophil Interactions'] = phagoCount
    df.to_csv(CSVfilename,index=False)




