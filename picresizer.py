import os
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
from tkinter import *
from time import sleep # for update_idletasks

def analyse_folder_of_files():
	pass


def close_window():
    window.destroy()
    exit()

def browse_button():
        selected_directory.set(filedialog.askdirectory())
##trying to get the label to update.
        window.update_idletasks()
##        sleep(1)
##        print(selected_directory.get())
	
#### main:
window = Tk()
window.title("picResizer")
window.configure(background="white")

global selected_directory
selected_directory = StringVar(window)
selected_directory.set(os.getcwd())
print(selected_directory.get())


### get the path
label1 = Label (window, text = "Paste the path of files to process", bg="white", fg="black", font="none 12")
label1.pack(pady=10)
#label1.grid(row=1, column=0, sticky=W)

## Selected directory
label2 = Label (window, textvariable = selected_directory, bg ="white", fg="black", font="none 12")
#label2 = Label (window, text = "Current folder: \n" + selected_directory.get(), bg ="white", fg="black", font="none 12")
label2.pack(pady=10, padx=5)
#label2.grid(row=2, column=0, sticky=W)

### start the process
button1 = Button (window, text ="Choose a folder", width=20, command=browse_button)
button1.pack(pady=10)
#button1.grid(row=3, column=0, sticky=W)

#Checkbox for Resize

#Max dimension height

#Max dimension width

#Checkbox for force to hero size

#Checkbox for canvas addition

#Checkbox for strip EXIF tag

#Checkbox for reporting (debugging)

### run the main loop
window.mainloop()
