
# from src.OtsuThreshold import getPath, generateBinary

import numpy as np
import cv2


# from src.SplitTiffs import tiffToImages


# CODE/INSPIRATION FROM USER "alkasm" ON STACKOVERFLOW (https://stackoverflow.com/a/47570902/24016481)


def countCellsInImage(binaryPath, cutoff=None):

    # reads image or MatLike to img variable
    if type(binaryPath) == str:
        img = cv2.imread(binaryPath, 0)
    elif type(binaryPath) == np.ndarray:
        img = binaryPath
    else:
        raise Exception("The image being counted cannot be analyzed. Make sure it is either a string or an array")
    
    # alkasm code:

    # initiate variables and array for thresholding
    seed_pt = (5,5)
    fill_color = 0
    mask = np.zeros_like(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # dont think the for loop is necessary, can just use mask at 60
    # for th in range(60, 120):
    #     prev_mask = mask.copy()
    #     mask = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
    #     mask = cv2.floodFill(mask, None, seed_pt, fill_color)[1]
    #     mask = cv2.bitwise_or(mask, prev_mask)
    #     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    mask = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.floodFill(mask, None, seed_pt, fill_color)[1]
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # the image should already be thresholded correctly; this is just to be safe

    # get count
    n_centers, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    # cv2.connectedComponents counts the background as an object, so subtract one to rectify
    stats = stats[:,-1]
    if cutoff != None:
        excluded = sum(1 for i in stats if i < cutoff)

        adjustedCount = n_centers-excluded-1
    else:
        adjustedCount = n_centers-1
    
    return adjustedCount

