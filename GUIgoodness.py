from pathlib import Path
import threading #to let us do multiple things at once
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
from tkinter import ttk #for the Combobox used in debugging selection
from tkinter import * #to build the GUI
from time import sleep # to allow small delays
#import tkinter as tk
#from time import sleep # for update_idletasks
import werkwerkwerk
import logging #to log errors

#logging.WARNING for least info
#logging.INFO for next amount
#logging.DEBUG for verbose
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

#PIL to read images (to get their dimensions)
from PIL import Image

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
        global selected_directory #This is the directory we'll read
        global buttonProcessImages #buttonProcessImages.config(state=DISABLED/NORMAL)
        global status #status bar text status.set("text")

        #get a working directory from filedialog
        selected_directory.set(filedialog.askdirectory())

        if selected_directory.get() != '': #this is more for the 2nd time we select a folder
            logging.info("We got this folder " + str(selected_directory.get()))

#####STEP ONE#####
            status.set(F"Finding files in {selected_directory.get()}. This may take a moment.")

            #Let the UI update.
            root.update_idletasks()
            
            #Get a list of files.
            file_list = return_file_list_from_directory(selected_directory.get().replace('/','\\'))

#####STEP TWO#####
            #build out images_list with imagges & dimensions from the files
            scan = threading.Thread(target=get_image_list_from_file_list(file_list))
            scan.start()

            #start updating UI with percentage done of file scan. 
            #Unless we can offload this to the function?
            
        else:
            #turn off the process image button
            buttonProcessImages.config(state=DISABLED)
        logging.info(selected_directory.get())
        logging.info("scan_folder function ended")

def return_file_list_from_directory(folder):
    ##STEP ONE of scan
    logging.info("find_files function started")
    found_files = []
    dir_counter = 0
    p = Path(folder)
    #Could set up a flag to use glob for non-recursive searches with p.glob("*")
    for file in p.rglob("*"):
        if file.is_file():
            found_files.append(file)
            logging.debug(F"Found file: {file}")
        if file.is_dir():
            dir_counter += 1
    logging.info(F"file_files found {len(found_files)} files in {dir_counter} folder(s).")
    logging.info("find_files function started ended")
    return found_files

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
            logging.debug(F"Found an image: {this_image}")
        except:
            logging.debug(F"Not an image: {file}")
        if i % 50 == 0:
            status.set(F"Found {len(image_list)} images from {len(files_to_scan)} files.")
            root.update_idletasks()
        img.close()

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
    #global work_happening I don't think this does what I want it to do
    logging.info("turn_off_button_during_work function started")
    buttonProcessImages.config(state=DISABLED)
    sleep(0.5)# a little pause to help multithreading be cool.
    work_happening = True
    while werkwerkwerk.work_happening:
        sleep(1)
        print(".", end=''),
        #print(werkwerkwerk.work_happening)
        status.set(werkwerkwerk.status_update_text)
        root.update_idletasks()
        pass
    status.set("Finished. " + str(werkwerkwerk.status_update_text))
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
    work = threading.Thread(target=lambda: werkwerkwerk.process_images(imageConfig, image_list))
    user_interface.start()
    work.start()
    logging.info("process_images_and_update_ui function ended")

def return_image_config():
    logging.info("return_image_config function started")
    settings = {
                "resizeMax":int(resizeMax.get()),#making these int to easy the comparisons for werkwerkwerk
                "maxWidth":int(maxWidth.get()),
                "maxHeight":int(maxHeight.get()),
                "maxDimension":int(max(maxWidth.get(), maxHeight.get())),
                
                "resizeMin":int(resizeMin.get()),
                "minWidth":int(minWidth.get()),
                "minHeight":int(minHeight.get()),
                "minDimension":int(min(minWidth.get(),minHeight.get())),
                
                "addCanvas":addCanvas.get(),
                "stripExif":stripExif.get(),
                "imageCompression":imageCompressionPercent.get(),
                "convertJPG":convertJPG.get(),
                "delOriginalFile":delOriginalFile.get(),
                "keepPNGFile":keepPNGFile.get(),
                "debuggingMenu":debuggingMenu.get(),
                }
    logging.info(F"The settings are: {settings}")
    logging.info("return_image_config function ended")
    return settings


