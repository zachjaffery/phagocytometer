from src.CountCells import countCellsInImage

import numpy as np
import cv2
import os

import datetime
from datetime import datetime


import pandas as pd

def countNeus(neuBins, baseDir, CSVname=None):
    #empty lists
    neutrophilCount = []
    frameNumber = []

    # count each image
    for i in range(len(neuBins)):
   
        count = countCellsInImage(neuBins[i], 50)
        neutrophilCount.append(count)
        frameNumber.append(i+1)


    
    # get proper filename or use default time/date
    CSVname = CSVname.replace("\n","")

    if CSVname == None or CSVname == "example.csv":
        currDateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        sheetname = currDateTime+'.csv'
        filepath = os.path.join(baseDir,sheetname)
    elif CSVname.endswith(".csv"):
        filepath = os.path.join(baseDir,CSVname)
    else:
        sheetname = CSVname+'.csv'
        filepath = os.path.join(baseDir,sheetname)



    # write to csv
    df = pd.DataFrame(list(zip(frameNumber,neutrophilCount)),columns=['Frame Number','Cell Count'])
    
    df.to_csv(filepath, index = False)
    return filepath
