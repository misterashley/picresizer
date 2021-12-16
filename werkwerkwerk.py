import subprocess, logging
from pathlib import Path
#from GUIgoodness import turn_off_button_during_work
from time import sleep #to allow delays
#import shutil
from PIL import Image
from shutil import which

si = subprocess.STARTUPINFO()
#si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # this is to hide the command line
'''
PSUEDO CODE FUN!
for image in list_of_images:
    ################################
    # Figure out target image size #
    ################################
    if resizeMax AND resizeMin:
        #check if either dim of image are larger than maxHeight
        if max(width,height) > settings.get('maxHeight'):
            #if so, shrink that larger edge to maxHeight
                if width > height:
                    shrink to width
                else:
                    shrink to height #either height is the same or larger than width. either are okay
        #if not larger than max, then check if the image is smaller than the minimum
        elif min(width,height) > settings(minHeight):
            if width > height:
                stretch to width
            else:
                stretch to height #either height is the same or larger than width. either are okay.
        #if largest image dimension is neither larger than maxHeight, nor smaller than minHeight
        #then do nothing here.
        else: pass

    elif resizeMax: # and not resizeMin
        #check if either dim of image are larger than maxHeight
        if max(width,height) > settings.get('maxHeight'):
            #if so, shrink that larger edge to maxHeight
                if width > height:
                    shrink to width
                else:
                    shrink to height #either height is the same or larger than width. either are okay


    elif resizeMin: #and not resizeMax
        #if not larger than max, then check if the image is smaller than the minimum
        elif min(width,height) > settings(minHeight):
            #stretch the larger edge to minHeight
            if width > height:
                stretch to width
            else:
                stretch to height #either height is the same or larger than width. either are okay.        

    else: #no resizing
        pass

    #for now we're only doing square canvasing
    if addCanvas:
        #If it's already square do nothing.    
        if width == height: pass

        elif width > height:
            canvas image to square on the width
        else:
            canvas iamge to square on the height

    #remove exif data from the image to make the image smaller
    if stripExif:
        #with imagemagick add "-strip" argument
    
    #image quality no if statement; always do it.
    #with imagemagick "-quality 99" so 
    "-quality {}".format(imageCompression)

    if convertJPG:
        if image is JPEG and if image ext is .jpg:
            pass

        elif image is not JPEG:
            #if image001.png is what we're converting check for image001.jpg (same filename new extension)
            #if image001.jpg exists what do we do? dunno yet. skip for now I guess.
            else: 
                #convert to .jpg file
                if delOriginalfile and #image001.jpg (new file) exists:
                    #delete original file

        else: #image ext is not .jpg, but file is JPEG type
            #if we are renaming image002.jpeg, check if image002.jpg exists.
            try:
                #rename image
                currentfilename = image[0]
                if currentfilename.rfind(".",-10) == -1: #there is no period in the last 10 chars of the filename:
                    newfilename = currentfilename + ".jpg"
                else:
                    newfilename = currentfilename[:-currentfilename.rfind(".",-10)] + ".jpg" #strip off ".extension" add ".jpg"
                    #rename currentfilename to newfilename
                    os.rename(currentfilename, newfilename)
            except FileExistsError:
                logging.warning(F"Couldn't rename {currentfilename} --> {newfilename}")


                newfilename = image[0](strip ext, add ".jpg"):
                dunno yet. skip for now.
            else:
                #rename image0002.jpeg to image002.jpg

'''

def get_max_dimensions(image_width, image_height, maximum_dimension):
    if image_width > image_height:
        new_width = maximum_dimension
        new_height = round(maximum_dimension/image_width*image_height)
    else:
        new_height = maximum_dimension
        new_width = round(maximum_dimension/image_height*image_width)
    #count("stretch") # update counter
    return new_width, new_height

def get_min_dimensions(image_width, image_height, minimum_dimension):
    if image_width > image_height:
        new_width = minimum_dimension
        new_height = round(minimum_dimension/image_width*image_height)
    else: #either height is the same or larger than width. either are okay.
        new_height = minimum_dimension
        new_width = round(minimum_dimension/image_height*image_width)
    #count("shrink") # update counter
    return new_width, new_height
#if largest image dimension is neither larger than maxHeight, nor smaller than minHeight
#then do not resize the image.

def count(action):
    global status_update_text
    if action not in status_update_text:
        status_update_text[action] = 1
    else:
        status_update_text[action] = status_update_text[action] + 1


