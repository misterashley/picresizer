#Windows file source
import os, sys, subprocess
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # this is to hide the command line

bksource =r"C:\Users\mrashley\Documents\temp\Wholesale Charms, Silver Charms, Pendants and Jewelry Findings _ Nina Designs_files\jpg - Copy" #the r is for 'raw' allowing \ 
source = bksource.replace('\\','/')
if source[-1] != '/': source = source + '/'

def chromaSampling(source):
    for filename in source:
        argument = str("convert " + filename + '" -sampling-factor 4:2:0 "' + ' filename'+'"')
        subprocess.call(argument, startupinfo=si, shell=True)

if __name__ == "__main__":
    chromaSampling(source)
