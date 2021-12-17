from tkinter import *

#Pillow is to get image dimensions. This overwrites tkinters
from PIL import Image as Imagereader
from PIL import UnidentifiedImageError

#To allow us to find files in the selected directory
from pathlib import Path

#To prevent the UI from freezing while work is being done.
import threading

#For browsing to the directory with tkinter directory chooser
from tkinter import filedialog

#To allow the use of Combobox used in debugging selection
from tkinter import ttk

from time import sleep
import logging

import subprocess
from shutil import which

from sys import platform

#This hides the command line from appearing & disappearing.
if platform == "win32":
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW 

#logging.WARNING for least info, logging.INFO for more info, logging.DEBUG for most info.
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

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

def count(action):
    global status_update_text
    if action not in status_update_text:
        status_update_text[action] = 1
    else:
        status_update_text[action] = status_update_text[action] + 1

def process_images(settings, list_of_images):
    logging.info(F"process_images started with {len(list_of_images)} images to change.")
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
            if platform == "win32":
                argument = F'"{executable}" "{currentfilename}" {flagstring} "{newfilename}"'
                go = subprocess.run(argument, startupinfo=si, capture_output=True)
            
            #testing for mac
            elif platform == "darwin" or platform == "linux":
                argument.append(executable)
                argument.append(currentfilename)
                argument.append(flagstring)
                argument.append(newfilename)
                go = subprocess.run(argument, capture_output=True)
            
            '''
            go = subprocess.run(argument, startupinfo=si, shell=True, capture_output=True)
            argument is the command to run
            startupinfo=si is the stuff above which makes the command line screen not show up
            shell=True means the shell is run. I'll try to turn this off.
            capture_output=True keeps the data from the output
            '''
            logging.debug(F"Flagstring: {flagstring}")
            logging.debug(F"Arguments: {go.args}") #the command
            logging.debug(F"Rec'd: {go.stderr}") #what came back
            logging.debug(F"Output: {go.stdout}")
            logging.debug(F"Error: {go.stderr}")
            logging.debug(F"Errorcode: {go.returncode}")
            if go.returncode:
                logging.info(go.returncode)

    work_happening = False #lets threading know that work is done.
    logging.info("werwerkwerk.process_images ended")

def scan_folder(): 
        logging.info("scan_folder function started")
        global selected_directory #This is the directory we'll read.
        global buttonProcessImages #buttonProcessImages.config(state=DISABLED/NORMAL)
        global status #Update the statusb bar. Usage: status.set("text")

        #Get a working directory from filedialog.
        selected_directory.set(filedialog.askdirectory())

        if selected_directory.get() != '':
            ##################
            #####STEP ONE#####
            ##################
            status.set(F"Finding files in {selected_directory.get()}. This may take a moment.")
            root.update_idletasks()
            
            #Get a list of files.
            file_list = return_file_list_from_directory(selected_directory.get())
            logging.info(len(file_list))
            ##################
            #####STEP TWO#####
            ##################
            #Build an images_list with images & dimensions from the files.
            logging.debug("thread about to start")
            scan = threading.Thread(target=get_image_list_from_file_list(file_list))
            scan.start()
            logging.debug("thread started")
            #start updating UI with percentage done of file scan. 
            #Unless we can offload this to the function?
            
        else:
            status.set("No folder was chosen. Please choose a folder.")
            root.update_idletasks()
            buttonProcessImages.config(state=DISABLED)
        logging.info(selected_directory.get())
        logging.info("scan_folder function ended")

def return_file_list_from_directory(folder):
    ##STEP ONE of scan
    logging.info("return_file_list_from_directory function started")
    found_files = []
    dir_counter = 0
    p = Path(folder)
    #Could set up a flag to use glob for non-recursive searches with p.glob("*")
    for file in p.rglob("*"):
        if file.is_file():
            found_files.append(file)
            #logging.debug(F"Found file: {file}")
        if file.is_dir():
            dir_counter += 1
    logging.info(F"return_file_list_from_directory found {len(found_files)} files in {dir_counter} folder(s).")
    logging.info("return_file_list_from_directory function started ended")
    return found_files

def get_image_list_from_file_list(files_to_scan):
    # Check if a file is an image. If so, store the file path & image dimensions.
    logging.info("get_image_list_from_file_list function started")
    logging.debug(F"Reviewing {len(files_to_scan)} files")

    global status
    
    # Check if there are any files, if none stop.
    if len(files_to_scan) == 0 :
        status.set("There were no files to scan.")
        root.update_idletasks()
        logging.info("There were no files to scan.")
    
    #refer to the image_list and clear it out
    global image_list
    image_list = []

    for file in files_to_scan:
        i =+ 1
        this_image = []
        try:
            img = Imagereader.open(file)
            width, height = img.size
            this_image.append(file)
            this_image.append(width)
            this_image.append(height)
            image_list.append(this_image)
            logging.debug(F"Found an image: {this_image}")
            img.close()
        except UnidentifiedImageError as error:
            logging.debug(F"Not an image: {file}")
        if i % 50 == 0:
            status.set(F"Found {len(image_list)} images from {len(files_to_scan)} files.")
            root.update_idletasks()
        

    #prepare to update the Process Images button
    global buttonProcessImages
    
    if image_list == 0:
        status.set("No images found.")
        buttonProcessImages.config(state=DISABLED)
        root.update_idletasks()

    elif len(image_list) > 0:
        status.set(F"Found {len(image_list)} images from {len(files_to_scan)} files.")
        buttonProcessImages.config(state=NORMAL, text=F"Modify {len(image_list)} images")
        root.update_idletasks()
    
    logging.info("Found " + str(len(image_list)) + " images from " + str(len(files_to_scan)) + " files.")
    logging.info("get_image_list_from_file_list function ended")

