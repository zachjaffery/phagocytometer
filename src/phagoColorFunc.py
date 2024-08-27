import os
import cv2
import numpy as np



def colorPhago(dir, yeastPath, neuPath, filename, doCount):

    # define kernels
    dilKernel = np.ones((1,1),np.uint8)
    morphKernel = np.ones((3,3),np.uint8)

    # define colors
    bgr_grey = np.array([128,128,128])
    bgr_green = np.array([0, 219, 0])

    bgr_blue = np.array([255, 80, 54])

    bgr_purple = np.array([0,0,255])

    hsv_black = (np.array([0,0,0]),np.array([0,0,3])) #black, yeast color
    hsv_50 = (np.array([0,0,127]),np.array([0,0,129])) # 50% grey, background color
    hsv_75 = (np.array([0,0,188]),np.array([0,0,193])) # 75% grey, phago color
    hsv_white = (np.array([0,0,253]),np.array([0,0,255])) # white, neutrophil color


    # read and pre-process individual binaries

    yeastImg = cv2.imread(yeastPath)
    yeastImg =cv2.morphologyEx(yeastImg,cv2.MORPH_OPEN,morphKernel)

    neuImg = cv2.imread(neuPath)
    neuImg =cv2.morphologyEx(neuImg,cv2.MORPH_OPEN,morphKernel)

    #create 'phago' mult
    mult = cv2.multiply(yeastImg,neuImg)

    # convert to signed space then subtract
    yeastImg = yeastImg.astype(np.int16)
    neuImg = neuImg.astype(np.int16)
    rawSub = neuImg-yeastImg

    # convert from int16 to int8
    scaleSub = (rawSub/2)+128

    # add overlap value
    subwithPhago = scaleSub + mult*0.25


    sub8 = subwithPhago.astype(np.uint8)

    # differentiation in case we want to use sub8 later?
    sub8color = sub8

    # convert to HSV
    sub_hsv = cv2.cvtColor(sub8color, cv2.COLOR_BGR2HSV)

    # create masks for each type
    bg_mask = cv2.inRange(sub_hsv,hsv_50[0],hsv_50[1])
    neu_mask = cv2.inRange(sub_hsv,hsv_white[0],hsv_white[1])
    yeast_mask = cv2.inRange(sub_hsv,hsv_black[0],hsv_black[1])
    phago_mask = cv2.inRange(sub_hsv,hsv_75[0],hsv_75[1])

    
    
    # color different areas 
    sub8color[bg_mask > 0] = bgr_grey
    sub8color[neu_mask > 0] = bgr_green
    sub8color[yeast_mask > 0] = bgr_blue
    sub8color[phago_mask > 0] = bgr_purple


    # create output and write to phago folder

    outfolder = os.path.join(dir, 'colorMaps/')

    if os.path.exists(outfolder) == False:
        os.mkdir(outfolder)
    
    outpath = os.path.join(outfolder, filename)
    
    cv2.imwrite(outpath, sub8color)

    if doCount:
        phago_count = cv2.connectedComponentsWithStats(phago_mask)[0]
        return phago_count
    else:
        return None




def colorTif(greenbin, bluebin, dir, export_format):
    greenFolder = os.listdir(greenbin)
    blueFolder = os.listdir(bluebin)

    greensSorted = sorted(greenFolder)
    bluesSorted = sorted(blueFolder)

    if len(greensSorted) == len(bluesSorted):

       
        if os.path.exists(dir) == False:
            os.mkdir(dir)

        
        for i in range(len(greensSorted)):

            currGreen = greensSorted[i]
            currBlue = bluesSorted[i]

            currGreenPath = os.path.join(greenbin,currGreen)
            currBluePath = os.path.join(bluebin,currBlue)
            
            filename = 'colormap'+str(i+1).rjust(3,'0')+'.jpg'
        
            colorPhago(dir, currBluePath,currGreenPath,filename,False)

def sequenceToMovie(imgs):

    coloredImgs = os.listdir(imgs)
    