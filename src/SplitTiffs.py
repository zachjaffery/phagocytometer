import cv2
import exifread


def tifChannelNames(filepath):
      # code to read exif data from TIF

    # get tags
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)

    # "Image Description" contains relevant metadata
    if "Image ImageDescription" in tags.keys():
        description = tags['Image ImageDescription']

        # for testing purposes:
        # logging.basicConfig(level=logging.DEBUG)
        # logging.debug("ImageDescription: %s (%s)", description, description.values)

        # get all values as big xml string
        vals = description.values
        # split to array, new line as delimiter
        split = vals.split('\r\n')
        # nd2 uses 'Name:' as metadata for channel names
        nameRaw = [s for s in split if 'Name:' in s]
        # name is also on "Camera Name:", so remove first entry
        nameNoCam = nameRaw[1:]
        channelNames = []

        #split "Name: <channel>" into just "<channel>"
        for i in range(len(nameNoCam)):
            nameStripped = ((nameNoCam[i].lstrip()))
            nameCleaved = nameStripped.split()
            channelNames.append(nameCleaved[1])

        return channelNames
    

# temp channels, will be given by user

yeastChannel = 'DAPI'
neuChannel = 'FITC'
channelNames = ['DAPI','DIC','FITC']

def tifToArrays(filepath, yeastChannel, neuChannel, channelNames):


    # List to store the loaded image 
    images = [] 

    # store tif stack as images
    ret, images = cv2.imreadmulti(mats=images, 
                                filename=filepath, 
                                flags=cv2.IMREAD_GRAYSCALE) 
    
    cv2
    # Write images to blue/green 
    if len(images) > 1: 
        
        yeastImgs = []
        neuImgs = []
        yeastIndex = channelNames.index(yeastChannel)
        neuIndex = channelNames.index(neuChannel)
        numChannels = len(channelNames)
        for i in range(len(images)):
                
                # Bring blue (yeast) to blue folder
                # WHICHEVER COLOR IS FIRST GOES HERE
                if ((i-yeastIndex) % numChannels) == 0:
                    yeastImgs.append(images[i])
                elif ((i-neuIndex) % numChannels) == 0:

                    neuImgs.append(images[i])
                # Skip non yeast/neutrophil
                else:
                    pass
    return yeastImgs, neuImgs

