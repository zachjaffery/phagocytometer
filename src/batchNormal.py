from newAlgoTest import normalMap
import os
import numpy as np
from BulkProcessToBinary import bulkToBinary

green = '/Users/zachjaffery/Desktop/Phagocytometer/greenNorm'
blue = '/Users/zachjaffery/Desktop/Phagocytometer/blueNorm'

if not os.path.exists(green):
    os.mkdir(green)
if not os.path.exists(blue):
    os.mkdir(blue)

greenIn = '/Users/zachjaffery/Desktop/Phagocytometer/tmp/GreenRaw'
greens = os.listdir(greenIn)
greens = sorted(greens)
blueIn = '/Users/zachjaffery/Desktop/Phagocytometer/tmp/BlueRaw'
blues = os.listdir(blueIn)
blues = sorted(blues)

for i in range(len(greens)):
    inpath = os.path.join(greenIn,greens[i])

    outname = str(i)+'.jpg'
    outpath = os.path.join(green,outname)
    normalMap(inpath,outpath)

for i in range(len(blues)):

    inpath = os.path.join(blueIn,blues[i])

    outname = str(i)+'.jpg'
    outpath = os.path.join(blue,outname)
    normalMap(inpath,outpath)

