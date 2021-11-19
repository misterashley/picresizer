import os #to manage files
import threading #to let us do multiple things at once
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
from tkinter import * #to build the GUI
from time import sleep # to allow small delays
#import tkinter as tk
#from time import sleep # for update_idletasks
import scan_n_plan, werkwerkwerk
import logging #to log errors
#logging.WARNING for least info
#logging.INFO for next amount
#logging.DEBUG for verbose
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

#global image_list


def close_window():
    root.destroy()
    logging.info("GUI stopped")
    exit()

def select_folder():
        logging.info("select_folder function started")
        global selected_directory
        global buttonProcessImages
        #global labelInstructions
        #global labelStatus
        selected_directory.set(filedialog.askdirectory())
        if selected_directory.get() != '':
            #labelStatus.config(text="Working")
            #global image_list
            logging.info("We got this folder " + str(selected_directory.get()))
            get_list_of_files_from_directory(selected_directory.get())
            
            #turn on the process image button
            #buttonProcessImages.config(state=NORMAL)

            #update Instructions
            #status.set("Click Process Images button to change your images.")
            #labelStatus.config(text ="Ready")
                        
        else:
            #turn off the process image button
            buttonProcessImages.config(state=DISABLED)
        logging.info(selected_directory.get())
        logging.info("select_folder function ended")

def get_list_of_files_from_directory(directory):
    logging.info("get_list_of_images_from_directory function started")
    global status
    status.set("Looking at the files...")
    list_of_files = scan_n_plan.find_files(selected_directory.get())
    status.set("Found " + str(len(list_of_files)) + " files.")

    logging.info("Now we'll scan the files to find out which are images.")
    logging.debug(str(list_of_files))
    scan_files_for_images_and_update_ui(list_of_files)
    #This scan happens in a thread, and the status is updated until it's done.
    #logging.debug("Here is a list of the images: " + (str(list_of_images)))
    
                
##    except:
##        #hide the process button
##        #change the message back to select a folder
##        status.set("Something unexpected happened!!")
    logging.info("get_list_of_images_from_directory function ended")

def turn_off_button_during_work():
    logging.info("turn_off_button_during_work function started")
    buttonProcessImages.config(state=DISABLED)
    sleep(0.1)
    #global work_happening
    work_happening = True
    print ("Work is happening? : " + str(work_happening))
    while work_happening:
        pass
    buttonProcessImages.config(state=NORMAL)
    logging.info("turn_off_button_during_work function ended")

def scan_files_for_images_and_update_ui(files):
    logging.info("scan_files_for_images_and_update_ui function started")
    logging.info("The var was sent with " + str(len(files)) + " entries.")

    #disable process images button
    user_interface = threading.Thread(target=turn_off_button_during_work)

    #the work of checking which files are images
    work = threading.Thread(target=lambda: scan_n_plan.create_list_of_images_from_file_list(files))

    #start both threads
    user_interface.start()
    work.start()
    logging.info("scan_files_for_images_and_update_ui function ended")

def process_images_and_update_ui():
    logging.info("process_images_and_update_ui function started")
    global image_list
    logging.info("The var was sent with " + str(len(image_list)) + "entries.")
    user_interface = threading.Thread(target=turn_off_button_during_work)
    work = threading.Thread(target=lambda: werkwerkwerk.process_images(image_list))
    user_interface.start()
    work.start()
    logging.info("process_images_and_update_ui function ended")

##def process_queue_of_images():
##        global image_list
##        #global root
##        #print(len(image_list))
##        logging.info("Images to process:" + str(len(image_list)))
##        global labelStatus
##        i = 0
##        for image in image_list:
##                try:
##                        #get an image from the list of images
##                        image = image_list.pop()
##                        #logging.info(image)
##
##                        #process that image file
##                        werkwerkwerk.process_image(image)
##
##                        #update counter. Every 10 images updates status bar.
##                        i = i + 1
##                        
##                        #update status bar every 10 images
##                        if i%10 == 0 : 
##                                labelStatus.config(text="Images processed: " + str(i))
##                                #let the window update
##                                root.updated_idletasks()
##                                
##                except:
##                        logging.info("An error during processing image queue.")
##                        #cannot pop a file from the list. This means we're done the whole list
##        logging.info("Finished processing image files.")
##
##        #Let us know we're done the process.
##        labelText.set("Processed " + str(i) + " images.")
##        global buttonProcessImages
##        buttonProcessImages.config(state=DISABLED)        

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
        buttonChoose = Button(main, text ="Select a folder to scan", width=20, command=select_folder)
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

        global image_list
        image_list = []
        #global work_happening
        #work_happening = False
        
        root.mainloop()