def turn_off_button_during_work():
    logging.info("turn_off_button_during_work function started")
    buttonProcessImages.config(state=DISABLED)
    #sleep(0.5)# a little pause to help multithreading be cool.
    work_happening = True
    while work_happening:
        sleep(0.5)
        #print(".", end='')
        status.set(status_update_text)
        root.update_idletasks()
    status.set(F"Finished. {status_update_text}")
    buttonProcessImages.config(state=NORMAL)
    root.update_idletasks()
    logging.info("turn_off_button_during_work function ended")

def process_images_and_update_ui():
    logging.info("process_images_and_update_ui function started")

    # fetch the current settings
    global imageConfig
    imageConfig = return_image_config()

    logging.info(F"The var was sent with {len(image_list)} entries.")
    user_interface = threading.Thread(target=turn_off_button_during_work)
    work = threading.Thread(target=lambda: process_images(imageConfig, image_list))
    user_interface.start()
    work.start()
    logging.info("process_images_and_update_ui function ended")

def return_image_config():
    logging.info("return_image_config function started")
    settings = {
                "resizeMax":int(resizeMax.get()),
                "maxDimension":int(maxDimension.get()),
                
                "resizeMin":int(resizeMin.get()),
                "minDimension":int(minDimension.get()),
                
                "addCanvas":addCanvas.get(),
                "stripExif":stripExif.get(),

                "imageCompression":imageCompression.get(),
                "imageCompressionPercent":imageCompressionPercent.get(),

                "convertJPG":convertJPG.get(),
                "delOriginalFile":delOriginalFile.get(),
                "keepPNGFile":keepPNGFile.get(),
                "debuggingMenu":debuggingMenu.get(),
                }
    logging.info(F"The settings are: {settings}")
    logging.info("return_image_config function ended")
    return settings

def validate_settings():
    #start building out some rules for how settings are checked.
    if 10000 <= number <= 30000:
        pass

