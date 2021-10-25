## scanNplan is part of version 2 of picresizer
## https://github.com/misterashley/picresizer
##
## Get a file selection (currently from config file, later from GUI)
## to build a list of images, with their dimensions.
##
## Get options from the user (currently from config file, later from GUI)
##
## Pass the image list & user options to werkwerkwerk, to do the image modifications.
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

    

import os
##import threading
import time #for timing purposes
from PIL import Image
#global counter
#counter = dict(touched=0, changed_ext=0, converted=0, grown=0, shrunk=0, canvased=0, stripped=0, adj_qual=0)

def scanDirectory(folder):
    found_files = []
##    os.chdir(folder)
    for root, dirs, files in os.walk(folder, topdown = False):
       for name in files:
          found_files.append(os.path.join(root, name))
    return found_files

def validateImageDimensions(file_to_check):
    try:
        img = Image.open(file_to_check)
        #img.verify() #check if the image is valid
        width, height = img.size
        print (img.format)
##        print(file_to_check, width, height)
        return (file_to_check, width, height)
    except IOError: pass # print(file_to_check,"is not an image."

def getImageListFromDir(folder):
    start_time = time.time()# for timing purposes
    
    files_to_check = scanDirectory(folder)
    print("I found",len(files_to_check),"files.")
    imagesfound = []
    while files_to_check:
        imagesfound.append(validateImageDimensions(files_to_check.pop()))
    print("Of these, I detected",len(imagesfound),"images.")
    #print(imagesfound[-1]) #Show the last image
    print("This took about %s seconds to perform." % round((time.time() - start_time),2)) #for timing purposes

    return imagesfound #returns a list of images, plus width and height

def planChanges(image_entry_list):
    for image_entry in image_entry_list:
        pass
        #change extension? #if file extension is "jfif, jpeg, jpe" (casefolded) then rename to "jpg"
        #Convert to JPG? #imagemagick. if convert to jpg is true and extension is not jpg, then convert. Delete original file.
        #Grow image? #imagemagick. if either image dimensions is smaller than min image size option, then resize.
        #Shrink image? #imagemagick. if either image height or width exceed max dimension as configured option, then resize.
        #Canvas Image? #imagemagick. if image size is not correct h:w ratio, then add canvas.
        #Strip image? #if option enabled then do this for all images.
        #Adjust image quality? #if option enabled then do this for all images.

if __name__ == "__main__":
    working_folder = "C://Users//mrashley//Documents//temp"
    getImageListFromDir(working_folder)

