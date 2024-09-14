import numpy as np
import cv2
import os
import pandas as pd


from src.CountCells import countCellsInImage
from src.declarations import z_factor

def splitAndCountInt(yeastBins, neuBins, csvname, useZ,  binDir, saveMult=False):



    if len(yeastBins) == len(neuBins):

        #create data lists
        multImgs = []
        phagoCount = []
        # fold = os.path.join(binDir,'mult')

        # if os.path.exists(fold) is False:
        #     os.mkdir(fold)
        for i in range(len(yeastBins)):

            # read current neutrophil binary
            neuFile = neuBins[i]


            yeastFile = yeastBins[i]


            kernel = np.ones((5,5),np.uint8)

            mult = cv2.multiply(neuFile,yeastFile)
            mult = cv2.morphologyEx(mult,cv2.MORPH_CLOSE,kernel)
            mult = cv2.dilate(mult,kernel, iterations=1)
            multImgs.append(mult)

            count = countCellsInImage(mult)

            #Z-FACTOR ADJUSTMENT
            if useZ:
                count = count*z_factor
            phagoCount.append(count)
    else: 
        raise Exception("Neutrophil and Yeast folders are different lengths")

   
    CSVfilename = csvname

    df = pd.read_csv(CSVfilename)
    df['Adjusted Neutrophil Interactions'] = phagoCount
    df.to_csv(CSVfilename,index=False)

    return multImgs