if __name__ == "__main__":
    #The GUI has been launched.
    logging.info("GUI launched.")

    #The app window
    global root
    root = Tk()
    root.title("picResizer by misterashley")
    root.configure(background="white")
    root.geometry('800x450')

    # The main part of the window
    main = Frame(root, bg='white')
    main.pack(side='top', expand=True, fill='both')

    #consider a part of the screen that looks for imagemagick and reports on this
    #perhaps a list of requirements with OK in green, missing in red, and an info button if missing.
    #the info button would give instructions on where to get the missing elements.

    # Build a label: A status bar
    status_bar = Frame(root, bg='black', relief='sunken')
    status_bar.pack(side='bottom', expand=True, fill='x', anchor='s')

    #Build a label: The instructions
    global instructions
    instructions = StringVar()
    instructions.set("""Instructions: \n1. Choose a folder of images to modify. \n2. Choose your options. \n3. Click Modify Images.""")
    #global labelInstructions
    labelInstructions = Label(main, textvariable=instructions, 
        justify='left', bg="white", fg="black", font=("Helvetica",10))
    labelInstructions.grid(row=0, column=0, columnspan=5)#, 'anchor='w')

    #Build the choose a folder button. This direction is meant to have images. We'll scan subdirectories as well.
    buttonChoose = Button(main, text ="Select a folder to scan", width=20, command=scan_folder)
    buttonChoose.grid(row=1, column=0)#.pack(pady=10)

    #Initialize selected_directory
    global selected_directory
    selected_directory = StringVar()

    #Build a label: This is the working directory to process
    #global labelPath
    labelPath = Label (main, textvariable=str(selected_directory), 
        bg="white", fg="blue", font=("monospace", 10))
    labelPath.grid(row=2, column=0, columnspan=5)#.pack()

    ########################################
    #  Maximum dimensions                  #
    ########################################
    resizeMax = IntVar()
    resizeMax.set(1) #0 for unchecked, 1 for checked.
    resizeImageBox = Checkbutton(main, text="Shrink images if either dimension is bigger than (in pixels):", background='white', variable=resizeMax)
    resizeImageBox.grid(row=3, column=0, sticky=W, padx=5)

    #Build an entry box: Max Dimension for Height
    maxDimension = Entry(main, width=10)
    maxDimension.grid(row=3, column=1)
    maxDimension.insert(0, 1000)
    #maxDimension.get() will give you the text supplied in the entry box... it will not Entry is unique apparent. How fucking stupid.

    ########################################
    #  Minimum dimensions                  #
    ########################################
    #Build a checkbox: Stretch image to at least minimum size
    resizeMin = IntVar()
    resizeMin.set(1) #0 for unchecked, 1 for checked.
    resizeImageBox = Checkbutton(main, text="Stretch images if either dimension is smaller than (in pixels):", background='white', variable=resizeMin)
    resizeImageBox.grid(row=4, column=0, sticky=W, padx=5)

    #Build an entry box: Min Dimension for Height
    minDimension = Entry(main, width=10)
    minDimension.grid(row=4, column=1)
    minDimension.insert(0,400)
    #minDimension.get() will give you the text supplied in the entry box... it will not Entry is unique apparent. How fucking stupid.

    ########################################
    #  Other options.                      #
    ########################################

    imageCompression = IntVar() # 0-100 percentage.
    imageCompression.set(1) #0 for unchecked, 1 for checked.
    imageCompressionBox = Checkbutton(main, text="Compress image. (0-100%, higher is clearer image)", background='white', variable=imageCompression)
    imageCompressionBox.grid(row=5, column=0, sticky=W, padx=5)

    imageCompressionPercent = Entry(main, width=5)
    imageCompressionPercent.insert(0,100)
    imageCompressionPercent.grid(row=5, column=1)

    #Build a checkbox: Add canvas to reshape image dimensions
    addCanvas = IntVar() #0 for unchecked, 1 for checked.
    addCanvas.set(1) #enable by default
    addCanvasBox = Checkbutton(main, text="Add a white canvas to images", background='white', variable=addCanvas)
    addCanvasBox.grid(row=6, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    #Build a checkbox: Strip EXIF from JPEG or PNG
    stripExif = IntVar()
    stripExif.set(1) #enable by default
    stripExifBox = Checkbutton(main, text="Strip EXIF info from images", background='white', variable=stripExif)
    stripExifBox.grid(row=7, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    #Build a checkbox: Convert images to .JPG
    convertJPG = IntVar() #0 for unchecked, 1 for checked.
    convertJPG.set(1) #enable by default
    convertJPGBox = Checkbutton(main, text="Convert images to .JPG", background='white', variable=convertJPG)
    convertJPGBox.grid(row=8, column=0, sticky=W, padx=5)

    #Build a checkbox: Delete original file if conversion is successful
    delOriginalFile = IntVar() #0 for unchecked, 1 for checked.
    delOriginalFile.set(1) #enable by default
    delOriginalFileBox = Checkbutton(main, text="Delete original file if conversion is successful", background='white', variable=delOriginalFile)
    delOriginalFileBox.grid(row=9, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    #Build a checkbox: Preserve PNG files
    keepPNGFile = IntVar() #0 for unchecked, 1 for checked.
    keepPNGFile.set(0) #enable by default
    keepPNGFileBox = Checkbutton(main, text="But, don't delete if the file is a .PNG", background='white', variable=keepPNGFile)
    keepPNGFileBox.grid(row=10, column=0, sticky=W, padx=30)#.pack(padx=10, anchor='w')

    debuggingLabel = Label(main, 
        text="Debugging log file. (WARNING least info ... DEBUG most info.)", background='white', anchor=W)
    debuggingLabel.grid(row=11, column=0, padx=5, pady=5, sticky=W)

    #List drop down (rather than Checkbox) for reporting (debugging)
    debuggingLevel = ["WARNING","INFO","DEBUG"]
    debuggingMenu = ttk.Combobox(main, value=debuggingLevel)#
    debuggingMenu.current(0) #WARNING by default
    debuggingMenu['state'] = 'readonly' #Don't allow other options to be entered
    debuggingMenu.grid(row=11, column=1)

    ########################################
    #  Modify image files button.          #
    ########################################

    global buttonProcessImages
    buttonProcessImages = Button(main, text="No images selected", 
        width=20, command=process_images_and_update_ui, state=DISABLED)
    buttonProcessImages.grid(row=20, column=0, sticky=E, padx=60, pady=20)

    ########################################
    #  Status bar.                         #
    ########################################

    #Build a label: Status message
    global status
    status = StringVar()
    status.set("Please choose a folder.")
    #global labelStatus
    labelStatus = Label(status_bar, textvariable=status, fg='green', bg='black', padx='10', font=("monospace",11))
    labelStatus.pack(expand='True', anchor=SE)
    #print(dir(labelStatus))
    #labelStatus.pack(status_bar, expand='True', anchor='se')


    #Gather all the settings into a single element and make it globally available.
    global imageConfig
    imageConfig = return_image_config()
    
    #This will be the list of images. Next make this a class and add methods.
    global image_list

    #This is what I'll monitor to evaluate if the scan is done. Ugly? Sure. Sorry.
    global work_happening
    work_happening = False

    root.mainloop()

## Reminders:
## a variable with StringVar() can use .set("text") and .get() to retrieve its contents
## a variable with Button() can use .config(state=DISABLED) or .config(state=NORMAL) 
