import os, sys, subprocess, logging
#from GUIgoodness import turn_off_button_during_work
from time import sleep #to allow delays
#import shutil
from PIL import Image

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # this is to hide the command line
'''
settings = 
    {
    "resizeMax":resizeMax.get(),
    "maxWidth":maxWidth.get(), 
    "maxHeight":maxHeight.get(), # for now we aren't going to worry about this. We'll only make images squares
    "maxDimension":max(maxWidth.get(), maxHeight.get()),

    "resizeMin":resizeMin.get(),
    "minWidth":minWidth.get(),
    "minHeight":minHeight.get(),
    "minDimension":min(minWidth.get(),minHeight.get()),

    "addCanvas":addCanvas.get(),
    "stripExif":stripExif.get(),
    "imageCompression":imageCompression.get(),
    "convertJPG":convertJPG.get(),
    "delOriginalFile":delOriginalFile.get(),
    "keepPNGFile":keepPNGFile.get(),
    "debuggingMenu":debuggingMenu.get(),
    }


PSUEDO CODE FUN!
for image in list_of_images:
    ################################
    # Figure out target image size #
    ################################
    if resizeMax AND resizeMin:
        #check if either dim of image are larger than maxHeight
        if max(width,height) > settings[maxHeight]:
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
        if max(width,height) > settings[maxHeight]:
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

def get_stretch_dimensions(image_width, image_height, maximum_dimension):
    if image_width > image_height: #Image width > height
        new_width = maximum_dimension
        new_height = round(image_width/image_height*new_width)
    else: #either height is the same or larger than width. either are okay
        new_height = maximum_dimension
        new_width = round(image_width/image_height*new_height)
    return new_width, new_height

def get_shrink_dimensions(image_width, image_height, minimum_dimension):
    if image[1] > image[2]: #Image width > height
        new_width = minimum_dimension
        new_height = round(image[1]/image[2]*new_width)
    else: #either height is the same or larger than width. either are okay.
        new_height = settings[minDimension]
        new_width = round(image[1]/image[2]*new_height)
    return new_width, new_height
#if largest image dimension is neither larger than maxHeight, nor smaller than minHeight
#then do not resize the image.


def process_images(settings, list_of_images):
    logging.info("werwerkwerk.process_images started")
    logging.debug(F"The var was received with {len(list_of_images)} entries.")
    global work_happening
    print(str(dir()))
    #print("Is work happening here in werkwerkwerk? " + str(work_happening))
    
    work_happening = True #lets threading know that work is happening.
    sleep(0) # not needed
    for image in list_of_images:
        #setup stuff....
        flagstring = "" #this will build the arguements to be sent to imagemagick
        currentfilename = image[0]
        file_without_extension, extension = os.path.splitext(currentfilename)
        newfilename = file_without_extension + extension.lower()
        w,h = image[1],image[2] #width, height. defining now, but may be overwritten if the image need to be resized
        logging.debug(F"Image {currentfilename} with width, height: {image[1]}, {image[2]}")

        ################################
        # Figure out target image size #
        ################################
        if settings[resizeMax] AND settings[resizeMin]:
            #check if either the largest image dimension is larger allowed
            if max(image[1],image[2]) > settings[maxDimension]:
                w,h = get_stretch_dimensions(image[1],image[2],settings[maxDimension])
                
                flagstring = flagstring + F"-resize {w}x{h} " #resize string for imagemagick

            #if not larger than max, then check if the image is smaller than the minimum
            elif min(image[1],image[2]) > settings[minDimension]:
                w,h = get_shrink_dimensions(image[1],image[2],settings[minDimension])
                
                flagstring = flagstring + F"-resize {w}x{h} " #resize string for imagemagick
                
            #if largest image dimension is neither larger than maxHeight, nor smaller than minHeight
            #then do not resize the image.
            else: pass

        elif settings[resizeMax]: #Only resizeMax
            #check if the image is larger than maximum
            if max(width,height) > settings[maxHeight]:
                w,h = get_stretch_dimensions(image[1],image[2],settings[maxDimension])
            
            flagstring = flagstring + F"-resize {w}x{h} " #resize string for imagemagick


        elif settings[resizeMin]: #Only resizeMin
            #check if the image is smaller than the minimum
            if min(image[1],image[2]) > settings[minDimension]:
                w,h = get_shrink_dimensions(image[1],image[2],settings[minDimension])
            
            flagstring = flagstring + F"-resize {w}x{h} " #resize string for imagemagick

        else: #no resizing
            logging.debug("This image is in the Goldilocks zone.")

        #Put a background on the image. A white background with a centered image.
        if settings[addCanvas]:
            logging.debug("addCanvas is true")
            if w != h:
                flagstring = flagstring + F"-gravity center -background white -extent {max(w,h)}x{max(w,h)} "
                #extend the image to the maximum border, to make it a square.
            
            else: pass #the image is already square, or w and h are both undefined. :-/

        if settings[convertJPG]: # convert to another jpg
            if extension.lower() == ".jpg": 
                pass #extension is built at the beginning of this function

            else:
                newfilename = file_without_extension + ".jpg"
                #file_without_extension is built at the beginning of this function

        if settings[stripExif]:
            logging.debug("stripping exif")
            flagstring = flagstring + "-strip "
        
        if settings[imageCompression]:
            logging.debug(F"quality set to {imageCompression}")
            flagstring = flagstring +  F"-quality {imageCompression} "
        
        if flagstring != "":
            from shutil import which
            executable = which('magick')
            argument = []
            argument.append(executable)
            argument.append(currentfilename)
            argument.append(flagstring)
            arument.append(newfilename)
            #argument = F'{executable} "{currentfilename}" {flagstring} "{newfilename}"'
            subprocess.call(argument, startupinfo=si, shell=True)

    #print(counter)
    work_happening = False #lets threading know that work is done.
    logging.info("werwerkwerk.process_images ended")

'''
def shrink_to_bounds(filename,width,height,newfilename):
    argument = str("convert " + filename + ' -resize '+str(width)+'x'+str(height)+' '+ newfilename)
    if reporting: print("Shrinking: " + argument)
    subprocess.call(argument, startupinfo=si, shell=True)
    counter['shrunk'] += 1

