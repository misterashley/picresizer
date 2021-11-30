import os #to manage files
import threading #to let us do multiple things at once
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
from tkinter import * #to build the GUI
from time import sleep # to allow small delays
#import tkinter as tk
#from time import sleep # for update_idletasks
import werkwerkwerk
import logging #to log errors

#logging.WARNING for least info
#logging.INFO for next amount
#logging.DEBUG for verbose
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

#PIL to read images (to get their dimensions)
from PIL import Image

'''

scan_n_plan comments

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
'''

def close_window():
    root.destroy()
    logging.info("GUI stopped")
    exit()

'''
scan_button runs scan_folder()
scan_folder asks user for folder
scan_folder gets file_list from folder
scan_folder resets image_list
scan_folder spins up thread_find_images with file_list
    thread_find_images searches files_list for images found, populates global image_list
    thread_find_images updates statusbar as it goes
    thread_find_images reports when it is done

process_button runs process_images()
process_images spins up thread update_image_files with image_list and settings
    update_image_files starts modifying images in image_list using settings
    update_image_files updates statsubar as it goes
    update_image_files reports when it is done
'''
def scan_folder(): 
        logging.info("scan_folder function started")
        global selected_directory
        global buttonProcessImages #buttonProcessImages.config(state=DISABLED/NORMAL)
        global status #status bar text status.set("text")

        selected_directory.set(filedialog.askdirectory())
        if selected_directory.get() != '': #this is more for the 2nd time we select a folder
            logging.info("We got this folder " + str(selected_directory.get()))

#####STEP ONE#####
##            status.set("Finding files in " + str(selected_directory.get()))
            root.update_idletasks() #show the status update
            
            #get a list of files
            file_list = return_file_list_from_directory(selected_directory.get())

#####STEP TWO#####
            #build out images_list with imagges & dimensions from the files
            threading_scan_images(file_list)

            #start updating UI with percentage done of file scan. Unless we can offload this to the function?
            
        else:
            #turn off the process image button
            buttonProcessImages.config(state=DISABLED)
        logging.info(selected_directory.get())
        logging.info("scan_folder function ended")

def return_file_list_from_directory(folder):
    ##STEP ONE of scan
    logging.info("find_files function started")
    found_files = []
    
    for root, dirs, files in os.walk(folder, topdown = False):
        for file in files:
            found_files.append(os.path.join(root, file))
            logging.debug("Found: " + str(os.path.join(root, file)))
    logging.info("file_files found " + str(len(found_files)) + " files.")
    logging.info("find_files function started ended")
    return found_files

def threading_scan_images(files):
    #STEP TWO of scan
    logging.info("threading_scan_images function started")
    logging.info("The var was sent with " + str(len(files)) + " entries.")

    #the work of checking which files are images
    scan = threading.Thread(target=get_image_list_from_file_list(files))

    #start both threads
    #user_interface.start()
    scan.start()
    logging.info("threading_scan_images function ended. Thread is still running.")

# Check if a file is an image. If so, store the file path & image dimensions.
def get_image_list_from_file_list(files_to_scan):
    logging.info("scan_files_for_images_and_update_ui function started")
    logging.debug(files_to_scan)

    global status
    
    
    # Check if there are any files, if none stop.
    if len(files_to_scan) == 0 :
        status.set("There were no files to scan.")
        logging.info("There were no files to scan.")
    
    #refer to the image_list and clear it out
    global image_list
    image_list = []

    for file in files_to_scan:
        i =+ 1
        this_image = []
        #this_image = (validate_image_dimensions(file))
        try:
            img = Image.open(file)
            width, height = img.size
            this_image.append(file)
            this_image.append(width)
            this_image.append(height)
            image_list.append(this_image)
            logging.debug("Found an image: " + str(this_image))
        except:
            logging.debug("Not an image: " + str(file))
        if i % 50 == 0:
            status.set("Found " + str(len(image_list)) + " images from " + str(len(files_to_scan)) + " files.")
            root.update_idletasks()

    #prepare to update the Process Images button
    global buttonProcessImages
    
    if image_list == 0:
        status.set("No images found.")
        buttonProcessImages.config(state=DISABLED)
        root.update_idletasks()

    elif len(image_list) > 0:
        status.set("Found " + str(len(image_list)) + " images from " + str(len(files_to_scan)) + " files.")
        buttonProcessImages.config(state=NORMAL)
        root.update_idletasks()
    
    logging.info("Found " + str(len(image_list)) + " images from " + str(len(files_to_scan)) + " files.")
    logging.info("get_image_list_from_file_list function ended")

def turn_off_button_during_work():
    #global work_happening I don't think this does what I want it to do
    logging.info("turn_off_button_during_work function started")
    buttonProcessImages.config(state=DISABLED)
    sleep(0.5)# a little pause to help multithreading be cool.
    work_happening = True
    while werkwerkwerk.work_happening:
        sleep(1)
        print(".")
        print(werkwerkwerk.work_happening)
        pass
    buttonProcessImages.config(state=NORMAL)
    logging.info("turn_off_button_during_work function ended")

def process_images_and_update_ui():
    logging.info("process_images_and_update_ui function started")
    logging.info("The var was sent with " + str(len(image_list)) + "entries.")
    user_interface = threading.Thread(target=turn_off_button_during_work)
    work = threading.Thread(target=lambda: werkwerkwerk.process_images(image_list))
    user_interface.start()
    work.start()
    logging.info("process_images_and_update_ui function ended")

