import os, sys, subprocess, logging
#from GUIgoodness import turn_off_button_during_work
from time import sleep #to allow delays
#import shutil
from PIL import Image

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # this is to hide the command line

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

def process_images(list_of_images):
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
