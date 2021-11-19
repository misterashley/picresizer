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

import os, logging
##import threading
import time #for timing purposes
start_time = time.time()# for timing purposes
from PIL import Image
global counter
counter = dict()
#counter = dict(touched=0, grown=0, shrunk=0, canvased=0, converted=0, stripped=0, adj_qual=0)
#global image_files
#image_files = []
#from GUIgoodness import image_list


def find_files(folder):
    logging.info("scan_n_plan.find_files function started")
    found_files = []
##    os.chdir(folder)
    for root, dirs, files in os.walk(folder, topdown = False):
        for name in files:
##            path = []
##            path.append(root)
##            path.append(name)
##            logging.debug("Found: " + str(path))
            found_files.append(os.path.join(root, name))
            logging.debug("Found: " + str(os.path.join(root, name)))
##            found_files.append(path)
    logging.info("scan_n_plan.file_files found " + str(len(found_files)) + " files.")
    logging.info("scan_n_plan.find_files function started ended")
    return found_files

##def validate_image_dimensions(file_to_check):
##    logging.info("scan_n_plan.validate_image_dimensions function started")
##    try:
##        img = Image.open(file_to_check)
##        width, height = img.size
####        print(file_to_check, width, height)
##        
##    except IOError:
##        logging.info(str(file_to_check) + "is not an image.")
##    logging.info("scan_n_plan.validate_image_dimensions function ended")
##    return (file_to_check, width, height)

##def check_image_dims(files):
##    if isinstance(files,list):
##        for file in files:
##            print(file)
##            try:
##                img = Image.open(file)
##                width, height = img.size
##                #print(file_to_check, width, height)
##                #return (file_to_check, width, height)
##            except IOError: print(file_to_check,"is not an image.")
##    else: print("not a list")

# Check if a file is an image. If so, store the file path & image dimensions.
def create_list_of_images_from_file_list(files_to_scan):
    logging.info("scan_n_plan.create_list_of_images_from_file_list function started")
    
    # Check if there are any files, if none stop.
    if len(files_to_scan) == 0 :
        logging.info("There were " + str(len(files_to_scan))+ " files to scan.")
    
    global image_list
    image_list = []

    for file in files_to_scan:
        this_image = []
        #this_image = (validate_image_dimensions(file))
        try:
            img = Image.open(file)
            width, height = img.size
            this_image.append(file)
            this_image.append(width)
            this_image.append(height)
            image_list.append(this_image)
            logging.info("Found an image: " + str(this_image))
        except:
            logging.debug("Not an image: " + str(file))
            break
    
    logging.info("Found " + str(len(image_list)) + " images from " + str(len(files_to_scan)) + " files.")
    print(dir(turn_off_button_during_work.work_happening)
    #print(str(turn_off_button_during_work.work_happening))
    logging.info("Work happening set to: " + str(work_happening))
    work_happening = False
    logging.info("scan_n_plan.create_list_of_images_from_file_list function ended")

##def create_list_of_images_from_file_list(files_to_scan,images_found):
##    for i in range (1000):
##        # Check if a file is an image. If so, store the file path & image dimensions.
##        if len(files_to_scan) == 0 :break
##        this_image = []
##        this_image = (validate_image_dimensions(files_to_scan.pop()))
##        #this_image = (validate_image_dimensions(file_list.pop()))
##        if this_image != None: images_found.append(this_image)
##            #print(dir())
##            #window.statusMessage.set(str(len(file_list)))
##    return(files_to_scan,images_found)

##def pop_and_check(files_to_check):
##    global image_files
##    #image_files = []
##    # Check if the files are images
##    while len(files_to_check) > 0:
##        possible_image = []
##        possible_image = (validate_image_dimensions(files_to_check.pop()))
##        if possible_image != None: image_files.append(possible_image)
    
if __name__ == "__main__":
    #working_folder = "C://Users//Ashley//Documents//temp//images to test"
    #global files_to_check
    #files_to_check = find_files(working_folder)
    #print("Remaining files to check:",str(len(files_to_check)))
    #global image_files
    #image_files = []
    #pop_and_check(files_to_check)
    #print("Image files found:",len(image_files))
    #print("-----%s seconds----" % (time.time() - start_time)) #for timing purposes
    pass