def App(): pass
## Reminders:
## a variable with StringVar() can use .set("text") and .get() to retrieve its contents
## a variable with Button() can use .config(state=DISABLED) or .config(state=NORMAL) 

if __name__ == "__main__":
        #The GUI has been launched.
        logging.info("GUI launched.")
        
        #The app window
        global root
        root = Tk()
        root.title("picResizer by misterashley")
        root.configure(background="white")
        root.geometry('500x500')

        # The main part of the window
        main = Frame(root, bg='white')
        main.pack(side = 'top', expand = True, fill = 'both')

        #consider a part of the screen that looks for imagemagick and reports on this
        #perhaps a list of requirements with OK in green, missing in red, and an info button if missing.
        #the info button would give instructions on where to get the missing elements.

        # Build a label: A status bar
        status_bar = Frame(root, bg='black', relief='sunken')
        status_bar.pack(side = 'bottom', expand = True, fill = 'x', anchor='s')

        #Build a label: The instructions
        global instructions
        instructions = StringVar()
        instructions.set("""Instructions: \n1. Choose a folder of images to modify. \n2. Choose your options. \n3. Click Process Images. \nWARNING: This will overwrite your images!!!""")
        #instructions ="""Instructions: \n1. Choose a folder of images to modify. \n2. Choose your options. \n3. Click Process Images. \nWARNING: This will overwrite your images!!!"""
        #global labelInstructions
        labelInstructions = Label(main, textvariable=instructions, justify='left', bg="white", fg="black", font=("Helvetica",10))
        labelInstructions.pack(padx=10, anchor='w')

        #Build the choose a folder button. This direction is meant to have images. We'll scan subdirectories as well.
        buttonChoose = Button(main, text ="Select a folder to scan", width=20, command=scan_folder)
        buttonChoose.pack(pady=10)

        #Initialize selected_directory
        global selected_directory
        selected_directory = StringVar()

        #Build a label: This is the working directory to process
        #global labelPath
        labelPath = Label (main, textvariable=selected_directory, bg="white", fg="blue", font=("monospace", 10))
        labelPath.pack()
        
        #Build a checkbox: Resize the images
        resizeImage = IntVar()
        resizeImage.set(1) #enable by default
        resizeImageBox = Checkbutton(main, text="Resize images", variable=resizeImage)
        resizeImageBox.pack(padx=10, anchor='w')

        #Build an entry box: Max Dimension for Height
        maxHeight = Entry(main, width=10, text="Maximum width of images")
        maxHeight.pack(padx=10, pady=10, anchor='w')
        #maxHeight.insert("1000")
        #maxHeight.get() will give you the text supplied in the entry box... it will not Entry is unique apparent. How fucking stupid.

        #Build an entry box: Max Dimension for Width
        maxWidth = Entry(main, width=10, text="Maximum width of images" )
        maxWidth.pack(padx=10, pady=10, anchor='w')
        maxWidth.insert(0, 1000)
        #maxHeight.get() will give you the text supplied in the entry box.

        #Build a checkbox: Stretch image to at least minimum size
        stretchToMin = IntVar()
        stretchToMinBox = Checkbutton(main, text="Stretch images to minimum size", variable=stretchToMin)
        stretchToMinBox.pack(padx=10, anchor='w')

        #Build a checkbox: Add canvas to reshape image dimensions
        addCanvas = IntVar() #0 for unchecked, 1 for checked.
        addCanvasBox = Checkbutton(main, text="Add a white canvas to images", variable=addCanvas)
        addCanvasBox.pack(padx=10, anchor='w')

        #Build a checkbox: Strip EXIF from JPEG or PNG
        stripExif = IntVar()
        stripExifBox = Checkbutton(main, text="Strip EXIF info from images", variable=stripExif)
        stripExifBox.pack(padx=10, anchor='w')

        #Gather all the settings into a single element and make it globally available.
        global imageConfig
        imageConfig = {"resizeImg":resizeImage.get(),
                       "maxHeight":maxHeight.get(),
                       "maxWidth":maxWidth.get(),
                       "stretchToMin":stretchToMin.get(),
                       "addCanvas":addCanvas.get(),
                       "stripExif":stripExif.get()
                       }
        logging.info("Image configuration: "+ str(imageConfig))

        #List drop down (rather than Checkbox) for reporting (debugging)

        #Build a button: Process Images
        global buttonProcessImages
        buttonProcessImages = Button(main, text="Process Images", width=20, command=process_images_and_update_ui, state=NORMAL)
        buttonProcessImages.pack(anchor='e', pady=20, padx=20)
        #turn off the Process Images buton.
        buttonProcessImages.config(state=DISABLED)

        #Build a label: Status message
        global status
        status = StringVar()
        status.set("Ready")
        #global labelStatus
        labelStatus = Label(status_bar, textvariable=status, fg='green', bg='black', padx='10', font=("monospace",13))
        labelStatus.pack(expand='True', anchor=SE)
        #print(dir(labelStatus))
        #labelStatus.pack(status_bar, expand='True', anchor='se')

        #This will be the list of images. Next make this a class and add methods.
        global image_list

        #This is what I'll monitor to evaluate if the scan is done. Ugly? Sure. Sorry.
        global work_happening
        work_happening = False
        
        root.mainloop()
