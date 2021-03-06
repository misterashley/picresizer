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

max_dimensions = (1000,1000)
hero_dimensions = (400,400)
#force_hero_size
#True means we will upsize the image's largest edge a hero dimension
#False means we will leave the image at it's native size
force_to_hero_size = False
#put_on_canvas
#True means we will put the image on a canvas for a consistent image ratio
#False means we will only resize large images
canvas = False

quality_percent = 85  #jpg percent quality // set quality_percent to 0 (zero) to disable.
#%92 is pretty good, %85 is okay.

strip = True #strip exif tag // True to enable, False to disable.
#This will make the files sometimes quite a bit smaller

image_format = ".jpg" #False for no conversion, or ".jpg", ".png", ".gif"
#string of ".jpg" or ".png" or ".gif" to convert files to this format.
#this is problematic at times...

resize = False #False for no resize

reporting = False #False for minor reporting. True for lots of reporting

#----------------------- no config below this -----------------

import os, sys, subprocess
#import shutil
from PIL import Image
global counter
counter = dict(touched=0, grown=0, shrunk=0, canvased=0, converted=0, stripped=0, adj_qual=0)

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # this is to hide the command line

def get_image_dimensions(filename):
    try:
        img = Image.open(filename) # get the image's width and height in pixels
        width, height = img.size #find image dimensions of file or return error
        return (width, height)
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
    process_images()
    print("Finished. Going up a level.")
    os.chdir("..") #change director to up one level, so the directory is unlocked

##    canvas the new images -

#os.system("""convert "RTK-logoSmartLight.jpg" -gravity center -background white -extent 250x250 "RTK-logoSmartLight.jpg" """)


