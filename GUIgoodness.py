import os #to manage files
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
from tkinter import * #to build the GUI
#import tkinter as tk
#from time import sleep # for update_idletasks
import scan_n_plan #to scan the folder, werkwerkwerk
import logging #to log errors
#logging.WARNING for least info
#logging.INFO for next amount
#logging.DEBUG for verbose
logging.basicConfig(level=logging.DEBUG)

def analyse_folder_of_files():
	pass

def close_window():
    root.destroy()
    exit()

def select_folder():
        selected_directory.set(filedialog.askdirectory())
        if selected_directory.get() != '':
                enable_button(buttonProcessImages, True)
                update_label(labelInstructions,"Click Process Images button to change your images.")
        else:
                enable_button(buttonProcessImages, False)
                update_label(labelInstructions,"No folder was selected.")
        logging.info(selected_directory.get())

def enable_button(button, t):
        global buttonProcessImages
        logging.debug("Button passed is the Process Images button: " + str(buttonProcessImages == button))
        #If True enable, otherwise disable the button.
        if t:
                button.config(state=NORMAL)
                logging.debug("Button enabled", type(button)) #I'd like the button to name itself, but anyway.
        else:
                button.config(state=DISABLED)
                logging.debug("Button disabled")

def update_label(label, message): #name the label, and give the message
        label.config(text=message)
        # Labels are labelInstructions, labelPath, labelStatusMessage

def scan():
        try:
                statusMessage.set("Getting list of files...")
                #global list_of_images  ##not sure if this needs to be global. Trying to avoid that.
                list_of_images = scan_n_plan.find_files(selected_directory.get())
                update_label(labelInstructions,"Looking at the files...")
                scan_n_plan.check_image_dims(list_of_images)
                logging.debug(selected_directory.get())
                
        except:
                #hide the process button
                #change the message back to select a folder
                pass




def App():
        #The GUI has been launched.
        logging.info("GUI launched.")
        
        #The app window
        root = Tk()
        root.title("picResizer by misterashley")
        root.configure(background="white")
        root.geometry('500x400')

        # The main part of the window
        main = Frame(root, bg='white')
        main.pack(side = 'top', expand = True, fill = 'both')

        # Build a label: A footer status bar
        footer = Frame(root, bg='black', relief='sunken')
        footer.pack(side = 'bottom', expand = True, fill = 'x', anchor='s')

        #Build a label: The instructions
        instructions ="""Instructions: \n1. Choose a folder of images to modify. \n2. Choose your options. \n3. Click Process Images. \nWARNING: This will overwrite your images!!!"""
        labelInstructions = Label(main, text=instructions, justify='left', bg="white", fg="black", font=("Helvetica",10))
        labelInstructions.pack(padx=10, anchor='w')

        #Build the choose a folder button. This direction is meant to have images. We'll scan subdirectories as well.
        buttonChoose = Button(main, text ="Select a folder to scan", width=20, command=lambda: select_folder(d))
        buttonChoose.pack(pady=10)

        #Initialize selected_directory
        selected_directory = StringVar()

        #Build a label: This is the working directory to process
        labelPath = Label (main, textvariable = selected_directory, bg ="white", fg="blue", font=("monospace", 10))
        labelPath.pack()
        
        #Build a checkbox: Resize the images
        resizeImg = IntVar()
        resizeImgBox = Checkbutton(main, text="Resize images", variable=resizeImg)
        resizeImgBox.pack(padx=10, anchor='w')

        #Build an entry box: Max Dimension for Height
        maxHeight = Entry(main, width = 10)
        maxHeight.pack(padx=10, pady=10, anchor='w')
        maxHeight.insert(0, "1000")
        #maxHeight.get() will give you the text supplied in the entry box.

        #Build an entry box: Max Width Dimension 
        ##maxWidth = Entry(main, width = 10)
        ##maxWidth.pack(padx=10, anchor='w')
        ##maxWidth.insert(0, "1000")

        #Build a checkbox: Stretch image to at least minimum size 
        stretchToMin = IntVar()
        stretchToMinBox = Checkbutton(main, text="Stretch images to minimum size", variable=stretchToMin)
        stretchToMinBox.pack(padx=10, anchor='w')

        #Build a checkbox: Add canvas to reshape image dimensions
        addCanvas = IntVar()
        addCanvasBox = Checkbutton(main, text="Add a white canvas to images", variable=addCanvas)
        addCanvasBox.pack(padx=10, anchor='w')

        #Build a checkbox: Strip EXIF from JPEG or PNG
        stripExif = IntVar()
        stripExifBox = Checkbutton(main, text="Strip EXIF info from images", variable=stripExif)
        stripExifBox.pack(padx=10, anchor='w')

        #List drop down (rather than Checkbox) for reporting (debugging)

        #Build a button: Process Images
        global buttonProcessImages
        buttonProcessImages = Button(main, text = "Process Images", width=20, command=scan, state=NORMAL)
        buttonProcessImages.pack(anchor='e', pady=20, padx=20)
        #turn off the Process Images buton.
        buttonProcessImages.config(state=DISABLED)
        enable_button(buttonProcessImages,False)

        #Build a label: Status message
        labelStatusMessage = Label (footer, text = "Ready", fg='green', bg='black', padx='10', font=("monospace",13)).pack(expand='True', anchor='se')

        root.mainloop()


if __name__ == "__main__":
        App()