def process_images(settings, list_of_images):
    logging.info("werwerkwerk.process_images started")
    logging.info(F"werkwerkwerk recieved {len(list_of_images)} images to change.")
    logging.info(settings)

    global work_happening
    work_happening = True #lets threading know that work is happening.

    global status_update_text
    status_update_text = {}
    
    for image in list_of_images:
        flagstring = "" #this will build the arguements to be sent to imagemagick
        currentfilename = image[0]
        logging.debug(80*"#")
        logging.debug(image[0])
        extension = image[0].suffix
        file_without_extension = str(image[0])[:-len(extension)]
        #file_without_extension, extension = os.path.splitext(currentfilename)
        newfilename = Path(file_without_extension + extension)
        w,h = image[1],image[2] #width, height. defining now, but may be overwritten if the image need to be resized
        logging.debug(F"Image {currentfilename} with width, height: {image[1]}, {image[2]}")
        count("looked at") # how many images did we look at

        ################################
        # Figure out target image size #
        ################################
        

        if settings.get('resizeMax') and settings.get('resizeMin'):
            #check if image is bigger than allowed
            if max(w,h) > settings.get('maxDimension'):
                w,h = get_max_dimensions(w,h,settings.get('maxDimension'))
                flagstring = flagstring + F"-resize {w}x{h} "

            #if bigger, then check if image smaller than allowed
            elif max(w,h) < settings.get('minDimension'):
                w,h = get_min_dimensions(w,h,settings.get('minDimension'))
                flagstring = flagstring + F"-resize {w}x{h} "
                
            #if largest image dimension is neither larger than maxHeight, nor smaller than minHeight
            #then do not resize the image.
            else: pass

        elif settings.get('resizeMax'): #Only resizeMax
            #check if image is bigger than allowed
            if max(w,h) > settings.get('maxDimension'):
                w,h = get_max_dimensions(w,h,settings.get('maxDimension'))
                flagstring = flagstring + F"-resize {w}x{h} "

        elif settings.get('resizeMin'): #Only resizeMin
            if max(w,h) < settings.get('minDimension'):
                w,h = get_min_dimensions(w,h,settings.get('minDimension'))
                flagstring = flagstring + F"-resize {w}x{h} "

        else: #no resizing
            logging.debug("This image is in the Goldilocks zone.")

        #Put a background on the image. A white background with a centered image.
        if settings.get('addCanvas'):
            logging.debug("addCanvas is true")
            if w != h:
                flagstring = flagstring + F"-gravity center -background white -extent {max(w,h)}x{max(w,h)} "
                count("add background") # update counter
                #extend the image to the maximum border, to make it a square.
            
            else: pass #the image is already square, or w and h are both undefined. :-/

        if settings.get('convertJPG'): # convert to another jpg
            if extension.lower() == ".jpg": 
                pass #extension is built at the beginning of this function

            else:
                newfilename = Path(file_without_extension + ".jpg")
                count("converted to jpg") # update counter
                #file_without_extension is built at the beginning of this function

        if settings.get('stripExif'):
            logging.debug("stripping exif")
            flagstring = flagstring + "-strip "
            count("EXIF data stripped") # update counter
        
        if settings.get('imageCompression'):
            logging.debug(F"quality set to {settings.get('imageCompressionPercent')}")
            flagstring = flagstring +  F"-quality {settings.get('imageCompressionPercent')} "
            count("compressed") # update counter
        
        if flagstring != "":
            executable = Path(which('magick'))
            argument = F'"{executable}" "{currentfilename}" {flagstring} "{newfilename}"'
##            argument = []
##            argument.append(executable)
##            argument.append(currentfilename)
##            argument.append(flagstring)
##            argument.append(newfilename)
            print(argument)
            go = subprocess.run(argument, startupinfo=si, shell=True, capture_output=True)
            #go = subprocess.run(argument, startupinfo=si, shell=True, capture_output=True)
            logging.debug(F"Flagstring: {flagstring}")
            logging.debug(F"Arguments: {go.args}") #the command
            logging.debug(F"Rec'd: {go.stderr}") #what came back
            logging.debug(F"Output: {go.stdout}")
            logging.debug(F"Error: {go.stderr}")
            logging.debug(F"Errorcode: {go.returncode}")
            if go.returncode:
                #print(go.output)
                break
            '''
            argument is the command to run
            startupinfo=si is the stuff above which makes the command line screen not show up
            shell=True means the shell is run. I'll try to turn this off.
            capture_output=True keeps the data from the output
            '''


    #print(counter)
    work_happening = False #lets threading know that work is done.
    logging.info("werwerkwerk.process_images ended")
