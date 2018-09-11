## scanNplan is part of version 2 of picresizer
## https://github.com/misterashley/picresizer
##
## Get a file selection (currently from config file, later from GUI)
##
## Get set of option to use, set these globally
##
## Pass the above to scanNplan, and build a VFO
##    (a list of verified files, with the options to work on)
##
## File selector
##   - Choose a folder
##       - Option to delve into subfolders
##   - Choose a file
## Options (set globally)
##   - Maximum desired output image dimension (Desired ratio is a function of max output)
##   - Minimum desired output image dimensions
##   - Resize images
##   - Canvas enabled
##   - Canvas colour ? (Hex value, colour wheel perhaps)
##   - Compression enabled / percent
##   - Strip EXIF data to shrink filesize
##   - Convert to .JPG
##       - Delete original image upon successful conversion
##   - Preserve .PNG images in that format
##   - Debug to console


#import config file

    

import os, sys, subprocess
#import shutil
from PIL import Image
global counter
counter = dict(touched=0, grown=0, shrunk=0, canvased=0, converted=0, stripped=0, adj_qual=0)

def get_image_dimensions(filename):
    try:
        img = Image.open(filename) # get the image's width and height in pixels
        width, height = img.size #find image dimensions of file or return error
        return (width, height)
    except IOError: print(filename,"is not an image.")


if __name__ == "__main__":
##    images to one folder

##    rename images to:
##                  caps, unformatted item, unformatted_[1] (if there are supporting)

##    resize images - do we want to stretch out images smaller than the hero size?
    os.chdir(source)
    print("Working in",str(os.getcwd()))
    process_images()
    print("Finished. Going up a level.")
    os.chdir("..") #change director to up one level, so the directory is unlocked

##    canvas the new images -

#os.system("""convert "RTK-logoSmartLight.jpg" -gravity center -background white -extent 250x250 "RTK-logoSmartLight.jpg" """)
