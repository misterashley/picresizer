## This will take all the images in the source folder convert them
## to a smaller version.
## Optionally it can will put them on a canvas of a given dimension
## or grow images that are smaller than the hero image default.

#user config
bksource =r"C:\Users\mrashley\Documents\temp\Wholesale Charms, Silver Charms, Pendants and Jewelry Findings _ Nina Designs_files\jpg - Copy" #the r is for 'raw' allowing \ 
source = bksource.replace('\\','/')
if source[-1] != '/':
	source = source + '/'
#source = "C:/Users/mrashley/Dropbox/Photos for website/" # must have trailing /

max_dimensions = (1000,1000) #maximum image size

hero_dimensions = (400,400) #minimum image size

force_to_hero_size = False
#True means we will upsize the image's largest edge a hero dimension
#False means we will leave the image at it's native size

canvas = False
#True means we will put the image on a canvas for a consistent image ratio
#False means we will only resize large images

quality_percent = 85
#jpg percent quality // set quality_percent to 0 (zero) to disable.
#%92 is pretty good, %85 is okay.

strip = True
#strip exif tag // True to enable, False to disable.
#This will make the files sometimes quite a bit smaller

image_to_jpg = False
#False for no conversion
#True to convert images to .jpg

resize = False
#False for no resize at all
#True to allow image resizing

reporting = False
#True to show command as they're created
#False for no commands

#----------------------- no config below this -----------------

import os, sys, subprocess
#import shutil
from PIL import Image
global counter
counter = dict(touched=0, grown=0, shrunk=0, canvased=0, converted=0, stripped=0, adj_qual=0)


## This is to hide the command line form appearing during operations
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

##################################################################################
## Pseudo code
##################################################################################

## The reason for this version is to use all the modules to create a set of
## arguments, which will then be executed in as few commands as possible,
## rather than a command for each step, which is inefficient.

##  Setup output images intentions:
##      hero size
##      force resize of small images up to hero? y/n (embiggen)
##      max size
##  	resize down to max y/n (shrinken)
##  	add image canvas y/n
##  	jpg quality %
##      jpg compress progressive y/n
##  	strip EXIF data from image y/n
##  	convert to jpg y/n
##      exempt_png_from_jpg_conversion y/n #if convert to jpg, do we want to leave png
##  	debugging report y/n

##      global Arguments[]
##      ##These are the arguments that we'll .append which will go between filenames 

##  def verifyExtension(file,extension):
##      return(file matches extension)

##  
##  def file_convert(imageFilename, newImageFilename, *Arguments):
##      command = file + " "
##      while Arguments:
##              command = command + Arguments.pop() + " "
##      command = command + newImageFilename
##      if debuging_report: print(command)
##      CliCall(command)


##def professFiles():
##   ##########################   MAIN PROGRAM   ##################
##  clear Arguments[]
##  for file in folder:
##  	find extension:
##  	        if extension is jpg, png, bmp, tif, gif:
##                      if verifyExtensions(file,extension):
##                              get image dimensions
##                              if embiggen AND dimensions < hero size: Arguments.add(embiggen_argument)
##                              if shrinken AND dimensions > max_size: Arguments.add(shrinken_argument)
##                              if canvasen: Arguments.add(canvasen_argument)
##                              if strip_exif: Arguments.add(strip_exif_argument)
##                              if convert_to_jpg or extension is jpg:
##                                      if jpg_quality: Arguments.add(jpg_quality_argument)
##                                      if jpg_progressive: Arguments.add(jpg_progressive_argument)
##                              if extension is png and convert_to_jpg:
##                                      if exempt_png_from_jpg_conversion:pass
##                                      else: Arguments.add(png_to_jpg_alpha_argument)
##                                      
##                      else: print("It looks like this file isn't right.")
##  		if other: tell user not an image, move to the next file

##      if source image is png:
##              if convert to jpg:
##                      if leave_as_png: pass
##                      else:
##                              png to jpg PIL call
##              	        change source file to be newly created jpg file ##hacky.. i don't like this solution###



def get_image_dimensions(filename):
    try:
        img = Image.open(filename) # get the image's width and height in pixels
        width, height = img.size #find image dimensions of file or return error
        return (width, height)
        # report ratio if you like
        # from fractions import gcd
        # greatest_common_denom = gcd (1000, 1000)
        # then divide each variable by greatest_common_denom
    except IOError: print(filename,"is not an image.")

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
    argument = str('convert "'+ filename + '" -strip "' + newfilename + '"')
    if reporting: print(argument)
    subprocess.call(argument, startupinfo=si, shell=True)
    counter['stripped'] += 1

def set_image_quality(filename,quality_percent,newfilename):
    argument = str('convert "' + filename + '" -quality '+str(quality_percent)+' "'+newfilename+'"')
    if reporting: print(argument)
    subprocess.call(argument, startupinfo=si, shell=True)
    counter['adj_qual'] += 1

def process_images():
    file_count = sum(1 for f in os.listdir())
    for filename in os.listdir(source):
        if reporting: print("-------------------------------")
        if reporting:   print (type(file_count),type(counter))
        sys.stdout.flush()
        if counter['touched'] % 50 == 0:
            sys.stdout.write('\r'+str(file_count - counter['touched']) +" files left to go. Working on " + filename + 15 * " "+"\n")
            sys.stdout.write(str(counter)+'\n')

            sys.stdout.flush()
        counter['touched'] += 1
        newfilename = filename   ## We will modify the images in place
        try:
            dimensions = get_image_dimensions(source + filename)
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

if __name__ == "__main__":
##    images to one folder

##    rename images to:
##                  caps, unformatted item, unformatted_[1] (if there are supporting)

##    resize images - do we want to stretch out images smaller than the hero size?
    os.chdir(source)
    print("Working in",str(os.getcwd()))
    process_files()
    print("Finished. Going up a level.")
    os.chdir("..") #change director to up one level, so the directory is unlocked

##    canvas the new images -

#os.system("""convert "RTK-logoSmartLight.jpg" -gravity center -background white -extent 250x250 "RTK-logoSmartLight.jpg" """)


