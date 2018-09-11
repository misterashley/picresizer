import os
from tkinter import filedialog # For browsing to the directory with tkinter directory chooser
from tkinter import *
from time import sleep # for update_idletasks
import scan_n_plan

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

def scan(selected_directory):
        doing = "doing it!"

#### main:
window = Tk()
window.title("picResizer")
window.configure(background="white")

global selected_directory
selected_directory = StringVar(window)
selected_directory.set(os.getcwd())
print(selected_directory.get())
doing = ''
#selected_folder = selected_directory.get()

### get the path
label1 = Label (window, text = "Paste the path of files to process", bg="white", fg="black", font="none 12")
label1.pack(pady=10)
#label1.grid(row=1, column=0, sticky=W)

## Selected directory
labelPath = Label (window, textvariable = selected_directory, bg ="white", fg="black", font="none 12")
#label2 = Label (window, text = "Current folder: \n" + selected_directory.get(), bg ="white", fg="black", font="none 12")
labelPath.pack(pady=10, padx=5)
#label2.grid(row=2, column=0, sticky=W)

### Choose one more folders or files
buttonChoose = Button (window, text ="Choose a folder", width=20, command=browse_button)
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
buttonRun = Button (window, text = "Zhu Li, do the thing!", width=20, command=scan(selected_directory))
buttonRun.pack(pady=15)

labelDoing = Label (window, textvariable = doing, bg ="white", fg="black", font="none 12")
#label2 = Label (window, text = "Current folder: \n" + selected_directory.get(), bg ="white", fg="black", font="none 12")
labelDoing.pack(pady=10, padx=5)


window.mainloop()
