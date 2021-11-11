import os
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
#from tkinter import *
import tkinter as tk
#from time import sleep # for update_idletasks
import scan_n_plan, werkwerkwerk

def analyse_folder_of_files():
	pass


def close_window():
    root.destroy()
    exit()

def select_folder():
        try: buttonProcessImages.destroy()
        except: pass
        selected_directory.set(filedialog.askdirectory())
        if selected_directory.get() != '':
                buttonProcessImages = tk.Button (main, text = "Process Images", width=20, command=scan)
                buttonProcessImages.pack(pady=15)
        print(selected_directory.get())
        root.update_idletasks()
        

def updateInstructions(message):
        statusMessage.set(message)

def updateMessage(message):
        stat

def scan():
        try:
                statusMessage.set("Getting list of files...")
                #global list_of_images  ##not sure if this needs to be global. Trying to avoid that.
                list_of_images = scan_n_plan.find_files(selected_directory.get())
                statusMessage.set("Looking at the files...")
                scan_n_plan.check_image_dims(list_of_images)
                #print(selected_directory.get())
                #statusMessage.set("...")
                
        except:
                #hide the process button
                #change the message back to select a folder
                pass



#### This is the main window :
root = tk.Tk()
root.title("picResizer")
root.configure(background="white")
root.geometry('400x300')

#
##root.columnconfigure(0, weight=1) #100% of the window
##
##root.rowconfigure(0,weight=8) #80%
##root.rowconfigure(1,weight=2) #20%

main = tk.Frame(root, bg='white')
footer = tk.Frame(root, bg='white')

#Initialize global selected_directory
selected_directory = tk.StringVar()
#selected_directory.set(os.getcwd())
#selected_directory.set("Choose a folder to scan.")
#print(selected_directory.get())

#Initialize the Instructions
labelInstructions = tk.StringVar()
labelInstructions.set("")
labelInstructions = tk.Label (main, textvariable = labelInstructions, bg="white", fg="black", font="none 12")
labelInstructions.pack(pady=10)

### Choose a directory. This direction is meant to have images. We'll scan subdirectories as well.
buttonChoose = tk.Button (main, text ="Select folder", width=20, command=select_folder)
buttonChoose.pack(pady=10)

#updateInstructions("Choose a file folder of images to process")

## Selected directory
labelPath = tk.Label (main, textvariable = selected_directory, bg ="white", fg="blue", font="none 10")
#label2 = Label (window, text = "Current folder: \n" + selected_directory.get(), bg ="white", fg="black", font="none 12")
labelPath.pack(pady=10, padx=5)
#label2.grid(row=2, column=0, sticky=W)


#Checkbox for Resize

#Max dimension height

#Max dimension width

#Checkbox for force to hero size

#Checkbox for canvas addition

#Checkbox for strip EXIF tag

#Checkbox for reporting (debugging)

### run the main loop
buttonProcessImages = tk.Button (main, text = "Process Images", width=20, command=scan)
buttonProcessImages.pack(pady=15)
buttonProcessImages.destroy()
#Initialize status message
statusMessage = tk.StringVar()
statusMessage.set("Ready")
labelStatusMessage = tk.Label (footer, textvariable = statusMessage, relief='sunken', fg='green', bg='black', padx='30', font="none 13")
labelStatusMessage.pack(expand = 'True', padx='20', pady='20', anchor = 'se')

main.pack(side = 'top', expand = 'True', fill = 'both')
footer.pack(side = 'bottom', expand = True, fill = 'both')

root.mainloop()
