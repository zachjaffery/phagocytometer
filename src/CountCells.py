
from OtsuThreshold import otsuThreshold, getPath, generateBinary

import numpy as np
import cv2

 
import os

from src.SplitTiffs import tiffToImages


 # CODE FROM USER "alkasm" ON STACKOVERFLOW (https://stackoverflow.com/a/47570902/24016481)


def countCellsInImage(binaryPath):
    if type(binaryPath) == str: 
        img = cv2.imread(binaryPath, 0)
    elif type(binaryPath) == np.ndarray:
        img = binaryPath
    else:
        raise Exception("The image being counted cannot be analyzed. Make sure it is either a string or an array")
    seed_pt = (25, 25)
    fill_color = 0
    mask = np.zeros_like(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    for th in range(60, 120):
        prev_mask = mask.copy()
        mask = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
        mask = cv2.floodFill(mask, None, seed_pt, fill_color)[1]
        mask = cv2.bitwise_or(mask, prev_mask)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    n_centers = cv2.connectedComponents(mask)[0] - 1
    return n_centers