def grow_to_bounds(filename,width,height,newfilename):
    argument = str("convert " + filename + ' -resize '+str(width)+'x'+str(height)+' '+newfilename) 
    if reporting: print("Growing: " + argument)
    subprocess.call(argument, startupinfo=si, shell=True)
    counter['grown'] += 1

def squareoff_image():
    pass

def canvas_image(filename,width,height,newfilename):
##            this is the imagemagick command to put on a white border
##            convert input.jpg -gravity center -background white -extent 250x250  output.jpg
    argument = str("convert "+ filename + " -gravity center -background white -extent "+ \
          str(width)+"x"+str(height)+" "+newfilename)
    if reporting: print(argument)
    if subprocess.call(argument, startupinfo=si, shell=True): counter['canvased'] += 1

def format_convert(filename,image_format):
    try:
        file_and_ext = os.path.splitext(filename)
        if reporting: print(str(file_and_ext[0],image_format))
        if file_and_ext[1].lower() == image_format:
            if reporting: print(str("same extension: " + image_format))
            pass
        else:
            argument = str('convert "' + filename + '" -background white -flatten "' + file_and_ext[0] + image_format + '"')
            if reporting: print(argument)
            if subprocess.call(argument, startupinfo=si, shell=True): counter['converted'] += 1
            #do the conversion, and if exits with process 0, then register this as converted.
            else: print("This file could not be converted. Perhaps it is not a graphic.") #delete the old filename also, please
                
    except:
        print("No format conversion.")
##

def PIL_transPNG_to_jpg(img,filename,target_ext):
    file, ext = os.path.splitext(filename)
    print(target_ext)
    print(ext)
    print(file)
    print(img)
    img.show()
    print(img.size)
    if ext != target_ext:
        bg = Image.new("RGB", img.size, (255,255,255))
        bg.paste(img,mask=img.split()[3])
        bg.save(file+target_ext)
    #img.save(fp,format=target_image_format)

def reduce_filesize(filename,filesize):
        #to define max file size "convert file.jpg -define jpeg:extent:500KB newfile.jpg"
    pass

def strip_exif(filename,newfilename):
    logging.debug("werwerkwerk.strip_exif started")
    argument = str('convert "'+ filename + '" -strip "' + newfilename + '"')
    logging.debug(argument)
    subprocess.call(argument, startupinfo=si, shell=True)
    counter['stripped'] += 1
    logging.debug("werwerkwerk.strip_exif started")

def set_image_quality(filename,quality_percent,newfilename):
    argument = str('convert "' + filename + '" -quality '+str(quality_percent)+' "'+newfilename+'"')
    if reporting: print(argument)
    subprocess.call(argument, startupinfo=si, shell=True)
    counter['adj_qual'] += 1

def process_images(conf, list_of_images):
    logging.info("werwerkwerk.process_images started")
    print(len(str(list_of_images)))
    logging.debug("The var was received with " + str(len(list_of_images)) + "entries.")
    global work_happening
    print(str(dir()))
    #print("Is work happening here in werkwerkwerk? " + str(work_happening))
    
    work_happening = True #lets threading know that work is happening.
    sleep(5)
    logging.debug("Start of process images function")
    logging.debug("List of images to process" + str(list_of_images))
##    file_count = sum(1 for f in os.listdir())
##    for filename in os.listdir(source):
    for image in list_of_images:
        logging.info("---------NEW IMAGE-----------")
