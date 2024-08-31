import os
import cv2
import numpy as np



def colorPhago(dir, yeastPath, neuPath, doCount):

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


    return sub8color

    # if doCount:
    #     phago_count = cv2.connectedComponentsWithStats(phago_mask)[0]
    #     return phago_count
    # else:
    #     return None




def colorTif(greenbin, bluebin, dir, export_format):
    greenFolder = os.listdir(greenbin)
    blueFolder = os.listdir(bluebin)

    greensSorted = sorted(greenFolder)
    bluesSorted = sorted(blueFolder)

    if len(greensSorted) == len(bluesSorted):

        imgs = []
        img_names = []
        if os.path.exists(dir) == False:
            os.mkdir(dir)

        # create output and write to phago folder

        outfolder = os.path.join(dir, 'colorMaps/')

        if os.path.exists(outfolder) == False:
            os.mkdir(outfolder)
        
        
        for i in range(len(greensSorted)):

            currGreen = greensSorted[i]
            currBlue = bluesSorted[i]

            currGreenPath = os.path.join(greenbin,currGreen)
            currBluePath = os.path.join(bluebin,currBlue)
            
            filename = 'colormap'+str(i+1).rjust(3,'0')+'.jpg'
            colored_img = colorPhago(dir, currBluePath,currGreenPath,False)

            imgs.append(colored_img)
            img_names.append(filename)

        if export_format == 'JPG Sequence':
            for i in range(len(imgs)):
                outpath = os.path.join(outfolder, img_names[i])
            
                cv2.imwritemulti(outpath, imgs[i])

        elif export_format == 'MP4':


            height,width,layers=imgs[0].shape

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoName = os.path.join(outfolder,'colored_sequence.mp4')
            video = cv2.VideoWriter(
                filename=videoName,
                apiPreference=cv2.CAP_FFMPEG,
                fourcc=fourcc,
                fps=10,
                frameSize=(width,height),
                params=[
                    cv2.VIDEOWRITER_PROP_DEPTH,
                    cv2.CV_8U,
                    cv2.VIDEOWRITER_PROP_IS_COLOR,
                    1
                ]
                )
            
            for i in range(len(imgs)):
                video.write(imgs[i])
            video.release()

    
def sequenceToTif(imgs, dir):

    coloredImgs = os.listdir(imgs)
    imgSeq = []

    for i in range(len(coloredImgs)):

        currPath = os.path.join(dir, coloredImgs[i])
        
        img = cv2.imread(currPath)
        imgSeq.append(img)

    filename = "tiff_color.tif"
    filepath = os.path.join(dir, filename)
    cv2.imwrite(filepath,imgSeq)