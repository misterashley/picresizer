import os
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
#from tkinter import *
import tkinter as tk
#from time import sleep # for update_idletasks
import scan_n_plan, werkwerkwerk
import logging
#logging.WARNING for least info
#logging.INFO for next amount
#logging.DEBUG for verbose
logging.basicConfig(level=logging.WARNING)
logging.info("GUI started")

def analyse_folder_of_files():
	pass

def close_window():
    root.destroy()
    exit()

def select_folder():
        selected_directory.set(filedialog.askdirectory())
        if selected_directory.get() != '':
                enableButton(buttonProcessImages, True)
                updateLabel(labelInstructions,"Click Process Images button to change your images.")
        else:
                enableButton(buttonProcessImages, False)
                updateLabel(labelInstructions,"No folder was selected.")
        logging.info(selected_directory.get())

def enableButton(button, t):
        #If True enable, otherwise disable the button.
        if t:
                button.config(state='normal')
                logging.debug("Button enabled")#, button) #I'd like the button to name itself, but anyway.
        else:
                button.config(state='disabled')
                logging.debug("Button disabled")

def updateLabel(label, message): #name the label, and give the message
        label.config(text=message)
        # Labels are labelInstructions, labelPath, labelStatusMessage

def scan():
        try:
                statusMessage.set("Getting list of files...")
                #global list_of_images  ##not sure if this needs to be global. Trying to avoid that.
                list_of_images = scan_n_plan.find_files(selected_directory.get())
                updateLabel(labelInstructions,"Looking at the files...")
                scan_n_plan.check_image_dims(list_of_images)
                logging.debug(selected_directory.get())
                
        except:
                #hide the process button
                #change the message back to select a folder
                pass



#The app window
root = tk.Tk()
root.title("picResizer by misterashley")
root.configure(background="white")
root.geometry('500x400')

# The main part of the window
main = tk.Frame(root, bg='white')
main.pack(side = 'top', expand = True, fill = 'both')

# A footer element
footer = tk.Frame(root, bg='black', relief='sunken')
footer.pack(side = 'bottom', expand = True, fill = 'x', anchor='s')


#Build the Instructions label
instructions ="""Instructions: \n1. Choose a folder of images to modify. \n2. Choose your options. \n3. Click Process Images. \nWARNING: This will overwrite your images!!!"""
labelInstructions = tk.Label (main, text=instructions, justify='left', bg="white", fg="black", font=("Helvetica",10)).pack(padx=10, anchor='w')

#Build the choose a folder button. This direction is meant to have images. We'll scan subdirectories as well.
buttonChoose = tk.Button (main, text ="Select a folder to scan", width=20, command=select_folder).pack(pady=10,)

#Initialize selected_directory
selected_directory = tk.StringVar()

#Build the 'directory to process' label
labelPath = tk.Label (main, textvariable = selected_directory, bg ="white", fg="blue", font=("monospace", 10)).pack()

#Build the Resize Images checkbox
resizeImg = tk.IntVar()
resizeImgBox = tk.Checkbutton(main, text="Resize images", variable=resizeImg).pack(padx=10, anchor='w')

#Max dimension height

#Max dimension width

#Build a force image to minimum size
stretchToMin = tk.IntVar()
stretchToMinBox = tk.Checkbutton(main, text="Stretch images to minimum size", variable=stretchToMin).pack(padx=10, anchor='w')

#Build the Add Canvas checkbox
addCanvas = tk.IntVar()
addCanvasBox = tk.Checkbutton(main, text="Add a white canvas to images", variable=addCanvas).pack(padx=10, anchor='w')

#Build the Strip EXIF checkbox
stripExif = tk.IntVar()
stripExifBox = tk.Checkbutton(main, text="Strip EXIF info from images", variable=stripExif).pack(padx=10, anchor='w')

#Checkbox for reporting (debugging)

#Build the Process Images button
buttonProcessImages = tk.Button (main, text = "Process Images", width=20, command=scan, state='disabled').pack(anchor='e', pady=20, padx=20)

#Build the status message
labelStatusMessage = tk.Label (footer, text = "Ready", fg='green', bg='black', padx='10', font=("monospace",13)).pack(expand='True', anchor='se')

root.mainloop()
