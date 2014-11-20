## This will take all the images in the source folder convert them
## to a smaller version.
## Optionally it can will put them on a canvas of a given dimension
## or grow images that are smaller than the hero image default.

#user config
bksource =r"C:\Users\mrashley\Google Drive\WebsiteImages\newtest" #the r is for 'raw' allowing \ 
source = bksource.replace('\\','/')
if source[-1] != '/':
	source = source + '/'
#source = "C:/Users/mrashley/Dropbox/Photos for website/" # must have trailing /

max_dimensions = (1000,1000)
hero_dimensions = (393,484)
#force_hero_size
#True means we will upsize the image's largest edge a hero dimension
#False means we will leave the image at it's native size
force_to_hero_size = True
#put_on_canvas
#True means we will put the image on a canvas for a consistent image ratio
#False means we will only resize large images
canvas = True
convert = ".jpg"
#string of ".jpg" or ".png" or ".gif" to convert files to this format.
resize = True

#----------------------- no config below this -----------------

import os, sys, subprocess
#import shutil
from PIL import Image

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # this is to hide the command line

def get_image_dimensions(filename):
    try:
        img = Image.open(filename) # get the image's width and height in pixels
        width, height = img.size #find image dimensions of file or return error
        return (width, height)
    except IOError: print(filename,"is not an image.")

def shrink_to_bounds(filename,width,height,newfilename):
##    print("convert " + filename + ' -resize '+str(width)+'x'+str(height)+' '+newfilename)
    subprocess.call("convert " + filename + ' -resize '+str(width)+'x'+str(height)+' '+newfilename, startupinfo=si, shell=True)


def grow_to_bounds(filename,width,height,newfilename):
##    print("convert " + filename + ' -resize '+str(width)+'x'+str(height)+' '+newfilename)
    subprocess.call("convert " + filename + ' -resize '+str(width)+'x'+str(height)+' '+newfilename, startupinfo=si, shell=True)

def squareoff_image():
    pass

def canvas_image(filename,width,height,newfilename):
##            this is the imagemagick command to put on a white border
##            convert input.jpg -gravity center -background white -extent 250x250  output.jpg
    subprocess.call("convert "+ filename + " -gravity center -background white -extent "+ \
          str(width)+"x"+str(height)+" "+newfilename, startupinfo=si, shell=True)

def format_convert(filename,wanted_format):
        try:
            file_and_ext = os.path.splitext(filename)
            if file_and_ext[1].lower() == wanted_format:
                pass
            else:
                print("converted ", filename, " to ", file_and_ext[0] + convert)
                subprocess.call("convert " + filename + " -background white -flatten " + \
                                file_and_ext[0] + convert, startupinfo=si, shell=True)
        except:
            print("Format coonversion failed")


def process_images():
    files_completed = 0
    file_count = sum(1 for f in os.listdir())
    for filename in os.listdir(source):
##        print (type(file_count),type(files_completed))
        if files_completed % 50 == 0:
            sys.stdout.write('\r'+str(file_count - files_completed) +" files left to go. Working on " + filename + 15 * " "+"\n")
            sys.stdout.flush()
        files_completed = files_completed + 1
        newfilename = filename   ## What we if modify them in place?
        try:
            dimensions = get_image_dimensions(source + filename)
            #Shrink huge image to max dimensions
            if resize:
                if max(dimensions) > max(max_dimensions): #picture is bigger than max_dimensions
                    shrink_to_bounds('"'+filename+'"',max_dimensions[0],max_dimensions[1],'"'+newfilename+'"')

                #Stretch small images to be at least hero-sized on one dimension
                if force_to_hero_size and max(dimensions) < max(hero_dimensions):
                    #resize image
                    grow_to_bounds('"'+filename+'"',hero_dimensions[0],hero_dimensions[1],'"'+newfilename+'"')

                else: pass
##                    print (filename,"is",dimensions)
        
            if canvas:
                if max(dimensions) < max(hero_dimensions):
                    canvas_image('"'+filename+'"',hero_dimensions[0],hero_dimensions[1],'"'+newfilename+'"')
                elif max(dimensions) > max(max_dimensions):
                    canvas_image('"'+filename+'"',max_dimensions[0],max_dimensions[1],'"'+newfilename+'"')
                else:
                    canvas_image('"'+filename+'"',max(dimensions),max(dimensions),'"'+newfilename+'"')

## convert to another format.                   
            if convert:
                format_convert(filename,convert)
##                try:
##                    file_and_ext = os.path.splitext(filename)
##                    if file_and_ext[1].lower() == convert:
##                        pass
##                    else:
##                        print("converted ", filename, " to ", file_and_ext[0], convert)
##                        subprocess.call("convert " + filename + " -background white -flatten " + \
##                                        file_and_ext[0] + convert, startupinfo=si, shell=True)
##                except:
##                    print("convert fail")
        
        except Exception as e: print(str(e))

if __name__ == "__main__":
##    images to one folder

##    rename images to:
##                  caps, unformatted item, unformatted_[1] (if there are supporting)

##    resize images - do we want to stretch out images smaller than the hero size?
    os.chdir(source)
    print("Working in",str(os.getcwd()))
    process_images()

##    canvas the new images -

#os.system("""convert "RTK-logoSmartLight.jpg" -gravity center -background white -extent 250x250 "RTK-logoSmartLight.jpg" """)

#to define max file size "convert file.jpg -define jpeg:extent:500KB newfile.jpg"