##        if counter['touched'] % 50 == 0:
##            sys.stdout.write('\r'+str(file_count - counter['touched']) +" files left to go. Working on " + filename + 15 * " "+"\n")
##            sys.stdout.write(str(counter)+'\n')
##
##            sys.stdout.flush()
##        counter['touched'] += 1
        newfilename = image[0]   ## We will modify the images in place
        try:
            dimensions = get_image_dimensions(image[0])
            logging.debug(dimensions)
            #Shrink huge image to max dimensions
            if resize:
                if reporting: print('resize')
                if max(dimensions) > max(max_dimensions): #picture is bigger than max_dimensions
                    shrink_to_bounds('"'+filename+'"',max_dimensions[0],max_dimensions[1],'"'+newfilename+'"')

                #Stretch small images to be at least hero-sized on one dimension
                if force_to_hero_size and max(dimensions) < max(hero_dimensions):
                    #resize image
                    grow_to_bounds('"'+filename+'"',hero_dimensions[0],hero_dimensions[1],'"'+newfilename+'"')

                else: pass
        
            if canvas: #apply a white background with the image centered
                if reporting: print('canvas')
                if max(dimensions) < max(hero_dimensions):
                    print("teeny picture:"+filename)
                    canvas_image('"'+filename+'"',hero_dimensions[0],hero_dimensions[1],'"'+newfilename+'"')
                elif max(dimensions) > max(max_dimensions):
                    print("biggy picture:"+filename)
                    canvas_image('"'+filename+'"',max_dimensions[0],max_dimensions[1],'"'+newfilename+'"')
                elif dimensions[0]/dimensions[1]== max_dimensions[0]/max_dimensions[1]:pass
##                    print('nothing to do here')
                else:
                    print("normal picture:"+filename)
                    canvas_image('"'+filename+'"',max(dimensions),max(dimensions),'"'+newfilename+'"')

            if image_format: # convert to another format
                if reporting: print('format')
                format_convert(filename,image_format)
            if strip:
                    if reporting: print("stripping exif")
                    strip_exif(filename,newfilename)
            if quality_percent:
                    if reporting: print("quality set to %",quality_percent)
                    set_image_quality(filename,quality_percent,newfilename)          
        
        except Exception as e: print(str(e))
    print(counter)
    work_happening = False #lets threading know that work is done.
    logging.info("werwerkwerk.process_images ended")

#processing a single image file. let's try to make this work before we
# do it with a bunch of files at once.
def process_image(file_with_dimensions):
    global imageConfig
    logging.debug(imageConfig)
    logging.debug(file_with_dimensions)
    newfilename = file_with_dimensions[0]   ## We will modify the images in place

    dimensions = ()
    dimensions.append(file_with_dimensions[1]) #width
    dimensions.append(file_with_dimensions[2]) #height
    
    #increment touched' every time we look at any image
    #need code to add a dictionary entry to the counter list.

    try:
        #Shrink huge image to max dimensions
        if imageConfig[resizeImage]:
            logging.info('Resize '+str(newfilename))
            if max(dimensions) > max(max_dimensions): #picture is bigger than max_dimensions
                shrink_to_bounds('"'+filename+'"',max_dimensions[0],max_dimensions[1],'"'+newfilename+'"')

            #Stretch small images to be at least hero-sized on one dimension
            if force_to_hero_size and max(dimensions) < max(hero_dimensions):
                #resize image
                grow_to_bounds('"'+filename+'"',hero_dimensions[0],hero_dimensions[1],'"'+newfilename+'"')

            else: pass
    
        if canvas: #apply a white background with the image centered
            if reporting: print('canvas')
            if max(dimensions) < max(hero_dimensions):
                print("teeny picture:"+filename)
                canvas_image('"'+filename+'"',hero_dimensions[0],hero_dimensions[1],'"'+newfilename+'"')
            elif max(dimensions) > max(max_dimensions):
                print("biggy picture:"+filename)
                canvas_image('"'+filename+'"',max_dimensions[0],max_dimensions[1],'"'+newfilename+'"')
            elif dimensions[0]/dimensions[1]== max_dimensions[0]/max_dimensions[1]:pass
##                    print('nothing to do here')
            else:
                print("normal picture:"+filename)
                canvas_image('"'+filename+'"',max(dimensions),max(dimensions),'"'+newfilename+'"')

        if image_format: # convert to another format
            if reporting: print('format')
            format_convert(filename,image_format)
        if strip:
                if reporting: print("stripping exif")
                strip_exif(filename,newfilename)
        if quality_percent:
                if reporting: print("quality set to %",quality_percent)
                set_image_quality(filename,quality_percent,newfilename)          
    
    except Exception as e: print(str(e))
'''