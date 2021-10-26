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

import os
##import threading
import time #for timing purposes
start_time = time.time()# for timing purposes
from PIL import Image
global counter
counter = dict(touched=0, grown=0, shrunk=0, canvased=0, converted=0, stripped=0, adj_qual=0)
#global image_files
#image_files = []


def find_files(folder):
    found_files = []
##    os.chdir(folder)
    for root, dirs, files in os.walk(folder, topdown = False):
        for name in files:
            found_files.append(os.path.join(root, name))
    return found_files

def validate_image_dimensions(file_to_check):
    try:
        img = Image.open(file_to_check)
        width, height = img.size
##        print(file_to_check, width, height)
        return (file_to_check, width, height)
    except IOError: pass # print(file_to_check,"is not an image.")

def check_image_dims(files):
    if isinstance(files,list):
        for file in files:
            print(file)
            try:
                img = Image.open(file)
                width, height = img.size
                #print(file_to_check, width, height)
                #return (file_to_check, width, height)
            except IOError: print(file_to_check,"is not an image.")
    else: print("not a list")

def create_list_of_images_from_file_list(files,images):
    for i in range (1000):
        # Check if a file is an image. If so, store the file path & image dimensions.
        if len(files) == 0 :break
        this_image = []
        this_image = (validate_image_dimensions(files.pop()))
        #this_image = (validate_image_dimensions(file_list.pop()))
        if this_image != None: images.append(this_image)
            #print(dir())
            #window.statusMessage.set(str(len(file_list)))
    return(files,images)

def pop_and_check(files_to_check):
    global image_files
    #image_files = []
    # Check if the files are images
    while len(files_to_check) > 0:
        possible_image = []
        possible_image = (validate_image_dimensions(files_to_check.pop()))
        if possible_image != None: image_files.append(possible_image)
    
if __name__ == "__main__":
    working_folder = "C://Users//Ashley//Documents//temp//images to test"
    global files_to_check
    files_to_check = find_files(working_folder)
    print("Remaining files to check:",str(len(files_to_check)))
    #global image_files
    #image_files = []
    pop_and_check(files_to_check)
    print("Image files found:",len(image_files))
    print("-----%s seconds----" % (time.time() - start_time)) #for timing purposes
