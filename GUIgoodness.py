import os
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
#from tkinter import *
import tkinter as tk
from time import sleep # for update_idletasks
import scan_n_plan #werkwerkwerk

def analyse_folder_of_files():
	pass

def close_window():
    window.destroy()
    exit()

def browse_button():
        selected_directory.set(filedialog.askdirectory())
##trying to get the label to update.
        window.update_idletasks()
        #global files_to_check
        files_to_check = scan_n_plan.find_files(selected_directory.get())
        image_files = []
        #print(type(files_to_check))
        #print(len(files_to_check))
        while len(files_to_check) > 0:
                statusMessage.set("Looking at "+ str(len(files_to_check))+" files...")
                #print(files_to_check)
                #image_files = scan_n_plan.pop_and_check(files_to_check)
                #scan_n_plan.check_image_dims(list_of_images)
                files_to_check, image_files = scan_n_plan.create_list_of_images_from_file_list(files_to_check, image_files)
                statusMessage.set(str(len(image_files)) + " images found. " + str(len(files_to_check)) + " files remaining.")
                window.update_idletasks()
        statusMessage.set(str(len(image_files)) + " image(s) found.")

def scan():
        if selected_directory.get() == '':
                statusMessage.set("Please select a folder first.")
                return

window = tk.Tk()
window.title("picResizer")
window.configure(background="yellow")

global selected_directory
selected_directory = tk.StringVar()
#selected_directory.set(os.getcwd())
#selected_directory.set("Choose a folder to scan.")
#print(selected_directory.get())
global statusMessage
statusMessage = tk.StringVar()
#statusMessage.set("...")
#selected_folder = selected_directory.get()

### get the path
label1 = tk.Label (window, text = "Find the file folder of images to convert.", bg="white", fg="black", font="none 12")
label1.pack(pady=10,padx=30)
#label1.grid(row=1, column=0, sticky=W)

## Selected directory
labelPath = tk.Label (window, textvariable = selected_directory, bg ="white", fg="blue", font="none 10")
#label2 = Label (window, text = "Current folder: \n" + selected_directory.get(), bg ="white", fg="black", font="none 12")
labelPath.pack(pady=10, padx=5)
#label2.grid(row=2, column=0, sticky=W)

### Choose one more folders or files
buttonChoose = tk.Button (window, text ="Choose a folder", width=20, command=browse_button)
buttonChoose.pack(pady=10)
#button1.grid(row=3, column=0, sticky=W)

#Checkbox for Resize

#Max dimension height

#Max dimension width

#Checkbox for force to hero size

#Checkbox for canvas addition

#Checkbox for strip EXIF tag

#Checkbox for reporting (debugging)

### run the main loop
buttonRun = tk.Button (window, text = "Process images", width=20, command=scan)
buttonRun.pack(pady=15)

labelStatusMessage = tk.Label (window, textvariable = statusMessage, bg ="white", fg="black", font="none 12")
#label2 = Label (window, text = "Current folder: \n" + selected_directory.get(), bg ="white", fg="black", font="none 12")
labelStatusMessage.pack(pady=10, padx=5)


window.mainloop()
