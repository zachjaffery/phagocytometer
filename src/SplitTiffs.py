import cv2
import os


def tiffToImages(filepath, greenPath, bluePath):
    
    # List to store the loaded image 
    images = [] 

    # store tif stack as images
    ret, images = cv2.imreadmulti(mats=images, 
                                filename=filepath, 
                                flags=cv2.IMREAD_GRAYSCALE) 
    
    # Write images to blue/green 
    if len(images) > 1: 
        
        for i in range(len(images)):
                
                # Bring blue (yeast) to blue folder
                # WHICHEVER COLOR IS FIRST GOES HERE
                if (i % 3) == 0:
                    # Dynamic name 
                    index = str(i).zfill(3)
                    name = index+"Blue" 


                    # Displaying the image 
                     

                    # Save the images 
                    
                    filename = name+'.jpg'
                    cv2.imwrite(os.path.join(bluePath , filename), images[i])

                # Bring green (neu) to green folder
                # WHICHEVER COLOR IS THIRD GOES HERE
                elif ((i-2) % 3) == 0:
                    # Dynamic name 
                    index = str(i).zfill(3)
                    name = index+"Green" 


                    

                    # Save the images 
                    
                    filename = name+'.jpg'
                    cv2.imwrite(os.path.join(greenPath , filename), images[i])

                # Skip second image
                elif ((i-1) % 3) == 0:
                    pass
                # Catch error
                else: 
                    print("Error: Mod 3 error")