## Reminders:
## a variable with StringVar() can use .set("text") and .get() to retrieve its contents
## a variable with Button() can use .config(state=DISABLED) or .config(state=NORMAL) 


'''

scan_n_plan comments

 scanNplan is part of version 2 of picresizer
 https://github.com/misterashley/picresizer

 Get a file selection (currently from config file, later from GUI)

 Get set of option to use, set these globally

 Pass the above to scanNplan, and build a VFO
    (a list of verified files, with the options to work on)

 File selector
   X Choose a folder
       - Option to delve into subfolders

 Options (captured into a list called settings)
   X Resize images
   X Maximum desired output image dimension (Desired ratio is a function of max output)
   X Minimum desired output image dimensions
   X Canvas enabled
   - Canvas colour ? (Hex value, colour wheel perhaps)
   - Compression enabled / percent
   X Strip EXIF data to shrink filesize
   - Convert to .JPG
       - Delete original image upon successful conversion
   - Preserve .PNG images in that format
   - Debug to console
'''


if __name__ == "__main__":
    #The GUI has been launched.
    logging.info("GUI launched.")

    #The app window
    global root
    root = Tk()
    root.title("picResizer by misterashley")
    root.configure(background="white")
    root.geometry('800x600')

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
    resizeMax.set(1) #enable by default
    resizeImageBox = Checkbutton(main, text="Shrink images to maximum", variable=resizeMax)
    resizeImageBox.grid(row=3, column=0, rowspan=2)#.pack(padx=10, anchor='w')

    maxHeightLabel = Label(main, text="Max Height")
    maxHeightLabel.grid(row=3, column=1)

    #Build an entry box: Max Dimension for Height
    maxHeight = Entry(main, width=10)
    maxHeight.grid(row=4, column=1)#.pack(padx=10, pady=10, anchor='w')
    maxHeight.insert(0, 1000)
    #maxHeight.get() will give you the text supplied in the entry box... it will not Entry is unique apparent. How fucking stupid.

    maxWidthLabel = Label(main, text="Max Width")
    maxWidthLabel.grid(row=3, column=2)

    #Build an entry box: Max Dimension for Width
    maxWidth = Entry(main, width=10, text="Maximum width of images" )
    maxWidth.grid(row=4, column=2)#.pack(padx=10, pady=10, anchor='w')
    maxWidth.insert(0, 1000)
    #maxHeight.get() will give you the text supplied in the entry box.

    ########################################
    #  Minimum dimensions.                 #
    ########################################
    #Build a checkbox: Stretch image to at least minimum size
    resizeMin = IntVar()
    resizeMin.set(1) #enable by default
    resizeImageBox = Checkbutton(main, text="Stretch images to minimum", variable=resizeMin)
    resizeImageBox.grid(row=5, column=0, rowspan=2)#.pack(padx=10, anchor='w')

    minHeightLabel = Label(main, text="Min Height")
    minHeightLabel.grid(row=5, column=1)

    #Build an entry box: Min Dimension for Height
    minHeight = Entry(main, width=10)
    minHeight.grid(row=6, column=1)#.pack(padx=10, pady=10, anchor='w')
    minHeight.insert(0,400)
    #minHeight.get() will give you the text supplied in the entry box... it will not Entry is unique apparent. How fucking stupid.

    minWidthLabel = Label(main, text="Min Width")
    minWidthLabel.grid(row=5, column=2)

    #Build an entry box: Minimum Dimension for Width
    minWidth = Entry(main, width=10)
    minWidth.grid(row=6, column=2)#.pack(padx=10, pady=10, anchor='w')
    minWidth.insert(0, 400)
    #minWidth.get() will give you the text supplied in the entry box.

    ########################################
    #  Other options.                      #
    ########################################

    #Build a checkbox: Convert images to .JPG
    convertJPG = IntVar() #0 for unchecked, 1 for checked.
    convertJPG.set(1) #enable by default
    convertJPGBox = Checkbutton(main, text="Convert images to .JPG", variable=convertJPG)
    convertJPGBox.grid(row=9, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    imageCompression = IntVar() # 0-100 percentage.
    imageCompression.set(1)
    imageCompressionBox = Checkbutton(main, text="Compress images", variable=imageCompression)
    imageCompressionBox.grid(row=10, column=0, rowspan=2, sticky=W, padx=5)

    imageCompressionLabel = Label(main, text="%100 is highest quality, \n but least compression \n (0 to 100)")
    imageCompressionLabel.grid(row=10, column=1, columnspan=2)

    imageCompressionPercent = Entry(main, width=5)
    imageCompressionPercent.insert(0,100)
    imageCompressionPercent.grid(row=11, column=1)

    #Build a checkbox: Add canvas to reshape image dimensions
    addCanvas = IntVar() #0 for unchecked, 1 for checked.
    addCanvas.set(1) #enable by default
    addCanvasBox = Checkbutton(main, text="Add a white canvas to images", variable=addCanvas)
    addCanvasBox.grid(row=12, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    #Build a checkbox: Strip EXIF from JPEG or PNG
    stripExif = IntVar()
    stripExif.set(1) #enable by default
    stripExifBox = Checkbutton(main, text="Strip EXIF info from images", variable=stripExif)
    stripExifBox.grid(row=13, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    #Build a checkbox: Delete original file if conversion is successful
    delOriginalFile = IntVar() #0 for unchecked, 1 for checked.
    delOriginalFile.set(1) #enable by default
    delOriginalFileBox = Checkbutton(main, text="Delete original file if conversion is successful", variable=delOriginalFile)
    delOriginalFileBox.grid(row=14, column=0, sticky=W, padx=5)#.pack(padx=10, anchor='w')

    #Build a checkbox: Preserve PNG files
    keepPNGFile = IntVar() #0 for unchecked, 1 for checked.
    keepPNGFile.set(0) #enable by default
    keepPNGFileBox = Checkbutton(main, text="But, don't delete if the file is a .PNG", variable=keepPNGFile)
    keepPNGFileBox.grid(row=15, column=0, sticky=W, padx=30)#.pack(padx=10, anchor='w')


    debuggingLabel = Label(main, 
        text="""Debugging log file.
        Set to WARNING for least info.
        Set to DEBUG for most info.
        {}""".format("some text"), anchor=W)
    debuggingLabel.grid(row=16, column=0, padx=5, pady=20,sticky=W)

    #List drop down (rather than Checkbox) for reporting (debugging)
    debuggingLevel = ["WARNING","INFO","DEBUG"]
    debuggingMenu = ttk.Combobox(main, value=debuggingLevel)#
    debuggingMenu.current(0) #WARNING by default
    debuggingMenu['state'] = 'readonly' #Don't allow other options to be entered
    debuggingMenu.grid(row=16, column=1)

    ########################################
    #  Modify image files button.          #
    ########################################

    global buttonProcessImages
    buttonProcessImages = Button(main, text="No images selected", 
        width=20, command=process_images_and_update_ui, state=DISABLED)
    buttonProcessImages.grid(row=20, column=0, sticky=E, padx=60, pady=20)#.pack(anchor='e', pady=20, padx=20)
    #turn off the Process Images buton.

    ########################################
    #  Status bar.                         #
    ########################################

    #Build a label: Status message
    global status
    status = StringVar()
    status.set("Ready")
    #global labelStatus
    labelStatus = Label(status_bar, textvariable=status, 
        fg='green', bg='black', padx='10', font=("monospace",13))
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
