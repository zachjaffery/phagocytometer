import nd2
import numpy as np
import cv2
import zarr
import os

def nd2ToArray(filepath,dir=None):

    with nd2.ND2File(filepath) as f:

        # get channel data
        channelNames = f._channel_names
        numOfChannels = len(channelNames)
        # print(numOfChannels,channelNames)
        
        # create empty list to hold all image arrays
        masterList = []
        for i in range(numOfChannels):
            masterList.append([])
        print(masterList)

        # nd2 file to numpy array
        layerArray = nd2.imread(filepath)
        
        # loop through layers and add them to relevant folders
        for i in range(len(layerArray)):

            # get current layer from array
            currLayer = layerArray[i][0]

            j = 0
            while j <= numOfChannels-1:
                
                # add channels from current layer to respective indexes in master list
                masterList[j].append(currLayer[j])
                j += 1

        return masterList, channelNames, numOfChannels


    f.close()

def arrayToImg(arr, yeastChannel, neuChannel, numchannels, dir=None):

    masterdict = {}
    for i in range(numchannels):
        masterdict["layer{}".format(i)] = arr[i]
    
